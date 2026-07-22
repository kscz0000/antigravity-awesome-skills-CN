# 触控心理学参考

> 深入探讨移动端触控交互、触控版Fitts定律、拇指区解剖、手势心理学和触觉反馈。
> **这是 ux-psychology.md 的移动端等价物——所有移动端工作的关键参考。**

---

## 1. 触控版Fitts定律

### 根本差异

```
DESKTOP (Mouse/Trackpad):
├── Cursor size: 1 pixel (precision)
├── Visual feedback: Hover states
├── Error cost: Low (easy to retry)
└── Target acquisition: Fast, precise

MOBILE (Finger):
├── Contact area: ~7mm diameter (imprecise)
├── Visual feedback: No hover, only tap
├── Error cost: High (frustrating retries)
├── Occlusion: Finger covers the target
└── Target acquisition: Slower, needs larger targets
```

### Fitts定律公式适配

```
Touch acquisition time = a + b × log₂(1 + D/W)

Where:
├── D = Distance to target
├── W = Width of target
└── For touch: W must be MUCH larger than desktop
```

### 最小触控目标尺寸

| 平台 | 最小值 | 推荐值 | 用途 |
|------|--------|--------|------|
| **iOS (HIG)** | 44pt × 44pt | 48pt+ | 所有可点击元素 |
| **Android (Material)** | 48dp × 48dp | 56dp+ | 所有可点击元素 |
| **WCAG 2.2** | 44px × 44px | - | 无障碍合规 |
| **关键操作** | - | 56-64px | 主要CTA、破坏性操作 |

### 视觉尺寸 vs 点击区域

```
┌─────────────────────────────────────┐
│                                     │
│    ┌─────────────────────────┐      │
│    │                         │      │
│    │    [  BUTTON  ]         │ ← Visual: 36px
│    │                         │      │
│    └─────────────────────────┘      │
│                                     │ ← Hit area: 48px (padding extends)
└─────────────────────────────────────┘

✅ CORRECT: Visual can be smaller if hit area is minimum 44-48px
❌ WRONG: Making hit area same as small visual element
```

### 应用规则

| 元素 | 视觉尺寸 | 点击区域 |
|------|----------|----------|
| 图标按钮 | 24-32px | 44-48px（内边距扩展） |
| 文本链接 | 任意 | 最小44px高度 |
| 列表项 | 全宽 | 48-56px高度 |
| 复选框/单选框 | 20-24px | 44-48px点击区域 |
| 关闭/X按钮 | 24px | 最小44px |
| Tab栏项 | 图标24-28px | 全tab宽度，49px高度（iOS） |

---

## 2. 拇指区解剖

### 单手持机使用

```
Research shows: 49% of users hold phone one-handed.

┌─────────────────────────────────────┐
│                                     │
│  ┌─────────────────────────────┐    │
│  │       HARD TO REACH         │    │ ← Status bar, top nav
│  │      (requires stretch)     │    │    Put: Back, menu, settings
│  │                             │    │
│  ├─────────────────────────────┤    │
│  │                             │    │
│  │       OK TO REACH           │    │ ← Content area
│  │      (comfortable)          │    │    Put: Secondary actions, content
│  │                             │    │
│  ├─────────────────────────────┤    │
│  │                             │    │
│  │       EASY TO REACH         │    │ ← Tab bar, FAB zone
│  │      (thumb's arc)          │    │    Put: PRIMARY CTAs!
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│          [    HOME    ]             │
└─────────────────────────────────────┘
```

### 拇指弧线（右手用户）

```
Right hand holding phone:

┌───────────────────────────────┐
│  STRETCH      STRETCH    OK   │
│                               │
│  STRETCH        OK       EASY │
│                               │
│    OK          EASY      EASY │
│                               │
│   EASY         EASY      EASY │
└───────────────────────────────┘

Left hand is mirrored.
→ Design for BOTH hands or assume right-dominant
```

### 布局指南

