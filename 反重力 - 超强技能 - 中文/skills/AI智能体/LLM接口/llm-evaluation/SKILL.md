---
name: llm-evaluation
description: "掌握 LLM 应用的全面评估策略，涵盖自动化指标、人工评估和 A/B 测试。当用户要求'评估LLM'、'LLM评测'、'模型评估'、'LLM evaluation'、'评估指标'、'A/B测试模型'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# LLM Evaluation

掌握 LLM 应用的全面评估策略，涵盖自动化指标、人工评估和 A/B 测试。

## 何时不使用此技能

- 任务与 LLM 评估无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，打开 `resources/implementation-playbook.md`。

## 何时使用此技能

- 系统化衡量 LLM 应用性能
- 比较不同模型或提示词
- 部署前检测性能回归
- 验证提示词变更带来的改进
- 建立对生产系统的信心
- 建立基线并随时间追踪进展
- 调试异常的模型行为

## 核心评估类型

### 1. 自动化指标
快速、可重复、可扩展的评估，基于计算得分。

**文本生成：**
- **BLEU**：N-gram 重叠度（翻译）
- **ROUGE**：面向召回率（摘要）
- **METEOR**：语义相似度
- **BERTScore**：基于嵌入的相似度
- **Perplexity**：语言模型置信度

**分类：**
- **Accuracy**：正确率
- **Precision/Recall/F1**：按类别衡量的性能
- **Confusion Matrix**：错误模式
- **AUC-ROC**：排序质量

**检索（RAG）：**
- **MRR**：平均倒数排名
- **NDCG**：归一化折损累积增益
- **Precision@K**：前 K 个中的相关结果
- **Recall@K**：前 K 个中的覆盖度

### 2. 人工评估
针对难以自动化的质量维度进行人工评定。

**维度：**
- **Accuracy**：事实正确性
- **Coherence**：逻辑连贯性
- **Relevance**：是否回答了问题
- **Fluency**：语言自然度
- **Safety**：无有害内容
- **Helpfulness**：对用户有用

### 3. LLM-as-Judge
用更强的 LLM 评估较弱模型的输出。

**方法：**
- **Pointwise**：对单个响应打分
- **Pairwise**：比较两个响应
- **Reference-based**：与黄金标准对比
- **Reference-free**：无真实标签评判

## 快速开始

```python
from llm_eval import EvaluationSuite, Metric

# Define evaluation suite
suite = EvaluationSuite([
    Metric.accuracy(),
    Metric.bleu(),
    Metric.bertscore(),
    Metric.custom(name="groundedness", fn=check_groundedness)
])

# Prepare test cases
test_cases = [
    {
        "input": "What is the capital of France?",
        "expected": "Paris",
        "context": "France is a country in Europe. Paris is its capital."
    },
    # ... more test cases
]

# Run evaluation
results = suite.evaluate(
    model=your_model,
    test_cases=test_cases
)

print(f"Overall Accuracy: {results.metrics['accuracy']}")
print(f"BLEU Score: {results.metrics['bleu']}")
```

## 自动化指标实现

### BLEU 分数
```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def calculate_bleu(reference, hypothesis):
    """Calculate BLEU score between reference and hypothesis."""
    smoothie = SmoothingFunction().method4

    return sentence_bleu(
        [reference.split()],
        hypothesis.split(),
        smoothing_function=smoothie
    )

# Usage
bleu = calculate_bleu(
    reference="The cat sat on the mat",
    hypothesis="A cat is sitting on the mat"
)
```

### ROUGE 分数
```python
from rouge_score import rouge_scorer

def calculate_rouge(reference, hypothesis):
    """Calculate ROUGE scores."""
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)

    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure
    }
```

### BERTScore
```python
from bert_score import score

def calculate_bertscore(references, hypotheses):
    """Calculate BERTScore using pre-trained BERT."""
    P, R, F1 = score(
        hypotheses,
        references,
        lang='en',
        model_type='microsoft/deberta-xlarge-mnli'
    )

    return {
        'precision': P.mean().item(),
        'recall': R.mean().item(),
        'f1': F1.mean().item()
    }
```

