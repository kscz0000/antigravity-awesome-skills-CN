---
name: browser-automation
description: 浏览器自动化驱动 Web 测试、数据抓取和 AI 智能体交互。脆弱脚本与可靠系统之间的差距，取决于你对选择器、等待策略和反检测模式的理解。当用户要求'浏览器自动化'、'Playwright'、'Puppeteer'、'数据抓取'、'E2E测试'、'无头浏览器'时使用。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 浏览器自动化

浏览器自动化驱动 Web 测试、数据抓取和 AI 智能体交互。脆弱脚本与可靠系统之间的差距，取决于你对选择器、等待策略和反检测模式的理解。

本技能覆盖 Playwright（推荐）和 Puppeteer，提供测试、抓取和智能体浏览器控制的模式。核心判断：Playwright 已赢得框架之争。除非你需要 Puppeteer 的隐身生态或仅限 Chrome，否则 Playwright 是 2025 年的更好选择。

关键区分：测试自动化（你控制的可预测应用）vs 抓取/智能体自动化（会反击的不可预测网站）。不同问题，不同解法。

## 原则

- 使用面向用户的定位器（getByRole、getByText）而非 CSS/XPath
- 永远不要手动等待——Playwright 的自动等待机制会处理
- 每个测试/任务应在全新上下文中完全隔离
- 截图和 Trace 是你的调试生命线
- CI 用无头模式，调试用有头模式
- 反检测是猫鼠游戏——保持更新，否则会被封

## 能力

- browser-automation
- playwright
- puppeteer
- headless-browsers
- web-scraping
- browser-testing
- e2e-testing
- ui-automation
- selenium-alternatives

## 范围

- api-testing → backend
- load-testing → performance-thinker
- accessibility-testing → accessibility-specialist
- visual-regression-testing → ui-design

## 工具

### 框架

- Playwright - 何时用：默认选择——跨浏览器、自动等待、最佳开发体验 备注：96% 成功率，平均 4.5s 执行，微软出品
- Puppeteer - 何时用：仅 Chrome、需要隐身插件、已有代码库 备注：大规模下 75% 成功率，但隐身生态最佳
- Selenium - 何时用：遗留系统、特定语言绑定 备注：更慢、更冗长，但浏览器支持最广

### 隐身工具

- puppeteer-extra-plugin-stealth - 何时用：需要用 Puppeteer 绕过机器人检测 备注：反检测金标准
- playwright-extra - 何时用：Playwright 的隐身插件 备注：puppeteer-extra 生态的移植版
- undetected-chromedriver - 何时用：Selenium 反检测 备注：动态绕过检测

### 云浏览器

- Browserbase - 何时用：托管无头基础设施 备注：内置隐身模式、会话管理
- BrowserStack - 何时用：大规模跨浏览器测试 备注：真实设备、CI 集成

## 模式

### 测试隔离模式

每个测试在完全隔离的环境中运行，拥有全新状态

**何时用**：测试、任何需要可重复性的自动化

# TEST ISOLATION:

"""
每个测试获得独立的：
- 浏览器上下文（cookies、存储）
- 全新页面
- 干净状态
"""

## Playwright Test 示例
"""
import { test, expect } from '@playwright/test';

// 每个测试在隔离的浏览器上下文中运行
test('user can add item to cart', async ({ page }) => {
  // 全新上下文——没有其他测试的 cookies 和存储
  await page.goto('/products');
  await page.getByRole('button', { name: 'Add to Cart' }).click();
  await expect(page.getByTestId('cart-count')).toHaveText('1');
});

test('user can remove item from cart', async ({ page }) => {
  // 完全隔离——购物车为空
  await page.goto('/cart');
  await expect(page.getByText('Your cart is empty')).toBeVisible();
});
"""

