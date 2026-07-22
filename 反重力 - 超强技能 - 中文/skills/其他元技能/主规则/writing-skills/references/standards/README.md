---
description: 创建智能体技能的标准和命名规则。触发词：技能标准、命名、YAML、结构
metadata:
  tags: [standards, naming, yaml, structure]
---

# 技能开发指南

创建有效智能体技能的综合参考。

## 目录结构

```
~/.config/opencode/skills/
  {skill-name}/           # kebab-case，与 `name` 字段匹配
    SKILL.md              # 必需：主技能定义
    references/           # 可选：支持文档
      README.md           # 子主题入口
      *.md                # 其他文件
```

**项目本地替代方案：**
```
.agent/skills/{skill-name}/SKILL.md
```

## 命名规则

| 元素 | 规则 | 示例 |
|---------|------|---------|
| 目录 | kebab-case，1-64 个字符 | `react-best-practices` |
| `SKILL.md` | 全大写，精确文件名 | `SKILL.md`（而非 `skill.md`） |
| `name` 字段 | 必须与目录名匹配 | `name: react-best-practices` |

## SKILL.md 结构

```markdown
---
name: {skill-name}
description: >-
  Use when [trigger condition].
metadata:
  category: technique
  triggers: keyword1, keyword2, error-text
---

# Skill Title

Brief description of what this skill does.

## When to Use

- Symptom or situation A
- Symptom or situation B

## How It Works

Step-by-step instructions or reference content.

## Examples

Concrete usage examples.

## Common Mistakes

What to avoid and why.
```

## 描述最佳实践

`description` 字段对技能发现至关重要：

```yaml
# ❌ BAD: 工作流概述（智能体跳过阅读完整技能）
description: Analyzes code, finds bugs, suggests fixes

# ✅ GOOD: 仅触发条件
description: Use when debugging errors or reviewing code quality.
metadata:
  triggers: bug, error, code review
```

**规则：**
- 以 "Use when..." 开头
- 将触发词放在 `metadata.triggers` 下
- 保持在 500 个字符以内
- 使用第三人称（不是"I"或"You"）

## 上下文效率

技能按需加载到上下文中。针对 token 使用进行优化：

| 指南 | 原因 |
|-----------|--------|
| 保持 SKILL.md < 500 行 | 减少上下文消耗 |
| 将详情放在支持文件中 | 智能体只读取所需内容 |
| 对参考数据使用表格 | 比散文更紧凑 |
| 链接到 CLI 工具的 `--help` | 避免重复文档 |

## 支持文件

对于复杂的技能，使用其他文件：

```
my-skill/
  SKILL.md              # 概览 + 导航
  patterns.md           # 详细模式
  examples.md           # 代码示例
  troubleshooting.md    # 常见问题
```

**支持文件需要 frontmatter**（除 `SKILL.md` 之外的任何 `.md`）：

```markdown
---
description: >-
  Short summary used for search and retrieval.
metadata:
  tags: [pattern, troubleshooting, api]
  source: internal
---
```

此 frontmatter 帮助 LLM 在从 `SKILL.md` 引用时定位正确的文件。

从 SKILL.md 引用：
```markdown
## Detailed Reference

- Patterns - Common usage patterns
- Examples - Code samples
```

## 技能类型

| 类型 | 用途 | 示例 |
|------|---------|---------|
| **参考** | 文档、API | `bigquery-analysis` |
| **技巧** | 操作指南 | `condition-based-waiting` |
| **模式** | 心智模型 | `flatten-with-flags` |
| **纪律** | 强制执行的规则 | `test-driven-development` |

## 验证清单

部署前：

- [ ] `name` 与目录名匹配？
- [ ] `SKILL.md` 全大写？
- [ ] 描述以 "Use when..." 开头？
- [ ] 触发词列在 metadata 下？
- [ ] 少于 500 行？
- [ ] 用真实场景测试过？
