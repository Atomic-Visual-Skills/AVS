python evaluation/run_model.py \
--model table-llava \
--input data/test.json \
--output results/run_model/table-llava/table-llava.json

python evaluation/run_model.py \
--model table-llava \
--input data/test.json \
--output results/run_model/table-llava/table-llava-cot.json \
--cot