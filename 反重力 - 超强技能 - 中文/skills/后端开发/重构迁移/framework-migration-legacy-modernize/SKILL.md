---
name: framework-migration-legacy-modernize
description: "使用绞杀者无花果模式编排全面的遗留系统现代化，通过专家智能体协调实现过时组件的渐进式替换，同时保持业务持续运营。当用户要求'遗留系统现代化'、'遗留代码重构'、'系统迁移'、'legacy modernization'、'strangler fig'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 遗留代码现代化工作流

使用绞杀者无花果模式编排全面的遗留系统现代化，通过专家智能体协调实现过时组件的渐进式替换，同时保持业务持续运营。

[扩展思考：绞杀者无花果模式得名于热带无花果树，它会逐渐包裹并替换宿主，代表了风险可控的遗留系统现代化的黄金标准。本工作流实现了系统化方法，新功能逐步替换遗留组件，允许两个系统在过渡期间共存。通过编排评估、测试、安全和实现方面的专业智能体，我们确保每个迁移阶段在继续之前都经过验证，在最大化现代化速度的同时最小化干扰。]

## 使用此技能的场景

- 处理遗留代码现代化工作流任务或流程
- 需要遗留代码现代化工作流的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与遗留代码现代化工作流无关
- 需要此范围之外的其他领域或工具

## 指令

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，打开 `resources/implementation-playbook.md`。

## 阶段1：遗留系统评估与风险分析

### 1. 全面遗留系统分析
- 使用 Task 工具，subagent_type="legacy-modernizer"
- Prompt: "Analyze the legacy codebase at $ARGUMENTS. Document technical debt inventory including: outdated dependencies, deprecated APIs, security vulnerabilities, performance bottlenecks, and architectural anti-patterns. Generate a modernization readiness report with component complexity scores (1-10), dependency mapping, and database coupling analysis. Identify quick wins vs complex refactoring targets."
- 预期输出：包含风险矩阵和现代化优先级的详细评估报告

### 2. 依赖与集成映射
- 使用 Task 工具，subagent_type="architect-review"
- Prompt: "Based on the legacy assessment report, create a comprehensive dependency graph showing: internal module dependencies, external service integrations, shared database schemas, and cross-system data flows. Identify integration points that will require facade patterns or adapter layers during migration. Highlight circular dependencies and tight coupling that need resolution."
- 前置上下文：遗留系统评估报告、组件复杂度评分
- 预期输出：可视化依赖图和集成点目录

### 3. 业务影响与风险评估
- 使用 Task 工具，subagent_type="business-analytics::business-analyst"
- Prompt: "Evaluate business impact of modernizing each component identified. Create risk assessment matrix considering: business criticality (revenue impact), user traffic patterns, data sensitivity, regulatory requirements, and fallback complexity. Prioritize components using a weighted scoring system: (Business Value × 0.4) + (Technical Risk × 0.3) + (Quick Win Potential × 0.3). Define rollback strategies for each component."
- 前置上下文：组件清单、依赖映射
- 预期输出：包含风险缓解策略的优先级迁移路线图

## 阶段2：测试覆盖建立

### 1. 遗留代码测试覆盖分析
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- Prompt: "Analyze existing test coverage for legacy components at $ARGUMENTS. Use coverage tools to identify untested code paths, missing integration tests, and absent end-to-end scenarios. For components with <40% coverage, generate characterization tests that capture current behavior without modifying functionality. Create test harness for safe refactoring."
- 预期输出：测试覆盖率报告和特征测试套件

### 2. 契约测试实现
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- Prompt: "Implement contract tests for all integration points identified in dependency mapping. Create consumer-driven contracts for APIs, message queue interactions, and database schemas. Set up contract verification in CI/CD pipeline. Generate performance baselines for response times and throughput to validate modernized components maintain SLAs."
- 前置上下文：集成点目录、现有测试覆盖
- 预期输出：包含性能基线的契约测试套件

### 3. 测试数据管理策略
- 使用 Task 工具，subagent_type="data-engineering::data-engineer"
- Prompt: "Design test data management strategy for parallel system operation. Create data generation scripts for edge cases, implement data masking for sensitive information, and establish test database refresh procedures. Set up monitoring for data consistency between legacy and modernized components during migration."
- 前置上下文：数据库模式、测试需求
- 预期输出：测试数据管道和一致性监控

## 阶段3：增量迁移实施

