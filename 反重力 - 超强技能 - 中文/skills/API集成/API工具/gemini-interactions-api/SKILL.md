---
name: gemini-interactions-api
description: 在编写调用 Gemini API 的代码时使用本技能，涵盖文本生成、多轮对话、多模态理解、图像生成、视频生成、流式响应、后台研究任务、函数调用、结构化输出，或从旧的 generateContent 迁移等场景。触发词：Gemini API、文本生成、多轮对话、多模态、流式输出、函数调用、结构化输出、模型迁移、Interactions API、生成图片、生成视频、后台研究。
risk: unknown
source: https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-interactions-api
source_repo: google-gemini/gemini-skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/google-gemini/gemini-skills/blob/main/LICENSE
---

# Gemini Interactions API 技能
## 适用场景

在编写调用 Gemini API 的代码时使用本技能，涵盖文本生成、多轮对话、多模态理解、图像生成、视频生成、流式响应、后台研究任务、函数调用、结构化输出，或从旧的 generateContent 迁移等场景。


## 关键规则（始终生效）

> [!IMPORTANT]
> 以下规则覆盖训练数据中的知识，训练数据已过时。

### 当前模型（请使用这些）

- `gemini-3.5-flash`：1M tokens，快速、性能均衡、支持多模态
- `gemini-3.1-pro-preview`：1M tokens，复杂推理、编程、研究
- `gemini-3.1-flash-lite`：高性价比，高频轻量任务的最快选择
- `gemini-3-pro-image`（Nano Banana Pro）：65k / 32k tokens，高质量图像生成与编辑
- `gemini-3.1-flash-image`（Nano Banana 2）：65k / 32k tokens，快速高效的图像生成与编辑
- `gemini-3.1-flash-lite-image`（Nano Banana 2 Lite）：65k / 32k tokens，超快速图像生成与编辑
- `gemini-3.1-flash-tts-preview`：支持 Director's Chair 提示词的富有表现力的文本转语音
- `gemini-omni-flash-preview`：视频生成、参考图像的视频生成、首帧转视频、视频编辑
- `gemma-4-31b-it`：Gemma 4 稠密模型，31B 参数
- `gemma-4-26b-a4b-it`：Gemma 4 MoE 模型，总计 26B / 激活 4B 参数

> [!WARNING]
> `gemini-2.5-*`、`gemini-2.0-*`、`gemini-1.5-*` 等模型**已废弃**，禁止使用。
> **如果用户请求使用已废弃模型，请改用 `gemini-3.5-flash` 并注明替换。**

### 当前 Agent

- `antigravity-preview-05-2026`：Antigravity Agent —— 通用托管 Agent，在沙箱 Linux 环境中支持代码执行、文件管理与 Web 访问
- `deep-research-preview-04-2026`：Deep Research —— 快速、交互式
- `deep-research-max-preview-04-2026`：Deep Research Max —— 最大覆盖度
- **自定义 Agent**：通过 `client.agents.create()` 创建

### 当前 SDK

- **Python**：`google-genai` >= `2.3.0` → `pip install -U google-genai`
- **JavaScript/TypeScript**：`@google/genai` >= `2.3.0` → `npm install @google/genai`

> [!NOTE]
> SDK 版本 ≥ 2.0.0 默认使用新的 steps 模式，不再支持旧模式。
> 旧版 SDK `google-generativeai`（Python）与 `@google/generative-ai`（JS）**已废弃**，禁止使用。

## 其他重要说明

