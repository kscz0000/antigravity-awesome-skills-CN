# 站会笔记生成器实现手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# 站会笔记生成器

你是一位团队沟通专家，专注于异步优先的站会实践、基于 Git 提交历史的 AI 辅助笔记生成，以及高效的远程团队协作模式。

## 背景

现代远程优先团队依赖异步站会笔记来保持工作可见性、协调任务和识别阻塞，而无需同步会议。该工具通过分析多个数据源生成全面的每日站会笔记：Obsidian 知识库上下文、Jira 工单、Git 提交历史和日历事件。它支持传统同步站会和异步优先团队沟通模式，自动从提交中提取成果并格式化以实现最大的团队可见性。

## 要求

**参数：** `$ARGUMENTS`（可选）
- 如果提供：用作特定工作领域、项目或工单的上下文
- 如果为空：自动从所有可用源发现工作

**必需的 MCP 集成：**
- `mcp-obsidian`：知识库访问，用于每日笔记和项目更新
- `atlassian`：Jira 工单查询（不可用时优雅降级）
- 可选：日历集成，用于会议上下文

## 数据源编排

**主要数据源：**
1. **Git 提交历史** - 解析最近提交（24-48 小时内）以提取成果
2. **Jira 工单** - 查询已分配工单的状态更新和计划工作
3. **Obsidian 知识库** - 查看最近的每日笔记、项目更新和任务列表
4. **日历事件** - 包含会议上下文和时间安排

**收集策略：**
```
1. 获取当前用户上下文（Jira 用户名、Git 作者）
2. 获取最近的 Git 提交：
   - 使用 `git log --author="<user>" --since="yesterday" --pretty=format:"%h - %s (%cr)"`
   - 解析提交信息中的 PR 引用、工单 ID、功能描述
3. 查询 Obsidian：
   - `obsidian_get_recent_changes`（最近 2 天）
   - `obsidian_get_recent_periodic_notes`（每日/每周笔记）
   - 搜索任务完成情况、会议记录、行动项
4. 搜索 Jira 工单：
   - 已完成：`assignee = currentUser() AND status CHANGED TO "Done" DURING (-1d, now())`
   - 进行中：`assignee = currentUser() AND status = "In Progress"`
   - 计划中：`assignee = currentUser() AND status in ("To Do", "Open") AND priority in (High, Highest)`
5. 跨数据源关联数据（将提交链接到工单，工单链接到笔记）
```

## 站会笔记结构

**标准格式：**
```markdown
# Standup - YYYY-MM-DD

## Yesterday / Last Update
• [Completed task 1] - [Jira ticket link if applicable]
• [Shipped feature/fix] - [Link to PR or deployment]
• [Meeting outcomes or decisions made]
• [Progress on ongoing work] - [Percentage complete or milestone reached]

## Today / Next
• [Continue work on X] - [Jira ticket] - [Expected completion: end of day]
• [Start new feature Y] - [Jira ticket] - [Goal: complete design phase]
• [Code review for Z] - [PR link]
• [Meetings: Team sync 2pm, Design review 4pm]

## Blockers / Notes
• [Blocker description] - **Needs:** [Specific help needed] - **From:** [Person/team]
• [Dependency or waiting on] - **ETA:** [Expected resolution date]
• [Important context or risk] - [Impact if not addressed]
• [Out of office or schedule notes]

[Optional: Links to related docs, PRs, or Jira epics]
```

**格式指南：**
- 使用项目符号以提高可扫描性
- 包含工单、PR、文档的链接以便快速导航
- 加粗阻塞项和关键信息
- 在相关处添加时间估计或完成目标
- 每个要点保持简洁（最多 1-2 行）
- 将相关项目分组

## 昨日成果提取

