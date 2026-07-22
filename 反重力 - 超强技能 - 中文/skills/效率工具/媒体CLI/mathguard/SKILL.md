---
name: mathguard
description: "面向 n >= 10^6 的数学重优化升级——Bloom、HyperLogLog、Count-Min、MinHash/LSH、FFT、JL 投影、扫描线。当经典 O(n log n) 已是下界且近似算法或数学方法能获胜时使用。触发词：大数据量优化、概率数据结构、近似算法、Bloom 过滤器、HyperLogLog、FFT 加速、高维降维、大规模去重、基数估算、流式计算、数学级优化。"
risk: safe
source: community
source_repo: morsechimwai/lemmaly
source_type: community
date_added: "2026-05-26"
author: morsechimwai
tags: [algorithms, probabilistic-data-structures, approximate-algorithms, bloom-filter, hyperloglog, fft, performance]
tools: [claude-code, antigravity, cursor, gemini-cli, codex-cli]
license: "Apache-2.0"
license_source: "https://github.com/morsechimwai/lemmaly/blob/main/LICENSE"
---

# mathguard — 面向 AI 代码的数学密集型优化

`lemmaly` 帮你选择正确的经典算法。`mathguard` 在经典算法已经最优但**数学方法能给出更优上界**时介入——通常通过接受有界近似、利用结构特性，或迁移到更智能的代数空间来实现。

模型知道这些技术。但它几乎不会主动提出。mathguard 解决这个问题。

**违反这些规则的字面含义就是违背该技能的精神。** 一个调用方期望精确答案的 Bloom 过滤器是生产事故，而非优化。

## 何时使用此技能

在以下场景使用 **mathguard**：

- 处理大规模数据（`n ≥ 10⁶`）：相似性搜索、去重、Top-K / 频繁项、流式分析、基数估算、嵌入向量、推荐系统。
- 执行信号/图像处理、多项式或大整数算术、卷积、图距离、计算几何、随机化算法。
- 经典 O(n log n) 已经是下界且你需要渐进优势（Bloom filter、HyperLogLog、Count-Min Sketch、MinHash/LSH、FFT/NTT、Johnson-Lindenstrauss 投影、扫描线、kd-tree/BVH、快速幂、monoid 并行归约、摊还势能法）。
- 在 `lemmaly` 确认经典方案不足之后加载。

**不要**在以下场景使用 mathguard：
- 调用方需要精确答案（认证、计费、正确性去重、主键）。
- `n` 较小（n < 10⁴）且非热点路径。
- 瓶颈是 I/O，而非 CPU/内存。

## 铁律

```text
NO APPROXIMATE STRUCTURE WITHOUT WRITTEN ε/δ AND EXPLICIT CALLER ACCEPTANCE
```

概率数据结构（Bloom、HyperLogLog、Count-Min、MinHash/LSH、t-digest）、随机化投影（JL）和有损变换（浮点 FFT）都会改变答案的含义。在提议之前：

1. 写出调用方能看到的误差参数（误报率、相对误差、失真边界）。
2. 识别调用方并用一句话说明他们容忍这类错误答案。
3. 如果你无法识别调用方，或者他们需要精确结果（认证检查、计费、去重键、用于正确性的去重、任何流入主键的数据），**不要**提议近似结构。保持经典方案，或升级为分片/流式精确设计。

这条规则避免的事故比本技能中其他规则都多。不要放松执行。

## 不可协商的规则

1. ** upfront 声明精确 vs 近似。** 在建议数学级技术之前，声明：
   - `mode: exact` 或 `mode: approximate`
   - 若为近似：误差参数（ε, δ, 误报率）以及调用方是否能容忍的判断句。
   - 如果调用方需要精确且没有精确优势方案，直说并停止——不要静默退化为近似。

