import os
import copy
import argparse
from tqdm import tqdm
from utils import *
from dotenv import find_dotenv, load_dotenv

from prompts import sys_prompt, demo_prompt_extract

# Check if the extracted answer is not empty
def verify_extraction(extraction):
    extraction = extraction.strip()
    if extraction == "" or extraction == None:
        return False
    return True

# Create a test prompt for the model to extract the answer
def create_test_prompt(demo_prompt, question, response):
    demo_prompt = demo_prompt.strip()
    test_prompt = f"Question: {question}\nModel response: {response}\nExtracted Answer: "
    full_prompt = f"{demo_prompt}\n\n{test_prompt}"
    return full_prompt

# Extract the answer from the model response
def extract_answer(question, response, api_key, verbose=False):
    try:
        test_prompt = create_test_prompt(demo_prompt_extract, question, response)
        extraction = get_evaluation_chat_response(sys_prompt, test_prompt, api_key)
        # Only extract the content after 'Extracted Answer:'
        if 'Extracted answer:' in extraction:
            return extraction.split('Extracted answer:')[-1].strip()
        # If the model does not provide the answer in an instructed format, return the whole response
        else:
            return extraction.strip()
    except Exception as e:
        printv(e, verbose)
        print(f"Error in extracting answer for '{response}'")
    return ""

# If necessary, truncate the response to the last n words
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
    parser.add_argument('--trunk_response', type=int, default=-1, help='trunk response to the last n words')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose mode')
    args = parser.parse_args()

    # Set api key
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    api_key = os.getenv("OPENAI_API_KEY")

    # Read results
    result_file = args.input
    printv(f"Reading {result_file}...", args.verbose)
    results = read_json(result_file)

    save_results = []

    # Enumerate results
    for i, inst in enumerate(tqdm(results)):
        save_inst = copy.deepcopy(inst)
        if 'model_answer' in save_inst:
            response = save_inst['model_answer']  
        else:
            response = ''
            printv(save_inst, args.verbose)
            printv("######### NO MODEL ANSWER ###########", args.verbose)  # some model may output nothing due to safety issue
            
        response = map(lambda x: trunk_response(x, args.trunk_response), response)

        save_inst['extraction'] = list(map(lambda x: extract_answer(save_inst['question'], x, api_key, args.verbose), response))            
        save_results.append(save_inst)

        if (i+1) % args.save_every == 0 or i == len(results) - 1:
            printv(f"Saving results to {args.output}...", args.verbose)
            write_json(args.output, save_results)
            printv(f"Results saved.", args.verbose)