---
name: red-team-tools
description: "从顶尖安全研究员的方法论中提炼侦察、漏洞挖掘和赏金猎杀的实战工作流。自动化常见任务的同时保持对攻击面的全面覆盖。触发词：红队工具、安全侦察、漏洞挖掘、bug bounty、渗透测试、信息收集、自动化扫描、攻击面评估。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权的安全评估、防御验证或受控的教育环境。

# 红队工具与方法论

## 目的

从顶尖安全研究员的方法论中提炼侦察、漏洞挖掘和赏金猎杀的实战工作流。自动化常见任务的同时保持对攻击面的全面覆盖。

## 输入/前置条件

- 目标范围定义（域名、IP 段、应用）
- 基于 Linux 的攻击机（Kali、Ubuntu）
- Bug bounty 计划规则和范围
- 已安装工具依赖（Go、Python、Ruby）
- 各服务的 API key（Shodan、Censys 等）

## 输出/交付物

- 全面子域名枚举
- 存活主机发现和技术指纹识别
- 已识别的漏洞和攻击向量
- 自动化侦察流水线输出
- 记录在案的发现用于报告

## 核心工作流

### 1. 项目跟踪与收购目标

设置侦察跟踪：

```bash
# Create project structure
mkdir -p target/{recon,vulns,reports}
cd target

# Find acquisitions using Crunchbase
# Search manually for subsidiary companies

# Get ASN for targets
amass intel -org "Target Company" -src

# Alternative ASN lookup
curl -s "https://bgp.he.net/search?search=targetcompany&commit=Search"
```

### 2. 子域名枚举

全面的子域名发现：

```bash
# Create wildcards file
echo "target.com" > wildcards

# Run Amass passively
amass enum -passive -d target.com -src -o amass_passive.txt

# Run Amass actively
amass enum -active -d target.com -src -o amass_active.txt

# Use Subfinder
subfinder -d target.com -silent -o subfinder.txt

# Asset discovery
cat wildcards | assetfinder --subs-only | anew domains.txt

# Alternative subdomain tools
findomain -t target.com -o

# Generate permutations with dnsgen
cat domains.txt | dnsgen - | httprobe > permuted.txt

# Combine all sources
cat amass_*.txt subfinder.txt | sort -u > all_subs.txt
```

### 3. 存活主机发现

识别有响应的主机：

```bash
# Check which hosts are live with httprobe
cat domains.txt | httprobe -c 80 --prefer-https | anew hosts.txt

# Use httpx for more details
cat domains.txt | httpx -title -tech-detect -status-code -o live_hosts.txt

# Alternative with massdns
massdns -r resolvers.txt -t A -o S domains.txt > resolved.txt
```

### 4. 技术指纹识别

识别目标技术栈以进行定向攻击：

```bash
# Whatweb scanning
whatweb -i hosts.txt -a 3 -v > tech_stack.txt

# Nuclei technology detection
nuclei -l hosts.txt -t technologies/ -o tech_nuclei.txt

# Wappalyzer (if available)
# Browser extension for manual review
```

### 5. 内容发现

查找隐藏的端点和文件：

```bash
# Directory bruteforce with ffuf
ffuf -ac -v -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt

# Historical URLs from Wayback
waybackurls target.com | tee wayback.txt

# Find all URLs with gau
gau target.com | tee all_urls.txt

# Parameter discovery
cat all_urls.txt | grep "=" | sort -u > params.txt

# Generate custom wordlist from historical data
cat all_urls.txt | unfurl paths | sort -u > custom_wordlist.txt
```

### 6. 应用分析（Jason Haddix 方法）

**热力图优先级区域：**

1. **文件上传** - 测试注入、XXE、SSRF、shell 上传
2. **Content Types** - 在 Burp 中过滤 multipart 表单
3. **API** - 寻找隐藏方法、缺少认证
4. **个人资料区域** - 存储型 XSS、自定义字段
5. **集成接口** - 通过第三方的 SSRF
6. **错误页面** - 非常规注入点

**分析问题：**
- 应用如何传递数据？（参数、API、混合型）
- 应用在何处涉及用户？（UID、UUID 端点）
- 站点是否有多租户或用户级别？
- 是否有独特的威胁模型？
- 站点如何处理 XSS/CSRF？
- 站点是否有过往的漏洞报告/利用？

