---
name: aws-cost-cleanup
description: "自动清理未使用的 AWS 资源以降低成本。触发词：AWS成本清理、资源清理、AWS省钱、清理未使用资源、EBS清理、快照清理、Elastic IP释放、AWS资源优化、成本优化、AWS清理脚本"
risk: safe
source: community
date_added: "2026-02-27"
---

# AWS 成本清理

自动识别并移除未使用的 AWS 资源，消除浪费。

## 何时使用此技能

当你需要自动清理未使用的 AWS 资源以降低成本并消除浪费时，使用此技能。

## 自动清理目标

**存储**
- 未挂载的 EBS 卷
- 旧的 EBS 快照（>90 天）
- 未完成的 S3 分片上传
- 启用版本控制的存储桶中的旧 S3 版本

**计算**
- 已停止的 EC2 实例（>30 天）
- 未使用的 AMI 及其关联快照
- 未使用的弹性 IP

**网络**
- 未使用的弹性负载均衡器
- 未使用的 NAT 网关
- 孤立的 ENI

## 清理脚本

### 安全清理（先试运行）

```bash
#!/bin/bash
# cleanup-unused-ebs.sh

echo "Finding unattached EBS volumes..."
VOLUMES=$(aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].VolumeId' \
  --output text)

for vol in $VOLUMES; do
  echo "Would delete: $vol"
  # Uncomment to actually delete:
  # aws ec2 delete-volume --volume-id $vol
done
```

```bash
#!/bin/bash
# cleanup-old-snapshots.sh

CUTOFF_DATE=$(date -d '90 days ago' --iso-8601)

aws ec2 describe-snapshots --owner-ids self \
  --query "Snapshots[?StartTime<='$CUTOFF_DATE'].[SnapshotId,StartTime,VolumeSize]" \
  --output text | while read snap_id start_time size; do
  
  echo "Snapshot: $snap_id (Created: $start_time, Size: ${size}GB)"
  # Uncomment to delete:
  # aws ec2 delete-snapshot --snapshot-id $snap_id
done
```

```bash
#!/bin/bash
# release-unused-eips.sh

aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].[AllocationId,PublicIp]' \
  --output text | while read alloc_id public_ip; do
  
  echo "Would release: $public_ip ($alloc_id)"
  # Uncomment to release:
  # aws ec2 release-address --allocation-id $alloc_id
done
```

### S3 生命周期自动化

```bash
# Apply lifecycle policy to transition old objects to cheaper storage
cat > lifecycle-policy.json <<EOF
{
  "Rules": [
    {
      "Id": "Archive old objects",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 180,
          "StorageClass": "GLACIER"
        }
      ],
      "NoncurrentVersionExpiration": {
        "NoncurrentDays": 30
      },
      "AbortIncompleteMultipartUpload": {
        "DaysAfterInitiation": 7
      }
    }
  ]
}
EOF

aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration file://lifecycle-policy.json
```

## 成本影响计算器

```python
#!/usr/bin/env python3
# calculate-savings.py

import boto3
from datetime import datetime, timedelta

ec2 = boto3.client('ec2')

# Calculate EBS volume savings
volumes = ec2.describe_volumes(
    Filters=[{'Name': 'status', 'Values': ['available']}]
)

total_size = sum(v['Size'] for v in volumes['Volumes'])
monthly_cost = total_size * 0.10  # $0.10/GB-month for gp3

print(f"Unattached EBS Volumes: {len(volumes['Volumes'])}")
print(f"Total Size: {total_size} GB")
print(f"Monthly Savings: ${monthly_cost:.2f}")

# Calculate Elastic IP savings
addresses = ec2.describe_addresses()
unused = [a for a in addresses['Addresses'] if 'AssociationId' not in a]

eip_cost = len(unused) * 3.65  # $0.005/hour * 730 hours
print(f"\nUnused Elastic IPs: {len(unused)}")
print(f"Monthly Savings: ${eip_cost:.2f}")

print(f"\nTotal Monthly Savings: ${monthly_cost + eip_cost:.2f}")
print(f"Annual Savings: ${(monthly_cost + eip_cost) * 12:.2f}")
```

