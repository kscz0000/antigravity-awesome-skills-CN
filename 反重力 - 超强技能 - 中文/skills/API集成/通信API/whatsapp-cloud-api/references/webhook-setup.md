# Webhook 配置 - WhatsApp Cloud API

> WhatsApp Cloud API webhook 的配置、验证和安全保护完整指南。

---

## 1. 概述

Webhook 是 Meta 在您的 WhatsApp Business 账户上发生事件时向您的服务器发送的 HTTP 回调。没有 webhook，您就无法实时接收消息、送达确认和状态更新。

**强制要求：**

| 要求 | 详情 |
|-----------|---------|
| 协议 | 使用有效 SSL 证书的 HTTPS（不接受自签名） |
| 响应 | 在 **5 秒内** 返回 HTTP 200 OK |
| 可用性 | 端点必须可在公共互联网上访问 |
| 幂等性 | Meta 可能会重新发送相同的事件；请处理重复事件 |

如果您的服务器未在 5 秒内响应 200，Meta 将以指数退避的方式重新发送事件，最长持续 7 天。超过此期限后，webhook 将自动停用。

---

## 2. 在 Meta Developers 中配置

### 操作步骤

1. 访问 [developers.facebook.com](https://developers.facebook.com)
2. 选择您的应用
3. 在侧边栏菜单中：**WhatsApp > Configuration**
4. 在 **Webhook** 部分，点击 **Edit**

### 必填字段

| 字段 | 描述 |
|-------|-----------|
| **Callback URL** | 您服务器的 HTTPS URL（例如：`https://api.seudominio.com/webhook`） |
| **Verify Token** | 您定义的安全字符串（例如：`meu_token_secreto_2024`） |

### 要订阅的字段（Webhook Fields）

至少勾选：

- **messages** - 收到的消息、送达状态、阅读状态

有用的可选字段：

- **message_template_status_update** - 模板的批准/拒绝
- **account_update** - 企业账户的更改

> **重要：** Verify Token 与 API 的 Access Token **不同**。
> 选择一个强且唯一的值，并将其存储为环境变量。

---

## 3. Webhook 验证（GET）

当您在 Meta 控制面板中保存配置时，Meta 会发送一个 GET 请求来验证该端点属于您。此流程称为 **challenge-response**。

### 验证流程

```
Meta                            您的服务器
  |                                  |
  |  GET /webhook?                   |
  |    hub.mode=subscribe            |
  |    hub.verify_token=您的_TOKEN   |
  |    hub.challenge=RANDOM_STRING   |
  |  ---------------------------->>  |
  |                                  |  1. 验证 hub.verify_token
  |                                  |  2. 如果有效，返回 hub.challenge
  |  <<----------------------------  |
  |  HTTP 200 + challenge 作为 body  |
```

### Node.js / Express

```javascript
// GET /webhook - 验证端点
app.get('/webhook', (req, res) => {
  const VERIFY_TOKEN = process.env.WEBHOOK_VERIFY_TOKEN;

  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === VERIFY_TOKEN) {
    console.log('Webhook 验证成功');
    return res.status(200).send(challenge);
  }

  console.error('Webhook 验证失败：token 无效');
  return res.sendStatus(403);
});
```

### Python / Flask

```python
# GET /webhook - 验证端点
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    verify_token = os.environ.get('WEBHOOK_VERIFY_TOKEN')

    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == verify_token:
        print('Webhook 验证成功')
        return challenge, 200

    print('Webhook 验证失败：token 无效')
    return 'Forbidden', 403
```

### 验证中的常见错误

| 错误 | 原因 | 解决方案 |
|------|-------|---------|
| 403 Forbidden | Verify token 不匹配 | 验证环境变量 |
| Webhook 无法验证 | Challenge 作为 JSON 返回 | 以 **纯文本** 形式返回，而不是 JSON |
| 超时 | 服务器响应时间超过 5 秒 | 检查延迟和中间件 |
| SSL 错误 | 证书无效或已过期 | 使用 Let's Encrypt 或有效证书 |

> **经典错误：** 返回 `res.json({ challenge })` 而不是 `res.send(challenge)`。
> Meta 期望 challenge 作为响应正文中的纯文本。

---

## 4. 消息接收（POST）

验证后，Meta 通过 POST 发送事件。每个负载遵循相同的基础结构，但内容因事件类型而异。

### Node.js / Express - 完整处理程序

```javascript
// POST /webhook - 接收事件
app.post('/webhook', (req, res) => {
  // 始终立即返回 200
  res.sendStatus(200);

  const body = req.body;

  if (!body.object || !body.entry) return;

  for (const entry of body.entry) {
    for (const change of entry.changes) {
      if (change.field !== 'messages') continue;

      const value = change.value;
      const metadata = value.metadata;
      const phoneNumberId = metadata.phone_number_id;

      // 状态更新（sent, delivered, read, failed）
      if (value.statuses) {
        for (const status of value.statuses) {
          handleStatusUpdate(status);
        }
      }

      // 收到的消息
      if (value.messages) {
        for (const message of value.messages) {
          const from = message.from;
          const timestamp = message.timestamp;

          switch (message.type) {
            case 'text':
              handleTextMessage(from, message.text.body, phoneNumberId);
              break;
            case 'image':
            case 'video':
            case 'audio':
            case 'document':
              handleMediaMessage(from, message.type, message[message.type]);
              break;
            case 'interactive':
              handleInteractiveResponse(from, message.interactive);
              break;
            case 'button':
              handleButtonResponse(from, message.button);
              break;
            case 'location':
              handleLocationMessage(from, message.location);
              break;
            default:
              console.log(`未处理的消息类型：${message.type}`);
          }
        }
      }
    }
  }
});
```

### Python / Flask - 完整处理程序

```python
# POST /webhook - 接收事件
@app.route('/webhook', methods=['POST'])
def receive_webhook():
    body = request.get_json()

    if not body or 'entry' not in body:
        return 'OK', 200

    for entry in body.get('entry', []):
        for change in entry.get('changes', []):
            if change.get('field') != 'messages':
                continue

            value = change.get('value', {})
            metadata = value.get('metadata', {})
            phone_number_id = metadata.get('phone_number_id')

            # 状态更新
            for status in value.get('statuses', []):
                handle_status_update(status)

            # 收到的消息
            for message in value.get('messages', []):
                sender = message['from']
                msg_type = message['type']

                if msg_type == 'text':
                    handle_text_message(sender, message['text']['body'], phone_number_id)
                elif msg_type in ('image', 'video', 'audio', 'document'):
                    handle_media_message(sender, msg_type, message[msg_type])
                elif msg_type == 'interactive':
                    handle_interactive_response(sender, message['interactive'])
                elif msg_type == 'button':
                    handle_button_response(sender, message['button'])
                elif msg_type == 'location':
                    handle_location_message(sender, message['location'])

    return 'OK', 200
```

### 各事件类型的负载示例

**收到的文本消息：**
```json
{
  "messages": [{
    "from": "5511999887766",
    "id": "wamid.HBgNNTUxMTk5OTg...",
    "timestamp": "1677000000",
    "type": "text",
    "text": { "body": "Ola, preciso de ajuda" }
  }]
}
```

**交互式按钮回复（list/button reply）：**
```json
{
  "messages": [{
    "from": "5511999887766",
    "type": "interactive",
    "interactive": {
      "type": "button_reply",
      "button_reply": {
        "id": "btn_confirm",
        "title": "Confirmar pedido"
      }
    }
  }]
}
```

**状态更新（送达）：**
```json
{
  "statuses": [{
    "id": "wamid.HBgNNTUxMTk5OTg...",
    "status": "delivered",
    "timestamp": "1677000030",
    "recipient_id": "5511999887766"
  }]
}
```

---

## 5. HMAC-SHA256 安全（关键）

### 为什么至关重要

如果没有签名验证，任何发现您 webhook URL 的人都可以发送虚假负载。这允许：

- **消息欺骗** - 模拟客户发送从未发送过的内容
- **执行命令** - 如果 webhook 触发操作（支付、发货），攻击者可以控制
- **数据泄露** - 恶意负载可能利用解析缺陷

> **已记录的真实事件：** 一家电商公司在未验证签名的 webhook 中收到攻击者发送的"支付确认"虚假负载后，造成了 84.7 万美元的损失，触发了无实际支付的商品发货。

### 工作原理

对于每个 POST 请求，Meta 在 `X-Hub-Signature-256` 请求头中包含：

```
sha256=<hmac-sha256-hex-digest>
```

HMAC 使用 **App Secret** 作为密钥，**raw body** 作为消息计算得出。

### 验证步骤

```
1. 在 JSON 解析之前捕获 raw body
2. 提取 X-Hub-Signature-256 请求头
3. 计算 HMAC-SHA256(app_secret, raw_body)
4. 使用常量时间函数比较（防止时序攻击）
5. 如果不匹配，使用 401 拒绝
```

### Node.js / Express - 验证中间件

```javascript
const crypto = require('crypto');

function validateWebhookSignature(req, res, next) {
  const APP_SECRET = process.env.META_APP_SECRET;

  // 关键：必须在 json 解析器之前捕获 raw body
  // 按如下方式配置 Express：
  // app.use(express.json({
  //   verify: (req, _res, buf) => { req.rawBody = buf; }
  // }));

  const signature = req.headers['x-hub-signature-256'];

  if (!signature) {
    console.error('缺少 X-Hub-Signature-256 请求头');
    return res.sendStatus(401);
  }

  const expectedSignature = 'sha256=' + crypto
    .createHmac('sha256', APP_SECRET)
    .update(req.rawBody)
    .digest('hex');

  const signatureBuffer = Buffer.from(signature);
  const expectedBuffer = Buffer.from(expectedSignature);

  if (signatureBuffer.length !== expectedBuffer.length ||
      !crypto.timingSafeEqual(signatureBuffer, expectedBuffer)) {
    console.error('Webhook 签名无效');
    return res.sendStatus(401);
  }

  next();
}

// 使用：
// app.post('/webhook', validateWebhookSignature, webhookHandler);
```

### Python / Flask - 验证装饰器

```python
import hmac
import hashlib
from functools import wraps

def validate_webhook_signature(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        app_secret = os.environ.get('META_APP_SECRET')

        # 关键：raw body 必须在 JSON 解析之前
        raw_body = request.get_data()

        signature = request.headers.get('X-Hub-Signature-256', '')

        if not signature:
            print('缺少 X-Hub-Signature-256 请求头')
            return 'Unauthorized', 401

        expected = 'sha256=' + hmac.new(
            app_secret.encode('utf-8'),
            raw_body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected):
            print('Webhook 签名无效')
            return 'Unauthorized', 401

        return f(*args, **kwargs)
    return decorated

# 使用：
# @app.route('/webhook', methods=['POST'])
# @validate_webhook_signature
# def receive_webhook():
#     ...
```

### 经典错误：使用已解析的 body

```javascript
// 错误 - body 已被解析为 JSON，内容已更改
const hmac = crypto.createHmac('sha256', secret)
  .update(JSON.stringify(req.body))  // 不要这样做
  .digest('hex');

// 正确 - 使用原始 body
const hmac = crypto.createHmac('sha256', secret)
  .update(req.rawBody)  // 请求的原始 Buffer
  .digest('hex');
```

> **为什么会失败：** `JSON.stringify(JSON.parse(raw))` 可能产生与原始 raw 不同的输出（间距、键顺序、Unicode 字符编码）。Meta 的签名是根据精确的原始 body 计算的。

---

## 6. 本地开发

要在本地测试 webhook，您需要将本地服务器暴露到互联网。最常用的工具是 **ngrok**。

### 安装和使用 ngrok

```bash
# 安装（macOS）
brew install ngrok

# 安装（Windows via Chocolatey）
choco install ngrok

# 安装（Linux）
snap install ngrok

# 身份验证（仅需一次）
ngrok config add-authtoken 您的_AUTH_TOKEN

# 暴露本地 3000 端口
ngrok http 3000
```

### ngrok 输出

```
Session Status   online
Forwarding       https://a1b2c3d4.ngrok-free.app -> http://localhost:3000
```

### 在 Meta Developers 中配置

1. 复制 ngrok 的 HTTPS URL（例如：`https://a1b2c3d4.ngrok-free.app`）
2. 在 Meta 控制面板中，将 Callback URL 更新为：`https://a1b2c3d4.ngrok-free.app/webhook`
3. 保存并验证

> **注意：** ngrok 的 URL 在每次重启时都会更改（免费版）。
> 每次重启 ngrok 时，您都需要在 Meta 控制面板中更新 URL。

### 调试负载

```bash
# ngrok 的 Web 面板显示所有请求
# 访问：http://127.0.0.1:4040

# 替代方法：在服务器中记录详细日志
app.post('/webhook', (req, res) => {
  console.log('Headers:', JSON.stringify(req.headers, null, 2));
  console.log('Body:', JSON.stringify(req.body, null, 2));
  res.sendStatus(200);
});
```

### 本地开发提示

- 使用 `ngrok http 3000 --log=stdout` 在终端查看日志
- Web 检查器（`http://127.0.0.1:4040`）允许**重放**请求
- 添加 `/health` 端点以快速检查服务器是否在线
- 考虑使用 **localtunnel** 作为 ngrok 的免费替代品

---

## 7. 生产部署

### HTTPS 证书要求

- 由公认 CA 颁发的有效 SSL 证书
- **Let's Encrypt** 可被接受且免费
- 不接受**自签名证书**
- 确保配置了完整的证书链
- 配置自动续订（通过 cron 运行 certbot renew）

### 重试逻辑和幂等性

当未收到 HTTP 200 时，Meta 使用指数退避重新发送事件：

| 尝试 | 大约间隔 |
|-----------|---------------------|
| 第 1 次 | 立即 |
| 第 2 次 | ~1 分钟 |
| 第 3 次 | ~5 分钟 |
| 第 4 次 | ~30 分钟 |
| 后续 | 递增的退避，最长 7 天 |

**实现幂等性：**

```javascript
const processedMessages = new Set(); // 在生产环境中使用 Redis

function isNewMessage(messageId) {
  if (processedMessages.has(messageId)) {
    return false;
  }
  processedMessages.add(messageId);

  // 24 小时后清除旧消息（在生产环境中使用 Redis 的 TTL）
  setTimeout(() => processedMessages.delete(messageId), 86400000);
  return true;
}

// 在处理程序中：
if (!isNewMessage(message.id)) {
  console.log(`重复消息 ${message.id}，已跳过`);
  return;
}
```

### 扩展和容量

Meta 建议您的服务器支持：

| 指标 | 建议 |
|---------|-------------|
| 入口容量 | 发送消息量的 **3 倍** + 接收消息量的 **1 倍** |
| 响应时间 | < 5 秒（理想情况下 < 1 秒） |
| 可用性 | 最低 99.9% 正常运行时间 |

**高容量推荐架构：**

```
[Meta Webhook] --> [Load Balancer]
                        |
                   [Web Server]  --> 立即返回 200
                        |
                   [Message Queue] (Redis/SQS/RabbitMQ)
                        |
                   [Workers]  --> 异步处理
```

### Webhook 健康监控

```javascript
// 健康检查端点
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// 监控的关键指标：
// - /webhook 端点的 4xx/5xx 错误率
// - 平均响应延迟（应 < 1 秒）
// - 收到的重复消息数量
// - 处理队列（大小和平均时间）
// - HMAC 验证失败（可能存在攻击）
```

**推荐告警：**

| 告警 | 阈值 | 措施 |
|--------|-----------|------|
| 高延迟 | > 3 秒 | 调查瓶颈，扩展 workers |
| 错误率 | > 1% | 检查日志，处理程序中可能存在 bug |
| HMAC 失败 | > 0/小时 | 可能存在攻击；验证 APP_SECRET |
| 队列增长 | > 1000 条消息 | 扩展处理 workers |
| Webhook 已停用 | Meta 告警 | 验证 SSL 和可用性 |

---

## 最终检查清单

- [ ] 端点可通过有效证书的 HTTPS 访问
- [ ] GET 验证以纯文本形式返回 challenge
- [ ] POST 处理程序在 5 秒内返回 200
- [ ] 使用 raw body 实现 HMAC-SHA256 验证
- [ ] 常量时间比较（timingSafeEqual / compare_digest）
- [ ] 重复消息的幂等性
- [ ] 耗时操作的异步处理
- [ ] 监控和告警已配置
- [ ] APP_SECRET 和 VERIFY_TOKEN 存储在环境变量中（绝不在代码中）
- [ ] 用于生产环境调试的结构化日志
