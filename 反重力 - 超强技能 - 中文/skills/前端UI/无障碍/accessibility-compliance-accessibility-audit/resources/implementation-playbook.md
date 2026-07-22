# 无障碍审计与测试实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## 说明

### 1. 使用 axe-core 进行自动化测试

```javascript
// accessibility-test.js
const { AxePuppeteer } = require("@axe-core/puppeteer");
const puppeteer = require("puppeteer");

class AccessibilityAuditor {
  constructor(options = {}) {
    this.wcagLevel = options.wcagLevel || "AA";
    this.viewport = options.viewport || { width: 1920, height: 1080 };
  }

  async runFullAudit(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport(this.viewport);
    await page.goto(url, { waitUntil: "networkidle2" });

    const results = await new AxePuppeteer(page)
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .exclude(".no-a11y-check")
      .analyze();

    await browser.close();

    return {
      url,
      timestamp: new Date().toISOString(),
      violations: results.violations.map((v) => ({
        id: v.id,
        impact: v.impact,
        description: v.description,
        help: v.help,
        helpUrl: v.helpUrl,
        nodes: v.nodes.map((n) => ({
          html: n.html,
          target: n.target,
          failureSummary: n.failureSummary,
        })),
      })),
      score: this.calculateScore(results),
    };
  }

  calculateScore(results) {
    const weights = { critical: 10, serious: 5, moderate: 2, minor: 1 };
    let totalWeight = 0;
    results.violations.forEach((v) => {
      totalWeight += weights[v.impact] || 0;
    });
    return Math.max(0, 100 - totalWeight);
  }
}

// 使用 jest-axe 进行组件测试
import { render } from "@testing-library/react";
import { axe, toHaveNoViolations } from "jest-axe";

expect.extend(toHaveNoViolations);

describe("Accessibility Tests", () => {
  it("should have no violations", async () => {
    const { container } = render(<MyComponent />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### 2. 颜色对比度验证

```javascript
// color-contrast.js
class ColorContrastAnalyzer {
    constructor() {
        this.wcagLevels = {
            'AA': { normal: 4.5, large: 3 },
            'AAA': { normal: 7, large: 4.5 }
        };
    }

    async analyzePageContrast(page) {
        const elements = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('*'))
                .filter(el => el.innerText && el.innerText.trim())
                .map(el => {
                    const styles = window.getComputedStyle(el);
                    return {
                        text: el.innerText.trim().substring(0, 50),
                        color: styles.color,
                        backgroundColor: styles.backgroundColor,
                        fontSize: parseFloat(styles.fontSize),
                        fontWeight: styles.fontWeight
                    };
                });
        });

        return elements
            .map(el => {
                const contrast = this.calculateContrast(el.color, el.backgroundColor);
                const isLarge = this.isLargeText(el.fontSize, el.fontWeight);
                const required = isLarge ? this.wcagLevels.AA.large : this.wcagLevels.AA.normal;

                if (contrast < required) {
                    return {
                        text: el.text,
                        currentContrast: contrast.toFixed(2),
                        requiredContrast: required,
                        foreground: el.color,
                        background: el.backgroundColor
                    };
                }
                return null;
            })
            .filter(Boolean);
    }

    calculateContrast(fg, bg) {
        const l1 = this.relativeLuminance(this.parseColor(fg));
        const l2 = this.relativeLuminance(this.parseColor(bg));
        const lighter = Math.max(l1, l2);
        const darker = Math.min(l1, l2);
        return (lighter + 0.05) / (darker + 0.05);
    }

    relativeLuminance(rgb) {
        const [r, g, b] = rgb.map(val => {
            val = val / 255;
            return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }
}

// 高对比度 CSS
@media (prefers-contrast: high) {
    :root {
        --text-primary: #000;
        --bg-primary: #fff;
        --border-color: #000;
    }
    a { text-decoration: underline !important; }
    button, input { border: 2px solid var(--border-color) !important; }
}
```

### 3. 键盘导航测试

```javascript
// keyboard-navigation.js
class KeyboardNavigationTester {
  async testKeyboardNavigation(page) {
    const results = {
      focusableElements: [],
      missingFocusIndicators: [],
      keyboardTraps: [],
    };

    // 获取所有可聚焦元素
    const focusable = await page.evaluate(() => {
      const selector =
        'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])';
      return Array.from(document.querySelectorAll(selector)).map((el) => ({
        tagName: el.tagName.toLowerCase(),
        text: el.innerText || el.value || el.placeholder || "",
        tabIndex: el.tabIndex,
      }));
    });

    results.focusableElements = focusable;

    // 测试 Tab 顺序和焦点指示器
    for (let i = 0; i < focusable.length; i++) {
      await page.keyboard.press("Tab");

      const focused = await page.evaluate(() => {
        const el = document.activeElement;
        return {
          tagName: el.tagName.toLowerCase(),
          hasFocusIndicator: window.getComputedStyle(el).outline !== "none",
        };
      });

      if (!focused.hasFocusIndicator) {
        results.missingFocusIndicators.push(focused);
      }
    }

    return results;
  }
}

// 增强键盘无障碍性
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const modal = document.querySelector(".modal.open");
    if (modal) closeModal(modal);
  }
});

