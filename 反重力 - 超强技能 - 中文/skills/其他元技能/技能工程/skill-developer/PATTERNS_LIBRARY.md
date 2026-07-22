# 常用模式库

可直接用于技能触发器的正则与 glob 模式。复制后按需自定义即可。

---

## 意图模式（Regex）

### 功能/端点创建
```regex
(add|create|implement|build).*?(feature|endpoint|route|service|controller)
```

### 组件创建
```regex
(create|add|make|build).*?(component|UI|page|modal|dialog|form)
```

### 数据库操作
```regex
(add|create|modify|update).*?(user|table|column|field|schema|migration)
(database|prisma).*?(change|update|query)
```

### 错误处理
```regex
(fix|handle|catch|debug).*?(error|exception|bug)
(add|implement).*?(try|catch|error.*?handling)
```

### 说明请求
```regex
(how does|how do|explain|what is|describe|tell me about).*?
```

### 工作流操作
```regex
(create|add|modify|update).*?(workflow|step|branch|condition)
(debug|troubleshoot|fix).*?workflow
```

### 测试
```regex
(write|create|add).*?(test|spec|unit.*?test)
```

---

## 文件路径模式（Glob）

### 前端
```glob
frontend/src/**/*.tsx        # All React components
frontend/src/**/*.ts         # All TypeScript files
frontend/src/components/**   # Only components directory
```

### 后端服务
```glob
form/src/**/*.ts            # Form service
email/src/**/*.ts           # Email service
users/src/**/*.ts           # Users service
projects/src/**/*.ts        # Projects service
```

### 数据库
```glob
**/schema.prisma            # Prisma schema (anywhere)
**/migrations/**/*.sql      # Migration files
database/src/**/*.ts        # Database scripts
```

### 工作流
```glob
form/src/workflow/**/*.ts              # Workflow engine
form/src/workflow-definitions/**/*.json # Workflow definitions
```

### 测试排除
```glob
**/*.test.ts                # TypeScript tests
**/*.test.tsx               # React component tests
**/*.spec.ts                # Spec files
```

---

## 内容模式（Regex）

### Prisma/数据库
```regex
import.*[Pp]risma                # Prisma imports
PrismaService                    # PrismaService usage
prisma\.                         # prisma.something
\.findMany\(                     # Prisma query methods
\.create\(
\.update\(
\.delete\(
```

### 控制器/路由
```regex
export class.*Controller         # Controller classes
router\.                         # Express router
app\.(get|post|put|delete|patch) # Express app routes
```

### 错误处理
```regex
try\s*\{                        # Try blocks
catch\s*\(                      # Catch blocks
throw new                        # Throw statements
```

### React/组件
```regex
export.*React\.FC               # React functional components
export default function.*       # Default function exports
useState|useEffect              # React hooks
```

---

**使用示例：**

```json
{
  "my-skill": {
    "promptTriggers": {
      "intentPatterns": [
        "(create|add|build).*?(component|UI|page)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "frontend/src/**/*.tsx"
      ],
      "contentPatterns": [
        "export.*React\\.FC",
        "useState|useEffect"
      ]
    }
  }
}
```

---

**相关文件：**
- [SKILL.md](SKILL.md) - 技能主指南
- [TRIGGER_TYPES.md](TRIGGER_TYPES.md) - 触发器详细文档
- [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) - 完整 Schema
