---
name: screenshots
description: "使用 Playwright 生成应用营销截图。当用户想要为 Product Hunt、社交媒体、落地页或文档创建截图时使用此技能。触发词：营销截图、应用截图、产品截图、Product Hunt 截图、Playwright 截图、HiDPI 截图、retina 截图、marketing screenshots、app screenshots、product screenshots。"
risk: safe
source: "https://github.com/Shpigford/skills/tree/main/screenshots"
date_added: "2026-02-27"
---

# Screenshots

直接使用 Playwright 生成营销质量的应用截图。截图以真正的 HiDPI（2x retina）分辨率捕获，使用 `deviceScaleFactor: 2`。

## 何时使用此技能

在以下情况下使用此技能：
- 用户想要为 Product Hunt 创建截图
- 为社交媒体创建截图
- 为落地页生成图片
- 创建文档截图
- 用户请求营销质量的应用截图

## 前置条件

Playwright 必须可用。检查方式：
```bash
npx playwright --version 2>/dev/null || npm ls playwright 2>/dev/null | grep playwright
```

如果未找到，告知用户：
> 需要 Playwright。使用以下命令安装：`npm install -D playwright` 或 `npm install -D @playwright/test`

## 步骤 1：确定应用 URL

如果提供了 `$1`，将其用作应用 URL。

如果未提供 URL：
1. 检查 `package.json` scripts 是否可能有开发服务器正在运行
2. 使用 `AskUserQuestion` 询问用户 URL 或提供帮助启动开发服务器

常见的默认 URL 建议：
- `http://localhost:3000`（Next.js、Create React App、Rails）
- `http://localhost:5173`（Vite）
- `http://localhost:4000`（Phoenix）
- `http://localhost:8080`（Vue CLI、通用）

## 步骤 2：收集需求

使用 `AskUserQuestion` 提出以下问题：

**问题 1：截图数量**
- 标题："数量"
- 问题："你需要多少张截图？"
- 选项：
  - "3-5" - 关键功能的快速集合
  - "5-10" - 全面功能覆盖
  - "10+" - 完整营销套件

**问题 2：用途**
- 标题："用途"
- 问题："这些截图将用于什么？"
- 选项：
  - "Product Hunt" - 主图和功能亮点
  - "社交媒体" - 吸引眼球的功能演示
  - "落地页" - 营销板块和优势展示
  - "文档" - UI 参考和教程

**问题 3：认证**
- 标题："认证"
- 问题："应用是否需要登录才能访问你想要截图的功能？"
- 选项：
  - "无需登录" - 仅公开页面
  - "是，我会提供凭据" - 需要先登录

如果用户选择"是，我会提供凭据"，追问以下问题：
- "登录页面 URL 是什么？"（例如 `/login`、`/sign-in`）
- "邮箱/用户名是什么？"
- "密码是什么？"

脚本将使用 Playwright 的智能定位器自动检测登录表单字段。

## 步骤 3：分析代码库以发现功能

彻底探索代码库以理解应用并识别截图机会。

### 3.1：首先阅读文档

**始终从阅读这些文件开始**以理解应用的功能：

1. **README.md**（以及子目录中的任何 README 文件）- 阅读完整 README 以理解：
   - 应用是什么，解决什么问题
   - 关键功能和能力
   - 已记录的截图或功能描述

2. **CHANGELOG.md** 或 **HISTORY.md** - 值得突出的近期功能

