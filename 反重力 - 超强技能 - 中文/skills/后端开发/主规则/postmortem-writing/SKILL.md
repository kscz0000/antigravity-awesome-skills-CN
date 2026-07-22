---
name: postmortem-writing
description: "编写有效、无指责的事后复盘文档的完整指南，推动组织学习并防止事故再次发生。当用户要求'写复盘''写postmortem''事故复盘''事后分析'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 事后复盘写作

编写有效、无指责的事后复盘文档的完整指南，推动组织学习并防止事故再次发生。

## 不要使用此技能的场景

- 任务与事后复盘写作无关
- 需要本技能范围之外的其他领域或工具

## 操作指南

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 使用此技能的场景

- 进行事故后复盘
- 撰写事后复盘文档
- 主持无指责的事后复盘会议
- 识别根本原因和促成因素
- 创建可执行的后续行动项
- 建设组织学习文化

## 核心概念

### 1. 无指责文化

| 指责导向 | 无指责 |
|----------|--------|
| "谁导致的？" | "什么条件允许了这件事发生？" |
| "某人犯了错误" | "系统允许了这个错误" |
| 惩罚个人 | 改进系统 |
| 隐藏信息 | 分享经验教训 |
| 害怕发声 | 心理安全感 |

### 2. 复盘触发条件

- SEV1 或 SEV2 级事故
- 面向客户的中断超过 15 分钟
- 数据丢失或安全事件
- 险些造成严重后果的未遂事件
- 全新的故障模式
- 需要非常规干预的事故

## 快速上手

### 复盘时间线
```
Day 0: Incident occurs
Day 1-2: Draft postmortem document
Day 3-5: Postmortem meeting
Day 5-7: Finalize document, create tickets
Week 2+: Action item completion
Quarterly: Review patterns across incidents
```

## 模板

### 模板 1：标准事后复盘

```markdown
# Postmortem: [Incident Title]

**Date**: 2024-01-15
**Authors**: @alice, @bob
**Status**: Draft | In Review | Final
**Incident Severity**: SEV2
**Incident Duration**: 47 minutes

## Executive Summary

On January 15, 2024, the payment processing service experienced a 47-minute outage affecting approximately 12,000 customers. The root cause was a database connection pool exhaustion triggered by a configuration change in deployment v2.3.4. The incident was resolved by rolling back to v2.3.3 and increasing connection pool limits.

**Impact**:
- 12,000 customers unable to complete purchases
- Estimated revenue loss: $45,000
- 847 support tickets created
- No data loss or security implications

## Timeline (All times UTC)

| Time | Event |
|------|-------|
| 14:23 | Deployment v2.3.4 completed to production |
| 14:31 | First alert: `payment_error_rate > 5%` |
| 14:33 | On-call engineer @alice acknowledges alert |
| 14:35 | Initial investigation begins, error rate at 23% |
| 14:41 | Incident declared SEV2, @bob joins |
| 14:45 | Database connection exhaustion identified |
| 14:52 | Decision to rollback deployment |
| 14:58 | Rollback to v2.3.3 initiated |
| 15:10 | Rollback complete, error rate dropping |
| 15:18 | Service fully recovered, incident resolved |

## Root Cause Analysis

### What Happened

The v2.3.4 deployment included a change to the database query pattern that inadvertently removed connection pooling for a frequently-called endpoint. Each request opened a new database connection instead of reusing pooled connections.

### Why It Happened

1. **Proximate Cause**: Code change in `PaymentRepository.java` replaced pooled `DataSource` with direct `DriverManager.getConnection()` calls.

2. **Contributing Factors**:
   - Code review did not catch the connection handling change
   - No integration tests specifically for connection pool behavior
   - Staging environment has lower traffic, masking the issue
   - Database connection metrics alert threshold was too high (90%)

3. **5 Whys Analysis**:
   - Why did the service fail? → Database connections exhausted
   - Why were connections exhausted? → Each request opened new connection
   - Why did each request open new connection? → Code bypassed connection pool
   - Why did code bypass connection pool? → Developer unfamiliar with codebase patterns
   - Why was developer unfamiliar? → No documentation on connection management patterns

### System Diagram

```
[Client] → [Load Balancer] → [Payment Service] → [Database]
                                    ↓
                            Connection Pool (broken)
                                    ↓
                            Direct connections (cause)
