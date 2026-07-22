---
name: skill-developer
description: "在 Claude Code 中创建和管理技能的综合指南，包含自动激活系统，遵循 Anthropic 官方最佳实践（含 500 行规则和渐进式披露模式）。触发词：创建技能、添加技能、修改技能触发器、技能激活调试、skill-rules.json、Hook 系统、渐进式披露、YAML frontmatter、500 行规则"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 技能开发指南

## 用途

在 Claude Code 中创建和管理技能的综合指南，包含自动激活系统，遵循 Anthropic 官方最佳实践（含 500 行规则和渐进式披露模式）。

## 何时使用此技能

当你提到以下内容时自动激活：
- 创建或添加技能
- 修改技能触发器或规则
- 了解技能激活机制
- 调试技能激活问题
- 使用 skill-rules.json
- Hook 系统机制
- Claude Code 最佳实践
- 渐进式披露
- YAML frontmatter
- 500 行规则

---

## 系统概述

### 双 Hook 架构

**1. UserPromptSubmit Hook**（主动建议）
- **文件**：`.claude/hooks/skill-activation-prompt.ts`
- **触发时机**：Claude 看到用户提示词之前
- **用途**：基于关键词 + 意图模式推荐相关技能
- **方法**：注入格式化的提醒作为上下文（stdout → Claude 的输入）
- **适用场景**：基于主题的技能、隐式工作检测

**2. Stop Hook - 错误处理提醒**（温和提醒）
- **文件**：`.claude/hooks/error-handling-reminder.ts`
- **触发时机**：Claude 完成响应之后
- **用途**：温和提醒对已编写代码进行错误处理自评
- **方法**：分析已编辑文件中的风险模式，必要时显示提醒
- **适用场景**：无阻塞摩擦的错误处理意识

**设计理念变更（2025-10-27）：** 我们放弃了阻塞式的 PreToolUse 用于 Sentry/错误处理。取而代之的是温和的响应后提醒，不阻塞工作流但保持代码质量意识。

### 配置文件

**位置**：`.claude/skills/skill-rules.json`

定义内容：
- 所有技能及其触发条件
- 强制级别（block、suggest、warn）
- 文件路径模式（glob）
- 内容检测模式（regex）
- 跳过条件（会话追踪、文件标记、环境变量）

---

## 技能类型

### 1. 护栏技能

**用途：** 强制执行防止错误的关键最佳实践

**特征：**
- 类型：`"guardrail"`
- 强制级别：`"block"`
- 优先级：`"critical"` 或 `"high"`
- 阻止文件编辑直到使用技能
- 防止常见错误（列名、关键错误）
- 会话感知（同一会话内不重复提醒）

**示例：**
- `database-verification` - 在 Prisma 查询前验证表名/列名
- `frontend-dev-guidelines` - 强制执行 React/TypeScript 模式

**适用场景：**
- 导致运行时错误的错误
- 数据完整性问题
- 关键兼容性问题

### 2. 领域技能

**用途：** 为特定领域提供全面指导

**特征：**
- 类型：`"domain"`
- 强制级别：`"suggest"`
- 优先级：`"high"` 或 `"medium"`
- 建议性，非强制
- 主题或领域特定
- 全面的文档

**示例：**
- `backend-dev-guidelines` - Node.js/Express/TypeScript 模式
- `frontend-dev-guidelines` - React/TypeScript 最佳实践
- `error-tracking` - Sentry 集成指导

**适用场景：**
- 需要深入知识的复杂系统
- 最佳实践文档
- 架构模式
- 操作指南

---

## 快速开始：创建新技能

### 步骤 1：创建技能文件

**位置：** `.claude/skills/{skill-name}/SKILL.md`

**模板：**
```markdown
---
name: my-new-skill
description: Brief description including keywords that trigger this skill. Mention topics, file types, and use cases. Be explicit about trigger terms.
---

# My New Skill

## Purpose
What this skill helps with

## When to Use
Specific scenarios and conditions

## Key Information
The actual guidance, documentation, patterns, examples
```

