---
name: eas-update-insights
description: "检查已发布 EAS 更新的健康状况：崩溃率、安装/启动次数、独立用户数、Payload 大小，以及每个渠道上 Embedded 与 OTA 用户之间的占比。当用户询问某个更新的表现、某次灰度的健康情况、最新更新与内置构建的用户数量对比时使用此技能。EAS、Expo、CLI、insights、metrics、crash rate、rollout monitoring"
risk: unknown
source: https://github.com/expo/skills/tree/main/plugins/expo/skills/eas-update-insights
source_repo: expo/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/expo/skills/blob/main/LICENSE
---

# EAS Update Insights

直接从 CLI 查询已发布 EAS 更新的健康状况：启动次数、启动失败次数、崩溃率、独立用户数、Payload 大小、每个渠道上 Embedded 与 OTA 用户的占比，以及按运行时版本排序的最热门更新。这些数据与 expo.dev 上 update 和 channel 详情页所使用的数据完全一致；通过这些命令可以在终端中以人类可读和 JSON 形式查看。

## 何时使用此技能

当用户希望评估某个已发布的 EAS 更新的健康状况或采用情况时使用：崩溃率、安装次数、独立用户数、包体大小，或者某个渠道上 Embedded 与 OTA 用户之间的占比。

示例提示：

- "最新更新表现如何？"
- "最新更新是否健康？"
- "新版本的崩溃次数是否比上一版更多？"
- "使用最新更新的用户数与内置构建的用户数对比是多少？"
- "当前 production 渠道上最受欢迎的更新是哪一个？"
- "我们的更新包体有多大？"

同样适用于：发布后的灰度监控和回归检测。

当用户需要每个用户的崩溃详情或设备级报告时，请勿使用此技能；本技能仅暴露聚合的 EAS 指标。

## 前置条件

- 已安装 `eas-cli`（`npm install -g eas-cli`）。
- 已登录：`eas login`。
- 对于 `channel:insights`：需在 Expo 项目目录下运行（命令会从 `app.json` 解析 project ID）。`update:insights` 仅需登录即可。

## 命令概览

| 命令 | 用途 |
|---|---|
| `eas update:list` | 发现最近的更新组、它们的 `group` ID 与分支名称 |
| `eas update:insights <groupId>` | 按平台展示启动次数、启动失败次数、崩溃率、独立用户数、Payload 大小、每日明细 |
| `eas update:view <groupId> --insights` | 更新组详情 + 同样的指标（附加在末尾） |
| `eas channel:insights --channel <name> --runtime-version <version>` | Embedded/OTA 用户数、最热门更新、某渠道 + 运行时的累计指标 |

以上所有命令均支持 `--json --non-interactive` 以便程序化解析。

## 获取 ID

在查询某个更新组的 insights 之前，你需要它的 `group` ID。使用 `eas update:list` 并传入 `--branch <name>`（该分支上的更新）或 `--all`（所有分支上的更新）。以非交互方式运行时请务必传入 `--json --non-interactive`；如果不传入分支/`--all` 标志，命令会以交互方式提示选择分支：

```bash
# 跨所有分支的最新 group id
eas update:list --all --json --non-interactive | jq -r '.currentPage[0].group'

# 特定分支上的最新 group id
eas update:list --branch production --json --non-interactive | jq -r '.currentPage[0].group'
```

JSON 响应包含一个 `currentPage` 数组，每个更新组对应一个条目（同一次发布的两个平台会合并为一条）：

```json
{
  "currentPage": [
    {
      "branch": "production",
      "message": "\"Fix checkout crash\" (1 week ago by someone)",
      "runtimeVersion": "1.0.6",
      "group": "03d5dfcf-736c-475a-8730-af039c3f4d06",
      "platforms": "android, ios",
      "isRollBackToEmbedded": false
    }
  ]
}
```

条目还会携带 `codeSigningKey` 与 `rolloutPercentage`，但仅当这些特性在该组中被使用时才会出现（未定义的值会从 JSON 输出中省略）。

当使用 `--branch <name>` 调用时，响应还会在顶层包含 `name`（分支名称）和 `id`（分支 ID）。

