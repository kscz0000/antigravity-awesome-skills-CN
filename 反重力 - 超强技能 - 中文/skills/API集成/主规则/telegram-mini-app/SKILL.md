---
name: telegram-mini-app
description: 构建 Telegram 迷你应用（TWA）的专家——在 Telegram 内运行、具备原生体验的 Web 应用。覆盖 TON 生态、Telegram Web App API、支付、用户认证，以及打造可变现的病毒式迷你应用。触发词：telegram mini app、TWA、telegram web app、TON app、mini app
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Telegram 迷你应用

构建 Telegram 迷你应用（TWA）的专家——在 Telegram 内运行、具备原生体验的 Web 应用。覆盖 TON 生态、Telegram Web App API、支付、用户认证，以及打造可变现的病毒式迷你应用。

**角色**：Telegram 迷你应用架构师

你面向 8 亿+ Telegram 用户构建应用。你理解迷你应用生态正在爆发——游戏、DeFi、工具、社交应用。你熟悉 TON 区块链和加密货币变现方式。你为 Telegram UX 范式而非传统 Web 设计。

### 专业领域

- Telegram Web App API
- TON 区块链
- 迷你应用 UX
- TON Connect
- 病毒式传播机制
- 加密货币支付

## 能力

- Telegram Web App API
- 迷你应用架构
- TON Connect 集成
- 应用内支付
- 通过 Telegram 进行用户认证
- 迷你应用 UX 模式
- 病毒式迷你应用机制
- TON 区块链集成

## 模式

### 迷你应用搭建

Telegram 迷你应用入门

**适用场景**：开始新迷你应用时

## 迷你应用搭建

### 基本结构
```html
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
  <script>
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    // User data
    const user = tg.initDataUnsafe.user;
    console.log(user.first_name, user.id);
  </script>
</body>
</html>
```

### React 搭建
```jsx
// hooks/useTelegram.js
export function useTelegram() {
  const tg = window.Telegram?.WebApp;

  return {
    tg,
    user: tg?.initDataUnsafe?.user,
    queryId: tg?.initDataUnsafe?.query_id,
    expand: () => tg?.expand(),
    close: () => tg?.close(),
    ready: () => tg?.ready(),
  };
}

// App.jsx
function App() {
  const { tg, user, expand, ready } = useTelegram();

  useEffect(() => {
    ready();
    expand();
  }, []);

  return <div>Hello, {user?.first_name}</div>;
}
```

### Bot 集成
```javascript
// Bot sends Mini App
bot.command('app', (ctx) => {
  ctx.reply('Open the app:', {
    reply_markup: {
      inline_keyboard: [[
        { text: '🚀 Open App', web_app: { url: 'https://your-app.com' } }
      ]]
    }
  });
});
```

### TON Connect 集成

TON 区块链的钱包连接

**适用场景**：构建 Web3 迷你应用时

## TON Connect 集成

### 安装
```bash
npm install @tonconnect/ui-react
```

### React 集成
```jsx
import { TonConnectUIProvider, TonConnectButton } from '@tonconnect/ui-react';

// Wrap app
function App() {
  return (
    <TonConnectUIProvider manifestUrl="https://your-app.com/tonconnect-manifest.json">
      <MainApp />
    </TonConnectUIProvider>
  );
}

// Use in components
function WalletSection() {
  return (
    <TonConnectButton />
  );
}
```

### Manifest 文件
```json
{
  "url": "https://your-app.com",
  "name": "Your Mini App",
  "iconUrl": "https://your-app.com/icon.png"
}
```

### 发送 TON 交易
```jsx
import { useTonConnectUI } from '@tonconnect/ui-react';

function PaymentButton({ amount, to }) {
  const [tonConnectUI] = useTonConnectUI();

  const handlePay = async () => {
    const transaction = {
      validUntil: Math.floor(Date.now() / 1000) + 60,
      messages: [{
        address: to,
        amount: (amount * 1e9).toString(), // TON to nanoton
      }]
    };

    await tonConnectUI.sendTransaction(transaction);
  };

  return <button onClick={handlePay}>Pay {amount} TON</button>;
}
```

### 迷你应用变现

迷你应用的盈利方式

**适用场景**：规划迷你应用收入时

## 迷你应用变现

### 收入来源
| 模式 | 示例 | 潜力 |
|-------|---------|-----------|
| TON 支付 | 高级功能 | 高 |
| 应用内购买 | 虚拟商品 | 高 |
| 广告（Telegram Ads） | 展示广告 | 中 |
| 推荐返利 | 分享赚取 | 中 |
| NFT 销售 | 数字收藏品 | 高 |

### Telegram Stars（新功能！）
```javascript
// In your bot
bot.command('premium', (ctx) => {
  ctx.replyWithInvoice({
    title: 'Premium Access',
    description: 'Unlock all features',
    payload: 'premium',
    provider_token: '', // Empty for Stars
    currency: 'XTR', // Telegram Stars
    prices: [{ label: 'Premium', amount: 100 }], // 100 Stars
  });
});
```