3. **docs/** 目录 - 任何关于功能的额外文档

### 3.2：分析路由以发现页面

阅读路由配置以发现所有可用页面：

| 框架 | 要读取的文件 | 查找内容 |
|------|-------------|----------|
| **Next.js App Router** | `app/` 目录结构 | 每个 `page.tsx` 文件夹是一个路由 |
| **Next.js Pages Router** | `pages/` 目录 | 每个文件是一个路由 |
| **Rails** | `config/routes.rb` | 阅读整个文件获取所有路由 |
| **React Router** | 搜索 `createBrowserRouter` 或 `<Route` | 带路径的路由定义 |
| **Vue Router** | `src/router/index.js` 或 `router.js` | 带路径定义的路由数组 |
| **SvelteKit** | `src/routes/` 目录 | 每个 `+page.svelte` 文件夹是一个路由 |
| **Remix** | `app/routes/` 目录 | 基于文件的路由 |
| **Laravel** | `routes/web.php` | 路由定义 |
| **Django** | `urls.py` 文件 | URL 模式 |
| **Express** | 搜索 `app.get`、`router.get` | 路由处理器 |

**重要**：实际阅读这些文件，不要只检查它们是否存在。路由定义告诉你有哪些页面可用于截图。

### 3.3：识别关键组件

寻找代表可截图功能的组件：

- 仪表盘组件
- 具有独特 UI 的功能区块
- 表单和交互式输入
- 数据可视化（图表、图形、表格）
- 模态框和对话框
- 导航和侧边栏
- 设置面板
- 用户资料区块

### 3.4：检查营销资源

寻找暗示关键功能的现有营销内容：
- 落地页组件（通常在 `components/landing/` 或 `components/marketing/`）
- 功能列表组件
- 定价表
- 推荐区块

### 3.5：构建功能列表

创建发现功能的综合列表，包含：
- 功能名称（来自 README 或组件名称）
- URL 路径（来自路由）
- 要聚焦的 CSS 选择器（来自组件结构）
- 所需 UI 状态（已登录、数据已填充、模态框打开、特定标签选中）

## 步骤 4：与用户规划截图

向用户展示发现的功能，让他们确认或修改列表。

使用 `AskUserQuestion`：
- 标题："功能"
- 问题："我在你的代码库中发现了这些功能。你想截图哪些？"
- 选项：列出 3-4 个发现的关键功能，加上"让我选择特定的"

如果用户想要特定的，追问以明确要捕获什么。

## 步骤 5：创建截图目录

```bash
mkdir -p screenshots
```

## 步骤 6：生成并运行 Playwright 脚本

创建一个使用 Playwright 并具有正确 HiDPI 设置的 Node.js 脚本。脚本应该：

1. **使用 `deviceScaleFactor: 2`** 获得真正的 retina 分辨率
2. **设置视口为 1440x900**（生成 2880x1800 像素的图片）
3. **处理认证**（如果提供了凭据）
4. **导航到每个页面**并捕获截图

### 脚本模板

将此脚本写入临时文件（例如 `screenshot-script.mjs`）并执行：

```javascript
import { chromium } from 'playwright';

const BASE_URL = '[APP_URL]';
const SCREENSHOTS_DIR = './screenshots';

// 认证配置（如需要）
const AUTH = {
  needed: [true|false],
  loginUrl: '[LOGIN_URL]',
  email: '[EMAIL]',
  password: '[PASSWORD]',
};

// 要捕获的截图
const SCREENSHOTS = [
  { name: '01-feature-name', url: '/path', waitFor: '[optional-selector]' },
  { name: '02-another-feature', url: '/another-path' },
  // ... 添加所有计划的截图
];

async function main() {
  const browser = await chromium.launch();

  // 使用 HiDPI 设置创建上下文
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,  // 这是真正 retina 截图的关键
  });

  const page = await context.newPage();

  // 如需要则处理认证
  if (AUTH.needed) {
    console.log('Logging in...');
    await page.goto(AUTH.loginUrl);

    // 智能登录：尝试多种常见模式匹配邮箱/用户名字段
    const emailField = page.locator([
      'input[type="email"]',
      'input[name="email"]',
      'input[id="email"]',
      'input[placeholder*="email" i]',
      'input[name="username"]',
      'input[id="username"]',
      'input[type="text"]',
    ].join(', ')).first();
    await emailField.fill(AUTH.email);

    // 智能登录：尝试多种常见模式匹配密码字段
    const passwordField = page.locator([
      'input[type="password"]',
      'input[name="password"]',
      'input[id="password"]',
    ].join(', ')).first();
    await passwordField.fill(AUTH.password);

    // 智能登录：尝试多种常见模式匹配提交按钮
    const submitButton = page.locator([
      'button[type="submit"]',
      'input[type="submit"]',
      'button:has-text("Sign in")',
      'button:has-text("Log in")',
      'button:has-text("Login")',
      'button:has-text("Submit")',
    ].join(', ')).first();
    await submitButton.click();

    await page.waitForLoadState('networkidle');
    console.log('Login complete');
  }

  // 捕获每张截图
  for (const shot of SCREENSHOTS) {
    console.log(`Capturing: ${shot.name}`);
    await page.goto(`${BASE_URL}${shot.url}`);
    await page.waitForLoadState('networkidle');

    // 可选：等待特定元素
    if (shot.waitFor) {
      await page.waitForSelector(shot.waitFor);
    }

    // 可选：截图前执行操作
    if (shot.actions) {
      for (const action of shot.actions) {
        if (action.click) await page.click(action.click);
        if (action.fill) await page.fill(action.fill.selector, action.fill.value);
        if (action.wait) await page.waitForTimeout(action.wait);
      }
    }

    await page.screenshot({
      path: `${SCREENSHOTS_DIR}/${shot.name}.png`,
      fullPage: shot.fullPage || false,
    });
    console.log(`  Saved: ${shot.name}.png`);
  }

  await browser.close();
  console.log('Done!');
}

main().catch(console.error);
```

### 运行脚本

```bash
node screenshot-script.mjs
```

运行后，清理临时脚本：
```bash
rm screenshot-script.mjs
```

## 步骤 7：高级截图选项

### 元素聚焦截图

要截取特定元素而非整个视口：

```javascript
const element = await page.locator('[CSS_SELECTOR]');
await element.screenshot({ path: `${SCREENSHOTS_DIR}/element.png` });
```

### 整页截图

对于可滚动内容，捕获整个页面：

```javascript
await page.screenshot({
  path: `${SCREENSHOTS_DIR}/full-page.png`,
  fullPage: true
});
```

### 等待动画

如果页面有动画，等待其完成：

```javascript
await page.waitForTimeout(500); // 等待 500ms 让动画完成
```

### 截图前点击元素

要捕获模态框、下拉菜单或悬停状态：

```javascript
await page.click('button.open-modal');
await page.waitForSelector('.modal-content');
await page.screenshot({ path: `${SCREENSHOTS_DIR}/modal.png` });
```

### 深色模式截图

如果应用支持深色模式：

```javascript
// 设置深色模式偏好
const context = await browser.newContext({
  viewport: { width: 1440, height: 900 },
  deviceScaleFactor: 2,
  colorScheme: 'dark',
});
```

## 步骤 8：文件命名规范

使用描述性的 kebab-case 文件名，带数字前缀以便排序：

| 功能 | 文件名 |
|------|--------|
| 仪表盘概览 | `01-dashboard-overview.png` |
| 链接管理 | `02-link-inbox.png` |
| 版本编辑器 | `03-edition-editor.png` |
| 数据分析 | `04-analytics.png` |
| 设置 | `05-settings.png` |

## 步骤 9：验证和总结

捕获所有截图后，验证结果：

```bash
ls -la screenshots/*.png
sips -g pixelWidth -g pixelHeight screenshots/*.png 2>/dev/null || file screenshots/*.png
```

向用户提供总结：

1. 列出所有生成的文件及其路径
2. 确认分辨率（1440x900 视口下 2x retina 应为 2880x1800）
3. 提及总文件大小
4. 建议任何后续操作

示例输出：
```
已生成 5 张营销截图：

screenshots/
├── 01-dashboard-overview.png (1.2 MB, 2880x1800 @ 2x)
├── 02-link-inbox.png (456 KB, 2880x1800 @ 2x)
├── 03-edition-editor.png (890 KB, 2880x1800 @ 2x)
├── 04-analytics.png (567 KB, 2880x1800 @ 2x)
└── 05-settings.png (234 KB, 2880x1800 @ 2x)

所有截图均为真正的 retina 质量（2x deviceScaleFactor），可直接用于营销。
```

## 错误处理

- **Playwright 未找到**：建议 `npm install -D playwright`
- **页面未加载**：检查开发服务器是否正在运行，建议启动它
- **登录失败**：智能定位器尝试常见模式，但可能在非常规登录表单上失败。如果登录失败，分析登录页面 HTML 找到正确的选择器并自定义脚本。
- **元素未找到**：验证 CSS 选择器，提供改用整页截图的建议
- **截图失败**：检查磁盘空间，验证对截图目录的写入权限

## 最佳实践提示

1. **干净的 UI 状态**：使用演示/种子数据展示真实内容
2. **一致的尺寸**：所有截图使用相同的视口
3. **等待内容**：使用 `waitForLoadState('networkidle')` 确保所有内容加载完成
4. **隐藏开发工具**：确保没有可见的浏览器扩展或开发覆盖层
5. **深色模式变体**：如果支持，考虑同时捕获浅色和深色模式

## 局限性
- 仅在任务明确符合上述描述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
