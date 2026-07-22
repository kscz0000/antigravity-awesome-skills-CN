---
name: analytics-product
description: "产品分析 — PostHog、Mixpanel、事件、漏斗、队列、留存、北极星指标、OKR 和产品仪表盘。触发词：产品分析、事件追踪、转化漏斗、队列分析、留存分析、DAU/MAU、Feature Flags、A/B测试、北极星指标、OKR、产品仪表盘、PostHog、Mixpanel、数据驱动决策。"
risk: none
source: community
date_added: '2026-03-06'
author: renat
tags:
- analytics
- product
- metrics
- posthog
- mixpanel
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# ANALYTICS-PRODUCT — 用数据决策

## 概述

产品分析 — PostHog、Mixpanel、事件、漏斗、队列、留存、北极星指标、OKR 和产品仪表盘。适用于：设置事件追踪、创建转化漏斗、队列分析、留存分析、DAU/MAU、Feature Flags、A/B测试、北极星指标、OKR、产品仪表盘。

## 何时使用此技能

- 当你需要该领域的专业协助时

## 何时不使用此技能

- 任务与产品分析无关
- 更简单、更具体的工具可以处理该请求
- 用户需要的是无领域专业知识的通用协助

## 工作原理

```
[对象]_[动词过去式]

正确：   user_signed_up, conversation_started, upgrade_completed
错误：    signup, click, conversion
```

## Analytics-Product — 用数据决策

> "我们相信上帝。其他人必须带数据来。" — W. Edwards Deming

---

## Auri 核心事件

```python
AURI_EVENTS = {
    # 获客
    "user_signed_up":        {"props": ["source", "medium", "campaign"]},
    "onboarding_started":    {"props": ["step_count"]},
    "onboarding_completed":  {"props": ["time_to_complete", "steps_skipped"]},

    # 激活
    "first_conversation":    {"props": ["intent", "response_time"]},
    "aha_moment_reached":    {"props": ["trigger", "session_number"]},
    "feature_discovered":    {"props": ["feature_name", "discovery_method"]},

    # 留存
    "conversation_started":  {"props": ["intent", "user_tier", "device"]},
    "conversation_completed":{"props": ["messages_count", "duration", "rating"]},
    "session_started":       {"props": ["days_since_last", "platform"]},

    # 收入
    "upgrade_viewed":        {"props": ["trigger", "current_tier"]},
    "upgrade_started":       {"props": ["target_tier", "trigger"]},
    "upgrade_completed":     {"props": ["tier", "plan", "revenue"]},
    "subscription_canceled": {"props": ["reason", "tier", "tenure_days"]},
    "payment_failed":        {"props": ["attempt_count", "error_code"]},
}
```

## PostHog 实现（Python）

```python
from posthog import Posthog
import os

posthog = Posthog(
    project_api_key=os.environ["POSTHOG_API_KEY"],
    host=os.environ.get("POSTHOG_HOST", "https://app.posthog.com")
)

def track(user_id: str, event: str, properties: dict = None):
    posthog.capture(
        distinct_id=user_id,
        event=event,
        properties=properties or {}
    )

def identify(user_id: str, traits: dict):
    posthog.identify(
        distinct_id=user_id,
        properties=traits
    )

## 使用：

track("user_123", "conversation_started", {
    "intent": "business_advice",
    "device": "alexa",
    "user_tier": "pro"
})
```

---

## Auri 激活漏斗

```
访问落地页              (100%)
    | [目标: 40%]
点击"试用"               (40%)
    | [目标: 70%]
完成注册                 (28%)
    | [目标: 60%]
完成首次对话              (17%)  <- AHA MOMENT
    | [目标: 50%]
次日回访                 (8.5%)
    | [目标: 40%]
一周内使用3天以上          (3.4%)
    | [目标: 20%]
转化为付费用户            (0.7%)
```

## 优化漏斗

```
对于每个流失率 > 基准的环节：
1. 识别：用户究竟在哪里离开？
2. 理解：为什么？（会话录制、问卷调查）
3. 假设：什么改变可以改善？
4. 测试：使用具有统计显著性的样本进行A/B测试
5. 测量：最少2周，p-value < 0.05
6. 学习：即使失败，也能更好地理解用户
```

---

## 队列分析（周留存）

