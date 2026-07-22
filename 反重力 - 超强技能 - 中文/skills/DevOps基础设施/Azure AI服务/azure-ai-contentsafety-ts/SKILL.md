---
name: azure-ai-contentsafety-ts
description: "分析文本和图像中的有害内容，支持自定义屏蔽列表。触发词：Azure内容安全、内容审核、文本分析、图像审核、敏感词过滤、内容过滤、有害内容检测、屏蔽列表、内容审查"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure AI Content Safety REST SDK for TypeScript

分析文本和图像中的有害内容，支持自定义屏蔽列表。

## 安装

```bash
npm install @azure-rest/ai-content-safety @azure/identity @azure/core-auth
```

## 环境变量

```bash
CONTENT_SAFETY_ENDPOINT=https://<resource>.cognitiveservices.azure.com
CONTENT_SAFETY_KEY=<api-key>
```

## 认证

**重要**：这是一个 REST 客户端。`ContentSafetyClient` 是一个**函数**，而不是类。

### API Key

```typescript
import ContentSafetyClient from "@azure-rest/ai-content-safety";
import { AzureKeyCredential } from "@azure/core-auth";

const client = ContentSafetyClient(
  process.env.CONTENT_SAFETY_ENDPOINT!,
  new AzureKeyCredential(process.env.CONTENT_SAFETY_KEY!)
);
```

### DefaultAzureCredential

```typescript
import ContentSafetyClient from "@azure-rest/ai-content-safety";
import { DefaultAzureCredential } from "@azure/identity";

const client = ContentSafetyClient(
  process.env.CONTENT_SAFETY_ENDPOINT!,
  new DefaultAzureCredential()
);
```

## 分析文本

```typescript
import ContentSafetyClient, { isUnexpected } from "@azure-rest/ai-content-safety";

const result = await client.path("/text:analyze").post({
  body: {
    text: "Text content to analyze",
    categories: ["Hate", "Sexual", "Violence", "SelfHarm"],
    outputType: "FourSeverityLevels"  // or "EightSeverityLevels"
  }
});

if (isUnexpected(result)) {
  throw result.body;
}

for (const analysis of result.body.categoriesAnalysis) {
  console.log(`${analysis.category}: severity ${analysis.severity}`);
}
```

## 分析图像

### Base64 内容

```typescript
import { readFileSync } from "node:fs";

const imageBuffer = readFileSync("./image.png");
const base64Image = imageBuffer.toString("base64");

const result = await client.path("/image:analyze").post({
  body: {
    image: { content: base64Image }
  }
});

if (isUnexpected(result)) {
  throw result.body;
}

for (const analysis of result.body.categoriesAnalysis) {
  console.log(`${analysis.category}: severity ${analysis.severity}`);
}
```

### Blob URL

```typescript
const result = await client.path("/image:analyze").post({
  body: {
    image: { blobUrl: "https://storage.blob.core.windows.net/container/image.png" }
  }
});
```

## 屏蔽列表管理

### 创建屏蔽列表

```typescript
const result = await client
  .path("/text/blocklists/{blocklistName}", "my-blocklist")
  .patch({
    contentType: "application/merge-patch+json",
    body: {
      description: "Custom blocklist for prohibited terms"
    }
  });

if (isUnexpected(result)) {
  throw result.body;
}

console.log(`Created: ${result.body.blocklistName}`);
```

### 添加屏蔽项

```typescript
const result = await client
  .path("/text/blocklists/{blocklistName}:addOrUpdateBlocklistItems", "my-blocklist")
  .post({
    body: {
      blocklistItems: [
        { text: "prohibited-term-1", description: "First blocked term" },
        { text: "prohibited-term-2", description: "Second blocked term" }
      ]
    }
  });

if (isUnexpected(result)) {
  throw result.body;
}

for (const item of result.body.blocklistItems ?? []) {
  console.log(`Added: ${item.blocklistItemId}`);
}
```

### 使用屏蔽列表分析

```typescript
const result = await client.path("/text:analyze").post({
  body: {
    text: "Text that might contain blocked terms",
    blocklistNames: ["my-blocklist"],
    haltOnBlocklistHit: false
  }
});

if (isUnexpected(result)) {
  throw result.body;
}

// 检查屏蔽列表匹配
if (result.body.blocklistsMatch) {
  for (const match of result.body.blocklistsMatch) {
    console.log(`Blocked: "${match.blocklistItemText}" from ${match.blocklistName}`);
  }
}
```