```

## Detection

### What Worked
- Error rate alert fired within 8 minutes of deployment
- Grafana dashboard clearly showed connection spike
- On-call response was swift (2 minute acknowledgment)

### What Didn't Work
- Database connection metric alert threshold too high
- No deployment-correlated alerting
- Canary deployment would have caught this earlier

### Detection Gap
The deployment completed at 14:23, but the first alert didn't fire until 14:31 (8 minutes). A deployment-aware alert could have detected the issue faster.

## Response

### What Worked
- On-call engineer quickly identified database as the issue
- Rollback decision was made decisively
- Clear communication in incident channel

### What Could Be Improved
- Took 10 minutes to correlate issue with recent deployment
- Had to manually check deployment history
- Rollback took 12 minutes (could be faster)

## Impact

### Customer Impact
- 12,000 unique customers affected
- Average impact duration: 35 minutes
- 847 support tickets (23% of affected users)
- Customer satisfaction score dropped 12 points

### Business Impact
- Estimated revenue loss: $45,000
- Support cost: ~$2,500 (agent time)
- Engineering time: ~8 person-hours

### Technical Impact
- Database primary experienced elevated load
- Some replica lag during incident
- No permanent damage to systems

## Lessons Learned

### What Went Well
1. Alerting detected the issue before customer reports
2. Team collaborated effectively under pressure
3. Rollback procedure worked smoothly
4. Communication was clear and timely

### What Went Wrong
1. Code review missed critical change
2. Test coverage gap for connection pooling
3. Staging environment doesn't reflect production traffic
4. Alert thresholds were not tuned properly

### Where We Got Lucky
1. Incident occurred during business hours with full team available
2. Database handled the load without failing completely
3. No other incidents occurred simultaneously

## Action Items

| Priority | Action | Owner | Due Date | Ticket |
|----------|--------|-------|----------|--------|
| P0 | Add integration test for connection pool behavior | @alice | 2024-01-22 | ENG-1234 |
| P0 | Lower database connection alert threshold to 70% | @bob | 2024-01-17 | OPS-567 |
| P1 | Document connection management patterns | @alice | 2024-01-29 | DOC-89 |
| P1 | Implement deployment-correlated alerting | @bob | 2024-02-05 | OPS-568 |
| P2 | Evaluate canary deployment strategy | @charlie | 2024-02-15 | ENG-1235 |
| P2 | Load test staging with production-like traffic | @dave | 2024-02-28 | QA-123 |

## Appendix

### Supporting Data

#### Error Rate Graph
[Link to Grafana dashboard snapshot]

#### Database Connection Graph
[Link to metrics]

### Related Incidents
- 2023-11-02: Similar connection issue in User Service (POSTMORTEM-42)

### References
- Connection Pool Best Practices
- Deployment Runbook
```

### 模板 2：5 Whys 分析

