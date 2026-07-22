# 示例：后端 API 智能体 + 前端 UI 智能体并行

## 场景
用户提示："构建一个方案生成器——前端表单，后端 AI 调用，屏幕显示结果。"

这是 ProposalKit 核心功能模式。

---

## 任务简报

```
MISSION BRIEF
─────────────────────────────────────────
Goal: 可用的方案生成器，包含表单输入、API 处理和结果展示。
Total Agents: 2 + 1 集成
Quota Strategy: MIXED — 后端用 Flash，前端 UI 用 Sonnet
Expected Token Cost: MEDIUM

AGENTS:
[1] ID: agent-001
    Role: Builder — 后端 API
    Scope: /app/api/generate/route.ts
    Model: Gemini Flash
    Input: NVIDIA API key 环境变量名，resources/prompt-template.md 中的提示模板
    Output: 接受 {clientName, projectType, budget}、返回 {proposal: string} 的 POST 路由
    Depends on: none

[2] ID: agent-002
    Role: Builder — 前端表单 + 展示
    Scope: /components/ProposalForm.tsx, /components/ProposalResult.tsx, /app/page.tsx
    Model: Claude Sonnet（UI 需要质量）
    Input: agent-001 规格中的 API 契约（仅输入/输出结构——不是代码）
    Output: 表单组件、结果展示、连接到 /api/generate
    Depends on: none（使用规格，不直接使用 agent-001 的输出）

[3] ID: agent-003
    Role: 集成者
    Scope: 仅审查——不创建新文件
    Model: Gemini Flash
    Input: agent-001 和 agent-002 的输出
    Output: API 契约与前端调用之间的任何不匹配列表
    Depends on: agent-001, agent-002
─────────────────────────────────────────
```

---

## 关键模式：规格优先并行

智能体 001 和 002 可以同时运行，因为：
- agent-002 接收的是 **API 契约**（输入/输出结构），而不是实际代码
- 契约在任一智能体运行前就已定义
- 两个智能体基于相同的约定规格工作

这避免了 agent-002 等待 agent-001 完成，节省了大量的时间和配额。

**在生成并行智能体之前始终定义 API 契约：**
```typescript
// 在智能体运行之前约定：
// POST /api/generate
// Input:  { clientName: string, projectType: string, budget: number }
// Output: { proposal: string, error?: string }
```

---

## 配额日志

| 事件 | 影响 |
|-------|--------|
| agent-001（Flash，1 个文件） | LOW |
| agent-002（Sonnet，3 个文件） | MEDIUM |
| agent-003（Flash，仅审查） | LOW |
| 0 个浏览器智能体 | NONE |
| **预估总量** | **~30% 冲刺** |