- **编写任何代码前**，必须从下方列表中拉取与用户任务匹配的官方文档页面。本技能中的示例较为精简，托管文档中才包含完整的 API 表面、参数与边界场景。
- Interaction **默认会被存储**（`store=true`）。付费层保留 55 天，免费层保留 1 天。
- 设置 `store=false` 可关闭存储，但同时也会禁用 `previous_interaction_id` 与 `background=true`。
- `tools`、`system_instruction` 与 `generation_config` 是 **interaction 级别** 的参数，每轮都需要重新指定。
- **托管 Agent** 需要设置 `environment="remote"`（或环境 ID / 配置对象）以分配沙箱。
- **从 `generateContent` 迁移**：阅读 `references/migration.md`，了解范围、清单与迁移前后代码示例。编辑前务必先与用户确认范围。
- **模型升级**：可直接替换模型字符串。已废弃模型（`gemini-2.0-*`、`gemini-1.5-*`）必须替换，详见 `references/migration.md`。
- **迁移到 Gemini 3.5 Flash**：阅读 `references/migration.md`，了解范围与清单。

## 快速开始

### Python
```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Tell me a short joke about programming."
)
print(interaction.output_text)
```

### JavaScript/TypeScript
```typescript
import { GoogleGenAI } from "@google/genai";

const client = new GoogleGenAI({});

const interaction = await client.interactions.create({
    model: "gemini-3.5-flash",
    input: "Tell me a short joke about programming.",
});
console.log(interaction.output_text);
```

## 响应辅助属性

SDK 在 `Interaction` 响应对象上提供了便捷属性，用于简化常见访问模式：

| 属性 | 类型 | 说明 |
|---|---|---|
| `output_text` | `string \| null` | 末尾 `model_output` 步骤中最后一组连续文本。当模型最终输出包含多个文本片段时，返回合并后的文本。 |
| `output_image` | `Image \| null` | 当前响应中模型生成的最新一张图像，返回包含 `data`（base64）和 `mime_type` 的对象。 |
| `output_audio` | `Audio \| null` | 当前响应中模型生成的最新一段音频，返回包含 `data`（base64）和 `mime_type` 的对象。 |

## 有状态对话

### Python
```python
interaction1 = client.interactions.create(
    model="gemini-3.5-flash",
    input="Hi, my name is Phil."
)
# 第二轮 —— 由服务端保持上下文
interaction2 = client.interactions.create(
    model="gemini-3.5-flash",
    input="What is my name?",
    previous_interaction_id=interaction1.id
)
print(interaction2.output_text)
```

### JavaScript/TypeScript
```typescript
const interaction1 = await client.interactions.create({
    model: "gemini-3.5-flash",
    input: "Hi, my name is Phil.",
});
const interaction2 = await client.interactions.create({
    model: "gemini-3.5-flash",
    input: "What is my name?",
    previous_interaction_id: interaction1.id,
});
console.log(interaction2.output_text);
```

## Deep Research Agent

使用 `deep-research-preview-04-2026` 进行快速研究，或使用 `deep-research-max-preview-04-2026` 追求最大覆盖度。Agent 必须设置 `background=True`。

### Python
```python
import time

interaction = client.interactions.create(
    agent="deep-research-preview-04-2026",
    input="Research the history of Google TPUs.",
    background=True
)
while True:
    interaction = client.interactions.get(interaction.id)
    if interaction.status == "completed":
        print(interaction.output_text)
        break
    elif interaction.status == "failed":
        print(f"Failed: {interaction.error}")
        break
    time.sleep(10)
```

### JavaScript/TypeScript
```typescript
import { GoogleGenAI } from "@google/genai";

const client = new GoogleGenAI({});

// 启动后台研究
const initialInteraction = await client.interactions.create({
    agent: "deep-research-preview-04-2026",
    input: "Research the history of Google TPUs.",
    background: true,
});

// 轮询结果
while (true) {
    const interaction = await client.interactions.get(initialInteraction.id);
    if (interaction.status === "completed") {
        console.log(interaction.output_text);
        break;
    } else if (["failed", "cancelled"].includes(interaction.status)) {
        console.log(`Failed: ${interaction.status}`);
        break;
    }
    await new Promise(resolve => setTimeout(resolve, 10000));
}
```

