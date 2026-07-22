---
name: n8n-code-javascript
description: 在 n8n Code 节点中编写 JavaScript 代码。当在 n8n 中编写 JavaScript、使用 $input/$json/$node 语法、用 $helpers 发起 HTTP 请求、使用 DateTime 处理日期、排查 Code 节点错误、或选择 Code 节点模式时使用。触发词：n8n代码节点、Code节点、JavaScript代码、n8n脚本、$input语法、$helpers、DateTime Luxon、Code节点错误、代码节点模式
risk: unknown
source: community
---

# JavaScript Code 节点

在 n8n Code 节点中编写 JavaScript 代码的专家指南。

---

## 快速入门

```javascript
// Basic template for Code nodes
const items = $input.all();

// Process data
const processed = items.map(item => ({
  json: {
    ...item.json,
    processed: true,
    timestamp: new Date().toISOString()
  }
}));

return processed;
```

### 核心规则

1. **选择"为所有项目运行一次"模式**（推荐大多数场景使用）
2. **访问数据**：`$input.all()`、`$input.first()` 或 `$input.item`
3. **关键**：必须返回 `[{json: {...}}]` 格式
4. **关键**：Webhook 数据在 `$json.body` 下（不是直接在 `$json` 下）
5. **可用内置函数**：$helpers.httpRequest()、DateTime (Luxon)、$jmespath()

---

## 模式选择指南

Code 节点提供两种执行模式。根据你的使用场景选择：

### 为所有项目运行一次（推荐 - 默认）

**适用场景：** 95% 的用例

- **工作原理**：无论输入数量多少，代码只执行**一次**
- **数据访问**：`$input.all()` 或 `items` 数组
- **最适合**：聚合、过滤、批处理、转换、处理全部数据的 API 调用
- **性能**：多条数据时更快（单次执行）

```javascript
// Example: Calculate total from all items
const allItems = $input.all();
const total = allItems.reduce((sum, item) => sum + (item.json.amount || 0), 0);

return [{
  json: {
    total,
    count: allItems.length,
    average: total / allItems.length
  }
}];
```

**何时使用：**
- ✅ 需要跨数据集比较项目
- ✅ 计算总计、平均值或统计信息
- ✅ 排序或排名项目
- ✅ 去重
- ✅ 构建聚合报告
- ✅ 合并多个项目的数据

### 为每个项目运行一次

**适用场景：** 仅限特殊情况

- **工作原理**：代码为每个输入项目**分别**执行
- **数据访问**：`$input.item` 或 `$item`
- **最适合**：项目特定逻辑、独立操作、逐项验证
- **性能**：大数据集时较慢（多次执行）

```javascript
// Example: Add processing timestamp to each item
const item = $input.item;

return [{
  json: {
    ...item.json,
    processed: true,
    processedAt: new Date().toISOString()
  }
}];
```

**何时使用：**
- ✅ 每个项目需要独立的 API 调用
- ✅ 逐项验证且错误处理不同
- ✅ 基于项目属性的特定转换
- ✅ 出于业务逻辑需要单独处理项目

**决策捷径：**
- **需要查看多个项目？** → 使用"所有项目"模式
- **每个项目完全独立？** → 使用"每个项目"模式
- **不确定？** → 使用"所有项目"模式（你总是可以在内部循环）

---

## 数据访问模式

### 模式 1：$input.all() - 最常用

**使用时机**：处理数组、批量操作、聚合

```javascript
// Get all items from previous node
const allItems = $input.all();

// Filter, map, reduce as needed
const valid = allItems.filter(item => item.json.status === 'active');
const mapped = valid.map(item => ({
  json: {
    id: item.json.id,
    name: item.json.name
  }
}));

return mapped;
```

### 模式 2：$input.first() - 很常用

**使用时机**：处理单个对象、API 响应、先进先出

```javascript
// Get first item only
const firstItem = $input.first();
const data = firstItem.json;

return [{
  json: {
    result: processData(data),
    processedAt: new Date().toISOString()
  }
}];
```

### 模式 3：$input.item - 仅限每个项目模式

**使用时机**：在"为每个项目运行一次"模式下

