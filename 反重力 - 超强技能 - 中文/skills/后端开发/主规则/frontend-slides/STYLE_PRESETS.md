# 样式预设参考

Frontend Slides 的精选视觉样式。每个预设都受真实设计参考启发 — 拒绝通用的"AI 模板感"美学。**仅限抽象形状 — 无插画。**

**视口 CSS：** 必需的基础样式，见 [viewport-base.css](viewport-base.css)。包含在每份演示文稿中。

---

## 深色主题

### 1. Bold Signal

**氛围：** 自信、大胆、现代、高冲击力

**布局：** 深色渐变上的彩色卡片。数字在左上角，导航在右上角，标题在左下角。

**排版：**
- 展示字体：`Archivo Black` (900)
- 正文字体：`Space Grotesk` (400/500)

**颜色：**
```css
:root {
    --bg-primary: #1a1a1a;
    --bg-gradient: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
    --card-bg: #FF5722;
    --text-primary: #ffffff;
    --text-on-card: #1a1a1a;
}
```

**标志性元素：**
- 大胆的彩色卡片作为焦点（橙色、珊瑚色或鲜艳强调色）
- 大号章节编号（01、02 等）
- 带活动/非活动透明度状态的导航面包屑
- 基于网格的布局实现精确对齐

---

### 2. Electric Studio

**氛围：** 大胆、简洁、专业、高对比度

**布局：** 分割面板 — 白色顶部，蓝色底部。品牌标志在角落。

**排版：**
- 展示字体：`Manrope` (800)
- 正文字体：`Manrope` (400/500)

**颜色：**
```css
:root {
    --bg-dark: #0a0a0a;
    --bg-white: #ffffff;
    --accent-blue: #4361ee;
    --text-dark: #0a0a0a;
    --text-light: #ffffff;
}
```

**标志性元素：**
- 双面板垂直分割
- 面板边缘的强调条
- 引用排版作为主视觉元素
- 极简、自信的间距

---

### 3. Creative Voltage

**氛围：** 大胆、创意、充满活力、复古现代

**布局：** 分割面板 — 电光蓝左侧，深色右侧。手写体点缀。

**排版：**
- 展示字体：`Syne` (700/800)
- 等宽字体：`Space Mono` (400/700)

**颜色：**
```css
:root {
    --bg-primary: #0066ff;
    --bg-dark: #1a1a2e;
    --accent-neon: #d4ff00;
    --text-light: #ffffff;
}
```

**标志性元素：**
- 电光蓝 + 霓虹黄对比
- 半调纹理图案
- 霓虹徽章/标注
- 手写字体增添创意风采

---

### 4. Dark Botanical

**氛围：** 优雅、精致、艺术、高端

**布局：** 深色背景上的居中内容。角落有抽象柔和形状。

**排版：**
- 展示字体：`Cormorant` (400/600) — 优雅衬线体
- 正文字体：`IBM Plex Sans` (300/400)

**颜色：**
```css
:root {
    --bg-primary: #0f0f0f;
    --text-primary: #e8e4df;
    --text-secondary: #9a9590;
    --accent-warm: #d4a574;
    --accent-pink: #e8b4b8;
    --accent-gold: #c9b896;
}
```

**标志性元素：**
- 抽象柔和渐变圆（模糊、重叠）
- 暖色调点缀（粉色、金色、赤陶色）
- 细垂直强调线
- 斜体签名排版
- **无插画 — 仅抽象 CSS 形状**

---

## 浅色主题

### 5. Notebook Tabs

**氛围：** 编辑风、有序、优雅、触感

**布局：** 深色背景上的米色纸卡片。右侧边缘有彩色标签。

**排版：**
- 展示字体：`Bodoni Moda` (400/700) — 经典编辑风
- 正文字体：`DM Sans` (400/500)

**颜色：**
```css
:root {
    --bg-outer: #2d2d2d;
    --bg-page: #f8f6f1;
    --text-primary: #1a1a1a;
    --tab-1: #98d4bb; /* 薄荷绿 */
    --tab-2: #c7b8ea; /* 薰衣草 */
    --tab-3: #f4b8c5; /* 粉色 */
    --tab-4: #a8d8ea; /* 天蓝 */
    --tab-5: #ffe6a7; /* 奶油色 */
}
```

**标志性元素：**
- 带柔和阴影的纸张容器
- 右侧边缘的彩色章节标签（垂直文字）
- 左侧的装订孔装饰
- 标签文字必须随视口缩放：`font-size: clamp(0.5rem, 1vh, 0.7rem)`

---

### 6. Pastel Geometry

**氛围：** 友好、有序、现代、亲切

**布局：** 柔和背景上的白色卡片。右侧边缘有垂直胶囊标签。

**排版：**
- 展示字体：`Plus Jakarta Sans` (700/800)
- 正文字体：`Plus Jakarta Sans` (400/500)

**颜色：**
```css
:root {
    --bg-primary: #c8d9e6;
    --card-bg: #faf9f7;
    --pill-pink: #f0b4d4;
    --pill-mint: #a8d4c4;
    --pill-sage: #5a7c6a;
    --pill-lavender: #9b8dc4;
    --pill-violet: #7c6aad;
}
```

