---
name: data-engineering-data-driven-feature
description: "使用专业智能体进行数据分析、实现和实验，以数据洞察、A/B 测试和持续测量为指导构建功能。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 数据驱动功能开发

使用专业智能体进行数据分析、实现和实验，以数据洞察、A/B 测试和持续测量为指导构建功能。

[扩展思考：此工作流编排了一个全面的数据驱动开发流程，从初始数据分析和假设形成，到带有集成分析、A/B 测试基础设施和发布后分析的功能实现。每个阶段都利用专业智能体确保功能基于数据洞察构建、正确配置测量工具，并通过受控实验验证。工作流强调现代产品分析实践、测试中的统计严谨性，以及从用户行为中持续学习。]

## 使用此技能的场景

- 处理数据驱动功能开发任务或工作流
- 需要数据驱动功能开发的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与数据驱动功能开发无关
- 需要此范围之外的不同领域或工具

## 指令

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 第一阶段：数据分析和假设形成

### 1. 探索性数据分析
- 使用 Task 工具，subagent_type="machine-learning-ops::data-scientist"
- 提示词："Perform exploratory data analysis for feature: $ARGUMENTS. Analyze existing user behavior data, identify patterns and opportunities, segment users by behavior, and calculate baseline metrics. Use modern analytics tools (Amplitude, Mixpanel, Segment) to understand current user journeys, conversion funnels, and engagement patterns."
- 输出：带有可视化、用户细分、行为模式、基准指标的 EDA 报告

### 2. 业务假设开发
- 使用 Task 工具，subagent_type="business-analytics::business-analyst"
- 上下文：数据科学家的 EDA 发现和行为模式
- 提示词："Formulate business hypotheses for feature: $ARGUMENTS based on data analysis. Define clear success metrics, expected impact on key business KPIs, target user segments, and minimum detectable effects. Create measurable hypotheses using frameworks like ICE scoring or RICE prioritization."
- 输出：假设文档、成功指标定义、预期 ROI 计算

### 3. 统计实验设计
- 使用 Task 工具，subagent_type="machine-learning-ops::data-scientist"
- 上下文：业务假设和成功指标
- 提示词："Design statistical experiment for feature: $ARGUMENTS. Calculate required sample size for statistical power, define control and treatment groups, specify randomization strategy, and plan for multiple testing corrections. Consider Bayesian A/B testing approaches for faster decision making. Design for both primary and guardrail metrics."
- 输出：实验设计文档、功效分析、统计测试计划

## 第二阶段：功能架构和分析设计

### 4. 功能架构规划
- 使用 Task 工具，subagent_type="data-engineering::backend-architect"
- 上下文：业务需求和实验设计
- 提示词："Design feature architecture for: $ARGUMENTS with A/B testing capability. Include feature flag integration (LaunchDarkly, Split.io, or Optimizely), gradual rollout strategy, circuit breakers for safety, and clean separation between control and treatment logic. Ensure architecture supports real-time configuration updates."
- 输出：架构图、功能开关模式、发布策略

### 5. 分析埋点设计
- 使用 Task 工具，subagent_type="data-engineering::data-engineer"
- 上下文：功能架构和成功指标
- 提示词："Design comprehensive analytics instrumentation for: $ARGUMENTS. Define event schemas for user interactions, specify properties for segmentation and analysis, design funnel tracking and conversion events, plan cohort analysis capabilities. Implement using modern SDKs (Segment, Amplitude, Mixpanel) with proper event taxonomy."
- 输出：事件追踪计划、分析模式、埋点指南

### 6. 数据管道架构
- 使用 Task 工具，subagent_type="data-engineering::data-engineer"
- 上下文：分析需求和现有数据基础设施
- 提示词："Design data pipelines for feature: $ARGUMENTS. Include real-time streaming for live metrics (Kafka, Kinesis), batch processing for detailed analysis, data warehouse integration (Snowflake, BigQuery), and feature store for ML if applicable. Ensure proper data governance and GDPR compliance."
- 输出：管道架构、ETL/ELT 规范、数据流图

## 第三阶段：带埋点的实现

### 7. 后端实现
- 使用 Task 工具，subagent_type="backend-development::backend-architect"
- 上下文：架构设计和功能需求
- 提示词："Implement backend for feature: $ARGUMENTS with full instrumentation. Include feature flag checks at decision points, comprehensive event tracking for all user actions, performance metrics collection, error tracking and monitoring. Implement proper logging for experiment analysis."
- 输出：带分析的后端代码、功能开关集成、监控设置

### 8. 前端实现
- 使用 Task 工具，subagent_type="frontend-mobile-development::frontend-developer"
- 上下文：后端 API 和分析需求
- 提示词："Build frontend for feature: $ARGUMENTS with analytics tracking. Implement event tracking for all user interactions, session recording integration if applicable, performance metrics (Core Web Vitals), and proper error boundaries. Ensure consistent experience between control and treatment groups."
- 输出：带分析的前端代码、A/B 测试变体、性能监控

