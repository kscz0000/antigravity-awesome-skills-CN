# Stitch 高级技巧

最大化 Stitch 能力、创建生产级设计的高级策略。

## 目录

1. [图片转 UI 工作流](#image-to-ui-workflows)
2. [设计系统集成](#design-system-integration)
3. [响应式设计策略](#responsive-design-strategies)
4. [无障碍设计考量](#accessibility-considerations)
5. [性能优化](#performance-optimization)
6. [组件复用](#component-reusability)

---

## Image-to-UI Workflows

### 将草图转为数字 UI

Stitch 能够解读手绘草图、线框图和粗略原型。

**最佳实践：**

1. **结构清晰** - 为组件画出明确的方框
2. **标注元素** - 注释按钮、输入框、区块
3. **体现层级** - 用大小和位置表示重要程度
4. **附加说明** - 添加描述交互或状态的文本

**工作流示例：**
```
1. Sketch wireframe on paper or tablet
2. Take clear photo or scan
3. Upload to Stitch with prompt:
   "Convert this wireframe to a modern web interface with 
   glassmorphic design and purple gradient accents"
4. Refine generated design with annotations
```

### 基于参考的设计

上传现有设计的截图，创建具有你自己品牌风格的类似布局。

**提示词结构：**
```
Create a [type] similar to this reference image, but with:
- [Your color scheme]
- [Your content/copy]
- [Your brand style]
- [Specific modifications]
```

**示例：**
```
Create a pricing page similar to this reference, but with:
- Navy blue and gold color scheme
- 4 pricing tiers instead of 3
- Annual/monthly toggle
- Feature comparison table below
- Testimonials section at bottom
```

---

## Design System Integration

### 建立设计令牌

在初始提示词中定义可复用的设计令牌，确保跨屏幕的一致性。

**令牌类别：**
- 颜色（主色、辅色、强调色、中性色、语义色）
- 字体（字族、字号、字重、行高）
- 间距（比例尺：4px、8px、16px、24px、32px、48px、64px）
- 圆角（无、sm、md、lg、full）
- 阴影（层级高度）

**示例提示词：**
```
Dashboard using this design system:

Colors:
- Primary: #2563EB (blue)
- Secondary: #7C3AED (purple)
- Success: #10B981 (green)
- Warning: #F59E0B (amber)
- Error: #EF4444 (red)
- Neutral: #6B7280 (gray)

Typography:
- Headings: Inter Bold
- Body: Inter Regular
- Code: JetBrains Mono

Spacing: 8px base unit
Border radius: 8px for cards, 4px for buttons
Shadows: Subtle elevation with 0 4px 6px rgba(0,0,0,0.1)
```

### 组件库方法

先生成独立组件，再组合成完整屏幕，构建组件库。

**工作流：**
```
1. Generate base components:
   - Button variants (primary, secondary, outline, ghost)
   - Input fields (text, email, password, search)
   - Cards (basic, with image, with actions)
   - Navigation (header, sidebar, tabs)

2. Document component specs:
   - States (default, hover, active, disabled)
   - Sizes (sm, md, lg)
   - Variants

3. Compose screens using established components:
   "Create a settings page using the button and input 
   components from previous generations"
```

---

## Responsive Design Strategies

### 移动端优先方法

从移动端设计开始，再扩展到平板和桌面。

**提示词序列：**

**步骤 1 - 手机（375px）：**
```
Mobile app home screen for recipe platform

Layout:
- Stacked vertical sections
- Full-width cards
- Bottom navigation
- Hamburger menu

Content:
- Search bar at top
- Featured recipe hero card
- Category chips (horizontal scroll)
- Recipe grid (1 column)
```

**步骤 2 - 平板（768px）：**
```
Adapt the mobile recipe home screen for tablet:
- 2-column recipe grid
- Persistent sidebar navigation (replaces hamburger)
- Larger featured hero with side-by-side layout
- Category chips remain scrollable
```

**步骤 3 - 桌面（1440px）：**
```
Adapt for desktop:
- 3-column recipe grid
- Full sidebar with categories expanded
- Hero section with 3 featured recipes
- Top navigation bar with search and user menu
```

### 断点专属提示词

指定精确的断点和布局变化。

**示例：**
```
Responsive product grid:

Mobile (< 640px):
- 1 column
- Full-width cards
- Vertical image orientation

Tablet (640px - 1024px):
- 2 columns
- Square images
- Compact card layout

Desktop (> 1024px):
- 4 columns
- Hover effects with overlay
- Quick view button
```

---

## Accessibility Considerations

### WCAG 合规提示词

在提示词中直接包含无障碍要求。

**需要指定的关键领域：**

1. **颜色对比度**
```
Ensure all text meets WCAG AA standards:
- Normal text: 4.5:1 contrast ratio minimum
- Large text (18pt+): 3:1 contrast ratio minimum
- Interactive elements: clear focus states with 3:1 contrast
```

2. **触控目标**
```
All interactive elements minimum 44x44px touch target size
Adequate spacing between clickable elements (8px minimum)
```

3. **键盘导航**
```
Clear focus indicators on all interactive elements
Logical tab order following visual flow
Skip navigation link for keyboard users
```

4. **屏幕阅读器支持**
```
Descriptive button labels (not just "Click here")
Alt text for all meaningful images
Form labels properly associated with inputs
Heading hierarchy (H1 → H2 → H3)
```

**综合无障碍提示词：**
```
Create an accessible contact form:

Fields:
- Name (required, with aria-required)
- Email (required, with validation and error message)
- Subject (dropdown with clear labels)
- Message (textarea with character count)

Accessibility features:
- All inputs have visible labels
- Required fields marked with asterisk and aria-required
- Error messages with role="alert"
- Submit button with descriptive text
- Focus indicators with 3px blue outline
- Color contrast meets WCAG AA
- Touch targets 44x44px minimum

Style: Clean, form-focused, high contrast
Colors: Dark text on light background, red for errors
```

### 包容性设计模式

**考虑多样化用户：**

```
Design a video player interface that supports:
- Captions/subtitles toggle
- Audio description option
- Keyboard shortcuts (space to play/pause, arrows to seek)
- Playback speed control
- High contrast mode
- Reduced motion option (disable animations)
```

---

## Performance Optimization

### 性能优化提示词

从一开始就请求注重性能的设计。

**图片优化：**
```
E-commerce product gallery with performance optimization:
- Lazy loading for images below fold
- Thumbnail images (200x200px) for grid
- Full-size images (1200x1200px) only on click
- WebP format with JPEG fallback
- Blur placeholder while loading
```

**代码效率：**
```
Generate lightweight HTML/CSS without:
- Unnecessary wrapper divs
- Inline styles (use classes)
- Large external dependencies
- Redundant CSS rules
```

### 渐进增强

先为核心功能设计，再逐步增强。

**示例：**
```
Create a filterable product list with progressive enhancement:

Base (no JavaScript):
- Server-rendered product grid
- Form-based filters with submit button
- Pagination links

Enhanced (with JavaScript):
- AJAX filter updates without page reload
- Infinite scroll
- Smooth animations
- Real-time search
```

---

## Component Reusability

### 原子设计方法论

从原子 → 分子 → 有机体 → 模板 → 页面逐层构建。

**原子（基础元素）：**
```
Generate design system atoms:
- Button (primary, secondary, outline, ghost, danger)
- Input field (text, email, password, search, textarea)
- Label, Badge, Tag
- Icon set (24x24px, consistent style)
- Avatar (circle, square, with status indicator)
```

**分子（简单组合）：**
```
Create molecules using atoms:
- Search bar (input + button + icon)
- Form field (label + input + error message)
- Card header (avatar + name + timestamp + menu)
- Stat card (icon + label + value + trend)
```

**有机体（复杂组件）：**
```
Build organisms from molecules:
- Navigation bar (logo + search bar + user menu)
- Product card (image + title + price + rating + button)
- Comment thread (avatar + name + timestamp + text + actions)
- Data table (headers + rows + pagination + filters)
```

**模板（页面布局）：**
```
Compose templates from organisms:
- Dashboard layout (sidebar + header + content grid)
- Article layout (header + hero + content + sidebar)
- Checkout flow (progress + form + summary)
```

### 变体生成

创建组件的系统化变体。

**按钮变体提示词：**
```
Generate button component with all variants:

Sizes: Small (32px), Medium (40px), Large (48px)

Types:
- Primary (filled, brand color)
- Secondary (filled, gray)
- Outline (border only)
- Ghost (transparent, hover background)
- Danger (filled, red)

States for each:
- Default
- Hover
- Active (pressed)
- Disabled
- Loading (with spinner)

Include: Icon support (left/right), full-width option
```

---

## Advanced Iteration Techniques

### 条件变体

根据不同条件生成多个版本。

**示例：**
```
Create 3 hero section variants for A/B testing:

Variant A - Image-focused:
- Large background image
- Minimal text overlay
- Single CTA button

Variant B - Text-focused:
- Solid color background
- Detailed copy with bullet points
- Two CTA buttons (primary + secondary)

Variant C - Video-focused:
- Background video
- Minimal text
- Play button + CTA

All variants use same brand colors and maintain mobile responsiveness
```

### 基于状态的设计

为所有可能的状态设计，而不仅仅是理想路径。

**综合状态提示词：**
```
Design a data table with all states:

Default state:
- 10 rows of data
- Sortable columns
- Pagination

Loading state:
- Skeleton loaders for rows
- Disabled controls

Empty state:
- Illustration
- "No data found" message
- "Add new" CTA button

Error state:
- Error icon
- Error message
- "Retry" button

Search/Filter active:
- Applied filters shown as chips
- Clear filters option
- Result count

Selected rows:
- Checkbox selection
- Bulk action toolbar
- Select all option
```

---

## Export and Handoff Best Practices

### 为开发做准备

导出前，确保设计已为开发做好准备。

**导出前检查清单：**

1. **命名规范**
   - 使用语义化类名
   - 遵循 BEM 或一致的方法论
   - 清晰命名组件

2. **文档**
   - 为复杂交互添加注释
   - 记录响应式断点
   - 标注所需的 JavaScript 行为

3. **资源组织**
   - 以正确尺寸导出图片
   - 提供 SVG 格式的图标
   - 包含字体文件或 CDN 链接

4. **规范说明**
   - 记录间距值
   - 列出颜色十六进制码
   - 指定字号和字重

### Figma 集成

优化 Stitch → Figma 工作流。

**步骤：**
```
1. Generate design in Stitch with detailed specifications
2. Use "Paste to Figma" export
3. In Figma:
   - Organize layers with clear naming
   - Create components from repeated elements
   - Set up auto-layout for responsive behavior
   - Define color and text styles
   - Add design system documentation
4. Share with developers using Figma's inspect mode
```

### 代码导出精修

改进导出的 HTML/CSS 以符合生产标准。

**导出后任务：**

1. **语义化 HTML**
   - 用语义标签替换 div（header、nav、main、article、section、footer）
   - 在需要处添加 ARIA 标签
   - 确保正确的标题层级

2. **CSS 优化**
   - 将重复样式提取为工具类
   - 使用 CSS 自定义属性存储主题值
   - 按方法论组织（BEM、SMACSS 等）
   - 添加缺失的响应式媒体查询

3. **无障碍**
   - 为图片添加 alt 文本
   - 确保表单标签正确关联
   - 添加焦点样式
   - 用屏幕阅读器测试

4. **性能**
   - 优化图片
   - 压缩 CSS
   - 移除未使用的样式
   - 添加加载策略

---

## 总结

这些高级技巧帮助你超越 Stitch 的基础用法，创建生产级、无障碍且高性能的设计。将这些策略与核心提示词原则结合，最大化你的效率和输出质量。

**关键要点：**
- 用图片和参考加速设计
- 尽早建立设计系统以保持一致性
- 从一开始就做响应式设计
- 在每个提示词中优先考虑无障碍
- 以可复用组件的思维思考
- 为所有状态做规划，不仅仅是理想路径
- 导出后先精修再用于生产