2. **按名称引用技术。** 永远不要用模糊术语描述概率或数值技巧。给它命名：`Bloom filter`、`HyperLogLog`、`Count-Min Sketch`、`MinHash + LSH`、`Johnson–Lindenstrauss projection`、`FFT`、`NTT`、`fast exponentiation`、`Karatsuba`、`Strassen`、`sweep line`、`kd-tree`、`BVH`、`union-find with path compression`、`Floyd's cycle detection`、`Boyer-Moore majority`、`reservoir sampling`、`Knuth shuffle`、`Aho-Corasick`、`suffix automaton`、`segment tree with lazy propagation`、`Fenwick tree`、`monoid scan / parallel prefix`。有命名的技术可审计；"一种智能近似"则不行。

3. **说明你在做的权衡。** 每个数学级优化都有成本地换取收益。一行概括：
   - 收获：`space`、`time`、`wall-clock`、`parallelism`。
   - 成本：`accuracy ε=?`、`code complexity`、`dependency`、`non-determinism`、`numerical stability`。
   - 若成本对调用方不可见，写"callers see no change"。

4. **论证渐进优势。** 不要在没有单行界论证的情况下提议数学技术：
   - "HyperLogLog：以 O(log log n) bit 计数唯一值，标准误差 1.04/√m。"
   - "FFT：多项式乘法 O(n log n) vs 朴素 O(n²)。"
   - "JL 投影：用 O(log n / ε²) 维度在 (1±ε) 内保留成对距离。"
   - "扫描线：矩形重叠检测从 O(n²) 对检查降至 O(n log n) 事件处理。"
   无界，不提议。

5. **禁止数学 cargo-culting。** 在以下情况不要引入这些技术：
   - n 足够小以至于线性扫描在微秒内完成（n < ~10⁴，除非是热点路径）。
   - 问题受 I/O 限制——数学优势在网络/磁盘延迟面前消失。
   - 需要精确答案且不存在精确技术。
   - 团队不会维护它（记下来："team familiarity: ?"）。

## 提议前协议

在建议数学级技术之前，你的消息必须按以下顺序包含：

1. **经典下界**——最佳的非数学算法及其 Big-O？（"Hash join 是 O(n+m)；我们已经到了。"）
2. **为何经典不够**——n 太大、空间爆炸、实时截止等。
3. **数学技术**——按命名引用（规则 2）。
4. **精确或近似**——若近似需带 ε（规则 1）。
5. **新界**——带单行推导（规则 4）。
6. **权衡**——收获/成本（规则 3）。
7. **何时不使用**——至少一个排除条件。
8. **代码或伪代码。**

如果 1-7 中有任何缺失，不要提议该技术。

## 实战手册 — 数学技术 → 问题 → 收益 → 注意事项

### 草图与概率结构（海量数据，近似）

| 问题 | 经典方案 | 数学技术 | 收益 | 注意事项 |
|---|---|---|---|---|
| 成员判定："我见过这个 key 吗？"（大规模） | `Set<id>`，O(n) 空间 | **Bloom filter** | 以选定 ε 误报率实现 O(n) bit | 仅存在误报；无法删除（需要时用 Cuckoo） |
| 统计流中的不同值数量 | 用 `Set` 计数，O(unique) 空间 | **HyperLogLog** | O(log log n) bit，~1% 相对误差 | 近似；无法列举元素 |
| 流中的 Top-K / 频繁项 | 全量计数器，O(unique) 空间 | **Count-Min Sketch** + 堆 | O(log(1/δ)·1/ε) 空间 | 会高估；审慎选择 ε,δ |
| 大规模文档/集合相似度 | 完整 Jaccard，O(n·m) | **MinHash + LSH** | 亚线性 ANN 查询 | 需调 recall vs precision；参数搜索 |
| 高维向量 k-NN | 暴力 O(n·d) | **JL 投影 → HNSW / IVF** | 每次 O(log n) 查询，(1±ε) 失真 | 索引构建成本；recall < 1 |
| 从未知长度流中取大小为 k 的蓄水池 | 缓冲全部，O(n) 空间 | **Reservoir sampling** | O(k) 空间，均匀采样 | 仅支持单遍 |
| 查找多数元素 | 计数器 map | **Boyer-Moore majority vote** | O(1) 空间，O(n) 时间 | 要求多数元素存在；需验证遍历 |
| 流中的分位数 | 排序，O(n log n) | **t-digest / GK** | O(1/ε) 空间，ε 精确分位数 | 近似 |

