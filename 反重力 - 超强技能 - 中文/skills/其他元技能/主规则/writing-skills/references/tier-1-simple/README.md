---
description: 何时使用 Tier 1（简单）技能架构。触发词：Tier 1、简单技能、单文件
metadata:
  tags: [tier-1, simple, single-file]
---

# Tier 1：简单技能

用于聚焦、单一目的的单文件技能。

## 何时使用

- **单一概念**：一个技巧、一个模式、一个参考
- **少于 200 行**：可以轻松放在一个文件中
- **无复杂决策逻辑**：用户确切知道他们需要什么
- **频繁加载**：需要最小的 token 占用

## 结构

```
my-skill/
└── SKILL.md          # 所有内容在一个文件中
```

## 示例

```yaml
---
name: flatten-with-flags
description: Use when simplifying deeply nested conditionals.
metadata:
  category: pattern
  triggers: nested if, complex conditionals, early return
---

# Flatten with Flags

## When to Use
- Code has 3+ levels of nesting
- Conditions are hard to follow

## The Pattern
Replace nested conditions with early returns and flag variables.

## Before
```javascript
function process(data) {
  if (data) {
    if (data.valid) {
      if (data.ready) {
        return doWork(data);
      }
    }
  }
  return null;
}
```

## After
```javascript
function process(data) {
  if (!data) return null;
  if (!data.valid) return null;
  if (!data.ready) return null;
  return doWork(data);
}
```
```

## 检查清单

- [ ] 适合在 <200 行内
- [ ] 单一聚焦目的
- [ ] 不需要 `references/` 目录
- [ ] 描述使用 "Use when..." 模式
