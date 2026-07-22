---
name: pipecat-friday-agent
description: "使用 Pipecat、Gemini 和 OpenAI 构建低延迟的钢铁侠风格战术语音助手（F.R.I.D.A.Y.）。当用户要求构建语音助手、集成语音AI或创建钢铁侠主题应用时使用。"
category: voice-agents
risk: safe
source: community
date_added: "2026-03-10"
tags: [pipecat, voice, gemini, openai, python]
tools: [pipecat]
---

# Pipecat Friday Agent

## 概述

本技能提供构建 **F.R.I.D.A.Y.**（Replacement Integrated Digital Assistant Youth）的蓝图——一个受钢铁侠电影中战术AI启发的本地语音助手。它使用 **Pipecat** 框架编排低延迟管道：
- **STT**：OpenAI Whisper（`whisper-1`）或 `gpt-4o-transcribe`
- **LLM**：Google Gemini 2.5 Flash（通过兼容性适配层）
- **TTS**：OpenAI TTS（`nova` 语音）
- **传输层**：本地音频（硬件麦克风/扬声器）

## 使用场景

- 需要构建实时对话式语音代理时
- 使用 Pipecat 框架进行管道式 AI 开发时
- 需要将多个提供商（Google 和 OpenAI）集成到单一语音循环时
- 构建钢铁侠主题或战术主题的语音应用时

## 工作原理

### 步骤1：安装依赖

需要安装 Pipecat 框架及其服务提供商：
```bash
pip install pipecat-ai[openai,google,silero] python-dotenv
```

### 步骤2：配置环境

创建 `.env` 文件，填入 API 密钥：
```env
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
```

### 步骤3：运行代理

执行提供的 Python 脚本启动界面：
```bash
python scripts/friday_agent.py
```

## 核心概念

### 管道架构
代理遵循线性管道：`Mic -> VAD -> STT -> LLM -> TTS -> Speaker`。与端到端语音到语音模型不同，这种设计允许对每个阶段进行精细控制。

### Google 兼容性适配层
由于 Google 的 Gemini API 消息格式与 OpenAI 标准不同（Pipecat 聚合器期望的是后者），脚本包含 `GoogleSafeContext` 和 `GoogleSafeMessage` 类来弥合差异。

## 最佳实践

- ✅ **使用 Silero VAD**：对本地硬件具有鲁棒性，防止背景噪音触发 LLM。
- ✅ **简洁提示词**：战术代理应给出简短、数据密集的响应以最小化延迟。
- ✅ **采样率匹配**：OpenAI TTS 输出 24kHz；确保 `audio_out_sample_rate` 匹配以避免音频变调或变慢。
- ❌ **不要使用礼貌性填充语**：避免"你好，今天有什么可以帮您的？"，改用"系统就绪，等待指令。"

## 故障排除

- **问题**：音频卡顿或延迟。
  - **解决方案**：检查 `OUTPUT_DEVICE` 索引。运行 `test_audio_output.py` 脚本找到操作系统对应的正确硬件索引。
- **问题**：消息格式"Validation error"。
  - **解决方案**：确保 `GoogleSafeContext` 适配层正确地将 OpenAI 风格的字典转换为 Gemini 风格的 schema。

## 相关技能

- `@voice-agents` - 语音 AI 通用原则。
- `@agent-tool-builder` - 为 Friday 代理添加工具（搜索、灯光等）。
- `@llm-architect` - 优化 LLM 层。

## 限制条件
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
