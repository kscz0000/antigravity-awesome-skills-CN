# WCAG 审计模式实施手册

本文件包含本技能所引用的详细模式、检查清单和代码示例。

## 核心概念

### 1. WCAG 一致性等级

| 等级   | 说明             | 适用场景       |
| ------ | ---------------- | -------------- |
| **A**   | 最低无障碍要求 | 法律底线       |
| **AA**  | 标准一致性     | 大多数法规     |
| **AAA** | 增强无障碍     | 特殊需求场景 |

### 2. POUR 原则

```
Perceivable:  Can users perceive the content?
Operable:     Can users operate the interface?
Understandable: Can users understand the content?
Robust:       Does it work with assistive tech?
```

### 3. 按影响分类的常见违规

```
Critical (Blockers):
├── Missing alt text for functional images
├── No keyboard access to interactive elements
├── Missing form labels
└── Auto-playing media without controls

Serious:
├── Insufficient color contrast
├── Missing skip links
├── Inaccessible custom widgets
└── Missing page titles

Moderate:
├── Missing language attribute
├── Unclear link text
├── Missing landmarks
└── Improper heading hierarchy
```

## 审计检查清单

### 可感知（原则 1）

````markdown
## 1.1 文本替代

### 1.1.1 非文本内容（Level A）

- [ ] 所有图片都有 alt 文本
- [ ] 装饰性图片使用 alt=""
- [ ] 复杂图片具有长描述
- [ ] 带有语义的图标具有可访问名称
- [ ] CAPTCHA 验证码提供替代方案

检查：

```html
<!-- Good -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2" />
<img src="decorative-line.png" alt="" />

<!-- Bad -->
<img src="chart.png" />
<img src="decorative-line.png" alt="decorative line" />
```
````

## 1.2 基于时间的媒体

### 1.2.1 纯音频与纯视频（Level A）

- [ ] 音频具有文字转录
- [ ] 视频具有音频描述或文字转录

### 1.2.2 字幕（Level A）

- [ ] 所有视频都有同步字幕
- [ ] 字幕准确完整
- [ ] 包含说话人身份标识

### 1.2.3 音频描述（Level A）

- [ ] 视频具有针对视觉内容的音频描述

## 1.3 可适配

### 1.3.1 信息与关系（Level A）

- [ ] 标题使用合适的标签（h1-h6）
- [ ] 列表使用 ul/ol/dl
- [ ] 表格包含表头
- [ ] 表单输入框具有标签
- [ ] 存在 ARIA 地标

检查：

```html
<!-- Heading hierarchy -->
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
<h2>Another Section</h2>

<!-- Table headers -->
<table>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Price</th>
    </tr>
  </thead>
</table>
```

### 1.3.2 有意义的顺序（Level A）

- [ ] 阅读顺序符合逻辑
- [ ] CSS 定位不会破坏顺序
- [ ] 焦点顺序匹配视觉顺序

### 1.3.3 感官特征（Level A）

- [ ] 指示说明不单独依赖形状或颜色
- [ ] "Click the red button" → "Click Submit (red button)"

## 1.4 可区分

### 1.4.1 颜色的使用（Level A）

- [ ] 颜色不是传达信息的唯一方式
- [ ] 不依赖颜色即可区分链接
- [ ] 错误状态不仅以颜色呈现

### 1.4.3 最小对比度（Level AA）

- [ ] 文本对比度 4.5:1
- [ ] 大字号（18pt+）对比度 3:1
- [ ] UI 组件对比度 3:1

工具：WebAIM Contrast Checker、axe DevTools

### 1.4.4 文本缩放（Level AA）

- [ ] 文本可缩放至 200% 而不丢失信息
- [ ] 在 320px 下不出现水平滚动
- [ ] 内容正确回流

### 1.4.10 重排（Level AA）

- [ ] 在 400% 缩放下内容可重排
- [ ] 不出现二维滚动
- [ ] 在 320px 宽度下所有内容均可访问

### 1.4.11 非文本对比度（Level AA）

- [ ] UI 组件具有 3:1 对比度
- [ ] 焦点指示器可见
- [ ] 图形对象可区分

### 1.4.12 文本间距（Level AA）

