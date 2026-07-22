---
name: security-and-hardening
description: 强化代码以抵御漏洞。当处理用户输入、身份认证、数据存储或外部集成时使用。当构建任何接受不可信数据、管理用户会话或与第三方服务交互的功能时使用。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/security-and-hardening
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# Security and Hardening

## 概述

安全优先的 Web 应用开发实践。将每一个外部输入视为敌意，每一个密钥视为神圣，每一个授权检查视为必须。安全不是一个阶段——它是每一行涉及用户数据、身份认证或外部系统的代码的约束。

## 何时使用

- 构建任何接受用户输入的功能
- 实现身份认证或授权
- 存储或传输敏感数据
- 集成外部 API 或服务
- 添加文件上传、Webhook 或回调
- 处理支付或个人身份信息（PII）数据

## 流程：先做威胁建模

没有威胁模型就加安全控制，那只是猜测。在加固之前，花五分钟像攻击者一样思考：

1. **绘制信任边界。** 不可信数据从哪里进入你的系统？HTTP 请求、表单字段、文件上传、Webhook、第三方 API、消息队列，以及 **LLM 输出**。每个边界都是攻击面。
2. **列出资产。** 什么值得窃取或破坏？凭证、PII、支付数据、管理操作、资金流动。
3. **对每个边界运行 STRIDE** —— 这是一个快速视角，而非繁文缛节：

| 威胁 | 追问 | 典型缓解措施 |
|---|---|---|
| **S**poofing（欺骗） | 有人能冒充用户/服务吗？ | 身份认证、签名验证 |
| **T**ampering（篡改） | 数据在传输或存储中能被篡改吗？ | 完整性校验、参数化查询、HTTPS |
| **R**epudiation（抵赖） | 操作事后能否被否认？ | 安全事件的审计日志 |
| **I**nformation disclosure（信息泄露） | 数据能泄露吗？ | 加密、字段白名单、通用错误信息 |
| **D**enial of service（拒绝服务） | 能被压垮吗？ | 速率限制、输入大小上限、超时 |
| **E**levation of privilege（权限提升） | 用户能获得不该有的权限吗？ | 授权检查、最小权限 |

4. **在用例旁边写滥用用例。** 对每个功能，问"我会如何滥用它？"——然后把它作为你的第一个测试。

如果你无法说清一个功能的信任边界，你就还没准备好保护它。这就是 OWASP **A04：不安全设计**——大多数泄露始于设计，而非代码。

## 三层边界体系

### 始终执行（无例外）

- **在系统边界验证所有外部输入**（API 路由、表单处理器）
- **参数化所有数据库查询**——绝不拼接用户输入到 SQL
- **编码输出**以防止 XSS（使用框架自动转义，不要绕过它）
- **对外部通信使用 HTTPS**
- **使用 bcrypt/scrypt/argon2 哈希密码**（绝不存储明文）
- **设置安全头**（CSP、HSTS、X-Frame-Options、X-Content-Type-Options）
- **使用 httpOnly、secure、sameSite Cookie** 管理会话
- **在每次发布前运行 `npm audit`**（或等效工具）

### 先问再做（需人工批准）

- 添加新的身份认证流程或修改认证逻辑
- 存储新类别的敏感数据（PII、支付信息）
- 添加新的外部服务集成
- 更改 CORS 配置
- 添加文件上传处理器
- 修改速率限制或节流策略
- 授予提升的权限或角色

### 绝不执行

- **绝不将密钥提交到版本控制**（API 密钥、密码、令牌）
- **绝不记录敏感数据**（密码、令牌、完整信用卡号）
- **绝不将客户端验证视为安全边界**
- **绝不为方便而禁用安全头**
- **绝不将 `eval()` 或 `innerHTML` 与用户提供的数据一起使用**
- **绝不将会话存储在客户端可访问的存储中**（如 localStorage 存认证令牌）
- **绝不向用户暴露堆栈跟踪或内部错误详情**

## OWASP Top 10 防护模式

这些是防护模式，不是排名。关于 2021 版排序，参见 `references/security-checklist.md` 中的快速参考表。

### 注入（SQL、NoSQL、OS 命令）

```typescript
// BAD: SQL injection via string concatenation
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// GOOD: Parameterized query
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// GOOD: ORM with parameterized input
const user = await prisma.user.findUnique({ where: { id: userId } });
```

### 身份认证缺陷

