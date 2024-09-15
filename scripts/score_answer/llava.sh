python evaluation/score_answer.py \
--input results/extract_answer/llava/llava-7b.json \
--output results/score_answer/llava/llava-7b.json

python evaluation/score_answer.py \
--input results/extract_answer/llava/llava-13b.json \
--output results/score_answer/llava/llava-13b.json 

python evaluation/score_answer.py \
--input results/extract_answer/llava/llava-7b-cot.json \
--output results/score_answer/llava/llava-7b-cot.json

python evaluation/score_answer.py \
--input results/extract_answer/llava/llava-13b-cot.json \
--output results/score_answer/llava/llava-13b-cot.json 

# python evaluation/score_answer.py \
# --input results/extract_answer/llava/llava-72b.json \
# --output results/score_answer/llava/llava-72b.json 

# python evaluation/score_answer.py \
# --input results/extract_answer/llava/llava-110b.json \
# --output results/score_answer/llava/llava-110b.json