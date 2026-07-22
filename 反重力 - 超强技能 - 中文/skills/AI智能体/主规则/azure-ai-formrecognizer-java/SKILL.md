---
name: azure-ai-formrecognizer-java
description: "使用 Azure AI Document Intelligence Java SDK 构建文档分析应用程序。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Document Intelligence (Form Recognizer) Java SDK

使用 Azure AI Document Intelligence Java SDK 构建文档分析应用程序。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-formrecognizer</artifactId>
    <version>4.2.0-beta.1</version>
</dependency>
```

## 客户端创建

### DocumentAnalysisClient

```java
import com.azure.ai.formrecognizer.documentanalysis.DocumentAnalysisClient;
import com.azure.ai.formrecognizer.documentanalysis.DocumentAnalysisClientBuilder;
import com.azure.core.credential.AzureKeyCredential;

DocumentAnalysisClient client = new DocumentAnalysisClientBuilder()
    .credential(new AzureKeyCredential("{key}"))
    .endpoint("{endpoint}")
    .buildClient();
```

### DocumentModelAdministrationClient

```java
import com.azure.ai.formrecognizer.documentanalysis.administration.DocumentModelAdministrationClient;
import com.azure.ai.formrecognizer.documentanalysis.administration.DocumentModelAdministrationClientBuilder;

DocumentModelAdministrationClient adminClient = new DocumentModelAdministrationClientBuilder()
    .credential(new AzureKeyCredential("{key}"))
    .endpoint("{endpoint}")
    .buildClient();
```

### 使用 DefaultAzureCredential

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

DocumentAnalysisClient client = new DocumentAnalysisClientBuilder()
    .endpoint("{endpoint}")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

## 预置模型

| 模型 ID | 用途 |
|----------|---------|
| `prebuilt-layout` | 提取文本、表格、选择标记 |
| `prebuilt-document` | 通用文档，包含键值对 |
| `prebuilt-receipt` | 收据数据提取 |
| `prebuilt-invoice` | 发票字段提取 |
| `prebuilt-businessCard` | 名片解析 |
| `prebuilt-idDocument` | 身份证件（护照、驾照） |
| `prebuilt-tax.us.w2` | 美国 W2 税务表格 |

## 核心模式

### 提取布局

```java
import com.azure.ai.formrecognizer.documentanalysis.models.*;
import com.azure.core.util.BinaryData;
import com.azure.core.util.polling.SyncPoller;
import java.io.File;

File document = new File("document.pdf");
BinaryData documentData = BinaryData.fromFile(document.toPath());

SyncPoller<OperationResult, AnalyzeResult> poller = 
    client.beginAnalyzeDocument("prebuilt-layout", documentData);

AnalyzeResult result = poller.getFinalResult();

// 处理页面
for (DocumentPage page : result.getPages()) {
    System.out.printf("Page %d: %.2f x %.2f %s%n",
        page.getPageNumber(),
        page.getWidth(),
        page.getHeight(),
        page.getUnit());
    
    // 行
    for (DocumentLine line : page.getLines()) {
        System.out.println("Line: " + line.getContent());
    }
    
    // 选择标记（复选框）
    for (DocumentSelectionMark mark : page.getSelectionMarks()) {
        System.out.printf("Checkbox: %s (confidence: %.2f)%n",
            mark.getSelectionMarkState(),
            mark.getConfidence());
    }
}

// 表格
for (DocumentTable table : result.getTables()) {
    System.out.printf("Table: %d rows x %d columns%n",
        table.getRowCount(),
        table.getColumnCount());
    
    for (DocumentTableCell cell : table.getCells()) {
        System.out.printf("Cell[%d,%d]: %s%n",
            cell.getRowIndex(),
            cell.getColumnIndex(),
            cell.getContent());
    }
}
```

### 从 URL 分析

```java
String documentUrl = "https://example.com/invoice.pdf";

SyncPoller<OperationResult, AnalyzeResult> poller = 
    client.beginAnalyzeDocumentFromUrl("prebuilt-invoice", documentUrl);

AnalyzeResult result = poller.getFinalResult();
```

### 分析收据

```java
SyncPoller<OperationResult, AnalyzeResult> poller = 
    client.beginAnalyzeDocumentFromUrl("prebuilt-receipt", receiptUrl);

AnalyzeResult result = poller.getFinalResult();

for (AnalyzedDocument doc : result.getDocuments()) {
    Map<String, DocumentField> fields = doc.getFields();
    
    DocumentField merchantName = fields.get("MerchantName");
    if (merchantName != null && merchantName.getType() == DocumentFieldType.STRING) {
        System.out.printf("Merchant: %s (confidence: %.2f)%n",
            merchantName.getValueAsString(),
            merchantName.getConfidence());
    }
    
    DocumentField transactionDate = fields.get("TransactionDate");
    if (transactionDate != null && transactionDate.getType() == DocumentFieldType.DATE) {
        System.out.printf("Date: %s%n", transactionDate.getValueAsDate());
    }
    
    DocumentField items = fields.get("Items");
    if (items != null && items.getType() == DocumentFieldType.LIST) {
        for (DocumentField item : items.getValueAsList()) {
            Map<String, DocumentField> itemFields = item.getValueAsMap();
            System.out.printf("Item: %s, Price: %.2f%n",
                itemFields.get("Name").getValueAsString(),
                itemFields.get("Price").getValueAsDouble());
        }
    }
}
```

### 通用文档分析

```java
SyncPoller<OperationResult, AnalyzeResult> poller = 
    client.beginAnalyzeDocumentFromUrl("prebuilt-document", documentUrl);

