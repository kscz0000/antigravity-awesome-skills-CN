# Subagent Orchestrator — Antigravity 2.0 技能

配额感知的并行子智能体协调技能，专为 Antigravity 2.0 设计。

将一个大任务拆分为一组隔离、高效的智能体任务——不会在 30 分钟内耗尽你的每周配额。

---

## 它做什么

- 在编写任何代码之前，将复杂任务拆分为隔离的智能体任务
- 将任务路由到能处理它们的最便宜模型（默认 Flash）
- 并行运行独立智能体，而非顺序运行
- 全程监控配额用量，接近限制时暂停
- 无需重新运行整个任务即可从智能体故障中恢复
- 在宣布任务完成之前运行最终集成检查

---

## 安装

**一条命令（Windows PowerShell）：**
```powershell
node scripts/install.js
```

**手动安装 — 将此文件夹复制到：**
```
Windows: %USERPROFILE%\.agents\skills\subagent-orchestrator\
Mac/Linux: ~/.agents/skills/subagent-orchestrator/
```

然后重启你的 Antigravity 会话。

---

## 使用方法

当你的任务满足以下条件时，技能自动激活：
- 涉及 3 个以上文件或组件
- 需要并行智能体（UI + API、规划者 + 构建者等）
- 存在配额风险（大型代码库、预期大量工具调用）

或手动触发：
```
"使用 subagent-orchestrator 构建认证流程"
```

---

## 文件夹结构

```
subagent-orchestrator/
├── SKILL.md                          ← 主技能文件（由 Antigravity 自动加载）
├── scripts/
│   └── install.js                    ← 安装脚本
├── examples/
│   ├── nextjs-feature.md             ← 3 智能体并行 Next.js 功能
│   ├── api-plus-frontend.md          ← 后端 + 前端并行构建
│   └── debug-mission.md              ← 最少配额修复任务
└── resources/
    ├── mission-brief-template.md     ← 任意任务的可复制模板
    └── quota-reference.md            ← 每种操作类型的成本估算
```

---

## 配额参考（速查）

| 模型 | 成本 |
|-------|------|
| Gemini Flash | 1x（所有子智能体的默认） |
| Claude Sonnet | ~4x（每次任务最多 1 个） |
| Claude Opus | 永远不要在子智能体中使用 |

| 任务规模 | 预估冲刺用量 |
|-------------|-----------------|
| 单文件修复 | < 5% |
| 单一功能 | 15–25% |
| 完整流程（认证、API、UI） | 30–45% |

---

## 贡献

此技能是为了填补一个真实的空白而构建的——社区现有的子智能体技能没有配额管理、没有并行协调、也没有错误恢复。

欢迎 PR。遵循 Antigravity 文档中的 SKILL.md 格式。
提交至：https://github.com/sickn33/antigravity-awesome-skills

---

## 兼容性

- Antigravity 2.0+（CLI 和 IDE）
- Claude Code
- Cursor（通过 SKILL.md 标准）
- OpenCode
