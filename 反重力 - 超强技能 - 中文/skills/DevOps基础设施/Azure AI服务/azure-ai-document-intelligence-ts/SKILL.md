---
name: azure-ai-document-intelligence-ts
description: "使用预构建和自定义模型从文档中提取文本、表格和结构化数据。触发词：Azure文档智能、Document Intelligence、文档提取、OCR、表格提取、发票识别、收据识别、ID识别、TypeScript SDK"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Document Intelligence REST SDK for TypeScript

使用预构建和自定义模型从文档中提取文本、表格和结构化数据。

## 安装

```bash
npm install @azure-rest/ai-document-intelligence @azure/identity
```

## 环境变量

```bash
DOCUMENT_INTELLIGENCE_ENDPOINT=https://<resource>.cognitiveservices.azure.com
DOCUMENT_INTELLIGENCE_API_KEY=<api-key>
```

## 认证

**重要**：这是一个 REST 客户端。`DocumentIntelligence` 是一个**函数**，而不是类。

### DefaultAzureCredential

```typescript
import DocumentIntelligence from "@azure-rest/ai-document-intelligence";
import { DefaultAzureCredential } from "@azure/identity";

const client = DocumentIntelligence(
  process.env.DOCUMENT_INTELLIGENCE_ENDPOINT!,
  new DefaultAzureCredential()
);
```

### API Key

```typescript
import DocumentIntelligence from "@azure-rest/ai-document-intelligence";

const client = DocumentIntelligence(
  process.env.DOCUMENT_INTELLIGENCE_ENDPOINT!,
  { key: process.env.DOCUMENT_INTELLIGENCE_API_KEY! }
);
```

## 分析文档（URL）

```typescript
import DocumentIntelligence, {
  isUnexpected,
  getLongRunningPoller,
  AnalyzeOperationOutput
} from "@azure-rest/ai-document-intelligence";

const initialResponse = await client
  .path("/documentModels/{modelId}:analyze", "prebuilt-layout")
  .post({
    contentType: "application/json",
    body: {
      urlSource: "https://example.com/document.pdf"
    },
    queryParameters: { locale: "en-US" }
  });

if (isUnexpected(initialResponse)) {
  throw initialResponse.body.error;
}

const poller = getLongRunningPoller(client, initialResponse);
const result = (await poller.pollUntilDone()).body as AnalyzeOperationOutput;

console.log("Pages:", result.analyzeResult?.pages?.length);
console.log("Tables:", result.analyzeResult?.tables?.length);
```

## 分析文档（本地文件）

```typescript
import { readFile } from "node:fs/promises";

const fileBuffer = await readFile("./document.pdf");
const base64Source = fileBuffer.toString("base64");

const initialResponse = await client
  .path("/documentModels/{modelId}:analyze", "prebuilt-invoice")
  .post({
    contentType: "application/json",
    body: { base64Source }
  });

if (isUnexpected(initialResponse)) {
  throw initialResponse.body.error;
}

const poller = getLongRunningPoller(client, initialResponse);
const result = (await poller.pollUntilDone()).body as AnalyzeOperationOutput;
```

## 预构建模型

| 模型 ID | 描述 |
|----------|-------------|
| `prebuilt-read` | OCR - 文本和语言提取 |
| `prebuilt-layout` | 文本、表格、选择标记、结构 |
| `prebuilt-invoice` | 发票字段 |
| `prebuilt-receipt` | 收据字段 |
| `prebuilt-idDocument` | 身份证件字段 |
| `prebuilt-tax.us.w2` | W-2 税表字段 |
| `prebuilt-healthInsuranceCard.us` | 医保卡字段 |
| `prebuilt-contract` | 合同字段 |
| `prebuilt-bankStatement.us` | 银行对账单字段 |

## 提取发票字段

```typescript
const initialResponse = await client
  .path("/documentModels/{modelId}:analyze", "prebuilt-invoice")
  .post({
    contentType: "application/json",
    body: { urlSource: invoiceUrl }
  });

if (isUnexpected(initialResponse)) {
  throw initialResponse.body.error;
}

const poller = getLongRunningPoller(client, initialResponse);
const result = (await poller.pollUntilDone()).body as AnalyzeOperationOutput;

const invoice = result.analyzeResult?.documents?.[0];
if (invoice) {
  console.log("Vendor:", invoice.fields?.VendorName?.content);
  console.log("Total:", invoice.fields?.InvoiceTotal?.content);
  console.log("Due Date:", invoice.fields?.DueDate?.content);
}
```

## 提取收据字段