## `eas update:insights <groupId>`

展示单个更新组的启动次数、启动失败次数、崩溃率、独立用户数、launch asset 数量以及平均 Payload 大小，按**每个平台**（iOS、Android）分别展示，并附带启动与失败的每日明细。

### 基本用法

```bash
eas update:insights 03d5dfcf-736c-475a-8730-af039c3f4d06
```

### 标志

| 标志 | 说明 |
|---|---|
| `--days <N>` | 回溯 N 天。默认：**7**。与 `--start`/`--end` 互斥。 |
| `--start <iso-date>` / `--end <iso-date>` | 显式时间范围，例如 `--start 2026-04-01 --end 2026-04-15`。 |
| `--platform <ios\|android>` | 仅查看单一平台。省略则查看该组的所有平台。 |
| `--json` | 机器可读输出。隐含 `--non-interactive`。 |
| `--non-interactive` | 编写脚本时必填。 |

### JSON 输出结构

顶层包含 `groupId`、`timespan`（`start`、`end`、`daysBack`），以及 `platforms[]`（每个已发布平台一条）。每个平台条目包含 `updateId`、`totals`（`uniqueUsers`、`installs`、`failedInstalls`、`crashRatePercent`）、`payload`（`launchAssetCount`、`averageUpdatePayloadBytes`），以及一个 `daily[]` 时间序列，包含 `{ date, installs, failedInstalls }`。

完整的 Schema 和字段参考，请参阅 [references/update-insights-schema.md](./references/update-insights-schema.md)。

健康评估时关注的关键字段：

- `platforms[].totals.crashRatePercent`，计算公式为 `failedInstalls / (installs + failedInstalls) * 100`。当没有安装时为 0。
- `platforms[].totals.installs` 与 `uniqueUsers` 提供采用情况信号。
- `platforms[].daily` 是一个时间序列，可用于发现突发的失败激增。

### 错误

- `Could not find any updates with group ID: "<id>"` — 组不存在或你没有访问权限。
- `Update group "<id>" has no ios update (available platforms: android)` — 使用了 `--platform ios`，但该组并未发布到 iOS。
- `EAS Update insights is not supported by this version of eas-cli. Please upgrade ...` — 服务端弃用了 CLI 所依赖的某个字段。请运行 `npm install -g eas-cli@latest`。

## `eas update:view <groupId> --insights`

将标准的 `update:view` 输出与同样的按平台 insights 合并展示。

```bash
# 人类可读格式
eas update:view 03d5dfcf-... --insights
eas update:view 03d5dfcf-... --insights --days 30

# JSON：包装为 { updates: [...], insights: {...} }
eas update:view 03d5dfcf-... --json --insights
```

如果不传 `--insights`，`update:view` 的行为与以往完全相同 —— 对现有调用方没有 JSON 结构变化。`--days` / `--start` / `--end` 这些标志仅在设置了 `--insights` 时生效；单独传入它们会报错。

## `eas channel:insights --channel <name> --runtime-version <version>`

按渠道展示 Embedded 构建与 OTA 更新各有多少用户，以及哪些更新占据了最多流量。必须从 Expo 项目目录下运行。

### 基本用法

```bash
eas channel:insights --channel production --runtime-version 1.0.6
```

### 标志

| 标志 | 说明 |
|---|---|
| `--channel <name>` | **必填。** 渠道名称（例如 `production`、`staging`）。 |
| `--runtime-version <version>` | **必填。** 必须与发布时所使用的值完全一致。可在 `update:list` 的 `runtimeVersion` 中查询。 |
| `--days <N>` | 回溯 N 天。默认：**7**。 |
| `--start` / `--end` | 显式时间范围，与 `update:insights` 一致。 |
| `--json` / `--non-interactive` | 机器可读输出。 |

### JSON 输出结构

顶层包含 `channel`、`runtimeVersion`、`timespan`、`embeddedUpdateTotalUniqueUsers`、`otaTotalUniqueUsers`、`mostPopularUpdates[]`（每条包含 `rank`、`groupId`、`message`、`platform`、`totalUniqueUsers`）、`cumulativeMetricsAtLastTimestamp[]`，以及图表形态的 `uniqueUsersOverTime` 和 `cumulativeMetricsOverTime` 对象（包含 `labels` 和 `datasets`）。

