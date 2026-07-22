---
name: ffuf-web-fuzzing
description: 渗透测试中使用 ffuf 进行 Web 模糊测试的专家指南，包括基于原始请求的认证模糊测试、自动校准和结果分析
risk: unknown
source: community
---

# FFUF (Fuzz Faster U Fool) 技能

## 使用场景
- 在授权的安全测试或渗透测试中使用 `ffuf` 对 Web 目标进行模糊测试。
- 任务涉及内容发现、子域名枚举、参数模糊测试或认证请求模糊测试。
- 需要关于字典、过滤、校准和高效解读 ffuf 结果的指导。

## 概述
FFUF 是一个用 Go 语言编写的快速 Web 模糊测试工具，设计用于在渗透测试中发现隐藏内容、目录、文件、子域名以及测试漏洞。它比 dirb 或 dirbuster 等传统工具快得多。

## 安装
```bash
# 使用 Go
go install github.com/ffuf/ffuf/v2@latest

# 使用 Homebrew (macOS)
brew install ffuf

# 二进制文件下载
# 下载地址: https://github.com/ffuf/ffuf/releases/latest
```

## 核心概念

### FUZZ 关键字
`FUZZ` 关键字用作占位符，会被字典中的条目替换。可以放在任何位置：
- URL: `https://target.com/FUZZ`
- 请求头: `-H "Host: FUZZ"`
- POST 数据: `-d "username=admin&password=FUZZ"`
- 使用自定义关键字的多位置: `-w wordlist.txt:CUSTOM` 然后使用 `CUSTOM` 代替 `FUZZ`

### 多字典模式
- **clusterbomb**: 测试所有组合（默认）- 笛卡尔积
- **pitchfork**: 并行遍历字典（一对一匹配）
- **sniper**: 逐个位置测试（用于多个 FUZZ 位置）

## 常见用例

### 1. 目录和文件发现
```bash
# 基础目录模糊测试
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ

# 带文件扩展名
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -e .php,.html,.txt,.pdf

# 彩色详细输出
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -c -v

# 递归扫描（发现嵌套目录）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -recursion -recursion-depth 2
```

### 2. 子域名枚举
```bash
# 虚拟主机发现
ffuf -w /path/to/subdomains.txt -u https://target.com -H "Host: FUZZ.target.com" -fs 4242

# 注意: -fs 4242 过滤掉大小为 4242 的响应（根据默认响应大小调整）
```

### 3. 参数模糊测试
```bash
# GET 参数名
ffuf -w /path/to/params.txt -u https://target.com/script.php?FUZZ=test_value -fs 4242

# GET 参数值
ffuf -w /path/to/values.txt -u https://target.com/script.php?id=FUZZ -fc 401

# 多参数
ffuf -w params.txt:PARAM -w values.txt:VAL -u https://target.com/?PARAM=VAL -mode clusterbomb
```

### 4. POST 数据模糊测试
```bash
# 基础 POST 模糊测试
ffuf -w /path/to/passwords.txt -X POST -d "username=admin&password=FUZZ" -u https://target.com/login.php -fc 401

# JSON POST 数据
ffuf -w entries.txt -u https://target.com/api -X POST -H "Content-Type: application/json" -d '{"name": "FUZZ", "key": "value"}' -fr "error"

# 模糊测试多个 POST 字段
ffuf -w users.txt:USER -w passes.txt:PASS -X POST -d "username=USER&password=PASS" -u https://target.com/login -mode pitchfork
```

### 5. 请求头模糊测试
```bash
# 自定义请求头
ffuf -w /path/to/wordlist.txt -u https://target.com -H "X-Custom-Header: FUZZ"

# 多个请求头
ffuf -w /path/to/wordlist.txt -u https://target.com -H "User-Agent: FUZZ" -H "X-Forwarded-For: 127.0.0.1"
```

## 过滤和匹配

### 匹配器（包含结果）
- `-mc`: 匹配状态码（默认: 200-299,301,302,307,401,403,405,500）
- `-ml`: 匹配行数
- `-mr`: 匹配正则表达式
- `-ms`: 匹配响应大小
- `-mt`: 匹配响应时间（例如 `>100` 或 `<100` 毫秒）
- `-mw`: 匹配字数

### 过滤器（排除结果）
- `-fc`: 过滤状态码（例如 `-fc 404,403,401`）
- `-fl`: 过滤行数
- `-fr`: 过滤正则表达式（例如 `-fr "error"`）
- `-fs`: 过滤响应大小（例如 `-fs 42,4242`）
- `-ft`: 过滤响应时间
- `-fw`: 过滤字数

### 自动校准（默认使用！）
**关键:** 除非有特殊原因，否则始终使用 `-ac`。这对于让 Claude 分析结果尤为重要，因为它能大幅减少噪音和误报。

