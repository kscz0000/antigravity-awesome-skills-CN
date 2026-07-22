---
name: bdistill-knowledge-extraction
description: "从 AI 模型中提取结构化领域知识，支持会话内提取或通过 Ollama 从本地开源模型提取，无需 API 密钥。当用户要求'提取知识'、'知识蒸馏'、'领域知识提取'、'bdistill'时使用。"
category: ai-research
risk: safe
source: community
date_added: "2026-03-20"
author: FrancyJGLisboa
tags: [ai, knowledge-extraction, domain-specific, data-moat, mcp, reference-data]
tools: [claude, cursor, codex, copilot]
---

# 知识提取

从任意 AI 模型中提取结构化、带质量评分的领域知识——会话内从闭源模型提取（无需 API 密钥），或通过 Ollama 从本地开源模型提取。

## 概述

bdistill 将你的 AI 订阅会话转化为持续积累的知识库。智能体回答针对性的领域问题，bdistill 对回答进行结构化和质量评分，输出累积为可搜索、可导出的参考数据集。

对抗模式会质疑智能体的断言——强制提供证据、纠正错误、承认局限——从而产出经过验证的知识条目。

## 何时使用此技能

- 需要任意领域的结构化参考数据时（医疗、法律、金融、网络安全）
- 构建查找表、问答数据集或研究语料库时
- 为传统 ML 模型生成训练数据时（回归、分类——不是竞争性 LLM）
- 需要跨模型的领域知识对比时

## 工作原理

### 步骤 1：安装

```bash
pip install bdistill
claude mcp add bdistill -- bdistill-mcp   # Claude Code
```

### 步骤 2：会话内提取知识

```
/distill medical cardiology                    # 预设领域
/distill --custom kubernetes docker helm       # 自定义术语
/distill --adversarial medical                 # 带对抗验证
```

### 步骤 3：搜索、导出、积累

```bash
bdistill kb list                               # 显示所有领域
bdistill kb search "atrial fibrillation"       # 关键词搜索
bdistill kb export -d medical -f csv           # 导出为电子表格
bdistill kb export -d medical -f markdown      # 可读知识文档
```

## 输出格式

结构化参考 JSONL——不是训练数据：

```json
{
  "question": "What causes myocardial infarction?",
  "answer": "Myocardial infarction results from acute coronary artery occlusion...",
  "domain": "medical",
  "category": "cardiology",
  "tags": ["mechanistic", "evidence-based"],
  "quality_score": 0.73,
  "confidence": 1.08,
  "validated": true,
  "source_model": "Claude Sonnet 4"
}
```

## 表格型 ML 数据生成

为传统 ML 模型生成结构化训练数据：

```
/schema sepsis | hr:float, bp:float, temp:float, wbc:float | risk:category[low,moderate,high,critical]
```

导出为 CSV，可直接用于 pandas/sklearn。每行追踪 source_model，支持跨模型分析。

## 本地模型提取（Ollama）

用于本地运行的开源模型：

```bash
# Install Ollama from https://ollama.com
ollama serve
ollama pull qwen3:4b

bdistill extract --domain medical --model qwen3:4b
```

## 安全与注意事项

- 会话内提取使用现有订阅——无需额外 API 密钥
- 本地提取完全通过 Ollama 在本机运行
- 不向外部服务发送数据
- 输出是参考数据，不是 LLM 训练格式

## 相关技能

- `@bdistill-behavioral-xray` - 透视模型的行为模式

## 局限性

- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
