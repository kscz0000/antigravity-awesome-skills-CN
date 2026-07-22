---
name: molykit
description: |
  MolyKit AI 聊天工具包最佳实践，涵盖跨平台异步、BotClient trait、OpenAI SSE 流式响应、聊天 Widget 及 MCP 支持。当用户要求'使用 MolyKit 构建 AI 聊天界面'、'集成 OpenAI 流式响应'、'Makepad 聊天 Widget'、'跨平台异步 spawn PlatformSend'、'BotClient trait 实现'时使用。
risk: unknown
source: community
---

# MolyKit 技能

使用 Makepad 和 MolyKit 构建 AI 聊天界面的最佳实践——MolyKit 是一个跨平台 AI 聊天应用工具包。

**源代码库**：`/Users/zhangalex/Work/Projects/FW/robius/moly/moly-kit`

## 何时使用

涉及以下场景时使用此技能：
- 使用 Makepad 构建 AI 聊天界面
- 集成 OpenAI 或其他 LLM API
- 为原生和 WASM 实现跨平台异步
- 创建聊天 Widget（Messages、PromptInput、Avatar）
- 处理 SSE 流式响应
- 关键词：molykit, moly-kit, ai chat, bot client, openai makepad, chat widget, sse streaming

## 概述

MolyKit 提供：
- 跨平台异步工具（PlatformSend、spawn()、ThreadToken）
- 开箱即用的聊天 Widget（Chat、Messages、PromptInput、Avatar）
- 用于 AI 提供商集成的 BotClient trait
- 支持 SSE 流式响应的 OpenAI 兼容客户端
- 消息、机器人和工具调用的协议类型
- MCP（模型上下文协议）支持

## 跨平台异步模式

### PlatformSend - 仅原生平台需要 Send

```rust
/// 仅在原生平台要求 Send，WASM 上不需要
/// - 原生平台：由实现了 Send 的类型实现
/// - WASM：由所有类型实现
pub trait PlatformSend: PlatformSendInner {}

/// 用于跨平台使用的装箱 Future 类型
pub type BoxPlatformSendFuture<'a, T> = Pin<Box<dyn PlatformSendFuture<Output = T> + 'a>>;

/// 用于跨平台使用的装箱 Stream 类型
pub type BoxPlatformSendStream<'a, T> = Pin<Box<dyn PlatformSendStream<Item = T> + 'a>>;
```

### 平台无关的任务派生

```rust
/// 独立运行一个 future
/// - 原生平台使用 tokio（需要 Send）
/// - WASM 使用 wasm-bindgen-futures（不需要 Send）
pub fn spawn(fut: impl PlatformSendFuture<Output = ()> + 'static);

// 用法
spawn(async move {
    let result = fetch_data().await;
    Cx::post_action(DataReady(result));
    SignalToUI::set_ui_signal();
});
```

### 使用 AbortOnDropHandle 取消任务

```rust
/// 在 drop 时中止其 future 的句柄
pub struct AbortOnDropHandle(AbortHandle);

// 用法 - Widget drop 时任务被取消
#[rust]
task_handle: Option<AbortOnDropHandle>,

fn start_task(&mut self) {
    let (future, handle) = abort_on_drop(async move {
        // 异步工作...
    });
    self.task_handle = Some(handle);
    spawn(async move { let _ = future.await; });
}
```

### ThreadToken 用于 WASM 上的非 Send 类型

```rust
/// 将非 Send 值存储在线程本地，通过 token 访问
pub struct ThreadToken<T: 'static>;

impl<T> ThreadToken<T> {
    pub fn new(value: T) -> Self;
    pub fn peek<R>(&self, f: impl FnOnce(&T) -> R) -> R;
    pub fn peek_mut<R>(&self, f: impl FnOnce(&mut T) -> R) -> R;
}

// 用法 - 包装非 Send 类型以跨 Send 边界使用
let token = ThreadToken::new(non_send_value);
spawn(async move {
    token.peek(|value| {
        // 使用 value...
    });
});
```

