from stf.configuration_utils import PretrainedConfig
from stf.utils import logging

logger = logging.get_logger(__name__)


class YanConfig(PretrainedConfig):
    model_type = "yan"
    keys_to_ignore_at_inference = ["past_key_values"]

    def __init__(
            self,
            pad_token_id=0,
            bos_token_id=1,
            eos_token_id=2,
            max_len=1024,
            relation_period=512,
            hidden_size=32000,
            vocab_size=65536,
            rms_norm_eps=1e-6,
            num_hidden_layers=1,
            use_mlp=False,
            intermediate_size=10240,
            use_residual=False,
            initializer_range=1,
            dropout=0.1,
            use_cache=True,
            infer=False,
            tie_word_embeddings=False,
            **kwargs,
    ):
        self.max_len = max_len
        self.relation_period = relation_period
        self.hidden_size = hidden_size
        self.vocab_size = vocab_size
        self.rms_norm_eps = rms_norm_eps
        self.num_hidden_layers = num_hidden_layers
        self.use_mlp = use_mlp
        self.intermediate_size = intermediate_size
        self.use_residual = use_residual
        self.initializer_range = initializer_range
        self.dropout = dropout
        self.use_cache = use_cache
        self.infer = infer

        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            tie_word_embeddings=tie_word_embeddings,
            **kwargs,
        )
