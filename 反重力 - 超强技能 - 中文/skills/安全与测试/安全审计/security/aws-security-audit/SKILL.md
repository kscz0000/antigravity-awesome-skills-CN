---
name: aws-security-audit
description: "使用 AWS CLI 和安全最佳实践，对 AWS 环境进行全面的安全态势评估"
category: security
risk: safe
source: community
tags: "[aws, security, audit, compliance, kiro-cli, security-assessment]"
date_added: "2026-02-27"
---

# AWS 安全审计

对 AWS 环境开展全面的安全评估，识别漏洞和错误配置。

## 适用场景
当需要审计 AWS 安全态势、识别漏洞或为合规评估做准备时，使用此技能。

## 审计类别

**身份与访问管理**
- 过度宽松的 IAM 策略
- 未使用的 IAM 用户和角色
- MFA 强制执行存在缺口
- 根账户使用情况
- 访问密钥轮换

**网络安全**
- 对外开放的安全组（0.0.0.0/0）
- 公开的 S3 存储桶
- 传输中的数据未加密
- VPC 流日志未启用
- 网络 ACL 配置错误

**数据保护**
- 未加密的 EBS 卷
- 未加密的 RDS 实例
- S3 存储桶加密未启用
- 缺少备份策略
- KMS 密钥轮换未启用

**日志与监控**
- CloudTrail 未启用
- 缺少 CloudWatch 告警
- VPC 流日志未启用
- S3 访问日志未启用
- Config 记录未启用

## 安全审计命令

### IAM 安全检查

```bash
# List users without MFA
aws iam get-credential-report --output text | \
  awk -F, '$4=="false" && $1!="<root_account>" {print $1}'

# Find unused IAM users (no activity in 90 days)
aws iam list-users --query 'Users[*].[UserName]' --output text | \
while read user; do
  last_used=$(aws iam get-user --user-name "$user" \
    --query 'User.PasswordLastUsed' --output text)
  echo "$user: $last_used"
done

# List overly permissive policies (AdministratorAccess)
aws iam list-policies --scope Local \
  --query 'Policies[?PolicyName==`AdministratorAccess`]'

# Find access keys older than 90 days
aws iam list-users --query 'Users[*].UserName' --output text | \
while read user; do
  aws iam list-access-keys --user-name "$user" \
    --query 'AccessKeyMetadata[*].[AccessKeyId,CreateDate]' \
    --output text
done

# Check root account access keys
aws iam get-account-summary \
  --query 'SummaryMap.AccountAccessKeysPresent'
```

### 网络安全检查

```bash
# Find security groups open to the world
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' \
  --output table

# List public S3 buckets
aws s3api list-buckets --query 'Buckets[*].Name' --output text | \
while read bucket; do
  acl=$(aws s3api get-bucket-acl --bucket "$bucket" 2>/dev/null)
  if echo "$acl" | grep -q "AllUsers"; then
    echo "PUBLIC: $bucket"
  fi
done

# Check VPC Flow Logs status
aws ec2 describe-vpcs --query 'Vpcs[*].VpcId' --output text | \
while read vpc; do
  flow_logs=$(aws ec2 describe-flow-logs \
    --filter "Name=resource-id,Values=$vpc" \
    --query 'FlowLogs[*].FlowLogId' --output text)
  if [ -z "$flow_logs" ]; then
    echo "No flow logs: $vpc"
  fi
done

# Find RDS instances without encryption
aws rds describe-db-instances \
  --query 'DBInstances[?StorageEncrypted==`false`].[DBInstanceIdentifier]' \
  --output table
```

### 数据保护检查

```bash
# Find unencrypted EBS volumes
aws ec2 describe-volumes \
  --query 'Volumes[?Encrypted==`false`].[VolumeId,Size,State]' \
  --output table

# Check S3 bucket encryption
aws s3api list-buckets --query 'Buckets[*].Name' --output text | \
while read bucket; do
  encryption=$(aws s3api get-bucket-encryption \
    --bucket "$bucket" 2>&1)
  if echo "$encryption" | grep -q "ServerSideEncryptionConfigurationNotFoundError"; then
    echo "No encryption: $bucket"
  fi
done

# Find RDS snapshots that are public
aws rds describe-db-snapshots \
  --query 'DBSnapshots[*].[DBSnapshotIdentifier]' --output text | \
while read snapshot; do
  attrs=$(aws rds describe-db-snapshot-attributes \
    --db-snapshot-identifier "$snapshot" \
    --query 'DBSnapshotAttributesResult.DBSnapshotAttributes[?AttributeName==`restore`].AttributeValues' \
    --output text)
  if echo "$attrs" | grep -q "all"; then
    echo "PUBLIC SNAPSHOT: $snapshot"
  fi
done

# Check KMS key rotation
aws kms list-keys --query 'Keys[*].KeyId' --output text | \
while read key; do
  rotation=$(aws kms get-key-rotation-status --key-id "$key" \
    --query 'KeyRotationEnabled' --output text 2>/dev/null)
  if [ "$rotation" = "False" ]; then
    echo "Rotation disabled: $key"
  fi
done
```

### 日志与监控检查