## BotClient Trait

### 实现 AI 提供商集成

```rust
pub trait BotClient: Send {
    /// 发送消息并获取流式响应
    fn send(
        &mut self,
        bot_id: &BotId,
        messages: &[Message],
        tools: &[Tool],
    ) -> BoxPlatformSendStream<'static, ClientResult<MessageContent>>;

    /// 获取可用的机器人/模型
    fn bots(&self) -> BoxPlatformSendFuture<'static, ClientResult<Vec<Bot>>>;

    /// 用于传递的克隆方法
    fn clone_box(&self) -> Box<dyn BotClient>;
}

// 用法
let client = OpenAIClient::new("https://api.openai.com/v1".into());
client.set_key("sk-...")?;
let context = BotContext::from(client);
```

### BotContext - 可共享的包装器

```rust
/// 可共享的包装器，包含已加载的机器人供同步 UI 访问
pub struct BotContext(Arc<Mutex<InnerBotContext>>);

impl BotContext {
    pub fn load(&mut self) -> BoxPlatformSendFuture<ClientResult<()>>;
    pub fn bots(&self) -> Vec<Bot>;
    pub fn get_bot(&self, id: &BotId) -> Option<Bot>;
    pub fn client(&self) -> Box<dyn BotClient>;
}

// 用法
let mut context = BotContext::from(client);
spawn(async move {
    if let Err(errors) = context.load().await.into_result() {
        // 处理错误
    }
    Cx::post_action(BotsLoaded);
});
```

## 协议类型

### 消息结构

```rust
pub struct Message {
    pub from: EntityId,         // User, System, Bot(BotId), App
    pub metadata: MessageMetadata,
    pub content: MessageContent,
}

pub struct MessageContent {
    pub text: String,           // 主要内容（markdown）
    pub reasoning: String,      // AI 推理/思考
    pub citations: Vec<String>, // 来源 URL
    pub attachments: Vec<Attachment>,
    pub tool_calls: Vec<ToolCall>,
    pub tool_results: Vec<ToolResult>,
}

pub struct MessageMetadata {
    pub is_writing: bool,       // 仍在流式输出中
    pub created_at: DateTime<Utc>,
}
```

### 机器人标识

```rust
/// 全局唯一的机器人 ID：<len>;<id>@<provider>
pub struct BotId(Arc<str>);

impl BotId {
    pub fn new(id: &str, provider: &str) -> Self;
    pub fn id(&self) -> &str;       // 提供商本地 id
    pub fn provider(&self) -> &str; // 提供商域名
}

// 示例：BotId::new("gpt-4", "api.openai.com")
// -> "5;gpt-4@api.openai.com"
```

## Widget 模式

### Slot Widget - 运行时内容替换

```rust
live_design! {
    pub Slot = {{Slot}} {
        width: Fill, height: Fit,
        slot = <View> {}  // 默认内容
    }
}

// 用法 - 在运行时替换内容
let mut slot = widget.slot(id!(content));
if let Some(custom) = client.content_widget(cx, ...) {
    slot.replace(custom);
} else {
    slot.restore();  // 恢复默认
    slot.default().as_standard_message_content().set_content(cx, &content);
}
```

### Avatar Widget - 文本/图片切换

```rust
live_design! {
    pub Avatar = {{Avatar}} <View> {
        grapheme = <RoundedView> {
            visible: false,
            label = <Label> { text: "P" }
        }
        dependency = <RoundedView> {
            visible: false,
            image = <Image> {}
        }
    }
}

impl Widget for Avatar {
    fn draw_walk(&mut self, cx: &mut Cx2d, ...) -> DrawStep {
        if let Some(avatar) = &self.avatar {
            match avatar {
                Picture::Grapheme(g) => {
                    self.view(id!(grapheme)).set_visible(cx, true);
                    self.view(id!(dependency)).set_visible(cx, false);
                    self.label(id!(label)).set_text(cx, &g);
                }
                Picture::Dependency(d) => {
                    self.view(id!(dependency)).set_visible(cx, true);
                    self.view(id!(grapheme)).set_visible(cx, false);
                    self.image(id!(image)).load_image_dep_by_path(cx, d.as_str());
                }
            }
        }
        self.deref.draw_walk(cx, scope, walk)
    }
}
```

