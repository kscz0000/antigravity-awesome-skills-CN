---
name: complexity-cuts
description: "通过"一次只做一个变换"的剧本（含验证-回退-停止循环）来降低既有代码的 Big-O。新写代码请使用 lemmaly；若需要数学层面的优化请升级到 mathguard。触发词：复杂度、Big-O、降低复杂度、算法优化、性能、O(n^2)、N+1、refactoring"
risk: safe
source: community
source_repo: morsechimwai/lemmaly
source_type: community
date_added: "2026-05-26"
author: morsechimwai
tags: [algorithms, big-o, refactoring, optimization, performance, n-plus-one]
tools: [claude-code, antigravity, cursor, gemini-cli, codex-cli]
license: "Apache-2.0"
license_source: "https://github.com/morsechimwai/lemmaly/blob/main/LICENSE"
---

# complexity-cuts — 降低既有代码的 Big-O

`lemmaly` 在代码写出之前防止糟糕的复杂度。**complexity-cuts** 则是在事后修复：代码已经存在且能运行，但其时间或空间复杂度高于必要水平。

**违背这些规则的字面要求，就违背了本技能的精神。** "稍微变通一下"正是更快但错误的重写能够上线的原因。

## 何时使用本技能

在重构已存在、但 Big-O 不佳的代码时使用 **complexity-cuts**：

- 嵌套循环、`O(n²)` 或更差的扫描、重复计算、冗余分配、内存爆掉。
- 常见的症状描述：「这个在大输入上很慢」「超时了」「OOM」「占内存太多」「降低复杂度」「优化算法」。
- ORM 中的 N+1 查询模式（Prisma、Drizzle、SQLAlchemy、Django、ActiveRecord）。
- 在针对独立项的 `for` 循环内使用 `await`，导致串行延迟。

要在代码写出之前*预防*糟糕的复杂度，请使用 **`lemmaly`**。如果是数学层面的优化（Bloom、HLL、FFT、JL 投影），请升级到 **`mathguard`**。

## 铁律

```text
NO TRANSFORMATION WITHOUT EXISTING TESTS GREEN BEFORE AND AFTER
（没有"变换前后测试均为绿"作为前提，不得做任何变换）
```

如果代码没有测试，你必须先写一个表征测试（特征化测试，golden input → current output）。然后再变换。然后再验证测试仍然通过。如果你跳过这一步，优化可能悄无声息地破坏调用方——更快但错误，不如慢但正确。

## 不可妥协的规则

1. **在动手前先写出当前和目标的 Big-O。** 一行写完：
   - 当前：`time = O(?)`，`space = O(?)`
   - 目标：`time = O(?)`，`space = O(?)`
   - 主导输入维度（n = 什么、实际规模多大）

   如果你写不出当前的 Big-O，说明你还没真正理解这段代码。继续读。

2. **定位瓶颈，不要靠猜。** 精确定位导致主导项的那一行（或几行）。是嵌套循环？是重复线性扫描？是重复计算？是热循环内的分配？修复就在那里，而不是别处。

3. **一次只做一个变换，配合「验证-回退-停止」循环。** 循环如下：

   1. 精确执行剧本中的一项变换。
   2. 运行既有的测试套件（或你按铁律写出的表征测试）。
   3. 如果有测试失败：**立即回退。** 不要打补丁改测试。不要绕过失败。回退。
   4. 统计本段代码的连续回退次数。如果**连续回退 3 次**，停止优化。瓶颈判断错了、变换选错了，或者代码存在你还没有建模的不变量。升级到 `invariant-guard` 并补齐缺失的契约——不要尝试第四次变换。
   5. 只有当一项变换成功落地为绿之后，才能选下一项。

   堆叠的改动会掩盖回归。被修改过的测试会让回归藏得更深。

4. **精确保持语义不变。** 降低复杂度不得改变输出、顺序保证、稳定性或错误行为。如果优化要求改变语义（例如输出不再有序），必须显式说明并确认可接受。

5. **不得编造数字。** 未经实测，绝不要写「快了 10 倍」「省了 200MB」。写成 `<measured: TBD>` 后继续推进，或者用代表性输入实际测量一下。