// 使可点击的 div 具有无障碍性
document.querySelectorAll("[onclick]").forEach((el) => {
  if (!["a", "button", "input"].includes(el.tagName.toLowerCase())) {
    el.setAttribute("tabindex", "0");
    el.setAttribute("role", "button");
    el.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        el.click();
        e.preventDefault();
      }
    });
  }
});
```

### 4. 屏幕阅读器测试

```javascript
// screen-reader-test.js
class ScreenReaderTester {
  async testScreenReaderCompatibility(page) {
    return {
      landmarks: await this.testLandmarks(page),
      headings: await this.testHeadingStructure(page),
      images: await this.testImageAccessibility(page),
      forms: await this.testFormAccessibility(page),
    };
  }

  async testHeadingStructure(page) {
    const headings = await page.evaluate(() => {
      return Array.from(
        document.querySelectorAll("h1, h2, h3, h4, h5, h6"),
      ).map((h) => ({
        level: parseInt(h.tagName[1]),
        text: h.textContent.trim(),
        isEmpty: !h.textContent.trim(),
      }));
    });

    const issues = [];
    let previousLevel = 0;

    headings.forEach((heading, index) => {
      if (heading.level > previousLevel + 1 && previousLevel !== 0) {
        issues.push({
          type: "skipped-level",
          message: `Heading level ${heading.level} skips from level ${previousLevel}`,
        });
      }
      if (heading.isEmpty) {
        issues.push({ type: "empty-heading", index });
      }
      previousLevel = heading.level;
    });

    if (!headings.some((h) => h.level === 1)) {
      issues.push({ type: "missing-h1", message: "Page missing h1 element" });
    }

    return { headings, issues };
  }

  async testFormAccessibility(page) {
    const forms = await page.evaluate(() => {
      return Array.from(document.querySelectorAll("form")).map((form) => {
        const inputs = form.querySelectorAll("input, textarea, select");
        return {
          fields: Array.from(inputs).map((input) => ({
            type: input.type || input.tagName.toLowerCase(),
            id: input.id,
            hasLabel: input.id
              ? !!document.querySelector(`label[for="${input.id}"]`)
              : !!input.closest("label"),
            hasAriaLabel: !!input.getAttribute("aria-label"),
            required: input.required,
          })),
        };
      });
    });

    const issues = [];
    forms.forEach((form, i) => {
      form.fields.forEach((field, j) => {
        if (!field.hasLabel && !field.hasAriaLabel) {
          issues.push({ type: "missing-label", form: i, field: j });
        }
      });
    });

    return { forms, issues };
  }
}

// ARIA 模式
const ariaPatterns = {
  modal: `
<div role="dialog" aria-labelledby="modal-title" aria-modal="true">
    <h2 id="modal-title">Modal Title</h2>
    <button aria-label="Close">×</button>
</div>`,

  tabs: `
<div role="tablist" aria-label="Navigation">
    <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">Content</div>`,

  form: `
<label for="name">Name <span aria-label="required">*</span></label>
<input id="name" required aria-required="true" aria-describedby="name-error">
<span id="name-error" role="alert" aria-live="polite"></span>`,
};
```

### 5. 人工测试检查清单

```markdown
## 人工无障碍测试

