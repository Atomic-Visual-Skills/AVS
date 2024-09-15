python evaluation/run_model.py \
--model phi \
--input data/test.json \
--output results/run_model/phi/phi.json

python evaluation/run_model.py \
--model phi \
--input data/test.json \
--output results/run_model/phi/phi-cot.json \
--cot