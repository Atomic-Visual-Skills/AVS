import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm
import os

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import *

# convert difficulty to ['easy', 'medium', 'hard', 'hell', 'abyss']
def convert_difficulty(difficulty):
    difficulty = str(difficulty).lower()
    if 'easy' in difficulty or '1' in difficulty:
        difficulty = 'easy'
    elif 'medium' in difficulty or '2' in difficulty:
        difficulty = 'medium'
    elif 'hard' in difficulty or '3' in difficulty:
        difficulty = 'hard'
    elif 'hell' in difficulty or '4' in difficulty:
        difficulty = 'hell'
    elif 'abyss' in difficulty or '5' in difficulty:
        difficulty = 'abyss'
    else:
        raise ValueError(f"Unknown difficulty: {difficulty}")
    return difficulty

# calculate average scores for each model
def get_scores(model_results, verbose=False):
    printv("Getting scores for each model...", verbose=verbose)
    model_avg_scores = {}
    for model in tqdm(model_results.keys()):
        scores = [d['judgement'] for d in model_results[model]]
        model_avg_scores[model] = {'correct_problems': sum(scores), 'total_problems': len(scores), 'avg_score': np.mean(scores)}
    return model_avg_scores

# calculate average scores for each model and skill
def get_scores_skill(model_results, verbose=False):
    printv("Getting scores for each model and skill...", verbose=verbose)
    model_skill_avg_scores = {}
    for model in tqdm(model_results.keys()):
        model_skill_avg_scores[model] = {}
        for entry in model_results[model]:
            try:
                skill = entry['skill']
            except Exception as e:
                print(entry)
                raise e
            if skill not in model_skill_avg_scores[model]:
                model_skill_avg_scores[model][skill] = {'correct_problems': 0, 'total_problems': 0}
            model_skill_avg_scores[model][skill]['correct_problems'] += entry['judgement']
            model_skill_avg_scores[model][skill]['total_problems'] += 1
        for skill in model_skill_avg_scores[model]:
            model_skill_avg_scores[model][skill]['avg_score'] = model_skill_avg_scores[model][skill]['correct_problems'] / model_skill_avg_scores[model][skill]['total_problems']
    return model_skill_avg_scores

# calculate average scores for each model and difficulty
def get_scores_difficulty(model_results, verbose=False):
    printv("Getting scores for each model and difficulty...", verbose=verbose)
    model_diff_avg_scores = {}
    for model in tqdm(model_results.keys()):
        model_diff_avg_scores[model] = {}
        for entry in model_results[model]:
            diff = entry['difficulty']
            if diff not in model_diff_avg_scores[model]:
                model_diff_avg_scores[model][diff] = {'correct_problems': 0, 'total_problems': 0}
            model_diff_avg_scores[model][diff]['correct_problems'] += entry['judgement']
            model_diff_avg_scores[model][diff]['total_problems'] += 1
        for diff in model_diff_avg_scores[model]:
            model_diff_avg_scores[model][diff]['avg_score'] = model_diff_avg_scores[model][diff]['correct_problems'] / model_diff_avg_scores[model][diff]['total_problems']
    return model_diff_avg_scores

# calculate average scores for each model and skill and difficulty
def get_scores_skill_difficulty(model_results, verbose=False):
    printv("Getting scores for each model and skill, difficulty...", verbose=verbose)
    model_skill_diff_avg_scores = {}
    for model in tqdm(model_results.keys()):
        model_skill_diff_avg_scores[model] = {}
        for entry in model_results[model]:
            print(entry)
            skill = entry['skill']
            diff = entry['difficulty']
            if skill not in model_skill_diff_avg_scores[model]:
                model_skill_diff_avg_scores[model][skill] = {}
            if diff not in model_skill_diff_avg_scores[model][skill]:
                model_skill_diff_avg_scores[model][skill][diff] = {'correct_problems': 0, 'total_problems': 0}
            model_skill_diff_avg_scores[model][skill][diff]['correct_problems'] += entry['judgement']
            model_skill_diff_avg_scores[model][skill][diff]['total_problems'] += 1
        for skill in model_skill_diff_avg_scores[model]:
            for diff in model_skill_diff_avg_scores[model][skill]:
                model_skill_diff_avg_scores[model][skill][diff]['avg_score'] = model_skill_diff_avg_scores[model][skill][diff]['correct_problems'] / model_skill_diff_avg_scores[model][skill][diff]['total_problems']
    return model_skill_diff_avg_scores

# save wrong logs
def save_wrong_logs(model_results, save_dir, verbose=False):
    printv("Saving wrong logs...", verbose=verbose)
    for model in model_results.keys():
        wrong_logs = [d for d in model_results[model] if d['judgement'] == 0]
        write_json(f'{save_dir}/{model}_wrong_logs.json', wrong_logs)

