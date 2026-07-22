---
name: backend-development-feature-development
description: "编排从需求到部署的端到端后端功能开发。当用户要求'协调跨团队和服务的多阶段功能交付'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

编排从需求到生产部署的端到端功能开发：

[扩展思考：本工作流通过专业智能体编排全面的功能开发阶段——从发现和规划到实现、测试和部署。每个阶段基于前一阶段的输出构建，确保功能交付的连贯性。工作流支持多种开发方法论（传统、TDD/BDD、DDD）、功能复杂度级别，以及现代部署策略，包括功能标志、渐进式发布和可观测性优先开发。智能体接收来自前序阶段的详细上下文，以在整个开发生命周期中保持一致性和质量。]

## 使用此技能的场景

- 协调跨后端、前端和数据团队的端到端功能交付
- 管理需求、架构、实现、测试和发布
- 规划需要部署和监控的多服务变更
- 在范围、风险和成功指标上对齐团队

## 不使用此技能的场景

- 任务是小型、独立的后端变更或 Bug 修复
- 只需要单一专业任务，而非完整工作流
- 不涉及部署或跨团队协调

## 指令

1. 确认功能范围、成功指标和约束条件。
2. 选择方法论并定义各阶段输出。
3. 编排实现、测试和安全验证。
4. 准备发布、监控和文档计划。

## 安全

- 避免未经审批和回滚计划的生产环境变更。
- 先在预发布环境中验证数据迁移和功能标志。

## 配置选项

### 开发方法论

- **traditional**：顺序开发，实现后测试
- **tdd**：测试驱动开发，红-绿-重构循环
- **bdd**：行为驱动开发，基于场景的测试
- **ddd**：领域驱动设计，限界上下文和聚合

### 功能复杂度

- **simple**：单一服务，最小集成（1-2 天）
- **medium**：多服务，适度集成（3-5 天）
- **complex**：跨领域，广泛集成（1-2 周）
- **epic**：重大架构变更，多团队（2+ 周）

### 部署策略

- **direct**：立即向所有用户发布
- **canary**：从 5% 流量开始的渐进式发布
- **feature-flag**：通过功能开关控制激活
- **blue-green**：零停机部署，支持即时回滚
- **a-b-test**：分流流量进行实验和指标对比

## 阶段 1：发现与需求规划

1. **业务分析与需求**
   - 使用 Task 工具，subagent_type="business-analytics::business-analyst"
   - 提示词："Analyze feature requirements for: $ARGUMENTS. Define user stories, acceptance criteria, success metrics, and business value. Identify stakeholders, dependencies, and risks. Create feature specification document with clear scope boundaries."
   - 预期输出：包含用户故事、成功指标、风险评估的需求文档
   - 上下文：初始功能请求和业务背景

2. **技术架构设计**
   - 使用 Task 工具，subagent_type="comprehensive-review::architect-review"
   - 提示词："Design technical architecture for feature: $ARGUMENTS. Using requirements: [include business analysis from step 1]. Define service boundaries, API contracts, data models, integration points, and technology stack. Consider scalability, performance, and security requirements."
   - 预期输出：包含架构图、API 规范、数据模型的技术设计文档
   - 上下文：业务需求、现有系统架构

3. **可行性与风险评估**
   - 使用 Task 工具，subagent_type="security-scanning::security-auditor"
   - 提示词："Assess security implications and risks for feature: $ARGUMENTS. Review architecture: [include technical design from step 2]. Identify security requirements, compliance needs, data privacy concerns, and potential vulnerabilities."
   - 预期输出：包含风险矩阵、合规检查清单、缓解策略的安全评估
   - 上下文：技术设计、法规要求

## 阶段 2：实现与开发

4. **后端服务实现**
   - 使用 Task 工具，subagent_type="backend-architect"
   - 提示词："Implement backend services for: $ARGUMENTS. Follow technical design: [include architecture from step 2]. Build RESTful/GraphQL APIs, implement business logic, integrate with data layer, add resilience patterns (circuit breakers, retries), implement caching strategies. Include feature flags for gradual rollout."
   - 预期输出：包含 API、业务逻辑、数据库集成、功能标志的后端服务
   - 上下文：技术设计、API 契约、数据模型

5. **前端实现**
   - 使用 Task 工具，subagent_type="frontend-mobile-development::frontend-developer"
   - 提示词："Build frontend components for: $ARGUMENTS. Integrate with backend APIs: [include API endpoints from step 4]. Implement responsive UI, state management, error handling, loading states, and analytics tracking. Add feature flag integration for A/B testing capabilities."
   - 预期输出：包含 API 集成、状态管理、分析的前端组件
   - 上下文：后端 API、UI/UX 设计、用户故事

