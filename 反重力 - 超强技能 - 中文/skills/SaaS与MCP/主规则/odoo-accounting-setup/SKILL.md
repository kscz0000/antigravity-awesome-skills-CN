---
name: odoo-accounting-setup
description: "Odoo 会计配置专家指南：会计科目表、日记账、财政状况、税款、付款条件和银行对账。当用户要求'配置 Odoo 会计'、'设置会计科目表'、'创建日记账'、'配置税款'、'设置付款条件'或'银行对账'时使用。"
risk: safe
source: "self"
---

# Odoo 会计设置

## 概述

本技能指导功能顾问和企业主从零开始正确设置 Odoo 会计。涵盖会计科目表配置、日记账设置、税则、财政状况、付款条件以及银行对账单对账工作流。

## 何时使用本技能

- 首次为公司设置新的 Odoo 实例。
- 配置多币种或多公司会计。
- 排查税款计算或财政状况映射错误。
- 创建分期付款的付款条件（例如 Net 30、50% 预付）。

## 工作原理

1. **激活**：提及 `@odoo-accounting-setup` 并描述您的会计场景。
2. **配置**：获取逐步 Odoo 菜单导航及精确字段值。
3. **验证**：获取检查清单以验证设置是否完整正确。

## 示例

### 示例 1：创建付款条件（Net 30 含 2% 早付折扣）

```text
Menu: Accounting → Configuration → Payment Terms → New

Name: Net 30 / 2% Early Pay Discount
Company: [Your Company]

Lines:
  Line 1:
    - Due Type: Percent
    - Value: 100%
    - Due: 30 days (full balance due in 30 days)

Early Payment Discount (Odoo 16+):
  Discount %: 2
  Discount Days: 10
  Balance Sheet Accounts:
    - Gain: 4900 Early Payment Discounts Granted
    - Loss: 5900 Early Payment Discounts Received
```

> **注意 (v16+)：** 使用内置的 **Early Payment Discount** 字段，而非旧的拆分行变通方案。Odoo 现在会在客户在折扣窗口内付款时自动过账折扣，并生成正确的会计分录。

### 示例 2：欧盟增值税财政状况（B2B 共同体内部）

```text
Menu: Accounting → Configuration → Fiscal Positions → New

Name: EU Intra-Community B2B
Auto-detection: ON
  - Country Group: Europe
  - VAT Required: YES (customer must have EU VAT number)

Tax Mapping:
  Tax on Sales (21% VAT) → 0% Intra-Community VAT
  Tax on Purchases      → 0% Reverse Charge

Account Mapping:
  (Leave empty unless your localization requires account remapping)
```

### 示例 3：银行费用对账模型

```text
Menu: Accounting → Configuration → Reconciliation Models → New

Name: Bank Fee Auto-Match
Type: Write-off
Matching Order: 1

Conditions:
  - Label Contains: "BANK FEE" OR "SERVICE CHARGE"
  - Amount Type: Amount is lower than: $50.00

Action:
  - Account: 6200 Bank Charges
  - Tax: None
  - Analytic: Administrative
```

## 最佳实践

- ✅ **应该：** 在手动创建科目之前，先安装您所在国家/地区的**本地化模块**（`l10n_us`、`l10n_mx` 等）——它会设置正确的会计科目表。
- ✅ **应该：** 使用**财政状况**自动切换 B2B 与 B2C 税款——切勿在单张发票上手动更改税款。
- ✅ **应该：** 月末结账后锁定会计期间（Accounting → Actions → Lock Dates）以防止追溯编辑。
- ✅ **应该：** 使用 **Early Payment Discount** 功能（v16+），而非拆分付款条件行来建模折扣。
- ❌ **不应该：** 删除日记账分录——始终使用贷项通知单或内置冲销功能进行冲销。
- ❌ **不应该：** 在同一日记账中混合个人和业务交易。
- ❌ **不应该：** 创建手动日记账分录来修复银行对账不匹配——请改用对账模型工作流。

## 限制

- 不深入涵盖**多币种重估**或外汇损益会计。
- **国家/地区特定电子发票**（CFDI、FatturaPA、SAF-T）需要额外的本地化模块——请使用 `@odoo-l10n-compliance`。
- 薪资会计集成（工资日记账、扣款科目）不在此处涵盖——请使用 `@odoo-hr-payroll-setup`。
- Odoo 社区版不包含完整的**锁定日期**功能；部分控件仅限企业版。
