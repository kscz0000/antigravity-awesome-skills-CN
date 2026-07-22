# 创业指标框架实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# 创业指标框架

从种子轮到A轮，针对不同创业商业模式，系统追踪、计算和优化关键绩效指标的完整指南。

## 概览

在正确的阶段追踪正确的指标。聚焦对融资和运营卓越至关重要的单位经济、增长效率和现金管理指标。

## 通用创业指标

### 收入指标

**MRR（月度经常性收入）**
```
MRR = Σ (Active Subscriptions × Monthly Price)
```

**ARR（年度经常性收入）**
```
ARR = MRR × 12
```

**增长率**
```
MoM Growth = (This Month MRR - Last Month MRR) / Last Month MRR
YoY Growth = (This Year ARR - Last Year ARR) / Last Year ARR
```

**目标基准：**
- 种子阶段：15-20% 月环比增长
- A轮：10-15% 月环比增长，3-5倍年同比增长
- B轮+：100%+ 年同比增长（Rule of 40）

### 单位经济

**CAC（客户获取成本）**
```
CAC = Total S&M Spend / New Customers Acquired
```

包括：销售人员薪资、营销支出、工具、运营开销

**LTV（客户生命周期价值）**
```
LTV = ARPU × Gross Margin% × (1 / Churn Rate)
```

简化版：
```
LTV = ARPU × Average Customer Lifetime × Gross Margin%
```

**LTV:CAC 比率**
```
LTV:CAC = LTV / CAC
```

**基准：**
- LTV:CAC > 3.0 = 健康
- LTV:CAC 1.0-3.0 = 需要改善
- LTV:CAC < 1.0 = 不可持续

**CAC 回收期**
```
CAC Payback = CAC / (ARPU × Gross Margin%)
```

**基准：**
- < 12个月 = 优秀
- 12-18个月 = 良好
- > 24个月 = 需要关注

### 现金效率指标

**Burn Rate（烧钱速率）**
```
Monthly Burn = Monthly Revenue - Monthly Expenses
```

负值 = 亏损（早期阶段常见）

**Runway（资金跑道）**
```
Runway (months) = Cash Balance / Monthly Burn Rate
```

**目标：** 始终保持 12-18 个月的资金跑道

**Burn Multiple（烧钱倍数）**
```
Burn Multiple = Net Burn / Net New ARR
```

**基准：**
- < 1.0 = 卓越效率
- 1.0-1.5 = 良好
- 1.5-2.0 = 可接受
- > 2.0 = 效率低下

越低越好（用更少的花费产生更多 ARR）

## SaaS 指标

### 收入构成

**New MRR（新增 MRR）**
新客户 × ARPU

**Expansion MRR（扩展 MRR）**
来自现有客户的增购和交叉销售

**Contraction MRR（收缩 MRR）**
现有客户的降级

**Churned MRR（流失 MRR）**
流失客户

**净新增 MRR 公式：**
```
Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR
```

### 留存指标

**Logo Retention（客户数留存）**
```
Logo Retention = (Customers End - New Customers) / Customers Start
```

**Dollar Retention（NDR - 净收入留存率）**
```
NDR = (ARR Start + Expansion - Contraction - Churn) / ARR Start
```

**基准：**
- NDR > 120% = 业界顶级
- NDR 100-120% = 良好
- NDR < 100% = 需要改善

**Gross Retention（毛留存率）**
```
Gross Retention = (ARR Start - Churn - Contraction) / ARR Start
```

**基准：**
- > 90% = 优秀
- 85-90% = 良好
- < 85% = 需要关注

### SaaS 专项指标

**Magic Number（魔力数字）**
```
Magic Number = Net New ARR (quarter) / S&M Spend (prior quarter)
```

**基准：**
- > 0.75 = 高效，准备规模化
- 0.5-0.75 = 中等效率
- < 0.5 = 低效，暂不扩张

**Rule of 40（40法则）**
```
Rule of 40 = Revenue Growth Rate% + Profit Margin%
```

