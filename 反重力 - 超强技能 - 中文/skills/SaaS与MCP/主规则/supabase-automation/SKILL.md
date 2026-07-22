---
name: supabase-automation
description: "通过 Rube MCP (Composio) 自动化 Supabase 数据库查询、表管理、项目管理、存储、Edge Functions 和 SQL 执行。始终先搜索工具获取当前模式。触发词：Supabase自动化、Supabase查询、Supabase数据库管理、Supabase表操作、Supabase SQL执行、Edge Functions管理、存储桶管理、Rube MCP"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Supabase

通过 Composio 的 Supabase 工具包自动化 Supabase 操作，包括数据库查询、表结构检查、SQL 执行、项目和组织管理、存储桶、Edge Functions 及服务健康监控。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Supabase 连接，工具包为 `supabase`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包为 `supabase`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Supabase 认证
4. 在运行任何工作流之前确认连接状态为 ACTIVE

## 核心工作流

### 1. 查询和管理数据库表

**适用场景**：用户需要从表中读取数据、检查表结构或执行 CRUD 操作

**工具调用顺序**：
1. `SUPABASE_LIST_ALL_PROJECTS` - 列出项目以找到目标 project_ref [前置条件]
2. `SUPABASE_LIST_TABLES` - 列出数据库中所有表和视图 [前置条件]
3. `SUPABASE_GET_TABLE_SCHEMAS` - 获取详细的列类型、约束和关系 [写入操作的前置条件]
4. `SUPABASE_SELECT_FROM_TABLE` - 带筛选、排序和分页查询行 [读取操作必需]
5. `SUPABASE_BETA_RUN_SQL_QUERY` - 执行任意 SQL，用于复杂查询、插入、更新或删除 [写入操作必需]

**SELECT_FROM_TABLE 关键参数**：
- `project_ref`：20 字符小写项目引用
- `table`：要查询的表或视图名称
- `select`：逗号分隔的列列表（支持嵌套选择和 JSON 路径，如 `profile->avatar_url`）
- `filters`：包含 `column`、`operator`、`value` 的筛选对象数组
- `order`：排序表达式，如 `created_at.desc`
- `limit`：返回的最大行数（最小为 1）
- `offset`：分页跳过的行数

**PostgREST 筛选运算符**：
- `eq`、`neq`：等于 / 不等于
- `gt`、`gte`、`lt`、`lte`：比较运算符
- `like`、`ilike`：模式匹配（区分大小写 / 不区分大小写）
- `is`：IS 检查（用于 null、true、false）
- `in`：在值列表中
- `cs`、`cd`：包含 / 被包含（数组）
- `fts`、`plfts`、`phfts`、`wfts`：全文搜索变体

**RUN_SQL_QUERY 关键参数**：
- `ref`：项目引用（20 个小写字母，模式 `^[a-z]{20}$`）
- `query`：有效的 PostgreSQL SQL 语句
- `read_only`：布尔值，强制只读事务（SELECT 查询更安全）

**注意事项**：
- `project_ref` 必须恰好为 20 个小写字母（仅 a-z，不含数字或连字符）
- `SELECT_FROM_TABLE` 是只读的；INSERT、UPDATE、DELETE 操作需使用 `RUN_SQL_QUERY`
- 对于 PostgreSQL 数组列（text[]、integer[]），使用 `ARRAY['item1', 'item2']` 或 `'{"item1", "item2"}'` 语法，而非 JSON 数组语法 `'["item1", "item2"]'`
- 区分大小写的 SQL 标识符在查询中必须加双引号
- 复杂 DDL 操作可能超时（约 60 秒限制）；拆分为更小的查询
- ERROR 42P01 "relation does not exist" 通常表示未加引号的大小写敏感标识符
- ERROR 42883 "function does not exist" 表示调用了非标准辅助函数；优先使用 information_schema 查询

### 2. 管理项目和组织

**适用场景**：用户需要列出项目、检查配置或管理组织

**工具调用顺序**：
1. `SUPABASE_LIST_ALL_ORGANIZATIONS` - 列出所有组织（ID 和名称）[必需]
2. `SUPABASE_GETS_INFORMATION_ABOUT_THE_ORGANIZATION` - 通过 slug 获取详细组织信息 [可选]
3. `SUPABASE_LIST_MEMBERS_OF_AN_ORGANIZATION` - 列出组织成员及其角色和 MFA 状态 [可选]
4. `SUPABASE_LIST_ALL_PROJECTS` - 列出所有项目及元数据 [必需]
5. `SUPABASE_GETS_PROJECT_S_POSTGRES_CONFIG` - 获取数据库配置 [可选]
6. `SUPABASE_GETS_PROJECT_S_AUTH_CONFIG` - 获取认证配置 [可选]
7. `SUPABASE_GET_PROJECT_API_KEYS` - 获取 API 密钥（敏感——谨慎处理）[可选]
8. `SUPABASE_GETS_PROJECT_S_SERVICE_HEALTH_STATUS` - 检查服务健康状态 [可选]

