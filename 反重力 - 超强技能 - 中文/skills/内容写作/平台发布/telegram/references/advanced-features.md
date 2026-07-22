# 高级功能 - Telegram Bot

## 目录
1. [内联模式](#inline-mode)
2. [支付（Telegram Stars）](#pagamentos)
3. [Mini Apps（WebApps）](#mini-apps)
4. [会话处理器（FSM）](#conversation-handlers)
5. [贴纸](#stickers)
6. [游戏](#games)
7. [Passport](#passport)
8. [商业机器人](#business-bots)
9. [消息草稿（流式传输）](#streaming)

---

## 内联模式

允许用户在任何聊天中通过输入 `@你的机器人 查询` 来使用机器人。

**启用方法：** 与 @BotFather 对话并发送 `/setinline`。

```python
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

async def inline_query(update: Update, context):
    query = update.inline_query.query
    if not query:
        return

    results = [
        InlineQueryResultArticle(
            id="1",
            title=f"搜索结果: {query}",
            input_message_content=InputTextMessageContent(
                message_text=f"你搜索的是: {query}"
            ),
            description="点击发送"
        ),
        InlineQueryResultArticle(
            id="2",
            title="大写转换",
            input_message_content=InputTextMessageContent(
                message_text=query.upper()
            )
        )
    ]

    await update.inline_query.answer(results, cache_time=10)

app.add_handler(InlineQueryHandler(inline_query))
```

### 内联结果类型

- `InlineQueryResultArticle` - 通用文本
- `InlineQueryResultPhoto` - 带预览的照片
- `InlineQueryResultGif` - GIF
- `InlineQueryResultVideo` - 视频
- `InlineQueryResultAudio` - 音频
- `InlineQueryResultDocument` - 文档
- `InlineQueryResultLocation` - 位置
- `InlineQueryResultVenue` - 地点/场所
- `InlineQueryResultContact` - 联系人
- `InlineQueryResultCachedPhoto` - 已在 Telegram 服务器上的照片

---

## 支付（Telegram Stars）

Telegram 允许通过 Stars（内部货币）进行数字商品支付。

```python
from telegram import LabeledPrice

# 发送发票
await bot.send_invoice(
    chat_id=chat_id,
    title="高级订阅",
    description="30天高级访问权限",
    payload="premium_30days",
    currency="XTR",  # XTR = Telegram Stars
    prices=[LabeledPrice("高级订阅", 100)],  # 100 Stars
)

# 预结账处理器
async def precheckout(update: Update, context):
    query = update.pre_checkout_query
    if query.invoice_payload == "premium_30days":
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="无效的载荷")

# 支付完成处理器
async def successful_payment(update: Update, context):
    payment = update.message.successful_payment
    await update.message.reply_text(
        f"收到支付！{payment.total_amount} Stars。"
        f"您的高级访问权限已激活。"
    )

app.add_handler(PreCheckoutQueryHandler(precheckout))
app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
```

### 外部支付提供商

对于实物商品，使用 Stripe、YooMoney 等提供商：

```python
await bot.send_invoice(
    chat_id=chat_id,
    title="Telegram Bot T恤",
    description="M码T恤，纯棉",
    payload="tshirt_m",
    provider_token="SEU_PROVIDER_TOKEN",  # 来自 BotFather
    currency="BRL",
    prices=[
        LabeledPrice("T恤", 5990),  # R$ 59.90（以分为单位）
        LabeledPrice("运费", 1500)   # R$ 15.00
    ],
    need_shipping_address=True,
    need_name=True,
    need_phone_number=True
)
```

---

## Mini Apps（WebApps）

Mini Apps 是在 Telegram 内部运行的 Web 应用。

```python
from telegram import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

# 打开 Mini App 的按钮
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(
        "打开应用",
        web_app=WebAppInfo(url="https://seu-app.com")
    )]
])
await bot.send_message(chat_id, "点击打开:", reply_markup=keyboard)

# 通过回复键盘
from telegram import ReplyKeyboardMarkup, KeyboardButton
keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("打开应用", web_app=WebAppInfo(url="https://seu-app.com"))]
])
```

### 接收 Mini App 数据

```python
async def web_app_data(update: Update, context):
    data = update.effective_message.web_app_data.data
    # data 是 Mini App 发送的 JSON 字符串
    import json
    parsed = json.loads(data)
    await update.message.reply_text(f"从应用收到: {parsed}")

app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
```

---

## 会话处理器（FSM）

用于多步骤对话（表单、向导）：

```python
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

# 状态
NAME, AGE, CONFIRM = range(3)

async def start_form(update: Update, context):
    await update.message.reply_text("你叫什么名字？")
    return NAME

async def get_name(update: Update, context):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("你多大了？")
    return AGE

async def get_age(update: Update, context):
    context.user_data['age'] = update.message.text
    name = context.user_data['name']
    age = context.user_data['age']
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("确认", callback_data="confirm"),
         InlineKeyboardButton("取消", callback_data="cancel")]
    ])
    await update.message.reply_text(
        f"姓名: {name}\n年龄: {age}\n\n确认吗？",
        reply_markup=keyboard
    )
    return CONFIRM

async def confirm(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm":
        await query.edit_message_text("注册成功！")
    else:
        await query.edit_message_text("注册已取消。")
    return ConversationHandler.END

async def cancel(update: Update, context):
    await update.message.reply_text("操作已取消。")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('cadastro', start_form)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        CONFIRM: [CallbackQueryHandler(confirm)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    conversation_timeout=300  # 5分钟超时
)
app.add_handler(conv_handler)
```

---

## 贴纸

```python
# 通过 file_id 发送贴纸
await bot.send_sticker(chat_id, sticker="CAACAgIAAxkBAAI...")

# 获取贴纸集
sticker_set = await bot.get_sticker_set("set_name")
for sticker in sticker_set.stickers:
    print(f"表情: {sticker.emoji}, ID: {sticker.file_id}")

# 创建贴纸集（需要 512x512 PNG/WEBP 图片）
await bot.create_new_sticker_set(
    user_id=user_id,
    name="meupack_by_meubot",
    title="我的贴纸包",
    stickers=[InputSticker(
        sticker=open("sticker.webp", "rb"),
        emoji_list=["😀"],
        format="static"
    )]
)

# 向贴纸集添加贴纸
await bot.add_sticker_to_set(
    user_id=user_id,
    name="meupack_by_meubot",
    sticker=InputSticker(
        sticker=open("sticker2.webp", "rb"),
        emoji_list=["😎"],
        format="static"
    )
)
```

---

## 游戏

```python
# 发送游戏（需在 BotFather 用 /newgame 注册）
await bot.send_game(chat_id, game_short_name="meu_jogo")

# 游戏回调处理器
async def game_callback(update: Update, context):
    query = update.callback_query
    await query.answer(url="https://seu-jogo.com/?user_id=" + str(query.from_user.id))

# 保存分数
await bot.set_game_score(
    user_id=user_id,
    score=150,
    chat_id=chat_id,
    message_id=game_message_id
)

# 获取高分榜
scores = await bot.get_game_high_scores(
    user_id=user_id,
    chat_id=chat_id,
    message_id=game_message_id
)
```

---

## 商业机器人

用于 Telegram 商业账户的机器人：

```python
# 接收商业连接
async def business_connection(update: Update, context):
    conn = update.business_connection
    if conn.is_enabled:
        print(f"机器人已连接到 {conn.user.first_name} 的商业账户")
    else:
        print(f"机器人已从 {conn.user.first_name} 的商业账户断开")

# 接收商业消息
async def business_message(update: Update, context):
    msg = update.business_message
    # 以商业账户名义回复
    await context.bot.send_message(
        chat_id=msg.chat.id,
        text="感谢您的消息！我们会尽快回复。",
        business_connection_id=msg.business_connection_id
    )

app.add_handler(BusinessConnectionHandler(business_connection))
app.add_handler(BusinessMessagesHandler(business_message))
```

---

## 消息草稿（流式传输）

对于长回复（如 AI 回复），使用草稿提供实时反馈：

```python
import requests

TOKEN = "SEU_TOKEN"
BASE = f"https://api.telegram.org/bot{TOKEN}"

def stream_response(chat_id, full_text):
    """通过发送部分草稿来模拟流式传输。"""
    words = full_text.split()
    partial = ""

    # 发送初始草稿
    for i, word in enumerate(words):
        partial += word + " "
        if i % 5 == 0:  # 每 5 个词更新一次
            requests.post(f"{BASE}/sendMessageDraft", json={
                "chat_id": chat_id,
                "text": partial.strip() + "..."
            })

    # 发送最终消息
    requests.post(f"{BASE}/sendMessage", json={
        "chat_id": chat_id,
        "text": full_text
    })
```

**注意：** `sendMessageDraft` 是一个较新的方法。请检查你使用的 API 版本是否支持。
