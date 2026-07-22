---
name: n8n-node-configuration
description: 操作感知的节点配置指导。当用户配置节点、理解属性依赖关系、确定必填字段、选择 get_node 详情级别或按节点类型学习常见配置模式时使用。
risk: unknown
source: community
---

# n8n 节点配置

操作感知节点配置的专业指导，涵盖属性依赖关系。

## 何时使用
- 需要为特定 resource 和 operation 正确配置 n8n 节点。
- 任务涉及必填字段、属性依赖或选择正确的 `get_node` 详情级别。
- 排查的是节点配置问题，而非整体工作流架构问题。

---

## 配置理念

**渐进式披露**：从最小配置开始，按需增加复杂度

配置最佳实践：
- `get_node` 配合 `detail: "standard"` 是最常用的发现模式
- 配置编辑间隔平均 56 秒
- 1-2K tokens 的响应即可覆盖 95% 的用例

**关键洞察**：大多数配置只需要 standard 详情，不需要完整 schema！

---

## 核心概念

### 1. 操作感知配置

**并非所有字段始终必填** — 取决于操作类型！

**示例**：Slack 节点
```javascript
// For operation='post'
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",  // Required for post
  "text": "Hello!"        // Required for post
}

// For operation='update'
{
  "resource": "message",
  "operation": "update",
  "messageId": "123",     // Required for update (different!)
  "text": "Updated!"      // Required for update
  // channel NOT required for update
}
```

**关键**：Resource + operation 决定哪些字段必填！

### 2. 属性依赖

**字段会根据其他字段的值出现/消失**

**示例**：HTTP Request 节点
```javascript
// When method='GET'
{
  "method": "GET",
  "url": "https://api.example.com"
  // sendBody not shown (GET doesn't have body)
}

// When method='POST'
{
  "method": "POST",
  "url": "https://api.example.com",
  "sendBody": true,       // Now visible!
  "body": {               // Required when sendBody=true
    "contentType": "json",
    "content": {...}
  }
}
```

**机制**：displayOptions 控制字段可见性

### 3. 渐进式发现

**使用合适的详情级别**：

1. **get_node({detail: "standard"})** — 默认
   - 快速概览（约 1-2K tokens）
   - 必填字段 + 常用选项
   - **优先使用** — 覆盖 95% 的需求

2. **get_node({mode: "search_properties", propertyQuery: "..."})** （查找特定字段）
   - 按名称查找属性
   - 用于查找 auth、body、headers 等

3. **get_node({detail: "full"})** （完整 schema）
   - 所有属性（约 3-8K tokens）
   - 仅在 standard 详情不足时使用

---

## 配置工作流

### 标准流程

```
1. 确定节点类型和操作
   ↓
2. 使用 get_node（默认 standard 详情）
   ↓
3. 配置必填字段
   ↓
4. 验证配置
   ↓
5. 若字段不清楚 → get_node({mode: "search_properties"})
   ↓
6. 按需添加可选字段
   ↓
7. 再次验证
   ↓
8. 部署
```

### 示例：配置 HTTP Request

**步骤 1**：明确需求
```javascript
// Goal: POST JSON to API
```

**步骤 2**：获取节点信息
```javascript
const info = get_node({
  nodeType: "nodes-base.httpRequest"
});

// Returns: method, url, sendBody, body, authentication required/optional
```

**步骤 3**：最小配置
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "authentication": "none"
}
```

**步骤 4**：验证
```javascript
validate_node({
  nodeType: "nodes-base.httpRequest",
  config,
  profile: "runtime"
});
// → Error: "sendBody required for POST"
```

**步骤 5**：添加必填字段
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "authentication": "none",
  "sendBody": true
}
```

**步骤 6**：再次验证
```javascript
validate_node({...});
// → Error: "body required when sendBody=true"
```

**步骤 7**：补全配置
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "={{$json.name}}",
      "email": "={{$json.email}}"
    }
  }
}
```

**步骤 8**：最终验证
```javascript
validate_node({...});
// → Valid! ✅
```

---

## get_node 详情级别

### Standard 详情（默认 — 优先使用！）

**✅ 初始配置**
```javascript
get_node({
  nodeType: "nodes-base.slack"
});
// detail="standard" is the default
```

**返回内容**（约 1-2K tokens）：
- 必填字段
- 常用选项
- 操作列表
- 元数据

**用途**：95% 的配置需求

### Full 详情（谨慎使用）

**✅ 当 standard 不够用时**
```javascript
get_node({
  nodeType: "nodes-base.slack",
  detail: "full"
});
```

**返回内容**（约 3-8K tokens）：
- 完整 schema
- 所有属性
- 所有嵌套选项

**警告**：响应较大，仅在 standard 不足时使用

### Search Properties 模式

**✅ 查找特定字段**
```javascript
get_node({
  nodeType: "nodes-base.httpRequest",
  mode: "search_properties",
  propertyQuery: "auth"
});
```

**用途**：查找 authentication、headers、body 等字段

### 决策树

```
┌─────────────────────────────────┐
│ 开始新节点配置？                 │
├─────────────────────────────────┤
│ 是 → get_node (standard)        │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ Standard 包含所需内容？          │
├─────────────────────────────────┤
│ 是 → 直接配置                    │
│ 否 → 继续                        │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ 查找特定字段？                   │
├─────────────────────────────────┤
│ 是 → search_properties 模式     │
│ 否 → 继续                        │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ 仍需更多详情？                   │
├─────────────────────────────────┤
│ 是 → get_node({detail: "full"}) │
└─────────────────────────────────┘
```

---

## 属性依赖深入

### displayOptions 机制

**字段有可见性规则**：

```javascript
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true],
      "method": ["POST", "PUT", "PATCH"]
    }
  }
}
```

**含义**：`body` 字段在以下条件满足时显示：
- sendBody = true 且
- method = POST、PUT 或 PATCH

### 常见依赖模式

#### 模式 1：布尔开关

**示例**：HTTP Request sendBody
```javascript
// sendBody controls body visibility
{
  "sendBody": true   // → body field appears
}
```

#### 模式 2：操作切换

**示例**：Slack resource/operation
```javascript
// Different operations → different fields
{
  "resource": "message",
  "operation": "post"
  // → Shows: channel, text, attachments, etc.
}

