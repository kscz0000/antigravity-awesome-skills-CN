---
name: n8n-validation-expert
description: "解读和修复 n8n 验证错误的专家指南。当用户要求解读或修复 n8n 验证错误时使用。"
risk: unknown
source: community
---

# n8n 验证专家

解读和修复 n8n 验证错误的专家指南。

## 何时使用
- 你需要解读或修复 n8n 工作流中的验证错误。
- 任务涉及 `missing_required`、`invalid_value`、表达式失败或迭代式验证-修复循环。
- 你需要针对工作流验证输出的具体修复指导。

---

## 验证理念

**尽早验证，频繁验证**

验证通常是迭代式的：
- 预期会有验证反馈循环
- 通常需要 2-3 轮验证 → 修复循环
- 平均：23 秒思考错误，58 秒修复错误

**关键洞察**：验证是一个迭代过程，不是一次性的！

---

## 错误严重性级别

### 1. 错误（必须修复）
**阻止工作流执行** - 必须在激活前解决

**类型**：
- `missing_required` - 未提供必填字段
- `invalid_value` - 值不匹配允许的选项
- `type_mismatch` - 错误的数据类型（字符串而非数字）
- `invalid_reference` - 引用的节点不存在
- `invalid_expression` - 表达式语法错误

**示例**：
```json
{
  "type": "missing_required",
  "property": "channel",
  "message": "Channel name is required",
  "fix": "Provide a channel name (lowercase, no spaces, 1-80 characters)"
}
```

### 2. 警告（应该修复）
**不阻止执行** - 工作流可以激活但可能有问题

**类型**：
- `best_practice` - 推荐但非必需
- `deprecated` - 使用旧 API/功能
- `performance` - 潜在的性能问题

**示例**：
```json
{
  "type": "best_practice",
  "property": "errorHandling",
  "message": "Slack API can have rate limits",
  "suggestion": "Add onError: 'continueRegularOutput' with retryOnFail"
}
```

### 3. 建议（可选）
**锦上添花** - 可以增强工作流的改进

**类型**：
- `optimization` - 可以更高效
- `alternative` - 实现相同结果的更好方式

---

## 验证循环

### 来自遥测的模式
**7,841 次出现**此模式：

```
1. Configure node
   ↓
2. validate_node (23 seconds thinking about errors)
   ↓
3. Read error messages carefully
   ↓
4. Fix errors
   ↓
5. validate_node again (58 seconds fixing)
   ↓
6. Repeat until valid (usually 2-3 iterations)
```

### 示例
```javascript
// Iteration 1
let config = {
  resource: "channel",
  operation: "create"
};

const result1 = validate_node({
  nodeType: "nodes-base.slack",
  config,
  profile: "runtime"
});
// → Error: Missing "name"

// ⏱️  23 seconds thinking...

// Iteration 2
config.name = "general";

const result2 = validate_node({
  nodeType: "nodes-base.slack",
  config,
  profile: "runtime"
});
// → Error: Missing "text"

// ⏱️  58 seconds fixing...

// Iteration 3
config.text = "Hello!";

const result3 = validate_node({
  nodeType: "nodes-base.slack",
  config,
  profile: "runtime"
});
// → Valid! ✅
```

**这是正常的！** 不要因为多次迭代而气馁。

---

## 验证配置文件

根据你的阶段选择合适的配置文件：

### minimal
**使用场景**：编辑时快速检查

**验证内容**：
- 仅必填字段
- 基本结构

**优点**：最快、最宽松
**缺点**：可能遗漏问题

### runtime（推荐）
**使用场景**：部署前验证

**验证内容**：
- 必填字段
- 值类型
- 允许的值
- 基本依赖

**优点**：平衡，捕获真实错误
**缺点**：某些边缘情况会遗漏

**这是大多数用例的推荐配置文件**

### ai-friendly
**使用场景**：AI 生成的配置

**验证内容**：
- 与 runtime 相同
- 减少误报
- 对小问题更宽容

**优点**：对 AI 工作流干扰更少
**缺点**：可能允许一些有问题的配置

### strict
**使用场景**：生产部署、关键工作流

**验证内容**：
- 所有内容
- 最佳实践
- 性能问题
- 安全问题

**优点**：最高安全性
**缺点**：警告较多，部分误报

---

## 常见错误类型

### 1. missing_required
**含义**：未提供必填字段

**修复方法**：
1. 使用 `get_node` 查看必填字段
2. 将缺失的字段添加到配置中
3. 提供适当的值

**示例**：
```javascript
// Error
{
  "type": "missing_required",
  "property": "channel",
  "message": "Channel name is required"
}

// Fix
config.channel = "#general";
```

### 2. invalid_value
**含义**：值不匹配允许的选项

**修复方法**：
1. 检查错误消息中的允许值
2. 使用 `get_node` 查看选项
3. 更新为有效值

**示例**：
```javascript
// Error
{
  "type": "invalid_value",
  "property": "operation",
  "message": "Operation must be one of: post, update, delete",
  "current": "send"
}

// Fix
config.operation = "post";  // Use valid operation
```

