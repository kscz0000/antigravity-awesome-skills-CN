# WhatsApp Cloud API - 消息类型（完整参考）

> WhatsApp Cloud API v21.0 支持的所有消息类型的完整参考。
> 提供 Node.js/TypeScript（axios）和 Python（httpx async）示例。

**基础 URL：** `https://graph.facebook.com/v21.0`

**所需环境变量：**

```env
WHATSAPP_TOKEN=seu_token_aqui
PHONE_NUMBER_ID=seu_phone_number_id
```

---

## 1. 文本消息（Text Message）

简单文本消息。最多支持 4096 个字符。当消息包含链接时，`preview_url` 选项会自动生成预览。

### JSON 负载

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "text",
  "text": {
    "preview_url": true,
    "body": "Confira nosso site: https://exemplo.com.br"
  }
}
```

### Node.js / TypeScript

```typescript
import axios from "axios";

interface TextMessage {
  messaging_product: "whatsapp";
  recipient_type: "individual";
  to: string;
  type: "text";
  text: {
    preview_url?: boolean;
    body: string;
  };
}

async function sendTextMessage(to: string, body: string, previewUrl = false): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: TextMessage = {
    messaging_product: "whatsapp",
    recipient_type: "individual",
    to,
    type: "text",
    text: { preview_url: previewUrl, body },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
import os
import httpx

async def send_text_message(to: str, body: str, preview_url: bool = False) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"preview_url": preview_url, "body": body},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["messages"][0]["id"]
```

### 预期响应

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{ "input": "5511999999999", "wa_id": "5511999999999" }],
  "messages": [{ "id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ..." }]
}
```

### 注意事项

- `body` 字段最多 4096 个字符。
- `preview_url: true` 要求正文包含有效 URL 才能生成预览。
- 支持的格式：`*粗体*`、`_斜体_`、`~删除线~`、`` `等宽字体` ``。

---

## 2. 模板消息（Template Message）

模板是 Meta 预先批准的消息。必须用于发起对话（24 小时窗口外）。支持变量、带媒体的标题和按钮。

### 2a. 带变量的模板

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "pedido_confirmado",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "body",
        "parameters": [
          { "type": "text", "text": "Renato" },
          { "type": "text", "text": "#12345" }
        ]
      }
    ]
  }
}
```

### 2b. 带图片标题的模板

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "promo_imagem",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "image",
            "image": { "link": "https://exemplo.com/banner.jpg" }
          }
        ]
      },
      {
        "type": "body",
        "parameters": [{ "type": "text", "text": "20%" }]
      }
    ]
  }
}
```

### 2c. 带按钮的模板（快速回复 + CTA）

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "acompanhar_pedido",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "body",
        "parameters": [{ "type": "text", "text": "#12345" }]
      },
      {
        "type": "button",
        "sub_type": "quick_reply",
        "index": "0",
        "parameters": [{ "type": "payload", "payload": "SIM_CONFIRMAR" }]
      },
      {
        "type": "button",
        "sub_type": "url",
        "index": "1",
        "parameters": [{ "type": "text", "text": "12345" }]
      }
    ]
  }
}
```

### Node.js / TypeScript

```typescript
interface TemplateParameter {
  type: "text" | "image" | "document" | "video" | "payload";
  text?: string;
  payload?: string;
  image?: { link: string };
}

interface TemplateComponent {
  type: "header" | "body" | "button";
  sub_type?: "quick_reply" | "url";
  index?: string;
  parameters: TemplateParameter[];
}

interface TemplateMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "template";
  template: {
    name: string;
    language: { code: string };
    components: TemplateComponent[];
  };
}

