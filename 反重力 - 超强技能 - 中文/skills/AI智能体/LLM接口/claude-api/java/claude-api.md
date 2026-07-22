# Claude API — Java

> **注意：** Java SDK 支持 Claude API 和通过注解类进行 beta 工具调用。Agent SDK 尚未支持 Java。

## 安装

Maven:

```xml
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>anthropic-java</artifactId>
    <version>2.15.0</version>
</dependency>
```

Gradle:

```groovy
implementation("com.anthropic:anthropic-java:2.15.0")
```

## 客户端初始化

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

// 默认（从环境变量读取 ANTHROPIC_API_KEY）
AnthropicClient client = AnthropicOkHttpClient.fromEnv();

// 显式 API 密钥
AnthropicClient client = AnthropicOkHttpClient.builder()
    .apiKey("your-api-key")
    .build();
```

---

## 基本消息请求

```java
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;

MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_6)
    .maxTokens(1024L)
    .addUserMessage("What is the capital of France?")
    .build();

Message response = client.messages().create(params);
response.content().stream()
    .flatMap(block -> block.text().stream())
    .forEach(textBlock -> System.out.println(textBlock.text()));
```

---

## 流式传输

```java
import com.anthropic.core.http.StreamResponse;
import com.anthropic.models.messages.RawMessageStreamEvent;

MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_6)
    .maxTokens(1024L)
    .addUserMessage("Write a haiku")
    .build();

try (StreamResponse<RawMessageStreamEvent> streamResponse = client.messages().createStreaming(params)) {
    streamResponse.stream()
        .flatMap(event -> event.contentBlockDelta().stream())
        .flatMap(deltaEvent -> deltaEvent.delta().text().stream())
        .forEach(textDelta -> System.out.print(textDelta.text()));
}
```

---

## 工具使用（Beta）

Java SDK 支持通过注解类进行 beta 工具调用。工具类实现 `Supplier<String>` 以通过 `BetaToolRunner` 自动执行。

### Tool Runner（自动循环）

```java
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.helpers.BetaToolRunner;
import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import java.util.function.Supplier;

@JsonClassDescription("Get the weather in a given location")
static class GetWeather implements Supplier<String> {
    @JsonPropertyDescription("The city and state, e.g. San Francisco, CA")
    public String location;

    @Override
    public String get() {
        return "The weather in " + location + " is sunny and 72°F";
    }
}

BetaToolRunner toolRunner = client.beta().messages().toolRunner(
    MessageCreateParams.builder()
        .model("claude-opus-4-6")
        .maxTokens(1024L)
        .putAdditionalHeader("anthropic-beta", "structured-outputs-2025-11-13")
        .addTool(GetWeather.class)
        .addUserMessage("What's the weather in San Francisco?")
        .build());

for (BetaMessage message : toolRunner) {
    System.out.println(message);
}
```

### 非 Beta 工具调用

工具调用也可以通过非 beta 的 `com.anthropic.models.messages.MessageCreateParams` 配合 `addTool(Tool)` 使用手动定义的 JSON schema，无需 beta 命名空间。beta 命名空间仅用于类注解便捷层（`@JsonClassDescription`、`BetaToolRunner`）。

### 手动循环

对于手动工具循环，在请求中将工具定义为 JSON schema，处理响应中的 `tool_use` 块，发送 `tool_result` 回去，并循环直到 `stop_reason` 为 `"end_turn"`。有关 Agent 循环模式，请参阅[共享工具使用概念](../shared/tool-use-concepts.md)。
