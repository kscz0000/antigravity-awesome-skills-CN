---
name: azure-ai-contentsafety-java
description: "使用 Azure AI Content Safety SDK for Java 构建内容审核应用程序。触发词：内容安全Java、Azure内容审核、文本安全分析、图像审核Java、黑名单管理、仇恨言论检测、有害内容过滤"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure AI Content Safety SDK for Java

使用 Azure AI Content Safety SDK for Java 构建内容审核应用程序。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-contentsafety</artifactId>
    <version>1.1.0-beta.1</version>
</dependency>
```

## 创建客户端

### 使用 API 密钥

```java
import com.azure.ai.contentsafety.ContentSafetyClient;
import com.azure.ai.contentsafety.ContentSafetyClientBuilder;
import com.azure.ai.contentsafety.BlocklistClient;
import com.azure.ai.contentsafety.BlocklistClientBuilder;
import com.azure.core.credential.KeyCredential;

String endpoint = System.getenv("CONTENT_SAFETY_ENDPOINT");
String key = System.getenv("CONTENT_SAFETY_KEY");

ContentSafetyClient contentSafetyClient = new ContentSafetyClientBuilder()
    .credential(new KeyCredential(key))
    .endpoint(endpoint)
    .buildClient();

BlocklistClient blocklistClient = new BlocklistClientBuilder()
    .credential(new KeyCredential(key))
    .endpoint(endpoint)
    .buildClient();
```

### 使用 DefaultAzureCredential

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

ContentSafetyClient client = new ContentSafetyClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(endpoint)
    .buildClient();
```

## 核心概念

### 危害类别
| 类别 | 描述 |
|----------|-------------|
| Hate（仇恨） | 基于身份群体的歧视性语言 |
| Sexual（性内容） | 性内容、关系、行为 |
| Violence（暴力） | 身体伤害、武器、损伤 |
| Self-harm（自残） | 自伤、自杀相关内容 |

### 严重程度级别
- 文本：0-7 级（默认输出 0、2、4、6）
- 图像：0、2、4、6（精简级别）

## 核心模式

### 分析文本

```java
import com.azure.ai.contentsafety.models.*;

AnalyzeTextResult result = contentSafetyClient.analyzeText(
    new AnalyzeTextOptions("This is text to analyze"));

for (TextCategoriesAnalysis category : result.getCategoriesAnalysis()) {
    System.out.printf("Category: %s, Severity: %d%n",
        category.getCategory(),
        category.getSeverity());
}
```

### 带选项分析文本

```java
AnalyzeTextOptions options = new AnalyzeTextOptions("Text to analyze")
    .setCategories(Arrays.asList(
        TextCategory.HATE,
        TextCategory.VIOLENCE))
    .setOutputType(AnalyzeTextOutputType.EIGHT_SEVERITY_LEVELS);

AnalyzeTextResult result = contentSafetyClient.analyzeText(options);
```

### 使用黑名单分析文本

```java
AnalyzeTextOptions options = new AnalyzeTextOptions("I h*te you and want to k*ll you")
    .setBlocklistNames(Arrays.asList("my-blocklist"))
    .setHaltOnBlocklistHit(true);

AnalyzeTextResult result = contentSafetyClient.analyzeText(options);

if (result.getBlocklistsMatch() != null) {
    for (TextBlocklistMatch match : result.getBlocklistsMatch()) {
        System.out.printf("Blocklist: %s, Item: %s, Text: %s%n",
            match.getBlocklistName(),
            match.getBlocklistItemId(),
            match.getBlocklistItemText());
    }
}
```

### 分析图像

```java
import com.azure.ai.contentsafety.models.*;
import com.azure.core.util.BinaryData;
import java.nio.file.Files;
import java.nio.file.Paths;

// 从文件读取
byte[] imageBytes = Files.readAllBytes(Paths.get("image.png"));
ContentSafetyImageData imageData = new ContentSafetyImageData()
    .setContent(BinaryData.fromBytes(imageBytes));

AnalyzeImageResult result = contentSafetyClient.analyzeImage(
    new AnalyzeImageOptions(imageData));

for (ImageCategoriesAnalysis category : result.getCategoriesAnalysis()) {
    System.out.printf("Category: %s, Severity: %d%n",
        category.getCategory(),
        category.getSeverity());
}
```