# draw a bar plot that summarizes the scores
# FIXME: this function is not working properly
def draw_plot(model_avg_scores, model_skill_avg_scores, model_diff_avg_scores, model_skill_diff_avg_scores, verbose=False):
    printv("Drawing plots...", verbose=verbose)
    for model in model_avg_scores.keys():
        avg_scores = model_avg_scores[model]
        skill_avg_scores = model_skill_avg_scores[model]
        diff_avg_scores = model_diff_avg_scores[model]
        skill_diff_avg_scores = model_skill_diff_avg_scores[model]

        # create a figure and a set of subplots
        fig, ax = plt.subplots(2, 2, figsize=(12, 12))

        # plot skill average scores
        for i, skill in enumerate(skill_avg_scores.keys()):
            ax[0, 1].bar(skill_avg_scores[skill].keys(), [d['avg_score'] for d in skill_avg_scores[skill].values()], label=skill, alpha=0.5)
        ax[0, 1].set_title(f'{model} skill average scores')
        ax[0, 1].set_xlabel('difficulty')
        ax[0, 1].set_ylabel('average score')
        ax[0, 1].legend()

        # plot difficulty average scores
        ax[1, 0].bar(diff_avg_scores.keys(), [d['avg_score'] for d in diff_avg_scores.values()])
        ax[1, 0].set_title(f'{model} difficulty average scores')
        ax[1, 0].set_xlabel('difficulty')
        ax[1, 0].set_ylabel('average score')

        # plot skill and difficulty average scores
        for i, skill in enumerate(skill_diff_avg_scores.keys()):
            for j, diff in enumerate(skill_diff_avg_scores[skill].keys()):
                ax[1, 1].bar(diff, skill_diff_avg_scores[skill][diff]['avg_score'], label=f'{skill} {diff}', alpha=0.5)
        ax[1, 1].set_title(f'{model} skill and difficulty average scores')
        ax[1, 1].set_xlabel('difficulty')
        ax[1, 1].set_ylabel('average score')
        ax[1, 1].legend()

        plt.tight_layout()
        plt.savefig(f'{model}_scores.png')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # directory to analyze
    parser.add_argument('--scored_dir', type=str, default='.')
    parser.add_argument('--models', type=str, nargs='+', required=True)
    parser.add_argument('--save_dir', type=str, default='.')
    parser.add_argument('--add_wrong_logs', action='store_true', help='add logs of problems that were not answered correctly')
    parser.add_argument('--add_plot', action='store_true', help='add plot of scores')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose mode')
    args = parser.parse_args()

    # if the save_dir does not exist, create it
    os.makedirs(args.save_dir, exist_ok=True)

    # for each model, find json files that include the model name
    model_files = {}
    for model in args.models:
        model_files[model] = []
        for file in Path(args.scored_dir).rglob('*.json'):
            if model.lower() in file.stem.lower():
                model_files[model].append(file)
    
    # for each model, load json files
    model_results = {}
    for model in args.models:
        model_results[model] = []
        for file in model_files[model]:
            data = read_json(file)
            model_results[model].extend(data)

    # for each model, remove duplicates that share same image_dir
    for model in args.models:
        image_dirs = set()
        unique_results = []
        for result in model_results[model]:
            if result['image_dir'] not in image_dirs:
                image_dirs.add(result['image_dir'])
                unique_results.append(result)
        model_results[model] = unique_results
        print(f'{model} has {len(model_results[model])} unique results')
    
    # convert various difficulty levels to ['easy', 'medium', 'hard', 'hell', 'abyss']
    for model in args.models:
        for result in model_results[model]:
            if 'difficulty' in result:
                result['difficulty'] = convert_difficulty(result['difficulty'])

    # calculate average scores
    model_avg_scores = get_scores(model_results, verbose=args.verbose)
    model_skill_avg_scores = get_scores_skill(model_results, verbose=args.verbose)
    model_diff_avg_scores = get_scores_difficulty(model_results, verbose=args.verbose)
    model_skill_diff_avg_scores = get_scores_skill_difficulty(model_results, verbose=args.verbose)

    # save each scores to json
    for model in args.models:
        write_json(f'{args.save_dir}/{model}_avg_scores.json', model_avg_scores[model])
        write_json(f'{args.save_dir}/{model}_skill_avg_scores.json', model_skill_avg_scores[model])
        write_json(f'{args.save_dir}/{model}_diff_avg_scores.json', model_diff_avg_scores[model])
        write_json(f'{args.save_dir}/{model}_skill_diff_avg_scores.json', model_skill_diff_avg_scores[model])
    
    # save wrong logs
    save_wrong_logs(model_results, args.save_dir, verbose=args.verbose)

    # TODO: fix this function
    # draw plot
    # if args.add_plot:
    #    draw_plot(model_avg_scores, model_skill_avg_scores, model_diff_avg_scores, model_skill_diff_avg_scores, verbose=args.verbose)

    # summarize the result to the console
    # do not use pd.dataframe to print the result
    if args.verbose:
        for model in args.models:
            # for model_diff_avg_scores and model_skill_diff_avg_scores, add the number 1, 2, 3, 4, 5 in front of 'easy', 'medium', 'hard', 'hell', 'abyss'
            # 1: easy, 2: medium, 3: hard, 4: hell, 5: abyss
            diff_label = {'easy': '1. easy', 'medium': '2. medium', 'hard': '3. hard', 'hell': '4. hell', 'abyss': '5. abyss'}
            model_diff_avg_scores[model] = {diff_label[k]: v for k, v in model_diff_avg_scores[model].items()}
            model_skill_diff_avg_scores[model] = {k: {diff_label[kk]: vv for kk, vv in v.items()} for k, v in model_skill_diff_avg_scores[model].items()}

            
            print(f'{model} average scores:')
            for key, value in model_avg_scores[model].items():
                print(f'{key}: {value}')
                
        for model in args.models:
            print(f'{model} skill average scores:')
            for skill, scores in sorted(model_skill_avg_scores[model].items()):
                print(f'{skill}: {scores}')
            print(f'{model} difficulty average scores:')
            for diff, scores in sorted(model_diff_avg_scores[model].items()):
                #
                print(f'{diff}: {scores}')
            print(f'{model} skill and difficulty average scores:')
            for skill, diff_scores in sorted(model_skill_diff_avg_scores[model].items()):
                print(f'{skill}:')
                for diff, scores in sorted(diff_scores.items()):
                    print(f'  {diff}: {scores}')
        