### 键盘导航

- [ ] 所有交互元素可通过 Tab 访问
- [ ] 按钮可通过 Enter/Space 激活
- [ ] Esc 键关闭模态框
- [ ] 焦点指示器始终可见
- [ ] 无键盘陷阱
- [ ] Tab 顺序符合逻辑

### 屏幕阅读器

- [ ] 页面标题具有描述性
- [ ] 标题创建逻辑大纲
- [ ] 图片具有替代文本
- [ ] 表单字段具有标签
- [ ] 错误消息被朗读
- [ ] 动态更新被朗读

### 视觉

- [ ] 文本可放大至 200% 而不丢失内容
- [ ] 颜色不是传递信息的唯一方式
- [ ] 焦点指示器具有足够的对比度
- [ ] 内容在 320px 宽度下可重排
- [ ] 动画可暂停

### 认知

- [ ] 说明清晰简洁
- [ ] 错误消息有帮助
- [ ] 表单无时间限制
- [ ] 导航一致
- [ ] 重要操作可撤销
```

### 6. 修复示例

```javascript
// 修复缺失的替代文本
document.querySelectorAll("img:not([alt])").forEach((img) => {
  const isDecorative =
    img.role === "presentation" || img.closest('[role="presentation"]');
  img.setAttribute("alt", isDecorative ? "" : img.title || "Image");
});

// 修复缺失的标签
document
  .querySelectorAll("input:not([aria-label]):not([id])")
  .forEach((input) => {
    if (input.placeholder) {
      input.setAttribute("aria-label", input.placeholder);
    }
  });

// React 无障碍组件
const AccessibleButton = ({ children, onClick, ariaLabel, ...props }) => (
  <button onClick={onClick} aria-label={ariaLabel} {...props}>
    {children}
  </button>
);

const LiveRegion = ({ message, politeness = "polite" }) => (
  <div
    role="status"
    aria-live={politeness}
    aria-atomic="true"
    className="sr-only"
  >
    {message}
  </div>
);
```

### 7. CI/CD 集成

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Tests

on: [push, pull_request]

jobs:
  a11y-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install and build
        run: |
          npm ci
          npm run build

      - name: Start server
        run: |
          npm start &
          npx wait-on http://localhost:3000

      - name: Run axe tests
        run: npm run test:a11y

      - name: Run pa11y
        run: npx pa11y http://localhost:3000 --standard WCAG2AA --threshold 0

      - name: Upload report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: a11y-report
          path: a11y-report.html
```

### 8. 报告生成

```javascript
// report-generator.js
class AccessibilityReportGenerator {
  generateHTMLReport(auditResults) {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Accessibility Audit</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .summary { background: #f0f0f0; padding: 20px; border-radius: 8px; }
        .score { font-size: 48px; font-weight: bold; }
        .violation { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .critical { border-color: #f00; background: #fee; }
        .serious { border-color: #fa0; background: #ffe; }
    </style>
</head>
<body>
    <h1>Accessibility Audit Report</h1>
    <p>Generated: ${new Date().toLocaleString()}</p>

    <div class="summary">
        <h2>Summary</h2>
        <div class="score">${auditResults.score}/100</div>
        <p>Total Violations: ${auditResults.violations.length}</p>
    </div>

    <h2>Violations</h2>
    ${auditResults.violations
      .map(
        (v) => `
        <div class="violation ${v.impact}">
            <h3>${v.help}</h3>
            <p><strong>Impact:</strong> ${v.impact}</p>
            <p>${v.description}</p>
            <a href="${v.helpUrl}">Learn more</a>
        </div>
    `,
      )
      .join("")}
</body>
</html>`;
  }
}
```

## 输出格式

1. **无障碍评分**：WCAG 各级别的整体合规性
2. **违规报告**：详细问题及其严重程度和修复方法
3. **测试结果**：自动化和人工测试结果
4. **修复指南**：每个问题的分步修复方法
5. **代码示例**：无障碍组件实现

专注于创建对所有用户都具有包容性的体验，无论其能力或辅助技术如何。
