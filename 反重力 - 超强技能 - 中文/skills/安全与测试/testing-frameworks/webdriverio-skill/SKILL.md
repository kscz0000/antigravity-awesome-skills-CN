---
name: webdriverio-skill
description: '生成 JavaScript 或 TypeScript 的 WebdriverIO（WDIO）自动化测试，支持本地与 TestMu AI 云端。涉及 "WebdriverIO"、"WDIO"、"wdio.conf"、"browser.url"、"$"、"$$" 时触发。触发词："WebdriverIO"、"WDIO"、"wdio"、"browser.$"。'
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/webdriverio-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# WebdriverIO 自动化技能
## 适用场景

生成 JavaScript 或 TypeScript 的 WebdriverIO（WDIO）自动化测试时使用本技能，支持本地与 TestMu AI 云端。当用户问题中涉及 "WebdriverIO"、"WDIO"、"wdio.conf"、"browser.url"、"$"、"$$" 等关键字时会触发本技能。触发词主要包括："WebdriverIO"、"WDIO"、"wdio"、"browser.$" 等。本技能适用于常见的浏览器自动化、跨浏览器端到端测试、页面对象建模以及云端并行执行等场景。


## 步骤 1 — 执行目标

本技能默认在本机本地执行 WebdriverIO 自动化测试（即在用户本机启动浏览器驱动并运行测试用例）。若用户提及 "cloud"、"TestMu"、"LambdaTest" 等关键字，则切换为通过 WDIO LambdaTest 服务将测试推向云端执行。

## 步骤 2 — 框架

根据用户问题中提到的关键字选择合适的测试运行器（Runner）框架，默认使用 Mocha。

| 信号 | Runner |
|--------|--------|
| 默认 | Mocha |
| "Jasmine" | Jasmine |
| "Cucumber"、"BDD" | Cucumber |

## 核心模式

下面整理了 WebdriverIO 最常用的核心模式与代码片段，分别覆盖选择器、基础测试、页面对象、云端配置与等待策略，按需取用即可。

### 选择器

推荐优先使用稳定选择器（如 `data-testid`、ARIA、文本匹配等）以减少页面样式变更带来的脆弱性。

```javascript
// ✅ Preferred
await $('[data-testid="submit"]').click();
await $('aria/Submit').click();
await $('button=Submit').click(); // text-based

// Chaining
await $('form').$('input[name="email"]').setValue('test@test.com');

// Multiple elements
const items = await $$('.list-item');
```

### 基础测试（Mocha）

下面是一个基于 Mocha 的标准登录测试用例示例：

```javascript
describe('Login', () => {
    it('should login successfully', async () => {
        await browser.url('/login');
        await $('[data-testid="email"]').setValue('user@test.com');
        await $('[data-testid="password"]').setValue('password123');
        await $('[data-testid="submit"]').click();
        await expect(browser).toHaveUrl(expect.stringContaining('/dashboard'));
    });
});
```

### 页面对象

使用页面对象（Page Object）模式将页面元素与业务操作封装到独立类中，便于复用与维护：

```javascript
class LoginPage {
    get inputEmail() { return $('[data-testid="email"]'); }
    get inputPassword() { return $('[data-testid="password"]'); }
    get btnSubmit() { return $('[data-testid="submit"]'); }

    async login(email, password) {
        await this.inputEmail.setValue(email);
        await this.inputPassword.setValue(password);
        await this.btnSubmit.click();
    }
}
module.exports = new LoginPage();
```

### TestMu AI 云端配置

切换到云端执行时，需要在 `wdio.conf.js` 中配置 LambdaTest 账号与能力项：

```javascript
// wdio.conf.js
exports.config = {
    user: process.env.LT_USERNAME,
    key: process.env.LT_ACCESS_KEY,
    hostname: 'hub.lambdatest.com',
    port: 80,
    path: '/wd/hub',
    services: ['lambdatest'],
    capabilities: [{
        browserName: 'Chrome',
        browserVersion: 'latest',
        'LT:Options': {
            platform: 'Windows 11',
            build: 'WDIO Build',
            name: 'WDIO Test',
            video: true,
            network: true,
        }
    }],
};
```

### 等待策略

在涉及异步页面或网络请求时，应使用显式等待（而非固定 sleep）以提升稳定性：

```javascript
// Wait for element
await $('[data-testid="result"]').waitForDisplayed({ timeout: 10000 });

// Wait for condition
await browser.waitUntil(
    async () => (await $('[data-testid="count"]').getText()) === '5',
    { timeout: 10000, timeoutMsg: 'Count did not reach 5' }
);
```

## 速查表

| 任务 | 命令 |
|------|---------|
| 项目初始化（一条命令即可完成） | `npm init wdio@latest` |
| 运行全部测试 | `npx wdio run wdio.conf.js` |
| 运行指定测试文件 | `npx wdio run wdio.conf.js --spec ./test/login.js` |
| 运行指定套件 | `npx wdio run wdio.conf.js --suite smoke` |
| 并发并行执行 | 在 wdio.conf.js 配置中设置 `maxInstances: 5` |
| 测试失败时自动截图 | `await browser.saveScreenshot('./screenshot.png')` |

## 参考文件

下列参考文件包含本技能的详细补充内容，请按需查阅。

| 文件 | 何时阅读 |
|------|-------------|
| `reference/cloud-integration.md` | 当需要了解 LambdaTest 服务接入、并行执行、能力配置等内容时阅读 |
| `reference/advanced-patterns.md` | 当需要了解自定义命令、报告器、服务扩展等进阶用法时阅读 |

## 深度模式（更详细的进阶用法请参考）→ `reference/playbook.md`

下面列出 playbook 手册中包含的深度章节（共 13 节），按需查阅：

| § | 章节 | 内容覆盖 |
|---|---------|-------|
| 1 | 生产环境配置 | 多环境、多浏览器配置 |
| 2 | 页面对象模型 | BasePage、LoginPage、DashboardPage |
| 3 | 自定义命令 | 浏览器 + 元素命令、TypeScript |
| 4 | 网络拦截 | DevTools 拦截、中止、错误模拟 |
| 5 | 文件操作 | 上传、下载、拖放 |
| 6 | 多标签页、iFrame 与 Shadow DOM | 窗口句柄、嵌套 Shadow |
| 7 | 视觉回归 | 图像比对服务 |
| 8 | API 测试 | 基于 Fetch、API + UI 联合 |
| 9 | 移动测试 | Appium 服务集成 |
| 10 | LambdaTest 集成 | 云端网格配置 |
| 11 | CI/CD 集成 | GitHub Actions、Docker Compose |
| 12 | 调试速查 | 涵盖 11 个常见问题的速查解答 |
| 13 | 最佳实践清单 | 共 14 项最佳实践的检查清单 |

## 局限性

使用本技能前请注意以下局限性与风险边界：

- 仅在任务与上游来源及本地项目上下文明确匹配时使用本技能；不要在与之无关的测试场景中强行套用。
- 在应用变更前，请核对命令、生成代码、依赖、凭证以及外部服务行为，避免引入未预期的副作用。
- 示例不能替代面向特定环境的测试、安全审查，也不能替代用户对破坏性或高成本操作的批准。