### 自定义指标
```python
def calculate_groundedness(response, context):
    """Check if response is grounded in provided context."""
    # Use NLI model to check entailment
    from transformers import pipeline

    nli = pipeline("text-classification", model="microsoft/deberta-large-mnli")

    result = nli(f"{context} [SEP] {response}")[0]

    # Return confidence that response is entailed by context
    return result['score'] if result['label'] == 'ENTAILMENT' else 0.0

def calculate_toxicity(text):
    """Measure toxicity in generated text."""
    from detoxify import Detoxify

    results = Detoxify('original').predict(text)
    return max(results.values())  # Return highest toxicity score

def calculate_factuality(claim, knowledge_base):
    """Verify factual claims against knowledge base."""
    # Implementation depends on your knowledge base
    # Could use retrieval + NLI, or fact-checking API
    pass
```

## LLM-as-Judge 模式

### 单输出评估
```python
def llm_judge_quality(response, question):
    """Use GPT-5 to judge response quality."""
    prompt = f"""Rate the following response on a scale of 1-10 for:
1. Accuracy (factually correct)
2. Helpfulness (answers the question)
3. Clarity (well-written and understandable)

Question: {question}
Response: {response}

Provide ratings in JSON format:
{{
  "accuracy": <1-10>,
  "helpfulness": <1-10>,
  "clarity": <1-10>,
  "reasoning": "<brief explanation>"
}}
"""

    result = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(result.choices[0].message.content)
```

### 成对比较
```python
def compare_responses(question, response_a, response_b):
    """Compare two responses using LLM judge."""
    prompt = f"""Compare these two responses to the question and determine which is better.

Question: {question}

Response A: {response_a}

Response B: {response_b}

Which response is better and why? Consider accuracy, helpfulness, and clarity.

Answer with JSON:
{{
  "winner": "A" or "B" or "tie",
  "reasoning": "<explanation>",
  "confidence": <1-10>
}}
"""

    result = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(result.choices[0].message.content)
```

## 人工评估框架

### 标注指南
```python
class AnnotationTask:
    """Structure for human annotation task."""

    def __init__(self, response, question, context=None):
        self.response = response
        self.question = question
        self.context = context

    def get_annotation_form(self):
        return {
            "question": self.question,
            "context": self.context,
            "response": self.response,
            "ratings": {
                "accuracy": {
                    "scale": "1-5",
                    "description": "Is the response factually correct?"
                },
                "relevance": {
                    "scale": "1-5",
                    "description": "Does it answer the question?"
                },
                "coherence": {
                    "scale": "1-5",
                    "description": "Is it logically consistent?"
                }
            },
            "issues": {
                "factual_error": False,
                "hallucination": False,
                "off_topic": False,
                "unsafe_content": False
            },
            "feedback": ""
        }
```

### 评分者间一致性
```python
from sklearn.metrics import cohen_kappa_score

def calculate_agreement(rater1_scores, rater2_scores):
    """Calculate inter-rater agreement."""
    kappa = cohen_kappa_score(rater1_scores, rater2_scores)

    interpretation = {
        kappa < 0: "Poor",
        kappa < 0.2: "Slight",
        kappa < 0.4: "Fair",
        kappa < 0.6: "Moderate",
        kappa < 0.8: "Substantial",
        kappa <= 1.0: "Almost Perfect"
    }

    return {
        "kappa": kappa,
        "interpretation": interpretation[True]
    }
```

## A/B 测试

