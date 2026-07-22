---
name: agent-memory-mcp
description: "为 AI 智能体提供持久化、可搜索知识管理的混合记忆系统（架构、模式、决策）。触发词：agent memory、智能体记忆、持久记忆、MCP 记忆、记忆系统、知识管理、架构决策记录、模式存储"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Agent Memory 技能

本技能提供持久化、可搜索的记忆库，可自动与项目文档同步。它作为 MCP 服务器运行，支持长期记忆的读取/写入/搜索。

## 前置条件

- Node.js (v18+)

## 安装配置

1. **克隆仓库**：
   将 `agentMemory` 项目克隆到智能体的工作空间或平行目录：

   ```bash
   git clone https://github.com/webzler/agentMemory.git .agent/skills/agent-memory
   ```

2. **安装依赖**：

   ```bash
   cd .agent/skills/agent-memory
   npm install
   npm run compile
   ```

3. **启动 MCP 服务器**：
   使用辅助脚本为当前项目激活记忆库：

   ```bash
   npm run start-server <project_id> <absolute_path_to_target_workspace>
   ```

   _当前目录示例：_

   ```bash
   npm run start-server my-project $(pwd)
   ```

## 功能（MCP 工具）

### `memory_search`

按查询词、类型或标签搜索记忆。

- **参数**：`query`（字符串）、`type?`（字符串）、`tags?`（字符串数组）
- **用法**："查找所有认证模式" -> `memory_search({ query: "authentication", type: "pattern" })`

### `memory_write`

记录新知识或决策。

- **参数**：`key`（字符串）、`type`（字符串）、`content`（字符串）、`tags?`（字符串数组）
- **用法**："保存这个架构决策" -> `memory_write({ key: "auth-v1", type: "decision", content: "..." })`

### `memory_read`

按键名获取特定记忆内容。

- **参数**：`key`（字符串）
- **用法**："获取认证设计" -> `memory_read({ key: "auth-v1" })`

### `memory_stats`

查看记忆使用情况统计。

- **用法**："显示记忆统计" -> `memory_stats({})`

## 仪表盘

本技能包含独立的仪表盘，用于可视化记忆使用情况。

```bash
npm run start-dashboard <absolute_path_to_target_workspace>
```

访问地址：`http://localhost:3333`

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不能替代特定环境的验证、测试或专家审查。
- 若缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
