---
name: odoo-edi-connector
description: "Odoo EDI 集成指南：X12、EDIFACT 文档映射、合作伙伴接入及自动化订单处理。当用户要求'配置 EDI 连接器'、'映射 X12 文档到 Odoo'、'设置 EDI 850/856/810'或'自动化 EDI 订单流程'时使用。"
risk: unknown
source: community
---

# Odoo EDI Connector

## 概述

电子数据交换（EDI）是 B2B 文档自动化交换的标准——采购订单、发票、ASN（提前发货通知）。本技能指导你完成 EDI 事务（ANSI X12 或 EDIFACT）到 Odoo 业务对象的映射、交易伙伴配置的设置，以及入站/出站文档流程的自动化。

## 使用场景

- 零售伙伴要求使用 EDI 850（采购订单）才能与你开展业务。
- 货物发出时需要发送 EDI 856（ASN）。
- 从 Odoo 已确认的发货自动生成 EDI 810（发票）。
- 为新交易伙伴映射 EDI 字段到 Odoo 字段。

## 工作方式

1. **激活**：提及 `@odoo-edi-connector` 并指定 EDI 事务集和交易伙伴。
2. **映射**：获取 EDI 段与 Odoo 字段之间的完整映射表。
3. **自动化**：获得 Python 代码来解析传入的 EDI 文件并创建 Odoo 记录。

## EDI ↔ Odoo 对象映射

| EDI 事务 | Odoo 对象 |
|---|---|
| 850 采购订单 | `sale.order`（入站客户 PO） |
| 855 PO 确认 | 确认邮件 / SO 确认 |
| 856 ASN（提前发货通知） | `stock.picking`（发货单） |
| 810 发票 | `account.move`（客户发票） |
| 846 库存查询 | `product.product` 库存水平 |
| 997 功能确认 | 自动接收确认 |

## 示例

### 示例 1：解析 EDI 850 并创建 Odoo 销售订单（Python）

```python
from pyx12 import x12file  # pip install pyx12
from datetime import datetime

import xmlrpc.client
import os

odoo_url = os.getenv("ODOO_URL")
db = os.getenv("ODOO_DB")
pwd = os.getenv("ODOO_API_KEY") 
uid = int(os.getenv("ODOO_UID", "2"))

models = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object")

def process_850(edi_file_path):
    """Parse X12 850 Purchase Order and create Odoo Sale Order"""
    with x12file.X12File(edi_file_path) as f:
        for transaction in f.get_transaction_sets():
            # Extract header info (BEG segment)                     
            po_number = transaction['BEG'][3]    # Purchase Order Number                                                    
            po_date   = transaction['BEG'][5]    # Purchase Order Date 

            # IDEMPOTENCY CHECK: Verify PO doesn't already exist in Odoo
            existing = models.execute_kw(db, uid, pwd, 'sale.order', 'search', [
                [['client_order_ref', '=', po_number]]
            ])
            if existing:
                print(f"Skipping: PO {po_number} already exists.")
                continue 

            # Extract partner (N1 segment — Buyer)


                        # Extract partner (N1 segment — Buyer)                  
            partner_name = transaction.get_segment('N1')[2] if transaction.get_segment('N1') else "Unknown"                                                                             
            
            # Find partner in Odoo                                  
            partner = models.execute_kw(db, uid, pwd, 'res.partner', 'search',                                                  
                                [[['name', 'ilike', partner_name]]])                
            
            if not partner:
                print(f"Error: Partner '{partner_name}' not found. Skipping transaction.")
                continue
                
            partner_id = partner[0]

            # Extract line items (PO1 segments)
            order_lines = []
            for po1 in transaction.get_segments('PO1'):
                sku     = po1[7]    # Product ID
                qty     = float(po1[2])
                price   = float(po1[4])

                product = models.execute_kw(db, uid, pwd, 'product.product', 'search',
                    [[['default_code', '=', sku]]])
                if product:
                    order_lines.append((0, 0, {
                        'product_id': product[0],
                        'product_uom_qty': qty,
                        'price_unit': price,
                    }))

            # Create Sale Order
            if partner_id and order_lines:
                models.execute_kw(db, uid, pwd, 'sale.order', 'create', [{
                    'partner_id': partner_id,
                    'client_order_ref': po_number,
                    'order_line': order_lines,
                }])
```

### 示例 2：发送 EDI 997 确认

```python
def generate_997(isa_control, gs_control, transaction_control):
    """Generate a functional acknowledgment for received EDI"""
    today = datetime.now().strftime('%y%m%d')
    return f"""ISA*00*          *00*          *ZZ*YOURISAID      *ZZ*PARTNERISAID   *{today}*1200*^*00501*{isa_control}*0*P*>~
GS*FA*YOURGID*PARTNERGID*{today}*1200*{gs_control}*X*005010X231A1~
ST*997*0001~
AK1*PO*{gs_control}~
AK9*A*1*1*1~
SE*4*0001~
GE*1*{gs_control}~
IEA*1*{isa_control}~"""
```

## 最佳实践

- ✅ **应该做**：在处理前将每笔原始 EDI 事务存储到审计日志表。
- ✅ **应该做**：在收到事务后 24 小时内发送 **997 功能确认**。
- ✅ **应该做**：上线前与交易伙伴协商测试周期——使用测试 ISA 限定符 `T`。
- ❌ **不要做**：在 Web 请求中同步处理 EDI 文件——应排队进行异步处理。
- ❌ **不要做**：硬编码交易伙伴限定符——存储在每个伙伴的配置表中。

## 限制

- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。