---
name: n8n-workflow-patterns
description: "构建 n8n 工作流的经过验证的架构模式。触发词：n8n工作流模式、n8n架构模式、工作流设计、webhook处理、API集成、定时任务、数据库同步、AI代理工作流、n8n workflow patterns"
risk: unknown
source: community
---

# n8n 工作流模式

构建 n8n 工作流的经过验证的架构模式。

## 何时使用
- 在构建 n8n 工作流之前，需要选择一种架构模式。
- 任务涉及 webhook 处理、API 集成、定时任务、数据库同步或 AI 代理工作流设计。
- 你需要的是高层级的工作流结构，而非逐节点排查问题。

---

## 5 种核心模式

基于实际工作流使用分析：

1. **Webhook 处理**（最常见）
   - 接收 HTTP 请求 → 处理 → 输出
   - 模式：Webhook → 验证 → 转换 → 响应/通知

2. **[HTTP API 集成]**
   - 从 REST API 获取数据 → 转换 → 存储/使用
   - 模式：触发器 → HTTP Request → 转换 → 操作 → 错误处理

3. **数据库操作**
   - 读取/写入/同步数据库数据
   - 模式：定时 → 查询 → 转换 → 写入 → 验证

4. **AI 代理工作流**
   - 带工具和记忆的 AI 代理
   - 模式：触发器 → AI Agent（模型 + 工具 + 记忆）→ 输出

5. **定时任务**
   - 周期性自动化工作流
   - 模式：定时 → 获取 → 处理 → 投递 → 日志

---

## 模式选择指南

### 各模式的适用场景：

**Webhook 处理** - 适用于：
- 从外部系统接收数据
- 构建集成（Slack 命令、表单提交、GitHub webhook）
- 需要对事件即时响应
- 示例："接收 Stripe 支付 webhook → 更新数据库 → 发送确认"

**HTTP API 集成** - 适用于：
- 从外部 API 获取数据
- 与第三方服务同步
- 构建数据管道
- 示例："获取 GitHub issues → 转换 → 创建 Jira 工单"

**数据库操作** - 适用于：
- 数据库之间同步
- 按计划运行数据库查询
- ETL 工作流
- 示例："读取 Postgres 记录 → 转换 → 写入 MySQL"

**AI 代理工作流** - 适用于：
- 构建对话式 AI
- 需要带工具访问的 AI
- 多步推理任务
- 示例："与可搜索文档、查询数据库、发送邮件的 AI 对话"

**定时任务** - 适用于：
- 周期性报告或摘要
- 定期数据获取
- 维护任务
- 示例："每日：获取分析数据 → 生成报告 → 邮件发送团队"

---

## 通用工作流组件

所有模式共享以下构建块：

### 1. 触发器
- **Webhook** - HTTP 端点（即时）
- **Schedule** - 基于 Cron 的定时（周期性）
- **Manual** - 点击执行（测试）
- **Polling** - 检查变更（间隔）

### 2. 数据源
- **HTTP Request** - REST API
- **Database 节点** - Postgres、MySQL、MongoDB
- **Service 节点** - Slack、Google Sheets 等
- **Code** - 自定义 JavaScript/Python

### 3. 转换
- **Set** - 映射/转换字段
- **Code** - 复杂逻辑
- **IF/Switch** - 条件路由
- **Merge** - 合并数据流

### 4. 输出
- **HTTP Request** - 调用 API
- **Database** - 写入数据
- **Communication** - Email、Slack、Discord
- **Storage** - 文件、云存储

### 5. 错误处理
- **Error Trigger** - 捕获工作流错误
- **IF** - 检查错误条件
- **Stop and Error** - 显式失败
- **Continue On Fail** - 逐节点设置

---

## 工作流创建检查清单

构建任何工作流时，请遵循此检查清单：

### 规划阶段
- [ ] 识别模式（webhook、API、数据库、AI、定时）
- [ ] 列出所需节点（使用 search_nodes）
- [ ] 理解数据流（输入 → 转换 → 输出）
- [ ] 规划错误处理策略

