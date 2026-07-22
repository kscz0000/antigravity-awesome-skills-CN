---
name: zapier-make-patterns
description: 无代码自动化让工作流构建大众化。Zapier 和 Make（原 Integromat）让非开发者无需编写代码即可自动化业务流程。但无代码不等于无复杂度——这些平台有自己的模式、陷阱和崩溃点。触发词：Zapier、Make、Integromat、无代码自动化、Zap、场景、工作流构建器、业务流程自动化、触发器动作、连接应用、自动化
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Zapier & Make 模式

无代码自动化让工作流构建大众化。Zapier 和 Make（原 Integromat）让非开发者无需编写代码即可自动化业务流程。但无代码不等于无复杂度——这些平台有自己的模式、陷阱和崩溃点。

本技能涵盖何时使用哪个平台、如何构建可靠的自动化，以及何时升级到基于代码的解决方案。核心洞察：Zapier 优化简单性和集成数量（7000+ 应用），Make 优化功能强大和成本效率（可视化分支、基于操作的定价）。

关键区别：无代码在失效之前都能正常工作。了解其边界。

## 原则

- 从简单开始，仅在需要时增加复杂度
- 上线前用真实数据测试
- 用清晰的命名记录每个自动化
- 监控错误——95% 错误率会自动禁用 Zap
- 知道何时升级到基于代码的解决方案
- 操作/任务要花钱——高效设计

## 能力

- zapier
- make
- integromat
- no-code-automation
- zaps
- scenarios
- workflow-builders
- business-process-automation

## 范围

- code-based-workflows → workflow-automation
- browser-automation → browser-automation
- custom-integrations → backend
- api-development → api-designer

## 工具

### 平台

- Zapier - 何时使用：简单自动化、最大应用覆盖、初学者 备注：7000+ 集成、线性工作流、基于任务的定价
- Make - 何时使用：复杂工作流、可视化分支、注重预算 备注：可视化场景、操作定价、强大的数据处理
- n8n - 何时使用：自托管、代码友好、无限操作 备注：开源、可添加自定义代码、技术用户

### AI 功能

- Zapier Agents - 何时使用：AI 驱动的自主自动化 备注：自然语言指令、7000+ 应用访问
- Zapier Copilot - 何时使用：AI 辅助构建 Zap 备注：描述工作流，AI 构建它
- Zapier MCP - 何时使用：LLM 工具访问 Zapier 操作 备注：30,000+ 操作可供 AI 模型使用

## 模式

### 基础触发器-动作模式

单个触发器触发一个或多个动作

**何时使用**：简单通知、数据同步、基础工作流

# BASIC TRIGGER-ACTION:

"""
[Trigger] → [Action]
  e.g., New Email → Create Task
"""

## Zapier 示例
"""
Zap Name: "Gmail New Email → Todoist Task"

TRIGGER: Gmail - New Email
  - From: specific-sender@example.com
  - Has attachment: yes

ACTION: Todoist - Create Task
  - Project: Inbox
  - Content: {{Email Subject}}
  - Description: From: {{Email From}}
  - Due date: Tomorrow
"""

## Make 示例
"""
Scenario: "Gmail to Todoist"

[Gmail: Watch Emails] → [Todoist: Create a Task]

Gmail Module:
  - Folder: INBOX
  - From: specific-sender@example.com

Todoist Module:
  - Project ID: (select from dropdown)
  - Content: {{1.subject}}
  - Due String: tomorrow
"""

## 最佳实践：
- 使用描述性的 Zap/场景名称
- 用真实样本数据测试
- 使用过滤器防止意外运行

### 多步顺序模式

按顺序执行的动作链

**何时使用**：多应用工作流、数据丰富管道

# MULTI-STEP SEQUENTIAL:

"""
[Trigger] → [Action 1] → [Action 2] → [Action 3]
Each step's output available to subsequent steps
"""

## Zapier 多步 Zap
"""
Zap: "New Lead → CRM → Slack → Email"

1. TRIGGER: Typeform - New Entry
   - Form: Lead Capture Form

2. ACTION: HubSpot - Create Contact
   - Email: {{Typeform Email}}
   - First Name: {{Typeform First Name}}
   - Lead Source: "Website Form"

3. ACTION: Slack - Send Channel Message
   - Channel: #sales-leads
   - Message: "New lead: {{Typeform Name}} from {{Typeform Company}}"

4. ACTION: Gmail - Send Email
   - To: {{Typeform Email}}
   - Subject: "Thanks for reaching out!"
   - Body: (template with personalization)
"""

