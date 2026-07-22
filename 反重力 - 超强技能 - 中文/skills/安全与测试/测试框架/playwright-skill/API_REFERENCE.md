# Playwright 技能 - 完整 API 参考

本文档包含完整的 Playwright API 参考和高级模式。快速入门执行模式请参见 [SKILL.md](SKILL.md)。

## 目录

- [安装与设置](#安装与设置)
- [核心模式](#核心模式)
- [选择器与定位器](#选择器与定位器)
- [常用操作](#常用操作)
- [等待策略](#等待策略)
- [断言](#断言)
- [页面对象模型](#页面对象模型-pom)
- [网络与 API 测试](#网络与-api-测试)
- [认证与会话管理](#认证与会话管理)
- [视觉测试](#视觉测试)
- [移动端测试](#移动端测试)
- [调试](#调试)
- [性能测试](#性能测试)
- [并行执行](#并行执行)
- [数据驱动测试](#数据驱动测试)
- [无障碍测试](#无障碍测试)
- [CI/CD 集成](#cicd-集成)
- [最佳实践](#最佳实践)
- [常用模式与解决方案](#常用模式与解决方案)
- [故障排除](#故障排除)

## 安装与设置

### 前提条件

使用此技能前，请确保 Playwright 可用：

```bash
# 检查 Playwright 是否已安装
npm list playwright 2>/dev/null || echo "Playwright not installed"

# 安装（如需要）
cd ~/.claude/skills/playwright-skill
npm run setup
```

### 基本配置

创建 `playwright.config.ts`：

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## 核心模式

### 基本浏览器自动化

```javascript
const { chromium } = require('playwright');

(async () => {
  // 启动浏览器
  const browser = await chromium.launch({
    headless: false,  // 设为 true 启用无头模式
    slowMo: 50       // 操作减慢 50ms
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
  });

  const page = await context.newPage();

  // 导航
  await page.goto('https://example.com', {
    waitUntil: 'networkidle'  // 等待网络空闲
  });

  // 在此编写你的自动化代码

  await browser.close();
})();
```

### 测试结构

```typescript
import { test, expect } from '@playwright/test';

test.describe('功能名称', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('应该执行某操作', async ({ page }) => {
    // 准备
    const button = page.locator('button[data-testid="submit"]');

    // 执行
    await button.click();

    // 断言
    await expect(page).toHaveURL('/success');
    await expect(page.locator('.message')).toHaveText('Success!');
  });
});
```

## 选择器与定位器

### 选择器最佳实践

```javascript
// 推荐：数据属性（最稳定）
await page.locator('[data-testid="submit-button"]').click();
await page.locator('[data-cy="user-input"]').fill('text');

// 良好：基于角色的选择器（无障碍）
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
await page.getByRole('heading', { level: 1 }).click();

// 良好：文本内容（用于唯一文本）
await page.getByText('Sign in').click();
await page.getByText(/welcome back/i).click();

// 可接受：语义化 HTML
await page.locator('button[type="submit"]').click();
await page.locator('input[name="email"]').fill('test@test.com');

// 避免：类名和 ID（可能频繁变化）
await page.locator('.btn-primary').click();  // 避免
await page.locator('#submit').click();       // 避免

// 最后手段：复杂 CSS/XPath
await page.locator('div.container > form > button').click();  // 脆弱
```

### 高级定位器模式

```javascript
// 过滤和链式定位器
const row = page.locator('tr').filter({ hasText: 'John Doe' });
await row.locator('button').click();

// 第 N 个元素
await page.locator('button').nth(2).click();

// 组合条件
await page.locator('button').and(page.locator('[disabled]')).count();

// 父子导航
const cell = page.locator('td').filter({ hasText: 'Active' });
const row = cell.locator('..');
await row.locator('button.edit').click();
```

## 常用操作

### 表单交互

```javascript
// 文本输入
await page.getByLabel('Email').fill('user@example.com');
await page.getByPlaceholder('Enter your name').fill('John Doe');

// 清空并输入
await page.locator('#username').clear();
await page.locator('#username').type('newuser', { delay: 100 });

// 复选框
await page.getByLabel('I agree').check();
await page.getByLabel('Subscribe').uncheck();

// 单选按钮
await page.getByLabel('Option 2').check();

// 下拉选择
await page.selectOption('select#country', 'usa');
await page.selectOption('select#country', { label: 'United States' });
await page.selectOption('select#country', { index: 2 });

// 多选
await page.selectOption('select#colors', ['red', 'blue', 'green']);

// 文件上传
await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');
await page.setInputFiles('input[type="file"]', [
  'file1.pdf',
  'file2.pdf'
]);
```

### 鼠标操作

```javascript
// 点击变体
await page.click('button');                          // 左键点击
await page.click('button', { button: 'right' });    // 右键点击
await page.dblclick('button');                       // 双击
await page.click('button', { position: { x: 10, y: 10 } });  // 指定位置点击

// 悬停
await page.hover('.menu-item');

// 拖放
await page.dragAndDrop('#source', '#target');

// 手动拖拽
await page.locator('#source').hover();
await page.mouse.down();
await page.locator('#target').hover();
await page.mouse.up();
```

### 键盘操作

```javascript
// 带延迟输入
await page.keyboard.type('Hello World', { delay: 100 });

// 组合键
await page.keyboard.press('Control+A');
await page.keyboard.press('Control+C');
await page.keyboard.press('Control+V');

// 特殊键
await page.keyboard.press('Enter');
await page.keyboard.press('Tab');
await page.keyboard.press('Escape');
await page.keyboard.press('ArrowDown');
```

## 等待策略

### 智能等待

```javascript
// 等待元素状态
await page.locator('button').waitFor({ state: 'visible' });
await page.locator('.spinner').waitFor({ state: 'hidden' });
await page.locator('button').waitFor({ state: 'attached' });
await page.locator('button').waitFor({ state: 'detached' });

// 等待特定条件
await page.waitForURL('**/success');
await page.waitForURL(url => url.pathname === '/dashboard');

// 等待网络
await page.waitForLoadState('networkidle');
await page.waitForLoadState('domcontentloaded');

// 等待函数
await page.waitForFunction(() => document.querySelector('.loaded'));
await page.waitForFunction(
  text => document.body.innerText.includes(text),
  'Content loaded'
);

// 等待响应
const responsePromise = page.waitForResponse('**/api/users');
await page.click('button#load-users');
const response = await responsePromise;

// 等待请求
await page.waitForRequest(request =>
  request.url().includes('/api/') && request.method() === 'POST'
);

// 自定义超时
await page.locator('.slow-element').waitFor({
  state: 'visible',
  timeout: 10000  // 10 秒
});
```

## 断言

### 常用断言

```javascript
import { expect } from '@playwright/test';

// 页面断言
await expect(page).toHaveTitle('My App');
await expect(page).toHaveURL('https://example.com/dashboard');
await expect(page).toHaveURL(/.*dashboard/);

// 元素可见性
await expect(page.locator('.message')).toBeVisible();
await expect(page.locator('.spinner')).toBeHidden();
await expect(page.locator('button')).toBeEnabled();
await expect(page.locator('input')).toBeDisabled();

// 文本内容
await expect(page.locator('h1')).toHaveText('Welcome');
await expect(page.locator('.message')).toContainText('success');
await expect(page.locator('.items')).toHaveText(['Item 1', 'Item 2']);

// 输入值
await expect(page.locator('input')).toHaveValue('test@example.com');
await expect(page.locator('input')).toBeEmpty();

// 属性
await expect(page.locator('button')).toHaveAttribute('type', 'submit');
await expect(page.locator('img')).toHaveAttribute('src', /.*\.png/);

// CSS 属性
await expect(page.locator('.error')).toHaveCSS('color', 'rgb(255, 0, 0)');

// 数量
await expect(page.locator('.item')).toHaveCount(5);

// 复选框/单选按钮状态
await expect(page.locator('input[type="checkbox"]')).toBeChecked();
```

## 页面对象模型 (POM)

### 基本页面对象

```javascript
// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.usernameInput = page.locator('input[name="username"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('.error-message');
  }

  async navigate() {
    await this.page.goto('/login');
  }

  async login(username, password) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }
}

// 在测试中使用
test('使用有效凭据登录', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

## 网络与 API 测试

### 拦截请求

```javascript
// 模拟 API 响应
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' }
    ])
  });
});

// 修改请求
await page.route('**/api/**', route => {
  const headers = {
    ...route.request().headers(),
    'X-Custom-Header': 'value'
  };
  route.continue({ headers });
});

// 阻止资源
await page.route('**/*.{png,jpg,jpeg,gif}', route => route.abort());
```

### 通过环境变量自定义请求头

此技能支持通过环境变量自动注入请求头：

```bash
# 单个请求头（简单）
PW_HEADER_NAME=X-Automated-By PW_HEADER_VALUE=playwright-skill

# 多个请求头（JSON）
PW_EXTRA_HEADERS='{"X-Automated-By":"playwright-skill","X-Request-ID":"123"}'
```

使用以下方式时，这些请求头会自动应用到所有请求：
- `helpers.createContext(browser)` - 自动合并请求头
- `getContextOptionsWithHeaders(options)` - 由 run.js 包装器注入的工具函数

**优先级（从高到低）：**
1. 在 `options.extraHTTPHeaders` 中直接传递的请求头
2. 环境变量请求头
3. Playwright 默认值

**用例：** 识别自动化流量，使后端可以返回 LLM 优化的响应（例如纯文本错误而非带样式的 HTML）。

## 视觉测试

### 截图

```javascript
// 全页截图
await page.screenshot({
  path: 'screenshot.png',
  fullPage: true
});

// 元素截图
await page.locator('.chart').screenshot({
  path: 'chart.png'
});

// 视觉对比
await expect(page).toHaveScreenshot('homepage.png');
```

## 移动端测试

```javascript
// 设备模拟
const { devices } = require('playwright');
const iPhone = devices['iPhone 12'];

const context = await browser.newContext({
  ...iPhone,
  locale: 'en-US',
  permissions: ['geolocation'],
  geolocation: { latitude: 37.7749, longitude: -122.4194 }
});
```

## 调试

### 调试模式

```bash
# 使用检查器运行
npx playwright test --debug

# 有头模式
npx playwright test --headed

# 慢动作
npx playwright test --headed --slowmo=1000
```

### 代码内调试

```javascript
// 暂停执行
await page.pause();

// 控制台日志
page.on('console', msg => console.log('Browser log:', msg.text()));
page.on('pageerror', error => console.log('Page error:', error));
```

## 性能测试

```javascript
// 测量页面加载时间
const startTime = Date.now();
await page.goto('https://example.com');
const loadTime = Date.now() - startTime;
console.log(`Page loaded in ${loadTime}ms`);
```

## 并行执行

```javascript
// 并行运行测试
test.describe.parallel('并行测试套件', () => {
  test('测试 1', async ({ page }) => {
    // 与测试 2 并行运行
  });

  test('测试 2', async ({ page }) => {
    // 与测试 1 并行运行
  });
});
```

## 数据驱动测试

```javascript
// 参数化测试
const testData = [
  { username: 'user1', password: 'pass1', expected: 'Welcome user1' },
  { username: 'user2', password: 'pass2', expected: 'Welcome user2' },
];

testData.forEach(({ username, password, expected }) => {
  test(`使用 ${username} 登录`, async ({ page }) => {
    await page.goto('/login');
    await page.fill('#username', username);
    await page.fill('#password', password);
    await page.click('button[type="submit"]');
    await expect(page.locator('.message')).toHaveText(expected);
  });
});
```

## 无障碍测试

```javascript
import { injectAxe, checkA11y } from 'axe-playwright';

test('无障碍检查', async ({ page }) => {
  await page.goto('/');
  await injectAxe(page);
  await checkA11y(page);
});
```

## CI/CD 集成

### GitHub Actions

```yaml
name: Playwright Tests
on:
  push:
    branches: [main, master]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps
      - name: Run tests
        run: npx playwright test
```

## 最佳实践

1. **测试组织** - 使用描述性测试名称，分组相关测试
2. **选择器策略** - 优先使用 data-testid 属性，使用基于角色的选择器
3. **等待** - 使用 Playwright 的自动等待，避免硬编码延迟
4. **错误处理** - 添加适当的错误消息，失败时截图
5. **性能** - 并行运行测试，复用认证状态

## 常用模式与解决方案

### 处理弹窗

```javascript
const [popup] = await Promise.all([
  page.waitForEvent('popup'),
  page.click('button.open-popup')
]);
await popup.waitForLoadState();
```

### 文件下载

```javascript
const [download] = await Promise.all([
  page.waitForEvent('download'),
  page.click('button.download')
]);
await download.saveAs(`./downloads/${download.suggestedFilename()}`);
```

### iFrame

```javascript
const frame = page.frameLocator('#my-iframe');
await frame.locator('button').click();
```

### 无限滚动

```javascript
async function scrollToBottom(page) {
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(500);
}
```

## 故障排除

### 常见问题

1. **找不到元素** - 检查元素是否在 iframe 中，验证可见性
2. **超时错误** - 增加超时时间，检查网络条件
3. **不稳定测试** - 使用正确的等待策略，模拟外部依赖
4. **认证问题** - 验证认证状态是否正确保存

## 快速参考命令

```bash
# 运行测试
npx playwright test

# 有头模式运行
npx playwright test --headed

# 调试测试
npx playwright test --debug

# 生成代码
npx playwright codegen https://example.com

# 查看报告
npx playwright show-report
```

## 其他资源

- [Playwright 文档](https://playwright.dev/docs/intro)
- [API 参考](https://playwright.dev/docs/api/class-playwright)
- [最佳实践](https://playwright.dev/docs/best-practices)
