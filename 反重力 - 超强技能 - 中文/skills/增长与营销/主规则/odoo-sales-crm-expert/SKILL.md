---
name: odoo-sales-crm-expert
description: "Odoo Sales 和 CRM 专家指南：pipeline 阶段、报价模板、价格表、销售团队、线索评分和预测。当用户要求'配置 Odoo Sales/CRM'、'设置 pipeline 阶段'、'创建报价模板'、'配置价格表'、'管理销售团队'或'线索评分预测'时使用。"
risk: safe
source: "self"
---

# Odoo Sales & CRM 专家

## 概述

本技能帮助你配置和优化 Odoo Sales 和 CRM。涵盖机会 pipeline 设置、自动化线索分配、报价模板、价格表策略、销售团队管理以及从销售到开票的完整工作流。

## 何时使用本技能

- 为你的销售流程设计 CRM pipeline 阶段
- 创建包含可选产品和捆绑的报价模板
- 设置客户层级定价的价格表
- 按区域或销售人员配置自动化线索分配

## 工作原理

1. **激活**：提及 `@odoo-sales-crm-expert` 并描述你的销售场景
2. **配置**：获取 Odoo 逐步设置指引
3. **优化**：获得提升 pipeline 转化速度和成交率的建议

## 示例

### 示例 1：配置 CRM Pipeline 阶段

```text
Menu: CRM → Configuration → Stages → New

Typical B2B Pipeline:
  Stage 1: New Lead          (probability: 10%)
  Stage 2: Qualified         (probability: 25%)
  Stage 3: Proposal Sent     (probability: 50%)
  Stage 4: Negotiation       (probability: 75%)
  Stage 5: Won               (is_won: YES — marks opportunity as closed-won)
  Stage 6: Lost              (mark as lost via the "Mark as Lost" button)

Tips:
  - Enable "Rotting Days" in CRM Settings to flag stale deals in red
  - In Odoo 16+, Predictive Lead Scoring (AI) auto-updates probability
    based on historical data. Disable it in Settings if you prefer manual
    stage-based probability.
```

### 示例 2：创建报价模板

```text
Menu: Sales → Configuration → Quotation Templates → New
(Requires the "Sales Management" module — enabled in Sales Settings)

Template Name: SaaS Annual Subscription
Valid for: 30 days

Lines:
  1. Platform License   | Qty: 1 | Price: $1,200/yr | (required)
  2. Onboarding Package | Qty: 1 | Price: $500       | Optional
  3. Premium Support    | Qty: 1 | Price: $300/yr    | Optional
  4. Extra User License | Qty: 0 | Price: $120/user  | Optional

Signature & Payment:
  ☑ Online Signature required before order confirmation
  ☑ Online Payment (deposit) — 50% upfront

Notes section:
  "Prices valid until expiration date. Subject to Schedule A terms."
```

### 示例 3：客户层级价格表（VIP 折扣）

```text
Menu: Sales → Configuration → Settings
  ☑ Enable Pricelists

Menu: Sales → Configuration → Pricelists → New

Name: VIP Customer — 15% Off
Currency: USD
Discount Policy: Show public price & discount on quotation

Rules:
  Apply To: All Products
  Compute Price: Discount
  Discount: 15%
  Min. Quantity: 1

Assign to a customer:
  Customer record → Sales & Purchase tab → Pricelist → VIP Customer
```

## 最佳实践

- ✅ **应该做：** 使用 **丢失原因**（CRM → Configuration → Lost Reasons）建立交易丢失原因的数据集——对销售辅导极有价值。
- ✅ **应该做：** 启用带收入目标的 **销售团队**，使 pipeline 预测对每个团队都有意义。
- ✅ **应该做：** 在每个机会上设置 **预期收入** 和 **成交日期**——这些数据会流入收入预测仪表板。
- ✅ **应该做：** 使用 **报价模板** 标准化报价，减少团队整体报价时间。
- ❌ **不应该做：** 销售时跳过 CRM 机会——从线索直接到发票会破坏 pipeline 分析。
- ❌ **不应该做：** 以手动编辑报价行价格作为变通方案——应该设置正确的价格表。
- ❌ **不应该做：** 忽视 v16+ 中的 **预测性线索评分** 功能——用历史数据配置它以获得准确预测。

## 限制

- **佣金规则**不是 Odoo CRM 的内置功能——需要自定义开发或第三方模块。
- **报价模板**的可选产品功能需要 **Sale Management** 模块；在基础 `sale` 模块中不可用。
- **基于区域的线索分配**（地理路由）需要自定义规则或 Enterprise Leads 模块。
- Odoo CRM 没有原生的 **邮件序列/节奏** 自动化——使用 **Email Marketing** 或 **Marketing Automation** 模块进行 drip 营销活动。