import os
import copy
import argparse
from tqdm import tqdm
from collections import defaultdict
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *
from dotenv import find_dotenv, load_dotenv

from prompts import sys_prompt, demo_prompt_score

# Check if the judgment is in the correct format
def verify_judgment(judgment):
    judgment = judgment.strip()
    if judgment == None or judgment not in ['0', '1']:
        return False
    return True

# Create a test prompt for the model to score the answer
def create_test_prompt(demo_prompt, answer, extraction):
    demo_prompt = demo_prompt.strip()
    test_prompt = f"[Standard Answer] {answer}\n[Model Answer] {extraction}\njudgment: "
    full_prompt = f"{demo_prompt}\n\n{test_prompt}"
    return full_prompt

# Match the standard answer with the extracted answer
def match_answer(answer, extraction, api_key, verbose=False):
    # general extraction
    try:
        test_prompt = create_test_prompt(demo_prompt_score, answer, extraction)
        judgment = get_evaluation_chat_response(sys_prompt, test_prompt, api_key)
        # sometimes gpt may return 'judgment: 1' or 'judgment: 0'
        return judgment.lower().replace("judgment:", "").strip()
    except Exception as e:
        printv(e, verbose)
        print(f"Error in matching answer:\n[Standard Answer] {answer}\n[Model Answer] {extraction}")
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

    score_dict = defaultdict(lambda: defaultdict(list))
    score_version_dict = defaultdict(list)

    # Enumerate results
    for i, inst in enumerate(tqdm(results)):
        save_inst = copy.deepcopy(inst)
        
        judgments = list(map(lambda x: match_answer(save_inst['answer'], x, api_key), save_inst['extraction']))
            
        for j in range(len(judgments)):
            while True:
                if not verify_judgment(judgments[j]):
                    print('Wrong judgment format: ', judgments[j])
                    judgments[j] = match_answer(save_inst['answer'], save_inst['extraction'][j], api_key, args.verbose)
                else:
                    judgments[j] = int(judgments[j])
                    break

        save_inst['judgments'] = judgments
        save_inst['judgment'] = majority_voting(judgments)

        save_results.append(save_inst)

        # Print and save judgment statistics
        printv(f"Total: {len(save_results)}, Correct: {len([inst for inst in save_results if inst['judgment']])}", args.verbose)

        if (i+1) % args.save_every == 0 or i == len(results)-1:
            printv(f"Saving results to {args.output}...", args.verbose)
            write_json(args.output, save_results)
            printv(f"Results saved.", args.verbose)