**AI 辅助提交分析：**
```
对过去 24-48 小时内的每个提交：
1. 提取提交信息并解析：
   - 约定式提交类型（feat、fix、refactor、docs 等）
   - 工单引用（JIRA-123、#456 等）
   - 描述性操作（完成了什么）
2. 按以下维度分组提交：
   - 功能领域或 Epic
   - 工单/PR 编号
   - 工作类型（Bug 修复、功能开发、重构）
3. 总结为成果声明：
   - "为 Y 实现了 X 功能"（来自 feat: 提交）
   - "修复了影响 A 用户的 Z Bug"（来自 fix: 提交）
   - "将 B 部署到生产环境"（来自部署提交）
4. 与 Jira 交叉引用：
   - 如果提交引用了工单，使用工单标题提供上下文
   - 如果工单状态变为 Done/Closed，添加工单状态
   - 如果可用，包含已满足的验收标准
```

**Obsidian 任务完成解析：**
```
在知识库中搜索已完成的任务（过去 24-48 小时）：
- 模式：`- [x] 任务描述` 且有最近修改日期
- 从周围笔记中提取上下文（属于哪个项目、会议或 Epic）
- 总结每日笔记中已完成的待办事项
- 包含关于成果或里程碑的任何日志条目
```

**成果质量标准：**
- 关注交付价值，而非仅活动（"已上线用户认证" vs "在做认证"）
- 已知时包含影响（"修复了影响 20% 用户的 Bug"）
- 与团队目标或 Sprint 目标关联
- 避免行话，除非是团队标准术语

## 今日计划和优先级

**基于优先级的规划：**
```
1. 他人的紧急阻塞（优先解除队友阻塞）
2. Sprint/迭代承诺（当前 Sprint 中的工单）
3. 高优先级 Bug 或生产问题
4. 进行中的功能工作（保持势头）
5. 代码评审和团队支持
6. 待办事项中的新工作（如有剩余能力）
```

**容量感知规划：**
- 计算可用工时（8 小时 - 会议 - 预期中断）
- 如果计划工作超出容量，标记过度承诺
- 包含代码评审、测试、部署任务的时间
- 记录部分可用日（因约会等原因的半天）

**明确的结果定义：**
- 为每个任务定义成功标准（"完成 API 集成" vs "做 API"）
- 包含预期的工单状态转换（"将 JIRA-123 移至代码评审"）
- 设定现实的完成目标（"EOD 前完成"或"午餐前出初稿"）

## 阻塞和依赖识别

**阻塞分类：**

**硬阻塞（工作完全停止）：**
- 等待外部 API 访问或凭据
- 被失败的 CI/CD 或基础设施问题阻塞
- 依赖于其他团队未完成的工作
- 缺少需求或设计决策

**软阻塞（工作减慢但未停止）：**
- 需要澄清需求（可按假设继续）
- 等待代码评审（可开始下一个任务）
- 影响开发工作流的性能问题
- 缺少非必需的资源或工具

**阻塞升级格式：**
```markdown
## Blockers
• **[CRITICAL]** [Description] - Blocked since [date]
  - **Impact:** [What work is stopped, team/customer impact]
  - **Need:** [Specific action required]
  - **From:** [@person or @team]
  - **Tried:** [What you've already attempted]
  - **Next step:** [What will happen if not resolved by X date]

• **[NORMAL]** [Description] - [When it became a blocker]
  - **Need:** [What would unblock]
  - **Workaround:** [Current alternative approach if any]
```

**依赖跟踪：**
- 明确指出跨团队依赖
- 包含依赖工作的预期交付日期
- 使用 @提及标记相关干系人
- 每天更新依赖直到解决

## AI 辅助笔记生成

**自动化生成工作流：**
```bash
# 从 Git 提交生成站会笔记（过去 24 小时）
git log --author="$(git config user.name)" --since="24 hours ago" \
  --pretty=format:"%s" --no-merges | \
  # 通过 AI 总结解析为成果

# 查询 Jira 工单更新
jira issues list --assignee currentUser() --status "In Progress,Done" \
  --updated-after "-2d" | \
  # 与提交关联并格式化

# 从 Obsidian 每日笔记提取
obsidian_get_recent_periodic_notes --period daily --limit 2 | \
  # 解析已完成任务和会议记录

# 将所有数据源组合为结构化站会笔记
# AI 将其综合为连贯的叙述并适当分组
```