## Make 场景
"""
[Typeform] → [HubSpot] → [Slack] → [Gmail]

- Each module passes data to the next
- Use {{N.field}} to reference module N's output
- Add error handlers between critical steps
"""

### 条件分支模式

根据条件执行不同动作

**何时使用**：对不同数据类型进行不同处理

# CONDITIONAL BRANCHING:

"""
              ┌→ [Action A] (condition met)
[Trigger] ───┤
              └→ [Action B] (condition not met)
"""

## Zapier 路径（需要 Pro+ 版本）
"""
Zap: "Route Support Tickets"

1. TRIGGER: Zendesk - New Ticket

2. PATH A: If priority = "urgent"
   - Slack: Post to #urgent-support
   - PagerDuty: Create incident

3. PATH B: If priority = "normal"
   - Slack: Post to #support
   - Asana: Create task

4. PATH C: Otherwise (catch-all)
   - Slack: Post to #support-overflow
"""

## Make 路由器
"""
[Zendesk: Watch Tickets]
      ↓
[Router]
   ├── Route 1: priority = urgent
   │     └→ [Slack] → [PagerDuty]
   │
   ├── Route 2: priority = normal
   │     └→ [Slack] → [Asana]
   │
   └── Fallback route
         └→ [Slack: overflow]

# Make's visual router makes complex branching clear
"""

## 最佳实践：
- 始终设置兜底/else 路径
- 独立测试每条路径
- 记录哪些条件触发哪条路径

### 数据转换模式

在应用之间清洗、格式化和转换数据

**何时使用**：应用期望不同的数据格式

# DATA TRANSFORMATION:

## Zapier 格式化器
"""
Common transformations:

1. Text manipulation:
   - Split text: "John Doe" → First: "John", Last: "Doe"
   - Capitalize: "john" → "John"
   - Replace: Remove special characters

2. Date formatting:
   - Convert: "2024-01-15" → "January 15, 2024"
   - Adjust: Add 7 days to date

3. Numbers:
   - Format currency: 1000 → "$1,000.00"
   - Spreadsheet formula: =SUM(A1:A10)

4. Lookup tables:
   - Map status codes: "1" → "Active", "2" → "Pending"
"""

## Make 数据函数
"""
Make has powerful built-in functions:

Text:
  {{lower(1.email)}}           # Lowercase
  {{substring(1.name; 0; 10)}} # First 10 chars
  {{replace(1.text; "-"; "")}} # Remove dashes

Arrays:
  {{first(1.items)}}           # First item
  {{length(1.items)}}          # Count items
  {{map(1.items; "id")}}       # Extract field

Dates:
  {{formatDate(1.date; "YYYY-MM-DD")}}
  {{addDays(now; 7)}}

Math:
  {{round(1.price * 0.8; 2)}}  # 20% discount, 2 decimals
"""

## 最佳实践：
- 在工作流中尽早转换
- 使用过滤器跳过无效数据
- 记录转换过程以便调试

### 错误处理模式

优雅地处理故障

**何时使用**：任何生产自动化

# ERROR HANDLING:

## Zapier 错误处理
"""
1. Built-in retry (automatic):
   - Zapier retries failed actions automatically
   - Exponential backoff for temporary failures

2. Error handling step:
   Zap:
     1. [Trigger]
     2. [Action that might fail]
     3. [Error Handler]
        - If error → [Slack: Alert team]
        - If error → [Email: Send report]

3. Path-based handling:
   [Action] → Path A: Success → [Continue]
            → Path B: Error → [Alert + Log]
"""

## Make 错误处理器
"""
Make has visual error handling:

[Module] ──┬── Success → [Next Module]
           │
           └── Error → [Error Handler]

Error handler types:
1. Break: Stop scenario, send notification
2. Rollback: Undo completed operations
3. Commit: Save partial results, continue
4. Ignore: Skip error, continue with next item

Example:
[API Call] → Error Handler (Ignore)
           → [Log to Airtable: "Failed: {{error.message}}"]
           → Continue scenario
"""

## 最佳实践：
- 始终为外部 API 添加错误处理器
- 将错误记录到电子表格/数据库
- 为关键故障设置 Slack/邮件告警
- 测试故障场景，而不仅是成功场景