| 元素类型 | 理想位置 | 原因 |
|----------|----------|------|
| **主要CTA** | 底部居中/右侧 | 拇指轻松触及 |
| **Tab栏** | 底部 | 拇指自然位置 |
| **FAB** | 右下角 | 右手轻松操作 |
| **导航** | 顶部（需伸展） | 使用频率较低 |
| **破坏性操作** | 左上角 | 难以触及 = 更难误触 |
| **关闭/取消** | 左上角 | 惯例 + 安全性 |
| **确认/完成** | 右上角或底部 | 惯例 |

### 大屏手机注意事项（>6英寸）

```
On large phones, top 40% becomes "dead zone" for one-handed use.

Solutions:
├── Reachability features (iOS)
├── Pull-down interfaces (drawer pulls content down)
├── Bottom sheet navigation
├── Floating action buttons
└── Gesture-based alternatives to top actions
```

---

## 3. 触控 vs 点击心理学

### 预期差异

| 维度 | 点击（桌面端） | 触控（移动端） |
|------|----------------|----------------|
| **反馈时机** | 可等待100ms | 期望即时（<50ms） |
| **视觉反馈** | 悬停 → 点击 | 即时点击响应 |
| **容错性** | 容易重试 | 令人沮丧，感觉坏了 |
| **精度** | 高 | 低 |
| **上下文菜单** | 右键点击 | 长按 |
| **取消操作** | ESC键 | 滑动关闭、点击外部 |

### 触控反馈要求

```
Tap → Immediate visual change (< 50ms)
├── Highlight state (background color change)
├── Scale down slightly (0.95-0.98)
├── Ripple effect (Android Material)
├── Haptic feedback for confirmation
└── Never nothing!

Loading → Show within 100ms
├── If action takes > 100ms
├── Show spinner/progress
├── Disable button (prevent double tap)
└── Optimistic UI when possible
```

### "粗手指"问题

```
Problem: Finger occludes target during tap
├── User can't see exactly where they're tapping
├── Visual feedback appears UNDER finger
└── Increases error rate

Solutions:
├── Show feedback ABOVE touch point (tooltips)
├── Use cursor-like offset for precision tasks
├── Magnification loupe for text selection
└── Large enough targets that precision doesn't matter
```

---

## 4. 手势心理学

### 手势可发现性问题

```
Problem: Gestures are INVISIBLE.
├── User must discover/remember them
├── No hover/visual hint
├── Different mental model than tap
└── Many users never discover gestures

Solution: Always provide visible alternative
├── Swipe to delete → Also show delete button or menu
├── Pull to refresh → Also show refresh button
├── Pinch to zoom → Also show zoom controls
└── Gestures as shortcuts, not only way
```

### 常见手势惯例

| 手势 | 通用含义 | 用法 |
|------|----------|------|
| **点击** | 选择、激活 | 主要操作 |
| **双击** | 放大、点赞/收藏 | 快捷操作 |
| **长按** | 上下文菜单、选择模式 | 次要选项 |
| **水平滑动** | 导航、删除、操作 | 列表操作 |
| **下拉** | 刷新、关闭 | 下拉刷新 |
| **捏合** | 缩放 | 地图、图片 |
| **双指滚动** | 嵌套滚动内滚动 | 嵌套滚动区域 |

### 手势可供性设计

```
Swipe actions need visual hints:

┌─────────────────────────────────────────┐
│  ┌───┐                                  │
│  │ ≡ │  Item with hidden actions...   → │ ← Edge hint (partial color)
│  └───┘                                  │
└─────────────────────────────────────────┘

✅ Good: Slight color peek at edge suggesting swipe
✅ Good: Drag handle icon ( ≡ ) suggesting reorder
✅ Good: Onboarding tooltip explaining gesture
❌ Bad: Hidden gestures with no visual affordance
```

### 平台手势差异

