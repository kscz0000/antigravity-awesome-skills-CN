---
name: shodan-reconnaissance
description: "提供利用 Shodan 作为渗透测试侦察工具的系统化方法论。触发词：Shodan侦察、渗透测试、信息收集、资产发现、漏洞扫描、物联网设备发现、网络侦察、Shodan搜索"
risk: unknown
source: community
author: zebbern
date_added: "2026-02-27"
---

# Shodan 侦察与渗透测试

## 目的

提供利用 Shodan 作为渗透测试侦察工具的系统化方法论。本技能涵盖 Shodan 网页界面、命令行接口（CLI）、REST API、搜索过滤器、按需扫描和网络监控功能，用于发现暴露的服务、存在漏洞的系统和物联网设备。

## 输入 / 前置条件

- **Shodan 账户**：shodan.io 的免费或付费账户
- **API 密钥**：从 Shodan 账户仪表板获取
- **目标信息**：待调查的 IP 地址、域名或网段
- **Shodan CLI**：已安装的 Python 命令行工具
- **授权**：对目标网络进行侦察的书面许可

## 输出 / 交付物

- **资产清单**：已发现的主机、端口和服务列表
- **漏洞报告**：已识别的 CVE 和暴露的脆弱服务
- **Banner 数据**：揭示软件版本的服务横幅
- **网络映射**：资产的地理和组织分布
- **截图集**：暴露界面的可视化侦察
- **导出数据**：用于进一步分析的 JSON/CSV 文件

## 核心工作流

### 1. 设置与配置

#### 安装 Shodan CLI
```bash
# 使用 pip
pip install shodan

# 或 easy_install
easy_install shodan

# 在 BlackArch/Arch Linux 上
sudo pacman -S python-shodan
```

#### 初始化 API 密钥
```bash
# 设置 API 密钥
shodan init YOUR_API_KEY

# 验证配置
shodan info
# 输出：Query credits available: 100
#         Scan credits available: 100
```

#### 检查账户状态
```bash
# 查看积分和套餐信息
shodan info

# 检查外部 IP
shodan myip

# 检查 CLI 版本
shodan version
```

### 2. 基础主机侦察

#### 查询单个主机
```bash
# 获取某个 IP 的全部信息
shodan host 1.1.1.1

# 示例输出：
# 1.1.1.1
# Hostnames: one.one.one.one
# Country: Australia
# Organization: Mountain View Communications
# Number of open ports: 3
# Ports:
#   53/udp
#   80/tcp
#   443/tcp
```

#### 检查主机是否为蜜罐
```bash
# 获取蜜罐概率评分
shodan honeyscore 192.168.1.100

# 输出：Not a honeypot
#         Score: 0.3
```

### 3. 搜索查询

#### 基础搜索（免费）
```bash
# 简单关键词搜索（不消耗积分）
shodan search apache

# 指定输出字段
shodan search --fields ip_str,port,os smb
```

#### 过滤搜索（1 积分）
```bash
# 按产品搜索
shodan search product:mongodb

# 多条件搜索
shodan search product:nginx country:US city:"New York"
```

#### 统计结果数量
```bash
# 获取结果数量（不消耗积分）
shodan count openssh
# 输出：23128

shodan count openssh 7
# 输出：219
```

#### 下载结果
```bash
# 下载 1000 条结果（默认）
shodan download results.json.gz "apache country:US"

# 下载指定数量的结果
shodan download --limit 5000 results.json.gz "nginx"

# 下载所有可用结果
shodan download --limit -1 all_results.json.gz "query"
```

#### 解析已下载数据
```bash
# 从已下载数据中提取特定字段
shodan parse --fields ip_str,port,hostnames results.json.gz

# 按特定条件过滤
shodan parse --fields location.country_code3,ip_str -f port:22 results.json.gz

# 导出为 CSV 格式
shodan parse --fields ip_str,port,org --separator , results.json.gz > results.csv
```

### 4. 搜索过滤器参考

#### 网络过滤器
```
ip:1.2.3.4                  # 特定 IP 地址
net:192.168.0.0/24          # 网段（CIDR）
hostname:example.com        # 主机名包含
port:22                     # 特定端口
asn:AS15169                 # 自治系统号
```

#### 地理位置过滤器
```
country:US                  # 两位国家代码
country:"United States"     # 完整国家名称
city:"San Francisco"        # 城市名称
state:CA                    # 州/地区
postal:94102                # 邮政编码
geo:37.7,-122.4             # 经纬度坐标
```

#### 组织过滤器
```
org:"Google"                # 组织名称
isp:"Comcast"               # ISP 名称
```

#### 服务/产品过滤器
```
product:nginx               # 软件产品
version:1.14.0              # 软件版本
os:"Windows Server 2019"    # 操作系统
http.title:"Dashboard"      # HTTP 页面标题
http.html:"login"           # HTML 内容
http.status:200             # HTTP 状态码
ssl.cert.subject.cn:*.example.com  # SSL 证书
ssl:true                    # 已启用 SSL
```

