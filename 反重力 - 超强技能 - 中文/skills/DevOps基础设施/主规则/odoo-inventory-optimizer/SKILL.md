---
name: odoo-inventory-optimizer
description: "Odoo 库存管理专家指南：库存计价（FIFO/AVCO）、补货规则、上架策略、路线及多仓库配置。当用户要求优化 Odoo 库存、配置补货规则或设置仓库路线时使用。"
risk: safe
source: "self"
---

# Odoo 库存优化器

## 概述

本技能帮助你配置和优化 Odoo 库存模块，提升准确性、效率和可追溯性。涵盖库存计价方法、补货规则、上架策略、仓库路线以及多步骤流程（收货 → 质检 → 入库）。

## 使用场景

- 选择并配置 FIFO 与 AVCO 库存计价方法。
- 设置最低库存补货规则，防止缺货。
- 设计多步骤仓库流程（两步收货、三步发货）。
- 配置上架规则，将产品定向到指定存储位置。
- 排查负库存、计价异常或库存移动缺失问题。

## 使用方式

1. **激活**：提及 `@odoo-inventory-optimizer` 并描述你的仓库场景。
2. **配置**：获取带精确 Odoo 菜单路径的分步配置指引。
3. **优化**：获得补货规则和库存准确性的改进建议。

## 示例

### 示例 1：启用 FIFO 库存计价

```text
Menu: Inventory → Configuration → Settings

Enable: Storage Locations
Enable: Multi-Step Routes
Costing Method: (set per Product Category, not globally)

Menu: Inventory → Configuration → Product Categories → Edit

  Category: All / Physical Goods
  Costing Method: First In First Out (FIFO)
  Inventory Valuation: Automated
  Account Stock Valuation: [Balance Sheet inventory account]
  Account Stock Input:   [Stock Received Not Billed]
  Account Stock Output:  [Stock Delivered Not Invoiced]
```

### 示例 2：设置最小/最大补货规则

```text
Menu: Inventory → Operations → Replenishment → New

Product: Office Paper A4
Location: WH/Stock
Min Qty: 100   (trigger reorder when stock falls below this)
Max Qty: 500   (purchase up to this quantity)
Multiple Qty: 50  (always order in multiples of 50)
Route: Buy    (triggers a Purchase Order automatically)
       or Manufacture (triggers a Manufacturing Order)
```

### 示例 3：配置上架规则

```text
Menu: Inventory → Configuration → Putaway Rules → New

Purpose: Direct products from WH/Input to specific bin locations

Rules:
  Product Category: Refrigerated Goods
    → Location: WH/Stock/Cold Storage

  Product: Laptop Model X
    → Location: WH/Stock/Electronics/Shelf A

  (leave Product blank to apply the rule to an entire category)

Result: When a receipt is validated, Odoo automatically suggests
the correct destination location per product or category.
```

### 示例 4：配置三步骤仓库发货

```text
Menu: Inventory → Configuration → Warehouses → [Your Warehouse]

Outgoing Shipments: Pick + Pack + Ship (3 steps)

Operations created automatically:
  PICK  — Move goods from storage shelf to packing area
  PACK  — Package items and print shipping label
  OUT   — Hand off to carrier / mark as shipped
```

## 最佳实践

- ✅ **建议**：对高价值或受管制物品（医疗器械、电子产品）使用**批次/序列号**。
- ✅ **建议**：至少每季度执行一次**实物盘点调整**（Inventory → Operations → Physical Inventory），修正账实差异。
- ✅ **建议**：为高频流转物料设置补货规则，自动生成采购订单。
- ✅ **建议**：在有多个存储区域的仓库启用**上架规则**——消除手动选择库位的错误。
- ❌ **避免**：在录入交易后切换库存计价方法（FIFO ↔ AVCO）——会导致历史成本数据失真。
- ❌ **避免**：使用"更新数量"修正库存错误——应始终使用库存调整功能以保留完整审计轨迹。
- ❌ **避免**：在不了解计价影响的情况下，将不同成本计算方法的产品类别混放在同一存储位置。

## 局限性

- **序列号追踪**在单件级别（每行一个序列号）会带来明显的界面开销；启用前请用大批量数据测试性能。
- 不涉及**到岸成本**（进口关税、运费分摊至产品成本）——需使用 `stock_landed_costs` 模块。
- **跨仓库调拨**存在路由复杂性（中转仓、公司间开票），此处未完全覆盖。
- 自动库存计价依赖**会计模块**；未安装该模块的社区版无法自动过账库存分录。