async function sendTemplateMessage(
  to: string,
  templateName: string,
  languageCode: string,
  components: TemplateComponent[]
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: TemplateMessage = {
    messaging_product: "whatsapp",
    to,
    type: "template",
    template: {
      name: templateName,
      language: { code: languageCode },
      components,
    },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_template_message(
    to: str,
    template_name: str,
    language_code: str,
    components: list[dict],
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code},
            "components": components,
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- 模板需要在使用前通过 Meta Business Manager 审批。
- `language.code` 字段必须与已批准的语言完全匹配（例如 `pt_BR`）。
- `url` 类型按钮使用动态后缀：参数会被拼接到模板中定义的基础 URL 末尾。
- `quick_reply` 类型按钮在被点击时会在 webhook 中返回配置的 `payload`。
- 每个模板最多 3 个 quick_reply 按钮或 2 个 CTA 按钮。

---

## 3. 图片消息（Image Message）

向收件人发送图片。可通过公共 URL 或媒体 ID（通过媒体 API 预先上传）。

### 3a. 通过 URL

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "image",
  "image": {
    "link": "https://exemplo.com/foto.jpg",
    "caption": "Foto do produto"
  }
}
```

### 3b. 通过媒体 ID

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "image",
  "image": {
    "id": "1234567890",
    "caption": "Foto do produto"
  }
}
```

### Node.js / TypeScript

```typescript
interface ImageMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "image";
  image: {
    link?: string;
    id?: string;
    caption?: string;
  };
}

async function sendImageMessage(
  to: string,
  source: { link: string } | { id: string },
  caption?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: ImageMessage = {
    messaging_product: "whatsapp",
    to,
    type: "image",
    image: { ...source, caption },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_image_message(
    to: str,
    source: dict,  # {"link": "..."} 或 {"id": "..."}
    caption: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    image_payload = {**source}
    if caption:
        image_payload["caption"] = caption

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": image_payload,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- 支持的格式：JPEG、PNG。
- 最大大小：5 MB。
- URL 必须是可公开访问的（无需身份验证）。
- `caption` 可选，最多 1024 个字符。

---

## 4. 文档消息（Document Message）

发送 PDF、电子表格等文档。`filename` 字段定义收件人设备上显示的下载文件名。

### JSON 负载

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "document",
  "document": {
    "link": "https://exemplo.com/relatorio.pdf",
    "caption": "Relatorio mensal - Janeiro 2026",
    "filename": "relatorio-janeiro-2026.pdf"
  }
}
```

### Node.js / TypeScript

```typescript
interface DocumentMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "document";
  document: {
    link?: string;
    id?: string;
    caption?: string;
    filename?: string;
  };
}

async function sendDocumentMessage(
  to: string,
  source: { link: string } | { id: string },
  filename: string,
  caption?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: DocumentMessage = {
    messaging_product: "whatsapp",
    to,
    type: "document",
    document: { ...source, filename, caption },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_document_message(
    to: str,
    source: dict,
    filename: str,
    caption: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    doc_payload = {**source, "filename": filename}
    if caption:
        doc_payload["caption"] = caption

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "document",
        "document": doc_payload,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- 支持的格式：PDF、DOC、DOCX、XLS、XLSX、PPT、PPTX、TXT 等。
- 最大大小：100 MB。
- `filename` 在收件人设备上显示为下载文件的名称。
- `caption` 可选，最多 1024 个字符。

---

## 5. 视频消息（Video Message）

发送带可选说明的视频。适用于教程、产品演示等。

### JSON 负载

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "video",
  "video": {
    "link": "https://exemplo.com/demo.mp4",
    "caption": "Demonstracao do produto"
  }
}
```

### Node.js / TypeScript

```typescript
interface VideoMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "video";
  video: {
    link?: string;
    id?: string;
    caption?: string;
  };
}

async function sendVideoMessage(
  to: string,
  source: { link: string } | { id: string },
  caption?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: VideoMessage = {
    messaging_product: "whatsapp",
    to,
    type: "video",
    video: { ...source, caption },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_video_message(
    to: str,
    source: dict,
    caption: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    video_payload = {**source}
    if caption:
        video_payload["caption"] = caption

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "video",
        "video": video_payload,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- 支持的格式：MP4、3GPP（仅 H.264 和 AAC 编解码器）。
- 最大大小：16 MB。
- `caption` 可选，最多 1024 个字符。

---

## 6. 音频消息（Audio Message）

发送语音消息或音频文件。在聊天中直接作为语音消息播放。

### JSON 负载

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "audio",
  "audio": {
    "link": "https://exemplo.com/audio.ogg"
  }
}
```

### Node.js / TypeScript

```typescript
interface AudioMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "audio";
  audio: {
    link?: string;
    id?: string;
  };
}

async function sendAudioMessage(
  to: string,
  source: { link: string } | { id: string }
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: AudioMessage = {
    messaging_product: "whatsapp",
    to,
    type: "audio",
    audio: source,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_audio_message(
    to: str,
    source: dict,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "audio",
        "audio": source,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- 支持的格式：OGG（OPUS 编解码器）、MP3、AMR、AAC、M4A。
- 最大大小：16 MB。
- 音频不支持 `caption`。
- 使用 OPUS 编解码器的 `.ogg` 文件会作为语音消息播放（带麦克风图标）。

---

## 7. 交互式按钮 - 快速回复（Interactive Buttons）

显示最多 3 个快速回复按钮。当用户点击按钮时，回复会自动作为文本消息发送，按钮的 `id` 会在 webhook 中返回。

### JSON 负载

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "header": {
      "type": "text",
      "text": "Confirmacao de Pedido"
    },
    "body": {
      "text": "Seu pedido #12345 esta pronto. Deseja confirmar a entrega?"
    },
    "footer": {
      "text": "Responda em ate 24h"
    },
    "action": {
      "buttons": [
        { "type": "reply", "reply": { "id": "btn_confirmar", "title": "Confirmar" } },
        { "type": "reply", "reply": { "id": "btn_reagendar", "title": "Reagendar" } },
        { "type": "reply", "reply": { "id": "btn_cancelar", "title": "Cancelar" } }
      ]
    }
  }
}
```

### Node.js / TypeScript

```typescript
interface ReplyButton {
  type: "reply";
  reply: { id: string; title: string };
}

interface InteractiveButtonMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "interactive";
  interactive: {
    type: "button";
    header?: { type: "text"; text: string };
    body: { text: string };
    footer?: { text: string };
    action: { buttons: ReplyButton[] };
  };
}

async function sendButtonMessage(
  to: string,
  body: string,
  buttons: Array<{ id: string; title: string }>,
  header?: string,
  footer?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const interactive: InteractiveButtonMessage["interactive"] = {
    type: "button",
    body: { text: body },
    action: {
      buttons: buttons.map((b) => ({
        type: "reply" as const,
        reply: { id: b.id, title: b.title },
      })),
    },
  };

  if (header) interactive.header = { type: "text", text: header };
  if (footer) interactive.footer = { text: footer };

  const payload: InteractiveButtonMessage = {
    messaging_product: "whatsapp",
    to,
    type: "interactive",
    interactive,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_button_message(
    to: str,
    body: str,
    buttons: list[dict],  # [{"id": "btn_1", "title": "Opcao 1"}, ...]
    header: str | None = None,
    footer: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    interactive: dict = {
        "type": "button",
        "body": {"text": body},
        "action": {
            "buttons": [
                {"type": "reply", "reply": {"id": b["id"], "title": b["title"]}}
                for b in buttons
            ]
        },
    }

    if header:
        interactive["header"] = {"type": "text", "text": header}
    if footer:
        interactive["footer"] = {"type": "text", "text": footer}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": interactive,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- 每条消息最多 3 个按钮。
- 按钮标题：最多 20 个字符。
- 按钮 ID：最多 256 个字符。
- `body` 是必需的；`header` 和 `footer` 是可选的。
- `header` 也可以是 `image`、`video` 或 `document` 类型。

---

## 8. 交互式列表（Interactive List）

显示带分区和可选项的菜单。非常适合目录、客服菜单、时间段选择等。

### JSON 负载

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "header": {
      "type": "text",
      "text": "Cardapio do Dia"
    },
    "body": {
      "text": "Escolha uma opcao do nosso cardapio:"
    },
    "footer": {
      "text": "Entrega em ate 40min"
    },
    "action": {
      "button": "Ver opcoes",
      "sections": [
        {
          "title": "Pratos Principais",
          "rows": [
            { "id": "prato_1", "title": "Frango Grelhado", "description": "Com arroz e salada - R$32" },
            { "id": "prato_2", "title": "Peixe Assado", "description": "Com pure e legumes - R$38" }
          ]
        },
        {
          "title": "Bebidas",
          "rows": [
            { "id": "bebida_1", "title": "Suco Natural", "description": "Laranja, limao ou maracuja - R$8" },
            { "id": "bebida_2", "title": "Agua Mineral", "description": "Com ou sem gas - R$5" }
          ]
        }
      ]
    }
  }
}
```

### Node.js / TypeScript

```typescript
interface ListRow {
  id: string;
  title: string;
  description?: string;
}

interface ListSection {
  title: string;
  rows: ListRow[];
}

interface InteractiveListMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "interactive";
  interactive: {
    type: "list";
    header?: { type: "text"; text: string };
    body: { text: string };
    footer?: { text: string };
    action: {
      button: string;
      sections: ListSection[];
    };
  };
}

async function sendListMessage(
  to: string,
  body: string,
  buttonText: string,
  sections: ListSection[],
  header?: string,
  footer?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const interactive: InteractiveListMessage["interactive"] = {
    type: "list",
    body: { text: body },
    action: { button: buttonText, sections },
  };

  if (header) interactive.header = { type: "text", text: header };
  if (footer) interactive.footer = { text: footer };

  const payload: InteractiveListMessage = {
    messaging_product: "whatsapp",
    to,
    type: "interactive",
    interactive,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_list_message(
    to: str,
    body: str,
    button_text: str,
    sections: list[dict],
    header: str | None = None,
    footer: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    interactive: dict = {
        "type": "list",
        "body": {"text": body},
        "action": {"button": button_text, "sections": sections},
    }

    if header:
        interactive["header"] = {"type": "text", "text": header}
    if footer:
        interactive["footer"] = {"type": "text", "text": footer}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": interactive,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- 最多 10 个分区。
- 所有分区中最多 10 个选项（行）。
- 行标题：最多 24 个字符。
- 行描述：最多 72 个字符（可选）。
- 按钮文本（`action.button`）：最多 20 个字符。
- `header` 在列表中仅支持 `text` 类型（不支持媒体）。

---

## 9. 位置消息（Location Message）

共享带有坐标、名称和地址的地理位置。可用于发送店铺地址、集合点等。

### JSON 负载

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "location",
  "location": {
    "latitude": -23.5505,
    "longitude": -46.6333,
    "name": "Loja Centro SP",
    "address": "Av. Paulista, 1000 - Bela Vista, Sao Paulo - SP"
  }
}
```

### Node.js / TypeScript

```typescript
interface LocationMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "location";
  location: {
    latitude: number;
    longitude: number;
    name?: string;
    address?: string;
  };
}

async function sendLocationMessage(
  to: string,
  latitude: number,
  longitude: number,
  name?: string,
  address?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: LocationMessage = {
    messaging_product: "whatsapp",
    to,
    type: "location",
    location: { latitude, longitude, name, address },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_location_message(
    to: str,
    latitude: float,
    longitude: float,
    name: str | None = None,
    address: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    location_data: dict = {"latitude": latitude, "longitude": longitude}
    if name:
        location_data["name"] = name
    if address:
        location_data["address"] = address

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "location",
        "location": location_data,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- `latitude` 和 `longitude` 是必需的。
- `name` 和 `address` 是可选的，但建议提供以获得更好的用户体验。
- 该位置在 WhatsApp 中以集成地图的形式显示。

---

## 10. 联系人消息（Contact Message）

共享包含姓名、电话、邮箱等信息的联系人卡片（vCard）。收件人可以直接将联系人保存到通讯录。

### JSON 负载

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "contacts",
  "contacts": [
    {
      "name": {
        "formatted_name": "Suporte TechCo",
        "first_name": "Suporte",
        "last_name": "TechCo"
      },
      "phones": [
        { "phone": "+5511988887777", "type": "WORK", "wa_id": "5511988887777" }
      ],
      "emails": [
        { "email": "suporte@techco.com.br", "type": "WORK" }
      ],
      "org": {
        "company": "TechCo Solucoes"
      },
      "urls": [
        { "url": "https://techco.com.br", "type": "WORK" }
      ]
    }
  ]
}
```

### Node.js / TypeScript

```typescript
interface ContactName {
  formatted_name: string;
  first_name?: string;
  last_name?: string;
}

interface ContactPhone {
  phone: string;
  type?: "CELL" | "MAIN" | "IPHONE" | "HOME" | "WORK";
  wa_id?: string;
}

interface ContactInfo {
  name: ContactName;
  phones?: ContactPhone[];
  emails?: Array<{ email: string; type?: string }>;
  org?: { company: string };
  urls?: Array<{ url: string; type?: string }>;
}

interface ContactMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "contacts";
  contacts: ContactInfo[];
}

async function sendContactMessage(
  to: string,
  contacts: ContactInfo[]
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: ContactMessage = {
    messaging_product: "whatsapp",
    to,
    type: "contacts",
    contacts,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_contact_message(
    to: str,
    contacts: list[dict],
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "contacts",
        "contacts": contacts,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- `name.formatted_name` 字段是必需的。
- 可以在单条消息中发送多个联系人（`contacts` 数组）。
- `wa_id` 允许收件人在 WhatsApp 中直接与该联系人发起对话。
- 支持的字段：`addresses`、`birthday`、`emails`、`name`、`org`、`phones`、`urls`。

---

## 11. 反应消息（Reaction Message）

对现有消息使用 emoji 进行反应。要删除反应，请发送空的 `emoji`。

### JSON 负载（添加反应）

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "reaction",
  "reaction": {
    "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ...",
    "emoji": "\ud83d\udc4d"
  }
}
```

### JSON 负载（删除反应）

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "reaction",
  "reaction": {
    "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ...",
    "emoji": ""
  }
}
```

### Node.js / TypeScript

```typescript
interface ReactionMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "reaction";
  reaction: {
    message_id: string;
    emoji: string;
  };
}