#### 漏洞过滤器
```
vuln:CVE-2019-0708          # 特定 CVE
has_vuln:true               # 存在任何漏洞
```

#### 截图过滤器
```
has_screenshot:true         # 有可用截图
screenshot.label:webcam     # 截图类型
```

### 5. 按需扫描

#### 提交扫描
```bash
# 扫描单个 IP（每个 IP 1 积分）
shodan scan submit 192.168.1.100

# 带详细输出的扫描（显示扫描 ID）
shodan scan submit --verbose 192.168.1.100

# 扫描并保存结果
shodan scan submit --filename scan_results.json.gz 192.168.1.100
```

#### 监控扫描状态
```bash
# 列出最近的扫描
shodan scan list

# 检查特定扫描状态
shodan scan status SCAN_ID

# 稍后下载扫描结果
shodan download --limit -1 results.json.gz scan:SCAN_ID
```

#### 可用扫描协议
```bash
# 列出可用协议/模块
shodan scan protocols
```

### 6. 统计与分析

#### 获取搜索统计
```bash
# 默认统计（前 10 个国家、组织）
shodan stats nginx

# 自定义分面
shodan stats --facets domain,port,asn --limit 5 nginx

# 保存为 CSV
shodan stats --facets country,org -O stats.csv apache
```

### 7. 网络监控

#### 设置告警（网页界面）
```
1. 导航至监控仪表板
2. 添加要监控的 IP、网段或域名
3. 配置通知服务（邮件、Slack、webhook）
4. 选择触发事件（新服务、漏洞等）
5. 在仪表板查看暴露的服务
```

### 8. REST API 使用

#### 直接 API 调用
```bash
# 获取 API 信息
curl -s "https://api.shodan.io/api-info?key=YOUR_KEY" | jq

# 主机查询
curl -s "https://api.shodan.io/shodan/host/1.1.1.1?key=YOUR_KEY" | jq

# 搜索查询
curl -s "https://api.shodan.io/shodan/host/search?key=YOUR_KEY&query=apache" | jq
```

#### Python 库
```python
import shodan

api = shodan.Shodan('YOUR_API_KEY')

# 搜索
results = api.search('apache')
print(f'Results found: {results["total"]}')
for result in results['matches']:
    print(f'IP: {result["ip_str"]}')

# 主机查询
host = api.host('1.1.1.1')
print(f'IP: {host["ip_str"]}')
print(f'Organization: {host.get("org", "n/a")}')
for item in host['data']:
    print(f'Port: {item["port"]}')
```

## 快速参考

### 常用 CLI 命令

| 命令 | 说明 | 积分 |
|------|------|------|
| `shodan init KEY` | 初始化 API 密钥 | 0 |
| `shodan info` | 显示账户信息 | 0 |
| `shodan myip` | 显示你的 IP | 0 |
| `shodan host IP` | 主机详情 | 0 |
| `shodan count QUERY` | 结果计数 | 0 |
| `shodan search QUERY` | 基础搜索 | 0* |
| `shodan download FILE QUERY` | 保存结果 | 1/100条 |
| `shodan parse FILE` | 提取数据 | 0 |
| `shodan stats QUERY` | 统计信息 | 1 |
| `shodan scan submit IP` | 按需扫描 | 1/IP |
| `shodan honeyscore IP` | 蜜罐检查 | 0 |

*使用过滤器时每次查询消耗 1 积分

### 常用搜索查询

| 目的 | 查询语句 |
|------|----------|
| 查找摄像头 | `webcam has_screenshot:true` |
| MongoDB 数据库 | `product:mongodb` |
| Redis 服务器 | `product:redis` |
| Elasticsearch | `product:elastic port:9200` |
| 默认密码 | `"default password"` |
| 存在漏洞的 RDP | `port:3389 vuln:CVE-2019-0708` |
| 工业控制系统 | `port:502 modbus` |
| Cisco 设备 | `product:cisco` |
| 开放的 VNC | `port:5900 authentication disabled` |
| 暴露的 FTP | `port:21 anonymous` |
| WordPress 站点 | `http.component:wordpress` |
| 打印机 | `"HP-ChaiSOE" port:80` |
| 摄像头（RTSP） | `port:554 has_screenshot:true` |
| Jenkins 服务器 | `X-Jenkins port:8080` |
| Docker API | `port:2375 product:docker` |

### 实用过滤器组合

| 场景 | 查询语句 |
|------|----------|
| 目标组织侦察 | `org:"Company Name"` |
| 域名枚举 | `hostname:example.com` |
| 网段扫描 | `net:192.168.0.0/24` |
| SSL 证书搜索 | `ssl.cert.subject.cn:*.target.com` |
| 存在漏洞的服务器 | `vuln:CVE-2021-44228 country:US` |
| 暴露的管理面板 | `http.title:"admin" port:443` |
| 数据库暴露 | `port:3306,5432,27017,6379` |

