---
name: application-performance-performance-optimization
description: "通过性能分析、可观测性和后端/前端调优优化端到端应用性能。当用户要求'性能优化''应用性能调优''端到端性能优化'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

使用专业的性能和优化智能体，端到端优化应用性能：

[扩展思考：本工作流编排了一个跨越整个应用栈的综合性能优化流程。从深度性能分析和基线建立开始，工作流逐步推进到各系统层的针对性优化，通过负载测试验证改进效果，并建立持续监控以维持性能。每个阶段都基于前一阶段的洞察，创建数据驱动的优化策略，解决真实瓶颈而非理论上的改进。工作流强调现代可观测性实践、以用户为中心的性能指标和成本效益优化策略。]

## 使用此技能的场景

- 协调后端、前端和基础设施的跨栈性能优化
- 建立基线和性能分析以识别瓶颈
- 设计负载测试、性能预算或容量规划
- 为性能和可靠性目标构建可观测性

## 不使用此技能的场景

- 任务是局部小修复，没有更广泛的性能目标
- 无法访问指标、链路追踪或性能分析数据
- 请求与性能或可扩展性无关

## 指令

1. 确认性能目标、约束和目标指标。
2. 通过性能分析、链路追踪和真实用户数据建立基线。
3. 跨栈执行分阶段优化，确保影响可度量。
4. 验证改进效果并设置防护措施以防止回归。

## 安全

- 避免在未经审批和保障措施的情况下对生产环境进行负载测试。
- 逐步推出性能变更，并准备回滚方案。

## 阶段 1：性能分析与基线

### 1. 综合性能分析

- 使用 Task 工具，subagent_type="performance-engineer"
- 提示词："Profile application performance comprehensively for: $ARGUMENTS. Generate flame graphs for CPU usage, heap dumps for memory analysis, trace I/O operations, and identify hot paths. Use APM tools like DataDog or New Relic if available. Include database query profiling, API response times, and frontend rendering metrics. Establish performance baselines for all critical user journeys."
- 上下文：初始性能调查
- 输出：包含火焰图、内存分析、瓶颈识别和基线指标的详细性能报告

### 2. 可观测性栈评估

- 使用 Task 工具，subagent_type="observability-engineer"
- 提示词："Assess current observability setup for: $ARGUMENTS. Review existing monitoring, distributed tracing with OpenTelemetry, log aggregation, and metrics collection. Identify gaps in visibility, missing metrics, and areas needing better instrumentation. Recommend APM tool integration and custom metrics for business-critical operations."
- 上下文：步骤 1 的性能分析结果
- 输出：可观测性评估报告、埋点缺口、监控建议

### 3. 用户体验分析

- 使用 Task 工具，subagent_type="performance-engineer"
- 提示词："Analyze user experience metrics for: $ARGUMENTS. Measure Core Web Vitals (LCP, FID, CLS), page load times, time to interactive, and perceived performance. Use Real User Monitoring (RUM) data if available. Identify user journeys with poor performance and their business impact."
- 上下文：步骤 1 的性能基线
- 输出：UX 性能报告、Core Web Vitals 分析、用户影响评估

## 阶段 2：数据库与后端优化

### 4. 数据库性能优化

- 使用 Task 工具，subagent_type="database-cloud-optimization::database-optimizer"
- 提示词："Optimize database performance for: $ARGUMENTS based on profiling data: {context_from_phase_1}. Analyze slow query logs, create missing indexes, optimize execution plans, implement query result caching with Redis/Memcached. Review connection pooling, prepared statements, and batch processing opportunities. Consider read replicas and database sharding if needed."
- 上下文：阶段 1 的性能瓶颈
- 输出：优化后的查询、新建索引、缓存策略、连接池配置

### 5. 后端代码与 API 优化

- 使用 Task 工具，subagent_type="backend-development::backend-architect"
- 提示词："Optimize backend services for: $ARGUMENTS targeting bottlenecks: {context_from_phase_1}. Implement efficient algorithms, add application-level caching, optimize N+1 queries, use async/await patterns effectively. Implement pagination, response compression, GraphQL query optimization, and batch API operations. Add circuit breakers and bulkheads for resilience."
- 上下文：步骤 4 的数据库优化、阶段 1 的性能分析数据
- 输出：优化后的后端代码、缓存实现、API 改进、弹性模式

### 6. 微服务与分布式系统优化

- 使用 Task 工具，subagent_type="performance-engineer"
- 提示词："Optimize distributed system performance for: $ARGUMENTS. Analyze service-to-service communication, implement service mesh optimizations, optimize message queue performance (Kafka/RabbitMQ), reduce network hops. Implement distributed caching strategies and optimize serialization/deserialization."
- 上下文：步骤 5 的后端优化
- 输出：服务通信改进、消息队列优化、分布式缓存配置

## 阶段 3：前端与 CDN 优化

### 7. 前端打包与加载优化