| 手势 | iOS | Android |
|------|-----|---------|
| **返回** | 从左边缘滑动 | 系统返回按钮/手势 |
| **分享** | Action Sheet | 分享面板 |
| **上下文菜单** | 长按 / Force Touch | 长按 |
| **关闭模态** | 下拉滑动 | 返回按钮或滑动 |
| **列表中删除** | 左滑，点击删除 | 左滑，立即删除或撤销 |

---

## 5. 触觉反馈模式

### 触觉为何重要

```
Haptics provide:
├── Confirmation without looking
├── Richer, more premium feel
├── Accessibility (blind users)
├── Reduced error rate
└── Emotional satisfaction

Without haptics:
├── Feels "cheap" or web-like
├── User unsure if action registered
└── Missed opportunity for delight
```

### iOS触觉类型

| 类型 | 强度 | 用例 |
|------|------|------|
| `selection` | 轻 | 选择器滚动、开关、选择 |
| `light` | 轻 | 次要操作、悬停等价 |
| `medium` | 中 | 标准点击确认 |
| `heavy` | 强 | 重要操作完成、放置 |
| `success` | 模式 | 任务成功完成 |
| `warning` | 模式 | 警告、需要注意 |
| `error` | 模式 | 发生错误 |

### Android触觉类型

| 类型 | 用例 |
|------|------|
| `CLICK` | 标准点击反馈 |
| `HEAVY_CLICK` | 重要操作 |
| `DOUBLE_CLICK` | 确认操作 |
| `TICK` | 滚动/拖拽反馈 |
| `LONG_PRESS` | 长按激活 |
| `REJECT` | 错误/无效操作 |

### 触觉使用指南

```
✅ DO use haptics for:
├── Button taps
├── Toggle switches
├── Picker/slider values
├── Pull to refresh trigger
├── Successful action completion
├── Errors and warnings
├── Swipe action thresholds
└── Important state changes

❌ DON'T use haptics for:
├── Every scroll position
├── Every list item
├── Background events
├── Passive displays
└── Too frequently (haptic fatigue)
```

### 触觉强度映射

| 操作重要性 | 触觉等级 | 示例 |
|------------|----------|------|
| 次要/浏览 | 轻 / 无 | 滚动、悬停 |
| 标准操作 | 中 / selection | 点击、切换 |
| 重要操作 | 强 / success | 完成、确认 |
| 关键/破坏性 | 强 / warning | 删除、支付 |
| 错误 | error模式 | 操作失败 |

---

## 6. 移动端认知负荷

### 移动端与桌面端的差异

| 因素 | 桌面端 | 移动端 | 设计启示 |
|------|--------|--------|----------|
| **注意力** | 专注时段 | 频繁中断 | 为微会话设计 |
| **环境** | 受控环境 | 任何地点、任何条件 | 处理强光、噪音 |
| **多任务** | 多窗口 | 单应用可见 | 在应用内完成任务 |
| **输入速度** | 快（键盘） | 慢（触控输入） | 最少输入、智能默认值 |
| **错误恢复** | 容易（撤销、后退） | 较难（无键盘快捷键） | 预防错误、轻松恢复 |

### 降低移动端认知负荷

```
1. ONE PRIMARY ACTION per screen
   └── Clear what to do next

2. PROGRESSIVE DISCLOSURE
   └── Show only what's needed now

3. SMART DEFAULTS
   └── Pre-fill what you can

4. CHUNKING
   └── Break long forms into steps

5. RECOGNITION over RECALL
   └── Show options, don't make user remember

6. CONTEXT PERSISTENCE
   └── Save state on interrupt/background
```

### 移动端Miller定律

```
Desktop: 7±2 items in working memory
Mobile: Reduce to 5±1 (more distractions)

Navigation: Max 5 tab bar items
Options: Max 5 per menu level
Steps: Max 5 visible steps in progress
```

### 移动端Hick定律