- [ ] 增加间距不导致内容丢失
- [ ] 行高为字号 1.5 倍
- [ ] 段落间距为字号 2 倍
- [ ] 字间距为字号 0.12 倍
- [ ] 词间距为字号 0.16 倍

````

### 可操作（原则 2）

```markdown
## 2.1 键盘可访问

### 2.1.1 键盘（Level A）
- [ ] 所有功能均支持键盘操作
- [ ] 不存在键盘陷阱
- [ ] Tab 顺序符合逻辑
- [ ] 自定义控件可键盘操作

检查：
```javascript
// Custom button must be keyboard accessible
<div role="button" tabindex="0"
     onkeydown="if(event.key === 'Enter' || event.key === ' ') activate()">
````

### 2.1.2 无键盘陷阱（Level A）

- [ ] 焦点可从所有组件移出
- [ ] 模态对话框正确限制焦点
- [ ] 模态关闭后焦点恢复

## 2.2 充足时间

### 2.2.1 可调整时间限制（Level A）

- [ ] 会话超时可延长
- [ ] 用户在超时前收到警告
- [ ] 可禁用自动刷新

### 2.2.2 暂停、停止、隐藏（Level A）

- [ ] 移动内容可暂停
- [ ] 自动更新内容可暂停
- [ ] 动画遵守 prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## 2.3 癫痫与生理反应

### 2.3.1 三次闪烁（Level A）

- [ ] 内容每秒闪烁不超过 3 次
- [ ] 闪烁区域较小（小于视口的 25%）

## 2.4 可导航

### 2.4.1 绕过块（Level A）

- [ ] 提供"跳转到主内容"链接
- [ ] 定义地标区域
- [ ] 标题结构合理

```html
<a href="#main" class="skip-link">Skip to main content</a>
<main id="main">...</main>
```

### 2.4.2 页面标题（Level A）

- [ ] 页面标题唯一且具有描述性
- [ ] 标题反映页面内容

### 2.4.3 焦点顺序（Level A）

- [ ] 焦点顺序匹配视觉顺序
- [ ] tabindex 使用正确

### 2.4.4 链接目的（情境下）（Level A）

- [ ] 链接脱离上下文也能理解
- [ ] 不单独使用 "click here" 或 "read more"

```html
<!-- Bad -->
<a href="report.pdf">Click here</a>

<!-- Good -->
<a href="report.pdf">Download Q4 Sales Report (PDF)</a>
```

### 2.4.6 标题与标签（Level AA）

- [ ] 标题描述内容
- [ ] 标签描述用途

### 2.4.7 焦点可见（Level AA）

- [ ] 所有元素均显示焦点指示
- [ ] 自定义焦点样式满足对比度

```css
:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}
```

### 2.4.11 焦点不被遮挡（Level AA） - WCAG 2.2

- [ ] 聚焦元素未被完全隐藏
- [ ] 粘性页头不遮挡焦点

````

### 可理解（原则 3）

```markdown
## 3.1 可读

### 3.1.1 页面语言（Level A）
- [ ] HTML lang 属性已设置
- [ ] 语言与内容匹配

```html
<html lang="en">
````

### 3.1.2 段落语言（Level AA）

- [ ] 语言变化处已标记

```html
<p>The French word <span lang="fr">bonjour</span> means hello.</p>
```

## 3.2 可预测

### 3.2.1 获得焦点时（Level A）

- [ ] 仅获得焦点时不会改变上下文
- [ ] 获得焦点时不会意外弹出

### 3.2.2 输入时（Level A）

- [ ] 不会自动提交表单
- [ ] 上下文变化前提醒用户

### 3.2.3 一致的导航（Level AA）

- [ ] 跨页面导航保持一致
- [ ] 重复组件顺序相同

### 3.2.4 一致的标识（Level AA）

- [ ] 相同功能使用相同标签
- [ ] 图标使用一致

## 3.3 输入辅助

### 3.3.1 错误标识（Level A）

- [ ] 错误被清晰标识
- [ ] 错误消息描述问题
- [ ] 错误关联到字段

```html
<input aria-describedby="email-error" aria-invalid="true" />
<span id="email-error" role="alert">Please enter valid email</span>
```

### 3.3.2 标签或说明（Level A）

- [ ] 所有输入框具有可见标签
- [ ] 必填字段已标识
- [ ] 提供格式提示

