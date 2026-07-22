---
name: kpi-dashboard-design
description: "设计高效关键绩效指标（KPI）仪表盘的全面模式，驱动业务决策。触发词：KPI仪表盘、仪表盘设计、指标看板、dashboard设计、绩效看板、数据看板"
risk: unknown
source: community
date_added: "2026-02-27"
---

# KPI 仪表盘设计

设计高效关键绩效指标（KPI）仪表盘的全面模式，驱动业务决策。

## 不使用此技能的情况

- 任务与 KPI 仪表盘设计无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 使用此技能的情况

- 设计高管仪表盘
- 选择有意义的 KPI
- 构建实时监控面板
- 创建部门级指标视图
- 改进现有仪表盘布局
- 建立指标治理体系

## 核心概念

### 1. KPI 框架

| 层级 | 关注点 | 更新频率 | 受众 |
| --------------- | ---------------- | ----------------- | ---------- |
| **战略层** | 长期目标 | 月度/季度 | 高管 |
| **战术层** | 部门目标 | 周度/月度 | 管理者 |
| **运营层** | 日常运营 | 实时/每日 | 团队 |

### 2. SMART KPI

```
Specific: Clear definition
Measurable: Quantifiable
Achievable: Realistic targets
Relevant: Aligned to goals
Time-bound: Defined period
```

### 3. 仪表盘层级

```
├── Executive Summary (1 page)
│   ├── 4-6 headline KPIs
│   ├── Trend indicators
│   └── Key alerts
├── Department Views
│   ├── Sales Dashboard
│   ├── Marketing Dashboard
│   ├── Operations Dashboard
│   └── Finance Dashboard
└── Detailed Drilldowns
    ├── Individual metrics
    └── Root cause analysis
```

## 各部门常用 KPI

### 销售 KPI

```yaml
Revenue Metrics:
  - Monthly Recurring Revenue (MRR)
  - Annual Recurring Revenue (ARR)
  - Average Revenue Per User (ARPU)
  - Revenue Growth Rate

Pipeline Metrics:
  - Sales Pipeline Value
  - Win Rate
  - Average Deal Size
  - Sales Cycle Length

Activity Metrics:
  - Calls/Emails per Rep
  - Demos Scheduled
  - Proposals Sent
  - Close Rate
```

### 市场 KPI

```yaml
Acquisition:
  - Cost Per Acquisition (CPA)
  - Customer Acquisition Cost (CAC)
  - Lead Volume
  - Marketing Qualified Leads (MQL)

Engagement:
  - Website Traffic
  - Conversion Rate
  - Email Open/Click Rate
  - Social Engagement

ROI:
  - Marketing ROI
  - Campaign Performance
  - Channel Attribution
  - CAC Payback Period
```

### 产品 KPI

```yaml
Usage:
  - Daily/Monthly Active Users (DAU/MAU)
  - Session Duration
  - Feature Adoption Rate
  - Stickiness (DAU/MAU)

Quality:
  - Net Promoter Score (NPS)
  - Customer Satisfaction (CSAT)
  - Bug/Issue Count
  - Time to Resolution

Growth:
  - User Growth Rate
  - Activation Rate
  - Retention Rate
  - Churn Rate
```

### 财务 KPI

```yaml
Profitability:
  - Gross Margin
  - Net Profit Margin
  - EBITDA
  - Operating Margin

Liquidity:
  - Current Ratio
  - Quick Ratio
  - Cash Flow
  - Working Capital

Efficiency:
  - Revenue per Employee
  - Operating Expense Ratio
  - Days Sales Outstanding
  - Inventory Turnover
```

## 仪表盘布局模式

### 模式 1：高管摘要

```
┌─────────────────────────────────────────────────────────────┐
│  EXECUTIVE DASHBOARD                        [Date Range ▼]  │
├─────────────┬─────────────┬─────────────┬─────────────────┤
│   REVENUE   │   PROFIT    │  CUSTOMERS  │    NPS SCORE    │
│   $2.4M     │    $450K    │    12,450   │       72        │
│   ▲ 12%     │    ▲ 8%     │    ▲ 15%    │     ▲ 5pts     │
├─────────────┴─────────────┴─────────────┴─────────────────┤
│                                                             │
│  Revenue Trend                    │  Revenue by Product     │
│  ┌───────────────────────┐       │  ┌──────────────────┐   │
│  │    /\    /\          │       │  │ ████████ 45%     │   │
│  │   /  \  /  \    /\   │       │  │ ██████   32%     │   │
│  │  /    \/    \  /  \  │       │  │ ████     18%     │   │
│  │ /            \/    \ │       │  │ ██        5%     │   │
│  └───────────────────────┘       │  └──────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  🔴 Alert: Churn rate exceeded threshold (>5%)              │
│  🟡 Warning: Support ticket volume 20% above average        │
└─────────────────────────────────────────────────────────────┘
```

