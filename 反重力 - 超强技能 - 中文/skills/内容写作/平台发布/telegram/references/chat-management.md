# 聊天管理 - Telegram Bot

## 目录
1. [聊天类型](#tipos-de-chat)
2. [聊天信息](#informacoes)
3. [成员管理](#membros)
4. [审核](#moderacao)
5. [聊天设置](#configuracoes)
6. [邀请](#convites)
7. [频道](#canais)
8. [论坛话题](#forum)

---

## 聊天类型

| 类型 | `chat.type` | 特点 |
|------|-------------|------|
| 私聊 | `private` | 与用户 1:1 |
| 群组 | `group` | 最多 200 成员，基础功能 |
| 超级群组 | `supergroup` | 最多 20 万成员，历史记录持久化 |
| 频道 | `channel` | 广播模式，成员无限制 |

---

## 聊天信息

```python
# 获取完整信息
chat = await bot.get_chat(chat_id)
print(f"标题: {chat.title}")
print(f"类型: {chat.type}")
print(f"成员数: {await bot.get_chat_member_count(chat_id)}")
print(f"描述: {chat.description}")

# 获取特定成员
member = await bot.get_chat_member(chat_id, user_id)
print(f"状态: {member.status}")  # creator, administrator, member, restricted, left, kicked

# 列出管理员
admins = await bot.get_chat_administrators(chat_id)
for admin in admins:
    print(f"{admin.user.first_name}: {admin.status}")
```

---

## 成员管理

```python
# 封禁成员（从群组移除）
await bot.ban_chat_member(chat_id, user_id)

# 临时封禁（在 until_date 后恢复）
from datetime import datetime, timedelta
until = datetime.now() + timedelta(hours=24)
await bot.ban_chat_member(chat_id, user_id, until_date=until)

# 解封
await bot.unban_chat_member(chat_id, user_id, only_if_banned=True)

# 限制权限
from telegram import ChatPermissions
await bot.restrict_chat_member(
    chat_id, user_id,
    permissions=ChatPermissions(
        can_send_messages=True,
        can_send_photos=False,
        can_send_videos=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_invite_users=False
    ),
    until_date=until  # 可选：临时限制
)

# 提升为管理员
await bot.promote_chat_member(
    chat_id, user_id,
    can_manage_chat=True,
    can_delete_messages=True,
    can_restrict_members=True,
    can_invite_users=True,
    can_pin_messages=True,
    can_manage_video_chats=True
)

# 为管理员设置自定义头衔
await bot.set_chat_administrator_custom_title(chat_id, user_id, "版主")
```

---

## 审核

### 自动审核机器人

```python
from telegram import Update, ChatPermissions
from telegram.ext import MessageHandler, filters, ContextTypes

# 禁词列表
BANNED_WORDS = ["垃圾", "广告", "违规"]

async def moderate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    text_lower = msg.text.lower()

    # 检查禁词
    for word in BANNED_WORDS:
        if word in text_lower:
            await msg.delete()
            await context.bot.restrict_chat_member(
                msg.chat.id, msg.from_user.id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=datetime.now() + timedelta(minutes=5)
            )
            await context.bot.send_message(
                msg.chat.id,
                f"{msg.from_user.first_name} 的消息因包含违规内容已被删除。"
                f"已禁言 5 分钟。"
            )
            return

    # 防刷屏：10 秒内最多 5 条消息
    user_key = f"flood_{msg.from_user.id}"
    msgs = context.bot_data.get(user_key, [])
    now = datetime.now().timestamp()
    msgs = [t for t in msgs if now - t < 10]  # 最近 10 秒
    msgs.append(now)
    context.bot_data[user_key] = msgs

    if len(msgs) > 5:
        await msg.delete()
        await context.bot.send_message(
            msg.chat.id,
            f"{msg.from_user.first_name}，请勿连续发送过多消息。"
        )

app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, moderate))
```

### 自动欢迎

```python
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        await update.message.reply_text(
            f"欢迎，{member.first_name}！"
            f"参与前请先阅读 /regras 规则。"
        )

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
```

---

## 聊天设置

```python
# 修改标题
await bot.set_chat_title(chat_id, "群组新标题")

# 修改描述
await bot.set_chat_description(chat_id, "群组描述已更新")

# 修改头像
with open("grupo_foto.jpg", "rb") as photo:
    await bot.set_chat_photo(chat_id, photo)

# 置顶消息
await bot.pin_chat_message(chat_id, message_id, disable_notification=True)

# 取消置顶
await bot.unpin_chat_message(chat_id, message_id)

# 取消所有置顶
await bot.unpin_all_chat_messages(chat_id)

# 设置默认权限
await bot.set_chat_permissions(chat_id, ChatPermissions(
    can_send_messages=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_invite_users=True
))
```

---

## 邀请

```python
# 生成默认邀请链接
link = await bot.export_chat_invite_link(chat_id)

# 创建自定义链接
invite = await bot.create_chat_invite_link(
    chat_id,
    name="一月活动链接",
    expire_date=datetime(2026, 2, 28),
    member_limit=100,
    creates_join_request=False  # True = 需要审批
)
print(f"链接: {invite.invite_link}")

# 编辑链接
await bot.edit_chat_invite_link(
    chat_id,
    invite.invite_link,
    name="更新后的链接",
    member_limit=200
)

# 撤销链接
await bot.revoke_chat_invite_link(chat_id, invite.invite_link)

# 批准入群申请
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    # 自动批准（或实现自定义逻辑）
    await request.approve()
    await context.bot.send_message(
        request.from_user.id,
        f"欢迎加入 {request.chat.title}！"
    )

app.add_handler(ChatJoinRequestHandler(handle_join_request))
```

---

## 频道

频道中的机器人可以发布、编辑和删除消息：

```python
# 在频道发布（使用 @用户名 或 chat_id）
await bot.send_message("@meu_canal", "频道帖子！")

# 带按钮发布
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("阅读更多", url="https://example.com")]
])
await bot.send_message("@meu_canal", "新文章！", reply_markup=keyboard)

# 编辑频道帖子
await bot.edit_message_text(
    "更新后的文本",
    chat_id="@meu_canal",
    message_id=123
)

# 从频道转发到群组
await bot.forward_message(
    chat_id=group_id,
    from_chat_id="@meu_canal",
    message_id=123
)
```

---

## 论坛话题

启用了话题的超级群组（论坛类型）：

```python
# 创建话题
topic = await bot.create_forum_topic(
    chat_id, name="常见问题",
    icon_color=0x6FB9F0  # 蓝色
)

# 在特定话题发送消息
await bot.send_message(
    chat_id, "话题中的消息",
    message_thread_id=topic.message_thread_id
)

# 关闭话题
await bot.close_forum_topic(chat_id, topic.message_thread_id)

# 重新打开话题
await bot.reopen_forum_topic(chat_id, topic.message_thread_id)

# 编辑话题
await bot.edit_forum_topic(
    chat_id, topic.message_thread_id,
    name="技术问题"
)

# 删除话题
await bot.delete_forum_topic(chat_id, topic.message_thread_id)
```