## 自动清理 Lambda

```python
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Delete unattached volumes older than 7 days
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    
    cutoff = datetime.now() - timedelta(days=7)
    deleted = 0
    
    for vol in volumes['Volumes']:
        create_time = vol['CreateTime'].replace(tzinfo=None)
        if create_time < cutoff:
            try:
                ec2.delete_volume(VolumeId=vol['VolumeId'])
                deleted += 1
                print(f"Deleted volume: {vol['VolumeId']}")
            except Exception as e:
                print(f"Error deleting {vol['VolumeId']}: {e}")
    
    return {
        'statusCode': 200,
        'body': f'Deleted {deleted} volumes'
    }
```

## 清理工作流程

1. **发现阶段**（只读）
   - 运行所有 describe 命令
   - 生成成本影响报告
   - 与团队一起审查

2. **验证阶段**
   - 验证资源确实未使用
   - 检查依赖关系
   - 通知资源所有者

3. **执行阶段**（先试运行）
   - 使用试运行模式运行清理脚本
   - 审查建议的更改
   - 执行实际清理

4. **验证阶段**
   - 确认删除
   - 监控问题
   - 记录节省的成本

## 安全检查清单

- [ ] 先在试运行模式下运行
- [ ] 验证资源没有依赖关系
- [ ] 检查资源标签以确定所有者
- [ ] 删除前通知利益相关者
- [ ] 为关键数据创建快照
- [ ] 先在非生产环境中测试
- [ ] 准备好回滚计划
- [ ] 记录所有删除操作

## 示例提示词

**发现**
- "查找所有未使用的资源并计算潜在节省"
- "为我的 AWS 账户生成清理报告"
- "哪些资源可以安全删除？"

**执行**
- "创建一个脚本来清理未挂载的 EBS 卷"
- "删除所有超过 90 天的快照"
- "释放未使用的弹性 IP"

**自动化**
- "为旧快照设置自动清理"
- "创建一个 Lambda 函数进行每周清理"
- "安排每月资源清理"

## 与 AWS Organizations 集成

```bash
# Run cleanup across multiple accounts
for account in $(aws organizations list-accounts \
  --query 'Accounts[*].Id' --output text); do
  
  echo "Checking account: $account"
  aws ec2 describe-volumes \
    --filters Name=status,Values=available \
    --profile account-$account
done
```

## 监控和告警

```bash
# Create CloudWatch alarm for cost anomalies
aws cloudwatch put-metric-alarm \
  --alarm-name high-cost-alert \
  --alarm-description "Alert when daily cost exceeds threshold" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 86400 \
  --evaluation-periods 1 \
  --threshold 100 \
  --comparison-operator GreaterThanThreshold
```

## 最佳实践

- 在维护窗口期间安排清理
- 删除前始终创建最终快照
- 使用资源标签识别清理候选
- 为生产环境实施审批工作流
- 记录所有清理操作以供审计
- 设置成本异常检测
- 每周审查清理结果

## 风险缓解

**中等风险操作：**
- 删除未挂载的卷（确保没有计划重新挂载）
- 删除旧快照（验证没有合规要求）
- 释放弹性 IP（检查 DNS 记录）

**始终：**
- 保持 30 天备份保留
- 对关键资源使用 AWS Backup
- 测试恢复流程
- 记录清理决策

## Kiro CLI 集成

```bash
# Analyze and cleanup in one command
kiro-cli chat "Use aws-cost-cleanup to find and remove unused resources"

# Generate cleanup script
kiro-cli chat "Create a safe cleanup script for my AWS account"

# Schedule automated cleanup
kiro-cli chat "Set up weekly automated cleanup using aws-cost-cleanup"
```

## 其他资源

- [AWS Resource Cleanup Best Practices](https://aws.amazon.com/blogs/mt/automate-resource-cleanup/)
- [AWS Systems Manager Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html)
- [AWS Config Rules for Compliance](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html)

## 限制
- 仅当任务明确符合上述描述的范围时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
