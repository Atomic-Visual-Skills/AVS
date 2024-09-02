import os
import copy

import torch

from .ModelInterface import ModelInterface

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules/LLaVA-NeXT')))
from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path, process_images, tokenizer_image_token
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN, IGNORE_INDEX
from llava.conversation import conv_templates, SeparatorStyle


class LLaVA_OneVision(ModelInterface):
    def __init__(self, model, temperature=0, max_tokens=1024):
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model_name = get_model_name_from_path(model)
        self.tokenizer, self.model, self.image_processor, self.max_length = load_pretrained_model(model, None, self.model_name, device_map='auto')
        self.model.eval()

    def run(self, image_path, prompt):
        conv_template = "qwen_1_5"  # Make sure you use correct chat template for different models
        prompt = DEFAULT_IMAGE_TOKEN + prompt
        conv = copy.deepcopy(conv_templates[conv_template])
        conv.append_message(conv.roles[0], prompt)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        image = open_image(image_path)
        image_tensor = process_images([image], self.image_processor, self.model.config)
        image_tensor = [_image.to(dtype=torch.float16, device=self.device) for _image in image_tensor]

        input_ids = tokenizer_image_token(prompt, self.tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt").unsqueeze(0).to(self.device)
        image_sizes = [image.size]

        output = self.model.generate(
            input_ids,
            images=image_tensor,
            image_sizes=image_sizes,
            do_sample=True if self.temperature > 0 else False,
            temperature=self.temperature,
            max_new_tokens=self.max_tokens,
        )[0]
        output = self.tokenizer.decode(output, skip_special_tokens=True)

        output = output.replace(prompt, '')
        output = output.replace('<s> ', '')
        output = output.replace('</s>', '')

        return output
