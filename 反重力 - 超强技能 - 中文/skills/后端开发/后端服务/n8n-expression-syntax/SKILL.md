---
name: n8n-expression-syntax
description: 验证 n8n expression 语法并修复常见错误。当用户编写 n8n expression、使用 {{}} 语法、访问 $json/$node 变量、排查 expression 错误或在 workflow 中处理 webhook 数据时使用。
risk: unknown
source: community
---

# n8n Expression 语法

在 workflow 中编写正确 n8n expression 的专家指南。

## 使用场景
- 需要编写或调试使用 `{{ ... }}` 语法的 n8n expression。
- 任务涉及 `$json`、`$node`、webhook payload 或 expression 相关的 workflow 错误。
- 需要在 n8n 节点和参数中使用语法正确的动态值。

---

## Expression 格式

n8n 中所有动态内容都使用**双花括号**：

```
{{expression}}
```

**示例**：
```
✅ {{$json.email}}
✅ {{$json.body.name}}
✅ {{$node["HTTP Request"].json.data}}
❌ $json.email  (无花括号 - 被视为纯文本)
❌ {$json.email}  (单花括号 - 无效)
```

---

## 核心变量

### $json - 当前节点输出

访问当前节点的数据：

```javascript
{{$json.fieldName}}
{{$json['field with spaces']}}
{{$json.nested.property}}
{{$json.items[0].name}}
```

### $node - 引用其他节点

访问任意前置节点的数据：

```javascript
{{$node["Node Name"].json.fieldName}}
{{$node["HTTP Request"].json.data}}
{{$node["Webhook"].json.body.email}}
```

**重要**：
- 节点名称**必须**用引号包裹
- 节点名称**区分大小写**
- 必须与 workflow 中的节点名称完全匹配

### $now - 当前时间戳

访问当前日期/时间：

```javascript
{{$now}}
{{$now.toFormat('yyyy-MM-dd')}}
{{$now.toFormat('HH:mm:ss')}}
{{$now.plus({days: 7})}}
```

### $env - 环境变量

访问环境变量：

```javascript
{{$env.API_KEY}}
{{$env.DATABASE_URL}}
```

---

## 🚨 关键：Webhook 数据结构

**最常见错误**：Webhook 数据**不在**根节点！

### Webhook 节点输出结构

```javascript
{
  "headers": {...},
  "params": {...},
  "query": {...},
  "body": {           // ⚠️ 用户数据在这里！
    "name": "John",
    "email": "john@example.com",
    "message": "Hello"
  }
}
```

### 正确的 Webhook 数据访问

```javascript
❌ WRONG: {{$json.name}}
❌ WRONG: {{$json.email}}

✅ CORRECT: {{$json.body.name}}
✅ CORRECT: {{$json.body.email}}
✅ CORRECT: {{$json.body.message}}
```

**原因**：Webhook 节点将传入数据封装在 `.body` 属性下，以保留 headers、params 和 query 参数。

---

## 常用模式

### 访问嵌套字段

```javascript
// Simple nesting
{{$json.user.email}}

// Array access
{{$json.data[0].name}}
{{$json.items[0].id}}

// Bracket notation for spaces
{{$json['field name']}}
{{$json['user data']['first name']}}
```

### 引用其他节点

```javascript
// Node without spaces
{{$node["Set"].json.value}}

// Node with spaces (common!)
{{$node["HTTP Request"].json.data}}
{{$node["Respond to Webhook"].json.message}}

// Webhook node
{{$node["Webhook"].json.body.email}}
```

### 组合变量

```javascript
// Concatenation (automatic)
Hello {{$json.body.name}}!

// In URLs
https://api.example.com/users/{{$json.body.user_id}}

// In object properties
{
  "name": "={{$json.body.name}}",
  "email": "={{$json.body.email}}"
}
```

---

## 不应使用 Expression 的场景

### ❌ Code 节点

