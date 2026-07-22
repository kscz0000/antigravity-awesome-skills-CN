---
name: agent-memory
description: 为 AI 智能体提供持久化、可检索的知识管理的混合记忆系统。
risk: unknown
source: https://github.com/webzler/agentMemory/tree/main/
source_repo: webzler/agentMemory
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/webzler/agentMemory/blob/main/LICENSE
---

# agentMemory 技能
## 适用场景

当你需要一套混合记忆系统为 AI 智能体提供持久化、可检索的知识管理时，使用本技能。

本技能通过提供一个持久化、可检索的内存库，自动与项目文档同步，扩展你的能力。

## 前置条件

- 已安装 Node.js
- 检查项目中是否已安装 `agentMemory`：
  ```bash
  ls -la .agentMemory
  ```

## 安装与配置

1. **安装依赖**：
   ```bash
   npm install
   ```

2. **构建项目**：
   ```bash
   npm run compile
   ```

3. **启动内存服务器**：
   需要运行 MCP 服务器才能与内存库交互。
   ```bash
   npm run start-server <project_id> <absolute_path_to_workspace>
   ```
   *注意：本技能通常作为后台进程或通过 mcp-server 配置运行，保持其处于运行状态是关键。*

## 可用能力（MCP 工具）

服务器运行后，可使用以下工具：

### `memory_search`
按查询词、类型或标签检索记忆。
- **参数**：`query`（字符串）、`type?`（字符串）、`tags?`（字符串数组）
- **示例**：「查找所有鉴权模式」-> `memory_search({ query: "authentication", type: "pattern" })`

### `memory_write`
记录新知识或决策。
- **参数**：`key`（字符串）、`type`（字符串）、`content`（字符串）、`tags?`（字符串数组）
- **示例**：「保存这条架构决策」-> `memory_write({ key: "auth-v1", type: "decision", content: "..." })`

### `memory_read`
按 key 读取指定记忆内容。
- **参数**：`key`（字符串）
- **示例**：「获取鉴权设计方案」-> `memory_read({ key: "auth-v1" })`

### `memory_stats`
查看内存使用情况的统计信息。
- **示例**：「展示内存统计」-> `memory_stats({})`

## 工作流

1. **初始化**：首次在项目中运行本技能时，可能会尝试从 `.kilocode/`、`.clinerules/` 或 `.roo/` 导入已有的 markdown 内存库。
2. **开发循环**：
   - **任务前**：检索内存中的相关上下文。
   - **任务中**：使用 read/search 回答问题。
   - **任务后**：把新发现写入内存。
3. **同步**：写入的内容会自动同步到项目中的标准 markdown 文件。

## 使用限制

- 仅在任务与上游来源及本地项目上下文明确匹配时使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 切勿把示例当作环境相关的测试、安全审查或破坏性/高成本操作的用户授权的替代品。
