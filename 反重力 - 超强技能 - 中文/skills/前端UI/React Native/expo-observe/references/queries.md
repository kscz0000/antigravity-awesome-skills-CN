# EAS Observe CLI

EAS Observe 收集 Expo 应用的应用性能遥测和自定义事件，并通过五个 EAS CLI 命令将其暴露出来。请对任何命令使用 `--help` 标志以查看最新 API。

## 命令概览

| 命令 | 用途 |
|---------|---------|
| `eas observe:metrics-summary` | 针对应用启动性能指标的每个版本的统计聚合（中位数、p90 等） |
| `eas observe:metrics` | 单个性能指标样本，按值或时间戳排序（分页） |
| `eas observe:routes` | 针对导航指标的每个路由的统计聚合（Cold TTR、Warm TTR、Nav TTI） |
| `eas observe:events` | 应用通过 `logEvent` 发出的自定义事件 —— 名称汇总、所有事件、或按事件名称过滤（分页） |
| `eas observe:versions` | 应用版本层级结构，包含构建号、OTA 更新 ID 和事件计数 |

所有五个命令共享以下通用标志：

- `--platform ios` 或 `--platform android` —— 按平台过滤（默认：两个平台）
- `--start <ISO 日期>` 和 `--end <ISO 日期>` —— 显式指定时间范围
- `--days <N>` —— 显示最近 N 天的数据（与 `--start`/`--end` 互斥）
- `--project-id <id>` —— 针对特定项目运行，无需项目目录。传入此参数时，命令不会尝试创建新的 EAS 项目。
- `--json` —— 机器可读输出（隐含 `--non-interactive`）
- `--non-interactive` —— 失败而非提示

当未给出 `--days`、`--start`、`--end` 时，默认时间范围为最近 60 天。

## 支持的指标

### 应用启动指标

供 `observe:metrics-summary` 和 `observe:metrics` 使用。

| 别名 | 完整名称 | 显示名称 |
|-------|-----------|---------|
| `tti` | `expo.app_startup.tti` | Startup TTI（可交互时间） |
| `ttr` | `expo.app_startup.ttr` | Startup TTR（首次渲染时间） |
| `cold_launch` | `expo.app_startup.cold_launch_time` | Cold Launch（冷启动） |
| `warm_launch` | `expo.app_startup.warm_launch_time` | Warm Launch（热启动） |
| `bundle_load` | `expo.app_startup.bundle_load_time` | Bundle Load（包加载） |
| `update_download` | `expo.updates.download_time` | Update Download（更新下载） |

### 导航指标

供 `observe:routes` 使用，按路由名称测量。

| 别名 | 完整名称 | 显示名称 |
|-------|-----------|---------|
| `cold_ttr` | `expo.navigation.cold_ttr` | Nav Cold TTR |
| `warm_ttr` | `expo.navigation.warm_ttr` | Nav Warm TTR |
| `nav_tti` | `expo.navigation.tti` | Nav TTI |

## `eas observe:metrics-summary`

显示一个或多个指标在每个版本下的统计聚合，每个平台单独成表。

```bash
# 所有默认指标、最近 60 天、双平台
eas observe:metrics-summary

# 单个指标
eas observe:metrics-summary --metric tti

# 多个指标 —— 每个指标渲染一张独立的表格
eas observe:metrics-summary --metric tti --metric cold_launch

# 选择要显示的统计项
eas observe:metrics-summary --metric tti --stat median --stat p90 --stat eventCount

# 缩小时间范围并指定平台
eas observe:metrics-summary --metric tti --days 14 --platform ios
```

**统计标志：** `min`、`max`、`median`（别名 `med`）、`average`（别名 `avg`）、`p80`、`p90`、`p99`、`eventCount`（别名 `count`）。

**默认统计项：** 表格中显示 `median` + `eventCount`；JSON 中显示所有统计项。

**表格布局：**
- 每个指标一张表（值与事件计数单元格合并，例如 `0.45s (150)`）
- 每张表的 iOS 与 Android 分别在不同小节中显示
- App Version 列在括号内包含构建号（例如 `1.2.0 (42)`）
- 每个平台有一行页脚显示该指标的总事件数
- **表格中省略 Update ID**，以在版本包含大量更新时保持输出可读；它们作为数组包含在对应版本的 JSON 输出中

**JSON 输出结构：**
```json
{
  "versions": [
    {
      "appVersion": "1.2.0",
      "platform": "IOS",
      "buildNumbers": ["42"],
      "updateIds": ["abc-def-...", "..."],
      "metrics": {
        "expo.app_startup.tti": { "median": 0.45, "p90": 0.9, "...": "..." }
      }
    }
  ],
  "totalEventCounts": {
    "expo.app_startup.tti": { "IOS": 1234, "ANDROID": 890 }
  }
}
```

## `eas observe:metrics`

