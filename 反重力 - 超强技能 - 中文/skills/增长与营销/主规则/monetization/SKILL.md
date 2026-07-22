---
name: monetization
description: "数字产品商业化策略与实施——Stripe、订阅制、定价实验、freemium、升级流程、流失预防、收入优化及 SaaS 商业模式。当用户要求'商业化策略'或'定价方案'时使用。"
risk: none
source: community
date_added: '2026-03-06'
author: renat
tags:
- monetization
- stripe
- saas
- pricing
- subscriptions
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# MONETIZATION - 从产品到收入

## 概述

数字产品商业化策略与实施——Stripe、订阅制、定价实验、freemium、升级流程、流失预防、收入优化及 SaaS 商业模式。涉及 Stripe 集成、创建订阅套餐、定价策略、升级/降级、支付 webhook、免费试用、churn、LTV/CAC、unit economics、商业模式时使用。

## 何时使用此技能

- 需要该领域的专业协助时

## 何时不使用此技能

- 任务与商业化无关
- 更简单、更具体的工具即可处理
- 用户需要的是通用帮助而非领域专业知识

## 工作原理

> Price is what you pay. Value is what you get. - Warren Buffett
> 完美的商业化按交付价值的比例捕获收益。

---

## 黄金法则

用户付费的条件：
1. 产品解决了真实问题（需求）
2. 方案优于替代品（差异化）
3. 价格被认为合理（价值感知）
4. 收费时机自然（时机）

## 经典错误

- 未展示价值就收费（扼杀激活）
- 定价过低（传递低质量信号）
- 套餐过多（选择瘫痪）
- 免费试用不绑卡（转化率低）
- 隐性流失（无即将取消的预警）

---

## 初始配置

```bash
pip install stripe

## Ou

npm install stripe
```

```python

## Config.Py

import stripe
import os

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
STRIPE_WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]

PLANS = {
    "free": None,
    "pro": os.environ["STRIPE_PRICE_PRO"],
    "business": os.environ["STRIPE_PRICE_BIZ"],
}
```

## 创建客户与订阅

```python
def create_customer(email: str, name: str, user_id: str) -> str:
    customer = stripe.Customer.create(
        email=email,
        name=name,
        metadata={"user_id": user_id}
    )
    return customer.id

def create_subscription(customer_id: str, price_id: str, trial_days: int = 14):
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
        trial_period_days=trial_days,
        payment_behavior="default_incomplete",
        expand=["latest_invoice.payment_intent"],
    )
    return {
        "subscription_id": subscription.id,
        "client_secret": subscription.latest_invoice.payment_intent.client_secret,
        "status": subscription.status
    }
```

## Checkout Session（推荐用于转化）

```python
def create_checkout_session(
    customer_id: str,
    price_id: str,
    success_url: str,
    cancel_url: str,
    trial_days: int = 14
) -> str:
    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        subscription_data={"trial_period_days": trial_days},
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
        allow_promotion_codes=True,
    )
    return session.url
```

## 客户门户（自助服务）

```python
def create_portal_session(customer_id: str, return_url: str) -> str:
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )
    return session.url
```

## Webhook - 处理事件

```python
from fastapi import Request, HTTPException
import stripe

async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    handlers = {
        "customer.subscription.created": handle_subscription_created,
        "customer.subscription.updated": handle_subscription_updated,
        "customer.subscription.deleted": handle_subscription_deleted,
        "invoice.payment_succeeded": handle_payment_succeeded,
        "invoice.payment_failed": handle_payment_failed,
        "customer.subscription.trial_will_end": handle_trial_ending,
    }

    handler = handlers.get(event["type"])
    if handler:
        await handler(event["data"]["object"])

    return {"status": "ok"}
```

## 检查订阅状态

```python
def get_subscription_status(customer_id: str) -> dict:
    subscriptions = stripe.Subscription.list(
        customer=customer_id,
        status="all",
        limit=1
    )
    if not subscriptions.data:
        return {"tier": "free", "status": "none"}

    sub = subscriptions.data[0]
    return {
        "tier": get_tier_from_price(sub.items.data[0].price.id),
        "status": sub.status,
        "trial_end": sub.trial_end,
        "current_period_end": sub.current_period_end,
        "cancel_at_period_end": sub.cancel_at_period_end,
    }
```

---

## SaaS 定价框架

**方法一：基于价值的定价（推荐）**
```
1. 计算交付给用户的经济价值
   示例：产品每周节省 2 小时 = 每月 ¥200 的价值
2. 捕获所创造价值的 10-30%
   示例：¥29/月 = 价值的 14%
3. 通过支付意愿调研验证
4. 测试 3 个价格点（A/B 测试）
```

**方法二：竞争锚定**
```
参考：ChatGPT Plus = $20/月（¥100）
锚点：Notion = ¥32/月
定位：Pro = ¥29/月（比 ChatGPT 便宜，与 Notion 相近）
信息：ChatGPT 能做的，通过 Alexa 语音实现
```

## 定价心理学

```
¥29/月（而非 ¥30——左侧数字效应）
年付套餐标注明确折扣：¥249/年（节省 ¥99）
重点突出你想卖的套餐（视觉层级）
锚定效应：先展示贵的套餐
试用不绑卡利于激活，绑卡利于留存
中间套餐加"最受欢迎"标签
```

