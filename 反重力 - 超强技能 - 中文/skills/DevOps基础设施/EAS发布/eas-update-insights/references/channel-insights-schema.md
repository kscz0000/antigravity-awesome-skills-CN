# `eas channel:insights` JSON schema

`eas channel:insights --channel <name> --runtime-version <version> --json --non-interactive` 返回的完整 JSON 输出结构。

```json
{
  "channel": "production",
  "runtimeVersion": "1.0.6",
  "timespan": { "start": "...", "end": "...", "daysBack": 7 },
  "embeddedUpdateTotalUniqueUsers": 2401,
  "otaTotalUniqueUsers": 8312,
  "mostPopularUpdates": [
    {
      "rank": 1,
      "groupId": "abc123",
      "message": "Fix checkout crash",
      "platform": "ios",
      "totalUniqueUsers": 4210
    }
  ],
  "cumulativeMetricsAtLastTimestamp": [
    { "id": "...", "label": "Embedded update", "data": 12345 },
    { "id": "...", "label": "Embedded update failed installs", "data": 0 }
  ],
  "uniqueUsersOverTime": { "labels": ["..."], "datasets": [ { "id": "...", "label": "...", "data": [100, 200] } ] },
  "cumulativeMetricsOverTime": { "labels": ["..."], "datasets": [ { "id": "...", "label": "...", "data": [10, 20] } ] }
}
```

## 字段参考

| 路径 | 含义 |
|---|---|
| `channel` | 被查询的渠道。 |
| `runtimeVersion` | 所使用的运行时版本过滤器。Channel insights 始终限定在单一运行时的范围内。 |
| `timespan.start` / `.end` / `.daysBack` | 时间窗口边界（UTC ISO）以及天数。 |
| `embeddedUpdateTotalUniqueUsers` | 时间窗口内运行 Embedded（二进制内置）构建的独立用户数。 |
| `otaTotalUniqueUsers` | `mostPopularUpdates` 中所有 `totalUniqueUsers` 的合计值。当活跃 OTA 更新超过 top-N 时，可能会低估（参见下面的注意事项）。 |
| `mostPopularUpdates[]` | 按 `totalUniqueUsers` 排序的 top-N 更新。每条包含 `rank`、`groupId`、`message`、`platform`、`totalUniqueUsers`。 |
| `cumulativeMetricsAtLastTimestamp[]` | 时间窗口结束时的快照合计值，带有标签（例如 "Embedded update"、"Embedded update failed installs"）。 |
| `uniqueUsersOverTime` | 图表形态的对象，包含 `labels`（日期）和 `datasets`，用于绘制独立用户数随时间的变化。 |
| `cumulativeMetricsOverTime` | 图表形态的对象，用于绘制累计指标随时间的变化。 |

## 注意事项

- `otaTotalUniqueUsers` 是 `mostPopularUpdates[].totalUniqueUsers` 的合计值。如果活跃的 OTA 更新数量超过服务端返回的 top-N，该数字会低估真实的 OTA 触达量。
- 同时在 iOS 与 Android 上运行同一发布的用户可能在每个平台都被分别计数。请勿将 `uniqueUsers` 视为跨平台去重后的数值。