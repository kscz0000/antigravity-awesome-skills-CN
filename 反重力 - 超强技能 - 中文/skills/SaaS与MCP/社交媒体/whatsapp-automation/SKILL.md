---
name: whatsapp-automation
description: "通过 Rube MCP (Composio) 自动化 WhatsApp Business 任务：发送消息、管理模板、上传媒体、处理联系人。始终先搜索工具以获取最新的 schema。触发词：whatsapp、whatsapp business、rube mcp、composio、发送消息、消息模板、whatsapp媒体、whatsapp联系人、whatsapp自动化、business api。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 WhatsApp Business 自动化

通过 Rube MCP 上的 Composio WhatsApp 工具集，自动化 WhatsApp Business 操作。

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具集 `whatsapp` 保持 WhatsApp 活动连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取最新的工具 schema
- 需要 WhatsApp Business API 账号（而非个人 WhatsApp 账号）

## 设置

**获取 Rube MCP**：在你的客户端配置中，将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具集 `whatsapp` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是 ACTIVE 状态，按照返回的鉴权链接完成 WhatsApp Business 设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 发送文本消息

**使用场景**：用户想要向 WhatsApp 联系人发送文本消息

**工具调用顺序**：
1. `WHATSAPP_GET_PHONE_NUMBERS` - 列出可用的商业电话号码 [前置]
2. `WHATSAPP_SEND_MESSAGE` - 发送文本消息 [必需]

**关键参数**：
- `to`：接收方电话号码（国际格式，例如 '+14155551234'）
- `body`：消息文本内容
- `phone_number_id`：用于发送的商业电话号码 ID

**注意事项**：
- 电话号码必须使用国际 E.164 格式并带国家代码
- 24 小时窗口之外的消息需要使用已审批的模板
- 24 小时窗口从客户最后一次给你发消息时开始计时
- 企业主动发起的会话必须先使用模板消息

### 2. 发送模板消息

**使用场景**：用户希望使用预先审批的模板消息进行主动外联

**工具调用顺序**：
1. `WHATSAPP_GET_MESSAGE_TEMPLATES` - 列出可用模板 [前置]
2. `WHATSAPP_GET_TEMPLATE_STATUS` - 检查模板审批状态 [可选]
3. `WHATSAPP_SEND_TEMPLATE_MESSAGE` - 发送模板消息 [必需]

**关键参数**：
- `template_name`：已审批模板的名称
- `language_code`：模板语言（例如 'en_US'）
- `to`：接收方电话号码
- `components`：模板变量值与参数

**注意事项**：
- 模板必须先经过 Meta 审批才能使用
- 模板变量必须与期望的数量和格式一致
- 发送未审批或被驳回的模板会返回错误
- 语言代码必须匹配模板已审批的翻译版本

### 3. 发送媒体消息

**使用场景**：用户希望发送图片、文档或其他媒体

**工具调用顺序**：
1. `WHATSAPP_UPLOAD_MEDIA` - 将媒体上传到 WhatsApp 服务器 [必需]
2. `WHATSAPP_SEND_MEDIA_BY_ID` - 使用上传得到的 media_id 发送媒体 [必需]
   或者
3. `WHATSAPP_SEND_MEDIA` - 使用公开 URL 发送媒体 [备选]

**关键参数**：
- `media_url`：媒体的公开 URL（用于 SEND_MEDIA）
- `media_id`：上传响应返回的 ID（用于 SEND_MEDIA_BY_ID）
- `type`：媒体类型（'image'、'document'、'audio'、'video'、'sticker'）
- `caption`：可选的媒体说明文字

**注意事项**：
- 上传的 media_id 是临时的，一段时间后会过期
- 不同媒体类型有不同的大小限制（图片：5MB，视频：16MB，文档：100MB）
- 支持的格式：图片（JPEG、PNG），视频（MP4、3GPP），文档（PDF 等）
- SEND_MEDIA 要求使用可公开访问的 HTTPS URL

### 4. 回复消息

**使用场景**：用户希望回复收到的 WhatsApp 消息

**工具调用顺序**：
1. `WHATSAPP_SEND_REPLY` - 针对特定消息发送回复 [必需]

**关键参数**：
- `message_id`：被回复消息的 ID
- `to`：接收方电话号码
- `body`：回复文本内容

**注意事项**：
- message_id 必须来自 24 小时窗口内收到的消息
- 回复会在会话中以引用形式显示
- 原始消息必须仍然存在（未被删除），引用内容才能正常显示

### 5. 管理 Business 个人资料和模板

**使用场景**：用户希望查看或管理其 WhatsApp Business 个人资料

