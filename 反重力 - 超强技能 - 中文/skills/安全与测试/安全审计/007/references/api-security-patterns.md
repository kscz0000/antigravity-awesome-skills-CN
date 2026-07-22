# API 安全模式与反模式

> 保护 REST API、Webhook 和服务间通信的参考指南。
> 在 `007 audit`、`007 threat-model` 和 API 代码审查期间使用。

---

## 1. 认证模式

### API 密钥

```yaml
# 好：API 密钥在请求头中
Authorization: ApiKey sk-live-abc123def456

# 坏：API 密钥在 URL 中（会记录在服务器日志、浏览器历史、Referer 头中）
GET /api/data?api_key=sk-live-abc123def456

# 最佳实践：
api_keys:
  - 为密钥添加前缀以识别：sk-live-、sk-test-、pk-
  - 存储哈希值（SHA-256），而非明文
  - 定期轮换（最长 90 天）
  - 限定特定权限/资源范围
  - 按密钥速率限制
  - 泄露时立即撤销
  - 每个环境使用不同密钥（开发/预发布/生产）
```

### OAuth 2.0

```yaml
# 按客户端类型推荐的流程
oauth2_flows:
  server_to_server: client_credentials
  web_app_with_backend: authorization_code + PKCE
  single_page_app: authorization_code + PKCE（无客户端密钥）
  mobile_app: authorization_code + PKCE
  NEVER_USE: implicit_grant  # 已弃用，Token 暴露在 URL 中

# Token 最佳实践
tokens:
  access_token_lifetime: 15_minutes  # 短期
  refresh_token_lifetime: 7_days     # 使用时轮换
  refresh_token_rotation: true       # 每次使用新的刷新 Token
  store_tokens: httponly_secure_cookie  # 非 localStorage
  revocation: 实现撤销端点
```

### JWT 最佳实践

```python
# 好：正确的 JWT 配置
jwt_config = {
    "algorithm": "RS256",           # 非对称，而非使用弱密钥的 HS256
    "expiration": 900,              # 最长 15 分钟
    "issuer": "auth.example.com",   # 始终验证
    "audience": "api.example.com",  # 始终验证
    "required_claims": ["sub", "exp", "iat", "iss", "aud"],
}

# 需要检测的反模式
jwt_antipatterns = [
    "algorithm: none",       # 无签名验证
    "algorithm: HS256",      # 使用弱/共享密钥
    "exp: far_future",       # Token 永不过期
    "no audience check",     # Token 在服务间重用
    "secret in code",        # 硬编码签名密钥
    "JWT in URL parameter",  # 被记录、缓存、通过 Referer 泄露
]

# 关键：始终验证
def validate_jwt(token: str) -> dict:
    return jwt.decode(
        token,
        key=PUBLIC_KEY,          # 不是弱共享密钥
        algorithms=["RS256"],    # 显式指定，而非从 Token 头获取
        audience="api.example.com",
        issuer="auth.example.com",
        options={"require": ["exp", "iat", "sub"]},
    )
```

---

## 2. 速率限制策略

### Token Bucket（令牌桶）

```python
# 最适合：允许突发同时维持平均速率
class TokenBucket:
    """
    capacity=100, refill_rate=10/秒
    允许 100 个请求的突发，然后维持 10/秒。
    """
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()

    def allow_request(self) -> bool:
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

### Sliding Window（滑动窗口）

```python
# 最适合：平滑速率限制，无突发允许
# 在时间窗口中跟踪请求，计算最近 N 秒的请求数
# Redis 实现：ZADD + ZRANGEBYSCORE + ZCARD
```

### 按用户速率限制

```yaml
rate_limits:
  unauthenticated:
    requests_per_minute: 20
    requests_per_hour: 100

  authenticated_free:
    requests_per_minute: 60
    requests_per_hour: 1000

  authenticated_paid:
    requests_per_minute: 300
    requests_per_hour: 10000

  # 始终包含响应头
  headers:
    X-RateLimit-Limit: "60"
    X-RateLimit-Remaining: "45"
    X-RateLimit-Reset: "1620000060"  # Unix 时间戳
    Retry-After: "30"               # 429 响应时
```

---

## 3. 输入验证

### Schema 验证

```python
from pydantic import BaseModel, Field, validator