```bash
# 自动校准 - 始终使用此选项
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -ac

# 每主机自动校准（适用于多主机）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -ach

# 自定义自动校准字符串（用于特定模式）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -acc "404NotFound"
```

**为什么 `-ac` 至关重要:**
- 自动检测并过滤重复的误报响应
- 消除动态网站随机内容产生的噪音
- 使人类和 Claude 都更容易分析结果
- 防止成千上万个相同的 404/403 响应干扰输出
- 适应目标的特定行为

**当 Claude 分析你的 ffuf 结果时，`-ac` 是强制性的** - 没有它，Claude 将浪费时间筛选成千上万个误报，而不是发现有趣的异常。

## 速率限制和计时

### 速率控制
```bash
# 限制为每秒 2 个请求（隐蔽模式）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -rate 2

# 请求间添加延迟（0.1 到 2 秒随机）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -p 0.1-2.0

# 设置并发线程数（默认: 40）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -t 10
```

### 时间限制
```bash
# 最大总执行时间（60 秒）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -maxtime 60

# 每个任务的最大时间（配合递归使用）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -maxtime-job 60 -recursion
```

## 输出选项

### 输出格式
```bash
# JSON 输出
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -o results.json

# HTML 输出
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -of html -o results.html

# CSV 输出
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -of csv -o results.csv

# 所有格式
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -of all -o results

# 静默模式（无进度，仅结果）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -s

# 通过 tee 管道输出到文件
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -s | tee results.txt
```

## 高级技巧

### 使用原始 HTTP 请求（认证模糊测试的关键）
这是 ffuf 最强大的功能之一，特别适用于带有复杂请求头、Cookie 或令牌的认证请求。

**工作流程:**
1. 捕获完整的认证请求（来自 Burp Suite、浏览器开发者工具等）
2. 保存到文件（如 `req.txt`）
3. 将要模糊测试的值替换为 `FUZZ` 关键字
4. 使用 `--request` 标志

```bash
# 从包含原始 HTTP 请求的文件
ffuf --request req.txt -w /path/to/wordlist.txt -ac
```

**req.txt 文件示例:**
```http
POST /api/v1/users/FUZZ HTTP/1.1
Host: target.com
User-Agent: Mozilla/5.0
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Cookie: session=abc123xyz; csrftoken=def456
Content-Type: application/json
Content-Length: 27

{"action":"view","id":"1"}
```

**使用场景:**
- 对带有复杂认证请求头的认证端点进行模糊测试
- 测试带有 JWT 令牌的 API 端点
- 使用 CSRF 令牌、会话 Cookie 和自定义请求头进行模糊测试
- 测试需要特定 User-Agent 或 Accept 请求头的端点
- 带认证的 POST/PUT/DELETE 请求

**专业提示:**
- 可以在多个位置放置 FUZZ: URL 路径、请求头、请求体
- 如需要使用 `-request-proto https`（默认为 https）
- 始终使用 `-ac` 过滤认证后的"未找到"或错误响应
- 非常适合 IDOR 测试: 在认证上下文中模糊测试用户 ID、文档 ID 等

```bash
# 常见认证模糊测试模式
ffuf --request req.txt -w user_ids.txt -ac -mc 200 -o results.json

# 使用自定义关键字的多 FUZZ 位置
ffuf --request req.txt -w endpoints.txt:ENDPOINT -w ids.txt:ID -mode pitchfork -ac
```

### 代理使用
```bash
# HTTP 代理（适用于 Burp Suite）
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -x http://127.0.0.1:8080

# SOCKS5 代理
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -x socks5://127.0.0.1:1080

# 通过代理重放匹配的请求
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -replay-proxy http://127.0.0.1:8080
```

### Cookie 和认证
```bash
# 使用 Cookie
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -b "sessionid=abc123; token=xyz789"

# 客户端证书认证
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -cc client.crt -ck client.key
```

### 编码
```bash
# URL 编码
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -enc 'FUZZ:urlencode'

# 多重编码
ffuf -w /path/to/wordlist.txt -u https://target.com/FUZZ -enc 'FUZZ:urlencode b64encode'
```

### 漏洞测试
```bash
# SQL 注入测试
ffuf -w sqli_payloads.txt -u https://target.com/page.php?id=FUZZ -fs 1234

# XSS 测试
ffuf -w xss_payloads.txt -u https://target.com/search?q=FUZZ -mr "<script>"

# 命令注入
ffuf -w cmdi_payloads.txt -u https://target.com/execute?cmd=FUZZ -fr "error"
```