6. **变换落地后必须报告实测加速比。** 一旦新代码测试为绿，跑一次代表性基准（同输入、同机器、热缓存），并报告 `before → after`，用 `N× faster`（或 `N× less memory`）给出加速比。一行，写在 diff 上：

   ```text
   p50:  186 ms → 1.1 ms   (169× faster, n=20,000, 200 samples)
   ```

   如果你无法实际测量（例如收益纯渐近，而你又拿不到相应输入），明确说明：`asymptotic only, no measurement — O(n²) → O(n)`。不要静默跳过这一步。

## 变换剧本

现实世界绝大多数 Big-O 收益都来自一小套固定招式。按以下顺序尝试：

### 时间复杂度的削减

| 气味 | 修法 | 典型收益 |
|---|---|---|
| `for x in A: if x in B`，其中 B 为 list/array | 把 B 一次性转为 `Set`/`Map` | O(n·m) → O(n+m) |
| 计算 pair/join 的嵌套循环 | 在 key 上做 hash-join；按查找字段建索引 | O(n·m) → O(n+m) |
| 在循环里反复 `.find` / `.indexOf` / `.includes` | 在循环外预算一个 `Map<key, item>` 索引 | O(n^2) → O(n) |
| 重复计算同一个值 | 按输入 key 做记忆化 / 缓存 | O(n·f(n)) → O(n + f(n)) |
| 在循环里排序 | 提到循环外只排一次 | O(n^2 log n) → O(n log n) |
| 反复线性扫描求 min/max/median | 堆 / 有序结构 | O(n·k) → O(n log k) |
| 递归式重复计算（类似朴素斐波那契） | 记忆化，或改为迭代 DP | 指数级 → O(n) |
| 在循环里拼接字符串（某些语言） | 用 builder / `join` / `array.push` 再 join | O(n^2) → O(n) |
| 在循环里重复编译正则 | 在循环外只编译一次 | 常数因子，大幅 |
| 通过嵌套循环做计数 / 分组 | 用 `Counter` / `Map<k, count>` 单趟完成 | O(n^2) → O(n) |
| 滑动窗口被写成嵌套循环 | 双指针 / 窗口求和 | O(n^2) → O(n) |
| 重复计算前缀和 | 预算前缀数组，支持 O(1) 区间查询 | O(n·q) → O(n+q) |
| 区间上的成对距离 / 包含检查 | 先排序再扫描线 | O(n^2) → O(n log n) |
| Top-K 用全量排序 | 大小为 K 的堆 | O(n log n) → O(n log k) |
| 循环体内反复判断集合成员关系 | 一次性建 `Set`，复用 | O(n·m) → O(n) |
| `await` 出现在针对独立项的 `for` 内 | `Promise.all` / 批量并发 | wall-clock O(n·latency) → O(latency) |
| ORM 查询出现在循环里（N+1） | `IN (...)` / `select_related` / 批量取数 | O(n) 次往返 → O(1) |

### 空间复杂度的削减

| 气味 | 修法 | 典型收益 |
|---|---|---|
| 仅为了迭代而实体化整个 list/array | 生成器 / 迭代器 / 流 | O(n) → O(1) |
| 对大数据链式 `.map().filter().map()` 产生中间数组 | 单趟循环或惰性流水线 | k·O(n) → O(n)（常可 O(1) 额外） |
| 缓存递归中每个中间结果 | 滚动窗口（保留最近 k 个状态） | O(n) → O(k) |
| 图遍历时只为计数却保存 parent/visited | 改用 bitset / counter | O(n) → O(1) |
| 为修改而拷贝输入 | 在调用方允许时原地修改 | O(n) → O(1) |
| 处理前就把整个文件读入内存 | 按行 / 按块流式读取 | O(file) → O(chunk) |
| 出于安全在循环里深拷贝 | 一次性 clone，或用结构共享 / 不可变结构 | O(n·m) → O(n+m) |
| 持有阻止 GC 回收的引用（闭包、监听器、缓存） | 给缓存设上限（LRU），摘掉监听器，缩小闭包作用域 | 无界 → 有界 |
| 一次性从 DB 加载完整结果集 | 游标 / 分页 / 流式查询 | O(rows) → O(page) |
| 用 `JSON.parse(JSON.stringify(x))` 复制 | `structuredClone` 或定向拷贝 | 消除 O(n) 的工作和分配 |