### PromptInput Widget

```rust
#[derive(Live, Widget)]
pub struct PromptInput {
    #[deref] deref: CommandTextInput,
    #[live] pub send_icon: LiveValue,
    #[live] pub stop_icon: LiveValue,
    #[rust] pub task: Task,           // Send 或 Stop
    #[rust] pub interactivity: Interactivity,
}

impl PromptInput {
    pub fn submitted(&self, actions: &Actions) -> bool;
    pub fn reset(&mut self, cx: &mut Cx);
    pub fn set_send(&mut self);
    pub fn set_stop(&mut self);
    pub fn enable(&mut self);
    pub fn disable(&mut self);
}
```

### Messages Widget - 对话视图

```rust
#[derive(Live, Widget)]
pub struct Messages {
    #[deref] deref: View,
    #[rust] pub messages: Vec<Message>,
    #[rust] pub bot_context: Option<BotContext>,
}

impl Messages {
    pub fn set_messages(&mut self, messages: Vec<Message>, scroll_to_bottom: bool);
    pub fn scroll_to_bottom(&mut self, cx: &mut Cx, triggered_by_stream: bool);
    pub fn is_at_bottom(&self) -> bool;
}
```

## UiRunner 模式——异步到 UI

```rust
impl Widget for PromptInput {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {
        self.deref.handle_event(cx, event, scope);
        self.ui_runner().handle(cx, event, scope, self);

        if self.button(id!(attach)).clicked(event.actions()) {
            let ui = self.ui_runner();
            Attachment::pick_multiple(move |result| match result {
                Ok(attachments) => {
                    ui.defer_with_redraw(move |me, cx, _| {
                        me.attachment_list_ref().write().attachments.extend(attachments);
                    });
                }
                Err(_) => {}
            });
        }
    }
}
```

## SSE 流式传输

```rust
/// 将 SSE 字节流解析为消息流
pub fn parse_sse<S, B, E>(s: S) -> impl Stream<Item = Result<String, E>>
where
    S: Stream<Item = Result<B, E>>,
    B: AsRef<[u8]>,
{
    // 按 "\n\n" 分割，提取 "data:" 内容
    // 过滤注释和 [DONE] 消息
}

// 在 BotClient::send 中的用法
fn send(&mut self, ...) -> BoxPlatformSendStream<...> {
    let stream = stream! {
        let response = client.post(url).send().await?;
        let events = parse_sse(response.bytes_stream());

        for await event in events {
            let completion: Completion = serde_json::from_str(&event)?;
            content.text.push_str(&completion.delta.content);
            yield ClientResult::new_ok(content.clone());
        }
    };
    Box::pin(stream)
}
```

## 最佳实践

1. **使用 PlatformSend 实现跨平台**：同一份代码在原生和 WASM 上都能工作
2. **使用 spawn() 而非 tokio::spawn**：平台无关的任务派生
3. **使用 AbortOnDropHandle**：Widget drop 时取消任务
4. **在 WASM 上使用 ThreadToken 处理非 Send 类型**：通过 token 访问线程本地存储
5. **使用 Slot 实现自定义内容**：允许 BotClient 提供自定义 Widget
6. **使用 read()/write() 模式**：通过 WidgetRef 安全地借用访问
7. **使用 UiRunner::defer_with_redraw**：从异步上下文更新 Widget
8. **处理 ClientResult 部分成功**：可能同时有值和错误

## 参考文件

- `llms.txt` - 完整的 MolyKit API 参考

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
