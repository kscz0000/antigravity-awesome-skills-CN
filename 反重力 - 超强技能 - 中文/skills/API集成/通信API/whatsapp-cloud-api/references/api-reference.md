# API 参考 - WhatsApp Cloud API

WhatsApp Cloud API（Graph API v21.0）端点、认证、错误代码、速率限制和价格的完整技术参考。

---

## 目录

1. [认证](#autenticacao)
2. [基础 URL 和请求头](#base-url-e-headers)
3. [端点 - 消息](#endpoints---mensagens)
4. [端点 - 媒体](#endpoints---midia)
5. [端点 - 模板](#endpoints---templates)
6. [端点 - 电话号码](#endpoints---phone-numbers)
7. [端点 - 商家资料](#endpoints---business-profile)
8. [Webhook 事件](#webhook-events)
9. [错误代码](#codigos-de-erro)
10. [速率限制](#rate-limits)
11. [2026 年价格](#pricing-2026)
12. [版本管理](#versionamento)

---

## 认证

### 临时 Token（开发环境）

在 Meta Developers Dashboard 获取。24 小时后过期。

### System User Token（生产环境）

通过 Business Settings 创建的永久 Token：
1. Business Settings → System Users → Add
2. 为应用分配 "Admin" 角色
3. 生成具有以下权限的 Token：
   - `whatsapp_business_messaging`（发送/接收消息）
   - `whatsapp_business_management`（管理模板、个人资料）

### 认证请求头

```
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json
```

---

## 基础 URL 和请求头

```
Base URL: https://graph.facebook.com/v21.0
```

所有请求中必需的请求头：
```http
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json
```

### 必需的 ID

| ID                  | 查找位置                               | 格式            |
|---------------------|---------------------------------------|-----------------|
| Phone Number ID     | 仪表板中的 WhatsApp > API Setup         | 数字型          |
| WABA ID             | 仪表板中的 WhatsApp > API Setup         | 数字型          |
| App Secret          | App Settings > Basic                   | 十六进制字符串  |
| Business ID         | Business Settings > Business Info      | 数字型          |

---

## 端点 - 消息

### 发送消息

```
POST /{phone-number-id}/messages
```

**请求正文（文本）：**
```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "text",
  "text": {
    "preview_url": false,
    "body": "Olá! Como posso ajudar?"
  }
}
```

**响应（成功）：**
```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    { "input": "5511999999999", "wa_id": "5511999999999" }
  ],
  "messages": [
    { "id": "wamid.HBgNNTUxMTk5..." }
  ]
}
```

**`type` 字段支持的类型：**
- `text` - 文本消息
- `template` - 模板消息
- `image` - 图片
- `document` - 文档
- `video` - 视频
- `audio` - 音频
- `sticker` - 贴纸
- `location` - 位置
- `contacts` - 联系人
- `interactive` - 按钮、列表、flows
- `reaction` - emoji 反应

### 标记为已读

```
POST /{phone-number-id}/messages
```

```json
{
  "messaging_product": "whatsapp",
  "status": "read",
  "message_id": "wamid.HBgNNTUxMTk5..."
}
```

---

## 端点 - 媒体

### 上传媒体

```
POST /{phone-number-id}/media
Content-Type: multipart/form-data
```

**表单字段：**
- `messaging_product`："whatsapp"
- `file`：二进制文件
- `type`：MIME 类型（例如 "image/jpeg"）

**响应：**
```json
{
  "id": "media_id_aqui"
}
```

### 下载媒体

```
GET /{media-id}
```

**响应：**
```json
{
  "url": "https://lookaside.fbsbx.com/...",
  "mime_type": "image/jpeg",
  "sha256": "hash_aqui",
  "file_size": 12345,
  "id": "media_id"
}
```

之后，使用相同的 Authorization 请求头对返回的 `url` 执行 GET 以下载文件。

### 删除媒体

```
DELETE /{media-id}
```

### 媒体限制

| 类型      | 支持的格式                          | 最大大小  |
|-----------|-------------------------------------|----------|
| Image     | JPEG、PNG                           | 5 MB     |
| Document  | PDF、DOC、DOCX、XLS、XLSX、PPT、TXT | 100 MB   |
| Video     | MP4、3GP                            | 16 MB    |
| Audio     | AAC、AMR、MP3、MP4、OGG             | 16 MB    |
| Sticker   | WEBP                                | 500 KB   |

---

## 端点 - 模板

### 列出模板

```
GET /{waba-id}/message_templates
```

**查询参数：**
- `limit` - 结果数量（默认：25）
- `status` - 按状态过滤：APPROVED、PENDING、REJECTED

**响应：**
```json
{
  "data": [
    {
      "name": "hello_world",
      "status": "APPROVED",
      "category": "UTILITY",
      "language": "pt_BR",
      "components": [
        {
          "type": "BODY",
          "text": "Olá {{1}}, seu pedido {{2}} foi confirmado!"
        }
      ],
      "id": "template_id"
    }
  ],
  "paging": { "cursors": { "before": "...", "after": "..." } }
}
```

### 创建模板

```
POST /{waba-id}/message_templates
```

```json
{
  "name": "order_confirmation",
  "category": "UTILITY",
  "language": "pt_BR",
  "components": [
    {
      "type": "HEADER",
      "format": "TEXT",
      "text": "Confirmação de Pedido"
    },
    {
      "type": "BODY",
      "text": "Olá {{1}}, seu pedido #{{2}} foi confirmado! Valor: R$ {{3}}",
      "example": {
        "body_text": [["João", "12345", "99,90"]]
      }
    },
    {
      "type": "FOOTER",
      "text": "Obrigado por comprar conosco!"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "URL",
          "text": "Rastrear Pedido",
          "url": "https://example.com/track/{{1}}",
          "example": ["12345"]
        }
      ]
    }
  ]
}
```

### 删除模板

```
DELETE /{waba-id}/message_templates
```

```json
{
  "name": "template_name_to_delete"
}
```

**注意：** 提交后无法编辑模板。要修改，请删除并创建新模板。

**限制：** 每个账户最多 6,000 个模板翻译版本。

有关模板管理的完整指南，请阅读 `references/template-management.md`。

---

## 端点 - 电话号码

### 列出号码

```
GET /{waba-id}/phone_numbers
```

**响应：**
```json
{
  "data": [
    {
      "verified_name": "Minha Empresa",
      "code_verification_status": "VERIFIED",
      "display_phone_number": "+55 11 99999-9999",
      "quality_rating": "GREEN",
      "id": "phone_number_id"
    }
  ]
}
```

### 获取号码信息

```
GET /{phone-number-id}?fields=verified_name,code_verification_status,display_phone_number,quality_rating,messaging_limit_tier
```

---

## 端点 - 商家资料

### 获取资料

```
GET /{phone-number-id}/whatsapp_business_profile?fields=about,address,description,email,websites,profile_picture_url
```

### 更新资料

```
POST /{phone-number-id}/whatsapp_business_profile
```

```json
{
  "messaging_product": "whatsapp",
  "about": "Atendimento de Seg a Sex, 8h-18h",
  "address": "Rua Example, 123 - São Paulo, SP",
  "description": "Empresa líder em soluções digitais",
  "email": "contato@empresa.com",
  "websites": ["https://www.empresa.com"]
}
```

---

## Webhook 事件

### 负载结构

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WABA_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "5511999999999",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "contacts": [
              { "profile": { "name": "João" }, "wa_id": "5511888888888" }
            ],
            "messages": [...],
            "statuses": [...]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

### 接收消息类型

| 字段 `type`     | 内容                    | 相关字段                              |
|-----------------|-------------------------|--------------------------------------|
| `text`          | 文本消息                | `text.body`                          |
| `image`         | 图片                    | `image.id`、`image.mime_type`        |
| `document`      | 文档                    | `document.id`、`document.filename`   |
| `video`         | 视频                    | `video.id`、`video.mime_type`        |
| `audio`         | 音频/语音               | `audio.id`、`audio.mime_type`        |
| `location`      | 位置                    | `location.latitude`、`.longitude`    |
| `contacts`      | 共享联系人              | `contacts[].name`、`.phones`         |
| `interactive`   | 按钮/列表回复           | `interactive.button_reply.id` 或 `interactive.list_reply.id` |
| `reaction`      | emoji 反应              | `reaction.emoji`、`.message_id`      |
| `sticker`       | 贴纸                    | `sticker.id`、`sticker.mime_type`    |

### 状态更新

```json
{
  "statuses": [
    {
      "id": "wamid.HBgNNTUxMTk5...",
      "status": "delivered",
      "timestamp": "1234567890",
      "recipient_id": "5511999999999"
    }
  ]
}
```

`status` 取值：`sent` → `delivered` → `read` → `failed`

---

## 错误代码

### 常见错误

| 代码    | 消息                              | 原因                              | 解决方案                              |
|---------|-----------------------------------|-----------------------------------|--------------------------------------|
| 0       | AuthException                     | Token 无效或过期                  | 生成新 Token                         |
| 3       | API Method                        | HTTP 方法错误                     | 检查 POST vs GET                     |
| 4       | Too many calls                    | 超出速率限制                      | 实现带退避的重试                     |
| 10      | Permission denied                 | Token 缺少必要权限                | 向 System User 添加权限              |
| 100     | Invalid parameter                 | 负载格式错误                      | 参照文档检查 JSON                    |
| 131026  | Message undeliverable             | 号码不在 WhatsApp 上              | 发送前验证号码                       |
| 131047  | Re-engagement message             | 24 小时窗口外未使用模板          | 使用模板消息                         |
| 131051  | Unsupported message type          | 不支持的消息类型                  | 检查 `type` 字段                     |
| 131053  | Media upload error                | 文件无效或过大                    | 检查格式和大小                       |
| 132000  | Template param count mismatch     | 参数数量错误                      | 检查模板和参数                       |
| 132001  | Template does not exist           | 模板未找到                        | 验证模板名称和语言                   |
| 132005  | Template hydration failed         | 填充变量出错                      | 检查参数格式                         |
| 133010  | Phone number not registered       | 号码未验证                        | 完成 OTP 验证                        |
| 135000  | Generic error                     | WhatsApp 内部错误                 | 几秒后重试                           |

### 错误处理

```typescript
async function sendWithRetry(payload: any, maxRetries = 3): Promise<any> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await axios.post(
        `${GRAPH_API}/${process.env.PHONE_NUMBER_ID}/messages`,
        payload,
        { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
      );
      return response.data;
    } catch (error: any) {
      const errorCode = error.response?.data?.error?.code;
      const errorMessage = error.response?.data?.error?.message;

      // 不应重试的错误
      if ([100, 131026, 131051, 132000, 132001].includes(errorCode)) {
        throw new Error(`WhatsApp API Error ${errorCode}: ${errorMessage}`);
      }

      // 速率限制或临时错误 - 带退避重试
      if (attempt < maxRetries && [4, 135000].includes(errorCode)) {
        const delay = Math.pow(2, attempt) * 1000; // 2 秒、4 秒、8 秒
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }

      throw error;
    }
  }
}
```

---

## 速率限制

### 吞吐量（每秒消息数）

| 等级              | 限制              |
|-------------------|-------------------|
| Standard          | 80 msg/s          |
| Unlimited tier    | 1,000 msg/s       |

### 每 24 小时对话数

| 等级         | 每 24 小时限制 | 如何达到                              |
|--------------|----------------|--------------------------------------|
| 初始         | 250            | 新账号或未验证                       |
| Tier 1       | 1,000          | 7 天内使用 50%+ 限额且质量良好       |
| Tier 2       | 10,000         | 7 天内使用 50%+ 限额且质量良好       |
| Tier 3       | 100,000        | 7 天内使用 50%+ 限额且质量良好       |
| 无限         | 无限制         | 7 天内使用 50%+ 限额且质量良好       |

**重要：** 自 2025 年 10 月起，限制按 Business Portfolio（而非按号码）计算。

### 其他限制

- 模板：每个账户 6,000 个翻译版本
- 交互按钮：每条消息最多 3 个
- 交互列表：最多 10 个选项，最多 3 个分区
- 文本：最多 4,096 字符
- 模板正文：最多 1,600 字符
- Webhook：5 秒内返回 200 响应

---

## 2026 年价格

自 2025 年 7 月起，定价模型**按消息**计算（不再是按对话）。

### 各类别费用

| 类别          | 价格范围              | 批量折扣    | 24 小时窗口  |
|---------------|----------------------|------------|-------------|
| Marketing     | $0.025 - $0.1365     | 无         | 计费         |
| Utility       | $0.004 - $0.0456     | 有         | 免费         |
| Authentication| $0.004 - $0.0456     | 有         | 计费         |
| Service       | 免费                 | 不适用     | 免费         |

### 各区域示例（Marketing）

| 区域              | 单条费用  |
|-------------------|----------|
| 巴西              | ~$0.05   |
| 印度              | ~$0.01   |
| 美国/加拿大        | ~$0.025  |
| 西欧              | ~$0.10+  |

### 24 小时窗口

- 当客户发送消息时打开
- 窗口期内：**utility** 模板免费
- Service 消息（回复）始终免费
- Marketing 和 authentication 在窗口期内也计费

### 2026 年 1 月变化

- 法国和埃及：Marketing 费用降低
- 印度：Marketing 费用上涨
- 北美：Utility 和 authentication 费用降低

---

## 版本管理

### 当前版本

**Graph API v21.0**（2026 年 1 月发布）

### 兼容性

- Meta 至少保持 12 个月的向后兼容
- 旧版本在移除前会收到弃用通知
- 始终在 URL 中指定版本：`https://graph.facebook.com/v21.0/`

### 2026 年计划变更

| 功能                       | 时间表   | 描述                                          |
|---------------------------|---------|----------------------------------------------|
| BSUID                     | 2026    | Business-Scoped User ID 替代电话号码         |
| Usernames                 | 2026    | WhatsApp 引入用户名以保护隐私                |
| 等级移除（2K/10K）        | Q2 2026 | 验证后立即获得 100K 限额                     |
| Business Portfolio Pacing | Q1 2026 | 根据反馈自动暂停营销活动                     |

### 版本管理最佳实践

- 关注 Meta 开发者博客以获取变更信息
- 在生产环境升级前在沙盒中进行测试
- 使用环境变量管理 API 版本（便于回滚）
- 保留调用日志以便进行兼容性调试