```typescript
// Password hashing
import { hash, compare } from 'bcrypt';

const SALT_ROUNDS = 12;
const hashedPassword = await hash(plaintext, SALT_ROUNDS);
const isValid = await compare(plaintext, hashedPassword);

// Session management
app.use(session({
  secret: process.env.SESSION_SECRET,  // From environment, not code
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,     // Not accessible via JavaScript
    secure: true,       // HTTPS only
    sameSite: 'lax',    // CSRF protection
    maxAge: 24 * 60 * 60 * 1000,  // 24 hours
  },
}));
```

### 跨站脚本攻击（XSS）

```typescript
// BAD: Rendering user input as HTML
element.innerHTML = userInput;

// GOOD: Use framework auto-escaping (React does this by default)
return <div>{userInput}</div>;

// If you MUST render HTML, sanitize first
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
```

### 访问控制缺陷

```typescript
// Always check authorization, not just authentication
app.patch('/api/tasks/:id', authenticate, async (req, res) => {
  const task = await taskService.findById(req.params.id);

  // Check that the authenticated user owns this resource
  if (task.ownerId !== req.user.id) {
    return res.status(403).json({
      error: { code: 'FORBIDDEN', message: 'Not authorized to modify this task' }
    });
  }

  // Proceed with update
  const updated = await taskService.update(req.params.id, req.body);
  return res.json(updated);
});
```

### 安全配置错误

```typescript
// Security headers (use helmet for Express)
import helmet from 'helmet';
app.use(helmet());

// Content Security Policy
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],  // Tighten if possible
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'"],
  },
}));

// CORS — restrict to known origins
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
  credentials: true,
}));
```

### 敏感数据泄露

```typescript
// Never return sensitive fields in API responses
function sanitizeUser(user: UserRecord): PublicUser {
  const { passwordHash, resetToken, ...publicFields } = user;
  return publicFields;
}

// Use environment variables for secrets
const API_KEY = process.env.STRIPE_API_KEY;
if (!API_KEY) throw new Error('STRIPE_API_KEY not configured');
```

### 服务端请求伪造（SSRF）

每当服务器获取用户影响的 URL 时——Webhook、"从 URL 导入"、图片代理、链接预览——攻击者都可以将其指向内部服务（云元数据、`localhost`、私有 IP）。

```typescript
// BAD: fetch whatever the user gives you
await fetch(req.body.webhookUrl);

// GOOD: allowlist scheme + host, reject if ANY resolved IP is private, forbid redirects
import { lookup } from 'node:dns/promises';
import ipaddr from 'ipaddr.js';

const ALLOWED_HOSTS = new Set(['hooks.example.com']);

async function assertSafeUrl(raw: string): Promise<URL> {
  const url = new URL(raw);
  if (url.protocol !== 'https:') throw new Error('https only');
  if (!ALLOWED_HOSTS.has(url.hostname)) throw new Error('host not allowed');
  // Resolve ALL records; a single private/reserved address fails the check.
  const addrs = await lookup(url.hostname, { all: true });
  if (addrs.some((a) => ipaddr.parse(a.address).range() !== 'unicast')) {
    throw new Error('private/reserved IP');
  }
  return url;
}

await fetch(await assertSafeUrl(req.body.webhookUrl), { redirect: 'error' });
```

`range() !== 'unicast'` 检查覆盖了环回地址、链路本地地址 `169.254.169.254`（云元数据，SSRF 的头号目标）、私有地址和唯一本地地址范围，适用于 IPv4 和 IPv6。

**注意——这仍存在 TOCTOU 间隙。** `fetch` 在检查后会再次解析 DNS，因此使用短 TTL 记录的攻击者可以在验证和连接之间将地址重新绑定到内部 IP。对于高风险攻击面，应解析一次并连接到固定 IP，或在前面部署过滤代理（`request-filtering-agent` / `ssrf-req-filter`）。

## 输入验证模式

### 边界处的 Schema 验证

```typescript
import { z } from 'zod';

const CreateTaskSchema = z.object({
  title: z.string().min(1).max(200).trim(),
  description: z.string().max(2000).optional(),
  priority: z.enum(['low', 'medium', 'high']).default('medium'),
  dueDate: z.string().datetime().optional(),
});

// Validate at the route handler
app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid input',
        details: result.error.flatten(),
      },
    });
  }
  // result.data is now typed and validated
  const task = await taskService.create(result.data);
  return res.status(201).json(task);
});
```

### 文件上传安全

