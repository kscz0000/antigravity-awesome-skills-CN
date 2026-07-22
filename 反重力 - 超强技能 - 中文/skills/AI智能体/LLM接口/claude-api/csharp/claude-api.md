# Claude API — C#

> **注意：** C# SDK 是 Anthropic 官方的 C# SDK。工具调用通过 Messages API 支持。基于类注解的 tool runner 不可用；请使用带有 JSON schema 的原始工具定义。该 SDK 还支持 Microsoft.Extensions.AI IChatClient 集成与函数调用。

## 安装

```bash
dotnet add package Anthropic
```

## 客户端初始化

```csharp
using Anthropic;

// 默认（使用 ANTHROPIC_API_KEY 环境变量）
AnthropicClient client = new();

// 显式 API 密钥（使用环境变量 — 切勿硬编码密钥）
AnthropicClient client = new() {
    ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
};
```

---

## 基本消息请求

```csharp
using Anthropic.Models.Messages;

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_6,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "What is the capital of France?" }]
};
var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
```

---

## 流式传输

```csharp
using Anthropic.Models.Messages;

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_6,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Write a haiku" }]
};

await foreach (RawMessageStreamEvent streamEvent in client.Messages.CreateStreaming(parameters))
{
    if (streamEvent.TryPickContentBlockDelta(out var delta) &&
        delta.Delta.TryPickText(out var text))
    {
        Console.Write(text.Text);
    }
}
```

---

## 工具使用（手动循环）

C# SDK 支持通过 JSON schema 定义原始工具。有关工具定义格式和 Agent 循环模式，请参阅[共享工具使用概念](../shared/tool-use-concepts.md)。
