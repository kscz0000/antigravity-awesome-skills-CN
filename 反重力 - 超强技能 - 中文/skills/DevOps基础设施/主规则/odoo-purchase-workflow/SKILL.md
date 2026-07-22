---
name: odoo-purchase-workflow
description: "Odoo 采购流程专家指南：询价单(RFQ) → 采购订单(PO) → 收货 → 供应商账单，涵盖采购协议、供应商价格表和三方匹配。当用户要求'配置Odoo采购流程'、'设置采购审批'、'供应商价格表'或'三方匹配'时使用。"
risk: safe
source: "self"
---

# Odoo 采购工作流

## 概述

本技能引导你完成完整的 Odoo 采购流程——从发送询价单(RFQ)到收货并匹配供应商账单。同时涵盖采购协议、产品上的供应商价格表、自动补货以及三方匹配控制。

## 使用场景

- 为新的 Odoo 实例配置采购流程
- 实施采购订单审批工作流（两级审批）
- 配置带数量折扣的供应商价格表
- 排查三方匹配中的账单/收货不一致问题

## 工作方式

1. **激活**：提及 `@odoo-purchase-workflow` 并描述你的采购场景。
2. **配置**：获取精确的 Odoo 菜单路径和逐字段配置指导。
3. **排查**：描述账单或收货问题，获取根因诊断。

## 示例

### 示例 1：标准 RFQ → PO → 收货 → 账单流程

```text
Step 1: Create RFQ
  Menu: Purchase → Orders → Requests for Quotation → New
  Vendor: Acme Supplies
  Add product lines with quantity and unit price

Step 2: Send RFQ to Vendor
  Click "Send by Email" → Vendor receives PDF with RFQ details

Step 3: Confirm as Purchase Order
  Click "Confirm Order" → Status changes to "Purchase Order"

Step 4: Receive Goods
  Click "Receive Products" → Validate received quantities
  (partial receipts are supported; PO stays open for remaining qty)

Step 5: Match Vendor Bill (3-Way Match)
  Click "Create Bill" → Bill pre-filled from PO quantities
  Verify: PO qty = Received qty = Billed qty
  Post Bill → Register Payment
```

### 示例 2：启用两级采购审批

```text
Menu: Purchase → Configuration → Settings

Purchase Order Approval:
  ☑ Purchase Order Approval
  Minimum Order Amount: $5,000

Result:
  Orders ≤ $5,000  → Confirm directly to PO
  Orders > $5,000  → Status: "Waiting for Approval"
                     A purchase manager must click "Approve"
```

### 示例 3：供应商价格表（产品上的数量阶梯定价）

```text
Vendor price lists are configured per product, not as a global menu.

Menu: Inventory → Products → [Select Product] → Purchase Tab
  → Vendor Pricelist section → Add a line

Vendor: Acme Supplies
Currency: USD
Price:    $12.00
Min. Qty: 1

Add another line for quantity discount:
Min. Qty: 100 → Price: $10.50   (12.5% discount)
Min. Qty: 500 → Price:  $9.00   (25% discount)

Result: Odoo automatically selects the right price on a PO
based on the ordered quantity for this vendor.
```

## 最佳实践

- ✅ **应该做：** 为超过公司审批阈值的订单启用**采购订单审批**。
- ✅ **应该做：** 对有年度预协商合同的长期供应商使用**采购协议（一揽子订单）**。
- ✅ **应该做：** 在产品上设置**供应商前置时间**（Purchase 选项卡），以便 Odoo 准确安排到货日期。
- ✅ **应该做：** 将**账单控制**策略设置为"基于收货数量"（而非订单数量），以确保三方匹配准确。
- ❌ **不应该做：** 在价格谈妥之前确认 PO——先使用草稿/询价单状态进行谈判。
- ❌ **不应该做：** 在未关联收货的情况下过账供应商账单——绕过三方匹配会导致账务差异。
- ❌ **不应该做：** 删除已收货的采购订单——应将其归档，以保留库存和账务记录。

## 局限性

- 不涵盖**委外采购流程**——委外需要制造模块和委外 BOM 类型。
- **基于 EDI 的订单交换**（自动 PO 导入/导出）需要自定义集成——可使用 `@odoo-edi-connector`。
- 供应商价格表的货币转换依赖 Odoo 中生效的**汇率**；汇率需保持更新以确保准确。
- **两级审批**是二元阈值；更复杂的审批矩阵（按部门、多层级）需要自定义开发或使用审批应用。