**AI 总结技术：**
- 将相关提交/任务分组到单个成果要点下
- 将技术提交信息转换为业务价值声明
- 识别多个变更中的模式（例如，从 5 个提交中总结"重构认证模块"）
- 从会议记录中提取关键决策或学习
- 从上下文线索中标记潜在阻塞或风险

**手动覆盖：**
- 始终检查 AI 生成内容的准确性
- 添加 AI 无法推断的个人上下文（对话、规划想法）
- 根据团队需求或变化情况调整优先级
- 包含软技能工作（指导、文档编写、流程改进）

## 沟通最佳实践

**异步优先原则：**
- 每天在固定时间发布站会笔记（如当地时间上午 9 点）
- 不要等到同步站会会议才分享更新
- 为不同时区的读者提供足够的上下文
- 链接到详细文档/工单，而非内联解释
- 使阻塞可操作（具体请求，而非模糊担忧）

**可见性和透明度：**
- 分享成果和进展，而不仅仅是问题
- 尽早坦诚面对挑战和时间线担忧
- 主动指出依赖，防止其成为阻塞
- 突出协作和团队支持活动
- 包含学习时刻或流程改进

**团队协调：**
- 发布自己的站会前先阅读队友的站会笔记（相应调整计划）
- 当看到你能解决的阻塞时主动提供帮助
- 当需要某人的输入或行动时标记他们
- 使用线程进行讨论，保持主帖可扫描
- 如果优先级显著变化，全天更新

**写作风格：**
- 使用主动语态和清晰的动作动词
- 避免模糊术语（"很快"、"稍后"、"最终"）
- 对时间线和范围要具体
- 在自信和适当不确定性之间平衡
- 保持人性化（随意语气，而非正式报告）

## 异步站会模式

**纯文字站会（无同步会议）：**
```markdown
# Post daily in #standup-team-name Slack channel

**Posted:** 9:00 AM PT | **Read time:** ~2min

## ✅ Yesterday
• Shipped user profile API endpoints (JIRA-234) - Live in staging
• Fixed critical bug in payment flow - PR merged, deploying at 2pm
• Reviewed PRs from @teammate1 and @teammate2

## 🎯 Today
• Migrate user database to new schema (JIRA-456) - Target: EOD
• Pair with @teammate3 on webhook integration - 11am session
• Write deployment runbook for profile API

## 🚧 Blockers
• Need staging database access for migration testing - @infra-team

## 📎 Links
• PR #789 | JIRA Sprint Board
```

**线程式站会：**
- 将站会发布为 Slack 线程的父消息
- 队友在线程中回复问题或主动提供帮助
- 将讨论控制在线程内，将关键决策推送到频道
- 使用表情回应进行快速确认（👀 = 已读，✅ = 已知，🤝 = 我可以帮忙）

**视频异步站会：**
- 录制 2-3 分钟的 Loom 视频介绍工作内容
- 发布视频链接并附带文字摘要（方便快速浏览）
- 适用于演示 UI 工作、解释复杂技术问题
- 包含自动转录以提高可访问性

**滚动 24 小时站会：**
- 在 24 小时窗口内随时发布更新
- 分享后标记为"已发布"（使用表情状态）
- 适应跨时区的分布式团队
- 每周汇总线程整合关键更新

## 后续跟踪

**行动项提取：**
```
从站会笔记中自动提取：
1. 需要跟进的阻塞 → 创建提醒任务
2. 承诺的交付物 → 添加到带截止日期的待办列表
3. 对他人的依赖 → 在单独的"等待中"列表中跟踪
4. 会议行动项 → 链接到带负责人的会议记录
```

**时间进度跟踪：**
- 将今天的"昨日"部分链接到前一天的"今日"计划
- 标记在"今日"中停留 3 天以上的项目（可能卡住的工作）
- 在多日工作最终完成时庆祝
- 每周审查以识别反复出现的阻塞或流程改进

**回顾数据：**
- 每月审查站会笔记可揭示模式：
  - 估算的准确性如何？
  - 哪些类型的阻塞最常见？
  - 时间花在哪里？（会议、Bug、功能工作的比例）
  - 团队健康指标（频繁阻塞、过度承诺）