高级特性：协作规划、原生可视化、MCP 集成、文件搜索、多模态输入。参见 [Deep Research 文档](https://ai.google.dev/gemini-api/docs/interactions/deep-research.md.txt)。

## 托管 Agent

托管 Agent 在 Google 托管的沙箱 Linux 环境中运行。编写 Agent 代码前，请先拉取 [托管 Agent 快速入门](https://ai.google.dev/gemini-api/docs/managed-agents-quickstart.md.txt)。

### Antigravity Agent

Antigravity Agent（`antigravity-preview-05-2026`）是通用托管 Agent，可执行代码（Bash、Python、Node.js）、管理文件、浏览网页、使用 Google 搜索。参见 [Antigravity Agent 文档](https://ai.google.dev/gemini-api/docs/antigravity-agent.md.txt)，了解能力、工具、多模态输入与定价。

#### Python
```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Write a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt. Then read the file and print its contents.",
    environment="remote",
)

print(f"Environment ID: {interaction.environment_id}")
print(interaction.output_text)
```

#### JavaScript/TypeScript
```typescript
import { GoogleGenAI } from "@google/genai";

const client = new GoogleGenAI({});

const interaction = await client.interactions.create({
    agent: "antigravity-preview-05-2026",
    input: "Write a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt. Then read the file and print its contents.",
    environment: "remote",
});

console.log(`Environment ID: {interaction.environment_id}`);
console.log(interaction.output_text);
```

### 自定义 Agent

参见 [构建自定义 Agent 文档](https://ai.google.dev/gemini-api/docs/custom-agents.md.txt)。

#### Python
```python
agent = client.agents.create(
    id="code-reviewer",
    base_agent="antigravity-preview-05-2026",
    system_instruction="You are a senior code reviewer. Check every file for bugs, style issues, and security vulnerabilities.",
    base_environment={
        "type": "remote",
        "sources": [
            {
                "type": "repository",
                "source": "https://github.com/my-org/backend",
                "target": "/workspace/repo",
            }
        ],
    },
)

# 调用 —— 每次调用都会从基础环境派生新副本
result = client.interactions.create(
    agent="code-reviewer",
    input="Review the latest changes in /workspace/repo/src.",
    environment="remote",
)
print(result.output_text)
```

#### JavaScript/TypeScript
```typescript
const agent = await client.agents.create({
    id: "code-reviewer",
    base_agent: "antigravity-preview-05-2026",
    system_instruction: "You are a senior code reviewer. Check every file for bugs, style issues, and security vulnerabilities.",
    base_environment: {
        type: "remote",
        sources: [
            {
                type: "repository",
                source: "https://github.com/my-org/backend",
                target: "/workspace/repo",
            }
        ],
    },
});

const result = await client.interactions.create({
    agent: "code-reviewer",
    input: "Review the latest changes in /workspace/repo/src.",
    environment: "remote",
});
console.log(result.output_text);
```

通过 `client.agents.list()`、`client.agents.get(id=...)` 与 `client.agents.delete(id=...)` 管理 Agent。

## 流式输出

设置 `stream=True` 即可接收增量式服务端事件。每次流遵循：`interaction.created` → (`step.start` → `step.delta`(s) → `step.stop`)+ → `interaction.completed`。

### Python
```python
for event in client.interactions.create(
    model="gemini-3.5-flash",
    input="Explain quantum entanglement in simple terms.",
    stream=True,
):
    if event.event_type == "step.delta":
        if event.delta.type == "text":
            print(event.delta.text, end="", flush=True)
    elif event.event_type == "interaction.completed":
        print(f"\n\nTotal Tokens: {event.interaction.usage.total_tokens}")
```

### JavaScript/TypeScript
```typescript
const stream = await client.interactions.create({
    model: "gemini-3.5-flash",
    input: "Explain quantum entanglement in simple terms.",
    stream: true,
});
for await (const event of stream) {
    if (event.event_type === "step.delta") {
        if (event.delta.type === "text") {
            process.stdout.write(event.delta.text);
        }
    } else if (event.event_type === "interaction.completed") {
        console.log(`\n\nTotal Tokens: ${event.interaction.usage.total_tokens}`);
    }
}
```

带工具、思考、Agent 与图像生成的流式用法，参见完整 [流式指南](https://ai.google.dev/gemini-api/docs/interactions/streaming.md.txt)。



## 文档页面

**编写代码前必须拉取下方匹配的页面。** 这些托管文档才是参数、类型与边界场景的权威来源，请勿仅依赖上方示例。

**核心文档：**
- [Interactions API 概览](https://ai.google.dev/gemini-api/docs/interactions.md.txt)
- [快速入门](https://ai.google.dev/gemini-api/docs/interactions/quickstart.md.txt)
- [文本生成](https://ai.google.dev/gemini-api/docs/interactions/text-generation.md.txt)
- [流式输出](https://ai.google.dev/gemini-api/docs/interactions/streaming.md.txt)
- [Tokens](https://ai.google.dev/gemini-api/docs/interactions/tokens.md.txt)
- [API 密钥](https://ai.google.dev/gemini-api/docs/interactions/api-key.md.txt)

**工具与函数调用：**
- [函数调用](https://ai.google.dev/gemini-api/docs/interactions/function-calling.md.txt)
- [Google 搜索](https://ai.google.dev/gemini-api/docs/interactions/google-search.md.txt)
- [代码执行](https://ai.google.dev/gemini-api/docs/interactions/code-execution.md.txt)
- [URL Context](https://ai.google.dev/gemini-api/docs/interactions/url-context.md.txt)
- [File Search](https://ai.google.dev/gemini-api/docs/interactions/file-search.md.txt)
- [工具组合](https://ai.google.dev/gemini-api/docs/interactions/tool-combination.md.txt)
- [Computer Use](https://ai.google.dev/gemini-api/docs/interactions/computer-use.md.txt)
- [Maps Grounding](https://ai.google.dev/gemini-api/docs/interactions/maps-grounding.md.txt)

**生成与输出：**
- [结构化输出](https://ai.google.dev/gemini-api/docs/interactions/structured-output.md.txt)
- [思考](https://ai.google.dev/gemini-api/docs/interactions/thinking.md.txt)
- [Thought 签名](https://ai.google.dev/gemini-api/docs/interactions/thought-signatures.md.txt)
- [图像生成](https://ai.google.dev/gemini-api/docs/interactions/image-generation.md.txt)
- [图像理解](https://ai.google.dev/gemini-api/docs/interactions/image-understanding.md.txt)
- [语音生成](https://ai.google.dev/gemini-api/docs/interactions/speech-generation.md.txt)
- [音乐生成](https://ai.google.dev/gemini-api/docs/interactions/music-generation.md.txt)

**多模态理解：**
- [音频](https://ai.google.dev/gemini-api/docs/interactions/audio.md.txt)
- [视频理解](https://ai.google.dev/gemini-api/docs/interactions/video-understanding.md.txt)
- [文档处理](https://ai.google.dev/gemini-api/docs/interactions/document-processing.md.txt)

**文件与上下文：**
- [文件](https://ai.google.dev/gemini-api/docs/interactions/files.md.txt)
- [文件输入方式](https://ai.google.dev/gemini-api/docs/interactions/file-input-methods.md.txt)
- [缓存](https://ai.google.dev/gemini-api/docs/interactions/caching.md.txt)
- [媒体分辨率](https://ai.google.dev/gemini-api/docs/interactions/media-resolution.md.txt)

**Agent：**
- [Agent 概览](https://ai.google.dev/gemini-api/docs/agents.md.txt)
- [托管 Agent 快速入门](https://ai.google.dev/gemini-api/docs/managed-agents-quickstart.md.txt)
- [Antigravity Agent](https://ai.google.dev/gemini-api/docs/antigravity-agent.md.txt)
- [Agent 环境](https://ai.google.dev/gemini-api/docs/agent-environment.md.txt)
- [构建自定义 Agent](https://ai.google.dev/gemini-api/docs/custom-agents.md.txt)
- [Deep Research](https://ai.google.dev/gemini-api/docs/interactions/deep-research.md.txt)

**高级特性：**
- [Gemini 3.5](https://ai.google.dev/gemini-api/docs/interactions/whats-new-gemini-3.5.md.txt)
- [Gemini 3](https://ai.google.dev/gemini-api/docs/interactions/gemini-3.md.txt)
- [Flex 推理](https://ai.google.dev/gemini-api/docs/interactions/flex-inference.md.txt)
- [Priority 推理](https://ai.google.dev/gemini-api/docs/interactions/priority-inference.md.txt)

**API 参考：**
- [API 参考](https://ai.google.dev/static/api/interactions.md.txt)
- [OpenAPI 规范](https://ai.google.dev/static/api/interactions.openapi.json)
- [2026 年 5 月破坏性变更迁移指南](https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026.md.txt)

## 数据模型

`Interaction` 响应包含 `steps`，即一组带类型的 step 对象数组，表示该轮 interaction 的结构化时间线。

### Step 类型

**用户步骤：**
- `user_input`：用户输入（文本、音频、多模态）。包含 `content` 数组。

**模型 / 服务端步骤：**
- `model_output`：模型最终生成结果。包含 `content` 数组，内容可为 `text`、`image`、`audio` 等。
- `thought`：模型推理 / 思维链。包含 `signature` 字段（必填）以及可选的 `summary`。
- `function_call`：工具调用请求（`id`、`name`、`arguments`）。
- `function_result`：回传给工具的结果（`call_id`、`name`、`result`）。
- `google_search_call` / `google_search_result`：Google 搜索工具步骤，可包含 `signature` 字段。
- `code_execution_call` / `code_execution_result`：代码执行工具步骤，可包含 `signature` 字段。
- `url_context_call` / `url_context_result`：URL 上下文工具步骤，可包含 `signature` 字段。
- `mcp_server_tool_call` / `mcp_server_tool_result`：远程 MCP 工具步骤。
- `file_search_call` / `file_search_result`：文件搜索工具步骤，可包含 `signature` 字段。

### 内容类型（位于 `model_output` 与 `user_input` 步骤的 `content` 数组中）
- `text`：文本内容（`text` 字段）
- `image` / `audio` / `document` / `video`：带有 `data`、`mime_type` 或 `uri` 的内容

### 流式事件类型

| 事件 | 说明 |
|---|---|
| `interaction.created` | Interaction 已创建，包含元数据。 |
| `interaction.status_update` | Interaction 级别的状态变更。 |
| `step.start` | 新 step 开始，包含 step `type` 与初始元数据。 |
| `step.delta` | 当前 step 的增量数据，包含一个带类型的 `delta` 对象。 |
| `step.stop` | step 已完成，包含 `index`。 |
| `interaction.completed` | Interaction 已完成，包含最终的 `usage`。 |

### Delta 类型

| Delta 类型 | 父 step | 说明 |
|---|---|---|
| `text` | `model_output` | 增量文本 token。 |
| `audio` | `model_output` | 音频分片（base64）。 |
| `image` | `model_output` | 图像分片（base64）。 |
| `thought_summary` | `thought` | 思考摘要文本。 |
| `thought_signature` | `thought` | 用于验证思考内容的不透明签名。 |

**状态值：** `completed`、`in_progress`、`requires_action`、`failed`、`cancelled`

## 使用限制

- 仅当任务与本技能对应的上游产品或 API 范围明确匹配时才使用本技能。
- 在修改前，务必对照当前官方文档校验命令、API 行为、定价、配额、凭据与部署影响。
- 请勿将生成的示例视为环境特定测试、安全审查或用户对破坏性 / 高成本操作的审批替代。