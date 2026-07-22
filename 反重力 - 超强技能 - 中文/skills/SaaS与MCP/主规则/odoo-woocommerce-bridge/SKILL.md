---
name: odoo-woocommerce-bridge
description: "通过 WooCommerce REST API 和 Odoo 外部 API 同步 Odoo 与 WooCommerce 的产品、库存、订单和客户数据。当用户要求'同步 Odoo 和 WooCommerce'时使用。"
risk: unknown
source: community
---

# Odoo ↔ WooCommerce 桥接

## 概述

本技能指导你在 Odoo（后台 ERP 系统）和 WooCommerce（WordPress 在线商店）之间构建可靠的同步桥接。涵盖产品目录同步、实时库存更新、订单导入和客户记录管理。

## 适用场景

- 使用 WooCommerce 商店运营，同时用 Odoo 管理库存和履约。
- 将 WooCommerce 订单自动拉取到 Odoo 中生成销售订单。
- 保持 WooCommerce 商品库存与 Odoo 仓库实时同步。
- 将 WooCommerce 订单状态映射到 Odoo 的发货状态。

## 工作方式

1. **激活**：提及 `@odoo-woocommerce-bridge` 并描述你的同步需求。
2. **设计**：获取 WooCommerce 与 Odoo 对象之间的字段映射表。
3. **构建**：接收基于 WooCommerce REST API 的 Python 集成脚本。

## 字段映射：WooCommerce → Odoo

| WooCommerce | Odoo |
|---|---|
| `products` | `product.template` + `product.product` |
| `orders` | `sale.order` + `sale.order.line` |
| `customers` | `res.partner` |
| `stock_quantity` | `stock.quant` |
| `sku` | `product.product.default_code` |
| `order status: processing` | Sale Order: `sale`（已确认） |
| `order status: completed` | Delivery: `done` |

## 示例

### 示例 1：将 WooCommerce 订单拉取到 Odoo（Python）

```python
from woocommerce import API
import xmlrpc.client
import os

# WooCommerce client
wcapi = API(
    url=os.getenv("WC_URL", "https://mystore.com"),
    consumer_key=os.getenv("WC_KEY"),
    consumer_secret=os.getenv("WC_SECRET"),
    version="wc/v3"
)

# Odoo client
odoo_url = os.getenv("ODOO_URL", "https://myodoo.example.com")
db = os.getenv("ODOO_DB", "my_db")
uid = int(os.getenv("ODOO_UID", "2"))
pwd = os.getenv("ODOO_PASSWORD")
models = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object")


def sync_orders():
    # Get unprocessed WooCommerce orders
    orders = wcapi.get("orders", params={"status": "processing", "per_page": 50}).json()

    for wc_order in orders:
        # Find or create Odoo partner
        email = wc_order['billing']['email']
        partner = models.execute_kw(db, uid, pwd, 'res.partner', 'search',
            [[['email', '=', email]]])
        if not partner:
            partner_id = models.execute_kw(db, uid, pwd, 'res.partner', 'create', [{
                'name': f"{wc_order['billing']['first_name']} {wc_order['billing']['last_name']}",
                'email': email,
                'phone': wc_order['billing']['phone'],
                'street': wc_order['billing']['address_1'],
                'city': wc_order['billing']['city'],
            }])
        else:
            partner_id = partner[0]

        # Create Sale Order in Odoo
        order_lines = []
        for item in wc_order['line_items']:
            product = models.execute_kw(db, uid, pwd, 'product.product', 'search',
                [[['default_code', '=', item['sku']]]])
            if product:
                order_lines.append((0, 0, {
                    'product_id': product[0],
                    'product_uom_qty': item['quantity'],
                    'price_unit': float(item['price']),
                }))

        models.execute_kw(db, uid, pwd, 'sale.order', 'create', [{
            'partner_id': partner_id,
            'client_order_ref': f"WC-{wc_order['number']}",
            'order_line': order_lines,
        }])

        # Mark WooCommerce order as on-hold (processed by Odoo)
        wcapi.put(f"orders/{wc_order['id']}", {"status": "on-hold"})
```

### 示例 2：将 Odoo 库存推送到 WooCommerce

```python
def sync_inventory_to_woocommerce():
    # Get all products with a SKU from Odoo
    products = models.execute_kw(db, uid, pwd, 'product.product', 'search_read',
        [[['default_code', '!=', False], ['type', '=', 'product']]],
        {'fields': ['default_code', 'qty_available']}
    )

    for product in products:
        sku = product['default_code']
        qty = int(product['qty_available'])

        # Update WooCommerce by SKU
        wc_products = wcapi.get("products", params={"sku": sku}).json()
        if wc_products:
            wcapi.put(f"products/{wc_products[0]['id']}", {
                "stock_quantity": qty,
                "manage_stock": True,
            })
```

## 最佳实践

- ✅ **推荐**：使用 **SKU** 作为关联 WooCommerce 产品与 Odoo 产品的唯一标识。
- ✅ **推荐**：按**定时计划**（每 15-30 分钟）运行库存同步，而非实时同步，以避免触发速率限制。
- ✅ **推荐**：将所有 API 调用和错误记录到数据库表中，便于调试。
- ❌ **避免**：重复处理同一个 WooCommerce 订单——导入后立即标记为已处理。
- ❌ **避免**：将草稿或已取消的 WooCommerce 订单同步到 Odoo——通过 `status = processing` 或 `completed` 进行过滤。

## 使用限制

- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为特定环境下的验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请暂停并请求澄清。
