---
name: api-security-best-practices
description: "实现安全的 API 设计模式，包括认证、授权、输入验证、速率限制和常见 API 漏洞防护。触发词：API安全、接口安全、认证授权、输入验证、速率限制、JWT、OAuth、SQL注入防护、XSS防护、API漏洞、OWASP、安全审计、渗透测试"
risk: unknown
source: community
date_added: "2026-02-27"
---

# API 安全最佳实践

## 概述

指导开发者构建安全的 API，实现认证、授权、输入验证、速率限制以及常见漏洞防护。本技能涵盖 REST、GraphQL 和 WebSocket API 的安全模式。

## 何时使用此技能

- 设计新的 API 端点时
- 保护现有 API 时
- 实现认证和授权时
- 防护 API 攻击（注入、DDoS 等）时
- 进行 API 安全审查时
- 准备安全审计时
- 实现速率限制和节流时
- 在 API 中处理敏感数据时

## 工作原理

### 步骤 1：认证与授权

我将帮助你实现安全的认证：
- 选择认证方式（JWT、OAuth 2.0、API 密钥）
- 实现基于令牌的认证
- 设置基于角色的访问控制（RBAC）
- 安全的会话管理
- 实现多因素认证（MFA）

### 步骤 2：输入验证与清理

防护注入攻击：
- 验证所有输入数据
- 清理用户输入
- 使用参数化查询
- 实现请求模式验证
- 防止 SQL 注入、XSS 和命令注入

### 步骤 3：速率限制与节流

防止滥用和 DDoS 攻击：
- 按用户/IP 实现速率限制
- 设置 API 节流
- 配置请求配额
- 优雅处理速率限制错误
- 监控可疑活动

### 步骤 4：数据保护

保护敏感数据：
- 传输中加密（HTTPS/TLS）
- 静态敏感数据加密
- 实现正确的错误处理（无数据泄露）
- 清理错误消息
- 使用安全头

### 步骤 5：API 安全测试

验证安全实现：
- 测试认证和授权
- 执行渗透测试
- 检查常见漏洞（OWASP API Top 10）
- 验证输入处理
- 测试速率限制


## 示例

### 示例 1：实现 JWT 认证