**关键参数**：
- `ref`：项目特定工具的项目引用
- `slug`：组织工具的组织 slug（URL 友好标识符）
- `services`：健康检查的服务数组：`auth`、`db`、`db_postgres_user`、`pg_bouncer`、`pooler`、`realtime`、`rest`、`storage`

**注意事项**：
- `LIST_ALL_ORGANIZATIONS` 同时返回 `id` 和 `slug`；`LIST_MEMBERS_OF_AN_ORGANIZATION` 需要 `slug` 而非 `id`
- `GET_PROJECT_API_KEYS` 返回真实密钥——切勿记录、显示或持久化完整密钥值
- `GETS_PROJECT_S_SERVICE_HEALTH_STATUS` 需要非空的 `services` 数组；空数组会导致 invalid_request 错误
- 配置工具在令牌缺少所需权限范围时可能返回 401/403；优雅处理而非中断整个工作流

### 3. 检查数据库模式

**适用场景**：用户需要了解表结构、列、约束或生成类型

**工具调用顺序**：
1. `SUPABASE_LIST_ALL_PROJECTS` - 找到目标项目 [前置条件]
2. `SUPABASE_LIST_TABLES` - 枚举所有表和视图及元数据 [必需]
3. `SUPABASE_GET_TABLE_SCHEMAS` - 获取特定表的详细模式 [必需]
4. `SUPABASE_GENERATE_TYPE_SCRIPT_TYPES` - 从模式生成 TypeScript 类型 [可选]

**LIST_TABLES 关键参数**：
- `project_ref`：项目引用
- `schemas`：要搜索的模式名称数组（如 `["public"]`）；省略则搜索所有非系统模式
- `include_views`：在表旁边包含视图（默认 true）
- `include_metadata`：包含行数估算和大小（默认 true）
- `include_system_schemas`：包含 pg_catalog、information_schema 等（默认 false）

**GET_TABLE_SCHEMAS 关键参数**：
- `project_ref`：项目引用
- `table_names`：表名数组（每次请求最多 20 个）；支持模式前缀，如 `public.users`、`auth.users`
- `include_relationships`：包含外键信息（默认 true）
- `include_indexes`：包含索引信息（默认 true）
- `exclude_null_values`：隐藏 null 字段以获得更简洁的输出（默认 true）

**GENERATE_TYPE_SCRIPT_TYPES 关键参数**：
- `ref`：项目引用
- `included_schemas`：逗号分隔的模式名称（默认 `"public"`）

**注意事项**：
- 不带模式前缀的表名默认为 `public` 模式
- LIST_TABLES 的 `row_count` 和 `size_bytes` 对于视图或新创建的表可能为 null；应视为未知，而非零
- GET_TABLE_SCHEMAS 每次请求最多 20 个表；需要时分批处理
- TypeScript 类型包含指定模式中的所有表；无法筛选单个表

### 4. 管理 Edge Functions

**适用场景**：用户需要列出、检查或操作 Supabase Edge Functions

**工具调用顺序**：
1. `SUPABASE_LIST_ALL_PROJECTS` - 找到项目引用 [前置条件]
2. `SUPABASE_LIST_ALL_FUNCTIONS` - 列出所有 Edge Functions 及元数据 [必需]
3. `SUPABASE_RETRIEVE_A_FUNCTION` - 获取特定函数的详细信息 [可选]

**关键参数**：
- `ref`：项目引用
- RETRIEVE_A_FUNCTION 的函数 slug

**注意事项**：
- `LIST_ALL_FUNCTIONS` 仅返回元数据，不返回函数代码或日志
- `created_at` 和 `updated_at` 可能是 Unix 纪元毫秒；需转换为可读时间戳
- 这些工具无法创建或部署 Edge Functions；它们是只读检查工具
- 没有组织/项目管理员权限可能遇到权限错误

### 5. 管理存储桶

**适用场景**：用户需要列出存储桶或管理文件存储

**工具调用顺序**：
1. `SUPABASE_LIST_ALL_PROJECTS` - 找到项目引用 [前置条件]
2. `SUPABASE_LISTS_ALL_BUCKETS` - 列出所有存储桶 [必需]

**关键参数**：
- `ref`：项目引用

**注意事项**：
- `LISTS_ALL_BUCKETS` 仅返回存储桶列表，不返回存储桶内容或访问策略
- 文件上传方面，`SUPABASE_RESUMABLE_UPLOAD_SIGN_OPTIONS_WITH_ID` 仅处理 TUS 可恢复上传的 CORS 预检
- 直接文件操作可能需要使用 `proxy_execute` 配合 Supabase 存储 API

## 常用模式

