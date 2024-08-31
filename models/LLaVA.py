import os

import torch
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration

from .ModelInterface import ModelInterface

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *


class LLaVA(ModelInterface):
    def __init__(self, model, temperature=0, max_tokens=1024):
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.processor = LlavaNextProcessor.from_pretrained(model)
        self.model = LlavaNextForConditionalGeneration.from_pretrained(model, torch_dtype=torch.float16, low_cpu_mem_usage=True).to(self.device)
        self.model.eval()

    def run(self, image_path, prompt):
        conversation = [
            {
                'role': 'user',
                'content': [
                    {'type': 'image'},
                    {'type': 'text', 'text': prompt}
                ]
            }
        ]

        prompt = self.processor.apply_chat_template(conversation, add_generation_prompt=True)

        image = open_image(image_path)
        inputs = self.processor(prompt, image, return_tensors='pt').to(self.device)

        output = self.model.generate(**inputs, max_new_tokens=self.max_tokens, temperature=self.temperature, do_sample=True if self.temperature > 0 else False, top_p=None)[0]
        output = self.processor.decode(output, skip_special_tokens=False)

        output = output.replace(prompt, '')
        output = output.replace('<s> ', '')
        output = output.replace('</s>', '')

        return output