完整的 Schema 和字段参考，请参阅 [references/channel-insights-schema.md](./references/channel-insights-schema.md)。

关键字段：

- `embeddedUpdateTotalUniqueUsers` 表示正在运行 Embedded（二进制内置）构建的用户数。
- `mostPopularUpdates[]` 是按 `totalUniqueUsers` 排序的更新列表。**注意**：这是服务端返回的 top-N；`otaTotalUniqueUsers` 是该列表的合计值，当存在超过 top-N 的活跃更新时，可能会低估真实的 OTA 触达量。
- `uniqueUsersOverTime` 与 `cumulativeMetricsOverTime` 是用于绘图的每日数据序列。

### 错误

- `Could not find channel with the name <name>` — 名称拼写错误或账号错误。
- 表格中显示 "No update launches recorded" / JSON 中 `mostPopularUpdates` 为空 — 该渠道 + 运行时下尚无 OTA 更新被启动。通常意味着该渠道仍然只提供 Embedded 构建。

## 常见工作流

### 验证我刚刚发布的更新是健康的

```bash
# 1. 获取 production 上最新一次发布
GROUP_ID=$(eas update:list --branch production --json --non-interactive \
  | jq -r '.currentPage[0].group')

# 2. 留出一段时间让其被采用（数分钟到数小时），然后检查崩溃率
eas update:insights "$GROUP_ID" --json --non-interactive \
  | jq '.platforms[] | {platform, installs: .totals.installs, crashRate: .totals.crashRatePercent}'
```

跨平台以及与历史版本比较 `crashRate`；突发的飙升或不对称表现（一端平台飙升、另一端平稳）是值得排查的信号。

### 对比两个渠道的采用情况

```bash
for channel in production staging; do
  echo "--- $channel ---"
  eas channel:insights --channel "$channel" --runtime-version 1.0.6 --json --non-interactive \
    | jq '{
        channel,
        embedded: .embeddedUpdateTotalUniqueUsers,
        ota: .otaTotalUniqueUsers,
        topUpdate: .mostPopularUpdates[0]
      }'
done
```

### 检测过去 24 小时内的灰度回归

```bash
eas update:insights "$GROUP_ID" --days 1 --json --non-interactive \
  | jq '.platforms[] | select(.totals.crashRatePercent > 1)'
```

### 为发布说明汇总更新组指标

```bash
eas update:view "$GROUP_ID" --insights --days 30
```

人类可读的更新组详情，外加 30 天内按平台统计的启动/失败数据 —— 适合直接粘贴到更新日志或事件复盘中。

## 输出提示

- 将 JSON 通过 `jq` 管道处理；Payload 的结构便于过滤。
- `--json` 隐含 `--non-interactive`，但同时显式传入两者对脚本更友好。
- `daily[].date` 中的日期为 UTC ISO 时间戳；人类可读的表格将其格式化为 `YYYY-MM-DD`（UTC）。
- CLI 表格中使用 "Launches" / "Crashes"，而 JSON 中使用 `installs` / `failedInstalls`。同一字段，仅展示名不同。

## 局限性

- **跨平台独立用户数** 可能会重复计算同时在 iOS 与 Android 上运行同一发布的用户。同样的注意事项也适用于 channel insights 中的 `otaTotalUniqueUsers`，它是 `mostPopularUpdates` 的合计值。
- **新发布的更新** 可能在短时间内显示为 0，因为指标管道尚未来得及追上。
- **Installs 指的是下载，而非启动**：`installs` / "Launches" 字段统计的是下载了 manifest 与 launch asset 的用户。一次确认运行只有在用户的*下一次*更新检查时（通常最多 24 小时后，取决于应用的更新策略）才会被记录。因此指标会略滞后于真实状态。
- **崩溃为自我上报**：`failedInstalls` / "Crashes" 统计的是在安装/启动过程中出错并在下一次更新检查时上报的更新。那些不会触发更新请求的崩溃（例如恢复前的进程被杀死）不会计入。