## 共享认证模式
"""
// 保存一次认证状态，跨测试复用
// setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Sign in' }).click();

  // 等待认证完成
  await page.waitForURL('/dashboard');

  // 保存认证状态
  await page.context().storageState({
    path: './playwright/.auth/user.json'
  });
});

// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'tests',
      dependencies: ['setup'],
      use: {
        storageState: './playwright/.auth/user.json',
      },
    },
  ],
});
"""

### 面向用户的定位器模式

以用户视角选择元素

**何时用**：始终——选择器的默认方案

# USER-FACING LOCATORS:

"""
优先级顺序：
1. getByRole  - 最佳：匹配无障碍树
2. getByText  - 良好：匹配可见内容
3. getByLabel - 良好：匹配表单标签
4. getByTestId - 备选：显式测试契约
5. CSS/XPath - 最后手段：脆弱，避免使用
"""

## 正确示例（面向用户）
"""
// 按角色——最佳选择
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('link', { name: 'Sign up' }).click();
await page.getByRole('heading', { name: 'Dashboard' }).isVisible();
await page.getByRole('textbox', { name: 'Search' }).fill('query');

// 按文本内容
await page.getByText('Welcome back').isVisible();
await page.getByText(/Order #\d+/).click();  // 支持正则

// 按标签（表单）
await page.getByLabel('Email address').fill('user@example.com');
await page.getByLabel('Password').fill('secret');

// 按占位符
await page.getByPlaceholder('Search...').fill('query');

// 按 test ID（当没有面向用户的选项时）
await page.getByTestId('submit-button').click();
"""

## 错误示例（脆弱）
"""
// 不要——绑定结构的 CSS 选择器
await page.locator('.btn-primary.submit-form').click();
await page.locator('#header > div > button:nth-child(2)').click();

// 不要——绑定结构的 XPath
await page.locator('//div[@class="form"]/button[1]').click();

// 不要——自动生成的选择器
await page.locator('[data-v-12345]').click();
"""

## 过滤与链式调用
"""
// 按包含文本过滤
await page.getByRole('listitem')
  .filter({ hasText: 'Product A' })
  .getByRole('button', { name: 'Add to cart' })
  .click();

// 按不包含过滤
await page.getByRole('listitem')
  .filter({ hasNotText: 'Sold out' })
  .first()
  .click();

// 链式定位器
const row = page.getByRole('row', { name: 'John Doe' });
await row.getByRole('button', { name: 'Edit' }).click();
"""

### 自动等待模式

让 Playwright 自动等待，永远不要手动等待

**何时用**：使用 Playwright 时始终如此

# AUTO-WAIT PATTERN:

"""
Playwright 自动等待：
- 元素挂载到 DOM
- 元素可见
- 元素稳定（不在动画中）
- 元素可接收事件
- 元素已启用

永远不要手动等待！
"""

## 错误——手动等待
"""
// 不要这样做
await page.goto('/dashboard');
await page.waitForTimeout(2000);  // 不行！任意等待
await page.click('.submit-button');

// 不要这样做
await page.waitForSelector('.loading-spinner', { state: 'hidden' });
await page.waitForTimeout(500);  // "保险起见"——不行！
"""

## 正确——让自动等待生效
"""
// 自动等待按钮可点击
await page.getByRole('button', { name: 'Submit' }).click();

// 自动等待文本出现
await expect(page.getByText('Success!')).toBeVisible();

// 自动等待导航完成
await page.goto('/dashboard');
// 页面就绪——无需手动等待
"""

## 确实需要等待时
"""
// 等待特定网络请求
const responsePromise = page.waitForResponse(
  response => response.url().includes('/api/data')
);
await page.getByRole('button', { name: 'Load' }).click();
const response = await responsePromise;

// 等待 URL 变化
await Promise.all([
  page.waitForURL('**/dashboard'),
  page.getByRole('button', { name: 'Login' }).click(),
]);

// 等待下载
const downloadPromise = page.waitForEvent('download');
await page.getByText('Export CSV').click();
const download = await downloadPromise;
"""

### 隐身浏览器模式

