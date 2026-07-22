---
name: invariant-guard
description: "正确性优先：强制在写代码之前先写出函数契约、循环不变量、终止论证和边界情况。捕获 Boyer-Moore、最左二分查找、QuickSelect 陷阱。触发词：循环不变量、正确性优先、不变量守卫、invariant-guard、契约先行、终止论证、边界情况枚举"
risk: safe
source: community
source_repo: morsechimwai/lemmaly
source_type: community
date_added: "2026-05-26"
author: morsechimwai
tags: [algorithms, correctness, loop-invariants, contracts, edge-cases, verification]
tools: [claude-code, antigravity, cursor, gemini-cli, codex-cli]
license: "Apache-2.0"
license_source: "https://github.com/morsechimwai/lemmaly/blob/main/LICENSE"
---

# invariant-guard — 正确性优先编码

模型知道什么是循环不变量。它知道递归需要基础情形。它知道空列表、整数溢出以及 `<` 和 `≤` 的区别。它只是在产出代码之前不把这些写下来，于是就会发布测试抓不到的微妙正确性 bug。

invariant-guard 修复了这个行为。陈述不变量。陈述基础情形。陈述终止论证。陈述边界情况。然后写代码——并验证代码维护了你所陈述的内容。

**违反这些规则的字面意思就是违反这个技能的精神。**"我知道这个算法"恰恰是发布差一和缺失后置条件 bug 的那个合理化借口。

## 何时使用此技能

在编写或审查那些"显而易见的实现却暗藏错误"的算法时，使用 **invariant-guard**：

- 后置条件比循环的自然不变量更强：Boyer-Moore 多数投票、Floyd 环检测、最左 vs 任意二分查找、QuickSelect 分区。
- 带读写指针的原地变异：原地去重、分区、旋转。
- 带多参数或累加器状态的递归。
- 疑似差一的重复元素、空输入、边界值。
- 必须终止的迭代精化：不动点、Newton、EM。
- 任何你发现自己在想"我知道这个算法"的函数——陷阱通常在契约里，不在循环体里。

与 `lemmaly`（选择算法）和 `mathguard`（选择数学）搭配使用。在算法选定*之后*、循环体编写*之前*加载 `invariant-guard`。

## 铁律

```text
NO LOOP OR RECURSION WITHOUT A WRITTEN INVARIANT AND TERMINATION ARGUMENT
```

如果你无法用一句话写出不变量，说明你还没有设计好这个循环。继续写代码就是在猜——bug 一定出在你没有枚举到的那个情况里。

## 不可协商的规则

1. **每个循环都有一行不变量。** 在编写任何循环之前，用一句话陈述每次迭代开头什么为真。示例：
   - "循环顶部：`result` 包含 `a[0..i)` 的和。"
   - "循环顶部：`lo ≤ target_position ≤ hi`。"
   - "循环顶部：`seen` 包含已处理的每个元素；`dups` 包含至少出现两次的每个元素。"

   如果你无法用一句话写出不变量，说明你还没有设计好这个循环。

2. **每个循环都有一行终止论证。** 指出每次迭代严格递减（或严格递增趋向某个上界）的量。示例：
   - "`hi − lo` 每次迭代严格递减。"
   - "`i` 每次增加 1，上界为 `n`。"
   - "`stack.length` 每次 pop 严格递减；此分支内没有任何 push。"

   没有终止论证，就没有循环。

3. **每个递归都有显式的基础情形和度量。** 在编写递归函数之前，陈述：
   - 基础情形——不递归就返回的最小输入。
   - 度量——每次递归调用严格递减的非负整数（如 `len(xs)`、`hi − lo`、`depth`、`n`）。
   - 组合方式——递归结果如何组合成答案。

   没有基础情形 + 度量，就没有递归。（互递归：陈述跨循环的度量。）

4. **先列出边界情况，不是之后。** 对于每个操作集合或数字的函数，列出以下哪些适用及其行为：
   - 空输入（`[]`、`""`、`null`、`undefined`、`None`）。
   - 单元素（`[x]`）。
   - 全等元素。
   - 已排序 / 逆序输入。
   - 重复元素（假设唯一性时）。
   - 负数、零、恰好是边界值。
   - 整数上溢 / 下溢于类型最大/最小值。
   - NaN、±Infinity、`-0`、非规格化数（浮点数）。
   - 差一边界：索引 0、索引 n−1、索引 n、长度 0、长度 1。
   - 迭代期间的并发修改。

   适用的每种情况都必须写下一句话的预期行为。