### 1. 绞杀者无花果基础设施搭建
- 使用 Task 工具，subagent_type="backend-development::backend-architect"
- Prompt: "Implement strangler fig infrastructure with API gateway for traffic routing. Configure feature flags for gradual rollout using environment variables or feature management service. Set up proxy layer with request routing rules based on: URL patterns, headers, or user segments. Implement circuit breakers and fallback mechanisms for resilience. Create observability dashboard for dual-system monitoring."
- 预期输出：API gateway 配置、特性开关系统、监控仪表盘

### 2. 组件现代化 - 第一波
- 使用 Task 工具，subagent_type="python-development::python-pro" 或 "golang-pro"（根据目标技术栈）
- Prompt: "Modernize first-wave components (quick wins identified in assessment). For each component: extract business logic from legacy code, implement using modern patterns (dependency injection, SOLID principles), ensure backward compatibility through adapter patterns, maintain data consistency with event sourcing or dual writes. Follow 12-factor app principles. Components to modernize: [list from prioritized roadmap]"
- 前置上下文：特征测试、契约测试、基础设施搭建
- 预期输出：带适配器的现代化组件

### 3. 安全加固
- 使用 Task 工具，subagent_type="security-scanning::security-auditor"
- Prompt: "Audit modernized components for security vulnerabilities. Implement security improvements including: OAuth 2.0/JWT authentication, role-based access control, input validation and sanitization, SQL injection prevention, XSS protection, and secrets management. Verify OWASP top 10 compliance. Configure security headers and implement rate limiting."
- 前置上下文：现代化组件代码
- 预期输出：安全审计报告和加固后的组件

## 阶段4：性能验证与优化

### 1. 性能测试与优化
- 使用 Task 工具，subagent_type="application-performance::performance-engineer"
- Prompt: "Conduct performance testing comparing legacy vs modernized components. Run load tests simulating production traffic patterns, measure response times, throughput, and resource utilization. Identify performance regressions and optimize: database queries with indexing, caching strategies (Redis/Memcached), connection pooling, and async processing where applicable. Validate against SLA requirements."
- 前置上下文：性能基线、现代化组件
- 预期输出：性能测试结果和优化建议

### 2. 渐进式发布与监控
- 使用 Task 工具，subagent_type="deployment-strategies::deployment-engineer"
- Prompt: "Implement progressive rollout strategy using feature flags. Start with 5% traffic to modernized components, monitor error rates, latency, and business metrics. Define automatic rollback triggers: error rate >1%, latency >2x baseline, or business metric degradation. Create runbook for traffic shifting: 5% → 25% → 50% → 100% with 24-hour observation periods."
- 前置上下文：特性开关配置、监控仪表盘
- 预期输出：带自动保障措施的发布计划

## 阶段5：迁移完成与文档化

### 1. 遗留组件退役
- 使用 Task 工具，subagent_type="legacy-modernizer"
- Prompt: "Plan safe decommissioning of replaced legacy components. Verify no remaining dependencies through traffic analysis (minimum 30 days at 0% traffic). Archive legacy code with documentation of original functionality. Update CI/CD pipelines to remove legacy builds. Clean up unused database tables and remove deprecated API endpoints. Document any retained legacy components with sunset timeline."
- 前置上下文：流量路由数据、现代化状态
- 预期输出：退役检查清单和时间线

### 2. 文档与知识转移
- 使用 Task 工具，subagent_type="documentation-generation::docs-architect"
- Prompt: "Create comprehensive modernization documentation including: architectural diagrams (before/after), API documentation with migration guides, runbooks for dual-system operation, troubleshooting guides for common issues, and lessons learned report. Generate developer onboarding guide for modernized system. Document technical decisions and trade-offs made during migration."
- 前置上下文：所有迁移产物和决策
- 预期输出：完整的现代化文档包

## 配置选项

- **--parallel-systems**：无限期保持双系统运行（用于渐进式迁移）
- **--big-bang**：验证后完全切换（风险较高，完成更快）
- **--by-feature**：按完整功能而非技术组件迁移
- **--database-first**：优先进行数据库现代化，再处理应用层
- **--api-first**：现代化 API 层，同时保留遗留后端

## 成功标准

- 所有高优先级组件完成现代化，测试覆盖率 >80%
- 迁移期间零计划外停机
- 性能指标保持或提升（P95 延迟在基线的 110% 以内）
- 安全漏洞减少 >90%
- 技术债务评分改善 >60%
- 迁移后成功运行 30 天无回滚
- 完整文档支持新开发者在 <1 周内上手

目标：$ARGUMENTS

## 局限性
- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