```typescript
const initialResponse = await client
  .path("/documentModels/{modelId}:analyze", "prebuilt-receipt")
  .post({
    contentType: "application/json",
    body: { urlSource: receiptUrl }
  });

const poller = getLongRunningPoller(client, initialResponse);
const result = (await poller.pollUntilDone()).body as AnalyzeOperationOutput;

const receipt = result.analyzeResult?.documents?.[0];
if (receipt) {
  console.log("Merchant:", receipt.fields?.MerchantName?.content);
  console.log("Total:", receipt.fields?.Total?.content);
  
  for (const item of receipt.fields?.Items?.values || []) {
    console.log("Item:", item.properties?.Description?.content);
    console.log("Price:", item.properties?.TotalPrice?.content);
  }
}
```

## 列出文档模型

```typescript
import DocumentIntelligence, { isUnexpected, paginate } from "@azure-rest/ai-document-intelligence";

const response = await client.path("/documentModels").get();

if (isUnexpected(response)) {
  throw response.body.error;
}

for await (const model of paginate(client, response)) {
  console.log(model.modelId);
}
```

## 构建自定义模型

```typescript
const initialResponse = await client.path("/documentModels:build").post({
  body: {
    modelId: "my-custom-model",
    description: "Custom model for purchase orders",
    buildMode: "template",  // or "neural"
    azureBlobSource: {
      containerUrl: process.env.TRAINING_CONTAINER_SAS_URL!,
      prefix: "training-data/"
    }
  }
});

if (isUnexpected(initialResponse)) {
  throw initialResponse.body.error;
}

const poller = getLongRunningPoller(client, initialResponse);
const result = await poller.pollUntilDone();
console.log("Model built:", result.body);
```

## 构建文档分类器

```typescript
import { DocumentClassifierBuildOperationDetailsOutput } from "@azure-rest/ai-document-intelligence";

const containerSasUrl = process.env.TRAINING_CONTAINER_SAS_URL!;

const initialResponse = await client.path("/documentClassifiers:build").post({
  body: {
    classifierId: "my-classifier",
    description: "Invoice vs Receipt classifier",
    docTypes: {
      invoices: {
        azureBlobSource: { containerUrl: containerSasUrl, prefix: "invoices/" }
      },
      receipts: {
        azureBlobSource: { containerUrl: containerSasUrl, prefix: "receipts/" }
      }
    }
  }
});

if (isUnexpected(initialResponse)) {
  throw initialResponse.body.error;
}

const poller = getLongRunningPoller(client, initialResponse);
const result = (await poller.pollUntilDone()).body as DocumentClassifierBuildOperationDetailsOutput;
console.log("Classifier:", result.result?.classifierId);
```

## 分类文档

```typescript
const initialResponse = await client
  .path("/documentClassifiers/{classifierId}:analyze", "my-classifier")
  .post({
    contentType: "application/json",
    body: { urlSource: documentUrl },
    queryParameters: { split: "auto" }
  });

if (isUnexpected(initialResponse)) {
  throw initialResponse.body.error;
}

const poller = getLongRunningPoller(client, initialResponse);
const result = await poller.pollUntilDone();
console.log("Classification:", result.body.analyzeResult?.documents);
```

## 获取服务信息

```typescript
const response = await client.path("/info").get();

if (isUnexpected(response)) {
  throw response.body.error;
}

console.log("Custom model limit:", response.body.customDocumentModels.limit);
console.log("Custom model count:", response.body.customDocumentModels.count);
```

## 轮询模式

```typescript
import DocumentIntelligence, {
  isUnexpected,
  getLongRunningPoller,
  AnalyzeOperationOutput
} from "@azure-rest/ai-document-intelligence";

// 1. 启动操作
const initialResponse = await client
  .path("/documentModels/{modelId}:analyze", "prebuilt-layout")
  .post({ contentType: "application/json", body: { urlSource } });

// 2. 检查错误
if (isUnexpected(initialResponse)) {
  throw initialResponse.body.error;
}

// 3. 创建轮询器
const poller = getLongRunningPoller(client, initialResponse);

// 4. 可选：监控进度
poller.onProgress((state) => {
  console.log("Status:", state.status);
});

// 5. 等待完成
const result = (await poller.pollUntilDone()).body as AnalyzeOperationOutput;
```

## 关键类型

```typescript
import DocumentIntelligence, {
  isUnexpected,
  getLongRunningPoller,
  paginate,
  parseResultIdFromResponse,
  AnalyzeOperationOutput,
  DocumentClassifierBuildOperationDetailsOutput
} from "@azure-rest/ai-document-intelligence";
```

## 最佳实践

1. **使用 getLongRunningPoller()** - 文档分析是异步的，始终轮询获取结果
2. **检查 isUnexpected()** - 类型守卫，用于正确的错误处理
3. **选择正确的模型** - 尽可能使用预构建模型，专业文档使用自定义模型
4. **处理置信度分数** - 字段有置信度值，根据使用场景设置阈值
5. **使用分页** - 使用 `paginate()` 辅助函数列出模型
6. **优先使用 neural 模式** - 对于自定义模型，neural 模式比 template 模式能处理更多变化

## 适用场景
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
