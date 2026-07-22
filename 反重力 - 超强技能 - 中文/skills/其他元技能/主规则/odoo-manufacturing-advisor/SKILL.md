---
name: odoo-manufacturing-advisor
description: "Odoo 制造模块专家指南：物料清单（BoM）、工作中心、工艺路线、MRP 计划和生产订单工作流。当用户要求配置或优化 Odoo 制造模块时使用。"
risk: safe
source: "self"
---

# Odoo 制造模块顾问

## 概述

本技能帮助你配置和优化 Odoo 制造模块（MRP）。涵盖物料清单（BoM）、工作中心、工艺路线操作、生产订单生命周期和物料需求计划（MRP）运行，确保物料供应充足。

## 使用场景

- 创建或构建成品的物料清单
- 配置工作中心的产能和效率参数
- 运行 MRP 自动生成采购订单和生产订单
- 排查生产订单差异或组件可用性问题

## 使用方法

1. **激活**：提及 `@odoo-manufacturing-advisor` 并描述你的制造场景
2. **配置**：获取 BoM 设置、工艺路线和 MRP 配置的分步指导
3. **计划**：获取运行 MRP 和解读采购异常消息的指导

## 示例

### 示例 1：创建物料清单

```text
Menu: Manufacturing → Products → Bills of Materials → New

Product: Finished Widget v2
BoM Type: Manufacture This Product
Quantity: 1 (produce 1 unit per BoM)

Components Tab:
  - Raw Plastic Sheet  | Qty: 0.5  | Unit: kg
  - Steel Bolt M6      | Qty: 4    | Unit: Units
  - Rubber Gasket      | Qty: 1    | Unit: Units

Operations Tab (requires "Work Orders" enabled in MFG Settings):
  - Operation: Injection Molding | Work Center: Press A   | Duration: 30 min
  - Operation: Assembly          | Work Center: Line 1    | Duration: 15 min
```

> **BoM 类型说明：**
>
> - **Manufacture This Product** — 标准生产 BoM，创建制造订单
> - **Kit** — 作为套件销售；组件分别交付（不创建制造订单）
> - **Subcontracting** — 组件发送给外包商，由其返回成品

### 示例 2：配置工作中心

```text
Menu: Manufacturing → Configuration → Work Centers → New

Work Center: CNC Machine 1
Working Hours: Standard 40h/week
Time Efficiency: 85%      (machine downtime factored in; 85% = 34 effective hrs/week)
Capacity: 2               (can run 2 production operations simultaneously)
OEE Target: 90%           (Overall Equipment Effectiveness KPI target)
Costs per Hour: $75.00    (used for manufacturing cost reporting)
```

### 示例 3：运行 MRP 计划器

```text
The MRP scheduler runs automatically via a daily cron job.
To trigger it manually:

Menu: Inventory → Operations → Replenishment → Run Scheduler
(or Manufacturing → Planning → Replenishment in some versions)

After running, review procurement exceptions:
Menu: Inventory → Operations → Replenishment

Message Types:
  "Replenish"   — Stock is below minimum; needs a PO or MO
  "Reschedule"  — An order's scheduled date conflicts with demand
  "Cancel"      — Demand no longer exists; the order can be cancelled
```

## 最佳实践

- ✅ **推荐**：在制造设置中启用 **Work Orders**，以使用工艺路线和每道工序的时间追踪
- ✅ **推荐**：对多配置产品（颜色、尺寸、电压）使用 **BoM with variants**（通过产品属性），避免重复创建 BoM
- ✅ **推荐**：为组件设置 **Lead Times**（供应商提前期 + 安全提前期），让 MRP 提前安排采购订单
- ✅ **推荐**：生产中丢弃不良组件时使用 **Scrap Orders**，切勿手动调整库存
- ❌ **禁止**：为 MRP 管理的物料手动创建采购订单——仅在有充分理由时才覆盖 MRP 建议
- ❌ **禁止**：混淆 **Kit** 和 **Manufacture This Product**——Kit 类型永远不会创建制造订单

## 限制

- 本技能针对 **Odoo Manufacturing (mrp)** 模块。**Maintenance**、**PLM**（产品生命周期管理）和 **Quality** 模块属于独立的企业版模块，此处不涉及
- **Subcontracting** 工作流（将组件发送给第三方制造商）有额外的收货和估值步骤，此处未详述
- 生产中的 **批次/序列号追溯**（追踪每个制造订单消耗的批次）会增加复杂度；全面推广前请先小批量测试
- MRP 计算假设需求来自 **Sale Orders** 和 **Reordering Rules**——来自外部系统的预测需要自定义集成