## 套餐结构（3 是正确数字）

| 功能             | 免费    | Pro        | Business   |
|-----------------|---------|------------|------------|
| 价格             | 免费    | ¥29/月     | ¥99/月     |
| 对话数/月        | 50      | 无限       | 无限       |
| 记忆             | 7 天    | 1 年       | 永久       |
| 专家面板         | 否      | 是         | 是         |
| 多用户           | 否      | 否         | 最多 10 人 |
| API access       | 否      | 否         | 是         |
| 支持             | 否      | 邮件       | 优先       |

---

## 流失预警信号

```python
CHURN_SIGNALS = {
    "high_risk": [
        "近 14 天未登录",
        "2 周内使用量下降 >70%",
        "发起取消但未完成",
        "工单未解决",
    ],
    "medium_risk": [
        "7 天未登录",
        "使用量下降 >40%",
        "未完成新手引导",
        "从未使用核心功能",
    ]
}
```

## 防流失序列

```
第 0 天：用户 7 天未使用
        -> 邮件：好久不见，发生了什么？

第 3 天：无回复
        -> 推送/邮件：相似用户的成功案例

第 7 天：仍未回来
        -> 邮件：特别优惠（3 个月 8 折）

第 14 天：试用即将到期
        -> 应用内弹窗 + 紧急邮件：你的账户将在 3 天后休眠

第 30 天：已取消
        -> 离场邮件：很遗憾看到你离开。
        -> 3 个月后：附带新功能的重新激活邮件
```

## 退出调查（必做）

```python
CANCELLATION_REASONS = [
    "太贵了",
    "用得不够多",
    "缺少 X 功能",
    "找到了更好的替代品",
    "技术问题",
    "其他"
]

## 缺少功能 -> 加入路线图 + 上线时通知

```

---

## 核心计算

```python
def calculate_unit_economics(
    mrr: float,
    customers: int,
    new_customers: int,
    churned: int,
    cac_total: float,
):
    arpu = mrr / customers
    churn_rate = churned / customers
    ltv = arpu / churn_rate
    cac = cac_total / new_customers
    ltv_cac = ltv / cac
    months_to_recover_cac = cac / arpu

    return {
        "ARPU": f"¥ {arpu:.2f}",
        "Churn Rate": f"{churn_rate*100:.1f}%",
        "LTV": f"¥ {ltv:.0f}",
        "CAC": f"¥ {cac:.0f}",
        "LTV/CAC": f"{ltv_cac:.1f}x",
        "Payback": f"{months_to_recover_cac:.1f} 个月",
        "Status": "健康" if ltv_cac > 3 else "需优化"
    }
```

## SaaS B2C 基准指标

| 指标               | 差    | 一般   | 良好   | 优秀   |
|-------------------|-------|--------|--------|--------|
| 月流失率           | >7%   | 5-7%   | 2-5%   | <2%    |
| LTV/CAC           | <1x   | 1-3x   | 3-5x   | >5x    |
| 回本周期           | >18月 | 12-18月| 6-12月 | <6月   |
| 试用转付费         | <3%   | 3-8%   | 8-15%  | >15%   |
| 环比增长           | <5%   | 5-10%  | 10-20% | >20%   |

---

## 收入仪表盘（日常指标）

```
当前 MRR：¥ XX.XXX
  新增 MRR（新订阅）：+¥ X.XXX
  扩展 MRR（升级）：+¥ XXX
  收缩 MRR（降级）：-¥ XXX
  流失 MRR（取消）：-¥ XXX
  净新增 MRR：+/- ¥ XXX

ARR（年化）：¥ XX.XXX x 12
Churn Rate：X.X%
Net Revenue Retention：XXX%（目标：>100%）
```

## Stripe 收入自动化

```python
async def check_usage_and_upsell(user_id: str, usage: dict):
    if usage["conversations_this_month"] >= 45:
        await send_upgrade_prompt(
            user_id=user_id,
            message="你已使用 90% 的额度，升级到 Pro 吧。",
            cta_url=f"/upgrade?utm=usage-limit"
        )
```

---

## 快捷命令

| 命令                | 操作                                     |
|--------------------|------------------------------------------|
| /stripe-setup      | 从零配置 Stripe                          |
| /pricing-analysis  | 分析当前定价策略                         |
| /churn-playbook    | 定制防流失序列                           |
| /unit-economics    | 计算 LTV/CAC 及财务健康度                |
| /upgrade-flow      | 设计升级流程                             |
| /revenue-dashboard | 收入仪表盘模板                           |
| /trial-optimization| 优化试用转化                             |

## 最佳实践

- 提供清晰、具体的项目背景和需求
- 应用到生产代码前审查所有建议
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于超出其领域的任务
- 不理解具体场景就套用建议
- 未提供足够的项目背景导致分析不准确

## 相关技能

- `analytics-product` - 互补技能，用于增强分析
- `growth-engine` - 互补技能，用于增强分析
- `product-design` - 互补技能，用于增强分析
- `product-inventor` - 互补技能，用于增强分析

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 输出不能替代针对具体环境的验证、测试或专家评审。
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。
