Journey 是以 XML 形式指定的 Android 应用行为测试，由一组 `<action>` 元素组成。例如：
```xml
<journey name="My Journey">
   <description>
      A sample journey to illustrate the format
   </description>
   <actions>
     <action>
       Tap the "Home" icon
     </action>
     <action>
       Verify that the app is on its Home screen
     </action>
   </actions>
</journey>
```

评估 journey 时，按顺序依次处理 `<actions>` 列表，逐个评估每个 `<action>` 块。
若 `<actions>` 列表中的所有元素均成功，则该 journey 成功。

Journey 是应用的一个测试用例。Journey 的 XML 是事实之源；如果应用与 journey 不一致，则视为应用失败。
此外，如果应用退出、崩溃或卡死，journey 评估立即停止并判定为失败。

**重要** — 严格按照所写的步骤执行每一步，且每一步独立评估！如果某条 action 指示 `"tap the first search result"`（点击第一个搜索结果），
则必须找到搜索结果并点击第一个。即使你认为已经理解了 action 的意图，也必须如此操作。

## 执行操作

某些 `<action>` 元素指定要在运行中的 Android 应用上执行的 UI 交互。请执行该交互，并验证应用没有崩溃或出现异常行为。这是 `<action>` 应执行的 *唯一* 验证。

如果无法按指定方式执行该交互，则 journey 失败。
示例：
```xml
<action>Click the red button</action>
```
如果判断当前 UI 中不存在红色按钮，则 journey 失败。

如果某条 `<action>` 的文本指定了一系列动作，请将其拆分为子动作并逐个评估：
示例：
```xml
<action>Search for soda and add the first result to the cart</action>
```
应将其评估为：
```xml
<action>Search for soda</action>
<action>Add the first result to the cart</action>
```

如果某条 `<action>` 包含的内容并非 UI 交互规范，请提醒用户该 journey 格式错误，并提前退出，同时说明具体错误。

## 验证期望

以 "check" 或 "verify" 开头的 `<action>` 元素指定对应用当前状态的期望。请确定应用的当前状态，并检查是否满足期望。

通过检查设备当前屏幕（不与之交互）来确定应用的当前状态。
示例：
```xml
<action>Check if "Switch 2" is visible on the screen</action>
```
这仅需检查当前屏幕，无需滚动或交互。如果 "Switch 2" 当前不可见，则该 action 失败。

如果未满足期望，请将该 `<action>` 标记为失败，并结束 journey 评估。单个 `<action>` 可包含多项期望。
示例：
```xml
<action>Verify that the app is on the Home screen, the Home icon is blue, and the temperature is displayed</action>
```
若以下任何一项为 false，则该 `<action>` 失败：
- 应用处于主屏幕
- 存在一个 Home 图标，且为蓝色
- 显示了温度

## 处理失败

运行 journey 时，将其作为一项测试进行评估。失败是可接受的，也常常是预期之中的。首要任务是正确报告失败。

尽量减少调试与排错；假定工具每次向你展示的输出都是正确的。目标是判断 *当前* Android 应用能否正确处理 journey 中列出的 *当前* 步骤。关于 bug 修复、澄清或其他改进的建议应留到 journey 评估总结中给出。

## 总结输出

对所评估的每一条 `<action>`，输出 JSON 描述结果。

```json
{
  "journey": "The name of the journey",
  "results": [
    {
      // A string containing the full text of the <action> 
      "action": "Click the blue button",
      // "PASSED" if the instruction was evaluated, "FAILED" if the instruction could not be evaluated, or "SKIPPED" if journey evaluation ended early because an instruction failed 
      "status": "PASSED", 
      // A list of the ADB commands executed while evaluating the instruction
      "commands": [ "adb input swipe 490 200 500 500 500", "adb input tap 45 920" ],  
      // Failure reasons, feedback, or other useful information 
      "comment": "The journey step doesn't specify that the button requires scrolling to see"
    },
    {
      "action": "The home screen is shown", 
      "status": "FAILED", 
      "comment": "The settings page was shown"
    }
  ]
}
```