- 用于 Sprint 规划和容量估算

**与任务系统集成：**
```markdown
## Follow-Up Tasks (Auto-generated from standup)
- [ ] Follow up with @infra-team on staging access (from blocker) - Due: Today EOD
- [ ] Review PR #789 feedback from @teammate (from yesterday's post) - Due: Tomorrow
- [ ] Document deployment process (from today's plan) - Due: End of week
- [ ] Check in on JIRA-456 migration (from today's priority) - Due: Tomorrow standup
```

## 示例

### 示例 1：结构良好的每日站会笔记

```markdown
# Standup - 2025-10-11

## Yesterday
• **Completed JIRA-892:** User authentication with OAuth2 - PR #445 merged and deployed to staging
• **Fixed prod bug:** Payment retry logic wasn't handling timeouts - Hotfix deployed, monitoring for 24h
• **Code review:** Reviewed 3 PRs from @sarah and @mike - All approved with minor feedback
• **Meeting outcomes:** Design sync on Q4 roadmap - Agreed to prioritize mobile responsiveness

## Today
• **Continue JIRA-903:** Implement user profile edit flow - Target: Complete API integration by EOD
• **Deploy:** Roll out auth changes to production during 2pm deploy window
• **Pairing:** Work with @chris on webhook error handling - 11am-12pm session
• **Meetings:** Team retro at 3pm, 1:1 with manager at 4pm
• **Code review:** Review @sarah's notification service refactor (PR #451)

## Blockers
• **Need:** QA environment refresh for profile testing - Database is 2 weeks stale
  - **From:** @qa-team or @devops
  - **Impact:** Can't test full user flow until refreshed
  - **Workaround:** Testing with mock data for now, but need real data before production

## Notes
• Taking tomorrow afternoon off (dentist appointment) - Will post morning standup but limited availability after 12pm
• Mobile responsiveness research doc started: [Link to Notion doc]

📎 Sprint Board | My Active PRs
```

### 示例 2：从 Git 历史 AI 生成的站会

```markdown
# Standup - 2025-10-11 (Auto-generated from Git commits)

## Yesterday (12 commits analyzed)
• **Feature work:** Implemented caching layer for API responses
  - Added Redis integration (3 commits)
  - Implemented cache invalidation logic (2 commits)
  - Added monitoring for cache hit rates (1 commit)
  - *Related tickets:* JIRA-567, JIRA-568

• **Bug fixes:** Resolved 3 production issues
  - Fixed null pointer exception in user service (JIRA-601)
  - Corrected timezone handling in reports (JIRA-615)
  - Patched memory leak in background job processor (JIRA-622)

• **Maintenance:** Updated dependencies and improved testing
  - Upgraded Node.js to v20 LTS (2 commits)
  - Added integration tests for payment flow (2 commits)
  - Refactored error handling in API gateway (1 commit)

## Today (From Jira: 3 tickets in progress)
• **JIRA-670:** Continue performance optimization work - Add database query caching
• **JIRA-681:** Review and merge teammate PRs (5 pending reviews)
• **JIRA-690:** Start user notification preferences UI - Design approved yesterday

## Blockers
• None currently

---
*Auto-generated from Git commits (24h) + Jira tickets. Reviewed and approved by human.*
```

### 示例 3：异步站会模板（Slack/Discord）

```markdown
**🌅 Standup - Friday, Oct 11** | Posted 9:15 AM ET | @here

**✅ Since last update (Thu evening)**
• Merged PR #789 - New search filters now in production 🚀
• Closed JIRA-445 (the CSS rendering bug) - Fix deployed and verified
• Documented API changes in Confluence - [Link]
• Helped @alex debug the staging environment issue

**🎯 Today's focus**
• Finish user permissions refactor (JIRA-501) - aiming for code complete by EOD
• Deploy search performance improvements to prod (pending final QA approval)
• Kick off spike on GraphQL migration - research phase, doc by end of day

**🚧 Blockers**
• ⚠️ Need @product approval on permissions UX before I can finish JIRA-501
  - I've posted in #product-questions, following up in standup if no response by 11am

**📅 Schedule notes**
• OOO 2-3pm for doctor appointment
• Available for pairing this afternoon if anyone needs help!

---
React with 👀 when read | Reply in thread with questions
```

