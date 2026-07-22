---
name: circleci-automation
description: "通过 Rube MCP (Composio) 自动化 CircleCI 任务：触发流水线、监控工作流/作业、获取构建产物和测试元数据。当用户要求'触发 CircleCI 流水线'、'监控 CircleCI 工作流'、'获取 CircleCI 构建产物'或'检查 CircleCI 测试结果'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 CircleCI 自动化

通过 Composio 的 CircleCI 工具包和 Rube MCP 自动化 CircleCI CI/CD 操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 与工具包 `circleci` 建立活跃的 CircleCI 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 使用工具包 `circleci` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 CircleCI 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 触发流水线

**何时使用**：用户想要启动新的 CI/CD 流水线运行

**工具调用顺序**：
1. `CIRCLECI_TRIGGER_PIPELINE` - 在项目上触发新流水线 [必需]
2. `CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID` - 监控生成的工作流 [可选]

**关键参数**：
- `project_slug`：项目标识符，格式为 `gh/org/repo` 或 `bb/org/repo`
- `branch`：运行流水线的 Git 分支
- `tag`：运行流水线的 Git 标签（与 branch 互斥）
- `parameters`：流水线参数键值对

**注意事项**：
- `project_slug` 格式为 `{vcs}/{org}/{repo}`（例如 `gh/myorg/myrepo`）
- `branch` 和 `tag` 互斥；同时提供会导致错误
- 流水线参数必须与 `.circleci/config.yml` 中定义的参数匹配
- 触发返回流水线 ID；工作流异步启动

### 2. 监控流水线和工作流

**何时使用**：用户想要检查流水线或工作流的状态

**工具调用顺序**：
1. `CIRCLECI_LIST_PIPELINES_FOR_PROJECT` - 列出项目的最近流水线 [必需]
2. `CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID` - 列出流水线内的工作流 [必需]
3. `CIRCLECI_GET_PIPELINE_CONFIG` - 查看使用的流水线配置 [可选]

**关键参数**：
- `project_slug`：项目标识符，格式为 `{vcs}/{org}/{repo}`
- `pipeline_id`：特定流水线的 UUID
- `branch`：按分支名称筛选流水线
- `page_token`：下一页结果的分页游标

**注意事项**：
- 流水线 ID 是 UUID，不是数字 ID
- 工作流继承流水线 ID；单个流水线可以有多个工作流
- 工作流状态包括：success、running、not_run、failed、error、failing、on_hold、canceled、unauthorized
- `page_token` 在响应中返回用于分页；持续调用直到不存在为止

### 3. 检查作业详情

**何时使用**：用户想要深入查看特定作业的执行详情

**工具调用顺序**：
1. `CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID` - 找到包含该作业的工作流 [前置条件]
2. `CIRCLECI_GET_JOB_DETAILS` - 获取详细作业信息 [必需]

**关键参数**：
- `project_slug`：项目标识符
- `job_number`：数字作业编号（非 UUID）

**注意事项**：
- 作业编号是整数，不是 UUID（与流水线和工作流 ID 不同）
- 作业详情包括执行器类型、并行度、开始/停止时间和状态
- 作业状态：success、running、not_run、failed、retried、timedout、infrastructure_fail、canceled

### 4. 获取构建产物

**何时使用**：用户想要下载或列出生成的产物

**工具调用顺序**：
1. `CIRCLECI_GET_JOB_DETAILS` - 确认作业已成功完成 [前置条件]
2. `CIRCLECI_GET_JOB_ARTIFACTS` - 列出作业的所有产物 [必需]

**关键参数**：
- `project_slug`：项目标识符
- `job_number`：数字作业编号

**注意事项**：
- 产物仅在作业完成后可用
- 每个产物都有用于下载的 `path` 和 `url`
- 产物 URL 可能需要认证头才能下载
- 大型产物可能有下载大小限制

### 5. 查看测试结果

**何时使用**：用户想要检查特定作业的测试结果

**工具调用顺序**：
1. `CIRCLECI_GET_JOB_DETAILS` - 验证作业运行了测试 [前置条件]
2. `CIRCLECI_GET_TEST_METADATA` - 获取测试结果和元数据 [必需]

**关键参数**：
- `project_slug`：项目标识符
- `job_number`：数字作业编号

**注意事项**：
- 测试元数据要求作业已上传测试结果（JUnit XML 格式）
- 如果未上传测试结果，响应将为空
- 测试元数据包括 classname、name、result、message 和 run_time 字段
- 失败的测试在 `message` 字段中包含失败消息

## 常见模式

### 项目 Slug 格式

```
格式: {vcs_type}/{org_name}/{repo_name}
- GitHub:    gh/myorg/myrepo
- Bitbucket: bb/myorg/myrepo
```

### 流水线 -> 工作流 -> 作业层级

```
1. 调用 CIRCLECI_LIST_PIPELINES_FOR_PROJECT 获取流水线 ID
2. 使用 pipeline_id 调用 CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID
3. 从工作流详情中提取作业编号
4. 使用 job_number 调用 CIRCLECI_GET_JOB_DETAILS
```

### 分页

- 检查响应中的 `next_page_token` 字段
- 在下一个请求中将 token 作为 `page_token` 传递
- 持续调用直到 `next_page_token` 不存在或为 null

## 已知注意事项

**ID 格式**：
- 流水线 ID：UUID（例如 `5034460f-c7c4-4c43-9457-de07e2029e7b`）
- 工作流 ID：UUID
- 作业编号：整数（例如 `123`）
- 不要在不同端点之间混淆 UUID 和整数

**项目 Slug**：
- 必须包含 VCS 前缀：`gh/` 表示 GitHub，`bb/` 表示 Bitbucket
- 组织和仓库名称区分大小写
- 错误的 slug 格式会导致 404 错误

**速率限制**：
- CircleCI API 有每个端点的速率限制
- 在收到 429 响应时实现指数退避
- 避免快速轮询；使用合理的间隔（5-10 秒）

## 快速参考

| 任务 | 工具 Slug | 关键参数 |
|------|-----------|----------|
| 触发流水线 | CIRCLECI_TRIGGER_PIPELINE | project_slug, branch, parameters |
| 列出流水线 | CIRCLECI_LIST_PIPELINES_FOR_PROJECT | project_slug, branch |
| 列出工作流 | CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID | pipeline_id |
| 获取流水线配置 | CIRCLECI_GET_PIPELINE_CONFIG | pipeline_id |
| 获取作业详情 | CIRCLECI_GET_JOB_DETAILS | project_slug, job_number |
| 获取作业产物 | CIRCLECI_GET_JOB_ARTIFACTS | project_slug, job_number |
| 获取测试元数据 | CIRCLECI_GET_TEST_METADATA | project_slug, job_number |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
