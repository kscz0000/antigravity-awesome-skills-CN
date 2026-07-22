---
name: multi-agent-patterns
description: 当用户要求"设计多智能体系统"、"实现 Supervisor 模式"、"创建 Swarm 架构"、"协调多个智能体"，或提及多智能体模式、上下文隔离、智能体交接、子智能体、并行智能体执行时使用。
risk: unknown
source: community
---

# 多智能体架构模式

多智能体架构将工作分配到多个语言模型实例上，每个实例拥有独立的上下文窗口。设计得当时，这种分配能实现超越单智能体限制的能力；设计不当时，它会引入协调开销，抵消收益。关键洞察在于：子智能体存在的主要目的是隔离上下文，而非拟人化地划分角色。

## 使用时机

在以下情况下激活此技能：
- 单智能体的上下文限制制约了任务复杂度
- 任务可自然分解为并行子任务
- 不同子任务需要不同的工具集或系统提示词
- 构建需要同时处理多个领域的能力系统
- 将智能体能力扩展到单上下文限制之外
- 设计具有多个专业组件的生产级智能体系统

## 核心概念

多智能体系统通过分布式方式解决单智能体的上下文限制。三种主导模式：Supervisor/Orchestrator 用于集中控制、Peer-to-Peer/Swarm 用于灵活交接、Hierarchical 用于分层抽象。关键设计原则是上下文隔离——子智能体存在的主要目的是划分上下文，而非模拟组织角色。

有效的多智能体系统需要明确的协调协议、避免谄媚的共识机制，以及对瓶颈、发散和错误传播等失败模式的细致关注。

## 详细主题

### 为何使用多智能体架构

**上下文瓶颈**
单智能体在推理能力、上下文管理和工具协调方面面临固有上限。随着任务复杂度增加，上下文窗口被累积的历史记录、检索文档和工具输出填满。性能按照可预测的模式下降：中间遗忘效应、注意力稀缺和上下文污染。

多智能体架构通过将工作分配到多个上下文窗口来解决这些限制。每个智能体在专注于其子任务的干净上下文中运行。结果在协调层聚合，没有任何单个上下文承担全部负担。

**Token 经济现实**
多智能体系统消耗的 Token 远多于单智能体方案。生产数据显示：

| 架构 | Token 倍数 | 使用场景 |
|--------------|------------------|----------|
| 单智能体对话 | 1× 基线 | 简单查询 |
| 单智能体 + 工具 | ~4× 基线 | 工具使用任务 |
| 多智能体系统 | ~15× 基线 | 复杂研究/协调 |

BrowseComp 评估研究发现，三个因素解释了 95% 的性能方差：Token 使用量（占方差的 80%）、工具调用次数和模型选择。这验证了多智能体方法——将工作分配到具有独立上下文窗口的多个智能体上，以增加并行推理能力。

关键的是，升级到更好的模型通常比将 Token 预算翻倍带来更大的性能提升。Claude Sonnet 4.5 比早期 Sonnet 版本翻倍 Token 展现出更大的收益。GPT-5.2 的思考模式同样优于单纯的 Token 增加。这表明模型选择和多智能体架构是互补策略。

**并行化论证**
许多任务包含可并行化的子任务，单智能体必须顺序执行。研究任务可能需要搜索多个独立来源、分析不同文档或比较竞争方案。单智能体会按顺序处理这些任务，每一步都累积上下文。

多智能体架构将每个子任务分配给拥有全新上下文的专用智能体。所有智能体同时工作，然后将结果返回给协调器。总实际耗时接近最长子任务的时长，而非所有子任务之和。

**专业化论证**
不同任务受益于不同的智能体配置：不同的系统提示词、不同的工具集、不同的上下文结构。通用智能体必须在上下文中携带所有可能的配置。专业智能体只携带所需内容。

多智能体架构在不产生组合爆炸的情况下实现专业化。协调器将任务路由到专业智能体；每个智能体使用为其领域优化的精简上下文运行。

### 架构模式

