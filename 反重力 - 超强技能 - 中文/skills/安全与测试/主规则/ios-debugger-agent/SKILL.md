---
name: ios-debugger-agent
description: 使用 XcodeBuildMCP 在已启动的模拟器上调试当前 iOS 项目。触发词：iOS调试、模拟器调试、XcodeBuildMCP、调试iOS应用、模拟器运行
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# iOS Debugger Agent

## 概述
使用 XcodeBuildMCP 在已启动的 iOS 模拟器上构建并运行当前项目的 scheme，与 UI 交互，并捕获日志。模拟器控制、日志和视图检查优先使用 MCP 工具。

## 使用时机
- 用户要求在模拟器上运行、调试或检查 iOS 应用时。
- 需要通过 XcodeBuildMCP 进行模拟器 UI 交互、截图或获取运行时日志时。

## 核心工作流
除非用户要求更窄范围的操作，否则按以下顺序执行。

### 1) 发现已启动的模拟器
- 调用 `mcp__XcodeBuildMCP__list_sims`，选择状态为 `Booted` 的模拟器。
- 如果没有已启动的模拟器，请用户启动一个（除非用户要求，否则不要自动启动）。

### 2) 设置会话默认值
- 调用 `mcp__XcodeBuildMCP__session-set-defaults`，参数如下：
  - `projectPath` 或 `workspacePath`（取决于仓库使用哪个）
  - `scheme`：当前应用的 scheme
  - `simulatorId`：来自已启动设备的 ID
  - 可选：`configuration: "Debug"`、`useLatestOS: true`

### 3) 构建 + 运行（按需）
- 调用 `mcp__XcodeBuildMCP__build_run_sim`。
- **如果构建失败**，检查错误输出并重试（可选择 `preferXcodebuild: true`），或在尝试任何 UI 交互之前上报给用户。
- **构建成功后**，在继续 UI 交互之前，调用 `mcp__XcodeBuildMCP__describe_ui` 或 `mcp__XcodeBuildMCP__screenshot` 验证应用已启动。
- 如果应用已构建且仅需启动，使用 `mcp__XcodeBuildMCP__launch_app_sim`。
- 如果 bundle id 未知：
  1) `mcp__XcodeBuildMCP__get_sim_app_path`
  2) `mcp__XcodeBuildMCP__get_app_bundle_id`

## UI 交互与调试
在要求检查或与运行中的应用交互时使用。

- **描述 UI**：在点击或滑动前调用 `mcp__XcodeBuildMCP__describe_ui`。
- **点击**：`mcp__XcodeBuildMCP__tap`（优先使用 `id` 或 `label`；仅在必要时使用坐标）。
- **输入文本**：聚焦字段后使用 `mcp__XcodeBuildMCP__type_text`。
- **手势**：`mcp__XcodeBuildMCP__gesture` 用于常见滚动和边缘滑动。
- **截图**：`mcp__XcodeBuildMCP__screenshot` 用于视觉确认。

## 日志与控制台输出
- 启动日志：使用 app bundle id 调用 `mcp__XcodeBuildMCP__start_sim_log_cap`。
- 停止日志：`mcp__XcodeBuildMCP__stop_sim_log_cap`，然后总结重要日志行。
- 如需控制台输出，设置 `captureConsole: true` 并在需要时重新启动应用。

## 故障排除
- 如果构建失败，询问是否使用 `preferXcodebuild: true` 重试。
- 如果启动了错误的应用，确认 scheme 和 bundle id。
- 如果 UI 元素不可点击，在布局变化后重新运行 `describe_ui`。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少必要的输入、权限、安全边界或成功标准，停止并请求澄清。