Code 节点使用**直接 JavaScript 访问**，而非 expression！

```javascript
// ❌ WRONG in Code node
const email = '={{$json.email}}';
const name = '{{$json.body.name}}';

// ✅ CORRECT in Code node
const email = $json.email;
const name = $json.body.name;

// Or using Code node API
const email = $input.item.json.email;
const allItems = $input.all();
```

### ❌ Webhook 路径

```javascript
// ❌ WRONG
path: "{{$json.user_id}}/webhook"

// ✅ CORRECT
path: "user-webhook"  // Static paths only
```

### ❌ 凭证字段

```javascript
// ❌ WRONG
apiKey: "={{$env.API_KEY}}"

// ✅ CORRECT
Use n8n credential system, not expressions
```

---

## 验证规则

### 1. 始终使用 {{}}

Expression **必须**用双花括号包裹。

```javascript
❌ $json.field
✅ {{$json.field}}
```

### 2. 含空格的名称使用引号

字段名或节点名包含空格时，需要使用**方括号表示法**：

```javascript
❌ {{$json.field name}}
✅ {{$json['field name']}}

❌ {{$node.HTTP Request.json}}
✅ {{$node["HTTP Request"].json}}
```

### 3. 匹配精确节点名称

节点引用**区分大小写**：

```javascript
❌ {{$node["http request"].json}}  // lowercase
❌ {{$node["Http Request"].json}}  // wrong case
✅ {{$node["HTTP Request"].json}}  // exact match
```

### 4. 不要嵌套 {{}}

不要双重包裹 expression：

```javascript
❌ {{{$json.field}}}
✅ {{$json.field}}
```

---

## 常见错误

完整的错误目录及修复方法，请参阅 COMMON_MISTAKES.md

### 快速修复

| 错误 | 修复 |
|---------|-----|
| `$json.field` | `{{$json.field}}` |
| `{{$json.field name}}` | `{{$json['field name']}}` |
| `{{$node.HTTP Request}}` | `{{$node["HTTP Request"]}}` |
| `{{{$json.field}}}` | `{{$json.field}}` |
| `{{$json.name}}` (webhook) | `{{$json.body.name}}` |
| `'={{$json.email}}'` (Code node) | `$json.email` |

---

## 实际示例

真实的 workflow 示例，请参阅 EXAMPLES.md

### 示例 1：Webhook 到 Slack

**Webhook 接收**：
```json
{
  "body": {
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello!"
  }
}
```

**在 Slack 节点文本字段中**：
```
New form submission!

Name: {{$json.body.name}}
Email: {{$json.body.email}}
Message: {{$json.body.message}}
```

### 示例 2：HTTP Request 到 Email

**HTTP Request 返回**：
```json
{
  "data": {
    "items": [
      {"name": "Product 1", "price": 29.99}
    ]
  }
}
```

**在 Email 节点中**（引用 HTTP Request）：
```
Product: {{$node["HTTP Request"].json.data.items[0].name}}
Price: ${{$node["HTTP Request"].json.data.items[0].price}}
```

### 示例 3：格式化时间戳

```javascript
// Current date
{{$now.toFormat('yyyy-MM-dd')}}
// Result: 2025-10-20

// Time
{{$now.toFormat('HH:mm:ss')}}
// Result: 14:30:45

// Full datetime
{{$now.toFormat('yyyy-MM-dd HH:mm')}}
// Result: 2025-10-20 14:30
```

---

## 数据类型处理

### 数组

```javascript
// First item
{{$json.users[0].email}}

// Array length
{{$json.users.length}}

// Last item
{{$json.users[$json.users.length - 1].name}}
```

### 对象

```javascript
// Dot notation (no spaces)
{{$json.user.email}}

// Bracket notation (with spaces or dynamic)
{{$json['user data'].email}}
```

### 字符串

