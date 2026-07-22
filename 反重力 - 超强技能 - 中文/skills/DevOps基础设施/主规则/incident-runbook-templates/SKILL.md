---
name: incident-runbook-templates
description: "生产级事件响应 Runbook 模板，覆盖检测、分诊、缓解、恢复和沟通。当用户要求'创建事件响应 Runbook'、'编写故障手册'、'制定应急流程'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 事件 Runbook 模板

生产级事件响应 Runbook 模板，覆盖检测、分诊、缓解、恢复和沟通。

## 不适用场景

- 任务与事件 Runbook 模板无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可操作的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 适用场景

- 创建事件响应流程
- 构建服务专属 Runbook
- 建立升级路径
- 编写恢复流程文档
- 响应正在发生的事件
- 值班工程师入职培训

## 核心概念

### 1. 事件严重级别

| 严重级别 | 影响 | 响应时间 | 示例 |
|----------|------|----------|------|
| **SEV1** | 完全宕机、数据丢失 | 15 分钟 | 生产环境不可用 |
| **SEV2** | 严重降级 | 30 分钟 | 核心功能故障 |
| **SEV3** | 轻微影响 | 2 小时 | 非关键 Bug |
| **SEV4** | 极小影响 | 下一个工作日 | 界面显示问题 |

### 2. Runbook 结构

```
1. Overview & Impact
2. Detection & Alerts
3. Initial Triage
4. Mitigation Steps
5. Root Cause Investigation
6. Resolution Procedures
7. Verification & Rollback
8. Communication Templates
9. Escalation Matrix
```

## Runbook 模板

### 模板 1：服务宕机 Runbook

```markdown
# [Service Name] Outage Runbook

## Overview
**Service**: Payment Processing Service
**Owner**: Platform Team
**Slack**: #payments-incidents
**PagerDuty**: payments-oncall

## Impact Assessment
- [ ] Which customers are affected?
- [ ] What percentage of traffic is impacted?
- [ ] Are there financial implications?
- [ ] What's the blast radius?

## Detection
### Alerts
- `payment_error_rate > 5%` (PagerDuty)
- `payment_latency_p99 > 2s` (Slack)
- `payment_success_rate < 95%` (PagerDuty)

### Dashboards
- [Payment Service Dashboard](https://grafana/d/payments)
- [Error Tracking](https://sentry.io/payments)
- [Dependency Status](https://status.stripe.com)

## Initial Triage (First 5 Minutes)

### 1. Assess Scope
```bash
# Check service health
kubectl get pods -n payments -l app=payment-service

# Check recent deployments
kubectl rollout history deployment/payment-service -n payments

# Check error rates
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{status=~'5..'}[5m]))"
```

### 2. Quick Health Checks
- [ ] Can you reach the service? `curl -I https://api.company.com/payments/health`
- [ ] Database connectivity? Check connection pool metrics
- [ ] External dependencies? Check Stripe, bank API status
- [ ] Recent changes? Check deploy history

### 3. Initial Classification
| Symptom | Likely Cause | Go To Section |
|---------|--------------|---------------|
| All requests failing | Service down | Section 4.1 |
| High latency | Database/dependency | Section 4.2 |
| Partial failures | Code bug | Section 4.3 |
| Spike in errors | Traffic surge | Section 4.4 |

## Mitigation Procedures

### 4.1 Service Completely Down
```bash
# Step 1: Check pod status
kubectl get pods -n payments

# Step 2: If pods are crash-looping, check logs
kubectl logs -n payments -l app=payment-service --tail=100

# Step 3: Check recent deployments
kubectl rollout history deployment/payment-service -n payments

# Step 4: ROLLBACK if recent deploy is suspect
kubectl rollout undo deployment/payment-service -n payments

# Step 5: Scale up if resource constrained
kubectl scale deployment/payment-service -n payments --replicas=10

# Step 6: Verify recovery
kubectl rollout status deployment/payment-service -n payments
```

### 4.2 High Latency
```bash
# Step 1: Check database connections
kubectl exec -n payments deploy/payment-service -- \
  curl localhost:8080/metrics | grep db_pool

# Step 2: Check slow queries (if DB issue)
psql -h $DB_HOST -U $DB_USER -c "
  SELECT pid, now() - query_start AS duration, query
  FROM pg_stat_activity
  WHERE state = 'active' AND duration > interval '5 seconds'
  ORDER BY duration DESC;"

# Step 3: Kill long-running queries if needed
psql -h $DB_HOST -U $DB_USER -c "SELECT pg_terminate_backend(pid);"

# Step 4: Check external dependency latency
curl -w "@curl-format.txt" -o /dev/null -s https://api.stripe.com/v1/health

# Step 5: Enable circuit breaker if dependency is slow
kubectl set env deployment/payment-service \
  STRIPE_CIRCUIT_BREAKER_ENABLED=true -n payments
```

### 4.3 Partial Failures (Specific Errors)
```bash
# Step 1: Identify error pattern
kubectl logs -n payments -l app=payment-service --tail=500 | \
  grep -i error | sort | uniq -c | sort -rn | head -20

# Step 2: Check error tracking
# Go to Sentry: https://sentry.io/payments

# Step 3: If specific endpoint, enable feature flag to disable
curl -X POST https://api.company.com/internal/feature-flags \
  -d '{"flag": "DISABLE_PROBLEMATIC_FEATURE", "enabled": true}'

# Step 4: If data issue, check recent data changes
psql -h $DB_HOST -c "
  SELECT * FROM audit_log
  WHERE table_name = 'payment_methods'
  AND created_at > now() - interval '1 hour';"
```

