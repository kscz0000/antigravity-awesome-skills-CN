---
name: github-automation
description: "通过 Rube MCP (Composio) 自动化 GitHub 仓库、Issue、Pull Request、分支、CI/CD 和权限管理。管理代码工作流、审查 PR、搜索代码及处理部署。触发词：GitHub自动化、仓库管理、Issue管理、PR管理、CI/CD、分支管理、GitHub权限"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 GitHub 自动化

通过 Composio 的 GitHub 工具包，自动化 GitHub 仓库管理、Issue 跟踪、Pull Request 工作流、分支操作和 CI/CD。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 GitHub 连接，工具包为 `github`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包为 `github`
3. 如果连接状态不是 ACTIVE，按照返回的授权链接完成 GitHub OAuth
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和管理 Issue

**适用场景**：用户想要创建、列出或管理 GitHub Issue

**工具调用顺序**：
1. `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` - 未知时查找目标仓库 [前提条件]
2. `GITHUB_LIST_REPOSITORY_ISSUES` - 列出现有 Issue（包含 PR）[必需]
3. `GITHUB_CREATE_AN_ISSUE` - 创建新 Issue [必需]
4. `GITHUB_CREATE_AN_ISSUE_COMMENT` - 为 Issue 添加评论 [可选]
5. `GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS` - 按关键词跨仓库搜索 [可选]

**关键参数**：
- `owner`：仓库所有者（用户名或组织），不区分大小写
- `repo`：仓库名称，不含 .git 扩展名
- `title`：Issue 标题（创建时必需）
- `body`：Issue 描述（支持 Markdown）
- `labels`：标签名称数组
- `assignees`：GitHub 用户名数组
- `state`：筛选条件，可选 'open'、'closed' 或 'all'

**注意事项**：
- `GITHUB_LIST_REPOSITORY_ISSUES` 同时返回 Issue 和 Pull Request；通过 `pull_request` 字段区分
- 只有拥有推送权限的用户才能设置指派人、标签和里程碑；否则会被静默忽略
- 分页：`per_page` 最大 100；需迭代页面直到为空

### 2. 管理 Pull Request

**适用场景**：用户想要创建、审查或合并 Pull Request

**工具调用顺序**：
1. `GITHUB_FIND_PULL_REQUESTS` - 搜索和筛选 PR [必需]
2. `GITHUB_GET_A_PULL_REQUEST` - 获取 PR 详细信息，包括可合并状态 [必需]
3. `GITHUB_LIST_PULL_REQUESTS_FILES` - 查看变更文件 [可选]
4. `GITHUB_CREATE_A_PULL_REQUEST` - 创建新 PR [必需]
5. `GITHUB_CREATE_AN_ISSUE_COMMENT` - 发布审查评论 [可选]
6. `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` - 合并前验证 CI 状态 [可选]
7. `GITHUB_MERGE_A_PULL_REQUEST` - 经用户明确批准后合并 [必需]

**关键参数**：
- `head`：包含变更的源分支（必须存在；跨仓库格式：'username:branch'）
- `base`：合并的目标分支（如 'main'）
- `title`：PR 标题（除非提供了 `issue` 编号，否则必需）
- `merge_method`：'merge'、'squash' 或 'rebase'
- `state`：'open'、'closed' 或 'all'

**注意事项**：
- `GITHUB_CREATE_A_PULL_REQUEST` 在 base/head 无效、相同或已合并时返回 422 错误
- `GITHUB_MERGE_A_PULL_REQUEST` 在 PR 为草稿、已关闭或受分支保护规则限制时可能被拒绝
- 合并前务必通过 `GITHUB_GET_A_PULL_REQUEST` 验证可合并状态
- 调用 MERGE 前必须获得用户明确确认

### 3. 管理仓库和分支

**适用场景**：用户想要创建仓库、管理分支或更新仓库设置

**工具调用顺序**：
1. `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` - 列出用户仓库 [必需]
2. `GITHUB_GET_A_REPOSITORY` - 获取仓库详细信息 [可选]
3. `GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER` - 创建个人仓库 [必需]
4. `GITHUB_CREATE_AN_ORGANIZATION_REPOSITORY` - 创建组织仓库 [替代方案]
5. `GITHUB_LIST_BRANCHES` - 列出分支 [必需]
6. `GITHUB_CREATE_A_REFERENCE` - 从 SHA 创建新分支 [必需]
7. `GITHUB_UPDATE_A_REPOSITORY` - 更新仓库设置 [可选]

