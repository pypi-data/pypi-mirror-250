import os
import sys

import torch
import torch.nn as nn
from stf.activations import ACT2FN
from stf.modeling_outputs import (
    BaseModelOutputWithPast,
    CausalLMOutputWithPast
)
from stf.modeling_utils import PreTrainedModel
from stf.utils import logging
from torch.nn import CrossEntropyLoss

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from yan.model.yan_configuration import YanConfig

logger = logging.get_logger(__name__)


class RMSNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        """
        RMSNorm is equivalent to T5LayerNorm
        """
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)
        variance = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
        return self.weight * hidden_states.to(input_dtype)


class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.intermediate_size = config.intermediate_size
        self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.up_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size, bias=False)
        self.act_fn = ACT2FN["silu"]

    def forward(self, x):
        return self.down_proj(self.act_fn(self.gate_proj(x)) * self.up_proj(x))


class YanPreTrainedModel(PreTrainedModel):
    config_class = YanConfig
    base_model_prefix = "model"
    supports_gradient_checkpointing = True

    def _init_weights(self, module):
        std = self.config.initializer_range
        if isinstance(module, nn.Embedding):
            module.weight.data.normal_(mean=0.0, std=std)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()

    def _set_gradient_checkpointing(self, module, value=False):
        if isinstance(module, YanBrainModel):
            module.gradient_checkpointing = value


class DecoderLayer(nn.Module):

    def __init__(self, config):
        super().__init__()
        if config.use_mlp:
            self.mlp = MLP(config=config)
            self.post_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        else:
            self.mlp = None

        self.use_residual = config.use_residual

        self.q_layer = nn.Linear(config.hidden_size, config.hidden_size)
        self.k_layer = nn.Linear(config.hidden_size, config.hidden_size)
        self.v_layer = nn.Linear(config.hidden_size, config.hidden_size)

        self.input_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.embedding_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.q_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.k_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.v_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)

    def forward(self,
                hidden_states,
                relation_embeddings,
                past_key_value=None,
                use_cache=False,
                infer=False
                ):
        if not infer:
            residual = hidden_states

            hidden_states = self.input_norm(hidden_states)

            embeddings = hidden_states * relation_embeddings
            embeddings = self.embedding_norm(embeddings)

            q_cumsum = torch.cumsum(self.q_layer(embeddings), dim=1)
            k_cumsum = torch.cumsum(self.k_layer(embeddings), dim=1)
            v_cumsum = torch.cumsum(self.v_layer(embeddings), dim=1)

            q = self.q_norm(q_cumsum)
            k = self.k_norm(k_cumsum)
            v = self.v_norm(v_cumsum)

            hidden_states = v + v * q - q * hidden_states - k * embeddings
            if self.use_residual:
                hidden_states = residual + hidden_states

            if self.mlp:
                residual = hidden_states
                hidden_states = self.post_norm(hidden_states)
                hidden_states = self.mlp(hidden_states)
                if self.use_residual:
                    hidden_states = residual + hidden_states

            outputs = (hidden_states,)
        else:
            residual = hidden_states

            hidden_states = self.input_norm(hidden_states)

            embeddings = hidden_states * relation_embeddings
            embeddings = self.embedding_norm(embeddings)

            q_cumsum = torch.cumsum(self.q_layer(embeddings), dim=1)
            k_cumsum = torch.cumsum(self.k_layer(embeddings), dim=1)
            v_cumsum = torch.cumsum(self.v_layer(embeddings), dim=1)

            if past_key_value is not None:
                (past_q_cumsum, past_k_cumsum, past_v_cumsum) = past_key_value
                q_cumsum = past_q_cumsum[:, -1, :] + q_cumsum
                k_cumsum = past_k_cumsum[:, -1, :] + k_cumsum
                v_cumsum = past_v_cumsum[:, -1, :] + v_cumsum

            q = self.q_norm(q_cumsum)
            k = self.k_norm(k_cumsum)
            v = self.v_norm(v_cumsum)

            hidden_states = v + v * q - q * hidden_states - k * embeddings
            if self.use_residual:
                hidden_states = residual + hidden_states

            if self.mlp:
                residual = hidden_states
                hidden_states = self.post_norm(hidden_states)
                hidden_states = self.mlp(hidden_states)
                if self.use_residual:
                    hidden_states = residual + hidden_states

            outputs = (hidden_states,)

            if use_cache:
                present_key_value = (q_cumsum, k_cumsum, v_cumsum)
                outputs += (present_key_value,)

        return outputs


