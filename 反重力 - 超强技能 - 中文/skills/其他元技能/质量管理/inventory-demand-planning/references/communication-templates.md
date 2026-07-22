# 库存需求规划 — 沟通模板参考

> 第 3 层参考。按需加载，用于需要针对常见需求规划场景的即用型沟通模板时。

---

## 如何使用本文件

当你需要与供应商、内部利益相关者或门店运营沟通需求规划决策时，找到匹配场景的模板，替换方括号变量，并根据语气校准指南调整语气。每个模板都包含目的、语气、关键收件人和发送前检查清单。

---

### 语气校准指南

| 收件人 | 语气 | 重点 | 避免 |
|---|---|---|---|
| 供应商（常规） | 事务性、简短 | PO 编号、日期、数量 | 解释、理由 |
| 供应商（升级） | 坚定、基于事实 | 业务影响、截止日期 | 情绪化语言、空洞威胁 |
| 商品部 | 数据驱动、以利润为中心 | 销售率、利润影响 | 指责（"我们买多了"） |
| 门店运营 | 可操作、简单 | 具体行动、截止日期 | 规划术语、公式 |
| 高管层 | 简洁、以风险为中心 | 财务影响、决策 | 运营细节 |
| 财务部 | 精确、可审计 | 数字、假设 | 模糊估计 |

---

### 模板 1：供应商常规补货订单

**目的：** 向供应商下达标准补货订单。

**语气：** 事务性、简短

**主题行：** PO #[PO_NUMBER] — [SUPPLIER_NAME] 补货订单

---

致 [SUPPLIER_CONTACT]，

请处理以下采购订单：

**PO 编号：** [PO_NUMBER]
**下单日期：** [ORDER_DATE]
**要求交货日期：** [DELIVERY_DATE]
**交货地点：** [DC_ADDRESS]

| 行号 | SKU | 描述 | 数量 | 单位成本 | 小计 |
|---|---|---|---|---|---|
| 1 | [SKU_1] | [DESC_1] | [QTY_1] | [COST_1] | [SUBTOTAL_1] |
| 2 | [SKU_2] | [DESC_2] | [QTY_2] | [COST_2] | [SUBTOTAL_2] |

**订单总计：** [TOTAL_AMOUNT]

请于 [CONFIRMATION_DEADLINE] 前确认收到并确认交货日期。

如有任何问题，请联系 [PLANNER_NAME]，电话 [PHONE] 或邮箱 [EMAIL]。

---

**发送前检查清单：**
- [ ] PO 编号唯一且顺序正确
- [ ] 数量是箱规倍数
- [ ] 交货日期考虑了提前期 + 缓冲
- [ ] 交货地点与供应商协议匹配
- [ ] 金额与商定定价一致

---

### 模板 2：供应商提前期升级

**目的：** 当供应商提前期增加影响服务水平时升级。

**语气：** 坚定、基于事实、量化业务影响

**主题行：** 紧急：提前期增加影响 — [SUPPLIER_NAME] — [CATEGORY]

---

致 [SUPPLIER_CONTACT]，

抄送：[INTERNAL_SUPPLY_CHAIN_DIRECTOR]

我们注意到 [SUPPLIER_NAME] 的提前期已从 [OLD_LT] 天增加至 [NEW_LT] 天，自 [EFFECTIVE_DATE] 起生效。

**业务影响：**
- 受影响 SKU：[AFFECTED_SKU_COUNT] 个 SKU
- 当前在库库存将维持约 [WEEKS_OF_SUPPLY] 周供应
- 按新提前期，我们预计约 [ESTIMATED_OOS_DATE] 出现缺货
- 预估损失收入：[LOST_REVENUE_ESTIMATE]
- 受影响门店：[AFFECTED_STORE_COUNT] 家

**我们请求：**
1. 确认新提前期是暂时的还是永久性的
2. 如可能，为 [AFFECTED_A_CLASS_SKUS] 个 A 类 SKU 提供加急装运
3. 在 [RESPONSE_DEADLINE] 前提供恢复原始提前期的时间线
4. 如有可用，提供替代装运方案（空运、分批装运）

