import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sklearn.metrics import f1_score
import numpy as np

# nltk 데이터 다운로드 (최초 실행 시 필요)
nltk.download('punkt')

# 평가 데이터 예시
true_texts = [
    "인문계 고등학교 출신으로서, 저는 대학에서 처음 접한 컴퓨터 프로그래밍과 전자회로 실습 과목에서의 어려움을 극복하기 위해 추가적인 노력을 기울였습니다.",
    "지원자가 시스템프로그래머 직무에 어떻게 기여할 수 있을지를 추가적으로 구체화하면 더 좋을 것입니다."
]

model_outputs = {
    "fine_tuned": [
        "저는 인문계 고등학교 출신으로, 대학에서 처음 접한 컴퓨터 프로그래밍과 전자회로 실습 과목에서 어려움을 극복하기 위해 많은 노력을 기울였습니다.",
        "지원자가 시스템프로그래머 직무에 어떻게 기여할 수 있을지 구체적으로 서술하는 것이 좋습니다."
    ],
    "educce": [
        "저는 인문계 고등학교에서 졸업한 후, 대학에서 프로그래밍과 전자회로 실습 과목을 배우면서 많은 어려움을 겪었습니다.",
        "지원자가 시스템프로그래머 직무에 어떻게 기여할 수 있을지를 추가적으로 설명하는 것이 좋습니다."
    ],
    "saramin": [
        "저는 인문계 고등학교를 졸업하고 대학에서 컴퓨터 프로그래밍과 전자회로 실습 과목에서 어려움을 극복하기 위해 노력했습니다.",
        "시스템프로그래머 직무에 기여할 수 있는 구체적인 방법을 추가적으로 서술하는 것이 좋습니다."
    ],
    "gpt_4": [
        "인문계 고등학교를 졸업한 후, 대학에서 컴퓨터 프로그래밍과 전자회로 실습 과목에서 처음으로 어려움을 겪었습니다.",
        "지원자가 시스템프로그래머 직무에 어떻게 기여할 수 있을지 추가적으로 서술하는 것이 좋습니다."
    ]
}

# BLEU 계산 함수
def calculate_bleu(reference, candidate):
    smoothie = SmoothingFunction().method4
    reference_tokens = nltk.word_tokenize(reference)
    candidate_tokens = nltk.word_tokenize(candidate)
    return sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothie)

# ROUGE 계산 함수
def calculate_rouge(reference, candidate):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, candidate)
    return scores

# F1-score 계산 함수
def calculate_f1(reference, candidate):
    ref_tokens = nltk.word_tokenize(reference)
    cand_tokens = nltk.word_tokenize(candidate)
    ref_set = set(ref_tokens)
    cand_set = set(cand_tokens)
    
    common_tokens = ref_set.intersection(cand_tokens)
    true_positives = len(common_tokens)
    
    if true_positives == 0:
        return 0.0
    
    precision = true_positives / len(cand_tokens)
    recall = true_positives / len(ref_tokens)
    
    return 2 * (precision * recall) / (precision + recall)

# 모델 평가
results = {}

for model, outputs in model_outputs.items():
    bleu_scores = []
    rouge_scores = {'rouge1': [], 'rouge2': [], 'rougeL': []}
    f1_scores = []
    
    for ref, out in zip(true_texts, outputs):
        bleu_scores.append(calculate_bleu(ref, out))
        rouge_score = calculate_rouge(ref, out)
        for key in rouge_scores:
            rouge_scores[key].append(rouge_score[key].fmeasure)
        f1_scores.append(calculate_f1(ref, out))
    
    results[model] = {
        'BLEU': np.mean(bleu_scores),
        'ROUGE-1': np.mean(rouge_scores['rouge1']),
        'ROUGE-2': np.mean(rouge_scores['rouge2']),
        'ROUGE-L': np.mean(rouge_scores['rougeL']),
        'F1-score': np.mean(f1_scores)
    }

# 결과 출력
for model, scores in results.items():
    print(f"Model: {model}")
    for metric, score in scores.items():
        print(f"  {metric}: {score:.4f}")
    print()
