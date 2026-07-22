---
name: makepad-layout
description: |
  关键：Makepad 布局系统专用技能。触发词：
  makepad layout、makepad width、makepad height、makepad flex、
  makepad padding、makepad margin、makepad flow、makepad align、
  Fit、Fill、Size、Walk、"how to center in makepad"、
  makepad 布局、makepad 宽度、makepad 对齐、makepad 居中。
  当用户要求 Makepad 布局、尺寸、对齐或排列控件时使用。
risk: safe
source: community
---

# Makepad 布局技能

> **版本：** makepad-widgets（dev 分支）| **最后更新：** 2026-01-19
>
> 检查更新：https://crates.io/crates/makepad-widgets

你是 Makepad 布局系统专家。通过以下方式帮助用户：
- **编写代码**：按照下方模式生成布局代码
- **解答问题**：解释布局概念、尺寸计算、排列方向

## 适用场景
- 需要在 Makepad UI 中设置控件尺寸、对齐或定位
- 任务涉及 `Walk`、`Align`、`Fit`、`Fill`、padding、spacing 或容器 flow 配置
- 需要 Makepad 特有的居中、响应式或组合布局方案

## 文档

详细文档请参考本地文件：
- `./references/layout-system.md` — 完整布局参考
- `./references/core-types.md` — Walk、Align、Margin、Padding 类型

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上方列出的相关参考文件
2. 如果文件读取失败或为空：
   - 告知用户："本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档"
   - 仍基于 SKILL.md 模式和内置知识回答
3. 如果参考文件存在，将其内容纳入回答

## 核心模式

### 1. 基础布局容器

```rust
<View> {
    width: Fill
    height: Fill
    flow: Down
    padding: 16.0
    spacing: 8.0

    <Label> { text: "Item 1" }
    <Label> { text: "Item 2" }
}
```

### 2. 居中内容

```rust
<View> {
    width: Fill
    height: Fill
    align: { x: 0.5, y: 0.5 }

    <Label> { text: "Centered" }
}
```

### 3. 水平行布局

```rust
<View> {
    width: Fill
    height: Fit
    flow: Right
    spacing: 10.0
    align: { y: 0.5 }  // Vertically center items

    <Button> { text: "Left" }
    <View> { width: Fill }  // Spacer
    <Button> { text: "Right" }
}
```

### 4. 固定 + 弹性布局

```rust
<View> {
    width: Fill
    height: Fill
    flow: Down

    // Fixed header
    <View> {
        width: Fill
        height: 60.0
    }

    // Flexible content
    <View> {
        width: Fill
        height: Fill  // Takes remaining space
    }
}
```

## 布局属性参考

| 属性 | 类型 | 说明 |
|------|------|------|
| `width` | Size | 元素宽度 |
| `height` | Size | 元素高度 |
| `padding` | Padding | 内边距 |
| `margin` | Margin | 外边距 |
| `flow` | Flow | 子元素排列方向 |
| `spacing` | f64 | 子元素间距 |
| `align` | Align | 子元素对齐 |
| `clip_x` | bool | 水平溢出裁剪 |
| `clip_y` | bool | 垂直溢出裁剪 |

## 尺寸值

| 值 | 说明 |
|----|------|
| `Fit` | 适应内容尺寸 |
| `Fill` | 填充可用空间 |
| `100.0` | 固定像素值 |
| `Fixed(100.0)` | 显式固定尺寸 |

## 排列方向

| 值 | 说明 |
|----|------|
| `Down` | 从上到下（纵向） |
| `Right` | 从左到右（横向） |
| `Overlay` | 层叠排列 |

## 对齐值

| 值 | 位置 |
|----|------|
| `{ x: 0.0, y: 0.0 }` | 左上 |
| `{ x: 0.5, y: 0.0 }` | 上中 |
| `{ x: 1.0, y: 0.0 }` | 右上 |
| `{ x: 0.0, y: 0.5 }` | 中左 |
| `{ x: 0.5, y: 0.5 }` | 居中 |
| `{ x: 1.0, y: 0.5 }` | 中右 |
| `{ x: 0.0, y: 1.0 }` | 左下 |
| `{ x: 0.5, y: 1.0 }` | 下中 |
| `{ x: 1.0, y: 1.0 }` | 右下 |

## 盒模型

```
+---------------------------+
|         margin            |
|  +---------------------+  |
|  |      padding        |  |
|  |  +---------------+  |  |
|  |  |   content     |  |  |
|  |  +---------------+  |  |
|  +---------------------+  |
+---------------------------+
```

## 编写代码时

1. 弹性容器用 `Fill`，内容自适应元素用 `Fit`
2. 纵向排列设 `flow: Down`，横向排列设 `flow: Right`
3. 行布局中用空的 `<View> { width: Fill }` 作间隔
4. 固定尺寸元素务必显式设置尺寸
5. 用 `align` 定位容器内的子元素

## 解答问题时

1. Makepad 采用"海龟"布局模型——元素按顺序依次排列
2. `Fill` 占满可用空间，`Fit` 收缩至内容大小
3. 与 CSS flexbox 不同，没有 flex-grow/shrink——用 Fill/Fit 代替
4. align 作用于子元素，而非元素自身

## 限制
- 仅在任务明确符合上述范围时使用本技能
- 输出不能替代环境验证、测试或专家审查
- 缺少必要输入、权限、安全边界或成功标准时，停下来询问确认
