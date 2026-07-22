---
name: puppeteer-skill
description: '生成 Puppeteer 脚本，用于浏览器自动化、数据抓取和 PDF 生成。触发词："Puppeteer"、"headless Chrome"、"page.goto"、"scrape"、"PDF 生成"。'
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/puppeteer-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Puppeteer 自动化技能
## 何时使用

当你需要生成 Puppeteer 脚本以实现浏览器自动化、数据抓取和 PDF 生成时使用此技能。触发词："Puppeteer"、"headless Chrome"、"page.goto"、"scrape"、"PDF 生成"。


## 核心模式

### 基础脚本

```javascript
const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });

    await page.goto('https://example.com', { waitUntil: 'networkidle0' });
    await page.type('#username', 'user@test.com');
    await page.type('#password', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle0' });

    const title = await page.title();
    console.log('Title:', title);

    await browser.close();
})();
```

### 等待策略

```javascript
// Wait for selector
await page.waitForSelector('.result', { visible: true, timeout: 10000 });

// Wait for navigation
await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle0' }),
    page.click('a.nav-link'),
]);

// Wait for function
await page.waitForFunction('document.querySelector(".count").innerText === "5"');

// Wait for network request
const response = await page.waitForResponse(resp =>
    resp.url().includes('/api/data') && resp.status() === 200
);
```

### 截图与 PDF

```javascript
await page.screenshot({ path: 'screenshot.png', fullPage: true });
await page.pdf({ path: 'page.pdf', format: 'A4', printBackground: true });
```

### 网络拦截

```javascript
await page.setRequestInterception(true);
page.on('request', request => {
    if (request.resourceType() === 'image') request.abort();
    else request.continue();
});

// Mock API
page.on('request', request => {
    if (request.url().includes('/api/data')) {
        request.respond({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({ items: [] }),
        });
    } else request.continue();
});
```

### TestMu AI 云端

完整配置、功能和共享能力参考，请参阅 [reference/cloud-integration.md](https://github.com/LambdaTest/agent-skills/tree/main/puppeteer-skill/reference/cloud-integration.md)。

```javascript
const capabilities = {
    browserName: 'Chrome', browserVersion: 'latest',
    'LT:Options': {
        platform: 'Windows 11', build: 'Puppeteer Build',
        user: process.env.LT_USERNAME, accessKey: process.env.LT_ACCESS_KEY,
    },
};

const browser = await puppeteer.connect({
    browserWSEndpoint: `wss://cdp.lambdatest.com/puppeteer?capabilities=${encodeURIComponent(JSON.stringify(capabilities))}`,
});
```

## 快速参考

| 任务 | 代码 |
|------|------|
| 有头模式启动 | `puppeteer.launch({ headless: false })` |
| 执行 JS | `await page.evaluate(() => document.title)` |
| 提取文本 | `await page.$eval('.el', el => el.textContent)` |
| 提取全部 | `await page.$$eval('.items', els => els.map(e => e.textContent))` |
| 设置 Cookie | `await page.setCookie({ name: 'token', value: 'abc' })` |
| 模拟设备 | `await page.emulate(puppeteer.devices['iPhone 12'])` |

## 深入模式 → `reference/playbook.md`

| § | 章节 | 内容 |
|---|------|------|
| 1 | 生产环境配置 | 启动选项、Jest 集成 |
| 2 | 页面对象模式 | BasePage、LoginPage、DashboardPage |
| 3 | 网络拦截与模拟 | 请求模拟、响应捕获 |
| 4 | 等待策略 | DOM、网络、自定义条件 |
| 5 | 截图、PDF 与媒体 | 全页面、裁剪、PDF、视频 |
| 6 | 认证与 Cookie | API 登录、会话保存/恢复 |
| 7 | iFrame、对话框与文件操作 | 上传、下载、对话框 |
| 8 | 性能与指标 | Web Vitals、Lighthouse、覆盖率 |
| 9 | 无障碍测试 | axe-core 集成 |
| 10 | CI/CD 集成 | GitHub Actions、Docker |
| 11 | 调试快速参考 | 11 个常见问题 |
| 12 | 最佳实践清单 | 13 项 |

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时才使用此技能。
- 在应用变更前，请验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 请勿将示例视为环境特定测试、安全审查或用户审批（针对破坏性或高成本操作）的替代方案。
