---
name: api-endpoint-builder
description: "构建生产级 REST API 端点，包含验证、错误处理、认证和文档。遵循安全与可扩展性最佳实践。触发词：创建API端点、构建REST API、API接口、endpoint、路由、REST、CRUD操作"
category: development
risk: safe
source: community
date_added: "2026-03-05"
---

# API 端点构建器

构建完整的、生产级 REST API 端点，包含适当的验证、错误处理、认证和文档。

## 何时使用此技能

- 用户要求"创建 API 端点"或"构建 REST API"
- 构建新的后端功能
- 向现有 API 添加端点
- 用户提到"API"、"端点"、"路由"或"REST"
- 创建 CRUD 操作

## 你将构建什么

对于每个端点，你需要创建：
- 具有正确 HTTP 方法的路由处理器
- 输入验证（请求体、参数、查询）
- 认证/授权检查
- 业务逻辑
- 错误处理
- 响应格式化
- API 文档
- 测试（如果需要）

## 端点结构

### 1. 路由定义

```javascript
// Express example
router.post('/api/users', authenticate, validateUser, createUser);

// Fastify example
fastify.post('/api/users', {
  preHandler: [authenticate],
  schema: userSchema
}, createUser);
```

### 2. 输入验证

始终在处理前验证：

```javascript
const validateUser = (req, res, next) => {
  const { email, name, password } = req.body;
  
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Valid email required' });
  }
  
  if (!name || name.length < 2) {
    return res.status(400).json({ error: 'Name must be at least 2 characters' });
  }
  
  if (!password || password.length < 8) {
    return res.status(400).json({ error: 'Password must be at least 8 characters' });
  }
  
  next();
};
```

### 3. 处理器实现

```javascript
const createUser = async (req, res) => {
  try {
    const { email, name, password } = req.body;
    
    // Check if user exists
    const existing = await db.users.findOne({ email });
    if (existing) {
      return res.status(409).json({ error: 'User already exists' });
    }
    
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Create user
    const user = await db.users.create({
      email,
      name,
      password: hashedPassword,
      createdAt: new Date()
    });
    
    // Don't return password
    const { password: _, ...userWithoutPassword } = user;
    
    res.status(201).json({
      success: true,
      data: userWithoutPassword
    });
    
  } catch (error) {
    console.error('Create user error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};
```

## 最佳实践

### HTTP 状态码
- `200` - 成功（GET、PUT、PATCH）
- `201` - 已创建（POST）
- `204` - 无内容（DELETE）
- `400` - 错误请求（验证失败）
- `401` - 未认证（未登录）
- `403` - 禁止访问（无权限）
- `404` - 未找到
- `409` - 冲突（重复）
- `500` - 服务器内部错误

### 响应格式

一致的结构：

```javascript
// Success
{
  "success": true,
  "data": { ... }
}

// Error
{
  "error": "Error message",
  "details": { ... } // optional
}

// List with pagination
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### 安全检查清单

- [ ] 受保护路由需要认证
- [ ] 授权检查（用户拥有资源）
- [ ] 所有字段进行输入验证
- [ ] SQL 注入防护（使用参数化查询）
- [ ] 公开端点设置速率限制
- [ ] 响应中不包含敏感数据（密码、令牌）
- [ ] 正确配置 CORS
- [ ] 设置请求大小限制

### 错误处理

```javascript
// Centralized error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  
  // Don't leak error details in production
  const message = process.env.NODE_ENV === 'production' 
    ? 'Internal server error' 
    : err.message;
  
  res.status(err.status || 500).json({ error: message });
});
```

## 常见模式

### CRUD 操作

```javascript
// Create
POST /api/resources
Body: { name, description }

// Read (list)
GET /api/resources?page=1&limit=20

// Read (single)
GET /api/resources/:id

// Update
PUT /api/resources/:id
Body: { name, description }

// Delete
DELETE /api/resources/:id
```

### 分页

```javascript
const getResources = async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const skip = (page - 1) * limit;
  
  const [resources, total] = await Promise.all([
    db.resources.find().skip(skip).limit(limit),
    db.resources.countDocuments()
  ]);
  
  res.json({
    success: true,
    data: resources,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  });
};
```

### 过滤与排序

```javascript
const getResources = async (req, res) => {
  const { status, sort = '-createdAt' } = req.query;
  
  const filter = {};
  if (status) filter.status = status;
  
  const resources = await db.resources
    .find(filter)
    .sort(sort)
    .limit(20);
  
  res.json({ success: true, data: resources });
};
```

## 文档模板

```javascript
/**
 * @route POST /api/users
 * @desc Create a new user
 * @access Public
 * 
 * @body {string} email - User email (required)
 * @body {string} name - User name (required)
 * @body {string} password - Password, min 8 chars (required)
 * 
 * @returns {201} User created successfully
 * @returns {400} Validation error
 * @returns {409} User already exists
 * @returns {500} Server error
 * 
 * @example
 * POST /api/users
 * {
 *   "email": "user@example.com",
 *   "name": "John Doe",
 *   "password": "securepass123"
 * }
 */
```

## 测试示例

```javascript
describe('POST /api/users', () => {
  it('should create a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      });
    
    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.email).toBe('test@example.com');
    expect(response.body.data.password).toBeUndefined();
  });
  
  it('should reject invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'invalid',
        name: 'Test User',
        password: 'password123'
      });
    
    expect(response.status).toBe(400);
    expect(response.body.error).toContain('email');
  });
});
```

## 核心原则

- 处理前验证所有输入
- 使用正确的 HTTP 状态码
- 优雅地处理错误
- 永不暴露敏感数据
- 保持响应一致性
- 在需要的地方添加认证
- 为端点编写文档
- 为关键路径编写测试

## 相关技能

- `@security-auditor` - 安全审查
- `@test-driven-development` - 测试驱动开发
- `@database-design` - 数据建模

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
