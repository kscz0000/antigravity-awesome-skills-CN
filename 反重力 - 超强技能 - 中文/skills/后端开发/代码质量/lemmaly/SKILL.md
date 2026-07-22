---
name: lemmaly
description: "算法优先纪律：在编写循环、查询或递归之前，先声明 Big-O、数据结构和算法族。捕获 O(n^2)、N+1 和暴力默认行为。触发词：算法纪律、Big-O声明、复杂度优先、算法族、循环前声明、复杂度审查、N+1检测、暴力代码预防。"
risk: safe
source: community
source_repo: morsechimwai/lemmaly
source_type: community
date_added: "2026-05-26"
author: morsechimwai
tags: [algorithms, big-o, performance, code-review, complexity, gateway]
tools: [claude-code, antigravity, cursor, gemini-cli, codex-cli]
license: "Apache-2.0"
license_source: "https://github.com/morsechimwai/lemmaly/blob/main/LICENSE"
---

# lemmaly — 算法优先证明

模型已经知道 Big-O、哈希表、分治法、动态规划、排序、图算法和摊还分析。它只是不会自发地应用它们。lemmaly 修复的是行为，而非知识。

本技能是四技能算法纪律套件（`lemmaly`、`mathguard`、`invariant-guard`、`complexity-cuts`）的入口关卡。它强制执行套件中其他守卫所依赖的硬性规则。

**违反这些规则的字面意思就是违反技能的精神。**"就这一次"正是 O(n²) 上线生产环境的方式。

## 何时使用本技能

在以下情况使用 **lemmaly**：

- 编写、编辑或审查涉及循环、集合、查找、搜索、连接、递归、图、查询，或对超过少量元素进行任何计算的代码时。
- 即将在 `for` 内写 `for`、在循环内使用 `.find` / `.includes` / `.indexOf`、在 `for` / `map` / `forEach` 中对独立项使用 `await`，或对集合中的每个项执行一次查询时。
- 审计代码库 / PR 中的已知反模式（await-in-loop、`.includes` 在 `.filter` 内、循环中字符串拼接、`SELECT *`、N+1 等）时。
- 审查"看起来惯用"但可能隐藏 O(n²) 或 N+1 的 AI 生成代码时。

拿不准时，**从 lemmaly 开始** — 它是入口关卡，会告诉你何时需要升级到其三个兄弟技能。

| 如果你即将… | 使用 | 原因 |
| --- | --- | --- |
| 编写*新*代码，涉及循环、查询、连接、递归或处理集合 | **lemmaly** | 在代码编写**之前**强制声明复杂度 + 数据结构 + 算法族。 |
| 重构*已有*代码，已经变慢、OOM、超时，或有嵌套循环 / N+1 / 重复工作 | **complexity-cuts** | 针对已上线且 Big-O 不良代码的纠正手册。 |
| 实现算法，但明显版本存在微妙错误（二分搜索变体、原地去重、Boyer–Moore、QuickSelect 分区、带累加器的递归、不动点 / 终止性问题） | **invariant-guard** | 强制在编码前写出函数契约 + 循环不变量。陷阱在契约中，而非循环体。 |
| 处理 n ≥ 10⁶、相似性搜索、大规模去重、top-K、流式分析、基数估计、嵌入、FFT/NTT、降维、计算几何、随机化算法 | **mathguard** | 经典算法已达下界；近似或数学密集型技术（Bloom、HLL、Count-Min、MinHash/LSH、FFT、JL 投影、扫描线、kd-tree）带来渐近优势。 |

### 路由流程

```text
Are you writing new code?
├── yes → lemmaly (state complexity, structure, family BEFORE coding)
│         ├── classical algorithm at its lower bound AND n is large? → mathguard
│         └── subtle correctness trap (invariant, base case, off-by-one)? → invariant-guard
└── no, refactoring existing slow / OOM / timed-out code → complexity-cuts
          └── still slow after classical fixes? → mathguard
```

### 一句话心智模型

- **lemmaly** = 先思考（预防）。
- **complexity-cuts** = 清理不良 Big-O（纠正）。
- **invariant-guard** = 证明正确性（验证）。
- **mathguard** = 突破经典下界（加速）。

## 铁律

```text
NO NON-TRIVIAL CODE WITHOUT STATED COMPLEXITY, DATA STRUCTURE, AND ALGORITHM FAMILY
```

