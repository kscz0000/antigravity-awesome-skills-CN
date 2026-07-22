---
name: robius-app-architecture
description: |
  关键：用于 Robius 应用架构模式。触发词：
  Tokio, async, submit_async_request, 异步, 架构,
  SignalToUI, Cx::post_action, worker task,
  app structure, MatchEvent, handle_startup
risk: unknown
source: community
---

# Robius 应用架构技能

基于 Robrix 和 Moly 代码库的 Makepad 应用程序结构最佳实践——这些是使用 Makepad 和 Robius 框架构建的生产级应用程序。

**源代码库：**
- **Robrix**：Matrix 聊天客户端——具有后台订阅的复杂同步/异步处理
- **Moly**：AI 聊天应用——跨平台（原生 + WASM）支持流式 API

## 何时使用
在以下情况使用此技能：
- 构建具有异步后端集成的 Makepad 应用程序
- 设计 Makepad 中的同步/异步通信模式
- 构建 Robius 风格的应用程序
- 关键词：robrix, robius, makepad app structure, async makepad, tokio makepad

## 生产级模式

关于生产就绪的异步模式，请参阅 `_base/` 目录：

| 模式 | 描述 |
|------|------|
| 08-async-loading | 带加载状态的异步数据加载 |
| 09-streaming-results | 使用 SignalToUI 的增量结果处理 |
| 13-tokio-integration | 完整的 tokio 运行时集成 |

## 核心架构模式

```
┌─────────────────────────────────────────────────────────────┐
│                     UI 线程 (Makepad)                       │
│  ┌─────────┐     ┌──────────┐     ┌──────────────────────┐ │
│  │   App   │────▶│ WidgetRef │────▶│ Widget Tree (View)  │ │
│  │ State   │     │    ui     │     │ Scope::with_data()  │ │
│  └────┬────┘     └──────────┘     └──────────────────────┘ │
│       │                                                     │
│       │ submit_async_request()                              │
│       ▼                                                     │
│  ┌─────────────────┐          ┌─────────────────────────┐  │
│  │ REQUEST_SENDER  │─────────▶│  Crossbeam SegQueue     │  │
│  │ (MPSC Channel)  │          │  (无锁更新)             │  │
│  └─────────────────┘          └─────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────┘
                                    │
                    SignalToUI::set_ui_signal()
                                    │
┌───────────────────────────────────┴─────────────────────────┐
│                   Tokio 运行时 (异步)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           worker_task (请求处理器)                    │   │
│  │  - 从 UI 接收 Request                                 │   │
│  │  - 为每个请求生成异步任务                              │   │
│  │  - 通过 Cx::post_action() 发回操作                    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         每项订阅者任务                                │   │
│  │  - 监听外部数据流                                     │   │
│  │  - 通过 crossbeam 通道发送 Update                     │   │
│  │  - 调用 SignalToUI::set_ui_signal() 唤醒 UI          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 应用结构

### 顶层 App 定义

```rust
use makepad_widgets::*;

live_design! {
    use link::theme::*;
    use link::widgets::*;

    App = {{App}} {
        ui: <Root>{
            main_window = <Window> {
                window: {inner_size: vec2(1280, 800), title: "MyApp"},
                body = {
                    // 主内容在此处
                }
            }
        }
    }
}

app_main!(App);

#[derive(Live)]
pub struct App {
    #[live] ui: WidgetRef,
    #[rust] app_state: AppState,
}

impl LiveRegister for App {
    fn live_register(cx: &mut Cx) {
        // 顺序很重要：先注册基础组件
        makepad_widgets::live_design(cx);
        // 然后是共享/通用组件
        crate::shared::live_design(cx);
        // 最后是功能模块
        crate::home::live_design(cx);
    }
}

impl LiveHook for App {
    fn after_new_from_doc(&mut self, cx: &mut Cx) {
        // 组件树创建后的一次性初始化
    }
}
```

### AppMain 实现

```rust
impl AppMain for App {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event) {
        // 转发到 MatchEvent trait
        self.match_event(cx, event);

        // 通过 Scope 将 AppState 传递到组件树
        let scope = &mut Scope::with_data(&mut self.app_state);
        self.ui.handle_event(cx, event, scope);
    }
}
```

## Tokio 运行时集成

### 静态运行时初始化

```rust
use std::sync::Mutex;
use tokio::sync::mpsc::{UnboundedReceiver, UnboundedSender};

static TOKIO_RUNTIME: Mutex<Option<tokio::runtime::Runtime>> = Mutex::new(None);
static REQUEST_SENDER: Mutex<Option<UnboundedSender<AppRequest>>> = Mutex::new(None);