**最佳实践：**
- ✅ **名称**：小写、连字符、优先使用动名词形式（动词 + -ing）
- ✅ **描述**：包含所有触发关键词/短语（最多 1024 字符）
- ✅ **内容**：控制在 500 行以内——详细内容使用引用文件
- ✅ **示例**：真实的代码示例
- ✅ **结构**：清晰的标题、列表、代码块

### 步骤 2：添加到 skill-rules.json

完整 schema 参见 [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md)。

**基础模板：**
```json
{
  "my-new-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium",
    "promptTriggers": {
      "keywords": ["keyword1", "keyword2"],
      "intentPatterns": ["(create|add).*?something"]
    }
  }
}
```

### 步骤 3：测试触发器

**测试 UserPromptSubmit：**
```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**测试 PreToolUse：**
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test","tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

### 步骤 4：优化模式

根据测试结果：
- 添加缺失的关键词
- 优化意图模式以减少误报
- 调整文件路径模式
- 针对实际文件测试内容模式

### 步骤 5：遵循 Anthropic 最佳实践

✅ SKILL.md 控制在 500 行以内
✅ 使用渐进式披露，详细内容放在引用文件中
✅ 超过 100 行的引用文件添加目录
✅ 编写包含触发关键词的详细描述
✅ 在文档化之前先用 3+ 个真实场景测试
✅ 根据实际使用情况迭代

---

## 强制级别

### BLOCK（关键护栏）

- 物理阻止 Edit/Write 工具执行
- Hook 返回退出码 2，stderr → Claude
- Claude 看到消息后必须使用技能才能继续
- **适用场景**：关键错误、数据完整性、安全问题

**示例：** 数据库列名验证

### SUGGEST（推荐）

- 在 Claude 看到提示词之前注入提醒
- Claude 感知到相关技能
- 不强制执行，仅建议
- **适用场景**：领域指导、最佳实践、操作指南

**示例：** 前端开发指南

### WARN（可选）

- 低优先级建议
- 仅建议，最小强制
- **适用场景**：锦上添花的建议、信息性提醒

**很少使用** - 大多数技能使用 BLOCK 或 SUGGEST。

---

## 跳过条件与用户控制

### 1. 会话追踪

**用途：** 同一会话内不重复提醒

**工作原理：**
- 首次编辑 → Hook 阻止，更新会话状态
- 同一会话第二次编辑 → Hook 放行
- 不同会话 → 再次阻止

**状态文件：** `.claude/hooks/state/skills-used-{session_id}.json`

### 2. 文件标记

**用途：** 已验证文件的永久跳过

**标记：** `// @skip-validation`

**用法：**
```typescript
// @skip-validation
import { PrismaService } from './prisma';
// This file has been manually verified
```

**注意：** 谨慎使用——过度使用会失去意义

### 3. 环境变量

**用途：** 紧急禁用、临时覆盖

**全局禁用：**
```bash
export SKIP_SKILL_GUARDRAILS=true  # 禁用所有 PreToolUse 阻止
```

**特定技能：**
```bash
export SKIP_DB_VERIFICATION=true
export SKIP_ERROR_REMINDER=true
```

---

## 测试清单

创建新技能时，验证以下内容：

- [ ] 技能文件已创建在 `.claude/skills/{name}/SKILL.md`
- [ ] 包含 name 和 description 的正确 frontmatter
- [ ] 已添加条目到 `skill-rules.json`
- [ ] 关键词已用真实提示词测试
- [ ] 意图模式已用变体测试
- [ ] 文件路径模式已用实际文件测试
- [ ] 内容模式已针对文件内容测试
- [ ] 阻止消息清晰且可操作（如果是护栏技能）
- [ ] 跳过条件已适当配置
- [ ] 优先级与重要性匹配
- [ ] 测试中无误报
- [ ] 测试中无漏报
- [ ] 性能可接受（<100ms 或 <200ms）
- [ ] JSON 语法已验证：`jq . skill-rules.json`
- [ ] **SKILL.md 控制在 500 行以内** ⭐
- [ ] 需要时已创建引用文件
- [ ] 超过 100 行的文件已添加目录

