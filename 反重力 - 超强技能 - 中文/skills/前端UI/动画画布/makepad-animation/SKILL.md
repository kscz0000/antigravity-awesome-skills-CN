---
name: makepad-animation
description: |
  CRITICAL: Use for Makepad animation system. Triggers on:
  makepad animation, makepad animator, makepad hover, makepad state,
  makepad transition, "from: { all: Forward", makepad pressed,
  makepad 动画, makepad 状态, makepad 过渡, makepad 悬停效果
risk: safe
source: community
---

# Makepad 动画技能

> **版本:** makepad-widgets (开发分支) | **最后更新:** 2026-01-19
>
> 检查更新: https://crates.io/crates/makepad-widgets

你是 Makepad 动画领域的专家。通过以下方式协助用户：
- **编写代码**: 遵循下方模式生成动画代码
- **解答问题**: 解释状态、过渡和时间轴

## 何时使用
- 需要在 Makepad 中构建或调试动画、过渡、悬停状态或动画器时间轴时。
- 任务涉及 `animator`、状态变更、缓动、关键帧或视觉交互反馈时。
- 需要 Makepad 专属的动画模式，而非通用 Rust UI 指导时。

## 文档

参阅本地文件获取详细文档：
- `./references/animation-system.md` - 完整的动画参考

## 高级模式

有关生产环境可用的动画模式，请查阅 `_base/` 目录：

| 模式 | 描述 |
|---------|-------------|
| 06-animator-basics | 动画器基础 |
| 07-easing-functions | 缓动与时间控制 |
| 08-keyframe-animation | 复杂关键帧 |

## 重要：文档完整性检查

**回答问题前，Claude 必须：**

1. 读取上方列出的相关参考文件
2. 若读取失败或文件为空：
   - 告知用户：“本地文档不完整，建议运行 `/sync-crate-skills makepad --force` 更新文档”
   - 仍基于 SKILL.md 模式和内置知识作答
3. 若参考文件存在，将其中内容融入答案

## 关键模式

### 1. 基础悬停动画

```rust
<Button> {
    text: "Hover Me"

    animator: {
        hover = {
            default: off

            off = {
                from: { all: Forward { duration: 0.15 } }
                apply: {
                    draw_bg: { color: #333333 }
                }
            }

            on = {
                from: { all: Forward { duration: 0.15 } }
                apply: {
                    draw_bg: { color: #555555 }
                }
            }
        }
    }
}
```

### 2. 多状态动画

```rust
<View> {
    animator: {
        hover = {
            default: off
            off = {
                from: { all: Forward { duration: 0.2 } }
                apply: { draw_bg: { color: #222222 } }
            }
            on = {
                from: { all: Forward { duration: 0.2 } }
                apply: { draw_bg: { color: #444444 } }
            }
        }

        pressed = {
            default: off
            off = {
                from: { all: Forward { duration: 0.1 } }
                apply: { draw_bg: { scale: 1.0 } }
            }
            on = {
                from: { all: Forward { duration: 0.1 } }
                apply: { draw_bg: { scale: 0.95 } }
            }
        }
    }
}
```

### 3. 焦点状态动画

```rust
<TextInput> {
    animator: {
        focus = {
            default: off

            off = {
                from: { all: Forward { duration: 0.2 } }
                apply: {
                    draw_bg: {
                        border_color: #444444
                        border_size: 1.0
                    }
                }
            }

            on = {
                from: { all: Forward { duration: 0.2 } }
                apply: {
                    draw_bg: {
                        border_color: #0066CC
                        border_size: 2.0
                    }
                }
            }
        }
    }
}
```

### 4. 禁用状态

```rust
<Button> {
    animator: {
        disabled = {
            default: off

            off = {
                from: { all: Snap }
                apply: {
                    draw_bg: { color: #0066CC }
                    draw_text: { color: #FFFFFF }
                }
            }

            on = {
                from: { all: Snap }
                apply: {
                    draw_bg: { color: #333333 }
                    draw_text: { color: #666666 }
                }
            }
        }
    }
}
```

## 动画器结构