### 4.4 Traffic Surge
```bash
# Step 1: Check current request rate
kubectl top pods -n payments

# Step 2: Scale horizontally
kubectl scale deployment/payment-service -n payments --replicas=20

# Step 3: Enable rate limiting
kubectl set env deployment/payment-service \
  RATE_LIMIT_ENABLED=true \
  RATE_LIMIT_RPS=1000 -n payments

# Step 4: If attack, block suspicious IPs
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-suspicious
  namespace: payments
spec:
  podSelector:
    matchLabels:
      app: payment-service
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 192.168.1.0/24  # Suspicious range
EOF
```

## Verification Steps
```bash
# Verify service is healthy
curl -s https://api.company.com/payments/health | jq

# Verify error rate is back to normal
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{status=~'5..'}[5m]))" | jq '.data.result[0].value[1]'

# Verify latency is acceptable
curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.99,sum(rate(http_request_duration_seconds_bucket[5m]))by(le))" | jq

# Smoke test critical flows
./scripts/smoke-test-payments.sh
```

## Rollback Procedures
```bash
# Rollback Kubernetes deployment
kubectl rollout undo deployment/payment-service -n payments

# Rollback database migration (if applicable)
./scripts/db-rollback.sh $MIGRATION_VERSION

# Rollback feature flag
curl -X POST https://api.company.com/internal/feature-flags \
  -d '{"flag": "NEW_PAYMENT_FLOW", "enabled": false}'
```

## Escalation Matrix

| Condition | Escalate To | Contact |
|-----------|-------------|---------|
| > 15 min unresolved SEV1 | Engineering Manager | @manager (Slack) |
| Data breach suspected | Security Team | #security-incidents |
| Financial impact > $10k | Finance + Legal | @finance-oncall |
| Customer communication needed | Support Lead | @support-lead |

## Communication Templates

### Initial Notification (Internal)
```
🚨 INCIDENT: Payment Service Degradation

Severity: SEV2
Status: Investigating
Impact: ~20% of payment requests failing
Start Time: [TIME]
Incident Commander: [NAME]

Current Actions:
- Investigating root cause
- Scaling up service
- Monitoring dashboards

Updates in #payments-incidents
```

### Status Update
```
📊 UPDATE: Payment Service Incident

Status: Mitigating
Impact: Reduced to ~5% failure rate
Duration: 25 minutes

Actions Taken:
- Rolled back deployment v2.3.4 → v2.3.3
- Scaled service from 5 → 10 replicas

Next Steps:
- Continuing to monitor
- Root cause analysis in progress

ETA to Resolution: ~15 minutes
```

### Resolution Notification
```
✅ RESOLVED: Payment Service Incident

Duration: 45 minutes
Impact: ~5,000 affected transactions
Root Cause: Memory leak in v2.3.4

Resolution:
- Rolled back to v2.3.3
- Transactions auto-retried successfully

Follow-up:
- Postmortem scheduled for [DATE]
- Bug fix in progress
```
```

### 模板 2：数据库事件 Runbook

```markdown
# Database Incident Runbook

## Quick Reference
| Issue | Command |
|-------|---------|
| Check connections | `SELECT count(*) FROM pg_stat_activity;` |
| Kill query | `SELECT pg_terminate_backend(pid);` |
| Check replication lag | `SELECT extract(epoch from (now() - pg_last_xact_replay_timestamp()));` |
| Check locks | `SELECT * FROM pg_locks WHERE NOT granted;` |

## Connection Pool Exhaustion
```sql
-- Check current connections
SELECT datname, usename, state, count(*)
FROM pg_stat_activity
GROUP BY datname, usename, state
ORDER BY count(*) DESC;

-- Identify long-running connections
SELECT pid, usename, datname, state, query_start, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- Terminate idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND query_start < now() - interval '10 minutes';
```

## Replication Lag
```sql
-- Check lag on replica
SELECT
  CASE
    WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN 0
    ELSE extract(epoch from now() - pg_last_xact_replay_timestamp())
  END AS lag_seconds;

-- If lag > 60s, consider:
-- 1. Check network between primary/replica
-- 2. Check replica disk I/O
-- 3. Consider failover if unrecoverable
```

## Disk Space Critical
```bash
# Check disk usage
df -h /var/lib/postgresql/data

# Find large tables
psql -c "SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;"

# VACUUM to reclaim space
psql -c "VACUUM FULL large_table;"

# If emergency, delete old data or expand disk
```
```

## 最佳实践

### 应该做的
- **保持 Runbook 更新** — 每次事件后都要复盘修订
- **定期测试 Runbook** — 演练日、混沌工程
- **包含回滚步骤** — 始终留有退路
- **记录前提假设** — 明确步骤生效所需的条件
- **链接到仪表盘** — 高压时快速访问

### 不应该做的
- **不要假设知识** — 按凌晨 3 点的大脑水平来写
- **不要跳过验证** — 确认每一步都生效了
- **不要忘记沟通** — 保持利益相关方知情
- **不要独自作战** — 尽早升级
- **不要跳过复盘** — 从每次事件中学习

## 参考资源

- [Google SRE Book - Incident Management](https://sre.google/sre-book/managing-incidents/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Atlassian Incident Management](https://www.atlassian.com/incident-management)

## 局限性
- 仅当任务明确匹配上述范围时使用本技能
- 输出内容不能替代针对具体环境的验证、测试或专家审查
- 如缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清
