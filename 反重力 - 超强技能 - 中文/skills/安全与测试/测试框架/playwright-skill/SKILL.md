---
name: playwright-skill
description: "重要提示 - 路径解析：此技能可安装在不同位置（插件系统、手动安装、全局或项目级）。执行任何命令前，请根据加载此 SKILL.md 文件的位置确定技能目录，并在下方所有命令中使用该路径。浏览器自动化、Playwright测试、网页测试、E2E测试、端到端测试、浏览器控制、页面截图、表单填写、登录测试、响应式测试、链接检查"
risk: unknown
source: community
date_added: "2026-02-27"
plugin:
  setup:
    type: manual
    summary: "首次使用前在技能目录中运行 `npm run setup` 以安装 Playwright 和 Chromium。"
    docs: "SKILL.md"
---

**重要提示 - 路径解析：**
此技能可安装在不同位置（插件系统、手动安装、全局或项目级）。执行任何命令前，请根据加载此 SKILL.md 文件的位置确定技能目录，并在下方所有命令中使用该路径。将 `$SKILL_DIR` 替换为实际发现的路径。

常见安装路径：

- 插件系统：`<plugin-root>/skills/playwright-skill`
- 手动全局：`<agent-home>/skills/playwright-skill`
- 项目级：`<project>/.agent/skills/playwright-skill`

# Playwright 浏览器自动化

通用浏览器自动化技能。我将为你请求的任何自动化任务编写自定义 Playwright 代码，并通过通用执行器运行。

**关键工作流 - 按以下顺序执行：**

1. **自动检测开发服务器** - 对于 localhost 测试，始终先运行服务器检测：

   ```bash
   cd $SKILL_DIR && node -e "require('./lib/helpers').detectDevServers().then(servers => console.log(JSON.stringify(servers)))"
   ```

   - 如果**找到 1 个服务器**：自动使用，通知用户
   - 如果**找到多个服务器**：询问用户测试哪一个
   - 如果**未找到服务器**：询问 URL 或提供帮助启动开发服务器

2. **将脚本写入 /tmp** - 切勿将测试文件写入技能目录；始终使用 `/tmp/playwright-test-*.js`

3. **默认使用可见浏览器** - 始终使用 `headless: false`，除非用户明确要求无头模式

4. **参数化 URL** - 始终通过环境变量或脚本顶部的常量使 URL 可配置

## 工作原理

1. 你描述想要测试/自动化的内容
2. 我自动检测运行中的开发服务器（如果测试外部站点则询问 URL）
3. 我在 `/tmp/playwright-test-*.js` 中编写自定义 Playwright 代码（不会弄乱你的项目）
4. 通过以下命令执行：`cd $SKILL_DIR && node run.js /tmp/playwright-test-*.js`
5. 实时显示结果，浏览器窗口可见以便调试
6. 测试文件由操作系统从 /tmp 自动清理

## 安装（首次使用）

```bash
cd $SKILL_DIR
npm run setup
```

此命令安装 Playwright 和 Chromium 浏览器。只需运行一次。

## 执行模式

**步骤 1：检测开发服务器（用于 localhost 测试）**

```bash
cd $SKILL_DIR && node -e "require('./lib/helpers').detectDevServers().then(s => console.log(JSON.stringify(s)))"
```

**步骤 2：将测试脚本写入 /tmp，带 URL 参数**

```javascript
// /tmp/playwright-test-page.js
const { chromium } = require('playwright');

// 参数化 URL（自动检测或用户提供）
const TARGET_URL = 'http://localhost:3001'; // <-- 自动检测或来自用户

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(TARGET_URL);
  console.log('Page loaded:', await page.title());

  await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true });
  console.log('📸 Screenshot saved to /tmp/screenshot.png');

  await browser.close();
})();
```

**步骤 3：从技能目录执行**

```bash
cd $SKILL_DIR && node run.js /tmp/playwright-test-page.js
```

## 常用模式

### 测试页面（多视口）

```javascript
// /tmp/playwright-test-responsive.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // 自动检测

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const page = await browser.newPage();

  // 桌面端测试
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto(TARGET_URL);
  console.log('Desktop - Title:', await page.title());
  await page.screenshot({ path: '/tmp/desktop.png', fullPage: true });

  // 移动端测试
  await page.setViewportSize({ width: 375, height: 667 });
  await page.screenshot({ path: '/tmp/mobile.png', fullPage: true });

  await browser.close();
})();
```