### 批处理模式

高效处理多个项目

**何时使用**：导入数据、批量操作

# BATCH PROCESSING:

## Zapier 循环
"""
Zap: "Process Order Items"

1. TRIGGER: Shopify - New Order
   - Returns: order with line_items array

2. LOOPING: For each item in line_items
   - Create inventory adjustment
   - Update product count
   - Log to spreadsheet

Note: Each loop iteration counts as tasks!
10 items = 10 tasks consumed
"""

## Make 迭代器
"""
[Webhook: Receive Order]
      ↓
[Iterator: line_items]
      ↓ (processes each item)
[Inventory: Adjust Stock]
      ↓
[Aggregator: Collect Results]
      ↓
[Slack: Summary Message]

Iterator creates one bundle per item.
Aggregator combines results back together.
Use Array Aggregator for collecting processed items.
"""

## 最佳实践：
- 使用聚合器合并结果
- 注意批量限制（某些 API 限制为 100）
- 关注操作/任务数量以控制成本
- 为有速率限制的 API 添加延迟

### 定时自动化模式

基于时间的触发器而非事件触发

**何时使用**：每日报告、定期同步、批处理任务

# SCHEDULED AUTOMATION:

## Zapier 定时触发器
"""
Zap: "Daily Sales Report"

TRIGGER: Schedule by Zapier
  - Every: Day
  - Time: 8:00 AM
  - Timezone: America/New_York

ACTIONS:
  1. Google Sheets: Get rows (yesterday's sales)
  2. Formatter: Calculate totals
  3. Gmail: Send report to team
"""

## Make 定时场景
"""
Scenario Schedule Options:
  - Run once (manual)
  - At regular intervals (every X minutes)
  - Advanced: Cron expression (0 8 * * *)

[Scheduled Trigger: Every day at 8 AM]
      ↓
[Google Sheets: Search Rows]
      ↓
[Iterator: Process each row]
      ↓
[Aggregator: Sum totals]
      ↓
[Gmail: Send Report]
"""

## 最佳实践：
- 考虑时区差异
- 为长时间运行的任务添加缓冲时间
- 记录执行时间以便监控
- 不要精确安排在午夜（高峰期）

## 常见陷阱

### 在下拉字段中使用文本而非 ID

严重程度：严重

场景：使用下拉选择配置动作

症状：
"Bad Request" 错误。"Invalid value" 消息。输入看起来正确但动作失败。从下拉菜单选择时正常，使用动态值时失败。

原因：
下拉菜单显示人类可读的文本，但向 API 发送的是 ID。当你输入"Marketing Team"而不是选择它时，Zapier 会尝试将该文本作为 ID 发送，而 API 无法识别。

推荐修复：

# ALWAYS use dropdowns to select, don't type

# If you need dynamic values:

## Zapier 方法：
1. 先添加"查找"或"搜索"动作
   - HubSpot: Find Contact → returns contact_id
   - Slack: Find User by Email → returns user_id

2. 在后续动作中使用返回的 ID
   - Dropdown: Use Custom Value
   - Select the ID from the search step

## Make 方法：
1. 先添加搜索模块
   - Search Contacts: filter by email
   - Returns: contact_id

2. 将 ID 映射到后续模块
   - Contact ID: {{2.id}} (from search module)

# 常见容易出错的 ID 字段：
- Slack、Teams 中的用户/成员 ID
- CRM 中的联系人/公司 ID
- 项目工具中的项目/文件夹 ID
- 内容系统中的分类/标签 ID

### Zap 在 95% 错误率时自动禁用

严重程度：严重

场景：运行频繁出错的 Zap

症状：
Zap 突然停止运行。收到自动禁用的邮件通知。"This Zap was automatically turned off" 消息。数据停止同步。

原因：
Zapier 会自动禁用 7 天内错误率达到 95% 或更高的 Zap。这可以防止失控的自动化故障消耗你的任务配额并造成数据问题。

推荐修复：

# 预防：

1. 添加错误处理步骤：
   - 使用 Path: If error → [Log + Alert]
   - 为故障添加兜底动作

2. 使用过滤器防止错误数据：
   - 仅在邮箱存在时继续
   - 仅在金额 > 0 时继续
   - 过滤掉测试/无效条目

3. 定期监控任务历史：
   - 检查反复出现的错误
   - 在达到 95% 阈值前修复问题

