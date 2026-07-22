---
name: machine-learning-ops-ml-pipeline
description: "设计并实现完整的 ML 流水线：$ARGUMENTS。当用户要求'设计ML流水线'、'MLOps编排'、'机器学习管道'、'ML pipeline'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 机器学习流水线 - 多智能体 MLOps 编排

设计并实现完整的 ML 流水线：$ARGUMENTS

## 使用此技能的场景

- 处理机器学习流水线——多智能体 MLOps 编排相关的任务或工作流
- 需要机器学习流水线——多智能体 MLOps 编排的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与机器学习流水线——多智能体 MLOps 编排无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，打开 `resources/implementation-playbook.md`。

## 设计思路

本工作流编排多个专业智能体，遵循现代 MLOps 最佳实践构建生产级 ML 流水线。核心原则：

- **分阶段协调**：每个阶段基于前一阶段的输出构建，智能体之间有清晰的交接
- **现代工具集成**：MLflow/W&B 管理实验，Feast/Tecton 管理特征，KServe/Seldon 管理服务
- **生产优先思维**：每个组件都为规模、监控和可靠性而设计
- **可复现性**：数据、模型和基础设施均纳入版本控制
- **持续改进**：自动化重训练、A/B 测试和漂移检测

多智能体方式确保每个方面由领域专家处理：
- 数据工程师负责数据摄入和质量
- 数据科学家设计特征和实验
- ML 工程师实现训练流水线
- MLOps 工程师负责生产部署
- 可观测性工程师确保监控到位

## 阶段 1：数据与需求分析

<Task>
subagent_type: data-engineer
prompt: |
  Analyze and design data pipeline for ML system with requirements: $ARGUMENTS

  Deliverables:
  1. Data source audit and ingestion strategy:
     - Source systems and connection patterns
     - Schema validation using Pydantic/Great Expectations
     - Data versioning with DVC or lakeFS
     - Incremental loading and CDC strategies

  2. Data quality framework:
     - Profiling and statistics generation
     - Anomaly detection rules
     - Data lineage tracking
     - Quality gates and SLAs

  3. Storage architecture:
     - Raw/processed/feature layers
     - Partitioning strategy
     - Retention policies
     - Cost optimization

  Provide implementation code for critical components and integration patterns.
</Task>

<Task>
subagent_type: data-scientist
prompt: |
  Design feature engineering and model requirements for: $ARGUMENTS
  Using data architecture from: {phase1.data-engineer.output}

  Deliverables:
  1. Feature engineering pipeline:
     - Transformation specifications
     - Feature store schema (Feast/Tecton)
     - Statistical validation rules
     - Handling strategies for missing data/outliers

  2. Model requirements:
     - Algorithm selection rationale
     - Performance metrics and baselines
     - Training data requirements
     - Evaluation criteria and thresholds

  3. Experiment design:
     - Hypothesis and success metrics
     - A/B testing methodology
     - Sample size calculations
     - Bias detection approach

  Include feature transformation code and statistical validation logic.
</Task>

## 阶段 2：模型开发与训练

<Task>
subagent_type: ml-engineer
prompt: |
  Implement training pipeline based on requirements: {phase1.data-scientist.output}
  Using data pipeline: {phase1.data-engineer.output}

  Build comprehensive training system:
  1. Training pipeline implementation:
     - Modular training code with clear interfaces
     - Hyperparameter optimization (Optuna/Ray Tune)
     - Distributed training support (Horovod/PyTorch DDP)
     - Cross-validation and ensemble strategies

  2. Experiment tracking setup:
     - MLflow/Weights & Biases integration
     - Metric logging and visualization
     - Artifact management (models, plots, data samples)
     - Experiment comparison and analysis tools

  3. Model registry integration:
     - Version control and tagging strategy
     - Model metadata and lineage
     - Promotion workflows (dev -> staging -> prod)
     - Rollback procedures

  Provide complete training code with configuration management.
</Task>

<Task>
subagent_type: python-pro
prompt: |
  Optimize and productionize ML code from: {phase2.ml-engineer.output}

  Focus areas:
  1. Code quality and structure:
     - Refactor for production standards
     - Add comprehensive error handling
     - Implement proper logging with structured formats
     - Create reusable components and utilities

  2. Performance optimization:
     - Profile and optimize bottlenecks
     - Implement caching strategies
     - Optimize data loading and preprocessing
     - Memory management for large-scale training

  3. Testing framework:
     - Unit tests for data transformations
     - Integration tests for pipeline components
     - Model quality tests (invariance, directional)
     - Performance regression tests

  Deliver production-ready, maintainable code with full test coverage.
</Task>

## 阶段 3：生产部署与服务