**工具调用顺序**：
1. `WHATSAPP_GET_BUSINESS_PROFILE` - 获取商业个人资料详情 [可选]
2. `WHATSAPP_GET_PHONE_NUMBERS` - 列出已注册的电话号码 [可选]
3. `WHATSAPP_GET_PHONE_NUMBER` - 获取指定号码的详情 [可选]
4. `WHATSAPP_CREATE_MESSAGE_TEMPLATE` - 创建新模板 [可选]
5. `WHATSAPP_GET_MESSAGE_TEMPLATES` - 列出所有模板 [可选]

**关键参数**：
- `phone_number_id`：商业电话号码 ID
- `template_name`：新模板的名称
- `category`：模板类别（MARKETING、UTILITY、AUTHENTICATION）
- `language`：模板语言代码

**注意事项**：
- 新模板在使用前需要经过 Meta 审核
- 模板名称必须为小写加下划线（不允许空格）
- 类别会影响定价和审批标准
- 模板对页眉、正文和按钮有特定的格式要求

### 6. 分享联系人

**使用场景**：用户希望通过 WhatsApp 发送联系人信息

**工具调用顺序**：
1. `WHATSAPP_SEND_CONTACTS` - 发送联系人卡片 [必需]

**关键参数**：
- `to`：接收方电话号码
- `contacts`：包含姓名、电话、邮箱等信息的联系人对象数组

**注意事项**：
- 联系人对象必须符合 WhatsApp Business API 联系人 schema
- 每个联系人至少需要 name 字段
- 联系人中的电话号码应包含国家代码

## 常见模式

### 24 小时消息窗口

- 客户必须先给你发消息，才能打开会话窗口
- 在其最后一条消息后的 24 小时内，你可以发送自由格式的消息
- 超过 24 小时后，只能发送已审批的模板消息
- 模板消息可以重新打开会话窗口

### 电话号码解析

```
1. Call WHATSAPP_GET_PHONE_NUMBERS
2. Extract phone_number_id for your business number
3. Use phone_number_id in all send operations
```

### 媒体上传流程

```
1. Call WHATSAPP_UPLOAD_MEDIA with the file
2. Extract media_id from response
3. Call WHATSAPP_SEND_MEDIA_BY_ID with media_id
4. OR use WHATSAPP_SEND_MEDIA with a public URL directly
```

## 已知注意事项

**电话号码格式**：
- 始终使用 E.164 格式：+[国家代码][号码]（例如 '+14155551234'）
- 不要包含短横线、空格或括号
- 国家代码是必需的；缺少国家代码的本地号码将发送失败

**消息发送限制**：
- 在 24 小时窗口之外，企业主动发起的消息必须使用模板
- 模板消息按会话计费
- 速率限制针对每个电话号码和每个账号分别生效

**媒体处理**：
- 上传的媒体会过期；上传后请尽快使用
- 媒体 URL 必须是可公开访问的 HTTPS
- Sticker 有特定要求（WebP 格式，512x512 像素）

**模板管理**：
- 模板审核最多可能耗时 24 小时
- 被驳回的模板需要修改后重新提交
- 模板变量使用双花括号：{{1}}、{{2}} 等

## 快速参考

| 任务 | 工具 Slug | 关键参数 |
|------|-----------|------------|
| 发送消息 | WHATSAPP_SEND_MESSAGE | to, body |
| 发送模板 | WHATSAPP_SEND_TEMPLATE_MESSAGE | template_name, to, language_code |
| 上传媒体 | WHATSAPP_UPLOAD_MEDIA | (file params) |
| 按 ID 发送媒体 | WHATSAPP_SEND_MEDIA_BY_ID | media_id, to, type |
| 按 URL 发送媒体 | WHATSAPP_SEND_MEDIA | media_url, to, type |
| 回复消息 | WHATSAPP_SEND_REPLY | message_id, to, body |
| 发送联系人 | WHATSAPP_SEND_CONTACTS | to, contacts |
| 获取媒体 | WHATSAPP_GET_MEDIA | media_id |
| 列出电话号码 | WHATSAPP_GET_PHONE_NUMBERS | (none) |
| 获取电话号码 | WHATSAPP_GET_PHONE_NUMBER | phone_number_id |
| 获取商业个人资料 | WHATSAPP_GET_BUSINESS_PROFILE | phone_number_id |
| 创建模板 | WHATSAPP_CREATE_MESSAGE_TEMPLATE | template_name, category, language |
| 列出模板 | WHATSAPP_GET_MESSAGE_TEMPLATES | (none) |
| 检查模板状态 | WHATSAPP_GET_TEMPLATE_STATUS | template_id |

## 何时使用
此技能适用于执行概览中描述的工作流或操作。

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
