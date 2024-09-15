import os

import torch

from .ModelInterface import ModelInterface

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules/Table-LLaVA')))
from llava.mm_utils import get_model_name_from_path
from llava.model.builder import load_pretrained_model
from llava.eval.run_llava import evalmodel


class Table_LLaVA(ModelInterface):
    def __init__(self, model, temperature=0, max_tokens=1024):
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model_path = model
        self.model_name = get_model_name_from_path(model)
        self.tokenizer, self.model, self.image_processor, self.context_len = load_pretrained_model(model, None, self.model_name)
        self.model = self.model.to(self.device)
        self.model.eval()


    def run(self, image_path, prompt):
        args_llava = type('Args', (), {
            "model_path": self.model_path,
            "model_base": None,
            "model_name": self.model_name,
            "query": prompt,
            "conv_mode": None,
            "image_file": image_path,
            "sep": ",",
            "temperature": self.temperature,
            "top_p": None,
            "num_beams": 1,
            "max_new_tokens": self.max_tokens,
            "tokenizer": self.tokenizer,
            "model": self.model,
            "image_processor": self.image_processor
        })()

        output = evalmodel(args_llava)

        return output
