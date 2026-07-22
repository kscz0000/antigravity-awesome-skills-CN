---
name: options-flow-analyzer
description: 期权P/C比率分析中的真实/彩票看涨分离 — 防止深度虚值噪音导致信号反转。触发词：期权流分析、P/C比率、看涨看跌比、彩票看涨、真实看涨、期权情绪分析、options flow、put/call ratio
category: finance
risk: safe
source: community
source_type: community
date_added: "2026-05-13"
author: tellmefrankie
tags: [options, sentiment-analysis, trading, polygon, market-analysis]
tools: [websearch]
---
# 期权流分析器

分析期权链数据，核心在于区分真实看涨与彩票看涨 — 这一关键洞察能防止 P/C 比率被误读。使用 Polygon.io API。

## 何时使用

- 当原始看跌/看涨比率看似看涨或看跌，但可能被廉价的深度虚值合约扭曲时使用。
- 当需要跨观察列表、持仓、行业或事件驱动标的比较期权流时使用。
- 当需要区分机构对冲与投机性彩票注活动时使用。
- 当需要追踪相对近期基线的期权异常时使用。

## 它做什么

标准 P/C 比率分析具有误导性。P/C 为 0.35 看起来"极度看涨"，但实际可能 84% 是彩票看涨（$0.01-$0.09 的虚值期权）。

本技能区分：
- **真实看涨**：行权价在股价 5% 以内，权利金有意义
- **彩票看涨**：深度虚值，权利金低廉，投机性押注
- **真实看跌**：实际对冲活动
- **彩票看跌**：廉价的下行押注

## 分析输出

针对每个标的：
- 真实 P/C 比率（排除彩票噪音）
- 彩票占比（成交量中投机比例）
- 按到期日分解（周度 vs 月度 vs LEAPS）
- 异常检测：P/C 偏移 >0.3，看涨未平仓量激增 >30%，IV 飙升 >20%
- 情绪分类：看涨/看跌/中性，附置信度

## 示例输出

```
Options Flow Summary — 2026-05-13

HOLDINGS:
CEG  $299.69 | Raw P/C: 1.06 | Lottery: 61% | Adj P/C: 2.72  BEARISH (was neutral raw)
IREN $55.15  | Raw P/C: 0.83 | Lottery: 34% | Adj P/C: 0.55  BULLISH
KTOS $56.99  | Raw P/C: 0.53 | Lottery: 28% | Adj P/C: 0.38  EXTREME BULLISH
RXRX $3.26   | Raw P/C: 0.38 | Lottery: 84% | Adj P/C: 2.37  BEARISH (was extreme bullish raw)

SECTORS:
XLI  | Raw P/C: 5.32 | Lottery:  8% | Adj P/C: 4.89  INSTITUTIONAL HEDGE

ANOMALIES:
XLI: P/C 5.32 vs 30-day baseline 0.87 — 4.5 std deviations above normal
RXRX: 84% lottery calls — raw P/C signal completely inverted after filtering
```

## 配置

```
Analyze options flow for my watchlist:
Holdings: CEG, IREN, KTOS, RXRX, TEM
Sectors: SPY, QQQ, XLI, XLK
Separate real vs lottery calls (threshold: premium < $0.10, delta < 0.05).
Flag anomalies vs 30-day baseline.
```

## 前置条件

- Polygon.io API 密钥（免费版覆盖基础数据；付费版可获取完整链数据）
- WebSearch 用于交叉验证

## 局限性

- 期权数据可能存在延迟、不完整或不可用，具体取决于 Polygon.io 套餐。
- 权利金和 delta 阈值等启发式参数需根据标的股价、波动率和到期日进行调整。
- 情绪分类为分析信号，不构成财务建议或交易推荐。
- 务必将异常流与价格走势、新闻催化剂、流动性和风控措施交叉验证。

## 关键发现

这一真实/彩票分离方法是在实盘组合管理中发现的：RXRX 的 P/C 为 0.35（看起来极度看涨），但实际 84% 是 $0.01-$0.09 的彩票看涨。"看涨信号"其实是噪音。本技能防止犯同样的错误。

## 定价

免费版：3 个标的的基础 P/C 比率
**完整版 — $29 一次性付费**：真实/彩票分离 + 异常检测 + 按到期日分解 + 无限标的
→ https://jaehyunpark.gumroad.com/l/tcyahy

## 作者

源自一次付出真金白银的实盘交易失误。真实/彩票发现已记录并经过 17 个标的、2 个月以上的实战验证。