6. **数据管道与集成**
   - 使用 Task 工具，subagent_type="data-engineering::data-engineer"
   - 提示词："Build data pipelines for: $ARGUMENTS. Design ETL/ELT processes, implement data validation, create analytics events, set up data quality monitoring. Integrate with product analytics platforms for feature usage tracking."
   - 预期输出：数据管道、分析事件、数据质量检查
   - 上下文：数据需求、分析需求、现有数据基础设施

## 阶段 3：测试与质量保证

7. **自动化测试套件**
   - 使用 Task 工具，subagent_type="unit-testing::test-automator"
   - 提示词："Create comprehensive test suite for: $ARGUMENTS. Write unit tests for backend: [from step 4] and frontend: [from step 5]. Add integration tests for API endpoints, E2E tests for critical user journeys, performance tests for scalability validation. Ensure minimum 80% code coverage."
   - 预期输出：包含单元测试、集成测试、E2E 测试和性能测试的测试套件
   - 上下文：实现代码、验收标准、测试需求

8. **安全验证**
   - 使用 Task 工具，subagent_type="security-scanning::security-auditor"
   - 提示词："Perform security testing for: $ARGUMENTS. Review implementation: [include backend and frontend from steps 4-5]. Run OWASP checks, penetration testing, dependency scanning, and compliance validation. Verify data encryption, authentication, and authorization."
   - 预期输出：安全测试结果、漏洞报告、修复措施
   - 上下文：实现代码、安全需求

9. **性能优化**
   - 使用 Task 工具，subagent_type="application-performance::performance-engineer"
   - 提示词："Optimize performance for: $ARGUMENTS. Analyze backend services: [from step 4] and frontend: [from step 5]. Profile code, optimize queries, implement caching, reduce bundle sizes, improve load times. Set up performance budgets and monitoring."
   - 预期输出：性能改进、优化报告、性能指标
   - 上下文：实现代码、性能需求

## 阶段 4：部署与监控

10. **部署策略与流水线**
    - 使用 Task 工具，subagent_type="deployment-strategies::deployment-engineer"
    - 提示词："Prepare deployment for: $ARGUMENTS. Create CI/CD pipeline with automated tests: [from step 7]. Configure feature flags for gradual rollout, implement blue-green deployment, set up rollback procedures. Create deployment runbook and rollback plan."
    - 预期输出：CI/CD 流水线、部署配置、回滚流程
    - 上下文：测试套件、基础设施需求、部署策略

11. **可观测性与监控**
    - 使用 Task 工具，subagent_type="observability-monitoring::observability-engineer"
    - 提示词："Set up observability for: $ARGUMENTS. Implement distributed tracing, custom metrics, error tracking, and alerting. Create dashboards for feature usage, performance metrics, error rates, and business KPIs. Set up SLOs/SLIs with automated alerts."
    - 预期输出：监控仪表盘、告警、SLO 定义、可观测性基础设施
    - 上下文：功能实现、成功指标、运维需求

12. **文档与知识传递**
    - 使用 Task 工具，subagent_type="documentation-generation::docs-architect"
    - 提示词："Generate comprehensive documentation for: $ARGUMENTS. Create API documentation, user guides, deployment guides, troubleshooting runbooks. Include architecture diagrams, data flow diagrams, and integration guides. Generate automated changelog from commits."
    - 预期输出：API 文档、用户指南、运维手册、架构文档
    - 上下文：所有前序阶段的输出

## 执行参数

### 必需参数

- **--feature**：功能名称和描述
- **--methodology**：开发方法（traditional|tdd|bdd|ddd）
- **--complexity**：功能复杂度级别（simple|medium|complex|epic）

### 可选参数

- **--deployment-strategy**：部署方式（direct|canary|feature-flag|blue-green|a-b-test）
- **--test-coverage-min**：最低测试覆盖率阈值（默认：80%）
- **--performance-budget**：性能要求（例如：<200ms 响应时间）
- **--rollout-percentage**：渐进式部署的初始发布百分比（默认：5%）
- **--feature-flag-service**：功能标志提供商（launchdarkly|split|unleash|custom）
- **--analytics-platform**：分析集成（segment|amplitude|mixpanel|custom）
- **--monitoring-stack**：可观测性工具（datadog|newrelic|grafana|custom）

## 成功标准

- 业务需求中的所有验收标准均已满足
- 测试覆盖率超过最低阈值（默认 80%）
- 安全扫描无严重漏洞
- 性能满足定义的预算和 SLO
- 功能标志已配置以支持受控发布
- 监控和告警完全运行
- 文档完整且已审批
- 成功部署到生产环境并具备回滚能力
- 产品分析跟踪功能使用情况
- A/B 测试指标已配置（如适用）

## 回滚策略

如果在部署期间或部署后出现问题：

1. 立即禁用功能标志（< 1 分钟）
2. 蓝绿流量切换（< 5 分钟）
3. 通过 CI/CD 完整部署回滚（< 15 分钟）
4. 如需要则回滚数据库迁移（与数据团队协调）
5. 事后复盘并在重新部署前修复

功能描述：$ARGUMENTS

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