### 实现阶段
- [ ] 使用合适的触发器创建工作流
- [ ] 添加数据源节点
- [ ] 配置认证/凭证
- [ ] 添加转换节点（Set、Code、IF）
- [ ] 添加输出/操作节点
- [ ] 配置错误处理

### 验证阶段
- [ ] 验证每个节点配置（validate_node）
- [ ] 验证完整工作流（validate_workflow）
- [ ] 使用样本数据测试
- [ ] 处理边界情况（空数据、错误）

### 部署阶段
- [ ] 检查工作流设置（执行顺序、超时、错误处理）
- [ ] 使用 `activateWorkflow` 操作激活工作流
- [ ] 监控首次执行
- [ ] 记录工作流用途和数据流

---

## 数据流模式

### 线性流
```
Trigger → Transform → Action → End
```
**适用场景**：单路径的简单工作流

### 分支流
```
Trigger → IF → [True Path]
             └→ [False Path]
```
**适用场景**：基于条件执行不同操作

### 并行处理
```
Trigger → [Branch 1] → Merge
       └→ [Branch 2] ↗
```
**适用场景**：可同时运行的独立操作

### 循环模式
```
Trigger → Split in Batches → Process → Loop (until done)
```
**适用场景**：分块处理大数据集

### 错误处理模式
```
Main Flow → [Success Path]
         └→ [Error Trigger → Error Handler]
```
**适用场景**：需要独立的错误处理工作流

---

## 常见陷阱

### 1. Webhook 数据结构
**问题**：无法访问 webhook 载荷数据

**解决方案**：数据嵌套在 `$json.body` 下
```javascript
❌ {{$json.email}}
✅ {{$json.body.email}}
```
参见：n8n Expression Syntax 技能

### 2. 多个输入项
**问题**：节点处理所有输入项，但我只需要处理一个

**解决方案**：使用"Execute Once"模式或仅处理第一项
```javascript
{{$json[0].field}}  // 仅第一项
```

### 3. 认证问题
**问题**：API 调用返回 401/403 失败

**解决方案**：
- 正确配置凭证
- 使用"Credentials"区域，而非参数
- 在工作流激活前测试凭证

### 4. 节点执行顺序
**问题**：节点以意外顺序执行

**解决方案**：检查工作流设置 → Execution Order
- v0：从上到下（旧版）
- v1：基于连接（推荐）

### 5. 表达式错误
**问题**：表达式显示为字面文本

**解决方案**：在表达式周围使用 {{}}
- 详见 n8n Expression Syntax 技能

---

## 与其他技能的集成

以下技能与工作流模式配合使用：

**n8n MCP Tools Expert** - 用于：
- 查找模式所需节点（search_nodes）
- 了解节点操作（get_node）
- 创建工作流（n8n_create_workflow）
- 部署模板（n8n_deploy_template）
- 使用 ai_agents_guide 获取 AI 模式指导

**n8n Expression Syntax** - 用于：
- 在转换节点中编写表达式
- 正确访问 webhook 数据（{{$json.body.field}}）
- 引用前置节点（{{$node["Node Name"].json.field}}）

**n8n Node Configuration** - 用于：
- 配置模式节点的具体操作
- 了解节点特定需求

**n8n Validation Expert** - 用于：
- 验证工作流结构
- 修复验证错误
- 确保部署前工作流正确性

---

## 模式统计

常见工作流模式：

**最常见触发器**：
1. Webhook - 35%
2. Schedule（周期性任务）- 28%
3. Manual（测试/管理）- 22%
4. Service 触发器（Slack、邮件等）- 15%

**最常见转换**：
1. Set（字段映射）- 68%
2. Code（自定义逻辑）- 42%
3. IF（条件路由）- 38%
4. Switch（多条件）- 18%

**最常见输出**：
1. HTTP Request（API）- 45%
2. Slack - 32%
3. Database 写入 - 28%
4. Email - 24%