### 统计检验框架
```python
from scipy import stats
import numpy as np

class ABTest:
    def __init__(self, variant_a_name="A", variant_b_name="B"):
        self.variant_a = {"name": variant_a_name, "scores": []}
        self.variant_b = {"name": variant_b_name, "scores": []}

    def add_result(self, variant, score):
        """Add evaluation result for a variant."""
        if variant == "A":
            self.variant_a["scores"].append(score)
        else:
            self.variant_b["scores"].append(score)

    def analyze(self, alpha=0.05):
        """Perform statistical analysis."""
        a_scores = self.variant_a["scores"]
        b_scores = self.variant_b["scores"]

        # T-test
        t_stat, p_value = stats.ttest_ind(a_scores, b_scores)

        # Effect size (Cohen's d)
        pooled_std = np.sqrt((np.std(a_scores)**2 + np.std(b_scores)**2) / 2)
        cohens_d = (np.mean(b_scores) - np.mean(a_scores)) / pooled_std

        return {
            "variant_a_mean": np.mean(a_scores),
            "variant_b_mean": np.mean(b_scores),
            "difference": np.mean(b_scores) - np.mean(a_scores),
            "relative_improvement": (np.mean(b_scores) - np.mean(a_scores)) / np.mean(a_scores),
            "p_value": p_value,
            "statistically_significant": p_value < alpha,
            "cohens_d": cohens_d,
            "effect_size": self.interpret_cohens_d(cohens_d),
            "winner": "B" if np.mean(b_scores) > np.mean(a_scores) else "A"
        }

    @staticmethod
    def interpret_cohens_d(d):
        """Interpret Cohen's d effect size."""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"
```

## 回归测试

### 回归检测
```python
class RegressionDetector:
    def __init__(self, baseline_results, threshold=0.05):
        self.baseline = baseline_results
        self.threshold = threshold

    def check_for_regression(self, new_results):
        """Detect if new results show regression."""
        regressions = []

        for metric in self.baseline.keys():
            baseline_score = self.baseline[metric]
            new_score = new_results.get(metric)

            if new_score is None:
                continue

            # Calculate relative change
            relative_change = (new_score - baseline_score) / baseline_score

            # Flag if significant decrease
            if relative_change < -self.threshold:
                regressions.append({
                    "metric": metric,
                    "baseline": baseline_score,
                    "current": new_score,
                    "change": relative_change
                })

        return {
            "has_regression": len(regressions) > 0,
            "regressions": regressions
        }
```

## 基准测试

### 运行基准测试
```python
class BenchmarkRunner:
    def __init__(self, benchmark_dataset):
        self.dataset = benchmark_dataset

    def run_benchmark(self, model, metrics):
        """Run model on benchmark and calculate metrics."""
        results = {metric.name: [] for metric in metrics}

        for example in self.dataset:
            # Generate prediction
            prediction = model.predict(example["input"])

            # Calculate each metric
            for metric in metrics:
                score = metric.calculate(
                    prediction=prediction,
                    reference=example["reference"],
                    context=example.get("context")
                )
                results[metric.name].append(score)

        # Aggregate results
        return {
            metric: {
                "mean": np.mean(scores),
                "std": np.std(scores),
                "min": min(scores),
                "max": max(scores)
            }
            for metric, scores in results.items()
        }
```

## 资源

- **references/metrics.md**：综合指标指南
- **references/human-evaluation.md**：标注最佳实践
- **references/benchmarking.md**：标准基准测试
- **references/a-b-testing.md**：统计检验指南
- **references/regression-testing.md**：CI/CD 集成
- **assets/evaluation-framework.py**：完整评估框架
- **assets/benchmark-dataset.jsonl**：示例数据集
- **scripts/evaluate-model.py**：自动化评估运行器

## 最佳实践

1. **多指标并用**：使用多种指标获得全面视角
2. **代表性数据**：在真实、多样的样本上测试
3. **基线对比**：始终与基线性能比较
4. **统计严谨性**：比较时使用适当的统计检验
5. **持续评估**：集成到 CI/CD 流水线
6. **人工验证**：将自动化指标与人工判断结合
7. **错误分析**：调查失败案例以理解薄弱环节
8. **版本控制**：随时间追踪评估结果

## 常见陷阱

- **单一指标执念**：为优化一个指标而牺牲其他指标
- **样本量过小**：从过少的样本中得出结论
- **数据污染**：在训练数据上测试
- **忽略方差**：未考虑统计不确定性
- **指标错配**：使用的指标与业务目标不一致

## 局限性
- 仅在任务明确符合上述范围时使用此技能。
- 输出不能替代针对具体环境的验证、测试或专家评审。
- 如缺少必要输入、权限、安全边界或成功标准，请停下来询问澄清。
