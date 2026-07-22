# 前置条件

## 两个 key，两种用途

Push ingestion 需要**两个单独的 Monte Carlo API key** — 一个用于推送数据，一个用于读取/验证数据。它们使用相同的头名称但不同的端点。

| Key | 用途 | 端点 |
|---|---|---|
| **Ingestion key** (scope=`Ingestion`) | 推送元数据、血缘、查询日志 | `https://integrations.getmontecarlo.com` |
| **GraphQL API key** | 验证推送的数据、运行管理 mutations | `https://api.getmontecarlo.com/graphql` |

两者使用以下方式认证：
```
x-mcd-id:    <key-id>
x-mcd-token: <key-secret>
```

两者的密钥在创建时**仅显示一次** — 请立即安全存储。

---

## 创建 Ingestion key（用于推送）

使用 Monte Carlo CLI：

```bash
montecarlo integrations create-key \
  --scope Ingestion \
  --description "Push ingestion key"
```

输出：
```
Key id:     <id>
Key secret: <secret>    ← only shown once
```

如需安装 CLI：
```bash
pip install montecarlodata
montecarlo configure   # enter your API key when prompted
```

**可选 — 限定到特定仓库：**
如果你希望 key 仅适用于一个仓库 UUID，请改用 GraphQL mutation：

```graphql
mutation {
  createIntegrationKey(
    description: "Push key for warehouse XYZ"
    scope: Ingestion
    warehouseIds: ["<warehouse-uuid>"]
  ) {
    key { id secret }
  }
}
```

---

## 创建 GraphQL API key（用于验证）

1. 前往 **https://getmontecarlo.com/settings/api**
2. 点击 **Add**
3. 选择 key 类型（个人或账户级 — 账户级需要 Account Owner 角色）
4. 立即复制 **Key ID** 和 **Secret**

GraphQL 端点是：`https://api.getmontecarlo.com/graphql`

测试：
```bash
curl -s -X POST https://api.getmontecarlo.com/graphql \
  -H "x-mcd-id: <id>" \
  -H "x-mcd-token: <secret>" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ getUser { email } }"}' | python3 -m json.tool
```

---

## 查找你的仓库（资源）UUID

Ingestion key 需要引用正确的 MC 资源 UUID。查找方法：

```graphql
query {
  getUser {
    account {
      warehouses {
        uuid
        name
        connectionType
      }
    }
  }
}
```

或在 MC UI 中：**Settings → Integrations** → 点击仓库 → 从 URL 复制 UUID。

---

## 安装 pycarlo（可选）

pycarlo SDK 简化了 push 调用，但不是必需的。你也可以通过 HTTP/curl 直接调用 push API — 请参阅 `references/direct-http-api.md`。

```bash
pip install pycarlo
```

在脚本中初始化 ingestion 客户端：

```python
from pycarlo.core import Client, Session
from pycarlo.features.ingestion import IngestionService

client = Client(session=Session(
    mcd_id="<ingestion-key-id>",
    mcd_token="<ingestion-key-secret>",
    scope="Ingestion",
))
service = IngestionService(mc_client=client)
```

从环境变量加载凭据（推荐）：

```python
import os
service = IngestionService(mc_client=Client(session=Session(
    mcd_id=os.environ["MCD_INGEST_ID"],
    mcd_token=os.environ["MCD_INGEST_TOKEN"],
    scope="Ingestion",
)))
```

---

## 环境变量约定

脚本模板默认使用以下环境变量名称：

| 变量 | Key 类型 | 使用者 |
|---|---|---|
| `MCD_INGEST_ID` | Ingestion key ID | push 和 collect_and_push 脚本 |
| `MCD_INGEST_TOKEN` | Ingestion key secret | push 和 collect_and_push 脚本 |
| `MCD_ID` | GraphQL API key ID | 验证脚本、斜杠命令 |
| `MCD_TOKEN` | GraphQL API key secret | 验证脚本、斜杠命令 |
| `MCD_RESOURCE_UUID` | 仓库 UUID | 所有脚本 |