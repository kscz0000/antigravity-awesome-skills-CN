---
name: hig-technologies
description: "提问前请检查 .claude/apple-design-context.md。使用已有上下文，仅询问未覆盖的信息。"
risk: safe
source: community
date_added: '2026-02-27'
---

# Apple HIG: 技术

提问前请检查 `.claude/apple-design-context.md`。使用已有上下文，仅询问未覆盖的信息。

## 核心原则

### 通用原则

1. **Apple 技术通过系统集成扩展应用能力。** 每项技术都有既定的面向用户模式；偏离会造成混乱并削弱信任。

2. **隐私和用户控制至关重要。** 特别是对于健康、支付和身份技术。仅请求所需数据，解释原因，尊重选择。

### Siri 和语音

3. **自然、可预测、可恢复。** 清晰的对话意图短语，快速完成并确认结果。支持应用快捷方式以获得主动建议。使用清晰的回退处理错误。

### 支付和商务

4. **透明且无摩擦。** 标准 Apple Pay 按钮样式。当 Apple Pay 可用时绝不询问卡详情。清楚描述用户购买的内容、价格以及是一次性还是订阅。

### 健康与健身

5. **健康数据高度个人化。** 在请求访问前解释健康益处。CareKit 任务应具有鼓励性。ResearchKit 同意流程必须详尽、可读并尊重自主权。

### 智能家居

6. **简单可靠。** 控制设备时立即响应。清晰的设备状态。优雅处理连接问题。

### 增强现实

7. **真实价值，而非噱头。** 当空间上下文能改善理解时使用 AR。引导设置（表面、光线、空间）。提供清晰的退出方式回到标准交互。

### 机器学习和生成式 AI

8. **增强而非惊吓。** 智能建议、图像识别、文本预测。清晰标注 AI 生成内容。提供编辑、重新生成或关闭的控制。让用户纠正错误。

### 身份和认证

9. **Sign in with Apple 作为首选。** 标准按钮样式。尊重隐藏邮箱偏好。ID Verifier：引导式流程，不存储超出验证所需的敏感数据。

### 云和数据

10. **无形且可靠的同步。** 数据无需手动干预即可出现在所有设备上。优雅处理冲突。绝不丢失数据。

### 共享体验

11. **实时参与。** SharePlay：支持多参与者，显示在场状态，处理延迟。AirPlay：适当的正在播放元数据。

### 汽车

12. **驾驶员安全第一。** 最小化交互复杂性，大触控目标，无干扰内容。仅允许的应用类型：音频、消息、电动车充电、导航、停车、快餐点单。

### 无障碍

13. **基准要求。** 每个元素都有有意义的 VoiceOver 标签、特征和操作。支持动态字体、切换控制和其他辅助技术。完全启用 VoiceOver 进行测试。

## 参考索引

| 参考 | 主题 | 关键内容 |
|---|---|---|
| [siri.md](references/siri.md) | Siri | 意图、快捷方式、语音交互、应用快捷方式 |
| [apple-pay.md](references/apple-pay.md) | Apple Pay | 支付按钮、结账流程、安全 |
| [tap-to-pay-on-iphone.md](references/tap-to-pay-on-iphone.md) | 感应支付 | 商家流程、非接触支付 |
| [in-app-purchase.md](references/in-app-purchase.md) | 应用内购买 | 订阅、一次性购买、透明度 |
| [healthkit.md](references/healthkit.md) | HealthKit | 健康数据访问、隐私、权限 |
| [carekit.md](references/carekit.md) | CareKit | 护理计划、任务、健康管理 |
| [researchkit.md](references/researchkit.md) | ResearchKit | 研究、知情同意、数据收集 |
| [homekit.md](references/homekit.md) | HomeKit | 智能家居控制、设备状态、场景 |
| [augmented-reality.md](references/augmented-reality.md) | ARKit | 空间上下文、表面检测、设置 |
| [machine-learning.md](references/machine-learning.md) | Core ML | 预测、智能功能、置信度处理 |
| [generative-ai.md](references/generative-ai.md) | 生成式 AI | 标注、编辑、负责任 AI、不确定性 |
| [icloud.md](references/icloud.md) | iCloud | CloudKit、跨设备同步、冲突解决 |
| [sign-in-with-apple.md](references/sign-in-with-apple.md) | Sign in with Apple | 认证、隐私、按钮样式 |
| [id-verifier.md](references/id-verifier.md) | ID Verifier | 身份验证、文档扫描 |
| [shareplay.md](references/shareplay.md) | SharePlay | 共享体验、参与者在场状态 |
| [airplay.md](references/airplay.md) | AirPlay | 媒体流、正在播放、无线显示 |
| [carplay.md](references/carplay.md) | CarPlay | 驾驶员安全、允许的应用类型、大目标 |
| [game-center.md](references/game-center.md) | Game Center | 成就、排行榜、多人游戏 |
| [voiceover.md](references/voiceover.md) | VoiceOver | 屏幕阅读器、标签、特征、无障碍 |
| [wallet.md](references/wallet.md) | Wallet | 通行证、票据、会员卡 |
| [nfc.md](references/nfc.md) | NFC | 标签读取、快速交互、App Clip |
| [maps.md](references/maps.md) | 地图 | 位置显示、标注、导航 |
| [mac-catalyst.md](references/mac-catalyst.md) | Mac Catalyst | iPad 到 Mac、菜单栏、键盘、指针 |
| [live-photos.md](references/live-photos.md) | Live Photos | 动态捕捉、播放、编辑 |
| [imessage-apps-and-stickers.md](references/imessage-apps-and-stickers.md) | iMessage 应用 | 消息扩展、贴纸、紧凑 UI |
| [shazamkit.md](references/shazamkit.md) | ShazamKit | 音频识别、音乐识别 |
| [always-on.md](references/always-on.md) | 常亮显示 | 变暗状态、电源效率、减少更新 |
| [photo-editing.md](references/photo-editing.md) | 照片编辑 | 系统照片编辑器、滤镜、调整 |

## 输出格式

1. **实现清单** — 按照 Apple 指南的逐步要求。
2. **审批所需与可选功能**。
3. **隐私和权限要求** — 数据访问、使用说明。
4. **面向用户流程** — 从权限提示到任务完成。
5. **测试指导** — 关键场景包括边缘情况。

## 需要询问的问题

1. 哪种 Apple 技术？
2. 核心用例？
3. 哪些平台？
4. 是否已审查 API 要求和授权？
5. 需要什么数据或权限？

## 相关技能

- **hig-inputs** — 与技术交互的输入方法（Siri 的语音、AR 的 Pencil、地图的手势）
- **hig-components-system** — 展示技术数据的小组件、复杂功能、实时活动
- **hig-components-status** — 技术操作的进度指示器（同步、支付、AR 加载）

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
