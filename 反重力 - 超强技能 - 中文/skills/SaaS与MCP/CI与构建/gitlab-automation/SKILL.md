---
name: gitlab-automation
description: "通过 Rube MCP (Composio) 自动化 GitLab 项目管理、Issue、Merge Request、Pipeline、分支和用户操作。始终先搜索工具以获取当前 schema。当用户要求 GitLab 自动化、GitLab 项目管理、GitLab Issue 管理、GitLab MR 管理、GitLab Pipeline 监控时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# GitLab Automation via Rube MCP

通过 Composio 的 GitLab 工具包自动化 GitLab 操作，包括项目管理、Issue 追踪、Merge Request 工作流、CI/CD Pipeline 监控、分支管理和用户管理。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 RUBE_MANAGE_CONNECTIONS 工具包 gitlab 建立活跃的 GitLab 连接
- 始终先调用 RUBE_SEARCH_TOOLS 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 https://rube.app/mcp 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 确认 RUBE_SEARCH_TOOLS 响应以验证 Rube MCP 可用
2. 使用工具包 gitlab 调用 RUBE_MANAGE_CONNECTIONS
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 GitLab OAuth
4. 在运行任何工作流前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 管理 Issue

**何时使用**：用户想要在 GitLab 项目中创建、更新、列出或搜索 Issue

**工具调用顺序**：
1. GITLAB_GET_PROJECTS - 查找目标项目并获取其 ID [前置条件]
2. GITLAB_LIST_PROJECT_ISSUES - 列出并筛选项目的 Issue [必需]
3. GITLAB_CREATE_PROJECT_ISSUE - 创建新 Issue [创建时必需]
4. GITLAB_UPDATE_PROJECT_ISSUE - 更新现有 Issue（标题、标签、状态、指派人）[更新时必需]
5. GITLAB_LIST_PROJECT_USERS - 查找用户 ID 用于指派 [可选]

**关键参数**：
- id：项目 ID（整数）或 URL 编码路径（如 my-group/my-project）
- title：Issue 标题（创建时必需）
- description：Issue 正文（最多 1,048,576 字符）
- labels：逗号分隔的标签名称（如 bug,critical）
- add_labels / remove_labels：增量添加或移除标签，不替换全部
- state：按 all、opened 或 closed 筛选
- state_event：close 或 reopen 更改 Issue 状态
- assignee_ids：用户 ID 数组；使用 [0] 取消所有指派
- issue_iid：项目内的内部 Issue ID（更新时必需）
- milestone：按里程碑标题筛选
- search：在标题和描述中搜索
- scope：created_by_me、assigned_to_me 或 all
- page / per_page：分页（默认 per_page: 20）

**常见陷阱**：
- id 接受整数项目 ID 或 URL 编码路径；错误的 ID 会导致 4xx 错误
- issue_iid 是项目内部 ID（显示为 #42），与全局 Issue ID 不同
- labels 字段会替换所有现有标签；使用 add_labels/remove_labels 进行增量修改
- 将 assignee_ids 设为空数组不会取消指派；需使用 [0]
- updated_at 字段需要管理员或项目/组所有者权限

### 2. 管理 Merge Request

**何时使用**：用户想要列出、筛选或审查项目中的 Merge Request

**工具调用顺序**：
1. GITLAB_GET_PROJECT - 获取项目详情并验证访问权限 [前置条件]
2. GITLAB_GET_PROJECT_MERGE_REQUESTS - 列出并筛选 Merge Request [必需]
3. GITLAB_GET_REPOSITORY_BRANCHES - 验证源/目标分支 [可选]
4. GITLAB_LIST_ALL_PROJECT_MEMBERS - 查找审查者/指派人 [可选]

**关键参数**：
- id：项目 ID 或 URL 编码路径
- state：opened、closed、locked、merged 或 all
- scope：created_by_me（默认）、assigned_to_me 或 all
- source_branch / target_branch：按分支名筛选
- author_id / author_username：按 MR 作者筛选
- assignee_id：按指派人筛选（使用 None 表示未指派，Any 表示已指派）
- reviewer_id / reviewer_username：按审查者筛选
- labels：逗号分隔的标签筛选
- search：在标题和描述中搜索
- wip：yes 表示草稿 MR，no 表示非草稿
- order_by：created_at（默认）、title、merged_at、updated_at
- view：simple 返回最少字段
- iids[]：按特定 MR 内部 ID 筛选

**常见陷阱**：
- 默认 scope 是 created_by_me，会限制结果；使用 all 获取完整列表
- author_id 和 author_username 互斥
- reviewer_id 和 reviewer_username 互斥
- approved 筛选器需要 mr_approved_filter 功能标志（默认禁用）
- 大型 MR 历史可能很嘈杂；使用筛选器和适度的 per_page 值