### 测试登录流程

```javascript
// /tmp/playwright-test-login.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // 自动检测

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/login`);

  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // 等待重定向
  await page.waitForURL('**/dashboard');
  console.log('✅ Login successful, redirected to dashboard');

  await browser.close();
})();
```

### 填写并提交表单

```javascript
// /tmp/playwright-test-form.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // 自动检测

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/contact`);

  await page.fill('input[name="name"]', 'John Doe');
  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('textarea[name="message"]', 'Test message');
  await page.click('button[type="submit"]');

  // 验证提交
  await page.waitForSelector('.success-message');
  console.log('✅ Form submitted successfully');

  await browser.close();
})();
```

### 检查失效链接

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('http://localhost:3000');

  const links = await page.locator('a[href^="http"]').all();
  const results = { working: 0, broken: [] };

  for (const link of links) {
    const href = await link.getAttribute('href');
    try {
      const response = await page.request.head(href);
      if (response.ok()) {
        results.working++;
      } else {
        results.broken.push({ url: href, status: response.status() });
      }
    } catch (e) {
      results.broken.push({ url: href, error: e.message });
    }
  }

  console.log(`✅ Working links: ${results.working}`);
  console.log(`❌ Broken links:`, results.broken);

  await browser.close();
})();
```

### 带错误处理的截图

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    await page.goto('http://localhost:3000', {
      waitUntil: 'networkidle',
      timeout: 10000,
    });

    await page.screenshot({
      path: '/tmp/screenshot.png',
      fullPage: true,
    });

    console.log('📸 Screenshot saved to /tmp/screenshot.png');
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
  }
})();
```

### 测试响应式设计

```javascript
// /tmp/playwright-test-responsive-full.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // 自动检测

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  const viewports = [
    { name: 'Desktop', width: 1920, height: 1080 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 },
  ];

  for (const viewport of viewports) {
    console.log(
      `Testing ${viewport.name} (${viewport.width}x${viewport.height})`,
    );

    await page.setViewportSize({
      width: viewport.width,
      height: viewport.height,
    });

    await page.goto(TARGET_URL);
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: `/tmp/${viewport.name.toLowerCase()}.png`,
      fullPage: true,
    });
  }

  console.log('✅ All viewports tested');
  await browser.close();
})();
```

## 内联执行（简单任务）

对于快速的一次性任务，可以内联执行代码而无需创建文件：

```bash
# 快速截图
cd $SKILL_DIR && node run.js "
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();
await page.goto('http://localhost:3001');
await page.screenshot({ path: '/tmp/quick-screenshot.png', fullPage: true });
console.log('Screenshot saved');
await browser.close();
"
```

**何时使用内联 vs 文件：**

- **内联**：快速一次性任务（截图、检查元素是否存在、获取页面标题）
- **文件**：复杂测试、响应式设计检查、用户可能想重新运行的任何内容

## 可用辅助函数

`lib/helpers.js` 中的可选工具函数：

```javascript
const helpers = require('./lib/helpers');

// 检测运行中的开发服务器（关键 - 先使用此功能！）
const servers = await helpers.detectDevServers();
console.log('Found servers:', servers);

// 带重试的安全点击
await helpers.safeClick(page, 'button.submit', { retries: 3 });

// 带清空的安全输入
await helpers.safeType(page, '#username', 'testuser');

// 带时间戳的截图
await helpers.takeScreenshot(page, 'test-result');

// 处理 Cookie 横幅
await helpers.handleCookieBanner(page);

// 提取表格数据
const data = await helpers.extractTableData(page, 'table.results');
```

完整列表请参见 `lib/helpers.js`。

## 自定义 HTTP 请求头

通过环境变量为所有 HTTP 请求配置自定义请求头。适用于：

- 识别发送到后端的自动化流量
- 获取 LLM 优化的响应（例如纯文本错误而非带样式的 HTML）
- 全局添加认证令牌

### 配置

**单个请求头（常见情况）：**

