---
name: telegram
description: Telegram Bot API 完整集成。BotFather 设置、消息、Webhook、内联键盘、群组、频道。Node.js 和 Python 模板代码。
risk: critical
source: community
date_added: '2026-03-06'
author: renat
tags:
- messaging
- telegram
- bots
- webhooks
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Telegram Bot API - 专业集成

## 概述

Telegram Bot API 完整集成。BotFather 设置、消息、Webhook、内联键盘、群组、频道。Node.js 和 Python 模板代码。

## 何时使用此技能

- 当用户提到 "telegram" 或相关话题时
- 当用户提到 "bot telegram" 或相关话题时
- 当用户提到 "telegram bot" 或相关话题时
- 当用户提到 "api telegram" 或相关话题时
- 当用户提到 "chatbot telegram" 或相关话题时
- 当用户提到 "telegram 消息" 或相关话题时

## 何时不使用此技能

- 任务与 Telegram 无关
- 更简单、更具体的工具可以处理请求
- 用户需要的是无需领域专业知识的通用帮助

## 工作原理

用于使用官方 Bot API 实现专业 Telegram 机器人的技能。支持 Node.js/TypeScript 和 Python。

## 概述

Telegram Bot API 允许创建通过消息、命令、内联键盘、支付等方式与用户交互的机器人。机器人通过 @BotFather 创建，并通过唯一令牌进行身份验证。

**基础 URL：** `https://api.telegram.org/bot<TOKEN>/METHOD_NAME`
**HTTP 方法：** GET 和 POST
**参数格式：** query string、application/x-www-form-urlencoded、application/json、multipart/form-data（上传文件）
**文件限制：** 下载 50MB，上传 20MB（通过 multipart），通过 URL 50MB

**Webhook 支持的端口：** 443、80、88、8443

**前置条件：**
- Telegram 账号
- 通过 @BotFather 创建的机器人（提供令牌）
- 令牌格式：`123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

如果用户还没有创建机器人，引导用户在 Telegram 中与 @BotFather 对话并发送 `/newbot`。

---

## 决策树

```
用户需要创建机器人吗？
├── 是 → 参见下方"BotFather 设置"章节
└── 否 → 使用哪种语言？
    ├── Node.js/TypeScript
    └── Python
    → 想做什么？
       ├── 发送消息 → "消息类型"章节
       ├── 接收消息 → "接收更新"章节
       ├── 交互式键盘 → "键盘"章节
       ├── 管理群组/频道 → references/chat-management.md
       ├── Webhook 设置 → references/webhook-setup.md
       ├── 内联模式 → references/advanced-features.md
       ├── 支付 → references/advanced-features.md
       ├── AI 客服机器人 → "AI 自动化"章节
       └── API 完整参考 → references/api-reference.md
```

使用现成模板从零开始项目：
```bash
python scripts/setup_project.py --language nodejs --path ./meu-bot-telegram

## 或

python scripts/setup_project.py --language python --path ./meu-bot-telegram
```

测试机器人令牌是否有效：
```bash
python scripts/test_bot.py --token "SEU_TOKEN"
```

发送测试消息：
```bash
python scripts/send_message.py --token "SEU_TOKEN" --chat-id "CHAT_ID" --text "Hello!"
```

---

## BotFather 设置

1. 打开 Telegram 搜索 @BotFather
2. 发送 `/newbot`
3. 选择显示名称（例如："我的超棒机器人"）
4. 选择用户名（必须以 "bot" 结尾，例如：`meu_incrivel_bot`）
5. BotFather 返回令牌 - 妥善保存
6. BotFather 实用命令：
   - `/setdescription` - 机器人描述
   - `/setabouttext` - 机器人"关于"文本
   - `/setuserpic` - 头像
   - `/setcommands` - 命令列表
   - `/mybots` - 管理已有机器人
   - `/setinline` - 启用内联模式
   - `/setprivacy` - 群组隐私模式

---

## 环境变量

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

## Node.js/TypeScript

```typescript
// 安装：npm install node-telegram-bot-api dotenv
// TypeScript 额外安装：npm install -D @types/node-telegram-bot-api typescript
import TelegramBot from 'node-telegram-bot-api';
import dotenv from 'dotenv';
dotenv.config();

const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN!, { polling: true });

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, '你好！我是你的机器人。有什么可以帮你的？');
});

bot.on('message', (msg) => {
  if (msg.text && !msg.text.startsWith('/')) {
    bot.sendMessage(msg.chat.id, `你说的是：${msg.text}`);
  }
});
```

## Python

```python

## 安装：pip install python-telegram-bot python-dotenv

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('你好！我是你的机器人。有什么可以帮你的？')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'你说的是：{update.message.text}')

app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.run_polling()
```

## 无库（纯 HTTP）

```python
import requests

