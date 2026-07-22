---
name: aws-iam-best-practices
description: "IAM 策略审查、权限收紧与最小权限落地实施"
category: security
risk: safe
source: community
tags: "[aws, iam, security, access-control, kiro-cli, least-privilege]"
date_added: "2026-02-27"
---

# AWS IAM 最佳实践

依照 AWS 安全最佳实践与最小权限原则，审查 IAM 策略并收紧权限。

## 适用场景

需要在以下场景中使用此技能：审查 IAM 策略、实施最小权限访问、或加固 IAM 安全。

## 核心原则

**最小权限**
- 仅授予所需的最小权限
- 优先使用托管策略
- 避免通配符 (*) 权限
- 定期进行访问审查

**纵深防御**
- 为所有用户启用 MFA
- 使用 IAM 角色代替长期 access key
- 实施服务控制策略 (SCP)
- 启用 CloudTrail 进行审计

**职责分离**
- 区分管理员角色与用户角色
- 为不同环境使用不同角色
- 实施审批工作流
- 定期进行权限审计

## IAM 安全检查

### 查找过度宽松的策略

```bash
# List policies with full admin access
aws iam list-policies --scope Local \
  --query 'Policies[*].[PolicyName,Arn]' --output table | \
  grep -i admin

# Find policies with wildcard actions
aws iam list-policies --scope Local --query 'Policies[*].Arn' --output text | \
while read arn; do
  version=$(aws iam get-policy --policy-arn "$arn" \
    --query 'Policy.DefaultVersionId' --output text)
  doc=$(aws iam get-policy-version --policy-arn "$arn" \
    --version-id "$version" --query 'PolicyVersion.Document')
  if echo "$doc" | grep -q '"Action": "\*"'; then
    echo "Wildcard action in: $arn"
  fi
done

# Find inline policies (should use managed policies)
aws iam list-users --query 'Users[*].UserName' --output text | \
while read user; do
  policies=$(aws iam list-user-policies --user-name "$user" \
    --query 'PolicyNames' --output text)
  if [ -n "$policies" ]; then
    echo "Inline policies on user $user: $policies"
  fi
done
```

### 强制 MFA

```bash
# List users without MFA
aws iam get-credential-report --output text | \
  awk -F, 'NR>1 && $4=="false" {print $1}'

# Check if MFA is required in policies
aws iam list-policies --scope Local --query 'Policies[*].Arn' --output text | \
while read arn; do
  version=$(aws iam get-policy --policy-arn "$arn" \
    --query 'Policy.DefaultVersionId' --output text)
  doc=$(aws iam get-policy-version --policy-arn "$arn" \
    --version-id "$version" --query 'PolicyVersion.Document')
  if echo "$doc" | grep -q "aws:MultiFactorAuthPresent"; then
    echo "MFA enforced in: $arn"
  fi
done

# Enable MFA for a user (returns QR code)
aws iam create-virtual-mfa-device \
  --virtual-mfa-device-name user-mfa \
  --outfile /tmp/qr.png \
  --bootstrap-method QRCodePNG
```

### Access Key 管理

```bash
# Find old access keys (>90 days)
aws iam list-users --query 'Users[*].UserName' --output text | \
while read user; do
  aws iam list-access-keys --user-name "$user" \
    --query 'AccessKeyMetadata[*].[AccessKeyId,CreateDate,Status]' \
    --output text | \
  while read key_id create_date status; do
    age_days=$(( ($(date +%s) - $(date -d "$create_date" +%s)) / 86400 ))
    if [ $age_days -gt 90 ]; then
      echo "$user: Key $key_id is $age_days days old"
    fi
  done
done

# Rotate access key
OLD_KEY="AKIAIOSFODNN7EXAMPLE"
USER="myuser"

# Create new key
NEW_KEY=$(aws iam create-access-key --user-name "$USER")
echo "New key created. Update applications, then run:"
echo "aws iam delete-access-key --user-name $USER --access-key-id $OLD_KEY"

# Deactivate old key (test first)
aws iam update-access-key \
  --user-name "$USER" \
  --access-key-id "$OLD_KEY" \
  --status Inactive
```

### 角色与策略分析

```bash
# List unused roles (no activity in 90 days)
aws iam list-roles --query 'Roles[*].[RoleName,RoleLastUsed.LastUsedDate]' \
  --output text | \
while read role last_used; do
  if [ "$last_used" = "None" ]; then
    echo "Never used: $role"
  fi
done

# Find roles with trust relationships to external accounts
aws iam list-roles --query 'Roles[*].RoleName' --output text | \
while read role; do
  trust=$(aws iam get-role --role-name "$role" \
    --query 'Role.AssumeRolePolicyDocument')
  if echo "$trust" | grep -q '"AWS":'; then
    echo "External trust: $role"
  fi
done

# Analyze policy permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/myuser \
  --action-names s3:GetObject s3:PutObject \
  --resource-arns arn:aws:s3:::mybucket/*
```

## IAM 策略模板

