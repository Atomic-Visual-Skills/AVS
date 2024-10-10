import argparse
import os
from tqdm import tqdm

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import *
import models

def run_model(model: models.ModelInterface, data, cot, image_dir, n):
    result = []
    errors = []

    for item in tqdm(data):
        prompt = item['question']

        if cot:
            prompt = f'{prompt} Let\'s think step by step.'

        image_path = os.path.join(image_dir, item['image_dir'])

        outputs = []

        for _ in range(n):
            outputs.append(model.run(image_path, prompt))
            try:
                outputs.append(model.run(image_path, prompt))
            except Exception as e:
                errors.append(item['image_dir'])
                outputs.append('')         

        result.append({
            **item,
            'model_answer': outputs
        })

    for error in errors:
        print(f'Model made error at {error}')

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, required=True, help='Input JSON file path')
    parser.add_argument('--output', type=str, required=True, help='Output JSON file path')
    parser.add_argument('--model', type=str, required=True, help='Name of the model',
                        choices=['gpt-4o', 'gemini', 'llava', 'llava-ov', 'mllava', 'table-llava', 'intern-vl', 'phi', 'deepseek-vl', 'custom'])
    parser.add_argument('--cot', action='store_true', help='Use chain of thought')
    parser.add_argument('--size', type=str, required=False, default=None, help='Size of the model')
    parser.add_argument('--n', type=int, default=3, help='Number of answers for each question')
    args = parser.parse_args()

    data = read_json(args.input)
    model = models.load_model(args.model, args.size)
    image_dir = os.path.join(os.path.dirname(args.input), 'images')

    result = run_model(model, data, args.cot, image_dir, args.n)

    write_json(args.output, result)