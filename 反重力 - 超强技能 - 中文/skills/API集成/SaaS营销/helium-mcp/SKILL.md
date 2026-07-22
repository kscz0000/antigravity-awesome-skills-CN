---
name: helium-mcp
description: "连接 Helium MCP 服务器进行新闻研究、媒体偏见分析、平衡观点、股票/期权数据和语义表情包搜索，覆盖 320 万+ 文章和 5000+ 来源。触发词：Helium MCP、新闻研究、媒体偏见、股票数据、期权定价、表情包搜索、balanced news、media bias analysis、stock data、options pricing、meme search"
risk: safe
source: "https://heliumtrades.com/mcp-page/"
source_repo: connerlambden/helium-mcp
source_type: community
date_added: "2026-04-13"
author: connerlambden
tags: [mcp, news, media-bias, stocks, options, finance, research]
tools: [claude, cursor, gemini]
---

# Helium MCP

## 概述

Helium MCP 通过模型上下文协议（Model Context Protocol）暴露的 9 个工具，为 AI 编程助手提供新闻情报、媒体偏见分析、金融市场数据和表情包搜索功能。它覆盖来自 5000+ 新闻源的 320 万+ 文章，包含 15+ 偏见维度、带有 AI 生成分析的实时股票/ETF/加密货币数据，以及 ML 预测的期权定价。

## 何时使用此技能

- 需要在带有偏见感知上下文的情况下搜索或分析新闻文章时使用
- 研究特定来源或文章 URL 的媒体偏见时使用
- 想要获取关于某个主题的平衡左/右/中派观点时使用
- 查询带有 AI 多空分析的实时股票、ETF 或加密货币数据时使用
- 定价期权或评估交易策略时使用
- 通过语义含义搜索表情包时使用

## MCP 配置

将 Helium MCP 服务器添加到你的客户端配置中。该端点使用可流式 HTTP，无需身份验证。

### Claude Desktop / Cursor / Windsurf

```json
{
  "mcpServers": {
    "helium": {
      "url": "https://heliumtrades.com/mcp"
    }
  }
}
```

无需 API 密钥或身份验证。

## 可用工具

### 新闻与媒体偏见

#### `search_news`
搜索来自 5000+ 来源的 320 万+ 文章，包含 15+ 偏见维度。可按主题、来源、日期范围和偏见属性过滤。

```
search_news({ query: "artificial intelligence regulation" })
```

#### `search_balanced_news`
获取 AI 合成的平衡文章，呈现关于任何主题的左派、右派和中派观点。

```
search_balanced_news({ query: "immigration policy" })
```

#### `get_source_bias`
检索任何新闻来源的详细偏见档案，包括政治倾向、事实报道评分和 15+ 偏见维度。

```
get_source_bias({ source: "reuters" })
```

#### `get_all_source_biases`
在单次调用中获取所有 5000+ 追踪新闻来源的偏见数据。

```
get_all_source_biases()
```

#### `get_bias_from_url`
对特定文章 URL 运行完整的偏见分析，返回来源偏见档案和文章级偏见指标。

```
get_bias_from_url({ url: "https://example.com/article" })
```

### 金融与市场

#### `get_ticker`
获取实时股票、ETF 或加密货币数据，包括价格、成交量、AI 生成的多空案例和预测。

```
get_ticker({ ticker: "AAPL" })
```

#### `get_option_price`
获取特定期权合约的 ML 预测公允价值和最终价内到期的概率。

```
get_option_price({ ticker: "AAPL", strike: 200, expiration: "2026-06-19", type: "call" })
```

#### `get_top_trading_strategies`
获取某个股票代码的顶级期权策略及风险/回报分析。

```
get_top_trading_strategies({ ticker: "TSLA" })
```

### 表情包

#### `search_memes`
语义表情包搜索——通过含义而非精确关键词查找表情包。

```
search_memes({ query: "debugging at 3am" })
```

## 示例

### 示例 1：平衡新闻研究

向你的 AI 助手提问：

> "搜索关于气候政策的平衡新闻报道，展示左派、右派和中派来源如何不同地构建这个问题。"

助手将调用 `search_balanced_news` 并呈现来自政治光谱各方的综合观点。

### 示例 2：来源可信度检查

> "纽约时报的媒体偏见档案是什么？"

助手将调用 `get_source_bias` 并返回完整的偏见细分，包括政治倾向、事实报道和其他维度。

### 示例 3：带期权的股票研究

> "给我 NVDA 的多空案例，然后找出最佳期权策略。"

助手将调用 `get_ticker` 获取市场数据和 AI 分析，然后调用 `get_top_trading_strategies` 获取排名的策略推荐。

### 示例 4：文章偏见分析

> "分析这篇文章的偏见：https://example.com/politics/story"

助手将调用 `get_bias_from_url` 返回来源级和文章级的偏见指标。

## 最佳实践

- **先宽后窄：** 使用 `search_news` 进行发现，然后使用 `get_bias_from_url` 对特定文章进行深度分析
- **交叉参考观点：** 结合 `search_balanced_news` 和 `get_source_bias` 来理解为什么不同来源以不同方式构建主题
- **配对市场工具：** 使用 `get_ticker` 获取基本面观点，然后使用 `get_option_price` 或 `get_top_trading_strategies` 获取可执行的交易
- **无需认证：** 该端点无需 API 密钥或设置即可立即使用，只需添加 MCP 配置

## 常见问题

- **问题：** 对于非常小众的查询，工具调用返回空结果
  **解决方案：** 扩大搜索词范围——Helium 索引主流和中层级来源，因此超本地化主题可能覆盖有限

- **问题：** 某个股票代码的期权数据不可用
  **解决方案：** 验证该股票代码有上市期权——一些小盘股和大多数加密资产没有期权市场

## 相关技能

- `@mcp-builder` - 如果你想构建自己的 MCP 服务器而不是使用此服务器

## 其他资源

- [Helium MCP Page](https://heliumtrades.com/mcp-page/)
- [GitHub Repository](https://github.com/connerlambden/helium-mcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## 限制
- 仅当任务明显符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
