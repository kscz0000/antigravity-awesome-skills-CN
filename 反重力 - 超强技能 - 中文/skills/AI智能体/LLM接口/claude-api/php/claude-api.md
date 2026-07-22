# Claude API — PHP

> **注意：** PHP SDK 是 Anthropic 官方的 PHP SDK。Tool runner 和 Agent SDK 不可用。支持 Bedrock、Vertex AI 和 Foundry 客户端。

## 安装

```bash
composer require "anthropic-ai/sdk"
```

## 客户端初始化

```php
use Anthropic\Client;

// 使用环境变量中的 API 密钥
$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));
```

### Amazon Bedrock

```php
use Anthropic\BedrockClient;

$client = new BedrockClient(
    region: 'us-east-1',
);
```

### Google Vertex AI

```php
use Anthropic\VertexClient;

$client = new VertexClient(
    region: 'us-east5',
    projectId: 'my-project-id',
);
```

### Anthropic Foundry

```php
use Anthropic\FoundryClient;

$client = new FoundryClient(
    authToken: getenv("ANTHROPIC_AUTH_TOKEN"),
);
```

---

## 基本消息请求

```php
$message = $client->messages->create(
    model: 'claude-opus-4-6',
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'What is the capital of France?'],
    ],
);
echo $message->content[0]->text;
```

---

## 流式传输

```php
$stream = $client->messages->createStream(
    model: 'claude-opus-4-6',
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Write a haiku'],
    ],
);

foreach ($stream as $event) {
    echo $event;
}
```

---

## 工具使用（手动循环）

PHP SDK 支持通过 JSON schema 定义原始工具。有关工具定义格式和 Agent 循环模式，请参阅[共享工具使用概念](../shared/tool-use-concepts.md)。