显示单个性能指标样本，分页展示。指标是位置参数，而不是标志。如果省略且以交互模式运行，会提示选择；非交互模式下会抛出错误。

```bash
# 交互模式：提示选择指标
eas observe:metrics

# 将指标指定为位置参数
eas observe:metrics tti

# 按版本或更新过滤，按最慢排序
eas observe:metrics tti --app-version 1.2.0 --sort slowest --limit 20

# 分页 —— 传入上一次运行的 endCursor
eas observe:metrics tti --after <cursor>
```

**样本专属标志：**
- `--sort <oldest|newest|slowest|fastest>` —— 默认为 `oldest`
- `--limit <N>` —— 每页样本数（默认 10，最大 100）
- `--after <cursor>` —— 上一页的分页游标
- `--app-version <version>` —— 按应用版本字符串过滤
- `--update-id <id>` —— 按 EAS 更新 ID 过滤

**表格布局：**
- 摘要标题显示指标名称、时间范围以及跨所有版本的总样本数（例如 `TTI samples for the last 60 days — 1,234 total events`）
- 列：Value、App Version（含构建号）、Update（仅当存在样本具有更新时显示）、Platform、Device、Country、Timestamp
- 当 `hasNextPage` 为 true 时，表格下方打印 `Next page: --after <endCursor>` 提示
- JSON 输出还包含 `sessionId`、`easClientId`，以及每个样本的 `customParams` 对象

## `eas observe:routes`

显示每个路由在导航指标（Cold TTR、Warm TTR、Nav TTI）上的统计聚合，按路由名称分组，每个平台单独成节。

```bash
# 全部三种导航指标、默认统计项、最近 60 天、双平台
eas observe:routes

# 单个指标、最近 7 天、仅 iOS
eas observe:routes --metric nav_tti --days 7 --platform ios

# 多个指标与统计项
eas observe:routes --metric cold_ttr --metric warm_ttr --stat median --stat p90 --stat count

# 过滤到单个构建
eas observe:routes --app-version 1.2.0 --build-number 42

# 收窄至特定路由（多次传此标志以指定多个路由）
eas observe:routes --route-name /new --route-name /settings

# 分页 —— 每个平台拥有独立的游标；传入对应的 endCursor
eas observe:routes --after <cursor>
```

**Routes 专属标志：**
- `--metric <cold_ttr|warm_ttr|nav_tti>` —— 要显示的导航指标，可重复。默认为全部三个。
- `--stat <median|p90|count>` —— 每个指标的统计项。别名：`med` → `median`，`event_count` / `eventCount` → `count`。
- `--limit <N>` —— 每页路由数（默认 **50**，最大 **200**，与 `metrics`/`events` 的默认 10 不同）。
- `--after <cursor>` —— 分页游标。
- `--app-version <version>` —— 按应用版本字符串过滤。
- `--build-number <number>` —— 按应用构建号过滤（仅 routes）。
- `--route-name <name>` —— 按路由名称过滤。可重复；只返回列出的路由（跨双平台）。重复项会自动去重；省略此标志则返回所有路由。
- `--update-id <id>` —— 按 EAS 更新 ID 过滤。

**默认统计项：** 表格中显示 `median` + `count`；JSON 中显示 `median`、`p90`、`count`。

**表格布局：**
- 摘要标题显示所选统计项与时间范围，例如 `Med, P90 values (navigation count) for the last 7 days`。
- iOS 与 Android 分开的小节。
- 第一列为 **Route**，其后为每个指标/统计项对应的一列。当同时显示统计值与 `count` 时，单元格会合并，例如 `0.32s (1240)`。
- 每个平台有独立的分页提示：`Next page (iOS): --after <endCursor>`。

**JSON 输出结构：**
```json
{
  "routes": [
    {
      "routeName": "(tabs)/home",
      "platform": "IOS",
      "metrics": {
        "expo.navigation.cold_ttr": { "median": 0.32, "p90": 0.85, "count": 1240 },
        "expo.navigation.tti":       { "median": 0.55, "p90": 1.10, "count": 1240 }
      }
    }
  ],
  "pageInfoByPlatform": {
    "IOS":     { "hasNextPage": true,  "endCursor": "..." },
    "ANDROID": { "hasNextPage": false, "endCursor": null }
  }
}
```

## `eas observe:events`

显示应用通过 `expo-observe` 中 `logEvent` API 发出的自定义事件。行为取决于传入的参数：

| 调用 | 结果 |
|---|---|
| `observe:events` | 可用事件名称及其计数的汇总表 |
| `observe:events --all-events` | 跨**所有**事件名称的完整事件列表 |
| `observe:events <event-name>` | 按该事件名称过滤的完整事件列表 |

