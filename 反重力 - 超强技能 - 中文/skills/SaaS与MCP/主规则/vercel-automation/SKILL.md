---
name: vercel-automation
description: "通过 Rube MCP（Composio）自动化执行 Vercel 任务：管理部署、域名、DNS、环境变量、项目和团队。务必先搜索工具以获取最新的 schema。触发词：Vercel、Rube MCP、部署管理、域名配置、DNS 记录、环境变量、项目管理、团队管理、Composio。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化操作 Vercel

通过 Rube MCP，使用 Composio 的 Vercel 工具包来自动化 Vercel 平台操作。

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 配合 toolkit `vercel` 建立有效的 Vercel 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具 schema

## 配置步骤

**获取 Rube MCP**：在你的客户端配置中，将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用 toolkit `vercel` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是 ACTIVE 状态，按照返回的认证链接完成 Vercel OAuth
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 监控与检查部署

**使用场景**：用户希望列出、检查或调试部署

**工具调用顺序**：
1. `VERCEL_LIST_ALL_DEPLOYMENTS` 或 `VERCEL_GET_DEPLOYMENTS` - 使用筛选条件列出部署 [必填]
2. `VERCEL_GET_DEPLOYMENT` 或 `VERCEL_GET_DEPLOYMENT_DETAILS` - 获取特定部署信息 [可选]
3. `VERCEL_GET_DEPLOYMENT_LOGS` 或 `VERCEL_GET_RUNTIME_LOGS` - 查看构建/运行日志 [可选]
4. `VERCEL_GET_DEPLOYMENT_EVENTS` - 获取部署事件时间线 [可选]
5. `VERCEL_LIST_DEPLOYMENT_CHECKS` - 查看部署检查结果 [可选]

**关键参数**：
- `projectId`：按项目筛选部署
- `state`：按部署状态筛选（例如 'READY'、'ERROR'、'BUILDING'）
- `limit`：返回的部署数量
- `target`：按环境筛选（'production'、'preview'）
- `deploymentId` 或 `idOrUrl`：特定部署标识符

**注意事项**：
- 在大多数端点中，部署 ID 和 URL 都可以作为标识符使用
- 构建日志和运行日志是分开的；请使用相应的工具
- `VERCEL_GET_DEPLOYMENT_LOGS` 返回构建日志；`VERCEL_GET_RUNTIME_LOGS` 返回 serverless 函数日志
- 部署事件包含状态转换，对于调试时序问题很有用

### 2. 创建与管理部署

**使用场景**：用户希望触发新的部署

**工具调用顺序**：
1. `VERCEL_LIST_PROJECTS` - 查找目标项目 [前置条件]
2. `VERCEL_CREATE_NEW_DEPLOYMENT` - 触发新部署 [必填]
3. `VERCEL_GET_DEPLOYMENT` - 监控部署进度 [可选]

**关键参数**：
- `name`：部署所属的项目名称
- `target`：部署目标（'production' 或 'preview'）
- `gitSource`：包含 ref/branch 信息的 Git 仓库来源
- `files`：用于基于文件的部署的文件对象数组

**注意事项**：
- `gitSource` 和 `files` 必须二选一，不能同时提供
- 基于 Git 的部署需要正确配置仓库集成
- 生产部署会自动更新生产域名别名
- 部署创建是异步的；请使用 GET_DEPLOYMENT 轮询状态

### 3. 管理环境变量

**使用场景**：用户希望为项目添加、列出或删除环境变量

**工具调用顺序**：
1. `VERCEL_LIST_PROJECTS` - 查找项目 ID [前置条件]
2. `VERCEL_LIST_ENV_VARIABLES` - 列出已有环境变量 [必填]
3. `VERCEL_ADD_ENVIRONMENT_VARIABLE` - 添加新的环境变量 [可选]
4. `VERCEL_DELETE_ENVIRONMENT_VARIABLE` - 删除环境变量 [可选]

**关键参数**：
- `projectId`：目标项目标识符
- `key`：环境变量名称
- `value`：环境变量值
- `target`：环境数组（'production'、'preview'、'development'）
- `type`：变量类型（'plain'、'secret'、'encrypted'、'sensitive'）

**注意事项**：
- 在同一目标环境下，环境变量名称必须唯一
- `type: 'secret'` 的变量创建后无法回读；只返回 ID
- 删除环境变量需要同时提供 `projectId` 和环境变量的 `id`（不是 key 名称）
- 环境变量变更需要重新部署才能生效

### 4. 管理域名与 DNS

**使用场景**：用户希望配置自定义域名或管理 DNS 记录

**工具调用顺序**：
1. `VERCEL_GET_DOMAIN` - 检查域名状态与配置 [必填]
2. `VERCEL_GET_DOMAIN_CONFIG` - 获取 DNS/SSL 配置详情 [可选]
3. `VERCEL_LIST_PROJECT_DOMAINS` - 列出项目关联的域名 [可选]
4. `VERCEL_GET_DNS_RECORDS` - 列出域名的 DNS 记录 [可选]
5. `VERCEL_CREATE_DNS_RECORD` - 添加新的 DNS 记录 [可选]
6. `VERCEL_UPDATE_DNS_RECORD` - 修改已有 DNS 记录 [可选]

