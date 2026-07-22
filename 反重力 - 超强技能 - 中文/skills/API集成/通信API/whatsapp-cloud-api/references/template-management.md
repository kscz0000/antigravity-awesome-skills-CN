# 通过 API 管理模板 - WhatsApp Cloud API

通过 WhatsApp Business Management API 以编程方式创建、列出、删除和管理消息模板的完整指南。

---

## 目录

1. [概述](#visao-geral)
2. [模板类别](#categorias-de-templates)
3. [创建模板](#criar-template)
4. [列出模板](#listar-templates)
5. [删除模板](#deletar-template)
6. [带变量的模板](#templates-com-variaveis)
7. [带媒体的模板](#templates-com-midia)
8. [带按钮的模板](#templates-com-botoes)
9. [发送模板消息](#enviar-template-message)
10. [最佳实践](#boas-praticas)

---

## 概述

模板是 WhatsApp 预先批准的消息。它们是**唯一**可以与客户发起对话的方式（24 小时窗口外）。

**限制：**
- 每个 WABA 账户最多 6,000 个模板翻译版本
- 审批时间从几分钟到几小时不等
- 模板**提交后无法编辑**（删除并创建新的）
- 模板正文：最多 1,600 字符

**基础端点：** `https://graph.facebook.com/v21.0/{waba-id}/message_templates`

---

## 模板类别

| 类别          | 用途                                            | 费用              |
|----------------|----------------------------------------------|---------------------|
| MARKETING      | 促销活动、营销活动、新品发布                | $0.025-$0.1365/msg  |
| UTILITY        | 订单确认、状态更新、物流跟踪                | $0.004-$0.0456/msg  |
| AUTHENTICATION | 一次性密码、密码重置、两步验证              | $0.004-$0.0456/msg  |

类别影响费用和审批规则。营销类模板有更严格的规则。

---

## 创建模板

### Node.js

```typescript
interface TemplateComponent {
  type: 'HEADER' | 'BODY' | 'FOOTER' | 'BUTTONS';
  format?: 'TEXT' | 'IMAGE' | 'VIDEO' | 'DOCUMENT';
  text?: string;
  example?: { header_handle?: string[]; body_text?: string[][] };
  buttons?: Array<{
    type: 'QUICK_REPLY' | 'URL' | 'PHONE_NUMBER';
    text: string;
    url?: string;
    phone_number?: string;
    example?: string[];
  }>;
}

async function createTemplate(
  name: string,
  category: 'MARKETING' | 'UTILITY' | 'AUTHENTICATION',
  language: string,
  components: TemplateComponent[]
): Promise<any> {
  const response = await axios.post(
    `${GRAPH_API}/${process.env.WABA_ID}/message_templates`,
    { name, category, language, components },
    { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
  );
  return response.data;
  // { id: "template_id", status: "PENDING", category: "UTILITY" }
}

// 示例：创建订单确认模板
await createTemplate(
  'order_confirmation_v1',
  'UTILITY',
  'pt_BR',
  [
    {
      type: 'HEADER',
      format: 'TEXT',
      text: 'Pedido Confirmado!'
    },
    {
      type: 'BODY',
      text: 'Ola {{1}}, seu pedido #{{2}} foi confirmado!\n\nValor: R$ {{3}}\nPrevisao de entrega: {{4}}',
      example: {
        body_text: [['Joao', '12345', '99,90', '3 dias uteis']]
      }
    },
    {
      type: 'FOOTER',
      text: 'Obrigado por comprar conosco!'
    }
  ]
);
```

### Python

```python
async def create_template(
    name: str,
    category: str,
    language: str,
    components: list[dict]
) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GRAPH_API}/{os.environ['WABA_ID']}/message_templates",
            json={
                "name": name,
                "category": category,
                "language": language,
                "components": components
            },
            headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}
        )
        return response.json()

# 示例：创建欢迎模板
await create_template(
    name="welcome_v1",
    category="MARKETING",
    language="pt_BR",
    components=[
        {
            "type": "BODY",
            "text": "Ola {{1}}, bem-vindo a nossa loja! 🎉\n\nConfira nossas ofertas exclusivas.",
            "example": {"body_text": [["Maria"]]}
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {
                    "type": "URL",
                    "text": "Ver Ofertas",
                    "url": "https://example.com/ofertas"
                },
                {
                    "type": "QUICK_REPLY",
                    "text": "Falar com Vendedor"
                }
            ]
        }
    ]
)
```

---

## 列出模板

### Node.js

```typescript
async function listTemplates(status?: string): Promise<any[]> {
  const params = new URLSearchParams({ limit: '100' });
  if (status) params.append('status', status);

  const response = await axios.get(
    `${GRAPH_API}/${process.env.WABA_ID}/message_templates?${params}`,
    { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
  );

  return response.data.data;
}

// 仅列出已批准的模板
const approved = await listTemplates('APPROVED');

// 列出所有
const all = await listTemplates();
```

### Python

```python
async def list_templates(status: str | None = None) -> list[dict]:
    params = {"limit": 100}
    if status:
        params["status"] = status

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GRAPH_API}/{os.environ['WABA_ID']}/message_templates",
            params=params,
            headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}
        )
        return response.json()["data"]
```

### 模板状态

| 状态        | 含义                              |
|-------------|--------------------------------------|
| APPROVED    | 已批准，可供使用                  |
| PENDING     | 正在由 WhatsApp 审核              |
| REJECTED    | 已拒绝（请查看响应中的原因）      |
| PAUSED      | 因低质量而暂停                    |
| DISABLED    | 已禁用                            |

---

## 删除模板

### Node.js

```typescript
async function deleteTemplate(templateName: string): Promise<void> {
  await axios.delete(
    `${GRAPH_API}/${process.env.WABA_ID}/message_templates`,
    {
      data: { name: templateName },
      headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` }
    }
  );
}

await deleteTemplate('old_template_v1');
```

### Python

```python
async def delete_template(template_name: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.request(
            "DELETE",
            f"{GRAPH_API}/{os.environ['WABA_ID']}/message_templates",
            json={"name": template_name},
            headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}
        )
```

**注意：** 删除模板会移除所有关联的翻译版本。

---

## 带变量的模板

变量在模板正文中以 `{{N}}`（从 1 开始索引）表示。

### 规则

- 变量必须按顺序排列：`{{1}}`、`{{2}}`、`{{3}}`
- 创建时，提供带有示例值的 `example`
- 发送时，提供带有实际值的 `parameters`
- 不要跳过数字：`{{1}}`、`{{3}}` 而没有 `{{2}}` 是无效的

### 完整示例

**创建：**
```json
{
  "type": "BODY",
  "text": "Ola {{1}}, seu pedido #{{2}} sera entregue em {{3}}.",
  "example": { "body_text": [["Joao", "12345", "2 dias"]] }
}
```

**发送：**
```json
{
  "type": "body",
  "parameters": [
    { "type": "text", "text": "Maria" },
    { "type": "text", "text": "67890" },
    { "type": "text", "text": "3 dias uteis" }
  ]
}
```

---

## 带媒体的模板

### 带图片的标题

**创建：**
```json
{
  "type": "HEADER",
  "format": "IMAGE",
  "example": {
    "header_handle": ["4::aW1hZ2UvanBlZw==:ARb..."]
  }
}
```

要获取 `header_handle`，请先上传示例图片：
```
POST /{app-id}/uploads?file_type=image/jpeg&file_length=12345
```

**发送：**
```json
{
  "type": "header",
  "parameters": [
    {
      "type": "image",
      "image": { "link": "https://example.com/image.jpg" }
    }
  ]
}
```

### 带文档的标题

**创建：**
```json
{
  "type": "HEADER",
  "format": "DOCUMENT",
  "example": {
    "header_handle": ["4::YXBwbGljYXRpb24vcGRm:ARb..."]
  }
}
```

**发送：**
```json
{
  "type": "header",
  "parameters": [
    {
      "type": "document",
      "document": {
        "link": "https://example.com/invoice.pdf",
        "filename": "Nota_Fiscal_12345.pdf"
      }
    }
  ]
}
```

---

## 带按钮的模板

### 快速回复（最多 3 个按钮）

```json
{
  "type": "BUTTONS",
  "buttons": [
    { "type": "QUICK_REPLY", "text": "Sim, confirmo" },
    { "type": "QUICK_REPLY", "text": "Nao, cancelar" },
    { "type": "QUICK_REPLY", "text": "Falar com atendente" }
  ]
}
```

### URL 按钮

```json
{
  "type": "BUTTONS",
  "buttons": [
    {
      "type": "URL",
      "text": "Rastrear Pedido",
      "url": "https://example.com/tracking/{{1}}",
      "example": ["12345"]
    }
  ]
}
```

### 电话号码按钮

```json
{
  "type": "BUTTONS",
  "buttons": [
    {
      "type": "PHONE_NUMBER",
      "text": "Ligar para Suporte",
      "phone_number": "+5511999999999"
    }
  ]
}
```

### 发送带动态 URL 按钮的模板

```typescript
await sendMessage({
  messaging_product: 'whatsapp',
  to: '5511999999999',
  type: 'template',
  template: {
    name: 'order_tracking_v1',
    language: { code: 'pt_BR' },
    components: [
      {
        type: 'body',
        parameters: [
          { type: 'text', text: 'Maria' },
          { type: 'text', text: '67890' }
        ]
      },
      {
        type: 'button',
        sub_type: 'url',
        index: 0,
        parameters: [
          { type: 'text', text: '67890' } // 替换 URL 中的 {{1}}
        ]
      }
    ]
  }
});
```

---

## 发送模板消息

### 完整示例 - Node.js

```typescript
async function sendTemplate(
  to: string,
  templateName: string,
  language: string,
  components?: Array<{
    type: string;
    parameters?: Array<{ type: string; text?: string; image?: any; document?: any }>;
    sub_type?: string;
    index?: number;
  }>
): Promise<any> {
  const payload: any = {
    messaging_product: 'whatsapp',
    to,
    type: 'template',
    template: {
      name: templateName,
      language: { code: language }
    }
  };

  if (components) {
    payload.template.components = components;
  }

  return sendWithRetry(payload);
}

// 简单使用（不带变量）
await sendTemplate('5511999999999', 'hello_world', 'pt_BR');

// 带正文中变量
await sendTemplate('5511999999999', 'order_confirmation_v1', 'pt_BR', [
  {
    type: 'body',
    parameters: [
      { type: 'text', text: 'Joao' },
      { type: 'text', text: '12345' },
      { type: 'text', text: '99,90' },
      { type: 'text', text: '3 dias uteis' }
    ]
  }
]);
```

### 完整示例 - Python

```python
async def send_template(
    to: str,
    template_name: str,
    language: str,
    components: list[dict] | None = None
) -> dict:
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language}
        }
    }

    if components:
        payload["template"]["components"] = components

    return await send_with_retry(payload)

# 简单使用
await send_template("5511999999999", "hello_world", "pt_BR")

# 带变量
await send_template("5511999999999", "order_confirmation_v1", "pt_BR", [
    {
        "type": "body",
        "parameters": [
            {"type": "text", "text": "Maria"},
            {"type": "text", "text": "67890"},
            {"type": "text", "text": "149,90"},
            {"type": "text", "text": "5 dias uteis"}
        ]
    }
])
```

---

## 最佳实践

### 命名约定

使用一致的模板名称模式：
```
{用途}_{描述}_v{版本}
```

示例：
- `order_confirmation_v1`
- `welcome_new_customer_v2`
- `payment_reminder_v1`
- `nps_survey_v3`

### 版本管理

由于模板提交后无法编辑：
1. 创建新版本：`template_name_v2`
2. 测试新版本
3. 批准后，将代码迁移到使用 v2
4. 不再需要时删除 v1

### 审批提示

- 在正文中避免过度宣传的语言
- 在 `example` 中包含清晰、真实的示例
- 不要使用短链接（bit.ly 等）
- 不要包含可能被解读为垃圾邮件的内容
- Utility 模板的审批速度比营销模板快
- 使用变量进行个性化（客户姓名、订单号）

### 监控

```typescript
// 定期检查模板状态
async function monitorTemplates(): Promise<void> {
  const templates = await listTemplates();

  for (const template of templates) {
    if (template.status === 'REJECTED') {
      console.warn(`模板已拒绝：${template.name}`);
      console.warn(`原因：${template.rejected_reason}`);
    }
    if (template.status === 'PAUSED') {
      console.warn(`模板因质量问题被暂停：${template.name}`);
    }
  }
}
```