```markdown
# 5 Whys Analysis: [Incident]

## Problem Statement
Payment service experienced 47-minute outage due to database connection exhaustion.

## Analysis

### Why #1: Why did the service fail?
**Answer**: Database connections were exhausted, causing all new requests to fail.

**Evidence**: Metrics showed connection count at 100/100 (max), with 500+ pending requests.

---

### Why #2: Why were database connections exhausted?
**Answer**: Each incoming request opened a new database connection instead of using the connection pool.

**Evidence**: Code diff shows direct `DriverManager.getConnection()` instead of pooled `DataSource`.

---

### Why #3: Why did the code bypass the connection pool?
**Answer**: A developer refactored the repository class and inadvertently changed the connection acquisition method.

**Evidence**: PR #1234 shows the change, made while fixing a different bug.

---

### Why #4: Why wasn't this caught in code review?
**Answer**: The reviewer focused on the functional change (the bug fix) and didn't notice the infrastructure change.

**Evidence**: Review comments only discuss business logic.

---

### Why #5: Why isn't there a safety net for this type of change?
**Answer**: We lack automated tests that verify connection pool behavior and lack documentation about our connection patterns.

**Evidence**: Test suite has no tests for connection handling; wiki has no article on database connections.

## Root Causes Identified

1. **Primary**: Missing automated tests for infrastructure behavior
2. **Secondary**: Insufficient documentation of architectural patterns
3. **Tertiary**: Code review checklist doesn't include infrastructure considerations

## Systemic Improvements

| Root Cause | Improvement | Type |
|------------|-------------|------|
| Missing tests | Add infrastructure behavior tests | Prevention |
| Missing docs | Document connection patterns | Prevention |
| Review gaps | Update review checklist | Detection |
| No canary | Implement canary deployments | Mitigation |
```

### 模板 3：快速复盘（轻微事故）

```markdown
# Quick Postmortem: [Brief Title]

**Date**: 2024-01-15 | **Duration**: 12 min | **Severity**: SEV3

## What Happened
API latency spiked to 5s due to cache miss storm after cache flush.

## Timeline
- 10:00 - Cache flush initiated for config update
- 10:02 - Latency alerts fire
- 10:05 - Identified as cache miss storm
- 10:08 - Enabled cache warming
- 10:12 - Latency normalized

## Root Cause
Full cache flush for minor config update caused thundering herd.

## Fix
- Immediate: Enabled cache warming
- Long-term: Implement partial cache invalidation (ENG-999)

## Lessons
Don't full-flush cache in production; use targeted invalidation.
```

## 引导指南

### 主持事后复盘会议

```markdown
## Meeting Structure (60 minutes)

### 1. Opening (5 min)
- Remind everyone of blameless culture
- "We're here to learn, not to blame"
- Review meeting norms

### 2. Timeline Review (15 min)
- Walk through events chronologically
- Ask clarifying questions
- Identify gaps in timeline

### 3. Analysis Discussion (20 min)
- What failed?
- Why did it fail?
- What conditions allowed this?
- What would have prevented it?

### 4. Action Items (15 min)
- Brainstorm improvements
- Prioritize by impact and effort
- Assign owners and due dates

### 5. Closing (5 min)
- Summarize key learnings
- Confirm action item owners
- Schedule follow-up if needed

## Facilitation Tips
- Keep discussion on track
- Redirect blame to systems
- Encourage quiet participants
- Document dissenting views
- Time-box tangents
```

## 要避免的反模式

| 反模式 | 问题 | 更好的做法 |
|--------|------|-----------|
| **互相指责** | 阻断学习 | 聚焦于系统 |
| **浅层分析** | 无法防止复发 | 问五次"为什么" |
| **没有行动项** | 浪费时间 | 始终有具体的后续步骤 |
| **不切实际的行动** | 永远完不成 | 范围限定在可实现的任务上 |
| **不做跟进** | 行动被遗忘 | 在工单系统中追踪 |

## 最佳实践

### 应该做的
- **立即开始** — 记忆衰减很快
- **具体精确** — 精确的时间、精确的错误
- **附上图表** — 可视化证据
- **指定负责人** — 不要出现无主的行动项
- **广泛分享** — 组织层面的学习

### 不应该做的
- **不要点名批评** — 永远不要
- **不要跳过小事故** — 它们能揭示模式
- **不要变成指责文件** — 那会扼杀学习
- **不要制造无效工作** — 行动项应该有意义
- **不要跳过跟进** — 验证行动项是否完成

## 参考资料

- [Google SRE - Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [Etsy's Blameless Postmortems](https://codeascraft.com/2012/05/22/blameless-postmortems/)
- [PagerDuty Postmortem Guide](https://postmortems.pagerduty.com/)

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来寻求澄清。
