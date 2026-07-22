---
name: smartui-skill
description: 生成 SmartUI 视觉回归测试配置，用于 TestMu AI 云端截图对比。框架无关 — 支持 Playwright、Selenium、Cypress、Puppeteer。当用户提到"SmartUI"、"视觉回归"、"截图对比"、"视觉测试"时使用。触发词：...
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/smartui-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# SmartUI Visual Regression Skill
## 何时使用

当你需要为 TestMu AI 云端截图对比生成 SmartUI 视觉回归测试配置时使用此技能。框架无关 — 支持 Playwright、Selenium、Cypress、Puppeteer。当用户提到"SmartUI"、"视觉回归"、"截图对比"、"视觉测试"时使用。触发词：...


## 核心模式

### Playwright + SmartUI SDK

```javascript
const { chromium } = require('playwright');
const { smartuiSnapshot } = require('@lambdatest/smartui-cli');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('https://example.com');
  await smartuiSnapshot(page, 'Homepage');

  await page.goto('https://example.com/login');
  await smartuiSnapshot(page, 'Login Page');

  await browser.close();
})();
```

### Selenium + SmartUI

```java
// Take SmartUI screenshot
((JavascriptExecutor) driver).executeScript(
    "smartui.takeScreenshot=Login Page"
);
```

### CLI 执行

```bash
# Install
npm install @lambdatest/smartui-cli --save-dev

# Configure
npx smartui config:create smartui.config.json

# Execute
npx smartui exec -- node test.js
# or with Playwright
npx smartui exec -- npx playwright test
```

### smartui.config.json

```json
{
  "web": {
    "browsers": ["chrome", "firefox", "safari"],
    "viewports": [[1920, 1080], [1366, 768], [375, 812]]
  },
  "waitForPageRender": 5000,
  "waitForTimeout": 1000
}
```

### SmartUI 与 Storybook

```bash
npx smartui storybook http://localhost:6006 --config smartui.config.json
```

### 审批工作流

1. 首次运行创建基线截图
2. 后续运行与基线进行对比
3. 差异在控制台中高亮显示
4. 在 LambdaTest SmartUI 控制台中审批/驳回变更
5. 已审批的截图成为新基线

### 反模式

| 错误做法 | 正确做法 | 原因 |
|-----|------|-----|
| 不配置视口 | 多视口配置 | 响应式问题 |
| 不等待渲染 | `waitForPageRender` | 截图不完整 |
| 截取所有页面 | 仅截取关键页面/组件 | 减少噪音 |
| 无审批流程 | 在控制台中审查差异 | 捕捉回归 |

### 云端认证

设置环境变量：

```bash
export PROJECT_TOKEN="your-smartui-project-token"   # From SmartUI dashboard
export LT_USERNAME="your-username"                   # For Selenium/Playwright cloud
export LT_ACCESS_KEY="your-access-key"               # For Selenium/Playwright cloud
```

**CLI 方式**（使用 `PROJECT_TOKEN`）：
```bash
npx smartui exec -- npx playwright test
```

**Selenium 云端方式**（使用 `LT_USERNAME`/`LT_ACCESS_KEY`）：
```java
// Capabilities include SmartUI options
HashMap<String, Object> ltOptions = new HashMap<>();
ltOptions.put("user", System.getenv("LT_USERNAME"));
ltOptions.put("accessKey", System.getenv("LT_ACCESS_KEY"));
ltOptions.put("build", "SmartUI Build");
ltOptions.put("smartUI.project", "My SmartUI Project");
ChromeOptions options = new ChromeOptions();
options.setCapability("LT:Options", ltOptions);
WebDriver driver = new RemoteWebDriver(
    new URL("https://hub.lambdatest.com/wd/hub"), options);
```

## 快速参考

| 任务 | 命令 |
|------|------|
| 安装 | `npm install @lambdatest/smartui-cli` |
| 初始化配置 | `npx smartui config:create smartui.config.json` |
| 运行 | `npx smartui exec -- <test command>` |
| Storybook | `npx smartui storybook <url>` |
| 控制台 | `https://smartui.lambdatest.com` |

## 深入模式

高级模式、调试指南、CI/CD 集成和最佳实践，参见 `reference/playbook.md`。

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更前，请先验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查或用户对破坏性或高成本操作的审批。