绕过机器人检测进行抓取

**何时用**：抓取有反爬保护的网站

# STEALTH BROWSER PATTERN:

"""
机器人检测检查：
- navigator.webdriver 属性
- Chrome DevTools 协议痕迹
- 浏览器指纹不一致
- 行为模式（完美时序、无鼠标移动）
- 无头浏览器特征
"""

## Puppeteer Stealth（最佳反检测）
"""
import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';

puppeteer.use(StealthPlugin());

const browser = await puppeteer.launch({
  headless: 'new',
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-blink-features=AutomationControlled',
  ],
});

const page = await browser.newPage();

// 设置真实视口
await page.setViewport({ width: 1920, height: 1080 });

// 真实 User-Agent
await page.setUserAgent(
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
);

// 以类人行为导航
await page.goto('https://target-site.com', {
  waitUntil: 'networkidle0',
});
"""

## Playwright Stealth
"""
import { chromium } from 'playwright-extra';
import stealth from 'puppeteer-extra-plugin-stealth';

chromium.use(stealth());

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  userAgent: 'Mozilla/5.0 ...',
  locale: 'en-US',
  timezoneId: 'America/New_York',
});
"""

## 类人行为
"""
// 操作间随机延迟
const randomDelay = (min: number, max: number) =>
  new Promise(r => setTimeout(r, Math.random() * (max - min) + min));

await page.goto(url);
await randomDelay(500, 1500);

// 点击前移动鼠标
const button = await page.$('button.submit');
const box = await button.boundingBox();
await page.mouse.move(
  box.x + box.width / 2,
  box.y + box.height / 2,
  { steps: 10 }  // 像人一样分步移动
);
await randomDelay(100, 300);
await button.click();

// 自然滚动
await page.evaluate(() => {
  window.scrollBy({
    top: 300 + Math.random() * 200,
    behavior: 'smooth'
  });
});
"""

### 错误恢复模式

通过截图和重试优雅处理失败

**何时用**：任何生产自动化

# ERROR RECOVERY PATTERN:

## 失败时自动截图
"""
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
    video: 'retain-on-failure',
  },
  retries: 2,  // 重试失败测试
});
"""

## Try-Catch 带调试信息
"""
async function scrapeProduct(page: Page, url: string) {
  try {
    await page.goto(url, { timeout: 30000 });

    const title = await page.getByRole('heading', { level: 1 }).textContent();
    const price = await page.getByTestId('price').textContent();

    return { title, price, success: true };

  } catch (error) {
    // 捕获调试信息
    const screenshot = await page.screenshot({
      path: `errors/${Date.now()}-error.png`,
      fullPage: true
    });

    const html = await page.content();
    await fs.writeFile(`errors/${Date.now()}-page.html`, html);

    console.error({
      url,
      error: error.message,
      currentUrl: page.url(),
    });

    return { success: false, error: error.message };
  }
}
"""

## 指数退避重试
"""
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt < maxRetries - 1) {
        const delay = baseDelay * Math.pow(2, attempt);
        const jitter = delay * 0.1 * Math.random();
        await new Promise(r => setTimeout(r, delay + jitter));
      }
    }
  }

  throw lastError;
}

// 用法
const result = await withRetry(
  () => scrapeProduct(page, url),
  3,
  2000
);
"""

### 并行执行模式

并行运行测试/任务以提升速度

**何时用**：多个独立页面或测试

# PARALLEL EXECUTION:

## Playwright Test 并行化
"""
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: process.env.CI ? 4 : undefined,  // CI: 4 workers, 本地: 基于 CPU

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
"""

## 浏览器上下文并行抓取
"""
const browser = await chromium.launch();

const urls = ['url1', 'url2', 'url3', 'url4', 'url5'];

// 创建多个上下文——每个相互隔离
const results = await Promise.all(
  urls.map(async (url) => {
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
      await page.goto(url);
      const data = await extractData(page);
      return { url, data, success: true };
    } catch (error) {
      return { url, error: error.message, success: false };
    } finally {
      await context.close();
    }
  })
);

await browser.close();
"""

