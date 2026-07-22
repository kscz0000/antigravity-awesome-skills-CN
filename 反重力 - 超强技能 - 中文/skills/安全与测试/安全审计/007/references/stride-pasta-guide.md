# STRIDE 与 PASTA 威胁建模指南

> 系统威胁建模的实用指南，适用于 API 和 AI 智能体。
> 在执行 `007 threat-model` 或任何需要结构化威胁识别的安全分析时使用此指南。

---

## 何时使用哪种方法

| 方法 | 最适合 | 工作量 | 输出 |
|------|--------|--------|------|
| **STRIDE** | 组件级分析、快速威胁识别 | 低-中 | 每个组件的威胁列表 |
| **PASTA** | 完整系统风险分析、业务对齐 | 中-高 | 优先级排序的攻击场景 |
| **两者结合** | 关键系统、合规要求 | 高 | 完整威胁全景 |

**经验法则：**
- 快速代码审查或 PR？-> 对变更组件使用 STRIDE
- 新系统设计或架构审查？-> PASTA 完整流程
- 处理敏感数据的生产系统？-> 两者结合（PASTA 定策略，STRIDE 分析每个组件）

---

## STRIDE 演练

STRIDE 将威胁分为六类。对每一类，问："攻击者能对我的系统做这个吗？"

### S - Spoofing（欺骗，身份）

**问题：** 有人能冒充其他用户、服务或组件吗？

**示例：**
```
# 无认证的 API
GET /api/users/123/data  # 任何人都能访问任何用户的数据

# 使用弱密钥的伪造 JWT
jwt.encode({"user_id": "admin", "role": "superuser"}, "password123")

# 无来源验证的 Webhook
POST /webhooks/payment  # 无签名验证，任何人都能发送伪造事件
```

**检测模式：** 缺少认证中间件、硬编码/弱密钥、服务间无双向 TLS。

**缓解措施：** 强认证（OAuth 2.0、mTLS）、HMAC 签名验证、API 密钥轮换。

---

### T - Tampering（篡改，数据完整性）

**问题：** 有人能在传输中、存储中或处理过程中修改数据吗？

**示例：**
```
# SQL 注入修改数据
POST /api/transfer {"amount": "100; UPDATE accounts SET balance=999999 WHERE id=1"}

# HTTP（非 HTTPS）上的中间人攻击
# 攻击者拦截并修改 API 响应

# 未签名的配置文件
config.yaml 加载时无完整性检查 -> 攻击者修改 log_level: DEBUG 以泄露机密
```

**检测模式：** 无输入验证、HTTP 端点、文件缺少完整性检查、无校验和。

**缓解措施：** 输入验证/清理、全站 HTTPS、签名制品、数据库约束。

---

### R - Repudiation（抵赖，可追溯性）

**问题：** 有人能执行操作后否认吗？

**示例：**
```
# 金融交易无审计日志
def transfer_money(from_acc, to_acc, amount):
    db.execute("UPDATE accounts ...")  # 无日志记录谁做的、何时、为何

# 日志存储在同一服务器（攻击者可删除）
# 用户在未授权访问后删除自己的审计追踪
```

**检测模式：** 缺少审计日志、日志无时间戳/用户 ID、可变日志存储、无日志转发。

**缓解措施：** 不可变审计日志（仅追加）、集中日志（SIEM）、签名日志条目、一次写入存储。

---

### I - Information Disclosure（信息泄露）

**问题：** 有人能访问不该看到的数据吗？

**示例：**
```python
# 生产 API 响应中的堆栈跟踪
{
  "error": "NullPointerException at com.app.UserService.getUser(UserService.java:42)",
  "database": "postgresql://admin:s3cret@db.internal:5432/users"
}

# 通过 Web 服务器暴露的 .env 文件
GET /.env  # 返回 API_KEY=sk-live-xxxxx, DB_PASSWORD=...

# 详细错误消息
"User admin@company.com not found" vs "Invalid credentials"（泄露有效邮箱）
```

**检测模式：** 生产环境详细错误、暴露的配置文件、端点缺少访问控制、启用调试模式。

**缓解措施：** 通用错误消息、机密存入 Vault（非环境文件）、所有端点访问控制、生产环境禁用调试。

---

### D - Denial of Service（拒绝服务）

**问题：** 有人能让系统不可用吗？

**示例：**
```python
# 无分页的无界查询
GET /api/users  # 返回 1000 万条记录，服务器崩溃

# ReDoS - 正则表达式拒绝服务
import re
re.match(r"(a+)+$", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!")  # 指数级回溯

# 昂贵操作无速率限制
POST /api/reports/generate  # 每个请求耗时 30 秒和 2GB 内存
```