### 病毒式传播机制
```jsx
// Referral system
function ReferralShare() {
  const { tg, user } = useTelegram();
  const referralLink = `https://t.me/your_bot?start=ref_${user.id}`;

  const share = () => {
    tg.openTelegramLink(
      `https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=Check this out!`
    );
  };

  return <button onClick={share}>Invite Friends (+10 coins)</button>;
}
```

### 游戏化留存策略
- 每日奖励
- 连续登录奖励
- 排行榜
- 成就徽章
- 推荐奖励

### 迷你应用 UX 模式

Telegram 迷你应用专属的 UX 设计

**适用场景**：设计迷你应用界面时

## 迷你应用 UX

### 平台规范
| 元素 | 实现方式 |
|---------|----------------|
| 主按钮 | tg.MainButton |
| 返回按钮 | tg.BackButton |
| 主题 | tg.themeParams |
| 触觉反馈 | tg.HapticFeedback |

### 主按钮
```javascript
const tg = window.Telegram.WebApp;

// Show main button
tg.MainButton.setText('Continue');
tg.MainButton.show();
tg.MainButton.onClick(() => {
  // Handle click
  submitForm();
});

// Loading state
tg.MainButton.showProgress();
// ...
tg.MainButton.hideProgress();
```

### 主题适配
```css
:root {
  --tg-theme-bg-color: var(--tg-theme-bg-color, #ffffff);
  --tg-theme-text-color: var(--tg-theme-text-color, #000000);
  --tg-theme-button-color: var(--tg-theme-button-color, #3390ec);
}

body {
  background: var(--tg-theme-bg-color);
  color: var(--tg-theme-text-color);
}
```

### 触觉反馈
```javascript
// Light feedback
tg.HapticFeedback.impactOccurred('light');

// Success
tg.HapticFeedback.notificationOccurred('success');

// Selection
tg.HapticFeedback.selectionChanged();
```

## 注意事项

### 未验证来自 Telegram 的 initData

严重程度：高

场景：后端未验证就信任用户数据

症状：
- 盲目信任客户端数据
- 缺少服务端验证
- 直接使用 initDataUnsafe
- 安全审计失败

为什么会出问题：
initData 可被伪造。
存在安全漏洞。
用户可冒充他人。
数据可能被篡改。

建议修复：

## 验证 initData

### 为什么需要验证
- initData 包含用户信息
- 必须验证其来源是 Telegram
- 防止伪造和篡改

### Node.js 验证
```javascript
import crypto from 'crypto';

function validateInitData(initData, botToken) {
  const params = new URLSearchParams(initData);
  const hash = params.get('hash');
  params.delete('hash');

  // Sort and join
  const dataCheckString = Array.from(params.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, v]) => `${k}=${v}`)
    .join('\n');

  // Create secret key
  const secretKey = crypto
    .createHmac('sha256', 'WebAppData')
    .update(botToken)
    .digest();

  // Calculate hash
  const calculatedHash = crypto
    .createHmac('sha256', secretKey)
    .update(dataCheckString)
    .digest('hex');

  return calculatedHash === hash;
}
```

### 在 API 中使用
```javascript
app.post('/api/action', (req, res) => {
  const { initData } = req.body;

  if (!validateInitData(initData, process.env.BOT_TOKEN)) {
    return res.status(401).json({ error: 'Invalid initData' });
  }

  // Safe to use data
  const params = new URLSearchParams(initData);
  const user = JSON.parse(params.get('user'));
  // ...
});
```

### TON Connect 在移动端不工作

严重程度：高

场景：在移动端 Telegram 中钱包连接失败

症状：
- 桌面端正常，移动端失败
- 钱包应用未打开
- 连接卡住
- 用户无法支付

为什么会出问题：
深度链接问题。
钱包应用未打开。
返回 URL 问题。
iOS 和 Android 行为不同。

建议修复：

## TON Connect 移动端问题

### 常见问题
1. 钱包未打开
2. 返回迷你应用失败
3. 交易确认丢失

### 修复方案
```jsx
// Use correct manifest
const manifestUrl = 'https://your-domain.com/tonconnect-manifest.json';

// Ensure HTTPS
// Localhost won't work on mobile

// Handle connection states
const [tonConnectUI] = useTonConnectUI();

useEffect(() => {
  return tonConnectUI.onStatusChange((wallet) => {
    if (wallet) {
      console.log('Connected:', wallet.account.address);
    }
  });
}, []);
```

### 测试建议
- 在真机上测试
- 用多个钱包测试（Tonkeeper、OpenMask）
- 同时测试 iOS 和 Android
- 使用 ngrok 进行本地开发 + 移动端测试

### 兜底方案
```jsx
// Show QR for desktop
// Show wallet list for mobile
<TonConnectButton />
// Automatically handles this
```

### 迷你应用卡顿缓慢

严重程度：中

场景：应用卡顿、过渡缓慢、体验差

症状：
- 首次加载慢
- 交互卡顿
- 用户抱怨速度
- 跳出率高

为什么会出问题：
JavaScript 代码过多。
没有代码分割。
打包体积大。
缺少加载优化。

建议修复：

## 迷你应用性能优化

### 打包体积
- 目标 gzip 后 < 200KB
- 使用代码分割
- 路由懒加载
- 依赖树摇优化

### 快速优化
```jsx
// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));

// Optimize images
<img loading="lazy" src="..." />

// Use CSS instead of JS animations
```

### 加载策略
```jsx
function App() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // Show skeleton immediately
    // Load data in background
    Promise.all([
      loadUserData(),
      loadAppConfig(),
    ]).then(() => setReady(true));
  }, []);

  if (!ready) return <Skeleton />;
  return <MainApp />;
}
```

### Vite 优化
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        }
      }
    }
  }
};
```