### 从 URL 分析图像

```java
ContentSafetyImageData imageData = new ContentSafetyImageData()
    .setBlobUrl("https://example.com/image.jpg");

AnalyzeImageResult result = contentSafetyClient.analyzeImage(
    new AnalyzeImageOptions(imageData));
```

## 黑名单管理

### 创建或更新黑名单

```java
import com.azure.core.http.rest.RequestOptions;
import com.azure.core.http.rest.Response;
import com.azure.core.util.BinaryData;
import java.util.Map;

Map<String, String> description = Map.of("description", "Custom blocklist");
BinaryData resource = BinaryData.fromObject(description);

Response<BinaryData> response = blocklistClient.createOrUpdateTextBlocklistWithResponse(
    "my-blocklist", resource, new RequestOptions());

if (response.getStatusCode() == 201) {
    System.out.println("Blocklist created");
} else if (response.getStatusCode() == 200) {
    System.out.println("Blocklist updated");
}
```

### 添加黑名单项

```java
import com.azure.ai.contentsafety.models.*;
import java.util.Arrays;

List<TextBlocklistItem> items = Arrays.asList(
    new TextBlocklistItem("badword1").setDescription("Offensive term"),
    new TextBlocklistItem("badword2").setDescription("Another term")
);

AddOrUpdateTextBlocklistItemsResult result = blocklistClient.addOrUpdateBlocklistItems(
    "my-blocklist",
    new AddOrUpdateTextBlocklistItemsOptions(items));

for (TextBlocklistItem item : result.getBlocklistItems()) {
    System.out.printf("Added: %s (ID: %s)%n",
        item.getText(),
        item.getBlocklistItemId());
}
```

### 列出黑名单

```java
PagedIterable<TextBlocklist> blocklists = blocklistClient.listTextBlocklists();

for (TextBlocklist blocklist : blocklists) {
    System.out.printf("Blocklist: %s, Description: %s%n",
        blocklist.getName(),
        blocklist.getDescription());
}
```

### 获取黑名单

```java
TextBlocklist blocklist = blocklistClient.getTextBlocklist("my-blocklist");
System.out.println("Name: " + blocklist.getName());
```

### 列出黑名单项

```java
PagedIterable<TextBlocklistItem> items = 
    blocklistClient.listTextBlocklistItems("my-blocklist");

for (TextBlocklistItem item : items) {
    System.out.printf("ID: %s, Text: %s%n",
        item.getBlocklistItemId(),
        item.getText());
}
```

### 移除黑名单项

```java
List<String> itemIds = Arrays.asList("item-id-1", "item-id-2");

blocklistClient.removeBlocklistItems(
    "my-blocklist",
    new RemoveTextBlocklistItemsOptions(itemIds));
```

### 删除黑名单

```java
blocklistClient.deleteTextBlocklist("my-blocklist");
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    contentSafetyClient.analyzeText(new AnalyzeTextOptions("test"));
} catch (HttpResponseException e) {
    System.out.println("Status: " + e.getResponse().getStatusCode());
    System.out.println("Error: " + e.getMessage());
    // 常见错误码：InvalidRequestBody、ResourceNotFound、TooManyRequests
}
```

## 环境变量

```bash
CONTENT_SAFETY_ENDPOINT=https://<resource>.cognitiveservices.azure.com/
CONTENT_SAFETY_KEY=<your-api-key>
```

## 最佳实践

1. **黑名单延迟**：更改约需 5 分钟生效
2. **类别选择**：仅请求所需类别以降低延迟
3. **严重程度阈值**：严格审核通常拦截严重程度 >= 4 的内容
4. **批量处理**：并行处理多项以提高吞吐量
5. **缓存**：在适当场景缓存黑名单结果

## 触发词

- "content safety Java"
- "content moderation Azure"
- "analyze text safety"
- "image moderation Java"
- "blocklist management"
- "hate speech detection"
- "harmful content filter"

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