**我们的应对措施：**
- 我们已重新计算安全库存和再订货点
- 我们正在认证该品类的二级供应商
- 我们已通知商品部服务水平可能暂时下降

请在 [RESPONSE_DEADLINE] 前回复并附上纠正方案。

---

**发送前检查清单：**
- [ ] 提前期变化已通过 PO 追踪或供应商通知确认
- [ ] 缺货日期基于当前库存位置和消耗率计算
- [ ] 损失收入估计有 POS 数据支持
- [ ] 内部利益相关者已在此邮件发送前得到通知
- [ ] 二级供应商认证已启动（即使尚未完成）

---

### 模板 3：内部缺货警报

**目的：** 通知内部利益相关者即将发生的缺货并建议行动。

**语气：** 紧急、可操作、包含预估风险收入

**主题行：** ⚠️ 缺货警报：[SKU_NAME] — 预计 [OOS_DATE] 缺货

---

致：[MERCHANDISING_LEAD], [STORE_OPS_LEAD]
抄送：[PLANNING_MANAGER], [CATEGORY_MANAGER]

**缺货摘要：**
- **SKU：** [SKU_NUMBER] — [SKU_NAME]
- **当前在库：** [ON_HAND_UNITS] 单位
- **当前在途：** [IN_TRANSIT_UNITS] 单位
- **日均消耗：** [DAILY_CONSUMPTION] 单位/天
- **预计缺货日期：** [OOS_DATE]
- **受影响门店：** [AFFECTED_STORE_COUNT] 家

**预估财务影响：**
- 日损失销售：[DAILY_LOST_SALES]
- 至补货的累计风险收入：[CUMULATIVE_RISK_REVENUE]

**建议行动（按优先级）：**

1. **加急补货：** [EXPEDITED_ORDER_DETAILS] — 预计 [EXPEDITED_DELIVERY_DATE] 到达
2. **门店重新分配：** 将库存从 [LOW_VELOCITY_STORES] 家低客流门店转移至 [HIGH_VELOCITY_STORES] 家高客流门店
3. **替代推荐：** 向缺货门店推荐 [ALTERNATE_SKU] 作为替代
4. **陈列调整：** 减少陈列面从 [CURRENT_FACING] 至 [REDUCED_FACING] 以减缓消耗

**需要决策：** 请在今天 [DECISION_DEADLINE] 前批准行动 #1 和/或 #2。

---

**发送前检查清单：**
- [ ] 缺货日期基于当前库存位置和消耗率计算
- [ ] 加急选项已与供应商确认（不仅是希望）
- [ ] 替代 SKU 已确认在库且可接受
- [ ] 门店重新分配在物流上可行（距离、运输）
- [ ] 累计风险收入计算合理

---

### 模板 4：向商品部建议降价

**目的：** 建议商品部对过剩库存进行降价。

**语气：** 数据驱动、以利润影响为中心

**主题行：** 降价建议：[CATEGORY_NAME] — [SKU_COUNT] 个 SKU

---

致：[MERCHANDISING_VP], [CATEGORY_MANAGER]

**建议摘要：**
我们建议对 [CATEGORY_NAME] 品类中 [SKU_COUNT] 个 SKU 实施降价，以在 [DEADLINE_DATE] 前改善库存位置。

**当前状况：**

| SKU | 当前供应周数 | 近 4 周速度 | 速度 vs 计划 | 建议折扣 |
|---|---|---|---|---|
| [SKU_1] | [WOS_1] | [VELOCITY_1] | [VS_PLAN_1]% | [DISCOUNT_1]% |
| [SKU_2] | [WOS_2] | [VELOCITY_2] | [VS_PLAN_2]% | [DISCOUNT_2]% |

**利润影响分析：**

| 场景 | 预计回收率 | 预计利润损失 | 剩余库存风险 |
|---|---|---|---|
| 维持当前价格 | [RECOVERY_CURRENT]% | [LOSS_CURRENT] | [RISK_CURRENT] |
| 建议降价 | [RECOVERY_PROPOSED]% | [LOSS_PROPOSED] | [RISK_PROPOSED] |
| 更深降价 ([DEEPER_DISCOUNT]%) | [RECOVERY_DEEPER]% | [LOSS_DEEPER] | [RISK_DEEPER] |