async function sendReaction(
  to: string,
  messageId: string,
  emoji: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: ReactionMessage = {
    messaging_product: "whatsapp",
    to,
    type: "reaction",
    reaction: { message_id: messageId, emoji },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}

async function removeReaction(to: string, messageId: string): Promise<string> {
  return sendReaction(to, messageId, "");
}
```

### Python

```python
async def send_reaction(to: str, message_id: str, emoji: str) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "reaction",
        "reaction": {"message_id": message_id, "emoji": emoji},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]


async def remove_reaction(to: str, message_id: str) -> str:
    return await send_reaction(to, message_id, "")
```

### 注意事项

- `message_id` 必须是您要响应的原始消息的 ID。
- 要删除反应，请将 `emoji` 发送为空字符串 `""`。
- 每个发送者对每条消息只能有一个 emoji 反应。
- 支持任何 Unicode emoji。

---

## 12. 带上下文/回复的消息（Reply / Context Message）

使用 `message_id` 作为上下文来回复特定消息。消息会显示在收件人聊天中，带有原始消息的可视化引用。

适用于任何类型的消息（文本、图片、按钮等），通过添加 `context` 字段实现。

### JSON 负载（文本回复）

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "context": {
    "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ..."
  },
  "type": "text",
  "text": {
    "body": "Obrigado pela sua mensagem! Vamos verificar e retornar em breve."
  }
}
```

