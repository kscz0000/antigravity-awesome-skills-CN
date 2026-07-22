---
name: aws-secrets-rotation
description: "自动化 AWS Secrets 轮换，覆盖 RDS、API 密钥与凭证。涉及 aws secrets rotation、rds credentials rotation、api key rotation、lambda rotation 时使用。"
category: security
risk: safe
source: community
tags: "[aws, secrets-manager, security, automation, kiro-cli, credentials]"
date_added: "2026-02-27"
---

# AWS Secrets 轮换

使用 AWS Secrets Manager 与 Lambda 自动化轮换 secrets、凭证与 API 密钥。

## 适用场景

需要实现自动化 secrets 轮换、安全地管理凭证，或需要满足定期密钥轮换的安全合规策略时，可使用本技能。

## 支持的 Secret 类型

**AWS 服务**
- RDS 数据库凭证
- DocumentDB 凭证
- Redshift 凭证
- ElastiCache 凭证

**第三方服务**
- API 密钥
- OAuth token
- SSH 密钥
- 自定义凭证

## Secrets Manager 配置

### 创建 Secret

```bash
# Create RDS secret
aws secretsmanager create-secret \
  --name prod/db/mysql \
  --description "Production MySQL credentials" \
  --secret-string '{
    "username": "admin",
    "password": "CHANGE_ME",
    "engine": "mysql",
    "host": "mydb.cluster-abc.us-east-1.rds.amazonaws.com",
    "port": 3306,
    "dbname": "myapp"
  }'

# Create API key secret
aws secretsmanager create-secret \
  --name prod/api/stripe \
  --secret-string '{
    "api_key": "sk_live_xxxxx",
    "webhook_secret": "whsec_xxxxx"
  }'

# Create secret from file
aws secretsmanager create-secret \
  --name prod/ssh/private-key \
  --secret-binary fileb://~/.ssh/id_rsa
```

### 读取 Secret

```bash
# Get secret value
aws secretsmanager get-secret-value \
  --secret-id prod/db/mysql \
  --query 'SecretString' --output text

# Get specific field
aws secretsmanager get-secret-value \
  --secret-id prod/db/mysql \
  --query 'SecretString' --output text | \
  jq -r '.password'

# Get binary secret
aws secretsmanager get-secret-value \
  --secret-id prod/ssh/private-key \
  --query 'SecretBinary' --output text | \
  base64 -d > private-key.pem
```

## 自动轮换配置

### 启用 RDS 轮换

```bash
# Enable automatic rotation (30 days)
aws secretsmanager rotate-secret \
  --secret-id prod/db/mysql \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:SecretsManagerRDSMySQLRotation \
  --rotation-rules AutomaticallyAfterDays=30

# Rotate immediately
aws secretsmanager rotate-secret \
  --secret-id prod/db/mysql

# Check rotation status
aws secretsmanager describe-secret \
  --secret-id prod/db/mysql \
  --query 'RotationEnabled'
```

### Lambda 轮换函数

```python
# lambda_rotation.py
import boto3
import json
import os

secrets_client = boto3.client('secretsmanager')
rds_client = boto3.client('rds')

def lambda_handler(event, context):
    """Rotate RDS MySQL password"""
    
    secret_arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']
    
    # Get current secret
    current = secrets_client.get_secret_value(SecretId=secret_arn)
    secret = json.loads(current['SecretString'])
    
    if step == "createSecret":
        # Generate new password
        new_password = generate_password()
        secret['password'] = new_password
        
        # Store as pending
        secrets_client.put_secret_value(
            SecretId=secret_arn,
            ClientRequestToken=token,
            SecretString=json.dumps(secret),
            VersionStages=['AWSPENDING']
        )
    
    elif step == "setSecret":
        # Update RDS password
        rds_client.modify_db_instance(
            DBInstanceIdentifier=secret['dbInstanceIdentifier'],
            MasterUserPassword=secret['password'],
            ApplyImmediately=True
        )
    
    elif step == "testSecret":
        # Test new credentials
        import pymysql
        conn = pymysql.connect(
            host=secret['host'],
            user=secret['username'],
            password=secret['password'],
            database=secret['dbname']
        )
        conn.close()
    
    elif step == "finishSecret":
        # Mark as current
        secrets_client.update_secret_version_stage(
            SecretId=secret_arn,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token,
            RemoveFromVersionId=current['VersionId']
        )
    
    return {'statusCode': 200}

def generate_password(length=32):
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
```

