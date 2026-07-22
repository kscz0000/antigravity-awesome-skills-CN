---
name: progressive-estimation
description: "使用研究支持的 PERT 统计和校准反馈循环，估算 AI 辅助及人机混合开发工作量。触发词：估算、项目管理、PERT、冲刺规划、AI代理、开发工作量估算、sprint planning、任务估算、capacity planning"
category: project-management
risk: safe
source: community
date_added: "2026-03-10"
author: Enreign
tags:
  - estimation
  - project-management
  - pert
  - sprint-planning
  - ai-agents
tools:
  - claude
---

# 渐进式估算

使用研究支持的公式、PERT 统计、置信区间和校准反馈循环，估算 AI 辅助及人机混合开发工作量。

## 概述

渐进式估算会适配团队的工作模式——纯人工、人机混合或代理优先——为每种模式应用相应的速率模型和乘数。它输出的是统计估算，而非主观感觉。

## 使用场景

- 估算 AI 代理参与部分工作的开发任务
- 人机混合团队的冲刺规划
- 批量评估待办事项规模（支持 5 到 500 个 issue）
- 结合代理乘数的人员配置和产能规划
- 带置信区间的发布日期预测

## 工作原理

1. **模式检测** — 判断团队是纯人工、人机混合还是代理优先
2. **任务分类** — 按规模（XS–XL）、复杂度和风险进行分类
3. **公式应用** — 基于实证研究应用乘数
4. **PERT 计算** — 使用三点估算生成期望值
5. **置信区间** — 输出 P50、P75、P90 区间
6. **输出格式化** — 适配 Linear、JIRA、ClickUp、GitHub Issues、Monday 或 GitLab
7. **校准** — 回馈实际数据以优化后续估算

## 示例

**单任务：**
> "估算用 Claude Code 构建带认证的 REST API 的工作量"

**批量模式：**
> "估算这 12 个 JIRA 工单在下个冲刺的工作量"

**带上下文：**
> "我们有 3 个开发者，AI 代理负责约 60% 的实现工作。估算这个功能。"

## 最佳实践

- 先用单任务校准，再进入批量模式
- 回馈实际完成时间以优化校准系统
- 使用"快速模式"进行 T-shirt 尺寸估算，无需完整 PERT 分析
- 明确团队构成和代理使用比例

## 常见问题

- **问题：** 估算过于乐观
  **方案：** 承诺时使用 P75 或 P90，而非 P50

- **问题：** 缺少上下文
  **方案：** 技能会主动提问——提供团队规模和代理使用比例

- **问题：** 校准数据过时
  **方案：** 团队构成或工具链发生重大变化时重新校准

## 相关技能

- `@sprint-planning` - 冲刺规划和待办事项管理
- `@project-management` - 通用项目管理工作流
- `@capacity-planning` - 团队速率和产能规划

## 延伸资源

- [源码仓库](https://github.com/Enreign/progressive-estimation)
- [安装指南](https://github.com/Enreign/progressive-estimation/blob/main/INSTALLATION.md)
- [研究参考](https://github.com/Enreign/progressive-estimation/tree/main/references)

## 局限性
- 仅在任务明确匹配上述范围时使用此技能
- 输出结果不能替代针对特定环境的验证、测试或专家评审
- 缺少必要输入、权限、安全边界或成功标准时，应停下来请求澄清
