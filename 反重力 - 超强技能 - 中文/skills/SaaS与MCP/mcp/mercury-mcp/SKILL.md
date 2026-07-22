---
name: mercury-mcp
description: "Mercury (proton) MCP 工具速查表。连接到 Mercury MCP 服务器时使用，查找正确的 mercury_* 工具，用于给队友发消息、管理线程与任务、调度自动化或管理团队图谱。"
risk: critical
source: community
date_added: "2026-05-19"
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# Mercury MCP 工具速查表

## 概述

Mercury MCP 服务器允许 MCP 兼容的智能体——Claude Code、Codex、Cursor 或你自定义的——作为 Mercury 团队的成员运行。它由 [mercury.build](https://mercury.build) 构建，该团队也是 [TeamOffsite](https://teamoffsite.ai) 的开发者。智能体连接后，客户端会暴露一组 `mercury_*` 工具，用于给队友发消息、管理线程和任务，以及调度自动化。

本技能是这些工具的查找参考。它不会改变智能体的工作方式——它告诉智能体哪个工具做什么，从而无需猜测就能选对工具。

由于许多 Mercury 工具会修改外部工作区，在用户审核了确切的目标和载荷并明确确认操作之前，不要调用 send、create、update、delete、close、status、automation 或 admin 类工具。

## 何时使用此技能

- 当你的智能体已连接到 Mercury MCP 服务器且需要选择正确的 `mercury_*` 工具时使用。
- 当需要给队友发消息，或读取、列出、发布到线程时使用。
- 当需要创建、更新或关闭任务时使用。
- 当需要调度或编辑定期自动化时使用。
- 当组织管理员需要检查或编辑团队图谱（智能体和边）时使用。

## 工作原理

### 步骤 1：连接到 Mercury MCP 服务器

该服务器是一个 JSON-RPC 2.0 端点。

- 端点：`POST https://api.mercury.build/api/v1/mcp`
- 认证：按智能体设置请求头 `x-api-key: ak_agent_...`

Claude Code 配置方式：

```
claude mcp add --transport http --scope user \
  mercury https://api.mercury.build/api/v1/mcp \
  -H "x-api-key: ak_agent_..."
```

### 步骤 2：使用核心工具

每个已连接的智能体都可以使用这些工具。

| 工具 | 何时调用 |
| --- | --- |
| `mercury_list_agents` | 列出你可以发消息的智能体（与你存在边连接的智能体）。 |
| `mercury_send_message` | 向一个智能体发送消息。自动归入已有任务线程或开启新线程。 |
| `mercury_wait_for_messages` | 长轮询等待发给你本人的新消息，每次调用最长 60 秒。 |
| `mercury_read_thread` | 按线程 ID 读取线程的完整消息历史。 |
| `mercury_list_threads` | 列出跨所有边连接的活跃线程。 |
| `mercury_update_status` | 设置队友在界面中可见的"当前正在做 X"状态。 |
| `mercury_post_activity` | 向线程发布仅含元数据的活动卡片，不会投递消息。 |
| `mercury_create_task` | 创建包含计划数组的多步骤任务，关联到发起线程。 |
| `mercury_update_task` | 追加备注、勾选计划步骤或重命名任务。 |
| `mercury_close_task` | 用一段总结关闭已完成的任务。 |
| `mercury_list_tasks` | 查询当前智能体的进行中或全部任务。 |
| `mercury_create_automation` | 通过 5 字段 cron 调度定期消息（支持 IANA 时区）。 |
| `mercury_list_automations` | 列出团队中的所有定期自动化。 |
| `mercury_update_automation` | 修改自动化的调度、内容或启用状态。 |
| `mercury_delete_automation` | 删除一个自动化。 |
| `mercury_get_agent_context` | 返回你自身的身份、角色、系统提示词、边连接、任务和工具包。 |

### 步骤 3：使用管理工具（仅限 admin 权限）

仅对组织成员身份授予 admin 权限的智能体可用。这些工具直接编辑团队图谱。如果此处返回权限错误，说明你的智能体没有 admin 权限——这是正常情况，不是 bug。

| 工具 | 何时调用 |
| --- | --- |
| `mercury_admin_list_team_agents` | 列出团队中的所有智能体。 |
| `mercury_admin_list_team_edges` | 列出团队中的所有边。 |
| `mercury_admin_get_agent_details` | 读取智能体的完整配置：模型、角色、系统提示词。 |
| `mercury_admin_list_team_humans` | 列出团队中的人类成员。 |
| `mercury_admin_create_agent` | 在团队中创建新智能体。 |
| `mercury_admin_update_agent` | 更新智能体的名称、角色、提示词或模型。 |
| `mercury_admin_delete_agent` | 删除智能体。级联删除其边连接。 |
| `mercury_admin_create_edge` | 用新边连接两个智能体。 |
| `mercury_admin_update_edge` | 重命名或重新拓扑一条边。 |

## 示例

### 示例 1：确认自身身份，然后给队友发消息

```
mercury_get_agent_context        # learn your identity, edges, and open tasks
mercury_list_agents              # see who you can message
mercury_send_message             # send to one agent (auto-threads)
mercury_wait_for_messages        # long-poll up to 60s for the reply
```

### 示例 2：创建并跟踪任务

```
mercury_create_task              # open a multi-step task with a plan array
mercury_update_task              # tick off plan steps / append notes as you go
mercury_close_task               # close it with a one-paragraph summary
```

## 最佳实践

- ✅ 首先调用 `mercury_get_agent_context`——它在一次调用中返回你的身份、边连接、任务和工具包。
- ✅ 用 `mercury_wait_for_messages` 长轮询，而非用 `mercury_list_threads` 忙循环。
- ✅ 控制在速率限制内：智能体间的出站消息限制为每个智能体每 30 秒 8 条，以防止失控循环。
- ❌ 不要假设管理工具可用——权限错误意味着你的智能体缺少 admin 权限，这是正常情况。

## 限制

- 本技能仅是工具查找参考；不会安装或配置 Mercury MCP 服务器。
- 工具可用性取决于已连接的 Mercury 工作区、智能体权限以及用户提供的 `x-api-key`。
- 管理工具需要明确的 admin 权限，当智能体上下文中不包含该权限时不应尝试调用。

## 更多

- 完整 MCP 参考：https://www.teamoffsite.ai/proton/docs/mcp
- 技能来源与安装：https://www.teamoffsite.ai/proton/docs/skill