### JSON 负载（带图片的回复）

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "context": {
    "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ..."
  },
  "type": "image",
  "image": {
    "link": "https://exemplo.com/resposta.jpg",
    "caption": "Aqui esta a imagem solicitada"
  }
}
```

### Node.js / TypeScript

```typescript
interface ContextPayload {
  message_id: string;
}

async function sendReplyMessage(
  to: string,
  replyToMessageId: string,
  body: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload = {
    messaging_product: "whatsapp",
    to,
    context: { message_id: replyToMessageId } as ContextPayload,
    type: "text",
    text: { body },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}

// 通用函数，为任何消息负载添加上下文
async function sendWithContext<T extends Record<string, unknown>>(
  basePayload: T,
  replyToMessageId: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload = {
    ...basePayload,
    context: { message_id: replyToMessageId },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_reply_message(
    to: str,
    reply_to_message_id: str,
    body: str,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "context": {"message_id": reply_to_message_id},
        "type": "text",
        "text": {"body": body},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]


async def send_with_context(
    base_payload: dict,
    reply_to_message_id: str,
) -> str:
    """为任何消息负载添加回复上下文。"""
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {**base_payload, "context": {"message_id": reply_to_message_id}}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### 注意事项

- `context.message_id` 字段必须包含原始消息的 ID。
- 适用于所有消息类型：文本、图片、视频、文档、交互消息等。
- 原始消息在聊天中显示为可视化引用。
- `message_id` 通过 webhook 接收消息时获得。

---

## 13. 标记为已读（Mark as Read）

将收到的消息标记为已读，在发送方设备上显示蓝色对勾。还会短暂触发"正在输入"事件。

**注意：** 此端点使用不同的操作（`"read"`），**不是**一种消息类型。

### JSON 负载

```json
{
  "messaging_product": "whatsapp",
  "status": "read",
  "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ..."
}
```

### Node.js / TypeScript

```typescript
interface MarkAsReadPayload {
  messaging_product: "whatsapp";
  status: "read";
  message_id: string;
}

async function markAsRead(messageId: string): Promise<boolean> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: MarkAsReadPayload = {
    messaging_product: "whatsapp",
    status: "read",
    message_id: messageId,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.success === true;
}
```

### Python

```python
async def mark_as_read(message_id: str) -> bool:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("success", False)
```

### 预期响应

```json
{
  "success": true
}
```

### 注意事项

- `message_id` 必须是**收到**的消息的 ID（不是发送的）。
- 标记为已读是幂等的：多次调用不会导致错误。
- 还会触发发送方聊天中的短暂"正在输入"指示器。
- 建议在 webhook 中处理消息时将其标记为已读，以提供良好的用户体验。

---

## 快速参考 - 限制和格式

| 类型            | 最大大小        | 格式                              | 说明文字 |
|---------------|---------------|-----------------------------------|---------|
| 文本           | 4096 字符     | -                                 | -       |
| 图片           | 5 MB          | JPEG、PNG                         | 1024 字符 |
| 文档           | 100 MB        | PDF、DOC、XLS、PPT、TXT 等       | 1024 字符 |
| 视频           | 16 MB         | MP4、3GPP（H.264 + AAC）          | 1024 字符 |
| 音频           | 16 MB         | OGG/OPUS、MP3、AMR、AAC、M4A      | N/A     |
| 贴纸           | 100 KB（静态）/ 500 KB（动画）| WEBP                | N/A     |

| 交互式          | 限制                                              |
|---------------|-----------------------------------------------------|
| 按钮           | 3 个按钮，标题最多 20 字符                          |
| 列表           | 10 个分区，总共 10 行，标题最多 24 字符              |
| 反应           | 每个发送者每条消息 1 个 emoji                        |

---

## 常见错误处理

上述所有函数都可能抛出 API 错误。标准错误结构：

```json
{
  "error": {
    "message": "(#131030) Recipient phone number not in allowed list",
    "type": "OAuthException",
    "code": 131030,
    "error_subcode": 2655007,
    "fbtrace_id": "AbCdEfGhIjKlMnOp"
  }
}
```

### 常见错误代码

| 代码      | 含义                                                |
|----------|----------------------------------------------------|
| 131030   | 收件人号码不在允许列表中                            |
| 131031   | 发送方账户被封锁                                    |
| 131047   | 重新参与消息（超过 24 小时窗口）                    |
| 131051   | 不支持的消息类型                                    |
| 131053   | 媒体上传失败                                        |
| 130429   | 超出速率限制                                        |
| 132000   | 模板参数数量不匹配                                  |
| 132015   | 模板已暂停/已禁用                                   |

### 带错误处理的包装器（Node.js）

```typescript
import axios, { AxiosError } from "axios";

interface WhatsAppError {
  error: {
    message: string;
    type: string;
    code: number;
    error_subcode?: number;
    fbtrace_id: string;
  };
}

async function sendWhatsAppRequest<T>(payload: T): Promise<Record<string, unknown>> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  try {
    const { data } = await axios.post(url, payload, {
      headers: {
        Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
        "Content-Type": "application/json",
      },
    });
    return data;
  } catch (err) {
    if (err instanceof AxiosError && err.response) {
      const waError = err.response.data as WhatsAppError;
      throw new Error(
        `WhatsApp API Error [${waError.error.code}]: ${waError.error.message}`
      );
    }
    throw err;
  }
}
```

### 带错误处理的包装器（Python）

```python
import httpx


class WhatsAppAPIError(Exception):
    def __init__(self, code: int, message: str, fbtrace_id: str):
        self.code = code
        self.fbtrace_id = fbtrace_id
        super().__init__(f"WhatsApp API Error [{code}]: {message}")


async def send_whatsapp_request(payload: dict) -> dict:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {
        "Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            error_data = response.json().get("error", {})
            raise WhatsAppAPIError(
                code=error_data.get("code", response.status_code),
                message=error_data.get("message", "Unknown error"),
                fbtrace_id=error_data.get("fbtrace_id", ""),
            )

        return response.json()
```