**标志性元素：**
- 带柔和阴影的圆角卡片
- **右侧边缘的垂直胶囊标签**，高度各异（类似标签）
- 统一胶囊宽度，高度：短 → 中 → 高 → 中 → 短
- 角落的下载/操作图标

---

### 7. Split Pastel

**氛围：** 俏皮、现代、友好、创意

**布局：** 双色垂直分割（蜜桃色左侧，薰衣草色右侧）。

**排版：**
- 展示字体：`Outfit` (700/800)
- 正文字体：`Outfit` (400/500)

**颜色：**
```css
:root {
    --bg-peach: #f5e6dc;
    --bg-lavender: #e4dff0;
    --text-dark: #1a1a1a;
    --badge-mint: #c8f0d8;
    --badge-yellow: #f0f0c8;
    --badge-pink: #f0d4e0;
}
```

**标志性元素：**
- 分割背景色
- 带图标的俏皮徽章胶囊
- 右侧面板上的网格图案叠加
- 圆角 CTA 按钮

---

### 8. Vintage Editorial

**氛围：** 机智、自信、编辑风、个性驱动

**布局：** 米色背景上的居中内容。抽象几何形状作为点缀。

**排版：**
- 展示字体：`Fraunces` (700/900) — 独特衬线体
- 正文字体：`Work Sans` (400/500)

**颜色：**
```css
:root {
    --bg-cream: #f5f3ee;
    --text-primary: #1a1a1a;
    --text-secondary: #555;
    --accent-warm: #e8d4c0;
}
```

**标志性元素：**
- 抽象几何形状（圆形轮廓 + 线条 + 点）
- 粗边框 CTA 框
- 机智、对话式的文案风格
- **无插画 — 仅几何 CSS 形状**

---

## 特殊主题

### 9. Neon Cyber

**氛围：** 未来感、科技感、自信

**排版：** `Clash Display` + `Satoshi` (Fontshare)

**颜色：** 深海军蓝 (#0a0f1c)、青色点缀 (#00ffcc)、品红 (#ff00aa)

**标志性元素：** 粒子背景、霓虹光晕、网格图案

---

### 10. Terminal Green

**氛围：** 开发者导向、黑客美学

**排版：** `JetBrains Mono`（仅等宽字体）

**颜色：** GitHub 深色 (#0d1117)、终端绿 (#39d353)

**标志性元素：** 扫描线、闪烁光标、代码语法样式

---

### 11. Swiss Modern

**氛围：** 简洁、精确、包豪斯风格

**排版：** `Archivo` (800) + `Nunito` (400)

**颜色：** 纯白、纯黑、红色点缀 (#ff3300)

**标志性元素：** 可见网格、不对称布局、几何形状

---

### 12. Paper & Ink

**氛围：** 编辑风、文学感、深思熟虑

**排版：** `Cormorant Garamond` + `Source Serif 4`

**颜色：** 暖米色 (#faf9f7)、炭灰 (#1a1a1a)、深红点缀 (#c41e3a)

**标志性元素：** 首字下沉、引文、优雅的水平分隔线

---

## 字体搭配快速参考

| 预设 | 展示字体 | 正文字体 | 来源 |
| ---- | -------- | -------- | ---- |
| Bold Signal | Archivo Black | Space Grotesk | Google |
| Electric Studio | Manrope | Manrope | Google |
| Creative Voltage | Syne | Space Mono | Google |
| Dark Botanical | Cormorant | IBM Plex Sans | Google |
| Notebook Tabs | Bodoni Moda | DM Sans | Google |
| Pastel Geometry | Plus Jakarta Sans | Plus Jakarta Sans | Google |
| Split Pastel | Outfit | Outfit | Google |
| Vintage Editorial | Fraunces | Work Sans | Google |
| Neon Cyber | Clash Display | Satoshi | Fontshare |
| Terminal Green | JetBrains Mono | JetBrains Mono | JetBrains |

---

## 禁止使用（通用 AI 模式）

**字体：** Inter、Roboto、Arial、作为展示字体的系统字体

**颜色：** `#6366f1`（通用靛蓝）、白色背景上的紫色渐变

**布局：** 一切居中、通用主视觉区域、相同的卡片网格

**装饰：** 真实插画、无目的的玻璃态、无意义的投影

---

## CSS 陷阱

### 对 CSS 函数取反

**错误 — 浏览器静默忽略（无控制台错误）：**
```css
right: -clamp(28px, 3.5vw, 44px);   /* 浏览器忽略此行 */
margin-left: -min(10vw, 100px);      /* 浏览器忽略此行 */
```

**正确 — 用 `calc()` 包装：**
```css
right: calc(-1 * clamp(28px, 3.5vw, 44px));  /* 有效 */
margin-left: calc(-1 * min(10vw, 100px));     /* 有效 */
```

CSS 不允许函数名前有前导 `-`。浏览器会静默丢弃整个声明 — 无错误，元素只是出现在错误位置。**始终使用 `calc(-1 * ...)` 来对 CSS 函数值取反。**