### 快速算术 / 变换（数值与组合）

| 问题 | 经典方案 | 数学技术 | 收益 | 注意事项 |
|---|---|---|---|---|
| 两个多项式/大整数相乘 | O(n²) | **FFT / NTT / Karatsuba** | O(n log n) | 浮点 FFT 损失精度——整数用 NTT |
| 两个信号卷积 | O(n·m) | **基于 FFT 的卷积** | O((n+m) log(n+m)) | 极小量级时存在数值噪声 |
| `pow(a, b) mod p`，b 很大 | O(b) 次乘法 | **快速幂（平方-乘法）** | O(log b) | 注意内部溢出；使用模运算 |
| 大整数 GCD | 反复减法 | **欧几里得算法** | O(log min) | 标准；AI 有时仍会写出减法循环 |
| 矩阵乘法，n 较大 | O(n³) | **Strassen**（及 Coppersmith-Winograd 家族） | O(n^2.81) | 高常数项；仅对超大稠密矩阵有优势 |
| 稀疏矩阵求解 Ax=b | O(n³) 稠密 | **共轭梯度 / 稀疏 LU** | O(nnz · iterations) | 数值条件数很重要 |
| 模逆元 | 暴力搜索 | **扩展欧几里得** 或 **Fermat**（p 为素数时） | O(log p) | Fermat 要求 p 必须为素数 |

### 降维与线性代数

| 问题 | 经典方案 | 数学技术 | 收益 | 注意事项 |
|---|---|---|---|---|
| d 维相似性，d 较大 | 暴力 O(n·d) | **JL 投影** 至 k = O(log n / ε²) | O(n·k)，(1±ε) 失真 | 随机性；在验证集上验证 |
| 从评分矩阵构建推荐 | 遍历完整矩阵 | **截断 SVD / 矩阵分解** | rank-k 时 O(k·(n+m)) | 选择 k；刷新策略 |
| 文档-词项相似度 | TF-IDF O(n·m) | **通过 SVD 做 LSA** | rank-k 近似 | 潜在维度不可解释 |
| d 维 n 样本的 PCA | O(n·d²) | **随机化 SVD** | rank-k 时 O(n·d·k) | 随机化；设置过采样 |

### 几何（空间查询）

| 问题 | 经典方案 | 数学技术 | 收益 | 注意事项 |
|---|---|---|---|---|
| 2D-3D 范围/最近邻查询 | 每次 O(n) | **kd-tree / R-tree / BVH** | 每次 O(log n) 查询 | 高维退化；改用 ANN |
| 矩形/区间重叠对 | O(n²) 对检查 | **扫描线 + 活跃集合（BBST）** | O((n+k) log n) | k = 输出规模；有线段树变体 |
| 大规模多边形点包含判定 | O(n·v) | **BSP / 单调分解 / R-tree** | 构建后每次 O(log v) 查询 | 构建成本 |
| n 点凸包 | O(n²) 礼物包装 | **Graham 扫描 / Andrew 单调链** | O(n log n) | 共线点的数值鲁棒性 |
| 最近点对 | O(n²) | **分治** | O(n log n) | 需仔细合并跨带区域 |

### 图与代数技巧

| 问题 | 经典方案 | 数学技术 | 收益 | 注意事项 |
|---|---|---|---|---|
| 合并操作下的连通分量 | 每次合并重算 BFS | **带路径压缩+秩的 Union-Find** | α(n) ≈ O(1)/op 摊还 | 逆 Ackermann 函数实际等价于常数 |
| 数组区间求和/更新 | 每次查询 O(n) | **Fenwick tree** | 每次 O(log n) | 包含区间；注意 off-by-one |
| monoid 区间查询（sum/min/max/gcd） | 每次查询 O(n) | **线段树**（范围更新时带懒标记） | O(log n) | 比 Fenwick 代码多；更通用 |
| 树中 LCA，大量查询 | 每次查询 O(n) | **倍增** 或 **欧拉序 + RMQ** | 每次 O(log n) 或 O(1) | 预处理开销 |
| DAG 最短路径 | Dijkstra | **拓扑排序 + 松弛** | O(V+E) | 仅适用于 DAG |
| 链表环检测 | 哈希已访问节点 | **Floyd 龟兔赛跑** | O(1) 空间 | 相同 big-O 时间，空间大幅节省 |
| n 元素的并行归约 | 顺序折叠 | **Monoid + 并行扫描** | p 核心 O(n/p + log p) | 运算必须满足结合律；验证之 |

