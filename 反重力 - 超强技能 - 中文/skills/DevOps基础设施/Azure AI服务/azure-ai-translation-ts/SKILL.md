---
name: azure-ai-translation-ts
description: "使用 Azure Translation SDK 进行文本和文档翻译，支持 TypeScript REST 风格客户端。触发词：Azure翻译、文本翻译、文档翻译、TypeScript翻译、Azure AI翻译、多语言翻译、翻译SDK、Azure认知服务翻译"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Translation SDKs for TypeScript

使用 REST 风格客户端进行文本和文档翻译。

## 安装

```bash
# 文本翻译
npm install @azure-rest/ai-translation-text @azure/identity

# 文档翻译
npm install @azure-rest/ai-translation-document @azure/identity
```

## 环境变量

```bash
TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com
TRANSLATOR_SUBSCRIPTION_KEY=<your-api-key>
TRANSLATOR_REGION=<your-region>  # 例如：westus, eastus
```

## 文本翻译客户端

### 身份认证

```typescript
import TextTranslationClient, { TranslatorCredential } from "@azure-rest/ai-translation-text";

// API Key + 区域
const credential: TranslatorCredential = {
  key: process.env.TRANSLATOR_SUBSCRIPTION_KEY!,
  region: process.env.TRANSLATOR_REGION!,
};
const client = TextTranslationClient(process.env.TRANSLATOR_ENDPOINT!, credential);

// 或仅使用凭证（使用全局端点）
const client2 = TextTranslationClient(credential);
```

### 翻译文本

```typescript
import TextTranslationClient, { isUnexpected } from "@azure-rest/ai-translation-text";

const response = await client.path("/translate").post({
  body: {
    inputs: [
      {
        text: "Hello, how are you?",
        language: "en",  // 源语言（可选，自动检测）
        targets: [
          { language: "es" },
          { language: "fr" },
        ],
      },
    ],
  },
});

if (isUnexpected(response)) {
  throw response.body.error;
}

for (const result of response.body.value) {
  for (const translation of result.translations) {
    console.log(`${translation.language}: ${translation.text}`);
  }
}
```

### 带选项翻译

```typescript
const response = await client.path("/translate").post({
  body: {
    inputs: [
      {
        text: "Hello world",
        language: "en",
        textType: "Plain",  // 或 "Html"
        targets: [
          {
            language: "de",
            profanityAction: "NoAction",  // "Marked" | "Deleted"
            tone: "formal",  // LLM 特定选项
          },
        ],
      },
    ],
  },
});
```

### 获取支持的语言

```typescript
const response = await client.path("/languages").get();

if (isUnexpected(response)) {
  throw response.body.error;
}

// 翻译语言
for (const [code, lang] of Object.entries(response.body.translation || {})) {
  console.log(`${code}: ${lang.name} (${lang.nativeName})`);
}
```

### 音译

```typescript
const response = await client.path("/transliterate").post({
  body: { inputs: [{ text: "这是个测试" }] },
  queryParameters: {
    language: "zh-Hans",
    fromScript: "Hans",
    toScript: "Latn",
  },
});

if (!isUnexpected(response)) {
  for (const t of response.body.value) {
    console.log(`${t.script}: ${t.text}`);  // Latn: zhè shì gè cè shì
  }
}
```

### 检测语言

```typescript
const response = await client.path("/detect").post({
  body: { inputs: [{ text: "Bonjour le monde" }] },
});

if (!isUnexpected(response)) {
  for (const result of response.body.value) {
    console.log(`Language: ${result.language}, Score: ${result.score}`);
  }
}
```

## 文档翻译客户端

### 身份认证

```typescript
import DocumentTranslationClient from "@azure-rest/ai-translation-document";
import { DefaultAzureCredential } from "@azure/identity";

const endpoint = "https://<translator>.cognitiveservices.azure.com";

// TokenCredential
const client = DocumentTranslationClient(endpoint, new DefaultAzureCredential());

// API Key
const client2 = DocumentTranslationClient(endpoint, { key: "<api-key>" });
```

### 单文档翻译

```typescript
import DocumentTranslationClient from "@azure-rest/ai-translation-document";
import { writeFile } from "node:fs/promises";

const response = await client.path("/document:translate").post({
  queryParameters: {
    targetLanguage: "es",
    sourceLanguage: "en",  // 可选
  },
  contentType: "multipart/form-data",
  body: [
    {
      name: "document",
      body: "Hello, this is a test document.",
      filename: "test.txt",
      contentType: "text/plain",
    },
  ],
}).asNodeStream();

if (response.status === "200") {
  await writeFile("translated.txt", response.body);
}
```

### 批量文档翻译

```typescript
import { ContainerSASPermissions, BlobServiceClient } from "@azure/storage-blob";

// 为源容器和目标容器生成 SAS URL
const sourceSas = await sourceContainer.generateSasUrl({
  permissions: ContainerSASPermissions.parse("rl"),
  expiresOn: new Date(Date.now() + 24 * 60 * 60 * 1000),
});

const targetSas = await targetContainer.generateSasUrl({
  permissions: ContainerSASPermissions.parse("rwl"),
  expiresOn: new Date(Date.now() + 24 * 60 * 60 * 1000),
});

// 启动批量翻译
const response = await client.path("/document/batches").post({
  body: {
    inputs: [
      {
        source: { sourceUrl: sourceSas },
        targets: [
          { targetUrl: targetSas, language: "fr" },
        ],
      },
    ],
  },
});

// 从响应头获取操作 ID
const operationId = new URL(response.headers["operation-location"])
  .pathname.split("/").pop();
```

### 获取翻译状态

```typescript
import { isUnexpected, paginate } from "@azure-rest/ai-translation-document";

const statusResponse = await client.path("/document/batches/{id}", operationId).get();

if (!isUnexpected(statusResponse)) {
  const status = statusResponse.body;
  console.log(`Status: ${status.status}`);
  console.log(`Total: ${status.summary.total}`);
  console.log(`Success: ${status.summary.success}`);
}

// 分页列出文档
const docsResponse = await client.path("/document/batches/{id}/documents", operationId).get();
const documents = paginate(client, docsResponse);

for await (const doc of documents) {
  console.log(`${doc.id}: ${doc.status}`);
}
```

### 获取支持的格式

```typescript
const response = await client.path("/document/formats").get();

if (!isUnexpected(response)) {
  for (const format of response.body.value) {
    console.log(`${format.format}: ${format.fileExtensions.join(", ")}`);
  }
}
```

## 核心类型

```typescript
// 文本翻译
import type {
  TranslatorCredential,
  TranslatorTokenCredential,
} from "@azure-rest/ai-translation-text";

// 文档翻译
import type {
  DocumentTranslateParameters,
  StartTranslationDetails,
  TranslationStatus,
} from "@azure-rest/ai-translation-document";
```

## 最佳实践

1. **自动检测源语言** - 省略 `language` 参数以自动检测
2. **批量请求** - 在一次调用中翻译多个文本以提高效率
3. **使用 SAS 令牌** - 对于文档翻译，使用有时限的 SAS URL
4. **处理错误** - 在访问 body 之前始终检查 `isUnexpected(response)`
5. **区域端点** - 使用区域端点以降低延迟

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
