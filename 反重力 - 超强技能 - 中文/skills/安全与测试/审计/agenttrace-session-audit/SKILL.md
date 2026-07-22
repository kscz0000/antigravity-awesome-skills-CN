---
name: agenttrace-session-audit
description: "使用 agenttrace 审计本地 AI 编程智能体会话，覆盖成本、工具失败、延迟、异常、健康度、差异对比与 CI 门禁。触发词：智能体会话审计、agenttrace、cost-tracking、ci gate、session audit。"
category: development
risk: safe
source: community
source_repo: luoyuctl/agenttrace
source_type: community
date_added: "2026-05-10"
author: luoyuctl
tags: [ai-coding, observability, cost-tracking, session-analysis]
tools: [claude, cursor, gemini, codex-cli]
license: "MIT"
license_source: "https://github.com/luoyuctl/agenttrace/blob/master/LICENSE"
---

# agenttrace 会话审计

## 概述

本技能用于借助 [agenttrace](https://github.com/luoyuctl/agenttrace) 检查本地 AI 编程智能体的运行会话，重点剖析运行背后的过程：token 与费用突增、工具失败、重试循环、延迟缺口、异常、健康分以及会话间的差异。

agenttrace 以本地优先为原则，可读取 Claude Code、Codex CLI、Gemini CLI、Aider、Cursor 导出文件、OpenCode、Qwen Code、Kimi 以及通用 JSON 或 JSONL 跟踪等来源的会话日志。

## 适用场景

- 用户询问某次 AI 编程运行为何缓慢、昂贵、浅尝辄止或不稳定时使用。
- 在重试失败或可疑任务之前，复盘本地智能体日志时使用。
- 为 AI 辅助编程会话构建轻量 CI 健康门禁时使用。
- 对比两次执行，查找工具调用路径、重试或费用模式的变化时使用。

## 工作流程

### 步骤一：发现可用会话

优先使用已安装且在 `PATH` 中的 `agenttrace` 二进制。若当前仓库本身就是 `luoyuctl/agenttrace`，则改用 `go run ./cmd/agenttrace`。

```bash
agenttrace --doctor
agenttrace --overview
```

若未检测到任何会话，需如实报告 `--doctor` 检查过的目录，并向用户索要导出的会话文件或日志目录。

### 步骤二：生成人类可读的审计报告

当用户希望得到一份便于查阅或分享的精炼报告时，使用 Markdown 格式。

```bash
agenttrace --overview -f markdown -o agenttrace-overview.md
```

在报告中，优先呈现风险最高的会话并说明其重要性：严重异常、反复出现的工具失败、token 或费用浪费、较长的延迟缺口、偏低的健康分，以及明显过于浅薄的会话。

### 步骤三：检查单个会话或目录

若需快速查看，可使用最新会话；用户提供了明确的导出路径时，则直接传入该路径。

```bash
agenttrace --latest
agenttrace --latest -f json
agenttrace path/to/session-or-export.json
agenttrace --overview -d path/to/session-dir
```

### 步骤四：当语义差异重要时对比多次执行

即便 token 与延迟指标看似健康，智能体仍可能自信地走上错误的实现路径。当存在语义漂移风险时，应将跟踪审计与针对上一次或已知良好执行的 diff 对比结合起来。

需要关注的信号：

- 与预期任务偏离的文件或命令变更
- 相对参考执行缺失的测试或验证步骤
- 围绕同一组文件的无故反复编辑
- 因跳过必要探索而出现的更低费用

### 步骤五：添加自动化门禁

对于 CI 或可复现的团队工作流，应使用 JSON 输出或健康阈值。

```bash
agenttrace --overview -f json -o agenttrace-overview.json
agenttrace --overview --fail-under-health 80 --fail-on-critical --max-tool-fail-rate 15
```

请根据项目实际情况调整阈值。关键工作流适合使用严格的门禁；而在团队尚未摸清基线阶段，仅生成报告的命令更稳妥。

## 示例

### 本地快速复盘

```bash
agenttrace --overview
agenttrace --latest
```

适用于在一次较长的编程智能体运行之后，用以判断下一轮提示应当拆分任务、规避失败的工具路径、补齐缺失测试，还是重置上下文。

### CI 健康检查

```bash
agenttrace --overview --fail-under-health 80 --fail-on-critical
```

适用于 CI 中已具备智能体会话日志、且团队希望以简单方式拦截严重异常或不健康运行的场景。

## 最佳实践

- 当会话发现结果不确定时，先从 `--doctor` 入手。
- 对缺失字段要如实报告，切勿凭空捏造费用、模型、延迟或健康数据。
- 将提示词、代码与会话内容视为本地隐私数据。
- 自动化场景优先使用 JSON 输出，人工复核场景优先使用 Markdown 输出。
- 过程层面的失败依靠跟踪指标，语义漂移则依靠 diff 或参考执行复核。

## 局限性

- agenttrace 只能分析本地存在或以导出形式提供的日志。
- 部分智能体未暴露足够的字段，难以推断费用、模型、缓存使用或延迟。
- 健康的跟踪指标并不能证明最终代码正确，仍需运行测试并审查 diff。
- CI 门禁在团队尚未理解正常基线行为之前，应先以建议性提示形式运行。

## 安全与隐私提示

- 未经用户明确许可，不得将私有会话日志上传至外部服务。
- 不得覆盖用户已有的报告，除非用户明确要求输出到该路径。
- 避免在输出中泄露提示词、工具输出、环境变量或日志中出现的敏感信息。

## 常见问题

- **问题：** 未找到任何会话。
  **对策：** 运行 `agenttrace --doctor`，随后将 agenttrace 指向导出文件或日志目录。

- **问题：** 某次运行看起来又快又便宜，却产出了错误的重构结果。
  **对策：** 与上一次执行或已知良好的 diff 进行对比；仅凭费用指标无法捕捉语义漂移。

- **问题：** 加入健康门禁后 CI 频繁失败。
  **对策：** 先以 JSON 或 Markdown 形式产出报告，摸清正常基线，再逐步收紧阈值。

## 相关技能

- `@langfuse` - 用于生产级 LLM 应用的链路追踪与评估。
- `@observability-engineer` - 用于更广泛的服务监控、SLO 与事件响应工作流。