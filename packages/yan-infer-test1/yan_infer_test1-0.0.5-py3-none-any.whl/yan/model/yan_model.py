import os

import torch

from yan.model.yan_brain import YanBrainForCausalLM
from yan.model.yan_configuration import YanConfig
from yan.tokenizer.yan_tokenization import YanTokenizer


def load_model(model_path: str, device: str = "cuda:0"):
    token_model_file = os.path.join(model_path, "tokenizer.model")
    model_config_path = os.path.join(model_path, "config.json")

    tokenizer = YanTokenizer(
        vocab_file=token_model_file,
        add_bos_token=False
    )
    if not tokenizer.pad_token_id:
        tokenizer.pad_token_id = tokenizer.unk_token_id
    tokenizer.padding_side = "right"

    config = YanConfig.from_pretrained(model_config_path)
    config.infer = True
    config.use_cache = True
    dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] == 8 else torch.float16
    kwargs = {
        "torch_dtype": dtype,
        "device_map": {"": device},
        "config": config
    }
    model = YanBrainForCausalLM.from_pretrained(
        model_path,
        low_cpu_mem_usage=True,
        **kwargs
    )
    model.eval()
    return model, tokenizer