{
  "resource": "message",
  "operation": "update"
  // → Shows: messageId, text (different fields!)
}
```

#### 模式 3：类型选择

**示例**：IF 节点条件
```javascript
{
  "type": "string",
  "operation": "contains"
  // → Shows: value1, value2
}

{
  "type": "boolean",
  "operation": "equals"
  // → Shows: value1, value2, different operators
}
```

### 查找属性依赖

**使用 get_node 的 search_properties 模式**：
```javascript
get_node({
  nodeType: "nodes-base.httpRequest",
  mode: "search_properties",
  propertyQuery: "body"
});

// Returns property paths matching "body" with descriptions
```

**或使用 full 详情获取完整 schema**：
```javascript
get_node({
  nodeType: "nodes-base.httpRequest",
  detail: "full"
});

// Returns complete schema with displayOptions rules
```

**使用时机**：验证失败且不清楚字段为何缺失/必填时

---

## 常见节点模式

### 模式 1：Resource/Operation 节点

**示例**：Slack、Google Sheets、Airtable

**结构**：
```javascript
{
  "resource": "<entity>",      // What type of thing
  "operation": "<action>",     // What to do with it
  // ... operation-specific fields
}
```

**配置方法**：
1. 选择 resource
2. 选择 operation
3. 使用 get_node 查看操作特定要求
4. 配置必填字段

### 模式 2：HTTP 类节点

**示例**：HTTP Request、Webhook

**结构**：
```javascript
{
  "method": "<HTTP_METHOD>",
  "url": "<endpoint>",
  "authentication": "<type>",
  // ... method-specific fields
}
```

**依赖关系**：
- POST/PUT/PATCH → sendBody 可用
- sendBody=true → body 必填
- authentication != "none" → 需要凭证

### 模式 3：数据库节点

**示例**：Postgres、MySQL、MongoDB

**结构**：
```javascript
{
  "operation": "<query|insert|update|delete>",
  // ... operation-specific fields
}
```

**依赖关系**：
- operation="executeQuery" → query 必填
- operation="insert" → table + values 必填
- operation="update" → table + values + where 必填

### 模式 4：条件逻辑节点

**示例**：IF、Switch、Merge

**结构**：
```javascript
{
  "conditions": {
    "<type>": [
      {
        "operation": "<operator>",
        "value1": "...",
        "value2": "..."  // Only for binary operators
      }
    ]
  }
}
```

**依赖关系**：
- 二元运算符（equals、contains 等）→ value1 + value2
- 一元运算符（isEmpty、isNotEmpty）→ 仅 value1 + singleValue: true

---

## 操作特定配置

### Slack 节点示例

#### 发送消息
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",      // Required
  "text": "Hello!",           // Required
  "attachments": [],          // Optional
  "blocks": []                // Optional
}
```

#### 更新消息
```javascript
{
  "resource": "message",
  "operation": "update",
  "messageId": "1234567890",  // Required (different from post!)
  "text": "Updated!",         // Required
  "channel": "#general"       // Optional (can be inferred)
}
```

#### 创建频道
```javascript
{
  "resource": "channel",
  "operation": "create",
  "name": "new-channel",      // Required
  "isPrivate": false          // Optional
  // Note: text NOT required for this operation
}
```

### HTTP Request 节点示例

#### GET 请求
```javascript
{
  "method": "GET",
  "url": "https://api.example.com/users",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "httpHeaderAuth",
  "sendQuery": true,                    // Optional
  "queryParameters": {                  // Shows when sendQuery=true
    "parameters": [
      {
        "name": "limit",
        "value": "100"
      }
    ]
  }
}
```

#### POST JSON
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,                     // Required for POST
  "body": {                             // Required when sendBody=true
    "contentType": "json",
    "content": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

### IF 节点示例

#### 字符串比较（二元）
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.status}}",
        "operation": "equals",
        "value2": "active"              // Binary: needs value2
      }
    ]
  }
}
```

#### 空值检查（一元）
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.email}}",
        "operation": "isEmpty",
        // No value2 - unary operator
        "singleValue": true             // Auto-added by sanitization
      }
    ]
  }
}
```

