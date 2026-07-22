---
name: tokenwise
description: '面向 Claude Code 的「测量驱动」型模型路由器。按任务类别路由 Haiku/Sonnet/Opus，记录每次路由任务的真实开销（美元），并在信任降本效果前先对更便宜的层级做 A/B 测试。关键词：模型路由、token 优化、成本控制、Claude Code、A/B 测试、测量、Haiku、Sonnet、Opus。'
category: developer-tools
risk: critical
source: community
source_repo: CodeShuX/tokenwise
source_type: community
date_added: "2026-05-12"
author: CodeShuX
tags: [model-routing, token-optimization, cost-reduction, anthropic, haiku, sonnet, opus, claude-code, ab-testing, measurement]
tools: [claude]
license: "MIT"
license_source: "https://github.com/CodeShuX/tokenwise/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# TokenWise — 测量驱动的模型路由器

## 概述

这是一款 Claude Code 技能，可将子任务自动路由到能处理它们的最低价模型（Haiku 做机械工作，Sonnet 做有范围的推理，Opus 仅用于综合），然后把每次路由任务与真实的 token 数和成本一起记录到本地 NDJSON 文件。还附带一个 A/B 测试子命令，让同一任务跨多个模型层级运行并给出质量评分，让路由决策基于真实工作负载得到验证——而不是估算。

Anthropic 自家的缺陷追踪器（Issue #27665）显示，Max 订阅用户 93.8% 的 Claude Code token 流向了 Opus。现有的路由器（claude-router、wshobson、VoltAgent）要么静态钉死模型，要么用"凭感觉"的启发式做路由且不做任何测量。TokenWise 正好补上了"测量"这块缺口。

## 适用场景

- 在不牺牲输出质量的前提下削减 Claude Code 的 token 花费
- 在信任自动路由之前，先验证 Haiku/Sonnet 对某类任务是否"够用"
- 审计 Opus 的 token 究竟被烧在了哪里
- 为财务或成本分摊记录每个会话的成本数据

## 子命令

- `/tokenwise:install` — 带 diff 预览、自动备份和 `--dry-run` 模式的引导式安装器
- `/tokenwise:report` — 按会话统计 token 与成本，并与"全程 Opus"的基线对比
- `/tokenwise:summary [--week|--month|--all]` — 历史聚合数据，带趋势
- `/tokenwise:ab "<task>"` — 对同一任务跨多个层级做 A/B 测试，生成 markdown 对比报告
- `/tokenwise:undo` — 从备份还原 CLAUDE.md / settings.json

## 路由分类法

| 层级 | 模型 | 任务类别 |
|---|---|---|
| 机械操作 | Haiku 4.5 | 文件读取、grep、格式化、重命名、简单编辑、文档查询 |
| 有范围的推理 | Sonnet 4.6 | 单文件重构、限定范围的调研、测试编写 |
| 综合 | Opus 4.7 | 架构决策、多文件重构、安全审查 |

安全上限：

- Haiku 不得再派生子智能体
- 最大派生深度 = 2
- 需要更聪明模型的子智能体必须回到父级——它们不得自行升档
- 字符数 < 100 且无文件上下文的任务直接内联运行（子智能体开销 > 节省）
- 子智能体上下文 > 30k token 时升一档

## 隐私

零遥测。所有日志位于项目本地的 `.tokenwise/log.ndjson`。任务描述在记录前会被截断到 80 字符并剥离文件内容。源码中不存在任何分析上报端点。

## 安装

在任意 Claude Code 会话中：

```
/plugin marketplace add CodeShuX/tokenwise
/plugin install tokenwise@tokenwise
```

随后运行 `/tokenwise:install` 并按引导提示操作。

## 局限性

- token 数与 Anthropic 账单存在约 ±2% 的近似偏差
- A/B 测试模式会消耗额外 token（一次任务 × N 个层级）——这属于有意的一次性验证
- 仅支持 Anthropic（跨厂商请用 LiteLLM 或 OpenRouter）
- 子智能体 `model:` 参数在部分 Claude Code 构建中存在已知的静默失败缺陷——本技能会在安装时探测这一点，若路由功能异常则拒绝继续配置

## 来源

- 仓库：https://github.com/CodeShuX/tokenwise
- 许可证：MIT
- 作者：CodeShuX