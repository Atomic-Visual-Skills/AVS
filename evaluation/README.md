## Extract Answer Script

`extract_answer.py` is designed to process a JSON file containing a list of questions and model answers, after getting responses from `run_model.py`. The script extracts one or more keywords from each model response to make the answer format easier to judge the correctness. Make sure you placed your `.env` file with `OPENAI_API_KEY` in your repository directory!

### Usage
To run the script, use the following command:

```
python extract_answer.py --input <input_json> --output <output_json> [OPTIONS]
```

`<input_json>`: The path to the input JSON file that is an output from `run_model.py`.

`<output_json>`: The path where the JSON file with extracted answers added will be saved.

### Options

`--save_every`: Specifies how often to save intermediate results (default is 10). The results are saved incrementally based on this parameter.

`--trunk_response`: Truncate the model response to the last n words. If set to -1 (default), the entire response is used.

`--verbose` or `-v`: Enables verbose mode, which provides detailed logging of the execution.

## Score Answer Script

`score_answer.py` is designed to process a JSON file containing a list of standard answers and extracted model answers, after extracting keywords from `extract_answer.py`. The script scores each model answer by comparing it to the corresponding standard answer, producing a judgment of '1' (correct) or '0' (incorrect). Make sure you placed your `.env` file with `OPENAI_API_KEY` in your repository directory!

### Usage
To run the script, use the following command:

```
python score_answer.py --input <input_json> --output <output_json> [OPTIONS]
```

`<input_json>`: The path to the input JSON file that is an output from `extract_answer.py`.

`<output_json>`: The path where the JSON file with judgments added will be saved.

### Options

`--exact_match`: If specified, the script uses exact matching for scoring. The extracted model answer must exactly match the standard answer to be considered correct.

`--save_every`: Specifies how often to save intermediate results (default is 10). The results are saved incrementally based on this parameter.

`--trunk_response`: Truncate the model response to the last n words. If set to -1 (default), the entire response is used.

`--verbose` or `-v`: Enables verbose mode, which provides detailed logging of the execution.

## Analyze Script

`analyze.py` is designed to process a JSON file containing scoring results from `score_answer.py`. The script extracts model-wise accuracy scores based on different criteria such as skill, difficulty, or both, and can generate statistics and logs of incorrectly answered problems. Make sure the input data is available and correctly formatted before running the script.

### Usage
To run the script, use the following command:

```
python analyze.py --scored_dir <scored_dir> --models <model_names> --save_dir <save_dir> [OPTIONS]
```

`<scored_dir>`: The directory containing the JSON files with scoring results for each model.

`<model_names>`: A space-separated list of model names to analyze.

`<save_dir>`: The directory where the analysis results will be saved.

### Options

`--add_wrong_logs`: If specified, the script saves logs of problems that were not answered correctly.

`--verbose` or `-v`: Enables verbose mode, which provides detailed logging of the execution and summarizes results to the console.

### Score Calculation

Overall Scores: Computes average accuracy across all problems for each model. Saved in `{model}_avg_scores.json`.

Skill Scores: Calculates average accuracy for each skill category for each model. Saved in `{model}_skill_avg_scores.json`.

Difficulty Scores: Computes average accuracy for each difficulty level. Saved in `{model}_diff_avg_scores.json`.

Skill and Difficulty Scores: Calculates average accuracy for combinations of skill and difficulty. `{model}_skill_diff_avg_scores.json`.