```javascript
// Current item in loop (Each Item mode only)
const currentItem = $input.item;

return [{
  json: {
    ...currentItem.json,
    itemProcessed: true
  }
}];
```

### 模式 4：$node - 引用其他节点

**使用时机**：需要工作流中特定节点的数据

```javascript
// Get output from specific node
const webhookData = $node["Webhook"].json;
const httpData = $node["HTTP Request"].json;

return [{
  json: {
    combined: {
      webhook: webhookData,
      api: httpData
    }
  }
}];
```

**参见**：DATA_ACCESS.md 获取完整指南

---

## 关键：Webhook 数据结构

**最常见错误**：Webhook 数据嵌套在 `.body` 下

```javascript
// ❌ WRONG - Will return undefined
const name = $json.name;
const email = $json.email;

// ✅ CORRECT - Webhook data is under .body
const name = $json.body.name;
const email = $json.body.email;

// Or with $input
const webhookData = $input.first().json.body;
const name = webhookData.name;
```

**原因**：Webhook 节点将所有请求数据包裹在 `body` 属性下，包括 POST 数据、查询参数和 JSON 载荷。

**参见**：DATA_ACCESS.md 获取完整的 webhook 结构详情

---

## 返回格式要求

**关键规则**：始终返回带有 `json` 属性的对象数组

### 正确的返回格式

```javascript
// ✅ Single result
return [{
  json: {
    field1: value1,
    field2: value2
  }
}];

// ✅ Multiple results
return [
  {json: {id: 1, data: 'first'}},
  {json: {id: 2, data: 'second'}}
];

// ✅ Transformed array
const transformed = $input.all()
  .filter(item => item.json.valid)
  .map(item => ({
    json: {
      id: item.json.id,
      processed: true
    }
  }));
return transformed;

// ✅ Empty result (when no data to return)
return [];

// ✅ Conditional return
if (shouldProcess) {
  return [{json: processedData}];
} else {
  return [];
}
```

### 错误的返回格式

```javascript
// ❌ WRONG: Object without array wrapper
return {
  json: {field: value}
};

// ❌ WRONG: Array without json wrapper
return [{field: value}];

// ❌ WRONG: Plain string
return "processed";

// ❌ WRONG: Raw data without mapping
return $input.all();  // Missing .map()

// ❌ WRONG: Incomplete structure
return [{data: value}];  // Should be {json: value}
```

**为什么重要**：后续节点期望数组格式。格式不正确会导致工作流执行失败。

**参见**：ERROR_PATTERNS.md #3 获取详细的错误解决方案

---

## 常用模式概览

基于生产工作流，以下是最实用的模式：

### 1. 多源数据聚合
合并来自多个 API、Webhook 或节点的数据

```javascript
const allItems = $input.all();
const results = [];

for (const item of allItems) {
  const sourceName = item.json.name || 'Unknown';
  // Parse source-specific structure
  if (sourceName === 'API1' && item.json.data) {
    results.push({
      json: {
        title: item.json.data.title,
        source: 'API1'
      }
    });
  }
}

return results;
```

### 2. 正则过滤
从文本中提取模式、提及或关键词

```javascript
const pattern = /\b([A-Z]{2,5})\b/g;
const matches = {};

for (const item of $input.all()) {
  const text = item.json.text;
  const found = text.match(pattern);

  if (found) {
    found.forEach(match => {
      matches[match] = (matches[match] || 0) + 1;
    });
  }
}

return [{json: {matches}}];
```

### 3. 数据转换与丰富
映射字段、规范化格式、添加计算字段

```javascript
const items = $input.all();

return items.map(item => {
  const data = item.json;
  const nameParts = data.name.split(' ');

  return {
    json: {
      first_name: nameParts[0],
      last_name: nameParts.slice(1).join(' '),
      email: data.email,
      created_at: new Date().toISOString()
    }
  };
});
```

### 4. Top N 过滤与排名
排序并限制结果

```javascript
const items = $input.all();

const topItems = items
  .sort((a, b) => (b.json.score || 0) - (a.json.score || 0))
  .slice(0, 10);

return topItems.map(item => ({json: item.json}));
```

### 5. 聚合与报告
求和、计数、分组数据