在你编写循环、递归、查询或对超过少量元素的任何计算之前，消息中必须出现以下三项 — 按此顺序：

1. `time = O(?)`、`space = O(?)`，并命名主导输入维度。
2. 你将使用的数据结构，附一句话理由。
3. 算法族（以下之一：linear scan、two-pointer、sliding window、binary search、sort+sweep、hash join、BFS/DFS、topo sort、Dijkstra/A*、union-find、DP、greedy、recursion+memo、prefix sum、segment tree、monoid reduction）。

如果你无法声明全部三项，说明你还没有理解问题。提问，或读更多代码。不要写代码。

## 不可协商的规则

1. **在编写任何非平凡代码之前声明复杂度。**一行：
   - `time = O(?)`、`space = O(?)`
   - 主导输入维度：`n = 什么`，附现实量级（例如 `n ~ 10^6 rows`）
   - 如果你无法声明这些，说明你还没有理解问题。提问，或读更多代码。

2. **命名数据结构并附一句话理由。**每个集合类型的值都应从 `Array / List / Set / HashMap / TreeMap / Heap / Deque / Trie / Graph / BitSet / Counter / LinkedList` 中做出明确选择 — 并附理由："Set 用于循环内 O(1) 成员检测"、"Heap 用于 O(n log k) 的 top-K"、"Counter 将嵌套循环折叠为单次遍历"。循环内查找时默认使用哈希结构（`Set`、`Map`）。n 较大时默认使用流式/迭代器而非物化列表。

3. **在编写之前识别算法族。**命名以下之一：`linear scan`、`divide and conquer`、`two-pointer`、`sliding window`、`binary search`、`sort + sweep`、`hash join`、`BFS/DFS`、`topological sort`、`Dijkstra/A*`、`union-find`、`dynamic programming`、`greedy`、`recursion + memoization`、`prefix sum`、`segment tree`、`monoid reduction`。如果你无法命名一个族，你即将写的就是暴力解法。停下来重新考虑。

4. **循环中的重复工作是算法浪费。**以下各项在说明理由之前均视为错误：
   - 循环内的 I/O（数据库查询、HTTP 调用、文件读取）— 使用 `IN (...)`、`Promise.all`、批量端点、流式处理进行批处理
   - 在循环中重复计算同一值 — 提取或记忆化
   - 在循环内重新排序 / 重新分组 — 在外部排序一次
   - 在循环内线性扫描（`.find`、`.indexOf`、`.includes`、`in list`）— 预计算索引 `Map`
   - 每次迭代分配新结构而一个可以复用时 — 提取分配
   - 物化中间集合只为再次遍历 — 融合为一次遍历

   如果你必须在循环内执行以上任何操作，写一行注释解释原因。

5. **禁止捏造复杂度或数字。**没有论证绝不写"平均 O(log n)"。没有测量绝不写"快10倍"或"约3ms"。如果你无法推导复杂度，写 `<complexity: TBD>`。如果你没有测量，写 `<measured: TBD>`。继续前进。

## 写前协议

在产出非平凡代码之前，你的消息必须包含 — 按此顺序：

1. **问题形态** — 一句话。（"给定 n 个带时间戳的事件，找到总权重 ≤ K 的最长连续窗口。"）
2. **输入维度** — `n = ?`，现实量级，是否热路径。
3. **目标复杂度** — `time = O(?)`、`space = O(?)`。
4. **数据结构** — 逐个命名并附短语。
5. **算法族** — 一个短语。
6. **你将处理的边界情况** — 空、单元素、全等、n=1、n=max、溢出、重复。列出适用的那些。
7. **代码。**

如果 1–6 中有任何缺失，不要输出代码。

## 典型示例 — 协议对比无协议

同一问题在有和没有七步协议情况下的对比。

**问题。**给定 `users: User[]` 和 `bannedIds: string[]`，返回 `id` 未被封禁的用户。现实 n：50k 用户，5k 封禁。

### 无协议 — 上线 O(n·m)

```ts
// Looks idiomatic, ships O(n·m)
const active = users.filter((u) => !bannedIds.includes(u.id));
```

`bannedIds.includes` 每次调用是 O(m)。filter 运行 n 次 → 50k × 5k = 250M 次比较。

### 有协议 — O(n + m)