5. **让非法状态不可达，而非仅仅未处理。** 优先在类型和结构中编码约束，使错误状态无法被构造：
   - 用和类型替代布尔标志堆（`Loading | Loaded(data) | Error(msg)` 而非 `{loading, data, error}`）。
   - 用新类型包装不应混淆的 ID（`UserId` vs `OrderId`）。
   - 当函数至少需要一个元素时使用非空列表类型。
   - 在边界处解析值，而非在下游反复验证（解析而非验证）。

   如果语言无法编码，将不变量写为注释并在边界处断言。

## 写前协议

在产出包含循环、递归或非平凡状态的非平凡代码之前，你的消息必须按以下顺序包含：

1. **函数契约**——前置条件、后置条件和函数返回什么。各一行。
2. **循环不变量**——每个循环一个。（规则 1。）
3. **终止论证**——每个循环或递归一个。（规则 2、3。）
4. **基础情形和度量**——针对递归。（规则 3。）
5. **边界情况表**——要点，每个适用情况一条，附预期行为。（规则 4。）
6. **非法状态不可表示**——命名强制不变量的类型或断言。（规则 5。）
7. **代码。**
8. **自检**——每个循环一行，确认不变量在顶部成立、循环体保持它、退出蕴含后置条件。

如果 1–6 中有任何缺失，不要输出代码。

## 示例陷阱 — Boyer-Moore 多数投票

这是典型的"陷阱在契约里，不在循环体里"的案例。

**朴素基线（没有此技能时发布的内容）：**

```typescript
function findMajority(arr: number[]): number | null {
  if (arr.length === 0) return null;
  let candidate = arr[0], count = 0;
  for (const x of arr) {
    if (count === 0) candidate = x;
    if (x === candidate) count++; else count--;
  }
  return candidate;   // BUG: returns the candidate even when no majority exists
}
```

此实现在 `[1,2,3]` 上失败（返回 `3`，预期 `null`）和 `[2,2,1,1]` 上失败（返回 `1`，预期 `null`）。投票循环是正确的；后置条件是错误的。

**为什么协议能捕获它。** 编写**步骤 1（函数契约）**迫使你用朴素语言写出后置条件：

> 当且仅当 `count(x, arr) > arr.length / 2` 时返回 `x`；否则返回 `null`。

然后编写**步骤 2（循环不变量）**迫使你写出投票轮次的不变量：

> 如果 `arr` 中存在严格多数元素，循环退出时它等于 `candidate`。

这两个陈述不等价。循环不变量保证"如果多数存在，它就是候选者"——而非"候选者是多数"。一旦你把两者都写下来，差距就可见了：你需要第二轮来验证，否则后置条件不满足。

**通过协议的正确实现：**

```typescript
function findMajority(arr: number[]): number | null {
  if (arr.length === 0) return null;
  // Pass 1: vote.
  let candidate = arr[0], count = 0;
  // inv: if a strict majority exists in arr, it equals candidate at every count===0 reset.
  for (const x of arr) {
    if (count === 0) candidate = x;
    if (x === candidate) count++; else count--;
  }
  // Pass 2: verify — the voting invariant is strictly weaker than the postcondition.
  let tally = 0;
  // inv: tally = count of candidate in arr[0..i).
  for (const x of arr) if (x === candidate) tally++;
  return tally * 2 > arr.length ? candidate : null;
}
```

**可泛化的模式。** 同样的陷阱出现在：

- **Floyd 环检测**——找到相遇点只告诉你环存在，*而非*环从哪里开始。你需要第二次遍历。
- **双指针"找任意"** vs **"找最左"**——前者的循环不变量不满足后者的后置条件。
- **QuickSelect 分区**——循环返回一个位置；后置条件是该位置上的元素是第 k 小的。分区不变量差一会悄悄破坏它。
- **带重建的 DP**——表告诉你最优值；重建最优路径需要在选择数组上有单独的不变量。

在每种情况下：**先写后置条件；再写循环不变量；检查后者是否蕴含前者。如果不是，你就缺少一轮遍历、一个检查或一个辅助状态。**

## 典型示例 — 最左匹配二分查找

大多数"我知道二分查找"的实现是为"找任意匹配"写的。陷阱在后置条件。

