python evaluation/run_model.py \
--model claude \
--input data/test.json \
--output results/run_model/claude/claude-3.5-sonnet.json

python evaluation/run_model.py \
--model claude \
--input data/test.json \
--output results/run_model/claude/claude-3.5-sonnet-cot.json
--cot