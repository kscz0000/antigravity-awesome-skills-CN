---
name: odoo-ecommerce-configurator
description: "Odoo 电商与网站的专业配置指南：产品目录、支付提供商、物流方式、SEO 及订单履约全流程。当用户要求'配置 Odoo 电商'、'设置 Odoo 网上商店'、'集成支付'、'配置物流'或'优化 Odoo 电商 SEO'时使用。"
risk: safe
source: "self"
---

# Odoo 电商配置器

## 概述

本技能帮助你搭建和优化基于 Odoo 的在线商店。涵盖产品发布、支付网关集成、物流商配置、购物车与结算定制，以及从线上订单到仓库履约的完整流程。

## 使用场景

- 首次搭建 Odoo 电商商店
- 集成支付提供商（Stripe、PayPal、Adyen）
- 配置物流费率并对接承运商（UPS、FedEx、DHL）
- 使用 Odoo 网站工具优化产品页面的 SEO

## 工作方式

1. **激活**：提及 `@odoo-ecommerce-configurator` 并描述你的商店场景
2. **配置**：获取带菜单路径的 Odoo 电商分步配置指引
3. **优化**：获取 SEO、转化率和目录管理的最佳实践

## 示例

### 示例 1：发布产品到网站

```text
Menu: Website → eCommerce → Products → Select Product

Fields to complete for a great product listing:
  Name:               Ergonomic Mesh Office Chair  (keyword-rich)
  Internal Reference: CHAIR-MESH-001               (required for inventory)
  Sales Price:        $299.00
  Website Description (website tab): 150–300 words of unique content

Publishing:
  Toggle "Published" in the top-right corner of the product form
  or via: Website → Go to Website → Toggle "Published" button

SEO (website tab → SEO section):
  Page Title:       Ergonomic Mesh Chair | Office Chairs | YourStore
  Meta Description: Discover the most comfortable ergonomic mesh office
                    chair, designed for all-day support...  (≤160 chars)

Website tab:
  Can be Sold: YES
  Website:     yourstore.com  (if running multiple websites)
```

### 示例 2：配置 Stripe 支付提供商

```text
Menu: Website → Configuration → Payment Providers → Stripe → Configure
(or: Accounting → Configuration → Payment Providers → Stripe)

State: Test  (use Test mode until fully validated, then switch to Enabled)

Credentials (from your Stripe Dashboard → Developers → API Keys):
  Publishable Key: pk_live_XXXXXXXX
  Secret Key:      sk_live_XXXXXXXX  (store securely; never expose client-side)

Payment Journal: Bank (USD)
Capture Mode:    Automatic  (charge card immediately on order confirmation)
                 or Manual  (authorize only; charge later on fulfillment)

Webhook:
  Add Odoo's webhook URL in Stripe Dashboard → Webhooks
  URL: https://yourstore.com/payment/stripe/webhook
  Events: payment_intent.succeeded, payment_intent.payment_failed
```

### 示例 3：设置固定运费及免邮门槛

```text
Menu: Inventory → Configuration → Delivery Methods → New

Name: Standard Shipping (3–5 business days)
Provider: Fixed Price
Delivery Product: [Shipping] Standard  (used for invoicing)

Pricing:
  Price: $9.99
  ☑ Free if order amount is above: $75.00

Availability:
  Countries: United States
  States: All states

Publish to website:
  ☑ Published  (visible to customers at checkout)
```

### 示例 4：设置弃购挽回邮件

```text
Menu: Email Marketing → Mailing Lists → (create a list if needed)

For automated abandoned cart emails in Odoo 16/17:
Menu: Marketing → Marketing Automation → New Campaign

Trigger: Odoo record updated
Model: eCommerce Cart (sale.order with state = 'draft')
Filter: Cart not updated in 1 hour AND not confirmed

Actions:
  1. Wait 1 hour
  2. Send Email: "You left something behind!"  (use a recovery email template)
  3. Wait 24 hours
  4. Send Email: "Last chance — items selling fast"

Note: Some Odoo hosting plans may require "Email Marketing" app enabled.
```

## 最佳实践

- ✅ **推荐：** 使用**产品变体**（颜色、尺寸）而非重复创建产品——目录更清晰，库存统一追踪。
- ✅ **推荐：** 通过托管商启用 **HTTPS**（SSL 证书），并在网站 → 设置 → 安全中设置 HSTS。
- ✅ **推荐：** 使用营销自动化或定时邮件序列设置**弃购挽回**。
- ✅ **推荐：** 添加 **Stripe webhook**，让 Odoo 实时接收支付事件——否则失败的支付可能无法正确更新状态。
- ❌ **避免：** 在生产环境将支付提供商保持在**测试模式**——无法处理真实扣款。
- ❌ **避免：** 发布缺少**内部参考编号（SKU）**的产品——会导致库存追踪和订单履约中断。
- ❌ **避免：** 测试和生产环境共用同一个 Stripe 密钥——上线前务必切换为正式密钥。

## 局限性

- **承运商集成**（实时 UPS/FedEx 费率计算）需要对应的承运商连接器模块（如 `delivery_ups`）及承运商账户 API 密钥。
- 不涵盖**多网站**配置——使用不同价格表和语言运行独立商店需要企业版。
- **B2B 电商**（需客户登录、按客户定制目录和价格）有额外配置步骤，此处未完全覆盖。
- Odoo 电商原生不支持**订阅计费**——需要企业版的**订阅**模块。
