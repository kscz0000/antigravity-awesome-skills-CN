# Claude API — Ruby

> **注意：** Ruby SDK 支持 Claude API。Tool runner 通过 `client.beta.messages.tool_runner()` 在 beta 中可用。Agent SDK 尚未支持 Ruby。

## 安装

```bash
gem install anthropic
```

## 客户端初始化

```ruby
require "anthropic"

# 默认（使用 ANTHROPIC_API_KEY 环境变量）
client = Anthropic::Client.new

# 显式 API 密钥
client = Anthropic::Client.new(api_key: "your-api-key")
```

---

## 基本消息请求

```ruby
message = client.messages.create(
  model: :"claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "What is the capital of France?" }
  ]
)
puts message.content.first.text
```

---

## 流式传输

```ruby
stream = client.messages.stream(
  model: :"claude-opus-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Write a haiku" }]
)

stream.text.each { |text| print(text) }
```

---

## 工具使用

Ruby SDK 支持通过原始 JSON schema 定义进行工具调用，并提供 beta tool runner 用于自动工具执行。

### Tool Runner（Beta）

```ruby
class GetWeatherInput < Anthropic::BaseModel
  required :location, String, doc: "City and state, e.g. San Francisco, CA"
end

class GetWeather < Anthropic::BaseTool
  doc "Get the current weather for a location"

  input_schema GetWeatherInput

  def call(input)
    "The weather in #{input.location} is sunny and 72°F."
  end
end

client.beta.messages.tool_runner(
  model: :"claude-opus-4-6",
  max_tokens: 1024,
  tools: [GetWeather.new],
  messages: [{ role: "user", content: "What's the weather in San Francisco?" }]
).each_message do |message|
  puts message.content
end
```

### 手动循环

有关工具定义格式和 Agent 循环模式，请参阅[共享工具使用概念](../shared/tool-use-concepts.md)。
