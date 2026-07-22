# `eas update:insights` JSON schema

`eas update:insights <groupId> --json --non-interactive` 返回的完整 JSON 输出结构。

```json
{
  "groupId": "03d5dfcf-736c-475a-8730-af039c3f4d06",
  "timespan": {
    "start": "2026-04-10T00:00:00.000Z",
    "end": "2026-04-17T00:00:00.000Z",
    "daysBack": 7
  },
  "platforms": [
    {
      "platform": "android",
      "updateId": "019d72ca-...",
      "totals": {
        "uniqueUsers": 500,
        "installs": 990,
        "failedInstalls": 10,
        "crashRatePercent": 1.0
      },
      "payload": {
        "launchAssetCount": 4,
        "averageUpdatePayloadBytes": 1115771
      },
      "daily": [
        { "date": "2026-04-10T00:00:00.000Z", "installs": 182, "failedInstalls": 2 },
        { "date": "2026-04-11T00:00:00.000Z", "installs": 195, "failedInstalls": 1 }
      ]
    },
    {
      "platform": "ios",
      "updateId": "019d72ca-...",
      "totals": { "uniqueUsers": 100, "installs": 1, "failedInstalls": 0, "crashRatePercent": 0 },
      "payload": { "launchAssetCount": 4, "averageUpdatePayloadBytes": 1115771 },
      "daily": [ { "date": "2026-04-10T00:00:00.000Z", "installs": 1, "failedInstalls": 0 } ]
    }
  ]
}
```

## 字段参考

| 路径 | 含义 |
|---|---|
| `groupId` | 被查询的更新组。 |
| `timespan.start` / `.end` | 用于界定时间窗口的 UTC ISO 时间戳。 |
| `timespan.daysBack` | 便捷字段：时间窗口的天数。 |
| `platforms[]` | 该组已发布的每个平台各一条（`ios`、`android`）。 |
| `platforms[].updateId` | 平台特定的 update ID（与 group ID 不同）。 |
| `platforms[].totals.uniqueUsers` | 在该时间窗口内运行过此更新的独立用户数。 |
| `platforms[].totals.installs` | 时间窗口内的启动次数 / 成功安装次数。 |
| `platforms[].totals.failedInstalls` | 时间窗口内的崩溃次数 / 失败安装次数。 |
| `platforms[].totals.crashRatePercent` | `failedInstalls / (installs + failedInstalls) * 100`。当没有安装时为 0。 |
| `platforms[].payload.launchAssetCount` | manifest 引用的资源数量。 |
| `platforms[].payload.averageUpdatePayloadBytes` | 该时间窗口内的平均包体大小。 |
| `platforms[].daily[]` | 按天的时间序列，记录安装与失败安装次数。 |

## `eas update:view <groupId> --insights --json`

`update:view --insights --json` 命令包装了同样的 insights 负载：

```json
{
  "updates": [ /* 标准的 update:view 条目 */ ],
  "insights": { /* 与上面的 eas update:insights 结构相同 */ }
}
```