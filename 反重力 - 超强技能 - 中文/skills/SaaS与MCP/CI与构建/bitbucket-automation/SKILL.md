---
name: bitbucket-automation
description: "通过 Rube MCP (Composio) 自动化 Bitbucket 仓库、Pull Request、分支、Issue 和工作空间管理。务必先搜索工具以获取当前 schema。当用户要求'管理Bitbucket'、'操作Bitbucket仓库'、'创建PR'、'管理分支'、'跟踪Issue'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Bitbucket

通过 Composio 的 Bitbucket 工具包自动化 Bitbucket 操作，包括仓库管理、Pull Request 工作流、分支操作、Issue 跟踪和工作空间管理。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立 Bitbucket 连接，toolkit 设为 `bitbucket`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：将 `https://rube.app/mcp` 添加为客户端配置中的 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 可响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `bitbucket`
3. 若连接状态非 ACTIVE，按返回的认证链接完成 Bitbucket OAuth
4. 确认连接状态为 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 管理 Pull Request

**适用场景**：用户需要创建、审查或查看 Pull Request

**工具调用顺序**：
1. `BITBUCKET_LIST_WORKSPACES` - 发现可访问的工作空间 [前置]
2. `BITBUCKET_LIST_REPOSITORIES_IN_WORKSPACE` - 查找目标仓库 [前置]
3. `BITBUCKET_LIST_BRANCHES` - 验证源分支和目标分支存在 [前置]
4. `BITBUCKET_CREATE_PULL_REQUEST` - 创建新 PR，指定标题、源分支和可选审查人 [必需]
5. `BITBUCKET_LIST_PULL_REQUESTS` - 按状态筛选 PR（OPEN、MERGED、DECLINED） [可选]
6. `BITBUCKET_GET_PULL_REQUEST` - 按 ID 获取特定 PR 的完整详情 [可选]
7. `BITBUCKET_GET_PULL_REQUEST_DIFF` - 获取统一 diff 用于代码审查 [可选]
8. `BITBUCKET_GET_PULL_REQUEST_DIFFSTAT` - 获取变更文件及增删行数 [可选]

**关键参数**：
- `workspace`：工作空间 slug 或 UUID（所有操作必需）
- `repo_slug`：URL 友好的仓库名称
- `source_branch`：包含待合并变更的分支
- `destination_branch`：目标分支（省略时默认为仓库主分支）
- `reviewers`：包含 `uuid` 字段的对象数组，用于指定审查人
- `state`：LIST_PULL_REQUESTS 的筛选条件 - `OPEN`、`MERGED` 或 `DECLINED`
- `max_chars`：GET_PULL_REQUEST_DIFF 的截断上限，用于处理大型 diff

**注意事项**：
- `reviewers` 期望的是包含 `uuid` 键的对象数组，而非用户名：`[{"uuid": "{...}"}]`
- UUID 格式必须包含花括号：`{123e4567-e89b-12d3-a456-426614174000}`
- `destination_branch` 省略时默认为仓库主分支，不一定是 `main`
- `pull_request_id` 在 GET/DIFF 操作中为整数，但在 PR 列表中返回时类型不同
- 大型 diff 可能超出上下文限制；GET_PULL_REQUEST_DIFF 务必设置 `max_chars`（如 50000）

### 2. 管理仓库和工作空间

**适用场景**：用户需要列出、创建或删除仓库，或浏览工作空间

**工具调用顺序**：
1. `BITBUCKET_LIST_WORKSPACES` - 列出所有可访问的工作空间 [必需]
2. `BITBUCKET_LIST_REPOSITORIES_IN_WORKSPACE` - 列出仓库，支持 BBQL 筛选 [必需]
3. `BITBUCKET_CREATE_REPOSITORY` - 创建新仓库，设置语言、可见性和项目 [可选]
4. `BITBUCKET_DELETE_REPOSITORY` - 永久删除仓库（不可逆） [可选]
5. `BITBUCKET_LIST_WORKSPACE_MEMBERS` - 列出成员，用于分配审查人或检查权限 [可选]

**关键参数**：
- `workspace`：工作空间 slug（通过 LIST_WORKSPACES 获取）
- `repo_slug`：用于创建/删除的 URL 友好名称
- `q`：BBQL 查询筛选（如 `name~"api"`、`project.key="PROJ"`、`is_private=true`）
- `role`：按用户角色筛选仓库：`member`、`contributor`、`admin`、`owner`
- `sort`：排序字段，`-` 前缀表示降序（如 `-updated_on`）
- `is_private`：仓库可见性布尔值（默认 `true`）
- `project_key`：Bitbucket 项目 key；省略则使用工作空间最早的项目

