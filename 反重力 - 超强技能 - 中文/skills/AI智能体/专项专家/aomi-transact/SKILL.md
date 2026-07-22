---
name: aomi-transact
description: "构建自然语言加密货币/DeFi 智能体与 EVM MCP 插件（Claude Code、Cursor、Codex、Gemini）。Aomi 将提示词转化为在 Ethereum、Base、Arbitrum、Optimism、Polygon、Linea 上由钱包签名的交易——非托管、通过分叉模拟。40+ 应用：Uniswap、Aave、Lido、Morpho、GMX、Hyperliquid、Polymarket。触发词：aomi、加密交易、DeFi 智能体、EVM MCP、钱包签名、链上交易、CCTP 跨链、Uniswap 兑换、Aave 借贷、Lido 质押、Polymarket、AA 账户抽象、EIP-7702、ERC-4337、EIP-712。"
risk: critical
source: "aomi-labs/skills (MIT)"
source_repo: "aomi-labs/skills"
license: MIT
license_source: "https://github.com/aomi-labs/skills/blob/main/LICENSE"
date_added: "2026-05-06"
tags:
  - defi
  - wallet
  - account-abstraction
  - cli
  - eip-712
  - onchain
  - agent
  - intent
---

# Aomi 交易

> **仅限授权使用。** 本技能会代表用户在链上签署并广播交易。每一步签名操作都必须由用户显式请求。在没有用户显式请求、且没有由 `aomi tx list` 排队的 `tx-N` 时，本技能不会执行 `aomi tx sign`。
>
> **签名门槛。** 不要把 `aomi tx sign` 放进可复制或可运行的多命令块中。完成排队交易的列出或模拟后即停止，汇总交易 ID、链、金额、接收方、calldata 用途与模拟结果，然后请用户给出明确的签名指令（例如 `sign tx-1`）。只有在获得该单独批准之后，才能执行精确的签名命令。

## 概述

