---
name: docusign-automation
description: "通过 Rube MCP (Composio) 自动化 DocuSign 任务：模板、envelope、签名、文档管理。始终先搜索工具以获取当前 schema。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 DocuSign 自动化

通过 Composio 的 DocuSign 工具包（经由 Rube MCP）自动化 DocuSign 电子签名工作流。

## 前提条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 连接 DocuSign 工具包（toolkit: `docusign`）
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并指定工具包 `docusign`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 DocuSign OAuth
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 浏览和选择模板

**适用场景**：用户想要查找可用的文档模板以发送

**工具调用顺序**：
1. `DOCUSIGN_LIST_ALL_TEMPLATES` - 列出所有可用模板 [必需]
2. `DOCUSIGN_GET_TEMPLATE` - 获取模板详细信息 [可选]

**关键参数**：
- 列表操作：可选的搜索/过滤参数
- 详情操作：`templateId`（来自列表结果）
- 响应包含模板的 `templateId`、`name`、`description`、角色和字段

**注意事项**：
- Template ID 是 GUID 格式（例如 '12345678-abcd-1234-efgh-123456789012'）
- 模板定义了带有签名标签（tabs）的收件人角色；在创建 envelope 前需了解角色
- 大型模板库需要分页；检查是否有续页标记
- 模板访问权限取决于账户权限

### 2. 从模板创建和发送 Envelope

**适用场景**：用户想要使用预构建模板发送文档以供签名

**工具调用顺序**：
1. `DOCUSIGN_LIST_ALL_TEMPLATES` - 查找要使用的模板 [前置条件]
2. `DOCUSIGN_GET_TEMPLATE` - 查看模板角色和字段 [可选]
3. `DOCUSIGN_CREATE_ENVELOPE_FROM_TEMPLATE` - 创建 envelope [必需]
4. `DOCUSIGN_SEND_ENVELOPE` - 发送 envelope 以供签名 [必需]

**关键参数**：
- CREATE_ENVELOPE_FROM_TEMPLATE：
  - `templateId`：要使用的模板
  - `templateRoles`：角色分配数组，包含 `roleName`、`name`、`email`
  - `status`：'created'（草稿）或 'sent'（立即发送）
  - `emailSubject`：签名邮件的自定义主题行
  - `emailBlurb`：签名邮件中的自定义消息
- SEND_ENVELOPE：
  - `envelopeId`：创建响应中返回的 Envelope ID

**注意事项**：
- `templateRoles` 必须与模板中定义的角色名称完全匹配（区分大小写）
- 创建时将 `status` 设为 'sent' 会立即发送；使用 'created' 创建草稿
- 如果创建时 status 为 'sent'，则无需单独调用 SEND_ENVELOPE
- 每个角色至少需要 `roleName`、`name` 和 `email`
- `emailSubject` 会覆盖模板的默认邮件主题

### 3. 监控 Envelope 状态

**适用场景**：用户想要检查已发送 envelope 的状态或跟踪签名进度

**工具调用顺序**：
1. `DOCUSIGN_GET_ENVELOPE` - 获取 envelope 详情和状态 [必需]

**关键参数**：
- `envelopeId`：Envelope 标识符（GUID）
- 响应包含 `status`、`recipients`、`sentDateTime`、`completedDateTime`

**注意事项**：
- Envelope 状态：'created'、'sent'、'delivered'、'signed'、'completed'、'declined'、'voided'
- 'delivered' 表示邮件已打开，而非文档已签名
- 'completed' 表示所有收件人已完成签名
- Recipients 数组显示每个收件人的个人签名状态
- Envelope ID 是 GUID 格式；始终从创建或搜索结果中获取

### 4. 向现有 Envelope 添加模板

**适用场景**：用户想要向现有 envelope 添加额外文档或模板

**工具调用顺序**：
1. `DOCUSIGN_GET_ENVELOPE` - 验证 envelope 存在且处于草稿状态 [前置条件]
2. `DOCUSIGN_ADD_TEMPLATES_TO_DOCUMENT_IN_ENVELOPE` - 向 envelope 添加模板 [必需]