### 9. ML 模型集成（如适用）
- 使用 Task 工具，subagent_type="machine-learning-ops::ml-engineer"
- 上下文：功能需求和数据管道
- 提示词："Integrate ML models for feature: $ARGUMENTS if needed. Implement online inference with low latency, A/B testing between model versions, model performance tracking, and automatic fallback mechanisms. Set up model monitoring for drift detection."
- 输出：ML 管道、模型服务基础设施、监控设置

## 第四阶段：发布前验证

### 10. 分析验证
- 使用 Task 工具，subagent_type="data-engineering::data-engineer"
- 上下文：已实现的追踪和事件模式
- 提示词："Validate analytics implementation for: $ARGUMENTS. Test all event tracking in staging, verify data quality and completeness, validate funnel definitions, ensure proper user identification and session tracking. Run end-to-end tests for data pipeline."
- 输出：验证报告、数据质量指标、追踪覆盖率分析

### 11. 实验设置
- 使用 Task 工具，subagent_type="cloud-infrastructure::deployment-engineer"
- 上下文：功能开关和实验设计
- 提示词："Configure experiment infrastructure for: $ARGUMENTS. Set up feature flags with proper targeting rules, configure traffic allocation (start with 5-10%), implement kill switches, set up monitoring alerts for key metrics. Test randomization and assignment logic."
- 输出：实验配置、监控仪表板、发布计划

## 第五阶段：发布和实验

### 12. 渐进式发布
- 使用 Task 工具，subagent_type="cloud-infrastructure::deployment-engineer"
- 上下文：实验配置和监控设置
- 提示词："Execute gradual rollout for feature: $ARGUMENTS. Start with internal dogfooding, then beta users (1-5%), gradually increase to target traffic. Monitor error rates, performance metrics, and early indicators. Implement automated rollback on anomalies."
- 输出：发布执行、监控告警、健康指标

### 13. 实时监控
- 使用 Task 工具，subagent_type="observability-monitoring::observability-engineer"
- 上下文：已部署功能和成功指标
- 提示词："Set up comprehensive monitoring for: $ARGUMENTS. Create real-time dashboards for experiment metrics, configure alerts for statistical significance, monitor guardrail metrics for negative impacts, track system performance and error rates. Use tools like Datadog, New Relic, or custom dashboards."
- 输出：监控仪表板、告警配置、SLO 定义

## 第六阶段：分析和决策

### 14. 统计分析
- 使用 Task 工具，subagent_type="machine-learning-ops::data-scientist"
- 上下文：实验数据和原始假设
- 提示词："Analyze A/B test results for: $ARGUMENTS. Calculate statistical significance with confidence intervals, check for segment-level effects, analyze secondary metrics impact, investigate any unexpected patterns. Use both frequentist and Bayesian approaches. Account for multiple testing if applicable."
- 输出：统计分析报告、显著性检验、细分分析

### 15. 业务影响评估
- 使用 Task 工具，subagent_type="business-analytics::business-analyst"
- 上下文：统计分析和业务指标
- 提示词："Assess business impact of feature: $ARGUMENTS. Calculate actual vs expected ROI, analyze impact on key business metrics, evaluate cost-benefit including operational overhead, project long-term value. Make recommendation on full rollout, iteration, or rollback."
- 输出：业务影响报告、ROI 分析、建议文档

### 16. 发布后优化
- 使用 Task 工具，subagent_type="machine-learning-ops::data-scientist"
- 上下文：发布结果和用户反馈
- 提示词："Identify optimization opportunities for: $ARGUMENTS based on data. Analyze user behavior patterns in treatment group, identify friction points in user journey, suggest improvements based on data, plan follow-up experiments. Use cohort analysis for long-term impact."
- 输出：优化建议、后续实验计划

## 配置选项

```yaml
experiment_config:
  min_sample_size: 10000
  confidence_level: 0.95
  runtime_days: 14
  traffic_allocation: "gradual"  # gradual, fixed, or adaptive

analytics_platforms:
  - amplitude
  - segment
  - mixpanel

feature_flags:
  provider: "launchdarkly"  # launchdarkly, split, optimizely, unleash

statistical_methods:
  - frequentist
  - bayesian

monitoring:
  - real_time_metrics: true
  - anomaly_detection: true
  - automatic_rollback: true
```

## 成功标准

- **数据覆盖率**：100% 的用户交互使用正确的事件模式追踪
- **实验有效性**：正确的随机化、足够的统计功效、无样本比例不匹配
- **统计严谨性**：清晰的显著性检验、正确的置信区间、多重检验校正
- **业务影响**：目标指标可衡量的改进，且不降低护栏指标
- **技术性能**：p95 延迟无退化，错误率低于 0.1%
- **决策速度**：在计划的实验运行时间内做出明确的通过/不通过决策
- **学习成果**：为未来功能开发记录的洞察

## 协调说明

- 数据科学家和业务分析师协作进行假设形成
- 工程师实现时将分析作为一等需求，而非事后补充
- 功能开关实现安全实验，无需完整部署
- 实时监控允许快速迭代和必要时回滚
- 统计严谨性与业务实用性和上市速度相平衡
- 持续学习循环反馈到下一个功能开发周期

使用数据驱动方法开发的功能：$ARGUMENTS

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