### 模式 2：SaaS 指标仪表盘

```
┌─────────────────────────────────────────────────────────────┐
│  SAAS METRICS                     Jan 2024  [Monthly ▼]     │
├──────────────────────┬──────────────────────────────────────┤
│  ┌────────────────┐  │  MRR GROWTH                          │
│  │      MRR       │  │  ┌────────────────────────────────┐  │
│  │    $125,000    │  │  │                          /──   │  │
│  │     ▲ 8%       │  │  │                    /────/      │  │
│  └────────────────┘  │  │              /────/            │  │
│  ┌────────────────┐  │  │        /────/                  │  │
│  │      ARR       │  │  │   /────/                       │  │
│  │   $1,500,000   │  │  └────────────────────────────────┘  │
│  │     ▲ 15%      │  │  J  F  M  A  M  J  J  A  S  O  N  D  │
│  └────────────────┘  │                                      │
├──────────────────────┼──────────────────────────────────────┤
│  UNIT ECONOMICS      │  COHORT RETENTION                    │
│                      │                                      │
│  CAC:     $450       │  Month 1: ████████████████████ 100%  │
│  LTV:     $2,700     │  Month 3: █████████████████    85%   │
│  LTV/CAC: 6.0x       │  Month 6: ████████████████     80%   │
│                      │  Month 12: ██████████████      72%   │
│  Payback: 4 months   │                                      │
├──────────────────────┴──────────────────────────────────────┤
│  CHURN ANALYSIS                                             │
│  ┌──────────┬──────────┬──────────┬──────────────────────┐ │
│  │ Gross    │ Net      │ Logo     │ Expansion            │ │
│  │ 4.2%     │ 1.8%     │ 3.1%     │ 2.4%                 │ │
│  └──────────┴──────────┴──────────┴──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 模式 3：实时运营

```
┌─────────────────────────────────────────────────────────────┐
│  OPERATIONS CENTER                    Live ● Last: 10:42:15 │
├────────────────────────────┬────────────────────────────────┤
│  SYSTEM HEALTH             │  SERVICE STATUS                │
│  ┌──────────────────────┐  │                                │
│  │   CPU    MEM    DISK │  │  ● API Gateway      Healthy    │
│  │   45%    72%    58%  │  │  ● User Service     Healthy    │
│  │   ███    ████   ███  │  │  ● Payment Service  Degraded   │
│  │   ███    ████   ███  │  │  ● Database         Healthy    │
│  │   ███    ████   ███  │  │  ● Cache            Healthy    │
│  └──────────────────────┘  │                                │
├────────────────────────────┼────────────────────────────────┤
│  REQUEST THROUGHPUT        │  ERROR RATE                    │
│  ┌──────────────────────┐  │  ┌──────────────────────────┐  │
│  │ ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅ │  │  │ ▁▁▁▁▁▂▁▁▁▁▁▁▁▁▁▁▁▁▁▁  │  │
│  └──────────────────────┘  │  └──────────────────────────┘  │
│  Current: 12,450 req/s     │  Current: 0.02%                │
│  Peak: 18,200 req/s        │  Threshold: 1.0%               │
├────────────────────────────┴────────────────────────────────┤
│  RECENT ALERTS                                              │
│  10:40  🟡 High latency on payment-service (p99 > 500ms)    │
│  10:35  🟢 Resolved: Database connection pool recovered     │
│  10:22  🔴 Payment service circuit breaker tripped          │
└─────────────────────────────────────────────────────────────┘
```

## 实现模式

### KPI 计算的 SQL

```sql
-- Monthly Recurring Revenue (MRR)
WITH mrr_calculation AS (
    SELECT
        DATE_TRUNC('month', billing_date) AS month,
        SUM(
            CASE subscription_interval
                WHEN 'monthly' THEN amount
                WHEN 'yearly' THEN amount / 12
                WHEN 'quarterly' THEN amount / 3
            END
        ) AS mrr
    FROM subscriptions
    WHERE status = 'active'
    GROUP BY DATE_TRUNC('month', billing_date)
)
SELECT
    month,
    mrr,
    LAG(mrr) OVER (ORDER BY month) AS prev_mrr,
    (mrr - LAG(mrr) OVER (ORDER BY month)) / LAG(mrr) OVER (ORDER BY month) * 100 AS growth_pct
FROM mrr_calculation;

-- Cohort Retention
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', created_at) AS cohort_month
    FROM users
),
activity AS (
    SELECT
        user_id,
        DATE_TRUNC('month', event_date) AS activity_month
    FROM user_events
    WHERE event_type = 'active_session'
)
SELECT
    c.cohort_month,
    EXTRACT(MONTH FROM age(a.activity_month, c.cohort_month)) AS months_since_signup,
    COUNT(DISTINCT a.user_id) AS active_users,
    COUNT(DISTINCT a.user_id)::FLOAT / COUNT(DISTINCT c.user_id) * 100 AS retention_rate