pub fn start_async_runtime() -> Result<tokio::runtime::Handle> {
    let (request_sender, request_receiver) = tokio::sync::mpsc::unbounded_channel();

    let rt_handle = TOKIO_RUNTIME.lock().unwrap()
        .get_or_insert_with(|| {
            tokio::runtime::Runtime::new()
                .expect("Failed to create Tokio runtime")
        })
        .handle()
        .clone();

    // 存储发送器供 UI 线程使用
    *REQUEST_SENDER.lock().unwrap() = Some(request_sender);

    // 生成主工作器任务
    rt_handle.spawn(worker_task(request_receiver));

    Ok(rt_handle)
}
```

### 请求提交模式

```rust
pub enum AppRequest {
    FetchData { id: String },
    SendMessage { content: String },
    // ... 其他请求类型
}

/// 从 UI 线程向异步运行时提交请求
pub fn submit_async_request(req: AppRequest) {
    if let Some(sender) = REQUEST_SENDER.lock().unwrap().as_ref() {
        sender.send(req)
            .expect("BUG: worker task receiver has died!");
    }
}
```

### 工作器任务模式

```rust
async fn worker_task(mut request_receiver: UnboundedReceiver<AppRequest>) -> Result<()> {
    while let Some(request) = request_receiver.recv().await {
        match request {
            AppRequest::FetchData { id } => {
                // 为每个请求生成新任务
                let _task = tokio::spawn(async move {
                    let result = fetch_data(&id).await;
                    // 将结果发回 UI 线程
                    Cx::post_action(DataFetchedAction { id, result });
                });
            }
            AppRequest::SendMessage { content } => {
                let _task = tokio::spawn(async move {
                    match send_message(&content).await {
                        Ok(()) => Cx::post_action(MessageSentAction::Success),
                        Err(e) => Cx::post_action(MessageSentAction::Failed(e)),
                    }
                });
            }
        }
    }
    Ok(())
}
```

## 无锁更新队列模式

用于后台任务的高频更新：

```rust
use crossbeam_queue::SegQueue;
use makepad_widgets::SignalToUI;

pub enum DataUpdate {
    NewItem { item: Item },
    ItemChanged { id: String, changes: Changes },
    Status { message: String },
}

static PENDING_UPDATES: SegQueue<DataUpdate> = SegQueue::new();

/// 从后台异步任务调用
pub fn enqueue_update(update: DataUpdate) {
    PENDING_UPDATES.push(update);
    SignalToUI::set_ui_signal();  // 唤醒 UI 线程
}

// 在组件的 handle_event 中：
impl Widget for MyWidget {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {
        // 在 Signal 事件时轮询更新
        if let Event::Signal = event {
            while let Some(update) = PENDING_UPDATES.pop() {
                match update {
                    DataUpdate::NewItem { item } => {
                        self.items.push(item);
                        self.redraw(cx);
                    }
                    // ... 处理其他更新
                }
            }
        }
    }
}
```

## 启动序列

```rust
impl MatchEvent for App {
    fn handle_startup(&mut self, cx: &mut Cx) {
        // 1. 初始化日志
        let _ = tracing_subscriber::fmt::try_init();

        // 2. 初始化应用数据目录
        let _app_data_dir = crate::app_data_dir();

        // 3. 加载持久化状态
        if let Err(e) = persistence::load_window_state(
            self.ui.window(ids!(main_window)), cx
        ) {
            error!("Failed to load window state: {}", e);
        }

        // 4. 根据加载的状态更新 UI
        self.update_ui_visibility(cx);

        // 5. 启动异步运行时
        let _rt_handle = crate::start_async_runtime().unwrap();
    }
}
```

## 关闭序列

```rust
impl AppMain for App {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event) {
        if let Event::Shutdown = event {
            // 保存窗口几何信息
            let window_ref = self.ui.window(ids!(main_window));
            if let Err(e) = persistence::save_window_state(window_ref, cx) {
                error!("Failed to save window state: {e}");
            }

            // 保存应用状态
            if let Some(user_id) = current_user_id() {
                if let Err(e) = persistence::save_app_state(
                    self.app_state.clone(), user_id
                ) {
                    error!("Failed to save app state: {e}");
                }
            }
        }
        // ... 其余事件处理
    }
}
```

## 最佳实践

1. **关注点分离**：将 UI 逻辑保留在主线程，异步操作在 Tokio 运行时中
2. **请求/响应模式**：使用类型化枚举表示请求和操作
3. **无锁更新**：使用 `crossbeam::SegQueue` 处理高频后台更新
4. **SignalToUI**：入队更新后始终调用 `SignalToUI::set_ui_signal()`
5. **Cx::post_action()**：用于需要操作处理的异步任务结果
6. **Scope::with_data()**：通过组件树传递共享状态
7. **模块注册顺序**：在 `live_register()` 中先注册基础组件，再注册依赖模块

## 参考文件

- `references/tokio-integration.md` - 详细的 Tokio 运行时模式 (Robrix)
- `references/channel-patterns.md` - 通道通信模式 (Robrix)
- `references/moly-async-patterns.md` - 跨平台异步模式 (Moly)
  - `PlatformSend` trait 用于原生/WASM 兼容性
  - `UiRunner` 用于异步延迟操作
  - `AbortOnDropHandle` 用于任务取消
  - `ThreadToken` 用于 WASM 上的非 Send 类型
  - `spawn()` 平台无关函数

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
