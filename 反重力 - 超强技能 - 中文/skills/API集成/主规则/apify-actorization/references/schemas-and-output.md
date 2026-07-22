# Schema 和输出配置

## 输入 Schema

将应用程序的输入映射到 `.actor/input_schema.json`。使用 `@apify/json_schemas` npm 包（`input.schema.json`）的 JSON Schema 进行验证。

```json
{
    "title": "My Actor Input",
    "type": "object",
    "schemaVersion": 1,
    "properties": {
        "startUrl": {
            "title": "Start URL",
            "type": "string",
            "description": "The URL to start processing from",
            "editor": "textfield",
            "prefill": "https://example.com"
        },
        "maxItems": {
            "title": "Max Items",
            "type": "integer",
            "description": "Maximum number of items to process",
            "default": 100,
            "minimum": 1
        }
    },
    "required": ["startUrl"]
}
```

### 映射指南

- 命令行参数 → 输入 schema 属性
- 环境变量 → 输入 schema 或 actor.json 中的 Actor 环境变量
- 配置文件 → 使用对象/数组类型的输入 schema
- 扁平化深层嵌套结构以获得更好的用户体验

## 输出 Schema

在 `.actor/output_schema.json` 中定义输出结构。使用 `@apify/json_schemas` npm 包（`output.schema.json`）的 JSON Schema 进行验证。

### 对于表格类数据（多个项目）

- 使用 `Actor.pushData()`（JS）或 `Actor.push_data()`（Python）
- 每个项目成为数据集中的一行

### 对于单个文件或 Blob

- 使用键值存储：`Actor.setValue()` / `Actor.set_value()`
- 获取公共 URL 并将其包含在数据集中：

```javascript
// 存储具有公共访问权限的文件
await Actor.setValue('report.pdf', pdfBuffer, { contentType: 'application/pdf' });

// 获取公共 URL
const storeInfo = await Actor.openKeyValueStore();
const publicUrl = `https://api.apify.com/v2/key-value-stores/${storeInfo.id}/records/report.pdf`;

// 在数据集输出中包含 URL
await Actor.pushData({ reportUrl: publicUrl });
```

### 对于具有公共前缀的多个文件（集合）

```javascript
// 使用前缀存储多个文件
for (const [name, data] of files) {
    await Actor.setValue(`screenshots/${name}`, data, { contentType: 'image/png' });
}
// 文件可访问于：.../records/screenshots%2F{name}
```

## Actor 配置（actor.json）

配置 `.actor/actor.json`。使用 `@apify/json_schemas` npm 包（`actor.schema.json`）的 JSON Schema 进行验证。

```json
{
    "actorSpecification": 1,
    "name": "my-actor",
    "title": "My Actor",
    "description": "Brief description of what the actor does",
    "version": "1.0.0",
    "meta": {
        "templateId": "ts_empty",
        "generatedBy": "Claude Code with Claude Opus 4.5"
    },
    "input": "./input_schema.json",
    "dockerfile": "../Dockerfile"
}
```

**重要：** 在 `generatedBy` 属性中填写使用的工具/模型。

## 状态管理

### 请求队列 - 用于可暂停的任务处理

请求队列适用于任何任务处理，不仅限于网页抓取。对于非 URL 任务，使用带有自定义 `uniqueKey` 和 `userData` 的虚拟 URL：

```javascript
const requestQueue = await Actor.openRequestQueue();

// 向队列添加任务（适用于任何处理，不仅限于 URL）
await requestQueue.addRequest({
    url: 'https://placeholder.local',  // 非抓取任务的虚拟 URL
    uniqueKey: `task-${taskId}`,       // 用于去重的唯一标识符
    userData: { itemId: 123, action: 'process' },  // 你的自定义任务数据
});

// 从队列处理任务（使用 Crawlee）
const crawler = new BasicCrawler({
    requestQueue,
    requestHandler: async ({ request }) => {
        const { itemId, action } = request.userData;
        // 使用 userData 处理你的任务
        await processTask(itemId, action);
    },
});
await crawler.run();

// 或不使用 Crawlee 手动消费：
let request;
while ((request = await requestQueue.fetchNextRequest())) {
    await processTask(request.userData);
    await requestQueue.markRequestHandled(request);
}
```

### 键值存储 - 用于检查点状态

```javascript
// 保存状态
await Actor.setValue('STATE', { processedCount: 100 });

// 重启时恢复状态
const state = await Actor.getValue('STATE') || { processedCount: 0 };
```