```javascript
const items = $input.all();
const total = items.reduce((sum, item) => sum + (item.json.amount || 0), 0);

return [{
  json: {
    total,
    count: items.length,
    average: total / items.length,
    timestamp: new Date().toISOString()
  }
}];
```

**参见**：COMMON_PATTERNS.md 获取 10 个详细的生产模式

---

## 错误预防 - 前 5 大错误

### #1：空代码或缺少 return（最常见）

```javascript
// ❌ WRONG: No return statement
const items = $input.all();
// ... processing code ...
// Forgot to return!

// ✅ CORRECT: Always return data
const items = $input.all();
// ... processing ...
return items.map(item => ({json: item.json}));
```

### #2：表达式语法混淆

```javascript
// ❌ WRONG: Using n8n expression syntax in code
const value = "{{ $json.field }}";

// ✅ CORRECT: Use JavaScript template literals
const value = `${$json.field}`;

// ✅ CORRECT: Direct access
const value = $input.first().json.field;
```

### #3：返回包装器不正确

```javascript
// ❌ WRONG: Returning object instead of array
return {json: {result: 'success'}};

// ✅ CORRECT: Array wrapper required
return [{json: {result: 'success'}}];
```

### #4：缺少空值检查

```javascript
// ❌ WRONG: Crashes if field doesn't exist
const value = item.json.user.email;

// ✅ CORRECT: Safe access with optional chaining
const value = item.json?.user?.email || 'no-email@example.com';

// ✅ CORRECT: Guard clause
if (!item.json.user) {
  return [];
}
const value = item.json.user.email;
```

### #5：Webhook Body 嵌套

```javascript
// ❌ WRONG: Direct access to webhook data
const email = $json.email;

// ✅ CORRECT: Webhook data under .body
const email = $json.body.email;
```

**参见**：ERROR_PATTERNS.md 获取完整的错误指南

---

## 内置函数与辅助工具

### $helpers.httpRequest()

在代码中发起 HTTP 请求：

```javascript
const response = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/data',
  headers: {
    'Authorization': 'Bearer token',
    'Content-Type': 'application/json'
  }
});

return [{json: {data: response}}];
```

### DateTime (Luxon)

日期和时间操作：

```javascript
// Current time
const now = DateTime.now();

// Format dates
const formatted = now.toFormat('yyyy-MM-dd');
const iso = now.toISO();

// Date arithmetic
const tomorrow = now.plus({days: 1});
const lastWeek = now.minus({weeks: 1});

return [{
  json: {
    today: formatted,
    tomorrow: tomorrow.toFormat('yyyy-MM-dd')
  }
}];
```

### $jmespath()

查询 JSON 结构：

```javascript
const data = $input.first().json;

// Filter array
const adults = $jmespath(data, 'users[?age >= `18`]');

// Extract fields
const names = $jmespath(data, 'users[*].name');

return [{json: {adults, names}}];
```

**参见**：BUILTIN_FUNCTIONS.md 获取完整参考

---

## 最佳实践

### 1. 始终验证输入数据

```javascript
const items = $input.all();

// Check if data exists
if (!items || items.length === 0) {
  return [];
}

// Validate structure
if (!items[0].json) {
  return [{json: {error: 'Invalid input format'}}];
}

// Continue processing...
```

### 2. 使用 Try-Catch 进行错误处理

```javascript
try {
  const response = await $helpers.httpRequest({
    url: 'https://api.example.com/data'
  });

  return [{json: {success: true, data: response}}];
} catch (error) {
  return [{
    json: {
      success: false,
      error: error.message
    }
  }];
}
```

### 3. 优先使用数组方法而非循环

```javascript
// ✅ GOOD: Functional approach
const processed = $input.all()
  .filter(item => item.json.valid)
  .map(item => ({json: {id: item.json.id}}));

// ❌ SLOWER: Manual loop
const processed = [];
for (const item of $input.all()) {
  if (item.json.valid) {
    processed.push({json: {id: item.json.id}});
  }
}
```

### 4. 先过滤，后处理

```javascript
// ✅ GOOD: Filter first to reduce processing
const processed = $input.all()
  .filter(item => item.json.status === 'active')  // Reduce dataset first
  .map(item => expensiveTransformation(item));  // Then transform

// ❌ WASTEFUL: Transform everything, then filter
const processed = $input.all()
  .map(item => expensiveTransformation(item))  // Wastes CPU
  .filter(item => item.json.status === 'active');
```

