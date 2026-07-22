---
name: android_ui_verification
description: 使用 ADB 在 Android 模拟器上进行自动化端到端 UI 测试和验证。触发词：Android UI测试、ADB自动化测试、模拟器UI验证、React Native测试、Android端到端测试、UI自动化、ADB交互测试
risk: safe
source: community
date_added: "2026-02-28"
---

# Android UI 验证技能

本技能提供了一种系统化的方法，使用 ADB 命令在 Android 模拟器上测试 React Native 应用程序。它支持自主交互、状态验证和视觉回归检查。

## 使用场景
- 验证 React Native 或原生 Android 应用中的 UI 变更。
- 自主调试布局问题或交互 bug。
- 当手动测试太慢时确保功能正常。
- 为 PR 文档捕获自动化截图。

## 🛠 前置条件
- Android 模拟器正在运行。
- `adb` 已安装并在 PATH 中。
- 应用处于调试模式以便访问 logcat。

## 🚀 工作流程

### 1. 设备校准
在交互之前，始终验证屏幕分辨率以确保点击坐标准确。
```bash
adb shell wm size
```
*注意：布局通常会缩放。使用返回的物理尺寸作为坐标计算的基础。*

### 2. UI 检查（状态发现）
使用 `uiautomator` dump 查找 UI 元素（按钮、输入框）的确切边界。
```bash
adb shell uiautomator dump /sdcard/view.xml && adb pull /sdcard/view.xml ./artifacts/view.xml
```
在 `view.xml` 中搜索 `text`、`content-desc` 或 `resource-id`。`bounds` 属性 `[x1,y1][x2,y2]` 定义了可点击区域。

### 3. 交互命令
- **点击**：`adb shell input tap <x> <y>`（使用元素边界的中心点）。
- **滑动**：`adb shell input swipe <x1> <y1> <x2> <y2> <duration_ms>`（用于滚动）。
- **文本输入**：`adb shell input text "<message>"`（注意：对特殊字符的支持有限）。
- **按键事件**：`adb shell input keyevent <code_id>`（例如，66 表示回车键）。

### 4. 验证与报告
#### 视觉验证
交互后捕获截图以确认 UI 变更。
```bash
adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./artifacts/test_result.png
```

#### 分析验证
实时监控 JS 控制台日志以检测错误或记录成功信息。
```bash
adb logcat -d | grep "ReactNativeJS" | tail -n 20
```

#### 清理
始终将生成的文件存储在 `artifacts/` 文件夹中，以满足项目组织规范。

## 💡 最佳实践
- **等待动画**：在交互和验证之间始终添加短暂延迟（如 1-2 秒）。
- **中心点击**：计算 `[x1,y1][x2,y2]` 的算术平均值以获得最可靠的点击目标。
- **日志标记**：在代码中使用独特的日志消息（如 `✅ Action Successful`）使 `grep` 验证更容易。
- **快速失败**：如果 `uiautomator dump` 失败或未找到预期文本，停止并排查问题，而不是盲目点击。

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，停止并请求澄清。
