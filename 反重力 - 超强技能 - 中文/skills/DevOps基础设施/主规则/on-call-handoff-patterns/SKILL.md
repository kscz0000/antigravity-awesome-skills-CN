---
name: on-call-handoff-patterns
description: "有效的值班交接模式，确保班次之间的连续性、上下文传递和可靠的事件响应。当用户要求'值班交接'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 值班交接模式

用于值班班次交接的有效模式，确保班次之间的连续性、上下文传递和可靠的事件响应。

## 不适用场景

- 任务与值班交接模式无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请查看 `resources/implementation-playbook.md`。

## 适用场景

- 交接值班职责
- 编写班次交接摘要
- 记录正在进行的调查
- 建立值班轮换流程
- 提升交接质量
- 培训新值班工程师

## 核心概念

### 1. 交接要素

| 要素 | 用途 |
|------|------|
| **Active Incidents** | 当前故障 |
| **Ongoing Investigations** | 正在调试的问题 |
| **Recent Changes** | 部署、配置变更 |
| **Known Issues** | 已知的临时解决方案 |
| **Upcoming Events** | 计划中的维护、发布 |

### 2. 交接时间安排

```
Recommended: 30 min overlap between shifts

Outgoing:
├── 15 min: Write handoff document
└── 15 min: Sync call with incoming

Incoming:
├── 15 min: Review handoff document
├── 15 min: Sync call with outgoing
└── 5 min: Verify alerting setup
```

## 模板

### 模板 1：班次交接文档

```markdown
# On-Call Handoff: Platform Team

**Outgoing**: @alice (2024-01-15 to 2024-01-22)
**Incoming**: @bob (2024-01-22 to 2024-01-29)
**Handoff Time**: 2024-01-22 09:00 UTC

---

## 🔴 Active Incidents

### None currently active
No active incidents at handoff time.

---

## 🟡 Ongoing Investigations

### 1. Intermittent API Timeouts (ENG-1234)
**Status**: Investigating
**Started**: 2024-01-20
**Impact**: ~0.1% of requests timing out

**Context**:
- Timeouts correlate with database backup window (02:00-03:00 UTC)
- Suspect backup process causing lock contention
- Added extra logging in PR #567 (deployed 01/21)

**Next Steps**:
- [ ] Review new logs after tonight's backup
- [ ] Consider moving backup window if confirmed

**Resources**:
- Dashboard: [API Latency](https://grafana/d/api-latency)
- Thread: #platform-eng (01/20, 14:32)

---

### 2. Memory Growth in Auth Service (ENG-1235)
**Status**: Monitoring
**Started**: 2024-01-18
**Impact**: None yet (proactive)

**Context**:
- Memory usage growing ~5% per day
- No memory leak found in profiling
- Suspect connection pool not releasing properly

**Next Steps**:
- [ ] Review heap dump from 01/21
- [ ] Consider restart if usage > 80%

**Resources**:
- Dashboard: [Auth Service Memory](https://grafana/d/auth-memory)
- Analysis doc: [Memory Investigation](https://docs/eng-1235)

---

## 🟢 Resolved This Shift

### Payment Service Outage (2024-01-19)
- **Duration**: 23 minutes
- **Root Cause**: Database connection exhaustion
- **Resolution**: Rolled back v2.3.4, increased pool size
- **Postmortem**: [POSTMORTEM-89](https://docs/postmortem-89)
- **Follow-up tickets**: ENG-1230, ENG-1231

---

## 📋 Recent Changes

### Deployments
| Service | Version | Time | Notes |
|---------|---------|------|-------|
| api-gateway | v3.2.1 | 01/21 14:00 | Bug fix for header parsing |
| user-service | v2.8.0 | 01/20 10:00 | New profile features |
| auth-service | v4.1.2 | 01/19 16:00 | Security patch |

### Configuration Changes
- 01/21: Increased API rate limit from 1000 to 1500 RPS
- 01/20: Updated database connection pool max from 50 to 75

### Infrastructure
- 01/20: Added 2 nodes to Kubernetes cluster
- 01/19: Upgraded Redis from 6.2 to 7.0

---

## ⚠️ Known Issues & Workarounds

### 1. Slow Dashboard Loading
**Issue**: Grafana dashboards slow on Monday mornings
**Workaround**: Wait 5 min after 08:00 UTC for cache warm-up
**Ticket**: OPS-456 (P3)

### 2. Flaky Integration Test
**Issue**: `test_payment_flow` fails intermittently in CI
**Workaround**: Re-run failed job (usually passes on retry)
**Ticket**: ENG-1200 (P2)

---

## 📅 Upcoming Events

| Date | Event | Impact | Contact |
|------|-------|--------|---------|
| 01/23 02:00 | Database maintenance | 5 min read-only | @dba-team |
| 01/24 14:00 | Major release v5.0 | Monitor closely | @release-team |
| 01/25 | Marketing campaign | 2x traffic expected | @platform |

---

## 📞 Escalation Reminders

| Issue Type | First Escalation | Second Escalation |
|------------|------------------|-------------------|
| Payment issues | @payments-oncall | @payments-manager |
| Auth issues | @auth-oncall | @security-team |
| Database issues | @dba-team | @infra-manager |
| Unknown/severe | @engineering-manager | @vp-engineering |

---

## 🔧 Quick Reference

### Common Commands
```bash
# Check service health
kubectl get pods -A | grep -v Running

