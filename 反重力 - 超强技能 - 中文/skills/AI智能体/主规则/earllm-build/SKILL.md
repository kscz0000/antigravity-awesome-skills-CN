---
name: earllm-build
description: "构建、维护和扩展 EarLLM One Android 项目——一个通过语音管道将蓝牙耳机连接到 LLM 的 Kotlin/Compose 应用。"
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- android
- kotlin
- bluetooth
- llm
- voice
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# EarLLM One — 构建与维护

## 概述

构建、维护和扩展 EarLLM One Android 项目——一个通过语音管道将蓝牙耳机连接到 LLM 的 Kotlin/Compose 应用。

## 何时使用此技能

- 当用户提到 "earllm" 或相关主题时
- 当用户提到 "earbudllm" 或相关主题时
- 当用户提到 "earbud app" 或相关主题时
- 当用户提到 "voice pipeline kotlin" 或相关主题时
- 当用户提到 "bluetooth audio android" 或相关主题时
- 当用户提到 "sco microphone" 或相关主题时

## 何时不使用此技能

- 任务与 earllm 构建无关
- 更简单、更具体的工具可以处理该请求
- 用户需要无领域专业知识的通用帮助

## 工作原理

EarLLM One 是一个多模块 Android 应用（Kotlin + Jetpack Compose），从蓝牙耳机捕获语音，转录后发送到 LLM，并将响应语音播放回来。

## 项目位置

`C:\Users\renat\earbudllm`

## 模块依赖图

```
app ──→ voice ──→ audio ──→ core-logging
  │       │
  ├──→ bluetooth ──→ core-logging
  └──→ llm ──→ core-logging
```

## 模块与关键文件

| 模块 | 用途 | 关键文件 |
|------|------|----------|
| **core-logging** | 结构化日志、性能追踪 | `EarLogger.kt`、`PerformanceTracker.kt` |
| **bluetooth** | BT 发现、配对、A2DP/HFP 配置文件 | `BluetoothController.kt`、`BluetoothState.kt`、`BluetoothPermissions.kt` |
| **audio** | 音频路由（SCO/BLE）、捕获、耳机按键 | `AudioRouteController.kt`、`VoiceCaptureController.kt`、`HeadsetButtonController.kt` |
| **voice** | STT（SpeechRecognizer + Vosk 存根）、TTS、管道 | `SpeechToTextController.kt`、`TextToSpeechController.kt`、`VoicePipeline.kt` |
| **llm** | LLM 接口、存根、OpenAI 兼容客户端 | `LlmClient.kt`、`StubLlmClient.kt`、`RealLlmClient.kt`、`SecureTokenStore.kt` |
| **app** | UI、ViewModel、Service、设置、所有屏幕 | `MainViewModel.kt`、`EarLlmForegroundService.kt`、6 个 Compose 屏幕 |

## 构建配置

- **SDK**: minSdk 26, targetSdk 34, compileSdk 34
- **构建工具**: AGP 8.2.2, Kotlin 1.9.22, Gradle 8.5
- **Compose BOM**: 2024.02.00
- **关键依赖**: OkHttp, AndroidX Security (EncryptedSharedPreferences), DataStore, Media

## 目标硬件

| 设备 | 型号 | 关键详情 |
|------|------|----------|
| 手机 | Samsung Galaxy S24 Ultra | Android 14, One UI 6.1, Snapdragon 8 Gen 3 |
| 耳机 | Xiaomi Redmi Buds 6 Pro | BT 5.3, A2DP/HFP/AVRCP, ANC, LDAC |

## 关键技术事实

这些是来自官方文档和设备测试的验证事实。在决策时将其视为基本真理：

1. **蓝牙 SCO 在大多数设备上仅限于 8kHz 单声道输入**。部分设备支持 16kHz mSBC。BLE Audio（Android 12+, `TYPE_BLE_HEADSET = 26`）支持最高 32kHz 立体声。可用时始终优先使用 BLE Audio。

2. **`startBluetoothSco()` 自 Android 12 (API 31) 起已弃用。** 改用 `AudioManager.setCommunicationDevice(AudioDeviceInfo)` 和 `clearCommunicationDevice()`。项目已在 `AudioRouteController.kt` 中实现两条路径。

3. **Samsung One UI 7/8 存在已知的 HFP 损坏 bug**，A2DP 播放会损坏 SCO 链路。应用通过静音检测和自动回退到手机内置麦克风来处理此问题。