**检测模式：** 缺少速率限制、无界查询、正则无超时、容器无资源限制。

**缓解措施：** 速率限制、分页、查询限制、熔断器、资源配额、CDN/WAF。

---

### E - Elevation of Privilege（权限提升）

**问题：** 有人能获得不该有的权限吗？

**示例：**
```python
# IDOR - 不安全的直接对象引用
GET /api/users/123/admin-panel  # 只检查用户是否登录，不检查是否是管理员

# 通过批量赋值的角色操控
POST /api/register {"name": "John", "email": "john@test.com", "role": "admin"}

# 路径遍历
GET /api/files?path=../../etc/passwd
```

**检测模式：** 缺少授权检查（不只是认证）、批量赋值漏洞、路径遍历、不安全的反序列化。

**缓解措施：** 基于角色的访问控制（RBAC）、可赋值字段的允许列表、输入路径验证、最小权限原则。

---

## PASTA 7 阶段演练

**P**rocess for **A**ttack **S**imulation and **T**hreat **A**nalysis（攻击模拟和威胁分析流程）

### 阶段 1：定义目标

**做什么：** 将安全分析与业务目标对齐。

```
业务目标："安全处理支付"
安全目标："防止未授权交易和数据泄露"
合规：PCI-DSS、LGPD
风险承受：低（金融数据）
```

### 阶段 2：定义技术范围

**做什么：** 映射范围内的所有技术组件。

```
组件：
- 前端：React SPA（app.example.com）
- API 网关：Kong（api.example.com）
- 后端：FastAPI（内部）
- 数据库：PostgreSQL（内部）
- 队列：RabbitMQ（内部）
- 外部：Stripe API、SendGrid
- 基础设施：AWS ECS、RDS、S3
```

### 阶段 3：应用分解

**做什么：** 创建数据流图（DFD），识别信任边界。

```
信任边界：
  [互联网] --HTTPS--> [WAF/CDN] --HTTPS--> [API 网关]
  [API 网关] --mTLS--> [后端服务]
  [后端] --TLS--> [数据库]
  [后端] --HTTPS--> [Stripe API]

数据流：
  用户凭证 -> API 网关 -> 认证服务 -> 数据库
  支付数据 -> API 网关 -> 支付服务 -> Stripe
  Webhook 事件 -> Stripe -> API 网关 -> 支付服务
```

### 阶段 4：威胁分析

**做什么：** 对阶段 3 的每个组件使用 STRIDE。

对跨越信任边界的每个数据流应用 STRIDE。

### 阶段 5：漏洞分析

**做什么：** 将已知漏洞映射到识别的威胁。

```
工具：OWASP ZAP、Semgrep、依赖审计（npm audit、pip-audit）
CVE 数据库：NVD、GitHub Advisory
现有发现：渗透测试报告、漏洞赏金报告
```

### 阶段 6：攻击建模

**做什么：** 为高优先级威胁构建攻击树。

（见下方攻击树部分）

### 阶段 7：风险与影响分析

**做什么：** 按业务影响和可能性对威胁优先级排序。

使用下方的威胁文档模板对每个威胁评分。

---

## 构建攻击树

攻击树将目标分解为带 AND/OR 关系的子目标。

```
目标：窃取用户支付数据
├── OR：直接攻陷数据库
│   ├── AND：找到 SQL 注入点
│   │   ├── 识别无清理的输入字段
│   │   └── 构造注入 Payload
│   └── AND：获取数据库凭证
│       ├── 找到暴露的 .env 文件
│       └── OR：通过 SSRF 访问
├── OR：传输中拦截数据
│   ├── 将 HTTPS 降级为 HTTP
│   └── 攻陷 TLS 证书
├── OR：利用 API 漏洞
│   ├── AND：支付端点的 BOLA
│   │   ├── 枚举用户 ID
│   │   └── 无授权访问 /users/{id}/payments
│   └── 用户对象的批量赋值
└── OR：社会工程
    ├── 钓鱼获取管理员凭证
    └── 攻陷开发者笔记本
```

**每个叶节点 = 可操作的待缓解威胁。**

---

## 威胁文档模板

对每个识别的威胁使用此模板：

