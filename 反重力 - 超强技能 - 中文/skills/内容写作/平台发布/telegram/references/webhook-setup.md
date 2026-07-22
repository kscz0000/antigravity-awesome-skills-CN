# Webhook 设置 - Telegram Bot

## 目录
1. [概念](#conceitos)
2. [Express.js (Node.js)](#expressjs)
3. [Flask (Python)](#flask)
4. [FastAPI (Python)](#fastapi)
5. [ngrok（开发环境）](#ngrok)
6. [生产环境部署](#deploy)
7. [安全](#seguranca)
8. [故障排除](#troubleshooting)

---

## 概念

Webhook 是生产环境推荐的方式。Telegram 通过 HTTP POST 将更新发送到你的 HTTPS URL。

**要求：**
- 有效的 HTTPS URL（SSL 证书）
- 支持的端口：443、80、88、8443
- 在 60 秒内响应 HTTP 200
- 如果无响应，Telegram 会以指数退避重试

**注册 webhook：**
```
POST https://api.telegram.org/bot<TOKEN>/setWebhook
{
  "url": "https://seu-dominio.com/webhook/<TOKEN>",
  "allowed_updates": ["message", "callback_query", "inline_query"],
  "max_connections": 40,
  "secret_token": "seu_token_secreto_256chars_max"
}
```

**验证 webhook：**
```
GET https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

**删除 webhook：**
```
POST https://api.telegram.org/bot<TOKEN>/deleteWebhook
{"drop_pending_updates": true}
```

---

## Express.js

```typescript
import express from 'express';
import TelegramBot from 'node-telegram-bot-api';

const app = express();
const TOKEN = process.env.TELEGRAM_BOT_TOKEN!;
const WEBHOOK_URL = process.env.WEBHOOK_URL!; // https://seu-dominio.com
const SECRET_TOKEN = process.env.WEBHOOK_SECRET || 'meu-secret-seguro';

// 不使用轮询的机器人（webhook 模式）
const bot = new TelegramBot(TOKEN);

app.use(express.json());

// 验证 secret token
app.post(`/webhook/${TOKEN}`, (req, res) => {
  const secretHeader = req.headers['x-telegram-bot-api-secret-token'];
  if (secretHeader !== SECRET_TOKEN) {
    return res.sendStatus(403);
  }

  bot.processUpdate(req.body);
  res.sendStatus(200);
});

// 健康检查
app.get('/health', (req, res) => res.json({ status: 'ok' }));

// 启动时注册 webhook
async function start() {
  await bot.setWebHook(`${WEBHOOK_URL}/webhook/${TOKEN}`, {
    max_connections: 40,
    allowed_updates: ['message', 'callback_query'],
    secret_token: SECRET_TOKEN,
  });

  const info = await bot.getWebHookInfo();
  console.log('Webhook 信息:', info);

  app.listen(3000, () => console.log('服务器运行在端口 3000'));
}

// 处理器
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, '机器人通过 webhook 激活！');
});

start();
```

---

## Flask

```python
import os
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
SECRET_TOKEN = os.getenv('WEBHOOK_SECRET', 'meu-secret-seguro')

flask_app = Flask(__name__)

# 创建 telegram application
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text('机器人通过 webhook 激活！')

application.add_handler(CommandHandler('start', start))

@flask_app.route(f'/webhook/{TOKEN}', methods=['POST'])
async def webhook():
    # 验证 secret token
    secret = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    if secret != SECRET_TOKEN:
        return 'Forbidden', 403

    update = Update.de_json(request.get_json(), application.bot)
    await application.process_update(update)
    return 'OK', 200

@flask_app.route('/health')
def health():
    return jsonify(status='ok')

# 注册 webhook
import requests
requests.post(
    f'https://api.telegram.org/bot{TOKEN}/setWebhook',
    json={
        'url': f'{WEBHOOK_URL}/webhook/{TOKEN}',
        'allowed_updates': ['message', 'callback_query'],
        'secret_token': SECRET_TOKEN,
        'max_connections': 40
    }
)
```

---

## FastAPI

```python
import os
from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
SECRET_TOKEN = os.getenv('WEBHOOK_SECRET', 'meu-secret-seguro')

app = FastAPI()
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text('机器人通过 FastAPI webhook 激活！')

application.add_handler(CommandHandler('start', start))

@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.set_webhook(
        url=f'{WEBHOOK_URL}/webhook/{TOKEN}',
        allowed_updates=['message', 'callback_query'],
        secret_token=SECRET_TOKEN
    )

@app.on_event("shutdown")
async def on_shutdown():
    await application.shutdown()

@app.post(f'/webhook/{TOKEN}')
async def webhook(request: Request):
    secret = request.headers.get('x-telegram-bot-api-secret-token')
    if secret != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail='Forbidden')

    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {'status': 'ok'}

@app.get('/health')
def health():
    return {'status': 'ok'}
```

---

## ngrok（开发环境）

对于本地开发，使用 ngrok 通过 HTTPS 暴露本地端口：

```bash
# 安装 ngrok: https://ngrok.com/download
ngrok http 3000
```

ngrok 会提供类似 `https://abc123.ngrok-free.app` 的 URL。使用该 URL 注册 webhook。

```bash
curl -X POST "https://api.telegram.org/bot$TOKEN/setWebhook" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://abc123.ngrok-free.app/webhook/$TOKEN\"}"
```

**免费替代方案：** localtunnel
```bash
npx localtunnel --port 3000
```

---

## 生产环境部署

### Railway
```bash
# railway.json
{
  "build": { "builder": "nixpacks" },
  "deploy": { "startCommand": "npm start" }
}
```

### Render
```yaml
# render.yaml
services:
  - type: web
    name: telegram-bot
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
```

### Vercel（Serverless）
```typescript
// api/webhook.ts
import { VercelRequest, VercelResponse } from '@vercel/node';
import TelegramBot from 'node-telegram-bot-api';

const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN!);

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'POST') {
    bot.processUpdate(req.body);
    res.status(200).send('OK');
  } else {
    res.status(200).json({ status: 'ok' });
  }
}
```

### Docker
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

---

## 安全

1. **Secret Token:** 注册 webhook 时始终使用 `secret_token`，并验证 `X-Telegram-Bot-Api-Secret-Token` 头
2. **URL 包含令牌:** 在 webhook URL 中包含令牌作为额外安全层
3. **IP 白名单:** Telegram 从以下 IP 发送 webhook：
   - `149.154.160.0/20`
   - `91.108.4.0/22`
4. **必须 HTTPS:** 生产环境切勿使用 HTTP
5. **不要暴露令牌:** 使用环境变量，切勿硬编码

---

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Webhook 未收到更新 | URL 错误或 SSL 无效 | 用 `getWebhookInfo` 检查 |
| 错误 409 Conflict | 轮询和 webhook 同时激活 | 删除 webhook 或停止轮询 |
| 错误 401 Unauthorized | 令牌无效 | 用 `/getMe` 验证令牌 |
| 更新重复 | 未返回 200 | 确保处理器返回 HTTP 200 |
| `last_error_message` | 多种原因 | 检查 `getWebhookInfo` 中的该字段 |
| 超时 | 处理器耗时 >60 秒 | 异步处理，快速返回 200 |