```bash
# 列出可用的自定义事件名称及其计数（最近 60 天）
eas observe:events

# 跨所有名称的所有事件，最近 7 天，仅 iOS
eas observe:events --all-events --days 7 --platform ios

# 仅显示具有给定名称的事件
eas observe:events login_failed --limit 50

# 深入查看单个会话
eas observe:events --all-events --session-id <session-id>

# 分页
eas observe:events login_failed --after <cursor>
```

**Events 专属标志：**
- `--all-events` —— 当未传入事件名称参数时，列出所有事件而不是名称汇总。不能与事件名称参数组合使用。
- `--session-id <id>` —— 过滤为单个会话的事件（仅 events）
- `--app-version <version>` —— 按应用版本字符串过滤
- `--update-id <id>` —— 按 EAS 更新 ID 过滤
- `--limit <N>` —— 每页事件数（默认 10，最大 100）
- `--after <cursor>` —— 分页游标

**表格布局（事件列表）：**
- 摘要标题：`<event-name> events <time range>`，或对 `--all-events` 显示 `Custom events <time range>`，并在可用时显示总事件数
- 列：Timestamp、Event（仅在跨多个名称列出时显示）、Severity（仅当本页中至少有一个事件具有严重级别时显示）、App Version（含构建号）、Platform、Device、Country
- 存在下一页时，表格下方有 `Next page: --after <endCursor>` 提示

**空结果辅助提示：** 如果查询特定事件名称但没有返回事件，命令会打印一条黄色 `No events found matching "<name>"` 警告，随后打印同一时间范围内可用的事件名称及其计数 —— 这有助于修正拼写错误。

**截断说明：** 事件名称汇总在事件名称数量超过单次响应所能返回的数量时，可能会出现 `Result is truncated; not all event names are shown.` 提示。

**JSON 输出结构（事件列表）：**
```json
{
  "events": [
    {
      "id": "...",
      "eventName": "login_failed",
      "timestamp": "2026-...",
      "sessionId": "...",
      "severityNumber": 13,
      "severityText": "WARN",
      "properties": [{ "key": "reason", "value": "bad_password", "type": "string" }],
      "appVersion": "1.2.0",
      "appBuildNumber": "42",
      "appUpdateId": null,
      "appEasBuildId": null,
      "deviceModel": "...",
      "deviceOs": "iOS",
      "deviceOsVersion": "17.4",
      "countryCode": "US",
      "environment": "production",
      "easClientId": "..."
    }
  ],
  "pageInfo": { "hasNextPage": true, "endCursor": "..." }
}
```

名称汇总模式返回 `{ "names": [{ "eventName": "...", "count": 123 }], "isTruncated": false }`。

## `eas observe:versions`

显示应用版本层级结构，包含构建号、OTA 更新 ID 与每个版本的事件计数。

```bash
# 双平台、最近 60 天
eas observe:versions

# 仅 iOS、最近 14 天
eas observe:versions --days 14 --platform ios
```

没有与指标相关的标志。输出分别显示 iOS 与 Android 的表格，列为：**App Version、First Seen、Events、Users、Builds (count)、Updates (count)**。

JSON 输出返回完整的嵌套层级，包含 `buildNumbers[].easBuilds[]` 和 `updates[].easBuilds[]`，并在每个层级上都包含 `firstSeenAt`、`eventCount`、`uniqueUserCount`。

## 常见工作流

**"我的应用目前启动时间是多少？"**
```bash
eas observe:metrics-summary --days 7 --stat median --stat p90
```

**"本周哪一些 TTI 样本最慢？"**
```bash
eas observe:metrics tti --sort slowest --days 7 --limit 20
```

**"OTA 更新在用户端的下载速度如何？"**
```bash
eas observe:metrics-summary --metric update_download --days 7
```

**"哪些屏幕导航最慢？"**
```bash
eas observe:routes --metric nav_tti --stat median --stat p90 --days 7
```

**"我所关心的那些路由上的导航性能如何？"**
```bash
eas observe:routes --route-name /home --route-name /checkout --days 7
```

**"我的应用正在发出哪些自定义事件？"**
```bash
eas observe:events --days 7
```

**"显示某个用户会话中所有的错误事件。"**
```bash
eas observe:events --all-events --session-id <session-id>
```

**"我的应用在用户端有哪些版本？"**
```bash
eas observe:versions
```

**"在仓库外针对特定项目显示指标"**
```bash
eas observe:metrics-summary --project-id <uuid> --metric tti
```

**"获取 JSON 以便脚本处理"**
```bash
eas observe:metrics-summary --metric tti --json --non-interactive
```

## 注意事项

- 要求用户已登录（`eas login`）。
- 当提供 `--project-id` 时，命令不需要在 EAS 项目目录中运行；否则项目 ID 从本地的 `app.config` / `app.json` 读取。如果使用此选项，请确保登录的用户有权访问指定项目。
- `observe:metrics-summary` 不在表格中打印 update ID，但仍然在 JSON 中返回它们，以便用于脚本或管道传递给其他命令。
