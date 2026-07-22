---
name: azure-search-documents-dotnet
description: Azure AI Search .NET SDK (Azure.Search.Documents)。用于构建支持全文搜索、向量搜索、语义搜索和混合搜索的搜索应用程序。当用户要求'使用 Azure Search .NET SDK 构建搜索应用'、'全文搜索'、'向量搜索'、'语义搜索'、'混合搜索'、'Azure.Search.Documents'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.Search.Documents (.NET)

构建支持全文搜索、向量搜索、语义搜索和混合搜索功能的搜索应用程序。

## 安装

```bash
dotnet add package Azure.Search.Documents
dotnet add package Azure.Identity
```

**当前版本**：稳定版 v11.7.0，预览版 v11.8.0-beta.1

## 环境变量

```bash
SEARCH_ENDPOINT=https://<search-service>.search.windows.net
SEARCH_INDEX_NAME=<index-name>
# 用于 API 密钥认证（生产环境不推荐）
SEARCH_API_KEY=<api-key>
```

## 认证

**DefaultAzureCredential（推荐）**：
```csharp
using Azure.Identity;
using Azure.Search.Documents;

var credential = new DefaultAzureCredential();
var client = new SearchClient(
    new Uri(Environment.GetEnvironmentVariable("SEARCH_ENDPOINT")),
    Environment.GetEnvironmentVariable("SEARCH_INDEX_NAME"),
    credential);
```

**API 密钥**：
```csharp
using Azure;
using Azure.Search.Documents;

var credential = new AzureKeyCredential(
    Environment.GetEnvironmentVariable("SEARCH_API_KEY"));
var client = new SearchClient(
    new Uri(Environment.GetEnvironmentVariable("SEARCH_ENDPOINT")),
    Environment.GetEnvironmentVariable("SEARCH_INDEX_NAME"),
    credential);
```

## 客户端选择

| 客户端 | 用途 |
|--------|------|
| `SearchClient` | 查询索引，上传/更新/删除文档 |
| `SearchIndexClient` | 创建/管理索引、同义词映射 |
| `SearchIndexerClient` | 管理索引器、技能集、数据源 |

## 索引创建

### 使用 FieldBuilder（推荐）

```csharp
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

// 使用特性定义模型
public class Hotel
{
    [SimpleField(IsKey = true, IsFilterable = true)]
    public string HotelId { get; set; }

    [SearchableField(IsSortable = true)]
    public string HotelName { get; set; }

    [SearchableField(AnalyzerName = LexicalAnalyzerName.EnLucene)]
    public string Description { get; set; }

    [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
    public double? Rating { get; set; }

    [VectorSearchField(VectorSearchDimensions = 1536, VectorSearchProfileName = "vector-profile")]
    public ReadOnlyMemory<float>? DescriptionVector { get; set; }
}

// 创建索引
var indexClient = new SearchIndexClient(endpoint, credential);
var fieldBuilder = new FieldBuilder();
var fields = fieldBuilder.Build(typeof(Hotel));

var index = new SearchIndex("hotels")
{
    Fields = fields,
    VectorSearch = new VectorSearch
    {
        Profiles = { new VectorSearchProfile("vector-profile", "hnsw-algo") },
        Algorithms = { new HnswAlgorithmConfiguration("hnsw-algo") }
    }
};

await indexClient.CreateOrUpdateIndexAsync(index);
```

### 手动字段定义

```csharp
var index = new SearchIndex("hotels")
{
    Fields =
    {
        new SimpleField("hotelId", SearchFieldDataType.String) { IsKey = true, IsFilterable = true },
        new SearchableField("hotelName") { IsSortable = true },
        new SearchableField("description") { AnalyzerName = LexicalAnalyzerName.EnLucene },
        new SimpleField("rating", SearchFieldDataType.Double) { IsFilterable = true, IsSortable = true },
        new SearchField("descriptionVector", SearchFieldDataType.Collection(SearchFieldDataType.Single))
        {
            VectorSearchDimensions = 1536,
            VectorSearchProfileName = "vector-profile"
        }
    }
};
```

## 文档操作

```csharp
var searchClient = new SearchClient(endpoint, indexName, credential);

// 上传（新增）
var hotels = new[] { new Hotel { HotelId = "1", HotelName = "Hotel A" } };
await searchClient.UploadDocumentsAsync(hotels);

// 合并（更新已有）
await searchClient.MergeDocumentsAsync(hotels);

// 合并或上传（upsert）
await searchClient.MergeOrUploadDocumentsAsync(hotels);

// 删除
await searchClient.DeleteDocumentsAsync("hotelId", new[] { "1", "2" });

// 批量操作
var batch = IndexDocumentsBatch.Create(
    IndexDocumentsAction.Upload(hotel1),
    IndexDocumentsAction.Merge(hotel2),
    IndexDocumentsAction.Delete(hotel3));
await searchClient.IndexDocumentsAsync(batch);
```

## 搜索模式

### 基本搜索

