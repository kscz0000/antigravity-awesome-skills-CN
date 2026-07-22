# 安全模式

## 良好模式（参考）

### 参数化查询（如 instagram/scripts/db.py）
```python
# 好：使用 ? 作为占位符
conn.execute("SELECT * FROM posts WHERE id = ?", [post_id])
conn.execute(
    "INSERT INTO accounts (ig_user_id, username) VALUES (?, ?)",
    [ig_user_id, username]
)
```

### 使用环境变量存储密钥
```python
# 好：密钥放在环境变量中
import os
API_KEY = os.environ.get("API_KEY")
APP_SECRET = os.getenv("APP_SECRET")
```

### Token 刷新与校验
```python
# 好：使用前检查是否过期
if token_expires_at and datetime.now() >= token_expires_at:
    token = refresh_token(refresh_token_value)
```

### 速率限制与阈值
```python
# 好：GovernanceManager 模式
if requests_used >= LIMIT * 0.9:
    warnings.append("Proximo do limite")
if requests_used >= LIMIT:
    raise RateLimitExceeded(...)
```

## 不良模式（Sentinel 会检测）

### 硬编码密钥
```python
# 坏：密钥直接写在代码里
API_KEY = "sk-abc123def456"
PASSWORD = "minha_senha_123"
```

### 通过 f-string 造成 SQL 注入
```python
# 坏：在 SQL 中进行字符串插值
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
cursor.execute("SELECT * FROM users WHERE name = '%s'" % name)
```

### 不安全的 HTTP URL
```python
# 坏：未使用 TLS 的 HTTP
API_URL = "http://api.external.com/data"
```

### 日志中记录 token
```python
# 坏：记录凭证信息
print(f"Token: {access_token}")
logging.info(f"Usando key: {api_key}")
```

### bare except
```python
# 坏：吞掉所有错误
try:
    do_something()
except:
    pass
```

## 已知例外

某些值看起来像密钥但其实是公开的：
- `546c25a59c58ad7` - Imgur 匿名上传 client ID（公开）
- 文档中的测试/示例密钥
