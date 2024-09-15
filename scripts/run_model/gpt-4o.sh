python evaluation/run_model.py \
--model gpt-4o \
--input data/test.json \
--output results/run_model/gpt-4o/gpt-4o.json

python evaluation/run_model.py \
--model gpt-4o \
--input data/test.json \
--output results/run_model/gpt-4o/gpt-4o-cot.json
--cot