## 限速并行处理
"""
import pLimit from 'p-limit';

const limit = pLimit(5);  // 最多 5 个并发

const results = await Promise.all(
  urls.map(url => limit(async () => {
    const context = await browser.newContext();
    const page = await context.newPage();

    // 请求间随机延迟
    await new Promise(r => setTimeout(r, Math.random() * 2000));

    try {
      return await scrapePage(page, url);
    } finally {
      await context.close();
    }
  }))
);
"""

### 网络拦截模式

模拟、阻止或修改网络请求

**何时用**：测试、屏蔽广告/分析、修改响应

# NETWORK INTERCEPTION:

## 屏蔽不必要的资源
"""
await page.route('**/*', (route) => {
  const url = route.request().url();
  const resourceType = route.request().resourceType();

  // 屏蔽图片、字体、分析以加速抓取
  if (['image', 'font', 'media'].includes(resourceType)) {
    return route.abort();
  }

  // 屏蔽追踪/分析
  if (url.includes('google-analytics') ||
      url.includes('facebook.com/tr')) {
    return route.abort();
  }

  return route.continue();
});
"""

## 模拟 API 响应（测试）
"""
await page.route('**/api/products', async (route) => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([
      { id: 1, name: 'Mock Product', price: 99.99 },
    ]),
  });
});

// 页面将收到模拟数据
await page.goto('/products');
"""

## 捕获 API 响应
"""
const apiResponses: any[] = [];

page.on('response', async (response) => {
  if (response.url().includes('/api/')) {
    const data = await response.json().catch(() => null);
    apiResponses.push({
      url: response.url(),
      status: response.status(),
      data,
    });
  }
});

await page.goto('/dashboard');
// apiResponses 现在包含所有 API 调用
"""

## 常见陷阱

### 用 waitForTimeout 代替正确的等待

严重度：CRITICAL

场景：等待元素或页面状态

症状：
测试本地通过，CI 失败。9 次通过，第 10 次失败。
"Element not found"错误看似随机。测试耗时 30+ 秒，
实际只需 3 秒。

为何出错：
waitForTimeout 是固定延迟。页面 500ms 加载完，你仍然等
2000ms。页面需要 2100ms（CI 更慢），你就失败了。
不存在正确的值——总是太短或太长。

推荐修复：

# 删除所有 waitForTimeout 调用

# 错误：
await page.goto('/dashboard');
await page.waitForTimeout(2000);  # 任意等待！
await page.click('.submit');

# 正确——自动等待处理：
await page.goto('/dashboard');
await page.getByRole('button', { name: 'Submit' }).click();

# 如需等待特定条件：
await expect(page.getByText('Dashboard')).toBeVisible();
await page.waitForURL('**/dashboard');
await page.waitForResponse(resp => resp.url().includes('/api/data'));

# 对于动画，等待元素稳定：
await page.getByRole('button').click();  # 自动等待稳定

# 永远不要在生产代码中使用 setTimeout 或 waitForTimeout

### CSS 选择器绑定样式类

严重度：HIGH

场景：选择元素进行交互

症状：
CSS 重构后测试崩溃。.btn-primary 等选择器失效。
前端改版导致所有测试失败，但行为完全没变。

为何出错：
CSS 类名是样式的实现细节，不是语义含义。设计师把
.btn-primary 改成 .button--primary，你的测试就崩了，
尽管行为完全相同。

推荐修复：

# 改用面向用户的定位器：

# 错误——绑定 CSS：
await page.locator('.btn-primary.submit-form').click();
await page.locator('#sidebar > div.menu > ul > li:nth-child(3)').click();

# 正确——面向用户：
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('menuitem', { name: 'Settings' }).click();

# 如果必须用 CSS，使用 data-testid：
<button data-testid="submit-order">Submit</button>