```bash
# Check CloudTrail status
aws cloudtrail describe-trails \
  --query 'trailList[*].[Name,IsMultiRegionTrail,LogFileValidationEnabled]' \
  --output table

# Verify CloudTrail is logging
aws cloudtrail get-trail-status --name my-trail \
  --query 'IsLogging'

# Check if AWS Config is enabled
aws configservice describe-configuration-recorders \
  --query 'ConfigurationRecorders[*].[name,roleARN]' \
  --output table

# List S3 buckets without access logging
aws s3api list-buckets --query 'Buckets[*].Name' --output text | \
while read bucket; do
  logging=$(aws s3api get-bucket-logging --bucket "$bucket" 2>&1)
  if ! echo "$logging" | grep -q "LoggingEnabled"; then
    echo "No access logging: $bucket"
  fi
done
```

## 自动化安全审计脚本

```bash
#!/bin/bash
# comprehensive-security-audit.sh

echo "=== AWS Security Audit Report ==="
echo "Generated: $(date)"
echo ""

# IAM Checks
echo "## IAM Security"
echo "Users without MFA:"
aws iam get-credential-report --output text | \
  awk -F, '$4=="false" && $1!="<root_account>" {print "  - " $1}'

echo ""
echo "Root account access keys:"
aws iam get-account-summary \
  --query 'SummaryMap.AccountAccessKeysPresent' --output text

# Network Checks
echo ""
echo "## Network Security"
echo "Security groups open to 0.0.0.0/0:"
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].GroupId' \
  --output text | wc -l

# Data Protection
echo ""
echo "## Data Protection"
echo "Unencrypted EBS volumes:"
aws ec2 describe-volumes \
  --query 'Volumes[?Encrypted==`false`].VolumeId' \
  --output text | wc -l

echo ""
echo "Unencrypted RDS instances:"
aws rds describe-db-instances \
  --query 'DBInstances[?StorageEncrypted==`false`].DBInstanceIdentifier' \
  --output text | wc -l

# Logging
echo ""
echo "## Logging & Monitoring"
echo "CloudTrail status:"
aws cloudtrail describe-trails \
  --query 'trailList[*].[Name,IsLogging]' \
  --output table

echo ""
echo "=== End of Report ==="
```

## 安全评分计算器

```python
#!/usr/bin/env python3
# security-score.py

import boto3
import json

def calculate_security_score():
    iam = boto3.client('iam')
    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')
    
    score = 100
    issues = []
    
    # Check MFA
    try:
        report = iam.get_credential_report()
        users_without_mfa = 0
        # Parse report and count
        if users_without_mfa > 0:
            score -= 10
            issues.append(f"{users_without_mfa} users without MFA")
    except:
        pass
    
    # Check open security groups
    sgs = ec2.describe_security_groups()
    open_sgs = 0
    for sg in sgs['SecurityGroups']:
        for perm in sg.get('IpPermissions', []):
            for ip_range in perm.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    open_sgs += 1
                    break
    
    if open_sgs > 0:
        score -= 15
        issues.append(f"{open_sgs} security groups open to internet")
    
    # Check unencrypted volumes
    volumes = ec2.describe_volumes()
    unencrypted = sum(1 for v in volumes['Volumes'] if not v['Encrypted'])
    
    if unencrypted > 0:
        score -= 20
        issues.append(f"{unencrypted} unencrypted EBS volumes")
    
    print(f"Security Score: {score}/100")
    print("\nIssues Found:")
    for issue in issues:
        print(f"  - {issue}")
    
    return score

if __name__ == "__main__":
    calculate_security_score()
```

## 合规映射

**CIS AWS 基础基线**
- 1.1：根账户使用情况
- 1.2-1.14：IAM 策略与 MFA
- 2.1-2.9：日志记录（CloudTrail、Config、VPC 流日志）
- 4.1-4.3：监控与告警

**PCI-DSS**
- 要求 1：网络安全控制
- 要求 2：安全配置
- 要求 8：访问控制与 MFA
- 要求 10：日志记录与监控

**HIPAA**
- 访问控制（IAM）
- 审计控制（CloudTrail）
- 加密（EBS、RDS、S3）
- 传输安全（TLS/SSL）

## 修复优先级

**紧急（立即修复）**
- 根账户访问密钥
- 公开的 RDS 快照
- 在敏感端口上对 0.0.0.0/0 开放的安全组
- CloudTrail 未启用

**高（7 天内修复）**
- 未启用 MFA 的用户
- 静态数据未加密
- 缺少 VPC 流日志
- 过度宽松的 IAM 策略

**中（30 天内修复）**
- 超过 90 天的旧访问密钥
- 缺少 S3 访问日志
- 未使用的 IAM 用户
- KMS 密钥轮换未启用

## 示例提示词

- "对我的 AWS 账户运行一次全面的安全审计"
- "检查 IAM 安全问题"
- "查找所有未加密的资源"
- "生成一份安全合规报告"
- "计算我的 AWS 安全评分"

## 最佳实践

- 每周运行一次审计
- 通过 Lambda/EventBridge 实现自动化
- 将结果导出到 S3 以便跟踪趋势
- 与 SIEM 工具集成
- 跟踪修复进度
- 对例外情况进行记录并附带业务理由

## Kiro CLI 集成

```bash
kiro-cli chat "Use aws-security-audit to assess my security posture"
kiro-cli chat "Generate a security audit report with aws-security-audit"
```

## 额外资源

- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)
- [AWS Security Hub](https://aws.amazon.com/security-hub/)

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为替代环境特定验证、测试或专家审查的方案。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
