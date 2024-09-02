import os

from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

from .ModelInterface import ModelInterface

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *


class Qwen(ModelInterface):
    def __init__(self, model, temperature=0, max_tokens=1024):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        dotenv_file = find_dotenv()
        load_dotenv(dotenv_file)
        api_key = os.environ.get('DASHSCOPE_API_KEY')
        self.client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)

    def run(self, image_path, prompt):
        base64_image = encode_image(image_path)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        },
                    },
                ],
                }
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        output = response.choices[0].message.content
        return output