```markdown
## 安全 JWT 认证实现

### 认证流程

1. 用户使用凭据登录
2. 服务器验证凭据
3. 服务器生成 JWT 令牌
4. 客户端安全存储令牌
5. 客户端在每次请求中发送令牌
6. 服务器验证令牌

### 实现

#### 1. 生成安全的 JWT 令牌

\`\`\`javascript
// auth.js
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// 登录端点
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // 验证输入
    if (!email || !password) {
      return res.status(400).json({ 
        error: 'Email and password are required' 
      });
    }
    
    // 查找用户
    const user = await db.user.findUnique({ 
      where: { email } 
    });
    
    if (!user) {
      // 不要透露用户是否存在
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }
    
    // 验证密码
    const validPassword = await bcrypt.compare(
      password, 
      user.passwordHash
    );
    
    if (!validPassword) {
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }
    
    // 生成 JWT 令牌
    const token = jwt.sign(
      { 
        userId: user.id,
        email: user.email,
        role: user.role
      },
      process.env.JWT_SECRET,
      { 
        expiresIn: '1h',
        issuer: 'your-app',
        audience: 'your-app-users'
      }
    );
    
    // 生成刷新令牌
    const refreshToken = jwt.sign(
      { userId: user.id },
      process.env.JWT_REFRESH_SECRET,
      { expiresIn: '7d' }
    );
    
    // 在数据库中存储刷新令牌
    await db.refreshToken.create({
      data: {
        token: refreshToken,
        userId: user.id,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    });
    
    res.json({
      token,
      refreshToken,
      expiresIn: 3600
    });
    
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ 
      error: 'An error occurred during login' 
    });
  }
});
\`\`\`

#### 2. 验证 JWT 令牌（中间件）

\`\`\`javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
  // 从请求头获取令牌
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
  
  if (!token) {
    return res.status(401).json({ 
      error: 'Access token required' 
    });
  }
  
  // 验证令牌
  jwt.verify(
    token, 
    process.env.JWT_SECRET,
    { 
      issuer: 'your-app',
      audience: 'your-app-users'
    },
    (err, user) => {
      if (err) {
        if (err.name === 'TokenExpiredError') {
          return res.status(401).json({ 
            error: 'Token expired' 
          });
        }
        return res.status(403).json({ 
          error: 'Invalid token' 
        });
      }
      
      // 将用户信息附加到请求对象
      req.user = user;
      next();
    }
  );
}

module.exports = { authenticateToken };
\`\`\`

#### 3. 保护路由

\`\`\`javascript
const { authenticateToken } = require('./middleware/auth');

// 受保护的路由
app.get('/api/user/profile', authenticateToken, async (req, res) => {
  try {
    const user = await db.user.findUnique({
      where: { id: req.user.userId },
      select: {
        id: true,
        email: true,
        name: true,
        // 不返回 passwordHash
      }
    });
    
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});
\`\`\`

#### 4. 实现令牌刷新

\`\`\`javascript
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  if (!refreshToken) {
    return res.status(401).json({ 
      error: 'Refresh token required' 
    });
  }
  
  try {
    // 验证刷新令牌
    const decoded = jwt.verify(
      refreshToken, 
      process.env.JWT_REFRESH_SECRET
    );
    
    // 检查刷新令牌是否存在于数据库中
    const storedToken = await db.refreshToken.findFirst({
      where: {
        token: refreshToken,
        userId: decoded.userId,
        expiresAt: { gt: new Date() }
      }
    });
    
    if (!storedToken) {
      return res.status(403).json({ 
        error: 'Invalid refresh token' 
      });
    }
    
    // 生成新的访问令牌
    const user = await db.user.findUnique({
      where: { id: decoded.userId }
    });
    
    const newToken = jwt.sign(
      { 
        userId: user.id,
        email: user.email,
        role: user.role
      },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );
    
    res.json({
      token: newToken,
      expiresIn: 3600
    });
    
  } catch (error) {
    res.status(403).json({ 
      error: 'Invalid refresh token' 
    });
  }
});
\`\`\`

### 安全最佳实践

- ✅ 使用强 JWT 密钥（至少 256 位）
- ✅ 设置短的过期时间（访问令牌 1 小时）
- ✅ 为长期会话实现刷新令牌
- ✅ 在数据库中存储刷新令牌（可撤销）
- ✅ 仅使用 HTTPS
- ✅ 不要在 JWT 载荷中存储敏感数据
- ✅ 验证令牌颁发者和受众
- ✅ 实现登出时的令牌黑名单
```


### 示例 2：输入验证和 SQL 注入防护

