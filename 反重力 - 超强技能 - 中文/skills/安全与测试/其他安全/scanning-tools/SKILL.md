---
name: scanning-tools
description: "掌握网络发现、漏洞评估、Web 应用测试、无线安全和合规验证的核心安全扫描工具。涵盖工具选型、配置和实际使用方法。触发词：安全扫描、漏洞扫描、网络扫描、渗透测试、Nmap、Nessus、Web 安全、无线安全、合规扫描"
risk: unknown
source: community
author: zebbern
date_added: "2026-02-27"
---

# 安全扫描工具

## 用途

掌握网络发现、漏洞评估、Web 应用测试、无线安全和合规验证的核心安全扫描工具。涵盖工具选型、配置和实际使用方法。

## 前置条件

### 环境要求
- Linux 系统（推荐 Kali Linux）
- 对目标系统的网络访问权限
- 合法的扫描授权

### 知识要求
- 基础网络概念（TCP/IP、端口、协议）
- 了解常见漏洞类型
- 熟悉命令行操作

## 输出与交付物

1. **网络发现报告** - 已识别的主机、端口和服务
2. **漏洞评估报告** - CVE、错误配置、风险评级
3. **Web 应用安全报告** - OWASP Top 10 发现
4. **合规报告** - CIS 基准、PCI-DSS、HIPAA 检查

## 核心工作流

### 阶段一：网络扫描工具

#### Nmap（网络映射器）

网络发现和安全审计的首选工具：

```bash
# Host discovery
nmap -sn 192.168.1.0/24              # Ping scan (no port scan)
nmap -sL 192.168.1.0/24              # List scan (DNS resolution)
nmap -Pn 192.168.1.100               # Skip host discovery

# Port scanning techniques
nmap -sS 192.168.1.100               # TCP SYN scan (stealth)
nmap -sT 192.168.1.100               # TCP connect scan
nmap -sU 192.168.1.100               # UDP scan
nmap -sA 192.168.1.100               # ACK scan (firewall detection)

# Port specification
nmap -p 80,443 192.168.1.100         # Specific ports
nmap -p- 192.168.1.100               # All 65535 ports
nmap -p 1-1000 192.168.1.100         # Port range
nmap --top-ports 100 192.168.1.100   # Top 100 common ports

# Service and OS detection
nmap -sV 192.168.1.100               # Service version detection
nmap -O 192.168.1.100                # OS detection
nmap -A 192.168.1.100                # Aggressive (OS, version, scripts)

# Timing and performance
nmap -T0 192.168.1.100               # Paranoid (slowest, IDS evasion)
nmap -T4 192.168.1.100               # Aggressive (faster)
nmap -T5 192.168.1.100               # Insane (fastest)

# NSE Scripts
nmap --script=vuln 192.168.1.100     # Vulnerability scripts
nmap --script=http-enum 192.168.1.100  # Web enumeration
nmap --script=smb-vuln* 192.168.1.100  # SMB vulnerabilities
nmap --script=default 192.168.1.100  # Default script set

# Output formats
nmap -oN scan.txt 192.168.1.100      # Normal output
nmap -oX scan.xml 192.168.1.100      # XML output
nmap -oG scan.gnmap 192.168.1.100    # Grepable output
nmap -oA scan 192.168.1.100          # All formats
```

#### Masscan

面向大型网络的高速端口扫描工具：

```bash
# Basic scanning
masscan -p80 192.168.1.0/24 --rate=1000
masscan -p80,443,8080 192.168.1.0/24 --rate=10000

# Full port range
masscan -p0-65535 192.168.1.0/24 --rate=5000

# Large-scale scanning
masscan 0.0.0.0/0 -p443 --rate=100000 --excludefile exclude.txt

# Output formats
masscan -p80 192.168.1.0/24 -oG results.gnmap
masscan -p80 192.168.1.0/24 -oJ results.json
masscan -p80 192.168.1.0/24 -oX results.xml

# Banner grabbing
masscan -p80 192.168.1.0/24 --banners
```

### 阶段二：漏洞扫描工具

#### Nessus

企业级漏洞评估平台：

```bash
# Start Nessus service
sudo systemctl start nessusd

# Access web interface
# https://localhost:8834

# Command-line (nessuscli)
nessuscli scan --create --name "Internal Scan" --targets 192.168.1.0/24
nessuscli scan --list
nessuscli scan --launch <scan_id>
nessuscli report --format pdf --output report.pdf <scan_id>
```

Nessus 核心特性：
- 全面的 CVE 检测
- 合规检查（PCI-DSS、HIPAA、CIS）
- 自定义扫描模板
- 凭证扫描，深入分析
- 定期插件更新

#### OpenVAS（Greenbone）

开源漏洞扫描平台：