```bash
PW_HEADER_NAME=X-Automated-By PW_HEADER_VALUE=playwright-skill \
  cd $SKILL_DIR && node run.js /tmp/my-script.js
```

**多个请求头（JSON 格式）：**

```bash
PW_EXTRA_HEADERS='{"X-Automated-By":"playwright-skill","X-Debug":"true"}' \
  cd $SKILL_DIR && node run.js /tmp/my-script.js
```

### 工作原理

使用 `helpers.createContext()` 时，请求头会自动应用：

```javascript
const context = await helpers.createContext(browser);
const page = await context.newPage();
// 此页面发出的所有请求都包含你的自定义请求头
```

对于使用原始 Playwright API 的脚本，使用注入的 `getContextOptionsWithHeaders()`：

```javascript
const context = await browser.newContext(
  getContextOptionsWithHeaders({ viewport: { width: 1920, height: 1080 } }),
);
```

## 高级用法

有关完整的 Playwright API 文档，请参见 [API_REFERENCE.md](API_REFERENCE.md)：

- 选择器与定位器最佳实践
- 网络拦截与 API 模拟
- 认证与会话管理
- 视觉回归测试
- 移动设备模拟
- 性能测试
- 调试技术
- CI/CD 集成

## 提示

- **关键：先检测服务器** - 在为 localhost 测试编写测试代码之前，始终运行 `detectDevServers()`
- **自定义请求头** - 使用 `PW_HEADER_NAME`/`PW_HEADER_VALUE` 环境变量识别发送到后端的自动化流量
- **测试文件使用 /tmp** - 写入 `/tmp/playwright-test-*.js`，切勿写入技能目录或用户项目
- **参数化 URL** - 在每个脚本顶部将检测到/提供的 URL 放入 `TARGET_URL` 常量
- **默认：可见浏览器** - 始终使用 `headless: false`，除非用户明确要求无头模式
- **无头模式** - 仅当用户明确要求"无头"或"后台"执行时才使用 `headless: true`
- **放慢速度：** 使用 `slowMo: 100` 使操作可见且更容易跟踪
- **等待策略：** 使用 `waitForURL`、`waitForSelector`、`waitForLoadState` 而非固定超时
- **错误处理：** 始终使用 try-catch 确保健壮的自动化
- **控制台输出：** 使用 `console.log()` 跟踪进度并显示正在发生的事情

## 故障排除

**Playwright 未安装：**

```bash
cd $SKILL_DIR && npm run setup
```

**找不到模块：**
确保通过 `run.js` 包装器从技能目录运行

**浏览器未打开：**
检查 `headless: false` 并确保显示器可用

**找不到元素：**
添加等待：`await page.waitForSelector('.element', { timeout: 10000 })`

## 使用示例

```
用户："测试营销页面是否看起来正常"

Claude：我将在多个视口下测试营销页面。让我先检测运行中的服务器...
[运行：detectDevServers()]
[输出：在端口 3001 上找到服务器]
我找到了你的开发服务器，运行在 http://localhost:3001

[将自定义自动化脚本写入 /tmp/playwright-test-marketing.js，URL 已参数化]
[运行：cd $SKILL_DIR && node run.js /tmp/playwright-test-marketing.js]
[显示结果及 /tmp/ 中的截图]
```

```
用户："检查登录是否正确重定向"

Claude：我将测试登录流程。首先，让我检查运行中的服务器...
[运行：detectDevServers()]
[输出：在端口 3000 和 3001 上找到服务器]
我找到了 2 个开发服务器。你想测试哪一个？
- http://localhost:3000
- http://localhost:3001

用户："用 3001"

[将登录自动化写入 /tmp/playwright-test-login.js]
[运行：cd $SKILL_DIR && node run.js /tmp/playwright-test-login.js]
[报告：✅ 登录成功，重定向到 /dashboard]
```

## 备注

- 每次自动化都是为你特定请求自定义编写的
- 不限于预构建脚本 - 任何浏览器任务都可能实现
- 自动检测运行中的开发服务器以消除硬编码 URL
- 测试脚本写入 `/tmp` 以便自动清理（不会产生杂乱文件）
- 代码通过 `run.js` 以正确的模块解析可靠执行
- 渐进式披露 - 仅在需要高级功能时加载 API_REFERENCE.md

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。