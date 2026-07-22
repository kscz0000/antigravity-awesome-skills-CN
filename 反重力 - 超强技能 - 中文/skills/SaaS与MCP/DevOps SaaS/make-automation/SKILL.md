---
name: make-automation
description: "通过 Rube MCP (Composio) 自动化 Make (Integromat) 任务：操作记录、枚举查询、语言和时区查找。始终先搜索工具获取最新 schema。当用户要求'操作 Make 自动化'、'查询 Make 操作记录'、'获取 Make 语言/时区列表'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Make

通过 Composio 的 Make 工具包和 Rube MCP 自动化 Make（原 Integromat）操作。

## 前提条件

- Rube MCP 已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立了 Make 的活跃连接，工具包为 `make`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 能正常响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包设为 `make`
3. 若连接状态非 ACTIVE，按返回的认证链接完成 Make 身份验证
4. 确认连接状态为 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 获取操作数据

**适用场景**：需要从 Make 场景中检索操作日志或使用数据

**工具调用顺序**：
1. `MAKE_GET_OPERATIONS` - 检索操作记录 [必需]

**关键参数**：
- 通过 RUBE_SEARCH_TOOLS 查看当前 schema 获取可用筛选条件
- 可包含日期范围、场景 ID 或状态筛选

**注意事项**：
- 操作数据可能分页返回；注意检查分页标记
- 日期筛选格式须与 schema 要求一致
- 大量结果应按日期范围或场景筛选

### 2. 列出可用语言

**适用场景**：需要查看 Make 场景或界面支持的语言

**工具调用顺序**：
1. `MAKE_LIST_ENUMS_LANGUAGES` - 获取所有支持的语言代码 [必需]

**关键参数**：
- 无必需参数；返回完整语言列表

**注意事项**：
- 语言代码遵循标准区域设置格式（如 'en'、'fr'、'de'）
- 列表为静态数据，极少变更；建议缓存结果

### 3. 列出可用时区

**适用场景**：需要查看 Make 场景调度支持的时区

**工具调用顺序**：
1. `MAKE_LIST_ENUMS_TIMEZONES` - 获取所有支持的时区标识符 [必需]

**关键参数**：
- 无必需参数；返回完整时区列表

**注意事项**：
- 时区标识符采用 IANA 格式（如 'America/New_York'、'Europe/London'）
- 列表为静态数据，极少变更；建议缓存结果
- 配置场景调度时须使用这些精确的时区字符串

### 4. 场景配置查询

**适用场景**：需要用正确的语言和时区值配置场景

**工具调用顺序**：
1. `MAKE_LIST_ENUMS_LANGUAGES` - 获取有效语言代码 [必需]
2. `MAKE_LIST_ENUMS_TIMEZONES` - 获取有效时区标识符 [必需]

**关键参数**：
- 两次调用均无需参数

**注意事项**：
- 配置前务必对照枚举列表验证语言和时区值
- 场景配置中使用无效值会导致错误

## 常用模式

### 枚举验证

配置任何接受语言或时区的 Make 场景属性前：
```
1. Call MAKE_LIST_ENUMS_LANGUAGES or MAKE_LIST_ENUMS_TIMEZONES
2. Verify the desired value exists in the returned list
3. Use the exact string value from the enum list
```

### 操作监控

```
1. Call MAKE_GET_OPERATIONS with date range filters
2. Analyze operation counts, statuses, and error rates
3. Identify failed operations for troubleshooting
```

### 枚举缓存策略

语言和时区列表为静态数据：
```
1. Call MAKE_LIST_ENUMS_LANGUAGES once at workflow start
2. Store results in memory or local cache
3. Validate user inputs against cached values
4. Refresh cache only when starting a new session
```

### 操作分析工作流

用于场景健康监控：
```
1. Call MAKE_GET_OPERATIONS with recent date range
2. Group operations by scenario ID
3. Calculate success/failure ratios per scenario
4. Identify scenarios with high error rates
5. Report findings to user or notification channel
```

### 与其他工具包集成

Make 工作流通常连接其他应用。组合多工具工作流：
```
1. Call RUBE_SEARCH_TOOLS to find tools for the target app
2. Connect required toolkits via RUBE_MANAGE_CONNECTIONS
3. Use Make operations data to understand workflow execution patterns
4. Execute equivalent workflows directly via individual app toolkits
```

## 已知注意事项

**工具包功能有限**：
- Composio 中的 Make 工具包目前工具有限（操作、语言、时区）
- 完整场景管理（创建、编辑、运行场景）建议使用 Make 原生 API
- 始终调用 RUBE_SEARCH_TOOLS 检查是否有新增工具
- 工具包可能逐步扩展；定期重新检查

**操作数据**：
- 活跃账户的操作记录量可能很大
- 务必按日期范围筛选，避免拉取过多数据
- 操作次数与 Make 的定价层级和配额使用相关
- 失败操作应排查原因；可能反映场景配置问题

**响应解析**：
- 响应数据可能嵌套在 `data` 键下
- 枚举列表返回对象数组，含 code 和 label 字段
- 操作数据包含场景执行的嵌套元数据
- 解析时须做防御性处理，对可选字段设置回退值

**速率限制**：
- Make API 按 API token 设有速率限制
- 避免对同一端点快速重复调用
- 枚举结果（语言、时区）极少变更，应缓存
- 操作查询应使用精确的日期范围

**身份验证**：
- Make API 使用基于 token 的认证
- 不同 token 可能有不同权限范围
- 部分操作数据可能因 token 权限范围受限
- 确认认证用户有权访问目标组织

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 获取操作记录 | MAKE_GET_OPERATIONS | （查看 schema 获取筛选条件） |
| 列出语言 | MAKE_LIST_ENUMS_LANGUAGES | （无） |
| 列出时区 | MAKE_LIST_ENUMS_TIMEZONES | （无） |

## 补充说明

### 替代方案

Make 工具包功能有限，常见用例可考虑以下替代方案：

| Make 用例 | 替代方案 |
|-----------|---------|
| 触发场景 | 直接使用 Make 原生 webhook 或 API 端点 |
| 创建场景 | 直接使用 Make 场景管理 API |
| 定时执行 | 使用 RUBE_MANAGE_RECIPE_SCHEDULE 组合工作流 |
| 多应用工作流 | 通过 RUBE_MULTI_EXECUTE_TOOL 组合各工具包工具 |
| 数据转换 | 使用 RUBE_REMOTE_WORKBENCH 处理复杂逻辑 |

### 组合等效工作流

不必仅依赖 Make 工具包，可直接构建等效自动化：
1. 识别 Make 场景涉及的应用
2. 通过 RUBE_SEARCH_TOOLS 搜索各应用的工具
3. 连接所有需要的工具包
4. 使用各应用工具逐步构建工作流
5. 通过 RUBE_CREATE_UPDATE_RECIPE 保存为可复用的 recipe

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代针对具体环境的验证、测试或专家评审
- 若缺少必要输入、权限、安全边界或成功标准，应停止并请求澄清
