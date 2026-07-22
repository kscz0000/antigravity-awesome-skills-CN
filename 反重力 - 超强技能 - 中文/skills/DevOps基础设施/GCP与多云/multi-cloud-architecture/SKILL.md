---
name: multi-cloud-architecture
description: "跨 AWS、Azure 和 GCP 的应用架构决策框架与模式。触发词：多云架构、multi-cloud、云服务商迁移、AWS Azure GCP、云原生架构、跨云部署、云服务选型、混合云策略、云成本优化"
risk: safe
source: community
date_added: "2026-02-27"
---

# 多云架构

跨 AWS、Azure 和 GCP 的应用架构决策框架与模式。

## 不适用场景

- 任务与多云架构无关
- 需要此范围之外的其他领域或工具

## 指导说明

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 目的

设计云无关架构，并跨云服务商做出明智的服务选择决策。

## 适用场景

- 设计多云策略
- 在云服务商之间迁移
- 为特定工作负载选择云服务
- 实现云无关架构
- 跨服务商优化成本

## 云服务对比

### 计算服务

| AWS | Azure | GCP | 用例 |
|-----|-------|-----|------|
| EC2 | Virtual Machines | Compute Engine | IaaS 虚拟机 |
| ECS | Container Instances | Cloud Run | 容器 |
| EKS | AKS | GKE | Kubernetes |
| Lambda | Functions | Cloud Functions | Serverless |
| Fargate | Container Apps | Cloud Run | 托管容器 |

### 存储服务

| AWS | Azure | GCP | 用例 |
|-----|-------|-----|------|
| S3 | Blob Storage | Cloud Storage | 对象存储 |
| EBS | Managed Disks | Persistent Disk | 块存储 |
| EFS | Azure Files | Filestore | 文件存储 |
| Glacier | Archive Storage | Archive Storage | 冷存储 |

### 数据库服务

| AWS | Azure | GCP | 用例 |
|-----|-------|-----|------|
| RDS | SQL Database | Cloud SQL | 托管 SQL |
| DynamoDB | Cosmos DB | Firestore | NoSQL |
| Aurora | PostgreSQL/MySQL | Cloud Spanner | 分布式 SQL |
| ElastiCache | Cache for Redis | Memorystore | 缓存 |

**参考：** 完整对比请参阅 `references/service-comparison.md`

## 多云模式

### 模式 1：单服务商 + 灾备

- 主工作负载在一个云上
- 灾备在另一个云上
- 跨云数据库复制
- 自动故障转移

### 模式 2：最佳组合

- 使用各服务商的最优服务
- AI/ML 在 GCP
- 企业应用在 Azure
- 通用计算在 AWS

### 模式 3：地理分布

- 从最近的云区域服务用户
- 数据主权合规
- 全局负载均衡
- 区域故障转移

### 模式 4：云无关抽象

- Kubernetes 用于计算
- PostgreSQL 用于数据库
- S3 兼容存储（MinIO）
- 开源工具

## 云无关架构

### 使用云原生替代方案

- **计算：** Kubernetes (EKS/AKS/GKE)
- **数据库：** PostgreSQL/MySQL (RDS/SQL Database/Cloud SQL)
- **消息队列：** Apache Kafka (MSK/Event Hubs/Confluent)
- **缓存：** Redis (ElastiCache/Azure Cache/Memorystore)
- **对象存储：** S3 兼容 API
- **监控：** Prometheus/Grafana
- **服务网格：** Istio/Linkerd

### 抽象层

```
应用层
    ↓
基础设施抽象 (Terraform)
    ↓
云服务商 API
    ↓
AWS / Azure / GCP
```

## 成本对比

### 计算定价因素

- **AWS：** 按需、预留、Spot、Savings Plans
- **Azure：** 按量付费、预留、Spot
- **GCP：** 按需、承诺使用、抢占式

### 成本优化策略

1. 使用预留/承诺容量（节省 30-70%）
2. 利用 Spot/抢占式实例
3. 合理配置资源规格
4. 可变工作负载使用 Serverless
5. 优化数据传输成本
6. 实施生命周期策略
7. 使用成本分配标签
8. 使用云成本工具监控

**参考：** 请参阅 `references/multi-cloud-patterns.md`

## 迁移策略

### 阶段 1：评估
- 盘点当前基础设施
- 识别依赖关系
- 评估云兼容性
- 估算成本

### 阶段 2：试点
- 选择试点工作负载
- 在目标云实施
- 充分测试
- 记录经验教训

### 阶段 3：迁移
- 增量迁移工作负载
- 保持双轨运行期
- 监控性能
- 验证功能

### 阶段 4：优化
- 合理配置资源规格
- 实施云原生服务
- 优化成本
- 增强安全性

## 最佳实践

1. **使用基础设施即代码**（Terraform/OpenTofu）
2. **实施 CI/CD 流水线**进行部署
3. **设计容错架构**跨云
4. **尽可能使用托管服务**
5. **实施全面监控**
6. **自动化成本优化**
7. **遵循安全最佳实践**
8. **记录云特定配置**
9. **测试灾难恢复**流程
10. **培训团队**掌握多云技能

## 参考文件

- `references/service-comparison.md` - 完整服务对比
- `references/multi-cloud-patterns.md` - 架构模式

## 相关技能

- `terraform-module-library` - 用于 IaC 实施
- `cost-optimization` - 用于成本管理
- `hybrid-cloud-networking` - 用于网络连接

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代针对具体环境的验证、测试或专家评审。
- 如缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