# 恢复：

1. 检查任务历史中的错误模式
2. 修复根本原因（认证、错误数据、API 变更）
3. 用样本数据测试
4. 手动重新启用 Zap
5. 密切监控接下来 24 小时

# 常见原因：
- 认证令牌过期
- API 速率限制
- 已连接应用中的字段名变更
- 无效的数据格式

### 循环消耗意外的任务数量

严重程度：高

场景：处理数组或多个项目

症状：
任务配额意外耗尽。一次 Zap 运行显示为 100+ 任务。月度限额几天内就用完。"You've used X of Y tasks" 惊讶。

原因：
在 Zapier 中，循环的每次迭代都计为单独的任务。如果 webhook 传递了一个包含 50 个行项目的订单，而你循环处理每个项目，那就是一个订单消耗 50+ 任务。

推荐修复：

# 理解计算方式：

包含 10 个项目的订单，每个项目 5 个动作：
= 1 个触发器 + (10 个项目 × 5 个动作) = 51 个任务

# 减少任务使用量的策略：

1. 尽可能批量操作：
   - 使用"Create Many Rows"而不是循环 + 创建
   - 使用批量 API 端点

2. 发送前聚合：
   - 收集所有项目
   - 发送一条汇总消息，而不是每个项目一条

3. 循环前过滤：
   - 仅处理需要操作的项目
   - 跳过未变更/重复的项目

4. 大量数据处理考虑使用 Make：
   - Make 使用操作数，而非每个动作的任务数
   - 对循环更具成本效益

# Make 方法：
[Iterator] → [Actions] → [Aggregator]
- Pay for operations (module executions)
- Not per-action like Zapier

### 应用更新导致现有 Zap 崩溃

严重程度：高

场景：你连接的应用发布更新

症状：
正常工作的 Zap 突然失败。"Field not found" 错误。输出中的数据格式不同。昨天还能用的动作今天失败了。

原因：
当已连接的应用更新其 API 时，字段名可能变更、出现新的必填字段，或数据格式发生变化。Zapier/Make 集成可能不会立即更新以匹配。

推荐修复：

# 当 Zap 在应用更新后崩溃时：

1. 检查任务历史中的具体错误
2. 打开 Zap 编辑器查看字段映射问题
3. 重新选择触发器/动作以刷新模式
4. 重新映射显示为"unknown"的字段
5. 用新的样本数据测试

# 预防：

1. 订阅关键应用的更新日志
2. 保持连接授权新鲜
3. 在重大应用更新后测试 Zap
4. 记录你的字段映射
5. 使用测试/副本 Zap 进行实验

# 如果集成已过时：
- 检查 Zapier/Make 状态页面
- 向支持团队报告问题
- 考虑临时使用 webhook 替代

# 常见问题来源：
- CRM 字段重构
- API 版本升级
- OAuth 范围变更
- 新增必需权限

### 认证令牌过期

严重程度：高

场景：使用 OAuth 连接到应用

症状：
"Authentication failed" 错误。"Please reconnect" 消息。Zap 运行数周后突然失败。多个应用同时失败。

原因：
OAuth 令牌会过期。某些应用每 60-90 天需要重新认证。如果连接应用的用户离开公司，其连接可能停止工作。

推荐修复：

# 立即修复：
1. 进入 Settings → Apps
2. 找到有问题的应用
3. 重新连接（重新授权）
4. 测试受影响的 Zap

# 预防：

1. 使用服务账号进行连接
   - 不要用个人账号连接
   - 使用共享的团队邮箱/账号

2. 监控连接健康
   - 定期检查 Apps 页面
   - 为已知过期时间设置日历提醒

3. 记录谁连接了什么
   - 在电子表格中跟踪
   - 人员离职时的交接流程

4. 优先使用不过期的连接
   - 可用时选择 API 密钥而非 OAuth
   - 长期有效的令牌

# Zapier 企业版：
- 管理连接的管理员控制
- SSO 集成
- 集中化连接管理

### Webhook 丢失或重复事件

严重程度：中

场景：使用 webhook 作为触发器

症状：
某些事件从不触发 Zap。同一事件触发多次。自动化行为不一致。"有时能用。"

原因：
Webhook 是即发即忘的。如果 Zapier 的接收端点缓慢或不可用，webhook 可能失败。某些系统会重试 webhook，导致重复。网络问题会丢失事件。

推荐修复：