**我们的建议：** 建议降价方案。在建议折扣下，我们预计 [EXPECTED_SELL_THROUGH]% 的清仓率，剩余库存 [REMAINING_UNITS] 单位于 [CLEARANCE_DATE] 进入清仓渠道。

**时间敏感性：** 每延迟一周降价启动，剩余库存利润率损失约 [MARGIN_LOSS_PER_WEEK] 个百分点。

请于 [DECISION_DEADLINE] 前批准或建议替代方案。

---

**发送前检查清单：**
- [ ] 供应周数基于当前速度计算（非计划速度）
- [ ] 利润影响分析包含持有成本
- [ ] 清仓渠道已确认可用（非假设）
- [ ] 每周利润率损失基于品类历史降价数据
- [ ] 表述为"销售率需要价格行动"而非"我们买多了"

---

### 模板 5：促销预测提交

**目的：** 向利益相关者提交促销预测供审查和承诺。

**语气：** 结构化、透明、包含假设和置信区间

**主题行：** 促销预测：[PROMO_NAME] — [START_DATE] 至 [END_DATE]

---

致：[MERCHANDISING_LEAD], [SUPPLY_CHAIN_LEAD]
抄送：[CATEGORY_MANAGER], [STORE_OPS_LEAD]

**促销详情：**
- **促销名称：** [PROMO_NAME]
- **日期：** [START_DATE] 至 [END_DATE]（[PROMO_WEEKS] 周）
- **促销类型：** [PROMO_TYPE]（TPR / 陈列 + TPR / 端头 + TPR + 传单特写）
- **折扣深度：** [DISCOUNT_DEPTH]% off
- **参与门店：** [PARTICIPATING_STORES] 家

**预测明细：**

| 指标 | 促销前基线 | 促销提升 | 促销期预测 | 促销后低谷 |
|---|---|---|---|---|
| 周度需求（单位） | [BASELINE_UNITS] | +[LIFT_PCT]% | [PROMO_UNITS] | −[TROUGH_PCT]% |
| 周度收入 | [BASELINE_REVENUE] | +[LIFT_REVENUE] | [PROMO_REVENUE] | [TROUGH_REVENUE] |

**提升预估方法：** [METHOD_USED]
- 数据来源：[DATA_SOURCE]（自有历史 / 类比商品 / 品类平均）
- 历史促销参考：[HISTORICAL_PROMOS_REFERENCED]
- 应用的调整：[ADJUSTMENTS_APPLIED]

**假设：**
1. [ASSUMPTION_1]
2. [ASSUMPTION_2]
3. [ASSUMPTION_3]

**置信区间：** ±[CONFIDENCE_PCT]%

**库存影响：**
- 促销前建库需求：[BUILDUP_UNITS] 单位
- 促销后过剩风险：[OVERSTOCK_RISK] 单位
- 建议安全库存调整：[SS_ADJUSTMENT]

**所需行动：**
- [ ] 商品部：确认促销条款和参与门店
- [ ] 供应链：确认建库 PO 交货日期
- [ ] 门店运营：确认陈列和传单执行时间线

请于 [COMMITMENT_DEADLINE] 前审查并承诺。

---

**发送前检查清单：**
- [ ] 提升预估基于数据（非猜测），方法已说明
- [ ] 促销后低谷已建模（非忽略）
- [ ] 置信区间反映实际不确定性
- [ ] 建库 PO 已下达或准备下达
- [ ] 蚕食效应对同品类近似替代品已建模

---

### 模板 6：新品预测假设文档

**目的：** 记录新品预测的假设，以便复盘时审计。

**语气：** 明确、可审计、列出每个假设

**主题行：** 新品预测假设：[PRODUCT_NAME] — 上市日期 [LAUNCH_DATE]

---

