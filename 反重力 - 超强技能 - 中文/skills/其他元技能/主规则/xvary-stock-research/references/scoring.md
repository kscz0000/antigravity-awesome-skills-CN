# XVARY 评分（公开定义）

本文件定义了本技能使用的**公开**评分框架。

重要提示：XVARY 生产系统使用的是专有校准。下方公式仅展示逻辑形态，并不暴露私有的阈值表。

## 评分量表

所有评分均归一化为 `0-100` 区间。

- `80-100`：强
- `60-79`：偏多
- `40-59`：中性偏混合
- `0-39`：弱

## 输入

数据来源：

- `tools/edgar.py`（申报文件 + 财务数据）
- `tools/market.py`（价格 + 估值上下文）

本公开技能优先采用可获取的最新年度与季度数据。

## 1) 动量评分

衡量基本面与市场行为的向前驱动力。

公开公式形态：

`Momentum = 100 * (w1*Growth + w2*Revision + w3*RelativeStrength + w4*OperatingLeverage)`

各因子定义（归一化到 `0-1` 区间）：

- `Growth`：营收/EPS 增长的持续性
- `Revision`：市场预期/估计的修正方向
- `RelativeStrength`：近期的相对价格表现
- `OperatingLeverage`：增长带来的增量利润转化能力

## 2) 稳定性评分

衡量持久性与方差控制能力。

公开公式形态：

`Stability = 100 * (w1*MarginStability + w2*CashFlowStability + w3*CyclicalityBuffer + w4*ExecutionConsistency)`

各因子：

- `MarginStability`：毛利/营业利润率的波动性
- `CashFlowStability`：经营性现金流的稳定程度
- `CyclicalityBuffer`：对外部需求冲击的敏感度
- `ExecutionConsistency`：业绩超预期/不及预期以及指引可靠性的趋势

## 3) 财务健康度评分

衡量偿付能力质量与资产负债表的抗压能力。

公开公式形态：

`FinancialHealth = 100 * (w1*Liquidity + w2*Leverage + w3*Coverage + w4*CashConversion)`

各因子：

- `Liquidity`：现金 + 短期财务灵活性
- `Leverage`：相对盈利能力的债务负担
- `Coverage`：偿债能力（debt service coverage）的强度
- `CashConversion`：利润到现金的实现质量

## 4) 上行空间评分

衡量风险-收益不对称性相对于市场隐含预期的情况。

公开公式形态：

`Upside = 100 * (w1*IntrinsicGap + w2*ScenarioAsymmetry + w3*CatalystDensity + w4*ExpectationMispricing)`

各因子：

- `IntrinsicGap`：保守估值区间与当前价格的差距
- `ScenarioAsymmetry`：上行/下行情景分布的质量
- `CatalystDensity`：近期催化剂的数量与质量
- `ExpectationMispricing`：市场一致预期与论点路径之间的错位

## 综合视图（可选）

部分输出会使用一个可选的综合评分：

`Composite = a*Momentum + b*Stability + c*FinancialHealth + d*Upside`

在生产环境中，权重可按行业/商业模式灵活配置。

## 置信度标注

每个评分可附带基于证据深度的置信度标签：

- `High`：多源证据充分、内部矛盾较少
- `Medium`：证据充足、但仍存在部分开放性假设
- `Low`：数据稀疏或存在未解决的矛盾

## 与失效条件的耦合

评分永远不脱离失效条件单独成立。

一旦任意已列出的失效条件被触发，无论评分高低，都应对论点进行重新承销（re-underwrite）。

## 公开文档中未包含的内容

- 生产环境的权重值（`w1..w4`、`a..d`）
- 阈值切分点与特定市场环境下的覆盖规则
- 在数据稀疏/矛盾时的内部回退逻辑
