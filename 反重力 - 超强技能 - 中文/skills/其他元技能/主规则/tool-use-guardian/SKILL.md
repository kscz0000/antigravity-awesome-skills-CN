---
name: tool-use-guardian
description: "免费 — 智能工具调用可靠性包装器。监控、重试、修复工具故障并从中学习。自动恢复截断 JSON、超时、速率限制和链中断裂。"
category: reliability
risk: safe
source: community
date_added: "2026-03-13"
author: christopherlhammer11-ai
tags: [reliability, tool-use, error-handling, retries, recovery, agent-infrastructure]
tools: [claude, cursor, codex, gemini, copilot, windsurf, antigravity]
---

# Tool Use Guardian

## 概述

每个 AI 智能体都需要的可靠性包装器。监控工具调用、自动重试失败、修复截断响应、识别不可靠工具——确保思维链永不中断。

永久免费。由 Genesis Agent Marketplace 构建。

## 安装

```bash
npx skills add christopherlhammer11-ai/tool-use-guardian
```

## 适用场景

- 工具调用返回截断或格式错误的 JSON
- API 超时或在任务中途触发速率限制
- 多步骤链路中途断裂
- 需要自动重试逻辑但不想自己写
- 任何依赖外部工具可靠性的智能体工作流

## 工作原理

### 步骤 1：调用前验证

每次工具调用前，Guardian 会验证：
- 必需参数存在且类型正确
- 工具未因历史失败被标记为"不可靠"
- 请求大小在已知限制范围内

### 步骤 2：故障分类

工具调用失败时，Guardian 将故障归入以下 9 类之一：

| 故障类型 | 恢复动作 |
|---|---|
| 截断 JSON | 分页或分块重新获取 |
| API 超时 | 用更简请求重试一次，然后分解 |
| 速率限制 (429) | 指数退避，最多重试 3 次 |
| 认证过期 | 标记需用户介入 |
| 链中断裂 | 从最后成功的检查点恢复 |
| 伪装 200 错误 | 检测 `{"error": "..."}` 伪装的成功响应 |
| Schema 不匹配 | 尝试自动类型转换，有损时警告 |
| 网络故障 | 带抖动重试，最多 2 次 |
| 未知错误 | 记录完整上下文，上报用户 |

### 步骤 3：链路保护

对多步骤工具链，Guardian 维护检查点。若 7 步中的第 4 步失败，从第 4 步恢复——不会从头重跑。

### 步骤 4：学习

Guardian 按工具追踪故障模式。同一类型失败 3 次以上，标记该工具为不可靠并推荐替代方案。

## 最佳实践

- ✅ 让 Guardian 自动包装所有外部工具调用
- ✅ 查看 Guardian 的可靠性报告识别不稳定工具
- ✅ 长链路使用检查点恢复
- ❌ 不要禁用速率受限 API 的重试逻辑
- ❌ 不要忽视重复失败警告

## 相关技能

- `@recallmax` - 长上下文记忆增强（同样免费，来自 Genesis Marketplace）

## 链接

- **仓库：** https://github.com/christopherlhammer11-ai/tool-use-guardian
- **市场：** https://genesis-node-api.vercel.app
- **浏览技能：** https://genesis-marketplace.vercel.app

## 限制

- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 缺少必要输入、权限、安全边界或成功标准时，请停下来请求澄清。
