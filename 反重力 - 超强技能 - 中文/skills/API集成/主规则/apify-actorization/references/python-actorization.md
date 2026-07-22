# Python Actorization

## 安装 Apify SDK

```bash
pip install apify
```

## 使用 Actor 上下文管理器包装主函数

```python
import asyncio
from apify import Actor

async def main() -> None:
    async with Actor:
        # ============================================
        # 你现有的代码放在这里
        # ============================================

        # 示例：从 Apify Console 或 API 获取输入
        actor_input = await Actor.get_input()
        print(f'Input: {actor_input}')

        # 示例：你的爬虫或处理逻辑
        # crawler = PlaywrightCrawler(...)
        # await crawler.run([actor_input.get('startUrl')])

        # 示例：推送结果到数据集
        # await Actor.push_data({'result': 'data'})

        # ============================================
        # 你的代码结束
        # ============================================

if __name__ == '__main__':
    asyncio.run(main())
```

## 关键点

- `async with Actor:` 同时处理初始化和清理
- 自动管理平台事件监听器和优雅关闭
- 本地执行保持不变 - SDK 自动检测环境

## Crawlee Python 项目

```python
import asyncio
from apify import Actor
from crawlee.playwright_crawler import PlaywrightCrawler

async def main() -> None:
    async with Actor:
        # 获取并验证输入
        actor_input = await Actor.get_input() or {}
        start_url = actor_input.get('startUrl', 'https://example.com')
        max_items = actor_input.get('maxItems', 100)

        item_count = 0

        async def request_handler(context):
            nonlocal item_count
            if item_count >= max_items:
                return

            title = await context.page.title()
            await context.push_data({'url': context.request.url, 'title': title})
            item_count += 1

        crawler = PlaywrightCrawler(request_handler=request_handler)
        await crawler.run([start_url])

if __name__ == '__main__':
    asyncio.run(main())
```

## 批处理脚本

```python
import asyncio
from apify import Actor

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        items = actor_input.get('items', [])

        for item in items:
            result = process_item(item)
            await Actor.push_data(result)

if __name__ == '__main__':
    asyncio.run(main())
```