**基准：**
- > 40% = 优秀
- 20-40% = 可接受
- < 20% = 需要改善

**示例：**
50% 增长 + (10%) 利润率 = 40% ✓

**Quick Ratio（速动比率）**
```
Quick Ratio = (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)
```

**基准：**
- > 4.0 = 健康增长
- 2.0-4.0 = 中等
- < 2.0 = 存在流失问题

## 市场平台指标

### GMV（总交易额）

**总交易量：**
```
GMV = Σ (Transaction Value)
```

**增长率：**
```
GMV Growth Rate = (Current Period GMV - Prior Period GMV) / Prior Period GMV
```

**目标：** 早期阶段月环比 20%+

### Take Rate（抽佣率）

```
Take Rate = Net Revenue / GMV
```

**典型范围：**
- 支付处理商：2-3%
- 电商平台：10-20%
- 服务平台：15-25%
- 高价值 B2B：5-15%

### 市场流动性

**交易达成时间**
从上架到成交/匹配需要多长时间？

**成交率**
请求转化为交易的百分比

**复购率**
多次交易的用户百分比

**基准：**
- 成交率 > 80% = 强流动性
- 复购率 > 60% = 强留存

### 市场平衡

**供需比率：**
追踪供需双方的相对增长。

**警示信号：**
- 供给过剩：成交率低，供应商受挫
- 需求过剩：等待时间长，客户受挫

**目标：** 均衡增长（1:1 比率理想，但因模式而异）

## 消费者/移动端指标

### 参与指标

**DAU（日活跃用户）**
每日活跃的独立用户数

**MAU（月活跃用户）**
每月活跃的独立用户数

**DAU/MAU 比率**
```
DAU/MAU = DAU / MAU
```

**基准：**
- > 50% = 卓越（日常习惯级）
- 20-50% = 良好
- < 20% = 参与度弱

**会话频率**
每用户每天/每周的平均会话数

**会话时长**
每次会话的平均时长

### 留存曲线

**次日留存：** 次日返回的用户百分比
**7日留存：** 注册7天后仍活跃的用户百分比
**30日留存：** 注册30天后仍活跃的用户百分比

**基准（30日）：**
- > 40% = 优秀
- 25-40% = 良好
- < 25% = 偏弱

**留存曲线形态：**
- 趋于平缓 = 良好（用户形成习惯）
- 急剧下降 = 产品市场匹配度差

### 病毒系数（K-Factor）

```
K-Factor = Invites per User × Invite Conversion Rate
```

**示例：**
10 次邀请/用户 × 20% 转化率 = 2.0 K-factor

**基准：**
- K > 1.0 = 病毒式增长
- K = 0.5-1.0 = 强推荐
- K < 0.5 = 病毒性弱

## B2B 指标

### 销售效率

**Win Rate（赢单率）**
```
Win Rate = Deals Won / Total Opportunities
```

**目标：** 新销售团队 20-30%，成熟团队 30-40%

**Sales Cycle Length（销售周期）**
从线索到成交的平均天数

**越短越好：**
- 中小企业：30-60天
- 中端市场：60-120天
- 企业级：120-270天

**ACV（平均合同价值）**
```
ACV = Total Contract Value / Contract Length (years)
```

### Pipeline 指标

**Pipeline Coverage（管线覆盖率）**
```
Pipeline Coverage = Total Pipeline Value / Quota
```

**目标：** 3-5倍覆盖率（需要3-5倍管线来完成配额）

**各阶段转化率：**
- Lead → Opportunity：10-20%
- Opportunity → Demo：50-70%
- Demo → Proposal：30-50%
- Proposal → Close：20-40%

## 按阶段划分的指标

### Pre-Seed（产品市场匹配）

**重点关注指标：**
1. 活跃用户增长
2. 用户留存（7日、30日）
3. 核心参与度（会话数、功能使用）
4. 定性反馈（NPS、用户访谈）

**暂不关注：**
- 收入（可能为零）
- CAC（尚未优化）
- 单位经济

### Seed（$500K-$2M ARR）