```markdown
## 防止 SQL 注入和输入验证

### 问题所在

**❌ 易受攻击的代码：**
\`\`\`javascript
// 永远不要这样做 - SQL 注入漏洞
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;
  
  // 危险：用户输入直接用于查询
  const query = \`SELECT * FROM users WHERE id = '\${userId}'\`;
  const user = await db.query(query);
  
  res.json(user);
});

// 攻击示例：
// GET /api/users/1' OR '1'='1
// 返回所有用户！
\`\`\`

### 解决方案

#### 1. 使用参数化查询

\`\`\`javascript
// ✅ 安全：参数化查询
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;
  
  // 先验证输入
  if (!userId || !/^\d+$/.test(userId)) {
    return res.status(400).json({ 
      error: 'Invalid user ID' 
    });
  }
  
  // 使用参数化查询
  const user = await db.query(
    'SELECT id, email, name FROM users WHERE id = $1',
    [userId]
  );
  
  if (!user) {
    return res.status(404).json({ 
      error: 'User not found' 
    });
  }
  
  res.json(user);
});
\`\`\`

#### 2. 使用具有正确转义的 ORM

\`\`\`javascript
// ✅ 安全：使用 Prisma ORM
app.get('/api/users/:id', async (req, res) => {
  const userId = parseInt(req.params.id);
  
  if (isNaN(userId)) {
    return res.status(400).json({ 
      error: 'Invalid user ID' 
    });
  }
  
  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: {
      id: true,
      email: true,
      name: true,
      // 不选择敏感字段
    }
  });
  
  if (!user) {
    return res.status(404).json({ 
      error: 'User not found' 
    });
  }
  
  res.json(user);
});
\`\`\`

#### 3. 使用 Zod 实现请求验证

\`\`\`javascript
const { z } = require('zod');

// 定义验证模式
const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[a-z]/, 'Password must contain lowercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name too long'),
  age: z.number()
    .int('Age must be an integer')
    .min(18, 'Must be 18 or older')
    .max(120, 'Invalid age')
    .optional()
});

// 验证中间件
function validateRequest(schema) {
  return (req, res, next) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      res.status(400).json({
        error: 'Validation failed',
        details: error.errors
      });
    }
  };
}

// 使用验证
app.post('/api/users', 
  validateRequest(createUserSchema),
  async (req, res) => {
    // 此时输入已验证
    const { email, password, name, age } = req.body;
    
    // 哈希密码
    const passwordHash = await bcrypt.hash(password, 10);
    
    // 创建用户
    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        name,
        age
      }
    });
    
    // 不返回密码哈希
    const { passwordHash: _, ...userWithoutPassword } = user;
    res.status(201).json(userWithoutPassword);
  }
);
\`\`\`

#### 4. 清理输出以防止 XSS

\`\`\`javascript
const DOMPurify = require('isomorphic-dompurify');

app.post('/api/comments', authenticateToken, async (req, res) => {
  const { content } = req.body;
  
  // 验证
  if (!content || content.length > 1000) {
    return res.status(400).json({ 
      error: 'Invalid comment content' 
    });
  }
  
  // 清理 HTML 以防止 XSS
  const sanitizedContent = DOMPurify.sanitize(content, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  });
  
  const comment = await prisma.comment.create({
    data: {
      content: sanitizedContent,
      userId: req.user.userId
    }
  });
  
  res.status(201).json(comment);
});
\`\`\`

### 验证清单

- [ ] 验证所有用户输入
- [ ] 使用参数化查询或 ORM
- [ ] 验证数据类型（字符串、数字、邮箱等）
- [ ] 验证数据范围（最小/最大长度、值范围）
- [ ] 清理 HTML 内容
- [ ] 转义特殊字符
- [ ] 验证文件上传（类型、大小、内容）
- [ ] 使用白名单，而非黑名单
```


### 示例 3：速率限制和 DDoS 防护

```markdown
## 实现速率限制

### 为什么需要速率限制？

- 防止暴力破解攻击
- 防护 DDoS
- 防止 API 滥用
- 确保公平使用
- 降低服务器成本

### 使用 Express Rate Limit 实现

\`\`\`javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const Redis = require('ioredis');

// 创建 Redis 客户端
const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT
});

// 通用 API 速率限制
const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:api:'
  }),
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 100, // 每个时间窗口 100 次请求
  message: {
    error: 'Too many requests, please try again later',
    retryAfter: 900 // 秒
  },
  standardHeaders: true, // 在响应头中返回速率限制信息
  legacyHeaders: false,
  // 自定义键生成器（按用户 ID 或 IP）
  keyGenerator: (req) => {
    return req.user?.userId || req.ip;
  }
});

// 认证端点的严格速率限制
const authLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:auth:'
  }),
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 5, // 15 分钟内仅允许 5 次登录尝试
  skipSuccessfulRequests: true, // 不计算成功的登录
  message: {
    error: 'Too many login attempts, please try again later',
    retryAfter: 900
  }
});

// 应用速率限制器
app.use('/api/', apiLimiter);
app.use('/api/auth/login', authLimiter);
app.use('/api/auth/register', authLimiter);

// 针对昂贵操作的自定义速率限制器
const expensiveLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 小时
  max: 10, // 每小时 10 次请求
  message: {
    error: 'Rate limit exceeded for this operation'
  }
});

app.post('/api/reports/generate', 
  authenticateToken,
  expensiveLimiter,
  async (req, res) => {
    // 昂贵的操作
  }
);
\`\`\`

### 进阶：按用户速率限制

\`\`\`javascript
// 根据用户等级设置不同的限制
function createTieredRateLimiter() {
  const limits = {
    free: { windowMs: 60 * 60 * 1000, max: 100 },
    pro: { windowMs: 60 * 60 * 1000, max: 1000 },
    enterprise: { windowMs: 60 * 60 * 1000, max: 10000 }
  };
  
  return async (req, res, next) => {
    const user = req.user;
    const tier = user?.tier || 'free';
    const limit = limits[tier];
    
    const key = \`rl:user:\${user.userId}\`;
    const current = await redis.incr(key);
    
    if (current === 1) {
      await redis.expire(key, limit.windowMs / 1000);
    }
    
    if (current > limit.max) {
      return res.status(429).json({
        error: 'Rate limit exceeded',
        limit: limit.max,
        remaining: 0,
        reset: await redis.ttl(key)
      });
    }
    
    // 设置速率限制响应头
    res.set({
      'X-RateLimit-Limit': limit.max,
      'X-RateLimit-Remaining': limit.max - current,
      'X-RateLimit-Reset': await redis.ttl(key)
    });
    
    next();
  };
}

app.use('/api/', authenticateToken, createTieredRateLimiter());
\`\`\`

### 使用 Helmet 进行 DDoS 防护

\`\`\`javascript
const helmet = require('helmet');

app.use(helmet({
  // 内容安全策略
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:']
    }
  },
  // 防止点击劫持
  frameguard: { action: 'deny' },
  // 隐藏 X-Powered-By 响应头
  hidePoweredBy: true,
  // 防止 MIME 类型嗅探
  noSniff: true,
  // 启用 HSTS
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
\`\`\`

### 速率限制响应头

\`\`\`
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1640000000
Retry-After: 900
\`\`\`
```

