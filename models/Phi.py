import os

import torch
from transformers import AutoProcessor, AutoModelForCausalLM

from .ModelInterface import ModelInterface

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *


class Phi(ModelInterface):
    def __init__(self, model='microsoft/Phi-3.5-vision-instruct', temperature=0, max_tokens=1024):
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'  # TODO: fix this
        self.processor = AutoProcessor.from_pretrained(model, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True, trust_remote_code=True).to(self.device)

    def run(self, image_path, prompt):
        conversation = [
            {
                'role': 'user',
                'content': '<|image_1|>\n' + prompt
            }
        ]

        prompt = self.processor.tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)
        print(prompt)

        image = open_image(image_path)
        inputs = self.processor(prompt, [image], return_tensors='pt').to(self.device)

        output = self.model.generate(**inputs, max_new_tokens=self.max_tokens, temperature=self.temperature, do_sample=True, top_p=None)[0]
        output = self.processor.decode(output, skip_special_tokens=False)

        output = output.replace(prompt, '')

        return output