**关键参数**：
- `name`：仓库名称
- `private`：布尔值，控制可见性
- `ref`：完整引用路径（如 'refs/heads/new-branch'）
- `sha`：新引用指向的提交 SHA
- `default_branch`：默认分支名称

**注意事项**：
- `GITHUB_CREATE_A_REFERENCE` 只能创建新引用；更新已有引用需使用 `GITHUB_UPDATE_A_REFERENCE`
- `ref` 必须以 'refs/' 开头且包含至少两个斜杠
- `GITHUB_LIST_BRANCHES` 通过 `page`/`per_page` 分页；迭代直到空页
- `GITHUB_DELETE_A_REPOSITORY` 是永久性操作，不可撤销；需要管理员权限

### 4. 搜索代码和提交

**适用场景**：用户想要跨仓库查找代码、文件或提交

**工具调用顺序**：
1. `GITHUB_SEARCH_CODE` - 搜索文件内容和路径 [必需]
2. `GITHUB_SEARCH_CODE_ALL_PAGES` - 多页代码搜索 [替代方案]
3. `GITHUB_SEARCH_COMMITS_BY_AUTHOR` - 按作者/日期/组织搜索提交 [必需]
4. `GITHUB_LIST_COMMITS` - 列出特定仓库的提交 [替代方案]
5. `GITHUB_GET_A_COMMIT` - 获取提交详细信息 [可选]
6. `GITHUB_GET_REPOSITORY_CONTENT` - 获取文件内容 [可选]

**关键参数**：
- `q`：带限定符的搜索查询（`language:python`、`repo:owner/repo`、`extension:js`）
- `owner`/`repo`：用于特定仓库的提交列表
- `author`：按提交作者筛选
- `since`/`until`：ISO 8601 日期范围

**注意事项**：
- 代码搜索仅索引默认分支上小于 384KB 的文件
- 代码搜索最多返回 1000 条结果
- `GITHUB_SEARCH_COMMITS_BY_AUTHOR` 除限定符外还需要关键词；不允许仅使用限定符的查询
- `GITHUB_LIST_COMMITS` 对空仓库返回 409

### 5. 管理 CI/CD 和部署

**适用场景**：用户想要查看工作流、检查 CI 状态或管理部署

**工具调用顺序**：
1. `GITHUB_LIST_REPOSITORY_WORKFLOWS` - 列出 GitHub Actions 工作流 [必需]
2. `GITHUB_GET_A_WORKFLOW` - 按 ID 或文件名获取工作流详情 [可选]
3. `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT` - 手动触发工作流 [必需]
4. `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` - 检查提交/分支的 CI 状态 [必需]
5. `GITHUB_LIST_DEPLOYMENTS` - 列出部署 [可选]
6. `GITHUB_GET_A_DEPLOYMENT_STATUS` - 获取部署状态 [可选]

**关键参数**：
- `workflow_id`：数字 ID 或文件名（如 'ci.yml'）
- `ref`：工作流触发的 Git 引用（分支/标签）
- `inputs`：匹配 `on.workflow_dispatch.inputs` 的工作流输入，JSON 字符串
- `environment`：按环境名称筛选部署

**注意事项**：
- `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT` 要求工作流配置了 `workflow_dispatch` 触发器
- 完整路径 `.github/workflows/main.yml` 会自动截断为 `main.yml`
- 输入最多 10 个键值对；必须匹配工作流的 `on.workflow_dispatch.inputs` 定义

### 6. 管理用户和权限

**适用场景**：用户想要检查协作者、权限或分支保护规则

**工具调用顺序**：
1. `GITHUB_LIST_REPOSITORY_COLLABORATORS` - 列出仓库协作者 [必需]
2. `GITHUB_GET_REPOSITORY_PERMISSIONS_FOR_A_USER` - 检查特定用户的权限 [可选]
3. `GITHUB_GET_BRANCH_PROTECTION` - 查看分支保护规则 [必需]
4. `GITHUB_UPDATE_BRANCH_PROTECTION` - 更新保护设置 [可选]
5. `GITHUB_ADD_A_REPOSITORY_COLLABORATOR` - 添加/更新协作者 [可选]