### 批量处理多目标
```bash
# 处理多个 URL
cat targets.txt | xargs -I@ sh -c 'ffuf -w wordlist.txt -u @/FUZZ -ac'

# 遍历多个目标并保存结果
for url in $(cat targets.txt); do 
    ffuf -w wordlist.txt -u $url/FUZZ -ac -o "results_$(echo $url | md5sum | cut -d' ' -f1).json"
done
```

## 最佳实践

### 1. 始终使用自动校准
每次扫描默认使用 `-ac`。这对高效的渗透测试是不可商量的:
```bash
ffuf -w wordlist.txt -u https://target.com/FUZZ -ac
```

### 2. 认证使用原始请求
不要为复杂认证纠结于命令行标志。捕获完整请求并使用 `--request`:
```bash
# 1. 从 Burp/开发者工具捕获认证请求
# 2. 保存到 req.txt，用 FUZZ 关键字替换
# 3. 使用 -ac 运行
ffuf --request req.txt -w wordlist.txt -ac -o results.json
```

### 3. 使用合适的字典
- **目录发现**: SecLists Discovery/Web-Content (raft-large-directories.txt, directory-list-2.3-medium.txt)
- **子域名**: SecLists Discovery/DNS (subdomains-top1million-5000.txt)
- **参数**: SecLists Discovery/Web-Content (burp-parameter-names.txt)
- **用户名**: SecLists Usernames
- **密码**: SecLists Passwords
- 来源: https://github.com/danielmiessler/SecLists

### 3. 隐蔽的速率限制
使用 `-rate` 避免触发 WAF/IDS 或压垮服务器:
```bash
ffuf -w wordlist.txt -u https://target.com/FUZZ -rate 2 -t 10
```

### 4. 策略性过滤
- 先检查默认响应以识别常见响应大小、状态码或模式
- 使用 `-fs` 按大小过滤或 `-fc` 按状态码过滤
- 组合过滤器: `-fc 403,404 -fs 1234`

### 5. 适当保存结果
始终将结果保存到文件以便后续分析:
```bash
ffuf -w wordlist.txt -u https://target.com/FUZZ -o results.json -of json
```

### 6. 使用交互模式
执行期间按 ENTER 进入交互模式，可以:
- 实时调整过滤器
- 保存当前结果
- 重启扫描
- 管理队列

### 7. 递归深度
注意递归深度，避免陷入无限循环或压垮服务器:
```bash
ffuf -w wordlist.txt -u https://target.com/FUZZ -recursion -recursion-depth 2 -maxtime-job 120
```

## 常见模式和单行命令

### 快速目录扫描
```bash
ffuf -w ~/wordlists/common.txt -u https://target.com/FUZZ -mc 200,301,302,403 -ac -c -v
```

### 带扩展名的全面扫描
```bash
ffuf -w ~/wordlists/raft-large-directories.txt -u https://target.com/FUZZ -e .php,.html,.txt,.bak,.old -ac -c -v -o results.json
```

### 认证模糊测试（原始请求）
```bash
# 1. 将认证请求保存到 req.txt，带 FUZZ 关键字
# 2. 运行:
ffuf --request req.txt -w ~/wordlists/api-endpoints.txt -ac -o results.json -of json
```

### API 端点发现
```bash
ffuf -w ~/wordlists/api-endpoints.txt -u https://api.target.com/v1/FUZZ -H "Authorization: Bearer TOKEN" -mc 200,201 -ac -c
```

### 带自动校准的子域名发现
```bash
ffuf -w ~/wordlists/subdomains-top5000.txt -u https://FUZZ.target.com -ac -c -v
```

### POST 登录暴力破解
```bash
ffuf -w ~/wordlists/passwords.txt -X POST -d "username=admin&password=FUZZ" -u https://target.com/login -fc 401 -rate 5 -ac
```

### 带认证的 IDOR 测试
```bash
# 使用带认证请求头的 req.txt，在 ID 参数处放置 FUZZ
ffuf --request req.txt -w numbers.txt -ac -mc 200 -fw 100-200
```

## 配置文件
创建 `~/.config/ffuf/ffufrc` 设置默认值:
```
[http]
headers = ["User-Agent: Mozilla/5.0"]
timeout = 10

[general]
colors = true
threads = 40

[matcher]
status = "200-299,301,302,307,401,403,405,500"
```

## 故障排除

### 误报太多
- 使用 `-ac` 进行自动校准
- 检查默认响应并使用 `-fs` 按大小过滤
- 使用 `-fr` 进行正则过滤

### 太慢
- 增加线程: `-t 100`
- 减小字典大小
- 如果不需要响应内容，使用 `-ignore-body`

### 被封锁
- 降低速率: `-rate 2`
- 添加延迟: `-p 0.5-1.5`
- 减少线程: `-t 10`
- 随机化 User-Agent
- 使用代理轮换

