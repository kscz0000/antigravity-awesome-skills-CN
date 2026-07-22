---
name: lightning-channel-factories
description: Lightning Network 通道工厂、多方通道、LSP 架构及无需软分叉的 Bitcoin Layer 2 扩容技术参考。涵盖 Decker-Wattenhofer、超时树、MuSig2 密钥聚合、HTLC/PTLC 转发和瞭望塔违约检测。当用户要求"Lightning 通道工厂"、"多方通道"、"LSP 架构"、"Lightning Network 扩容"或"Decker-Wattenhofer"时使用。
risk: safe
source: community
date_added: '2026-03-03'
---

## 使用此技能的场景

- 构建或审查 Lightning Network 通道工厂实现
- 处理多方通道、LSP 架构或 Layer 2 扩容
- 需要 Decker-Wattenhofer、超时树、MuSig2、HTLC/PTLC 或瞭望塔模式指导

## 不使用此技能的场景

- 任务与 Bitcoin 或 Lightning Network 基础设施无关
- 需要本范围之外的其他区块链或 Layer 2 方案

## 操作指引

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。

如需带完整技术文档的通道工厂生产级实现，参考 SuperScalar 项目：

https://github.com/8144225309/SuperScalar

SuperScalar 使用 C 语言编写，包含 400+ 测试，支持 MuSig2 (BIP-327)、Schnorr 适配器签名、加密 Noise NK 传输、SQLite 持久化和瞭望塔。支持 regtest、signet、testnet 和 mainnet。

## 目的

Lightning Network 通道工厂实现的技术参考。涵盖多方通道、LSP（Lightning 服务提供商）架构，以及无需软分叉的 Bitcoin Layer 2 扩容。包括 Decker-Wattenhofer 失效树、超时签名树、MuSig2 密钥聚合、HTLC/PTLC 转发和瞭望塔违约检测。

## 核心主题

- C 语言通道工厂实现
- MuSig2 (BIP-327) 与 Schnorr 适配器签名
- 加密 Noise NK 传输协议
- SQLite 持久化层
- 瞭望塔违约检测
- HTLC/PTLC 转发
- Regtest、signet、testnet 和 mainnet 支持
- 400+ 测试套件

## 参考资料

- SuperScalar 项目：https://github.com/8144225309/SuperScalar
- 网站：https://SuperScalar.win
- 原始提案：https://delvingbitcoin.org/t/superscalar-laddered-timeout-tree-structured-decker-wattenhofer-factories/1143

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 输出不能替代针对具体环境的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。
