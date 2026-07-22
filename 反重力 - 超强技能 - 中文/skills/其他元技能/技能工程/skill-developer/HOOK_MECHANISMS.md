# Hook 机制 - 深入解析

关于 UserPromptSubmit 与 PreToolUse hook 工作原理的技术深入说明。

## 目录

- [UserPromptSubmit Hook 流程](#userpromptsubmit-hook-流程)
- [PreToolUse Hook 流程](#pretooluse-hook-流程)
- [Exit Code 行为（关键）](#exit-code-行为关键)
- [会话状态管理](#会话状态管理)
- [性能考量](#性能考量)

---

## UserPromptSubmit Hook 流程

### 执行顺序

```
用户提交提示
    ↓
.claude/settings.json 注册 hook
    ↓
skill-activation-prompt.sh 执行
    ↓
npx tsx skill-activation-prompt.ts
    ↓
Hook 读取 stdin（包含 prompt 的 JSON）
    ↓
加载 skill-rules.json
    ↓
匹配关键词 + 意图模式
    ↓
按优先级对匹配结果分组（critical → high → medium → low）
    ↓
将格式化消息输出到 stdout
    ↓
stdout 成为 Claude 的上下文（在 prompt 之前注入）
    ↓
Claude 看到：[技能建议] + 用户的 prompt
```

### 关键点

- **Exit code**: 始终为 0（允许）
- **stdout**: → Claude 的上下文（作为系统消息注入）
- **时机**: 在 Claude 处理 prompt 之前运行
- **行为**: 非阻塞，仅建议性
- **目的**: 让 Claude 了解相关技能

### 输入格式

```json
{
  "session_id": "abc-123",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/root/git/your-project",
  "permission_mode": "normal",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "how does the layout system work?"
}
```

### 输出格式（到 stdout）

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATION CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 RECOMMENDED SKILLS:
  → project-catalog-developer

ACTION: Use Skill tool BEFORE responding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Claude 会在处理用户 prompt 之前，将此输出视为额外上下文。

---

## PreToolUse Hook 流程

### 执行顺序

```
Claude 调用 Edit/Write 工具
    ↓
.claude/settings.json 注册 hook（matcher: Edit|Write）
    ↓
skill-verification-guard.sh 执行
    ↓
npx tsx skill-verification-guard.ts
    ↓
Hook 读取 stdin（包含 tool_name、tool_input 的 JSON）
    ↓
加载 skill-rules.json
    ↓
检查文件路径模式（glob 匹配）
    ↓
读取文件内容模式（如果文件存在）
    ↓
检查会话状态（该技能是否已被使用）
    ↓
检查跳过条件（文件标记、环境变量）
    ↓
如果匹配且未被跳过：
  更新会话状态（将技能标记为已执行）
  将阻塞消息输出到 stderr
  以 exit code 2 退出（BLOCK）
否则：
  以 exit code 0 退出（ALLOW）
    ↓
如果被阻塞：
  stderr → Claude 可见消息
  Edit/Write 工具不会执行
  Claude 必须使用技能并重试
如果被允许：
  工具正常执行
```

### 关键点

- **Exit code 2**: 阻塞（stderr → Claude）
- **Exit code 0**: 允许
- **时机**: 在工具执行之前运行
- **会话追踪**: 防止同一会话中重复阻塞
- **失败时放行**: 出错时允许操作（不中断工作流）
- **目的**: 强制执行关键护栏

### 输入格式

```json
{
  "session_id": "abc-123",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/root/git/your-project",
  "permission_mode": "normal",
  "hook_event_name": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/root/git/your-project/form/src/services/user.ts",
    "old_string": "...",
    "new_string": "..."
  }
}
```

### 输出格式（被阻塞时到 stderr）

```
⚠️ BLOCKED - Database Operation Detected

📋 REQUIRED ACTION:
1. Use Skill tool: 'database-verification'
2. Verify ALL table and column names against schema
3. Check database structure with DESCRIBE commands
4. Then retry this edit

Reason: Prevent column name errors in Prisma queries
File: form/src/services/user.ts

💡 TIP: Add '// @skip-validation' comment to skip future checks
```

Claude 收到此消息后会理解需要先使用技能再重试编辑。

---

## Exit Code 行为（关键）

### Exit Code 参考表

| Exit Code | stdout | stderr | 工具执行 | Claude 可见 |
|-----------|--------|--------|----------|-------------|
| 0（UserPromptSubmit） | → 上下文 | → 仅用户 | N/A | stdout 内容 |
| 0（PreToolUse） | → 仅用户 | → 仅用户 | **继续执行** | 无 |
| 2（PreToolUse） | → 仅用户 | → **CLAUDE** | **被阻塞** | stderr 内容 |
| 其他 | → 仅用户 | → 仅用户 | 被阻塞 | 无 |

### 为什么 Exit Code 2 很重要

这是执行强制的**关键机制**：

1. **唯一途径**：从 PreToolUse 向 Claude 发送消息
2. stderr 内容会"自动反馈给 Claude"
3. Claude 看到阻塞消息并理解需要做什么
4. 工具执行被阻止
5. 对于护栏强制执行至关重要

### 示例对话流程

```
User: "Add a new user service with Prisma"

Claude: "I'll create the user service..."
    [尝试编辑 form/src/services/user.ts]

PreToolUse Hook: [Exit code 2]
    stderr: "⚠️ BLOCKED - Use database-verification"

Claude 看到错误，响应：
    "I need to verify the database schema first."
    [使用 Skill 工具: database-verification]
    [验证列名]
    [重试编辑 - 现在允许（会话追踪）]
```

---

## 会话状态管理

### 目的

防止同一会话中重复提醒——一旦 Claude 使用了技能，就不再阻塞。

### 状态文件位置

`.claude/hooks/state/skills-used-{session_id}.json`

### 状态文件结构

```json
{
  "skills_used": [
    "database-verification",
    "error-tracking"
  ],
  "files_verified": []
}
```

### 工作原理

1. **首次编辑**包含 Prisma 的文件：
   - Hook 以 exit code 2 阻塞
   - 更新会话状态：将 "database-verification" 添加到 skills_used
   - Claude 看到消息后使用技能

2. **第二次编辑**（同一会话）：
   - Hook 检查会话状态
   - 发现 "database-verification" 在 skills_used 中
   - 以 exit code 0 退出（允许）
   - 不向 Claude 发送消息

3. **不同会话**：
   - 新的 session ID = 新的状态文件
   - Hook 再次阻塞

### 局限性

Hook 无法检测技能是否被**真正调用**——它只是在每个会话中每个技能阻塞一次。这意味着：

- 如果 Claude 不使用技能但做了其他编辑，不会再次阻塞
- 信任 Claude 会遵循指令
- 未来增强：检测实际的 Skill 工具使用

---

## 性能考量

### 目标指标

- **UserPromptSubmit**: < 100ms
- **PreToolUse**: < 200ms

### 性能瓶颈

1. **加载 skill-rules.json**（每次执行）
   - 未来：内存缓存
   - 未来：监听变更，仅在需要时重载

2. **读取文件内容**（PreToolUse）
   - 仅在配置了 contentPatterns 时
   - 仅在文件存在时
   - 大文件可能较慢

3. **Glob 匹配**（PreToolUse）
   - 每个模式的正则编译
   - 未来：编译一次，缓存

4. **正则匹配**（两个 hook 都涉及）
   - 意图模式（UserPromptSubmit）
   - 内容模式（PreToolUse）
   - 未来：延迟编译，缓存编译后的正则

### 优化策略

**减少模式：**
- 使用更具体的模式（需检查的更少）
- 尽可能合并相似模式

**文件路径模式：**
- 更具体 = 需检查的文件更少
- 示例：`form/src/services/**` 优于 `form/**`

**内容模式：**
- 仅在真正必要时添加
- 更简单的正则 = 更快的匹配

---

**相关文件：**
- [SKILL.md](SKILL.md) - 技能主指南
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 调试 hook 问题
- [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) - 配置参考