### 积分体系

| 操作 | 积分类型 | 费用 |
|------|----------|------|
| 基础搜索 | 查询 | 0（无过滤器） |
| 过滤搜索 | 查询 | 1 |
| 下载 100 条结果 | 查询 | 1 |
| 生成报告 | 查询 | 1 |
| 扫描 1 个 IP | 扫描 | 1 |
| 网络监控 | 监控 IP 数 | 取决于套餐 |

## 约束与限制

### 操作边界
- 速率限制为每秒 1 次请求
- 扫描结果非即时（异步）
- 24 小时内无法重复扫描同一 IP（非企业版）
- 免费账户积分有限
- 部分数据需要付费订阅

### 数据时效
- Shodan 持续爬取但数据可能已有数天/数周
- 按需扫描提供最新数据但消耗积分
- 历史数据需付费套餐

### 法律要求
- 仅对已授权的目标执行侦察
- 被动侦察通常合法但需确认管辖权
- 主动扫描（scan submit）需要授权
- 记录所有侦察活动

## 示例

### 示例 1：组织侦察
```bash
# 查找属于目标组织的所有主机
shodan search 'org:"Target Company"'

# 获取其基础设施的统计信息
shodan stats --facets port,product,country 'org:"Target Company"'

# 下载详细数据
shodan download target_data.json.gz 'org:"Target Company"'

# 解析特定信息
shodan parse --fields ip_str,port,product target_data.json.gz
```

### 示例 2：脆弱服务发现
```bash
# 查找受 BlueKeep（RDP CVE）影响的主机
shodan search 'vuln:CVE-2019-0708 country:US'

# 查找无认证的暴露 Elasticsearch
shodan search 'product:elastic port:9200 -authentication'

# 查找受 Log4j 影响的系统
shodan search 'vuln:CVE-2021-44228'
```

### 示例 3：物联网设备发现
```bash
# 查找暴露的摄像头
shodan search 'webcam has_screenshot:true country:US'

# 查找工业控制系统
shodan search 'port:502 product:modbus'

# 查找暴露的打印机
shodan search '"HP-ChaiSOE" port:80'

# 查找智能家居设备
shodan search 'product:nest'
```

### 示例 4：SSL/TLS 证书分析
```bash
# 查找具有特定 SSL 证书的主机
shodan search 'ssl.cert.subject.cn:*.example.com'

# 查找过期证书
shodan search 'ssl.cert.expired:true org:"Company"'

# 查找自签名证书
shodan search 'ssl.cert.issuer.cn:self-signed'
```

### 示例 5：Python 自动化脚本
```python
#!/usr/bin/env python3
import shodan
import json

API_KEY = 'YOUR_API_KEY'
api = shodan.Shodan(API_KEY)

def recon_organization(org_name):
    """对组织执行侦察"""
    try:
        # 搜索组织
        query = f'org:"{org_name}"'
        results = api.search(query)
        
        print(f"[*] Found {results['total']} hosts for {org_name}")
        
        # 收集唯一 IP 和端口
        hosts = {}
        for result in results['matches']:
            ip = result['ip_str']
            port = result['port']
            product = result.get('product', 'unknown')
            
            if ip not in hosts:
                hosts[ip] = []
            hosts[ip].append({'port': port, 'product': product})
        
        # 输出发现
        for ip, services in hosts.items():
            print(f"\n[+] {ip}")
            for svc in services:
                print(f"    - {svc['port']}/tcp ({svc['product']})")
        
        return hosts
        
    except shodan.APIError as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    recon_organization("Target Company")
```

### 示例 6：网段评估
```bash
# 扫描 /24 网段
shodan search 'net:192.168.1.0/24'

# 获取端口分布
shodan stats --facets port 'net:192.168.1.0/24'

# 查找网段中的特定漏洞
shodan search 'net:192.168.1.0/24 vuln:CVE-2021-44228'

# 导出网段全部数据
shodan download network_scan.json.gz 'net:192.168.1.0/24'
```

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 未配置 API 密钥 | 密钥未初始化 | 运行 `shodan init YOUR_API_KEY` 然后用 `shodan info` 验证 |
| 查询积分用尽 | 月度积分已消耗 | 使用无积分查询（无过滤器），等待重置，或升级 |
| 主机近期已爬取 | 24 小时内无法重复扫描 | 使用 `shodan host IP` 获取现有数据，或等待 24 小时 |
| 超出速率限制 | >1 请求/秒 | 在 API 请求间添加 `time.sleep(1)` |
| 搜索结果为空 | 条件过窄或语法错误 | 短语使用引号：`'org:"Company Name"'`；放宽条件 |
| 下载文件无法解析 | 文件损坏或格式错误 | 用 `gunzip -t file.gz` 验证，使用 `--limit` 重新下载 |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。