### 当你无法再降低渐近 Big-O 时

有时 O(n log n) 真的就是下界。这时转向常数因子层面的优化：

- 用连续内存的数组替换指针追逐型结构（提升缓存局部性）。
- 把循环不变量提到外面。
- 避免在热循环内分配（复用缓冲区）。
- 对数值运算，优先使用类型化数组 / 原生容器，而不是装箱对象。
- 合并系统调用 / I/O。

必须显式说明：「渐近下界就是 O(n log n)；下面只做常数因子优化。」

## 必需的工作流

对待优化的每一段代码：

1. **测量或估算当前的 Big-O。** 写下来。
2. **定位瓶颈行。** 指出来。
3. **从剧本里挑一个变换。** 给出名字。
4. **应用它。** 一次性单点改动。
5. **验证行为。** 测试通过，或在代表性输入下输出一致。
6. **写出新的 Big-O。** 时间和空间一起。
7. **如果还有收益并且值得复杂度代价，重复执行。**

## 经典范例 — 有工作流 vs 无工作流

同一项优化，有无「验证-回退-停止」循环的对比。

**瓶颈。** `getOrdersWithUsers()` 处理 1 万订单要 10 秒。原因是：在 map 中执行 `users.find(u => u.id === o.userId)`，导致 O(n·m)。

### 无工作流 — 既改了语义又打补丁改测试

```ts
// No workflow: change semantics + the optimization in one go
export function getOrdersWithUsers(orders, users) {
  const userById = Object.fromEntries(users.map(u => [u.id, u]));
  return orders
    .map(o => ({ ...o, user: userById[o.userId] }))
    .filter(o => o.user); // silently drops orders whose user was deleted
}
```

既变快，又同时改变了结果集。现有测试能抓到这点——但 diff 还通过移除校验旧行为的断言，"修好"了一个 flaky 测试。CI 显示绿。两周后账单报表被打崩。

### 有工作流 — 一次变换，语义保持

```ts
// Workflow applied:
//   Bottleneck: orders.map → users.find  (line 14)
//   Current: time = O(n·m), space = O(1)
//   Target:  time = O(n+m), space = O(m)
//   Transformation: precompute index Map<userId, User> outside the loop
//   Semantic risk: None — orders with missing users still emit `user: undefined` exactly as before
//   Reverts so far: 0

export function getOrdersWithUsers(orders, users) {
  const userById = new Map(users.map(u => [u.id, u]));
  return orders.map(o => ({ ...o, user: userById.get(o.userId) }));
}
```

一次变换。既有测试原封不动。跑测试。绿就上线。红就回退（不要改测试）。3 次回退后停下来加载 `invariant-guard`——瓶颈判断错了，或者函数存在没人写下来的契约。

## 输出规范

当你提出或应用一次优化时，你的消息必须按以下顺序包含这些内容：

1. **瓶颈** — file:line 加一句话原因。
2. **当前复杂度** — `time = O(?)`，`space = O(?)`。
3. **变换** — 剧本里的名字（如果是新招式，简短描述）。
4. **新复杂度** — `time = O(?)`，`space = O(?)`。
5. **语义风险** — 调用方可能注意到的任何变化（顺序、稳定性、错误时机）。如果真的没有，写「None」也是合法答案。
6. **实测加速比** — `before → after`，用 `N× faster` 表示（如果未实测，写 `asymptotic only`）。一行，数字诚实。
7. **diff 内容。**

如果上述 1–6 任何一项缺失，说明这次优化还没准备好落地。

## 停止条件 — 出现以下情况就不要再优化

