---
name: pattern-name
description: >-
  Use when [recognizable symptom].
metadata:
  category: pattern
  triggers: complexity, hard-to-follow, nested
---

# 模式名称

## 模式

[1-2 句核心思想]

## 识别标志

- [模式适用的标志]
- [另一个标志]
- [代码坏味]

## 之前

```typescript
// 复杂/有问题的
function before() {
  // 嵌套、混乱
}
```

## 之后

```typescript
// 简洁/改进的
function after() {
  // 扁平、清晰
}
```

## 何时不使用

- [过度工程化的情况]
- [不需要的简单情况]

## 影响

**之前：** [问题指标]
**之后：** [改进的指标]
