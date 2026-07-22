---
name: huggingface-best
description: '当用户询问如何为某个任务找到最佳、顶级或推荐模型，想知道该使用哪个 AI 模型，或希望按基准分数比较模型时使用。触发词："X 任务的最佳模型"、"我应该用哪个模型做"、"[任务] 的顶级模型"、"我的设备能跑哪个模型"。'
risk: unknown
source: https://github.com/huggingface/skills/tree/main/skills/huggingface-best
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

# HuggingFace 最佳模型查找器
## 使用时机

当用户询问如何为某个任务找到最佳、顶级或推荐模型，想知道该使用哪个 AI 模型，或希望按基准分数比较模型时使用。触发词："X 任务的最佳模型"、"我应该用哪个模型做"、"[任务] 的顶级模型"、"我的设备能跑哪个模型"。


通过查询官方 HF 基准排行榜、补充模型规模数据、过滤能在用户设备上运行的型号，返回一个带基准分数的对比表。

---

## 步骤 1：解析请求

从用户消息中提取：
- **任务**：希望模型做什么（编码、数学/推理、聊天、OCR、RAG/检索、语音识别、图像分类、多模态、Agent 等）
- **设备**：硬件约束（MacBook M 系列 8/16/32/64GB 统一内存，指定显存大小的 RTX GPU，仅 CPU，云端/无限制等）

如果未提及设备，则完全跳过过滤，直接返回表现最好的模型，不考虑规模。如果任务真的含糊不清，则问一个澄清性问题。

### 设备 → 最大参数量上限

当指定设备时，提取其可用内存（Apple Silicon 取统一内存，独立的 GPU 取显存），并应用以下规则：

- **fp16 最大参数量（B）** ≈ 内存（GB）÷ 2
- **Q4 最大参数量（B）** ≈ 内存（GB）× 2

示例：16GB → 8B fp16 / 32B Q4 — 24GB 显存 → 12B fp16 / 48B Q4 — 8GB → 4B fp16 / 16B Q4

---

## 步骤 2：查找相关基准数据集

获取官方 HF 基准的完整列表：

```bash
curl -s -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  "https://huggingface.co/api/datasets?filter=benchmark:official&limit=500" | jq '[.[] | {id, tags, description}]'
```

阅读返回的列表，挑选与用户任务最相关的数据集 —— 在数据集 id、标签、描述三处匹配。凭判断选择，不要局限于 2-3 个。目标是覆盖全面：如果有 5 个基准明显覆盖该任务，就全部使用。

---

## 步骤 3：从排行榜获取顶级模型

针对每个选中的基准数据集：

```bash
curl -s -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  "https://huggingface.co/api/datasets/<namespace>/<repo>/leaderboard" | jq '[.[:15] | .[] | {rank, modelId, value, verified}]'
```

跨所有基准收集模型 ID 与分数。如果某个排行榜返回错误（如 404、401 等），跳过并在输出中注明。

---

## 步骤 4：补充模型元数据

针对前 10-15 个候选模型 ID，获取模型详情。

```bash
# REST API
curl -s -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  "https://huggingface.co/api/models/org/model1" | jq '{safetensors, tags, cardData}'

# CLI (hf-cli)
hf models info org/model1 --json | jq '{safetensors, tags, cardData}'
```

从每个响应中提取：
- **参数量**：`safetensors.total` → 转换为 B（例如 7_241_748_480 → "7.2B"）
- **许可证**：来自模型卡片标签（查找 `license:apache-2.0`、`license:mit` 等）
- 若 `safetensors` 字段缺失，则从模型名称解析规模（查找 "7b"、"8b"、"13b"、"70b"、"72b" 等）

---

## 步骤 5：过滤与排序

**若指定了设备：**
1. 移除超过该设备 fp16 参数量上限的模型
2. 标记那些只能通过 Q4 量化放下的模型（Q4 容量上限约为 fp16 的 4 倍）
3. 如果某个排名很高的模型略微超出预算，则保留并加 "需要 Q4" 备注 —— 不要默默丢弃

**若未提及设备：** 跳过所有规模过滤，直接按基准分数排序。

然后：按基准分数（降序）排序，保留前 5-8 个模型。

如果闭源模型（GPT-4、Claude、Gemini）出现在排行榜上，也一并包含，但标记为 "仅 API / 无法自托管"。如果用户明确要求只要本地/开源模型，则排除。

---

## 步骤 6：输出

### 对比表

```markdown
| # | Model | Params | [Benchmark 1] | [Benchmark 2] | License | On device |
|---|-------|--------|--------------|--------------|---------|-----------|
| ⭐1 | [org/name](https://huggingface.co/org/name) | 7B | 85.2% | — | Apache 2.0 | Yes (fp16) |
| 2 | [org/name](https://huggingface.co/org/name) | 13B | 83.1% | 71.5% | MIT | Q4 only |
| 3 | [org/name](https://huggingface.co/org/name) | 70B | 90.0% | 81.0% | Llama | Too large |
```

- 将模型名称链接到 `https://huggingface.co/<model_id>`
- 模型未参与评测的基准用 `—` 占位
- 用 ⭐ 标记最推荐的模型
- "On device" 取值：`Yes (fp16)`、`Q4 only`、`Too large`、`API only`

### 后续追问

展示完表格后，询问用户："是否想运行 **[最推荐的模型]**？"

如果用户同意，再询问其偏好：
- **本地运行** —— 若尚未了解设备信息则询问，然后给出对应的部署说明
- **在 HF Jobs 上运行** —— 引导至 HF Jobs 文档：https://huggingface.co/docs/huggingface_hub/en/guides/jobs

---

## 错误处理

- **未找到排行榜**：跳过，在输出中注明 "leaderboard unavailable"
- **模型缺失 hub_repo_details**：回退到从模型名称解析规模
- **该任务未找到任何基准**：使用上文的精选后备表，或尝试 `hub_repo_search` 并按 `trendingScore` 排序、`filters=["<task>"]` 过滤
- **所有排行榜都失败**：回退到 `hub_repo_search` 搜索带该任务标签的热门模型，并注明结果按热度而非基准分数排序

## 局限性

- 仅当任务明确匹配其上游产品或 API 范围时才使用此技能。
- 在执行变更前，命令、API 行为、价格、配额、凭据和部署效果都要对照当前官方文档进行核对。
- 不要将生成的示例视为环境特定测试、安全审查或用户对破坏性/高成本操作的审批的替代品。
