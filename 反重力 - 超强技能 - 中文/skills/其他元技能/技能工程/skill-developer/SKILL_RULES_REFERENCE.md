# skill-rules.json - 完整参考

`.claude/skills/skill-rules.json` 的完整 Schema 与配置参考。

## 目录

- [文件位置](#文件位置)
- [完整 TypeScript Schema](#完整-typescript-schema)
- [字段指南](#字段指南)
- [示例：Guardrail 技能](#示例guardrail-技能)
- [示例：Domain 技能](#示例domain-技能)
- [校验](#校验)

---

## 文件位置

**路径：** `.claude/skills/skill-rules.json`

该 JSON 文件定义所有技能及其触发条件，用于自动激活系统。

---

## 完整 TypeScript Schema

```typescript
interface SkillRules {
    version: string;
    skills: Record<string, SkillRule>;
}

interface SkillRule {
    type: 'guardrail' | 'domain';
    enforcement: 'block' | 'suggest' | 'warn';
    priority: 'critical' | 'high' | 'medium' | 'low';

    promptTriggers?: {
        keywords?: string[];
        intentPatterns?: string[];  // Regex strings
    };

    fileTriggers?: {
        pathPatterns: string[];     // Glob patterns
        pathExclusions?: string[];  // Glob patterns
        contentPatterns?: string[]; // Regex strings
        createOnly?: boolean;       // Only trigger on file creation
    };

    blockMessage?: string;  // For guardrails, {file_path} placeholder

    skipConditions?: {
        sessionSkillUsed?: boolean;      // Skip if used in session
        fileMarkers?: string[];          // e.g., ["@skip-validation"]
        envOverride?: string;            // e.g., "SKIP_DB_VERIFICATION"
    };
}
```

---

## 字段指南

### 顶层

| 字段 | 类型 | 是否必须 | 说明 |
|-------|------|----------|-------------|
| `version` | string | 是 | Schema 版本（当前为 "1.0"） |
| `skills` | object | 是 | 技能名称 → SkillRule 的映射 |

### SkillRule 字段

| 字段 | 类型 | 是否必须 | 说明 |
|-------|------|----------|-------------|
| `type` | string | 是 | "guardrail"（强制执行）或 "domain"（建议性） |
| `enforcement` | string | 是 | "block"（PreToolUse）、"suggest"（UserPromptSubmit）或 "warn" |
| `priority` | string | 是 | "critical"、"high"、"medium" 或 "low" |
| `promptTriggers` | object | 可选 | UserPromptSubmit hook 的触发器 |
| `fileTriggers` | object | 可选 | PreToolUse hook 的触发器 |
| `blockMessage` | string | 可选* | enforcement="block" 时必须。可使用 `{file_path}` 占位符 |
| `skipConditions` | object | 可选 | 跳过出口与会话追踪 |

*Guardrail 必须

### promptTriggers 字段

| 字段 | 类型 | 是否必须 | 说明 |
|-------|------|----------|-------------|
| `keywords` | string[] | 可选 | 精确子串匹配（不区分大小写） |
| `intentPatterns` | string[] | 可选 | 用于意图检测的正则模式 |

### fileTriggers 字段

| 字段 | 类型 | 是否必须 | 说明 |
|-------|------|----------|-------------|
| `pathPatterns` | string[] | 是* | 文件路径的 glob 模式 |
| `pathExclusions` | string[] | 可选 | 需排除的 glob 模式（如测试文件） |
| `contentPatterns` | string[] | 可选 | 用于匹配文件内容的正则模式 |
| `createOnly` | boolean | 可选 | 仅在创建新文件时触发 |

*存在 fileTriggers 时必须

### skipConditions 字段

| 字段 | 类型 | 是否必须 | 说明 |
|-------|------|----------|-------------|
| `sessionSkillUsed` | boolean | 可选 | 本次会话已使用该技能则跳过 |
| `fileMarkers` | string[] | 可选 | 文件包含注释标记则跳过 |
| `envOverride` | string | 可选 | 用于禁用该技能的环境变量名 |

---

## 示例：Guardrail 技能

一个包含全部功能的阻塞型 Guardrail 技能完整示例：

```json
{
  "database-verification": {
    "type": "guardrail",
    "enforcement": "block",
    "priority": "critical",

    "promptTriggers": {
      "keywords": [
        "prisma",
        "database",
        "table",
        "column",
        "schema",
        "query",
        "migration"
      ],
      "intentPatterns": [
        "(add|create|implement).*?(user|login|auth|tracking|feature)",
        "(modify|update|change).*?(table|column|schema|field)",
        "database.*?(change|update|modify|migration)"
      ]
    },

    "fileTriggers": {
      "pathPatterns": [
        "**/schema.prisma",
        "**/migrations/**/*.sql",
        "database/src/**/*.ts",
        "form/src/**/*.ts",
        "email/src/**/*.ts",
        "users/src/**/*.ts",
        "projects/src/**/*.ts",
        "utilities/src/**/*.ts"
      ],
      "pathExclusions": [
        "**/*.test.ts",
        "**/*.spec.ts"
      ],
      "contentPatterns": [
        "import.*[Pp]risma",
        "PrismaService",
        "prisma\\.",
        "\\.findMany\\(",
        "\\.findUnique\\(",
        "\\.findFirst\\(",
        "\\.create\\(",
        "\\.createMany\\(",
        "\\.update\\(",
        "\\.updateMany\\(",
        "\\.upsert\\(",
        "\\.delete\\(",
        "\\.deleteMany\\("
      ]
    },

    "blockMessage": "⚠️ BLOCKED - Database Operation Detected\n\n📋 REQUIRED ACTION:\n1. Use Skill tool: 'database-verification'\n2. Verify ALL table and column names against schema\n3. Check database structure with DESCRIBE commands\n4. Then retry this edit\n\nReason: Prevent column name errors in Prisma queries\nFile: {file_path}\n\n💡 TIP: Add '// @skip-validation' comment to skip future checks",

    "skipConditions": {
      "sessionSkillUsed": true,
      "fileMarkers": [
        "@skip-validation"
      ],
      "envOverride": "SKIP_DB_VERIFICATION"
    }
  }
}
```

### Guardrail 关键点

1. **type**：必须为 "guardrail"
2. **enforcement**：必须为 "block"
3. **priority**：通常为 "critical" 或 "high"
4. **blockMessage**：必须提供，且包含清晰可执行步骤
5. **skipConditions**：通过会话追踪避免重复阻塞
6. **fileTriggers**：通常同时包含路径与内容模式
7. **contentPatterns**：用于捕获技术的真实使用场景

---

## 示例：Domain 技能

一个基于建议的 Domain 技能完整示例：

```json
{
  "project-catalog-developer": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",

    "promptTriggers": {
      "keywords": [
        "layout",
        "layout system",
        "grid",
        "grid layout",
        "toolbar",
        "column",
        "cell editor",
        "cell renderer",
        "submission",
        "submissions",
        "blog dashboard",
        "datagrid",
        "data grid",
        "CustomToolbar",
        "GridLayoutDialog",
        "useGridLayout",
        "auto-save",
        "column order",
        "column width",
        "filter",
        "sort"
      ],
      "intentPatterns": [
        "(how does|how do|explain|what is|describe).*?(layout|grid|toolbar|column|submission|catalog)",
        "(add|create|modify|change).*?(toolbar|column|cell|editor|renderer)",
        "blog dashboard.*?"
      ]
    },

    "fileTriggers": {
      "pathPatterns": [
        "frontend/src/features/submissions/**/*.tsx",
        "frontend/src/features/submissions/**/*.ts"
      ],
      "pathExclusions": [
        "**/*.test.tsx",
        "**/*.test.ts"
      ]
    }
  }
}
```

### Domain 技能关键点

1. **type**：必须为 "domain"
2. **enforcement**：通常为 "suggest"
3. **priority**：通常为 "high" 或 "medium"
4. **blockMessage**：不需要（不会阻塞）
5. **skipConditions**：可选（优先级较低）
6. **promptTriggers**：通常包含大量关键词
7. **fileTriggers**：可能仅有路径模式（内容模式不那么重要）

---

## 校验

### 检查 JSON 语法

```bash
cat .claude/skills/skill-rules.json | jq .
```

如果有效，jq 会格式化输出 JSON；如果无效，会显示错误。

### 常见 JSON 错误

**尾随逗号：**
```json
{
  "keywords": ["one", "two",]  // ❌ Trailing comma
}
```

**缺少引号：**
```json
{
  type: "guardrail"  // ❌ Missing quotes on key
}
```

**单引号（非法 JSON）：**
```json
{
  'type': 'guardrail'  // ❌ Must use double quotes
}
```

### 校验清单

- [ ] JSON 语法有效（使用 `jq`）
- [ ] 所有技能名称与 SKILL.md 文件名匹配
- [ ] Guardrail 包含 `blockMessage`
- [ ] 阻塞消息使用 `{file_path}` 占位符
- [ ] 意图模式为合法正则（在 regex101.com 上测试）
- [ ] 文件路径模式使用正确的 glob 语法
- [ ] 内容模式正确转义特殊字符
- [ ] 优先级与 enforcement 等级匹配
- [ ] 无重复技能名称

---

**相关文件：**
- [SKILL.md](SKILL.md) - 技能主指南
- [TRIGGER_TYPES.md](TRIGGER_TYPES.md) - 完整触发器文档
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 配置问题调试