### 3.3.3 错误建议（Level AA）

- [ ] 错误包含修正建议
- [ ] 建议具体明确

### 3.3.4 错误预防（Level AA）

- [ ] 法律/金融表单可撤销
- [ ] 提交前进行数据校验
- [ ] 用户可在提交前复核

````

### 健壮（原则 4）

```markdown
## 4.1 兼容

### 4.1.1 解析（Level A） - WCAG 2.2 中已废弃
- [ ] HTML 合法（良好实践）
- [ ] 不存在重复 ID
- [ ] 起止标签完整

### 4.1.2 名称、角色、值（Level A）
- [ ] 自定义控件具有可访问名称
- [ ] ARIA 角色正确
- [ ] 状态变化被播报

```html
<!-- Accessible custom checkbox -->
<div role="checkbox"
     aria-checked="false"
     tabindex="0"
     aria-labelledby="label">
</div>
<span id="label">Accept terms</span>
````

### 4.1.3 状态消息（Level AA）

- [ ] 状态更新被播报
- [ ] 正确使用 live regions

```html
<div role="status" aria-live="polite">3 items added to cart</div>

<div role="alert" aria-live="assertive">Error: Form submission failed</div>
```

````

## 自动化测试

```javascript
// axe-core integration
const axe = require('axe-core');

async function runAccessibilityAudit(page) {
  await page.addScriptTag({ path: require.resolve('axe-core') });

  const results = await page.evaluate(async () => {
    return await axe.run(document, {
      runOnly: {
        type: 'tag',
        values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']
      }
    });
  });

  return {
    violations: results.violations,
    passes: results.passes,
    incomplete: results.incomplete
  };
}

// Playwright test example
test('should have no accessibility violations', async ({ page }) => {
  await page.goto('/');
  const results = await runAccessibilityAudit(page);

  expect(results.violations).toHaveLength(0);
});
````

```bash
# CLI tools
npx @axe-core/cli https://example.com
npx pa11y https://example.com
lighthouse https://example.com --only-categories=accessibility
```

## 修复模式

### 修复：缺失的表单标签

```html
<!-- Before -->
<input type="email" placeholder="Email" />

<!-- After: Option 1 - Visible label -->
<label for="email">Email address</label>
<input id="email" type="email" />

<!-- After: Option 2 - aria-label -->
<input type="email" aria-label="Email address" />

<!-- After: Option 3 - aria-labelledby -->
<span id="email-label">Email</span>
<input type="email" aria-labelledby="email-label" />
```

### 修复：对比度不足

```css
/* Before: 2.5:1 contrast */
.text {
  color: #767676;
}

/* After: 4.5:1 contrast */
.text {
  color: #595959;
}

/* Or add background */
.text {
  color: #767676;
  background: #000;
}
```

### 修复：键盘导航

```javascript
// Make custom element keyboard accessible
class AccessibleDropdown extends HTMLElement {
  connectedCallback() {
    this.setAttribute("tabindex", "0");
    this.setAttribute("role", "combobox");
    this.setAttribute("aria-expanded", "false");

    this.addEventListener("keydown", (e) => {
      switch (e.key) {
        case "Enter":
        case " ":
          this.toggle();
          e.preventDefault();
          break;
        case "Escape":
          this.close();
          break;
        case "ArrowDown":
          this.focusNext();
          e.preventDefault();
          break;
        case "ArrowUp":
          this.focusPrevious();
          e.preventDefault();
          break;
      }
    });
  }
}
```

## 最佳实践

### 推荐做法

- **尽早开始** - 在设计阶段就考虑无障碍
- **邀请真实用户测试** - 残障用户能提供最佳反馈
- **能自动化的就自动化** - 30-50% 的问题可被检测到
- **使用语义化 HTML** - 减少对 ARIA 的需求
- **沉淀模式** - 构建无障碍组件库

### 不推荐做法

- **不要仅依赖自动化测试** - 仍需人工测试
- **不要把 ARIA 作为首选** - 优先使用原生 HTML
- **不要隐藏焦点轮廓** - 键盘用户需要它们
- **不要禁用缩放** - 用户需要调整大小
- **不要单独使用颜色** - 需要多种指示

## 资源

- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
- [WebAIM](https://webaim.org/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [axe DevTools](https://www.deque.com/axe/)