### 3. type_mismatch
**含义**：字段的数据类型错误

**修复方法**：
1. 检查错误消息中的期望类型
2. 将值转换为正确的类型

**示例**：
```javascript
// Error
{
  "type": "type_mismatch",
  "property": "limit",
  "message": "Expected number, got string",
  "current": "100"
}

// Fix
config.limit = 100;  // Number, not string
```

### 4. invalid_expression
**含义**：表达式语法错误

**修复方法**：
1. 使用 n8n Expression Syntax 技能
2. 检查是否缺少 `{{}}` 或有拼写错误
3. 验证节点/字段引用

**示例**：
```javascript
// Error
{
  "type": "invalid_expression",
  "property": "text",
  "message": "Invalid expression: $json.name",
  "current": "$json.name"
}

// Fix
config.text = "={{$json.name}}";  // Add {{}}
```

### 5. invalid_reference
**含义**：引用的节点不存在

**修复方法**：
1. 检查节点名称拼写
2. 验证节点存在于工作流中
3. 更新引用为正确的名称

**示例**：
```javascript
// Error
{
  "type": "invalid_reference",
  "property": "expression",
  "message": "Node 'HTTP Requets' does not exist",
  "current": "={{$node['HTTP Requets'].json.data}}"
}

// Fix - correct typo
config.expression = "={{$node['HTTP Request'].json.data}}";
```

---

## 自动清理系统

### 功能说明
**在任何工作流更新时自动修复常见的操作符结构问题**

**运行时机**：
- `n8n_create_workflow`
- `n8n_update_partial_workflow`
- 任何工作流保存操作

### 修复内容

#### 1. 二元运算符（两个值）
**运算符**：equals, notEquals, contains, notContains, greaterThan, lessThan, startsWith, endsWith

**修复**：移除 `singleValue` 属性（二元运算符比较两个值）

**修复前**：
```javascript
{
  "type": "boolean",
  "operation": "equals",
  "singleValue": true  // ❌ Wrong!
}
```

**修复后**（自动）：
```javascript
{
  "type": "boolean",
  "operation": "equals"
  // singleValue removed ✅
}
```

#### 2. 一元运算符（一个值）
**运算符**：isEmpty, isNotEmpty, true, false

**修复**：添加 `singleValue: true`（一元运算符检查单个值）

**修复前**：
```javascript
{
  "type": "boolean",
  "operation": "isEmpty"
  // Missing singleValue ❌
}
```

**修复后**（自动）：
```javascript
{
  "type": "boolean",
  "operation": "isEmpty",
  "singleValue": true  // ✅ Added
}
```

#### 3. IF/Switch 元数据
**修复**：为 IF v2.2+ 和 Switch v3.2+ 添加完整的 `conditions.options` 元数据

### 无法修复的内容

#### 1. 断开的连接
引用不存在的节点

**解决方案**：在 `n8n_update_partial_workflow` 中使用 `cleanStaleConnections` 操作

#### 2. 分支数量不匹配
3 个 Switch 规则但只有 2 个输出连接

**解决方案**：添加缺失的连接或移除多余的规则

#### 3. 矛盾的损坏状态
API 返回损坏数据但拒绝更新

**解决方案**：可能需要手动数据库干预

---

## 误报

### 什么是误报？
在技术上"错误"但在你的用例中可以接受的验证警告

### 常见误报

#### 1. "缺少错误处理"
**警告**：未配置错误处理

**何时可以接受**：
- 失败明显的简单工作流
- 测试/开发工作流
- 非关键通知

**何时修复**：处理重要数据的生产工作流

#### 2. "无重试逻辑"
**警告**：节点在失败时不重试

**何时可以接受**：
- 自带重试逻辑的 API
- 幂等操作
- 手动触发工作流

**何时修复**：不稳定的外部服务、生产自动化

#### 3. "缺少速率限制"
**警告**：API 调用没有速率限制

**何时可以接受**：
- 无限制的内部 API
- 低流量工作流
- 服务端有限速的 API

**何时修复**：公共 API、高流量工作流

#### 4. "无界查询"
**警告**：没有 LIMIT 的 SELECT

**何时可以接受**：
- 小型已知数据集
- 聚合查询
- 开发/测试

**何时修复**：大表的生产查询

### 减少误报

**使用 `ai-friendly` 配置文件**：
```javascript
validate_node({
  nodeType: "nodes-base.slack",
  config: {...},
  profile: "ai-friendly"  // Fewer false positives
})
```

---

## 验证结果结构

### 完整响应
```javascript
{
  "valid": false,
  "errors": [
    {
      "type": "missing_required",
      "property": "channel",
      "message": "Channel name is required",
      "fix": "Provide a channel name (lowercase, no spaces)"
    }
  ],
  "warnings": [
    {
      "type": "best_practice",
      "property": "errorHandling",
      "message": "Slack API can have rate limits",
      "suggestion": "Add onError: 'continueRegularOutput'"
    }
  ],
  "suggestions": [
    {
      "type": "optimization",
      "message": "Consider using batch operations for multiple messages"
    }
  ],
  "summary": {
    "hasErrors": true,
    "errorCount": 1,
    "warningCount": 1,
    "suggestionCount": 1
  }
}
```