**问题。** 给定一个带重复元素的有序数组，返回 `target` **最左**出现位置的索引，或 `-1`。

### 没有协议 — 返回任意匹配

```ts
function leftmost(a: number[], target: number): number {
  let lo = 0, hi = a.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (a[mid] === target) return mid;       // returns ANY occurrence
    if (a[mid] < target) lo = mid + 1; else hi = mid - 1;
  }
  return -1;
}
// leftmost([1,2,2,2,3], 2) → may return 2, not 1
```

循环不变量（"target 如果存在则位于 `a[lo..hi]`"）是满足的。但后置条件（"返回的索引是满足 `a[i] === target` 的*最小* `i`"）严格更强。循环体的提前返回在到达最左匹配之前就放弃了搜索。

### 有协议 — 契约驱动的最左查找

```ts
function leftmost(a: number[], target: number): number {
  // contract:
  //   pre:  a is sorted ascending
  //   post: returns smallest i with a[i] === target, or -1 if absent
  let lo = 0, hi = a.length;                 // half-open [lo, hi)
  // inv: every index < lo has a[i] < target; every index ≥ hi has a[i] > target OR is past leftmost match
  // term: hi - lo strictly halves each iteration
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (a[mid] < target) lo = mid + 1; else hi = mid;
  }
  // exit: lo === hi, and by invariant lo is the leftmost index where a[lo] >= target
  return lo < a.length && a[lo] === target ? lo : -1;
}
```

相同的循环形态。区别在于契约先写——循环体被选择来维护一个*蕴含*后置条件的不变量。

## 常见不变量模式速查

| 循环 / 算法形态 | 典型不变量 | 终止论证 |
|---|---|---|
| 线性扫描累加 | 顶部 `acc = f(a[0..i))` | `i` 每次增加 1，上界为 `n` |
| 双指针（有序） | `target（若存在）位于 a[lo..hi]` | `hi − lo` 严格递减 |
| 二分查找 | `target（若存在）∈ a[lo..hi]` 且 `a[lo..hi]` 非空 | `hi − lo` 严格减半 |
| 滑动窗口 | 窗口 `[l..r)` 满足约束；答案 ≥ 当前最优 | `r` 每轮外循环至少前进一次 |
| BFS | 距离 < d 的所有节点已弹出；队列包含一些距离为 d 的节点 | 每次弹出的节点数严格递减 |
| DFS / 树上递归 | 以 v 为根的子树结果 = combine(子节点结果) | 深度（或剩余节点数）严格递减 |
| 分治 | `a[lo..hi]` 上的结果 = combine(两半的结果) | `hi − lo` 严格减半 |
| 带优先队列的贪心 | 提取的元素对剩余问题全局最优 | 每次提取堆大小严格递减 |
| Union-Find 操作 | `find(x)` 始终返回 x 所在分量的规范根 | 树高度以 O(log n) 为界（带 rank） |
| 原地分区 | `a[0..i)` < pivot；`a[i..j)` ≥ pivot；`a[j..n)` 未见 | `n − j` 严格递减 |

## 边界情况表 — 默认待检项

| 输入形态 | 待检情况 |
|---|---|
| 数组 / 列表 | 空、单元素、全等、已排序、逆序、含重复 |
| 字符串 | 空、单字符、全空白、unicode（代理对、组合字符）、字节 vs 码点 |
| 整数 | 0、1、−1、MIN、MAX、MAX − 1、算术接近溢出、除以 0 |
| 浮点数 | 0.0、−0.0、NaN、±Inf、非规格化、精确比较应基于 ε |
| Map / dict | 空、缺失键（默认值 vs 报错）、键冲突语义 |
| 树 / 图 | 空、单节点、环（若为无向图）、自环、多重图、不连通 |
| 流 / 迭代器 | 空、无限、单次产出、迭代中途异常 |
| 时间 / 日期 | 夏令时切换、闰秒/闰日、时区偏移、纪元边界 |
| 并发 | 无竞争、单线程、最大竞争、操作中途取消 |

## 输出纪律

你输出的代码必须：

- 每个循环有一条注释陈述不变量（使用 `// inv:` 或 `# inv:`）。
- 每个递归有一条注释陈述基础情形和度量。
- 处理你在步骤 5 中列出的每个边界情况，或显式委托（"空输入时抛异常——调用方责任"）。
- 在语言支持且代价低时，在函数入口断言前置条件。
- 在语言允许时优先使用类型（和类型、新类型、非空、非 null）而非运行时检查。

