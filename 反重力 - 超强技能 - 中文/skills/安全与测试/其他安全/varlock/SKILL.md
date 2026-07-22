---
name: varlock
description: "Claude Code 会话的默认安全环境变量管理。触发词：环境变量、密钥管理、secrets管理、.env安全、环境变量验证、敏感数据保护、密钥验证"
risk: critical
source: "https://github.com/dmno-dev/varlock"
version: 1.0.0
---

<!-- security-allowlist: curl-pipe-bash -->

# Varlock 安全技能

Claude Code 会话的默认安全环境变量管理。

> **仓库**: https://github.com/dmno-dev/varlock
> **文档**: https://varlock.dev

## 何时使用
- 需要在 Claude Code 会话中处理环境变量或密钥，但不暴露其值。
- 任务涉及验证、加载或审计密钥，同时将其保持在日志、差异和助手上下文之外。
- 希望围绕 Varlock 而非直接检查 `.env` 来构建默认安全的工作流程。

## 核心原则：密钥永不暴露

在与 Claude 合作时，密钥绝不能出现在：
- 终端输出
- Claude 的输入/输出上下文
- 日志文件或跟踪
- Git 提交或差异
- 错误消息

此技能确保所有敏感数据得到妥善保护。

---

## 关键：Claude 的安全规则

### 规则 1：永不回显密钥

```bash
# ❌ 永远不要这样做 - 会将密钥暴露给 Claude 的上下文
echo $CLERK_SECRET_KEY
cat .env | grep SECRET
printenv | grep API

# ✅ 这样做 - 验证但不暴露
varlock load --quiet && echo "✓ 密钥已验证"
```

### 规则 2：永不直接读取 .env

```bash
# ❌ 永远不要这样做 - 会暴露所有密钥
cat .env
less .env
Read tool on .env file

# ✅ 这样做 - 读取 schema（安全）而非值
cat .env.schema
varlock load  # 显示遮蔽的值
```

### 规则 3：使用 Varlock 进行验证

```bash
# ❌ 永远不要这样做 - 会在错误中暴露密钥
test -n "$API_KEY" && echo "Key: $API_KEY"

# ✅ 这样做 - Varlock 验证并遮蔽
varlock load
# 输出显示: API_KEY 🔐sensitive └ ▒▒▒▒▒
```

### 规则 4：永不在命令中包含密钥

```bash
# ❌ 永远不要这样做 - 密钥会出现在命令历史中
curl -H "Authorization: Bearer sk_live_xxx" https://api.example.com

# ✅ 这样做 - 使用环境变量
curl -H "Authorization: Bearer $API_KEY" https://api.example.com
# 或更好: varlock run -- curl ...
```

---

## 快速开始

### 安装

```bash
# 安装 Varlock CLI
curl -sSfL https://varlock.dev/install.sh | sh -s -- --force-no-brew

# 添加到 PATH（添加到 ~/.zshrc 或 ~/.bashrc）
export PATH="$HOME/.varlock/bin:$PATH"

# 验证
varlock --version
```

### 初始化项目

```bash
# 从现有 .env 创建 .env.schema
varlock init

# 或手动创建
touch .env.schema
```

---

## Schema 文件：.env.schema

schema 定义每个变量的类型、验证和敏感度。

### 基本结构

```bash
# 全局默认值
# @defaultSensitive=true @defaultRequired=infer

# 应用程序
# @type=enum(development,staging,production) @sensitive=false
NODE_ENV=development

# @type=port @sensitive=false
PORT=3000

# 数据库 - 敏感
# @type=url @required
DATABASE_URL=

# @type=string @required @sensitive
DATABASE_PASSWORD=

# API 密钥 - 敏感
# @type=string(startsWith=sk_) @required @sensitive
STRIPE_SECRET_KEY=

# @type=string(startsWith=pk_) @sensitive=false
STRIPE_PUBLISHABLE_KEY=
```

### 安全注解

