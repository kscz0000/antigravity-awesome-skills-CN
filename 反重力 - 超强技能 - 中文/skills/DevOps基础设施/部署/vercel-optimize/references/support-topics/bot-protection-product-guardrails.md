---
id: bot-protection-product-guardrails
title: Bot Protection product guardrails
status: active
candidateKinds: ["platform_bot_protection"]
frameworks: ["*"]
priority: 90
citations: ["https://vercel.com/docs/bot-management", "https://vercel.com/docs/vercel-firewall/vercel-waf/managed-rulesets", "https://vercel.com/docs/vercel-firewall/vercel-waf/custom-rules", "https://vercel.com/docs/botid"]
maxBriefChars: 800
---

## 调查简报
Bot 保护建议必须以观察到的自动流量或有意义的边缘请求规模为基础。

## 需要检查的证据
检查 bot 带宽份额、边缘请求量、现有的 WAF 托管规则，以及 BotID 或 Bot 保护是否已启用。对于未证明误报风险的规则，优先选择分阶段的 Log to Challenge 或 Deny 路径。

## 何时不建议
不要推荐禁用 Vercel 安全产品来降低成本。不要在没有 bot 证据的安静项目上推荐 Bot 保护。

## 验证
说明观察到的 bot 份额或规模信号、当前保护状态，以及任何现有的 log、challenge、deny 或 BotID 检查。