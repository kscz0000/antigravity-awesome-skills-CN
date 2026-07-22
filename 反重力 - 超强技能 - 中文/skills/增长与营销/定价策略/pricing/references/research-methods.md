# 定价研究方法

## 目录
- Van Westendorp 价格敏感度测试（四个问题、分析方法、调研建议、示例输出）
- MaxDiff 分析（工作原理、示例调研问题、结果分析、用 MaxDiff 指导打包）
- 支付意愿调研
- 使用-价值关联分析

## Van Westendorp 价格敏感度测试

Van Westendorp 调研用于识别产品的可接受价格范围。

### 四个问题

向每位受访者提问：
1. "在什么价格下，你会认为 [产品] 太贵以至于不会考虑购买？"（太贵）
2. "在什么价格下，你会认为 [产品] 定价太低以至于会质疑其质量？"（太便宜）
3. "在什么价格下，你会认为 [产品] 开始变贵，但仍可能考虑？"（偏贵/高端）
4. "在什么价格下，你会认为 [产品] 很划算——物超所值？"（便宜/高性价比）

### 分析方法

1. 绘制每个问题的累积分布
2. 找到交叉点：
   - **边际便宜点（PMC）：** "太便宜"与"偏贵"的交叉
   - **边际昂贵点（PME）：** "太贵"与"便宜"的交叉
   - **最优价格点（OPP）：** "太便宜"与"太贵"的交叉
   - **无差异价格点（IDP）：** "偏贵"与"便宜"的交叉

**可接受价格范围：** PMC 到 PME
**最优定价区间：** OPP 与 IDP 之间

### 调研建议
- 需要 100-300 名受访者以获得可靠数据
- 按画像分段（不同的支付意愿）
- 使用真实的产品描述
- 考虑添加购买意向问题

### 示例输出

```
Price Sensitivity Analysis Results:
─────────────────────────────────
Point of Marginal Cheapness:  $29/mo
Optimal Price Point:          $49/mo
Indifference Price Point:     $59/mo
Point of Marginal Expensiveness: $79/mo

Recommended range: $49-59/mo
Current price: $39/mo (below optimal)
Opportunity: 25-50% price increase without significant demand impact
```

---

## MaxDiff 分析（最佳-最差缩放法）

MaxDiff 识别客户最看重哪些功能，指导打包决策。

### 工作原理

1. 列出 8-15 个可包含的功能
2. 每次向受访者展示 4-5 个功能的组合
3. 问："哪个最重要？哪个最不重要？"
4. 在多个组合中重复，直到所有功能都比较完毕
5. 统计分析生成重要性评分

### 示例调研问题

```
Which feature is MOST important to you?
Which feature is LEAST important to you?

□ Unlimited projects
□ Custom branding
□ Priority support
□ API access
□ Advanced analytics
```

### 结果分析

功能按效用分数排名：
- 高效用 = 必需功能（包含在基础层级）
- 中效用 = 差异化功能（用于层级区分）
- 低效用 = 锦上添花（高级层级或砍掉）

### 用 MaxDiff 指导打包

| 效用分数 | 打包决策 |
|---------|---------|
| 前 20% | 包含在所有层级（基本要求） |
| 20-50% | 用于区分层级 |
| 50-80% | 仅限更高层级 |
| 后 20% | 考虑砍掉或作为高级附加功能 |

---

## 支付意愿调研

**直接方法（简单但有偏差）：**
"你愿意为 [产品] 支付多少？"

**更好的方法：Gabor-Granger 方法：**
"你愿意以 [$X] 购买 [产品] 吗？"（是/否）
在不同受访者中变换价格，构建需求曲线。

**更优方法：Conjoint 分析：**
展示不同价格的产品组合
受访者选择偏好的选项
统计分析揭示每个功能的价格敏感度

---

## 使用-价值关联分析

### 1. 埋点使用数据
追踪客户如何使用你的产品：
- 功能使用频率
- 量级指标（用户数、记录数、API 调用数）
- 结果指标（产生的收入、节省的时间）

### 2. 与客户成功关联
- 哪些使用模式预测留存？
- 哪些使用模式预测扩展？
- 哪些客户付费最多，为什么？

### 3. 识别价值阈值
- 在什么使用水平客户"真正上手"？
- 在什么使用水平他们会扩展？
- 在什么使用水平应该涨价？

### 示例分析

```
Usage-Value Correlation Analysis:
─────────────────────────────────
Segment: High-LTV customers (>$10k ARR)
Average monthly active users: 15
Average projects: 8
Average integrations: 4

Segment: Churned customers
Average monthly active users: 3
Average projects: 2
Average integrations: 0

Insight: Value correlates with team adoption (users)
        and depth of use (integrations)

Recommendation: Price per user, gate integrations to higher tiers
```
