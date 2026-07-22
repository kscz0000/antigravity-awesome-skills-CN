---
name: cost-optimization
description: "跨 AWS、Azure 和 GCP 的云成本优化策略与模式。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 云成本优化

跨 AWS、Azure 和 GCP 的云成本优化策略与模式。

## 不使用此技能的情况

- 任务与云成本优化无关
- 需要此范围之外的其他领域或工具

## 指令

- 明确目标、约束条件和所需输入。
- 应用相关的最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 目的

实施系统化的成本优化策略，在保持性能和可靠性的同时降低云支出。

## 使用此技能的情况

- 降低云支出
- 资源规格优化
- 实施成本治理
- 优化多云成本
- 满足预算约束

## 成本优化框架

### 1. 可见性
- 实施成本分摊标签
- 使用云成本管理工具
- 设置预算告警
- 创建成本仪表盘

### 2. 规格优化
- 分析资源利用率
- 缩减过度配置的资源
- 使用自动伸缩
- 移除闲置资源

### 3. 定价模型
- 使用预留容量
- 利用 Spot/抢占式实例
- 实施节省计划
- 使用承诺使用折扣

### 4. 架构优化
- 使用托管服务
- 实施缓存
- 优化数据传输
- 使用生命周期策略

## AWS 成本优化

### 预留实例
```
节省：相比按需定价节省 30-72%
期限：1 年或 3 年
付款方式：全预付/部分预付/无预付
灵活性：标准型或可转换型
```

### 节省计划
```
计算节省计划：节省 66%
EC2 实例节省计划：节省 72%
适用于：EC2、Fargate、Lambda
灵活跨：实例系列、区域、操作系统
```

### Spot 实例
```
节省：相比按需定价最高节省 90%
适用于：批处理作业、CI/CD、无状态工作负载
风险：2 分钟中断通知
策略：与按需实例混合使用以提高弹性
```

### S3 成本优化
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
```

## Azure 成本优化

### 预留 VM 实例
- 1 年或 3 年期限
- 最高节省 72%
- 灵活调整规格
- 可交换

### Azure 混合权益
- 使用现有的 Windows Server 许可证
- 配合预留实例最高节省 80%
- 适用于 Windows 和 SQL Server

### Azure Advisor 建议
- 优化 VM 规格
- 删除未使用的资源
- 使用预留容量
- 优化存储

## GCP 成本优化

### 承诺使用折扣
- 1 年或 3 年承诺
- 最高节省 57%
- 适用于 vCPU 和内存
- 基于资源或基于支出

### 持续使用折扣
- 自动折扣
- 运行中的实例最高节省 30%
- 无需承诺
- 适用于 Compute Engine、GKE

### 抢占式 VM
- 最高节省 80%
- 最长运行时间 24 小时
- 最适合批处理工作负载

## 标签策略

### AWS 标签
```hcl
locals {
  common_tags = {
    Environment = "production"
    Project     = "my-project"
    CostCenter  = "engineering"
    Owner       = "team@example.com"
    ManagedBy   = "terraform"
  }
}

resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t3.medium"

  tags = merge(
    local.common_tags,
    {
      Name = "web-server"
    }
  )
}
```

**参考：** 参见 `references/tagging-standards.md`

## 成本监控

### 预算告警
```hcl
# AWS 预算
resource "aws_budgets_budget" "monthly" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "1000"
  limit_unit        = "USD"
  time_period_start = "2024-01-01_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["team@example.com"]
  }
}
```

### 成本异常检测
- AWS Cost Anomaly Detection
- Azure Cost Management alerts
- GCP Budget alerts

## 架构模式

### 模式 1：Serverless 优先
- 使用 Lambda/Functions 处理事件驱动
- 仅按执行时间付费
- 内置自动伸缩
- 无闲置成本

### 模式 2：规格优化的数据库
```
开发环境：t3.small RDS
预发布环境：t3.large RDS
生产环境：r6g.2xlarge RDS 配置只读副本
```

### 模式 3：多层存储
```
热数据：S3 Standard
温数据：S3 Standard-IA（30 天）
冷数据：S3 Glacier（90 天）
归档数据：S3 Deep Archive（365 天）
```

### 模式 4：自动伸缩
```hcl
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.main.name
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  threshold           = "80"
  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]
}
```

## 成本优化检查清单

- [ ] 实施成本分摊标签
- [ ] 删除未使用的资源（EBS、EIP、快照）
- [ ] 根据利用率优化实例规格
- [ ] 为稳定工作负载使用预留容量
- [ ] 实施自动伸缩
- [ ] 优化存储类别
- [ ] 使用生命周期策略
- [ ] 启用成本异常检测
- [ ] 设置预算告警
- [ ] 每周审查成本
- [ ] 使用 Spot/抢占式实例
- [ ] 优化数据传输成本
- [ ] 实施缓存层
- [ ] 使用托管服务
- [ ] 持续监控和优化

## 工具

- **AWS：** Cost Explorer、Cost Anomaly Detection、Compute Optimizer
- **Azure：** Cost Management、Advisor
- **GCP：** Cost Management、Recommender
- **多云：** CloudHealth、Cloudability、Kubecost

## 参考文件

- `references/tagging-standards.md` - 标签规范
- `assets/cost-analysis-template.xlsx` - 成本分析电子表格

## 相关技能

- `terraform-module-library` - 用于资源供应
- `multi-cloud-architecture` - 用于云平台选择

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
