---
name: close-automation
description: "通过 Rube MCP (Composio) 自动化 Close CRM 任务：创建线索、管理通话/短信、处理任务和跟踪笔记。当用户要求'自动化 Close CRM 操作'、'创建 Close 线索'、'记录通话'、'发送短信'、'管理任务'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Close CRM 自动化

通过 Composio 的 Close 工具包和 Rube MCP 自动化 Close CRM 操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 工具包 `close` 建立活跃的 Close 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `close` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Close API 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和管理线索

**何时使用**：用户想要创建新线索或管理现有线索记录

**工具序列**：
1. `CLOSE_CREATE_LEAD` - 在 Close 中创建新线索 [必需]

**关键参数**：
- `name`：线索/公司名称
- `contacts`：与线索关联的联系人对象数组
- `custom`：自定义字段值，以键值对形式
- `status_id`：线索状态 ID

**注意事项**：
- Close 中的线索代表公司/组织，而非个人
- 联系人嵌套在线索中；先创建线索，然后包含联系人
- 自定义字段键使用自定义字段 ID（如 'custom.cf_XXX'），而非显示名称
- 重复线索检测不是自动的；创建前请先检查

### 2. 记录通话

**何时使用**：用户想要针对线索记录电话通话活动

**工具序列**：
1. `CLOSE_CREATE_CALL` - 记录通话活动 [必需]

**关键参数**：
- `lead_id`：关联线索的 ID
- `contact_id`：被呼叫联系人的 ID
- `direction`：'outbound'（呼出）或 'inbound'（呼入）
- `status`：通话状态（'completed'、'no-answer'、'busy' 等）
- `duration`：通话时长（秒）
- `note`：通话备注

**注意事项**：
- lead_id 是必需的；通话必须关联到线索
- 时长单位是秒，不是分钟
- 通话方向影响报告和分析
- contact_id 是可选的，但建议用于跟踪

### 3. 发送短信

**何时使用**：用户想要通过 Close 发送或记录短信

**工具序列**：
1. `CLOSE_CREATE_SMS` - 发送或记录短信 [必需]

**关键参数**：
- `lead_id`：关联线索的 ID
- `contact_id`：联系人的 ID
- `direction`：'outbound'（发出）或 'inbound'（接收）
- `text`：短信内容
- `status`：消息状态

**注意事项**：
- 短信功能需要配置 Close 电话/短信集成
- 所有短信活动都需要 lead_id
- 发送短信可能需要验证过的发送号码
- 根据运营商不同，消息长度限制可能适用

### 4. 管理任务

**何时使用**：用户想要创建或管理跟进任务

**工具序列**：
1. `CLOSE_CREATE_TASK` - 创建新任务 [必需]

**关键参数**：
- `lead_id`：关联线索的 ID
- `text`：任务描述
- `date`：任务截止日期
- `assigned_to`：受派人的用户 ID
- `is_complete`：任务是否已完成

**注意事项**：
- 任务关联到线索，而非联系人
- 日期格式应遵循 ISO 8601
- assigned_to 需要 Close 用户 ID，而非邮箱或姓名
- 没有日期的任务会出现在"无截止日期"部分

### 5. 管理笔记

**何时使用**：用户想要添加或获取线索笔记

**工具序列**：
1. `CLOSE_GET_NOTE` - 获取特定笔记 [必需]

**关键参数**：
- `note_id`：要获取的笔记 ID

**注意事项**：
- 笔记关联到线索
- 获取笔记需要笔记 ID；先搜索线索以找到笔记引用
- 笔记支持纯文本和基本格式

### 6. 删除活动

**何时使用**：用户想要删除通话记录或其他活动

**工具序列**：
1. `CLOSE_DELETE_CALL` - 删除通话活动 [必需]

**关键参数**：
- `call_id`：要删除的通话 ID

**注意事项**：
- 删除是永久性的，无法撤销
- 只有通话创建者或管理员可以删除通话
- 删除通话会将其从所有报告和时间线中移除

## 常见模式

### 线索和联系人关系

```
Close 数据模型：
- Lead（线索）= 公司/组织
  - Contact（联系人）= 个人（嵌套在线索中）
  - Activity（活动）= 通话、短信、邮件、笔记（链接到线索）
  - Task（任务）= 跟进项（链接到线索）
  - Opportunity（商机）= 交易（链接到线索）
```

### ID 解析

**线索 ID**：
```
1. 使用 Close 搜索 API 搜索线索
2. 从结果中提取 lead_id（格式：'lead_XXXXXXXXXXXXX'）
3. 在所有活动创建调用中使用 lead_id
```

**联系人 ID**：
```
1. 获取线索详情以获取嵌套的联系人
2. 提取 contact_id（格式：'cont_XXXXXXXXXXXXX'）
3. 在通话/短信活动中使用以实现准确跟踪
```

### 活动记录模式

```
1. 识别 lead_id 和可选的 contact_id
2. 使用 lead_id 创建活动（通话、短信、笔记）
3. 包含相关元数据（时长、方向、状态）
4. 如需要，创建跟进任务
```

## 已知注意事项

**ID 格式**：
- 线索 ID：'lead_XXXXXXXXXXXXX'
- 联系人 ID：'cont_XXXXXXXXXXXXX'
- 活动 ID 因类型而异：'acti_XXXXXXXXXXXXX'、'call_XXXXXXXXXXXXX'
- 自定义字段 ID：'custom.cf_XXXXXXXXXXXXX'
- 始终使用完整的 ID 字符串

**速率限制**：
- Close API 根据您的套餐有速率限制
- 在批量操作之间实施延迟
- 监控响应头中的速率限制状态
- 429 响应需要退避处理

**自定义字段**：
- 自定义字段通过其 API ID 引用，而非显示名称
- 不同的线索状态可能有不同的必填自定义字段
- 自定义字段类型（文本、数字、日期、下拉）强制执行值格式

**数据完整性**：
- 线索是主要实体；联系人和活动链接到线索
- 删除线索可能会级联删除其联系人和活动
- 批量操作应在执行前验证 ID

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 创建线索 | CLOSE_CREATE_LEAD | name, contacts, custom |
| 记录通话 | CLOSE_CREATE_CALL | lead_id, direction, status, duration |
| 发送短信 | CLOSE_CREATE_SMS | lead_id, text, direction |
| 创建任务 | CLOSE_CREATE_TASK | lead_id, text, date, assigned_to |
| 获取笔记 | CLOSE_GET_NOTE | note_id |
| 删除通话 | CLOSE_DELETE_CALL | call_id |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
