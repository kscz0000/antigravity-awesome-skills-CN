---
name: domain-modeling
description: 构建并打磨项目的领域模型。当用户想要敲定领域术语或通用语言、记录架构决策，或当其他技能需要维护领域模型时使用。领域建模、通用语言、领域术语、架构决策记录、ADR、CONTEXT、词汇表、ubiquitous language
category: "architecture"
risk: "safe"
source: "community"
source_repo: "mattpocock/skills"
source_type: "community"
date_added: "2026-06-19"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/main/LICENSE"
tags:
  - architecture
  - workflow
  - coding-agents
tools:
  - claude-code
  - codex-cli
  - cursor
---

# 领域建模

## 使用时机

当此工作流匹配用户请求时使用：构建并打磨项目的领域模型。当用户想要敲定领域术语或通用语言、记录架构决策，或当其他技能需要维护领域模型时使用。

_来源：[mattpocock/skills](https://github.com/mattpocock/skills) (MIT)。_

在设计过程中主动构建并打磨项目的领域模型。这是一种*主动*纪律——质疑术语、构造边界场景，并在术语和决策清晰的那一刻立即将它们写入词汇表和决策记录。（仅仅*阅读* `CONTEXT.md` 来获取词汇并不是本技能——那是任何技能都能做到的一行习惯。本技能针对的是你在改变模型，而不仅仅是消费它的时候。）

## 文件结构

大多数仓库只有一个上下文：

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

如果根目录存在 `CONTEXT-MAP.md`，则该仓库有多个上下文。映射文件指明每个上下文所在位置：

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← 系统级决策
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← 上下文特定决策
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

懒加载创建文件——只有在有内容可写时才创建。如果不存在 `CONTEXT.md`，则在第一个术语得到澄清时创建一个。如果不存在 `docs/adr/`，则在需要第一个 ADR 时创建。

## 会话过程中

### 对照词汇表质疑

当用户使用的术语与 `CONTEXT.md` 中已有的语言相冲突时，立即指出。"你的词汇表把 'cancellation' 定义为 X，但你似乎指的是 Y——到底是哪个？"

### 打磨模糊的语言

当用户使用模糊或多义的术语时，提出一个精确的规范术语。"你说的是 'account'——指的是 Customer 还是 User？它们是不同的东西。"

### 讨论具体场景

当讨论领域关系时，用具体场景进行压力测试。构造探测边界场景的场景，迫使用户对概念之间的边界保持精确。

### 与代码交叉引用

当用户陈述某事的运作方式时，检查代码是否一致。如果你发现矛盾，请主动提出："你的代码取消了整个 Orders，但你刚才说支持部分取消——哪个是对的？"

### 即时更新 CONTEXT.md

当某个术语被澄清时，立即更新 `CONTEXT.md`。不要批量处理——要在它们发生时及时捕获。使用 [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) 中的格式。

`CONTEXT.md` 应该完全不含实现细节。不要把 `CONTEXT.md` 当作规范、草稿本或实现决策的存储库。它只是一个词汇表，仅此而已。

### 谨慎提供 ADR

仅当以下三个条件同时满足时，才提供创建 ADR：

1. **难以撤销** —— 事后改变主意的代价很大
2. **脱离上下文会令人惊讶** —— 未来的读者会好奇"他们为什么要这样做？"
3. **是真正权衡的结果** —— 存在真正的备选方案，你因特定原因选择了其中一个

如果三者缺一，就跳过 ADR。使用 [ADR-FORMAT.md](./ADR-FORMAT.md) 中的格式。

## 局限性

- 当工作流指定上游工具、账号、API 密钥或本地设置时，需要相应配置。
- 未经用户明确批准，不会授权执行破坏性、生产环境、付费或外部消息操作。
- 在将生成的产物或建议视为最终结果之前，请对照用户的真实来源进行验证。