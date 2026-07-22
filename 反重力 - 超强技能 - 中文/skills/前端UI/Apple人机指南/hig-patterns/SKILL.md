---
name: hig-patterns
description: Apple 人机交互指南交互和 UX 模式。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG: 交互模式

提问前请检查 `.claude/apple-design-context.md`。使用已有上下文，仅询问未覆盖的信息。

## 核心原则

1. **最小化模态。** 仅在需要引起注意、任务必须完成或放弃、或保存更改至关重要时使用模态。优先使用非模态替代方案。

2. **提供清晰反馈。** 每个操作都应产生可见、可听或触觉响应。不确定等待使用活动指示器，确定进度使用进度条，物理确认使用触觉反馈。

3. **支持撤销而非确认对话框。** 破坏性操作应尽可能可逆。撤销几乎总是比"您确定吗？"更好。

4. **快速启动。** 显示能无缝过渡到第一个屏幕的启动屏幕。不要使用带 logo 的闪屏。恢复之前的状态。

5. **延迟登录。** 让用户在要求创建账户之前先探索。支持 Sign in with Apple 和通行密钥。

6. **保持引导流程简短。** 最多三个屏幕。让用户可以跳过。通过渐进式披露和上下文提示进行教学。

7. **使用渐进式披露。** 首先显示要点，让用户深入查看详情。不要在一个屏幕上用所有选项淹没用户。

8. **尊重用户注意力。** 整合通知，最小化中断，让用户控制提醒。切勿将通知用于营销。

## 参考索引

| 参考 | 主题 | 关键内容 |
|---|---|---|
| [charting-data.md](references/charting-data.md) | 数据图表 | 数据可视化模式、无障碍图表、交互元素 |
| [collaboration-and-sharing.md](references/collaboration-and-sharing.md) | 协作与共享 | 分享面板、活动视图、协作编辑、SharePlay |
| [drag-and-drop.md](references/drag-and-drop.md) | 拖放 | 拖拽源、放置目标、弹簧加载、多项目拖拽、视觉反馈 |
| [entering-data.md](references/entering-data.md) | 数据输入 | 文本字段、选择器、步进器、输入验证、键盘类型、自动填充 |
| [feedback.md](references/feedback.md) | 反馈 | 警告、操作表、触觉模式、声音反馈、视觉指示器 |
| [file-management.md](references/file-management.md) | 文件管理 | 文档浏览器、文件提供者、iCloud 集成、文档生命周期 |
| [going-full-screen.md](references/going-full-screen.md) | 全屏 | 全屏转场、沉浸式内容、退出全屏 |
| [launching.md](references/launching.md) | 启动 | 启动屏幕、状态恢复、冷启动与热启动 |
| [live-viewing-apps.md](references/live-viewing-apps.md) | 实时查看应用 | 实时内容展示、实时更新、实时活动、灵动岛 |
| [loading.md](references/loading.md) | 加载 | 活动指示器、进度视图、骨架屏、懒加载、占位符 |
| [managing-accounts.md](references/managing-accounts.md) | 账户管理 | Sign in with Apple、通行密钥、账户创建、凭证自动填充、账户删除 |
| [managing-notifications.md](references/managing-notifications.md) | 通知管理 | 权限请求、分组、可操作通知、临时投递 |
| [modality.md](references/modality.md) | 模态 | 表单、警告、弹出框、全屏模态、何时使用每种 |
| [multitasking.md](references/multitasking.md) | 多任务 | iPad 分屏视图、侧拉、台前调度、响应式布局、尺寸类别转换 |
| [offering-help.md](references/offering-help.md) | 提供帮助 | 上下文提示、引导提示、帮助菜单、支持链接 |
| [onboarding.md](references/onboarding.md) | 引导流程 | 欢迎屏幕、功能亮点、渐进式引导、跳过选项 |
| [playing-audio.md](references/playing-audio.md) | 音频播放 | 音频会话、后台音频、正在播放、音频路由、中断处理 |
| [playing-haptics.md](references/playing-haptics.md) | 触觉播放 | Core Haptics、UIFeedbackGenerator、触觉模式、自定义触觉 |
| [playing-video.md](references/playing-video.md) | 视频播放 | 视频播放器控件、画中画、AirPlay、全屏视频 |
| [printing.md](references/printing.md) | 打印 | 打印对话框、页面设置、AirPrint 集成 |
| [ratings-and-reviews.md](references/ratings-and-reviews.md) | 评分与评论 | SKStoreReviewController、时机、频率限制、应用内反馈 |
| [searching.md](references/searching.md) | 搜索 | 搜索栏、建议、范围搜索、结果展示、最近搜索 |
| [settings.md](references/settings.md) | 设置 | 应用内与系统设置应用、偏好组织、开关、默认值 |
| [undo-and-redo.md](references/undo-and-redo.md) | 撤销与重做 | 摇动撤销、撤销/重做栈、多级撤销 |
| [workouts.md](references/workouts.md) | 健身 | 健身会话、实时指标、常亮显示、摘要、HealthKit |

## 模式选择指南

| 用户目标 | 推荐模式 | 避免 |
|---|---|---|
| 首次应用体验 | 简短引导（最多 3 个屏幕）+ 渐进式披露 | 长教程、强制注册 |
| 等待内容 | 骨架屏或进度指示器 | 无上下文的阻塞式加载器 |
| 确认破坏性操作 | 撤销支持 | 过多的"您确定吗？"对话框 |
| 收集用户输入 | 内联验证、智能默认值、自动填充 | 简单输入使用模态表单 |
| 请求权限 | 上下文相关、即时请求并说明 | 启动时请求所有权限 |
| 提供反馈 | 触觉 + 视觉指示器 | 无确认的静默操作 |
| 组织偏好 | 频繁使用的项目放在应用内设置 | 将所有设置埋在系统设置应用中 |

## 输出格式

1. **推荐模式及理由**，引用相关参考文件。
2. **分步实现**，涵盖每个屏幕或状态。
3. **目标平台的平台变体**。
4. **违反此模式 HIG 的常见陷阱**。

## 需要询问的问题

1. 此模式出现在应用的哪个位置？前后是什么？
2. 哪些平台？
3. 从头设计还是改进现有流程？
4. 是否涉及敏感操作？（破坏性操作、支付、权限）

## 相关技能

- **hig-foundations** — 每个模式基础的无障碍、颜色、排版和隐私原则
- **hig-platforms** — 平台特定的模式实现
- **hig-components-layout** — 导航模式的结构组件（标签栏、侧边栏、分屏视图）
- **hig-components-content** — 模式中的内容展示（图表、集合、搜索结果）

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