| 属性 | 描述 |
|----------|-------------|
| `animator` | 根动画容器 |
| `{state} =` | 状态定义 (hover, pressed, focus, disabled) |
| `default:` | 初始状态值 |
| `{value} =` | 状态值定义 (on, off, custom) |
| `from:` | 过渡时间轴 |
| `apply:` | 要应用动画的属性 |

## 时间轴类型 (Play 枚举)

| 类型 | 描述 |
|------|-------------|
| `Forward { duration: f64 }` | 线性向前动画 |
| `Snap` | 瞬间变更，无过渡 |
| `Reverse { duration: f64, end: f64 }` | 反向动画 |
| `Loop { duration: f64, end: f64 }` | 循环动画 |
| `BounceLoop { duration: f64, end: f64 }` | 弹跳循环动画 |

## 缓动函数 (Ease 枚举)

```rust
// Basic
Linear

// Quadratic
InQuad, OutQuad, InOutQuad

// Cubic
InCubic, OutCubic, InOutCubic

// Quartic
InQuart, OutQuart, InOutQuart

// Quintic
InQuint, OutQuint, InOutQuint

// Sinusoidal
InSine, OutSine, InOutSine

// Exponential
InExp, OutExp, InOutExp

// Circular
InCirc, OutCirc, InOutCirc

// Elastic
InElastic, OutElastic, InOutElastic

// Back
InBack, OutBack, InOutBack

// Bounce
InBounce, OutBounce, InOutBounce

// Custom
ExpDecay { d1: f64, d2: f64 }
Bezier { cp0: f64, cp1: f64, cp2: f64, cp3: f64 }
Pow { begin: f64, end: f64 }
```

### 使用缓动

```rust
from: {
    all: Ease { duration: 0.3, ease: InOutQuad }
}
```

## 常用状态

| 状态 | 值 | 触发条件 |
|-------|--------|---------|
| `hover` | on, off | 鼠标进入/离开 |
| `pressed` / `down` | on, off | 鼠标按下/释放 |
| `focus` | on, off | 获取/失去焦点 |
| `disabled` | on, off | 控件启用/禁用 |
| `selected` | on, off | 选中状态变更 |

## 可动画化属性

大多数 `draw_*` shader uniforms 都可以应用动画：
- 颜色: `color`, `border_color`, `shadow_color`
- 尺寸: `border_size`, `border_radius`, `shadow_radius`
- 变换: `scale`, `rotation`, `offset`
- 透明度: `opacity`

## 编写代码时

1. 始终为初始状态设置 `default:`
2. 使用 `Forward` 实现平滑过渡
3. 使用 `Snap` 实现瞬间状态变更（如禁用）
4. 保持短时长 (0.1-0.3s) 以获得响应感
5. 在 `draw_bg`, `draw_text` 等中对 shader uniforms 应用动画

## Rust API (AnimatorImpl Trait)

```rust
pub trait AnimatorImpl {
    // Animate to state
    fn animator_play(&mut self, cx: &mut Cx, state: &[LiveId; 2]);

    // Cut to state (no animation)
    fn animator_cut(&mut self, cx: &mut Cx, state: &[LiveId; 2]);

    // Check current state
    fn animator_in_state(&self, cx: &Cx, state: &[LiveId; 2]) -> bool;
}

// Usage example
fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {
    match event.hits(cx, self.area()) {
        Hit::FingerHoverIn(_) => {
            self.animator_play(cx, id!(hover.on));
        }
        Hit::FingerHoverOut(_) => {
            self.animator_play(cx, id!(hover.off));
        }
        Hit::FingerDown(_) => {
            self.animator_play(cx, id!(pressed.on));
        }
        Hit::FingerUp(_) => {
            self.animator_play(cx, id!(pressed.off));
        }
        _ => {}
    }
}
```

## 回答问题时

1. 状态是独立的 - 多个状态可同时激活
2. 当状态达到某个值时，动画应用属性
3. `from` 定义如何动画，`apply` 定义动画化什么
4. Makepad 自动在新旧值之间进行插值
5. 使用 `id!(state.value)` 宏在 Rust 中引用动画状态

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 切勿将输出视为环境特定验证、测试或专家审查的替代品。
- 若缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