AnalyzeResult result = poller.getFinalResult();

// 键值对
for (DocumentKeyValuePair kvp : result.getKeyValuePairs()) {
    System.out.printf("Key: %s => Value: %s%n",
        kvp.getKey().getContent(),
        kvp.getValue() != null ? kvp.getValue().getContent() : "null");
}
```

## 自定义模型

### 构建自定义模型

```java
import com.azure.ai.formrecognizer.documentanalysis.administration.models.*;

String blobContainerUrl = "{SAS_URL_of_training_data}";
String prefix = "training-docs/";

SyncPoller<OperationResult, DocumentModelDetails> poller = adminClient.beginBuildDocumentModel(
    blobContainerUrl,
    DocumentModelBuildMode.TEMPLATE,
    prefix,
    new BuildDocumentModelOptions()
        .setModelId("my-custom-model")
        .setDescription("Custom invoice model"),
    Context.NONE);

DocumentModelDetails model = poller.getFinalResult();

System.out.println("Model ID: " + model.getModelId());
System.out.println("Created: " + model.getCreatedOn());

model.getDocumentTypes().forEach((docType, details) -> {
    System.out.println("Document type: " + docType);
    details.getFieldSchema().forEach((field, schema) -> {
        System.out.printf("  Field: %s (%s)%n", field, schema.getType());
    });
});
```

### 使用自定义模型分析

```java
SyncPoller<OperationResult, AnalyzeResult> poller = 
    client.beginAnalyzeDocumentFromUrl("my-custom-model", documentUrl);

AnalyzeResult result = poller.getFinalResult();

for (AnalyzedDocument doc : result.getDocuments()) {
    System.out.printf("Document type: %s (confidence: %.2f)%n",
        doc.getDocType(),
        doc.getConfidence());
    
    doc.getFields().forEach((name, field) -> {
        System.out.printf("Field '%s': %s (confidence: %.2f)%n",
            name,
            field.getContent(),
            field.getConfidence());
    });
}
```

### 组合模型

```java
List<String> modelIds = Arrays.asList("model-1", "model-2", "model-3");

SyncPoller<OperationResult, DocumentModelDetails> poller = 
    adminClient.beginComposeDocumentModel(
        modelIds,
        new ComposeDocumentModelOptions()
            .setModelId("composed-model")
            .setDescription("Composed from multiple models"));

DocumentModelDetails composedModel = poller.getFinalResult();
```

### 管理模型

```java
// 列出模型
PagedIterable<DocumentModelSummary> models = adminClient.listDocumentModels();
for (DocumentModelSummary summary : models) {
    System.out.printf("Model: %s, Created: %s%n",
        summary.getModelId(),
        summary.getCreatedOn());
}

// 获取模型详情
DocumentModelDetails model = adminClient.getDocumentModel("model-id");

// 删除模型
adminClient.deleteDocumentModel("model-id");

// 检查资源限制
ResourceDetails resources = adminClient.getResourceDetails();
System.out.printf("Models: %d / %d%n",
    resources.getCustomDocumentModelCount(),
    resources.getCustomDocumentModelLimit());
```

## 文档分类

### 构建分类器

```java
Map<String, ClassifierDocumentTypeDetails> docTypes = new HashMap<>();
docTypes.put("invoice", new ClassifierDocumentTypeDetails()
    .setAzureBlobSource(new AzureBlobContentSource(containerUrl).setPrefix("invoices/")));
docTypes.put("receipt", new ClassifierDocumentTypeDetails()
    .setAzureBlobSource(new AzureBlobContentSource(containerUrl).setPrefix("receipts/")));

SyncPoller<OperationResult, DocumentClassifierDetails> poller = 
    adminClient.beginBuildDocumentClassifier(docTypes,
        new BuildDocumentClassifierOptions().setClassifierId("my-classifier"));

DocumentClassifierDetails classifier = poller.getFinalResult();
```

### 分类文档

```java
SyncPoller<OperationResult, AnalyzeResult> poller = 
    client.beginClassifyDocumentFromUrl("my-classifier", documentUrl, Context.NONE);

AnalyzeResult result = poller.getFinalResult();

for (AnalyzedDocument doc : result.getDocuments()) {
    System.out.printf("Classified as: %s (confidence: %.2f)%n",
        doc.getDocType(),
        doc.getConfidence());
}
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    client.beginAnalyzeDocumentFromUrl("prebuilt-receipt", "invalid-url");
} catch (HttpResponseException e) {
    System.out.println("Status: " + e.getResponse().getStatusCode());
    System.out.println("Error: " + e.getMessage());
}
```

## 环境变量

```bash
FORM_RECOGNIZER_ENDPOINT=https://<resource>.cognitiveservices.azure.com/
FORM_RECOGNIZER_KEY=<your-api-key>
```

## 触发词

- "document intelligence Java"
- "form recognizer SDK"
- "extract text from PDF"
- "OCR document Java"
- "analyze invoice receipt"
- "custom document model"
- "document classification"

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 输出不应替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