**产品信息：**
- **产品名称：** [PRODUCT_NAME]
- **SKU：** [SKU_NUMBER]
- **品类：** [CATEGORY]
- **零售价：** [RETAIL_PRICE]
- **供应商成本：** [COST_PRICE]
- **箱规：** [CASE_PACK]
- **保质期：** [SHELF_LIFE]
- **上市日期：** [LAUNCH_DATE]
- **分销门店：** [STORE_COUNT] 家

**预测方法：** 类比商品画像

**类比商品选择：**

| 类比商品 | 品类匹配 | 价位带 | 品牌层级 | 加权得分 | 上市速度（单位/门店/周） |
|---|---|---|---|---|---|
| [ANALOG_1] | [SCORE_1] | [PRICE_1] | [TIER_1] | [WEIGHTED_1] | [VELOCITY_1] |
| [ANALOG_2] | [SCORE_2] | [PRICE_2] | [TIER_2] | [WEIGHTED_2] | [VELOCITY_2] |
| [ANALOG_3] | [SCORE_3] | [PRICE_3] | [TIER_3] | [WEIGHTED_3] | [VELOCITY_3] |

**加权中位速度：** [MEDIAN_VELOCITY] 单位/门店/周

**预测情景：**

| 周 | 保守（单位/周） | 基准（单位/周） | 乐观（单位/周） |
|---|---|---|---|
| 1–4 | [CONSERVATIVE_W1_4] | [BASELINE_W1_4] | [OPTIMISTIC_W1_4] |
| 5–8 | [CONSERVATIVE_W5_8] | [BASELINE_W5_8] | [OPTIMISTIC_W5_8] |
| 9–13 | [CONSERVATIVE_W9_13] | [BASELINE_W9_13] | [OPTIMISTIC_W9_13] |

**关键假设：**
1. 分销至 [STORE_COUNT] 家门店，[LAUNCH_DATE] 全部完成
2. 价位 [RETAIL_PRICE] 与类比商品价位带一致
3. 上市期间无竞争性促销活动
4. 促销支持：[PROMO_SUPPORT_DESCRIPTION]
5. 陈列位置：[DISPLAY_COMMITMENT]

**初始采购决策：**
- 订单数量：[ORDER_QUANTITY] 单位
- 方法：基准情景第 1–8 周 + 保守率安全库存
- 供应商 MOQ：[MOQ] — [MOQ_STATUS]（已满足 / 需要谈判）
- 预计到货日期：[DELIVERY_DATE]

**监控触发器：**
- 第 1 周速度 > [TRIGGER_HIGH] → 升级至乐观情景
- 第 2 周速度 < [TRIGGER_LOW] → 标记审查
- 第 3 周检查点与商品部

**文档准备人：** [PLANNER_NAME]
**日期：** [DOCUMENT_DATE]
**审查日期：** [REVIEW_DATE]（上市后第 3 周）

---

**发送前检查清单：**
- [ ] 类比商品选择有评分理由支持
- [ ] 三种情景覆盖合理范围
- [ ] 每个假设都是可证伪的（复盘时可验证为真或假）
- [ ] 初始采购与基准情景一致（非乐观情景）
- [ ] 监控触发器有具体阈值和行动

---

### 模板 7：供应商季度业务审查 (QBR) 准备

**目的：** 为供应商 QBR 准备需求规划视角。

**语气：** 专业、数据丰富、建设性

**QBR 议程 — 需求规划部分（20 分钟）：**

---

**1. 预测准确度回顾（5 分钟）**

| 指标 | Q3 实际 | Q4 实际 | 趋势 |
|---|---|---|---|
| WMAPE | [Q3_WMAPE] | [Q4_WMAPE] | ↑↓→ |
| 预测偏差 | [Q3_BIAS] | [Q4_BIAS] | ↑↓→ |
| 追踪信号违规 | [Q3_TS] | [Q4_TS] | ↑↓→ |

**关键发现：**
- [FINDING_1]
- [FINDING_2]

**2. 服务水平回顾（5 分钟）**

| 指标 | Q3 实际 | Q4 实际 | 目标 |
|---|---|---|---|
| 在架率 | [Q3_AVAIL] | [Q4_AVAIL] | [TARGET_AVAIL] |
| PO 准时交付率 | [Q3_OTIF] | [Q4_OTIF] | [TARGET_OTIF] |
| PO 完整交付率 | [Q3_FILL] | [Q4_FILL] | [TARGET_FILL] |

