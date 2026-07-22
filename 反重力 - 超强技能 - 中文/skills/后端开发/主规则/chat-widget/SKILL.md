---
name: chat-widget
description: 构建实时客服聊天系统，包含用户端悬浮小部件和管理员后台。触发词：实时聊天、客服聊天、在线客服、即时消息、应用内支持、live chat、customer support、real-time messaging、in-app support、聊天小部件、客服系统。
risk: unknown
source: community
---

# 实时客服聊天小部件

构建实时客服聊天系统，包含用户端悬浮小部件和管理员后台。

## 何时使用此技能

当用户想要：
- 在应用中添加实时聊天小部件
- 构建客服聊天功能
- 创建用户与管理员之间的实时消息系统
- 添加应用内支持渠道

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        前端                                      │
├─────────────────────────────┬───────────────────────────────────┤
│   用户小部件                 │   管理员后台                       │
│   - 悬浮聊天按钮             │   - 聊天列表（活跃/已归档）         │
│   - 消息面板                 │   - 对话视图                       │
│   - 未读徽章                 │   - 归档/恢复控制                   │
│   - 连接状态指示器           │   - 用户信息展示                   │
└─────────────┬───────────────┴───────────────┬───────────────────┘
              │                               │
              │     WebSocket + REST API      │
              ▼                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        后端                                      │
├─────────────────────────────────────────────────────────────────┤
│   频道                       │   控制器                          │
│   - ChatChannel（每个聊天）   │   - 用户：获取/创建聊天            │
│   - AdminChannel（全局）     │   - 管理员：列表、查看、归档        │
├─────────────────────────────┼───────────────────────────────────┤
│   模型                       │   任务                            │
│   - Chat（每用户一个）        │   - 邮件通知（延迟）               │
│   - Message（每聊天多条）     │                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 实现指南

### 步骤 1：数据模型

创建两张表：`support_chats` 和 `support_messages`。

**support_chats**
```
id              - 主键（推荐 UUID）
user_id         - 用户外键（UNIQUE - 每用户一个聊天）
last_message_at - 时间戳（用于按最近消息排序）
admin_viewed_at - 时间戳（追踪管理员最后查看时间）
archived_at     - 时间戳（null = 活跃，有值 = 已归档）
created_at
updated_at
```

**support_messages**
```
id              - 主键（推荐 UUID）
chat_id         - support_chats 外键
content         - 文本（必填）
sender_type     - 枚举：'user' | 'admin'
read_at         - 时间戳（null = 未读）
created_at
updated_at
```

**关键索引：**
- `support_chats.user_id`（唯一）
- `support_chats.last_message_at`（用于排序）
- `support_chats.archived_at`（用于筛选）
- `support_messages.chat_id`
- `support_messages.(chat_id, created_at)`（复合索引，用于排序）

**模型关系：**
```
User has_one SupportChat
SupportChat belongs_to User
SupportChat has_many SupportMessages
SupportMessage belongs_to SupportChat
```

**需要实现的模型方法：**

Chat 模型：
```pseudo
function touch_last_message()
  update last_message_at = now()

function unread_for_admin?()
  return exists message where sender_type = 'user'
    and created_at > admin_viewed_at

function mark_viewed_by_admin()
  update admin_viewed_at = now()

function archive()
  update archived_at = now()

function unarchive()
  update archived_at = null

function archived?()
  return archived_at != null
```

Message 模型：
```pseudo
after_create:
  chat.touch_last_message()
  if sender_type == 'user' and chat.archived?:
    chat.unarchive()  // 用户发送新消息时自动重新激活

after_create_commit:
  broadcast_to_chat_channel(message_data)
  if sender_type == 'user':
    broadcast_to_admin_notification_channel(message_data, chat_info)
  if sender_type == 'admin':
    schedule_email_notification(delay: 5.minutes)
```

### 步骤 2：API 端点

**用户端：**
```
GET  /support_chat       - 获取或创建用户的聊天及消息
PATCH /support_chat/mark_read - 标记管理员消息为已读
```

**管理员端：**
```
GET  /admin/chats              - 聊天列表（查询参数：archived=true/false）
GET  /admin/chats/:id          - 获取聊天及消息
POST /admin/chats/:id/archive  - 归档聊天
POST /admin/chats/:id/unarchive - 恢复聊天
```