**注意事项**：
- `BITBUCKET_DELETE_REPOSITORY` **不可逆**，且不影响 fork
- BBQL 字符串值必须用双引号包裹：`name~"my-repo"` 而非 `name~my-repo`
- `repository` 不是有效的 BBQL 字段；应使用 `name`
- 默认分页为 10 条结果；完整列表需显式设置 `pagelen`
- `CREATE_REPOSITORY` 默认为私有仓库；公开仓库需设置 `is_private: false`

### 3. 管理 Issue

**适用场景**：用户需要创建、更新、列出或评论仓库 Issue

**工具调用顺序**：
1. `BITBUCKET_LIST_ISSUES` - 列出 Issue，支持按状态、优先级、类型、指派人筛选 [必需]
2. `BITBUCKET_CREATE_ISSUE` - 创建新 Issue，指定标题、内容、优先级和类型 [必需]
3. `BITBUCKET_UPDATE_ISSUE` - 修改 Issue 属性（状态、优先级、指派人等） [可选]
4. `BITBUCKET_CREATE_ISSUE_COMMENT` - 为已有 Issue 添加 Markdown 评论 [可选]
5. `BITBUCKET_DELETE_ISSUE` - 永久删除 Issue [可选]

**关键参数**：
- `issue_id`：Issue 的字符串标识符
- `title`、`content`：创建时必需
- `kind`：`bug`、`enhancement`、`proposal` 或 `task`
- `priority`：`trivial`、`minor`、`major`、`critical` 或 `blocker`
- `state`：`new`、`open`、`resolved`、`on hold`、`invalid`、`duplicate`、`wontfix`、`closed`
- `assignee`：CREATE 时为 Bitbucket 用户名；UPDATE 时为 `assignee_account_id`（UUID）
- `due_on`：ISO 8601 格式日期字符串

**注意事项**：
- 仓库必须启用 Issue 跟踪（`has_issues: true`），否则 API 调用会失败
- `CREATE_ISSUE` 使用 `assignee`（用户名字符串），而 `UPDATE_ISSUE` 使用 `assignee_account_id`（UUID）——两者是不同字段
- `DELETE_ISSUE` 不可逆，无法恢复
- `state` 值包含空格：`"on hold"` 而非 `"on_hold"`
- LIST_ISSUES 中按 `assignee` 筛选使用账户 ID 而非用户名；未指派使用 `"null"` 字符串

### 4. 管理分支

**适用场景**：用户需要创建分支或浏览分支结构

**工具调用顺序**：
1. `BITBUCKET_LIST_BRANCHES` - 列出分支，支持 BBQL 筛选和排序 [必需]
2. `BITBUCKET_CREATE_BRANCH` - 从指定 commit hash 创建新分支 [必需]

**关键参数**：
- `name`：分支名称，不含 `refs/heads/` 前缀（如 `feature/new-login`）
- `target_hash`：完整的 SHA1 commit hash，作为分支起点（必须存在于仓库中）
- `q`：BBQL 筛选（如 `name~"feature/"`、`name="main"`）
- `sort`：按 `name` 或 `-target.date`（按提交日期降序）排序
- `pagelen`：每页 1-100 条结果（默认 10）

**注意事项**：
- `CREATE_BRANCH` 需要完整 commit hash 作为 `target_hash`，不接受分支名
- 分支名称不要包含 `refs/heads/` 前缀
- 分支名称须遵循 Bitbucket 命名规范（字母数字、`/`、`.`、`_`、`-`）
- BBQL 字符串值需要双引号：`name~"feature/"` 而非 `name~feature/`

### 5. 审查 Pull Request 并添加评论

**适用场景**：用户需要为 Pull Request 添加审查评论，包括行内代码评论

**工具调用顺序**：
1. `BITBUCKET_GET_PULL_REQUEST` - 获取 PR 详情并确认其存在 [前置]
2. `BITBUCKET_GET_PULL_REQUEST_DIFF` - 审查实际代码变更 [前置]
3. `BITBUCKET_GET_PULL_REQUEST_DIFFSTAT` - 获取变更文件列表 [可选]
4. `BITBUCKET_CREATE_PULL_REQUEST_COMMENT` - 发布审查评论 [必需]

**关键参数**：
- `pull_request_id`：PR 的字符串 ID
- `content_raw`：Markdown 格式的评论文本
- `content_markup`：默认为 `markdown`；也支持 `plaintext`
- `inline`：包含 `path`、`from`、`to` 的对象，用于行内代码评论
- `parent_comment_id`：整数 ID，用于回复已有评论（嵌套回复）

**注意事项**：
- `pull_request_id` 在 CREATE_PULL_REQUEST_COMMENT 中为字符串，在 GET_PULL_REQUEST 中为整数
- 行内评论至少需要 `inline.path`；`from`/`to` 为可选行号
- `parent_comment_id` 创建嵌套回复；省略则为顶级评论
- 行内评论的行号引用的是 diff，而非源文件

## 常用模式