| 注解 | 效果 | 用途 |
|------------|--------|---------|
| `@sensitive` | 在所有输出中遮蔽 | API 密钥、密码、令牌 |
| `@sensitive=false` | 在日志中显示 | 公钥、非密钥配置 |
| `@defaultSensitive=true` | 默认所有变量为敏感 | 高安全项目 |

### 类型注解

| 类型 | 验证 | 示例 |
|------|-----------|---------|
| `string` | 任意字符串 | `@type=string` |
| `string(startsWith=X)` | 前缀验证 | `@type=string(startsWith=sk_)` |
| `string(contains=X)` | 子字符串验证 | `@type=string(contains=+clerk_test)` |
| `url` | 有效 URL | `@type=url` |
| `port` | 1-65535 | `@type=port` |
| `boolean` | true/false | `@type=boolean` |
| `enum(a,b,c)` | 枚举值之一 | `@type=enum(dev,prod)` |

---

## Claude 的安全命令

### 验证环境

```bash
# 检查所有变量（安全 - 遮蔽敏感值）
varlock load

# 静默模式（成功时无输出）
varlock load --quiet

# 检查特定环境
varlock load --env=production
```

### 使用密钥运行命令

```bash
# 将验证过的环境变量注入命令
varlock run -- npm start
varlock run -- node script.js
varlock run -- pytest

# 密钥对命令可用但永不打印
```

### 检查 Schema（安全）

```bash
# Schema 可以安全读取 - 不包含值
cat .env.schema

# 列出预期变量
grep "^[A-Z]" .env.schema
```

---

## 常见模式

### 模式 1：操作前验证

```bash
# 始终先验证环境
varlock load --quiet || {
  echo "❌ 环境验证失败"
  exit 1
}

# 然后继续操作
npm run build
```

### 模式 2：安全的密钥轮换

```bash
# 1. 在外部源（1Password、AWS 等）中更新密钥
# 2. 手动更新 .env 文件（不要使用 Claude 做这件事）
# 3. 验证新值是否生效
varlock load

# 4. 如果使用 GitHub Secrets，同步（值不显示）
./scripts/update-github-secrets.sh
```

### 模式 3：CI/CD 集成

```yaml
# GitHub Actions - 来自 GitHub Secrets 的密钥
- name: 验证环境
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    API_KEY: ${{ secrets.API_KEY }}
  run: varlock load --quiet
```

### 模式 4：Docker 集成

```dockerfile
# 在容器中安装 Varlock
RUN curl -sSfL https://varlock.dev/install.sh | sh -s -- --force-no-brew \
    && ln -s /root/.varlock/bin/varlock /usr/local/bin/varlock

# 容器启动时验证
CMD ["varlock", "run", "--", "npm", "start"]
```

---

## 处理与密钥相关的任务

### 当用户要求"检查 API 密钥是否已设置"

```bash
# ✅ 安全方法
varlock load 2>&1 | grep "API_KEY"
# 显示: ✅ API_KEY 🔐sensitive └ ▒▒▒▒▒

# ❌ 永远不要这样做
echo $API_KEY
```

### 当用户要求"调试身份验证"

```bash
# ✅ 安全方法 - 检查存在性和格式
varlock load  # 验证类型和必需字段

# 检查密钥是否有正确的前缀（不显示值）
varlock load 2>&1 | grep -E "(CLERK|AUTH)"

# ❌ 永远不要这样做
printenv | grep KEY
```

### 当用户要求"更新密钥"

```
Claude 应该回复：
"出于安全原因，我无法直接修改密钥。请：
1. 手动更新 .env 文件中的值
2. 或在密钥管理器（1Password、AWS 等）中更新
3. 然后运行 `varlock load` 验证

如果需要添加新变量，我可以帮您更新 .env.schema。"
```

### 当用户要求"显示 .env 文件"

