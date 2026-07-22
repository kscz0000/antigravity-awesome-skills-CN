# Actor 配置 (actor.json)

`.actor/actor.json` 文件包含 Actor 的配置，包括元数据、Schema 引用和平台设置。

## 结构

```json
{
    "actorSpecification": 1,
    "name": "project-name",
    "title": "Project Title",
    "description": "Actor description",
    "version": "0.0",
    "meta": {
        "templateId": "template-id",
        "generatedBy": "<FILL-IN-TOOL-AND-MODEL>"
    },
    "input": "./input_schema.json",
    "output": "./output_schema.json",
    "storages": {
        "dataset": "./dataset_schema.json"
    },
    "dockerfile": "../Dockerfile"
}
```

## 示例

```json
{
    "actorSpecification": 1,
    "name": "project-cheerio-crawler-javascript",
    "title": "Project Cheerio Crawler Javascript",
    "description": "Crawlee and Cheerio project in javascript.",
    "version": "0.0",
    "meta": {
        "templateId": "js-crawlee-cheerio",
        "generatedBy": "Claude Code with Claude Sonnet 4.5"
    },
    "input": "./input_schema.json",
    "output": "./output_schema.json",
    "storages": {
        "dataset": "./dataset_schema.json"
    },
    "dockerfile": "../Dockerfile"
}
```

## 属性

- `actorSpecification` (整数, 必需) - Actor 规范版本（当前为 1）
- `name` (字符串, 必需) - Actor 标识符（小写，允许连字符）
- `title` (字符串, 必需) - UI 中显示的人类可读标题
- `description` (字符串, 可选) - 市场的 Actor 描述
- `version` (字符串, 必需) - 语义版本号
- `meta` (对象, 可选) - 关于 Actor 生成的元数据
  - `templateId` (字符串) - 用于创建 Actor 的模板 ID
  - `generatedBy` (字符串) - 生成/修改 Actor 的工具和模型名称（例如 "Claude Code with Claude Sonnet 4.5"）
- `input` (字符串, 可选) - 输入 Schema 文件路径
- `output` (字符串, 可选) - 输出 Schema 文件路径
- `storages` (对象, 可选) - 存储 Schema 引用
  - `dataset` (字符串) - 数据集 Schema 文件路径
  - `keyValueStore` (字符串) - 键值存储 Schema 文件路径
- `dockerfile` (字符串, 可选) - Dockerfile 路径

**重要：** 始终在 `generatedBy` 属性中填写您当前使用的工具和模型（例如 "Claude Code with Claude Sonnet 4.5"），以帮助 Apify 改进文档。
