import os
import copy
import argparse
from tqdm import tqdm
from collections import defaultdict
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

# OpenAI
import openai

from prompts import sys_prompt, demo_prompt_extract

def verify_extraction(extraction):
    extraction = extraction.strip()
    if extraction == "" or extraction == None:
        return False
    return True


def create_test_prompt(demo_prompt, question, response):
    demo_prompt = demo_prompt.strip()
    test_prompt = f"Question: {question}\nModel response: {response}\nExtracted Answer: "
    full_prompt = f"{demo_prompt}\n\n{test_prompt}"
    return full_prompt


def extract_answer(question, response, api_key, verbose=False):
    try:
        test_prompt = create_test_prompt(demo_prompt_extract, question, response)
        extraction = get_evaluation_chat_response(sys_prompt, test_prompt, api_key)
        # only extract the content after 'Extracted Answer:'
        if 'Extracted answer:' in extraction:
            return extraction.split('Extracted answer:')[-1].strip()
        else:
            return extraction.strip()
    except Exception as e:
        printv(e, verbose)
        print(f"Error in extracting answer for '{response}'")
    return ""


def trunk_response(response, trunk_length):
    if trunk_length <= 0:
        return response
    else:
        return_res = ' '.join(response.split(' ')[-trunk_length:])
        return return_res


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--save_every', type=int, default=10, help='save every n problems')
    parser.add_argument('--cache', action='store_true', help='cache results')
    parser.add_argument('--trunk_response', type=int, default=-1, help='trunk response to the last n words')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose mode')
    # args
    args = parser.parse_args()

    # set api key
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    api_key = os.getenv("OPENAI_API_KEY")

    # read results
    result_file = args.input
    printv(f"Reading {result_file}...", args.verbose)
    results = read_json(result_file)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    if os.path.exists(args.output):
        save_results = json.load(open(args.output))
    else:
        save_results = []

    # enumerate results
    for i, inst in enumerate(tqdm(results)):
        save_inst = save_results[i] if i < len(save_results) else copy.deepcopy(inst)
        if args.cache and 'extraction' in save_inst:
            pass
        else:
            if 'model_answer' in save_inst:
                response = save_inst['model_answer']  
            else:
                response = ''
                printv(save_inst, args.verbose)
                printv("######### NO MODEL ANSWER ###########", args.verbose)  # some model may output nothing due to safety issue
            response = trunk_response(response, args.trunk_response)

            save_inst['extraction'] = extract_answer(save_inst['question'], response, api_key, args.verbose)

            # verify extraction
            if not verify_extraction(save_inst['extraction']):
                save_inst['extraction'] = ''
                printv(save_inst, args.verbose)
                printv("######### NO VALID EXTRACTION ###########", args.verbose)
            
            save_results.append(save_inst)

        if (i+1) % args.save_every == 0 or i == len(results) - 1:
            printv(f"Saving results to {args.output}...", args.verbose)
            write_json(args.output, save_results)
            printv(f"Results saved.", args.verbose)