# 回归原因分类法

本分类法说明了在评估某个描述候选以决定是否晋升时，迭代回归是如何被分类的。

## 核心原则

候选不应仅凭聚合的通过/失败计数来评判。迭代系统应当解释：候选为何被拦截、被留置于当前描述之后、或被晋升。

## 原因标签

### `no_candidate_outperformed_current`

被选出的胜者仍然是当前描述。没有候选获得晋升。

### `visible_holdout_regression`

候选在可见留出集上发生了回归，增加了误报或漏报。

### `blind_holdout_regression`

候选在盲留出提示上发生了回归。这会拦截晋升，因为该失败并非仅局限于调优循环内部。

### `current_holdout_gap_present`

当前描述或被选出的胜者仍然存在一处可见留出集的遗漏。晋升可能仍停留在 `keep_current`，但迭代包应当展示出该未解决的缺口。

### `current_holdout_risk`

即便晋升未被拦截，可见留出集的校准看起来仍有风险。这是一个审计信号，表明路由边界需要后续工作。

### `judge_blind_regression`

评分裁判发现盲留出表现比当前描述或基线描述更差。

### `judge_blind_low_agreement`

由裁判支撑的盲评估未能产生足够的同意置信度来支持晋升。

### `adversarial_regression`

候选在模拟路由冲突或伪装请求的对抗性留出提示上表现更差。

### `adversarial_overlap_risk`

对抗性校准层报告了 `overlap` 风险带，意味着路由边界过弱、不足以安全晋升。

### `adversarial_watch_risk`

对抗性校准层报告了一个非失败但需警惕的风险带，例如 `watch` 或 `tight`。

### `family_instability`

在盲评估、由裁判支撑的盲评估或对抗性评估下，至少一个被追踪的家族不再保持干净。

### `route_confusion`

路由混淆矩阵显示兄弟技能之间存在路由窃取或误路由。

### `route_ambiguity`

路由混淆矩阵报告了在配置的边际警告阈值附近的歧义案例。

### `longer_without_gain`

候选在实质上比当前描述更长，但并未带来更好的路由结果。

### `promotion_ready`

候选通过了每一道晋升门，有资格进入审查与晋升。

## 用法

这些原因标签应当出现在以下位置：

- 晋升决策
- 迭代包
- 回归历史
- 人工审查摘要

它们旨在让迭代可被审计，而不仅仅是可被描述。