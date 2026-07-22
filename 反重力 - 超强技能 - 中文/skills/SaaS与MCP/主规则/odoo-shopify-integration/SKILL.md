---
name: odoo-shopify-integration
description: "将 Odoo 与 Shopify 连接：使用 Shopify API 和 Odoo 外部 API 或连接器模块同步产品、库存、订单和客户数据。当用户要求'集成 Odoo 和 Shopify'、'同步 Shopify 订单到 Odoo'、'Odoo Shopify 对接'时使用。"
risk: unknown
source: community
---

# Odoo ↔ Shopify 集成

## 概述

本技能指导你完成 Odoo 与 Shopify 的集成——同步产品目录、实时库存水平、新到订单和客户数据。涵盖使用官方 Odoo Shopify 连接器（企业版）和通过 Shopify REST + Odoo XMLRPC API 构建自定义集成两种方式。

## 适用场景

- 在 Shopify 上销售，同时在 Odoo 中管理库存。
- 从 Shopify 购买自动创建 Odoo 销售订单。
- 保持 Odoo 库存水平与 Shopify 产品可用性同步。
- 将 Shopify 产品变体映射到 Odoo 产品模板。

## 工作流程

1. **激活**：提及 `@odoo-shopify-integration` 并描述你的同步场景。
2. **设计**：接收数据流架构和字段映射。
3. **构建**：获取 Shopify webhook 接收器和 Odoo API 调用器的代码片段。

## 数据流架构

```
SHOPIFY                          ODOO
--------                         ----
Product Catalog <──────sync──────  Product Templates + Variants
Inventory Level <──────sync──────  Stock Quants (real-time)
New Order       ───────push──────> Sale Order (auto-confirmed)
Customer        ───────push──────> res.partner (created if new)
Fulfillment     <──────push──────  Delivery Order validated
```

## 示例

### 示例 1：为 Shopify 订单推送 Odoo 销售订单（Python）

```python
import xmlrpc.client, requests

# Odoo connection
odoo_url = "https://myodoo.example.com"
db, uid, pwd = "my_db", 2, "api_key"
models = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object")

def create_odoo_order_from_shopify(shopify_order):
    # Find or create customer
    partner = models.execute_kw(db, uid, pwd, 'res.partner', 'search_read',
        [[['email', '=', shopify_order['customer']['email']]]],
        {'fields': ['id'], 'limit': 1}
    )
    partner_id = partner[0]['id'] if partner else models.execute_kw(
        db, uid, pwd, 'res.partner', 'create', [{
            'name': shopify_order['customer']['first_name'] + ' ' + shopify_order['customer']['last_name'],
            'email': shopify_order['customer']['email'],
        }]
    )

    # Create Sale Order
    order_id = models.execute_kw(db, uid, pwd, 'sale.order', 'create', [{
        'partner_id': partner_id,
        'client_order_ref': f"Shopify #{shopify_order['order_number']}",
        'order_line': [(0, 0, {
            'product_id': get_odoo_product_id(line['sku']),
            'product_uom_qty': line['quantity'],
            'price_unit': float(line['price']),
        }) for line in shopify_order['line_items']],
    }])
    return order_id

def get_odoo_product_id(sku):
    result = models.execute_kw(db, uid, pwd, 'product.product', 'search_read',
        [[['default_code', '=', sku]]], {'fields': ['id'], 'limit': 1})
    return result[0]['id'] if result else False
```

### 示例 2：Shopify Webhook 实时订单处理

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/webhook/shopify/orders', methods=['POST'])
def shopify_order_webhook():
    shopify_order = request.json
    order_id = create_odoo_order_from_shopify(shopify_order)
    return {"odoo_order_id": order_id}, 200
```

## 最佳实践

- ✅ **推荐**：使用 Shopify 的 **webhook 系统**进行实时订单同步，而非轮询。
- ✅ **推荐**：使用 **SKU / 内部参考编号** 作为两个系统之间的唯一匹配键。
- ✅ **推荐**：在处理任何请求体之前，验证 Shopify webhook 的 HMAC 签名。
- ❌ **避免**：在没有"主系统"的情况下同时从两个系统同步库存——选定一个作为唯一数据源。
- ❌ **避免**：使用 Shopify 产品 ID 作为匹配键——应使用跨平台稳定的 SKU。

## 限制

- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出替代针对特定环境的验证、测试或专家审查。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
