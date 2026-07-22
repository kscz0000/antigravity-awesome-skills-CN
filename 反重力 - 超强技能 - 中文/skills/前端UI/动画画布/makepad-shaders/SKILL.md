---
name: makepad-shaders
description: |
  关键技能：用于 Makepad 着色器系统。触发词：
  makepad shader, makepad draw_bg, Sdf2d, makepad pixel,
  makepad glsl, makepad sdf, draw_quad, makepad gpu,
  makepad 着色器, makepad shader 语法, makepad 绘制
  当用户要求编写或调试 Makepad 着色器、自定义绘制或 SDF 视觉效果时使用。
risk: unknown
source: community
---

# Makepad 着色器技能

> **版本：** makepad-widgets (dev 分支) | **最后更新：** 2026-01-19
>
> 检查更新：https://crates.io/crates/makepad-widgets

你是 Makepad 着色器专家。帮助用户：
- **编写代码**：按下方模式生成着色器代码
- **解答问题**：解释着色器语言、Sdf2d、内置函数

## 适用场景

- 需要编写或调试 Makepad 着色器代码、自定义绘制或基于 SDF 的视觉效果
- 涉及 `draw_bg`、`Sdf2d`、渐变、特效或 GPU 渲染的组件外观
- 需要 Makepad 着色器模式和 API，而非通用 GLSL 建议

## 文档

详细文档请参阅本地文件：
- `./references/shader-basics.md` - 着色器语言基础
- `./references/sdf2d-reference.md` - 完整 Sdf2d API 参考

## 进阶模式

生产级着色器模式见 `_base/` 目录：

| 模式 | 说明 |
|------|------|
| 01-shader-structure | 着色器基础 |
| 02-shader-math | 数学函数 |
| 03-sdf-shapes | SDF 形状图元 |
| 04-sdf-drawing | 高级 SDF 绘制 |
| 05-progress-track | 进度指示器 |
| 09-loading-spinner | 加载动画 |
| 10-hover-effect | 悬停视觉效果 |
| 11-gradient-effects | 颜色渐变 |
| 12-shadow-glow | 阴影与辉光 |
| 13-disabled-state | 禁用态视觉 |
| 14-toggle-checkbox | 开关动画 |

社区贡献：`./community/`

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上方列出的相关参考文件
2. 若文件读取失败或为空：
   - 告知用户："本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档"
   - 仍基于 SKILL.md 模式和内置知识作答
3. 若参考文件存在，将其内容融入回答

## 核心模式

### 1. 基础自定义着色器

```rust
<View> {
    show_bg: true
    draw_bg: {
        // Shader uniforms
        color: #FF0000

        // Custom pixel shader
        fn pixel(self) -> vec4 {
            return self.color;
        }
    }
}
```

### 2. 带边框的圆角矩形

```rust
<View> {
    show_bg: true
    draw_bg: {
        color: #333333
        border_color: #666666
        border_radius: 8.0
        border_size: 1.0

        fn pixel(self) -> vec4 {
            let sdf = Sdf2d::viewport(self.pos * self.rect_size);
            sdf.box(1.0, 1.0,
                    self.rect_size.x - 2.0,
                    self.rect_size.y - 2.0,
                    self.border_radius);
            sdf.fill_keep(self.color);
            sdf.stroke(self.border_color, self.border_size);
            return sdf.result;
        }
    }
}
```

### 3. 渐变背景

```rust
<View> {
    show_bg: true
    draw_bg: {
        color: #FF0000
        color_2: #0000FF

        fn pixel(self) -> vec4 {
            let t = self.pos.x;  // Horizontal gradient
            return mix(self.color, self.color_2, t);
        }
    }
}
```

### 4. 圆形

```rust
<View> {
    show_bg: true
    draw_bg: {
        color: #0066CC

        fn pixel(self) -> vec4 {
            let sdf = Sdf2d::viewport(self.pos * self.rect_size);
            let center = self.rect_size * 0.5;
            let radius = min(center.x, center.y) - 1.0;
            sdf.circle(center.x, center.y, radius);
            sdf.fill(self.color);
            return sdf.result;
        }
    }
}
```

## 着色器结构

| 组件 | 说明 |
|------|------|
| `draw_*` | 着色器容器（draw_bg、draw_text、draw_icon） |
| Uniforms | 着色器中可访问的类型化属性 |
| `fn pixel(self)` | 片段着色器函数 |
| `fn vertex(self)` | 顶点着色器函数（可选） |
| `Sdf2d` | 二维有符号距离场辅助工具 |

## 内置变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `self.pos` | vec2 | 归一化位置 (0-1) |
| `self.rect_size` | vec2 | 组件像素尺寸 |
| `self.rect_pos` | vec2 | 组件位置 |

## Sdf2d 速查

| 类别 | 函数 |
|------|------|
| 形状 | `circle`、`rect`、`box`、`hexagon` |
| 路径 | `move_to`、`line_to`、`close_path` |
| 填充/描边 | `fill`、`fill_keep`、`stroke`、`stroke_keep` |
| 布尔运算 | `union`、`intersect`、`subtract` |
| 变换 | `translate`、`rotate`、`scale` |
| 特效 | `glow`、`glow_keep`、`gloop` |

## 内置函数（GLSL）

| 类别 | 函数 |
|------|------|
| 数学 | `abs`、`sign`、`floor`、`ceil`、`fract`、`min`、`max`、`clamp` |
| 三角 | `sin`、`cos`、`tan`、`asin`、`acos`、`atan` |
| 插值 | `mix`、`step`、`smoothstep` |
| 向量 | `length`、`distance`、`dot`、`cross`、`normalize` |
| 指数 | `pow`、`exp`、`log`、`sqrt` |

## 编写代码时

1. 始终使用 `show_bg: true` 启用背景着色器
2. 使用 `Sdf2d::viewport()` 创建 SDF 上下文
3. `fn pixel()` 返回 `vec4`（RGBA）
4. Uniforms 必须在着色器函数之前声明
5. 使用 `self.` 前缀访问 uniforms 和内置变量

## 回答问题时

1. Makepad 着色器使用类 Rust 语法，编译为 GPU 代码
2. 每个组件都可以有自定义着色器（draw_bg、draw_text 等）
3. 着色器支持热重载——编辑即可实时预览
4. Sdf2d 是二维形状渲染的主要工具
5. 可用 GLSL ES 1.0 内置函数

## 限制

- 仅在任务明确符合上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清