- 渐近 Big-O 已经到了该问题已知的下界。
- 输入规模可证明地小且有界（n < ~100，且不在热路径上）。
- 优化会让正确性变模糊或损害可读性，却没有实测收益。
- 瓶颈是 I/O 或外部服务时延，而不是 CPU/内存——那就直接去修那个。

越过这些点继续做"提前优化"，只会徒增风险，却没有回报。

## 需要警惕的自我辩解

| 借口 | 现实 |
| --- | --- |
| "我脑子里已经算好了，直接贴 diff 再补标签就行。" | 后补的标签会撒谎，让你以为推理就是那么来的。必须按 瓶颈 → 复杂度 → 变换 → diff 的顺序写，否则你写的是小说。 |
| "写当前 Big-O 是做无用功——这嵌套循环谁都看得出来。" | 既然谁都看得出来，写一行又有何妨。如果只有你看得出来，那你就替 reviewer 省了时间。 |
| "语义风险就是 None，这步略过。" | 「None」是合法答案——但请写出来。下一个读者并不知道你考虑了哪些保证。 |
| "我把三个变换一次性合到一个 diff 里。" | 堆叠变换会掩盖回归。一次变换、验证、再来一次。 |
| "只是小重构，这套流程杀鸡用牛刀。" | 既然是小重构，30 秒就搞定。你跳过流程的那些场景，恰恰是你把显而易见的优化点也漏掉的场景。 |
| "等会儿再测。" | "等会儿"永远是 `<measured: TBD>`。要么现在测，要么承认只有渐近论据可用。 |

## 红旗信号 — 立刻停下来

- 不写当前 Big-O 就开始优化。
- 没有定位到具体瓶颈行就声称"这应该更快"。
- 在验证任何一项变换之前就堆叠多个变换。
- 没有实测，也没有渐近论据，就宣称加速比。
- 通过悄悄改变输出语义来降低复杂度。
- 启动时只跑一次（n = 12）的代码也要去重写。

## 验证清单

在宣称一次优化完成之前：

- [ ] 既有测试（或写出的表征测试）在变换之前是绿的。
- [ ] 精确应用了一项变换。
- [ ] 变换之后测试也是绿的。
- [ ] 没有任何测试被修改、削弱或跳过以让它通过。
- [ ] 当前 Big-O 与目标 Big-O 已写在 diff 或 PR 描述里。
- [ ] 语义风险已写下来（如果真的没有，写「None」也合规）。
- [ ] 已报告实测加速比 `before → after · N× faster`（如确未测量，也明确标注 `asymptotic only`）。
- [ ] 如果做出了实测声明（例如「3 倍快」），必须附上测量命令。
- [ ] 本段代码的连续回退次数 < 3。

不能勾完以上每一项？那么这次优化就还没完成。要么回退，要么补完缺口——绝不允许上线一个只验证了一半的加速。

## 局限性

- **需要既有测试或写出的表征测试。** 没有就无法发现静默的语义回归；铁律不允许跳过。
- **只攻渐近收益；常数因子是另一种模式**（需明确标注）。本剧本不会自己改善缓存局部性或 SIMD 利用率。
- **单进程作用域。** 分布式系统的瓶颈（共识时延、副本滞后、队列反压）不在本技能范围内。
- **3 次回退规则是死的。** 如果连续三次变换失败，本技能明确强制升级到 `invariant-guard`；不允许尝试第四次。
- **测量的责任在作者身上。** complexity-cuts 要求你上报加速比，但不会替你跑基准——你必须自己提供代表性输入。
- **对 I/O 密集型代码没有帮助。** 如果主导项是网络时延或磁盘，剧本作用有限——去修 I/O 模式。

## 主题，一句话

> **既有代码的慢，是一次次的捷径累积出来的。complexity-cuts 一次次地移除它们——而且坚持在测试没绿之前，绝不放出这次优化。**

## 相关技能

- `lemmaly` — 预防关口；写新代码（而非重构既有代码）时使用。
- `invariant-guard` — 升级目标：当 3 次及以上变换未通过测试时——缺失的环节是契约，而不是优化。
- `mathguard` — 升级目标：当经典下界已经达到，且某个近似或重数学的结构可能带来收益时使用。
