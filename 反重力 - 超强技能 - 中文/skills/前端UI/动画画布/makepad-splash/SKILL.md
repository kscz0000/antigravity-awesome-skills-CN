---
name: makepad-splash
description: |
  Makepad Splash 脚本语言技能。涉及 Splash 语言、Makepad 脚本、script!、cx.eval、
  Makepad 动态开发、Makepad AI、splash 语言、makepad 脚本时使用。
risk: unknown
source: community
---

# Makepad Splash 技能

> **版本：** makepad-widgets (dev 分支) | **最后更新：** 2026-01-19
>
> 检查更新：https://crates.io/crates/makepad-widgets

你是 Makepad Splash 脚本语言专家，通过以下方式帮助用户：
- **编写 Splash 脚本**：动态 UI 和工作流自动化
- **理解 Splash**：用途、语法和能力

## 适用场景

- 需要在 Makepad 中使用 Splash 进行动态脚本开发
- 任务涉及 `script!`、`cx.eval`、运行时生成 UI 或 Makepad 工作流自动化
- 需要 Splash 语法和用途指导，而非纯 Rust 静态模式

## 文档

详细文档请参考本地文件：
- `./references/splash-tutorial.md` - Splash 语言教程

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上方列出的相关参考文件
2. 如果文件读取失败或为空：
   - 告知用户："本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档"
   - 仍基于 SKILL.md 模式和内置知识回答
3. 如果参考文件存在，将其内容纳入回答

## Splash 是什么？

Splash 是 Makepad 的动态脚本语言，专为以下场景设计：
- AI 辅助工作流
- 动态 UI 生成
- 快速原型开发
- HTTP 请求和异步操作

## Script 宏

```rust
// Embed Splash code in Rust
script!{
    fn main() {
        let x = 10;
        console.log("Hello from Splash!");
    }
}
```

## 执行

```rust
// Evaluate Splash code at runtime
cx.eval(code_string);

// With context
cx.eval_with_context(code, context);
```

## 基础语法

### 变量

```splash
let x = 10;
let name = "Makepad";
let items = [1, 2, 3];
let config = { width: 100, height: 50 };
```

### 函数

```splash
fn add(a, b) {
    return a + b;
}

fn greet(name) {
    console.log("Hello, " + name);
}
```

### 控制流

```splash
// If-else
if x > 10 {
    console.log("big");
} else {
    console.log("small");
}

// Loops
for i in 0..10 {
    console.log(i);
}

while condition {
    // ...
}
```

## 内置对象

### console

```splash
console.log("Message");
console.warn("Warning");
console.error("Error");
```

### http

```splash
// GET request
let response = http.get("https://api.example.com/data");

// POST request
let response = http.post("https://api.example.com/data", {
    body: { key: "value" }
});
```

### timer

```splash
// Set timeout
timer.set(1000, fn() {
    console.log("1 second passed");
});

// Set interval
let id = timer.interval(500, fn() {
    console.log("tick");
});

// Clear timer
timer.clear(id);
```

## Widget 交互

```splash
// Access widgets
let button = ui.widget("my_button");
button.set_text("Click Me");
button.set_visible(true);

// Listen to events
button.on_click(fn() {
    console.log("Button clicked!");
});
```

## 异步操作

```splash
// Async function
async fn fetch_data() {
    let response = await http.get("https://api.example.com");
    return response.json();
}

// Call async
fetch_data().then(fn(data) {
    console.log(data);
});
```

## AI 工作流集成

Splash 专为 AI 辅助开发设计：

```splash
// Dynamic UI generation
fn create_form(fields) {
    let form = ui.create("View");
    for field in fields {
        let input = ui.create("TextInput");
        input.set_label(field.label);
        form.add_child(input);
    }
    return form;
}

// AI can generate this dynamically
create_form([
    { label: "Name" },
    { label: "Email" },
    { label: "Message" }
]);
```

## 典型用途

1. **快速原型**：无需重新编译即可快速测试 UI 布局
2. **AI 代理**：让 AI 动态生成和修改 UI
3. **运行时配置**：运行时配置应用行为
4. **脚本化工作流**：自动化重复任务
5. **插件系统**：用脚本扩展应用功能

## 回答问题时的要点

1. Splash 用于动态/运行时脚本，不适合核心应用逻辑
2. 性能关键代码用 Rust，灵活性需求用 Splash
3. Splash 语法类似 JavaScript/Rust 混合体
4. 脚本在沙箱环境中运行
5. HTTP 和 timer API 支持异步操作

## 限制

- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清
