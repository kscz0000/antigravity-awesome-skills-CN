# Claude API — Go

> **注意：** Go SDK 支持 Claude API 和通过 `BetaToolRunner` 进行 beta 工具调用。Agent SDK 尚未支持 Go。

## 安装

```bash
go get github.com/anthropics/anthropic-sdk-go
```

## 客户端初始化

```go
import (
    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/option"
)

// 默认（使用 ANTHROPIC_API_KEY 环境变量）
client := anthropic.NewClient()

// 显式 API 密钥
client := anthropic.NewClient(
    option.WithAPIKey("your-api-key"),
)
```

---

## 基本消息请求

```go
response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaudeOpus4_6,
    MaxTokens: 1024,
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("What is the capital of France?")),
    },
})
if err != nil {
    log.Fatal(err)
}
fmt.Println(response.Content[0].Text)
```

---

## 流式传输

```go
stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaudeOpus4_6,
    MaxTokens: 1024,
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("Write a haiku")),
    },
})

for stream.Next() {
    event := stream.Current()
    switch eventVariant := event.AsAny().(type) {
    case anthropic.ContentBlockDeltaEvent:
        switch deltaVariant := eventVariant.Delta.AsAny().(type) {
        case anthropic.TextDelta:
            fmt.Print(deltaVariant.Text)
        }
    }
}
if err := stream.Err(); err != nil {
    log.Fatal(err)
}
```

---

## 工具使用

### Tool Runner（Beta — 推荐）

**Beta：** Go SDK 通过 `toolrunner` 包提供 `BetaToolRunner` 用于自动工具调用循环。

```go
import (
    "context"
    "fmt"
    "log"

    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/toolrunner"
)

// 使用 jsonschema 标签定义工具输入以自动生成 schema
type GetWeatherInput struct {
    City string `json:"city" jsonschema:"required,description=The city name"`
}

// 从结构体标签创建具有自动 schema 生成的工具
weatherTool, err := toolrunner.NewBetaToolFromJSONSchema(
    "get_weather",
    "Get current weather for a city",
    func(ctx context.Context, input GetWeatherInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
        return anthropic.BetaToolResultBlockParamContentUnion{
            OfText: &anthropic.BetaTextBlockParam{
                Text: fmt.Sprintf("The weather in %s is sunny, 72°F", input.City),
            },
        }, nil
    },
)
if err != nil {
    log.Fatal(err)
}

// 创建自动处理对话循环的 tool runner
runner := client.Beta.Messages.NewToolRunner(
    []anthropic.BetaTool{weatherTool},
    anthropic.BetaToolRunnerParams{
        BetaMessageNewParams: anthropic.BetaMessageNewParams{
            Model:     anthropic.ModelClaudeOpus4_6,
            MaxTokens: 1024,
            Messages: []anthropic.BetaMessageParam{
                anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What's the weather in Paris?")),
            },
        },
        MaxIterations: 5,
    },
)

// 运行直到 Claude 产生最终响应
message, err := runner.RunToCompletion(context.Background())
if err != nil {
    log.Fatal(err)
}
fmt.Println(message.Content[0].Text)
```

**Go tool runner 的关键特性：**

- 通过 `jsonschema` 标签从 Go 结构体自动生成 schema
- `RunToCompletion()` 用于简单的一次性使用
- `All()` 迭代器用于处理对话中的每条消息
- `NextMessage()` 用于逐步迭代
- 通过 `NewToolRunnerStreaming()` 配合 `AllStreaming()` 的流式变体

### 手动循环

要精细控制，请通过 JSON schema 使用原始工具定义。有关工具定义格式和 Agent 循环模式，请参阅[共享工具使用概念](../shared/tool-use-concepts.md)。
