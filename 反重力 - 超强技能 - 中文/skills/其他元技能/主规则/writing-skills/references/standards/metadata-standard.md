# SKILL.md 元数据标准

OpenCode 识别的官方 frontmatter 字段。

## 必需字段

```yaml
---
name: skill-name
description: >-
  Use when [trigger condition].
metadata:
  triggers: keyword1, keyword2, error-message
---
```

| 字段 | 规则 |
|-------|-------|
| `name` | 1-64 个字符，小写，仅连字符，必须与目录名匹配 |
| `description` | 1-1024 个字符，应描述何时使用 |

## 可选字段

```yaml
---
name: skill-name
description: Purpose and triggers.
metadata:
  license: MIT
  compatibility: opencode
  author: "your-name"
  version: "1.0.0"
  category: "reference"
  tags: "tag1, tag2"
---
```

| 字段 | 用途 |
|-------|---------|
| `license` | 许可证标识符（如 MIT、Apache-2.0） |
| `compatibility` | 工具兼容性标记 |
| `metadata` | 用于自定义键值对的字符串到字符串映射 |

## 名称验证

```regex
^[a-z0-9]+(-[a-z0-9]+)*$
```

**有效**：`my-skill`、`git-release`、`tdd`  
**无效**：`My-Skill`、`my_skill`、`-my-skill`、`my--skill`

## 常用元数据键

使用以下约定以保持技能的一致性：

| 键 | 示例 | 用途 |
|-----|---------|---------|
| `author` | `"your-name"` | 技能创建者 |
| `version` | `"1.0.0"` | 语义化版本 |
| `category` | `"reference"` | 类型：reference、technique、discipline、pattern |
| `tags` | `"react, hooks"` | 可搜索的关键词 |

> [!IMPORTANT]
> 此处未列出的任何字段都会被 OpenCode 的技能加载器**忽略**。
