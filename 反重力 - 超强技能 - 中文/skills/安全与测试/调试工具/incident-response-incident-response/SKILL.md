---
name: incident-response-incident-response
description: "使用现代 SRE 实践编排多智能体事件响应，实现快速恢复与经验沉淀。当用户要求'事件响应'、'incident response'、'故障响应'、'生产事故处理'、'应急响应'、'故障排查流程'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

## 使用此技能的场景

- 处理事件响应相关任务或工作流
- 需要事件响应的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与事件响应无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

使用现代 SRE 实践编排多智能体事件响应，实现快速恢复与经验沉淀：

[扩展思考：本工作流实现了遵循现代 SRE 原则的综合事件指挥系统（ICS）。多个专业智能体通过定义的阶段协作：检测/分流、调查/缓解、沟通/协调、解决/复盘。工作流强调速度但不牺牲准确性，维护清晰的沟通渠道，并通过无责复盘和系统性改进确保每个事件都成为学习机会。]

## 配置

### 严重等级
- **P0/SEV-1**：完全宕机、安全漏洞、数据丢失 — 全员立即响应
- **P1/SEV-2**：严重降级、重大用户影响 — 快速响应
- **P2/SEV-3**：轻微降级、有限影响 — 标准响应
- **P3/SEV-4**：外观问题、无用户影响 — 计划解决

### 事件类型
- 性能降级
- 服务中断
- 安全事件
- 数据完整性问题
- 基础设施故障
- 第三方服务中断

## 阶段 1：检测与分流

### 1. 事件检测与分类
- 使用 Task 工具，subagent_type="incident-responder"
- 提示词："URGENT: Detect and classify incident: $ARGUMENTS. Analyze alerts from PagerDuty/Opsgenie/monitoring. Determine: 1) Incident severity (P0-P3), 2) Affected services and dependencies, 3) User impact and business risk, 4) Initial incident command structure needed. Check error budgets and SLO violations."
- 输出：严重等级分类、影响评估、事件指挥分配、SLO 状态
- 上下文：初始告警、监控仪表盘、近期变更

### 2. 可观测性分析
- 使用 Task 工具，subagent_type="observability-monitoring::observability-engineer"
- 提示词："Perform rapid observability sweep for incident: $ARGUMENTS. Query: 1) Distributed tracing (OpenTelemetry/Jaeger), 2) Metrics correlation (Prometheus/Grafana/DataDog), 3) Log aggregation (ELK/Splunk), 4) APM data, 5) Real User Monitoring. Identify anomalies, error patterns, and service degradation points."
- 输出：可观测性发现、异常检测、服务健康矩阵、链路分析
- 上下文：步骤 1 的严重等级、受影响服务

### 3. 初始缓解
- 使用 Task 工具，subagent_type="incident-responder"
- 提示词："Implement immediate mitigation for P$SEVERITY incident: $ARGUMENTS. Actions: 1) Traffic throttling/rerouting if needed, 2) Feature flag disabling for affected features, 3) Circuit breaker activation, 4) Rollback assessment for recent deployments, 5) Scale resources if capacity-related. Prioritize user experience restoration."
- 输出：已执行的缓解措施、已应用的临时修复、回滚决策
- 上下文：可观测性发现、严重等级分类

## 阶段 2：调查与根因分析

### 4. 深度系统调试
- 使用 Task 工具，subagent_type="error-debugging::debugger"
- 提示词："Conduct deep debugging for incident: $ARGUMENTS using observability data. Investigate: 1) Stack traces and error logs, 2) Database query performance and locks, 3) Network latency and timeouts, 4) Memory leaks and CPU spikes, 5) Dependency failures and cascading errors. Apply Five Whys analysis."
- 输出：根因识别、促成因素、依赖影响图
- 上下文：可观测性分析、缓解状态

### 5. 安全评估
- 使用 Task 工具，subagent_type="security-scanning::security-auditor"
- 提示词："Assess security implications of incident: $ARGUMENTS. Check: 1) DDoS attack indicators, 2) Authentication/authorization failures, 3) Data exposure risks, 4) Certificate issues, 5) Suspicious access patterns. Review WAF logs, security groups, and audit trails."
- 输出：安全评估、入侵分析、漏洞识别
- 上下文：根因发现、系统日志

### 6. 性能工程分析
- 使用 Task 工具，subagent_type="application-performance::performance-engineer"
- 提示词："Analyze performance aspects of incident: $ARGUMENTS. Examine: 1) Resource utilization patterns, 2) Query optimization opportunities, 3) Caching effectiveness, 4) Load balancer health, 5) CDN performance, 6) Autoscaling triggers. Identify bottlenecks and capacity issues."
- 输出：性能瓶颈、资源建议、优化机会
- 上下文：调试发现、当前缓解状态

## 阶段 3：解决与恢复

