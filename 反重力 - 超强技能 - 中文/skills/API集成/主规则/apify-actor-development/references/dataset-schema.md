# 数据集 Schema 参考

数据集 Schema 定义 Actor 输出数据的结构、转换方式，以及在 Apify Console 输出标签页中的显示方式。

## 示例

### JavaScript 和 TypeScript

考虑一个调用 `Actor.pushData()` 将数据存储到数据集的示例 Actor：

```javascript
import { Actor } from 'apify';
// Initialize the JavaScript SDK
await Actor.init();

/**
 * Actor code
 */
await Actor.pushData({
    numericField: 10,
    pictureUrl: 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png',
    linkUrl: 'https://google.com',
    textField: 'Google',
    booleanField: true,
    dateField: new Date(),
    arrayField: ['#hello', '#world'],
    objectField: {},
});

// Exit successfully
await Actor.exit();
```

### Python

考虑一个调用 `Actor.push_data()` 将数据存储到数据集的示例 Actor：

```python
# Dataset push example (Python)
import asyncio
from datetime import datetime
from apify import Actor

async def main():
    await Actor.init()

    # Actor code
    await Actor.push_data({
        'numericField': 10,
        'pictureUrl': 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png',
        'linkUrl': 'https://google.com',
        'textField': 'Google',
        'booleanField': True,
        'dateField': datetime.now().isoformat(),
        'arrayField': ['#hello', '#world'],
        'objectField': {},
    })

    # Exit successfully
    await Actor.exit()

if __name__ == '__main__':
    asyncio.run(main())
```

## 配置

要设置 Actor 的输出标签页 UI，在 `.actor/actor.json` 中引用数据集 Schema 文件：

```json
{
    "actorSpecification": 1,
    "name": "book-library-scraper",
    "title": "Book Library Scraper",
    "version": "1.0.0",
    "storages": {
        "dataset": "./dataset_schema.json"
    }
}
```

然后在 `.actor/dataset_schema.json` 中创建数据集 Schema：

```json
{
    "actorSpecification": 1,
    "fields": {},
    "views": {
        "overview": {
            "title": "Overview",
            "transformation": {
                "fields": [
                    "pictureUrl",
                    "linkUrl",
                    "textField",
                    "booleanField",
                    "arrayField",
                    "objectField",
                    "dateField",
                    "numericField"
                ]
            },
            "display": {
                "component": "table",
                "properties": {
                    "pictureUrl": {
                        "label": "Image",
                        "format": "image"
                    },
                    "linkUrl": {
                        "label": "Link",
                        "format": "link"
                    },
                    "textField": {
                        "label": "Text",
                        "format": "text"
                    },
                    "booleanField": {
                        "label": "Boolean",
                        "format": "boolean"
                    },
                    "arrayField": {
                        "label": "Array",
                        "format": "array"
                    },
                    "objectField": {
                        "label": "Object",
                        "format": "object"
                    },
                    "dateField": {
                        "label": "Date",
                        "format": "date"
                    },
                    "numericField": {
                        "label": "Number",
                        "format": "number"
                    }
                }
            }
        }
    }
}
```

## 结构

```json
{
    "actorSpecification": 1,
    "fields": {},
    "views": {
        "<VIEW_NAME>": {
            "title": "string (required)",
            "description": "string (optional)",
            "transformation": {
                "fields": ["string (required)"],
                "unwind": ["string (optional)"],
                "flatten": ["string (optional)"],
                "omit": ["string (optional)"],
                "limit": "integer (optional)",
                "desc": "boolean (optional)"
            },
            "display": {
                "component": "table (required)",
                "properties": {
                    "<FIELD_NAME>": {
                        "label": "string (optional)",
                        "format": "text|number|date|link|boolean|image|array|object (optional)"
                    }
                }
            }
        }
    }
}
```

## 属性

### 数据集 Schema 属性

- `actorSpecification` (整数, 必需) - 指定数据集 Schema 结构文档的版本（当前仅版本 1）
- `fields` (JSONSchema 对象, 必需) - 单个数据集对象的 Schema（使用 JsonSchema Draft 2020-12 或兼容版本）
- `views` (DatasetView 对象, 必需) - 包含 API 和 UI 视图描述的对象

### DatasetView 属性

- `title` (字符串, 必需) - 在 UI 输出标签页和 API 中可见
- `description` (字符串, 可选) - 仅在 API 响应中可用
- `transformation` (ViewTransformation 对象, 必需) - 从数据集 API 加载时应用的数据转换
- `display` (ViewDisplay 对象, 必需) - 输出标签页 UI 可视化定义

### ViewTransformation 属性

- `fields` (字符串数组, 必需) - 输出中呈现的字段（顺序匹配列顺序）
- `unwind` (字符串数组, 可选) - 将嵌套子项解构到父对象中
- `flatten` (字符串数组, 可选) - 将嵌套对象转换为扁平结构
- `omit` (字符串数组, 可选) - 从输出中移除指定字段
- `limit` (整数, 可选) - 最大结果数（默认：全部）
- `desc` (布尔值, 可选) - 排序顺序（true = 最新优先）

### ViewDisplay 属性

- `component` (字符串, 必需) - 仅 `table` 可用
- `properties` (对象, 可选) - 与 `transformation.fields` 匹配的键，值为 ViewDisplayProperty

### ViewDisplayProperty 属性

- `label` (字符串, 可选) - 表格列标题
- `format` (字符串, 可选) - 以下之一：`text`、`number`、`date`、`link`、`boolean`、`image`、`array`、`object`