### 列出屏蔽列表

```typescript
const result = await client.path("/text/blocklists").get();

if (isUnexpected(result)) {
  throw result.body;
}

for (const blocklist of result.body.value ?? []) {
  console.log(`${blocklist.blocklistName}: ${blocklist.description}`);
}
```

### 删除屏蔽列表

```typescript
await client.path("/text/blocklists/{blocklistName}", "my-blocklist").delete();
```

## 有害内容类别

| 类别 | API 术语 | 描述 |
|----------|----------|-------------|
| 仇恨与公平 | `Hate` | 针对身份群体的歧视性语言 |
| 性内容 | `Sexual` | 性内容、裸露、色情 |
| 暴力 | `Violence` | 身体伤害、武器、恐怖主义 |
| 自残 | `SelfHarm` | 自伤、自杀、饮食失调 |

## 严重程度级别

| 级别 | 风险 | 建议操作 |
|-------|------|-------------------|
| 0 | 安全 | 允许 |
| 2 | 低 | 审核或允许并警告 |
| 4 | 中 | 拦截或需人工审核 |
| 6 | 高 | 立即拦截 |

**输出类型**：
- `FourSeverityLevels`（默认）：返回 0, 2, 4, 6
- `EightSeverityLevels`：返回 0-7

## 内容审核助手

```typescript
import ContentSafetyClient, { 
  isUnexpected, 
  TextCategoriesAnalysisOutput 
} from "@azure-rest/ai-content-safety";

interface ModerationResult {
  isAllowed: boolean;
  flaggedCategories: string[];
  maxSeverity: number;
  blocklistMatches: string[];
}

async function moderateContent(
  client: ReturnType<typeof ContentSafetyClient>,
  text: string,
  maxAllowedSeverity = 2,
  blocklistNames: string[] = []
): Promise<ModerationResult> {
  const result = await client.path("/text:analyze").post({
    body: { text, blocklistNames, haltOnBlocklistHit: false }
  });

  if (isUnexpected(result)) {
    throw result.body;
  }

  const flaggedCategories = result.body.categoriesAnalysis
    .filter(c => (c.severity ?? 0) > maxAllowedSeverity)
    .map(c => c.category!);

  const maxSeverity = Math.max(
    ...result.body.categoriesAnalysis.map(c => c.severity ?? 0)
  );

  const blocklistMatches = (result.body.blocklistsMatch ?? [])
    .map(m => m.blocklistItemText!);

  return {
    isAllowed: flaggedCategories.length === 0 && blocklistMatches.length === 0,
    flaggedCategories,
    maxSeverity,
    blocklistMatches
  };
}
```

## API 端点

| 操作 | 方法 | 路径 |
|-----------|--------|------|
| 分析文本 | POST | `/text:analyze` |
| 分析图像 | POST | `/image:analyze` |
| 创建/更新屏蔽列表 | PATCH | `/text/blocklists/{blocklistName}` |
| 列出屏蔽列表 | GET | `/text/blocklists` |
| 删除屏蔽列表 | DELETE | `/text/blocklists/{blocklistName}` |
| 添加屏蔽项 | POST | `/text/blocklists/{blocklistName}:addOrUpdateBlocklistItems` |
| 列出屏蔽项 | GET | `/text/blocklists/{blocklistName}/blocklistItems` |
| 移除屏蔽项 | POST | `/text/blocklists/{blocklistName}:removeBlocklistItems` |

## 关键类型

```typescript
import ContentSafetyClient, {
  isUnexpected,
  AnalyzeTextParameters,
  AnalyzeImageParameters,
  TextCategoriesAnalysisOutput,
  ImageCategoriesAnalysisOutput,
  TextBlocklist,
  TextBlocklistItem
} from "@azure-rest/ai-content-safety";
```

## 最佳实践

1. **始终使用 isUnexpected()** - 用于错误处理的类型守卫
2. **设置适当的阈值** - 不同类别可能需要不同的严重程度阈值
3. **使用屏蔽列表处理领域特定术语** - 用自定义规则补充 AI 检测
4. **记录审核决策** - 保留审计记录以符合合规要求
5. **处理边界情况** - 空文本、超长文本、不支持的图像格式

## 使用时机
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