**模式 1：Supervisor/Orchestrator**
Supervisor 模式将中央智能体置于控制地位，委派给专家并综合结果。Supervisor 维护全局状态和轨迹，将用户目标分解为子任务，并路由给适当的工作者。

```
User Query -> Supervisor -> [Specialist, Specialist, Specialist] -> Aggregation -> Final Output
```

使用时机：具有清晰分解的复杂任务、需要跨领域协调的任务、人类监督很重要的任务。

优势：严格控制工作流程、更容易实现人机交互干预、确保遵循预定义计划。

劣势：Supervisor 上下文成为瓶颈、Supervisor 故障级联到所有工作者、"传话游戏"问题——Supervisor 不正确地转述子智能体的响应。

**传话游戏问题与解决方案**
LangGraph 基准测试发现，Supervisor 架构最初比优化版本表现差 50%，原因是"传话游戏"问题——Supervisor 不正确地转述子智能体的响应，导致保真度损失。

修复方案：实现 `forward_message` 工具，允许子智能体直接将响应传递给用户：

```python
def forward_message(message: str, to_user: bool = True):
    """
    Forward sub-agent response directly to user without supervisor synthesis.
    
    Use when:
    - Sub-agent response is final and complete
    - Supervisor synthesis would lose important details
    - Response format must be preserved exactly
    """
    if to_user:
        return {"type": "direct_response", "content": message}
    return {"type": "supervisor_input", "content": message}
```

使用此模式后，Swarm 架构略微优于 Supervisor，因为子智能体直接响应用户，消除了翻译错误。

实现说明：实现直接传递机制，允许子智能体在适当时直接将响应传递给用户，而非通过 Supervisor 综合。

**模式 2：Peer-to-Peer/Swarm**
Peer-to-Peer 模式移除中央控制，允许智能体基于预定义协议直接通信。任何智能体都可以通过显式交接机制将控制权转移给其他智能体。

```python
def transfer_to_agent_b():
    return agent_b  # Handoff via function return

agent_a = Agent(
    name="Agent A",
    functions=[transfer_to_agent_b]
)
```

使用时机：需要灵活探索的任务、严格规划适得其反的任务、具有无法预先分解的涌现需求的任务。

优势：无单点故障、有效扩展广度优先探索、支持涌现式问题解决行为。

劣势：协调复杂度随智能体数量增加、无中央状态维护者存在发散风险、需要健壮的收敛约束。

实现说明：定义带有状态传递的显式交接协议。确保智能体能够将其上下文需求传达给接收智能体。

**模式 3：Hierarchical**
分层结构将智能体组织为抽象层次：战略层、规划层和执行层。战略层智能体定义目标和约束；规划层智能体将目标分解为可执行计划；执行层智能体执行原子任务。

```
Strategy Layer (Goal Definition) -> Planning Layer (Task Decomposition) -> Execution Layer (Atomic Tasks)
```

使用时机：具有清晰层级结构的大型项目、具有管理层的企业工作流程、同时需要高层规划和详细执行的任务。

优势：镜像组织结构、清晰的关注点分离、在不同层级支持不同的上下文结构。

劣势：层间协调开销、战略与执行之间可能出现错位、复杂的错误传播。

### 上下文隔离作为设计原则

多智能体架构的主要目的是上下文隔离。每个子智能体在专注于其子任务的干净上下文窗口中运行，不携带来自其他子任务的累积上下文。

**隔离机制**
完全上下文委派：对于子智能体需要完整理解的复杂任务，规划器共享其完整上下文。子智能体拥有自己的工具和指令，但接收完整上下文以做出决策。

指令传递：对于简单、明确的子任务，规划器通过函数调用创建指令。子智能体仅接收其特定任务所需的指令。

文件系统记忆：对于需要共享状态的复杂任务，智能体读写持久化存储。文件系统作为协调机制，避免共享状态传递导致的上下文膨胀。

**隔离权衡**
完全上下文委派提供最大能力但违背了子智能体的目的。指令传递维持隔离但限制子智能体的灵活性。文件系统记忆在不传递上下文的情况下实现共享状态，但引入延迟和一致性挑战。