**控制器逻辑：**

用户 GET /support_chat：
```pseudo
function show()
  chat = current_user.support_chat || create_chat(user: current_user)
  return {
    id: chat.id,
    messages: chat.messages.map(m => serialize_message(m))
  }
```

管理员 GET /admin/chats：
```pseudo
function index()
  chats = SupportChat
    .where(archived_at: params.archived ? not_null : null)
    .includes(:user, :messages)
    .order(last_message_at: desc)

  return chats.map(c => {
    id: c.id,
    user_email: c.user.email,
    last_message_preview: c.messages.last?.content.truncate(100),
    last_message_sender: c.messages.last?.sender_type,
    message_count: c.messages.count,
    unread: c.unread_for_admin?,
    archived: c.archived?
  })
```

### 步骤 3：WebSocket 频道

创建两个频道用于实时通信。

**ChatChannel**（每个聊天专用）：
```pseudo
class ChatChannel
  on_subscribe(chat_id):
    chat = find_chat(chat_id)
    if not authorized(chat):
      reject()
      return
    stream_from "support_chat:#{chat_id}"

  function authorized(chat):
    return chat.user_id == current_user.id OR current_user.is_admin

  action send_message(content):
    if content.blank: return
    sender_type = current_user.is_admin ? 'admin' : 'user'
    chat.messages.create(content: content, sender_type: sender_type)
```

**AdminNotificationChannel**（所有管理员的全局频道）：
```pseudo
class AdminNotificationChannel
  on_subscribe:
    if not current_user.is_admin:
      reject()
      return
    stream_from "admin_support_notifications"
```

**广播（从 Message 模型）：**
```pseudo
function broadcast_message():
  message_data = {
    id: id,
    content: content,
    sender_type: sender_type,
    read_at: read_at,
    created_at: created_at
  }

  // 广播给聊天订阅者（用户 + 任何正在查看的管理员）
  broadcast("support_chat:#{chat.id}", {
    type: "new_message",
    message: message_data
  })

  // 用户发送消息时通知所有管理员
  if sender_type == 'user':
    broadcast("admin_support_notifications", {
      type: "new_user_message",
      chat_id: chat.id,
      user_email: chat.user.email,
      message: message_data
    })
```

### 步骤 4：前端 - 用户小部件

创建一个悬浮聊天小部件，包含以下组件：

**组件结构：**
```
ChatWidget（根容器）
├── ChatButton（固定定位，右下角）
│   ├── Icon（关闭时显示消息气泡，打开时显示 X）
│   └── UnreadBadge（显示计数，上限显示 "9+"）
└── ChatPanel（打开时向上滑出）
    ├── Header（标题 + 连接状态点）
    ├── MessageList（可滚动）
    │   └── MessageBubble（按 sender_type 样式化）
    └── InputArea
        ├── Textarea（自动扩展）
        └── SendButton
```

**状态管理 hook：**
```pseudo
function useSupportChat():
  state:
    chat: Chat | null
    connected: boolean
    loading: boolean

  refs:
    consumer: WebSocketConsumer
    subscription: ChannelSubscription
    seenMessageIds: Set<string>  // 用于去重

  on_mount:
    fetch('/support_chat')
      .then(data => {
        chat = data
        seenMessageIds.addAll(data.messages.map(m => m.id))
      })

  when chat.id changes:
    subscription = consumer.subscribe('ChatChannel', { chat_id: chat.id })
    subscription.on_received(data => {
      if data.type == 'new_message':
        if seenMessageIds.has(data.message.id): return  // 去重
        seenMessageIds.add(data.message.id)
        chat.messages.push(data.message)
        if data.message.sender_type == 'admin':
          play_notification_sound()
    })
    subscription.on_connected(() => connected = true)
    subscription.on_disconnected(() => connected = false)

  on_unmount:
    subscription.unsubscribe()

  function sendMessage(content):
    subscription.perform('send_message', { content: content.trim() })

  function markAsRead():
    fetch('/support_chat/mark_read', { method: 'PATCH' })
    // 更新本地状态，标记管理员消息为已读

  return { chat, connected, loading, sendMessage, markAsRead }
```

