---
name: makepad-basics
description: |
  Makepad 入门与应用结构指南。触发词：
  makepad, makepad getting started, makepad tutorial, live_design!, app_main!,
  makepad project setup, makepad hello world, "how to create makepad app",
  makepad 入门, 创建 makepad 应用, makepad 教程, makepad 项目结构。
  当用户要求'Makepad入门'、'Makepad教程'、'创建Makepad应用'、
  'Makepad项目搭建'、'live_design!'、'app_main!'、'Makepad Hello World'时使用。
risk: unknown
source: "https://github.com/makepad/makepad"
---

# Makepad 基础技能

> **版本：** makepad-widgets (dev 分支) | **最后更新：** 2026-01-19
>
> 检查更新：https://crates.io/crates/makepad-widgets

你是 Rust `makepad-widgets` crate 的专家，帮助用户：
- **编写代码**：按照以下模式生成 Rust 代码
- **解答问题**：解释概念、排查问题、参考文档

## 适用场景
- 需要入门 Makepad 或了解基本应用结构与模板代码
- 涉及项目搭建、`live_design!`、`app_main!` 或首屏应用构建
- 在深入布局、组件或着色器等专题前，需要 Makepad 基础指导

## 文档

详细文档请参考本地文件：
- `./references/app-structure.md` - 完整应用模板与结构
- `./references/event-handling.md` - 事件处理模式

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上方列出的相关参考文件
2. 若文件读取失败或为空：
   - 告知用户："本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档"
   - 仍基于 SKILL.md 模式 + 内置知识作答
3. 若参考文件存在，将其内容纳入回答

## 核心模式

### 1. 基本应用结构

```rust
use makepad_widgets::*;

live_design! {
    use link::theme::*;
    use link::shaders::*;
    use link::widgets::*;

    App = {{App}} {
        ui: <Root> {
            main_window = <Window> {
                body = <View> {
                    width: Fill, height: Fill
                    flow: Down

                    <Label> { text: "Hello Makepad!" }
                }
            }
        }
    }
}

app_main!(App);

#[derive(Live, LiveHook)]
pub struct App {
    #[live] ui: WidgetRef,
}

impl LiveRegister for App {
    fn live_register(cx: &mut Cx) {
        crate::makepad_widgets::live_design(cx);
    }
}

impl AppMain for App {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event) {
        self.ui.handle_event(cx, event, &mut Scope::empty());
    }
}
```

### 2. Cargo.toml 配置

```toml
[package]
name = "my_app"
version = "0.1.0"
edition = "2024"

[dependencies]
makepad-widgets = { git = "https://github.com/makepad/makepad", branch = "dev" }
```

### 3. 处理按钮点击

```rust
impl AppMain for App {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event) {
        let actions = self.ui.handle_event(cx, event, &mut Scope::empty());

        if self.ui.button(id!(my_button)).clicked(&actions) {
            log!("Button clicked!");
        }
    }
}
```

### 4. 访问和修改组件

```rust
// Get widget references
let label = self.ui.label(id!(my_label));
label.set_text("Updated text");

let input = self.ui.text_input(id!(my_input));
let text = input.text();
```

## API 速查表

| 宏/类型 | 说明 | 示例 |
|---------|------|------|
| `live_design!` | 用 DSL 定义 UI | `live_design! { App = {{App}} { ... } }` |
| `app_main!` | 入口宏 | `app_main!(App);` |
| `#[derive(Live)]` | 派生 live 数据 | `#[derive(Live, LiveHook)]` |
| `WidgetRef` | UI 树引用 | `#[live] ui: WidgetRef` |
| `Cx` | 渲染上下文 | `fn handle_event(&mut self, cx: &mut Cx, ...)` |
| `id!()` | 组件 ID 宏 | `self.ui.button(id!(my_button))` |

## 平台配置

| 平台 | 要求 |
|------|------|
| macOS | 开箱即用 |
| Windows | 开箱即用 |
| Linux | `apt-get install clang libaudio-dev libpulse-dev libx11-dev libxcursor-dev` |
| Web | `cargo install wasm-pack` |

## 编写代码时

1. 始终包含必要导入：`use makepad_widgets::*;`
2. 所有 UI 定义使用 `live_design!` 宏
3. 实现 `LiveRegister` 和 `AppMain` trait
4. 组件引用使用 `id!()` 宏
5. 通过 `handle_event` 方法处理事件

## 解答问题时

1. 强调 live design — DSL 中的修改即时生效，无需重新编译
2. Makepad 是 GPU 优先 — 所有渲染基于着色器
3. 跨平台：同一份代码运行于 Android、iOS、Linux、macOS、Windows、Web
4. 推荐使用 UI Zoo 示例探索组件

## 限制
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代特定环境下的验证、测试或专家审查
- 若缺少必要输入、权限、安全边界或成功标准，应暂停并请求澄清