# Recent deployments
kubectl get events --sort-by='.lastTimestamp' | tail -20

# Database connections
psql -c "SELECT count(*) FROM pg_stat_activity;"

# Clear cache (emergency only)
redis-cli FLUSHDB
```

### Important Links
- [Runbooks](https://wiki/runbooks)
- [Service Catalog](https://wiki/services)
- [Incident Slack](https://slack.com/incidents)
- [PagerDuty](https://pagerduty.com/schedules)

---

## Handoff Checklist

### Outgoing Engineer
- [x] Document active incidents
- [x] Document ongoing investigations
- [x] List recent changes
- [x] Note known issues
- [x] Add upcoming events
- [x] Sync with incoming engineer

### Incoming Engineer
- [ ] Read this document
- [ ] Join sync call
- [ ] Verify PagerDuty is routing to you
- [ ] Verify Slack notifications working
- [ ] Check VPN/access working
- [ ] Review critical dashboards
```

### 模板 2：快速交接（异步）

```markdown
# Quick Handoff: @alice → @bob

## TL;DR
- No active incidents
- 1 investigation ongoing (API timeouts, see ENG-1234)
- Major release tomorrow (01/24) - be ready for issues

## Watch List
1. API latency around 02:00-03:00 UTC (backup window)
2. Auth service memory (restart if > 80%)

## Recent
- Deployed api-gateway v3.2.1 yesterday (stable)
- Increased rate limits to 1500 RPS

## Coming Up
- 01/23 02:00 - DB maintenance (5 min read-only)
- 01/24 14:00 - v5.0 release

## Questions?
I'll be available on Slack until 17:00 today.
```

### 模板 3：事件交接（进行中）

```markdown
# INCIDENT HANDOFF: Payment Service Degradation

**Incident Start**: 2024-01-22 08:15 UTC
**Current Status**: Mitigating
**Severity**: SEV2

---

## Current State
- Error rate: 15% (down from 40%)
- Mitigation in progress: scaling up pods
- ETA to resolution: ~30 min

## What We Know
1. Root cause: Memory pressure on payment-service pods
2. Triggered by: Unusual traffic spike (3x normal)
3. Contributing: Inefficient query in checkout flow

## What We've Done
- Scaled payment-service from 5 → 15 pods
- Enabled rate limiting on checkout endpoint
- Disabled non-critical features

## What Needs to Happen
1. Monitor error rate - should reach <1% in ~15 min
2. If not improving, escalate to @payments-manager
3. Once stable, begin root cause investigation

## Key People
- Incident Commander: @alice (handing off)
- Comms Lead: @charlie
- Technical Lead: @bob (incoming)

## Communication
- Status page: Updated at 08:45
- Customer support: Notified
- Exec team: Aware

## Resources
- Incident channel: #inc-20240122-payment
- Dashboard: [Payment Service](https://grafana/d/payments)
- Runbook: [Payment Degradation](https://wiki/runbooks/payments)

---

**Incoming on-call (@bob) - Please confirm you have:**
- [ ] Joined #inc-20240122-payment
- [ ] Access to dashboards
- [ ] Understand current state
- [ ] Know escalation path
```

