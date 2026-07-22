---
name: makepad-event-action
description: |
  关键：用于 Makepad 事件与 Action 处理。触发词：makepad event、makepad action、Event 枚举、ActionTrait、handle_event、MouseDown、KeyDown、TouchUpdate、Hit、FingerDown、post_action、makepad 事件、makepad action、事件处理。当用户要求处理 Makepad 事件或 Action 时使用。
risk: safe
source: community
---

# Makepad Event/Action 技能

> **版本：** makepad-widgets (dev 分支) | **最后更新：** 2026-01-19
>
> 检查更新：https://crates.io/crates/makepad-widgets

你是 Makepad 事件与 Action 处理专家，帮助用户：
- **处理事件**：鼠标、键盘、触摸、生命周期事件
- **创建 Action**：子组件向父组件通信
- **事件流**：理解事件传播机制

## 适用场景
- 需要在 Makepad 中处理输入、生命周期或 UI 交互事件
- 任务涉及 `handle_event`、`Event` 变体、`Hit` 处理或组件 Action 传播
- 需要设计或调试组件与父组件之间的事件/Action 流

## 文档

详细文档请参考本地文件：
- `./references/event-system.md` - Event 枚举与处理
- `./references/action-system.md` - Action trait 与模式

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上方列出的相关参考文件
2. 如果文件读取失败或为空：
   - 告知用户："本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档"
   - 仍基于 SKILL.md 模式 + 内置知识回答
3. 如果参考文件存在，将其内容纳入回答

## Event 枚举（关键变体）

```rust
pub enum Event {
    // Lifecycle
    Startup,
    Shutdown,
    Foreground,
    Background,
    Resume,
    Pause,

    // Drawing
    Draw(DrawEvent),
    LiveEdit,

    // Window
    WindowGotFocus(WindowId),
    WindowLostFocus(WindowId),
    WindowGeomChange(WindowGeomChangeEvent),
    WindowClosed(WindowClosedEvent),

    // Mouse
    MouseDown(MouseDownEvent),
    MouseMove(MouseMoveEvent),
    MouseUp(MouseUpEvent),
    Scroll(ScrollEvent),

    // Touch
    TouchUpdate(TouchUpdateEvent),

    // Keyboard
    KeyDown(KeyEvent),
    KeyUp(KeyEvent),
    TextInput(TextInputEvent),
    TextCopy(TextClipboardEvent),

    // Timer
    Timer(TimerEvent),
    NextFrame(NextFrameEvent),

    // Network
    HttpResponse(HttpResponse),

    // Widget Actions
    Actions(ActionsBuf),
}
```

## 在组件中处理事件

```rust
impl Widget for MyWidget {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {
        // Check if event hits this widget's area
        match event.hits(cx, self.area()) {
            Hit::FingerDown(fe) => {
                // Mouse/touch down on this widget
                cx.action(MyWidgetAction::Pressed);
            }
            Hit::FingerUp(fe) => {
                if fe.is_over {
                    // Released while still over widget = click
                    cx.action(MyWidgetAction::Clicked);
                }
            }
            Hit::FingerHoverIn(_) => {
                self.animator_play(cx, id!(hover.on));
            }
            Hit::FingerHoverOut(_) => {
                self.animator_play(cx, id!(hover.off));
            }
            Hit::KeyDown(ke) => {
                if ke.key_code == KeyCode::Return {
                    cx.action(MyWidgetAction::Submitted);
                }
            }
            _ => {}
        }
    }
}
```

## Hit 枚举

```rust
pub enum Hit {
    // Finger/Mouse
    FingerDown(FingerDownEvent),
    FingerUp(FingerUpEvent),
    FingerMove(FingerMoveEvent),
    FingerHoverIn(FingerHoverEvent),
    FingerHoverOver(FingerHoverEvent),
    FingerHoverOut(FingerHoverEvent),
    FingerLongPress(FingerLongPressEvent),

    // Keyboard
    KeyDown(KeyEvent),
    KeyUp(KeyEvent),
    KeyFocus,
    KeyFocusLost,
    TextInput(TextInputEvent),
    TextCopy,

    // Nothing
    Nothing,
}
```

## Action 系统

### 定义 Action

```rust
#[derive(Clone, Debug, DefaultNone)]
pub enum ButtonAction {
    None,
    Clicked,
    Pressed,
    Released,
}

// DefaultNone derives Default returning None variant
```

### 发射 Action

```rust
// From main thread (in handle_event)
cx.action(ButtonAction::Clicked);

// From any thread (thread-safe)
Cx::post_action(MyAction::DataLoaded(data));
```

### 处理 Action

```rust
fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {
    // Handle child widget actions
    let actions = cx.capture_actions(|cx| {
        self.button.handle_event(cx, event, scope);
    });

    // Check for specific action
    if self.button(id!(my_button)).clicked(&actions) {
        // Button was clicked
    }

    // Or iterate actions
    for action in actions.iter() {
        if let Some(ButtonAction::Clicked) = action.downcast_ref() {
            // Handle click
        }
    }
}
```

## 组件 Action 辅助方法

```rust
// Common widget action checks
impl ButtonRef {
    fn clicked(&self, actions: &ActionsBuf) -> bool;
    fn pressed(&self, actions: &ActionsBuf) -> bool;
    fn released(&self, actions: &ActionsBuf) -> bool;
}

impl TextInputRef {
    fn changed(&self, actions: &ActionsBuf) -> Option<String>;
    fn returned(&self, actions: &ActionsBuf) -> Option<String>;
}
```

## 事件流

1. **事件到达** — 来自平台层
2. **根组件** — 最先接收事件
3. **向下传播** — 通过 `handle_event` 传递给子组件
4. **组件发射 Action** — 通过 `cx.action()`
5. **父组件捕获 Action** — 通过 `cx.capture_actions()`
6. **应用层处理** — 剩余 Action

## 定时器与 NextFrame

```rust
// Start a timer
let timer = cx.start_timer(1.0); // 1 second

// In handle_event
if let Event::Timer(te) = event {
    if te.timer_id == self.timer {
        // Timer fired
    }
}

// Request next frame callback
let next_frame = cx.new_next_frame();

// In handle_event
if let Event::NextFrame(ne) = event {
    if ne.frame_id == self.next_frame {
        // Next frame arrived
    }
}
```

## 回答问题时

1. 用 `event.hits(cx, area)` 检查事件是否指向某组件
2. Action 向上流动（子→父），事件向下传播（父→子）
3. 用 `cx.capture_actions()` 拦截子组件 Action
4. `Cx::post_action()` 线程安全，适用于异步操作
5. `DefaultNone` 派生宏自动为枚举实现 Default

## 局限性
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清