```ts
// Protocol applied:
//   time = O(n + m), space = O(m), n = 50k users, m = 5k banned
//   structure: Set<string> for O(1) membership inside the loop
//   family: linear scan with hashed lookup
//   edge cases: empty users → [], empty bannedIds → users, duplicates in bannedIds → fine (Set dedupes)
const banned = new Set(bannedIds);
const active = users.filter((u) => !banned.has(u.id));
```

第一个版本是 AI 被要求"过滤活跃用户"时默认产出的。第二个版本是协议强制的结果 — 代码可读性不变。

## 规则目录（lemmaly 扫描器）

上游仓库附带一个确定性 CLI 扫描器，执行与本技能相同的反模式检测（**11 种语言的 59 条规则**：JavaScript/TypeScript、Python、SQL、Java、C#、C++、Go、Rust、PHP、Ruby、Shell/Bash）。每条规则都有文档化的原因、错误示例、正确示例，以及需要升级到的兄弟技能。

扫描器是可选的。不要自动克隆并运行上游仓库的默认分支，因为那会执行第三方仓库中的当前代码。如果用户明确需要扫描器，将源固定到已审查的发布标签或提交，使用一次性目录，并在运行前显示解析的提交：

```bash
# Replace <reviewed-tag-or-commit> after reviewing the upstream release.
tmpdir="$(mktemp -d)"
git clone --filter=blob:none https://github.com/morsechimwai/lemmaly.git "$tmpdir/lemmaly"
git -C "$tmpdir/lemmaly" checkout --detach <reviewed-tag-or-commit>
git -C "$tmpdir/lemmaly" rev-parse HEAD
node "$tmpdir/lemmaly/cli/lemmaly.js" scan <path>
node "$tmpdir/lemmaly/cli/lemmaly.js" rules
```

扫描完成后，仅在验证 `$tmpdir` 指向 `mktemp -d` 创建的目录之后，才删除一次性目录。

**CRITICAL 严重度（CI 中为错误）：**

- `js-await-in-for-loop` — 网络上的 N+1
- `js-async-in-foreach` — 丢失的 promise
- `py-mutable-default-arg` — 共享的默认状态
- `sql-update-no-where` — 影响每一行
- `java-arraylist-remove-in-for-i` — 索引偏移；ConcurrentModification
- `cs-async-void` — 异常未被观察；导致进程崩溃
- `go-loop-var-capture` — 1.22 前对最后一个值的竞态
- `php-query-in-loop` — 对数据库的 N+1

**HIGH 严重度（CI 中为警告）：** `js-deep-clone-via-json`、`js-useeffect-missing-deps`、`js-inline-object-jsx-prop`、`js-anonymous-handler-jsx`、`js-spread-in-reduce`、`js-unique-via-indexof`、`js-helper-call-in-iterator`、`py-string-concat-in-loop`、`py-django-loop-without-eager`、`py-bare-except`、`sql-select-star`、`sql-leading-wildcard-like`、`sql-not-in-subquery`、`java-string-concat-in-loop`、`java-list-contains-in-loop`、`java-bare-catch-exception`、`cs-string-concat-in-loop`、`cs-list-contains-in-loop`、`cs-disposable-no-using`、`go-string-concat-in-loop`、`go-defer-in-loop`、`go-err-not-checked`、`rs-unwrap-in-prod`、`cpp-string-concat-in-loop`、`cpp-raw-new`、`php-count-in-for-condition`、`php-in-array-in-loop`、`rb-include-in-iterator`、`rb-n-plus-one-activerecord`、`rb-bare-rescue`、`sh-set-e-no-pipefail`、`sh-unquoted-var`、`sh-for-ls`。

**MEDIUM 严重度（CI 中为信息）：** `js-nested-for-loops`、`js-includes-in-iterator`、`js-array-key-index`、`py-range-len`、`py-in-list-literal`、`py-open-without-with`、`sql-select-no-limit`、`sql-or-in-where`、`go-slice-append-no-cap`、`rs-clone-in-loop`、`rs-vec-push-no-capacity`、`rs-string-push-no-capacity`、`cpp-vector-push-no-reserve`、`cpp-range-loop-copy`、`cpp-map-double-lookup`、`php-loose-equality`、`rb-string-concat-in-loop`、`sh-useless-cat-pipe`。

## 何时升级到兄弟技能

lemmaly 处理经典的日常算法纪律。在以下情况升级：