await page.getByTestId('submit-order').click();

# 定位器优先级：
# 1. getByRole - 匹配无障碍树
# 2. getByText - 匹配可见内容
# 3. getByLabel - 匹配表单标签
# 4. getByTestId - 显式测试契约
# 5. CSS/XPath - 最后手段

### navigator.webdriver 暴露自动化

严重度：HIGH

场景：抓取有机器人检测的网站

症状：
立即 403 错误。CAPTCHA 验证。空白页面。"Access Denied"
消息。1 次请求成功，然后被封。

为何出错：
默认情况下，无头浏览器设置 navigator.webdriver = true。这是
机器人检测首先检查的内容。这是一个鲜红的标志，
写着"我是自动化程序"。

推荐修复：

# 使用隐身插件：

## Puppeteer Stealth（最佳选项）：
import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';

puppeteer.use(StealthPlugin());

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--disable-blink-features=AutomationControlled'],
});

## Playwright Stealth：
import { chromium } from 'playwright-extra';
import stealth from 'puppeteer-extra-plugin-stealth';

chromium.use(stealth());

## 手动（部分）：
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
  });
});

# 注意：这是猫鼠游戏。检测在进化。
# 严肃的抓取，考虑托管方案如 Browserbase。

### 测试共享状态互相影响

严重度：HIGH

场景：顺序运行多个测试

症状：
测试单独通过，一起运行就失败。顺序有关——
测试 A 先运行，测试 B 就失败。随机失败"重跑就好了"。

为何出错：
共享浏览器上下文意味着共享 cookies、localStorage 和会话
状态。测试 A 登录了，测试 B 期望未登录状态。测试 A 往
购物车加了商品，测试 B 的购物车数量不对。

推荐修复：

# 每个测试必须完全隔离：

## Playwright Test（自动隔离）：
test('first test', async ({ page }) => {
  // 全新上下文，全新页面
});

test('second test', async ({ page }) => {
  // 与第一个测试完全隔离
});

## 手动隔离：
const context = await browser.newContext();  // 全新上下文
const page = await context.newPage();
// ... 测试代码 ...
await context.close();  // 清理

## 共享认证（正确方式）：
// 1. 保存认证状态到文件
await context.storageState({ path: './auth.json' });

// 2. 在其他测试中复用
const context = await browser.newContext({
  storageState: './auth.json'
});

# 永远不要在测试中修改全局状态
# 永远不要依赖前一个测试的操作

### CI 失败无 Trace 记录

严重度：MEDIUM

场景：调试 CI 中的测试失败

症状：
"CI 测试失败"但没有有用信息。本地无法复现。
截图显示页面但看不出哪里出了问题。靠猜根因。

为何出错：
CI 在不同硬件上无头运行。时序不同。网络不同。
没有 Trace，你看不到实际发生了什么——
操作序列、网络请求、控制台日志。

推荐修复：

# 为失败启用 Trace：

## playwright.config.ts：
export default defineConfig({
  use: {
    trace: 'retain-on-failure',    # 失败时保留 Trace
    screenshot: 'only-on-failure', # 失败时截图
    video: 'retain-on-failure',    # 失败时录视频
  },
  outputDir: './test-results',
});

## 本地查看 Trace：
npx playwright show-trace test-results/path/to/trace.zip

## CI 中上传 test-results 作为制品：
# GitHub Actions：
- uses: actions/upload-artifact@v3
  if: failure()
  with:
    name: playwright-traces
    path: test-results/

# Trace 显示：
# - 操作时间线
# - 每步截图
# - 网络请求和响应
# - 控制台日志
# - DOM 快照

### 有头模式通过但无头模式失败

严重度：MEDIUM

场景：CI 中以无头模式运行测试

症状：
看着运行时完美。CI 中神秘失败。
无头模式"Element not visible"，有头模式可见。

