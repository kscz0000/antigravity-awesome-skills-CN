---
name: odoo-rpc-api
description: "Odoo 外部 JSON-RPC 和 XML-RPC API 专家。涵盖认证、模型调用、记录 CRUD 以及 Python、JavaScript 和 curl 的实际集成示例。当用户要求'odoo-rpc-api'时使用。"
risk: safe
source: "self"
---

# Odoo RPC API

## 概述

Odoo 通过 JSON-RPC 和 XML-RPC 暴露强大的外部 API，允许任何外部应用程序读取、创建、更新和删除记录。本技能指导您完成认证、调用模型和构建健壮的集成。

## 何时使用此技能

- 将外部应用（如 Django、Node.js、移动应用）连接到 Odoo。
- 运行自动化脚本从 Odoo 导入/导出数据。
- 在 Odoo 和第三方平台之间构建中间件层。
- 调试 API 认证或权限错误。

## 工作原理

1. **激活**：提及 `@odoo-rpc-api` 并描述所需的集成。
2. **生成**：获取可直接复制粘贴的 RPC 调用代码（Python、JavaScript 或 curl）。
3. **调试**：粘贴错误并获取诊断结果和修正后的调用。

## 示例

### 示例 1：认证并读取记录（Python）

```python
import xmlrpc.client

url = 'https://myodoo.example.com'
db = 'my_database'
username = 'admin'
password = 'my_api_key'  # 生产环境请使用 API 密钥而非密码

# 步骤 1：认证
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
print(f"Authenticated as UID: {uid}")

# 步骤 2：调用模型
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# 搜索已确认的销售订单
orders = models.execute_kw(db, uid, password,
    'sale.order', 'search_read',
    [[['state', '=', 'sale']]],
    {'fields': ['name', 'partner_id', 'amount_total'], 'limit': 10}
)
for order in orders:
    print(order)
```

### 示例 2：创建记录（Python）

```python
new_partner_id = models.execute_kw(db, uid, password,
    'res.partner', 'create',
    [{'name': 'Acme Corp', 'email': 'info@acme.com', 'is_company': True}]
)
print(f"Created partner ID: {new_partner_id}")
```

### 示例 3：通过 curl 使用 JSON-RPC

```bash
curl -X POST https://myodoo.example.com/web/dataset/call_kw \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 1,
    "params": {
      "model": "res.partner",
      "method": "search_read",
      "args": [[["is_company", "=", true]]],
      "kwargs": {"fields": ["name", "email"], "limit": 5}
    }
  }'
# 注意：JSON-RPC 2.0 规范要求 "id" 字段用于关联响应。
# Odoo 16+ 也支持 /web/dataset/call_kw 端点，
# 但模型方法调用推荐使用 /web/dataset/call_kw。
```

## 最佳实践

- ✅ **推荐**：使用 **API 密钥**（设置 → 技术 → API 密钥）替代密码——Odoo 14+ 可用。
- ✅ **推荐**：使用 `search_read` 而非 `search` + `read` 以减少网络往返。
- ✅ **推荐**：始终处理连接错误，并在生产环境中实现带指数退避的重试逻辑。
- ✅ **推荐**：将凭据存储在环境变量或密钥管理器（如 AWS Secrets Manager、`.env` 文件）中。
- ❌ **禁止**：在脚本中硬编码密码或 API 密钥——定期轮换并使用环境变量。
- ❌ **禁止**：在未批量处理的情况下紧密循环调用 API——批量操作可显著降低服务器负载。
- ❌ **禁止**：使用主管理员密码进行 API 集成——创建具有最小权限的专用集成用户。

## 局限性

- 不涵盖 **OAuth2 或基于会话 Cookie 的认证**——示例仅使用 API 密钥（令牌）认证。
- **速率限制**未内置于 Odoo XMLRPC 层；您必须在客户端实现限流。
- XML-RPC 端点（`/xmlrpc/2/`）不支持文件上传——对于二进制数据，请通过 JSON-RPC 使用基于 REST 的 `ir.attachment` 模型。
- Odoo.sh（SaaS）可能会根据订阅计划阻止某些 API 调用；请确认您的订阅支持外部 API 访问。