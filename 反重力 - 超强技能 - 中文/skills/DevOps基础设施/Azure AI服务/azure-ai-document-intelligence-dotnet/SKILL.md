---
name: azure-ai-document-intelligence-dotnet
description: Azure AI Document Intelligence .NET SDK。使用预构建和自定义模型从文档中提取文本、表格和结构化数据。触发词：文档智能、Document Intelligence、文档提取、OCR、表格提取、发票识别、收据识别、身份证识别、Azure文档处理、文档分析
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.AI.DocumentIntelligence (.NET)

使用预构建和自定义模型从文档中提取文本、表格和结构化数据。

## 安装

```bash
dotnet add package Azure.AI.DocumentIntelligence
dotnet add package Azure.Identity
```

**当前版本**：v1.0.0 (GA)

## 环境变量

```bash
DOCUMENT_INTELLIGENCE_ENDPOINT=https://<resource-name>.cognitiveservices.azure.com/
DOCUMENT_INTELLIGENCE_API_KEY=<your-api-key>
BLOB_CONTAINER_SAS_URL=https://<storage>.blob.core.windows.net/<container>?<sas-token>
```

## 身份验证

### Microsoft Entra ID（推荐）

```csharp
using Azure.Identity;
using Azure.AI.DocumentIntelligence;

string endpoint = Environment.GetEnvironmentVariable("DOCUMENT_INTELLIGENCE_ENDPOINT");
var credential = new DefaultAzureCredential();
var client = new DocumentIntelligenceClient(new Uri(endpoint), credential);
```

> **注意**：Entra ID 需要**自定义子域**（例如 `https://<resource-name>.cognitiveservices.azure.com/`），而非区域端点。

### API 密钥

```csharp
string endpoint = Environment.GetEnvironmentVariable("DOCUMENT_INTELLIGENCE_ENDPOINT");
string apiKey = Environment.GetEnvironmentVariable("DOCUMENT_INTELLIGENCE_API_KEY");
var client = new DocumentIntelligenceClient(new Uri(endpoint), new AzureKeyCredential(apiKey));
```

## 客户端类型

| 客户端 | 用途 |
|--------|------|
| `DocumentIntelligenceClient` | 分析文档、分类文档 |
| `DocumentIntelligenceAdministrationClient` | 构建/管理自定义模型和分类器 |

## 预构建模型

| 模型 ID | 描述 |
|----------|-------------|
| `prebuilt-read` | 提取文本、语言、手写内容 |
| `prebuilt-layout` | 提取文本、表格、选择标记、结构 |
| `prebuilt-invoice` | 提取发票字段（供应商、项目、总计） |
| `prebuilt-receipt` | 提取收据字段（商家、项目、总计） |
| `prebuilt-idDocument` | 提取身份证件字段（姓名、出生日期、地址） |
| `prebuilt-businessCard` | 提取名片字段 |
| `prebuilt-tax.us.w2` | 提取 W-2 税务表单字段 |
| `prebuilt-healthInsuranceCard.us` | 提取健康保险卡字段 |

## 核心工作流

### 1. 分析发票

```csharp
using Azure.AI.DocumentIntelligence;

Uri invoiceUri = new Uri("https://example.com/invoice.pdf");

Operation<AnalyzeResult> operation = await client.AnalyzeDocumentAsync(
    WaitUntil.Completed, 
    "prebuilt-invoice", 
    invoiceUri);

AnalyzeResult result = operation.Value;

foreach (AnalyzedDocument document in result.Documents)
{
    if (document.Fields.TryGetValue("VendorName", out DocumentField vendorNameField)
        && vendorNameField.FieldType == DocumentFieldType.String)
    {
        string vendorName = vendorNameField.ValueString;
        Console.WriteLine($"Vendor Name: '{vendorName}', confidence: {vendorNameField.Confidence}");
    }

    if (document.Fields.TryGetValue("InvoiceTotal", out DocumentField invoiceTotalField)
        && invoiceTotalField.FieldType == DocumentFieldType.Currency)
    {
        CurrencyValue invoiceTotal = invoiceTotalField.ValueCurrency;
        Console.WriteLine($"Invoice Total: '{invoiceTotal.CurrencySymbol}{invoiceTotal.Amount}'");
    }
    
    // 提取行项目
    if (document.Fields.TryGetValue("Items", out DocumentField itemsField)
        && itemsField.FieldType == DocumentFieldType.List)
    {
        foreach (DocumentField item in itemsField.ValueList)
        {
            var itemFields = item.ValueDictionary;
            if (itemFields.TryGetValue("Description", out DocumentField descField))
                Console.WriteLine($"  Item: {descField.ValueString}");
        }
    }
}
```