- 使用 Task 工具，subagent_type="frontend-developer"
- 提示词："Optimize frontend performance for: $ARGUMENTS targeting Core Web Vitals: {context_from_phase_1}. Implement code splitting, tree shaking, lazy loading, and dynamic imports. Optimize bundle sizes with webpack/rollup analysis. Implement resource hints (prefetch, preconnect, preload). Optimize critical rendering path and eliminate render-blocking resources."
- 上下文：阶段 1 的 UX 分析、阶段 2 的后端优化
- 输出：优化后的打包、懒加载实现、改善的 Core Web Vitals

### 8. CDN 与边缘优化

- 使用 Task 工具，subagent_type="cloud-infrastructure::cloud-architect"
- 提示词："Optimize CDN and edge performance for: $ARGUMENTS. Configure CloudFlare/CloudFront for optimal caching, implement edge functions for dynamic content, set up image optimization with responsive images and WebP/AVIF formats. Configure HTTP/2 and HTTP/3, implement Brotli compression. Set up geographic distribution for global users."
- 上下文：步骤 7 的前端优化
- 输出：CDN 配置、边缘缓存规则、压缩设置、地理优化

### 9. 移动端与渐进式 Web 应用优化

- 使用 Task 工具，subagent_type="frontend-mobile-development::mobile-developer"
- 提示词："Optimize mobile experience for: $ARGUMENTS. Implement service workers for offline functionality, optimize for slow networks with adaptive loading. Reduce JavaScript execution time for mobile CPUs. Implement virtual scrolling for long lists. Optimize touch responsiveness and smooth animations. Consider React Native/Flutter specific optimizations if applicable."
- 上下文：步骤 7-8 的前端优化
- 输出：移动端优化代码、PWA 实现、离线功能

## 阶段 4：负载测试与验证

### 10. 综合负载测试

- 使用 Task 工具，subagent_type="performance-engineer"
- 提示词："Conduct comprehensive load testing for: $ARGUMENTS using k6/Gatling/Artillery. Design realistic load scenarios based on production traffic patterns. Test normal load, peak load, and stress scenarios. Include API testing, browser-based testing, and WebSocket testing if applicable. Measure response times, throughput, error rates, and resource utilization at various load levels."
- 上下文：阶段 1-3 的所有优化
- 输出：负载测试结果、负载下的性能表现、断裂点、可扩展性分析

### 11. 性能回归测试

- 使用 Task 工具，subagent_type="performance-testing-review::test-automator"
- 提示词："Create automated performance regression tests for: $ARGUMENTS. Set up performance budgets for key metrics, integrate with CI/CD pipeline using GitHub Actions or similar. Create Lighthouse CI tests for frontend, API performance tests with Artillery, and database performance benchmarks. Implement automatic rollback triggers for performance regressions."
- 上下文：步骤 10 的负载测试结果、阶段 1 的基线指标
- 输出：性能测试套件、CI/CD 集成、回归防护系统

## 阶段 5：监控与持续优化

### 12. 生产环境监控配置

- 使用 Task 工具，subagent_type="observability-engineer"
- 提示词："Implement production performance monitoring for: $ARGUMENTS. Set up APM with DataDog/New Relic/Dynatrace, configure distributed tracing with OpenTelemetry, implement custom business metrics. Create Grafana dashboards for key metrics, set up PagerDuty alerts for performance degradation. Define SLIs/SLOs for critical services with error budgets."
- 上下文：所有先前阶段的性能改进
- 输出：监控仪表盘、告警规则、SLI/SLO 定义、运维手册

### 13. 持续性能优化

- 使用 Task 工具，subagent_type="performance-engineer"
- 提示词："Establish continuous optimization process for: $ARGUMENTS. Create performance budget tracking, implement A/B testing for performance changes, set up continuous profiling in production. Document optimization opportunities backlog, create capacity planning models, and establish regular performance review cycles."
- 上下文：步骤 12 的监控配置、所有先前的优化工作
- 输出：性能预算跟踪、优化待办列表、容量规划、评审流程

## 配置选项

- **performance_focus**: "latency" | "throughput" | "cost" | "balanced"（默认值："balanced"）
- **optimization_depth**: "quick-wins" | "comprehensive" | "enterprise"（默认值："comprehensive"）
- **tools_available**: ["datadog", "newrelic", "prometheus", "grafana", "k6", "gatling"]
- **budget_constraints**: 为基础设施变更设置最大可接受成本
- **user_impact_tolerance**: "zero-downtime" | "maintenance-window" | "gradual-rollout"

## 成功标准

- **响应时间**：关键端点 P50 < 200ms，P95 < 1s，P99 < 2s
- **Core Web Vitals**：LCP < 2.5s，FID < 100ms，CLS < 0.1
- **吞吐量**：支持 2 倍当前峰值负载，错误率 < 1%
- **数据库性能**：查询 P95 < 100ms，无超过 1s 的查询
- **资源利用率**：正常负载下 CPU < 70%，内存 < 80%
- **成本效率**：每美元性能提升至少 30%
- **监控覆盖率**：100% 的关键路径已埋点并配置告警

性能优化目标：$ARGUMENTS

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代方案。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
