# antigravity-skill-orchestrator

Antigravity IDE 生态系统的元技能包。

## 概述

`antigravity-skill-orchestrator` 是一个智能元技能，可增强 AI 智能体处理复杂、跨领域任务的能力。它提供严格的指导原则和工作流程，使智能体能够：

1. **评估任务复杂度**：实施防护措施，防止在简单、直接的任务上过度使用专业技能。
2. **动态选择技能**：为给定复杂问题识别最佳技能组合。
3. **追踪技能组合**：利用 `agent-memory-mcp` 技能存储、搜索和检索成功的技能组合以供未来参考，逐步构建机构知识。

## 安装

此技能设计用于 Antigravity IDE 内部，并与现有的 AWESOME 技能套件集成。

确保已安装并运行 `agent-memory-mcp` 技能，以充分利用组合追踪功能。

## 使用方法

在 Antigravity IDE 中通过 AI 助手执行提示词时，可以这样调用此技能：

```bash
@antigravity-skill-orchestrator Please build a comprehensive dashboard integrating fetching live data, an interactive UI, and performance optimizations.
```

智能体将按照 `SKILL.md` 中的指令分解任务、在记忆中搜索类似挑战、组装合适的技能团队（例如 `@react-patterns` + `@nodejs-backend-patterns`），并在不过度复杂化的情况下执行任务。

---

**作者：** [Wahid](https://github.com/wahidzzz)  
**来源：** [antigravity-skill-orchestrator](https://github.com/wahidzzz/antigravity-skill-orchestrator)
