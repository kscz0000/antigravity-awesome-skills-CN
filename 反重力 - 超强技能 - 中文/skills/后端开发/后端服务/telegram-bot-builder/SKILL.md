---
name: telegram-bot-builder
description: 构建解决实际问题的 Telegram 机器人专家——从简单自动化到复杂 AI 驱动的机器人。涵盖机器人架构、Telegram Bot API、用户体验、变现策略及支撑数千用户的扩展方案。触发词：telegram bot、bot api、telegram automation、chat bot telegram、tg bot
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Telegram 机器人构建专家

构建解决实际问题的 Telegram 机器人专家——从简单自动化到复杂 AI 驱动的机器人。涵盖机器人架构、Telegram Bot API、用户体验、变现策略及支撑数千用户的扩展方案。

**角色**：Telegram 机器人架构师

你构建的机器人是用户每天真正会用的。你理解机器人应该像贴心助手，而不是笨重的界面。你深入了解 Telegram 生态——什么能做、什么流行、什么能赚钱。你设计的对话体验自然流畅。

### 专业领域

- Telegram Bot API
- 机器人用户体验设计
- 变现策略
- Node.js/Python 机器人开发
- Webhook 架构
- 内联键盘

## 核心能力

- Telegram Bot API
- 机器人架构设计
- 命令设计
- 内联键盘
- 机器人变现
- 用户引导流程
- 机器人数据分析
- Webhook 管理

## 设计模式

### 机器人架构

构建可维护的 Telegram 机器人结构

**适用场景**：启动新的机器人项目时

## 机器人架构

### 技术栈选择
| 语言 | 库 | 最佳用途 |
|----------|---------|----------|
| Node.js | telegraf | 大多数项目 |
| Node.js | grammY | TypeScript、现代化项目 |
| Python | python-telegram-bot | 快速原型开发 |
| Python | aiogram | 异步、可扩展项目 |

### Telegraf 基础配置
```javascript
import { Telegraf } from 'telegraf';

const bot = new Telegraf(process.env.BOT_TOKEN);

// Command handlers
bot.start((ctx) => ctx.reply('Welcome!'));
bot.help((ctx) => ctx.reply('How can I help?'));

// Text handler
bot.on('text', (ctx) => {
  ctx.reply(`You said: ${ctx.message.text}`);
});

// Launch
bot.launch();

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
```

### 项目结构
```
telegram-bot/
├── src/
│   ├── bot.js           # Bot initialization
│   ├── commands/        # Command handlers
│   │   ├── start.js
│   │   ├── help.js
│   │   └── settings.js
│   ├── handlers/        # Message handlers
│   ├── keyboards/       # Inline keyboards
│   ├── middleware/      # Auth, logging
│   └── services/        # Business logic
├── .env
└── package.json
```

### 内联键盘

交互式按钮界面

**适用场景**：构建交互式机器人流程时

## 内联键盘

### 基础键盘
```javascript
import { Markup } from 'telegraf';

bot.command('menu', (ctx) => {
  ctx.reply('Choose an option:', Markup.inlineKeyboard([
    [Markup.button.callback('Option 1', 'opt_1')],
    [Markup.button.callback('Option 2', 'opt_2')],
    [
      Markup.button.callback('Yes', 'yes'),
      Markup.button.callback('No', 'no'),
    ],
  ]));
});

// Handle button clicks
bot.action('opt_1', (ctx) => {
  ctx.answerCbQuery('You chose Option 1');
  ctx.editMessageText('You selected Option 1');
});
```

### 键盘布局模式
| 模式 | 适用场景 |
|---------|----------|
| 单列布局 | 简单菜单 |
| 多列布局 | 是/否选择、分页 |
| 网格布局 | 分类选择 |
| URL 按钮 | 链接、支付 |

### 分页功能
```javascript
function getPaginatedKeyboard(items, page, perPage = 5) {
  const start = page * perPage;
  const pageItems = items.slice(start, start + perPage);

  const buttons = pageItems.map(item =>
    [Markup.button.callback(item.name, `item_${item.id}`)]
  );

  const nav = [];
  if (page > 0) nav.push(Markup.button.callback('◀️', `page_${page-1}`));
  if (start + perPage < items.length) nav.push(Markup.button.callback('▶️', `page_${page+1}`));

  return Markup.inlineKeyboard([...buttons, nav]);
}
```

### 机器人变现

通过 Telegram 机器人盈利

**适用场景**：规划机器人收入时

## 机器人变现

### 收入模式
| 模式 | 示例 | 复杂度 |
|-------|---------|------------|
| 免费增值 | 基础免费、高级付费 | 中等 |
| 订阅制 | 按月付费 | 中等 |
| 按次付费 | 按操作收费 | 低 |
| 广告 | 赞助消息 | 低 |
| 分销推广 | 商品推荐 | 低 |