**重点关注指标：**
1. MRR 增长率（月环比 15-20%）
2. CAC 和 LTV（建立基线）
3. 毛留存率（> 85%）
4. 核心产品参与度

**开始追踪：**
- 销售效率
- 烧钱速率和资金跑道

### Series A（$2M-$10M ARR）

**重点关注指标：**
1. ARR 增长（年同比 3-5倍）
2. 单位经济（LTV:CAC > 3，回收期 < 18个月）
3. 净收入留存率（> 100%）
4. 烧钱倍数（< 2.0）
5. 魔力数字（> 0.5）

**成熟追踪：**
- Rule of 40
- 销售效率
- Pipeline 覆盖率

## 指标追踪最佳实践

### 数据基础设施

**要求：**
- 单一数据源（分析平台）
- 实时或每日更新
- 自动化计算
- 历史追踪

**工具：**
- Mixpanel、Amplitude（产品分析）
- ChartMogul、Baremetrics（SaaS 指标）
- Looker、Tableau（BI 仪表盘）

### 汇报节奏

**每日：**
- MRR、活跃用户
- 注册量、转化率

**每周：**
- 增长率
- 留存队列
- 销售管线

**每月：**
- 完整指标套件
- 董事会报告
- 投资人更新

**每季度：**
- 趋势分析
- 基准对标
- 战略复盘

### 常见错误

**错误1：虚荣指标**
不要关注：
- 总用户数（不看留存）
- 页面浏览量（不看参与度）
- 下载量（不看激活率）

聚焦与价值挂钩的可行动指标。

**错误2：指标过多**
深度追踪 5-7 个核心指标，而非粗放追踪 50 个。

**错误3：忽视单位经济**
即使在种子阶段，CAC 和 LTV 也至关重要。

**错误4：不做分层分析**
按客户分层、渠道、队列拆解指标。

**错误5：刷指标**
为真正的业务成果优化，而非为仪表盘数字优化。

## 投资人关注的指标

### VC 想看什么

**种子轮：**
- MRR 增长率
- 用户留存
- 早期单位经济
- 产品参与度

**A轮：**
- ARR 和增长率
- CAC 回收期 < 18个月
- LTV:CAC > 3.0
- 净收入留存率 > 100%
- 烧钱倍数 < 2.0

**B轮+：**
- Rule of 40 > 40%
- 高效增长（魔力数字）
- 盈利路径
- 市场领导力指标

### 指标展示

**仪表盘格式：**
```
Current MRR: $250K (↑ 18% MoM)
ARR: $3.0M (↑ 280% YoY)
CAC: $1,200 | LTV: $4,800 | LTV:CAC = 4.0x
NDR: 112% | Logo Retention: 92%
Burn: $180K/mo | Runway: 18 months
```

**包含要素：**
- 当前值
- 增长率或趋势
- 背景（目标、基准）

## 补充资源

### 参考文件
- **`references/metric-definitions.md`** — 50+ 指标的完整定义和公式
- **`references/benchmarks-by-stage.md`** — 按公司阶段划分的各指标目标范围
- **`references/calculation-examples.md`** — 逐步计算示例

### 示例文件
- **`examples/saas-metrics-dashboard.md`** — B2B SaaS 公司的完整指标套件
- **`examples/marketplace-metrics.md`** — 市场平台专项指标及示例
- **`examples/investor-metrics-deck.md`** — 如何为融资展示指标

## 快速开始

实施创业指标框架：

1. **确定商业模式** — SaaS、市场平台、消费者、B2B
2. **选择 5-7 个核心指标** — 根据阶段和模式
3. **建立追踪体系** — 搭建分析平台和仪表盘
4. **计算单位经济** — CAC、LTV、回收期
5. **设定目标** — 以基准为参考
6. **定期复盘** — 核心指标每周回顾
7. **团队对齐** — 就目标和进展达成共识
8. **投资人汇报** — 月度/季度报告

详细定义、基准和示例，请参阅 `references/` 和 `examples/`。