### 3. 管理项目和仓库

**何时使用**：用户想要列出项目、创建新项目或管理分支

**工具调用顺序**：
1. GITLAB_GET_PROJECTS - 列出所有可访问的项目并筛选 [必需]
2. GITLAB_GET_PROJECT - 获取特定项目的详细信息 [可选]
3. GITLAB_LIST_USER_PROJECTS - 列出特定用户拥有的项目 [可选]
4. GITLAB_CREATE_PROJECT - 创建新项目 [创建时必需]
5. GITLAB_GET_REPOSITORY_BRANCHES - 列出项目中的分支 [分支操作必需]
6. GITLAB_CREATE_REPOSITORY_BRANCH - 创建新分支 [可选]
7. GITLAB_GET_REPOSITORY_BRANCH - 获取特定分支详情 [可选]
8. GITLAB_LIST_REPOSITORY_COMMITS - 查看提交历史 [可选]
9. GITLAB_GET_PROJECT_LANGUAGES - 获取语言分布 [可选]

**关键参数**：
- name / path：项目名称和 URL 友好路径（创建时两者都必需）
- visibility：private、internal 或 public
- namespace_id：项目放置的组或用户 ID
- search：项目名不区分大小写的子字符串搜索
- membership：true 限制为用户所属项目
- owned：true 限制为用户拥有的项目
- project_id：分支操作的项目 ID
- branch_name：新分支名称
- ref：新分支的源分支或提交 SHA
- order_by：id、name、path、created_at、updated_at、star_count、last_activity_at

**常见陷阱**：
- GITLAB_GET_PROJECTS 需要分页才能完整覆盖；停在第一页会遗漏项目
- 某些响应将项目放在 data.details 下；解析实际返回的列表结构
- 大多数后续调用依赖正确的 project_id；先用 GITLAB_GET_PROJECT 验证
- 无效的 branch_name/ref/sha 会导致客户端错误；先通过 GITLAB_GET_REPOSITORY_BRANCHES 验证分支存在
- GITLAB_CREATE_PROJECT 同时需要 name 和 path

### 4. 监控 CI/CD Pipeline

**何时使用**：用户想要检查 Pipeline 状态、列出 Job 或监控 CI/CD 运行

**工具调用顺序**：
1. GITLAB_GET_PROJECT - 验证项目访问权限 [前置条件]
2. GITLAB_LIST_PROJECT_PIPELINES - 列出 Pipeline 并筛选 [必需]
3. GITLAB_GET_SINGLE_PIPELINE - 获取特定 Pipeline 详情 [可选]
4. GITLAB_LIST_PIPELINE_JOBS - 列出 Pipeline 内的 Job [可选]

**关键参数**：
- id：项目 ID 或 URL 编码路径
- status：按状态筛选 created、waiting_for_resource、preparing、pending、running、success、failed、canceled、skipped、manual、scheduled
- scope：running、pending、finished、branches、tags
- ref：分支或标签名
- sha：特定提交 SHA
- source：Pipeline 来源（使用 parent_pipeline 表示子 Pipeline）
- order_by：id（默认）、status、ref、updated_at、user_id
- created_after / created_before：ISO 8601 日期筛选
- pipeline_id：列出 Job 的特定 Pipeline ID
- include_retried：true 包含重试的 Job（默认 false）

**常见陷阱**：
- 大型 Pipeline 历史可能很嘈杂；使用 status、ref 和日期筛选缩小结果
- 使用适度的 per_page 值保持输出可控
- Pipeline Job scope 接受单个状态字符串或状态数组
- yaml_errors: true 仅返回配置无效的 Pipeline

### 5. 管理用户和成员

**何时使用**：用户想要查找用户、列出项目成员或检查用户状态

**工具调用顺序**：
1. GITLAB_GET_USERS - 搜索并列出 GitLab 用户 [必需]
2. GITLAB_GET_USER - 按 ID 获取特定用户详情 [可选]
3. GITLAB_GET_USERS_ID_STATUS - 获取用户状态消息和可用性 [可选]
4. GITLAB_LIST_ALL_PROJECT_MEMBERS - 列出所有项目成员（直接 + 继承）[列出成员必需]
5. GITLAB_LIST_PROJECT_USERS - 列出项目用户并搜索筛选 [可选]

**关键参数**：
- search：按姓名、用户名或公开邮箱搜索
- username：按用户名获取特定用户
- active / blocked：按用户状态筛选
- id：列出成员的项目 ID
- query：按姓名、邮箱或用户名筛选成员
- state：按 awaiting 或 active 筛选成员（Premium/Ultimate）
- user_ids：按特定用户 ID 筛选

