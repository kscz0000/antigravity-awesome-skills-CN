# 工具

执行 `android layout --help` 与 `android screen --help` 查看帮助。

## UI 转储

`android layout` 返回当前屏幕上 UI 元素的扁平 JSON 列表。
`android layout --diff` 返回自上次调用 `layout` 或 `layout --diff` 以来发生变化的 UI 元素的扁平 JSON 列表。

每个 JSON 对象表示 Android 应用中的一个 UI 元素，可能包含以下属性：
- `text` - 元素包含的任何字面文本
- `resourceId` - 用于引用该元素的 Android 资源 ID
- `contentDesc` - 供无障碍工具使用的 UI 元素描述
- `interactions` - 元素支持的用户交互集合，可能包含以下一项或多项：`checkable`、`clickable`、`focusable`、`scrollable`、`long-clickable`、`password`
- `state` - 元素所处的状态集合，可能包含 `checked`、`focused`、`selected` 中的一项或多项
- `bounds` - 元素边界矩形在屏幕上的坐标，格式为 `[min X,min Y][max X, max Y]`
- `center` - 元素中心在屏幕上的坐标，格式为 `[x,y]`
- `off-screen` - 若为 true，表示该元素存在于 UI 层级中但不可见，可能需要滚动才能查看。

应将 `layout` 作为检查 Android 应用的主要手段。使用 `layout --diff` 来聚焦变化并保持较小的上下文。
示例：在计算器中输入数字时，使用 `layout --diff` 仅输出数字显示区域的元素。

`layout` 在应用显示 WebView 或动画时可能失败；在这种情况下，请使用 `android screen --annotate` 来检查应用。
此类失败在离开当前屏幕后通常会自行恢复。

## 截屏

`android screen capture -o <file path>` 将当前设备屏幕的 PNG 保存到 `<file path>`

应将 `screen capture` 作为检查 Android 应用的次要手段
示例：
- 理解屏幕上图像的内容
- 查看 `WebView`（网页内容不一定出现在 UI 转储中）
- 通过外观查找某个 UI 元素

**重要**：在使用 `android screen` 后、进行任何其他操作之前，必须 *目视* 检查返回的 PNG 图像。

## 带标注的截屏

`android screen capture --annotate -o <file path>`
`android screen resolve --screen <path> --string <string>`

`--annotate` 命令会在 UI 元素周围添加数字标签和边界框。使用此命令来定位那些在 `layout` 输出中无法定位的 UI 元素。

**重要**：在使用 `android --annotate` 时，必须 *目视* 检查生成的 PNG 文件。

要在输入命令中引用这些标签，请使用 `screen resolve` 将标签转换为坐标：

`android screen resolve --screen <file path> --string "#3"` 返回 `<x 坐标 of region 3> <y 坐标 of region 3>`

为节省轮次，可以组合 shell 命令：

`adb shell input $(android screen resolve --screen screen.png --string "tap #34")`

此命令会点击来自 `screen.png` 中的 #34 区域。

## 输入

使用 `adb shell input` 与 Android 设备交互。
请参考元素的 `"interactions"` 属性，了解可在该元素上执行的交互。

通过 UI 元素的 `center` 坐标或 `bounds` 坐标与其交互：
```json
{
  "key": -248568265,
  "class": "android.widget.Button",
  "bounds": "[138,9][167,38]",
  "center": "[152,23]"
}
```
若要点击此按钮，可执行 `adb shell input tap 152 23`。此操作会点击按钮中心。

```json
{
  "key": 12487234,
  "class": "com.example.ui.ScrollableList",
  "bounds": "[100,200][400,600]",
  "center": "[250,400]"
}
```
若要在该列表上下滑，可执行 `adb shell input swipe 250 400 250 200 500`。此操作会从中心向顶部滑动，持续 500ms。

# Android 交互规则
1. 在输入文本之前，请始终确保文本输入字段的 `"state"` 列表中包含 `"focused"`
2. 如果元素的 `"interactions"` 列表中包含 `"scrollable"`，在查找缺失的 UI 元素时可尝试滚动该元素
3. 执行滑动输入时请始终缓慢滚动。在 `adb shell input swipe <x1> <y1> <x2> <y2> [duration(ms)]` 中，duration 是 `swipe` 之后可选的第 5 个参数（即 `input` 工具的第 6 个参数）。
4. 内容加载可能需要时间；如果执行某个操作后 `layout` 缺少信息，请等待几秒，然后执行 `layout --diff` 查看是否有变化。