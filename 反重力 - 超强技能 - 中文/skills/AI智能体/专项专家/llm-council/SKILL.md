---
name: llm-council
description: "运行 Fireworks 托管的开源权重模型委员会，比较多个模型的响应并综合出最终答案。触发词：LLM委员会、模型委员会、多模型审议、Fireworks AI委员会、council、多模型对比、模型协商"
allowed-tools: Read, Write, Bash, AskUserQuestion
category: "ai-agents"
risk: "safe"
source: "official"
source_repo: "dair-ai/dair-academy-plugins"
source_type: "official"
date_added: "2026-06-19"
author: "DAIR.AI"
license: "MIT"
license_source: "https://github.com/dair-ai/dair-academy-plugins/blob/main/README.md#license"
tags:
  - dair-academy
  - ai
  - workflow
tools:
  - claude-code
  - codex-cli
  - cursor
---

# LLM 委员会（Fireworks AI）

## 何时使用

当用户请求匹配此工作流时使用：使用此技能执行其文档中描述的工作流。


_来源：[dair-ai/dair-academy-plugins](https://github.com/dair-ai/dair-academy-plugins)（MIT）。_

本技能实现了 Karpathy 的 LLM Council 概念，即多个开源权重 LLM 对一个查询进行审议，完全由 Fireworks AI 驱动：

1. **阶段 1**：所有模型独立响应查询（并行）
2. **阶段 2**：模型对彼此的匿名响应进行排名
3. **阶段 3**：主席 LLM 综合出最终答案

所有推理通过 **Fireworks AI** 使用开源权重模型运行。Fireworks 的速度和定价使得在其他提供商上缓慢或昂贵的多模型审议变得实际可行。

## 关键规则

1. **始终使用 AskUserQuestion** 让用户选择委员会模型（多选）和主席模型
2. **始终将原始响应保存到文件** — 绝不摘要或截断 API 输出
3. **始终展示完全透明** — 显示所有单独响应、所有排名以及最终综合结果
4. **绝不跳过排名阶段** — 它是委员会审议过程的核心
5. **从文件读取以展示** — 确保内容未经修改地展示
6. **始终在阶段 3 完成后向用户显示最终输出**

## 预检

在运行任何阶段之前，验证 Fireworks API 密钥是否已设置：

```bash
if [ -z "$FIREWORKS_API_KEY" ]; then
  echo "ERROR: FIREWORKS_API_KEY is not set."
  echo "Create a Fireworks AI account at: https://fireworks.ai/"
  echo "Then export it in your shell profile (~/.zshrc or ~/.bashrc):"
  echo '  export FIREWORKS_API_KEY="your_api_key_here"'
  exit 1
fi
echo "FIREWORKS_API_KEY is set."
```

## 可用模型

通过 AskUserQuestion 向用户展示这些选项（多选）：

| 模型 | Fireworks ID | 提供方 |
|------|-------------|--------|
| GLM 5 | accounts/fireworks/models/glm-5 | Z.ai |
| DeepSeek V3.1 | accounts/fireworks/models/deepseek-v3p1 | DeepSeek |
| DeepSeek V3.2 | accounts/fireworks/models/deepseek-v3p2 | DeepSeek |
| MiniMax M2.1 | accounts/fireworks/models/minimax-m2p1 | MiniMax |
| Kimi K2.5 | accounts/fireworks/models/kimi-k2p5 | Moonshot |
| Qwen3 235B | accounts/fireworks/models/qwen3-235b-a22b | Alibaba |
| Llama 4 Maverick | accounts/fireworks/models/llama4-maverick-instruct-basic | Meta |

## 工作流

### 步骤 1：收集用户输入

使用 AskUserQuestion 获取：
1. 委员会的查询/问题（或从对话中接受）
2. 包含哪些模型（多选，推荐 3-5 个模型）
3. 哪个模型应担任主席（单选）

注意：AskUserQuestion 每个问题最多支持 4 个选项。由于有 7 个模型，需将模型选择拆分为两个问题，或展示最热门的 4 个并让用户输入"其他"来选择其余模型。较好的默认方式是在第一个问题中展示 4 个模型，并注明其余模型可通过"其他"选择。根据多样性轮换展示哪些模型。

模型选择的 AskUserQuestion 示例（展示 4 个，提及其他）：
```
question: "Which models should participate in the LLM Council? (Also available via Other: Llama 4 Maverick, Qwen3 235B, GLM 5)"
header: "Models"
multiSelect: true
options:
  - label: "DeepSeek V3.2"
    description: "DeepSeek's newest and most capable model"
  - label: "MiniMax M2.1"
    description: "MiniMax's strong open-weight model"
  - label: "Kimi K2.5"
    description: "Moonshot's strong open-weight model"
  - label: "DeepSeek V3.1"
    description: "DeepSeek's proven reasoning model"
```

主席选择的 AskUserQuestion 示例：
```
question: "Which model should be the Chairman (synthesizes the final answer)?"
header: "Chairman"
multiSelect: false
options:
  - label: "DeepSeek V3.2 (Recommended)"
    description: "Newest DeepSeek, strong at comprehensive analysis"
  - label: "GLM 5"
    description: "Strong reasoning for synthesis"
  - label: "Kimi K2.5"
    description: "Strong at structured synthesis"
  - label: "MiniMax M2.1"
    description: "Strong open-weight model for synthesis"
```

### 模型名称到 ID 的映射

使用此映射将用户选择转换为 Fireworks 模型 ID：

```python
MODEL_MAP = {
    "GLM 5": "accounts/fireworks/models/glm-5",
    "DeepSeek V3.1": "accounts/fireworks/models/deepseek-v3p1",
    "DeepSeek V3.2": "accounts/fireworks/models/deepseek-v3p2",
    "MiniMax M2.1": "accounts/fireworks/models/minimax-m2p1",
    "Kimi K2.5": "accounts/fireworks/models/kimi-k2p5",
    "Qwen3 235B": "accounts/fireworks/models/qwen3-235b-a22b",
    "Llama 4 Maverick": "accounts/fireworks/models/llama4-maverick-instruct-basic",
}
```

### 步骤 2：运行阶段 1 — 独立响应

收集输入后，运行此脚本以并行获取所有选中模型的响应：

```bash
QUERY="USER_QUERY_HERE"
MODELS='["accounts/fireworks/models/glm-5", "accounts/fireworks/models/deepseek-v3p1"]'

python3 << 'PYEOF'
import os
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

FIREWORKS_API_KEY = os.environ.get("FIREWORKS_API_KEY")
API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"

QUERY = os.environ.get("QUERY", "")
MODELS = json.loads(os.environ.get("MODELS", "[]"))

# Create session directory
timestamp = time.strftime("%Y%m%d-%H%M%S")
SESSION_DIR = f"/tmp/llm-council/{timestamp}"
os.makedirs(SESSION_DIR, exist_ok=True)

# Save config
config = {"query": QUERY, "models": MODELS, "timestamp": timestamp}
with open(f"{SESSION_DIR}/config.json", "w") as f:
    json.dump(config, f, indent=2)

def call_model(model_id, query):
    """Call a single model via Fireworks AI"""
    try:
        start = time.time()
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {FIREWORKS_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model_id,
                "messages": [
                    {"role": "system", "content": "You are participating in an LLM council deliberation. Provide your best, most thoughtful response to the query. Be comprehensive but focused."},
                    {"role": "user", "content": query}
                ],
                "max_tokens": 4000,
                "temperature": 1
            },
            timeout=120
        )
        response.raise_for_status()
        elapsed = time.time() - start
        data = response.json()
        usage = data.get("usage", {})
        return {
            "success": True,
            "content": data["choices"][0]["message"]["content"],
            "model": model_id,
            "latency_seconds": round(elapsed, 2),
            "tokens": {
                "prompt": usage.get("prompt_tokens", 0),
                "completion": usage.get("completion_tokens", 0),
                "total": usage.get("total_tokens", 0)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "content": f"[ERROR: {str(e)}]",
            "model": model_id,
            "latency_seconds": 0,
            "tokens": {"prompt": 0, "completion": 0, "total": 0}
        }

print(f"\n{'='*60}")
print("PHASE 1: Collecting Individual Responses")
print(f"{'='*60}")
print(f"Query: {QUERY[:200]}...")
print(f"Models: {', '.join([m.split('/')[-1] for m in MODELS])}")
print(f"Session: {SESSION_DIR}")
print()

# Parallel execution
results = {}
with ThreadPoolExecutor(max_workers=len(MODELS)) as executor:
    futures = {executor.submit(call_model, m, QUERY): m for m in MODELS}
    for future in as_completed(futures):
        model = futures[future]
        result = future.result()
        results[model] = result
        status = "OK" if result["success"] else "FAILED"
        latency = f"{result['latency_seconds']}s" if result["success"] else "N/A"
        print(f"  [{status}] {model.split('/')[-1]} ({latency})")

# Save raw results
with open(f"{SESSION_DIR}/phase1_responses.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nPhase 1 complete. Results saved to: {SESSION_DIR}/phase1_responses.json")
print(f"SESSION_DIR={SESSION_DIR}")
PYEOF
```

### 步骤 3：运行阶段 2 — 跨模型排名

每个模型审阅并对阶段 1 的匿名响应进行排名：

```bash
SESSION_DIR="/tmp/llm-council/TIMESTAMP_HERE"

python3 << 'PYEOF'
import os
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

FIREWORKS_API_KEY = os.environ.get("FIREWORKS_API_KEY")
API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
SESSION_DIR = os.environ.get("SESSION_DIR")

# Load Phase 1 results
with open(f"{SESSION_DIR}/config.json") as f:
    config = json.load(f)
with open(f"{SESSION_DIR}/phase1_responses.json") as f:
    phase1_results = json.load(f)

QUERY = config["query"]
MODELS = config["models"]

# Create anonymized mapping
labels = ["A", "B", "C", "D", "E", "F", "G"][:len(MODELS)]
model_to_label = dict(zip(MODELS, labels))
label_to_model = {v: k for k, v in model_to_label.items()}

# Format anonymized responses
anonymized_responses = []
for model_id in MODELS:
    label = model_to_label[model_id]
    content = phase1_results[model_id]["content"]
    anonymized_responses.append(f"=== Response {label} ===\n{content}")

anonymized_text = "\n\n".join(anonymized_responses)

def get_rankings(model_id, query, anonymized, own_label):
    """Get rankings from a single model"""
    ranking_prompt = f"""You are evaluating responses from multiple AI models to this query:

QUERY: {query}

Here are the anonymized responses:

{anonymized}

Please rank these responses from BEST to WORST. For each ranking:
1. State the response letter (A, B, C, etc.)
2. Give a brief reason (1-2 sentences)
3. You may skip ranking your own response (labeled {own_label}) or rank it fairly

Format your response EXACTLY as:
RANKINGS:
1. [Letter] - [Brief reason]
2. [Letter] - [Brief reason]
3. [Letter] - [Brief reason]
..."""

    try:
        start = time.time()
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {FIREWORKS_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model_id,
                "messages": [
                    {"role": "system", "content": f"You are ranking AI responses objectively. Your own response is labeled '{own_label}'."},
                    {"role": "user", "content": ranking_prompt}
                ],
                "max_tokens": 1000,
                "temperature": 1
            },
            timeout=90
        )
        response.raise_for_status()
        elapsed = time.time() - start
        return {
            "success": True,
            "content": response.json()["choices"][0]["message"]["content"],
            "model": model_id,
            "latency_seconds": round(elapsed, 2)
        }
    except Exception as e:
        return {
            "success": False,
            "content": f"[ERROR: {str(e)}]",
            "model": model_id,
            "latency_seconds": 0
        }

print(f"\n{'='*60}")
print("PHASE 2: Cross-Model Ranking")
print(f"{'='*60}")
print(f"Label mapping: {json.dumps({v: k.split('/')[-1] for k, v in model_to_label.items()})}")
print()

# Collect rankings from all models in parallel
rankings = {}
with ThreadPoolExecutor(max_workers=len(MODELS)) as executor:
    futures = {
        executor.submit(get_rankings, mid, QUERY, anonymized_text, model_to_label[mid]): mid
        for mid in MODELS
    }
    for future in as_completed(futures):
        model = futures[future]
        result = future.result()
        rankings[model] = result
        status = "OK" if result["success"] else "FAILED"
        latency = f"{result['latency_seconds']}s" if result["success"] else "N/A"
        print(f"  [{status}] {model.split('/')[-1]} ({latency})")

# Save rankings
output = {
    "label_mapping": label_to_model,
    "model_to_label": model_to_label,
    "rankings": rankings
}
with open(f"{SESSION_DIR}/phase2_rankings.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nPhase 2 complete. Rankings saved to: {SESSION_DIR}/phase2_rankings.json")
PYEOF
```

### 步骤 4：运行阶段 3 — 主席综合

主席模型接收所有响应和排名，然后生成最终综合结果：

```bash
SESSION_DIR="/tmp/llm-council/TIMESTAMP_HERE"
CHAIRMAN_MODEL="accounts/fireworks/models/glm-5"

python3 << 'PYEOF'
import os
import json
import requests
import time

FIREWORKS_API_KEY = os.environ.get("FIREWORKS_API_KEY")
API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
SESSION_DIR = os.environ.get("SESSION_DIR")
CHAIRMAN_MODEL = os.environ.get("CHAIRMAN_MODEL")

# Load all previous results
with open(f"{SESSION_DIR}/config.json") as f:
    config = json.load(f)
with open(f"{SESSION_DIR}/phase1_responses.json") as f:
    phase1 = json.load(f)
with open(f"{SESSION_DIR}/phase2_rankings.json") as f:
    phase2 = json.load(f)

QUERY = config["query"]
label_to_model = phase2["label_mapping"]
model_to_label = phase2["model_to_label"]

# Format responses with model names revealed
responses_text = []
for model_id, result in phase1.items():
    label = model_to_label.get(model_id, "?")
    model_name = model_id.split("/")[-1]
    responses_text.append(f"=== {label}: {model_name} ===\n{result['content']}")

# Format rankings
rankings_text = []
for model_id, result in phase2["rankings"].items():
    model_name = model_id.split("/")[-1]
    rankings_text.append(f"[{model_name}'s Rankings]\n{result['content']}")

synthesis_prompt = f"""You are the Chairman of an LLM Council. Your task is to synthesize the best possible answer from multiple AI responses.

ORIGINAL QUERY:
{QUERY}

INDIVIDUAL RESPONSES:
{chr(10).join(responses_text)}

MODEL RANKINGS:
{chr(10).join(rankings_text)}

As Chairman, produce a FINAL SYNTHESIS that:
1. Incorporates the strongest elements from the best-ranked responses
2. Resolves any contradictions between responses
3. Addresses aspects that multiple models agreed on
4. Corrects any errors identified through cross-ranking
5. Provides the most complete, accurate, and helpful answer

Begin your synthesis:"""

print(f"\n{'='*60}")
print("PHASE 3: Chairman Synthesis")
print(f"{'='*60}")
print(f"Chairman: {CHAIRMAN_MODEL.split('/')[-1]}")
print()

try:
    start = time.time()
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {FIREWORKS_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": CHAIRMAN_MODEL,
            "messages": [
                {"role": "system", "content": "You are the Chairman of an LLM Council. Synthesize multiple AI perspectives into a definitive, comprehensive response."},
                {"role": "user", "content": synthesis_prompt}
            ],
            "max_tokens": 4000,
            "temperature": 1
        },
        timeout=180
    )
    response.raise_for_status()
    elapsed = time.time() - start
    synthesis = response.json()["choices"][0]["message"]["content"]

    with open(f"{SESSION_DIR}/phase3_synthesis.txt", "w") as f:
        f.write(synthesis)

    print(f"Phase 3 complete ({elapsed:.2f}s). Synthesis saved to: {SESSION_DIR}/phase3_synthesis.txt")

except Exception as e:
    print(f"ERROR: {e}")
    synthesis = f"[ERROR: {str(e)}]"
    with open(f"{SESSION_DIR}/phase3_synthesis.txt", "w") as f:
        f.write(synthesis)

# Update config with chairman
config["chairman"] = CHAIRMAN_MODEL
with open(f"{SESSION_DIR}/config.json", "w") as f:
    json.dump(config, f, indent=2)
PYEOF
```

### 步骤 5：展示完整结果

读取所有保存的文件并展示完整的委员会审议过程：

```bash
SESSION_DIR="/tmp/llm-council/TIMESTAMP_HERE"

python3 << 'PYEOF'
import os
import json

SESSION_DIR = os.environ.get("SESSION_DIR")

# Load all data
with open(f"{SESSION_DIR}/config.json") as f:
    config = json.load(f)
with open(f"{SESSION_DIR}/phase1_responses.json") as f:
    phase1 = json.load(f)
with open(f"{SESSION_DIR}/phase2_rankings.json") as f:
    phase2 = json.load(f)
with open(f"{SESSION_DIR}/phase3_synthesis.txt") as f:
    synthesis = f.read()

model_to_label = phase2["model_to_label"]
label_to_model = phase2["label_mapping"]

# Build formatted output
output = []
output.append("=" * 70)
output.append("                  LLM COUNCIL DELIBERATION")
output.append("                  Powered by Fireworks AI")
output.append("=" * 70)
output.append("")
output.append(f"QUERY: {config['query']}")
output.append(f"COUNCIL: {', '.join([m.split('/')[-1] for m in config['models']])}")
output.append(f"CHAIRMAN: {config.get('chairman', 'N/A').split('/')[-1]}")
output.append("")

# Phase 1: Individual Responses
output.append("-" * 70)
output.append("                 PHASE 1: INDIVIDUAL RESPONSES")
output.append("-" * 70)
output.append("")

for model_id, result in phase1.items():
    model_name = model_id.split("/")[-1]
    label = model_to_label.get(model_id, "?")
    latency = result.get("latency_seconds", "N/A")
    tokens = result.get("tokens", {})
    output.append(f"[{label}] {model_name} (latency: {latency}s, tokens: {tokens.get('total', 'N/A')})")
    output.append("-" * 40)
    output.append(result["content"])
    output.append("")

# Phase 2: Cross-Model Rankings
output.append("-" * 70)
output.append("                 PHASE 2: CROSS-MODEL RANKINGS")
output.append("-" * 70)
output.append("")
output.append(f"Label mapping: {json.dumps({v: k.split('/')[-1] for k, v in model_to_label.items()}, indent=2)}")
output.append("")

for model_id, result in phase2["rankings"].items():
    model_name = model_id.split("/")[-1]
    output.append(f"[{model_name}'s Rankings]")
    output.append(result["content"])
    output.append("")

# Phase 3: Chairman Synthesis
output.append("-" * 70)
output.append("                 PHASE 3: CHAIRMAN'S SYNTHESIS")
output.append("-" * 70)
output.append("")
chairman_name = config.get("chairman", "Chairman").split("/")[-1]
output.append(f"[{chairman_name} - Chairman]")
output.append("")
output.append(synthesis)
output.append("")
output.append("=" * 70)
output.append(f"Session files: {SESSION_DIR}/")

# Save formatted output
final_output = "\n".join(output)
with open(f"{SESSION_DIR}/final_output.md", "w") as f:
    f.write(final_output)

print(final_output)
print(f"\nFull output saved to: {SESSION_DIR}/final_output.md")
PYEOF
```

## 重要说明

1. **会话目录**：每次运行在 `/tmp/llm-council/{timestamp}/` 中创建唯一的会话
2. **原始数据保留**：所有 API 响应原样保存到 JSON 文件，确保完全透明
3. **费用**：Fireworks 按令牌计费。模型越多、查询越长，费用越高。查看当前定价：https://fireworks.ai/pricing
4. **延迟追踪**：每次 API 调用追踪延迟，可直观感受 Fireworks 的速度
5. **令牌用量**：阶段 1 的响应包含令牌计数，便于成本感知
6. **速率限制**：如触发速率限制，稍等后重试
7. **模型可用性**：查看 https://app.fireworks.ai/ 了解当前模型状态

## 设置

1. 在 https://fireworks.ai/ 创建 Fireworks AI 账户，并从控制面板获取 API 密钥
2. 在 shell 配置文件中导出：
   ```bash
   export FIREWORKS_API_KEY="your_api_key_here"
   ```
3. 重启终端或运行 `source ~/.zshrc`
4. 当你需要多个开源权重 AI 视角来回答问题时，调用此技能


## 限制

- 需要工作流中提及的上游工具、账户、API 密钥或本地设置。
- 未经用户明确批准，不授权执行破坏性、生产环境、付费或外部消息操作。
- 在将生成的产物或建议视为最终结果之前，请对照用户的真实来源进行验证。
