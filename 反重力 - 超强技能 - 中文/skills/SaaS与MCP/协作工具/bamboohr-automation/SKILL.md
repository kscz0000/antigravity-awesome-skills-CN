---
name: bamboohr-automation
description: "通过 Rube MCP (Composio) 自动化 BambooHR 任务：员工、休假、福利、家属、员工信息更新。始终先搜索工具以获取当前模式。当用户要求'BambooHR自动化'、'管理员工信息'、'请假审批'、'休假管理'、'HR自动化'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 BambooHR

通过 Composio 的 BambooHR 工具包和 Rube MCP 自动化 BambooHR 人力资源操作。

## 前提条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立 BambooHR 活跃连接，工具包为 `bamboohr`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需密钥——只需添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 可响应，验证 Rube MCP 可用
2. 使用工具包 `bamboohr` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 BambooHR 认证
4. 在运行任何工作流之前确认连接状态为 ACTIVE

## 核心工作流

### 1. 列出和搜索员工

**使用时机**：用户想要查找员工或获取完整员工目录

**工具调用顺序**：
1. `BAMBOOHR_GET_ALL_EMPLOYEES` - 获取员工目录 [必需]
2. `BAMBOOHR_GET_EMPLOYEE` - 获取特定员工的详细信息 [可选]

**关键参数**：
- GET_ALL_EMPLOYEES：无必需参数；返回目录
- GET_EMPLOYEE：
  - `id`：员工 ID（数字）
  - `fields`：逗号分隔的返回字段列表（如 'firstName,lastName,department,jobTitle'）

**注意事项**：
- 员工 ID 为数字整数
- GET_ALL_EMPLOYEES 返回基本目录信息；使用 GET_EMPLOYEE 获取完整详情
- `fields` 参数控制返回哪些字段；省略可能只返回最少数据
- 常用字段：firstName、lastName、department、division、jobTitle、workEmail、status
- 可能包含已离职/已终止员工；检查 `status` 字段

### 2. 追踪员工变更

**使用时机**：用户想要检测最近的员工数据变更，用于同步或审计

**工具调用顺序**：
1. `BAMBOOHR_EMPLOYEE_GET_CHANGED` - 获取近期有变更的员工 [必需]

**关键参数**：
- `since`：变更检测阈值的 ISO 8601 日期时间字符串
- `type`：要检查的变更类型（如 'inserted'、'updated'、'deleted'）

**注意事项**：
- `since` 参数为必需；使用 ISO 8601 格式（如 '2024-01-15T00:00:00Z'）
- 返回变更员工的 ID，而非完整员工数据
- 必须单独调用 GET_EMPLOYEE 获取每位变更员工的详情
- 适用于增量同步工作流；缓存上次同步时间戳

### 3. 管理休假

**使用时机**：用户想要查看休假余额、申请休假或管理休假申请

**工具调用顺序**：
1. `BAMBOOHR_GET_META_TIME_OFF_TYPES` - 列出可用的休假类型 [前置条件]
2. `BAMBOOHR_GET_TIME_OFF_BALANCES` - 查看当前余额 [可选]
3. `BAMBOOHR_GET_TIME_OFF_REQUESTS` - 列出现有申请 [可选]
4. `BAMBOOHR_CREATE_TIME_OFF_REQUEST` - 提交新申请 [可选]
5. `BAMBOOHR_UPDATE_TIME_OFF_REQUEST` - 修改或批准/拒绝申请 [可选]

**关键参数**：
- 余额查询：`employeeId`、休假类型 ID
- 申请查询：`start`、`end`（日期范围）、`employeeId`
- 创建申请：
  - `employeeId`：申请休假的员工
  - `timeOffTypeId`：来自 GET_META_TIME_OFF_TYPES 的类型 ID
  - `start`：开始日期（YYYY-MM-DD）
  - `end`：结束日期（YYYY-MM-DD）
  - `amount`：天数/小时数
  - `notes`：申请备注（可选）
- 更新申请：`requestId`、`status`（'approved'、'denied'、'cancelled'）

**注意事项**：
- 休假类型 ID 为数字；先通过 GET_META_TIME_OFF_TYPES 解析
- 日期格式为 'YYYY-MM-DD'
- 余额可能以小时或天数表示，取决于公司配置
- 申请状态更新需要相应权限（经理/管理员）
- 创建申请不会自动批准；需要单独的审批步骤

### 4. 更新员工信息

**使用时机**：用户想要修改员工档案数据

**工具调用顺序**：
1. `BAMBOOHR_GET_EMPLOYEE` - 获取当前员工数据 [前置条件]
2. `BAMBOOHR_UPDATE_EMPLOYEE` - 更新员工字段 [必需]