```javascript
// Concatenation (automatic)
Hello {{$json.name}}!

// String methods
{{$json.email.toLowerCase()}}
{{$json.name.toUpperCase()}}
```

### 数字

```javascript
// Direct use
{{$json.price}}

// Math operations
{{$json.price * 1.1}}  // Add 10%
{{$json.quantity + 5}}
```

---

## 高级模式

### 条件内容

```javascript
// Ternary operator
{{$json.status === 'active' ? 'Active User' : 'Inactive User'}}

// Default values
{{$json.email || 'no-email@example.com'}}
```

### 日期操作

```javascript
// Add days
{{$now.plus({days: 7}).toFormat('yyyy-MM-dd')}}

// Subtract hours
{{$now.minus({hours: 24}).toISO()}}

// Set specific date
{{DateTime.fromISO('2025-12-25').toFormat('MMMM dd, yyyy')}}
```

### 字符串操作

```javascript
// Substring
{{$json.email.substring(0, 5)}}

// Replace
{{$json.message.replace('old', 'new')}}

// Split and join
{{$json.tags.split(',').join(', ')}}
```

---

## 调试 Expression

### 在 Expression 编辑器中测试

1. 点击包含 expression 的字段
2. 打开 expression 编辑器（点击 "fx" 图标）
3. 查看结果的实时预览
4. 检查以红色高亮显示的错误

### 常见错误信息

**"Cannot read property 'X' of undefined"**
→ 父对象不存在
→ 检查数据路径

**"X is not a function"**
→ 尝试在非函数上调用方法
→ 检查变量类型

**Expression 显示为纯文本**
→ 缺少 {{ }}
→ 添加花括号

---

## Expression 辅助方法

### 可用方法

**String**:
- `.toLowerCase()`, `.toUpperCase()`
- `.trim()`, `.replace()`, `.substring()`
- `.split()`, `.includes()`

**Array**:
- `.length`, `.map()`, `.filter()`
- `.find()`, `.join()`, `.slice()`

**DateTime** (Luxon):
- `.toFormat()`, `.toISO()`, `.toLocal()`
- `.plus()`, `.minus()`, `.set()`

**Number**:
- `.toFixed()`, `.toString()`
- Math operations: `+`, `-`, `*`, `/`, `%`

---

## 最佳实践

### ✅ 应该做

- 动态内容始终使用 {{ }}
- 含空格的字段名使用方括号表示法
- 通过 `.body` 引用 webhook 数据
- 使用 $node 获取其他节点的数据
- 在 expression 编辑器中测试 expression

### ❌ 不应该做

- 不要在 Code 节点中使用 expression
- 不要忘记给含空格的节点名加引号
- 不要用额外的 {{ }} 双重包裹
- 不要假设 webhook 数据在根节点（它在 .body 下！）
- 不要在 webhook 路径或凭证中使用 expression

---

## 相关技能

- **n8n MCP Tools Expert**：学习如何使用 MCP 工具验证 expression
- **n8n Workflow Patterns**：在真实 workflow 示例中查看 expression
- **n8n Node Configuration**：了解何时需要使用 expression

---

## 总结

**核心规则**：
1. 用 {{ }} 包裹 expression
2. Webhook 数据在 `.body` 下
3. Code 节点中不使用 {{ }}
4. 含空格的节点名用引号包裹
5. 节点名称区分大小写

**最常见错误**：
- 缺少 {{ }} → 添加花括号
- webhook 中使用 `{{$json.name}}` → 改用 `{{$json.body.name}}`
- Code 中使用 `{{$json.email}}` → 改用 `$json.email`
- `{{$node.HTTP Request}}` → 改用 `{{$node["HTTP Request"]}}`

更多信息，请参阅：
- COMMON_MISTAKES.md - 完整错误目录
- EXAMPLES.md - 真实 workflow 示例

---

**需要帮助？** 请参考 n8n expression 文档或使用 n8n-mcp 验证工具检查你的 expression。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
