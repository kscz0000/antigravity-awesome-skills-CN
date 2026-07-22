---
name: n8n-mcp-tools-expert
description: 有效使用 n8n-mcp MCP 工具的专家指南。用于搜索节点、验证配置、访问模板、管理工作流或使用任何 n8n-mcp 工具。提供工具选择指导、参数格式和常见模式。当用户要求"n8n MCP 工具"时使用。
risk: unknown
source: community
---

# n8n MCP 工具专家

使用 n8n-mcp MCP 服务器工具构建工作流的主指南。

## 何时使用
- 您正在使用 `n8n-mcp` 工具集来发现节点、验证配置或管理工作流。
- 任务涉及选择正确的 MCP 工具或理解其预期参数和使用模式。
- 您需要通过 n8n MCP（而非仅通过 n8n UI）创建工作流或编辑工作流的指导。

---

## 工具分类

n8n-mcp 提供的工具按类别组织：

1. **节点发现** → SEARCH_GUIDE.md
2. **配置验证** → VALIDATION_GUIDE.md
3. **工作流管理** → WORKFLOW_GUIDE.md
4. **模板库** - 搜索和部署 2,700+ 个真实工作流
5. **文档与指南** - 工具文档、AI 代理指南、代码节点指南

---

## 快速参考

### 最常用工具（按成功率）

| 工具 | 使用场景 | 速度 |
|------|----------|-------|
| `search_nodes` | 按关键字查找节点 | <20ms |
| `get_node` | 了解节点操作 (detail="standard") | <10ms |
| `validate_node` | 检查配置 (mode="full") | <100ms |
| `n8n_create_workflow` | 创建工作流 | 100-500ms |
| `n8n_update_partial_workflow` | 编辑工作流（最常用！） | 50-200ms |
| `validate_workflow` | 检查完整工作流 | 100-500ms |
| `n8n_deploy_template` | 部署模板到 n8n 实例 | 200-500ms |

---

## 工具选择指南

### 查找正确的节点

**工作流**：
```
1. search_nodes({query: "keyword"})
2. get_node({nodeType: "nodes-base.name"})
3. [Optional] get_node({nodeType: "nodes-base.name", mode: "docs"})
```

**示例**：
```javascript
// 步骤 1：搜索
search_nodes({query: "slack"})
// 返回：nodes-base.slack

// 步骤 2：获取详情
get_node({nodeType: "nodes-base.slack"})
// 返回：operations, properties, examples (standard detail)

// 步骤 3：获取可读文档
get_node({nodeType: "nodes-base.slack", mode: "docs"})
// 返回：markdown documentation
```

**常见模式**：search → get_node（平均 18 秒）

### 验证配置

**工作流**：
```
1. validate_node({nodeType, config: {}, mode: "minimal"}) - 检查必填字段
2. validate_node({nodeType, config, profile: "runtime"}) - 完整验证
3. [重复] 修复错误，再次验证
```

**常见模式**：validate → fix → validate（每周期 23 秒思考，58 秒修复）

### 管理工作流

**工作流**：
```
1. n8n_create_workflow({name, nodes, connections})
2. n8n_validate_workflow({id})
3. n8n_update_partial_workflow({id, operations: [...]})
4. n8n_validate_workflow({id}) 再次验证
5. n8n_update_partial_workflow({id, operations: [{type: "activateWorkflow"}]})
```

**常见模式**：迭代更新（编辑间隔平均 56 秒）

---

## 关键：nodeType 格式

**两种不同格式**用于不同的工具！

### 格式 1：搜索/验证工具
```javascript
// 使用短前缀
"nodes-base.slack"
"nodes-base.httpRequest"
"nodes-base.webhook"
"nodes-langchain.agent"
```

**使用此格式的工具**：
- search_nodes（返回此格式）
- get_node
- validate_node
- validate_workflow

### 格式 2：工作流工具
```javascript
// 使用完整前缀
"n8n-nodes-base.slack"
"n8n-nodes-base.httpRequest"
"n8n-nodes-base.webhook"
"@n8n/n8n-nodes-langchain.agent"
```

**使用此格式的工具**：
- n8n_create_workflow
- n8n_update_partial_workflow

### 转换

```javascript
// search_nodes 返回两种格式
{
  "nodeType": "nodes-base.slack",          // 用于搜索/验证工具
  "workflowNodeType": "n8n-nodes-base.slack"  // 用于工作流工具
}
```

---

## 常见错误

### 错误 1：nodeType 格式错误

**问题**："Node not found" 错误