**小部件行为：**
- 在右下角显示悬浮按钮（固定定位）
- 显示未读计数徽章（计算 sender_type='admin' 且 read_at=null 的消息数）
- 点击按钮切换面板打开/关闭
- 面板打开时自动调用 markAsRead()
- 新消息到达时自动滚动到底部
- 显示连接状态指示器（绿点 = 已连接）
- 键盘：Enter 发送，Shift+Enter 换行

**消息样式：**
- 用户消息：右对齐，主色背景
- 管理员消息：左对齐，次级/灰色背景
- 每条消息显示时间戳

### 步骤 5：前端 - 管理员后台

创建两个页面：聊天列表和聊天详情。

**聊天列表页面：**
```
Header: "客服聊天"
Tabs: [活跃] [已归档]

聊天卡片（按 last_message_at 降序排列）：
┌─────────────────────────────────────────┐
│ [未读指示器] user@example.com            │
│ 最后一条消息预览文本...                   │
│ 5 条消息 · 2 分钟前                      │
└─────────────────────────────────────────┘
```

功能：
- 标签筛选（活跃 vs 已归档）
- 未读指示器（高亮边框或徽章）
- 点击导航到详情
- 如果最后一条消息来自管理员，显示"你："前缀

**聊天详情页面：**
```
Header: user@example.com [归档/恢复按钮]
返回链接

消息（按日期分组）：
──── 1月29日 星期一 ────
[用户气泡]  消息内容
            10:30 AM

          [管理员气泡] 回复内容
                       10:35 AM

输入区域（与小部件相同）
```

功能：
- 用分隔线按日期分组消息
- 用户消息靠左，管理员消息靠右（与用户小部件相反）
- 显示发送者标签（管理员显示"你"，用户显示邮箱/姓名）
- 归档/恢复切换按钮
- 与用户小部件使用相同的 WebSocket 订阅实现实时更新
- 页面加载时调用 mark_viewed_by_admin()（服务端）

### 步骤 6：邮件通知

当管理员回复且用户未查看时，发送邮件给用户。

**任务/工作器：**
```pseudo
class SupportReplyNotificationJob
  perform(message):
    if message.sender_type != 'admin': return
    if message.read_at != null: return  // 已读，跳过

    send_email(
      to: message.chat.user.email,
      subject: "客服新回复",
      body: "您有一条来自客服团队的新消息..."
    )
```

**调度：**
- 管理员发送消息时，延迟 5 分钟调度任务
- 给用户时间在应用内查看消息，避免邮件打扰
- 任务执行前检查是否仍然未读

### 步骤 7：TypeScript 类型

```typescript
interface SupportMessage {
  id: string
  content: string
  sender_type: 'user' | 'admin'
  read_at: string | null  // ISO8601
  created_at: string      // ISO8601
}

interface SupportChat {
  id: string
  messages: SupportMessage[]
}

interface SupportChatListItem {
  id: string
  user_id: string
  user_email: string
  last_message_at: string | null
  last_message_preview: string | null
  last_message_sender: 'user' | 'admin' | null
  message_count: number
  unread: boolean
  archived: boolean
}

interface AdminSupportChat {
  id: string
  user_id: string
  user_email: string
  archived: boolean
  messages: SupportMessage[]
}

// WebSocket 消息类型
interface ChatChannelMessage {
  type: 'new_message'
  message: SupportMessage
}

interface AdminNotificationMessage {
  type: 'new_user_message'
  chat_id: string
  user_email: string
  message: SupportMessage
}
```

## 关键设计决策

1. **每用户一个聊天** - 简化用户体验，用户始终拥有相同的对话历史
2. **通过归档实现软删除** - 保留历史记录，允许恢复
3. **自动取消归档** - 当用户向已归档聊天发送消息时，自动重新激活
4. **延迟邮件通知** - 5 分钟延迟防止快速回复时的邮件轰炸
5. **消息去重** - 追踪已见 ID，防止发送 + 广播回显导致的重复
6. **独立的管理员频道** - 允许未来扩展功能，如全局未读计数、桌面通知

## 测试清单

