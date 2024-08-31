import os

import torch
from transformers import AutoModelForCausalLM

from .ModelInterface import ModelInterface

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules/DeepSeek-VL')))

from deepseek_vl.models import VLChatProcessor, MultiModalityCausalLM
from deepseek_vl.utils.io import load_pil_images


class DeepSeek_VL(ModelInterface):
    def __init__(self, model='deepseek-ai/deepseek-vl-1.3b-chat', temperature=0, max_tokens=1024):
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.processor = VLChatProcessor.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(model, trust_remote_code=True)
        self.model = self.model.to(torch.bfloat16).to(self.device).eval()

    def run(self, image_path, prompt):
        conversation = [
            {
                'role': 'User',
                'content': f'<image_placeholder>{prompt}',
                'images': [image_path]
            },
            {
                'role': 'Assistant',
                'content': ''
            }
        ]

        pil_images = load_pil_images(conversation)
        inputs = self.processor(
            conversations=conversation,
            images=pil_images,
            force_batchify=True
        ).to(self.device)
        inputs_embeds = self.model.prepare_inputs_embeds(**inputs)

        outputs = self.model.language_model.generate(
            inputs_embeds=inputs_embeds,
            attention_mask=inputs.attention_mask,
            pad_token_id=self.processor.tokenizer.eos_token_id,
            bos_token_id=self.processor.tokenizer.bos_token_id,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            max_new_tokens=512,
            do_sample=False,
            use_cache=True
        )

        output = self.processor.tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
        return output