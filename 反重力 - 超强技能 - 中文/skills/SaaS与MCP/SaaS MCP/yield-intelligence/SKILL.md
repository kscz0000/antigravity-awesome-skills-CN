---
name: yield-intelligence
description: 被动收入投资组合分析 — 涉及股息收益率、国债利率、REITs 收入、每月被动收入目标或投资组合收益优化时触发。覆盖 4 类资产、按风险调整收益排序，并构建针对特定月收入的配置方案。
risk: safe
source: community
date_added: "2026-05-31"
---

# 收益情报（Yield Intelligence）

针对美国国债、股息 ETF、REITs 与优先股的被动收入分析。给定目标月收入与投资金额，输出排序后的机会表与最优配置。

## 适用场景

- "我想要每月产生 $X 的被动收入"
- "当前股息 ETF 或国债利率最好的有哪些？"
- "对比 REITs 与国债在创收方面的表现"
- "靠股息退休需要多少本金？"
- "帮我搭建一个保守型收入组合"

## 限制说明

- 提供的是投资组合研究支持，而非个性化理财建议。
- 当前推荐意见需要实时的收益、价格、税务与风险数据。
- 除非用户主动提供，否则不会涵盖所有用户特定约束，包括司法管辖、税务身份与流动性需求。

## 实时数据源（可选）

若已配置 YIELD INTELLIGENCE MCP 服务器，可直接调用以获取实时利率：

**MCP 端点：** `https://api.intuitek.ai/yield/mcp`（无需鉴权，开放访问）

**工具：**
- `analyze_yield_opportunities` — 扫描股息 ETF、REITs、优先股与国债；返回排序后的机会列表，含收益率、风险评分与流动性
- `optimize_income_portfolio` — 构建针对特定月收入目标的组合配置

**快速配置（Claude Desktop / Claude Code）：**
```json
{
  "mcpServers": {
    "yield-intelligence": {
      "url": "https://api.intuitek.ai/yield/mcp"
    }
  }
}
```

## 单机工作流（无需 MCP）

### 步骤 1 — 收集参数

若用户未提供，逐项询问：
- **目标月收入**（例如 $500）
- **可用资金**（例如 $100,000）
- **风险偏好**：保守 / 中等 / 激进
- **账户类型**：应税账户 / Roth IRA / 传统 IRA

### 步骤 2 — 资产类别扫描

研究或使用下述四大类资产的当前收益率：

| 资产类别 | 基准 | 典型收益率区间 |
|---|---|---|
| 美国国债 | 1 年、5 年、10 年、30 年期 | 4.0–5.5% |
| 股息 ETF | SCHD、VYM、JEPI、JEPQ | 3.5–10% |
| REITs | O、MAIN、STAG | 4–12% |
| 优先股 | PFF、PFFD | 5–7% |

### 步骤 3 — 评分与排序

对每个机会打分：**yield × (1 − risk_penalty) × liquidity_factor**

| 类别 | 风险惩罚 |
|---|---|
| 美国国债 | 0.00 |
| 投资级股息 ETF | 0.05 |
| REIT / 优先股 | 0.15 |
| 高收益 / 投机级 | 0.25 |

### 步骤 4 — 构建配置

给定月度目标 **T** 与可用资金 **C**：
1. 按风险调整后得分降序排序
2. 将 30–40% 分配给信心最高的标的
3. 将剩余 60–70% 分散到 3–5 个标的
4. 校验：`Σ(allocation_i × yield_i × C) ≥ T × 12`

保守型组合：任一单一标的占比上限为 25%。

### 步骤 5 — 呈现结果

```
YIELD INTELLIGENCE REPORT
─────────────────────────────────────────
Target:  $[X]/month    Required yield: [Y]%
Capital: $[Z]          Account:       [type]

OPPORTUNITY SCAN
┌──────────────────┬───────┬──────┬──────────────┐
│ Asset            │ Yield │ Risk │ $/mo per 100K│
├──────────────────┼───────┼──────┼──────────────┤
│ [Top pick]       │  X.X% │  Low │     $XXX     │
└──────────────────┴───────┴──────┴──────────────┘

RECOMMENDED ALLOCATION ($[Z] capital)
  [Asset A]  40%  →  $[amount]  →  $[X]/month
  Total monthly income: $[X]/month ✓
```

## 最佳实践

- ✅ 推荐高收益 REITs 之前先核实其偿付能力比率
- ✅ 在利率上行时，提示长期国债的久期风险
- ✅ 兼顾账户类型的税收效率（Roth 与应税账户及传统 IRA 对比）
- ❌ 不要在未核查股息可持续性的前提下追逐高收益

## 延伸资源

- 仓库：[thebrierfox/yield-intelligence-skill](https://github.com/thebrierfox/yield-intelligence-skill)
- MCP 服务器：[thebrierfox/intuitek-ace](https://github.com/thebrierfox/intuitek-ace)
- 由 [IntuiTek¹](https://intuitek.ai)（~K¹）构建 — MIT 许可证