### 最小权限的 S3 访问

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/user-data/${aws:username}/*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-bucket",
      "Condition": {
        "StringLike": {
          "s3:prefix": "user-data/${aws:username}/*"
        }
      }
    }
  ]
}
```

### 强制 MFA 的策略

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "BoolIfExists": {
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    }
  ]
}
```

### 基于时间的访问

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*",
      "Condition": {
        "DateGreaterThan": {
          "aws:CurrentTime": "2026-01-01T00:00:00Z"
        },
        "DateLessThan": {
          "aws:CurrentTime": "2026-12-31T23:59:59Z"
        }
      }
    }
  ]
}
```

### IP 受限的访问

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "NotIpAddress": {
          "aws:SourceIp": [
            "203.0.113.0/24",
            "198.51.100.0/24"
          ]
        }
      }
    }
  ]
}
```

## IAM 加固检查清单

**用户管理**
- [ ] 为所有用户启用 MFA
- [ ] 删除未使用的 IAM 用户
- [ ] 每 90 天轮换一次 access key
- [ ] 使用 IAM 角色代替长期凭证
- [ ] 实施密码策略（长度、复杂度、轮换）

**策略管理**
- [ ] 用托管策略替换内联策略
- [ ] 移除通配符 (*) 权限
- [ ] 实施最小权限
- [ ] 使用策略条件（MFA、IP、时间）
- [ ] 定期审查策略

**角色管理**
- [ ] 为 EC2 实例使用角色
- [ ] 正确实施跨账户角色
- [ ] 审查信任关系
- [ ] 删除未使用的角色
- [ ] 使用会话标签实现细粒度访问

**监控**
- [ ] 为 IAM 事件启用 CloudTrail
- [ ] 为 IAM 变更设置 CloudWatch 告警
- [ ] 使用 AWS IAM Access Analyzer
- [ ] 定期进行访问审查
- [ ] 监控权限提升行为

## IAM 加固自动化

```python
#!/usr/bin/env python3
# iam-hardening.py

import boto3
from datetime import datetime, timedelta

iam = boto3.client('iam')

def enforce_mfa():
    """Identify users without MFA"""
    users = iam.list_users()['Users']
    no_mfa = []
    
    for user in users:
        mfa_devices = iam.list_mfa_devices(
            UserName=user['UserName']
        )['MFADevices']
        
        if not mfa_devices:
            no_mfa.append(user['UserName'])
    
    return no_mfa

def rotate_old_keys():
    """Find access keys older than 90 days"""
    users = iam.list_users()['Users']
    old_keys = []
    
    for user in users:
        keys = iam.list_access_keys(
            UserName=user['UserName']
        )['AccessKeyMetadata']
        
        for key in keys:
            age = datetime.now(key['CreateDate'].tzinfo) - key['CreateDate']
            if age.days > 90:
                old_keys.append({
                    'user': user['UserName'],
                    'key_id': key['AccessKeyId'],
                    'age_days': age.days
                })
    
    return old_keys

def find_overpermissive_policies():
    """Find policies with wildcard actions"""
    policies = iam.list_policies(Scope='Local')['Policies']
    overpermissive = []
    
    for policy in policies:
        version = iam.get_policy_version(
            PolicyArn=policy['Arn'],
            VersionId=policy['DefaultVersionId']
        )
        
        doc = version['PolicyVersion']['Document']
        for statement in doc.get('Statement', []):
            if statement.get('Action') == '*':
                overpermissive.append(policy['PolicyName'])
                break
    
    return overpermissive

if __name__ == "__main__":
    print("IAM Hardening Report")
    print("=" * 50)
    
    print("\nUsers without MFA:")
    for user in enforce_mfa():
        print(f"  - {user}")
    
    print("\nOld access keys (>90 days):")
    for key in rotate_old_keys():
        print(f"  - {key['user']}: {key['age_days']} days")
    
    print("\nOverpermissive policies:")
    for policy in find_overpermissive_policies():
        print(f"  - {policy}")
```

## 示例提示词

- "审查我的 IAM 策略中的安全问题"
- "查找未启用 MFA 的用户"
- "为 S3 访问创建一条最小权限策略"
- "识别过度宽松的 IAM 角色"
- "生成一份 IAM 加固报告"

## 最佳实践

- 优先使用 AWS 托管策略
- 实施策略版本管理
- 先在非生产环境测试策略
- 记录策略用途
- 定期（每季度）进行访问审查
- 使用 IAM Access Analyzer
- 为组织级管控实施 SCP

## Kiro CLI 集成

```bash
kiro-cli chat "Use aws-iam-best-practices to review my IAM setup"
kiro-cli chat "Create a least privilege policy with aws-iam-best-practices"
```

## 补充资源

- [IAM 最佳实践](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [IAM Policy Simulator](https://policysim.aws.amazon.com/)
- [IAM Access Analyzer](https://aws.amazon.com/iam/features/analyze-access/)

## 使用边界

- 仅在任务与上文描述的范围明确匹配时使用此技能。
- 不要把输出当作环境特定验证、测试或专家审查的替代品。
- 当必需的输入、权限、安全边界或成功标准缺失时，停下来向用户澄清。