```
Claude 应该回复：
"我不会直接读取 .env 文件，因为它们包含密钥。请：
- 运行 `varlock load` 查看遮蔽的值
- 运行 `cat .env.schema` 查看 schema（安全）
- 如有需要，我可以帮您修改 .env.schema"
```

---

## 外部密钥源

### 1Password 集成

```bash
# 在 .env.schema 中
# @type=string @sensitive
API_KEY=exec('op read "op://vault/item/field"')
```

### AWS Secrets Manager

```bash
# 在 .env.schema 中
# @type=string @sensitive
DB_PASSWORD=exec('aws secretsmanager get-secret-value --secret-id prod/db')
```

### 环境特定值

```bash
# 在 .env.schema 中
# @type=url
API_URL=env('API_URL_${NODE_ENV}', 'http://localhost:3000')
```

---

## 故障排除

### "varlock: command not found"

```bash
# 检查安装
ls ~/.varlock/bin/varlock

# 添加到 PATH
export PATH="$HOME/.varlock/bin:$PATH"

# 或使用完整路径
~/.varlock/bin/varlock load
```

### "Schema validation failed"

```bash
# 检查哪些变量缺失/无效
varlock load  # 显示详细错误

# 常见修复：
# - 将缺失的必需变量添加到 .env
# - 修复类型不匹配（端口必须是数字）
# - 检查字符串前缀是否匹配 schema
```

### "Sensitive value exposed in logs"

```bash
# 1. 立即轮换暴露的密钥
# 2. 检查 .env.schema 是否有 @sensitive 注解
# 3. 确保使用 varlock 命令，而非 echo/cat

# 添加缺失的敏感度：
# 之前: API_KEY=
# 之后:  # @type=string @sensitive
#        API_KEY=
```

---

## npm 脚本

将这些添加到您的 package.json：

```json
{
  "scripts": {
    "env:validate": "varlock load",
    "env:check": "varlock load --quiet || echo '环境验证失败'",
    "prestart": "varlock load --quiet",
    "start": "varlock run -- node server.js"
  }
}
```

---

## 新项目安全检查清单

- [ ] 安装 Varlock CLI
- [ ] 创建 `.env.schema` 并定义所有变量
- [ ] 用 `@sensitive` 注解标记所有密钥
- [ ] 在 schema 头部添加 `@defaultSensitive=true`
- [ ] 将 `.env` 添加到 `.gitignore`
- [ ] 将 `.env.schema` 提交到版本控制
- [ ] 在 CI/CD 中添加 `npm run env:validate`
- [ ] 记录密钥轮换流程
- [ ] 永远不要在 Claude 会话中使用 `cat .env` 或 `echo $SECRET`

---

## 快速参考卡

| 任务 | 安全命令 |
|------|-------------|
| 验证所有环境变量 | `varlock load` |
| 静默验证 | `varlock load --quiet` |
| 使用环境变量运行 | `varlock run -- <cmd>` |
| 查看 schema | `cat .env.schema` |
| 检查特定变量 | `varlock load \| grep VAR_NAME` |

| 永远不要做 | 原因 |
|----------|-----|
| `cat .env` | 暴露所有密钥 |
| `echo $SECRET` | 暴露给 Claude 上下文 |
| `printenv \| grep` | 暴露匹配的密钥 |
| 用工具读取 .env | 密钥进入 Claude 上下文 |
| 在命令中硬编码 | 进入 shell 历史 |

---

## 与其他技能的集成

### Clerk 技能
- 测试用户密码是 `@sensitive`
- 测试邮箱是 `@sensitive=false`（包含 +clerk_test，非密钥）
- 参见：`~/.claude/skills/clerk/SKILL.md`

### Docker 技能
- 挂载 `.env` 文件，永不将密钥复制到镜像
- 使用 `varlock run` 作为入口点
- 参见：`~/.claude/skills/docker/SKILL.md`

---

*最后更新：2025年12月22日*
*Claude Code 的默认安全管理*

## 局限性
- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