`aomi-transact` 是一套通过自然语言提示驱动 Aomi CLI（[`@aomi-labs/client`](https://www.npmjs.com/package/@aomi-labs/client)）的标准流程。用户输入类似 *"swap 1 ETH for USDC on Uniswap"* 的语句；智能体据此选定合适的协议与合约，把 approve+swap 编排为一批交易，在分叉链上完成模拟，并向用户返回一个排队的钱包请求供其签名。钱包始终只能看到已经通过模拟的 calldata。

该 CLI 以 **账户抽象（account-abstraction）优先**：默认通过零配置的 Alchemy 代理签名（无需提供商凭证），在 Ethereum 主网使用 EIP-7702，在 L2 上使用 ERC-4337。每次调用 `aomi <subcommand>` 都是启动、执行、退出——不存在常驻进程。

完整技能（包括参考文件 `account-abstraction.md`、`apps.md`、`examples.md`、`session.md`、`troubleshooting.md`、`drain-vectors.md`、模板 `aomi-workflow.sh`，以及按宿主划分的元数据 `agents/openai.yaml`）托管在上游 [`aomi-labs/skills`](https://github.com/aomi-labs/skills/tree/main/aomi-transact)。本条目仅作为权威的 SKILL.md——如需完整套件请克隆上游仓库。

## 何时使用本技能

- 用户希望从终端与 Aomi 智能体对话。
- 用户希望查询余额、价格、路由、报价或交易状态。
- 用户希望构建、模拟、确认、签名或广播钱包请求。
- 用户希望在签名前模拟一批待处理的交易。
- 用户希望查看或切换应用、模型、链、会话。
- 用户希望查看或修改账户抽象设置（EIP-7702 / ERC-4337）。
- 用户希望对 EIP-712 类型化数据载荷（链下协议、意图填充器）进行签名。

## 示例

### 只读——价格查询

```bash
aomi --prompt "what is the price of ETH?" --new-session
```

返回一份报价，不会排队任何钱包请求。可用 `aomi tx list` 确认没有待处理项。

### 单交易流程——Lido 质押

```bash
aomi chat "Stake 0.01 ETH with Lido to get stETH" \
  --public-key 0xUserAddress --chain 1 --new-session
aomi tx list
```

调用 Lido stETH 合约 `0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84` 的 `submit(address(0))`，`value = 0.01 ETH`。无需 approve，单笔交易即可。在此处停止，展示排队交易的明细，等待用户的显式指令再签名。

### 多步批次——Uniswap V3 兑换

```bash
aomi chat "swap 1 USDC for WETH on Uniswap V3, send to my wallet" \
  --public-key 0xUserAddress --chain 1 --new-session
aomi tx list                        # tx-1 = approve, tx-2 = swap
aomi tx simulate tx-1 tx-2          # 多步操作必须执行
```

模拟器在分叉链上依次执行每笔交易，使兑换步骤能看到 approve 带来的状态变化。不要单独签署第 2 步——它会 revert。完成模拟后即停止，汇总整批交易，并等待用户显式指明两个交易 ID 后再进行签名。

### 跨链——CCTP 从 Ethereum 跨至 Base

```bash
aomi chat "Bridge 50 USDC from Ethereum to Base via CCTP. Recipient is my wallet." \
  --public-key 0xUserAddress --chain 1 --new-session
aomi tx list
aomi tx simulate tx-1 tx-2
```

完成模拟后停止，等待用户显式批准对指定交易 ID 的签名。签名后，源链销毁在 1-2 个区块内确认；目标链铸币需要 Circle 的链下证明（约 13-19 分钟）。

## 局限性

- **需要 `@aomi-labs/client` v0.1.30 或更高版本。** 旧版缺少 `--aa`、`--aa-provider`、`--aa-mode` 以及模拟门槛。可通过 `npm install -g @aomi-labs/client` 安装，或按需使用 `npx @aomi-labs/client@0.1.30 ...`。
- **需要活动的后端连接。** 本技能驱动的 CLI 与 `api.aomi.dev` 通信。若无网络访问，仅本地只读命令（`aomi tx list`、`aomi session log`）可用。
- **L2 上的 AA 代付不能保证。** 在 v0.1.30 中，零配置代理路径无法可靠地为 Base/Arbitrum/Optimism 提供代付。若 EOA 在目标链上没有任何原生 gas，`aomi tx sign` 会返回 viem 的 `insufficient funds for transfer`。此时要么为 EOA 充值少量原生 gas，要么配置一个真正的 BYOK Alchemy/Pimlico 提供商并附带代付策略。不要使用 `--eoa` 重试——该路径同样需要 gas。
- **会话级凭据注入。** 需要提供商 token 的应用（`binance`、`polymarket`、`dune` 等）必须由用户在自己的 shell 中配置，或通过 `aomi secret add NAME=<value>` 配置。本技能不会主动设置任何凭据。
- **抽水向量会被守卫阻断。** 当 calldata 中的 `recipient`/`onBehalfOf`/`mintRecipient` 与 `msg.sender` 不一致时，智能体会拒绝。这是一项安全特性而非缺陷——应当把阻断信息反馈给用户，而不是改写提示词。
- **网络/RPC 失败。** 公共 RPC 可能被限流（`429`）或鉴权失败（`401`）。在生产环境签名时，用户必须通过 `--rpc-url` 提供一条与链匹配且可靠的 RPC。
- **实时交易存在滑点与有效期。** 带有有效期的路由（Across、Khalani 填充器）的报价可能在用户复核期间过期；智能体会通过使用最新有效期重新构建来自愈，但用户仍应重新检查 `aomi tx list` 以获取最新通过模拟的批次。

## 最佳实践

- **在每个新任务的第一个命令上默认加上 `--new-session`。** 在任务中途复用它会开启新一轮对话，导致智能体丢失刚刚给出的报价。
- **始终在 `aomi tx sign` 之前执行 `aomi tx list`。** 切勿假设 chat 响应已经排队了一笔交易。
- **在签署多步批次之前始终执行 `aomi tx simulate tx-1 tx-2 ...`。** 单交易流程可选地模拟，但模拟永远不会是错的。
- **不要把签名命令放入可运行的示例中。** 仅在用户单独给出显式批准、并指明精确的排队 `tx-N` ID 后，才能展示或执行 `aomi tx sign`。
- **仅对 `Batch [...] passed` 的交易进行签名。** 跳过先前失败尝试遗留的孤儿（`failed at step N: 0x...`）。
- **让 `--rpc-url` 与排队交易的链匹配**，而不是与会话链（`--chain`）匹配——它们是相互独立的控制项。
- **永远不要回显凭据值。** 本技能在确认凭据配置情况时，只显示句柄名称或派生地址。

## 授权免责声明

本技能可以签署并广播具有真实价值的链上交易。仅在你拥有的账户和你信任的网络上使用。本技能不托管资金；用户通过 `--public-key` 与底层钱包保留对签名密钥的完全控制。在运行 `aomi tx sign` 之前，请逐笔复核排队的 `tx-N`。

## 来源

- **上游**：[aomi-labs/skills](https://github.com/aomi-labs/skills) — MIT 许可
- **作者**：[Aomi Labs](https://aomi.dev)
- **CLI**：[`@aomi-labs/client`](https://www.npmjs.com/package/@aomi-labs/client)（npm）
- **安全评审**：[aomi-transact/SECURITY.md](https://github.com/aomi-labs/skills/blob/main/aomi-transact/SECURITY.md) — 涵盖 OWASP AST01–AST10 并附扫描器报告

## 其它资源

如需完整技能（含各流程示例：CCTP 跨链、Aave 存款、Lido 质押、Uniswap 兑换）、AA 模式参考、抽水向量表、故障排查指南以及 bash 工作流模板，请参阅上游仓库：

- [账户抽象参考](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/account-abstraction.md)
- [应用目录（25+ 应用）](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/apps.md)
- [流程示例](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/examples.md)
- [抽水向量参考](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/drain-vectors.md)
- [故障排查](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/troubleshooting.md)
- [aomi-workflow.sh 模板](https://github.com/aomi-labs/skills/blob/main/aomi-transact/templates/aomi-workflow.sh)