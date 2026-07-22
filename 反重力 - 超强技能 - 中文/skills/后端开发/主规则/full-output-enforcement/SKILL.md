---
name: full-output-enforcement
description: "当任务需要详尽完整的输出、完整文件或严格禁止占位符和跳过代码时使用。当用户要求'完整输出'、'完整文件'、'完整实现'时使用。"
category: frontend
risk: safe
source: community
source_repo: Leonxlnx/taste-skill
source_type: community
date_added: "2026-04-17"
author: Leonxlnx
tags: [output, code-generation, quality]
tools: [claude, cursor, codex, antigravity]
---
# Full-Output Enforcement

## 何时使用

- 用户明确要求完整文件、完整实现、详尽列表或完整交付物时使用。
- 当占位符代码、跳过章节、TODO 存根或用描述替代实现会破坏请求时使用。
- 当长回答可能需要清晰的续写块且不丢失完整性或结构完整性时使用。

## 限制

- 此技能强制完整性，但不会覆盖 token 限制、安全约束、缺失的源上下文或用户提供的范围边界。
- 必要时将长输出拆分为清晰标注的续写块，并验证每个块与上一个块干净连接。
- 不要为了满足完整输出请求而编造不可用的代码、凭证、私有 API 或项目文件。


## 基线原则

将每个任务视为生产关键。部分输出即损坏输出。不要为简洁优化——为完整性优化。如果用户要求完整文件，就交付完整文件。如果用户要求 5 个组件，就交付 5 个组件。没有例外。

## 禁止的输出模式

以下模式是硬性失败。绝不要产生它们：

**代码块中：** `// ...`、`// rest of code`、`// implement here`、`// TODO`、`/* ... */`、`// similar to above`、`// continue pattern`、`// add more as needed`、单独的 `...` 代表省略的代码

**散文中：** "Let me know if you want me to continue"、"I can provide more details if needed"、"for brevity"、"the rest follows the same pattern"、"similarly for the remaining"、"and so on"（当替代实际内容时）、"I'll leave that as an exercise"

**结构捷径：** 当请求要求完整实现时输出骨架。展示第一和最后一节而跳过中间。用一个示例和描述替代重复逻辑。描述代码应该做什么而不是编写它。

## 执行流程

1. **范围** — 读取完整请求。计算期望多少个独立交付物（文件、函数、章节、答案）。锁定该数字。
2. **构建** — 完整生成每个交付物。不要部分草稿，不要"你可以稍后扩展"。
3. **交叉检查** — 输出前，重读原始请求。将交付物数量与范围数量比较。如有遗漏，在响应前添加。

## 处理长输出

当响应接近 token 限制时：

- 不要压缩剩余章节来塞入它们。
- 不要跳到结论。
- 以完整质量写到干净的断点（函数结束、文件结束、章节结束）。
- 以此结束：

```
[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
```

收到 "continue" 时，从停止处精确继续。不要回顾，不要重复。

## 快速检查

在最终确定任何响应前，验证：
- 输出中任何地方都没有出现上述禁止模式
- 用户请求的每个项目都存在且已完成
- 代码块包含实际可运行的代码，而非代码应该做什么的描述
- 没有任何内容为了节省空间而被缩短