**关键参数**：
- `domain`：域名（例如 'example.com'）
- `name`：DNS 记录名/子域名
- `type`：DNS 记录类型（'A'、'AAAA'、'CNAME'、'MX'、'TXT'、'SRV'）
- `value`：DNS 记录值
- `ttl`：生存时间（秒）

**注意事项**：
- 域名必须先添加到 Vercel 账户才能进行 DNS 管理
- SSL 证书会自动配置，但新域名可能需要一些时间
- 根域名不支持 CNAME 记录；请改用 A 记录
- MX 记录需要提供优先级值

### 5. 管理项目

**使用场景**：用户希望列出、检查或更新项目设置

**工具调用顺序**：
1. `VERCEL_LIST_PROJECTS` - 列出所有项目 [必填]
2. `VERCEL_GET_PROJECT` - 获取详细项目信息 [可选]
3. `VERCEL_UPDATE_PROJECT` - 修改项目设置 [可选]

**关键参数**：
- `idOrName`：用于查找的项目 ID 或名称
- `name`：用于更新的项目名称
- `framework`：框架预设（例如 'nextjs'、'vite'、'remix'）
- `buildCommand`：自定义构建命令覆盖
- `rootDirectory`：根目录（若非仓库根目录）

**注意事项**：
- 项目名称在团队/账户内全局唯一
- 更改框架设置会影响后续部署
- `rootDirectory` 相对于仓库根目录

### 6. 团队管理

**使用场景**：用户希望查看团队信息或列出团队成员

**工具调用顺序**：
1. `VERCEL_LIST_TEAMS` - 列出用户所属的全部团队 [必填]
2. `VERCEL_GET_TEAM` - 获取详细团队信息 [可选]
3. `VERCEL_GET_TEAM_MEMBERS` - 列出特定团队的成员 [可选]

**关键参数**：
- `teamId`：团队标识符
- `limit`：每页结果数
- `role`：按角色筛选成员

**注意事项**：
- 团队操作需要相应的团队级权限
- 个人账户没有团队；团队端点会返回空结果
- 成员角色包括 'OWNER'、'MEMBER'、'DEVELOPER'、'VIEWER'

## 常用模式

### ID 解析

**项目名称 -> 项目 ID**：
```
1. Call VERCEL_LIST_PROJECTS
2. Find project by name in response
3. Extract id field for subsequent operations
```

**域名 -> DNS 记录**：
```
1. Call VERCEL_GET_DNS_RECORDS with domain name
2. Extract record IDs for update/delete operations
```

### 分页

- 使用 `limit` 参数控制分页大小
- 检查响应中的分页令牌或 `next` 字段
- 持续拉取直到没有更多页

## 已知注意事项

**部署状态**：
- 状态包括：INITIALIZING、ANALYZING、BUILDING、DEPLOYING、READY、ERROR、CANCELED、QUEUED
- 只有 READY 状态的部署才会上线并对外提供流量
- ERROR 状态的部署应通过日志检查失败详情

**环境变量**：
- 密钥类型变量为只写；创建后无法获取其值
- 环境变量按环境（production、preview、development）作用域
- 环境变量变更需要重新部署才能生效

**速率限制**：
- Vercel API 各个端点存在速率限制
- 遇到 429 响应时实施退避策略
- 尽可能批量操作以减少 API 调用

## 速查表

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 列出项目 | VERCEL_LIST_PROJECTS | limit |
| 获取项目详情 | VERCEL_GET_PROJECT | idOrName |
| 更新项目 | VERCEL_UPDATE_PROJECT | idOrName, name, framework |
| 列出部署 | VERCEL_LIST_ALL_DEPLOYMENTS | projectId, state, limit |
| 获取部署 | VERCEL_GET_DEPLOYMENT | idOrUrl |
| 创建部署 | VERCEL_CREATE_NEW_DEPLOYMENT | name, target, gitSource |
| 部署日志 | VERCEL_GET_DEPLOYMENT_LOGS | deploymentId |
| 运行日志 | VERCEL_GET_RUNTIME_LOGS | deploymentId |
| 列出环境变量 | VERCEL_LIST_ENV_VARIABLES | projectId |
| 添加环境变量 | VERCEL_ADD_ENVIRONMENT_VARIABLE | projectId, key, value, target |
| 删除环境变量 | VERCEL_DELETE_ENVIRONMENT_VARIABLE | projectId, id |
| 获取域名 | VERCEL_GET_DOMAIN | domain |
| 获取域名配置 | VERCEL_GET_DOMAIN_CONFIG | domain |
| 列出 DNS 记录 | VERCEL_GET_DNS_RECORDS | domain |
| 创建 DNS 记录 | VERCEL_CREATE_DNS_RECORD | domain, name, type, value |
| 更新 DNS 记录 | VERCEL_UPDATE_DNS_RECORD | domain, recordId |
| 列出项目域名 | VERCEL_LIST_PROJECT_DOMAINS | projectId |
| 列出团队 | VERCEL_LIST_TEAMS | (none) |
| 获取团队 | VERCEL_GET_TEAM | teamId |
| 获取团队成员 | VERCEL_GET_TEAM_MEMBERS | teamId, limit |

## 使用时机

本技能适用于执行上述概述中描述的工作流或操作。

## 限制说明
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
