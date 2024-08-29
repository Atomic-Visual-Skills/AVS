import os

import torch
from transformers import AutoTokenizer, AutoModel, CLIPImageProcessor

from .ModelInterface import ModelInterface

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *


class InternVL(ModelInterface):
    def __init__(self, model='OpenGVLab/InternVL-Chat-V1-1', temperature=0, max_tokens=1024):
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'  # TODO: fix this
        self.tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True, use_fast=False)
        self.image_processor = CLIPImageProcessor.from_pretrained(model)
        self.model = AutoModel.from_pretrained(
            model,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            use_flash_attn=True,
            trust_remote_code=True).eval().to(self.device)

    def run(self, image_path, prompt):
        prompt = '<image>\n' + prompt

        image = open_image(image_path)
        pixel_values = self.image_processor(images=image, return_tensors='pt').pixel_values.to(torch.bfloat16).to(self.device)
        generation_config = dict(max_new_tokens=self.max_tokens, do_sample=True if self.temperature > 0 else False, temperature=self.temperature)

        output = self.model.chat(self.tokenizer, pixel_values, prompt, generation_config)

        return output
