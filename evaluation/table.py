import json
import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *

models = {
    'gpt-4o': 'gpt-4o/gpt-4o.json',
    'gpt-4o-cot': 'gpt-4o/gpt-4o-cot.json',

    'gemini': 'gemini/gemini-1.5-pro.json',
    'gemini-cot': 'gemini/gemini-1.5-pro-cot.json',

    'llava-7b': 'llava/llava-7b.json',
    'llava-13b': 'llava/llava-13b.json',

    'llava-ov': 'llava-ov/llava-ov-7b.json',
    'table-llava': 'table-llava/table-llava.json',
    'mllava': 'mllava/mllava.json',

    'phi': 'phi/phi.json',
    'intern-vl': 'intern-vl/intern-vl-8b.json',
    'deepseek-vl': 'deepseek-vl/deepseek-vl-7b.json'
}





results = []

for model, path in models.items():
    path = f'results/score_answer/{path}'

    data = read_json(path)

    count = {'total': 0}
    correct = {'total': 0}

    for item in data:
        skill = item['skill']

        if skill not in count:
            count[skill] = 0
            correct[skill] = 0
        count[skill] += 1
        count['total'] += 1
        if item['judgment'] == 1:
            correct[skill] += 1
            correct['total'] += 1
    
    result = {'model': model}

    for skill in count:
        result[skill] = round(correct[skill] / count[skill] * 100, 1)
    
    results.append(result)

write_json('results/table/skill.json', results)

rows = []
columns = results[0].keys()

for item in results:
    row = []
    for column in columns:
        row.append(item[column])
    rows.append(row)

with open('results/table/skill.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

data = read_json('data/test.json')

count = {}
sum_of_p = {}
random_chance = {}

total_count = 0
total_sum_of_p = 0

row1 = []
row2 = []

for item in data:
    skill = item['skill']
    if skill not in count:
        count[skill] = 0
        sum_of_p[skill] = 0
    
    count[skill] += 1
    total_count += 1

    if item['random'] != 0:
        sum_of_p[skill] += 1 / item['random']
        total_sum_of_p += 1 / item['random']

row1.append('total')
row2.append(round(total_sum_of_p / total_count * 100, 1))

for key in count:
    random_chance[key] = round(sum_of_p[key] / count[key] * 100, 1)

    row1.append(key)
    row2.append(random_chance[key])

with open('results/table/skill_random_chance.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(row1)
    writer.writerow(row2)







results = []

for model, path in models.items():
    path = f'results/score_answer/{path}'

    data = read_json(path)

    count = {'total': {'easy': 0, 'medium': 0, 'hard': 0, 'total': 0}}
    correct = {'total': {'easy': 0, 'medium': 0, 'hard': 0, 'total': 0}}

    for item in data:
        skill = item['skill']
        difficulty = item['difficulty'].lower()

        if difficulty == 'very hard':
            difficulty = 'hard'

        if skill not in count:
            count[skill] = {'easy': 0, 'medium': 0, 'hard': 0, 'total': 0}
            correct[skill] = {'easy': 0, 'medium': 0, 'hard': 0, 'total': 0}
        count[skill][difficulty] += 1
        count['total'][difficulty] += 1
        count[skill]['total'] += 1
        count['total']['total'] += 1
        if item['judgment'] == 1:
            correct[skill][difficulty] += 1
            correct['total'][difficulty] += 1
            correct[skill]['total'] += 1
            correct['total']['total'] += 1
    
    result = {'model': model}

    for skill in count:
        result[skill] = {}
        result[skill]['easy'] = round(correct[skill]['easy'] / count[skill]['easy'] * 100, 1)
        result[skill]['medium'] = round(correct[skill]['medium'] / count[skill]['medium'] * 100, 1)
        result[skill]['hard'] = round(correct[skill]['hard'] / count[skill]['hard'] * 100, 1)
        result[skill]['total'] = round(correct[skill]['total'] / count[skill]['total'] * 100, 1)
    
    results.append(result)

write_json('results/table/skill-difficulty.json', results)

rows = []
cols1 = results[0].keys()

def flatten_2d_list(two_d_list):
    return [item for sublist in two_d_list for item in sublist]

cols2 = flatten_2d_list([[col] if col == 'model' else ([col] * 4) for col in cols1])

cols3 = flatten_2d_list([[col] if col == 'model' else ['easy', 'medium', 'hard', 'total'] for col in cols1])

for item in results:
    row = []
    for col1 in cols1:
        if isinstance(item[col1], str):
            row.append(item[col1])
        else:
            for difficulty in item[col1]:
                row.append(item[col1][difficulty])
    rows.append(row)

with open('results/table/skill-difficulty.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(cols2)
    writer.writerow(cols3)
    writer.writerows(rows)

data = read_json('data/test.json')

count = {}
sum_of_p = {}
random_chance = {}

total_count = {'easy':0, 'medium':0, 'hard':0, 'total':0}
total_sum_of_p = {'easy':0, 'medium':0, 'hard':0, 'total':0}

row1 = []
row2 = []

for item in data:
    skill = item['skill']
    difficulty = item['difficulty'].lower()

    difficulty = 'hard' if difficulty == 'very hard' else difficulty

    if skill not in count:
        count[skill] = {'easy':0, 'medium':0, 'hard':0, 'total':0}
        sum_of_p[skill] = {'easy':0, 'medium':0, 'hard':0, 'total':0}
    
    count[skill][difficulty] += 1
    total_count[difficulty] += 1
    count[skill]['total'] += 1
    total_count['total'] += 1

    if item['random'] != 0:
        sum_of_p[skill][difficulty] += 1 / item['random']
        total_sum_of_p[difficulty] += 1 / item['random']
        sum_of_p[skill]['total'] += 1 / item['random']
        total_sum_of_p['total'] += 1 / item['random']

row1.append('total easy')
row1.append('total medium')
row1.append('total hard')
row1.append('total total')

for difficulty in total_count:
    row2.append(round(total_sum_of_p[difficulty] / total_count[difficulty] * 100, 1))

for key in count:
    random_chance[key] = {}
    for difficulty in count[key]:
        random_chance[key][difficulty] = round(sum_of_p[key][difficulty] / count[key][difficulty] * 100, 1) if count[key][difficulty] > 0 else '-'

        row1.append(key + ' ' + difficulty)
        row2.append(random_chance[key][difficulty])

with open('results/table/skill-difficulty_random_chance.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(row1)
    writer.writerow(row2)