class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    age: int = Field(ge=13, le=150)
    role: str = Field(default="user")  # 忽略用户尝试设置的 "admin"

    @validator("role")
    def restrict_role(cls, v):
        if v not in ("user", "viewer"):  # 只允许安全角色
            return "user"
        return v

    class Config:
        extra = "forbid"  # 拒绝未知字段（防止批量赋值）
```

### 类型检查和大小限制

```yaml
validation_rules:
  string_fields:
    max_length: 10_000         # 无无限字符串
    strip_whitespace: true
    reject_null_bytes: true     # \x00 可能导致问题

  numeric_fields:
    define_min_max: true        # 始终设置边界
    reject_nan_infinity: true   # 可能破坏数学运算

  array_fields:
    max_items: 100              # 无无限数组
    validate_each_item: true

  file_uploads:
    max_size: 10MB
    allowed_types: ["image/jpeg", "image/png", "application/pdf"]
    validate_magic_bytes: true  # 不只信任 Content-Type 头
    scan_for_malware: true

  query_parameters:
    max_page_size: 100
    default_page_size: 20
    max_query_length: 500
```

---

## 4. Webhook 安全

### HMAC 签名验证

```python
import hmac
import hashlib
import time

def verify_webhook(payload: bytes, headers: dict, secret: str) -> bool:
    """完整 Webhook 验证：签名 + 时间戳。"""

    signature = headers.get("X-Webhook-Signature")
    timestamp = headers.get("X-Webhook-Timestamp")

    if not signature or not timestamp:
        return False

    # 1. 防止重放攻击（5 分钟窗口）
    if abs(time.time() - int(timestamp)) > 300:
        return False

    # 2. 计算预期签名
    signed_payload = f"{timestamp}.{payload.decode()}"
    expected = hmac.new(
        secret.encode(), signed_payload.encode(), hashlib.sha256
    ).hexdigest()

    # 3. 常量时间比较（防止时序攻击）
    return hmac.compare_digest(f"sha256={expected}", signature)
```

### Webhook 最佳实践

```yaml
webhook_security:
  sending:
    - 用 HMAC-SHA256 签名每个 Payload
    - 在签名中包含时间戳
    - 发送唯一事件 ID 用于幂等性
    - 仅使用 HTTPS
    - 实现带指数退避的重试
    - 定期轮换签名密钥

  receiving:
    - 在任何处理前验证签名
    - 拒绝超过 5 分钟的请求（重放保护）
    - 实现幂等性（存储已处理事件 ID）
    - 快速返回 200，异步处理
    - 不盲目信任 Payload 数据（验证 Schema）
    - 对传入 Webhook 速率限制
    - 记录所有 Webhook 事件用于审计
```

---

## 5. CORS 配置

```python
# 危险：允许一切
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Credentials: true  # 与 * 源一起无效

# 安全：显式允许列表
CORS_CONFIG = {
    "allowed_origins": [
        "https://app.example.com",
        "https://admin.example.com",
    ],
    "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
    "allowed_headers": ["Authorization", "Content-Type"],
    "allow_credentials": True,
    "max_age": 3600,  # 预检缓存（1 小时）
    "expose_headers": ["X-RateLimit-Remaining"],
}

# 需要检测的反模式
cors_antipatterns = [
    "Access-Control-Allow-Origin: *",                  # 过于宽松
    "reflect Origin header as Allow-Origin",           # 带凭证时等同于 *
    "Access-Control-Allow-Origin: null",               # 可遭攻击者利用
    "Allow-Origin without credentials but with auth",  # 不一致
]
```

---

## 6. 安全头检查清单

```yaml
# 所有 API 响应所需的安全头
security_headers:
  # 防止 MIME 嗅探
  X-Content-Type-Options: "nosniff"

  # 防止点击劫持（HTML 响应）
  X-Frame-Options: "DENY"

  # XSS 保护（旧浏览器）
  X-XSS-Protection: "0"  # 禁用，改用 CSP

  # HTTPS 强制
  Strict-Transport-Security: "max-age=31536000; includeSubDomains; preload"

  # 内容安全策略（HTML 响应）
  Content-Security-Policy: "default-src 'self'; script-src 'self'; style-src 'self'"

  # Referer 策略
  Referrer-Policy: "strict-origin-when-cross-origin"

  # 权限策略
  Permissions-Policy: "camera=(), microphone=(), geolocation=()"

  # 移除服务器信息头
  Server: REMOVE_THIS_HEADER
  X-Powered-By: REMOVE_THIS_HEADER

  # 敏感数据的缓存控制
  Cache-Control: "no-store, no-cache, must-revalidate, private"
  Pragma: "no-cache"
