---
name: open-dynamic-workflows
description: "规划、编排并行 AI 编码智能体，并对输出进行对抗性验证的动态多智能体工作流引擎。触发词：动态工作流、多智能体编排、并行智能体、对抗性验证、ODW、动态工作流引擎"
category: ai-agents
risk: critical
source: community
source_repo: Suraj1235/open-dynamic-workflows
source_type: community
date_added: "2026-06-06"
author: Suraj1235
tags: [multi-agent, orchestration, workflow, adversarial-verification, coding-agents]
tools: [claude, cursor, codex, gemini, antigravity]
# Optional: declare the upstream license if source_repo is set
license: "MIT"
license_source: "https://github.com/Suraj1235/open-dynamic-workflows/blob/main/LICENSE"
---

# Open Dynamic Workflows 动态工作流引擎

## 概述

Open Dynamic Workflows（ODW）是一款开源的动态多智能体工作流引擎，面向 OpenCode、Codex、Antigravity 和 VS Code 等 AI 编码智能体。它让你可以规划任务、编排多个智能体并行工作，并在输出落地前进行对抗性验证。ODW 提供了 Codex/Antigravity 技能文件夹（`SKILL.md` 加守护进程桥接）和 OpenCode 插件，采用自带模型模式（Anthropic、OpenAI 兼容或 Ollama）。本技能改编自社区项目 `Suraj1235/open-dynamic-workflows`。

## 何时使用本技能

- 需要将编码任务分解为独立子任务并并行运行多个智能体时使用。
- 跨多个 AI 编码工具（OpenCode、Codex、Antigravity、VS Code）工作并需要统一编排层时使用。
- 用户要求在合并前对智能体生成的变更进行对抗性审查或验证时使用。

## 工作原理

### 步骤 1：规划

ODW 接收一个高层目标，生成子任务的动态工作流图，识别哪些可以并行执行、哪些存在依赖关系。

### 步骤 2：编排

引擎通过 OpenCode 插件或 Codex/Antigravity 守护进程桥接将子任务分派给并行智能体，使用你配置的模型提供方（Anthropic、OpenAI 兼容或 Ollama）。

### 步骤 3：对抗性验证

已完成的工作会经过对抗性验证通道，在结果综合和返回之前对输出进行质疑检验。

## 示例

### 示例 1：运行并行工作流

ODW 从源码安装（克隆仓库后执行 `npm install`）。CLI 为
`odw-daemon`——在仓库内以 `npm run odw -- <args>` 运行，或以
`npx odw-daemon <args>` / 全局 `odw-daemon`（如果链接了 bin）运行。

```bash
# Configure your model provider (bring-your-own-model)
export ANTHROPIC_API_KEY=...        # or an OpenAI-compatible / Ollama endpoint

# One-time setup: generate ~/.odw/config.json
npm run setup

# Start the local workflow daemon (once)
npm run odw -- start

# Plan, orchestrate, and verify a task across parallel agents
npm run odw -- run --prompt "refactor the auth module and add tests"
```

### 示例 2：使用 Codex/Antigravity 技能桥接

```bash
# ODW ships a SKILL.md + daemon bridge consumed by Codex / Antigravity.
# Start the daemon, then run a saved orchestration script through it:
npm run odw -- start
npm run odw -- run --script examples/workflows/studio-prime.workflow.js --cwd .
```

## 最佳实践

- 每个子任务限定作用域，使智能体无需共享状态即可运行。
- 合并智能体输出前，保持对抗性验证通道启用。
- 不要在未声明依赖关系的情况下并行运行相互依赖的子任务。
- 不要提交模型提供方的 API 密钥；使用环境变量或密钥管理器。

## 局限性

- 本技能不能替代特定环境的验证、测试或专家审查。
- 如果缺少所需的输入、权限或安全边界，请停下来寻求确认。

## 安全与注意事项

- ODW 会执行智能体生成的代码和 Shell 命令；仅在授权的本地或沙盒环境中运行。
- 模型提供方凭证（Anthropic / OpenAI 兼容 / Ollama）必须通过环境变量提供，绝不能提交到源码中。
- 将对抗性验证输出应用到生产分支前，务必先审查。

## 常见问题

- **问题：** 并行智能体在相同文件上冲突。
  **解决方案：** 为每个子任务分配独占的文件/模块所有权，冲突任务改为顺序执行。

## 相关技能

- `@multi-agent-orchestration` - 协调多个智能体围绕同一目标工作时使用。
- `@code-review` - 对抗性验证如何补充人工审查。