```javascript
// 错误
get_node({nodeType: "slack"})  // 缺少前缀
get_node({nodeType: "n8n-nodes-base.slack"})  // 前缀错误

// 正确
get_node({nodeType: "nodes-base.slack"})
```

### 错误 2：默认使用 detail="full"

**问题**：响应体过大、响应变慢、浪费 token

```javascript
// 错误 - 返回 3-8K token，谨慎使用
get_node({nodeType: "nodes-base.slack", detail: "full"})

// 正确 - 返回 1-2K token，覆盖 95% 的用例
get_node({nodeType: "nodes-base.slack"})  // detail="standard" 是默认值
get_node({nodeType: "nodes-base.slack", detail: "standard"})
```

**何时使用 detail="full"**：
- 调试复杂配置问题
- 需要完整属性 schema 及所有嵌套选项
- 探索高级功能

**更好的替代方案**：
1. `get_node({detail: "standard"})` - 获取操作列表（默认）
2. `get_node({mode: "docs"})` - 获取可读文档
3. `get_node({mode: "search_properties", propertyQuery: "auth"})` - 获取特定属性

### 错误 3：未使用验证配置文件

**问题**：误报过多或遗漏真实错误

**配置文件**：
- `minimal` - 仅必填字段（快速、宽松）
- `runtime` - 值 + 类型（推荐用于部署前）
- `ai-friendly` - 减少误报（用于 AI 配置）
- `strict` - 最大验证（用于生产环境）

```javascript
// 错误 - 使用默认配置文件
validate_node({nodeType, config})

// 正确 - 显式指定配置文件
validate_node({nodeType, config, profile: "runtime"})
```

### 错误 4：忽略自动清理

**发生情况**：任何工作流更新时，所有节点都会被清理

**自动修复**：
- 二元运算符（equals, contains）→ 移除 singleValue
- 一元运算符（isEmpty, isNotEmpty）→ 添加 singleValue: true
- IF/Switch 节点 → 添加缺失的元数据

**无法修复**：
- 断开的连接
- 分支数量不匹配
- 矛盾的损坏状态

```javascript
// 任何更新后，自动清理会在所有节点上运行
n8n_update_partial_workflow({id, operations: [...]})
// → 自动修复运算符结构
```

### 错误 5：未使用智能参数

**问题**：多输出节点的复杂 sourceIndex 计算

**旧方式**（手动）：
```javascript
// IF 节点连接
{
  type: "addConnection",
  source: "IF",
  target: "Handler",
  sourceIndex: 0  // 哪个输出？难以记忆！
}
```

**新方式**（智能参数）：
```javascript
// IF 节点 - 语义化分支名称
{
  type: "addConnection",
  source: "IF",
  target: "True Handler",
  branch: "true"  // 清晰可读！
}

{
  type: "addConnection",
  source: "IF",
  target: "False Handler",
  branch: "false"
}

// Switch 节点 - 语义化 case 编号
{
  type: "addConnection",
  source: "Switch",
  target: "Handler A",
  case: 0
}
```

### 错误 6：未使用 intent 参数

**问题**：工具响应帮助性降低

```javascript
// 错误 - 响应无上下文
n8n_update_partial_workflow({
  id: "abc",
  operations: [{type: "addNode", node: {...}}]
})

// 正确 - 更好的 AI 响应
n8n_update_partial_workflow({
  id: "abc",
  intent: "Add error handling for API failures",
  operations: [{type: "addNode", node: {...}}]
})
```

---

## 工具使用模式

### 模式 1：节点发现（最常见）

**常见工作流**：步骤间平均 18 秒

```javascript
// 步骤 1：搜索（快速！）
const results = await search_nodes({
  query: "slack",
  mode: "OR",  // 默认：任何词匹配
  limit: 20
});
// → 返回：nodes-base.slack, nodes-base.slackTrigger

// 步骤 2：获取详情（约 18 秒后，用户查看结果）
const details = await get_node({
  nodeType: "nodes-base.slack",
  includeExamples: true  // 获取真实模板配置
});
// → 返回：operations, properties, metadata
```

### 模式 2：验证循环

**典型周期**：23 秒思考，58 秒修复

```javascript
// 步骤 1：验证
const result = await validate_node({
  nodeType: "nodes-base.slack",
  config: {
    resource: "channel",
    operation: "create"
  },
  profile: "runtime"
});

// 步骤 2：检查错误（约 23 秒思考）
if (!result.valid) {
  console.log(result.errors);  // "Missing required field: name"
}

// 步骤 3：修复配置（约 58 秒修复）
config.name = "general";

// 步骤 4：再次验证
await validate_node({...});  // 重复直到无错误
```

### 模式 3：工作流编辑

