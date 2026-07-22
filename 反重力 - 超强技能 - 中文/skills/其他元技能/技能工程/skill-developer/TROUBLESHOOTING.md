# 故障排查 - 技能激活问题

技能激活问题的完整调试指南。

## 目录

- [技能未触发](#技能未触发)
  - [UserPromptSubmit 未给出建议](#userpromptsubmit-未给出建议)
  - [PreToolUse 未阻塞](#pretooluse-未阻塞)
- [误报](#误报)
- [Hook 未执行](#hook-未执行)
- [性能问题](#性能问题)

---

## 技能未触发

### UserPromptSubmit 未给出建议

**症状：** 提出问题，但输出中没有出现技能建议。

**常见原因：**

####  1. 关键词不匹配

**检查：**
- 查看 skill-rules.json 中的 `promptTriggers.keywords`
- 你的提示中是否真的包含这些关键词？
- 记住：不区分大小写的子串匹配

**示例：**
```json
"keywords": ["layout", "grid"]
```
- "how does the layout work?" → ✅ 匹配 "layout"
- "how does the grid system work?" → ✅ 匹配 "grid"
- "how do layouts work?" → ✅ 匹配 "layout"
- "how does it work?" → ❌ 未匹配

**修复：** 在 skill-rules.json 中添加更多关键词变体

#### 2. 意图模式过于具体

**检查：**
- 查看 `promptTriggers.intentPatterns`
- 在 https://regex101.com/ 上测试正则
- 可能需要更宽泛的模式

**示例：**
```json
"intentPatterns": [
  "(create|add).*?(database.*?table)"  // Too specific
]
```
- "create a database table" → ✅ 匹配
- "add new table" → ❌ 不匹配（缺少 "database"）

**修复：** 放宽模式：
```json
"intentPatterns": [
  "(create|add).*?(table|database)"  // Better
]
```

#### 3. 技能名称拼写错误

**检查：**
- SKILL.md frontmatter 中的技能名称
- skill-rules.json 中的技能名称
- 必须完全一致

**示例：**
```yaml
# SKILL.md
name: project-catalog-developer
```
```json
// skill-rules.json
"project-catalogue-developer": {  // ❌ Typo: catalogue vs catalog
  ...
}
```

**修复：** 使名称完全匹配

#### 4. JSON 语法错误

**检查：**
```bash
cat .claude/skills/skill-rules.json | jq .
```

如果 JSON 无效，jq 会显示错误。

**常见错误：**
- 尾随逗号
- 缺少引号
- 使用单引号而非双引号
- 字符串中存在未转义字符

**修复：** 修正 JSON 语法，并用 jq 校验

#### 调试命令

手动测试 hook：

```bash
echo '{"session_id":"debug","prompt":"your test prompt here"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

预期：你的技能应出现在输出中。

---

### PreToolUse 未阻塞

**症状：** 编辑了应该触发护栏的文件，但未发生阻塞。

**常见原因：**

#### 1. 文件路径不匹配模式

**检查：**
- 正在编辑的文件路径
- skill-rules.json 中的 `fileTriggers.pathPatterns`
- glob 模式语法

**示例：**
```json
"pathPatterns": [
  "frontend/src/**/*.tsx"
]
```
- 编辑： `frontend/src/components/Dashboard.tsx` → ✅ 匹配
- 编辑： `frontend/tests/Dashboard.test.tsx` → ✅ 匹配（需添加排除规则！）
- 编辑： `backend/src/app.ts` → ❌ 不匹配

**修复：** 调整 glob 模式或添加缺失路径

#### 2. 被 pathExclusions 排除

**检查：**
- 你是否在编辑测试文件？
- 查看 `fileTriggers.pathExclusions`

**示例：**
```json
"pathExclusions": [
  "**/*.test.ts",
  "**/*.spec.ts"
]
```
- 编辑： `services/user.test.ts` → ❌ 被排除
- 编辑： `services/user.ts` → ✅ 未被排除

**修复：** 如果测试排除范围过宽，缩小或移除

#### 3. 内容模式未找到

**检查：**
- 文件是否真的包含该模式？
- 查看 `fileTriggers.contentPatterns`
- 正则是否正确？

**示例：**
```json
"contentPatterns": [
  "import.*[Pp]risma"
]
```
- 文件包含： `import { PrismaService } from './prisma'` → ✅ 匹配
- 文件包含： `import { Database } from './db'` → ❌ 不匹配

**调试：**
```bash
# 检查文件中是否存在该模式
grep -i "prisma" path/to/file.ts
```

**修复：** 调整内容模式或添加缺失的导入

#### 4. 会话中已使用过该技能

**检查会话状态：**
```bash
ls .claude/hooks/state/
cat .claude/hooks/state/skills-used-{session-id}.json
```

**示例：**
```json
{
  "skills_used": ["database-verification"],
  "files_verified": []
}
```

如果该技能在 `skills_used` 中，本次会话不会再次阻塞。

**修复：** 删除状态文件以重置：
```bash
rm .claude/hooks/state/skills-used-{session-id}.json
```

#### 5. 文件标记存在

**检查文件中的跳过标记：**
```bash
grep "@skip-validation" path/to/file.ts
```

如果找到，该文件会被永久跳过。

**修复：** 如果需要再次校验，移除该标记

#### 6. 环境变量覆盖

**检查：**
```bash
echo $SKIP_DB_VERIFICATION
echo $SKIP_SKILL_GUARDRAILS
```

如果已设置，技能将被禁用。

**修复：** 取消设置环境变量：
```bash
unset SKIP_DB_VERIFICATION
```

#### 调试命令

手动测试 hook：

```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts 2>&1
{
  "session_id": "debug",
  "tool_name": "Edit",
  "tool_input": {"file_path": "/root/git/your-project/form/src/services/user.ts"}
}
EOF
echo "Exit code: $?"
```

预期：
- exit code 2 + stderr 消息：应阻塞
- exit code 0 + 无输出：应放行

---

## 误报

**症状：** 技能在不应触发时被触发。

**常见原因与解决方案：**

### 1. 关键词过于泛化

**问题：**
```json
"keywords": ["user", "system", "create"]  // Too broad
```
- 会触发： "user manual"、"file system"、"create directory"

**解决方案：** 使关键词更具体
```json
"keywords": [
  "user authentication",
  "user tracking",
  "create feature"
]
```

### 2. 意图模式过于宽泛

**问题：**
```json
"intentPatterns": [
  "(create)"  // Matches everything with "create"
]
```
- 会触发： "create file"、"create folder"、"create account"

**解决方案：** 给模式添加上下文
```json
"intentPatterns": [
  "(create|add).*?(database|table|feature)"  // More specific
]
```

**进阶：** 使用负前瞻排除
```regex
(create)(?!.*test).*?(feature)  // Don't match if "test" appears
```

### 3. 文件路径过于泛化

**问题：**
```json
"pathPatterns": [
  "form/**"  // Matches everything in form/
]
```
- 会触发：测试文件、配置文件、所有内容

**解决方案：** 使用更窄的模式
```json
"pathPatterns": [
  "form/src/services/**/*.ts",  // Only service files
  "form/src/controllers/**/*.ts"
]
```

### 4. 内容模式匹配到无关代码

**问题：**
```json
"contentPatterns": [
  "Prisma"  // Matches in comments, strings, etc.
]
```
- 会触发： `// Don't use Prisma here`
- 会触发： `const note = "Prisma is cool"`

**解决方案：** 使模式更具体
```json
"contentPatterns": [
  "import.*[Pp]risma",        // Only imports
  "PrismaService\\.",         // Only actual usage
  "prisma\\.(findMany|create)" // Specific methods
]
```

### 5. 调整执行等级

**最后手段：** 如果误报频繁：

```json
{
  "enforcement": "block"  // Change to "suggest"
}
```

这样会从阻塞变为建议性提示。

---

## Hook 未执行

**症状：** Hook 完全未运行——无建议，也无阻塞。

**常见原因：**

### 1. Hook 未注册

**检查 `.claude/settings.json`：**
```bash
cat .claude/settings.json | jq '.hooks.UserPromptSubmit'
cat .claude/settings.json | jq '.hooks.PreToolUse'
```

预期：存在 Hook 条目

**修复：** 添加缺失的 hook 注册：
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-activation-prompt.sh"
          }
        ]
      }
    ]
  }
}
```

### 2. Bash 包装脚本不可执行

**检查：**
```bash
ls -l .claude/hooks/*.sh
```

预期： `-rwxr-xr-x`（可执行）

**修复：**
```bash
chmod +x .claude/hooks/*.sh
```

### 3. Shebang 不正确

**检查：**
```bash
head -1 .claude/hooks/skill-activation-prompt.sh
```

预期： `#!/bin/bash`

**修复：** 在首行添加正确的 shebang

### 4. npx/tsx 不可用

**检查：**
```bash
npx tsx --version
```

预期：版本号

**修复：** 安装依赖：
```bash
cd .claude/hooks
npm install
```

### 5. TypeScript 编译错误

**检查：**
```bash
cd .claude/hooks
npx tsc --noEmit skill-activation-prompt.ts
```

预期：无输出（无错误）

**修复：** 修正 TypeScript 语法错误

---

## 性能问题

**症状：** Hook 较慢，在提示/编辑前有明显延迟。

**常见原因：**

### 1. 模式过多

**检查：**
- 统计 skill-rules.json 中的模式数量
- 每个模式 = 正则编译 + 匹配

**解决方案：** 减少模式
- 合并相似模式
- 移除冗余模式
- 使用更具体的模式（匹配更快）

### 2. 复杂正则

**问题：**
```regex
(create|add|modify|update|implement|build).*?(feature|endpoint|route|service|controller|component|UI|page)
```
- 长交替项 = 慢

**解决方案：** 简化
```regex
(create|add).*?(feature|endpoint)  // Fewer alternatives
```

### 3. 检查文件过多

**问题：**
```json
"pathPatterns": [
  "**/*.ts"  // Checks ALL TypeScript files
]
```

**解决方案：** 更具体
```json
"pathPatterns": [
  "form/src/services/**/*.ts",  // Only specific directory
  "form/src/controllers/**/*.ts"
]
```

### 4. 大文件

内容模式匹配会读取整个文件——大文件会较慢。

**解决方案：**
- 仅在必要时使用内容模式
- 考虑文件大小限制（未来增强）

### 性能测量

```bash
# UserPromptSubmit
time echo '{"prompt":"test"}' | npx tsx .claude/hooks/skill-activation-prompt.ts

# PreToolUse
time cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

**目标指标：**
- UserPromptSubmit： < 100ms
- PreToolUse： < 200ms

---

**相关文件：**
- [SKILL.md](SKILL.md) - 技能主指南
- [HOOK_MECHANISMS.md](HOOK_MECHANISMS.md) - Hook 工作原理
- [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) - 配置参考