# 处理重复：

1. 添加去重逻辑：
   - Filter: Only continue if ID not in Airtable
   - First action: Check if already processed

2. 使用幂等性：
   - 存储已处理的 ID
   - 如果 ID 已存在则跳过

## Zapier 示例：
[Webhook Trigger]
   ↓
[Airtable: Find Records] - search by event_id
   ↓
[Filter: Only continue if not found]
   ↓
[Process Event]
   ↓
[Airtable: Create Record] - store event_id

# 处理遗漏事件：

1. 对关键数据使用轮询触发器
   - 不那么实时但更可靠
   - 能捕获停机期间的事件

2. 实现对账：
   - 定时 Zap 检查数据缺口
   - 比较源数据与已处理数据

3. 检查源系统的重试设置：
   - 某些系统在失败时重试
   - 配置重试次数/时间

### Make 错误重试消耗操作数

严重程度：中

场景：包含失败模块的场景

症状：
操作配额快速耗尽。场景运行"成功"但消耗了大量操作。同一场景运行次数超出预期。

原因：
Make 按模块执行计数操作，包括失败尝试和重试。错误处理器模块也会消耗操作。失败并重试的场景可能消耗 3-5 倍的预期操作数。

推荐修复：

# 理解操作计数：

成功运行：每个模块 = 1 次操作
失败 + 重试 (3次)：该模块 3 次操作
错误处理器：每个处理器模块额外 1 次操作

# 减少操作浪费：

1. 添加尽早中断的错误处理器：
   [Module] → Error → [Break] (1 additional op)
   vs
   [Module] → Error → [Log] → [Alert] → [Update] (3+ ops)

2. 适当时使用忽略而非重试：
   - 如果失败是预期的（记录已存在）
   - 如果重试无济于事（错误数据）

3. 在昂贵操作前预验证：
   [Check Data] → Filter → [API Call]
   - 在消耗操作前快速失败

4. 优化场景调度：
   - 如果每小时足够就不要每分钟运行
   - 尽可能使用 webhook 实现实时性

# 监控使用量：
- 检查 Operations 仪表盘
- 设置使用量告警
- 审查高消耗场景

### 定时触发器中的时区不匹配

严重程度：中

场景：设置定时自动化

症状：
Zap 在错误的时间运行。"9 AM" 触发器在下午 2 点触发。不同天行为不同。夏令时导致小时偏移。

原因：
Zapier 以你的本地时区显示时间，但可能以 UTC 存储。如果你更换时区或发生夏令时，定时时间会偏移。不同时区的团队成员看到不同的时间。

推荐修复：

# 最佳实践：

1. 在计划中明确设置时区：
   - 不要依赖浏览器检测
   - 使用业务时区，而非个人时区

2. 在 Zap 名称中记录：
   - "Daily Report 9AM EST"
   - 在描述中包含时区

3. 在夏令时转换前后测试：
   - 在夏令时边界处安排变更
   - 验证变更前后的时间

4. 对于全球团队：
   - 使用 UTC 作为标准
   - 在描述中转换为本地时间

5. 考虑缓冲时间：
   - 不要精确安排在午夜
   - 避免整点（高峰期）

## Make 时区处理：
- 场景使用账户时区设置
- formatDate() 函数遵循时区
- 使用 parseDate() 并指定明确时区

## 协作

### 委派触发器

- 自动化需要自定义代码 -> workflow-automation（基于代码的解决方案，如 Inngest、Temporal）
- 工作流中需要浏览器自动化 -> browser-automation（Playwright/Puppeteer 集成）
- 构建自定义 API 集成 -> api-designer（API 设计与实现）
- 自动化需要 AI 能力 -> agent-tool-builder（AI 代理工具和 Zapier MCP）
- 大量数据处理 -> backend（自定义后端处理）
- 需要自托管自动化 -> devops（n8n 或自定义工作流部署）

## 相关技能

配合使用：`workflow-automation`、`agent-tool-builder`、`backend`、`api-designer`

## 何时使用
- 用户提及或暗示：zapier
- 用户提及或暗示：make
- 用户提及或暗示：integromat
- 用户提及或暗示：zap
- 用户提及或暗示：scenario
- 用户提及或暗示：no-code automation
- 用户提及或暗示：trigger action
- 用户提及或暗示：workflow automation
- 用户提及或暗示：connect apps
- 用户提及或暗示：automate

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