## 交接同步会议

### 议程（15 分钟）

```markdown
## Handoff Sync: @alice → @bob

1. **Active Issues** (5 min)
   - Walk through any ongoing incidents
   - Discuss investigation status
   - Transfer context and theories

2. **Recent Changes** (3 min)
   - Deployments to watch
   - Config changes
   - Known regressions

3. **Upcoming Events** (3 min)
   - Maintenance windows
   - Expected traffic changes
   - Releases planned

4. **Questions** (4 min)
   - Clarify anything unclear
   - Confirm access and alerting
   - Exchange contact info
```

## 值班最佳实践

### 上岗前

```markdown
## Pre-Shift Checklist

### Access Verification
- [ ] VPN working
- [ ] kubectl access to all clusters
- [ ] Database read access
- [ ] Log aggregator access (Splunk/Datadog)
- [ ] PagerDuty app installed and logged in

### Alerting Setup
- [ ] PagerDuty schedule shows you as primary
- [ ] Phone notifications enabled
- [ ] Slack notifications for incident channels
- [ ] Test alert received and acknowledged

### Knowledge Refresh
- [ ] Review recent incidents (past 2 weeks)
- [ ] Check service changelog
- [ ] Skim critical runbooks
- [ ] Know escalation contacts

### Environment Ready
- [ ] Laptop charged and accessible
- [ ] Phone charged
- [ ] Quiet space available for calls
- [ ] Secondary contact identified (if traveling)
```

### 值班期间

```markdown
## Daily On-Call Routine

### Morning (start of day)
- [ ] Check overnight alerts
- [ ] Review dashboards for anomalies
- [ ] Check for any P0/P1 tickets created
- [ ] Skim incident channels for context

### Throughout Day
- [ ] Respond to alerts within SLA
- [ ] Document investigation progress
- [ ] Update team on significant issues
- [ ] Triage incoming pages

### End of Day
- [ ] Hand off any active issues
- [ ] Update investigation docs
- [ ] Note anything for next shift
```

### 下岗后

```markdown
## Post-Shift Checklist

- [ ] Complete handoff document
- [ ] Sync with incoming on-call
- [ ] Verify PagerDuty routing changed
- [ ] Close/update investigation tickets
- [ ] File postmortems for any incidents
- [ ] Take time off if shift was stressful
```

## 升级指南

### 何时升级

```markdown
## Escalation Triggers

### Immediate Escalation
- SEV1 incident declared
- Data breach suspected
- Unable to diagnose within 30 min
- Customer or legal escalation received

### Consider Escalation
- Issue spans multiple teams
- Requires expertise you don't have
- Business impact exceeds threshold
- You're uncertain about next steps

### How to Escalate
1. Page the appropriate escalation path
2. Provide brief context in Slack
3. Stay engaged until escalation acknowledges
4. Hand off cleanly, don't just disappear
```

## 最佳实践

### 应该做的
- **记录一切** — 未来的你会感谢现在的你
- **尽早升级** — 宁可多此一举
- **适当休息** — 告警疲劳是真实存在的
- **保持同步交接** — 异步交接会丢失上下文
- **提前测试** — 在故障发生前测试，而非发生时

### 不应该做的
- **不要跳过交接** — 上下文丢失会导致故障
- **不要逞英雄** — 需要时就升级
- **不要忽略告警** — 即使看起来无关紧要
- **不要带病值班** — 换班才是正确选择
- **不要失联** — 值班期间保持可联系状态

## 参考资源

- [Google SRE - Being On-Call](https://sre.google/sre-book/being-on-call/)
- [PagerDuty On-Call Guide](https://www.pagerduty.com/resources/learn/on-call-management/)
- [Increment On-Call Issue](https://increment.com/on-call/)

## 使用限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来要求澄清。