### 5. 使用描述性变量名

```javascript
// ✅ GOOD: Clear intent
const activeUsers = $input.all().filter(item => item.json.active);
const totalRevenue = activeUsers.reduce((sum, user) => sum + user.json.revenue, 0);

// ❌ BAD: Unclear purpose
const a = $input.all().filter(item => item.json.active);
const t = a.reduce((s, u) => s + u.json.revenue, 0);
```

### 6. 使用 console.log() 调试

```javascript
// Debug statements appear in browser console
const items = $input.all();
console.log(`Processing ${items.length} items`);

for (const item of items) {
  console.log('Item data:', item.json);
  // Process...
}

return result;
```

---

## 何时使用 Code 节点

在以下情况使用 Code 节点：
- ✅ 需要多步骤的复杂转换
- ✅ 自定义计算或业务逻辑
- ✅ 递归操作
- ✅ 解析复杂结构的 API 响应
- ✅ 多步骤条件判断
- ✅ 跨项目数据聚合

在以下情况考虑使用其他节点：
- ❌ 简单字段映射 → 使用 **Set** 节点
- ❌ 基本过滤 → 使用 **Filter** 节点
- ❌ 简单条件判断 → 使用 **IF** 或 **Switch** 节点
- ❌ 仅需 HTTP 请求 → 使用 **HTTP Request** 节点

**Code 节点的优势**：处理需要串联多个简单节点才能实现的复杂逻辑

---

## 与其他技能的集成

### 配合使用：

**n8n Expression Syntax**：
- 表达式在其他节点中使用 `{{ }}` 语法
- Code 节点直接使用 JavaScript（无需 `{{ }}`）
- 何时使用表达式 vs 代码

**n8n MCP Tools Expert**：
- 如何查找 Code 节点：`search_nodes({query: "code"})`
- 获取配置帮助：`get_node_essentials("nodes-base.code")`
- 验证代码：`validate_node_operation()`

**n8n Node Configuration**：
- 模式选择（所有项目 vs 每个项目）
- 语言选择（JavaScript vs Python）
- 理解属性依赖关系

**n8n Workflow Patterns**：
- 转换步骤中的 Code 节点
- Webhook → Code → API 模式
- 工作流中的错误处理

**n8n Validation Expert**：
- 验证 Code 节点配置
- 处理验证错误
- 自动修复常见问题

---

## 快速参考清单

部署 Code 节点前，请验证：

- [ ] **代码不为空** - 必须有有意义的逻辑
- [ ] **存在 return 语句** - 必须返回对象数组
- [ ] **返回格式正确** - 每个项目：`{json: {...}}`
- [ ] **数据访问正确** - 使用 `$input.all()`、`$input.first()` 或 `$input.item`
- [ ] **不使用 n8n 表达式** - 使用 JavaScript 模板字符串：`` `${value}` ``
- [ ] **错误处理** - 对 null/undefined 输入使用守卫子句
- [ ] **Webhook 数据** - 如果来自 webhook，通过 `.body` 访问
- [ ] **模式选择** - 大多数情况使用"所有项目"
- [ ] **性能** - 优先使用 map/filter 而非手动循环
- [ ] **输出一致** - 所有代码路径返回相同结构

---

## 附加资源

### 相关文件
- DATA_ACCESS.md - 完整的数据访问模式
- COMMON_PATTERNS.md - 10 个经过生产验证的模式
- ERROR_PATTERNS.md - 前 5 大错误及解决方案
- BUILTIN_FUNCTIONS.md - 完整的内置函数参考

### n8n 文档
- Code Node Guide: https://docs.n8n.io/code/code-node/
- Built-in Methods: https://docs.n8n.io/code-examples/methods-variables-reference/
- Luxon Documentation: https://moment.github.io/luxon/

---

**准备好在 n8n Code 节点中编写 JavaScript 了！** 从简单的转换开始，使用错误模式指南避免常见错误，并参考模式库获取生产就绪的示例。

## 限制
- 仅当任务明确匹配上述描述的范围时才使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