- **数学级优化**（概率数据结构、FFT、降维、近似算法、计算几何）— 加载 **mathguard**。
- **算法正确性**（循环不变量、终止性、递归基线、测试遗漏的边界情况）— 加载 **invariant-guard**。
- **已有不良复杂度的已上线代码** — 加载 **complexity-cuts** 获取纠正性转换手册。

## 需要警惕的合理化借口

这些是受控测试中捕获的真实逐字想法，模型输出了七步协议本可阻止的 O(n·m) 代码：

| 借口 | 现实 |
| --- | --- |
| "`.filter` 然后 `.reduce` 是惯用写法，就这样上线。" | 惯用 ≠ 正确的渐近复杂度。惯用驱动编码正是 O(n²) 上线的方式。 |
| "现在没问题，以后可以优化。" | 以后是另一个没有上下文的工程师。现在就声明复杂度。 |
| "我就用 `Array.find`，只是一次查找。" | 循环内对 `n` 个项的一次查找就是 `O(n)` 次查找。在外面建 `Map`。 |
| "开发环境数据量小 — 上线时再担心规模。" | 生产数据永远不会是开发数据的规模。七步协议只需 30 秒。 |
| "我已经理解问题了，协议是多余的开销。" | 协议"浪费时间"的那些情况，正是在生产中出问题的情况。 |

如果其中任何一条在思考过程中听起来耳熟：停下来，写下七步。

## 红旗 — 停下来重新启动协议

- 即将在未声明预期 O(n·m) 的情况下在 `for` 内写 `for`。
- 即将在循环体内调用 `.find` / `.includes` / `.indexOf`。
- 即将对独立项在 `for` / `map` / `forEach` 内 `await`。
- 即将对集合中的每个项发起一次查询。
- 即将在未声明基线或记忆化计划的情况下递归。
- 即将在未声明复杂度的情况下编写代码。
- 即将在无推导的情况下声称"这很快" / "这很高效" / "这可扩展"。
- 即将因为"暂时能用"而从记忆中复制暴力解法。

以上所有意味着：停下来，重新启动七步协议，选择更好的算法，或明确接受暴力解法并书面说明理由。

## 验证清单

在声称实现完成之前：

- [ ] 消息或 PR 描述中出现了声明的 `time = O(?)` 和 `space = O(?)`。
- [ ] 命名了主导输入维度并附现实量级。
- [ ] 每个集合类型的值都有明确的数据结构选择并附一句话理由。
- [ ] 命名了算法族（不是"一个循环"）。
- [ ] 循环内没有无一行说明的 I/O、`.find` / `.includes` / `.indexOf`、正则编译、排序或独立 `await`。
- [ ] 上线代码与声明的复杂度一致（不确定时重新推导）。
- [ ] 写前协议中列出的每个边界情况都有对应的代码路径或测试。
- [ ] 任何"快速" / "高效" / "可扩展"的声明都有推导或测量 — `<measured: TBD>` 可接受；无依据的声明不可接受。

无法勾选每一项？说明你没有执行协议。从第 1 步重新开始。

## 局限性

- **不是性能分析的替代品。** lemmaly 强制渐近推理，而非测量。对于常数因子优化、延迟尾端或 I/O 瓶颈，你仍然需要性能分析器。
- **推理关卡，而非代码生成器。** 本技能改变模型在编写前的思考方式；它不会自动重写已有代码（使用 `complexity-cuts` 做那个）。
- **仅限英文执行。** 规则目录和提示词仅支持英文。
- **n < ~10 豁免。** 协议明确接受平凡集合和一次性设置代码；不要为 `for i in range(3)` 浪费时间声明复杂度。
- **无法阻止有意的暴力解法。** 如果作者写了一行理由（"实践中 n ≤ 100；可读性更重要"），暴力解法可以上线。技能只要求理由，而非禁止。
- **CLI 扫描器是独立的。** 59 条规则由上游仓库中的 `lemmaly scan` 执行，而非仅凭本 SKILL.md。

## 论点，一句话

> **AI 默认输出算法上懒惰的代码。lemmaly 让它先思考。**

## 相关技能

- `mathguard` — 升级到 n ≥ 10⁶，经典 O(n log n) 已是下界，概率 / 数学密集型技术胜出。
- `invariant-guard` — 正确性层，针对明显版本存在微妙错误的算法。
- `complexity-cuts` — 纠正手册，针对已上线且 Big-O 不良的代码。