### 如何解读结果

#### 1. 检查 `valid` 字段
```javascript
if (result.valid) {
  // ✅ Configuration is valid
} else {
  // ❌ Has errors - must fix before deployment
}
```

#### 2. 先修复错误
```javascript
result.errors.forEach(error => {
  console.log(`Error in ${error.property}: ${error.message}`);
  console.log(`Fix: ${error.fix}`);
});
```

#### 3. 审查警告
```javascript
result.warnings.forEach(warning => {
  console.log(`Warning: ${warning.message}`);
  console.log(`Suggestion: ${warning.suggestion}`);
  // Decide if you need to address this
});
```

#### 4. 考虑建议
```javascript
// Optional improvements
// Not required but may enhance workflow
```

---

## 工作流验证

### validate_workflow（结构）
**验证整个工作流**，而不仅仅是单个节点

**检查内容**：
1. **节点配置** - 每个节点有效
2. **连接** - 无断开的引用
3. **表达式** - 语法和引用有效
4. **流程** - 逻辑工作流结构

**示例**：
```javascript
validate_workflow({
  workflow: {
    nodes: [...],
    connections: {...}
  },
  options: {
    validateNodes: true,
    validateConnections: true,
    validateExpressions: true,
    profile: "runtime"
  }
})
```

### 常见工作流错误

#### 1. 断开的连接
```json
{
  "error": "Connection from 'Transform' to 'NonExistent' - target node not found"
}
```

**修复**：移除过时连接或创建缺失的节点

#### 2. 循环依赖
```json
{
  "error": "Circular dependency detected: Node A → Node B → Node A"
}
```

**修复**：重构工作流以移除循环

#### 3. 多个起始节点
```json
{
  "warning": "Multiple trigger nodes found - only one will execute"
}
```

**修复**：移除多余的触发器或拆分为单独的工作流

#### 4. 断开的节点
```json
{
  "warning": "Node 'Transform' is not connected to workflow flow"
}
```

**修复**：连接节点或移除未使用的节点

---

## 恢复策略

### 策略 1：重新开始
**适用场景**：配置严重损坏

**步骤**：
1. 从 `get_node` 记录必填字段
2. 创建最小有效配置
3. 逐步添加功能
4. 每次添加后验证

### 策略 2：二分搜索
**适用场景**：工作流验证通过但执行不正确

**步骤**：
1. 移除一半节点
2. 验证并测试
3. 如果正常：问题在移除的节点中
4. 如果失败：问题在剩余的节点中
5. 重复直到问题隔离

### 策略 3：清理过时连接
**适用场景**："节点未找到"错误

**步骤**：
```javascript
n8n_update_partial_workflow({
  id: "workflow-id",
  operations: [{
    type: "cleanStaleConnections"
  }]
})
```

### 策略 4：使用自动修复
**适用场景**：操作符结构错误

**步骤**：
```javascript
n8n_autofix_workflow({
  id: "workflow-id",
  applyFixes: false  // Preview first
})

// Review fixes, then apply
n8n_autofix_workflow({
  id: "workflow-id",
  applyFixes: true
})
```

---

## 最佳实践

### ✅ 应该做的

- 每次重要更改后验证
- 完整阅读错误消息
- 迭代修复错误（一次一个）
- 部署前使用 `runtime` 配置文件
- 假设成功前检查 `valid` 字段
- 对操作符问题信任自动清理
- 不清楚需求时使用 `get_node`
- 记录你接受的误报

### ❌ 不应该做的

- 激活前跳过验证
- 试图一次修复所有错误
- 忽略错误消息
- 开发时使用 `strict` 配置文件（干扰太多）
- 假设验证通过（始终检查结果）
- 手动修复自动清理问题
- 部署有未解决错误的工作流
- 忽略所有警告（有些很重要！）

---

## 详细指南

获取完整的错误目录和误报示例：

- **ERROR_CATALOG.md** - 完整的错误类型列表及示例
- **FALSE_POSITIVES.md** - 警告何时可以接受

---

## 总结

**关键要点**：
1. **验证是迭代的**（平均 2-3 轮，23 秒 + 58 秒）
2. **错误必须修复**，警告可选
3. **自动清理**自动修复操作符结构
4. **使用 runtime 配置文件**进行平衡验证
5. **误报存在** - 学会识别它们
6. **阅读错误消息** - 包含修复指导

**验证流程**：
1. 验证 → 阅读错误 → 修复 → 再次验证
2. 重复直到有效（通常 2-3 轮）
3. 审查警告并决定是否可接受
4. 自信地部署

**相关技能**：
- n8n MCP Tools Expert - 正确使用验证工具
- n8n Expression Syntax - 修复表达式错误
- n8n Node Configuration - 理解必填字段

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