TOKEN = "SEU_TOKEN"
BASE = f"https://api.telegram.org/bot{TOKEN}"

## 验证机器人

r = requests.get(f"{BASE}/getMe")
print(r.json())

## 发送消息

r = requests.post(f"{BASE}/sendMessage", json={
    "chat_id": "CHAT_ID",
    "text": "Hello from pure HTTP!",
    "parse_mode": "HTML"
})
print(r.json())
```

---

## 消息类型

Telegram 支持多种内容类型。所有方法都接受 `chat_id`、`reply_parameters`（用于回复）、`reply_markup`（用于键盘）、`disable_notification` 和 `protect_content`。

## HTML（推荐）

await bot.send_message(
    chat_id=chat_id,
    text="<b>粗体</b>, <i>斜体</i>, <code>代码</code>, <a href='https://example.com'>链接</a>",
    parse_mode="HTML"
)

## MarkdownV2（需转义特殊字符：_ * [ ] ( ) ~ ` > # + - = | { } . !）

await bot.send_message(
    chat_id=chat_id,
    text="*粗体*, _斜体_, `代码`, [链接](https://example\\.com)",
    parse_mode="MarkdownV2"
)
```

## 图片（通过 URL、File_Id 或上传）

await bot.send_photo(chat_id, photo="https://example.com/img.jpg", caption="图片说明")

## 文档

await bot.send_document(chat_id, document=open("relatorio.pdf", "rb"), caption="月度报告")

## 视频

await bot.send_video(chat_id, video="https://example.com/video.mp4", caption="看看这个！")

## 音频

await bot.send_audio(chat_id, audio=open("musica.mp3", "rb"), title="我的音乐")

## 语音（Ogg Opus 格式）

await bot.send_voice(chat_id, voice=open("audio.ogg", "rb"))

## 位置

await bot.send_location(chat_id, latitude=-23.5505, longitude=-46.6333)

## 联系人

await bot.send_contact(chat_id, phone_number="+5511999999999", first_name="Joao")

## 投票

await bot.send_poll(
    chat_id, question="你最喜欢的颜色是什么？",
    options=["蓝色", "绿色", "红色"],
    is_anonymous=False
)

## 媒体组

await bot.send_media_group(chat_id, media=[
    InputMediaPhoto("url1", caption="图片 1"),
    InputMediaPhoto("url2"),
    InputMediaVideo("url3")
])

## 聊天动作（typing、upload_photo 等）

await bot.send_chat_action(chat_id, action="typing")
```

## Node.js 等效代码

```typescript
// 图片
bot.sendPhoto(chatId, 'https://example.com/img.jpg', { caption: '图片说明' });

// 文档
bot.sendDocument(chatId, fs.createReadStream('relatorio.pdf'), { caption: '报告' });

// 位置
bot.sendLocation(chatId, -23.5505, -46.6333);

// 投票
bot.sendPoll(chatId, '你最喜欢的颜色是什么？', ['蓝色', '绿色', '红色']);
```

---

## 内联键盘（消息内的按钮）

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("选项 A", callback_data="opt_a"),
     InlineKeyboardButton("选项 B", callback_data="opt_b")],
    [InlineKeyboardButton("打开网站", url="https://example.com")],
    [InlineKeyboardButton("分享", switch_inline_query="texto")]
])

await bot.send_message(chat_id, "请选择一个选项：", reply_markup=keyboard)

## 回调处理器

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # 重要：始终回复回调
    await query.edit_message_text(f"你选择了：{query.data}")

app.add_handler(CallbackQueryHandler(button_callback))
```

## 回复键盘（自定义键盘）

```python
from telegram import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("发送位置", request_location=True)],
     [KeyboardButton("发送联系人", request_contact=True)],
     ["选项 1", "选项 2"]],
    resize_keyboard=True,
    one_time_keyboard=True
)

await bot.send_message(chat_id, "请选择：", reply_markup=keyboard)
```

## 移除键盘

```python
from telegram import ReplyKeyboardRemove
await bot.send_message(chat_id, "键盘已移除", reply_markup=ReplyKeyboardRemove())
```

---

## 接收更新

有两种接收更新的方式：**长轮询** 和 **Webhook**。

## 长轮询（开发环境）

更简单，适合开发。机器人定期向 Telegram 服务器发送请求。

```python

## python-telegram-bot 已自动处理

app.run_polling(allowed_updates=Update.ALL_TYPES)
```

```typescript
// node-telegram-bot-api 使用轮询
const bot = new TelegramBot(token, { polling: true });
```

## Webhook（生产环境）

生产环境中 Webhook 更高效。Telegram 通过 POST 将更新发送到你的 HTTPS URL。

阅读 `references/webhook-setup.md` 了解使用 Express、Flask、ngrok 和部署的完整配置。

快速设置：

```python