### 2. 提取布局（文本、表格、结构）

```csharp
Uri fileUri = new Uri("https://example.com/document.pdf");

Operation<AnalyzeResult> operation = await client.AnalyzeDocumentAsync(
    WaitUntil.Completed, 
    "prebuilt-layout", 
    fileUri);

AnalyzeResult result = operation.Value;

// 按页提取文本
foreach (DocumentPage page in result.Pages)
{
    Console.WriteLine($"Page {page.PageNumber}: {page.Lines.Count} lines, {page.Words.Count} words");
    
    foreach (DocumentLine line in page.Lines)
    {
        Console.WriteLine($"  Line: '{line.Content}'");
    }
}

// 提取表格
foreach (DocumentTable table in result.Tables)
{
    Console.WriteLine($"Table: {table.RowCount} rows x {table.ColumnCount} columns");
    foreach (DocumentTableCell cell in table.Cells)
    {
        Console.WriteLine($"  Cell ({cell.RowIndex}, {cell.ColumnIndex}): {cell.Content}");
    }
}
```

### 3. 分析收据

```csharp
Operation<AnalyzeResult> operation = await client.AnalyzeDocumentAsync(
    WaitUntil.Completed, 
    "prebuilt-receipt", 
    receiptUri);

AnalyzeResult result = operation.Value;

foreach (AnalyzedDocument document in result.Documents)
{
    if (document.Fields.TryGetValue("MerchantName", out DocumentField merchantField))
        Console.WriteLine($"Merchant: {merchantField.ValueString}");
        
    if (document.Fields.TryGetValue("Total", out DocumentField totalField))
        Console.WriteLine($"Total: {totalField.ValueCurrency.Amount}");
        
    if (document.Fields.TryGetValue("TransactionDate", out DocumentField dateField))
        Console.WriteLine($"Date: {dateField.ValueDate}");
}
```

### 4. 构建自定义模型

```csharp
var adminClient = new DocumentIntelligenceAdministrationClient(
    new Uri(endpoint), 
    new AzureKeyCredential(apiKey));

string modelId = "my-custom-model";
Uri blobContainerUri = new Uri("<blob-container-sas-url>");

var blobSource = new BlobContentSource(blobContainerUri);
var options = new BuildDocumentModelOptions(modelId, DocumentBuildMode.Template, blobSource);

Operation<DocumentModelDetails> operation = await adminClient.BuildDocumentModelAsync(
    WaitUntil.Completed, 
    options);

DocumentModelDetails model = operation.Value;

Console.WriteLine($"Model ID: {model.ModelId}");
Console.WriteLine($"Created: {model.CreatedOn}");

foreach (var docType in model.DocumentTypes)
{
    Console.WriteLine($"Document type: {docType.Key}");
    foreach (var field in docType.Value.FieldSchema)
    {
        Console.WriteLine($"  Field: {field.Key}, Confidence: {docType.Value.FieldConfidence[field.Key]}");
    }
}
```

### 5. 构建文档分类器

```csharp
string classifierId = "my-classifier";
Uri blobContainerUri = new Uri("<blob-container-sas-url>");

var sourceA = new BlobContentSource(blobContainerUri) { Prefix = "TypeA/train" };
var sourceB = new BlobContentSource(blobContainerUri) { Prefix = "TypeB/train" };

var docTypes = new Dictionary<string, ClassifierDocumentTypeDetails>()
{
    { "TypeA", new ClassifierDocumentTypeDetails(sourceA) },
    { "TypeB", new ClassifierDocumentTypeDetails(sourceB) }
};

var options = new BuildClassifierOptions(classifierId, docTypes);

Operation<DocumentClassifierDetails> operation = await adminClient.BuildClassifierAsync(
    WaitUntil.Completed, 
    options);

DocumentClassifierDetails classifier = operation.Value;
Console.WriteLine($"Classifier ID: {classifier.ClassifierId}");
```

