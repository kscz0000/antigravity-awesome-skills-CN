---
name: ml-pipeline-workflow
description: "端到端 MLOps 流水线编排，涵盖从数据准备到模型部署的全流程。当用户要求'搭建ML流水线'、'MLOps编排'、'模型部署自动化'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# ML Pipeline Workflow

端到端 MLOps 流水线编排，涵盖从数据准备到模型部署的全流程。

## 不适用场景

- 任务与 ML 流水线无关
- 需要本范围之外的领域或工具

## 使用说明

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可操作的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 概述

本技能为构建生产级 ML 流水线提供全面指导，覆盖完整生命周期：数据接入 → 准备 → 训练 → 验证 → 部署 → 监控。

## 适用场景

- 从零搭建 ML 流水线
- 设计 ML 系统的工作流编排
- 实现数据 → 模型 → 部署的自动化
- 搭建可复现的训练工作流
- 创建基于 DAG 的 ML 编排
- 将 ML 组件集成到生产系统

## 本技能提供的内容

### 核心能力

1. **流水线架构**
   - 端到端工作流设计
   - DAG 编排模式（Airflow、Dagster、Kubeflow）
   - 组件依赖与数据流
   - 错误处理与重试策略

2. **数据准备**
   - 数据验证与质量检查
   - 特征工程流水线
   - 数据版本管理与血缘追踪
   - 训练/验证/测试集划分策略

3. **模型训练**
   - 训练任务编排
   - 超参数管理
   - 实验追踪集成
   - 分布式训练模式

4. **模型验证**
   - 验证框架与指标
   - A/B 测试基础设施
   - 性能回归检测
   - 模型对比工作流

5. **部署自动化**
   - 模型服务模式
   - 金丝雀部署
   - 蓝绿部署策略
   - 回滚机制

### 参考文档

详见 `references/` 目录：
- **data-preparation.md** - 数据清洗、验证与特征工程
- **model-training.md** - 训练工作流与最佳实践
- **model-validation.md** - 验证策略与指标
- **model-deployment.md** - 部署模式与服务架构

### 资产与模板

`assets/` 目录包含：
- **pipeline-dag.yaml.template** - 工作流编排 DAG 模板
- **training-config.yaml** - 训练配置模板
- **validation-checklist.md** - 部署前验证清单

## 使用模式

### 基础流水线搭建

```python
# 1. Define pipeline stages
stages = [
    "data_ingestion",
    "data_validation",
    "feature_engineering",
    "model_training",
    "model_validation",
    "model_deployment"
]

# 2. Configure dependencies
# See assets/pipeline-dag.yaml.template for full example
```

### 生产工作流

1. **数据准备阶段**
   - 从数据源接入原始数据
   - 运行数据质量检查
   - 执行特征转换
   - 对处理后的数据集版本化

2. **训练阶段**
   - 加载版本化的训练数据
   - 执行训练任务
   - 追踪实验与指标
   - 保存训练好的模型

3. **验证阶段**
   - 运行验证测试套件
   - 与基线对比
   - 生成性能报告
   - 审批部署

4. **部署阶段**
   - 打包模型产物
   - 部署到服务基础设施
   - 配置监控
   - 验证生产流量

## 最佳实践

### 流水线设计

- **模块化**：每个阶段可独立测试
- **幂等性**：重复运行阶段应安全无副作用
- **可观测性**：每个阶段记录指标
- **版本化**：追踪数据、代码和模型版本
- **故障处理**：实现重试逻辑和告警

### 数据管理

- 使用数据验证库（Great Expectations、TFX）
- 用 DVC 等工具管理数据集版本
- 记录特征工程转换逻辑
- 维护数据血缘追踪

### 模型运维

- 分离训练和服务基础设施
- 使用模型注册中心（MLflow、Weights & Biases）
- 新模型采用渐进式发布
- 监控模型性能漂移
- 保持回滚能力

### 部署策略

- 从影子部署开始
- 用金丝雀发布做验证
- 搭建 A/B 测试基础设施
- 设置自动回滚触发器
- 监控延迟和吞吐量

## 集成点

### 编排工具

- **Apache Airflow**：基于 DAG 的工作流编排
- **Dagster**：基于资产的流水线编排
- **Kubeflow Pipelines**：Kubernetes 原生 ML 工作流
- **Prefect**：现代数据流自动化

### 实验追踪

- MLflow 用于实验追踪和模型注册
- Weights & Biases 用于可视化和协作
- TensorBoard 用于训练指标

### 部署平台

- AWS SageMaker 托管 ML 基础设施
- Google Vertex AI 用于 GCP 部署
- Azure ML 用于 Azure 云
- Kubernetes + KServe 用于云无关的服务部署

## 渐进式学习

从基础开始，逐步增加复杂度：

1. **Level 1**：简单线性流水线（数据 → 训练 → 部署）
2. **Level 2**：增加验证和监控阶段
3. **Level 3**：实现超参数调优
4. **Level 4**：增加 A/B 测试和渐进式发布
5. **Level 5**：多模型流水线与集成策略

## 常见模式

### 批量训练流水线

```yaml
# See assets/pipeline-dag.yaml.template
stages:
  - name: data_preparation
    dependencies: []
  - name: model_training
    dependencies: [data_preparation]
  - name: model_evaluation
    dependencies: [model_training]
  - name: model_deployment
    dependencies: [model_evaluation]
```

### 实时特征流水线

```python
# Stream processing for real-time features
# Combined with batch training
# See references/data-preparation.md
```

### 持续训练

```python
# Automated retraining on schedule
# Triggered by data drift detection
# See references/model-training.md
```

## 故障排查

### 常见问题

- **流水线失败**：检查依赖和数据可用性
- **训练不稳定**：审查超参数和数据质量
- **部署问题**：验证模型产物和服务配置
- **性能退化**：监控数据漂移和模型指标

### 调试步骤

1. 检查各阶段的流水线日志
2. 在边界处验证输入/输出数据
3. 隔离测试各组件
4. 审查实验追踪指标
5. 检查模型产物和元数据

## 后续步骤

流水线搭建完成后：

1. 探索 **hyperparameter-tuning** 技能进行优化
2. 学习 **experiment-tracking-setup** 接入 MLflow/W&B
3. 查看 **model-deployment-patterns** 了解服务策略
4. 用可观测性工具实现监控

## 相关技能

- **experiment-tracking-setup**：MLflow 与 Weights & Biases 集成
- **hyperparameter-tuning**：自动超参数优化
- **model-deployment-patterns**：高级部署策略

## 局限性
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境专属的验证、测试或专家评审
- 若缺少必要输入、权限、安全边界或成功标准，应停下来询问确认