```typescript
// Restrict file types and sizes
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function validateUpload(file: UploadedFile) {
  if (!ALLOWED_TYPES.includes(file.mimetype)) {
    throw new ValidationError('File type not allowed');
  }
  if (file.size > MAX_SIZE) {
    throw new ValidationError('File too large (max 5MB)');
  }
  // Don't trust the file extension — check magic bytes if critical
}
```

## npm audit 结果分级处理

并非所有审计发现都需要立即处理。使用以下决策树：

```
npm audit reports a vulnerability
├── Severity: critical or high
│   ├── Is the vulnerable code reachable in your app?
│   │   ├── YES --> Fix immediately (update, patch, or replace the dependency)
│   │   └── NO (dev-only dep, unused code path) --> Fix soon, but not a blocker
│   └── Is a fix available?
│       ├── YES --> Update to the patched version
│       └── NO --> Check for workarounds, consider replacing the dependency, or add to allowlist with a review date
├── Severity: moderate
│   ├── Reachable in production? --> Fix in the next release cycle
│   └── Dev-only? --> Fix when convenient, track in backlog
└── Severity: low
    └── Track and fix during regular dependency updates
```

**关键问题：**
- 漏洞函数在你的代码路径中是否实际被调用？
- 该依赖是运行时依赖还是仅开发依赖？
- 考虑你的部署环境，该漏洞是否可利用（例如，仅客户端应用中的服务端漏洞）？

推迟修复时，记录原因并设定复查日期。

### 供应链卫生

`npm audit` 能捕获已知 CVE；但无法捕获恶意或仿冒包。还需注意：

- **提交锁文件**，并在 CI 中使用 `npm ci`（而非 `npm install`）安装——可复现构建，无静默版本漂移。
- **添加新依赖前先审查**——维护状况、下载数量，以及是否真正值得引入。每个依赖都是攻击面（OWASP **A06：脆弱组件**、**LLM03：供应链**）。
- **警惕不熟悉包中的 `postinstall` 脚本**——它们在安装时执行任意代码。
- **注意仿冒包**——`cross-env` vs `crossenv`、`react-dom` vs `reactdom`。

## 速率限制

```typescript
import rateLimit from 'express-rate-limit';

// General API rate limit
app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,                   // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
}));

// Stricter limit for auth endpoints
app.use('/api/auth/', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,  // 10 attempts per 15 minutes
}));
```

## 密钥管理

```
.env files:
  ├── .env.example  → Committed (template with placeholder values)
  ├── .env          → NOT committed (contains real secrets)
  └── .env.local    → NOT committed (local overrides)

.gitignore must include:
  .env
  .env.local
  .env.*.local
  *.pem
  *.key
```

**提交前务必检查：**
```bash
# Check for accidentally staged secrets
git diff --cached | grep -i "password\|secret\|api_key\|token"
```

**如果密钥曾被提交，立即轮换。** 删除该行或重写历史不够——假设它到达远程的那一刻就已泄露。先撤销并重新签发密钥，然后再从历史中清除。

## AI / LLM 功能安全