class YanBrainModel(YanPreTrainedModel):

    def __init__(self, config: YanConfig):
        super().__init__(config)
        self.padding_idx = config.pad_token_id
        self.vocab_size = config.vocab_size
        self.infer = config.infer
        self.relation_period = config.relation_period

        self.token_embedding = nn.Embedding(
            config.vocab_size,
            config.hidden_size,
            padding_idx=self.padding_idx
        )
        self.relation_embedding = nn.Embedding(
            config.relation_period + 1,
            config.hidden_size,
            padding_idx=self.padding_idx
        )
        self.layers = nn.ModuleList([DecoderLayer(config) for _ in range(config.num_hidden_layers)])
        self.relation_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)

        self.gradient_checkpointing = False

        # Initialize weights and apply final processing
        self.post_init()

    def get_input_embeddings(self):
        return self.token_embedding

    def set_input_embeddings(self, value):
        self.token_embedding = value

    def forward(self,
                input_ids,
                position_ids,
                past_key_values=None,
                use_cache=None,
                **kwargs
                ):
        # 获取Token和Relation编码
        hidden_states = self.token_embedding(input_ids)
        if position_ids is None:
            _, seq_len, _ = hidden_states.shape
            position_ids = torch.arange(0, seq_len) % self.relation_period + 1
        relation_embeddings = self.relation_embedding(position_ids.to(hidden_states.device))
        relation_embeddings = self.relation_norm(relation_embeddings)

        if self.gradient_checkpointing and self.training:
            if use_cache:
                logger.warning_once(
                    "`use_cache=True` is incompatible with gradient checkpointing. Setting `use_cache=False`..."
                )
                use_cache = False

        # decoder layers
        next_decoder_cache = () if use_cache else None

        for idx, decoder_layer in enumerate(self.layers):
            past_key_value = past_key_values[idx] if past_key_values is not None else None

            if self.gradient_checkpointing and self.training:

                def create_custom_forward(module):
                    def custom_forward(*inputs):
                        # None for past_key_value
                        return module(*inputs, None)

                    return custom_forward

                layer_outputs = torch.utils.checkpoint.checkpoint(
                    create_custom_forward(decoder_layer),
                    hidden_states,
                    relation_embeddings,
                    self.infer,
                )
            else:
                layer_outputs = decoder_layer(
                    hidden_states,
                    relation_embeddings,
                    past_key_value=past_key_value,
                    use_cache=use_cache,
                    infer=self.infer,
                )

            hidden_states = layer_outputs[0]
            if use_cache:
                next_decoder_cache += (layer_outputs[1],)

        hidden_states = self.norm(hidden_states)

        next_cache = next_decoder_cache if use_cache else None

        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=next_cache,
        )


class YanBrainForCausalLM(YanPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)
        self.infer = config.infer
        self.relation_period = config.relation_period
        self.model = YanBrainModel(config)
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        self.loss_fct = CrossEntropyLoss()

        # Initialize weights and apply final processing
        self.post_init()

    def get_input_embeddings(self):
        return self.model.token_embedding

    def set_input_embeddings(self, value):
        self.model.token_embedding = value

    def get_output_embeddings(self):
        return self.lm_head

    def set_output_embeddings(self, new_embeddings):
        self.lm_head = new_embeddings

    def forward(
            self,
            input_ids,
            position_ids=None,
            past_key_values=None,
            labels=None,
            use_cache=None,
            return_dict=None,
            **kwargs
    ):
        outputs = self.model(
            input_ids=input_ids,
            position_ids=position_ids,
            past_key_values=past_key_values,
            use_cache=use_cache,
        )

        hidden_states = outputs[0]
        if not self.infer:
            logits = self.lm_head(hidden_states)
        else:
            logits = self.lm_head(hidden_states[:, -1, :])
            logits = torch.unsqueeze(logits, 1)

        logits = logits.float()

        loss = None
        if labels is not None:
            # Flatten the tokens
            flatten_logits = logits.view(-1, self.config.vocab_size)
            flatten_labels = labels.view(-1)
            # Enable model parallelism
            flatten_labels = flatten_labels.to(flatten_logits.device)
            loss = self.loss_fct(flatten_logits, flatten_labels)

        if not return_dict:
            output = (logits,)
            return (loss,) + output if loss is not None else output

        return CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
        )

    def prepare_inputs_for_generation(
            self,
            input_ids,
            past_key_values=None,
            **kwargs
    ):
        seq_len = len(input_ids[0])
        if past_key_values and seq_len > 0:
            position_ids = torch.arange(seq_len - 1, seq_len) % self.relation_period + 1
            input_ids = input_ids[:, -1:]
        else:
            position_ids = torch.arange(0, seq_len) % self.relation_period + 1

        model_inputs = {
            "input_ids": input_ids,
            "position_ids": position_ids,
            "past_key_values": past_key_values,
            "use_cache": kwargs.get("use_cache"),
        }
        return model_inputs

    @torch.inference_mode()
    def chat(self, tokenizer, query: str, max_new_tokens: int = 200,
             num_beams=1, do_sample=True, top_p=0.85, temperature=0.7,
             top_k=30, repetition_penalty=1.0, **kwargs):

        gen_kwargs = dict(
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=do_sample,
            num_beams=num_beams,
            repetition_penalty=repetition_penalty,
            max_new_tokens=max_new_tokens,
        )
        gen_kwargs.update(kwargs)

        inputs = ["<|USER|>" + query]

        # Infer时去除首个"▁"
        if isinstance(inputs, str):
            inputs = [inputs]
        input_ids = tokenizer(inputs)["input_ids"]
        input_ids = [item[2:] for item in input_ids]
        input_ids = torch.tensor(input_ids)

        inputs = input_ids.to(self.device)
        outputs = self.generate(input_ids=inputs, **gen_kwargs)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
