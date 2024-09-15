# python evaluation/run_model.py \
# --model deepseek-vl \
# --input data/test.json \
# --output results/run_model/deepseek-vl/deepseek-vl-1.3b.json \
# --size 1.3b

python evaluation/run_model.py \
--model deepseek-vl \
--input data/test.json \
--output results/run_model/deepseek-vl/deepseek-vl-7b.json \
--size 7b

python evaluation/run_model.py \
--model deepseek-vl \
--input data/test.json \
--output results/run_model/deepseek-vl/deepseek-vl-7b-cot.json \
--size 7b
--cot