**平均工作流复杂度**：
- 简单（3-5 个节点）：42%
- 中等（6-10 个节点）：38%
- 复杂（11+ 个节点）：20%

---

## 快速入门示例

### 示例 1：简单 Webhook → Slack
```
1. Webhook (path: "form-submit", POST)
2. Set (map form fields)
3. Slack (post message to #notifications)
```

### 示例 2：定时报告
```
1. Schedule (daily at 9 AM)
2. HTTP Request (fetch analytics)
3. Code (aggregate data)
4. Email (send formatted report)
5. Error Trigger → Slack (notify on failure)
```

### 示例 3：数据库同步
```
1. Schedule (every 15 minutes)
2. Postgres (query new records)
3. IF (check if records exist)
4. MySQL (insert records)
5. Postgres (update sync timestamp)
```

### 示例 4：AI 助手
```
1. Webhook (receive chat message)
2. AI Agent
   ├─ OpenAI Chat Model (ai_languageModel)
   ├─ HTTP Request Tool (ai_tool)
   ├─ Database Tool (ai_tool)
   └─ Window Buffer Memory (ai_memory)
3. Webhook Response (send AI reply)
```

### 示例 5：API 集成
```
1. Manual Trigger (for testing)
2. HTTP Request (GET /api/users)
3. Split In Batches (process 100 at a time)
4. Set (transform user data)
5. Postgres (upsert users)
6. Loop (back to step 3 until done)
```

---

## 详细模式文件

各模式的完整指导：

- **webhook_processing.md** - Webhook 模式、数据结构、响应处理
- **http_api_integration** - REST API、认证、分页、重试
- **database_operations.md** - 查询、同步、事务、批处理
- **ai_agent_workflow.md** - AI 代理、工具、记忆、langchain 节点
- **scheduled_tasks.md** - Cron 定时、报告、维护任务

---

## 真实模板示例

来自 n8n 模板库：

**Template #2947**：天气推送到 Slack
- 模式：定时任务
- 节点：Schedule → HTTP Request (weather API) → Set → Slack
- 复杂度：简单（4 个节点）

**Webhook 处理**：最常见模式
- 最常见：表单提交、支付 webhook、聊天集成

**HTTP API**：常见模式
- 最常见：数据获取、第三方集成

**数据库操作**：常见模式
- 最常见：ETL、数据同步、备份工作流

**AI 代理**：使用量增长中
- 最常见：聊天机器人、内容生成、数据分析

使用 n8n-mcp 工具中的 `search_templates` 和 `get_template` 查找示例！

---

## 最佳实践

### ✅ 推荐

- 从能解决问题的最简单模式开始
- 在构建前规划工作流结构
- 所有工作流都使用错误处理
- 激活前使用样本数据测试
- 遵循工作流创建检查清单
- 使用描述性节点名称
- 记录复杂工作流（notes 字段）
- 部署后监控工作流执行

### ❌ 不推荐

- 一次性构建整个工作流（要迭代！平均编辑间隔 56 秒）
- 激活前跳过验证
- 忽略错误场景
- 简单模式够用时使用复杂模式
- 在参数中硬编码凭证
- 忘记处理空数据情况
- 没有清晰边界地混合多种模式
- 未经测试直接部署

---

## 总结

**要点**：
1. **5 种核心模式**覆盖 90%+ 的工作流用例
2. **Webhook 处理**是最常见的模式
3. 每个工作流都使用**工作流创建检查清单**
4. **规划模式** → **选择节点** → **构建** → **验证** → **部署**
5. 与其他技能集成完成完整的工作流开发

**下一步**：
1. 识别你的用例模式
2. 阅读详细模式文件
3. 使用 n8n MCP Tools Expert 查找节点
4. 遵循工作流创建检查清单
5. 使用 n8n Validation Expert 验证

**相关技能**：
- n8n MCP Tools Expert - 查找和配置节点
- n8n Expression Syntax - 正确编写表达式
- n8n Validation Expert - 验证和修复错误
- n8n Node Configuration - 配置具体操作

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
