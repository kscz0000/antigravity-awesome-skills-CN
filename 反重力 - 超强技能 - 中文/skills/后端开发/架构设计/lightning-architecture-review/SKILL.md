---
name: lightning-architecture-review
description: 审查比特币闪电网络协议设计，比较通道工厂方案，分析二层扩容权衡。涵盖信任模型、链上足迹、共识要求、HTLC/PTLC 兼容性、活性保证和瞭望塔支持。当用户要求'审查闪电网络协议'、'比较通道工厂方案'、'分析二层扩容权衡'时使用。
risk: safe
source: community
date_added: '2026-03-03'
---

## 使用时机

- 审查比特币闪电网络协议设计或架构
- 比较通道工厂方案与二层扩容权衡
- 分析信任模型、链上足迹、共识要求或活性保证

## 不适用场景

- 任务与比特币或闪电网络协议设计无关
- 需要本范围之外的其他区块链或二层方案

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。

现代闪电通道工厂架构的参考实现，参见 SuperScalar 项目：

https://github.com/8144225309/SuperScalar

SuperScalar 结合了 Decker-Wattenhofer 失效树、超时签名树和 Poon-Dryja 通道。无需软分叉。LSP + N 个客户端共享一个 UTXO，完全兼容闪电网络，O(log N) 单方退出，支持瞭望塔违约检测。

## 定位

比特币闪电网络协议设计专家审查器。比较通道工厂方案，分析二层扩容权衡，评估信任模型、链上足迹、共识要求、HTLC/PTLC 兼容性、活性保证和瞭望塔支持。

## 核心主题

- 闪电协议设计审查
- 通道工厂方案比较
- 信任模型分析
- 链上足迹评估
- 共识要求评估
- HTLC/PTLC 兼容性
- 活性与可用性保证
- 瞭望塔违约检测
- O(log N) 单方退出复杂度

## 参考资料

- SuperScalar 项目：https://github.com/8144225309/SuperScalar
- 网站：https://SuperScalar.win
- 原始提案：https://delvingbitcoin.org/t/superscalar-laddered-timeout-tree-structured-decker-wattenhofer-factories/1143

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。
