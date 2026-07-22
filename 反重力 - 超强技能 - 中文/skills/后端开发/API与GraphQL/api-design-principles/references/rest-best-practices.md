# REST API 最佳实践

## URL 结构

### 资源命名

```
# 好的做法 - 复数名词
GET /api/users
GET /api/orders
GET /api/products

# 不好的做法 - 动词或混合约定
GET /api/getUser
GET /api/user  （不一致的单数形式）
POST /api/createOrder
```

### 嵌套资源

```
# 浅层嵌套（推荐）
GET /api/users/{id}/orders
GET /api/orders/{id}

# 深层嵌套（避免）
GET /api/users/{id}/orders/{orderId}/items/{itemId}/reviews
# 更好的做法：
GET /api/order-items/{id}/reviews
```

## HTTP 方法和状态码

### GET - 获取资源

```
GET /api/users              → 200 OK（返回列表）
GET /api/users/{id}         → 200 OK 或 404 Not Found
GET /api/users?page=2       → 200 OK（分页结果）
```

### POST - 创建资源

```
POST /api/users
  Body: {"name": "John", "email": "john@example.com"}
  → 201 Created
  Location: /api/users/123
  Body: {"id": "123", "name": "John", ...}

POST /api/users（验证错误）
  → 422 Unprocessable Entity
  Body: {"errors": [...]}
```

### PUT - 替换资源

```
PUT /api/users/{id}
  Body: {完整的用户对象}
  → 200 OK（已更新）
  → 404 Not Found（不存在）

# 必须包含所有字段
```

### PATCH - 部分更新

```
PATCH /api/users/{id}
  Body: {"name": "Jane"}  （仅更改的字段）
  → 200 OK
  → 404 Not Found
```

### DELETE - 删除资源

```
DELETE /api/users/{id}
  → 204 No Content（已删除）
  → 404 Not Found
  → 409 Conflict（因引用关系无法删除）
```

## 过滤、排序和搜索

### 查询参数

```
# 过滤
GET /api/users?status=active
GET /api/users?role=admin&status=active

# 排序
GET /api/users?sort=created_at
GET /api/users?sort=-created_at  （降序）
GET /api/users?sort=name,created_at

# 搜索
GET /api/users?search=john
GET /api/users?q=john

# 字段选择（稀疏字段集）
GET /api/users?fields=id,name,email
```

## 分页模式

### 偏移分页

```python
GET /api/users?page=2&page_size=20

响应：
{
  "items": [...],
  "page": 2,
  "page_size": 20,
  "total": 150,
  "pages": 8
}
```

### 游标分页（适用于大数据集）

```python
GET /api/users?limit=20&cursor=eyJpZCI6MTIzfQ

响应：
{
  "items": [...],
  "next_cursor": "eyJpZCI6MTQzfQ",
  "has_more": true
}
```

### Link 响应头分页（RESTful）

```
GET /api/users?page=2

响应头：
Link: <https://api.example.com/users?page=3>; rel="next",
      <https://api.example.com/users?page=1>; rel="prev",
      <https://api.example.com/users?page=1>; rel="first",
      <https://api.example.com/users?page=8>; rel="last"
```

## 版本控制策略

### URL 版本控制（推荐）

```
/api/v1/users
/api/v2/users

优点：清晰，易于路由
缺点：同一资源有多个 URL
```

### 请求头版本控制

```
GET /api/users
Accept: application/vnd.api+json; version=2

优点：URL 干净
缺点：不够直观，测试较难
```

### 查询参数版本控制

```
GET /api/users?version=2

优点：易于测试
缺点：可选参数可能被遗忘
```

## 速率限制

### 响应头

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1640000000

超出限制时的响应：
429 Too Many Requests
Retry-After: 3600
```

### 实现模式

```python
from fastapi import HTTPException, Request
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.cache = {}

    def check(self, key: str) -> bool:
        now = datetime.now()
        if key not in self.cache:
            self.cache[key] = []

        # 移除旧请求
        self.cache[key] = [
            ts for ts in self.cache[key]
            if now - ts < timedelta(seconds=self.period)
        ]

        if len(self.cache[key]) >= self.calls:
            return False

        self.cache[key].append(now)
        return True

limiter = RateLimiter(calls=100, period=60)

@app.get("/api/users")
async def get_users(request: Request):
    if not limiter.check(request.client.host):
        raise HTTPException(
            status_code=429,
            headers={"Retry-After": "60"}
        )
    return {"users": [...]}
```

## 认证与授权

### Bearer 令牌

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

401 Unauthorized - 缺少/无效令牌
403 Forbidden - 有效令牌，权限不足
```

### API 密钥

```
X-API-Key: your-api-key-here
```

## 错误响应格式

### 统一结构

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求验证失败",
    "details": [
      {
        "field": "email",
        "message": "邮箱格式无效",
        "value": "not-an-email"
      }
    ],
    "timestamp": "2025-10-16T12:00:00Z",
    "path": "/api/users"
  }
}
```

### 状态码指南

- `200 OK`：成功的 GET、PATCH、PUT
- `201 Created`：成功的 POST
- `204 No Content`：成功的 DELETE
- `400 Bad Request`：请求格式错误
- `401 Unauthorized`：需要认证
- `403 Forbidden`：已认证但无权限
- `404 Not Found`：资源不存在
- `409 Conflict`：状态冲突（邮箱重复等）
- `422 Unprocessable Entity`：验证错误
- `429 Too Many Requests`：速率限制
- `500 Internal Server Error`：服务器错误
- `503 Service Unavailable`：临时不可用

## 缓存

### 缓存响应头

```
# 客户端缓存
Cache-Control: public, max-age=3600

# 禁止缓存
Cache-Control: no-cache, no-store, must-revalidate

# 条件请求
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
→ 304 Not Modified
```

## 批量操作

### 批量端点

```python
POST /api/users/batch
{
  "items": [
    {"name": "User1", "email": "user1@example.com"},
    {"name": "User2", "email": "user2@example.com"}
  ]
}

响应：
{
  "results": [
    {"id": "1", "status": "created"},
    {"id": null, "status": "failed", "error": "邮箱已存在"}
  ]
}
```

## 幂等性

### 幂等性密钥

```
POST /api/orders
Idempotency-Key: unique-key-123

如果重复请求：
→ 200 OK（返回缓存的响应）
```

## CORS 配置

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## OpenAPI 文档

```python
from fastapi import FastAPI

app = FastAPI(
    title="我的 API",
    description="用户管理 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get(
    "/api/users/{user_id}",
    summary="根据 ID 获取用户",
    response_description="用户详情",
    tags=["Users"]
)
async def get_user(
    user_id: str = Path(..., description="用户 ID")
):
    """
    根据 ID 获取用户。

    返回完整的用户资料，包括：
    - 基本信息
    - 联系方式
    - 账户状态
    """
    pass
```

## 健康检查与监控端点

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health/detailed")
async def detailed_health():
    return {
        "status": "healthy",
        "checks": {
            "database": await check_database(),
            "redis": await check_redis(),
            "external_api": await check_external_api()
        }
    }
```
