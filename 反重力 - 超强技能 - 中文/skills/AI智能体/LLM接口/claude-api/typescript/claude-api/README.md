# Claude API — TypeScript

## 安装

```bash
npm install @anthropic-ai/sdk
```

## 客户端初始化

```typescript
import Anthropic from "@anthropic-ai/sdk";

// Default (uses ANTHROPIC_API_KEY env var)
const client = new Anthropic();

// Explicit API key
const client = new Anthropic({ apiKey: "your-api-key" });
```

---

## 基本消息请求

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "What is the capital of France?" }],
});
console.log(response.content[0].text);
```

---

## System Prompt

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  system:
    "You are a helpful coding assistant. Always provide examples in Python.",
  messages: [{ role: "user", content: "How do I read a JSON file?" }],
});
```

---

## 视觉（图片）

### URL

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: { type: "url", url: "https://example.com/image.png" },
        },
        { type: "text", text: "Describe this image" },
      ],
    },
  ],
});
```

### Base64

```typescript
import fs from "fs";

const imageData = fs.readFileSync("image.png").toString("base64");

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: { type: "base64", media_type: "image/png", data: imageData },
        },
        { type: "text", text: "What's in this image?" },
      ],
    },
  ],
});
```

---

## Prompt 缓存

### 自动缓存（推荐）

使用顶层 `cache_control` 自动缓存请求中最后一个可缓存的块：

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  cache_control: { type: "ephemeral" }, // auto-caches the last cacheable block
  system: "You are an expert on this large document...",
  messages: [{ role: "user", content: "Summarize the key points" }],
});
```

### 手动缓存控制

如需更细粒度的控制，可为特定内容块添加 `cache_control`：

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "You are an expert on this large document...",
      cache_control: { type: "ephemeral" }, // default TTL is 5 minutes
    },
  ],
  messages: [{ role: "user", content: "Summarize the key points" }],
});

// With explicit TTL (time-to-live)
const response2 = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "You are an expert on this large document...",
      cache_control: { type: "ephemeral", ttl: "1h" }, // 1 hour TTL
    },
  ],
  messages: [{ role: "user", content: "Summarize the key points" }],
});
```

---

## 扩展思考

> **Opus 4.6 和 Sonnet 4.6：** 使用自适应思考。`budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上均已弃用。
> **较早的模型：** 使用 `thinking: {type: "enabled", budget_tokens: N}`（必须小于 `max_tokens`，最小值为 1024）。

```typescript
// Opus 4.6: adaptive thinking (recommended)
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 16000,
  thinking: { type: "adaptive" },
  output_config: { effort: "high" }, // low | medium | high | max
  messages: [
    { role: "user", content: "Solve this math problem step by step..." },
  ],
});

for (const block of response.content) {
  if (block.type === "thinking") {
    console.log("Thinking:", block.thinking);
  } else if (block.type === "text") {
    console.log("Response:", block.text);
  }
}
```

---

## 错误处理

使用 SDK 的类型化异常类——永远不要用字符串匹配来检查错误信息：

```typescript
import Anthropic from "@anthropic-ai/sdk";

try {
  const response = await client.messages.create({...});
} catch (error) {
  if (error instanceof Anthropic.BadRequestError) {
    console.error("Bad request:", error.message);
  } else if (error instanceof Anthropic.AuthenticationError) {
    console.error("Invalid API key");
  } else if (error instanceof Anthropic.RateLimitError) {
    console.error("Rate limited - retry later");
  } else if (error instanceof Anthropic.APIError) {
    console.error(`API error ${error.status}:`, error.message);
  }
}
```

所有异常类都继承自 `Anthropic.APIError`，并带有类型化的 `status` 字段。检查顺序应从最具体到最笼统。完整的错误码参考请见 [shared/error-codes.md](../../shared/error-codes.md)。

---

## 多轮对话

API 是无状态的——每次请求需发送完整的对话历史。使用 `Anthropic.MessageParam[]` 为消息数组添加类型：

```typescript
const messages: Anthropic.MessageParam[] = [
  { role: "user", content: "My name is Alice." },
  { role: "assistant", content: "Hello Alice! Nice to meet you." },
  { role: "user", content: "What's my name?" },
];

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: messages,
});
```

**规则：**

- 消息必须在 `user` 和 `assistant` 之间交替
- 第一条消息必须是 `user`
- 对所有 API 数据结构使用 SDK 类型（`Anthropic.MessageParam`、`Anthropic.Message`、`Anthropic.Tool` 等）——不要重新定义等效的接口

---

### 压缩（长对话）

> **Beta，仅限 Opus 4.6。** 当对话接近 200K 上下文窗口时，压缩功能会在服务端自动总结较早的上下文。API 会返回一个 `compaction` 块；你必须在后续请求中将其传回——追加 `response.content` 整体，而非仅追加文本。

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const messages: Anthropic.Beta.BetaMessageParam[] = [];

async function chat(userMessage: string): Promise<string> {
  messages.push({ role: "user", content: userMessage });

  const response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-6",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [{ type: "compact_20260112" }],
    },
  });

  // Append full content — compaction blocks must be preserved
  messages.push({ role: "assistant", content: response.content });

  const textBlock = response.content.find((block) => block.type === "text");
  return textBlock?.text ?? "";
}

// Compaction triggers automatically when context grows large
console.log(await chat("Help me build a Python web scraper"));
console.log(await chat("Add support for JavaScript-rendered pages"));
console.log(await chat("Now add rate limiting and error handling"));
```

---

## 停止原因

响应中的 `stop_reason` 字段表示模型停止生成的原因：

| 值              | 含义                                                          |
| --------------- | ------------------------------------------------------------- |
| `end_turn`      | Claude 正常完成了响应                                         |
| `max_tokens`    | 达到 `max_tokens` 限制——增大该值或使用流式输出                |
| `stop_sequence` | 命中了自定义停止序列                                          |
| `tool_use`      | Claude 想要调用工具——执行该工具并继续                         |
| `pause_turn`    | 模型已暂停，可恢复继续（智能体流程）                          |
| `refusal`       | Claude 因安全原因拒绝——输出可能不符合 schema                 |

---

## 成本优化策略

### 1. 对重复上下文使用 Prompt 缓存

```typescript
// Automatic caching (simplest — caches the last cacheable block)
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  cache_control: { type: "ephemeral" },
  system: largeDocumentText, // e.g., 50KB of context
  messages: [{ role: "user", content: "Summarize the key points" }],
});

// First request: full cost
// Subsequent requests: ~90% cheaper for cached portion
```

### 2. 在请求前使用 Token 计数

```typescript
const countResponse = await client.messages.countTokens({
  model: "claude-opus-4-6",
  messages: messages,
  system: system,
});

const estimatedInputCost = countResponse.input_tokens * 0.000005; // $5/1M tokens
console.log(`Estimated input cost: $${estimatedInputCost.toFixed(4)}`);
```