## 最佳实践

### ✅ 应该这样做

- **始终使用 HTTPS** - 永远不要通过 HTTP 发送敏感数据
- **实现认证** - 为受保护的端点要求认证
- **验证所有输入** - 永远不要信任用户输入
- **使用参数化查询** - 防止 SQL 注入
- **实现速率限制** - 防护暴力破解和 DDoS
- **哈希密码** - 使用 bcrypt，盐轮数 >= 10
- **使用短期令牌** - JWT 访问令牌应快速过期
- **正确实现 CORS** - 仅允许可信来源
- **记录安全事件** - 监控可疑活动
- **保持依赖更新** - 定期更新包
- **使用安全响应头** - 实现 Helmet.js
- **清理错误消息** - 不要泄露敏感信息

### ❌ 不应该这样做

- **不要明文存储密码** - 始终哈希密码
- **不要使用弱密钥** - 使用强随机 JWT 密钥
- **不要信任用户输入** - 始终验证和清理
- **不要暴露堆栈跟踪** - 在生产环境隐藏错误详情
- **不要使用字符串拼接 SQL** - 使用参数化查询
- **不要在 JWT 中存储敏感数据** - JWT 不是加密的
- **不要忽略安全更新** - 定期更新依赖
- **不要使用默认凭据** - 更改所有默认密码
- **不要完全禁用 CORS** - 正确配置它
- **不要记录敏感数据** - 清理日志

## 常见陷阱