### 7. 自动化 XSS 猎杀

```bash
# ParamSpider for parameter extraction
python3 paramspider.py --domain target.com -o params.txt

# Filter with Gxss
cat params.txt | Gxss -p test

# Dalfox for XSS testing
cat params.txt | dalfox pipe --mining-dict params.txt -o xss_results.txt

# Alternative workflow
waybackurls target.com | grep "=" | qsreplace '"><script>alert(1)</script>' | while read url; do
    curl -s "$url" | grep -q 'alert(1)' && echo "$url"
done > potential_xss.txt
```

### 8. 漏洞扫描

```bash
# Nuclei comprehensive scan
nuclei -l hosts.txt -t ~/nuclei-templates/ -o nuclei_results.txt

# Check for common CVEs
nuclei -l hosts.txt -t cves/ -o cve_results.txt

# Web vulnerabilities
nuclei -l hosts.txt -t vulnerabilities/ -o vuln_results.txt
```

### 9. API 枚举

**API Fuzzing 字典：**

```bash
# Enumerate API endpoints
ffuf -u https://target.com/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt

# Test API versions
ffuf -u https://target.com/api/v1/FUZZ -w api_wordlist.txt
ffuf -u https://target.com/api/v2/FUZZ -w api_wordlist.txt

# Check for hidden methods
for method in GET POST PUT DELETE PATCH; do
    curl -X $method https://target.com/api/users -v
done
```

### 10. 自动化侦察脚本

```bash
#!/bin/bash
domain=$1

if [[ -z $domain ]]; then
    echo "Usage: ./recon.sh <domain>"
    exit 1
fi

mkdir -p "$domain"

# Subdomain enumeration
echo "[*] Enumerating subdomains..."
subfinder -d "$domain" -silent > "$domain/subs.txt"

# Live host discovery
echo "[*] Finding live hosts..."
cat "$domain/subs.txt" | httpx -title -tech-detect -status-code > "$domain/live.txt"

# URL collection
echo "[*] Collecting URLs..."
cat "$domain/live.txt" | waybackurls > "$domain/urls.txt"

# Nuclei scanning
echo "[*] Running Nuclei..."
nuclei -l "$domain/live.txt" -o "$domain/nuclei.txt"

echo "[+] Recon complete!"
```

## 速查表

### 核心工具

| 工具 | 用途 |
|------|------|
| Amass | 子域名枚举 |
| Subfinder | 快速子域名发现 |
| httpx/httprobe | 存活主机检测 |
| ffuf | 内容发现 |
| Nuclei | 漏洞扫描 |
| Burp Suite | 手动测试 |
| Dalfox | XSS 自动化 |
| waybackurls | 历史 URL 挖掘 |

### 需要检查的关键 API 端点

```
/api/v1/users
/api/v1/admin
/api/v1/profile
/api/users/me
/api/config
/api/debug
/api/swagger
/api/graphql
```

### XSS 过滤器测试

```html
<!-- Test encoding handling -->
<h1><img><table>
<script>
%3Cscript%3E
%253Cscript%253E
%26lt;script%26gt;
```

## 约束

- 遵守计划范围边界
- 未经许可避免在生产环境进行 DoS 或 Fuzzing
- 对请求进行限速以避免被封锁
- 部分工具可能产生误报
- 部分工具的完整功能需要 API key

## 示例

### 示例 1：快速子域名侦察

```bash
subfinder -d target.com | httpx -title | tee results.txt
```

### 示例 2：XSS 猎杀流水线

```bash
waybackurls target.com | grep "=" | qsreplace "test" | httpx -silent | dalfox pipe
```

### 示例 3：全面扫描

```bash
# Full recon chain
amass enum -d target.com | httpx | nuclei -t ~/nuclei-templates/
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 被限速 | 使用代理轮换，降低并发 |
| 结果过多 | 聚焦特定技术栈 |
| 误报 | 报告前手动验证发现 |
| 缺失子域名 | 组合多个枚举源 |
| API key 报错 | 在配置文件中验证 key |
| 工具未找到 | 使用 `go install` 安装 Go 工具 |

## 使用场景
本技能适用于执行概述中描述的工作流或操作。
