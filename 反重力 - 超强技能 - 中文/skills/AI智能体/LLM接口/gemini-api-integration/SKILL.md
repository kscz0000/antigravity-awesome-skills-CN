---
name: gemini-api-integration
description: "在项目中集成 Google Gemini API 时使用。涵盖模型选择、多模态输入、流式响应、函数调用和生产最佳实践。当用户要求'集成 Gemini API'、'使用 Gemini 模型'、'实现多模态输入'或'添加函数调用'时使用。"
risk: safe
source: community
date_added: "2026-03-04"
---

# Gemini API 集成

## 概述

本技能指导 AI 智能体将 Google Gemini API 集成到应用程序中——从基础文本生成到高级多模态、函数调用和流式响应用例。涵盖完整的 Gemini SDK 生命周期及生产级模式。

## 何时使用本技能

- 在 Node.js、Python 或浏览器项目中首次设置 Gemini API 时使用
- 实现多模态输入（文本 + 图像/音频/视频）时使用
- 添加流式响应以改善感知延迟时使用
- 使用 Gemini 实现函数调用/工具使用时使用
- 优化模型选择（Flash vs Pro vs Ultra）以平衡成本和性能时使用
- 调试 Gemini API 错误、速率限制或配额问题时使用

## 分步指南

### 1. 安装与设置

**Node.js / TypeScript:**
```bash
npm install @google/generative-ai
```

**Python:**
```bash
pip install google-generativeai
```

安全设置 API 密钥：
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 2. 基础文本生成

**Node.js:**
```javascript
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const result = await model.generateContent("Explain async/await in JavaScript");
console.log(result.response.text());
```

**Python:**
```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Explain async/await in JavaScript")
print(response.text)
```

### 3. 流式响应

```javascript
const result = await model.generateContentStream("Write a detailed blog post about AI");

for await (const chunk of result.stream) {
  process.stdout.write(chunk.text());
}
```

### 4. 多模态输入（文本 + 图像）

```javascript
import fs from "fs";

const imageData = fs.readFileSync("screenshot.png");
const imagePart = {
  inlineData: {
    data: imageData.toString("base64"),
    mimeType: "image/png",
  },
};

const result = await model.generateContent(["Describe this image:", imagePart]);
console.log(result.response.text());
```

### 5. 函数调用 / 工具使用

```javascript
const tools = [{
  functionDeclarations: [{
    name: "get_weather",
    description: "Get current weather for a city",
    parameters: {
      type: "OBJECT",
      properties: {
        city: { type: "STRING", description: "City name" },
      },
      required: ["city"],
    },
  }],
}];

const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro", tools });
const result = await model.generateContent("What's the weather in Mumbai?");

const call = result.response.functionCalls()?.[0];
if (call) {
  // Execute the actual function
  const weatherData = await getWeather(call.args.city);
  // Send result back to model
}
```

### 6. 多轮对话

```javascript
const chat = model.startChat({
  history: [
    { role: "user", parts: [{ text: "You are a helpful coding assistant." }] },
    { role: "model", parts: [{ text: "Sure! I'm ready to help with code." }] },
  ],
});

const response = await chat.sendMessage("How do I reverse a string in Python?");
console.log(response.response.text());
```

### 7. 模型选择指南

| 模型 | 适用场景 | 速度 | 成本 |
|-------|----------|-------|------|
| `gemini-1.5-flash` | 高吞吐量、成本敏感型任务 | 快 | 低 |
| `gemini-1.5-pro` | 复杂推理、长上下文 | 中 | 中 |
| `gemini-2.0-flash` | 最新快速模型、多模态 | 极快 | 低 |
| `gemini-2.0-pro` | 最强大、高级任务 | 慢 | 高 |

## 最佳实践

- ✅ **推荐：** 大多数任务使用 `gemini-1.5-flash`——速度快且性价比高
- ✅ **推荐：** 面向用户的聊天 UI 始终使用流式响应以降低感知延迟
- ✅ **推荐：** 将 API 密钥存储在环境变量中，切勿硬编码
- ✅ **推荐：** 对速率限制（429）错误实现指数退避
- ✅ **推荐：** 使用 `systemInstruction` 设置持久化模型行为
- ❌ **不推荐：** 简单任务使用 `gemini-pro`——Flash 更便宜更快
- ❌ **不推荐：** 超过 20MB 的大文件使用内联 base64 图像——改用 File API
- ❌ **不推荐：** 生产应用忽略响应中的安全评级

## 错误处理

```javascript
try {
  const result = await model.generateContent(prompt);
  return result.response.text();
} catch (error) {
  if (error.status === 429) {
    // Rate limited — wait and retry with exponential backoff
    await new Promise(r => setTimeout(r, 2 ** retryCount * 1000));
  } else if (error.status === 400) {
    // Invalid request — check prompt or parameters
    console.error("Invalid request:", error.message);
  } else {
    throw error;
  }
}
```

## 故障排除

**问题：** `API_KEY_INVALID` 错误
**解决方案：** 确保 `GEMINI_API_KEY` 环境变量已设置，且密钥在 Google AI Studio 中处于活跃状态。

**问题：** 响应被安全过滤器阻止
**解决方案：** 检查 `result.response.promptFeedback.blockReason` 并调整提示词或安全设置。

**问题：** 响应时间慢
**解决方案：** 切换到 `gemini-1.5-flash` 并启用流式响应。考虑缓存重复的提示词。

**问题：** `RESOURCE_EXHAUSTED`（配额超限）
**解决方案：** 在 Google Cloud Console 中检查配额。实现请求队列和指数退避。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不应替代环境特定的验证、测试或专家评审。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
