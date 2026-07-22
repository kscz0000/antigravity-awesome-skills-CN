---
name: longbridge
description: "长桥证券 125+ 智能体技能 — 实时行情、K线图、基本面、持仓分析、期权及更多，覆盖港股/美股/A股/新加坡市场。三语支持：简体中文、繁体中文、英文。触发词：长桥、股票行情、港股、美股、持仓分析、期权分析、K线图、基本面、板块筛选"
category: finance
risk: critical
source: official
source_repo: longbridge/skills
source_type: official
date_added: "2026-05-29"
author: longbridge
tags: [finance, stocks, trading, portfolio, market-data]
tools: [claude, cursor, gemini, codex]
license: "MIT"
license_source: "https://github.com/longbridge/skills/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# 长桥证券

## 概述

Longbridge 是长桥证券官方技能集合，涵盖 125+ 智能体技能，包括实时行情、K线分析、公司基本面、持仓管理、期权、板块筛选等。支持港股、美股、A股（沪/深）和新加坡市场。所有技能均支持三语（简体中文/繁体中文/英文）。

源码仓库：[github.com/longbridge/skills](https://github.com/longbridge/skills)（约 840 星标，MIT 协议）

## 何时使用

- 查询港股/美股/A股/新加坡市场的股票价格、K线或行情数据时
- 需要公司基本面、财报或分析师评级时
- 通过长桥查看持仓、仓位或账户盈亏时
- 需要期权分析、板块排名、资金流向或新闻时
- 用中文（简体或繁体）或英文咨询任何证券相关话题时

## 工作原理

### 第 1 步：发现正确的子命令

```bash
longbridge --help
```

列出所有可用的子命令。切勿硬编码子命令名称 — CLI 会持续更新。

### 第 2 步：查看子命令选项

```bash
longbridge <subcommand> --help
```

调用前确认参数和输出格式。

### 第 3 步：以 JSON 格式调用

```bash
longbridge <subcommand> --format json
```

解析结构化输出，以用户使用的语言呈现（根据输入自动检测）。

## 认证

```bash
longbridge auth login          # Basic market data (read-only)
longbridge auth login --trade  # Portfolio and account features
```

## 安装

```bash
# Claude Code plugin marketplace
/plugin marketplace add longbridge/skills

# Or via npx
npx skills add https://github.com/longbridge/skills
```

## MCP 回退

如果未安装 `longbridge` CLI 二进制文件，则回退到 MCP 工具。运行时检查可用的 MCP 工具 — 不要硬编码 MCP 工具名称，因为它们会随服务器版本变化。

## 限制

- 持仓和账户功能需登录 Trade 权限。
- 实时数据受长桥数据订阅限制（未订阅可使用延迟数据）。
- 加密货币代码在长桥平台使用 `.HAS` 后缀。
- 本技能不下单 — 默认只读，除非使用账户写入权限。

## 安全注意事项

- 所有行情查询均为只读（无副作用）。
- 自选股变更和订单相关功能遵循预览+确认两步协议。
- 凭证由 Longbridge 认证系统处理；本技能不存储或传输 token。