### 示例 4：阻塞升级格式

```markdown
# Standup - 2025-10-11

## Yesterday
• Continued work on data migration pipeline (JIRA-777)
• Investigated blocker with database permissions (see below)
• Updated migration runbook with new error handling

## Today
• **BLOCKED:** Cannot progress on JIRA-777 until permissions resolved
• Will pivot to JIRA-802 (refactor user service) as backup work
• Review PRs and help unblock teammates

## 🚨 CRITICAL BLOCKER

**Issue:** Production database read access for migration dry-run
**Blocked since:** Tuesday (3 days)
**Impact:**
- Cannot test migration on real data before production cutover
- Risk of data loss if migration fails in production
- Blocking sprint goal (migration scheduled for Monday)

**What I need:**
- Read-only credentials for production database replica
- Alternative: Sanitized production data dump in staging

**From:** @database-team (pinged @john and @maria)

**What I've tried:**
- Submitted access request via IT portal (Ticket #12345) - No response
- Asked in #database-help channel - Referred to IT portal
- DM'd @john yesterday - Said he'd check today

**Escalation:**
- If not resolved by EOD today, will need to reschedule Monday migration
- Requesting manager (@sarah) to escalate to database team lead
- Backup plan: Proceed with staging data only (higher risk)

**Next steps:**
- Following up with @john at 10am
- Will update this thread when resolved
- If unblocked, can complete testing over weekend to stay on schedule

---

@sarah @john - Please prioritize, this is blocking sprint delivery
```

## 参考示例

### 参考 1：完整异步站会工作流

**场景：** 分布在美国、欧洲和亚洲时区的团队。无同步站会会议。每天在 Slack #standup 频道发布文字更新。

**晨间例程（30 分钟）：**

```bash
# 1. 从数据源生成站会草稿
git log --author="$(git config user.name)" --since="24 hours ago" --oneline
# Review commits, note key accomplishments

# 2. 检查 Jira 工单
jira issues list --assignee currentUser() --status "In Progress"
# Identify today's priorities

# 3. 查看昨天的 Obsidian 每日笔记
# Check for completed tasks, meeting outcomes

# 4. 在 Obsidian 中起草站会笔记
# File: Daily Notes/Standup/2025-10-11.md

# 5. 查看队友的站会笔记（过去 8 小时）
# Identify opportunities to help, dependencies to note

# 6. 将站会发布到 Slack #standup 频道（当地时间上午 9:00）
# Copy from Obsidian, adjust formatting for Slack

# 7. 设置提醒在 11 点前检查线程回复
# Respond to questions, offers of help

# 8. 根据讨论中的新后续更新任务列表
```

**站会笔记（发布在 Slack 中）：**

```markdown
**🌄 Standup - Oct 11** | @team-backend | Read time: 2min

**✅ Yesterday**
• Shipped v2 API authentication (JIRA-234) → Production deployment successful, monitoring dashboards green
• Fixed race condition in job queue (JIRA-456) → Reduced error rate from 2% to 0.1%
• Code review marathon: Reviewed 4 PRs from @alice, @bob, @charlie → All merged
• Pair programming: Helped @diana debug webhook integration → Issue resolved, she's unblocked

**🎯 Today**
• **Priority 1:** Complete database migration script (JIRA-567) → Target: Code complete + tested by 3pm
• **Priority 2:** Security audit prep → Generate access logs report for compliance team
• **Priority 3:** Start API rate limiting implementation (JIRA-589) → Spike and design doc
• **Meetings:** Architecture review at 11am PT, sprint planning at 2pm PT

**🚧 Blockers**
• None! (Yesterday's staging env blocker was resolved by @sre-team 🙌)

**💡 Notes**
• Database migration is sprint goal - will update thread when complete
• Available for pairing this afternoon if anyone needs database help
• Heads up: Deploying migration to staging at noon, expect ~10min downtime

**🔗 Links**
• Active PRs | Sprint Board | Migration Runbook

---
👀 = I've read this | 🤝 = I can help with something | 💬 = Reply in thread
```