### 6. 分类文档

```csharp
string classifierId = "my-classifier";
Uri documentUri = new Uri("https://example.com/document.pdf");

var options = new ClassifyDocumentOptions(classifierId, documentUri);

Operation<AnalyzeResult> operation = await client.ClassifyDocumentAsync(
    WaitUntil.Completed, 
    options);

AnalyzeResult result = operation.Value;

foreach (AnalyzedDocument document in result.Documents)
{
    Console.WriteLine($"Document type: {document.DocumentType}, confidence: {document.Confidence}");
}
```

### 7. 管理模型

```csharp
// 获取资源详情
DocumentIntelligenceResourceDetails resourceDetails = await adminClient.GetResourceDetailsAsync();
Console.WriteLine($"Custom models: {resourceDetails.CustomDocumentModels.Count}/{resourceDetails.CustomDocumentModels.Limit}");

// 获取特定模型
DocumentModelDetails model = await adminClient.GetModelAsync("my-model-id");
Console.WriteLine($"Model: {model.ModelId}, Created: {model.CreatedOn}");

// 列出模型
await foreach (DocumentModelDetails modelItem in adminClient.GetModelsAsync())
{
    Console.WriteLine($"Model: {modelItem.ModelId}");
}

// 删除模型
await adminClient.DeleteModelAsync("my-model-id");
```

## 关键类型参考

| 类型 | 描述 |
|------|------|
| `DocumentIntelligenceClient` | 分析主客户端 |
| `DocumentIntelligenceAdministrationClient` | 模型管理 |
| `AnalyzeResult` | 文档分析结果 |
| `AnalyzedDocument` | 结果中的单个文档 |
| `DocumentField` | 提取的字段，包含值和置信度 |
| `DocumentFieldType` | String、Date、Number、Currency 等 |
| `DocumentPage` | 页面信息（行、词、选择标记） |
| `DocumentTable` | 提取的表格及单元格 |
| `DocumentModelDetails` | 自定义模型元数据 |
| `BlobContentSource` | 训练数据源 |

## 构建模式

| 模式 | 用例 |
|------|------|
| `DocumentBuildMode.Template` | 固定布局文档（表单） |
| `DocumentBuildMode.Neural` | 可变布局文档 |

## 最佳实践

1. **生产环境使用 DefaultAzureCredential**
2. **复用客户端实例** — 客户端是线程安全的
3. **处理长时间运行的操作** — 使用 `WaitUntil.Completed` 简化操作
4. **检查字段置信度** — 始终验证 `Confidence` 属性
5. **选择合适的模型** — 常见文档使用预构建模型，专业文档使用自定义模型
6. **使用自定义子域** — Entra ID 身份验证必需

## 错误处理

```csharp
using Azure;

try
{
    var operation = await client.AnalyzeDocumentAsync(
        WaitUntil.Completed, 
        "prebuilt-invoice", 
        documentUri);
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Error: {ex.Status} - {ex.Message}");
}
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|---------|---------|
| `Azure.AI.DocumentIntelligence` | 文档分析（本 SDK） | `dotnet add package Azure.AI.DocumentIntelligence` |
| `Azure.AI.FormRecognizer` | 旧版 SDK（已弃用） | 请改用 DocumentIntelligence |

## 参考链接

| 资源 | URL |
|----------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.AI.DocumentIntelligence |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.ai.documentintelligence |
| GitHub 示例 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/documentintelligence/Azure.AI.DocumentIntelligence/samples |
| Document Intelligence Studio | https://documentintelligence.ai.azure.com/ |
| 预构建模型 | https://aka.ms/azsdk/formrecognizer/models |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述描述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
