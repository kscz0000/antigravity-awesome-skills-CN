# JavaScript/TypeScript Actorization

## 安装 Apify SDK

```bash
npm install apify
```

## 使用 Actor 生命周期包装主代码

```javascript
import { Actor } from 'apify';

// 初始化与 Apify 平台的连接
await Actor.init();

// ============================================
// 你现有的代码放在这里
// ============================================

// 示例：从 Apify Console 或 API 获取输入
const input = await Actor.getInput();
console.log('Input:', input);

// 示例：你的爬虫或处理逻辑
// const crawler = new PlaywrightCrawler({ ... });
// await crawler.run([input.startUrl]);

// 示例：推送结果到数据集
// await Actor.pushData({ result: 'data' });

// ============================================
// 你的代码结束
// ============================================

// 优雅关闭
await Actor.exit();
```

## 关键点

- `Actor.init()` 配置存储在平台上运行时使用 Apify API
- `Actor.exit()` 处理优雅关闭和清理
- 两个调用都必须 await
- 本地执行保持不变 - SDK 自动检测环境

## Crawlee 项目

Crawlee 项目需要最少的更改 - 只需用 Actor 生命周期包装：

```javascript
import { Actor } from 'apify';
import { PlaywrightCrawler } from 'crawlee';

await Actor.init();

// 获取并验证输入
const input = await Actor.getInput();
const {
    startUrl = 'https://example.com',
    maxItems = 100,
} = input ?? {};

let itemCount = 0;

const crawler = new PlaywrightCrawler({
    requestHandler: async ({ page, request, pushData }) => {
        if (itemCount >= maxItems) return;

        const title = await page.title();
        await pushData({ url: request.url, title });
        itemCount++;
    },
});

await crawler.run([startUrl]);

await Actor.exit();
```

## Express/HTTP 服务器

对于 Web 服务器，在 actor.json 中使用待机模式：

```json
{
    "actorSpecification": 1,
    "name": "my-api",
    "usesStandbyMode": true
}
```

然后实现就绪探针。参见 [standby-mode.md](../../apify-actor-development/references/standby-mode.md)。

## 批处理脚本

```javascript
import { Actor } from 'apify';

await Actor.init();

const input = await Actor.getInput();
const items = input.items || [];

for (const item of items) {
    const result = processItem(item);
    await Actor.pushData(result);
}

await Actor.exit();
```