如果你的应用调用了 LLM——聊天机器人、摘要器、智能体、RAG——它就继承了新的攻击面。将其映射到 [OWASP LLM 应用 Top 10（2025）](https://genai.owasp.org/llm-top-10/)：

- **将所有模型输出视为不可信输入（LLM05：不当输出处理）。** 绝不将 LLM 输出直接传入 `eval`、SQL、Shell、`innerHTML` 或文件路径。像对待原始用户输入一样进行验证和编码。
- **假设提示可被劫持（LLM01：提示注入）。** 上下文窗口中的不可信文本——用户消息、抓取的网页、PDF——都可能携带指令。系统提示不是安全边界；在代码中而非提示中强制执行权限。
- **将密钥和其他用户数据排除在提示之外（LLM02 / LLM07）。** 上下文中的任何内容都可能被回显。不要将 API 密钥、跨租户数据或完整系统提示放在模型可以重复的位置。
- **约束工具和智能体权限（LLM06：过度授权）。** 将工具权限限制到最小，对破坏性或不可逆操作要求确认，验证每个工具参数。
- **限制消耗（LLM10：无限制消耗）。** 设定令牌上限、请求速率和循环/递归深度上限，防止精心构造的输入推高成本或挂起系统。
- **隔离检索数据（LLM08：向量与嵌入弱点）。** 在 RAG 中，将向量存储视为信任边界：按租户分区嵌入，使一个用户无法检索另一个用户的数据，并在索引前验证文档，防止污染内容操纵回答。

```typescript
// BAD: trusting model output as a command or as markup
const sql = await llm.generate(`Write SQL for: ${userQuestion}`);
await db.query(sql);                                   // arbitrary query execution
container.innerHTML = await llm.reply(userMessage);   // stored XSS, via the model

// GOOD: model output is data — parse defensively, then validate, then encode
let intent;
try {
  intent = CommandSchema.parse(JSON.parse(await llm.replyJson(userMessage)));
} catch {
  throw new ValidationError('unexpected model output'); // JSON.parse or schema failed
}
await runAllowlistedAction(intent.action, intent.params);
container.textContent = await llm.reply(userMessage);
```

## 安全审查清单

```markdown
### Authentication
- [ ] Passwords hashed with bcrypt/scrypt/argon2 (salt rounds ≥ 12)
- [ ] Session tokens are httpOnly, secure, sameSite
- [ ] Login has rate limiting
- [ ] Password reset tokens expire

### Authorization
- [ ] Every endpoint checks user permissions
- [ ] Users can only access their own resources
- [ ] Admin actions require admin role verification

### Input
- [ ] All user input validated at the boundary
- [ ] SQL queries are parameterized
- [ ] HTML output is encoded/escaped
- [ ] Server-side URL fetches are allowlisted (no SSRF to internal services)

### Data
- [ ] No secrets in code or version control
- [ ] Sensitive fields excluded from API responses
- [ ] PII encrypted at rest (if applicable)

### Infrastructure
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] CORS restricted to known origins
- [ ] Dependencies audited for vulnerabilities
- [ ] Error messages don't expose internals

### Supply Chain
- [ ] Lockfile committed; CI installs with `npm ci`
- [ ] New dependencies reviewed (maintenance, downloads, postinstall scripts)

### AI / LLM (if used)
- [ ] Model output treated as untrusted (no eval/SQL/innerHTML/shell)
- [ ] Secrets and other users' data kept out of prompts
- [ ] Tool/agent permissions scoped; destructive actions require confirmation
```
## 另见

关于详细的安全检查清单和预提交验证步骤，参见 `references/security-checklist.md`。

## 常见借口

| 借口 | 现实 |
|---|---|
| "这是内部工具，安全不重要" | 内部工具也会被攻破。攻击者瞄准最薄弱的环节。 |
| "安全以后再加" | 安全加固的成本是初始构建的 10 倍。现在就加。 |
| "没人会试图利用这个" | 自动化扫描器会发现它。靠隐蔽不是安全。 |
| "框架已经处理了安全" | 框架提供工具，不提供保证。你仍需正确使用它们。 |
| "这只是原型" | 原型会变成产品。从第一天就养成安全习惯。 |
| "威胁建模在这里太过头了" | 五分钟思考"我会怎么攻击这个？"能预防后续任何控制都无法修补的设计缺陷。 |
| "这只是 LLM 输出，只是文本而已" | 那段"文本"可以是一条 SQL 语句、一个 script 标签或一条 Shell 命令。像对待任何不可信输入一样对待它。 |

## 危险信号

- 用户输入直接传入数据库查询、Shell 命令或 HTML 渲染
- 源代码或提交历史中存在密钥
- API 端点缺少身份认证或授权检查
- 缺少 CORS 配置或使用通配符（`*`）源
- 身份认证端点无速率限制
- 向用户暴露堆栈跟踪或内部错误
- 依赖存在已知严重漏洞
- 服务器获取用户提供的 URL 但未使用白名单（SSRF）
- LLM/模型输出被传入查询、DOM、Shell 或 `eval`
- 密钥、PII 或完整系统提示被放入 LLM 上下文窗口

## 验证

实现安全相关代码后：

- [ ] `npm audit` 无严重或高危漏洞
- [ ] 源代码或 Git 历史中无密钥
- [ ] 所有用户输入在系统边界处已验证
- [ ] 每个受保护端点均检查身份认证和授权
- [ ] 响应中存在安全头（使用浏览器开发者工具检查）
- [ ] 错误响应不暴露内部细节
- [ ] 身份认证端点已启用速率限制
- [ ] 服务端 URL 获取已通过白名单验证（无 SSRF）
- [ ] LLM/模型输出在使用前已验证和编码（如存在 AI 功能）

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更前，验证命令、生成的代码、依赖、凭证和外部服务行为。
- 不要将示例替代针对特定环境的测试、安全审查或用户对破坏性/高成本操作的批准。
