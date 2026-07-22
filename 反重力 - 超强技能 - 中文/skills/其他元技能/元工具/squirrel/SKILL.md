---
name: squirrel
description: "全周期 AI 编码技能：规划、构建、测试、lint、修复 bug 并编写生产级文档。自动检测项目状态并适配其 8 阶段流水线。当用户说'构建项目'、'修复这个 bug'、'squirrel 这个项目'、'开发新功能'或任何多步骤开发任务时使用。"
category: development
risk: safe
source: community
source_repo: flyingsquirrel0419/squirrel-skill
source_type: community
license: "Apache-2.0"
license_source: "https://github.com/flyingsquirrel0419/squirrel-skill/blob/main/LICENSE"
date_added: "2026-04-29"
author: flying_squirrel__
tags: [development, testing, planning, code-review, documentation, ci-cd]
tools: [claude, cursor, codex, antigravity, gemini, windsurf, opencode, copilot]
---

# Squirrel — 全周期软件开发技能

## 概述

Squirrel 是一个全周期 AI 编码技能，可在 9 个 AI 编码智能体上运行。它会自动检测项目状态（全新项目、进行中或成熟项目），并相应地调整其 8 阶段工程流水线。它不采用一刀切的工作流，而是判断项目实际所处的阶段，并从正确的切入点介入。

## 何时使用此技能

- 从零开始创建新项目时（全新项目）
- 改进现有代码库时（进行中或成熟项目）
- 修复 bug、添加功能或重构时
- 为项目添加测试、lint 或 CI/CD 时
- 编写生产级文档时
- 当用户说"构建我"、"修复这个"、"squirrel 这个项目"或任何多步骤开发任务时

## 工作原理

### 步骤 0：检测模式

Squirrel 对项目目录进行分类：

| 信号 | 模式 | 入口点 |
|--------|------|-------------|
| 空目录 | 全新项目 | 从头执行全部 8 个阶段 |
| 有源文件，无测试/文档 | 进行中 | 先审计，再改进 |
| 源码 + 测试 + CI + README | 成熟项目 | 针对性改进 |
| "修复这个 bug / 添加功能" | 定向修复 | 仅限定范围内的工作 |

### 8 阶段流水线

1. **探索** — 理解项目（审计现有代码或收集需求）
2. **规划** — 具体的任务列表，包含依赖关系和完成标准
3. **构建** — 编写或修改代码（支持时使用并行子智能体）
4. **测试** — 运行现有测试，编写新测试，目标覆盖率 70%+
5. **Bug 狩猎** — 静态分析 + 人工审查
6. **打磨** — Lint、格式化、类型检查、移除死代码
7. **文档** — README + 内联文档（更新现有文档，不覆盖）
8. **发布** — 最终检查清单：测试通过、无密钥泄露、CI 已配置

### 失败恢复（三振规则）

1. **第一次：** 修复具体错误。运行测试。继续。
2. **第二次：** 重新阅读代码。尝试不同的方法。
3. **第三次：** 停止。回滚。记录失败原因。询问用户。

## 示例

### 示例 1：构建 REST API

```text
> build me a REST API for a todo app with TypeScript and Express
```

Squirrel 自动检测到全新项目模式并运行全部 8 个阶段。

### 示例 2：修复 bug

```text
> fix this bug in src/auth/login.py
```

Squirrel 进入定向模式 — 简化审计、限定修复、验证。

### 示例 3：改进现有项目

```text
> squirrel this project — add tests, fix lint errors, write README
```

Squirrel 审计现有代码库，然后应用第 4-8 阶段。

## 最佳实践

- 尊重现有代码 — 匹配命名规范、测试框架、导入风格和架构
- 编写新文件前先阅读 2-3 个类似文件
- 永远不要用 `as any` 或 `@ts-ignore` 抑制类型错误
- 永远不要通过删除失败测试来"通过"
- 永远不要让代码处于损坏状态

## 平台兼容性

Squirrel 支持以下平台：Claude Code、Codex、Cursor、Antigravity、Gemini CLI、GitHub Copilot、Windsurf、OpenCode、Aider（共 9 个）。

安装方式：

```bash
# Universal installer
npx skills add flyingsquirrel0419/squirrel-skill

```

## 限制

- 不替代环境特定的验证或专家审查
- CI/CD 模板是起点，非开箱即用的保证
- 并行子智能体执行取决于平台支持

## 相关技能

- `@brainstorming` - 用于实现前的规划
- `@test-driven-development` - 用于 TDD 导向的工作流
- `@systematic-debugging` - 用于系统化的问题解决