为何出错：
无头浏览器没有显示器，这影响某些 CSS（可见性计算）、
视口大小和字体渲染。某些动画行为不同。弹窗可能不工作。

推荐修复：

# 设置一致的视口：
const browser = await chromium.launch({
  headless: true,
});

const context = await browser.newContext({
  viewport: { width: 1280, height: 720 },
});

# 或在配置中：
export default defineConfig({
  use: {
    viewport: { width: 1280, height: 720 },
  },
});

# 调试无头失败：
# 1. 本地以有头模式运行
npx playwright test --headed

# 2. 放慢速度观察
npx playwright test --headed --slowmo 100

# 3. 用 Trace 查看器分析 CI 失败
npx playwright show-trace trace.zip

# 4. 顽固问题，在失败点截图：
await page.screenshot({ path: 'debug.png', fullPage: true });

### 被速率限制封禁

严重度：HIGH

场景：快速抓取多个页面

症状：
前 50 页正常，然后 429 错误。突然所有请求失败。
IP 被封。成功请求后开始出现 CAPTCHA。

为何出错：
网站监控请求模式。一个 IP 每秒 100 个请求
明显是自动化。速率限制保护服务器并捕获爬虫。

推荐修复：

# 请求间添加延迟：

const randomDelay = () =>
  new Promise(r => setTimeout(r, 1000 + Math.random() * 2000));

for (const url of urls) {
  await randomDelay();  // 1-3 秒延迟
  await page.goto(url);
  // ... 抓取 ...
}

# 使用轮换代理：
const proxies = ['http://proxy1:8080', 'http://proxy2:8080'];
let proxyIndex = 0;

const getNextProxy = () => proxies[proxyIndex++ % proxies.length];

const context = await browser.newContext({
  proxy: { server: getNextProxy() },
});

# 限制并发请求：
import pLimit from 'p-limit';
const limit = pLimit(3);  // 最多 3 个并发

await Promise.all(
  urls.map(url => limit(() => scrapePage(url)))
);

# 轮换 User-Agent：
const userAgents = [
  'Mozilla/5.0 (Windows...',
  'Mozilla/5.0 (Macintosh...',
];

await page.setExtraHTTPHeaders({
  'User-Agent': userAgents[Math.floor(Math.random() * userAgents.length)]
});

### 新窗口/弹窗未处理

严重度：MEDIUM

场景：点击打开新窗口的链接

症状：
点击按钮，什么都没发生。测试挂起。"Window not found"错误。
操作成功但验证失败，因为你在错误的页面上。

为何出错：
target="_blank" 链接打开新窗口。你的 page 引用仍然
指向原始页面。新窗口存在但你没有监听它。

推荐修复：

# 在触发弹窗之前等待它：

## 新窗口/标签页：
const pagePromise = context.waitForEvent('page');
await page.getByRole('link', { name: 'Open in new tab' }).click();
const newPage = await pagePromise;
await newPage.waitForLoadState();

// 现在可以与新页面交互
await expect(newPage.getByRole('heading')).toBeVisible();

// 完成后关闭
await newPage.close();

## 弹出窗口：
const popupPromise = page.waitForEvent('popup');
await page.getByRole('button', { name: 'Open popup' }).click();
const popup = await popupPromise;
await popup.waitForLoadState();

## 多个窗口：
const pages = context.pages();  // 获取所有打开的页面

### 无法与 iframe 中的元素交互

严重度：MEDIUM

场景：页面包含嵌入的 iframe

症状：
元素明显可见但"not found"。选择器在 DevTools 中有效
但在 Playwright 中无效。父页面选择器有效，iframe 内容
无效。

为何出错：
iframe 是独立的文档。page.locator 只搜索主
框架。你需要显式获取 iframe 的 frame 才能与其
内容交互。

推荐修复：

# 按名称或选择器获取 frame：

## 按 frame 名称：
const frame = page.frame('payment-iframe');
await frame.getByRole('textbox', { name: 'Card number' }).fill('4242...');