### 7. 修复实施
- 使用 Task 工具，subagent_type="backend-development::backend-architect"
- 提示词："Design and implement production fix for incident: $ARGUMENTS based on root cause. Requirements: 1) Minimal viable fix for rapid deployment, 2) Risk assessment and rollback capability, 3) Staged rollout plan with monitoring, 4) Validation criteria and health checks. Consider both immediate fix and long-term solution."
- 输出：修复实现、部署策略、验证计划、回滚流程
- 上下文：根因分析、性能发现、安全评估

### 8. 部署与验证
- 使用 Task 工具，subagent_type="deployment-strategies::deployment-engineer"
- 提示词："Execute emergency deployment for incident fix: $ARGUMENTS. Process: 1) Blue-green or canary deployment, 2) Progressive rollout with monitoring, 3) Health check validation at each stage, 4) Rollback triggers configured, 5) Real-time monitoring during deployment. Coordinate with incident command."
- 输出：部署状态、验证结果、监控仪表盘、回滚就绪状态
- 上下文：修复实现、当前系统状态

## 阶段 4：沟通与协调

### 9. 利益相关方沟通
- 使用 Task 工具，subagent_type="content-marketing::content-marketer"
- 提示词："Manage incident communication for: $ARGUMENTS. Create: 1) Status page updates (public-facing), 2) Internal engineering updates (technical details), 3) Executive summary (business impact/ETA), 4) Customer support briefing (talking points), 5) Timeline documentation with key decisions. Update every 15-30 minutes based on severity."
- 输出：沟通产物、状态更新、利益相关方简报、时间线日志
- 上下文：所有前序阶段、当前解决状态

### 10. 客户影响评估
- 使用 Task 工具，subagent_type="incident-responder"
- 提示词："Assess and document customer impact for incident: $ARGUMENTS. Analyze: 1) Affected user segments and geography, 2) Failed transactions or data loss, 3) SLA violations and contractual implications, 4) Customer support ticket volume, 5) Revenue impact estimation. Prepare proactive customer outreach list."
- 输出：客户影响报告、SLA 分析、主动触达建议
- 上下文：解决进展、沟通状态

## 阶段 5：复盘与预防

### 11. 无责复盘
- 使用 Task 工具，subagent_type="documentation-generation::docs-architect"
- 提示词："Conduct blameless postmortem for incident: $ARGUMENTS. Document: 1) Complete incident timeline with decisions, 2) Root cause and contributing factors (systems focus), 3) What went well in response, 4) What could improve, 5) Action items with owners and deadlines, 6) Lessons learned for team education. Follow SRE postmortem best practices."
- 输出：复盘文档、行动项列表、流程改进、培训需求
- 上下文：完整事件历史、所有智能体输出

### 12. 监控与告警增强
- 使用 Task 工具，subagent_type="observability-monitoring::observability-engineer"
- 提示词："Enhance monitoring to prevent recurrence of: $ARGUMENTS. Implement: 1) New alerts for early detection, 2) SLI/SLO adjustments if needed, 3) Dashboard improvements for visibility, 4) Runbook automation opportunities, 5) Chaos engineering scenarios for testing. Ensure alerts are actionable and reduce noise."
- 输出：新监控配置、告警规则、仪表盘更新、Runbook 自动化
- 上下文：复盘发现、根因分析

### 13. 系统加固
- 使用 Task 工具，subagent_type="backend-development::backend-architect"
- 提示词："Design system improvements to prevent incident: $ARGUMENTS. Propose: 1) Architecture changes for resilience (circuit breakers, bulkheads), 2) Graceful degradation strategies, 3) Capacity planning adjustments, 4) Technical debt prioritization, 5) Dependency reduction opportunities. Create implementation roadmap."
- 输出：架构改进、韧性模式、技术债务项、实施路线图
- 上下文：复盘行动项、性能分析

## 成功标准

### 即时成功（事件期间）
- 在 SLA 目标内恢复服务
- 5 分钟内完成准确的严重等级分类
- 每 15-30 分钟更新利益相关方沟通
- 无级联故障或事件升级
- 维持清晰的事件指挥结构

### 长期成功（事件后）
- 48 小时内完成全面复盘
- 所有行动项已分配负责人和截止日期
- 1 周内部署监控改进
- 完成 Runbook 更新
- 基于经验教训开展团队培训
- 评估并沟通错误预算影响

## 协调协议

### 事件指挥结构
- **事件指挥官**：决策权威、协调
- **技术负责人**：技术调查与解决
- **沟通负责人**：利益相关方更新
- **领域专家**：特定系统专长

### 沟通渠道
- 作战室（Slack/Teams 频道或 Zoom）
- 状态页更新（StatusPage、Statusly）
- PagerDuty/Opsgenie 告警
- Confluence/Notion 文档

### 交接要求
- 每个阶段为下一阶段提供清晰的上下文
- 所有发现记录在共享事件文档中
- 决策理由记录以供复盘
- 为所有重要事件添加时间戳

需要立即响应的生产事件：$ARGUMENTS

## 局限性
- 仅当任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家审查的替代
- 如果缺少所需输入、权限、安全边界或成功标准，停下来请求澄清