<Task>
subagent_type: mlops-engineer
prompt: |
  Design production deployment for models from: {phase2.ml-engineer.output}
  With optimized code from: {phase2.python-pro.output}

  Implementation requirements:
  1. Model serving infrastructure:
     - REST/gRPC APIs with FastAPI/TorchServe
     - Batch prediction pipelines (Airflow/Kubeflow)
     - Stream processing (Kafka/Kinesis integration)
     - Model serving platforms (KServe/Seldon Core)

  2. Deployment strategies:
     - Blue-green deployments for zero downtime
     - Canary releases with traffic splitting
     - Shadow deployments for validation
     - A/B testing infrastructure

  3. CI/CD pipeline:
     - GitHub Actions/GitLab CI workflows
     - Automated testing gates
     - Model validation before deployment
     - ArgoCD for GitOps deployment

  4. Infrastructure as Code:
     - Terraform modules for cloud resources
     - Helm charts for Kubernetes deployments
     - Docker multi-stage builds for optimization
     - Secret management with Vault/Secrets Manager

  Provide complete deployment configuration and automation scripts.
</Task>

<Task>
subagent_type: kubernetes-architect
prompt: |
  Design Kubernetes infrastructure for ML workloads from: {phase3.mlops-engineer.output}

  Kubernetes-specific requirements:
  1. Workload orchestration:
     - Training job scheduling with Kubeflow
     - GPU resource allocation and sharing
     - Spot/preemptible instance integration
     - Priority classes and resource quotas

  2. Serving infrastructure:
     - HPA/VPA for autoscaling
     - KEDA for event-driven scaling
     - Istio service mesh for traffic management
     - Model caching and warm-up strategies

  3. Storage and data access:
     - PVC strategies for training data
     - Model artifact storage with CSI drivers
     - Distributed storage for feature stores
     - Cache layers for inference optimization

  Provide Kubernetes manifests and Helm charts for entire ML platform.
</Task>

## 阶段 4：监控与持续改进

<Task>
subagent_type: observability-engineer
prompt: |
  Implement comprehensive monitoring for ML system deployed in: {phase3.mlops-engineer.output}
  Using Kubernetes infrastructure: {phase3.kubernetes-architect.output}

  Monitoring framework:
  1. Model performance monitoring:
     - Prediction accuracy tracking
     - Latency and throughput metrics
     - Feature importance shifts
     - Business KPI correlation

  2. Data and model drift detection:
     - Statistical drift detection (KS test, PSI)
     - Concept drift monitoring
     - Feature distribution tracking
     - Automated drift alerts and reports

  3. System observability:
     - Prometheus metrics for all components
     - Grafana dashboards for visualization
     - Distributed tracing with Jaeger/Zipkin
     - Log aggregation with ELK/Loki

  4. Alerting and automation:
     - PagerDuty/Opsgenie integration
     - Automated retraining triggers
     - Performance degradation workflows
     - Incident response runbooks

  5. Cost tracking:
     - Resource utilization metrics
     - Cost allocation by model/experiment
     - Optimization recommendations
     - Budget alerts and controls

  Deliver monitoring configuration, dashboards, and alert rules.
</Task>

## 配置选项

- **experiment_tracking**: mlflow | wandb | neptune | clearml
- **feature_store**: feast | tecton | databricks | custom
- **serving_platform**: kserve | seldon | torchserve | triton
- **orchestration**: kubeflow | airflow | prefect | dagster
- **cloud_provider**: aws | azure | gcp | multi-cloud
- **deployment_mode**: realtime | batch | streaming | hybrid
- **monitoring_stack**: prometheus | datadog | newrelic | custom

## 成功标准

1. **数据流水线**：
   - 生产环境中数据质量问题 < 0.1%
   - 自动化数据验证通过率 99.9%
   - 完整的数据血缘追踪
   - 特征服务延迟低于 1 秒

2. **模型性能**：
   - 达到或超过基线指标
   - 重训练前性能下降 < 5%
   - A/B 测试结果具有统计显著性
   - 模型漂移未被检测的时间不超过 24 小时

3. **运维卓越**：
   - 模型服务可用性 99.9%
   - p99 推理延迟 < 200ms
   - 5 分钟内自动回滚
   - 完整可观测性，告警响应时间 < 1 分钟

4. **开发速度**：
   - 从提交到上线 < 1 小时
   - 支持并行实验执行
   - 训练运行可复现
   - 自助式模型部署

5. **成本效率**：
   - 基础设施浪费 < 20%
   - 资源分配优化
   - 基于负载自动扩缩容
   - Spot 实例利用率 > 60%

## 最终交付物

完成后，编排流水线将提供：
- 端到端全自动 ML 流水线
- 完整的文档和运维手册
- 生产级基础设施即代码
- 完整的监控和告警系统
- 持续改进的 CI/CD 流水线
- 成本优化和扩缩容策略
- 灾难恢复和回滚流程

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，应停下来请求澄清。
