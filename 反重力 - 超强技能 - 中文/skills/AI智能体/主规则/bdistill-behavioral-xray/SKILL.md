---
name: bdistill-behavioral-xray
description: "透视任意 AI 模型的行为模式——拒绝边界、幻觉倾向、推理风格、格式默认值。无需 API 密钥。当用户要求'行为透视''模型行为分析''X-Ray 行为探测'时使用。"
category: ai-testing
risk: safe
source: community
date_added: "2026-03-20"
author: FrancyJGLisboa
tags: [ai, testing, behavioral-analysis, model-evaluation, red-team, compliance, mcp]
tools: [claude, cursor, codex, copilot]
---

# 行为透视

系统化探测 AI 模型的行为模式，生成可视化报告。AI 智能体探测*自身*——无需 API 密钥或外部配置。

## 概述

bdistill 的行为透视功能运行 30 道精心设计的探测问题，覆盖 6 个维度，自动为每个响应标注行为元数据，并将结果编译为带雷达图和可操作洞察的样式化 HTML 报告。

用于在构建前理解模型、为任务选型比较模型、或追踪行为漂移。

## 何时使用此技能

- 想了解 AI 模型的真实行为（而非它声称的行为）时使用
- 为特定任务在多个模型间做选择时使用
- 调试意外的拒绝、幻觉或格式问题时使用
- 合规审计时使用——记录部署边界上的模型行为
- 红队评估时使用——跨安全维度系统化映射边界

## 工作原理

### 第 1 步：安装

```bash
pip install bdistill
claude mcp add bdistill -- bdistill-mcp   # Claude Code
```

其他工具请在项目配置中将 bdistill-mcp 添加为 MCP 服务器。

### 第 2 步：运行探测

在 Claude Code 中：
```
/xray                          # 完整行为探测（30 道问题）
/xray --dimensions refusal     # 仅探测一个维度
/xray-report                   # 从已完成的探测生成报告
```

在任何支持 MCP 的工具中：
```
"X-ray your behavioral patterns"
"Test your refusal boundaries"
"Generate a behavioral report"
```

## 探测维度

| 维度 | 测量内容 |
|------|---------|
| **tool_use** | 何时调用工具 vs. 从知识作答？ |
| **refusal** | 安全边界划在哪里？是否过度拒绝？ |
| **formatting** | 列表还是散文？代码块？长度校准？ |
| **reasoning** | 是否展示思维链？能否应对陷阱题？ |
| **persona** | 身份、语气匹配、面对敌意时的镇定度 |
| **grounding** | 幻觉抵抗力、捏造陷阱、知识边界 |

## 输出

样式化 HTML 报告，展示：
- 拒绝率、模糊率、思维链使用率
- 各维度细分及柱状图
- 带行为标签的典型响应示例
- 可操作洞察（如"你已有 85% 的时间展示 CoT，无需额外提示"）

## 最佳实践

- 诚实回答探测问题——真实行为数据才有价值
- 定期对同一模型运行探测，追踪行为漂移
- 跨模型对比报告，做出明智的选型决策
- 结合对抗性知识提取（`/distill --adversarial`）与行为探测，完成完整的模型画像

## 相关技能

- `@bdistill-knowledge-extraction` - 从任意 AI 模型提取结构化领域知识

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 输出不能替代针对具体环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
