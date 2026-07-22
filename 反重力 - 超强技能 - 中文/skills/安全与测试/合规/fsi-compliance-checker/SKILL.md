---
name: fsi-compliance-checker
description: "将代码、架构和基础设施变更映射到 PCI-DSS v4.0 与 MAS TRM（新加坡金融监管局）中的具体控制项 ID，产出可审计追溯的发现报告，并为每个控制项给出修复建议。涉及支付卡合规、新加坡银行监管、PCI-DSS 审计、TRM 控制项检查、PCI 合规审查时使用。"
category: security
risk: safe
source: community
source_repo: timwukp/agent-skills-best-practice
source_type: community
date_added: "2026-06-12"
author: timwukp
tags: [compliance, pci-dss, mas-trm, fintech, banking, security-review, audit, financial-services]
tools: [claude, cursor, gemini, codex, antigravity]
license: "MIT"
license_source: "https://github.com/timwukp/agent-skills-best-practice/blob/main/LICENSE"
---

# FSI 合规检查器

## 概述

将一项具体变更（代码 diff、架构设计、IaC、流水线配置）映射到金融服务合规框架中它所触及的具体控制项 —— PCI-DSS v4.0（支付卡数据）与 MAS TRM（新加坡监管机构）—— 并以可执行的修复建议报告差距。这是工程层面的合规分流：帮助团队在审计前发现违规，但**不能**替代合格评估员（QSA）或机构自身的合规职能。每份报告都需明确这一点。

## 何时使用此技能

- 当变更涉及支付卡数据（PAN、CVV、磁道数据）并需要进行 PCI-DSS 检查时使用
- 当针对新加坡监管的金融机构审查变更是否符合 MAS TRM 预期时使用
- 当有人询问"这合规吗"、"记录这些是否违反 PCI"，或要求对 diff、设计、Terraform 变更进行银行法规审查时使用
- 不要用于通用安全审查（无框架涉及）、GDPR/SOC2/HIPAA（超出打包范围）或法律建议

## 工作流程

### 步骤 1：选择框架

仅加载本次任务需要的参考文件：

| 情形 | 加载 |
|------|------|
| 支付卡数据被存储、处理或传输 | [pci-dss.md](pci-dss.md) |
| 新加坡监管的金融机构（银行、保险公司、资本市场、主要支付机构） | [mas-trm.md](mas-trm.md) |
| 两者均适用（例如处理卡数据的新加坡银行） | 两个文件均加载 |
| 其他司法管辖区/框架（SOX、GDPR、HKMA、APRA） | 说明超出范围；改为提供通用安全工程审查 |

如果用户未明确适用哪个框架，只问一个问题：变更涉及什么数据，该机构是否受新加坡监管？

### 步骤 2：界定变更范围

明确 diff/设计实际触及的内容：数据元素（卡数据？客户 PII？凭证？）、信任边界、环境（生产？灾备？）以及第三方。

### 步骤 3：评估适用的控制项

从加载的参考文件中选择适用的控制项 —— 通常为 5-15 项，而非整个框架。列出已排除的控制项及其原因（每项一行），以便范围界定可审计。每项评估为 `合规` / `差距` / `需补充证据`（无法从工件判断 —— 列出所需证据名称）。

### 步骤 4：报告

每个差距需包含：控制项 ID、本次变更中具体的问题、可执行的修复、严重程度（Critical = 涉及线上受监管数据的违规；High = 控制项缺失；Medium = 控制项部分缺失/无文档）。

```markdown
# Compliance Review: [change title]
**Frameworks:** [PCI-DSS v4.0 / MAS TRM 2021] · **Date:** [YYYY-MM-DD]
**Scope:** [what was reviewed: files, design doc, pipeline]
> Engineering triage only — not a substitute for QSA assessment or the compliance function.

## Data & Boundary Analysis
- Data elements touched: [e.g. PAN (masked), customer NRIC, none]
- Environments/boundaries: [e.g. CDE-adjacent service, public API]

## Findings
| # | Control | Status | Severity | Finding | Remediation |
|---|---------|--------|----------|---------|-------------|
| 1 | [PCI 3.5.1] | Gap | Critical | [specific issue in this change] | [specific fix] |

## Ruled Out (not applicable)
- [Control area] — [one-line reason]

## Evidence Needed
- [Control]: [what artifact would demonstrate compliance]
```

### 步骤 5：提供故事卡转换

提议将发现转化为待办事项，并在每张故事卡中包含控制项 ID 以便追溯。

## 示例

### 示例 1：日志审查

**用户**："这符合 PCI-DSS 吗：我们为了调试将卡授权调用的完整请求体记录到日志中？"

**技能**：加载 pci-dss.md → 针对 3.3.1（CVV 授权后绝不得存储 —— 日志即为存储）、3.4.1（PAN 显示脱敏）、3.5.1（PAN 在存储时不可读）提出 Critical 发现；修复方案：移除该行日志或应用字段白名单脱敏过滤器；标记下游日志流水线的范围（10.3.x）；包含 QSA 免责声明。

### 示例 2：云迁移

**用户**："我们新加坡银行正在将客户通知服务迁移到另一个国家的云区域。MAS TRM 的影响？"

**技能**：加载 mas-trm.md → 按 §11.5（云：尽职调查、数据驻留、退出策略）进行审查，标记 MAS 外包指南为相关工具，在评估严重程度前询问该服务涉及哪些客户数据。

## 常见 FSI 工程触发器

几乎总是具有合规影响的变更 —— 在 diff 中出现时应主动检查：

- 支付或身份验证流程附近的日志语句（PAN/CVV 绝不能被记录；MAS TRM 要求安全事件日志 —— 两个方向都要考虑）
- 接收客户或卡数据的新数据存储或缓存（静态加密、保留期、驻留性）
- 身份验证/会话变更（MFA 要求、会话超时、凭证存储）
- 新的第三方 SDK 或 API 集成（外包/供应商控制、数据流离开边界）
- 涉及网络分段、安全组或公网暴露的基础设施变更
- 改变谁能/什么可部署到生产的 CI/CD 变更（变更管理、职责分离）

## 护栏

- 精确引用控制项 ID（例如 "PCI-DSS 8.3.6"、"MAS TRM 9.1.1"），以便发现可在审计工具中追溯；打包的参考文件包含 ID 体系。
- 严重程度纪律：不要夸大。漏掉的注释不是 Critical；未加密的静态 PAN 才是。
- 当变更合规时，按控制项明确肯定 —— "无发现"加上已检查的控制项清单是有用的审计工件。
- 绝不输出真实卡号，即使是示例；说明时使用标准测试 PAN（例如 4111 1111 1111 1111）。
- 只读：本技能仅审查和报告，从不修改代码、基础设施或配置。

## 局限性

- 仅覆盖打包的 PCI-DSS v4.0 与 MAS TRM 工程摘要；其他框架或本地策略叠加需单独审查。
- 提供工程分流，而非法律建议、QSA 评估或正式合规签核。
- 要求具体证据，例如 diff、设计、IaC、日志或控制项工件；证据不完整应标记为 `需补充证据`。
- 打包的参考文件是简洁的控制项映射，不能替代阅读官方标准。

## 致谢

改编自 [timwukp/agent-skills-best-practice](https://github.com/timwukp/agent-skills-best-practice)（MIT），该技能随附评估和文档化的 4 层测试方法（参见该仓库的 TESTING.md）。