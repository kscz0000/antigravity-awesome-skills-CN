---
name: helpdesk-automation
description: "通过 Rube MCP (Composio) 自动化 HelpDesk 任务：列出工单、管理视图、使用预设回复和配置自定义字段。始终先搜索工具获取当前模式。当用户要求'列出工单'、'管理工单视图'、'使用预设回复'或'配置自定义字段'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 HelpDesk 自动化

通过 Rube MCP 使用 Composio 的 HelpDesk 工具包自动化工单操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `helpdesk` 建立活跃的 HelpDesk 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `helpdesk`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 HelpDesk 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出和浏览工单

**何时使用**：用户想要检索、浏览或分页查看支持工单

**工具调用顺序**：
1. `HELPDESK_LIST_TICKETS` - 列出工单并支持排序和分页 [必需]

**关键参数**：
- `silo`：工单文件夹 - 'tickets'、'archive'、'trash' 或 'spam'（默认：'tickets'）
- `sortBy`：排序字段 - 'createdAt'、'updatedAt' 或 'lastMessageAt'（默认：'createdAt'）
- `order`：排序方向 - 'asc' 或 'desc'（默认：'desc'）
- `pageSize`：每页结果数，1-100（默认：20）
- `next.value`：向前分页的时间戳游标
- `next.ID`：向前分页的 ID 游标
- `prev.value`：向后分页的时间戳游标
- `prev.ID`：向后分页的 ID 游标

**注意事项**：
- 分页使用基于游标的方式，需要时间戳 + ID 对
- 向前分页需要前一次响应中的 `next.value` 和 `next.ID`
- 向后分页需要 `prev.value` 和 `prev.ID`
- `silo` 决定从哪个文件夹列出；默认为活跃工单
- `pageSize` 最大值为 100；默认为 20
- 已归档和已删除的工单位于独立的 silo 中

### 2. 管理工单视图

**何时使用**：用户想要查看用于组织工单的已保存客服视图

**工具调用顺序**：
1. `HELPDESK_LIST_VIEWS` - 列出所有客服视图 [必需]

**关键参数**：（无必需参数）

**注意事项**：
- 视图是客服在 HelpDesk UI 中配置的预定义保存过滤器
- 视图定义包含过滤器条件，可用于理解工单组织方式
- 无法通过 API 创建或修改视图；它们在 HelpDesk UI 中管理

### 3. 使用预设回复

**何时使用**：用户想要列出可用的预设（模板）回复

**工具调用顺序**：
1. `HELPDESK_LIST_CANNED_RESPONSES` - 检索所有预定义回复模板 [必需]

**关键参数**：（无必需参数）

**注意事项**：
- 预设回复是用于常见回复的预定义模板
- 它们可能包含需要填充的占位符变量
- 预设回复通过 HelpDesk UI 管理
- 回复内容可能包含 HTML 格式

### 4. 检查自定义字段

**何时使用**：用户想要查看账户的自定义字段定义

**工具调用顺序**：
1. `HELPDESK_LIST_CUSTOM_FIELDS` - 列出所有自定义字段定义 [必需]

**关键参数**：（无必需参数）

**注意事项**：
- 自定义字段使用组织特定的数据扩展默认工单模式
- 字段定义包括字段类型、名称和验证规则
- 自定义字段在 HelpDesk 管理面板中配置
- 当字段被填充时，字段值会显示在工单上

## 常见模式

### 工单浏览模式

```
1. Call HELPDESK_LIST_TICKETS with desired silo and sortBy
2. Process the returned page of tickets
3. Extract next.value and next.ID from the response
4. Call HELPDESK_LIST_TICKETS with those cursor values for next page
5. Continue until no more cursor values are returned
```

### 工单文件夹导航

```
Active tickets:  silo='tickets'
Archived:        silo='archive'
Trashed:         silo='trash'
Spam:            silo='spam'
```

### 基于游标的分页

```
Forward pagination:
  - Use next.value (timestamp) and next.ID from response
  - Pass as next.value and next.ID parameters in next call

Backward pagination:
  - Use prev.value (timestamp) and prev.ID from response
  - Pass as prev.value and prev.ID parameters in next call
```

## 已知注意事项

**游标分页**：
- 游标导航需要时间戳和 ID 两者
- 游标值是 ISO 8601 日期时间格式的时间戳
- 在同一请求中混合使用向前和向后游标是未定义行为

**Silo 过滤**：
- 工单在物理上被分离到不同的 silo（文件夹）中
- 在 silo 之间移动工单需要在 HelpDesk UI 中完成
- 每个 silo 查询是独立的；没有跨 silo 搜索

**只读操作**：
- 当前 Composio 工具包提供列表/读取操作
- 工单创建、更新和回复操作可能需要额外工具
- 检查 RUBE_SEARCH_TOOLS 以获取任何新可用的工具

**速率限制**：
- HelpDesk API 有每个账户的速率限制
- 在收到 429 响应时实现退避策略
- 保持合理的页面大小以避免超时

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 下
- 使用防御性解析和回退模式
- 工单 ID 是字符串

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 列出工单 | HELPDESK_LIST_TICKETS | silo, sortBy, order, pageSize |
| 列出视图 | HELPDESK_LIST_VIEWS | (无) |
| 列出预设回复 | HELPDESK_LIST_CANNED_RESPONSES | (无) |
| 列出自定义字段 | HELPDESK_LIST_CUSTOM_FIELDS | (无) |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
