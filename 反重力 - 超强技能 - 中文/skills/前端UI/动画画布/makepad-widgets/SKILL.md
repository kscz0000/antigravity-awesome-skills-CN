---
name: makepad-widgets
description: "版本：makepad-widgets（dev 分支）| 最后更新：2026-01-19 > > 检查更新：https://crates.io/crates/makepad-widgets | 当用户需要使用 Makepad 组件、编写 Makepad UI 代码、查询组件属性或变体时使用。"
risk: safe
source: community
---

# Makepad Widgets 技能

> **版本：** makepad-widgets（dev 分支）| **最后更新：** 2026-01-19
>
> 检查更新：https://crates.io/crates/makepad-widgets

你是 Makepad 组件专家，帮助用户：
- **编写代码**：按照下方模式生成组件代码
- **解答问题**：解释组件属性、变体和用法

## 适用场景
- 需要使用 Makepad 核心或高级组件
- 涉及组件选择、属性、变体、组合或组件特有行为
- 需要 `View`、`Button`、标签、富文本等 `makepad-widgets` 构建块的示例

## 文档

详细文档请参阅本地文件：
- `./references/widgets-core.md` - 核心组件（View、Button、Label 等）
- `./references/widgets-advanced.md` - 辅助与高级组件
- `./references/widgets-richtext.md` - 富文本组件（Markdown、Html、TextFlow）

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上方列出的相关参考文件
2. 若文件读取失败或为空：
   - 提示用户："本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档"
   - 仍基于 SKILL.md 模式和内置知识作答
3. 若参考文件存在，将其内容纳入回答

## 核心模式

### 1. View（基础容器）

```rust
<View> {
    width: Fill
    height: Fill
    flow: Down
    padding: 16.0
    show_bg: true
    draw_bg: { color: #1A1A1A }

    <Label> { text: "Content" }
}
```

### 2. Button

```rust
<Button> {
    text: "Click Me"
    draw_bg: {
        color: #0066CC
        color_hover: #0088FF
        border_radius: 4.0
    }
    draw_text: {
        color: #FFFFFF
        text_style: { font_size: 14.0 }
    }
}
```

### 3. 带样式的 Label

```rust
<Label> {
    width: Fit
    height: Fit
    text: "Hello World"
    draw_text: {
        color: #FFFFFF
        text_style: {
            font_size: 16.0
            line_spacing: 1.4
        }
    }
}
```

### 4. Image

```rust
<Image> {
    width: 200.0
    height: 150.0
    source: dep("crate://self/resources/photo.png")
    fit: Contain
}
```

### 5. TextInput

```rust
<TextInput> {
    width: Fill
    height: Fit
    text: "Default value"
    draw_text: {
        text_style: { font_size: 14.0 }
    }
}
```

## Widget Traits（源自源码）

```rust
pub trait WidgetNode: LiveApply {
    fn find_widgets(&self, path: &[LiveId], cached: WidgetCache, results: &mut WidgetSet);
    fn walk(&mut self, cx: &mut Cx) -> Walk;
    fn area(&self) -> Area;
    fn redraw(&mut self, cx: &mut Cx);
}

pub trait Widget: WidgetNode {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {}
    fn draw_walk(&mut self, cx: &mut Cx2d, scope: &mut Scope, walk: Walk) -> DrawStep;
    fn draw(&mut self, cx: &mut Cx2d, scope: &mut Scope) -> DrawStep;
    fn widget(&self, path: &[LiveId]) -> WidgetRef;
}
```

## 全部内置组件（widgets/src/ 下 84 个文件）

| 分类 | 组件 |
|------|------|
| **基础** | `View`、`Label`、`Button`、`Icon`、`Image` |
| **输入** | `TextInput`、`CheckBox`、`RadioButton`、`Slider`、`DropDown`、`ColorPicker` |
| **容器** | `ScrollBars`、`PortalList`、`FlatList`、`StackNavigation`、`Dock`、`Splitter` |
| **导航** | `TabBar`、`Tab`、`FoldHeader`、`FoldButton`、`ExpandablePanel` |
| **浮层** | `Modal`、`Tooltip`、`PopupMenu`、`PopupNotification` |
| **媒体** | `Video`、`RotatedImage`、`ImageBlend`、`MultiImage` |
| **布局** | `AdaptiveView`、`SlidePanel`、`PageFlip`、`SlidesView` |
| **特殊** | `Markdown`、`Html`、`TextFlow`、`WebView`、`KeyboardView` |
| **工具** | `LoadingSpinner`、`DesktopButton`、`LinkLabel`、`ScrollShadow` |

## 核心组件参考

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `View` | 容器 | `flow`、`align`、`show_bg`、`draw_bg`、`optimize` |
| `Button` | 可点击 | `text`、`draw_bg`、`draw_text`、`draw_icon` |
| `Label` | 文本显示 | `text`、`draw_text` |
| `Image` | 图片显示 | `source`、`fit` |
| `TextInput` | 文本输入 | `text`、`draw_text`、`draw_cursor`、`draw_selection` |
| `CheckBox` | 开关 | `text`、`selected` |
| `RadioButton` | 单选 | `text`、`selected` |
| `Slider` | 滑块 | `min`、`max`、`step` |
| `DropDown` | 下拉菜单 | `labels`、`selected` |
| `PortalList` | 虚拟列表 | 大列表高效滚动 |
| `Modal` | 对话框 | 浮层对话框 |
| `Tooltip` | 提示 | 悬停提示 |

## View 变体

| 变体 | 说明 |
|------|------|
| `SolidView` | 纯色背景 |
| `RoundedView` | 圆角 |
| `RoundedAllView` | 独立控制各角 |
| `RectView` | 带边框/渐变的矩形 |
| `CircleView` | 圆形/椭圆 |
| `GradientXView` | 水平渐变 |
| `GradientYView` | 垂直渐变 |
| `RoundedShadowView` | 圆角带阴影 |
| `ScrollXView` | 水平滚动 |
| `ScrollYView` | 垂直滚动 |
| `ScrollXYView` | 双向滚动 |
| `CachedView` | 纹理缓存 |

## Button 变体

| 变体 | 说明 |
|------|------|
| `ButtonFlat` | 扁平样式 |
| `ButtonFlatIcon` | 扁平带图标 |
| `ButtonFlatter` | 无背景 |
| `ButtonGradientX` | 水平渐变 |
| `ButtonGradientY` | 垂直渐变 |
| `ButtonIcon` | 标准带图标 |

## ImageFit 值

| 值 | 说明 |
|----|------|
| `Stretch` | 拉伸填满 |
| `Contain` | 适应区域，保持比例 |
| `Cover` | 覆盖区域，可能裁剪 |
| `Fill` | 填满，不保持比例 |

## 编写代码时

1. 始终为组件设置 `width` 和 `height`
2. 使用 `show_bg: true` 启用背景渲染
3. 通过 `draw_bg`、`draw_text`、`draw_icon` 访问着色器 uniform
4. 使用 `dep("crate://self/...")` 指定资源路径
5. 根据视觉需求选择合适的 View 变体

## 解答问题时

1. 推荐 UI Zoo 示例用于组件探索
2. View 是基础容器——大多数视觉组件继承自它
3. 绘制着色器（`draw_bg`、`draw_text`）控制外观
4. 所有组件通过 `animator` 属性支持动画

## 局限
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清
