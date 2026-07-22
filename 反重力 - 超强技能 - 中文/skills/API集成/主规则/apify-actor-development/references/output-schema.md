# 输出 Schema 参考

Actor 输出 Schema 基于数据集和键值存储的 Schema 构建。它指定 Actor 将输出存储在何处，并定义访问该输出的模板。Apify Console 使用这些输出定义来显示运行结果。

## 结构

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "<OUTPUT-SCHEMA-TITLE>",
    "properties": {
        /* define your outputs here */
    }
}
```

## 示例

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "Output schema of the files scraper",
    "properties": {
        "files": {
            "type": "string",
            "title": "Files",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys"
        },
        "dataset": {
            "type": "string",
            "title": "Dataset",
            "template": "{{links.apiDefaultDatasetUrl}}/items"
        }
    }
}
```

## 输出 Schema 模板变量

- `links` (对象) - 包含最常用 URL 的快速链接
- `links.publicRunUrl` (字符串) - 公共运行 URL，格式为 `https://console.apify.com/view/runs/:runId`
- `links.consoleRunUrl` (字符串) - Console 运行 URL，格式为 `https://console.apify.com/actors/runs/:runId`
- `links.apiRunUrl` (字符串) - API 运行 URL，格式为 `https://api.apify.com/v2/actor-runs/:runId`
- `links.apiDefaultDatasetUrl` (字符串) - 默认数据集的 API URL，格式为 `https://api.apify.com/v2/datasets/:defaultDatasetId`
- `links.apiDefaultKeyValueStoreUrl` (字符串) - 默认键值存储的 API URL，格式为 `https://api.apify.com/v2/key-value-stores/:defaultKeyValueStoreId`
- `links.containerRunUrl` (字符串) - 运行内部运行的 Web 服务器 URL，格式为 `https://<containerId>.runs.apify.net/`
- `run` (对象) - 包含运行信息，与 `GET Run` API 端点返回的信息相同
- `run.defaultDatasetId` (字符串) - 默认数据集的 ID
- `run.defaultKeyValueStoreId` (字符串) - 默认键值存储的 ID