```bash
# Install OpenVAS
sudo apt install openvas
sudo gvm-setup

# Start services
sudo gvm-start

# Access web interface (Greenbone Security Assistant)
# https://localhost:9392

# Command-line operations
gvm-cli socket --xml "<get_version/>"
gvm-cli socket --xml "<get_tasks/>"

# Create and run scan
gvm-cli socket --xml '
<create_target>
  <name>Test Target</name>
  <hosts>192.168.1.0/24</hosts>
</create_target>'
```

### 阶段三：Web 应用扫描工具

#### Burp Suite

综合性的 Web 应用测试平台：

```
# Proxy configuration
1. Set browser proxy to 127.0.0.1:8080
2. Import Burp CA certificate for HTTPS
3. Add target to scope

# Key modules:
- Proxy: Intercept and modify requests
- Spider: Crawl web applications
- Scanner: Automated vulnerability detection
- Intruder: Automated attacks (fuzzing, brute-force)
- Repeater: Manual request manipulation
- Decoder: Encode/decode data
- Comparer: Compare responses
```

核心测试流程：
1. 配置代理和作用域
2. 爬取应用
3. 分析站点地图
4. 运行主动扫描器
5. 使用 Repeater/Intruder 进行手动测试
6. 审查发现并生成报告

#### OWASP ZAP

开源 Web 应用扫描器：

```bash
# Start ZAP
zaproxy

# Automated scan from CLI
zap-cli quick-scan https://target.com

# Full scan
zap-cli spider https://target.com
zap-cli active-scan https://target.com

# Generate report
zap-cli report -o report.html -f html

# API mode
zap.sh -daemon -port 8080 -config api.key=<your_key>
```

ZAP 自动化扫描：
```bash
# Docker-based scanning
docker run -t owasp/zap2docker-stable zap-full-scan.py \
  -t https://target.com -r report.html

# Baseline scan (passive only)
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://target.com -r report.html
```

#### Nikto

Web 服务器漏洞扫描器：

```bash
# Basic scan
nikto -h https://target.com

# Scan specific port
nikto -h target.com -p 8080

# Scan with SSL
nikto -h target.com -ssl

# Multiple targets
nikto -h targets.txt

# Output formats
nikto -h target.com -o report.html -Format html
nikto -h target.com -o report.xml -Format xml
nikto -h target.com -o report.csv -Format csv

# Tuning options
nikto -h target.com -Tuning 123456789  # All tests
nikto -h target.com -Tuning x          # Exclude specific tests
```

### 阶段四：无线扫描工具

#### Aircrack-ng 套件

无线网络渗透测试工具：

```bash
# Check wireless interface
airmon-ng

# Enable monitor mode
sudo airmon-ng start wlan0

# Scan for networks
sudo airodump-ng wlan0mon

# Capture specific network
sudo airodump-ng -c <channel> --bssid <target_bssid> -w capture wlan0mon

# Deauthentication attack
sudo aireplay-ng -0 10 -a <bssid> wlan0mon

# Crack WPA handshake
aircrack-ng -w wordlist.txt -b <bssid> capture*.cap

# Crack WEP
aircrack-ng -b <bssid> capture*.cap
```

#### Kismet

被动式无线检测工具：

```bash
# Start Kismet
kismet

# Specify interface
kismet -c wlan0

# Access web interface
# http://localhost:2501

# Detect hidden networks
# Kismet passively collects all beacon frames
# including those from hidden SSIDs
```

### 阶段五：恶意软件与漏洞利用扫描

#### ClamAV

开源杀毒扫描工具：

```bash
# Update virus definitions
sudo freshclam

# Scan directory
clamscan -r /path/to/scan

# Scan with verbose output
clamscan -r -v /path/to/scan

# Move infected files
clamscan -r --move=/quarantine /path/to/scan

# Remove infected files
clamscan -r --remove /path/to/scan

# Scan specific file types
clamscan -r --include='\.exe$|\.dll$' /path/to/scan

# Output to log
clamscan -r -l scan.log /path/to/scan
```

#### Metasploit 漏洞验证

通过利用验证漏洞真实性：

```bash
# Start Metasploit
msfconsole

# Database setup
msfdb init
db_status

# Import Nmap results
db_import /path/to/nmap_scan.xml

# Vulnerability scanning
use auxiliary/scanner/smb/smb_ms17_010
set RHOSTS 192.168.1.0/24
run

# Auto exploitation
vulns                           # View vulnerabilities
analyze                         # Suggest exploits
```

### 阶段六：云安全扫描

#### Prowler（AWS）

AWS 安全评估工具：

```bash
# Install Prowler
pip install prowler

# Basic scan
prowler aws

# Specific checks
prowler aws -c iam s3 ec2

# Compliance framework
prowler aws --compliance cis_aws

# Output formats
prowler aws -M html json csv

# Specific region
prowler aws -f us-east-1

# Assume role
prowler aws -R arn:aws:iam::123456789012:role/ProwlerRole
```

#### ScoutSuite（多云）

多云安全审计工具：