正确的选择取决于任务复杂度、协调需求和可接受的延迟。

### 共识与协调

**投票问题**
简单多数投票将弱模型的幻觉视为等同于强模型的推理。若不加干预，多智能体会因固有的同意偏向而在错误前提上达成共识。

**加权投票**
按置信度或专业度加权智能体投票。具有更高置信度或领域专业度的智能体在最终决策中拥有更大权重。

**辩论协议**
辩论协议要求智能体在多轮中相互批评对方的输出。对抗性批评在复杂推理上通常比协作共识产生更高准确性。

**基于触发器的干预**
监控多智能体交互中的特定行为标记。停滞触发器在讨论无进展时激活。谄媚触发器检测智能体在没有独立推理的情况下相互模仿答案的行为。

### 框架考量

不同框架以不同理念实现这些模式。LangGraph 使用基于图的状态机，具有显式的节点和边。AutoGen 使用对话式/事件驱动模式，配合 GroupChat。CrewAI 使用基于角色的流程，配合分层的 Crew 结构。

## 实践指导

### 失败模式与缓解措施

**失败：Supervisor 瓶颈**
Supervisor 从所有工作者累积上下文，容易出现饱和和退化。

缓解：实现输出 Schema 约束，使工作者仅返回精炼摘要。使用检查点持久化 Supervisor 状态，而非携带完整历史。

**失败：协调开销**
智能体通信消耗 Token 并引入延迟。复杂的协调可能抵消并行化收益。

缓解：通过清晰的交接协议最小化通信。尽可能批量处理结果。使用异步通信模式。

**失败：发散**
在没有中央协调的情况下，追求不同目标的智能体可能偏离预期目标。

缓解：为每个智能体定义清晰的目标边界。实现收敛检查以验证向共享目标的进展。对智能体执行设置生存时间限制。

**失败：错误传播**
一个智能体输出中的错误传播到消费该输出的下游智能体。

缓解：在传递给消费者之前验证智能体输出。实现带有断路器的重试逻辑。尽可能使用幂等操作。

## 示例

**示例 1：研究团队架构**
```text
Supervisor
├── Researcher (web search, document retrieval)
├── Analyzer (data analysis, statistics)
├── Fact-checker (verification, validation)
└── Writer (report generation, formatting)
```

**示例 2：交接协议**
```python
def handle_customer_request(request):
    if request.type == "billing":
        return transfer_to(billing_agent)
    elif request.type == "technical":
        return transfer_to(technical_agent)
    elif request.type == "sales":
        return transfer_to(sales_agent)
    else:
        return handle_general(request)
```

## 准则

1. 将上下文隔离设计为多智能体系统的主要收益
2. 基于协调需求选择架构模式，而非组织隐喻
3. 实现带有状态传递的显式交接协议
4. 使用加权投票或辩论协议达成共识
5. 监控 Supervisor 瓶颈并实现检查点
6. 在智能体之间传递前验证输出
7. 设置生存时间限制以防止无限循环
8. 显式测试失败场景

## 集成

此技能基于 context-fundamentals 和 context-degradation 构建。它连接到：

- memory-systems - 跨智能体的共享状态管理
- tool-design - 每个智能体的工具专业化
- context-optimization - 上下文分区策略

## 参考

内部参考：
- Frameworks Reference - 详细框架实现模式

此系列中的相关技能：
- context-fundamentals - 上下文基础
- memory-systems - 跨智能体记忆
- context-optimization - 分区策略

外部资源：
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) - 多智能体模式与状态管理
- [AutoGen Framework](https://microsoft.github.io/autogen/) - GroupChat 与对话模式
- [CrewAI Documentation](https://docs.crewai.com/) - 分层智能体流程
- [Research on Multi-Agent Coordination](https://arxiv.org/abs/2308.00352) - 多智能体系统综述

---

## 技能元数据

**创建日期**: 2025-12-20
**最后更新**: 2025-12-20
**作者**: Agent Skills for Context Engineering Contributors
**版本**: 1.0.0

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
