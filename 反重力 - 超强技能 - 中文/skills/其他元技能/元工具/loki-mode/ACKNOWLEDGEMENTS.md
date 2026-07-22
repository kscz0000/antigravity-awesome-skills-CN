# 致谢

Loki Mode 站在巨人的肩膀上。本项目融合了来自领先 AI 实验室、学术机构和业界实践者的研究、模式与洞见。

---

## 研究实验室

### Anthropic

Loki Mode 专为 Claude 构建，融合了 Anthropic 在 AI 安全和智能体开发方面的前沿研究。

| 论文/资源 | 对 Loki Mode 的贡献 |
|----------------|---------------------------|
| [Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) | 基于原则的自我批评、修订工作流 |
| [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | 评估器-优化器模式、并行化、路由 |
| [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) | Explore-Plan-Code 工作流、上下文管理 |
| [Simple Probes Can Catch Sleeper Agents](https://www.anthropic.com/research/probes-catch-sleeper-agents) | 叛逃探针、异常检测模式 |
| [Alignment Faking in Large Language Models](https://www.anthropic.com/research/alignment-faking) | 战略性顺从监控 |
| [Visible Extended Thinking](https://www.anthropic.com/research/visible-extended-thinking) | 思维等级（think、think hard、ultrathink） |
| [Computer Use Safety](https://www.anthropic.com/news/3-5-models-and-computer-use) | 安全自主操作模式 |
| [Sabotage Evaluations](https://www.anthropic.com/research/sabotage-evaluations-for-frontier-models) | 安全评估方法论 |
| [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 单功能迭代模式、Playwright MCP 用于 E2E |
| [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview) | Task 工具、子智能体、resume 参数、hooks |

### Google DeepMind

DeepMind 在世界模型、层次化推理和可扩展监督方面的研究为 Loki Mode 的架构提供了支撑。

| 论文/资源 | 对 Loki Mode 的贡献 |
|----------------|---------------------------|
| [SIMA 2: Generalist AI Agent](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/) | 自我改进循环、奖励模型训练 |
| [Gemini Robotics 1.5](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/) | 层次化推理（规划器 + 执行器） |
| [Dreamer 4: World Model Training](https://danijar.com/project/dreamer4/) | 仿真优先测试、安全探索 |
| [Genie 3: World Models](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) | 世界模型架构模式 |
| [Scalable AI Safety via Doubly-Efficient Debate](https://deepmind.google/research/publications/34920/) | 基于辩论的关键变更验证 |
| [Human-AI Complementarity for Amplified Oversight](https://deepmindsafetyresearch.medium.com/human-ai-complementarity-a-goal-for-amplified-oversight-0ad8a44cae0a) | AI 辅助人类监督 |
| [Technical AGI Safety Approach](https://arxiv.org/html/2504.01849v1) | 安全优先的智能体设计 |

### OpenAI

OpenAI 的 Agents SDK 和深度研究模式为智能体编排提供了基础模式。

| 论文/资源 | 对 Loki Mode 的贡献 |
|----------------|---------------------------|
| [Agents SDK Documentation](https://openai.github.io/openai-agents-python/) | 追踪 spans、guardrails、tripwires |
| [A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | 智能体架构最佳实践 |
| [Building Agents Track](https://developers.openai.com/tracks/building-agents/) | 开发模式、handoff 回调 |
| [AGENTS.md Specification](https://agents.md/) | 标准化智能体指令 |
| [Introducing Deep Research](https://openai.com/index/introducing-deep-research/) | 自适应规划、回溯 |
| [Deep Research System Card](https://cdn.openai.com/deep-research-system-card.pdf) | 研究智能体的安全考量 |
| [Introducing o3 and o4-mini](https://openai.com/index/introducing-o3-and-o4-mini/) | 推理模型指导 |
| [Reasoning Best Practices](https://platform.openai.com/docs/guides/reasoning-best-practices) | 扩展思维模式 |
| [Chain of Thought Monitoring](https://openai.com/index/chain-of-thought-monitoring/) | 推理链监控 |
| [Agent Builder Safety](https://platform.openai.com/docs/guides/agent-builder-safety) | 智能体构建者安全模式 |
| [Computer-Using Agent](https://openai.com/index/computer-using-agent/) | 计算机使用模式 |
| [Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) | 行业标准、互操作性 |

### Amazon Web Services (AWS)

AWS Bedrock 的多智能体协作模式为 Loki Mode 的路由和调度策略提供了参考。

| 论文/资源 | 对 Loki Mode 的贡献 |
|----------------|---------------------------|
| [Multi-Agent Orchestration Guidance](https://aws.amazon.com/solutions/guidance/multi-agent-orchestration-on-aws/) | 三种协调机制、架构模式 |
| [Bedrock Multi-Agent Collaboration](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html) | Supervisor 模式、路由模式、10 智能体限制 |
| [Multi-Agent Collaboration Announcement](https://aws.amazon.com/blogs/aws/introducing-multi-agent-collaboration-capability-for-amazon-bedrock/) | 意图分类、选择性上下文共享 |
| [AgentCore for SRE](https://aws.amazon.com/blogs/machine-learning/build-multi-agent-site-reliability-engineering-assistants-with-amazon-bedrock-agentcore/) | Gateway、Memory、Identity、Observability 组件 |

**采纳的关键模式：** 路由模式优化 - 简单任务直接调度（低延迟），复杂任务由 supervisor 编排（完整协调）。

---

## 学术研究

### 多智能体系统

| 论文 | 作者/来源 | 贡献 |
|-------|----------------|--------------|
| [Multi-Agent Collaboration Mechanisms Survey](https://arxiv.org/abs/2501.06322) | arXiv 2501.06322 | 协作结构、竞合 |
| [CONSENSAGENT: Anti-Sycophancy Framework](https://aclanthology.org/2025.findings-acl.1141/) | ACL 2025 Findings | 盲审、魔鬼代言人 |
| [GoalAct: Hierarchical Execution](https://arxiv.org/abs/2504.16563) | arXiv 2504.16563 | 全局规划、技能分解 |
| [A-Mem: Agentic Memory System](https://arxiv.org/html/2502.12110v11) | arXiv 2502.12110 | Zettelkasten 风格的记忆链接 |
| [Multi-Agent Reflexion (MAR)](https://arxiv.org/html/2512.20845) | arXiv 2512.20845 | 结构化辩论、基于人设的批评者 |
| [Iter-VF: Iterative Verification-First](https://arxiv.org/html/2511.21734v1) | arXiv 2511.21734 | 仅答案验证、马尔可夫重试 |

### 评估与安全

| 论文 | 作者/来源 | 贡献 |
|-------|----------------|--------------|
| [Assessment Framework for Agentic AI](https://arxiv.org/html/2512.12791v1) | arXiv 2512.12791 | 四支柱评估框架 |
| [Measurement Imbalance in Agentic AI](https://arxiv.org/abs/2506.02064) | arXiv 2506.02064 | 多维评估轴 |
| [Demo-to-Deployment Gap](https://www.marktechpost.com/2025/12/24/) | Stanford/Harvard | 工具可靠性 vs 工具选择 |

---

## 行业资源

### 工具与框架

| 资源 | 贡献 |
|----------|--------------|
| [NVIDIA ToolOrchestra](https://github.com/NVlabs/ToolOrchestra) | 效率指标、三奖励信号框架、动态智能体选择 |
| [LerianStudio/ring](https://github.com/LerianStudio/ring) | 子智能体驱动开发模式 |
| [Awesome Agentic Patterns](https://github.com/nibzard/awesome-agentic-patterns) | 105+ 生产模式目录 |

### 最佳实践指南

| 资源 | 贡献 |
|----------|--------------|
| [Maxim AI: Production Multi-Agent Systems](https://www.getmaxim.ai/articles/best-practices-for-building-production-ready-multi-agent-systems/) | 关联 ID、故障处理 |
| [UiPath: Agent Builder Best Practices](https://www.uipath.com/blog/ai/agent-builder-best-practices) | 单一职责智能体 |
| [GitHub: Speed Without Control](https://github.blog/) | 静态分析 + AI 审查、guardrails |

---

## Hacker News 社区

来自在生产环境中部署智能体的实践者的实战经验。

### 讨论

| 帖子 | 核心洞见 |
|--------|-------------|
| [What Actually Works in Production for Autonomous Agents](https://news.ycombinator.com/item?id=44623207) | "没有任何公司能在没有人类参与的情况下运作" |
| [Coding with LLMs in Summer 2025](https://news.ycombinator.com/item?id=44623953) | 上下文策展优于自动 RAG |
| [Superpowers: How I'm Using Coding Agents](https://news.ycombinator.com/item?id=45547344) | 用子智能体实现上下文隔离（Simon Willison） |
| [Claude Code Experience After Two Weeks](https://news.ycombinator.com/item?id=44596472) | 全新上下文能产出更好的结果 |
| [AI Agent Benchmarks Are Broken](https://news.ycombinator.com/item?id=44531697) | LLM-as-judge 存在共同盲区 |
| [How to Orchestrate Multi-Agent Workflows](https://news.ycombinator.com/item?id=45955997) | 事件驱动、解耦协调 |
| [Context Engineering vs Prompt Engineering](https://news.ycombinator.com/item?id=44427757) | 手动上下文选择原则 |

### Show HN 项目

| 项目 | 贡献 |
|---------|--------------|
| [Self-Evolving Agents Repository](https://news.ycombinator.com/item?id=45099226) | 自我改进模式 |
| [Package Manager for Agent Skills](https://news.ycombinator.com/item?id=46422264) | 技能架构 |
| [Wispbit - AI Code Review Agent](https://news.ycombinator.com/item?id=44722603) | 代码审查模式 |
| [Agtrace - Monitoring for AI Coding Agents](https://news.ycombinator.com/item?id=46425670) | 智能体监控模式 |

---

## 个人贡献者

特别感谢那些其模式和洞见塑造了 Loki Mode 的思想领袖：

| 贡献者 | 贡献 |
|-------------|--------------|
| **Boris Cherny**（Claude Code 创建者） | 自我验证循环（2-3 倍质量提升）、扩展思维模式、"减少提示，更多系统"理念 |
| **Ivan Steshov** | 集中式宪法、智能体谱系追踪、结构化制品作为契约 |
| **Addy Osmani** | Git 检查点系统、规格优先方法、可视化辅助（Mermaid 图表） |
| **Simon Willison** | 子智能体上下文隔离、技能系统、上下文策展模式 |

---

## 生产模式总结

从实践者经验中提炼的关键模式：

| 模式 | 来源 | 实现 |
|---------|--------|----------------|
| 人在环路（HITL） | HN 生产讨论 | 基于置信度的升级阈值 |
| 窄范围（3-5 步） | 多位实践者 | 任务范围约束 |
| 确定性验证 | 生产团队 | 基于规则的外层循环（非 LLM 判断） |
| 上下文策展 | Simon Willison | 手动选择、聚焦上下文 |
| 盲审 + 魔鬼代言人 | CONSENSAGENT | 反谄媚协议 |
| 层次化推理 | DeepMind Gemini | 编排器 + 专业化执行器 |
| 宪法式自我批评 | Anthropic | 基于原则的修订 |
| 辩论验证 | DeepMind | 关键变更验证 |
| 单功能迭代 | Anthropic Harness | 每次迭代单一功能、完整验证 |
| E2E 浏览器测试 | Anthropic Harness | Playwright MCP 用于可视化验证 |

---

## 许可证

本致谢文件记录了影响 Loki Mode 设计的研究和资源。所有引用的作品保留其原始许可证和版权。

Loki Mode 本身以 MIT 许可证发布。

---

*最后更新：v2.35.0*