**关键参数**：
- `id`：员工 ID（数字，必需）
- 要更新的字段-值对（如 `department`、`jobTitle`、`workPhone`）

**注意事项**：
- 仅更新请求中包含的字段；其余字段保持不变
- 部分字段为只读，无法通过 API 更新
- 字段名必须与 BambooHR 预期的字段名完全匹配
- 更新操作会被审计；变更会出现在员工的变更历史中
- 更新前先用 GET_EMPLOYEE 确认当前值，避免覆盖

### 5. 管理家属和福利

**使用时机**：用户想要查看员工家属或福利覆盖信息

**工具调用顺序**：
1. `BAMBOOHR_DEPENDENTS_GET_ALL` - 列出所有家属 [必需]
2. `BAMBOOHR_BENEFIT_GET_COVERAGES` - 获取福利覆盖详情 [可选]

**关键参数**：
- 家属查询：可选 `employeeId` 筛选
- 福利查询：取决于模式；查看 RUBE_SEARCH_TOOLS 获取当前参数

**注意事项**：
- 家属数据包含敏感 PII；需妥善处理
- 福利覆盖可能包含每位员工的多种计划类型
- 并非所有 BambooHR 套餐都包含福利管理功能；检查账户功能
- 数据访问取决于密钥权限

## 常见模式

### ID 解析

**员工姓名 -> 员工 ID**：
```
1. Call BAMBOOHR_GET_ALL_EMPLOYEES
2. Find employee by name in directory results
3. Extract id (numeric) for detailed operations
```

**休假类型名称 -> 类型 ID**：
```
1. Call BAMBOOHR_GET_META_TIME_OFF_TYPES
2. Find type by name (e.g., 'Vacation', 'Sick Leave')
3. Extract id for time-off requests
```

### 增量同步模式

用于保持外部系统与 BambooHR 同步：
```
1. Store last_sync_timestamp
2. Call BAMBOOHR_EMPLOYEE_GET_CHANGED with since=last_sync_timestamp
3. For each changed employee ID, call BAMBOOHR_GET_EMPLOYEE
4. Process updates in external system
5. Update last_sync_timestamp
```

### 休假工作流

```
1. GET_META_TIME_OFF_TYPES -> find type ID
2. GET_TIME_OFF_BALANCES -> verify available balance
3. CREATE_TIME_OFF_REQUEST -> submit request
4. UPDATE_TIME_OFF_REQUEST -> approve/deny (manager action)
```

## 已知注意事项

**员工 ID**：
- 始终为数字整数
- 通过 GET_ALL_EMPLOYEES 将姓名解析为 ID
- 已离职员工保留其 ID

**日期格式**：
- 休假日期：'YYYY-MM-DD'
- 变更检测：带时区的 ISO 8601
- 不同端点间格式可能不一致；检查每个端点的模式

**权限**：
- 密钥权限决定可访问的字段和操作
- 部分操作需要管理员或经理级别权限
- 休假审批需要相应的角色权限

**敏感数据**：
- 员工数据包含 PII（姓名、地址、SSN 等）
- 所有响应需采取适当的安全措施
- 家属数据尤其敏感

**速率限制**：
- BambooHR API 对每个密钥有速率限制
- 批量操作应进行节流
- GET_ALL_EMPLOYEES 比逐个调用 GET_EMPLOYEE 更高效

**响应解析**：
- 响应数据可能嵌套在 `data` 键下
- 员工字段因 `fields` 参数而异
- 空字段可能被省略或返回为 null
- 防御性解析，设置回退值

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出所有员工 | BAMBOOHR_GET_ALL_EMPLOYEES | (无) |
| 获取员工详情 | BAMBOOHR_GET_EMPLOYEE | id, fields |
| 追踪变更 | BAMBOOHR_EMPLOYEE_GET_CHANGED | since, type |
| 休假类型 | BAMBOOHR_GET_META_TIME_OFF_TYPES | (无) |
| 休假余额 | BAMBOOHR_GET_TIME_OFF_BALANCES | employeeId |
| 列出休假申请 | BAMBOOHR_GET_TIME_OFF_REQUESTS | start, end, employeeId |
| 创建休假申请 | BAMBOOHR_CREATE_TIME_OFF_REQUEST | employeeId, timeOffTypeId, start, end |
| 更新休假申请 | BAMBOOHR_UPDATE_TIME_OFF_REQUEST | requestId, status |
| 更新员工 | BAMBOOHR_UPDATE_EMPLOYEE | id, (字段更新) |
| 列出家属 | BAMBOOHR_DEPENDENTS_GET_ALL | employeeId |
| 福利覆盖 | BAMBOOHR_BENEFIT_GET_COVERAGES | (查看模式) |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
