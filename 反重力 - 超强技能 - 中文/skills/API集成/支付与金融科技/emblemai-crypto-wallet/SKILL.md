---
name: emblemai-crypto-wallet
description: "通过 EmblemAI Agent Hustle API 管理 7 条区块链的加密钱包。支持 Solana、Ethereum、Base、BSC、Polygon、Hedera 和 Bitcoin 的余额查询、代币兑换、投资组合分析和交易执行。"
risk: critical
source: "EmblemCompany/Agent-skills (MIT)"
date_added: "2026-03-06"
---

# EmblemAI 加密钱包

你通过 EmblemAI Agent Hustle API 管理加密钱包。可以在 7 条支持的链上查询余额、兑换代币、查看投资组合以及执行区块链交易。

## 使用场景
- 用户想要查询加密钱包余额
- 用户想要兑换或交易代币
- 用户想要投资组合分析或代币研究
- 用户想要与 DeFi 协议交互
- 用户需要跨链钱包操作

## 安装

安装包含参考资料和脚本的完整技能：

```bash
npx skills add EmblemCompany/Agent-skills --skill emblem-ai-agent-wallet
```

或直接安装 npm 包：

```bash
npm install @emblemvault/agentwallet
```

## 支持的链

| 链 | 操作 |
|-------|-----------|
| Solana | 余额、兑换、转账、代币查询 |
| Ethereum | 余额、兑换、转账、NFT |
| Base | 余额、兑换、转账 |
| BSC | 余额、兑换、转账 |
| Polygon | 余额、兑换、转账 |
| Hedera | 余额、转账 |
| Bitcoin | 余额、转账 |

## API 集成

基础 URL：`https://api.agenthustle.ai`

认证需要在请求头中传递 `x-api-key`。

### 核心端点

- `GET /balance/{chain}/{address}` — 查询钱包余额
- `POST /swap` — 执行代币兑换
- `GET /portfolio/{address}` — 投资组合概览
- `GET /token/{chain}/{contract}` — 代币信息
- `POST /transfer` — 发送代币

## 关键行为

1. **执行前确认** — 在执行交易前向用户展示将要发生的操作
2. **先查余额** — 在尝试兑换或转账前先检查余额
3. **验证代币合约** — 交易未知代币前使用 rugcheck 或类似工具验证
4. **报告 Gas 估算** — 在可用时报告 Gas 费用估算
5. **永不暴露私钥** — 所有签名通过保险库在服务端完成

## 链接

- [完整技能及参考资料](https://github.com/EmblemCompany/Agent-skills/tree/main/skills/emblem-ai-agent-wallet)
- [npm 包](https://www.npmjs.com/package/@emblemvault/agentwallet)
- [EmblemAI](https://agenthustle.ai)

## 限制
- 仅在任务明确符合上述范围时使用此技能。
- 输出内容不应替代特定环境的验证、测试或专家评审。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
