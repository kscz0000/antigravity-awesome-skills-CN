# 键值存储 Schema 参考

键值存储 Schema 将键组织成称为集合的逻辑组，便于数据管理。

## 示例

### JavaScript 和 TypeScript

考虑一个调用 `Actor.setValue()` 将记录保存到键值存储的示例 Actor：

```javascript
import { Actor } from 'apify';
// Initialize the JavaScript SDK
await Actor.init();

/**
 * Actor code
 */
await Actor.setValue('document-1', 'my text data', { contentType: 'text/plain' });

await Actor.setValue(`image-${imageID}`, imageBuffer, { contentType: 'image/jpeg' });

// Exit successfully
await Actor.exit();
```

### Python

考虑一个调用 `Actor.set_value()` 将记录保存到键值存储的示例 Actor：

```python
# Key-Value Store set example (Python)
import asyncio
from apify import Actor

async def main():
    await Actor.init()

    # Actor code
    await Actor.set_value('document-1', 'my text data', content_type='text/plain')

    image_id = '123'          # example placeholder
    image_buffer = b'...'     # bytes buffer with image data
    await Actor.set_value(f'image-{image_id}', image_buffer, content_type='image/jpeg')

    # Exit successfully
    await Actor.exit()

if __name__ == '__main__':
    asyncio.run(main())
```

## 配置

要配置键值存储 Schema，在 `.actor/actor.json` 中引用 Schema 文件：

```json
{
    "actorSpecification": 1,
    "name": "data-collector",
    "title": "Data Collector",
    "version": "1.0.0",
    "storages": {
        "keyValueStore": "./key_value_store_schema.json"
    }
}
```

然后在 `.actor/key_value_store_schema.json` 中创建键值存储 Schema：

```json
{
    "actorKeyValueStoreSchemaVersion": 1,
    "title": "Key-Value Store Schema",
    "collections": {
        "documents": {
            "title": "Documents",
            "description": "Text documents stored by the Actor",
            "keyPrefix": "document-"
        },
        "images": {
            "title": "Images",
            "description": "Images stored by the Actor",
            "keyPrefix": "image-",
            "contentTypes": ["image/jpeg"]
        }
    }
}
```

## 结构

```json
{
    "actorKeyValueStoreSchemaVersion": 1,
    "title": "string (required)",
    "description": "string (optional)",
    "collections": {
        "<COLLECTION_NAME>": {
            "title": "string (required)",
            "description": "string (optional)",
            "key": "string (conditional - use key OR keyPrefix)",
            "keyPrefix": "string (conditional - use key OR keyPrefix)",
            "contentTypes": ["string (optional)"],
            "jsonSchema": "object (optional)"
        }
    }
}
```

## 属性

### 键值存储 Schema 属性

- `actorKeyValueStoreSchemaVersion` (整数, 必需) - 键值存储 Schema 结构文档版本（当前仅版本 1）
- `title` (字符串, 必需) - Schema 标题
- `description` (字符串, 可选) - Schema 描述
- `collections` (对象, 必需) - 对象，每个键是集合 ID，值是 Collection 对象

### Collection 属性

- `title` (字符串, 必需) - UI 标签中显示的集合标题
- `description` (字符串, 可选) - UI 工具提示中显示的集合描述
- `key` (字符串, 条件必需) - 此集合的单个特定键
- `keyPrefix` (字符串, 条件必需) - 此集合中包含的键的前缀
- `contentTypes` (字符串数组, 可选) - 用于验证的允许内容类型
- `jsonSchema` (对象, 可选) - 用于 `application/json` 内容类型验证的 JSON Schema Draft 07 格式

每个集合必须指定 `key` 或 `keyPrefix`，但不能同时指定两者。