### Telegram 支付
```javascript
// Create invoice
bot.command('buy', (ctx) => {
  ctx.replyWithInvoice({
    title: 'Premium Access',
    description: 'Unlock all features',
    payload: 'premium_monthly',
    provider_token: process.env.PAYMENT_TOKEN,
    currency: 'USD',
    prices: [{ label: 'Premium', amount: 999 }], // $9.99
  });
});

// Handle successful payment
bot.on('successful_payment', (ctx) => {
  const payment = ctx.message.successful_payment;
  // Activate premium for user
  await activatePremium(ctx.from.id);
  ctx.reply('🎉 Premium activated!');
});
```

### 免费增值策略
```
Free tier:
- 10 uses per day
- Basic features
- Ads shown

Premium ($5/month):
- Unlimited uses
- Advanced features
- No ads
- Priority support
```

### 使用限制
```javascript
async function checkUsage(userId) {
  const usage = await getUsage(userId);
  const isPremium = await checkPremium(userId);

  if (!isPremium && usage >= 10) {
    return { allowed: false, message: 'Daily limit reached. Upgrade?' };
  }
  return { allowed: true };
}
```

### Webhook 部署

生产环境机器人部署

**适用场景**：将机器人部署到生产环境时

## Webhook 部署

### 轮询 vs Webhooks
| 方式 | 最佳用途 |
|--------|----------|
| 轮询 | 开发阶段、简单机器人 |
| Webhooks | 生产环境、可扩展 |

### Express + Webhook
```javascript
import express from 'express';
import { Telegraf } from 'telegraf';

const bot = new Telegraf(process.env.BOT_TOKEN);
const app = express();

app.use(express.json());
app.use(bot.webhookCallback('/webhook'));

// Set webhook
const WEBHOOK_URL = 'https://your-domain.com/webhook';
bot.telegram.setWebhook(WEBHOOK_URL);

app.listen(3000);
```

### Vercel 部署
```javascript
// api/webhook.js
import { Telegraf } from 'telegraf';

const bot = new Telegraf(process.env.BOT_TOKEN);
// ... bot setup

export default async (req, res) => {
  await bot.handleUpdate(req.body);
  res.status(200).send('OK');
};
```

### Railway/Render 部署
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "src/bot.js"]
```

## 验证检查项

### 机器人 Token 硬编码

严重级别：HIGH

问题：机器人 Token 似乎被硬编码——存在安全风险！

修复：将 Token 移至环境变量 BOT_TOKEN

### 缺少机器人错误处理

严重级别：HIGH

问题：机器人没有全局错误处理器。

修复：添加 bot.catch() 优雅处理错误

### 缺少速率限制

严重级别：MEDIUM

问题：没有速率限制——可能触发 Telegram 限制。

修复：使用 Bottleneck 或类似库添加限流

### 生产环境使用内存会话

严重级别：MEDIUM

问题：使用内存会话——重启后会丢失状态。

修复：生产环境使用 Redis 或数据库存储会话

### 缺少输入状态指示器

严重级别：LOW

问题：建议添加输入状态指示器以提升用户体验。

修复：在耗时操作前添加 ctx.sendChatAction('typing')

## 协作对接

### 委派触发条件

- mini app|web app|TON|twa → telegram-mini-app（Mini App 集成）
- AI|GPT|Claude|LLM|chatbot → ai-wrapper-product（AI 集成）
- database|postgres|redis → backend（数据持久化）
- payments|subscription|billing → fintech-integration（支付集成）
- deploy|host|production → devops（部署运维）

### AI Telegram 机器人

技能组合：telegram-bot-builder、ai-wrapper-product、backend

工作流程：

```
1. Design bot conversation flow
2. Set up AI integration (OpenAI/Claude)
3. Build backend for state/data
4. Implement bot commands and handlers
5. Add monetization (freemium)
6. Deploy and monitor
```

### 机器人 + Mini App

技能组合：telegram-bot-builder、telegram-mini-app、frontend

工作流程：

```
1. Design bot as entry point
2. Build Mini App for complex UI
3. Integrate bot commands with Mini App
4. Handle payments in Mini App
5. Deploy both components
```

## 相关技能

配合使用效果更佳：`telegram-mini-app`、`backend`、`ai-wrapper-product`、`workflow-automation`

## 适用场景
- 用户提及或暗示：telegram bot
- 用户提及或暗示：bot api
- 用户提及或暗示：telegram automation
- 用户提及或暗示：chat bot telegram
- 用户提及或暗示：tg bot

## 使用限制
- 仅在任务明确匹配上述范围时使用此技能。
- 输出不能替代针对特定环境的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，请暂停并请求澄清。
