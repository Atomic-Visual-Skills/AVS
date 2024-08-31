python ../../evaluation/run_model.py \
--model llava \
--input ../../data/test.json \
--output ../../results/run_model/llava/llava-7b.json \
--size 7b

python ../../evaluation/run_model.py \
--model llava \
--input ../../data/test.json \
--output ../../results/run_model/llava/llava-13b.json \
--size 13b

python ../../evaluation/run_model.py \
--model llava \
--input ../../data/test.json \
--output ../../results/run_model/llava/llava-72b.json \
--size 72b

python ../../evaluation/run_model.py \
--model llava \
--input ../../data/test.json \
--output ../../results/run_model/llava/llava-110b.json \
--size 110b