import os
import copy
import argparse
from tqdm import tqdm
from collections import defaultdict
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *
from dotenv import find_dotenv, load_dotenv

# OpenAI
import openai

from prompts import sys_prompt, demo_prompt_score


# load demo prompt
def verify_judgment(judgment):
    judgment = judgment.strip()
    if judgment == None or judgment not in ['0', '1']:
        return False
    return True


def create_test_prompt(demo_prompt, inst):
    demo_prompt = demo_prompt.strip()
    test_prompt = f"[Standard Answer] {inst['answer']}\n[Model Answer] {inst['extraction']}\nJudgment: "
    full_prompt = f"{demo_prompt}\n\n{test_prompt}"
    return full_prompt


def match_answer(inst, api_key, exact_match=False, verbose=False):
    # quick match
    if exact_match:
        return '1' if inst['answer'] == inst['extraction'] else '0'
    # general extraction
    try:
        test_prompt = create_test_prompt(demo_prompt_score, inst)
        judgment = get_evaluation_chat_response(sys_prompt, test_prompt, api_key)
        # sometimes gpt may return 'Judgment: 1' or 'Judgment: 0'
        return judgment.lower().replace("judgment:", "").strip()
    except Exception as e:
        printv(e, verbose)
        print(f"Error in matching answer:\n[Standard Answer] {inst['answer']}\n[Model Answer] {inst['extraction']}")
    return ""


def trunk_response(response, trunk_length):
    if trunk_length <= 0:
        return response
    else:
        return_res = ' '.join(response.split(' ')[-trunk_length:])
        return return_res

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # input
    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str)
    # match
    parser.add_argument('--exact_match', action='store_true', help='use exact match to match answer for some problems')
    # output
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

    score_dict = defaultdict(lambda: defaultdict(list))
    score_version_dict = defaultdict(list)
    # tqdm, enumerate results
    for i, inst in enumerate(tqdm(results)):
        save_inst = save_results[i] if i < len(save_results) else copy.deepcopy(inst)
        if args.cache and 'judgment' in save_inst:
            pass
        else:
            judgment = match_answer(save_inst, api_key, args.exact_match)
            while True:
                if not verify_judgment(judgment):
                    print('Wrong judgment format: ', judgment)
                    judgment = match_answer(save_inst, api_key, args.exact_match)
                else:
                    save_inst['judgment'] = int(judgment)
                    break

            save_results.append(save_inst)

        # judgment statistics
        printv(f"Total: {len(save_results)}, Correct: {len([inst for inst in save_results if inst['judgment']])}", args.verbose)

        if (i+1) % args.save_every == 0 or i == len(results)-1:
            printv(f"Saving results to {args.output}...", args.verbose)
            write_json(args.output, save_results)
            printv(f"Results saved.", args.verbose)
    
     