```csharp
var options = new SearchOptions
{
    Filter = "rating ge 4",
    OrderBy = { "rating desc" },
    Select = { "hotelId", "hotelName", "rating" },
    Size = 10,
    Skip = 0,
    IncludeTotalCount = true
};

SearchResults<Hotel> results = await searchClient.SearchAsync<Hotel>("luxury", options);

Console.WriteLine($"Total: {results.TotalCount}");
await foreach (SearchResult<Hotel> result in results.GetResultsAsync())
{
    Console.WriteLine($"{result.Document.HotelName} (Score: {result.Score})");
}
```

### 分面搜索

```csharp
var options = new SearchOptions
{
    Facets = { "rating,count:5", "category" }
};

var results = await searchClient.SearchAsync<Hotel>("*", options);

foreach (var facet in results.Value.Facets["rating"])
{
    Console.WriteLine($"Rating {facet.Value}: {facet.Count}");
}
```

### 自动补全和建议

```csharp
// 自动补全
var autocompleteOptions = new AutocompleteOptions { Mode = AutocompleteMode.OneTermWithContext };
var autocomplete = await searchClient.AutocompleteAsync("lux", "suggester-name", autocompleteOptions);

// 建议
var suggestOptions = new SuggestOptions { UseFuzzyMatching = true };
var suggestions = await searchClient.SuggestAsync<Hotel>("lux", "suggester-name", suggestOptions);
```

## 向量搜索

详细模式请参见 references/vector-search.md。

```csharp
using Azure.Search.Documents.Models;

// 纯向量搜索
var vectorQuery = new VectorizedQuery(embedding)
{
    KNearestNeighborsCount = 5,
    Fields = { "descriptionVector" }
};

var options = new SearchOptions
{
    VectorSearch = new VectorSearchOptions
    {
        Queries = { vectorQuery }
    }
};

var results = await searchClient.SearchAsync<Hotel>(null, options);
```

## 语义搜索

详细模式请参见 references/semantic-search.md。

```csharp
var options = new SearchOptions
{
    QueryType = SearchQueryType.Semantic,
    SemanticSearch = new SemanticSearchOptions
    {
        SemanticConfigurationName = "my-semantic-config",
        QueryCaption = new QueryCaption(QueryCaptionType.Extractive),
        QueryAnswer = new QueryAnswer(QueryAnswerType.Extractive)
    }
};

var results = await searchClient.SearchAsync<Hotel>("best hotel for families", options);

// 访问语义答案
foreach (var answer in results.Value.SemanticSearch.Answers)
{
    Console.WriteLine($"Answer: {answer.Text} (Score: {answer.Score})");
}

// 访问标题
await foreach (var result in results.Value.GetResultsAsync())
{
    var caption = result.SemanticSearch?.Captions?.FirstOrDefault();
    Console.WriteLine($"Caption: {caption?.Text}");
}
```

## 混合搜索（向量 + 关键词 + 语义）

```csharp
var vectorQuery = new VectorizedQuery(embedding)
{
    KNearestNeighborsCount = 5,
    Fields = { "descriptionVector" }
};

var options = new SearchOptions
{
    QueryType = SearchQueryType.Semantic,
    SemanticSearch = new SemanticSearchOptions
    {
        SemanticConfigurationName = "my-semantic-config"
    },
    VectorSearch = new VectorSearchOptions
    {
        Queries = { vectorQuery }
    }
};

// 结合关键词搜索、向量搜索和语义排序
var results = await searchClient.SearchAsync<Hotel>("luxury beachfront", options);
```

## 字段特性参考

| 特性 | 用途 |
|------|------|
| `SimpleField` | 不可搜索字段（筛选、排序、分面） |
| `SearchableField` | 全文可搜索字段 |
| `VectorSearchField` | 向量嵌入字段 |
| `IsKey = true` | 文档键（必需，每个索引一个） |
| `IsFilterable = true` | 启用 $filter 表达式 |
| `IsSortable = true` | 启用 $orderby |
| `IsFacetable = true` | 启用分面导航 |
| `IsHidden = true` | 从结果中排除 |
| `AnalyzerName` | 指定文本分析器 |

## 错误处理

```csharp
using Azure;

try
{
    var results = await searchClient.SearchAsync<Hotel>("query");
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Index not found");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Search error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## 最佳实践

1. **生产环境使用 `DefaultAzureCredential`** 而非 API 密钥
2. **使用 `FieldBuilder`** 配合模型特性实现类型安全的索引定义
3. **使用 `CreateOrUpdateIndexAsync`** 实现幂等的索引创建
4. **批量执行文档操作** 以提升吞吐量
5. **使用 `Select`** 仅返回所需字段
6. **配置语义搜索** 用于自然语言查询
7. **组合向量 + 关键词 + 语义** 以获得最佳相关性

## 参考文件

| 文件 | 内容 |
|------|------|
| references/vector-search.md | 向量搜索、混合搜索、向量化器 |
| references/semantic-search.md | 语义排序、标题、答案 |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