4. **Redmi Buds 6 Pro 触控设置必须在小米耳机配套应用中设为"默认"（播放/暂停）**。如果设为 ANC 或自定义功能，事件将由耳机内部处理，永远不会传递到 Android。

5. **Android 14+ 需要 `FOREGROUND_SERVICE_MICROPHONE` 权限**，并在服务声明中设置 `foregroundServiceType="microphone"`。`RECORD_AUDIO` 必须在 `startForeground()` 之前授予。

6. **`VOICE_COMMUNICATION` 音频源启用 AEC（声学回声消除）**，这对防止 TTS 音频输出反馈到 STT 麦克风输入至关重要。切勿在未理解回声影响的情况下更改此源。

7. **切勿在通过 SCO 录音的同时播放 TTS（A2DP）。** 正确序列是：停止播放 → 切换到 HFP → 录音 → 切换到 A2DP → 播放响应。

## 数据流

```
耳机按键点击
  → MediaSession (HeadsetButtonController)
  → TapAction.RECORD_TOGGLE
  → VoicePipeline.toggleRecording()
  → VoiceCaptureController 捕获 PCM (16kHz 单声道)
  → stopRecording() 返回 ByteArray
  → SpeechToTextController.transcribe(pcmData)
  → LlmClient.chat(messages)
  → TextToSpeechController.speak(response)
  → 通过 A2DP 输出音频到耳机
```

## 添加新功能

1. 确定受影响的模块
2. 先阅读这些模块中的现有代码
3. 遵循 StateFlow 模式——通过 `MutableStateFlow` / `StateFlow` 暴露状态
4. 如果功能需要 UI 集成，更新 `MainViewModel.kt`
5. 在模块的 `src/test/` 目录添加单元测试
6. 如果功能改变了行为，更新文档

## 修改音频捕获

- `VoiceCaptureController.kt` 处理 16kHz 单声道 PCM 录音
- WAV 头使用十六进制字节值（而非字符字面量）以避免 shell 引号问题
- VU 表：RMS 计算 → dB 转换 → 归一化到 0-1 范围
- 缓冲区大小：`getMinBufferSize().coerceAtLeast(4096)`

## 更改蓝牙行为

- `BluetoothController.kt` 管理发现、配对、配置文件代理
- 耳机检测使用名称启发式："buds"、"earbuds"、"tws"、"pods"、"ear"
- 始终处理蓝牙经典和 BLE Audio 两条路径

## 修改 LLM 集成

- `LlmClient.kt` 定义接口——保持通用
- `StubLlmClient.kt` 用于离线测试（500ms 模拟延迟）
- `RealLlmClient.kt` 使用 OkHttp 调用 OpenAI 兼容 API
- API 密钥存储在 `SecureTokenStore.kt`（EncryptedSharedPreferences）

## 生成构建产物

代码更改后，重新生成 ZIP：
```powershell

## 从项目根目录

powershell -Command "Remove-Item 'EarLLM_One_v1.0.zip' -Force -ErrorAction SilentlyContinue; Compress-Archive -Path (Get-ChildItem -Exclude '*.zip','_zip_verify','.git') -DestinationPath 'EarLLM_One_v1.0.zip' -Force"
```

## 运行测试

```bash
./gradlew test --stacktrace          # 单元测试
./gradlew connectedAndroidTest       # 仪器测试（需要设备）
```

## 第二阶段路线图

- 通过耳机与 LLM 进行实时流式语音对话
- 智能助手：将语音分类为会议、购物清单、备忘录、邮件
- Vosk 离线 STT 集成（当前为存根）
- 唤醒词检测，避免持续保持 SCO 开启
- 流式 TTS（Android 内置 TTS 不支持流式）

## STT 引擎参考

| 引擎 | 大小 | WER | 流式 | 最佳用途 |
|------|------|-----|------|----------|
| Vosk small-en | 40 MB | ~10% | 是 | 实时移动端 |
| Vosk lgraph | 128 MB | ~8% | 是 | 更高准确率 |
| Whisper tiny | 40 MB | ~10-12% | 否（批处理） | 话语后润色 |
| Android SpeechRecognizer | 0 MB | 变化 | 是 | 在线，无额外依赖 |

## 最佳实践

- 提供清晰、具体的项目背景和需求
- 在应用到生产代码前审查所有建议
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其领域专业范围之外的任务
- 在不了解具体背景的情况下应用建议
- 未提供足够的项目背景以进行准确分析

## 局限性
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