**关键参数**：
- `affiliation`：协作者筛选，可选 'outside'、'direct' 或 'all'
- `permission`：按权限筛选，可选 'pull'、'triage'、'push'、'maintain'、'admin'
- `branch`：分支保护规则对应的分支名称
- `enforce_admins`：保护规则是否适用于管理员

**注意事项**：
- `GITHUB_GET_BRANCH_PROTECTION` 对未保护的分支返回 404；应视为无保护规则
- 通过 `permissions.push` 或 `role_name` 判断推送权限，而非显示标签
- `GITHUB_LIST_REPOSITORY_COLLABORATORS` 需分页；需迭代所有页面
- `GITHUB_GET_REPOSITORY_PERMISSIONS_FOR_A_USER` 对非协作者可能无法得出明确结论

## 常用模式

### ID 解析
- **仓库名 -> owner/repo**：`GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`
- **PR 编号 -> PR 详情**：`GITHUB_FIND_PULL_REQUESTS` 然后 `GITHUB_GET_A_PULL_REQUEST`
- **分支名 -> SHA**：`GITHUB_GET_A_BRANCH`
- **工作流名称 -> ID**：`GITHUB_LIST_REPOSITORY_WORKFLOWS`

### 分页
所有列表端点使用基于页码的分页：
- `page`：页码（从 1 开始）
- `per_page`：每页结果数（最大 100）
- 迭代直到返回结果数少于 `per_page`

### 安全
- 合并前务必验证 PR 的可合并状态
- 破坏性操作（合并、删除）必须获得用户明确确认
- 合并前通过 `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` 检查 CI 状态

## 已知注意事项

- **Issue 与 PR 混合**：`GITHUB_LIST_REPOSITORY_ISSUES` 同时返回两者；检查 `pull_request` 字段区分
- **分页限制**：`per_page` 最大 100；始终迭代页面直到为空
- **分支创建**：引用已存在时 `GITHUB_CREATE_A_REFERENCE` 返回 422 错误
- **合并守卫**：合并可能因分支保护、检查失败或草稿状态而失败
- **代码搜索限制**：仅索引默认分支上 <384KB 的文件；最多 1000 条结果
- **提交搜索**：限定符之外还需要搜索文本关键词
- **破坏性操作**：仓库删除不可撤销；合并无法撤回
- **权限静默丢失**：无推送权限时，标签、指派人、里程碑会被静默忽略

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出仓库 | `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` | `type`, `sort`, `per_page` |
| 获取仓库 | `GITHUB_GET_A_REPOSITORY` | `owner`, `repo` |
| 创建 Issue | `GITHUB_CREATE_AN_ISSUE` | `owner`, `repo`, `title`, `body` |
| 列出 Issue | `GITHUB_LIST_REPOSITORY_ISSUES` | `owner`, `repo`, `state` |
| 查找 PR | `GITHUB_FIND_PULL_REQUESTS` | `repo`, `state`, `author` |
| 创建 PR | `GITHUB_CREATE_A_PULL_REQUEST` | `owner`, `repo`, `head`, `base`, `title` |
| 合并 PR | `GITHUB_MERGE_A_PULL_REQUEST` | `owner`, `repo`, `pull_number`, `merge_method` |
| 列出分支 | `GITHUB_LIST_BRANCHES` | `owner`, `repo` |
| 创建分支 | `GITHUB_CREATE_A_REFERENCE` | `owner`, `repo`, `ref`, `sha` |
| 搜索代码 | `GITHUB_SEARCH_CODE` | `q` |
| 列出提交 | `GITHUB_LIST_COMMITS` | `owner`, `repo`, `author`, `since` |
| 搜索提交 | `GITHUB_SEARCH_COMMITS_BY_AUTHOR` | `q` |
| 列出工作流 | `GITHUB_LIST_REPOSITORY_WORKFLOWS` | `owner`, `repo` |
| 触发工作流 | `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT` | `owner`, `repo`, `workflow_id`, `ref` |
| 检查 CI | `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` | `owner`, `repo`, ref |
| 列出协作者 | `GITHUB_LIST_REPOSITORY_COLLABORATORS` | `owner`, `repo` |
| 分支保护 | `GITHUB_GET_BRANCH_PROTECTION` | `owner`, `repo`, `branch` |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
