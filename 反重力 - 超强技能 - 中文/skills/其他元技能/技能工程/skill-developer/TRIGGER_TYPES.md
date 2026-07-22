# 触发器类型 - 完整指南

在 Claude Code 的技能自动激活系统中配置技能触发器的完整参考。

## 目录

- [关键词触发器（显式）](#关键词触发器显式)
- [意图模式触发器（隐式）](#意图模式触发器隐式)
- [文件路径触发器](#文件路径触发器)
- [内容模式触发器](#内容模式触发器)
- [最佳实践总结](#最佳实践总结)

---

## 关键词触发器（显式）

### 工作原理

在用户提示中进行不区分大小写的子串匹配。

### 适用场景

基于主题的激活：用户明确提到相关主题时触发。

### 配置

```json
"promptTriggers": {
  "keywords": ["layout", "grid", "toolbar", "submission"]
}
```

### 示例

- 用户提示： "how does the **layout** system work?"
- 命中关键词： "layout"
- 触发技能： `project-catalog-developer`

### 最佳实践

- 使用具体、无歧义的术语
- 包含常见变体（"layout"、"layout system"、"grid layout"）
- 避免过于泛化的词（"system"、"work"、"create"）
- 用真实提示进行测试

---

## 意图模式触发器（隐式）

### 工作原理

通过正则模式匹配，在用户未显式提到主题时检测其意图。

### 适用场景

基于行为的激活：用户描述想要做什么，而不是具体主题。

### 配置

```json
"promptTriggers": {
  "intentPatterns": [
    "(create|add|implement).*?(feature|endpoint)",
    "(how does|explain).*?(layout|workflow)"
  ]
}
```

### 示例

**数据库操作：**
- 用户提示： "add user tracking feature"
- 命中模式： `(add).*?(feature)`
- 触发技能： `database-verification`、`error-tracking`

**组件创建：**
- 用户提示： "create a dashboard widget"
- 命中模式： `(create).*?(component)`（如果模式包含 component）
- 触发技能： `frontend-dev-guidelines`

### 最佳实践

- 捕获常见动作动词：`(create|add|modify|build|implement)`
- 包含领域名词：`(feature|endpoint|component|workflow)`
- 使用非贪婪匹配：用 `.*?` 而不是 `.*`
- 在正则测试工具中充分测试（https://regex101.com/）
- 不要让模式过于宽泛（会增加误报）
- 不要让模式过于具体（会增加漏报）

### 常见模式示例

```regex
# Database Work
(add|create|implement).*?(user|login|auth|feature)

# Explanations
(how does|explain|what is|describe).*?

# Frontend Work
(create|add|make|build).*?(component|UI|page|modal|dialog)

# Error Handling
(fix|handle|catch|debug).*?(error|exception|bug)

# Workflow Operations
(create|add|modify).*?(workflow|step|branch|condition)
```

---

## 文件路径触发器

### 工作原理

对正在编辑的文件路径进行 glob 模式匹配。

### 适用场景

基于项目中文件位置的区域/领域激活。

### 配置

```json
"fileTriggers": {
  "pathPatterns": [
    "frontend/src/**/*.tsx",
    "form/src/**/*.ts"
  ],
  "pathExclusions": [
    "**/*.test.ts",
    "**/*.spec.ts"
  ]
}
```

### Glob 模式语法

- `**` = 任意数量的目录（包括零个）
- `*` = 目录名称内的任意字符
- 示例：
  - `frontend/src/**/*.tsx` = frontend/src 及其子目录中的所有 .tsx 文件
  - `**/schema.prisma` = 项目中任意位置的 schema.prisma
  - `form/src/**/*.ts` = form/src 子目录中的所有 .ts 文件

### 示例

- 正在编辑的文件： `frontend/src/components/Dashboard.tsx`
- 命中模式： `frontend/src/**/*.tsx`
- 触发技能： `frontend-dev-guidelines`

### 最佳实践

- 使用更具体的模式以避免误报
- 使用排除规则过滤测试文件：`**/*.test.ts`
- 考虑子目录结构
- 用实际文件路径测试模式
- 尽可能使用更窄的模式：`form/src/services/**` 而非 `form/**`

### 常见路径模式

```glob
# Frontend
frontend/src/**/*.tsx        # All React components
frontend/src/**/*.ts         # All TypeScript files
frontend/src/components/**   # Only components directory

# Backend Services
form/src/**/*.ts            # Form service
email/src/**/*.ts           # Email service
users/src/**/*.ts           # Users service

# Database
**/schema.prisma            # Prisma schema (anywhere)
**/migrations/**/*.sql      # Migration files
database/src/**/*.ts        # Database scripts

# Workflows
form/src/workflow/**/*.ts              # Workflow engine
form/src/workflow-definitions/**/*.json # Workflow definitions

# Test Exclusions
**/*.test.ts                # TypeScript tests
**/*.test.tsx               # React component tests
**/*.spec.ts                # Spec files
```

---

## 内容模式触发器

### 工作原理

对文件实际内容（文件内部）进行正则模式匹配。

### 适用场景

基于代码导入或使用的技术（Prisma、控制器、特定库）的激活。

### 配置

```json
"fileTriggers": {
  "contentPatterns": [
    "import.*[Pp]risma",
    "PrismaService",
    "\\.findMany\\(",
    "\\.create\\("
  ]
}
```

### 示例

**Prisma 检测：**
- 文件包含： `import { PrismaService } from '@project/database'`
- 命中模式： `import.*[Pp]risma`
- 触发技能： `database-verification`

**控制器检测：**
- 文件包含： `export class UserController {`
- 命中模式： `export class.*Controller`
- 触发技能： `error-tracking`

### 最佳实践

- 匹配导入语句：`import.*[Pp]risma`（通过 [Pp] 实现不区分大小写）
- 转义正则特殊字符：`\\.findMany\\(` 而非 `.findMany(`
- 模式使用不区分大小写标志
- 用真实文件内容测试
- 模式要足够具体以避免误匹配

### 常见内容模式

```regex
# Prisma/Database
import.*[Pp]risma                # Prisma imports
PrismaService                    # PrismaService usage
prisma\.                         # prisma.something
\.findMany\(                     # Prisma query methods
\.create\(
\.update\(
\.delete\(

# Controllers/Routes
export class.*Controller         # Controller classes
router\.                         # Express router
app\.(get|post|put|delete|patch) # Express app routes

# Error Handling
try\s*\{                        # Try blocks
catch\s*\(                      # Catch blocks
throw new                        # Throw statements

# React/Components
export.*React\.FC               # React functional components
export default function.*       # Default function exports
useState|useEffect              # React hooks
```

---

## 最佳实践总结

### 推荐做法：
✅ 使用具体、无歧义的关键词
✅ 用真实示例测试所有模式
✅ 包含常见变体
✅ 使用非贪婪正则：`.*?`
✅ 在内容模式中转义特殊字符
✅ 添加测试文件排除规则
✅ 使用更窄的文件路径模式

### 避免做法：
❌ 使用过于泛化的关键词（"system"、"work"）
❌ 意图模式过于宽泛（会增加误报）
❌ 模式过于具体（会增加漏报）
❌ 忘记使用正则测试工具（https://regex101.com/）
❌ 使用贪婪正则：`.*` 而非 `.*?`
❌ 文件路径匹配范围过广

### 测试你的触发器

**测试关键词/意图触发器：**
```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**测试文件路径/内容触发器：**
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{
  "session_id": "test",
  "tool_name": "Edit",
  "tool_input": {"file_path": "/path/to/test/file.ts"}
}
EOF
```

---

**相关文件：**
- [SKILL.md](SKILL.md) - 技能主指南
- [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) - 完整 skill-rules.json Schema
- [PATTERNS_LIBRARY.md](PATTERNS_LIBRARY.md) - 可直接使用的模式库