---

## 处理条件性必填项

### 示例：HTTP Request Body

**场景**：body 字段有时必填，有时不必填

**规则**：
```
body 在以下情况必填：
  - sendBody = true 且
  - method IN (POST, PUT, PATCH, DELETE)
```

**如何发现**：
```javascript
// Option 1: Read validation error
validate_node({...});
// Error: "body required when sendBody=true"

// Option 2: Search for the property
get_node({
  nodeType: "nodes-base.httpRequest",
  mode: "search_properties",
  propertyQuery: "body"
});
// Shows: body property with displayOptions rules

// Option 3: Try minimal config and iterate
// Start without body, validation will tell you if needed
```

### 示例：IF 节点 singleValue

**场景**：singleValue 属性在一元运算符时出现

**规则**：
```
singleValue 在以下情况应为 true：
  - operation IN (isEmpty, isNotEmpty, true, false)
```

**好消息**：自动清理会修复此问题！

**手动检查**：
```javascript
get_node({
  nodeType: "nodes-base.if",
  detail: "full"
});
// Shows complete schema with operator-specific rules
```

---

## 配置反模式

### ❌ 不要：预先过度配置

**错误做法**：
```javascript
// Adding every possible field
{
  "method": "GET",
  "url": "...",
  "sendQuery": false,
  "sendHeaders": false,
  "sendBody": false,
  "timeout": 10000,
  "ignoreResponseCode": false,
  // ... 20 more optional fields
}
```

**正确做法**：
```javascript
// Start minimal
{
  "method": "GET",
  "url": "...",
  "authentication": "none"
}
// Add fields only when needed
```

### ❌ 不要：跳过验证

**错误做法**：
```javascript
// Configure and deploy without validating
const config = {...};
n8n_update_partial_workflow({...});  // YOLO
```

**正确做法**：
```javascript
// Validate before deploying
const config = {...};
const result = validate_node({...});
if (result.valid) {
  n8n_update_partial_workflow({...});
}
```

### ❌ 不要：忽略操作上下文

**错误做法**：
```javascript
// Same config for all Slack operations
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",
  "text": "..."
}

// Then switching operation without updating config
{
  "resource": "message",
  "operation": "update",  // Changed
  "channel": "#general",  // Wrong field for update!
  "text": "..."
}
```

**正确做法**：
```javascript
// Check requirements when changing operation
get_node({
  nodeType: "nodes-base.slack"
});
// See what update operation needs (messageId, not channel)
```

---

## 最佳实践

### ✅ 推荐

1. **从 get_node（standard 详情）开始**
   - 约 1-2K tokens 响应
   - 覆盖 95% 的配置需求
   - 默认详情级别

2. **迭代验证**
   - 配置 → 验证 → 修复 → 重复
   - 平均 2-3 轮迭代属正常
   - 仔细阅读验证错误信息

3. **卡住时使用 search_properties 模式**
   - 字段看似缺失时，搜索它
   - 理解什么控制字段可见性
   - `get_node({mode: "search_properties", propertyQuery: "..."})`

4. **尊重操作上下文**
   - 不同操作 = 不同要求
   - 切换操作时始终检查 get_node
   - 不要假设配置可直接复用

5. **信任自动清理**
   - 运算符结构会自动修正
   - 不要手动添加/移除 singleValue
   - IF/Switch 元数据在保存时自动添加

### ❌ 避免

1. **直接使用 detail="full"**
   - 先尝试 standard 详情
   - 仅在需要时升级
   - 完整 schema 为 3-8K tokens

2. **盲目配置**
   - 部署前务必验证
   - 理解字段为何必填
   - 对条件字段使用 search_properties

3. **不理解就复制配置**
   - 不同操作需要不同字段
   - 复制后要验证
   - 根据新上下文调整

4. **手动修复自动清理问题**
   - 让自动清理处理运算符结构
   - 专注业务逻辑
   - 保存后让系统修正结构

---

## 详细参考

特定主题的完整指南：

- **DEPENDENCIES.md** — 属性依赖和 displayOptions 的深入解析
- **OPERATION_PATTERNS.md** — 按节点类型分类的常见配置模式

---

## 总结

**配置策略**：
1. 从 `get_node` 开始（默认 standard 详情）
2. 为操作配置必填字段
3. 验证配置
4. 卡住时搜索属性
5. 迭代直到有效（平均 2-3 轮）
6. 自信部署

**核心原则**：
- **操作感知**：不同操作 = 不同要求
- **渐进式披露**：从最小开始，按需添加
- **依赖感知**：理解字段可见性规则
- **验证驱动**：让验证引导配置

**相关技能**：
- **n8n MCP Tools Expert** — 如何正确使用发现工具
- **n8n Validation Expert** — 解读验证错误
- **n8n Expression Syntax** — 配置表达式字段
- **n8n Workflow Patterns** — 使用正确配置应用模式

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，应停止并请求澄清。