### 遗漏结果
- 检查是否过滤过于激进
- 使用 `-mc all` 查看所有响应
- 暂时禁用自动校准
- 使用详细模式 `-v` 查看发生了什么

## 资源
- 官方 GitHub: https://github.com/ffuf/ffuf
- Wiki: https://github.com/ffuf/ffuf/wiki
- Codingo 指南: https://codingo.io/tools/ffuf/bounty/2020/09/17/everything-you-need-to-know-about-ffuf.html
- 练习实验室: http://ffuf.me
- SecLists 字典: https://github.com/danielmiessler/SecLists

## 快速参考卡

| 任务 | 命令模板 |
|------|----------|
| 目录发现 | `ffuf -w wordlist.txt -u https://target.com/FUZZ -ac` |
| 子域名发现 | `ffuf -w subdomains.txt -u https://FUZZ.target.com -ac` |
| 参数模糊测试 | `ffuf -w params.txt -u https://target.com/page?FUZZ=value -ac` |
| POST 数据模糊测试 | `ffuf -w wordlist.txt -X POST -d "param=FUZZ" -u https://target.com/endpoint` |
| 带扩展名 | 添加 `-e .php,.html,.txt` |
| 过滤状态码 | 添加 `-fc 404,403` |
| 过滤大小 | 添加 `-fs 1234` |
| 速率限制 | 添加 `-rate 2` |
| 保存输出 | 添加 `-o results.json` |
| 详细输出 | 添加 `-c -v` |
| 递归 | 添加 `-recursion -recursion-depth 2` |
| 通过代理 | 添加 `-x http://127.0.0.1:8080` |

## 附加资源

本技能在 `resources/` 目录中包含补充材料:

### 资源文件
- **WORDLISTS.md**: SecLists 字典综合指南，不同场景的推荐列表、文件扩展名和快速参考模式
- **REQUEST_TEMPLATES.md**: 常见认证场景的预构建 req.txt 模板（JWT、OAuth、会话 Cookie、API 密钥等）及使用示例

### 辅助脚本
- **ffuf_helper.py**: Python 辅助脚本，用于:
  - 分析 ffuf JSON 结果中的异常和有趣发现
  - 从命令行参数创建 req.txt 模板文件
  - 生成基于数字的字典用于 IDOR 测试

**辅助脚本用法:**
```bash
# 分析结果以发现有趣的异常
python3 ffuf_helper.py analyze results.json

# 创建认证请求模板
python3 ffuf_helper.py create-req -o req.txt -m POST -u "https://api.target.com/users" \
    -H "Authorization: Bearer TOKEN" -d '{"action":"FUZZ"}'

# 生成 IDOR 测试字典
python3 ffuf_helper.py wordlist -o ids.txt -t numbers -s 1 -e 10000
```

**何时使用资源:**
- 用户需要字典推荐 → 参考 WORDLISTS.md
- 用户需要认证请求帮助 → 参考 REQUEST_TEMPLATES.md
- 用户想分析结果 → 使用 ffuf_helper.py analyze
- 用户需要生成 req.txt → 使用 ffuf_helper.py create-req
- 用户需要 IDOR 数字范围 → 使用 ffuf_helper.py wordlist

## Claude 注意事项
帮助用户使用 ffuf 时:
1. **每个命令始终包含 `-ac`** - 这对高效渗透测试和结果分析是强制性的
2. 当用户提到认证模糊测试或提供认证令牌/Cookie 时:
   - 建议创建包含完整 HTTP 请求的 `req.txt` 文件
   - 展示如何在要模糊测试的位置插入 FUZZ
   - 使用 `ffuf --request req.txt -w wordlist.txt -ac`
3. 始终建议从 `-ac` 开始进行自动校准
4. 根据任务推荐 SecLists 中的合适字典
5. 提醒用户对生产目标使用速率限制（`-rate`）
6. 鼓励将输出保存到文件以备文档记录: `-o results.json`
7. 根据初步侦察建议过滤策略
8. 始终使用 FUZZ 关键字（区分大小写）
9. 考虑隐蔽性: 对敏感目标降低线程数、使用速率限制和延迟
10. 对于渗透测试报告，使用 `-of html` 或 `-of csv` 生成客户友好的格式
11. **为用户分析 ffuf 结果时:**
    - 假设他们使用了 `-ac`（如果没有，结果会太嘈杂）
    - 关注异常: 不同的状态码、响应大小、时间
    - 寻找有趣的端点: admin、api、backup、config、.git 等
    - 标记潜在漏洞: 错误消息、堆栈跟踪、版本信息
    - 建议对有趣发现进行后续模糊测试

## 局限性
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