实现后检查：
- [ ] 用户可以打开小部件并发送消息
- [ ] 管理员在后台实时看到消息
- [ ] 管理员可以回复，用户即时看到
- [ ] 未读徽章显示正确计数
- [ ] 打开小部件时徽章清除
- [ ] 连接指示器反映实际状态
- [ ] 归档/恢复正常工作
- [ ] 用户消息触发自动取消归档
- [ ] 消息未读 5 分钟后发送邮件
- [ ] 用户已读消息则不发送邮件
- [ ] 消息按时间顺序显示
- [ ] 无重复消息出现

## 常见陷阱

1. **忘记去重** - 当前用户发送的消息会通过广播回显
2. **已读状态的竞态条件** - 使用数据库事务
3. **WebSocket 认证** - 验证用户可以访问特定聊天
4. **连接状态过期** - 优雅处理重连
5. **缺少索引** - 在 (chat_id, created_at) 上添加复合索引
6. **邮件时机** - 使用后台任务，而非同步发送

---

## 框架特定指南

### Ruby on Rails

**模型：**
```ruby
# app/models/support_chat.rb
class SupportChat < ApplicationRecord
  belongs_to :user
  has_many :support_messages, dependent: :destroy

  scope :active, -> { where(archived_at: nil) }
  scope :archived, -> { where.not(archived_at: nil) }
  scope :recent_first, -> { order(last_message_at: :desc) }

  def touch_last_message
    update_column(:last_message_at, Time.current)
  end

  def unread_for_admin?
    support_messages.where(sender_type: :user)
      .where("created_at > ?", admin_viewed_at || Time.at(0)).exists?
  end

  def archive!
    update_column(:archived_at, Time.current)
  end

  def unarchive!
    update_column(:archived_at, nil)
  end
end

# app/models/support_message.rb
class SupportMessage < ApplicationRecord
  belongs_to :support_chat
  enum :sender_type, { user: 0, admin: 1 }
  validates :content, presence: true

  after_create :update_chat_timestamp
  after_create :auto_unarchive, if: :user?
  after_create_commit :broadcast_message
  after_create_commit :schedule_notification, if: :admin?

  private

  def broadcast_message
    ActionCable.server.broadcast("support_chat:#{support_chat_id}", {
      type: "new_message",
      message: { id:, content:, sender_type:, read_at:, created_at: }
    })
  end

  def schedule_notification
    SupportReplyNotificationJob.set(wait: 5.minutes).perform_later(self)
  end
end
```

**频道：**
```ruby
# app/channels/support_chat_channel.rb
class SupportChatChannel < ApplicationCable::Channel
  def subscribed
    @chat = SupportChat.find(params[:chat_id])
    reject unless @chat.user_id == current_user.id || current_user.admin?
    stream_from "support_chat:#{@chat.id}"
  end

  def send_message(data)
    @chat.support_messages.create!(
      content: data["content"],
      sender_type: current_user.admin? ? :admin : :user
    )
  end
end
```

**迁移：**
```ruby
create_table :support_chats, id: :uuid do |t|
  t.references :user, type: :uuid, null: false, foreign_key: true, index: { unique: true }
  t.datetime :last_message_at
  t.datetime :admin_viewed_at
  t.datetime :archived_at
  t.timestamps
end

create_table :support_messages, id: :uuid do |t|
  t.references :support_chat, type: :uuid, null: false, foreign_key: true
  t.text :content, null: false
  t.integer :sender_type, default: 0
  t.datetime :read_at
  t.timestamps
end
add_index :support_messages, [:support_chat_id, :created_at]
```

### React（任意后端）

**Hook：**
```typescript
// hooks/useSupportChat.ts
import { useEffect, useState, useRef, useCallback } from 'react'

export function useSupportChat(websocketUrl: string) {
  const [chat, setChat] = useState<Chat | null>(null)
  const [connected, setConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const seenIds = useRef(new Set<string>())

  useEffect(() => {
    fetch('/api/support_chat').then(r => r.json()).then(data => {
      setChat(data)
      data.messages.forEach((m: Message) => seenIds.current.add(m.id))
    })
  }, [])

  useEffect(() => {
    if (!chat?.id) return
    const ws = new WebSocket(`${websocketUrl}?chat_id=${chat.id}`)
    wsRef.current = ws

    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'new_message' && !seenIds.current.has(data.message.id)) {
        seenIds.current.add(data.message.id)
        setChat(prev => prev ? { ...prev, messages: [...prev.messages, data.message] } : prev)
      }
    }
    return () => ws.close()
  }, [chat?.id])

  const sendMessage = useCallback((content: string) => {
    wsRef.current?.send(JSON.stringify({ action: 'send_message', content }))
  }, [])

  return { chat, connected, sendMessage }
}
```

