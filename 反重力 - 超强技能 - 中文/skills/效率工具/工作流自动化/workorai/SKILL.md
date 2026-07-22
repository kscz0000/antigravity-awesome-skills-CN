---
name: workorai
description: "WorkorAI 人才市场技能：求职者可搜索职位并管理应聘，雇主可运行职位全生命周期并获得带白盒匹配说明的候选人排名。"
category: productivity
risk: critical
source: community
source_repo: work0r-ai/agent-kit
source_type: community
date_added: "2026-07-03"
author: work0r-ai
tags: [job-search, hiring, recruiting, talent-marketplace, mcp]
tools: [claude, cursor, gemini]
license: "MIT"
license_source: "https://github.com/work0r-ai/agent-kit/blob/main/skills/workorai/LICENSE.txt"
---

# WorkorAI

## 概述

WorkorAI 是一个面向智能体开放的人才市场，通过 MCP 服务器提供能力
（streamable HTTP，地址 https://workorai.com/mcp，在官方 MCP 注册表中
登记为 `io.github.work0r-ai/workorai`）。本技能按意图在双角色工具面之间
路由请求：9 个 `candidate.*` 工具（职位搜索、职位详情、应聘、申请、邀请、
收藏职位）和 `employer.*` 工具（职位全生命周期、候选人发现、邀请、
应聘者审核）。雇主的候选人发现功能返回分层排名（最佳/良好/较弱），
并为每位候选人附带白盒匹配说明——契合度分数、面试中已验证的技能、
差距项以及可引用的理由——而非黑盒分数。

## 适用场景

- 用户希望找工作、搜索职位空缺、申请某个岗位或跟踪自己的应聘进度
  （如"帮我找工作"、"ищу работу"）时使用。
- 雇主希望在 WorkorAI 上发布、出版、更新、关闭或归档职位时使用。
- 雇主希望查找、排名、比较或评估候选人，或询问某位候选人为何匹配
  某个角色时使用。
- 用户需要搭建或排查 WorkorAI MCP 连接及 API 密钥接入流程时使用。

## 工作方式

### 步骤一：连接 MCP 服务器

将 WorkorAI MCP 服务器添加到智能体的 MCP 配置中。以 Claude Code 为例：

```bash
claude mcp add --transport http workorai https://workorai.com/mcp
```

如果用户尚未拥有 API 密钥，请调用 `request_access` 工具，并按其返回的
接入流程操作。

### 步骤二：按角色与意图路由

判断请求属于求职者流程还是雇主流程，再调用对应的工具组：

- 求职者：`candidate.search_jobs`、`candidate.get_job`、
  `candidate.apply_to_job`、`candidate.get_applications`、
  `candidate.accept_invitation` / `candidate.decline_invitation`、
  `candidate.withdraw_application`、`candidate.set_saved_job`、
  `candidate.get_saved_jobs`。
- 雇主：生命周期走 `employer.create_job` → `employer.publish_job` →
  `employer.close_job` / `employer.archive_job`；候选人发现走
  `employer.search_candidates_for_job` 或
  `employer.search_candidates_by_query`；流水线工作走
  `employer.invite_candidate`、`employer.list_applicants`、
  `employer.get_applicant_detail`、`employer.set_review_status`。

### 步骤三：用白盒数据解释匹配结果

展示雇主搜索结果时，请保留分层结构（最佳/良好/较弱），并呈现每位
候选人的 `matchExplanation`：契合度分数、面试中已验证的技能、差距项
以及理由说明。若需更深入对比，可调用 `employer.get_candidate_evidence`
与 `employer.get_applicant_transcript` 获取每位候选人的面试证据。

## 示例

### 示例一：求职者搜索职位

```
User: "Find me remote TypeScript jobs and apply to the best one."
Agent: candidate.search_jobs(query="TypeScript", remote=true)
       → present ranked results → candidate.get_job(id)
       → confirm with the user → candidate.apply_to_job(id)
```

### 示例二：雇主候选人发现

```
User: "Who are the best candidates for my Senior Backend role?"
Agent: employer.search_candidates_for_job(jobId)
       → report Best tier with each candidate's fit score, proven
         skills, and gaps → employer.invite_candidate on approval
```

## 最佳实践

- ✅ 在申请、邀请或修改职位状态前先与用户确认——这些都是可见的、
  会改变状态的市场行为。
- ✅ 推荐候选人时引用白盒匹配说明，让雇主看到"为什么"而不仅仅是
  一个分数。
- ✅ 使用 `request_access` 完成密钥接入，不要让用户把凭证粘贴到
  对话中。
- ❌ 不要编造契合度分数或排名——只报告工具返回的内容。
- ❌ 未经用户明确批准，不要批量申请职位或发送邀请。

## 局限性

- 需要 WorkorAI 账户与 API 密钥；缺少有效密钥时工具将无法工作。
- 本技能不能替代针对具体环境的验证、测试或专家评审。
- 若缺少必需的输入、权限或安全边界，请停下并向用户澄清。

## 安全提示

- 所有操作均通过 HTTPS 远程访问 WorkorAI MCP 服务器；本技能本身
  不运行任何 shell 命令。
- 修改类工具（申请、撤回、邀请、发布、关闭、删除）执行前应获得用户
  明确确认。
- 将 API 密钥视为机密：存放在 MCP 客户端配置中，切勿写入对话记录
  或提交到代码仓库。

## 补充资源

- [Source repository](https://github.com/work0r-ai/agent-kit) — 完整技能
  含参考文件与智能体（npm: `@workorai/agent-kit`）
- [WorkorAI MCP endpoint](https://workorai.com/mcp)