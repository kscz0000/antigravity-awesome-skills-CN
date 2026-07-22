# 参考：Manus 上下文工程原则

本技能基于 Manus 的上下文工程原则。Manus 是一家 AI 智能体公司，于 2025 年 12 月被 Meta 以 20 亿美元收购。

## Manus 六大原则

### 原则 1：围绕 KV-Cache 设计

> "KV-cache 命中率是生产级 AI 智能体最重要的指标。"

**数据：**
- 输入与输出 token 比约 100:1
- 缓存 token：$0.30/MTok vs 未缓存：$3/MTok
- 成本相差 10 倍！

**实现要点：**
- 保持提示词前缀稳定（单个 token 变化就会使缓存失效）
- 系统提示词中不要放时间戳
- 上下文只追加，使用确定性序列化

### 原则 2：遮罩，而非移除

不要动态移除工具（会破坏 KV-cache），改用 logit 遮罩。

**最佳实践：** 使用一致的动作前缀（如 `browser_`、`shell_`、`file_`）便于遮罩。

### 原则 3：文件系统即外部记忆

> "Markdown 是我在磁盘上的「工作记忆」。"

**公式：**
```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)
```

**压缩必须可还原：**
- 即使丢弃网页内容，也要保留 URL
- 丢弃文档内容时，保留文件路径
- 永远不要丢失指向完整数据的指针

### 原则 4：通过复述操纵注意力

> "在整个任务过程中创建和更新 todo.md，将全局计划推入模型的近期注意力范围。"

**问题：** 经过约 50 次工具调用后，模型会遗忘原始目标（"迷失在中间"效应）。

**解决方案：** 每次决策前重读 `task_plan.md`。目标会出现在注意力窗口中。

```
Start of context: [Original goal - far away, forgotten]
...many tool calls...
End of context: [Recently read task_plan.md - gets ATTENTION!]
```

### 原则 5：保留错误信息

> "把错误的路径留在上下文中。"

**原因：**
- 带堆栈跟踪的失败操作让模型隐式更新认知
- 减少错误重复
- 错误恢复是"真正的智能体行为最清晰的信号之一"

### 原则 6：不要被 Few-Shot 带偏

> "一致性滋生脆弱性。"

**问题：** 重复的动作-观察对会导致漂移和幻觉。

**解决方案：** 引入可控的变化：
- 略微改变措辞
- 不要盲目复制粘贴模式
- 在重复性任务中重新校准

---

## 三大上下文工程策略

基于 Lance Martin 对 Manus 架构的分析。

### 策略 1：上下文缩减

**压缩：**
```
Tool calls have TWO representations:
├── FULL: Raw tool content (stored in filesystem)
└── COMPACT: Reference/file path only

RULES:
- Apply compaction to STALE (older) tool results
- Keep RECENT results FULL (to guide next decision)
```

**摘要化：**
- 当压缩收益递减时使用
- 基于完整工具结果生成
- 创建标准化的摘要对象

### 策略 2：上下文隔离（多智能体）

**架构：**
```
┌─────────────────────────────────┐
│         PLANNER AGENT           │
│  └─ Assigns tasks to sub-agents │
├─────────────────────────────────┤
│       KNOWLEDGE MANAGER         │
│  └─ Reviews conversations       │
│  └─ Determines filesystem store │
├─────────────────────────────────┤
│      EXECUTOR SUB-AGENTS        │
│  └─ Perform assigned tasks      │
│  └─ Have own context windows    │
└─────────────────────────────────┘
```

**关键发现：** Manus 最初用 `todo.md` 做任务规划，但发现约 33% 的操作都在更新它。后来改为由专用的规划智能体调用执行子智能体。

### 策略 3：上下文卸载

**工具设计：**
- 总共使用不到 20 个原子函数
- 完整结果存文件系统，不存上下文
- 用 `glob` 和 `grep` 搜索
- 渐进式披露：按需加载信息

---

## 智能体循环

Manus 运行在一个持续的 7 步循环中：

```
┌─────────────────────────────────────────┐
│  1. ANALYZE CONTEXT                      │
│     - Understand user intent             │
│     - Assess current state               │
│     - Review recent observations         │
├─────────────────────────────────────────┤
│  2. THINK                                │
│     - Should I update the plan?          │
│     - What's the next logical action?    │
│     - Are there blockers?                │
├─────────────────────────────────────────┤
│  3. SELECT TOOL                          │
│     - Choose ONE tool                    │
│     - Ensure parameters available        │
├─────────────────────────────────────────┤
│  4. EXECUTE ACTION                       │
│     - Tool runs in sandbox               │
├─────────────────────────────────────────┤
│  5. RECEIVE OBSERVATION                  │
│     - Result appended to context         │
├─────────────────────────────────────────┤
│  6. ITERATE                              │
│     - Return to step 1                   │
│     - Continue until complete            │
├─────────────────────────────────────────┤
│  7. DELIVER OUTCOME                      │
│     - Send results to user               │
│     - Attach all relevant files          │
└─────────────────────────────────────────┘
```

---

## Manus 创建的文件类型

| 文件 | 用途 | 创建时机 | 更新时机 |
|------|------|----------|----------|
| `task_plan.md` | 阶段追踪、进度 | 任务开始时 | 完成阶段后 |
| `findings.md` | 发现、决策 | 任何发现之后 | 查看图片/PDF 后 |
| `progress.md` | 会话日志、已完成事项 | 断点处 | 整个会话期间 |
| 代码文件 | 实现 | 执行前 | 出错后 |

---

## 关键约束

- **单步执行：** 每轮只执行一次工具调用，不支持并行执行。
- **计划必须存在：** 智能体必须始终知道：目标、当前阶段、剩余阶段。
- **文件即记忆：** 上下文 = 易失。文件系统 = 持久。
- **永不重复失败：** 如果某操作失败，下一次操作必须不同。
- **通信是一种工具：** 消息类型：`info`（进度）、`ask`（阻塞）、`result`（终止）

---

## Manus 数据

| 指标 | 值 |
|------|-----|
| 每任务平均工具调用次数 | ~50 |
| 输入与输出 token 比 | 100:1 |
| 收购价格 | 20 亿美元 |
| 达到 1 亿美元收入的时间 | 8 个月 |
| 上线后框架重构次数 | 5 次 |

---

## 核心引言

> "Context window = RAM (volatile, limited). Filesystem = Disk (persistent, unlimited). Anything important gets written to disk."

> "if action_failed: next_action != same_action. Track what you tried. Mutate the approach."

> "Error recovery is one of the clearest signals of TRUE agentic behavior."

> "KV-cache hit rate is the single most important metric for a production-stage AI agent."

> "Leave the wrong turns in the context."

---

## 来源

基于 Manus 官方上下文工程文档：
https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