### ID 解析
操作前始终将可读名称解析为 ID：
- **工作空间**：`BITBUCKET_LIST_WORKSPACES` 获取 workspace slug
- **仓库**：`BITBUCKET_LIST_REPOSITORIES_IN_WORKSPACE` 配合 `q` 筛选查找 repo slug
- **分支**：`BITBUCKET_LIST_BRANCHES` 在创建 PR 前验证分支存在
- **成员**：`BITBUCKET_LIST_WORKSPACE_MEMBERS` 获取 UUID 用于分配审查人

### 分页
Bitbucket 使用基于页码的分页（非游标分页）：
- 使用 `page`（从 1 开始）和 `pagelen`（每页条数）参数
- 默认每页通常为 10 条；显式设置 `pagelen`（PR 最多 50，其他最多 100）
- 检查响应中的 `next` URL 或总数判断是否有更多页
- 完整结果务必遍历所有页

### BBQL 筛选
Bitbucket 查询语言可用于列表接口：
- 字符串值必须用双引号：`name~"pattern"`
- 运算符：`=`（精确）、`~`（包含）、`!=`（不等于）、`>`、`>=`、`<`、`<=`
- 用 `AND` / `OR` 组合：`name~"api" AND is_private=true`

## 已知注意事项

### ID 格式
- 工作空间：slug 字符串（如 `my-workspace`）或带花括号的 UUID（`{uuid}`）
- 审查人 UUID 必须包含花括号：`{123e4567-e89b-12d3-a456-426614174000}`
- Issue ID 为字符串；PR ID 在某些工具中为整数，在其他工具中为字符串
- Commit hash 必须为完整 SHA1（40 个字符）

### 参数差异
- `assignee` 与 `assignee_account_id`：CREATE_ISSUE 使用用户名，UPDATE_ISSUE 使用 UUID
- Issue 的 `state` 值包含空格：`"on hold"` 而非 `"on_hold"`
- `destination_branch` 省略时默认为仓库主分支，不一定是字面值 `main`
- BBQL 中 `repository` 不是有效字段——应使用 `name`

### 速率限制
- Bitbucket Cloud API 有速率限制；大批量操作应加入延迟
- 分页请求计入速率限制；尽量减少不必要的页面请求

### 破坏性操作
- `BITBUCKET_DELETE_REPOSITORY` 不可逆，且不会删除 fork
- `BITBUCKET_DELETE_ISSUE` 永久删除，无法恢复
- 执行删除操作前务必与用户确认

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出工作空间 | `BITBUCKET_LIST_WORKSPACES` | `q`, `sort` |
| 列出仓库 | `BITBUCKET_LIST_REPOSITORIES_IN_WORKSPACE` | `workspace`, `q`, `role` |
| 创建仓库 | `BITBUCKET_CREATE_REPOSITORY` | `workspace`, `repo_slug`, `is_private` |
| 删除仓库 | `BITBUCKET_DELETE_REPOSITORY` | `workspace`, `repo_slug` |
| 列出分支 | `BITBUCKET_LIST_BRANCHES` | `workspace`, `repo_slug`, `q` |
| 创建分支 | `BITBUCKET_CREATE_BRANCH` | `workspace`, `repo_slug`, `name`, `target_hash` |
| 列出 PR | `BITBUCKET_LIST_PULL_REQUESTS` | `workspace`, `repo_slug`, `state` |
| 创建 PR | `BITBUCKET_CREATE_PULL_REQUEST` | `workspace`, `repo_slug`, `title`, `source_branch` |
| 获取 PR 详情 | `BITBUCKET_GET_PULL_REQUEST` | `workspace`, `repo_slug`, `pull_request_id` |
| 获取 PR diff | `BITBUCKET_GET_PULL_REQUEST_DIFF` | `workspace`, `repo_slug`, `pull_request_id`, `max_chars` |
| 获取 PR diffstat | `BITBUCKET_GET_PULL_REQUEST_DIFFSTAT` | `workspace`, `repo_slug`, `pull_request_id` |
| 评论 PR | `BITBUCKET_CREATE_PULL_REQUEST_COMMENT` | `workspace`, `repo_slug`, `pull_request_id`, `content_raw` |
| 列出 Issue | `BITBUCKET_LIST_ISSUES` | `workspace`, `repo_slug`, `state`, `priority` |
| 创建 Issue | `BITBUCKET_CREATE_ISSUE` | `workspace`, `repo_slug`, `title`, `content` |
| 更新 Issue | `BITBUCKET_UPDATE_ISSUE` | `workspace`, `repo_slug`, `issue_id` |
| 评论 Issue | `BITBUCKET_CREATE_ISSUE_COMMENT` | `workspace`, `repo_slug`, `issue_id`, `content` |
| 删除 Issue | `BITBUCKET_DELETE_ISSUE` | `workspace`, `repo_slug`, `issue_id` |
| 列出成员 | `BITBUCKET_LIST_WORKSPACE_MEMBERS` | `workspace` |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 若缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