**缺货事件：**
- [OOS_EVENT_1]：[ROOT_CAUSE] — [CORRECTIVE_ACTION]
- [OOS_EVENT_2]：[ROOT_CAUSE] — [CORRECTIVE_ACTION]

**3. 库存健康（5 分钟）**

| 指标 | 当前 | 目标 | 状态 |
|---|---|---|---|
| 供应周数 | [CURRENT_WOS] | [TARGET_WOS] | ✅⚠️❌ |
| 过剩库存（>26 周） | [EXCESS_UNITS] | <[TARGET] | ✅⚠️❌ |
| 死库存 | [DEAD_UNITS] | <[TARGET] | ✅⚠️❌ |

**4. 行动项和请求（5 分钟）**

| # | 行动项 | 负责方 | 截止日期 |
|---|---|---|---|
| 1 | [ACTION_1] | [OWNER_1] | [DEADLINE_1] |
| 2 | [ACTION_2] | [OWNER_2] | [DEADLINE_2] |
| 3 | [ACTION_3] | [OWNER_3] | [DEADLINE_3] |

**供应商请求：**
1. [REQUEST_1]
2. [REQUEST_2]

**我方承诺：**
1. [COMMITMENT_1]
2. [COMMITMENT_2]

---

**发送前检查清单：**
- [ ] 所有指标基于可审计数据（非估计）
- [ ] 缺货根因分析完成（非仅列举事件）
- [ ] 供应商请求具体且可操作
- [ ] 我方承诺可交付
- [ ] 行动项有明确负责方和截止日期

---

### 模板 8：门店运营 — 分配变更通知

**目的：** 通知门店运营库存分配变更。

**语气：** 可操作、简单、无规划术语

**主题行：** 分配变更：[PRODUCT_NAME] — [EFFECTIVE_DATE] 起

---

致：[STORE_OPS_MANAGERS]

**变更摘要：**
由于 [REASON_BRIEF]，[PRODUCT_NAME]（SKU [SKU_NUMBER]）的分配将从 [EFFECTIVE_DATE] 起调整。

**新分配：**

| 门店层级 | 原分配 | 新分配 | 变更 |
|---|---|---|---|
| [TIER_1_NAME]（[TIER_1_COUNT] 家门店） | [OLD_ALLOC_1] 单位/周 | [NEW_ALLOC_1] 单位/周 | [CHANGE_1] |
| [TIER_2_NAME]（[TIER_2_COUNT] 家门店） | [OLD_ALLOC_2] 单位/周 | [NEW_ALLOC_2] 单位/周 | [CHANGE_2] |
| [TIER_3_NAME]（[TIER_3_COUNT] 家门店） | [OLD_ALLOC_3] 单位/周 | [NEW_ALLOC_3] 单位/周 | [CHANGE_3] |

**门店行动：**
1. 每笔交易实施 [MAX_PURCHASE] 单位购买限制
2. 如缺货，展示替代标牌："寻找 [PRODUCT_NAME]？试试 [ALTERNATE_PRODUCT]"
3. 不要在 POS 系统中创建补货请求——分配由配送中心管理

**预期持续时间：** [EXPECTED_DURATION] 周（预计 [RECOVERY_DATE] 恢复正常分配）

**问题？** 联系 [PLANNER_NAME]，[PHONE]，[EMAIL]

---

**发送前检查清单：**
- [ ] 分配变更已与配送中心能力确认
- [ ] 购买限制可在 POS 系统中实施
- [ ] 替代产品在库
- [ ] 恢复日期基于供应商确认（非猜测）
- [ ] 门店层级分配已按速度排名计算

---

### 模板 9：高管层 — 供应风险简报

**目的：** 向高管层简报重大供应风险及建议应对措施。

**语气：** 简洁、以风险为中心、可决策

**主题行：** 供应风险简报：[RISK_DESCRIPTION]

---

**风险摘要（2 句话）：**
[RISK_SUMMARY]