## 何时升级或重定向

- 函数是性能关键的你还没选算法——先回到 **`lemmaly`**；选好算法，再在此陈述其不变量。
- 技术是数学的（概率、FFT、几何）——加载 **`mathguard`**；近似算法的不变量包含 ε-界，而非等式。
- 代码是并发的——不变量必须考虑交错；如果假设是单线程的，显式声明"仅限单线程"。

## 需要警惕的合理化借口

| 借口 | 现实 |
| --- | --- |
| "我知道这个算法——单遍扫描，搞定。" | 知道循环 ≠ 知道契约。陷阱通常在循环未强化的后置条件里。 |
| "我在脑子里跟踪过了，没问题。" | 心理跟踪会跳过边界情况。写下不变量；检查它是否蕴含后置条件。 |
| "边界情况很明显。" | 那 30 秒写下来。如果明显，这张表很廉价。如果不明显，这张表刚救了你。 |
| "测试会抓住的。" | 测试只能抓住你想到的例子。陷阱是你没想到的那个。后置条件能抓住所有例子。 |
| "后置条件是蕴含的。" | 如果是的话，自然循环不变量就会等于它。当它们不同时（Boyer-Moore、最左查找、QuickSelect），你需要第二轮遍历、额外检查或辅助状态。 |
| "加一轮验证感觉多余。" | Boyer-Moore 投票 + 验证仍然是 O(n)。"感觉多余"恰恰是发布 bug 的那个合理化借口。 |

## 红旗 — 停下来先写不变量

- 正要写 `while (...)` 却还没陈述入口处什么为真。
- 正要写 `if (i === n − 1)` 或 `if (i === n)`——边界可疑，重述不变量。
- 正要递归却没在本消息中命名基础情形。
- 正要写 `// TODO: handle empty`——现在处理它或改类型使空不可能。
- 正要在浮点数上用 `==`。
- 正要跨有符号/无符号或溢出会回卷的类型做比较。
- 正要在循环中间默默吞掉一个错误（"just continue"）。
- 测试通过了但你实际没有陈述函数保证什么。
- "在我试过的例子上能用。"

## 验证清单

在声称函数正确之前：

- [ ] 每个循环在代码中有一行 `// inv:` 注释。
- [ ] 每个循环有写下的终止论证（在注释或 PR 描述中）。
- [ ] 每个递归在代码中命名了其基础情形和度量。
- [ ] 函数的后置条件已写下，且被最后一个循环的退出状态所蕴含。
- [ ] 表中每个适用的边界情况都有测试或显式的"委托给调用方"注释。
- [ ] 至少一个测试覆盖每个非平凡边界（空、单元素、最大值、差一）。
- [ ] 函数拒绝的非法状态要么在类型中不可表示，要么在入口处断言。
- [ ] 对于近似/随机化算法（升级到 mathguard）：ε-界是后置条件的一部分，而非等式。

无法勾选每个框？代码是示例正确的，而非行为正确的。要么填补差距，要么降级函数声明的契约。

## 局限性

- **不是自动化证明器。** invariant-guard 要求作者*写下*不变量；它不会机械地检查它们。配合基于属性的测试以获得更强证据。
- **并发默认不在范围内。** 所述不变量默认假设单线程执行，除非显式扩展；多线程推理需要额外的 happens-before / 可线性化论证。
- **浮点和溢出边界情况因语言而异。** 边界情况表是一份清单，不能替代理解你所用语言的数值语义。
- **会拖慢简单代码。** 对于显然不会失败的单行代码，协议是额外开销；留给非平凡的循环、递归和原地变异。
- **文档是唯一的强制手段。** 如果作者跳过了写不变量，此技能无法检测到——配合代码审查或要求契约的 PR 模板。

## 一句话论点

> **测试验证示例。不变量验证行为。AI 助手默认发布示例正确、行为错误的代码。invariant-guard 让它们先推理行为。**

## 相关技能

- `lemmaly` — 算法选择必须在不变量之前确定；如果算法族不明确，先加载 lemmaly。
- `mathguard` — 针对近似 / 随机化算法的 ε-有界后置条件。
- `complexity-cuts` — 如果 3+ 次优化变换导致测试失败，bug 是缺失的契约，不是缺失的优化——在此升级。
