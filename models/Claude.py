import os

import anthropic
from dotenv import find_dotenv, load_dotenv

from .ModelInterface import ModelInterface

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *


class Claude(ModelInterface):
    def __init__(self, model, temperature=0, max_tokens=1024):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        dotenv_file = find_dotenv()
        load_dotenv(dotenv_file)

        self.client = anthropic.Anthropic()


    def run(self, image_path, prompt):
        output = self.client.messages.create(
            model = self.model,
            temperature = self.temperature,
            max_tokens = self.max_tokens,
            messages = [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'image',
                            'source': {
                                'type': 'base64',
                                'media_type': 'image/png',
                                'data': encode_image(image_path),
                            }
                        },
                        {
                            'type': 'text',
                            'text': prompt
                        }
                    ]
                }
            ]
        ).content
        return output