# 示例数据

为没有自带数据，或希望快速看到示例效果的 Weaviate 用户，向其 collection 添加示例数据。从 huggingface hub 下载数据。

```bash
uv run scripts/example_data.py --domain "DOMAIN_NAME" [--vectorizer "..."] [--nrows X]
```

## 参数

| 参数 | 标志 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `--domain` | `-d` | 否 | `academic` | 指定使用的数据集。可选值：'academic'、'finance'、'ecommerce'、'medical' 或 'customer_support'。 |
| `--vectorizer` | `-v` | 否 | `text2vec_weaviate` | 可选的 vectorizer（例如 `text2vec_openai`、`text2vec_cohere`、`none`） |
| `--nrows` | `-n` | 否 | `None` | 可选地取数据子集；不提供则使用完整数据集。 |

**使用场景**：在没有任何数据可用，或用户请求一些玩具数据时，创建示例数据以便立即使用其他技能。

**领域数据集：**
- `academic` 对应 `jamescalam/ai-arxiv2` 数据集，包含从 Arxiv 上选取的、围绕 AI/ML 主题的论文 chunk。在 Weaviate 实例中创建 `AI_Arxiv` collection。
- `finance` 对应 `AgamiAI/Indian-Income-Tax-Returns` 数据集，全合成的印度所得税申报表。在 Weaviate 实例中创建 `Income_Tax_Returns` collection。
- `ecommerce` 对应 `pkghf/ecom-product-catalog` 数据集，包含结构化的电商产品信息（产品详情、定价、分类等）。在 Weaviate 实例中创建 `Product_Catalog` collection。
- `medical` 对应 `Amod/hair_medical_sit`，包含常见毛发相关疾病的信息。在 Weaviate 实例中创建 `Hair_Medical` collection。
- `customer_support` 对应 `Console-AI/IT-helpdesk-synthetic-tickets`，IT 领域的合成客户支持工单。在 Weaviate 实例中创建 `IT_Support_Tickets` collection。
