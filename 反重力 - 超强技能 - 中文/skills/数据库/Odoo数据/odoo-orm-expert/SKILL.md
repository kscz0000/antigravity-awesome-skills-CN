---
name: odoo-orm-expert
description: "精通 Odoo ORM 模式：search、browse、create、write、domain 过滤器、计算字段和性能安全的查询技术。当用户要求编写 Odoo ORM 查询、优化数据库操作或调试 Odoo 数据模型时使用。"
risk: safe
source: "self"
---

# Odoo ORM 专家

## 概述

本技能深入讲解 Odoo 的对象关系映射器（ORM）。涵盖记录的读写操作、构建 domain 过滤器、处理关联字段，以及避免 N+1 查询等常见性能陷阱。

## 使用场景

- 编写 `search()`、`browse()`、`create()`、`write()` 或 `unlink()` 调用
- 为视图或服务器动作构建复杂的 domain 过滤器
- 实现计算字段、存储字段和关联字段
- 调试慢查询或优化批量操作

## 工作流程

1. **激活**：提及 `@odoo-orm-expert` 并描述你需要的数据操作
2. **获取代码**：接收正确、地道的 Odoo ORM 代码及解释
3. **优化**：请求对现有 ORM 代码进行性能审查

## 示例

### 示例 1：使用 Domain 过滤器搜索

```python
# Find all confirmed sale orders for a specific customer, created this year
import datetime

start_of_year = datetime.date.today().replace(month=1, day=1).strftime('%Y-%m-%d')

orders = self.env['sale.order'].search([
    ('partner_id', '=', partner_id),
    ('state', '=', 'sale'),
    ('date_order', '>=', start_of_year),
], order='date_order desc', limit=50)

# Note: pass dates as 'YYYY-MM-DD' strings in domains,
# NOT as fields.Date objects — the ORM serializes them correctly.
```

### 示例 2：计算字段

```python
total_order_count = fields.Integer(
    string='Total Orders',
    compute='_compute_total_order_count',
    store=True
)

@api.depends('sale_order_ids')
def _compute_total_order_count(self):
    for record in self:
        record.total_order_count = len(record.sale_order_ids)
```

### 示例 3：安全的批量写入（避免 N+1）

```python
# ✅ GOOD: One query for all records
partners = self.env['res.partner'].search([('country_id', '=', False)])
partners.write({'country_id': self.env.ref('base.us').id})

# ❌ BAD: Triggers a separate query per record
for partner in partners:
    partner.country_id = self.env.ref('base.us').id
```

## 最佳实践

- ✅ **推荐：** 在记录集上使用 `mapped()`、`filtered()` 和 `sorted()`，而非 Python 循环
- ✅ **推荐：** 谨慎使用 `sudo()`，仅在理解安全影响时使用
- ✅ **推荐：** 只需要计数时，优先使用 `search_count()` 而非 `len(search(...))`
- ✅ **推荐：** 使用 `with_context(...)` 传递上下文值，而非直接修改 `self.env.context`
- ❌ **禁止：** 在循环内调用 `search()` —— 这是 Odoo 头号性能杀手
- ❌ **禁止：** 除非绝对必要，否则不要使用原生 SQL；所有标准操作都用 ORM
- ❌ **禁止：** 将 Python `datetime`/`date` 对象直接传入 domain 元组 —— 始终转为 `'YYYY-MM-DD'` 字符串

## 限制

- 不深入涵盖 **`cr.execute()` 原生 SQL** 模式 —— SQL 级优化请使用 Odoo 性能调优技能
- **存储计算字段**在大规模场景下会产生显著的写入开销；本技能不涵盖分区策略
- 不涵盖**瞬态模型**（`models.TransientModel`）或向导模式
- 由于配置覆盖，ORM 行为在 Odoo SaaS 和本地部署版本之间可能存在细微差异