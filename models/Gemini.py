import os

import google.generativeai as genai
from dotenv import find_dotenv, load_dotenv

from .ModelInterface import ModelInterface

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *


class Gemini(ModelInterface):
    def __init__(self, model, temperature=0, max_tokens=1024):
        self.temperature = temperature
        self.max_tokens = max_tokens

        dotenv_file = find_dotenv()
        load_dotenv(dotenv_file)
        api_key = os.environ.get('GOOGLE_API_KEY')

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model)

    def run(self, image_path, prompt):
        image = open_image(image_path)
        output = self.model.generate_content([prompt, image], temperature=self.temperature, max_tokens=self.max_tokens).text
        return output