**关键参数**：
- `envelopeId`：目标 Envelope ID
- `documentId`：Envelope 内的文档 ID
- `templateId`：要添加的模板

**注意事项**：
- Envelope 必须处于 'created'（草稿）状态才能添加模板
- 无法向已发送的 envelope 添加模板
- 文档 ID 在 envelope 内按顺序编号（从 '1' 开始）
- 添加模板会将其字段和角色合并到现有 envelope 中

### 5. 管理 Envelope 生命周期

**适用场景**：用户想要发送、作废或管理草稿 envelope

**工具调用顺序**：
1. `DOCUSIGN_GET_ENVELOPE` - 检查当前 envelope 状态 [前置条件]
2. `DOCUSIGN_SEND_ENVELOPE` - 发送草稿 envelope [可选]

**关键参数**：
- `envelopeId`：要管理的 Envelope
- 发送操作：envelope 必须处于 'created' 状态且所有必需收件人已配置

**注意事项**：
- 只有 'created'（草稿）状态的 envelope 可以发送
- 已发送的 envelope 无法撤回；只能作废
- 作废 envelope 会通知所有收件人
- 发送前所有必需收件人必须有有效的电子邮件地址

## 常见模式

### ID 解析

**模板名称 -> Template ID**：
```
1. 调用 DOCUSIGN_LIST_ALL_TEMPLATES
2. 在结果中按名称查找模板
3. 提取 templateId（GUID 格式）
```

**Envelope 跟踪**：
```
1. 存储 CREATE_ENVELOPE_FROM_TEMPLATE 响应中的 envelopeId
2. 定期调用 DOCUSIGN_GET_ENVELOPE 检查状态
3. 检查收件人级别的状态以了解个人签名进度
```

### 模板角色映射

从模板创建 envelope 时：
```
1. 调用 DOCUSIGN_GET_TEMPLATE 查看定义的角色
2. 将每个角色映射到实际收件人：
   {
     "roleName": "Signer 1",     // 必须与模板角色名称完全匹配
     "name": "John Smith",
     "email": "john@example.com"
   }
3. 在 templateRoles 数组中包含所有必需角色
```

### Envelope 状态流转

```
created (草稿) -> sent -> delivered -> signed -> completed
                       \-> declined
                       \-> voided (由发送者操作)
```

## 已知注意事项

**模板角色**：
- 角色名称区分大小写；必须与模板定义完全匹配
- 创建 envelope 时必须分配所有必需角色
- 缺少角色分配会导致 envelope 创建失败

**Envelope 状态**：
- 'delivered' 表示邮件已打开，而非文档已签名
- 'completed' 是最终成功状态（所有方已签名）
- 状态转换是单向的；无法恢复到之前的状态

**GUID**：
- 所有 DocuSign ID（模板、envelope）都是 GUID 格式
- 始终通过列表/搜索端点将名称解析为 GUID
- 不要硬编码 GUID；它们对每个账户是唯一的

**速率限制**：
- DocuSign API 有每个账户的速率限制
- 批量创建 envelope 应进行节流控制
- 轮询 envelope 状态应使用合理的间隔（30-60 秒）

**响应解析**：
- 响应数据可能嵌套在 `data` 键下
- 收件人信息嵌套在 envelope 响应中
- 日期字段使用 ISO 8601 格式
- 防御性解析，对可选字段设置回退值

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出模板 | DOCUSIGN_LIST_ALL_TEMPLATES | (可选过滤器) |
| 获取模板 | DOCUSIGN_GET_TEMPLATE | templateId |
| 创建 envelope | DOCUSIGN_CREATE_ENVELOPE_FROM_TEMPLATE | templateId, templateRoles, status |
| 发送 envelope | DOCUSIGN_SEND_ENVELOPE | envelopeId |
| 获取 envelope 状态 | DOCUSIGN_GET_ENVELOPE | envelopeId |
| 向 envelope 添加模板 | DOCUSIGN_ADD_TEMPLATES_TO_DOCUMENT_IN_ENVELOPE | envelopeId, documentId, templateId |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
