python evaluation/run_model.py \
--model intern-vl \
--input data/test.json \
--output results/run_model/intern-vl/intern-vl-1b.json \
--size 1b

python evaluation/run_model.py \
--model intern-vl \
--input data/test.json \
--output results/run_model/intern-vl/intern-vl-2b.json \
--size 2b

python evaluation/run_model.py \
--model intern-vl \
--input data/test.json \
--output results/run_model/intern-vl/intern-vl-4b.json \
--size 4b

python evaluation/run_model.py \
--model intern-vl \
--input data/test.json \
--output results/run_model/intern-vl/intern-vl-8b.json \
--size 8b

python evaluation/run_model.py \
--model intern-vl \
--input data/test.json \
--output results/run_model/intern-vl/intern-vl-26b.json \
--size 26b


python evaluation/run_model.py \
--model intern-vl \
--input data/test.json \
--output results/run_model/intern-vl/intern-vl-40b.json \
--size 40b


python evaluation/run_model.py \
--model intern-vl \
--input data/test.json \
--output results/run_model/intern-vl/intern-vl-76b.json \
--size 76b