```python
def calculate_cohort_retention(events_df):
    """
    events_df: 包含列 [user_id, event_date, event_name] 的 DataFrame
    返回：留存矩阵 [队列周 x 周数]
    """
    import pandas as pd

    first_session = events_df[events_df.event_name == "session_started"] \
        .groupby("user_id")["event_date"].min() \
        .dt.to_period("W")

    sessions = events_df[events_df.event_name == "session_started"].copy()
    sessions["cohort"] = sessions["user_id"].map(first_session)
    sessions["weeks_since"] = (
        sessions["event_date"].dt.to_period("W") - sessions["cohort"]
    ).apply(lambda x: x.n)

    cohort_data = sessions.groupby(["cohort", "weeks_since"])["user_id"].nunique()
    cohort_sizes = cohort_data.unstack().iloc[:, 0]
    retention = cohort_data.unstack().divide(cohort_sizes, axis=0) * 100

    return retention
```

## 留存基准（语音助手）

| 周数 | 差 | 一般 | 好 | 优秀 |
|--------|---------|-----|-----|-----------|
| W1 | <20% | 20-35% | 35-50% | >50% |
| W4 | <10% | 10-20% | 20-30% | >30% |
| W8 | <5% | 5-12% | 12-20% | >20% |

---

## 定义 Auri 的北极星指标

```
框架：
1. 什么能为用户创造真实价值？ -> 产生洞察/行动的对话
2. 什么能预测长期增长？ -> 每周3次以上对话的用户
3. 如何测量？ -> "周活跃对话用户" (WAC)

北极星：WAC (Weekly Active Conversationalists)
定义：每周进行 >= 3 次且时长 >= 2 分钟对话的用户

第1年目标：10,000 WAC
第2年目标：100,000 WAC
```

## 北极星仪表盘

```python
def calculate_north_star(db):
    wac = db.query("""
        SELECT COUNT(DISTINCT user_id) as wac
        FROM conversations
        WHERE
            created_at >= NOW() - INTERVAL '7 days'
            AND duration_seconds >= 120
        GROUP BY user_id
        HAVING COUNT(*) >= 3
    """).scalar()

    return {
        "wac": wac,
        "wow_growth": calculate_wow_growth(db, "wac"),
        "target": 10000,
        "progress": f"{wac/10000*100:.1f}%"
    }
```

---

## PostHog Feature Flags

```python
def is_feature_enabled(user_id: str, feature: str) -> bool:
    return posthog.feature_enabled(feature, user_id)

if is_feature_enabled(user_id, "new-onboarding-v2"):
    show_new_onboarding()
else:
    show_old_onboarding()
```

## 统计显著性计算器

```python
from scipy import stats
import numpy as np

def ab_test_significance(
    control_conversions: int,
    control_visitors: int,
    variant_conversions: int,
    variant_visitors: int,
    confidence: float = 0.95
) -> dict:
    control_rate = control_conversions / control_visitors
    variant_rate = variant_conversions / variant_visitors
    lift = (variant_rate - control_rate) / control_rate * 100

    _, p_value = stats.chi2_contingency([
        [control_conversions, control_visitors - control_conversions],
        [variant_conversions, variant_visitors - variant_conversions]
    ])[:2]

    significant = p_value < (1 - confidence)

    return {
        "control_rate": f"{control_rate*100:.2f}%",
        "variant_rate": f"{variant_rate*100:.2f}%",
        "lift": f"{lift:+.1f}%",
        "p_value": round(p_value, 4),
        "significant": significant,
        "recommendation": "Deploy variant" if significant and lift > 0 else "Keep control"
    }
```

---

## 6. 命令

| 命令 | 操作 |
|---------|------|
| `/event-taxonomy` | 定义事件分类体系 |
| `/funnel-analysis` | 分析转化漏斗 |
| `/cohort-retention` | 计算队列留存 |
| `/north-star` | 定义或修订北极星指标 |
| `/ab-test` | 计算A/B测试显著性 |
| `/dashboard-setup` | 创建产品仪表盘 |
| `/okr-template` | 产品OKR模板 |

## 最佳实践

- 提供清晰、具体的项目和需求背景
- 在将建议应用到生产代码之前进行审查
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其专业领域之外的任务
- 在不了解具体背景的情况下应用建议
- 未提供足够的项目背景以进行准确分析

## 相关技能

- `growth-engine` - 互补技能，用于增强分析
- `monetization` - 互补技能，用于增强分析
- `product-design` - 互补技能，用于增强分析
- `product-inventor` - 互补技能，用于增强分析

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出替代为环境特定的验证、测试或专家审查。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