### 摊还与在线算法

| 问题 | 经典方案 | 数学技术 | 收益 | 注意事项 |
|---|---|---|---|---|
| "动态数组 push 开销大" | 调整大小时每操作 O(n) | **摊还分析（倍增）** | O(1) 摊还 | `ArrayList` / `vec` 本身就这样做；为其辩护即可 |
| 流式中位数 | 重排序 | **双堆（最大堆 + 最小堆）** | 每次插入 O(log n) | 维护大小不变量 |
| 在线区间调度 | 按截止时间重排序 | **贪心 + 优先队列** | 每次到达 O(log n) | 特定目标；检查问题适配性 |
| 滑动窗口最大值 | O(n·k) | **单调队列** | 总计 O(n) | 窗口不变量维护微妙 |

## 规范示例 —— 统计独立用户数

**问题。** 统计一个 24 小时事件流中见到的独立用户数。每天 ~20 亿事件，~5000 万独立用户。展示在仪表盘上，±2% 可接受。

### 不遵循协议 —— 静默 OOM，或更糟，静默计费错误

```ts
// "直接用 Set 就行"——在 ~5000 万字符串时静默 OOM
const seen = new Set<string>();
for await (const event of stream) {
  seen.add(event.userId);
}
return seen.size; // 精确，但进程在第 4100 万行挂了
```

或者更糟——为了"性能"提议 HyperLogLog 却接入计费流水线，而后者依赖该结果。计费系统看到 4970 万而非 5000 万用户，部分用户永远不会被收费。

### 遵循协议 —— 可审计的 HLL

```ts
// 经典下界：精确 Set 需要 O(unique) 内存。5000 万字符串 × 每个 ~50B，~2.5GB。
// 为何经典不够：仪表盘容器只有 512MB 且每分钟刷新。
// 技术：HyperLogLog (HLL)。
// 模式：近似。ε ≈ 1.04/√m。m=2^14 个寄存器 → ~0.8% 相对误差。
// 权衡：收获 O(log log n)-bit 空间（~12KB）；代价 ±0.8% 显示计数偏差。
// 何时不使用：任何流入计费、主键或逐用户操作的路径。
// 调用方确认：已确认——仪表盘产品负责人接受 ±2%，写入 PR。

import { createHLL } from 'hyperloglog-lite';
const hll = createHLL({ precision: 14 });
for await (const event of stream) {
  hll.add(event.userId);
}
return hll.estimate(); // 4960 万 ± 40 万；仪表盘读取约 5000 万
```

第一个版本不是"不用 HLL"——而是"HLL 但没写下 ε 和谁容忍这种误差"。第二个版本技术上完全相同但可审计：ε 在注释中，调用方已指名，排除条件（计费）明确列出。

## 输出规范

使用数学级技术的代码必须包含：

- 一条注释命名该技术并附带文档链接或单行引用。
- 选定的精确误差参数（ε, δ, bits, dimensions 等）及取值理由。
- 参数旁的实测或渐进论证。
- 若调用方可能需要，提供精确模式回退路径。

## 何时升级或重定向

- 瓶颈是 I/O 而非 CPU/内存 → 回到 `lemmaly` 规则 4；数学帮不上忙。
- 你需要位级精确可复现性 → 避免浮点 FFT、随机化投影和概率结构。
- 结果被假设精确的下游系统消费 → 保持经典方案或包装验证步骤。
- 你需要正确性证明（不仅是界论证）→ 选择技术后加载 **invariant-guard**。