```bash
# Install ScoutSuite
pip install scoutsuite

# AWS scan
scout aws

# Azure scan
scout azure --cli

# GCP scan
scout gcp --user-account

# Generate report
scout aws --report-dir ./reports
```

### 阶段七：合规扫描

#### Lynis

Unix/Linux 安全审计工具：

```bash
# Run audit
sudo lynis audit system

# Quick scan
sudo lynis audit system --quick

# Specific profile
sudo lynis audit system --profile server

# Output report
sudo lynis audit system --report-file /tmp/lynis-report.dat

# Check specific section
sudo lynis show profiles
sudo lynis audit system --tests-from-group malware
```

#### OpenSCAP

安全合规扫描工具：

```bash
# List available profiles
oscap info /usr/share/xml/scap/ssg/content/ssg-<distro>-ds.xml

# Run scan with profile
oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_pci-dss \
  --report report.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel8-ds.xml

# Generate fix script
oscap xccdf generate fix \
  --profile xccdf_org.ssgproject.content_profile_pci-dss \
  --output remediation.sh \
  /usr/share/xml/scap/ssg/content/ssg-rhel8-ds.xml
```

### 阶段八：扫描方法论

结构化扫描流程：

1. **规划**
   - 定义范围和目标
   - 获取合法授权
   - 选择合适的工具

2. **发现**
   - 主机发现（Nmap ping 扫描）
   - 端口扫描
   - 服务枚举

3. **漏洞评估**
   - 自动化扫描（Nessus/OpenVAS）
   - Web 应用扫描（Burp/ZAP）
   - 人工验证

4. **分析**
   - 关联发现结果
   - 排除误报
   - 按严重程度排序

5. **报告**
   - 记录发现
   - 提供修复建议
   - 编写执行摘要

### 阶段九：工具选型指南

根据不同场景选择合适的工具：

| 场景 | 推荐工具 |
|------|----------|
| 网络发现 | Nmap、Masscan |
| 漏洞评估 | Nessus、OpenVAS |
| Web 应用测试 | Burp Suite、ZAP、Nikto |
| 无线安全 | Aircrack-ng、Kismet |
| 恶意软件检测 | ClamAV、YARA |
| 云安全 | Prowler、ScoutSuite |
| 合规检查 | Lynis、OpenSCAP |
| 协议分析 | Wireshark、tcpdump |

### 阶段十：报告与文档

生成专业报告：

```bash
# Nmap XML to HTML
xsltproc nmap-output.xml -o report.html

# OpenVAS report export
gvm-cli socket --xml '<get_reports report_id="<id>" format_id="<pdf_format>"/>'

# Combine multiple scan results
# Use tools like Faraday, Dradis, or custom scripts

# Executive summary template:
# 1. Scope and methodology
# 2. Key findings summary
# 3. Risk distribution chart
# 4. Critical vulnerabilities
# 5. Remediation recommendations
# 6. Detailed technical findings
```

## 快速参考

### Nmap 速查表

| 扫描类型 | 命令 |
|----------|------|
| Ping 扫描 | `nmap -sn <target>` |
| 快速扫描 | `nmap -T4 -F <target>` |
| 全端口扫描 | `nmap -p- <target>` |
| 服务扫描 | `nmap -sV <target>` |
| 操作系统检测 | `nmap -O <target>` |
| 激进模式 | `nmap -A <target>` |
| 漏洞脚本 | `nmap --script=vuln <target>` |
| 隐蔽扫描 | `nmap -sS -T2 <target>` |

### 常用端口参考

| 端口 | 服务 |
|------|------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 3389 | RDP |

## 约束与限制

### 法律须知
- 始终获取书面授权
- 严格遵守扫描范围
- 遵循负责任的漏洞披露流程
- 遵守当地法律法规

### 技术限制
- 部分扫描可能触发 IDS/IPS 告警
- 大规模扫描可能影响网络性能
- 误报需要人工验证
- 加密流量可能限制分析深度

### 最佳实践
- 从非侵入式扫描开始
- 逐步提升扫描强度
- 记录所有扫描活动
- 报告前先验证发现

## 故障排查

### 扫描未发现主机

**解决方案：**
1. 尝试不同发现方式：`nmap -Pn` 或 `nmap -sn -PS/PA/PU`
2. 检查防火墙是否阻止了 ICMP
3. 使用 TCP SYN 扫描：`nmap -PS22,80,443`
4. 验证网络连通性

### 扫描速度过慢

**解决方案：**
1. 提升时序级别：`nmap -T4` 或 `-T5`
2. 缩小端口范围：`--top-ports 100`
3. 使用 Masscan 进行初始发现
4. 禁用 DNS 解析：`-n`

### Web 扫描器遗漏漏洞

**解决方案：**
1. 登录认证以访问受保护区域
2. 增加爬取深度
3. 添加自定义注入点
4. 使用多种工具提高覆盖率
5. 进行手动测试

## 适用场景
本技能适用于执行概述中描述的工作流程或操作。