---

## 引用文件

关于特定主题的详细信息，请参阅：

### [TRIGGER_TYPES.md](TRIGGER_TYPES.md)
所有触发类型的完整指南：
- 关键词触发（显式主题匹配）
- 意图模式（隐式动作检测）
- 文件路径触发（glob 模式）
- 内容模式（文件中的 regex）
- 每种类型的最佳实践和示例
- 常见陷阱和测试策略

### [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md)
完整的 skill-rules.json schema：
- 完整的 TypeScript 接口定义
- 逐字段说明
- 完整的护栏技能示例
- 完整的领域技能示例
- 验证指南和常见错误

### [HOOK_MECHANISMS.md](HOOK_MECHANISMS.md)
Hook 内部机制深入解析：
- UserPromptSubmit 流程（详细）
- PreToolUse 流程（详细）
- 退出码行为表（关键）
- 会话状态管理
- 性能考量

### [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
全面的调试指南：
- 技能未触发（UserPromptSubmit）
- PreToolUse 未阻止
- 误报（触发过多）
- Hook 完全未执行
- 性能问题

### [PATTERNS_LIBRARY.md](PATTERNS_LIBRARY.md)
开箱即用的模式集合：
- 意图模式库（regex）
- 文件路径模式库（glob）
- 内容模式库（regex）
- 按用例组织
- 可直接复制使用

### [ADVANCED.md](ADVANCED.md)
未来增强和创意：
- 动态规则更新
- 技能依赖
- 条件强制
- 技能分析
- 技能版本管理

---

## 快速参考摘要

### 创建新技能（5 步）

1. 创建 `.claude/skills/{name}/SKILL.md` 并包含 frontmatter
2. 添加条目到 `.claude/skills/skill-rules.json`
3. 使用 `npx tsx` 命令测试
4. 根据测试优化模式
5. SKILL.md 控制在 500 行以内

### 触发类型

- **关键词**：显式主题提及
- **意图**：隐式动作检测
- **文件路径**：基于位置的激活
- **内容**：技术特定检测

详见 [TRIGGER_TYPES.md](TRIGGER_TYPES.md)。

### 强制级别

- **BLOCK**：退出码 2，仅限关键场景
- **SUGGEST**：注入上下文，最常用
- **WARN**：建议性，很少使用

### 跳过条件

- **会话追踪**：自动（防止重复提醒）
- **文件标记**：`// @skip-validation`（永久跳过）
- **环境变量**：`SKIP_SKILL_GUARDRAILS`（紧急禁用）

### Anthropic 最佳实践

✅ **500 行规则**：SKILL.md 控制在 500 行以内
✅ **渐进式披露**：详细内容使用引用文件
✅ **目录**：超过 100 行的引用文件添加目录
✅ **单层深度**：不要深层嵌套引用
✅ **丰富描述**：包含所有触发关键词（最多 1024 字符）
✅ **测试优先**：在大量文档化之前先构建 3+ 个评估
✅ **动名词命名**：优先使用动词 + -ing（例如 "processing-pdfs"）

### 故障排查

手动测试 Hook：
```bash
# UserPromptSubmit
echo '{"prompt":"test"}' | npx tsx .claude/hooks/skill-activation-prompt.ts

# PreToolUse
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

完整的调试指南详见 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)。

---

## 相关文件

**配置：**
- `.claude/skills/skill-rules.json` - 主配置
- `.claude/hooks/state/` - 会话追踪
- `.claude/settings.json` - Hook 注册

**Hooks：**
- `.claude/hooks/skill-activation-prompt.ts` - UserPromptSubmit
- `.claude/hooks/error-handling-reminder.ts` - Stop 事件（温和提醒）

**所有技能：**
- `.claude/skills/*/SKILL.md` - 技能内容文件

---

**技能状态**：已完成 - 按照 Anthropic 最佳实践重构 ✅
**行数**：< 500（遵循 500 行规则） ✅
**渐进式披露**：详细信息使用引用文件 ✅

**下一步**：创建更多技能，根据使用情况优化模式

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来寻求澄清。