**小部件组件：**
```tsx
// components/ChatWidget.tsx
export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const { chat, connected, sendMessage } = useSupportChat('/ws/chat')
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const unreadCount = chat?.messages.filter(
    m => m.sender_type === 'admin' && !m.read_at
  ).length ?? 0

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chat?.messages])

  const handleSend = () => {
    if (!input.trim()) return
    sendMessage(input.trim())
    setInput('')
  }

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {isOpen ? (
        <div className="w-80 h-96 bg-white rounded-lg shadow-xl flex flex-col">
          <header className="p-3 border-b flex justify-between items-center">
            <span>客服聊天</span>
            <span className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500' : 'bg-gray-400'}`} />
          </header>
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {chat?.messages.map(m => (
              <div key={m.id} className={`p-2 rounded ${m.sender_type === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-100'}`}>
                {m.content}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="p-3 border-t flex gap-2">
            <input value={input} onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSend()}
              className="flex-1 border rounded px-2" placeholder="输入消息..." />
            <button onClick={handleSend} className="px-3 py-1 bg-blue-500 text-white rounded">发送</button>
          </div>
        </div>
      ) : (
        <button onClick={() => setIsOpen(true)} className="w-14 h-14 bg-blue-500 rounded-full text-white relative">
          💬
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 bg-red-500 text-xs w-5 h-5 rounded-full flex items-center justify-center">
              {unreadCount > 9 ? '9+' : unreadCount}
            </span>
          )}
        </button>
      )}
    </div>
  )
}
```

### Next.js（App Router）

**API 路由：**
```typescript
// app/api/support-chat/route.ts
import { getServerSession } from 'next-auth'
import { prisma } from '@/lib/prisma'

export async function GET() {
  const session = await getServerSession()
  if (!session?.user) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  let chat = await prisma.supportChat.findUnique({
    where: { userId: session.user.id },
    include: { messages: { orderBy: { createdAt: 'asc' } } }
  })

  if (!chat) {
    chat = await prisma.supportChat.create({
      data: { userId: session.user.id },
      include: { messages: true }
    })
  }

  return Response.json(chat)
}
```

**WebSocket 与 Pusher/Ably（无服务器友好）：**
```typescript
// 无服务器环境使用 Pusher、Ably 或类似服务
import Pusher from 'pusher'
const pusher = new Pusher({ appId, key, secret, cluster })

// 创建消息时：
await pusher.trigger(`support-chat-${chatId}`, 'new-message', messageData)

// 客户端使用 pusher-js：
const channel = pusher.subscribe(`support-chat-${chatId}`)
channel.bind('new-message', (data) => { /* 更新状态 */ })
```

### PHP/Laravel

**模型：**
```php
// app/Models/SupportChat.php
class SupportChat extends Model
{
    protected $casts = ['last_message_at' => 'datetime', 'archived_at' => 'datetime'];

    public function user() { return $this->belongsTo(User::class); }
    public function messages() { return $this->hasMany(SupportMessage::class); }

    public function scopeActive($query) { return $query->whereNull('archived_at'); }
    public function scopeArchived($query) { return $query->whereNotNull('archived_at'); }

    public function isUnreadForAdmin(): bool {
        return $this->messages()
            ->where('sender_type', 'user')
            ->where('created_at', '>', $this->admin_viewed_at ?? '1970-01-01')
            ->exists();
    }
}

// app/Models/SupportMessage.php
class SupportMessage extends Model
{
    protected static function booted() {
        static::created(function ($message) {
            $message->supportChat->update(['last_message_at' => now()]);
            broadcast(new NewSupportMessage($message))->toOthers();

            if ($message->sender_type === 'admin') {
                SendSupportReplyNotification::dispatch($message)->delay(now()->addMinutes(5));
            }
        });
    }
}
```

**广播事件：**
```php
// app/Events/NewSupportMessage.php
class NewSupportMessage implements ShouldBroadcast
{
    public function __construct(public SupportMessage $message) {}