```

---

## 7. 常见 API 漏洞

### BOLA / IDOR（对象级授权失效）

```python
# 有漏洞：无所有权检查
@app.get("/api/users/{user_id}/orders")
def get_orders(user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()
    # 任何认证用户都能访问其他用户的订单

# 安全：强制所有权
@app.get("/api/users/{user_id}/orders")
def get_orders(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403, "Forbidden")
    return db.query(Order).filter(Order.user_id == user_id).all()
```

### 批量赋值

```python
# 有漏洞：接受请求中的所有字段
@app.put("/api/users/{user_id}")
def update_user(user_id: int, data: dict):
    db.query(User).filter(User.id == user_id).update(data)
    # 攻击者发送 {"role": "admin", "is_verified": true}

# 安全：显式可更新字段允许列表
class UserUpdateRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    # role 和 is_verified 未包含

@app.put("/api/users/{user_id}")
def update_user(user_id: int, data: UserUpdateRequest):
    db.query(User).filter(User.id == user_id).update(
        data.dict(exclude_unset=True)
    )
```

### 过度数据暴露

```python
# 有漏洞：返回整个数据库模型
@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    return db.query(User).get(user_id).__dict__
    # 返回：id、name、email、password_hash、ssn、internal_notes...

# 安全：显式响应 Schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    # 只有公开字段

@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return db.query(User).get(user_id)
```

---

## 8. 幂等性模式

```python
# 防止同一请求的重复处理
# 适用于：支付、Webhook、任何非幂等操作

class IdempotencyMiddleware:
    """
    客户端发送：Idempotency-Key: unique-uuid-here
    服务端存储结果，重试时返回缓存响应。
    """
    def __init__(self, cache):
        self.cache = cache  # Redis 或类似

    async def process(self, idempotency_key: str, handler):
        # 1. 检查是否已处理
        cached = await self.cache.get(f"idempotency:{idempotency_key}")
        if cached:
            return cached  # 返回与首次相同的响应

        # 2. 加锁防止并发重复处理
        lock = await self.cache.lock(f"lock:{idempotency_key}", timeout=30)
        if not lock:
            raise HTTPException(409, "Request already in progress")

        try:
            # 3. 处理请求
            result = await handler()

            # 4. 缓存结果（24 小时 TTL）
            await self.cache.set(
                f"idempotency:{idempotency_key}",
                result,
                ttl=86400,
            )
            return result
        finally:
            await lock.release()
```

### 何时需要幂等性密钥

```yaml
require_idempotency_key:
  - POST /payments
  - POST /transfers
  - POST /orders
  - POST /webhooks/*  # 使用事件 ID 作为密钥
  - 任何非幂等变更

naturally_idempotent:  # 无需密钥
  - GET（所有）
  - PUT（完整替换）
  - DELETE（按 ID）
```

---

## 快速安全审查检查清单

```
认证：
[ ] 所有端点需要认证（除非显式公开）
[ ] API 密钥在请求头中，而非 URL
[ ] JWT 使用 RS256 且短期过期
[ ] 公共客户端使用 OAuth 2.0 + PKCE
[ ] Token 轮换已实现

授权：
[ ] 每次数据访问检查所有权（BOLA 防护）
[ ] 每个特权操作检查角色
[ ] 批量赋值保护（显式字段允许列表）
[ ] 响应 Schema 过滤敏感字段

输入/输出：
[ ] 所有输入有 Schema 验证
[ ] 所有字段、数组和文件有大小限制
[ ] 参数化查询（无字符串拼接）
[ ] 通用错误消息（无堆栈跟踪）

传输：
[ ] 全站 HTTPS（TLS 1.2+）
[ ] 安全头已设置
[ ] CORS 显式配置
[ ] HSTS 已启用

运维：
[ ] 按用户/IP 速率限制
[ ] 带关联 ID 的请求日志
[ ] Webhook 签名已验证
[ ] 变更操作有幂等性密钥
[ ] 依赖已扫描 CVE
```
