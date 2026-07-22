---
name: antigravity-agent-manager
description: "使用独立的 Antigravity 2.0 Agent Manager 和 Antigravity IDE 配置并编排并行 Agent。触发词：antigravity、agent manager、多智能体编排、并行 agent、双窗口工作区、多 agent 配置。"
category: general
risk: critical
source: self
source_type: self
date_added: "2026-06-04"
author: community
tags: [agent-manager, orchestration, multi-agent, setup]
tools: [antigravity, gemini]
---

# Antigravity Agent 管理器

## 概述

本指南介绍如何使用独立的 **Antigravity 2.0 Agent 管理器**（白色图标）与 **Antigravity IDE**（黑色图标）并行编排多智能体系统。

从 2.0 版本起，Google 将 Agent 管理器从主 IDE 界面中解耦，移除了 "Open Agent Manager" 按钮。本技能概述了如何安装、配置并并排运行这两个环境，从而同时指挥多个 AI Agent 协作完成前后端项目。

## 适用场景

- 需要在同一代码库上同时协调多个前端、后端或 QA Agent 时。
- 搭建双窗口工作区（Antigravity IDE + Antigravity 2.0 Agent 管理器）时。
- 解决冲突或过时教程中提及的内置 "Open Agent Manager" 按钮相关步骤时。

## 工作流程

### 步骤 1：并行安装

1. **保留当前 Antigravity IDE**：不要卸载经典版 IDE（黑色图标）。
2. **下载 Antigravity 2.0**：从 Antigravity 官方下载页获取独立的 Agent 管理器应用。
3. **安装**：运行安装程序。它会与现有 IDE 并行安装，不会覆盖现有 IDE。安装完成后你将同时拥有：
   - **Antigravity IDE**（黑色图标）—— 你的代码编辑器与手工开发工作区。
   - **Antigravity 2.0**（白色图标）—— 你的多智能体编排仪表盘。

### 步骤 2：双工作区配置

1. 同时打开 **Antigravity IDE** 与 **Antigravity 2.0** 两个应用。
2. 在两个应用中加载同一个项目目录（例如 `C:/Users/erwinpzocikk/Dev/GroupProjects/intIntercatedraAdmin`）。
3. 在 Agent 管理器（白色图标）中配置 Agent 池。为其分配专门角色（例如 `frontend-agent`、`backend-agent`、`qa-validator`）。

### 步骤 3：协调 Agent 执行

1. 在 Agent 管理器中定义任务范围。为防止目录冲突与竞态条件：
   - 将 `backend-agent` 分配到服务端目录（例如 `/server` 或 `/api`）。
   - 将 `frontend-agent` 分配到前端目录（例如 `/client` 或 `/src`）。
2. 并行运行这些 Agent。
3. 使用 Antigravity IDE（黑色图标）实时监控文件变更、审阅 diff 并进行手工微调。

## 示例

### 示例 1：在多 Agent 项目中定义独立范围

在配置 Agent 管理器仪表盘时，在提示词中明确目标文件或目录，避免 Agent 之间相互冲突：

**后端 Agent 任务提示词：**
```text
Role: Backend Developer Agent
Workspace Target: /server
Task: Add a new POST /api/v1/students endpoint in server/routes/students.js and update database/models/student.js. Do not edit files outside the /server directory.
```

**前端 Agent 任务提示词：**
```text
Role: Frontend UI Agent
Workspace Target: /client
Task: Build the student registration form under client/components/StudentForm.jsx. Consume the /api/v1/students endpoint. Do not edit files outside the /client directory.
```

### 示例 2：通过 Git 同步变更

由于 Agent 并行编写代码，需要在 IDE 终端中使用 git 同步其工作成果：

```bash
# In the Antigravity IDE terminal, check the changes written by the agents
git status

# Review diffs before committing
git diff

# Commit stable checkpoints so both agents stay in sync with main branch
git add .
git commit -m "feat: synchronize parallel front-end and back-end agent changes"
```

## 最佳实践

- ✅ **建议：** 同时并排运行两个应用。
- ✅ **建议：** 在 Agent 管理器中为每个 Agent 强制执行严格的目录级边界（范围）。
- ✅ **建议：** 在让 Agent 执行大规模重写前，使用 git 分支或提交来标记进度检查点。
- ❌ **避免：** 让多个 Agent 同时编辑同一文件，这会导致写冲突与 git 合并冲突。
- ❌ **避免：** 在黑色图标 IDE 中寻找 "Open Agent Manager" 按钮；应改用独立的白色图标应用。

## 限制

- 本技能假设你拥有在 Windows/macOS 上安装这两个应用的本地管理员权限。
- 文件锁的协调依赖标准 IDE 的文件系统监视器。如果变更未能反映，请重新加载 IDE 工作区（`Ctrl+R` 或开发者重载）。

## 常见陷阱

- **问题：** Agent 互相覆盖代码或陷入写锁。
  **解决：** 隔离它们的工作区。如果必须编辑同一文件，应按顺序编排执行（例如先运行后端 Agent，提交其变更，然后再运行前端 Agent）。
- **问题：** Agent 管理器中的变更在 IDE 中不可见。
  **解决：** 确认两个应用都指向完全相同的绝对文件路径。在 Windows 上要留意映射驱动器或符号链接。

## 相关技能

- `@antigravity-workflows` - 引导 Agent 完成顺序执行的多 Agent 流程。
- `@antigravity-skill-orchestrator` - 用于任务复杂度评估与通用技能路由。
- `@gitops-workflow` - 用于在团队环境中协调提交与分支合并。