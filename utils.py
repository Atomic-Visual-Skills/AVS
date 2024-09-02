import base64
import json
import os
from openai import OpenAI
from PIL import Image


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def open_image(image_path):
    return Image.open(image_path)

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def write_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        return json.dump(data, f, ensure_ascii=False)
    
def get_evaluation_chat_response(sys_prompt, user_prompt, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content

def printv(print_content, verbose):
    if verbose:
        print(print_content)

def majority_voting(lst):
    if lst.count(0) > lst.count(1):
        return 0
    else:
        return 1