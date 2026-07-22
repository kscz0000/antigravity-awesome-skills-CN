---
name: makepad-font
description: |
  关键：用于 Makepad 字体与文字渲染。当用户要求'makepad字体'、'makepad文字'、
  'makepad字形'、'makepad排版'、'font atlas'、'text layout'、'font family'、
  'font size'、'text shaping'、'makepad字体'、'makepad文字'、'makepad排版'、
  'makepad字形'时使用。
risk: safe
source: community
---

# Makepad 字体技能

> **版本：** makepad-widgets (dev 分支) | **最后更新：** 2026-01-19
>
> 检查更新：https://crates.io/crates/makepad-widgets

你是 Makepad 文字和字体渲染方面的专家。帮助用户处理：
- **字体配置**：字体族、字号、样式
- **文字排版**：理解文字排版器和塑形
- **文字渲染**：基于 GPU 的 SDF 文字渲染

## 文档

详细文档请参考本地文件：
- `./references/font-system.md` - 字体模块结构与 API

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上方列出的相关参考文件
2. 如果文件读取失败或为空：
   - 告知用户："本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档"
   - 仍基于 SKILL.md 模式 + 内置知识作答
3. 如果参考文件存在，将其内容整合到回答中

## 文字模块结构

```
draw/src/text/
├── font.rs           # Font handle and metrics
├── font_atlas.rs     # GPU texture atlas for glyphs
├── font_face.rs      # Font face data
├── font_family.rs    # Font family management
├── fonts.rs          # Built-in fonts
├── glyph_outline.rs  # Glyph vector outlines
├── glyph_raster_image.rs # Rasterized glyph images
├── layouter.rs       # Text layout engine
├── rasterizer.rs     # Glyph rasterization
├── sdfer.rs          # Signed distance field generator
├── selection.rs      # Text selection/cursor
├── shaper.rs         # Text shaping (harfbuzz)
```

## 在 DSL 中使用字体

### 文字样式

```rust
<Label> {
    text: "Hello World"
    draw_text: {
        text_style: {
            font: { path: dep("crate://self/resources/fonts/MyFont.ttf") }
            font_size: 16.0
            line_spacing: 1.5
            letter_spacing: 0.0
        }
        color: #FFFFFF
    }
}
```

### 主题字体

```rust
<Label> {
    text: "Styled Text"
    draw_text: {
        text_style: <THEME_FONT_REGULAR> {
            font_size: (THEME_FONT_SIZE_P)
        }
    }
}
```

## 在 DSL 中定义字体

```rust
live_design! {
    // Define font path
    FONT_REGULAR = {
        font: { path: dep("crate://self/resources/fonts/Regular.ttf") }
    }

    FONT_BOLD = {
        font: { path: dep("crate://self/resources/fonts/Bold.ttf") }
    }

    // Use in widget
    <Label> {
        draw_text: {
            text_style: <FONT_REGULAR> {
                font_size: 14.0
            }
        }
    }
}
```

## Layouter API

```rust
pub struct Layouter {
    loader: Loader,
    cache_size: usize,
    cached_params: VecDeque<OwnedLayoutParams>,
    cached_results: HashMap<OwnedLayoutParams, Rc<LaidoutText>>,
}

impl Layouter {
    pub fn new(settings: Settings) -> Self;
    pub fn rasterizer(&self) -> &Rc<RefCell<Rasterizer>>;
    pub fn is_font_family_known(&self, id: FontFamilyId) -> bool;
    pub fn define_font_family(&mut self, id: FontFamilyId, definition: FontFamilyDefinition);
    pub fn define_font(&mut self, id: FontId, definition: FontDefinition);
    pub fn get_or_layout(&mut self, params: impl LayoutParams) -> Rc<LaidoutText>;
}
```

## 排版参数

```rust
pub struct OwnedLayoutParams {
    pub text: Substr,
    pub spans: Box<[Span]>,
    pub options: LayoutOptions,
}

pub struct Span {
    pub style: Style,
    pub len: usize,
}

pub struct Style {
    pub font_family_id: FontFamilyId,
    pub font_size_in_pts: f32,
    pub color: Option<Color>,
}

pub struct LayoutOptions {
    pub max_width_in_lpxs: Option<f32>,  // Max width for wrapping
    pub wrap: bool,                       // Enable word wrap
    pub first_row_indent_in_lpxs: f32,    // First line indent
}
```

## 光栅化器设置

```rust
pub struct Settings {
    pub loader: loader::Settings,
    pub cache_size: usize,  // Default: 4096
}

pub struct rasterizer::Settings {
    pub sdfer: sdfer::Settings {
        padding: 4,     // SDF padding
        radius: 8.0,    // SDF radius
        cutoff: 0.25,   // SDF cutoff
    },
    pub grayscale_atlas_size: Size::new(4096, 4096),
    pub color_atlas_size: Size::new(2048, 2048),
}
```

## DrawText 组件

```rust
<View> {
    // Label is a simple text widget
    <Label> {
        text: "Simple Label"
        draw_text: {
            color: #FFFFFF
            text_style: {
                font_size: 14.0
            }
        }
    }

    // TextFlow for rich text
    <TextFlow> {
        <Bold> { text: "Bold text" }
        <Italic> { text: "Italic text" }
        <Link> {
            text: "Click here"
            href: "https://example.com"
        }
    }
}
```

## 文字属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `text` | String | 文字内容 |
| `font` | Font | 字体资源 |
| `font_size` | f64 | 字号（磅） |
| `line_spacing` | f64 | 行高倍数 |
| `letter_spacing` | f64 | 字间距 |
| `color` | Vec4 | 文字颜色 |
| `brightness` | f64 | 文字亮度 |
| `curve` | f64 | 文字弯曲效果 |

## 回答问题须知

1. Makepad 使用 SDF（有符号距离场）实现任意缩放下的清晰文字
2. 字体加载一次后缓存在 GPU 纹理图集中
3. 文字塑形使用 harfbuzz 实现正确的字形定位
4. 内嵌字体资源使用 `dep("crate://...")` 路径
5. 默认字体缓存大小为 4096 个字形
6. 图集尺寸：灰度 4096x4096，彩色（emoji）2048x2048


## 使用时机
涉及上述核心领域或功能的相关任务时使用本技能。

## 局限
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境验证、测试或专家审查
- 缺少必要输入、权限、安全边界或成功标准时，停下来确认