**财务影响：**
- 风险收入：[AT_RISK_REVENUE]
- 预计利润影响：[PROFIT_IMPACT]
- 受影响品类：[AFFECTED_CATEGORIES]
- 受影响门店：[AFFECTED_STORES]

**当前状况：**
- [SITUATION_FACT_1]
- [SITUATION_FACT_2]
- [SITUATION_FACT_3]

**建议应对措施（按优先级）：**

| # | 行动 | 成本 | 预期缓解 | 时间线 |
|---|---|---|---|---|
| 1 | [ACTION_1] | [COST_1] | [MITIGATION_1] | [TIMELINE_1] |
| 2 | [ACTION_2] | [COST_2] | [MITIGATION_2] | [TIMELINE_2] |
| 3 | [ACTION_3] | [COST_3] | [MITIGATION_3] | [TIMELINE_3] |

**需要决策：** [DECISION_REQUIRED] — 请于 [DECISION_DEADLINE] 前批准或指示替代方案。

**下一步：** 如获批准，[PLANNER_NAME] 将在 [EXECUTION_DATE] 前执行行动 #1。

---

**发送前检查清单：**
- [ ] 财务影响基于数据（非最坏情况猜测）
- [ ] 建议行动具体且可执行（非模糊建议）
- [ ] 每项行动的成本已估算
- [ ] 决策请求明确且有时间限制
- [ ] 简报不超过 1 页

---

### 模板 10：促销后复盘

**目的：** 促销后记录实际 vs 预测结果以改进未来预估。

**语气：** 分析性、无指责、以学习为导向

**促销复盘：[PROMO_NAME]**

---

**促销摘要：**
- **日期：** [START_DATE] 至 [END_DATE]
- **类型：** [PROMO_TYPE]
- **折扣深度：** [DISCOUNT_DEPTH]%
- **参与门店：** [PARTICIPATING_STORES]

**预测 vs 实际：**

| 指标 | 预测 | 实际 | 偏差 |
|---|---|---|---|
| 促销期总销量 | [FORECAST_UNITS] | [ACTUAL_UNITS] | [VARIANCE]% |
| 提升率 | [FORECAST_LIFT]% | [ACTUAL_LIFT]% | [LIFT_VARIANCE] |
| 促销后低谷 | [FORECAST_TROUGH]% | [ACTUAL_TROUGH]% | [TROUGH_VARIANCE] |
| 促销期收入 | [FORECAST_REVENUE] | [ACTUAL_REVENUE] | [REV_VARIANCE]% |
| 促销期利润 | [FORECAST_MARGIN] | [ACTUAL_MARGIN] | [MARGIN_VARIANCE]% |

**提升预估方法：** [METHOD_USED]
**方法准确度：** [METHOD_ACCURACY]（好/可接受/差）

**哪些对了：**
- [WHAT_WORKED_1]
- [WHAT_WORKED_2]

**哪些错了：**
- [WHAT_MISSED_1] — 根因：[ROOT_CAUSE_1]
- [WHAT_MISSED_2] — 根因：[ROOT_CAUSE_2]

**下次改进：**
1. [IMPROVEMENT_1]
2. [IMPROVEMENT_2]

**蚕食效应观察：**
- [CANNIBALIZED_SKU_1]：促销期间速度下降 [CANNIBALIZATION_1]%
- [CANNIBALIZED_SKU_2]：促销期间速度下降 [CANNIBALIZATION_2]%

**库存影响：**
- 促销后过剩：[OVERSTOCK_UNITS] 单位（[OVERSTOCK_WOS] 周供应）
- 所需降价：[MARKDOWN_NEEDED]（是/否）
- 降价成本：[MARKDOWN_COST]

**存档用于未来参考：** 此复盘将用于校准 [CATEGORY] 品类未来促销的提升预估。

---

**发送前检查清单：**
- [ ] 实际数据完整（非部分周）
- [ ] 偏差计算一致（(实际 − 预测) / 预测）
- [ ] 根因分析具体（非"市场条件"）
- [ ] 改进行动可执行（非"做得更好"）
- [ ] 蚕食效应对近似替代品已量化
- [ ] 复盘已归档至促销历史数据库