### 问题：JWT 密钥暴露在代码中
**症状：** JWT 密钥硬编码或提交到 Git
**解决方案：**
\`\`\`javascript
// ❌ 错误
const JWT_SECRET = 'my-secret-key';

// ✅ 正确
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
  throw new Error('JWT_SECRET environment variable is required');
}

// 生成强密钥
// node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
\`\`\`

### 问题：弱密码要求
**症状：** 用户可以设置像 "password123" 这样的弱密码
**解决方案：**
\`\`\`javascript
const passwordSchema = z.string()
  .min(12, 'Password must be at least 12 characters')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[a-z]/, 'Must contain lowercase letter')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character');

// 或使用密码强度库
const zxcvbn = require('zxcvbn');
const result = zxcvbn(password);
if (result.score < 3) {
  return res.status(400).json({
    error: 'Password too weak',
    suggestions: result.feedback.suggestions
  });
}
\`\`\`

### 问题：缺少授权检查
**症状：** 用户可以访问他们不应该访问的资源
**解决方案：**
\`\`\`javascript
// ❌ 错误：仅检查认证
app.delete('/api/posts/:id', authenticateToken, async (req, res) => {
  await prisma.post.delete({ where: { id: req.params.id } });
  res.json({ success: true });
});

// ✅ 正确：同时检查认证和授权
app.delete('/api/posts/:id', authenticateToken, async (req, res) => {
  const post = await prisma.post.findUnique({
    where: { id: req.params.id }
  });
  
  if (!post) {
    return res.status(404).json({ error: 'Post not found' });
  }
  
  // 检查用户是否拥有该文章或是管理员
  if (post.userId !== req.user.userId && req.user.role !== 'admin') {
    return res.status(403).json({ 
      error: 'Not authorized to delete this post' 
    });
  }
  
  await prisma.post.delete({ where: { id: req.params.id } });
  res.json({ success: true });
});
\`\`\`

### 问题：详细的错误消息
**症状：** 错误消息泄露系统详情
**解决方案：**
\`\`\`javascript
// ❌ 错误：暴露数据库详情
app.post('/api/users', async (req, res) => {
  try {
    const user = await prisma.user.create({ data: req.body });
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
    // 错误："Unique constraint failed on the fields: (`email`)"
  }
});

// ✅ 正确：通用错误消息
app.post('/api/users', async (req, res) => {
  try {
    const user = await prisma.user.create({ data: req.body });
    res.json(user);
  } catch (error) {
    console.error('User creation error:', error); // 记录完整错误
    
    if (error.code === 'P2002') {
      return res.status(400).json({ 
        error: 'Email already exists' 
      });
    }
    
    res.status(500).json({ 
      error: 'An error occurred while creating user' 
    });
  }
});
\`\`\`

## 安全清单

### 认证与授权
- [ ] 实现强认证（JWT、OAuth 2.0）
- [ ] 所有端点使用 HTTPS
- [ ] 使用 bcrypt 哈希密码（盐轮数 >= 10）
- [ ] 实现令牌过期
- [ ] 添加刷新令牌机制
- [ ] 验证每个请求的用户授权
- [ ] 实现基于角色的访问控制（RBAC）

### 输入验证
- [ ] 验证所有用户输入
- [ ] 使用参数化查询或 ORM
- [ ] 清理 HTML 内容
- [ ] 验证文件上传
- [ ] 实现请求模式验证
- [ ] 使用白名单，而非黑名单

### 速率限制与 DDoS 防护
- [ ] 按用户/IP 实现速率限制
- [ ] 为认证端点添加更严格的限制
- [ ] 使用 Redis 进行分布式速率限制
- [ ] 返回正确的速率限制响应头
- [ ] 实现请求节流

### 数据保护
- [ ] 所有流量使用 HTTPS/TLS
- [ ] 静态敏感数据加密
- [ ] 不要在 JWT 中存储敏感数据
- [ ] 清理错误消息
- [ ] 实现正确的 CORS 配置
- [ ] 使用安全响应头（Helmet.js）

### 监控与日志
- [ ] 记录安全事件
- [ ] 监控可疑活动
- [ ] 为失败的认证尝试设置告警
- [ ] 跟踪 API 使用模式
- [ ] 不要记录敏感数据

## OWASP API 安全 Top 10

1. **对象级授权失效** - 始终验证用户可以访问资源
2. **认证失效** - 实现强认证机制
3. **对象属性级授权失效** - 验证用户可以访问哪些属性
4. **资源消耗无限制** - 实现速率限制和配额
5. **功能级授权失效** - 为每个功能验证用户角色
6. **敏感业务流程访问无限制** - 保护关键工作流
7. **服务器端请求伪造（SSRF）** - 验证和清理 URL
8. **安全配置错误** - 使用安全最佳实践和响应头
9. **资产管理不当** - 文档化并保护所有 API 端点
10. **不安全的 API 消费** - 验证来自第三方 API 的数据

## 相关技能

- `@ethical-hacking-methodology` - 安全测试视角
- `@sql-injection-testing` - SQL 注入测试
- `@xss-html-injection` - XSS 漏洞测试
- `@broken-authentication` - 认证漏洞
- `@backend-dev-guidelines` - 后端开发标准
- `@systematic-debugging` - 调试安全问题

## 其他资源

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [Node.js Security Checklist](https://blog.risingstack.com/node-js-security-checklist/)
- [API Security Checklist](https://github.com/shieldfy/API-Security-Checklist)

---

**专业提示：** 安全不是一次性任务——定期审计你的 API，保持依赖更新，并随时了解新漏洞！

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