## 需警惕的合理化借口

| 借口 | 现实 |
| --- | --- |
| "`set` 能用——我在注释里标一下内存问题就行。" | 发现问题不等于解决问题。如果内存是预算，就交付尊重它的结构。 |
| "概率结构听起来花哨/太学术。" | Cloudflare 在请求路径中使用 Bloom filter。Redis 内置 HyperLogLog。这些都是生产环境验证过的，不是学术玩具。 |
| "近似有风险——我做精确的，以后 OOM 了再说。" | 凌晨 3 点静默 OOM 比声明的 0.81% 误差风险更大。声明 ε，选参数，交付。 |
| "我把 set 分片到多台机器就行了。" | 分片会成倍增加基础设施成本；HLL 在一台机器上用 12KB 就解决了。先问自己是否真的需要精确。 |
| "FFT 对这个来说杀鸡用牛刀。" | 99% 的时候确实如此。但要说出 n。n ≥ ~64 做多项式乘法时，朴素算法就已经输了。 |
| "JL 投影对嵌入来说损失太大。" | ε = 0.1 时，JL 在 10% 内保留成对距离。对 ANN 来说几乎总是没问题——测量 recall，不要凭肉眼判断。 |

## 红色警报 —— 停止

- 提议概率结构但不声明 ε 和 δ。
- 说"这里可以用 FFT"却不写出 FFT 实际超过朴素算法的 n 阈值。
- 使用 `JSON.parse(JSON.stringify(...))` 深拷贝而 `structuredClone` 存在，却声称这是优化。
- 在 100×100 矩阵上推荐 Strassen。
- 在调用方未同意的情况下切换到近似输出。
- 命名你无法推导界的技术。
- 在 n 小且非热点路径时做数学优化。
- "平均应该是 O(log n)"但没有平均情形论证。

## 验证清单

在使用数学级技术的代码发布前：

- [ ] 技术已命名（不允许"一种智能近似"）。
- [ ] 若为近似：ε 和 δ（或等效误差参数）已写入代码或 PR 描述。
- [ ] 调用方已识别且其对该误差的容忍度已声明。
- [ ] 存在单行界推导（渐近或实测）。
- [ ] 至少记录了一个排除条件（"何时不使用此项"）。
- [ ] 存在精确模式回退路径，或有一行注释说明为何精确不可能。
- [ ] 若涉及随机化：种子策略已记录（固定用于复现，或声明为非确定性）。
- [ ] 假设精确性的下游消费者（基于此值的 JOIN、计费、认证、主键）已审计。

无法勾选每一项？该技术尚未准备好发布。保持经典方案，或停下来询问。

## 局限性

- **不适用于要求精确结果的流水线。** 结果作为主键、去重键、计费输入或认证决策的任何系统不在范围内——保持经典方案。
- **假设输入具有代表性。** ε/δ 界是平均情形或高概率的；对抗性输入可能突破它们。声明威胁模型。
- **库质量参差不齐。** Bloom / HLL / MinHash 实现在种子策略、哈希函数和内存布局上有差异——选择维护良好的库并锁定版本。
- **数值稳定性。** 浮点 FFT、随机化 SVD 和 JL 投影会累积浮点误差；组合精确性需求请用 NTT 或精确整数变体。
- **团队熟悉度风险。** 凌晨 3 点没人能调试的技术是负债——在权衡旁写好维护备注。
- **不是性能分析器。** mathguard 告诉你可以突破哪个渐进上界；它不测量常数因子。在声称实际耗时收益前先 benchmark。

## 核心主张（一行总结）

> **当经典算法触达其下界时，数学之下还有另一层下界。mathguard 让模型伸手去够那层下界，而不是接受第一个答案。**

## 相关技能

- `lemmaly`——网关；在求助数学之前先选择经典算法。
- `invariant-guard`——用于将 ε 界声明为近似算法后置条件的一部分。
- `complexity-cuts`——当基线代码已存在且瓶颈是 CPU/内存而非近似时使用。
