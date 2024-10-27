# Decomposing Complex Visual Comprehension into Atomic Visual Skills for Vision Language Models

![MathQA](https://img.shields.io/badge/Task-MathQA-red) 
![Mathematical Reasoning](https://img.shields.io/badge/Task-Mathematical_Reasoning-red) 
![Multi-Modal](https://img.shields.io/badge/Task-Multi--Modal-red)

[[Paper](https://openreview.net/forum?id=nFU4xCyoe0&referrer=%5BAuthor%20Console%5D(%2Fgroup%3Fid%3DNeurIPS.cc%2F2024%2FWorkshop%2FMATH-AI%2FAuthors%23your-submissions))]

## Evaluation
**1. Download**
```
git clone https://github.com/Atomic-Visual-Skills/AVS.git
cd AVS
pip install -r requirements.txt
```
Also, write down .env file with your api key.

**2. Get Model Responses**
```
sh scripts/run_model/gpt-4o.sh
```

**3. Extract Answers**
```
sh scripts/extract_answer/gpt-4o.sh
```

**4. Score Answers**
```
sh scripts/score_answer/gpt-4o.sh
```

**All at once (2 ~ 4)**
```
sh scripts/process/gpt-4o.sh
```

## Citation
```latex
@inproceedings{
    chae2024decomposing,
    title={Decomposing Complex Visual Comprehension into Atomic Visual Skills for Vision Language Models},
    author={Hyunsik Chae and Seungwoo Yoon and Chloe Yewon Chun and Gyehun Go and Yongin Cho and Gyeongmin Lee and Ernest K. Ryu},
    booktitle={The 4th Workshop on Mathematical Reasoning and AI at NeurIPS'24},
    year={2024},
    url={https://openreview.net/forum?id=nFU4xCyoe0}
}
```