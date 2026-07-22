---
name: aws-cost-optimizer
description: "使用 AWS CLI 和 Cost Explorer 进行全面的 AWS 成本分析和优化建议。触发词：AWS成本优化、云成本分析、AWS费用优化、成本分析、云资源优化、AWS省钱、云支出分析、成本降低、资源利用率、AWS账单优化"
risk: safe
source: community
date_added: "2026-02-27"
---

# AWS 成本优化器

分析 AWS 支出模式，识别浪费，并提供可操作的成本降低策略。

## 何时使用此技能

当需要分析 AWS 支出、识别成本优化机会或减少云资源浪费时使用此技能。

## 核心能力

**成本分析**
- 解析 AWS Cost Explorer 数据以发现趋势和异常
- 按服务、区域和资源标签细分成本
- 识别月度支出增长趋势

**资源优化**
- 检测空闲 EC2 实例（低 CPU 利用率）
- 查找未挂载的 EBS 卷和旧快照
- 识别未使用的弹性 IP
- 定位利用率低的 RDS 实例
- 查找符合生命周期策略的旧 S3 对象

**节省建议**
- 建议预留实例/节省计划机会
- 基于 CloudWatch 指标推荐实例规格调整
- 识别昂贵区域的资源
- 计算具体操作的潜在节省

## AWS CLI 命令

### 获取成本和使用情况
```bash
# 最近 30 天按服务分类的成本
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

# 当月每日成本
aws ce get-cost-and-usage \
  --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics UnblendedCost
```

### 查找未使用的资源
```bash
# 未挂载的 EBS 卷
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].[VolumeId,Size,VolumeType,CreateTime]' \
  --output table

# 未使用的弹性 IP
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].[PublicIp,AllocationId]' \
  --output table

# 空闲 EC2 实例（需要 CloudWatch）
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average

# 旧的 EBS 快照（>90 天）
aws ec2 describe-snapshots \
  --owner-ids self \
  --query 'Snapshots[?StartTime<=`'$(date -d '90 days ago' --iso-8601)'`].[SnapshotId,StartTime,VolumeSize]' \
  --output table
```

### 规格调整分析
```bash
# 列出 EC2 实例及其类型
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# 获取 RDS 实例利用率
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=mydb \
  --start-time $(date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average,Maximum
```

## 优化工作流程

1. **基线评估**
   - 提取 3-6 个月的成本数据
   - 识别支出最高的 5 个服务
   - 计算增长率

2. **快速见效**
   - 删除未挂载的 EBS 卷
   - 释放未使用的弹性 IP
   - 停止/终止空闲 EC2 实例
   - 删除旧快照

3. **战略性优化**
   - 分析预留实例覆盖率
   - 审查实例类型与工作负载的匹配度
   - 实施 S3 生命周期策略
   - 考虑对非关键工作负载使用 Spot 实例

4. **持续监控**
   - 设置带告警的 AWS Budgets
   - 启用成本异常检测
   - 为资源打标签以便成本分摊
   - 每月成本审查会议

## 成本优化检查清单

- [ ] 启用 AWS Cost Explorer
- [ ] 设置成本分配标签
- [ ] 创建带告警的 AWS Budget
- [ ] 审查并删除未使用的资源
- [ ] 分析预留实例机会
- [ ] 实施 S3 Intelligent-Tiering
- [ ] 审查数据传输成本
- [ ] 优化 Lambda 内存分配
- [ ] 使用 CloudWatch Logs 保留策略
- [ ] 考虑多区域成本差异

## 示例提示词

**分析**
- "显示最近 3 个月按服务分类的 AWS 成本"
- "我成本最高的 10 个资源是什么？"
- "比较本月和上月的支出"

**优化**
- "查找所有未挂载的 EBS 卷并计算节省"
- "识别 CPU 利用率 <5% 的 EC2 实例"
- "根据使用情况建议预留实例购买"
- "计算删除 90 天以上快照的节省"

**实施**
- "创建一个删除未挂载卷的脚本"
- "设置每月 $1000 的预算告警"
- "为管理层生成成本优化报告"

## 最佳实践

- 始终先在非生产环境测试
- 删除前验证资源确实未使用
- 记录所有成本优化操作
- 计算优化工作的 ROI
- 自动化重复的优化任务
- 使用 AWS Trusted Advisor 建议
- 启用 AWS 成本异常检测

## 与 Kiro CLI 集成

此技能与 Kiro CLI 的 AWS 集成无缝协作：

```bash
# 使用 Kiro 分析成本
kiro-cli chat "Use aws-cost-optimizer to analyze my spending"

# 生成优化报告
kiro-cli chat "Create a cost optimization plan using aws-cost-optimizer"
```

## 安全说明

- **风险等级：低** - 只读分析是安全的
- **删除操作：中等风险** - 删除资源前务必验证
- **生产变更：高风险** - 先在开发/测试环境测试规格调整
- 删除前保留备份
- 可用时使用 `--dry-run` 标志

## 其他资源

- [AWS Cost Optimization Best Practices](https://aws.amazon.com/pricing/cost-optimization/)
- [AWS Well-Architected Framework - Cost Optimization](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- [AWS Cost Explorer API](https://docs.aws.amazon.com/cost-management/latest/APIReference/Welcome.html)

## 局限性
- 仅在任务明确符合上述描述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