## Flask Webhook

from flask import Flask, request
import requests

app = Flask(__name__)
TOKEN = "SEU_TOKEN"
BASE = f"https://api.telegram.org/bot{TOKEN}"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        requests.post(f"{BASE}/sendMessage", json={
            "chat_id": chat_id,
            "text": f"收到：{text}"
        })
    return "OK", 200

## 注册 Webhook

requests.post(f"{BASE}/setWebhook", json={
    "url": "https://seu-dominio.com/webhook/" + TOKEN,
    "allowed_updates": ["message", "callback_query"],
    "secret_token": "seu_secret_seguro_aqui"
})
```

---

## 机器人命令

注册命令以显示在 Telegram 菜单中：

```python
from telegram import BotCommand

await bot.set_my_commands([
    BotCommand("start", "启动机器人"),
    BotCommand("help", "查看可用命令"),
    BotCommand("settings", "设置"),
    BotCommand("status", "查看服务状态"),
])
```

通过 HTTP：
```bash
curl -X POST "https://api.telegram.org/bot$TOKEN/setMyCommands" \
  -H "Content-Type: application/json" \
  -d '{"commands":[{"command":"start","description":"启动机器人"},{"command":"help","description":"帮助"}]}'
```

---

## AI 自动化

AI 客服机器人模式（Claude、GPT 等）：

```python
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import anthropic  # 或 openai

client = anthropic.Anthropic()
user_conversations = {}  # chat_id -> 消息历史

async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_text = update.message.text

    # 显示正在输入
    await context.bot.send_chat_action(chat_id, "typing")

    # 维护历史记录
    if chat_id not in user_conversations:
        user_conversations[chat_id] = []

    user_conversations[chat_id].append({"role": "user", "content": user_text})

    # 调用 AI
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="你是一个有用的助手。用中文回答。",
        messages=user_conversations[chat_id]
    )

    reply = response.content[0].text
    user_conversations[chat_id].append({"role": "assistant", "content": reply})

    # 限制历史记录（最近 20 条消息）
    if len(user_conversations[chat_id]) > 20:
        user_conversations[chat_id] = user_conversations[chat_id][-20:]

    await update.message.reply_text(reply)

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response))
app.run_polling()
```

---

## 编辑文本

await bot.edit_message_text(
    chat_id=chat_id,
    message_id=msg.message_id,
    text="文本已更新！",
    parse_mode="HTML"
)

## 编辑标记（按钮）

await bot.edit_message_reply_markup(
    chat_id=chat_id,
    message_id=msg.message_id,
    reply_markup=new_keyboard
)

## 删除消息

await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)

## 转发消息

await bot.forward_message(
    chat_id=dest_chat_id,
    from_chat_id=source_chat_id,
    message_id=msg.message_id
)
```

---

## 错误处理

```python
from telegram.error import TelegramError, BadRequest, TimedOut, NetworkError

async def safe_send(bot, chat_id, text, **kwargs):
    """带重试和错误处理的发送。"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await bot.send_message(chat_id, text, **kwargs)
        except TimedOut:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise
        except BadRequest as e:
            if "chat not found" in str(e).lower():
                print(f"聊天 {chat_id} 未找到")
                return None
            raise
        except NetworkError:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise
```

---

## 速率限制

- **私聊消息：** 约 30 条/秒
- **群组消息：** 每个群组约 20 条/分钟
- **全局广播：** 总计约 30 条/秒
- **批量通知：** 在发送之间使用 `asyncio.sleep(0.05)` 以避免洪水

如果收到 429 错误（Too Many Requests），请遵守返回的 `retry_after` 值。

---

## 文件参考

| 主题 | 文件 |
|------|------|
| Webhook 设置 | `references/webhook-setup.md` |
| 聊天管理 | `references/chat-management.md` |
| 高级功能 | `references/advanced-features.md` |
| API 完整参考 | `references/api-reference.md` |
| Node.js 模板 | `assets/boilerplate/nodejs/` |
| Python 模板 | `assets/boilerplate/python/` |
| Payload 示例 | `assets/examples/` |

## 最佳实践

- 提供关于项目和需求的清晰、具体的上下文
- 在将建议应用到生产代码之前进行审查
- 与其他互补技能结合使用以进行全面分析

## 常见陷阱

- 将此技能用于超出其领域专业知识的任务
- 在不了解具体上下文的情况下应用建议
- 没有提供足够的项目上下文以进行准确分析

## 相关技能

- `instagram` - 互补技能，用于增强分析
- `social-orchestrator` - 互补技能，用于增强分析
- `whatsapp-cloud-api` - 互补技能，用于增强分析

## 限制
- 仅当任务明确匹配上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
