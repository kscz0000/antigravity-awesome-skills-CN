# 高级功能 - WhatsApp Cloud API

WhatsApp Business 平台高级功能指南：Flows、Commerce、Channels、Click-to-WhatsApp Ads 和 Status Tracking。

---

## 目录

1. [WhatsApp Flows](#whatsapp-flows)
2. [商务与商品目录](#commerce-e-catalogo)
3. [WhatsApp 频道](#whatsapp-channels)
4. [Click-to-WhatsApp 广告](#click-to-whatsapp-ads)
5. [状态跟踪](#status-tracking)
6. [分析与报表](#analytics-e-reporting)

---

## WhatsApp Flows

WhatsApp Flows 允许您在 WhatsApp 内创建多屏交互式表单。客户可以填写字段、选择选项并提交数据，无需离开应用。

### 何时使用

- 注册和登记
- 预约和预订
- NPS 调查和反馈
- 带选项的产品选择
- 带有结构化字段的支持表单
- 销售线索资格问卷

### Flow 的 JSON 结构

Flow 由 **screens**（屏幕）和 **components**（字段）组成：

```json
{
  "version": "3.0",
  "screens": [
    {
      "id": "SCREEN_1",
      "title": "Agendamento",
      "data": {},
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Agende sua consulta"
          },
          {
            "type": "TextInput",
            "name": "customer_name",
            "label": "Seu nome completo",
            "required": true,
            "input-type": "text"
          },
          {
            "type": "DatePicker",
            "name": "appointment_date",
            "label": "Data desejada",
            "required": true,
            "min-date": "1709251200000",
            "max-date": "1711929600000"
          },
          {
            "type": "Dropdown",
            "name": "service_type",
            "label": "Tipo de servico",
            "required": true,
            "data-source": [
              { "id": "consulta", "title": "Consulta" },
              { "id": "retorno", "title": "Retorno" },
              { "id": "exame", "title": "Exame" }
            ]
          },
          {
            "type": "Footer",
            "label": "Confirmar",
            "on-click-action": {
              "name": "navigate",
              "next": { "type": "screen", "name": "SCREEN_2" },
              "payload": {
                "customer_name": "${form.customer_name}",
                "appointment_date": "${form.appointment_date}",
                "service_type": "${form.service_type}"
              }
            }
          }
        ]
      }
    },
    {
      "id": "SCREEN_2",
      "title": "Confirmacao",
      "terminal": true,
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Confirme seus dados"
          },
          {
            "type": "TextBody",
            "text": "Nome: ${data.customer_name}\nData: ${data.appointment_date}\nServico: ${data.service_type}"
          },
          {
            "type": "Footer",
            "label": "Confirmar Agendamento",
            "on-click-action": {
              "name": "complete",
              "payload": {
                "customer_name": "${data.customer_name}",
                "appointment_date": "${data.appointment_date}",
                "service_type": "${data.service_type}"
              }
            }
          }
        ]
      }
    }
  ]
}
```

### 可用组件

| 组件              | 描述                            | 主要字段                            |
|------------------|--------------------------------|-----------------------------------|
| TextHeading      | 章节标题                        | text                              |
| TextBody         | 描述性文本                      | text                              |
| TextInput        | 文本输入框                      | name, label, input-type           |
| TextArea         | 多行文本区域                    | name, label                       |
| DatePicker       | 日期选择器                      | name, label, min-date, max-date   |
| Dropdown         | 下拉列表                        | name, label, data-source          |
| RadioButtonsGroup| 单选按钮组                      | name, label, data-source          |
| CheckboxGroup    | 复选框组                        | name, label, data-source          |
| OptIn            | 接受条款复选框                  | name, label                       |
| Footer           | 操作/导航按钮                   | label, on-click-action            |

### 通过 API 发送 Flow

```typescript
async function sendFlow(to: string, flowId: string, screenId: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'flow',
      header: { type: 'text', text: 'Agendar Consulta' },
      body: { text: 'Preencha o formulário abaixo para agendar.' },
      footer: { text: 'Seus dados são protegidos' },
      action: {
        name: 'flow',
        parameters: {
          flow_message_version: '3',
          flow_id: flowId,
          flow_cta: 'Agendar',
          flow_action: 'navigate',
          flow_action_payload: {
            screen: screenId,
            data: {}
          }
        }
      }
    }
  });
}
```

### 接收 Flow 回复

```typescript
function handleFlowResponse(message: IncomingMessage): Record<string, any> | null {
  if (message.interactive?.type === 'nfm_reply') {
    return JSON.parse(message.interactive.nfm_reply.response_json);
    // 例如：{ customer_name: "João", appointment_date: "2026-03-01", service_type: "consulta" }
  }
  return null;
}
```

### 创建 Flows

Flows 可以通过两种方式创建：
1. **可视化构建器** - 在 WhatsApp Manager 中拖放组件
2. **JSON 编辑器** - 直接编辑 JSON 以实现完全控制

---

## 商务与商品目录

### 配置目录

WhatsApp 目录最多支持链接到您业务资料的 **500 个商品**。

**配置：**
1. 打开 WhatsApp Manager
2. 前往 Account Tools → Catalog
3. 添加商品：名称、描述、价格、图片、URL

### 发送单品消息

```typescript
async function sendSingleProduct(to: string, catalogId: string, productId: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'product',
      body: { text: 'Confira este produto!' },
      footer: { text: 'Responda para comprar' },
      action: {
        catalog_id: catalogId,
        product_retailer_id: productId
      }
    }
  });
}
```

### 发送多品消息

```typescript
async function sendMultiProduct(
  to: string,
  catalogId: string,
  sections: Array<{ title: string; product_items: Array<{ product_retailer_id: string }> }>
): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'product_list',
      header: { type: 'text', text: 'Nossos Produtos' },
      body: { text: 'Selecione os produtos que deseja:' },
      footer: { text: 'Adicione ao carrinho' },
      action: {
        catalog_id: catalogId,
        sections
      }
    }
  });
}

// 使用示例：
await sendMultiProduct('5511999999999', 'CATALOG_ID', [
  {
    title: 'Eletronicos',
    product_items: [
      { product_retailer_id: 'SKU_001' },
      { product_retailer_id: 'SKU_002' }
    ]
  },
  {
    title: 'Acessorios',
    product_items: [
      { product_retailer_id: 'SKU_003' },
      { product_retailer_id: 'SKU_004' }
    ]
  }
]);
```

### 应用内结账

当客户选择商品并进行结账时，您将通过 webhook 收到：

```json
{
  "type": "order",
  "order": {
    "catalog_id": "CATALOG_ID",
    "product_items": [
      {
        "product_retailer_id": "SKU_001",
        "quantity": 2,
        "item_price": 99.90,
        "currency": "BRL"
      }
    ],
    "text": "Quero esses produtos"
  }
}
```

### 与库存同步

要保持目录更新：

```python
async def sync_inventory(catalog_id: str, products: list[dict]) -> None:
    """通过 Commerce Manager API 将库存与 WhatsApp 目录同步。"""
    for product in products:
        await update_product(
            catalog_id=catalog_id,
            product_id=product["sku"],
            data={
                "availability": "in stock" if product["stock"] > 0 else "out of stock",
                "price": product["price"] * 100,  # 单位为分
                "currency": "BRL"
            }
        )
```

---

## WhatsApp 频道

WhatsApp Channels 是一种单向广播功能。您可以在 WhatsApp 的"更新"标签页中向无限订阅者发送更新。

### 特性

- **单向通信：** 仅管理员发送，订阅者接收
- **管理员隐私：** 关注者看不到您的个人号码
- **订阅者隐私：** 管理员看不到关注者的号码（除非保存为联系人）
- **内容：** 文本、图片、视频、贴纸、投票

### 可用分析（30 天）

| 指标              | 描述                                  |
|-------------------|--------------------------------------|
| 增长              | 新增关注者与取消关注                  |
| 触达              | 看到您消息的人数                      |
| 互动              | emoji 反应                            |
| 投票结果          | 投票中的票数                          |

### 最佳实践

- 发布相关且非过度推广的内容
- 使用投票促进互动
- 理想频率：每周 2-5 条
- 独家内容可激励关注

---

## Click-to-WhatsApp 广告

在 Facebook 和 Instagram 上投放带有打开 WhatsApp 对话按钮的广告。

### 在 Meta Ads Manager 中设置

1. 创建目标为 "Messaging"、"Leads" 或 "Sales" 的广告活动
2. 选择 "Click to WhatsApp" 作为目标
3. 链接 WhatsApp Business 账户
4. 配置预填充消息（问候语 + 预填消息）

### 预填消息

配置客户打开聊天时看到的消息：

```
问候语："Olá! Obrigado por clicar no nosso anúncio."
预填内容："Oi, vi o anúncio sobre [produto] e gostaria de saber mais!"
```

### 在 Webhook 中集成

当客户来自广告时，webhook 包含引流数据：

```json
{
  "messages": [{
    "from": "5511999999999",
    "type": "text",
    "text": { "body": "Oi, vi o anúncio..." },
    "referral": {
      "source_url": "https://fb.me/...",
      "source_type": "ad",
      "source_id": "AD_ID",
      "headline": "Titulo do Anuncio",
      "body": "Texto do anuncio",
      "ctwa_clid": "click_id_para_tracking"
    }
  }]
}
```

### 转化跟踪

```typescript
function handleAdReferral(message: IncomingMessage): void {
  if (message.referral) {
    const adData = {
      adId: message.referral.source_id,
      clickId: message.referral.ctwa_clid,
      headline: message.referral.headline,
      customerPhone: message.from,
      timestamp: new Date()
    };

    // 记录来自广告的潜在客户
    trackConversion(adData);

    // 使用广告上下文个性化服务
    customizeGreeting(message.from, adData.headline);
  }
}
```

### 指标

- **打开率：** 约 99%（WhatsApp 消息）
- **成本降低：** 比表单的每个潜在客户成本低达 32%
- **增长：** 客户消息量增加高达 46%

---

## 状态跟踪

### 消息生命周期

```
已发送 (sent) → 已送达服务器 (delivered) → 已送达设备 (delivered) → 已读 (read)
```

### 通过 Webhook 获取状态

```json
{
  "statuses": [
    {
      "id": "wamid.HBgNNTUxMTk5...",
      "status": "delivered",
      "timestamp": "1709251200",
      "recipient_id": "5511999999999",
      "conversation": {
        "id": "CONVERSATION_ID",
        "origin": { "type": "business_initiated" },
        "expiration_timestamp": "1709337600"
      },
      "pricing": {
        "billable": true,
        "pricing_model": "CBP",
        "category": "utility"
      }
    }
  ]
}
```

### 可能的状态

| 状态          | 描述                              | 可靠性            |
|---------------|-----------------------------------|-------------------|
| `sent`        | 消息已发送到 Meta 服务器          | 高                |
| `delivered`   | 已送达客户设备                    | 高                |
| `read`        | 客户已读消息（蓝色对勾）          | 中（可能离线）    |
| `failed`      | 投递失败                          | 高                |

### 重要限制

`read` 状态取决于用户是否在 WhatsApp 设置中开启了**已读回执**。许多用户会关闭该功能。使用 `delivered` 作为可靠的送达确认。

### 跟踪实现

```typescript
interface MessageStatus {
  messageId: string;
  to: string;
  sentAt: Date;
  deliveredAt?: Date;
  readAt?: Date;
  failedAt?: Date;
  failureReason?: string;
}

async function processStatusUpdate(status: WebhookStatus): Promise<void> {
  const update: Partial<MessageStatus> = {};

  switch (status.status) {
    case 'sent':
      update.sentAt = new Date(parseInt(status.timestamp) * 1000);
      break;
    case 'delivered':
      update.deliveredAt = new Date(parseInt(status.timestamp) * 1000);
      break;
    case 'read':
      update.readAt = new Date(parseInt(status.timestamp) * 1000);
      break;
    case 'failed':
      update.failedAt = new Date(parseInt(status.timestamp) * 1000);
      update.failureReason = status.errors?.[0]?.message;
      break;
  }

  await db.messageStatuses.updateOne(
    { messageId: status.id },
    { $set: update }
  );
}
```

---

## 分析与报表

### 客服关键指标

| 指标                          | 计算方式                                | 理想目标          |
|-------------------------------|----------------------------------------|------------------|
| 首次响应时间 (FRT)            | 响应时间戳 - 消息时间戳                  | < 5 分钟         |
| 平均解决时间                  | 关闭时间戳 - 开始时间戳                  | < 30 分钟        |
| 机器人解决率                  | 机器人解决数 / 总数                      | > 60%            |
| 人工升级率                    | 升级到人工数 / 总数                      | < 40%            |
| CSAT（满意度）                | 服务后 NPS 调查                          | > 4.0 / 5.0      |
| 送达率                        | 已送达 / 已发送                          | > 95%            |
| 阅读率                        | 已读 / 已送达                            | > 70%            |
| 退订率                        | 退订数 / 总基数                          | < 2% / 每次活动  |

### 通过 WhatsApp 进行 NPS 调查

```typescript
async function sendNPSSurvey(to: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'button',
      body: {
        text: '从 1 到 5，您如何评价我们的服务？\n\n' +
              '1 = 非常差\n5 = 非常好'
      },
      action: {
        buttons: [
          { type: 'reply', reply: { id: 'nps_1_2', title: '1-2 差' } },
          { type: 'reply', reply: { id: 'nps_3', title: '3 一般' } },
          { type: 'reply', reply: { id: 'nps_4_5', title: '4-5 好' } }
        ]
      }
    }
  });
}
```

### 分析仪表板

要获得高级分析功能，可考虑与以下平台集成：
- **Infobip** - 带有 reporting API 的完整仪表板
- **Trengo** - CSAT 跟踪、响应时间、热门话题
- **Wassenger** - 客服对比、CSV/JSON/PDF 导出
- **自建方案** - MongoDB/PostgreSQL + Grafana/Metabase
