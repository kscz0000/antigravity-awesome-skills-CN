# EAS Observe 指标 —— 解读速查表

用于阅读 EAS Observe 仪表板和 CLI 输出的快速参考。

> 来源：https://docs.expo.dev/eas/observe/reference/metrics/ —— 这是指标的权威参考。获取最新指南、完整的文字定义、优化建议与原理，请查阅此页面。

所有时长均以秒为单位。数据保留 90 天。所有时长均以秒为单位。默认情况下，每个安装都会上报其所有事件。事件量较大的应用可以通过 `configure({ sampleRate })` 选择开启按安装采样。参见[采样](https://docs.expo.dev/eas/observe/configuration/#sampling)。

## 目标阈值

| 指标 | 完整名称 | 目标 | 是否自动采集？ |
|---|---|---|---|
| 冷启动（Cold launch） | `expo.app_startup.cold_launch_time` | **< 1.5s** | 是（仅原生层 —— JS 代码不影响） |
| 热启动（Warm launch） | `expo.app_startup.warm_launch_time` | **< 0.5s** | 是（由操作系统决定是热启动还是冷启动） |
| Bundle 加载（Bundle load） | `expo.app_startup.bundle_load_time` | **< 0.3s** | 是（JS 加载与求值，在 `runApplication` 之前） |
| 首次渲染时间（TTR） | `expo.app_startup.ttr` | **< 2s**（含冷启动） | 当根组件被 `AppMetricsRoot`（SDK 55）/ `ObserveRoot`（SDK 56+）包裹时自动采集 |
| 可交互时间（TTI） | `expo.app_startup.tti` | **< 3s**（含冷启动） | **否** —— 屏幕真正可用时调用一次 `markInteractive()` |

TTR 和 TTI 都是从**原生启动开始**经过 React 渲染来测量的，因此冷启动部分会计入其中。

## 解读 TTI 事件（frameRate 参数）

每个 TTI 事件携带三个帧率参数。这些参数高低值的组合模式能告诉你看到的是*哪种类型*的慢。

| 参数 | 定义 | 含义 |
|---|---|---|
| `expo.frameRate.slowFrames` | 时长 ≥ 17ms 的帧数 | 启动期间主线程持续繁忙（繁重的布局、同步桥接调用、过多组件渲染） |
| `expo.frameRate.frozenFrames` | 时长 ≥ 700ms 的帧数 | 硬卡顿。启动期间哪怕出现一次都是严重问题（同步 I/O、大型 JSON 解析、阻塞型网络调用） |
| `expo.frameRate.totalDelay` | 帧超出目标时长的累计总时间（秒） | 最佳单一的"流畅度"指标 —— 与 TTI 进行对比 |

**诊断模式：**

- **TTI 高 + totalDelay 低** → 慢但流畅。启动序列本身很长。应优化包体积、数据获取瀑布流和初始化链路。
- **TTI 高 + totalDelay 高 + slowFrames 多** → 主线程争用。应将工作移出主线程，简化初始渲染树。
- **TTI 高 + totalDelay 高 + 存在 frozenFrames** → 存在严重的阻塞。需要查找同步 I/O、大型 JSON 解析或阻塞型网络调用。

## 上报注意事项

- **调试构建**（原生调试或 JS bundle 中 `__DEV__` 为 true）**不会**上报指标，除非设置 `configure({ dispatchInDebug: true })`。
- `environment` 标签（默认值为 `process.env.NODE_ENV`）仅为元数据，**不会**单独用于控制上报。
- 离线事件在设备本地缓存，并在应用进入后台或调用 `Observe.dispatchEvents()` 时刷新上报。

## 交叉引用

- 完整的指标定义与优化指南：https://docs.expo.dev/eas/observe/reference/metrics/
- 设置步骤（`AppMetricsRoot` / `ObserveRoot`、`markInteractive`）：参见 [`./setup.md`](./setup.md)。
- 通过 EAS CLI 查询指标：参见 [`./queries.md`](./queries.md)。