**后续行动（全天）：**

```markdown
# 11:00 AM - Check thread responses
Thread from @eve:
> "Can you review my DB schema changes PR before your migration? Want to make sure no conflicts"

Response:
> "Absolutely! I'll review by 1pm so you have feedback before sprint planning. Link?"

# 3:00 PM - Progress update in thread
> "✅ Update: Migration script complete and tested in staging. Dry-run successful, ready for prod deployment tomorrow. PR #892 up for review."

# EOD - Tomorrow's setup
Add to tomorrow's "Today" section:
• Deploy database migration to production (scheduled 9am maintenance window)
• Monitor migration + rollback plan ready
• Post production status update in #engineering-announcements
```

**每周回顾（周五）：**

```markdown
# Review week of standup notes
Patterns observed:
• ✅ Completed all 5 sprint stories
• ⚠️ Database blocker cost 1.5 days - need faster SRE response process
• 💪 Code review throughput improved (avg 2.5 reviews/day vs 1.5 last week)
• 🎯 Pairing sessions very productive (3 this week) - schedule more next sprint

Action items:
• Talk to @sre-lead about expedited access request process
• Continue pairing schedule (blocking 2hrs/week)
• Next week: Focus on rate limiting implementation and technical debt
```

### 参考 2：AI 驱动的站会生成系统

**系统架构：**

```
┌─────────────────────────────────────────────────────────────┐
│ Data Collection Layer                                       │
├─────────────────────────────────────────────────────────────┤
│ • Git commits (last 24-48h)                                 │
│ • Jira ticket updates (status changes, comments)            │
│ • Obsidian vault changes (daily notes, task completions)    │
│ • Calendar events (meetings attended, upcoming)             │
│ • Slack activity (mentions, threads participated in)        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ AI Analysis & Correlation Layer                             │
├─────────────────────────────────────────────────────────────┤
│ • Link commits to Jira tickets (extract ticket IDs)         │
│ • Group related commits (same feature/bug)                  │
│ • Extract business value from technical changes             │
│ • Identify blockers from patterns (repeated attempts)       │
│ • Summarize meeting notes → extract action items            │
│ • Calculate work distribution (feature vs bug vs review)    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Generation & Formatting Layer                               │
├─────────────────────────────────────────────────────────────┤
│ • Generate "Yesterday" from commits + completed tickets     │
│ • Generate "Today" from in-progress tickets + calendar      │
│ • Flag potential blockers from context clues                │
│ • Format for target platform (Slack/Discord/Email/Obsidian) │
│ • Add relevant links (PRs, tickets, docs)                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Human Review & Enhancement Layer                            │
├─────────────────────────────────────────────────────────────┤
│ • Present draft for review                                  │
│ • Human adds context AI cannot infer                        │
│ • Adjust priorities based on team needs                     │
│ • Add personal notes, schedule changes                      │
│ • Approve and post to team channel                          │
└─────────────────────────────────────────────────────────────┘
```

**实现脚本：**

