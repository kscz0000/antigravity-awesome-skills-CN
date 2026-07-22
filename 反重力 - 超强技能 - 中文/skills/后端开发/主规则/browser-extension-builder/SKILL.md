---
name: browser-extension-builder
description: 浏览器扩展开发专家——涵盖 Chrome、Firefox 及跨浏览器扩展。包括扩展架构、Manifest V3、内容脚本、弹出窗口 UI、变现策略和 Chrome Web Store 发布。当用户要求"浏览器扩展""Chrome扩展""Firefox插件""浏览器插件"时使用。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 浏览器扩展构建器

浏览器扩展开发专家——涵盖 Chrome、Firefox 及跨浏览器扩展。包括扩展架构、Manifest V3、内容脚本、弹出窗口 UI、变现策略和 Chrome Web Store 发布。

**角色**：浏览器扩展架构师

你为浏览器赋予超能力。你理解扩展开发的独特约束——权限、安全、商店政策。你构建的扩展，用户装了就会天天用。你分得清玩具和工具。

### 专长

- Chrome 扩展 API
- Manifest V3
- 内容脚本
- Service Worker
- 扩展 UX
- 商店发布

## 能力

- 扩展架构
- Manifest V3（MV3）
- 内容脚本
- Background Worker
- 弹出窗口界面
- 扩展变现
- Chrome Web Store 发布
- 跨浏览器支持

## 模式

### 扩展架构

现代浏览器扩展的项目结构

**何时使用**：启动新扩展时

## 扩展架构

### 项目结构
```
extension/
├── manifest.json      # Extension config
├── popup/
│   ├── popup.html     # Popup UI
│   ├── popup.css
│   └── popup.js
├── content/
│   └── content.js     # Runs on web pages
├── background/
│   └── service-worker.js  # Background logic
├── options/
│   ├── options.html   # Settings page
│   └── options.js
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

### Manifest V3 模板
```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "description": "What it does",
  "permissions": ["storage", "activeTab"],
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "content_scripts": [{
    "matches": ["<all_urls>"],
    "js": ["content/content.js"]
  }],
  "background": {
    "service_worker": "background/service-worker.js"
  },
  "options_page": "options/options.html"
}
```

### 通信模式
```
Popup ←→ Background (Service Worker) ←→ Content Script
              ↓
        chrome.storage
```

### 内容脚本

在网页上运行的代码

**何时使用**：修改或读取页面内容时

## 内容脚本

### 基础内容脚本
```javascript
// content.js - Runs on every matched page

// Wait for page to load
document.addEventListener('DOMContentLoaded', () => {
  // Modify the page
  const element = document.querySelector('.target');
  if (element) {
    element.style.backgroundColor = 'yellow';
  }
});

// Listen for messages from popup/background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'getData') {
    const data = document.querySelector('.data')?.textContent;
    sendResponse({ data });
  }
  return true; // Keep channel open for async
});
```

### 注入 UI
```javascript
// Create floating UI on page
function injectUI() {
  const container = document.createElement('div');
  container.id = 'my-extension-ui';
  container.innerHTML = `
    <div style="position: fixed; bottom: 20px; right: 20px;
                background: white; padding: 16px; border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 10000;">
      <h3>My Extension</h3>
      <button id="my-extension-btn">Click me</button>
    </div>
  `;
  document.body.appendChild(container);

  document.getElementById('my-extension-btn').addEventListener('click', () => {
    // Handle click
  });
}

injectUI();
```

### 内容脚本权限
```json
{
  "content_scripts": [{
    "matches": ["https://specific-site.com/*"],
    "js": ["content.js"],
    "run_at": "document_end"
  }]
}
```

### 存储与状态

持久化扩展数据

**何时使用**：保存用户设置或数据时

## 存储与状态

### Chrome Storage API
```javascript
// Save data
chrome.storage.local.set({ key: 'value' }, () => {
  console.log('Saved');
});

// Get data
chrome.storage.local.get(['key'], (result) => {
  console.log(result.key);
});

// Sync storage (syncs across devices)
chrome.storage.sync.set({ setting: true });

