---
name: macos-screen-recorder
description: "macOS 屏幕录制器，通过 ScreenCaptureKit 捕获主显示器及系统音频——无需 BlackHole/回环驱动，无需 sudo，仅需标准的屏幕录制权限。CLI 驱动；填补 QuickTime 和 `screencapture -v` 无法覆盖的无头屏幕录制+系统音频空白。触发词：macOS屏幕录制、系统音频录制、screencapturekit、CLI录屏、屏幕录制、screen recording、sck-record"
risk: critical
source: community
source_type: community
source_repo: connerkward/macos-screen-recorder-system-audio
date_added: "2026-06-16"
author: Conner K Ward
license: MIT
tags:
  - macos
  - screen-recording
  - system-audio
  - screencapturekit
  - cli
  - swift
tools:
  - claude-code
  - antigravity
  - cursor
  - gemini-cli
  - codex-cli
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "屏幕/音频/输入捕获需要敏感的 macOS 权限；请勿纳入插件安全包。"
    docs: SKILL.md
---
## 何时使用

当你需要在 macOS 上通过 CLI 编写屏幕录制脚本并包含系统声音时使用（演示、捕获、语音演示录制）——这是 QuickTime 和 `screencapture -v` 在没有虚拟音频设备的情况下无法覆盖的场景。

_来源：[connerkward/macos-screen-recorder-system-audio](https://github.com/connerkward/macos-screen-recorder-system-audio) (MIT)。_

# macOS 屏幕录制器 (sck-record)

`sck-record.swift` → 编译后的 `sck-record`（二进制文件已被 gitignore；由 `setup-machine` 构建，或通过
`swiftc -O sck-record.swift -o sck-record` 编译）。通过 ScreenCaptureKit 录制主显示器 + 系统音频。

```
./sck-record <out.mp4> <seconds>
```

**核心差异化：** 通过 CLI 录制系统音频，**零安装**——无需
BlackHole / 回环虚拟设备，无需 sudo；仅需标准的屏幕录制权限
（对调用它的应用授予一次即可）。它*不是*一个通用的"比 OBS/Screen
Studio 更好"的工具——它精确填补的是无头 CLI + 系统音频的空白。

`sck-record` 是原始捕获原语——它只负责录制，别无其他。若要在录制后
润色视频（空闲加速、自动缩放、按键标记、光标平滑、
竖屏导出），请配合
[screenstudio-alternative-skill](https://github.com/connerkward/screenstudio-alternative-skill)：
使用 `sck-record --no-cursor <out.mp4> <seconds>` 录制，然后对其生成的 mp4
运行后处理流程。（自动缩放和按键叠加还需要在录制*期间*
捕获的输入事件日志，该技能会提供；`sck-record` 的
像素数据本身可覆盖空闲加速、光标平滑和竖屏导出。）

## 局限性

- 仅限 macOS；依赖 ScreenCaptureKit 和用户的屏幕录制权限。
- 录制器捕获原始显示器画面和系统音频，但本身不提供编辑、自动缩放、字幕或社交格式润色功能。
- 输入事件叠加需要在录制期间单独捕获的事件日志；仅凭像素数据无法还原按键或精确的点击元数据。