```
More choices = slower decisions

Mobile impact: Even worse than desktop
├── Smaller screen = less overview
├── Scrolling required = items forgotten
├── Interruptions = lost context
└── Decision fatigue faster

Solution: Progressive disclosure
├── Start with 3-5 options
├── "More" for additional
├── Smart ordering (most used first)
└── Previous selections remembered
```

---

## 7. 触控无障碍

### 运动障碍考量

```
Users with motor impairments may:
├── Have tremors (need larger targets)
├── Use assistive devices (different input method)
├── Have limited reach (one-handed necessity)
├── Need more time (avoid timeouts)
└── Make accidental touches (need confirmation)

Design responses:
├── Generous touch targets (48dp+)
├── Adjustable timing for gestures
├── Undo for destructive actions
├── Switch control support
└── Voice control support
```

### 触控目标间距（无障碍）

```
WCAG 2.2 Success Criterion 2.5.8:

Touch targets MUST have:
├── Width: ≥ 44px
├── Height: ≥ 44px
├── Spacing: ≥ 8px from adjacent targets

OR the target is:
├── Inline (within text)
├── User-controlled (user can resize)
├── Essential (no alternative design)
```

### 无障碍触控模式

| 模式 | 无障碍实现方式 |
|------|----------------|
| 滑动操作 | 提供菜单替代 |
| 拖放 | 提供选择 + 移动选项 |
| 捏合缩放 | 提供缩放按钮 |
| Force Touch | 提供长按替代 |
| 摇动手势 | 提供按钮替代 |

---

## 8. 触控中的情感

### 高级质感

```
What makes touch feel "premium":
├── Instant response (< 50ms)
├── Appropriate haptic feedback
├── Smooth 60fps animations
├── Correct resistance/physics
├── Sound feedback (when appropriate)
└── Attention to spring physics
```

### 情感化触控反馈

| 情感 | 触控响应 |
|------|----------|
| 成功 | 触觉success + 彩带/对勾 |
| 错误 | 触觉error + 抖动动画 |
| 警告 | 触觉warning + 注意色 |
| 愉悦 | 意外的流畅动画 |
| 力量感 | 重要操作的强触觉反馈 |

### 通过触控建立信任

```
Trust signals in touch interactions:
├── Consistent behavior (same action = same response)
├── Reliable feedback (never fails silently)
├── Secure feel for sensitive actions
├── Professional animations (not janky)
└── No accidental actions (confirmation for destructive)
```

---

## 9. 触控心理学检查清单

### 每个界面之前

- [ ] **所有触控目标 ≥ 44-48px？**
- [ ] **主要CTA在拇指区内？**
- [ ] **破坏性操作需要确认？**
- [ ] **手势替代方案存在（可见按钮）？**
- [ ] **重要操作有触觉反馈？**
- [ ] **点击后即时视觉反馈？**
- [ ] **超过100ms的操作有加载状态？**

### 发布之前

- [ ] **在最小支持设备上测试过？**
- [ ] **在大屏手机上单手测试过？**
- [ ] **所有手势都有可见替代方案？**
- [ ] **触觉反馈正常工作（真机测试）？**
- [ ] **触控目标在无障碍设置下测试过？**
- [ ] **没有微小的关闭按钮或图标？**

---

## 10. 快速参考卡

### 触控目标尺寸

```
                     iOS        Android     WCAG
Minimum:           44pt       48dp       44px
Recommended:       48pt+      56dp+      -
Spacing:           8pt+       8dp+       8px+
```

### 拇指区操作

```
TOP:      Navigation, settings, back (infrequent)
MIDDLE:   Content, secondary actions
BOTTOM:   Primary CTA, tab bar, FAB (frequent)
```

### 触觉选择

```
Light:    Selection, toggle, minor
Medium:   Tap, standard action
Heavy:    Confirm, complete, drop
Success:  Task done
Error:    Failed action
Warning:  Attention needed
```

---

> **记住：** 每一次触控都是用户与设备之间的对话。让它感觉自然、响应迅速、尊重人类手指——而非精确的光标点。