### API 密钥的自定义轮换

```python
# api_key_rotation.py
import boto3
import requests
import json

secrets_client = boto3.client('secretsmanager')

def rotate_stripe_key(secret_arn, token, step):
    """Rotate Stripe API key"""
    
    current = secrets_client.get_secret_value(SecretId=secret_arn)
    secret = json.loads(current['SecretString'])
    
    if step == "createSecret":
        # Create new Stripe key via API
        response = requests.post(
            'https://api.stripe.com/v1/api_keys',
            auth=(secret['api_key'], ''),
            data={'name': f'rotated-{token[:8]}'}
        )
        new_key = response.json()['secret']
        
        secret['api_key'] = new_key
        secrets_client.put_secret_value(
            SecretId=secret_arn,
            ClientRequestToken=token,
            SecretString=json.dumps(secret),
            VersionStages=['AWSPENDING']
        )
    
    elif step == "testSecret":
        # Test new key
        response = requests.get(
            'https://api.stripe.com/v1/balance',
            auth=(secret['api_key'], '')
        )
        if response.status_code != 200:
            raise Exception("New key failed validation")
    
    elif step == "finishSecret":
        # Revoke old key
        old_key = json.loads(current['SecretString'])['api_key']
        requests.delete(
            f'https://api.stripe.com/v1/api_keys/{old_key}',
            auth=(secret['api_key'], '')
        )
        
        # Promote to current
        secrets_client.update_secret_version_stage(
            SecretId=secret_arn,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token
        )
```

## 轮换监控

### CloudWatch 告警

```bash
# Create alarm for rotation failures
aws cloudwatch put-metric-alarm \
  --alarm-name secrets-rotation-failures \
  --alarm-description "Alert on secrets rotation failures" \
  --metric-name RotationFailed \
  --namespace AWS/SecretsManager \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:alerts
```

### 轮换审计脚本

```bash
#!/bin/bash
# audit-rotations.sh

echo "Secrets Rotation Audit"
echo "====================="

aws secretsmanager list-secrets --query 'SecretList[*].[Name,RotationEnabled,LastRotatedDate]' \
  --output text | \
while read name enabled last_rotated; do
  echo ""
  echo "Secret: $name"
  echo "  Rotation Enabled: $enabled"
  echo "  Last Rotated: $last_rotated"
  
  if [ "$enabled" = "True" ]; then
    # Check rotation schedule
    rules=$(aws secretsmanager describe-secret --secret-id "$name" \
      --query 'RotationRules.AutomaticallyAfterDays' --output text)
    echo "  Rotation Schedule: Every $rules days"
    
    # Calculate days since last rotation
    if [ "$last_rotated" != "None" ]; then
      days_ago=$(( ($(date +%s) - $(date -d "$last_rotated" +%s)) / 86400 ))
      echo "  Days Since Rotation: $days_ago"
      
      if [ $days_ago -gt $rules ]; then
        echo "  ⚠️  OVERDUE for rotation!"
      fi
    fi
  fi
done
```

## 应用集成

### Python SDK

```python
import boto3
import json

def get_secret(secret_name):
    """Retrieve secret from Secrets Manager"""
    client = boto3.client('secretsmanager')
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise

# Usage
db_creds = get_secret('prod/db/mysql')
connection = pymysql.connect(
    host=db_creds['host'],
    user=db_creds['username'],
    password=db_creds['password'],
    database=db_creds['dbname']
)
```

### Node.js SDK