**常见陷阱**：
- 许多用户筛选器（admins、auditors、extern_uid、two_factor）仅限管理员
- GITLAB_LIST_ALL_PROJECT_MEMBERS 包含直接、继承和受邀成员
- 用户搜索不区分大小写，但可能无法匹配部分邮箱域名
- Premium/Ultimate 功能（状态筛选、席位信息）在免费计划中不可用

## 常用模式

### ID 解析
GitLab 对项目使用两种标识符格式：
- 数字 ID：整数项目 ID（如 123）
- URL 编码路径：Namespace/project 格式（如 my-group%2Fmy-project 或 my-group/my-project）
- Issue IID vs ID：issue_iid 是项目内部编号（#42）；全局 id 不同
- User ID：数字；通过 GITLAB_GET_USERS 使用 search 或 username 解析

### 分页
GitLab 使用基于偏移的分页：
- 设置 page（从 1 开始）和 per_page（1-100，默认 20）
- 持续递增 page 直到返回的项目数少于 per_page 或为空
- 总数可能在响应头中可用（X-Total、X-Total-Pages）
- 始终完整分页以获得准确结果

### URL 编码路径
使用项目路径作为标识符时：
- 正斜杠必须 URL 编码：my-group/my-project 变为 my-group%2Fmy-project
- 某些工具接受未编码路径；检查每个工具的 schema
- 可用时优先使用数字 ID 以提高可靠性

## 已知陷阱

### ID 格式
- 项目 id 字段接受整数和字符串（URL 编码路径）
- Issue issue_iid 是项目范围的；不要与全局 Issue ID 混淆
- Pipeline ID 是项目范围的整数
- User ID 是 GitLab 实例范围内的全局整数

### 速率限制
- GitLab 有每用户速率限制（通常 300-2000 请求/分钟，取决于计划）
- 大型 Pipeline/Issue 历史应使用日期和状态筛选减少结果集
- 使用适度的 per_page 值负责任地分页

### 参数特性
- labels 字段替换所有标签；使用 add_labels/remove_labels 进行增量修改
- assignee_ids: [0] 取消所有指派；空数组无效果
- scope 默认值不同：MR 为 created_by_me，Issue 为 all
- MR 筛选中的 author_id 和 author_username 互斥
- 日期参数使用 ISO 8601 格式：2024-01-15T10:30:00Z

### 计划限制
- 某些功能需要 Premium/Ultimate：epic_id、weight、iteration_id、approved_by_ids、成员 state 筛选
- 仅限管理员的功能：用户管理筛选器、updated_at 覆盖、自定义属性
- mr_approved_filter 功能标志默认禁用

## 快速参考

| 任务 | 工具 Slug | 关键参数 |
|------|-----------|----------|
| 列出项目 | GITLAB_GET_PROJECTS | search, membership, visibility |
| 获取项目详情 | GITLAB_GET_PROJECT | id |
| 用户的项目 | GITLAB_LIST_USER_PROJECTS | id, search, owned |
| 创建项目 | GITLAB_CREATE_PROJECT | name, path, visibility |
| 列出 Issue | GITLAB_LIST_PROJECT_ISSUES | id, state, labels, search |
| 创建 Issue | GITLAB_CREATE_PROJECT_ISSUE | id, title, description, labels |
| 更新 Issue | GITLAB_UPDATE_PROJECT_ISSUE | id, issue_iid, state_event |
| 列出 Merge Request | GITLAB_GET_PROJECT_MERGE_REQUESTS | id, state, scope, labels |
| 列出分支 | GITLAB_GET_REPOSITORY_BRANCHES | project_id, search |
| 获取分支 | GITLAB_GET_REPOSITORY_BRANCH | project_id, branch_name |
| 创建分支 | GITLAB_CREATE_REPOSITORY_BRANCH | project_id, branch_name, ref |
| 列出提交 | GITLAB_LIST_REPOSITORY_COMMITS | project ID, branch ref |
| 项目语言 | GITLAB_GET_PROJECT_LANGUAGES | project ID |
| 列出 Pipeline | GITLAB_LIST_PROJECT_PIPELINES | id, status, ref |
| 获取 Pipeline | GITLAB_GET_SINGLE_PIPELINE | project_id, pipeline_id |
| 列出 Pipeline Job | GITLAB_LIST_PIPELINE_JOBS | id, pipeline_id, scope |
| 搜索用户 | GITLAB_GET_USERS | search, username, active |
| 获取用户 | GITLAB_GET_USER | user ID |
| 用户状态 | GITLAB_GET_USERS_ID_STATUS | user ID |
| 列出项目成员 | GITLAB_LIST_ALL_PROJECT_MEMBERS | id, query, state |
| 列出项目用户 | GITLAB_LIST_PROJECT_USERS | id, search |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。