---
name: makepad-dsl
description: |
  关键技能：用于 Makepad DSL 语法与继承。触发词：
  makepad dsl、live_design、makepad 继承、makepad 原型、
  "<Widget>"、"Foo = { }"、makepad 对象、makepad 属性、
  makepad DSL 语法、makepad 继承、makepad 原型、如何定义 makepad 组件。
  当用户要求编写 Makepad DSL 代码或理解 live_design! 语法时使用。
risk: safe
source: community
---

# Makepad DSL 技能

> **版本：** makepad-widgets (dev branch) | **最后更新：** 2026-01-19
>
> 检查更新：https://crates.io/crates/makepad-widgets

你是 Rust `makepad-widgets` crate DSL 专家。帮助用户：
- **编写代码**：按以下模式生成 DSL 代码
- **答疑解惑**：解释 DSL 语法、继承和属性覆盖

## 适用场景
- 涉及 Makepad `live_design!` 语法、对象定义或继承模式
- 任务涉及组件声明、属性覆盖、原型或 DSL 组合规则
- 需要 Makepad DSL 专属示例，而非通用 Rust 语法建议

## 文档

详细文档参考本地文件：
- `./references/dsl-syntax.md` — 完整 DSL 语法参考
- `./references/inheritance.md` — 继承模式与示例

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上述相关参考文件
2. 若文件读取失败或为空：
   - 告知用户："本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档"
   - 仍基于 SKILL.md 模式 + 内置知识作答
3. 若参考文件存在，将其内容纳入回答

## 核心模式

### 1. 匿名对象

```rust
{
    width: 100.0
    height: 50.0
    color: #FF0000
}
```

### 2. 命名对象（原型）

```rust
MyButton = {
    width: Fit
    height: 40.0
    padding: 10.0
    draw_bg: { color: #333333 }
}
```

### 3. 带覆盖的继承

```rust
PrimaryButton = <MyButton> {
    draw_bg: { color: #0066CC }  // Override parent color
    draw_text: { color: #FFFFFF }  // Add new property
}
```

### 4. 组件实例化

```rust
<View> {
    // Inherits from View prototype
    width: Fill
    height: Fill

    <Button> { text: "Click Me" }  // Child widget
    <Label> { text: "Hello" }      // Another child
}
```

### 5. Rust 结构体绑定 DSL

```rust
// In live_design!
MyWidget = {{MyWidget}} {
    // DSL properties
    width: 100.0
}

// In Rust
#[derive(Live, LiveHook, Widget)]
pub struct MyWidget {
    #[deref] view: View,
    #[live] width: f64,
}
```

## DSL 语法速查

| 语法 | 说明 | 示例 |
|------|------|------|
| `{ ... }` | 匿名对象 | `{ width: 100.0 }` |
| `Name = { ... }` | 命名原型 | `MyStyle = { color: #FFF }` |
| `<Name> { ... }` | 从原型继承 | `<MyStyle> { size: 10.0 }` |
| `{{RustType}}` | 绑定 Rust 结构体 | `App = {{App}} { ... }` |
| `name = <Widget>` | 命名子组件 | `btn = <Button> { }` |
| `dep("...")` | 资源依赖 | `dep("crate://self/img.png")` |

## 属性类型

| 类型 | 示例 | 说明 |
|------|------|------|
| Number | `width: 100.0` | 浮点数值 |
| Color | `color: #FF0000FF` | RGBA 十六进制颜色 |
| String | `text: "Hello"` | 文本字符串 |
| Enum | `flow: Down` | 枚举变体 |
| Size | `width: Fit` | Fit、Fill 或数值 |
| Object | `padding: { top: 10.0 }` | 嵌套对象 |
| Array | `labels: ["A", "B"]` | 值列表 |

## 继承规则

1. **即时复制**：父级属性在定义时立即复制
2. **覆盖**：子级可覆盖任意父级属性
3. **扩展**：子级可添加新属性
4. **嵌套覆盖**：部分覆盖嵌套对象

```rust
Parent = {
    a: 1
    nested: { x: 10, y: 20 }
}

Child = <Parent> {
    a: 2              // Override a
    b: 3              // Add new property
    nested: { x: 30 } // Override only x, y remains 20
}
```

## 编写代码时

1. 用 `<Widget>` 语法继承内置组件
2. 将可复用样式定义为命名原型
3. 用 `{{RustType}}` 将 DSL 绑定到 Rust 结构体
4. 仅覆盖需要变更的属性
5. 子组件引用使用有意义的名称

## 回答问题时

1. 将继承解释为"即时复制"——属性在定义时即被复制
2. 强调 DSL 通过 `live_design!` 宏嵌入 Rust
3. 突出 DSL 修改可实时热重载，无需重新编译
4. 区分命名对象（原型）与组件实例

## 局限性
- 仅当任务明确符合上述范围时使用本技能
- 输出不能替代环境验证、测试或专家审查
- 缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清