FROM cohorts c
LEFT JOIN activity a ON c.user_id = a.user_id
    AND a.activity_month >= c.cohort_month
GROUP BY c.cohort_month, EXTRACT(MONTH FROM age(a.activity_month, c.cohort_month))
ORDER BY c.cohort_month, months_since_signup;

-- Customer Acquisition Cost (CAC)
SELECT
    DATE_TRUNC('month', acquired_date) AS month,
    SUM(marketing_spend) / NULLIF(COUNT(new_customers), 0) AS cac,
    SUM(marketing_spend) AS total_spend,
    COUNT(new_customers) AS customers_acquired
FROM (
    SELECT
        DATE_TRUNC('month', u.created_at) AS acquired_date,
        u.id AS new_customers,
        m.spend AS marketing_spend
    FROM users u
    JOIN marketing_spend m ON DATE_TRUNC('month', u.created_at) = m.month
    WHERE u.source = 'marketing'
) acquisition
GROUP BY DATE_TRUNC('month', acquired_date);
```

### Python 仪表盘代码（Streamlit）

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="KPI Dashboard", layout="wide")

# Header with date filter
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Executive Dashboard")
with col2:
    date_range = st.selectbox(
        "Period",
        ["Last 7 Days", "Last 30 Days", "Last Quarter", "YTD"]
    )

# KPI Cards
def metric_card(label, value, delta, prefix="", suffix=""):
    delta_color = "green" if delta >= 0 else "red"
    delta_arrow = "▲" if delta >= 0 else "▼"
    st.metric(
        label=label,
        value=f"{prefix}{value:,.0f}{suffix}",
        delta=f"{delta_arrow} {abs(delta):.1f}%"
    )

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Revenue", 2400000, 12.5, prefix="$")
with col2:
    metric_card("Customers", 12450, 15.2)
with col3:
    metric_card("NPS Score", 72, 5.0)
with col4:
    metric_card("Churn Rate", 4.2, -0.8, suffix="%")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue Trend")
    revenue_data = pd.DataFrame({
        'Month': pd.date_range('2024-01-01', periods=12, freq='M'),
        'Revenue': [180000, 195000, 210000, 225000, 240000, 255000,
                    270000, 285000, 300000, 315000, 330000, 345000]
    })
    fig = px.line(revenue_data, x='Month', y='Revenue',
                  line_shape='spline', markers=True)
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue by Product")
    product_data = pd.DataFrame({
        'Product': ['Enterprise', 'Professional', 'Starter', 'Other'],
        'Revenue': [45, 32, 18, 5]
    })
    fig = px.pie(product_data, values='Revenue', names='Product',
                 hole=0.4)
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

# Cohort Heatmap
st.subheader("Cohort Retention")
cohort_data = pd.DataFrame({
    'Cohort': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'M0': [100, 100, 100, 100, 100],
    'M1': [85, 87, 84, 86, 88],
    'M2': [78, 80, 76, 79, None],
    'M3': [72, 74, 70, None, None],
    'M4': [68, 70, None, None, None],
})
fig = go.Figure(data=go.Heatmap(
    z=cohort_data.iloc[:, 1:].values,
    x=['M0', 'M1', 'M2', 'M3', 'M4'],
    y=cohort_data['Cohort'],
    colorscale='Blues',
    text=cohort_data.iloc[:, 1:].values,
    texttemplate='%{text}%',
    textfont={"size": 12},
))
fig.update_layout(height=250)
st.plotly_chart(fig, use_container_width=True)

# Alerts Section
st.subheader("Alerts")
alerts = [
    {"level": "error", "message": "Churn rate exceeded threshold (>5%)"},
    {"level": "warning", "message": "Support ticket volume 20% above average"},
]
for alert in alerts:
    if alert["level"] == "error":
        st.error(f"🔴 {alert['message']}")
    elif alert["level"] == "warning":
        st.warning(f"🟡 {alert['message']}")
```

## 最佳实践

### 应做

- **限制为 5-7 个 KPI** — 聚焦关键指标
- **展示上下文** — 对比、趋势、目标值
- **使用一致的配色** — 红色=不良，绿色=良好
- **支持下钻** — 从摘要到明细
- **按需更新** — 匹配指标频率

### 不应做

- **不要展示虚荣指标** — 聚焦可操作的数据
- **不要过度拥挤** — 留白有助于理解
- **不要使用 3D 图表** — 它们会扭曲感知
- **不要隐藏计算方法** — 记录计算逻辑
- **不要忽视移动端** — 确保响应式设计

## 参考资料

- [Stephen Few's Dashboard Design](https://www.perceptualedge.com/articles/visual_business_intelligence/rules_for_using_color.pdf)
- [Edward Tufte's Principles](https://www.edwardtufte.com/tufte/)
- [Google Data Studio Gallery](https://datastudio.google.com/gallery)

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代方案。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