### 用自定义按钮替代 MainButton

严重程度：中

场景：应用使用自定义提交按钮，缺乏原生感

症状：
- 自定义提交按钮
- 从未使用 MainButton
- UX 不一致
- 用户对操作感到困惑

为什么会出问题：
MainButton 是用户预期的 UX。
自定义按钮显得格格不入。
与 Telegram 风格不一致。
用户不知道该点哪里。

建议修复：

## 正确使用 MainButton

### 适用场景
- 表单提交
- 主要操作
- 继续/下一步流程
- 结算/支付

### 实现方式
```javascript
const tg = window.Telegram.WebApp;

// Show for forms
function showMainButton(text, onClick) {
  tg.MainButton.setText(text);
  tg.MainButton.onClick(onClick);
  tg.MainButton.show();
}

// Hide when not needed
function hideMainButton() {
  tg.MainButton.hide();
  tg.MainButton.offClick();
}

// Loading state
function setMainButtonLoading(loading) {
  if (loading) {
    tg.MainButton.showProgress();
    tg.MainButton.disable();
  } else {
    tg.MainButton.hideProgress();
    tg.MainButton.enable();
  }
}
```

### React Hook
```jsx
function useMainButton(text, onClick, visible = true) {
  const tg = window.Telegram?.WebApp;

  useEffect(() => {
    if (!tg) return;

    if (visible) {
      tg.MainButton.setText(text);
      tg.MainButton.onClick(onClick);
      tg.MainButton.show();
    } else {
      tg.MainButton.hide();
    }

    return () => {
      tg.MainButton.offClick(onClick);
    };
  }, [text, onClick, visible]);
}
```

## 验证检查

### 未验证 initData

严重程度：高

提示：未验证 initData——存在安全漏洞。

修复：实现服务端 initData 验证，使用哈希校验

### 缺少 Telegram Web App 脚本

严重程度：高

提示：未引入 Telegram Web App 脚本。

修复：添加 <script src='https://telegram.org/js/telegram-web-app.js'></script>

### 未调用 tg.ready()

严重程度：中

提示：未调用 tg.ready()——Telegram 可能显示加载状态。

修复：在应用就绪时调用 window.Telegram.WebApp.ready()

### 未使用 Telegram 主题

严重程度：中

提示：未适配 Telegram 主题颜色。

修复：使用 tg.themeParams 的 CSS 变量设置颜色

### 缺少 Viewport Meta 标签

严重程度：中

提示：缺少移动端 viewport meta 标签。

修复：添加 <meta name='viewport' content='width=device-width, initial-scale=1.0'>

## 协作

### 委派触发条件

- bot|command|handler → telegram-bot-builder（Bot 集成）
- TON|smart contract|blockchain → blockchain-defi（TON 区块链功能）
- react|vue|frontend → frontend（前端框架）
- viral|referral|share → viral-generator-builder（病毒式传播机制）
- game|gamification → gamification-loops（游戏机制）

### 点击赚取游戏

技能：telegram-mini-app、gamification-loops、telegram-bot-builder

工作流程：

```
1. Design game mechanics
2. Build Mini App with tap mechanics
3. Add referral/viral features
4. Integrate TON payments
5. Bot for notifications/onboarding
6. Launch and grow
```

### DeFi 迷你应用

技能：telegram-mini-app、blockchain-defi、frontend

工作流程：

```
1. Design DeFi feature (swap, stake, etc.)
2. Integrate TON Connect
3. Build transaction UI
4. Add wallet management
5. Implement security measures
6. Deploy and audit
```

## 相关技能

配合使用效果更佳：`telegram-bot-builder`、`frontend`、`blockchain-defi`、`viral-generator-builder`

## 适用场景
- 用户提及或暗示：telegram mini app
- 用户提及或暗示：TWA
- 用户提及或暗示：telegram web app
- 用户提及或暗示：TON app
- 用户提及或暗示：mini app

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不可将输出替代特定环境的验证、测试或专家评审。
- 缺少必要输入、权限、安全边界或成功标准时，请停下来确认。
