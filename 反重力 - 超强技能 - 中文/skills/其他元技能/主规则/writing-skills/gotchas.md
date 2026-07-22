---
description: 技能创建的常见陷阱和部落知识。触发词：技能陷阱、技能故障、常见错误、gotchas
metadata:
  tags: [gotchas, troubleshooting, mistakes]
---

# 技能编写陷阱

避免常见错误的部落知识。

## YAML Frontmatter

### 语法无效

```yaml
# ❌ BAD: 混合 list 和 map
metadata:
  references: 
  triggers: a, b, c
  - item1
  - item2

# ✅ GOOD: 一致的结构
metadata:
  triggers: a, b, c
  references:
    - item1
    - item2
```

### 多行描述

```yaml
# ❌ BAD: 换行导致解析错误
description: Use when creating skills.
  Also for updating.

# ✅ GOOD: 使用 YAML 多行语法
description: >-
  Use when creating or updating skills.
  Triggers: new skill, update skill
```

## 命名

### 目录必须与 `name` 字段匹配

```
# ❌ BAD
directory: my-skill/
name: mySkill  # 不匹配！

# ✅ GOOD
directory: my-skill/
name: my-skill  # 精确匹配
```

### SKILL.md 必须全大写

```
# ❌ BAD
skill.md
Skill.md

# ✅ GOOD
SKILL.md
```

## 发现

### 描述 = 触发词，而非工作流

```yaml
# ❌ BAD: 智能体读到这个就跳过整个技能
description: Analyzes code, finds bugs, suggests fixes

# ✅ GOOD: 智能体读取完整技能以理解工作流
description: Use when debugging errors or reviewing code quality
```

### 纪律型技能的违规前触发词

```yaml
# ❌ BAD: 违规之后触发
description: Use when you forgot to write tests

# ✅ GOOD: 违规之前触发
description: Use when implementing any feature, before writing code
```

## Token 效率

### 每次对话都加载的技能 = Token 消耗

- 频繁加载的技能：<200 词
- 其他技能：<500 词
- 将细节移到 `references/` 文件

### 不要复制 CLI 帮助

```markdown
# ❌ BAD: 50 行记录所有标志

# ✅ GOOD: 一行
Run `mytool --help` for all options.
```

## 反合理化（仅限纪律型技能）

### 智能体擅长找漏洞

```markdown
# ❌ BAD: 信任智能体会"领会精神"
Write test before code.

# ✅ GOOD: 显式关闭每个漏洞
Write test before code.

**No exceptions:**
- Don't keep code as "reference"
- Don't "adapt" existing code
- Delete means delete
```

### 建立合理化表

基线测试中的每个借口都放入表中：

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests-after prove nothing immediately. |

## 交叉引用

### 保持引用一层深

```markdown
# ❌ BAD: 嵌套链（A → B → C）
See [patterns.md] → which links to [advanced.md] → which links to [deep.md]

# ✅ GOOD: 扁平（A → B，A → C）
See [patterns.md] and [advanced.md]
```

### 永远不要用 @ 强制加载

```markdown
# ❌ BAD: 立即消耗上下文
@skills/my-skill/SKILL.md

# ✅ GOOD: 智能体在需要时加载
See [my-skill] for details.
```

## OpenCode 集成

### 正确的技能目录

```bash
# ❌ BAD: 旧的单数路径
~/.config/opencode/skill/my-skill/

# ✅ GOOD: 复数路径
~/.config/opencode/skills/my-skill/
```

### 技能交叉引用语法

```markdown
# ❌ BAD: 文件路径（脆弱）
See /home/user/.config/opencode/skills/my-skill/SKILL.md

# ✅ GOOD: 技能协议
See my-skill
```

## 层级选择

### 不要过度思考层级选择

```markdown
# ❌ BAD: 一开始就选择 Tier 3"以防万一"
# 结果：浪费精力，参考文件为空

# ✅ GOOD: 从 Tier 1 开始，需要时升级
# 之后随时可以添加 references/
```

### 需要升级的信号

| Signal | Action |
|--------|--------|
| SKILL.md > 200 行 | → Tier 2 |
| 3+ 相关的子主题 | → Tier 2 |
| 10+ 产品/服务 | → Tier 3 |
| "我需要 X" vs "我想要 Y" | → Tier 3 决策树 |