```javascript
const AWS = require('aws-sdk');
const secretsManager = new AWS.SecretsManager();

async function getSecret(secretName) {
  try {
    const data = await secretsManager.getSecretValue({
      SecretId: secretName
    }).promise();
    
    return JSON.parse(data.SecretString);
  } catch (err) {
    console.error('Error retrieving secret:', err);
    throw err;
  }
}

// Usage
const dbCreds = await getSecret('prod/db/mysql');
const connection = mysql.createConnection({
  host: dbCreds.host,
  user: dbCreds.username,
  password: dbCreds.password,
  database: dbCreds.dbname
});
```

## 轮换最佳实践

**规划阶段**
- [ ] 梳理所有需要轮换的 secrets
- [ ] 定义轮换周期（30 / 60 / 90 天）
- [ ] 先在非生产环境测试轮换
- [ ] 编写轮换流程文档
- [ ] 制定紧急轮换预案

**实施阶段**
- [ ] 优先使用 AWS 托管轮换
- [ ] 实现完善的错误处理
- [ ] 加入 CloudWatch 监控
- [ ] 验证应用兼容性
- [ ] 采用灰度发布

**运维阶段**
- [ ] 监控轮换成功/失败情况
- [ ] 配置失败告警
- [ ] 定期执行轮换审计
- [ ] 整理故障排查步骤
- [ ] 维护轮换 runbook

## 紧急轮换

```bash
# Immediate rotation (compromise detected)
aws secretsmanager rotate-secret \
  --secret-id prod/db/mysql \
  --rotate-immediately

# Force rotation even if recently rotated
aws secretsmanager rotate-secret \
  --secret-id prod/api/stripe \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:RotateStripeKey \
  --rotate-immediately

# Verify rotation completed
aws secretsmanager describe-secret \
  --secret-id prod/db/mysql \
  --query 'LastRotatedDate'
```

## 合规追踪

```python
#!/usr/bin/env python3
# compliance-report.py

import boto3
from datetime import datetime, timedelta

client = boto3.client('secretsmanager')

def generate_compliance_report():
    secrets = client.list_secrets()['SecretList']
    
    compliant = []
    non_compliant = []
    
    for secret in secrets:
        name = secret['Name']
        rotation_enabled = secret.get('RotationEnabled', False)
        last_rotated = secret.get('LastRotatedDate')
        
        if not rotation_enabled:
            non_compliant.append({
                'name': name,
                'issue': 'Rotation not enabled'
            })
            continue
        
        if last_rotated:
            days_ago = (datetime.now(last_rotated.tzinfo) - last_rotated).days
            if days_ago > 90:
                non_compliant.append({
                    'name': name,
                    'issue': f'Not rotated in {days_ago} days'
                })
            else:
                compliant.append(name)
        else:
            non_compliant.append({
                'name': name,
                'issue': 'Never rotated'
            })
    
    print(f"Compliant Secrets: {len(compliant)}")
    print(f"Non-Compliant Secrets: {len(non_compliant)}")
    print("\nNon-Compliant Details:")
    for item in non_compliant:
        print(f"  - {item['name']}: {item['issue']}")

if __name__ == "__main__":
    generate_compliance_report()
```

## 示例提示词

- "为我的 RDS 凭证配置自动轮换"
- "编写一个用于轮换 API 密钥的 Lambda 函数"
- "审计所有 secrets 的轮换合规情况"
- "为已泄露的凭证实施紧急轮换"
- "生成一份 secrets 轮换报告"

## Kiro CLI 集成

```bash
kiro-cli chat "Use aws-secrets-rotation to set up RDS credential rotation"
kiro-cli chat "Create a rotation audit report with aws-secrets-rotation"
```

## 补充资源

- [AWS Secrets Manager Rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [Rotation Lambda Templates](https://github.com/aws-samples/aws-secrets-manager-rotation-lambdas)
- [Best Practices for Secrets](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)

## 使用边界
- 仅在任务明确匹配上述范围时使用本技能。
- 不要把输出当作环境特定验证、测试或专家评审的替代。
- 若缺少必要输入、权限、安全边界或成功标准，请停下来与用户澄清。