**最常用的更新工具**：99.0% 成功率，编辑间隔平均 56 秒

```javascript
// 迭代式工作流构建（非一次性！）
// 编辑 1
await n8n_update_partial_workflow({
  id: "workflow-id",
  intent: "Add webhook trigger",
  operations: [{type: "addNode", node: {...}}]
});

// 约 56 秒后...

// 编辑 2
await n8n_update_partial_workflow({
  id: "workflow-id",
  intent: "Connect webhook to processor",
  operations: [{type: "addConnection", source: "...", target: "..."}]
});

// 约 56 秒后...

// 编辑 3（验证）
await n8n_validate_workflow({id: "workflow-id"});

// 准备好了？激活！
await n8n_update_partial_workflow({
  id: "workflow-id",
  intent: "Activate workflow for production",
  operations: [{type: "activateWorkflow"}]
});
```

---

## 详细指南

### 节点发现工具
参见 SEARCH_GUIDE.md 了解：
- search_nodes
- get_node 详情级别（minimal, standard, full）
- get_node 模式（info, docs, search_properties, versions）

### 验证工具
参见 VALIDATION_GUIDE.md 了解：
- 验证配置文件说明
- validate_node 模式（minimal, full）
- validate_workflow 完整结构
- 自动清理系统
- 处理验证错误

### 工作流管理
参见 WORKFLOW_GUIDE.md 了解：
- n8n_create_workflow
- n8n_update_partial_workflow（17 种操作类型！）
- 智能参数（branch, case）
- AI 连接类型（8 种）
- 工作流激活（activateWorkflow/deactivateWorkflow）
- n8n_deploy_template
- n8n_workflow_versions

---

## 模板使用

### 搜索模板

```javascript
// 按关键字搜索（默认模式）
search_templates({
  query: "webhook slack",
  limit: 20
});

// 按节点类型搜索
search_templates({
  searchMode: "by_nodes",
  nodeTypes: ["n8n-nodes-base.httpRequest", "n8n-nodes-base.slack"]
});

// 按任务类型搜索
search_templates({
  searchMode: "by_task",
  task: "webhook_processing"
});

// 按元数据搜索（复杂度、设置时间）
search_templates({
  searchMode: "by_metadata",
  complexity: "simple",
  maxSetupMinutes: 15
});
```

### 获取模板详情

```javascript
get_template({
  templateId: 2947,
  mode: "structure"  // 仅 nodes+connections
});

get_template({
  templateId: 2947,
  mode: "full"  // 完整工作流 JSON
});
```

### 直接部署模板

```javascript
// 部署模板到您的 n8n 实例
n8n_deploy_template({
  templateId: 2947,
  name: "My Weather to Slack",  // 自定义名称（可选）
  autoFix: true,  // 自动修复常见问题（默认）
  autoUpgradeVersions: true  // 升级节点版本（默认）
});
// 返回：workflow ID, required credentials, fixes applied
```

---

## 自助工具

### 获取工具文档

```javascript
// 所有工具概览
tools_documentation()

// 特定工具详情
tools_documentation({
  topic: "search_nodes",
  depth: "full"
})

// 代码节点指南
tools_documentation({topic: "javascript_code_node_guide", depth: "full"})
tools_documentation({topic: "python_code_node_guide", depth: "full"})
```

### AI 代理指南

```javascript
// 综合 AI 工作流指南
ai_agents_guide()
// 返回：Architecture, connections, tools, validation, best practices
```

### 健康检查

```javascript
// 快速健康检查
n8n_health_check()

// 详细诊断
n8n_health_check({mode: "diagnostic"})
// → 返回：status, env vars, tool status, API connectivity
```

---

## 工具可用性

**始终可用**（无需 n8n API）：
- search_nodes, get_node
- validate_node, validate_workflow
- search_templates, get_template
- tools_documentation, ai_agents_guide

**需要 n8n API**（N8N_API_URL + N8N_API_KEY）：
- n8n_create_workflow
- n8n_update_partial_workflow
- n8n_validate_workflow (by ID)
- n8n_list_workflows, n8n_get_workflow
- n8n_test_workflow
- n8n_executions
- n8n_deploy_template
- n8n_workflow_versions
- n8n_autofix_workflow

如果 API 工具不可用，请使用模板和仅验证工作流。

---

## 统一工具参考

### get_node（统一节点信息）

**详情级别** (mode="info", 默认)：
- `minimal` (~200 tokens) - 仅基本元数据
- `standard` (~1-2K tokens) - 核心属性 + 操作（推荐）
- `full` (~3-8K tokens) - 完整 schema（谨慎使用）