    public function broadcastOn() {
        return new PrivateChannel('support-chat.' . $this->message->support_chat_id);
    }

    public function broadcastAs() { return 'new-message'; }
}
```

### Vue.js

**组合式函数：**
```typescript
// composables/useSupportChat.ts
import { ref, onMounted, onUnmounted } from 'vue'

export function useSupportChat() {
  const chat = ref<Chat | null>(null)
  const connected = ref(false)
  let ws: WebSocket | null = null
  const seenIds = new Set<string>()

  onMounted(async () => {
    const res = await fetch('/api/support-chat')
    chat.value = await res.json()
    chat.value?.messages.forEach(m => seenIds.add(m.id))

    ws = new WebSocket(`/ws/chat?id=${chat.value?.id}`)
    ws.onopen = () => connected.value = true
    ws.onclose = () => connected.value = false
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data)
      if (data.type === 'new_message' && !seenIds.has(data.message.id)) {
        seenIds.add(data.message.id)
        chat.value?.messages.push(data.message)
      }
    }
  })

  onUnmounted(() => ws?.close())

  const sendMessage = (content: string) => {
    ws?.send(JSON.stringify({ action: 'send_message', content }))
  }

  return { chat, connected, sendMessage }
}
```

---

## 数据库建议

### PostgreSQL（推荐）
- 使用 UUID 主键以增强安全性（不可猜测的 ID）
- 所有日期时间列使用 `timestamptz`
- 可选：在 content 上添加 GIN 索引支持全文搜索

### MySQL
- UUID 使用 `CHAR(36)` 或 `BINARY(16)`
- 使用 `DATETIME(6)` 获取微秒精度
- 考虑使用 `utf8mb4` 字符集支持 emoji

### SQLite（开发/小规模）
- 适合原型开发
- UUID 存储为 TEXT
- 无原生日期时间类型，存储为 ISO8601 字符串

### MongoDB（文档存储）
- 如果消息数量有限，可将消息嵌入聊天文档
- 或使用单独的集合，通过 chat_id 引用
- 可选：在已归档聊天上使用 TTL 索引自动清理

---

## 邮件处理建议

### 事务性邮件服务
- **Postmark** - 最佳送达率，API 简单
- **SendGrid** - 免费额度好，功能强大
- **AWS SES** - 大规模使用最便宜
- **Resend** - 现代开发体验，React 邮件模板

### 实现模式
```pseudo
// 始终使用后台任务发送邮件
Job: SendSupportReplyNotification
  delay: 管理员消息发送后 5 分钟

  perform(message_id):
    message = find_message(message_id)

    // 守卫条件 - 以下情况不发送：
    if message.sender_type != 'admin': return
    if message.read_at != null: return        // 已读
    if message.chat.archived?: return         // 聊天已归档

    send_email(
      to: message.chat.user.email,
      template: 'support_reply',
      data: { message_preview: message.content.truncate(200) }
    )
```

### 邮件模板提示
- 包含消息预览（截断）
- 添加直接打开聊天的链接（如果是 Web 应用）
- 保持主题简单："来自 [应用名] 客服的新回复"
- 包含退订链接以符合合规要求

---

## 实时技术选项

| 技术 | 最佳场景 | 无服务器支持？ |
|------|----------|----------------|
| ActionCable (Rails) | Rails 应用 | 否 |
| Socket.IO | Node.js 应用 | 否 |
| Pusher | 任意技术栈 | 是 |
| Ably | 任意技术栈 | 是 |
| Supabase Realtime | Supabase 用户 | 是 |
| Firebase RTDB | Firebase 用户 | 是 |
| Server-Sent Events | 简单单向通信 | 是 |

### 降级策略
如果 WebSocket 不可用，实现轮询：
```pseudo
// 断开连接时每 5 秒轮询一次
if (!websocket.connected) {
  setInterval(() => {
    fetch('/api/support-chat/messages?since=' + lastMessageTime)
      .then(newMessages => appendMessages(newMessages))
  }, 5000)
}
```

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