// Watch for changes
chrome.storage.onChanged.addListener((changes, area) => {
  if (changes.key) {
    console.log('key changed:', changes.key.newValue);
  }
});
```

### 存储限制
| 类型 | 限制 |
|------|------|
| local | 5MB |
| sync | 总计 100KB，单项 8KB |

### Async/Await 模式
```javascript
// Modern async wrapper
async function getStorage(keys) {
  return new Promise((resolve) => {
    chrome.storage.local.get(keys, resolve);
  });
}

async function setStorage(data) {
  return new Promise((resolve) => {
    chrome.storage.local.set(data, resolve);
  });
}

// Usage
const { settings } = await getStorage(['settings']);
await setStorage({ settings: { ...settings, theme: 'dark' } });
```

### 扩展变现

从扩展中赚钱

**何时使用**：规划扩展收入时

## 扩展变现

### 收入模式
| 模式 | 运作方式 |
|------|----------|
| 免费增值 | 基础免费，高级付费 |
| 一次性购买 | 一次付费，永久使用 |
| 订阅 | 按月/年付费 |
| 捐赠 | 赞赏 / 请我喝咖啡 |
| 联盟推广 | 推荐产品获取佣金 |

### 支付集成
```javascript
// Use your backend for payments
// Extension can't directly use Stripe

// 1. User clicks "Upgrade" in popup
// 2. Open your website with user ID
chrome.tabs.create({
  url: `https://your-site.com/upgrade?user=${userId}`
});

// 3. After payment, sync status
async function checkPremium() {
  const { userId } = await getStorage(['userId']);
  const response = await fetch(
    `https://your-api.com/premium/${userId}`
  );
  const { isPremium } = await response.json();
  await setStorage({ isPremium });
  return isPremium;
}
```

### 功能门控
```javascript
async function usePremiumFeature() {
  const { isPremium } = await getStorage(['isPremium']);
  if (!isPremium) {
    showUpgradeModal();
    return;
  }
  // Run premium feature
}
```

### Chrome Web Store 支付
- Chrome 已停用内置支付功能
- 使用自有支付系统
- 链接到外部结账页面

## 验证检查

### 使用已弃用的 Manifest V2

严重程度：高

说明：使用了 Manifest V2——Chrome 要求新扩展必须使用 V3。

修复：迁移到 Manifest V3 并使用 Service Worker

### 请求过多权限

严重程度：高

说明：请求了过宽的权限——可能导致商店审核被拒。

修复：使用具体的 host_permissions 和 optional_permissions

### 扩展缺少错误处理

严重程度：中

说明：未检查 chrome.runtime.lastError。

修复：在 API 调用后检查 chrome.runtime.lastError

### 扩展中硬编码 URL

严重程度：中

说明：硬编码 URL 可能在生产环境中引发问题。

修复：使用 chrome.storage 或 manifest 进行配置

### 缺少扩展图标

严重程度：低

说明：缺少扩展图标——影响商店展示。

修复：添加 16、48、128 像素尺寸的图标

## 协作

### 委派触发

- react|vue|svelte -> frontend（扩展弹出窗口框架）
- monetization|payment|subscription -> micro-saas-launcher（扩展商业模式）
- personal tool|just for me -> personal-tool-builder（个人扩展）
- AI|LLM|GPT -> ai-wrapper-product（AI 驱动扩展）

### 生产力扩展

技能：browser-extension-builder、frontend、micro-saas-launcher

工作流：

```
1. 定义扩展功能
2. 用 React 构建弹出窗口 UI
3. 实现内容脚本
4. 添加高级付费功能
5. 发布到 Chrome Web Store
6. 推广与迭代
```

### AI 浏览器助手

技能：browser-extension-builder、ai-wrapper-product、frontend

工作流：

```
1. 设计浏览器 AI 功能
2. 构建扩展架构
3. 集成 AI API
4. 创建弹出窗口界面
5. 处理用量限制/支付
6. 发布与增长
```

## 相关技能

配合使用：`frontend`、`micro-saas-launcher`、`personal-tool-builder`

## 何时使用
- 用户提到或暗示：浏览器扩展
- 用户提到或暗示：Chrome 扩展
- 用户提到或暗示：Firefox 插件
- 用户提到或暗示：扩展
- 用户提到或暗示：Manifest V3

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家评审。
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。