**操作模式**：
- `info` (默认) - 带详情级别的节点 schema
- `docs` - 可读的 markdown 文档
- `search_properties` - 查找特定属性（与 propertyQuery 配合使用）
- `versions` - 列出所有版本及破坏性变更
- `compare` - 比较两个版本
- `breaking` - 仅显示破坏性变更
- `migrations` - 显示可自动迁移的变更

```javascript
// 标准（推荐）
get_node({nodeType: "nodes-base.httpRequest"})

// 获取文档
get_node({nodeType: "nodes-base.webhook", mode: "docs"})

// 搜索属性
get_node({nodeType: "nodes-base.httpRequest", mode: "search_properties", propertyQuery: "auth"})

// 检查版本
get_node({nodeType: "nodes-base.executeWorkflow", mode: "versions"})
```

### validate_node（统一验证）

**模式**：
- `full` (默认) - 包含错误/警告/建议的全面验证
- `minimal` - 仅快速检查必填字段

**配置文件** (用于 mode="full")：
- `minimal` - 非常宽松
- `runtime` - 标准（默认，推荐）
- `ai-friendly` - 针对 AI 工作流的平衡配置
- `strict` - 最严格（生产环境）

```javascript
// 使用 runtime 配置文件的完整验证
validate_node({nodeType: "nodes-base.slack", config: {...}, profile: "runtime"})

// 快速必填字段检查
validate_node({nodeType: "nodes-base.webhook", config: {}, mode: "minimal"})
```

---

## 性能特征

| 工具 | 响应时间 | 响应体大小 |
|------|---------------|--------------|
| search_nodes | <20ms | 小 |
| get_node (standard) | <10ms | ~1-2KB |
| get_node (full) | <100ms | 3-8KB |
| validate_node (minimal) | <50ms | 小 |
| validate_node (full) | <100ms | 中等 |
| validate_workflow | 100-500ms | 中等 |
| n8n_create_workflow | 100-500ms | 中等 |
| n8n_update_partial_workflow | 50-200ms | 小 |
| n8n_deploy_template | 200-500ms | 中等 |

---

## 最佳实践

### 推荐
- 对大多数用例使用 `get_node({detail: "standard"})`
- 显式指定验证配置文件 (`profile: "runtime"`)
- 使用智能参数 (`branch`, `case`) 提高清晰度
- 在工作流更新中包含 `intent` 参数
- 遵循 search → get_node → validate 工作流
- 迭代式构建工作流（编辑间隔平均 56 秒）
- 每次重要更改后验证
- 使用 `includeExamples: true` 获取真实配置
- 使用 `n8n_deploy_template` 快速开始

### 避免
- 除非必要，否则不要使用 `detail: "full"`（浪费 token）
- 不要忘记 nodeType 前缀 (`nodes-base.*`)
- 不要跳过验证配置文件
- 不要尝试一次性构建工作流（迭代！）
- 不要忽略自动清理行为
- 不要在搜索/验证工具中使用完整前缀 (`n8n-nodes-base.*`)
- 不要忘记构建后激活工作流

---

## 总结

**最重要**：
1. 使用 **get_node** 并设置 `detail: "standard"`（默认）- 覆盖 95% 的用例
2. nodeType 格式不同：`nodes-base.*`（搜索/验证）vs `n8n-nodes-base.*`（工作流）
3. 指定**验证配置文件**（推荐 `runtime`）
4. 使用**智能参数** (`branch="true"`, `case=0`)
5. 在工作流更新中包含 **intent 参数**
6. 更新时**自动清理**会在所有节点上运行
7. 工作流可以通过 **API 激活** (`activateWorkflow` 操作)
8. 工作流是**迭代式构建**的（编辑间隔平均 56 秒）

**常见工作流**：
1. search_nodes → 查找节点
2. get_node → 了解配置
3. validate_node → 检查配置
4. n8n_create_workflow → 构建
5. n8n_validate_workflow → 验证
6. n8n_update_partial_workflow → 迭代
7. activateWorkflow → 上线！

详情参见：
- SEARCH_GUIDE.md - 节点发现
- VALIDATION_GUIDE.md - 配置验证
- WORKFLOW_GUIDE.md - 工作流管理

---

**相关技能**：
- n8n Expression Syntax - 在工作流字段中编写表达式
- n8n Workflow Patterns - 来自模板的架构模式
- n8n Validation Expert - 解释验证错误
- n8n Node Configuration - 操作特定要求
- n8n Code JavaScript - 在 Code 节点中编写 JavaScript
- n8n Code Python - 在 Code 节点中编写 Python

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。