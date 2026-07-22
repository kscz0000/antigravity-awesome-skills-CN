---
name: parallel-agents
description: "多智能体编排模式。当多个独立任务可以使用不同领域专业知识运行，或当综合分析需要多个视角时使用。当用户要求'并行智能体编排'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 原生并行智能体

> 通过 Claude Code 内置 Agent 工具实现编排

## 概述

本技能通过 Claude Code 原生智能体系统协调多个专业智能体。与外部脚本不同，这种方式将所有编排保持在 Claude 的控制范围内。

## 何时使用编排

✅ **适合场景**：
- 需要多个专业领域知识的复杂任务
- 从安全、性能和质量角度分析代码
- 综合审查（架构 + 安全 + 测试）
- 需要后端 + 前端 + 数据库协作的功能实现

❌ **不适合场景**：
- 简单的单领域任务
- 快速修复或小改动
- 一个智能体就能搞定的任务

---

## 原生智能体调用

### 单个智能体
```
Use the security-auditor agent to review authentication
```

### 顺序链
```
First, use the explorer-agent to discover project structure.
Then, use the backend-specialist to review API endpoints.
Finally, use the test-engineer to identify test gaps.
```

### 带上下文传递
```
Use the frontend-specialist to analyze React components.
Based on those findings, have the test-engineer generate component tests.
```

### 恢复之前的工作
```
Resume agent [agentId] and continue with additional requirements.
```

---

## 编排模式

### 模式 1：综合分析
```
Agents: explorer-agent → [domain-agents] → synthesis

1. explorer-agent: Map codebase structure
2. security-auditor: Security posture
3. backend-specialist: API quality
4. frontend-specialist: UI/UX patterns
5. test-engineer: Test coverage
6. Synthesize all findings
```

### 模式 2：功能审查
```
Agents: affected-domain-agents → test-engineer

1. Identify affected domains (backend? frontend? both?)
2. Invoke relevant domain agents
3. test-engineer verifies changes
4. Synthesize recommendations
```

### 模式 3：安全审计
```
Agents: security-auditor → penetration-tester → synthesis

1. security-auditor: Configuration and code review
2. penetration-tester: Active vulnerability testing
3. Synthesize with prioritized remediation
```

---

## 可用智能体

| 智能体 | 专业领域 | 触发短语 |
|-------|-----------|-----------------|
| `orchestrator` | 协调 | "comprehensive", "multi-perspective" |
| `security-auditor` | 安全 | "security", "auth", "vulnerabilities" |
| `penetration-tester` | 安全测试 | "pentest", "red team", "exploit" |
| `backend-specialist` | 后端 | "API", "server", "Node.js", "Express" |
| `frontend-specialist` | 前端 | "React", "UI", "components", "Next.js" |
| `test-engineer` | 测试 | "tests", "coverage", "TDD" |
| `devops-engineer` | DevOps | "deploy", "CI/CD", "infrastructure" |
| `database-architect` | 数据库 | "schema", "Prisma", "migrations" |
| `mobile-developer` | 移动端 | "React Native", "Flutter", "mobile" |
| `api-designer` | API 设计 | "REST", "GraphQL", "OpenAPI" |
| `debugger` | 调试 | "bug", "error", "not working" |
| `explorer-agent` | 发现 | "explore", "map", "structure" |
| `documentation-writer` | 文档 | "write docs", "create README", "generate API docs" |
| `performance-optimizer` | 性能 | "slow", "optimize", "profiling" |
| `project-planner` | 规划 | "plan", "roadmap", "milestones" |
| `seo-specialist` | SEO | "SEO", "meta tags", "search ranking" |
| `game-developer` | 游戏开发 | "game", "Unity", "Godot", "Phaser" |

---

## Claude Code 内置智能体

这些与自定义智能体配合使用：

| 智能体 | 模型 | 用途 |
|-------|-------|---------|
| **Explore** | Haiku | 快速只读代码库搜索 |
| **Plan** | Sonnet | 规划模式下的研究 |
| **General-purpose** | Sonnet | 复杂的多步骤修改 |

使用 **Explore** 进行快速搜索，使用**自定义智能体**处理领域专业知识。

---

## 综合协议

所有智能体完成后，进行综合：

```markdown
## Orchestration Synthesis

### Task Summary
[What was accomplished]

### Agent Contributions
| Agent | Finding |
|-------|---------|
| security-auditor | Found X |
| backend-specialist | Identified Y |

### Consolidated Recommendations
1. **Critical**: [Issue from Agent A]
2. **Important**: [Issue from Agent B]
3. **Nice-to-have**: [Enhancement from Agent C]

### Action Items
- [ ] Fix critical security issue
- [ ] Refactor API endpoint
- [ ] Add missing tests
```

---

## 最佳实践

1. **可用智能体** - 可编排 17 个专业智能体
2. **逻辑顺序** - 发现 → 分析 → 实现 → 测试
3. **共享上下文** - 将相关发现传递给后续智能体
4. **单一综合** - 一份统一报告，而非各自独立的输出
5. **验证变更** - 代码修改始终包含 test-engineer

---

## 核心优势

- ✅ **单会话** - 所有智能体共享上下文
- ✅ **AI 控制** - Claude 自主编排
- ✅ **原生集成** - 与内置 Explore、Plan 智能体配合
- ✅ **恢复支持** - 可继续之前的智能体工作
- ✅ **上下文传递** - 发现在智能体间流转

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，停下来请求澄清。
