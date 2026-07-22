# Logic-Lens — 逻辑全修 — 阶段 3-5（审查 · 定位 · 澄清）

---

## 阶段 3 — 深度审查（logic-review）

3a. 按阶段 1 优先顺序对每个文件应用 `../logic-review/logic-review-guide.md`，使用 `../_shared/common.md` §9 和 §13 的范围预算。对于超过审查预算的文件，优先追踪最高风险的入口点，将未追踪的函数记入发现状态；不得执行浅层模式扫描来声称完全覆盖。

3b. 根据文件角色调整方法：
- **源码：** 标准 Premises→Trace→Divergence。
- **运行时配置：** 前提 = 声明的形状和值约束；追踪代码如何读取每个键；分歧 = 缺失/类型错误的键或约束违规。
- **约束文件**（CLAUDE.md、.logic-lens.yaml、AGENTS.md）：前提 = 声明的不变量；追踪它们管辖的代码路径；分歧 = 代码违反该不变量。
- **行为文档：** 前提 = 文档描述的行为；追踪实现；分歧 = 矛盾。

3c. 为每个发现打标签：文件路径 + 行范围、文件角色、风险代码（L1–L9 或 Cx）、严重程度、完整 Premises→Trace→Divergence 三元组，以及一个来源标签：
- `"confirmed by trace"`（默认）
- `"unconfirmed — manual check recommended"`（按铁律排除在修复队列之外）
- `"confirmed by test/error"`（由阶段 4b 写入）
- `"discovered during verification"`（由阶段 7c 写入；排队进入下一次迭代）

3d. 去重：若同一根因出现在多个文件中，为根因记录一条发现并列出所有调用点。

3e. 批次预算：超过 20 个文件时，以 20 个文件为一批按排序完成阶段 3。每批完成后，立即将已确认的 Critical 发现推进至阶段 6，再继续低层级文件。Warning/Suggestion 发现可等当前批次结束后处理。

---

## 阶段 4 — 故障定位（logic-locate，条件性）

仅在以下情况运行：用户提供了堆栈追踪或错误消息、仓库存在失败的测试、或用户描述了具体的错误行为。

4a. 对每个具体故障应用 `../logic-locate/logic-locate-guide.md`。

4b. 对每个定位发现：若已在阶段 3 结果中 → 标记为 "confirmed by test/error"；若不在 → 以 "confirmed by test/error" 标签添加。

---

## 阶段 5 — 路径澄清（logic-explain，条件性）

仅当阶段 3/4 的发现匹配以下任一条件时调用 logic-explain：
- 调用深度 > 3
- 跨模块（追踪跨越模块/包边界）
- 前提标记为 "partial — path unclear"
- 异步/并发/回调流程难以线性化

5a. 对每个标记的发现应用 `../logic-explain/logic-explain-guide.md`。

5b. 用 explain 输出更新发现的 Premises→Trace→Divergence。若 explain 步骤表明原始分歧是误解，从队列中移除该发现并在阶段 9 的 "Resolved by clarification" 中记录。