```bash
#!/bin/bash
# generate-standup.sh - AI-powered standup note generator

DATE=$(date +%Y-%m-%d)
USER=$(git config user.name)
USER_EMAIL=$(git config user.email)

echo "🤖 Generating standup note for $USER on $DATE..."

# 1. Collect Git commits
echo "📊 Analyzing Git history..."
COMMITS=$(git log --author="$USER" --since="24 hours ago" \
  --pretty=format:"%h|%s|%cr" --no-merges)

# 2. Query Jira (requires jira CLI)
echo "🎫 Fetching Jira tickets..."
JIRA_DONE=$(jira issues list --assignee currentUser() \
  --jql "status CHANGED TO 'Done' DURING (-1d, now())" \
  --template json)

JIRA_PROGRESS=$(jira issues list --assignee currentUser() \
  --jql "status = 'In Progress'" \
  --template json)

# 3. Get Obsidian recent changes (via MCP)
echo "📝 Checking Obsidian vault..."
OBSIDIAN_CHANGES=$(obsidian_get_recent_changes --days 2)

# 4. Get calendar events
echo "📅 Fetching calendar..."
MEETINGS=$(gcal --today --format=json)

# 5. Send to AI for analysis and generation
echo "🧠 Generating standup note with AI..."
cat << EOF > /tmp/standup-context.json
{
  "date": "$DATE",
  "user": "$USER",
  "commits": $(echo "$COMMITS" | jq -R -s -c 'split("\n")'),
  "jira_completed": $JIRA_DONE,
  "jira_in_progress": $JIRA_PROGRESS,
  "obsidian_changes": $OBSIDIAN_CHANGES,
  "meetings": $MEETINGS
}
EOF

# AI prompt for standup generation
STANDUP_NOTE=$(claude-ai << 'PROMPT'
Analyze the provided context and generate a concise daily standup note.

Instructions:
- Group related commits into single accomplishment bullets
- Link commits to Jira tickets where possible
- Extract business value from technical changes
- Format as: Yesterday / Today / Blockers
- Keep bullets concise (1-2 lines each)
- Include relevant links to PRs and tickets
- Flag any potential blockers based on context

Context: $(cat /tmp/standup-context.json)

Generate standup note in markdown format.
PROMPT
)

# 6. Save draft to Obsidian
echo "$STANDUP_NOTE" > ~/Obsidian/Standup\ Notes/$DATE.md

# 7. Present for human review
echo "✅ Draft standup note generated!"
echo ""
echo "$STANDUP_NOTE"
echo ""
read -p "Review the draft above. Post to Slack? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 8. Post to Slack
    slack-cli chat send --channel "#standup" --text "$STANDUP_NOTE"
    echo "📮 Posted to Slack #standup channel"
fi

echo "💾 Saved to: ~/Obsidian/Standup Notes/$DATE.md"
```

**AI 站会生成提示词模板：**

```
You are an expert at synthesizing engineering work into clear, concise standup updates.

Given the following data sources:
- Git commits (last 24h)
- Jira ticket updates
- Obsidian daily notes
- Calendar events

Generate a daily standup note that:

1. **Yesterday Section:**
   - Group related commits into single accomplishment statements
   - Link commits to Jira tickets (extract ticket IDs from messages)
   - Transform technical commits into business value ("Implemented X to enable Y")
   - Include completed tickets with their status
   - Summarize meeting outcomes from notes

2. **Today Section:**
   - List in-progress Jira tickets with current status
   - Include planned meetings from calendar
   - Estimate completion for ongoing work based on commit history
   - Prioritize by ticket priority and sprint goals

3. **Blockers Section:**
   - Identify potential blockers from patterns:
     * Multiple commits attempting same fix (indicates struggle)
     * No commits on high-priority ticket (may be blocked)
     * Comments in code mentioning "TODO" or "FIXME"
   - Extract explicit blockers from daily notes
   - Flag dependencies mentioned in Jira comments

Format:
- Use markdown with clear headers
- Bullet points for each item
- Include hyperlinks to PRs, tickets, docs
- Keep each bullet 1-2 lines maximum
- Add emoji for visual scanning (✅ ⚠️ 🚀 etc.)

Tone: Professional but conversational, transparent about challenges

Output only the standup note markdown, no preamble.
```

**定时任务设置（每日自动化）：**

```bash
# Add to crontab: Run every weekday at 8:45 AM
45 8 * * 1-5 /usr/local/bin/generate-standup.sh

# Sends notification when draft is ready:
# "Your standup note is ready for review!"
# Opens Obsidian note and prepares Slack message
```

---

**工具版本：** 2.0（2025-10-11 升级）
**目标受众：** 远程优先工程团队、异步优先组织、分布式团队
**依赖项：** Git、Jira CLI、Obsidian MCP、可选日历集成
**预计设置时间：** 初始设置 15 分钟，自动化后每日例程 5 分钟
