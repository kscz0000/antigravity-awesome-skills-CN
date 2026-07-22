---
name: jobgpt
description: "使用 JobGPT MCP 服务器进行求职自动化、自动投递、简历生成、申请追踪、薪资情报和招聘人员外联。触发词：求职自动化、自动投递、简历生成、申请追踪、薪资情报、招聘人员外联、job search、auto apply、resume generation、application tracking、salary intelligence、recruiter outreach。"
risk: safe
source: community
date_added: "2026-03-23"
---

# JobGPT - 求职自动化

## 概述

JobGPT 通过 JobGPT MCP 服务器将你的 AI 助手连接到完整的求职自动化平台。它提供 34 个工具，涵盖职位搜索、自动投递、简历生成、申请追踪、薪资情报和招聘人员外联，让你可以在 AI 编码助手中管理整个求职过程。

由 [6figr.com](https://6figr.com/jobgpt-ai) 构建，该平台支持 150+ 个国家的薪资数据、职位匹配和自动投递。

## 何时使用此技能

- 你想要**搜索职位**，支持职位名称、地点、薪资、远程和 H1B 签证等筛选条件
- 你想要**自动投递**到职位
- 你想要为特定职位申请**生成定制简历**
- 你想要**追踪你的职位申请**，跨多个求职过程
- 你想要**寻找招聘人员或推荐人**，并向目标公司发送外联邮件
- 你想要从 LinkedIn、Greenhouse、Lever、Workday 或任何招聘网站 URL **导入职位**
- 你想要**查询薪资**并比较不同职位的薪酬

## 设置

此技能需要 JobGPT MCP 服务器：

1. **创建账户** - 在 [6figr.com/jobgpt-ai](https://6figr.com/jobgpt-ai) 注册
2. **获取 API 密钥** - 前往 [6figr.com/account](https://6figr.com/account)，滚动到 MCP Integrations，点击 Generate API Key。密钥以 `mcp_` 开头。
3. **添加 MCP 服务器：**
   - Claude Code: `claude mcp add jobgpt -t http -u https://mcp.6figr.com/mcp --header "Authorization: <api-key>"`
   - 其他工具：将 `jobgpt-mcp-server` 添加为 MCP 服务器，并设置环境变量 `JOBGPT_API_KEY`。通过 `npx jobgpt-mcp-server` 安装。

运行本地 `npx jobgpt-mcp-server` 路径时，请设置 `JOBGPT_API_KEY` 环境变量。

## 示例

### 查找远程职位

> "Find remote senior React jobs paying over $150k"

该技能使用 `search_jobs` 配合职位名称、远程和薪资筛选条件查找匹配职位，然后展示结果，包含公司、职位名称、地点、薪资范围和关键技能。

### 自动投递职位

> "Auto-apply to the top 5 matches from my job hunt"

该技能检查你的简历是否已上传，使用 `match_jobs` 查找新匹配，用 `add_job_to_applications` 保存选中的匹配，然后为每个申请触发 `apply_to_job`。它通过 `get_application_stats` 监控进度。

### 生成定制简历

> "Generate a tailored resume for this Google application"

该技能调用 `generate_resume_for_job` 为特定职位要求创建 AI 优化的简历，然后通过 `get_generated_resume` 提供下载链接。

### 从 URL 导入并投递

> "Apply to this job for me - https://boards.greenhouse.io/company/jobs/12345"

该技能使用 `import_job_by_url` 从支持的平台（LinkedIn、Greenhouse、Lever、Workday）导入职位，添加到申请列表，并可选择触发自动投递。

### 招聘人员外联

> "Find recruiters for this job and draft an outreach email"

该技能使用 `get_job_recruiters` 查找招聘人员并帮助撰写个性化消息。草稿展示给用户审核；只有在用户明确确认后才调用 `send_outreach`。

### 查看申请统计

> "Show my application stats for the last 7 days"

该技能使用 `get_application_stats` 获取聚合概览——按状态分类的总数、自动投递指标和管道进度。

## 最佳实践

- **先检查积分** - 自动投递和简历生成消耗积分。批量操作前使用 `get_credits`。
- **完善个人资料** - 首先运行 `get_profile`，用 `update_profile` 填补缺失字段以获得更好的职位匹配。
- **投递前上传简历** - 使用 `list_resumes` 检查，如需要则使用 `upload_resume`。
- **为持续搜索使用求职任务** - 用 `create_job_hunt` 创建求职任务以保存筛选条件并获得持续匹配。
- **对已保存职位使用 `get_application`** - 如果用户询问他们已保存的职位，使用 `get_application` 而非 `get_job`。

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| "Missing Authorization header" | 对于 Claude Code 和其他远程 HTTP MCP 设置，确认 MCP 服务器条目上配置了 `Authorization` 头 |
| "Missing API key" | 对于本地 `npx jobgpt-mcp-server` 设置，确保 `JOBGPT_API_KEY` 设置为你的 API 密钥 |
| "Insufficient credits" | 使用 `get_credits` 检查余额。在 6figr.com/account 购买更多 |
| 自动投递不工作 | 确保已上传简历且求职任务已启用自动投递 |
| 找不到职位匹配 | 放宽搜索筛选条件（更少职位名称、更多地点、更宽薪资范围） |

## 其他资源

- [JobGPT 平台](https://6figr.com/jobgpt-ai) - 注册和管理账户
- [MCP 服务器仓库](https://github.com/6figr-com/jobgpt-mcp-server) - 源代码和设置指南
- [技能仓库](https://github.com/6figr-com/skills) - 此技能的源码
- [npm 包](https://www.npmjs.com/package/jobgpt-mcp-server) - 通过 npm 安装

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