```markdown
### THREAT-{ID}：{简短标题}

**类别：** STRIDE 类别（S/T/R/I/D/E）
**组件：** 受影响的系统组件
**攻击向量：** 攻击者如何利用此漏洞
**前提条件：** 攻击者需要什么（访问级别、知识、工具）

**影响：**
- 机密性：高/中/低
- 完整性：高/中/低
- 可用性：高/中/低
- 业务影响：业务后果描述

**概率：** 高/中/低
**严重性：** 严重/高/中/低（影响 × 概率）

**证据/检测：**
- 如何检测是否正在遭攻击者利用
- 日志模式、监控告警

**缓解措施：**
- [ ] 短期修复（热修复）
- [ ] 长期修复（架构级）
- [ ] 待添加的监控/告警

**状态：** 待处理 | 已缓解 | 已接受 | 已转移
**负责人：** 负责的团队/人员
**截止日期：** YYYY-MM-DD
```

---

## 示例：Webhook 端点威胁建模

**上下文：** `POST /webhooks/stripe` 接收来自 Stripe 的支付事件。

### STRIDE 分析

| 类别 | 威胁 | 严重性 | 缓解措施 |
|------|------|--------|----------|
| **欺骗** | 攻击者发送伪造的 Stripe 事件 | 严重 | 用 HMAC 验证 `Stripe-Signature` 头 |
| **篡改** | 事件 Payload 在传输中被修改 | 高 | HTTPS + 签名验证 |
| **抵赖** | 无法证明事件被接收/处理 | 中 | 用幂等性密钥记录所有 Webhook 事件 |
| **信息泄露** | 错误响应泄露内部状态 | 中 | 返回通用 200/400，内部记录详情 |
| **拒绝服务** | 用伪造事件淹没端点 | 高 | 按 IP 速率限制，处理前验证签名 |
| **权限提升** | Webhook 触发管理员级操作 | 高 | Webhook 处理器以最小权限运行，验证事件类型 |

### 关键实现

```python
import hmac
import hashlib

def verify_stripe_webhook(payload: bytes, signature: str, secret: str) -> bool:
    """始终在处理任何 Webhook 逻辑前验证。"""
    timestamp, sig = parse_stripe_signature(signature)

    # 防止重放攻击（拒绝超过 5 分钟的事件）
    if abs(time.time() - int(timestamp)) > 300:
        return False

    expected = hmac.new(
        secret.encode(), f"{timestamp}.{payload.decode()}".encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, sig)
```

---

## 示例：带工具访问的 AI 智能体威胁建模

**上下文：** AI 智能体可访问文件系统、API 调用和数据库查询。

### STRIDE 分析

| 类别 | 威胁 | 严重性 | 缓解措施 |
|------|------|--------|----------|
| **欺骗** | 提示注入使智能体冒充管理员 | 严重 | 输入清理、系统提示加固 |
| **篡改** | 智能体修改超出预期范围的文件/数据库 | 严重 | 默认只读，可写路径允许列表 |
| **抵赖** | 无法追踪哪个智能体操作造成了损害 | 高 | 记录每个工具调用的完整上下文 |
| **信息泄露** | 智能体从上下文/环境向输出泄露机密 | 严重 | 注入上下文前移除机密、输出过滤 |
| **拒绝服务** | 智能体进入无限循环，消耗 API 额度 | 高 | 迭代限制、Token 预算、每次操作超时 |
| **权限提升** | 智能体通过工具链逃逸沙箱 | 严重 | 最小权限工具访问、无 Shell 访问、沙箱执行 |

### AI 智能体的关键控制

```yaml
agent_security:
  tool_access:
    file_system: READ_ONLY  # 默认
    writable_paths: ["/tmp/agent-workspace/"]  # 显式允许列表
    blocked_paths: ["~/.ssh", "~/.aws", ".env"]
    max_file_size: 1MB

  execution_limits:
    max_iterations: 25
    max_tokens_per_request: 4000
    max_total_tokens: 100000
    timeout_seconds: 120
    max_tool_calls: 50

  monitoring:
    log_all_tool_calls: true
    alert_on_file_write: true
    alert_on_external_api: true
    alert_on_secret_pattern: true  # API 密钥、密码的正则匹配

  isolation:
    network: RESTRICTED  # 仅允许列表域名
    allowed_domains: ["api.openai.com", "api.anthropic.com"]
    no_shell_access: true
    no_code_execution: true  # 除非显式沙箱化
```

---

## 快速参考：严重性矩阵

| | 低影响 | 中影响 | 高影响 |
|---|---|---|---|
| **高概率** | 中 | 高 | 严重 |
| **中概率** | 低 | 中 | 高 |
| **低概率** | 低 | 低 | 中 |
