# 领域文档

工程技能在探索代码库时应如何消费本仓库的领域文档。

## 探索前，先读取以下文件

- 仓库根目录下的 **`CONTEXT.md`**，或
- 仓库根目录下的 **`CONTEXT-MAP.md`**（如果存在） — 它指向每个上下文各自的 `CONTEXT.md`。读取与当前主题相关的每一个。
- **`docs/adr/`** — 读取与你即将工作区域相关的 ADR。在多上下文仓库中，还需检查 `src/<context>/docs/adr/` 中的上下文范围决策。

如果以上任何文件不存在，**静默继续**。不要标记其缺失；不要建议预先创建。`/domain-modeling` 技能（通过 `/grill-with-docs` 和 `/improve-codebase-architecture` 调用）会在术语或决策实际被确立时惰性创建它们。

## 文件结构

单上下文仓库（大多数仓库）：

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文仓库（根目录存在 `CONTEXT-MAP.md`）：

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← 系统级决策
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← 上下文范围决策
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## 使用词汇表中的术语

当你的输出命名一个领域概念时（在 Issue 标题、重构提案、假设、测试名称中），使用 `CONTEXT.md` 中定义的术语。不要漂移到词汇表明确避免的同义词。

如果你需要的概念尚不在词汇表中，这是一个信号 — 要么你在发明项目不使用的语言（请重新考虑），要么存在真实缺口（标注给 `/domain-modeling`）。

## 标记 ADR 冲突

如果你的输出与已有 ADR 矛盾，请明确指出，而非静默覆盖：

> _与 ADR-0007（事件溯源订单）矛盾 — 但值得重新讨论，因为…_
