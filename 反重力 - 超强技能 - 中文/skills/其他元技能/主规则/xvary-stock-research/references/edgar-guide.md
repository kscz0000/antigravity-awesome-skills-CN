# EDGAR 在 Claude Code 中的使用指南

本指南说明本技能如何使用 `tools/edgar.py` 读取 SEC 数据。

## 使用的端点

- CIK 查询：`https://www.sec.gov/files/company_tickers.json`
- 公司事实（XBRL）：`https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`
- 申报文件元信息：`https://data.sec.gov/submissions/CIK{cik}.json`

## 支持的申报文件类型

- `10-K`
- `10-Q`
- `20-F`
- `6-K`

## 公共函数

- `get_cik(ticker)`
- `get_company_facts(ticker)`
- `get_financials(ticker)`
- `get_filings_metadata(ticker)`

## 数据规范化模式

- 股票代码统一为大写。
- 在 CIK 查询阶段，兼容 `.` 与 `-` 形式的变体。
- 同时解析 `us-gaap` 与 `ifrs-full` 概念命名空间。
- 在可能的情况下，将 IFRS 术语映射到公共输出字段名。
- 年度与季度快照分开保存。
- `shares_outstanding` 只能从期末股本概念中获取；如不可得，应保留为 null，而不是用加权平均 EPS 的分母代替。

## CLI 示例

```bash
python3 tools/edgar.py AAPL
python3 tools/edgar.py NVDA --mode filings
python3 tools/edgar.py ASML --mode facts
```

## 实用说明

- SEC 请求应附带合理的 `User-Agent`。
- SEC 端点会对突发性请求进行限流；应避免高频循环调用。
- 国际股票代码的 EDGAR 覆盖度可能较为稀疏。
- 在分析中展示数值时，应同时关联到对应的申报文件元信息。

## 错误处理原则

- 在股票代码/CIK 解析失败时直接大声报错。
- 在部分概念不可用时返回部分数据集。
- 永远不要凭空捏造缺失值。