### ID 解析
- **项目引用**：`SUPABASE_LIST_ALL_PROJECTS` -- 提取 `ref` 字段（20 个小写字母）
- **组织 slug**：`SUPABASE_LIST_ALL_ORGANIZATIONS` -- 使用 `slug`（而非 `id`）用于下游组织工具
- **表名**：`SUPABASE_LIST_TABLES` -- 在查询前枚举可用表
- **模式发现**：`SUPABASE_GET_TABLE_SCHEMAS` -- 在写入前检查列和约束

### 分页
- `SUPABASE_SELECT_FROM_TABLE`：使用 `offset` + `limit` 分页。按 limit 递增 offset，直到返回行数少于 limit。
- `SUPABASE_LIST_ALL_PROJECTS`：大型账户可能需要分页；跟随游标/页码直到耗尽。
- `SUPABASE_LIST_TABLES`：大型数据库可能需要分页。

### SQL 最佳实践
- 编写 SQL 前始终使用 `SUPABASE_GET_TABLE_SCHEMAS` 或 `SUPABASE_LIST_TABLES`
- SELECT 查询使用 `read_only: true` 防止意外修改
- 区分大小写的标识符加引号：`SELECT * FROM "MyTable"` 而非 `SELECT * FROM MyTable`
- 数组列使用 PostgreSQL 数组语法：`ARRAY['a', 'b']` 而非 `['a', 'b']`
- 将复杂 DDL 拆分为更小的语句以避免超时

## 已知注意事项

### ID 格式
- 项目引用恰好为 20 个小写字母（a-z）：模式 `^[a-z]{20}$`
- 组织标识符同时有 `id`（UUID）和 `slug`（URL 友好字符串）；不同工具接受的标识符不同
- `LIST_MEMBERS_OF_AN_ORGANIZATION` 需要 `slug` 而非 `id`

### SQL 执行
- `BETA_RUN_SQL_QUERY` 对复杂操作有约 60 秒超时
- 必须使用 PostgreSQL 数组语法：`ARRAY['item']` 或 `'{"item"}'`，而非 JSON 语法 `'["item"]'`
- 区分大小写的标识符在 SQL 中必须加双引号
- ERROR 42P01：关系不存在（检查引号和模式前缀）
- ERROR 42883：函数不存在（使用 information_schema 而非自定义辅助函数）

### 敏感数据
- `GET_PROJECT_API_KEYS` 返回服务角色密钥——切勿暴露完整值
- 认证配置工具排除了密钥但仍可能包含敏感配置
- 始终在输出中遮盖或截断 API 密钥

### 模式元数据
- `LIST_TABLES` 的 `row_count` 和 `size_bytes` 可能为 null；不要视为零
- 系统模式默认排除；设置 `include_system_schemas: true` 可查看
- 除非设置 `include_views: false`，视图会与表一起显示

### 速率限制和权限
- 增强工具（API 密钥、配置）在缺少适当权限范围时可能返回 401/403；优雅跳过
- 大型表列表可能需要分页
- `GETS_PROJECT_S_SERVICE_HEALTH_STATUS` 在 `services` 数组为空时会失败——始终至少指定一个服务

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出组织 | `SUPABASE_LIST_ALL_ORGANIZATIONS` | (无) |
| 获取组织信息 | `SUPABASE_GETS_INFORMATION_ABOUT_THE_ORGANIZATION` | `slug` |
| 列出组织成员 | `SUPABASE_LIST_MEMBERS_OF_AN_ORGANIZATION` | `slug` |
| 列出项目 | `SUPABASE_LIST_ALL_PROJECTS` | (无) |
| 列出表 | `SUPABASE_LIST_TABLES` | `project_ref`、`schemas` |
| 获取表模式 | `SUPABASE_GET_TABLE_SCHEMAS` | `project_ref`、`table_names` |
| 查询表 | `SUPABASE_SELECT_FROM_TABLE` | `project_ref`、`table`、`select`、`filters` |
| 执行 SQL | `SUPABASE_BETA_RUN_SQL_QUERY` | `ref`、`query`、`read_only` |
| 生成 TS 类型 | `SUPABASE_GENERATE_TYPE_SCRIPT_TYPES` | `ref`、`included_schemas` |
| Postgres 配置 | `SUPABASE_GETS_PROJECT_S_POSTGRES_CONFIG` | `ref` |
| 认证配置 | `SUPABASE_GETS_PROJECT_S_AUTH_CONFIG` | `ref` |
| 获取 API 密钥 | `SUPABASE_GET_PROJECT_API_KEYS` | `ref` |
| 服务健康 | `SUPABASE_GETS_PROJECT_S_SERVICE_HEALTH_STATUS` | `ref`、`services` |
| 列出 Edge Functions | `SUPABASE_LIST_ALL_FUNCTIONS` | `ref` |
| 获取 Edge Function | `SUPABASE_RETRIEVE_A_FUNCTION` | `ref`、函数 slug |
| 列出存储桶 | `SUPABASE_LISTS_ALL_BUCKETS` | `ref` |
| 列出数据库分支 | `SUPABASE_LIST_ALL_DATABASE_BRANCHES` | `ref` |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