## 按选择器：
const frame = page.frameLocator('iframe#payment');
await frame.getByRole('textbox', { name: 'Card number' }).fill('4242...');

## 嵌套 iframe：
const outer = page.frameLocator('iframe#outer');
const inner = outer.frameLocator('iframe#inner');
await inner.getByRole('button').click();

## 等待 iframe 加载：
await page.waitForSelector('iframe#payment');
const frame = page.frameLocator('iframe#payment');
await frame.getByText('Secure Payment').waitFor();

## 验证检查

### 使用 waitForTimeout

严重度：ERROR

waitForTimeout 导致测试不稳定且执行缓慢

消息：使用了 waitForTimeout——请移除。Playwright 自动等待元素。改用 waitForResponse、waitForURL 或断言。

### 测试代码中使用 setTimeout

严重度：WARNING

setTimeout 在测试中不可靠

消息：使用 setTimeout 而非 Playwright 等待。替换为 await expect(...).toBeVisible() 或 page.waitFor*。

### 自定义 Sleep 函数

严重度：WARNING

Sleep 函数表明等待策略不当

消息：检测到自定义 sleep 函数。改用 Playwright 内置等待机制。

### 使用 CSS 类选择器

严重度：WARNING

CSS 类选择器很脆弱

消息：使用了 CSS 类选择器。优先使用 getByRole、getByText、getByLabel 或 getByTestId 以获得更稳定的选择器。

### nth-child CSS 选择器

严重度：WARNING

基于位置的选择器非常脆弱

消息：使用了基于位置的选择器。DOM 顺序变化时这些会失效。改用面向用户的定位器。

### 使用 XPath 选择器

严重度：INFO

XPath 应作为最后手段

消息：使用了 XPath 选择器。优先考虑 getByRole、getByText。XPath 只应作为复杂 DOM 遍历的最后手段。

### 自动生成的选择器

严重度：WARNING

框架生成的选择器极其脆弱

消息：使用了自动生成的选择器。每次构建都会变化。改用 data-testid。

### Puppeteer 未使用隐身插件

严重度：INFO

无隐身抓取容易被检测

消息：Puppeteer 未使用隐身插件。考虑使用 puppeteer-extra-plugin-stealth 进行反检测。

### navigator.webdriver 未隐藏

严重度：INFO

navigator.webdriver 暴露自动化

消息：启动浏览器时未隐藏自动化标志。用于抓取时，请添加隐身措施。

### 抓取循环无错误处理

严重度：WARNING

一个失败不应导致整个抓取崩溃

消息：抓取循环没有 try/catch。一个页面失败会导致整个抓取崩溃。请添加错误处理。

## 协作

### 委派触发

- 用户需要浏览器之外的完整桌面控制 -> computer-use-agents（非浏览器应用的桌面自动化）
- 用户需要浏览器测试之外的 API 测试 -> backend（API 集成和测试模式）
- 用户需要测试策略 -> test-architect（整体测试架构决策）
- 用户需要视觉回归测试 -> ui-design（视觉比较和设计验证）
- 用户需要工作流中的浏览器自动化 -> workflow-automation（浏览器任务的持久执行）
- 用户为智能体构建浏览器工具 -> agent-tool-builder（LLM 智能体的工具设计模式）

## 相关技能

配合使用：`agent-tool-builder`、`workflow-automation`、`computer-use-agents`、`test-architect`

## 何时使用
- 用户提及或暗示：playwright
- 用户提及或暗示：puppeteer
- 用户提及或暗示：浏览器自动化
- 用户提及或暗示：无头浏览器
- 用户提及或暗示：网页抓取
- 用户提及或暗示：e2e 测试
- 用户提及或暗示：端到端
- 用户提及或暗示：selenium
- 用户提及或暗示：chromium
- 用户提及或暗示：浏览器测试
- 用户提及或暗示：page.click
- 用户提及或暗示：定位器

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
