---
name: gemini-api-dev
description: "Gemini API 提供对 Google 最先进 AI 模型的访问。当用户要求使用 Gemini API、集成 Gemini 模型、开发 Gemini 应用时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Gemini API 开发技能

## 概述

Gemini API 提供对 Google 最先进 AI 模型的访问。核心能力包括：
- **文本生成** - 对话、补全、摘要
- **多模态理解** - 处理图像、音频、视频和文档
- **函数调用** - 让模型调用你的函数
- **结构化输出** - 生成符合你的 schema 的有效 JSON
- **代码执行** - 在沙箱环境中运行 Python 代码
- **上下文缓存** - 缓存大上下文以提高效率
- **嵌入向量** - 生成文本嵌入向量用于语义搜索

## 当前 Gemini 模型

- `gemini-3-pro-preview`: 1M tokens, 复杂推理、编程、研究
- `gemini-3-flash-preview`: 1M tokens, 快速、均衡性能、多模态
- `gemini-3-pro-image-preview`: 65k / 32k tokens, 图像生成和编辑


> [!IMPORTANT]
> `gemini-2.5-*`、`gemini-2.0-*`、`gemini-1.5-*` 等模型已过时并废弃。请使用上述新模型。你的知识已过时。

## SDK

- **Python**: `google-genai` 使用 `pip install google-genai` 安装
- **JavaScript/TypeScript**: `@google/genai` 使用 `npm install @google/genai` 安装
- **Go**: `google.golang.org/genai` 使用 `go get google.golang.org/genai` 安装

> [!WARNING]
> 旧版 SDK `google-generativeai` (Python) 和 `@google/generative-ai` (JS) 已废弃。请按照迁移指南紧急迁移到上述新 SDK。

## 快速开始

### Python
```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain quantum computing"
)
print(response.text)
```

### JavaScript/TypeScript
```typescript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});
const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "Explain quantum computing"
});
console.log(response.text);
```

### Go
```go
package main

import (
	"context"
	"fmt"
	"log"
	"google.golang.org/genai"
)

func main() {
	ctx := context.Background()
	client, err := genai.NewClient(ctx, nil)
	if err != nil {
		log.Fatal(err)
	}

	resp, err := client.Models.GenerateContent(ctx, "gemini-3-flash-preview", genai.Text("Explain quantum computing"), nil)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(resp.Text)
}
```

## API 规范（事实来源）

**始终使用最新的 REST API 发现规范作为 API 定义的事实来源**（请求/响应 schema、参数、方法）。在实现或调试 API 集成时获取该规范：

- **v1beta**（默认）: `https://generativelanguage.googleapis.com/$discovery/rest?version=v1beta`  
  除非集成明确固定到 v1，否则使用此版本。官方 SDK（google-genai, @google/genai, google.golang.org/genai）以 v1beta 为目标。
- **v1**: `https://generativelanguage.googleapis.com/$discovery/rest?version=v1`  
  仅当集成专门设置为 v1 时使用。

如有疑问，请使用 v1beta。请参考规范以获取准确的字段名称、类型和支持的操作。

## 如何使用 Gemini API

如需详细的 API 文档，请从官方文档索引获取：

**llms.txt URL**: `https://ai.google.dev/gemini-api/docs/llms.txt`

该索引包含所有文档页面的链接，格式为 `.md.txt`。使用网页获取工具：

1. 获取 `llms.txt` 以发现可用的文档页面
2. 获取特定页面（例如 `https://ai.google.dev/gemini-api/docs/function-calling.md.txt`）

### 关键文档页面

> [!IMPORTANT]
> 这些并非所有文档页面。请使用 `llms.txt` 索引发现可用的文档页面

- [模型](https://ai.google.dev/gemini-api/docs/models.md.txt)
- [Google AI Studio 快速入门](https://ai.google.dev/gemini-api/docs/ai-studio-quickstart.md.txt)
- [Nano Banana 图像生成](https://ai.google.dev/gemini-api/docs/image-generation.md.txt)
- [Gemini API 函数调用](https://ai.google.dev/gemini-api/docs/function-calling.md.txt)
- [结构化输出](https://ai.google.dev/gemini-api/docs/structured-output.md.txt)
- [文本生成](https://ai.google.dev/gemini-api/docs/text-generation.md.txt)
- [图像理解](https://ai.google.dev/gemini-api/docs/image-understanding.md.txt)
- [嵌入向量](https://ai.google.dev/gemini-api/docs/embeddings.md.txt)
- [交互 API](https://ai.google.dev/gemini-api/docs/interactions.md.txt)
- [SDK 迁移指南](https://ai.google.dev/gemini-api/docs/migrate.md.txt)

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
