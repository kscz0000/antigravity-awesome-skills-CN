---
name: bdi-mental-states
description: 当用户要求"建模智能体心智状态"、"实现BDI架构"、"创建信念-愿望-意图模型"、"将RDF转换为信念"、"构建认知智能体"时使用，或提及BDI本体、心智状态建模、理性代理、神经符号AI集成时使用。
risk: unknown
source: community
---

# BDI 心智状态建模

使用形式化 BDI 本体模式将外部 RDF 上下文转换为智能体心智状态（信念、愿望、意图）。本技能使智能体能够通过认知架构对上下文进行推理，支持审慎推理、可解释性以及多智能体系统中的语义互操作性。

## 使用时机

在以下情况激活本技能：
- 将外部 RDF 上下文处理为智能体关于世界状态的信念
- 使用感知、审慎和行动循环建模理性代理
- 通过可追溯的推理链实现可解释性
- 实现 BDI 框架（SEMAS、JADE、JADEX）
- 用形式化认知结构增强 LLM（Logic Augmented Generation）
- 跨多智能体平台协调心智状态
- 追踪信念、愿望和意图的时间演化
- 将动机状态链接到行动计划

## 核心概念

### 心智现实架构

**心智状态（持续体）**：持久的认知属性
- `Belief`：智能体认为关于世界的真实情况
- `Desire`：智能体希望实现的目标
- `Intention`：智能体承诺要达成的事项

**心智过程（历时体）**：修改心智状态的事件
- `BeliefProcess`：从感知中形成/更新信念
- `DesireProcess`：从信念中生成愿望
- `IntentionProcess`：将愿望承诺为可执行的意图

### 认知链模式

```turtle
:Belief_store_open a bdi:Belief ;
    rdfs:comment "Store is open" ;
    bdi:motivates :Desire_buy_groceries .

:Desire_buy_groceries a bdi:Desire ;
    rdfs:comment "I desire to buy groceries" ;
    bdi:isMotivatedBy :Belief_store_open .

:Intention_go_shopping a bdi:Intention ;
    rdfs:comment "I will buy groceries" ;
    bdi:fulfils :Desire_buy_groceries ;
    bdi:isSupportedBy :Belief_store_open ;
    bdi:specifies :Plan_shopping .
```

### 世界状态奠基

心智状态引用环境的结构化配置：

```turtle
:Agent_A a bdi:Agent ;
    bdi:perceives :WorldState_WS1 ;
    bdi:hasMentalState :Belief_B1 .

:WorldState_WS1 a bdi:WorldState ;
    rdfs:comment "Meeting scheduled at 10am in Room 5" ;
    bdi:atTime :TimeInstant_10am .

:Belief_B1 a bdi:Belief ;
    bdi:refersTo :WorldState_WS1 .
```

### 目标导向规划

意图指定通过任务序列来应对目标的计划：

```turtle
:Intention_I1 bdi:specifies :Plan_P1 .

:Plan_P1 a bdi:Plan ;
    bdi:addresses :Goal_G1 ;
    bdi:beginsWith :Task_T1 ;
    bdi:endsWith :Task_T3 .

:Task_T1 bdi:precedes :Task_T2 .
:Task_T2 bdi:precedes :Task_T3 .
```

## T2B2T 范式

三元组-到-信念-到-三元组（Triples-to-Beliefs-to-Triples）实现了 RDF 知识图谱与内部心智状态之间的双向流转：

**阶段1：三元组到信念**
```turtle
# External RDF context triggers belief formation
:WorldState_notification a bdi:WorldState ;
    rdfs:comment "Push notification: Payment request $250" ;
    bdi:triggers :BeliefProcess_BP1 .

:BeliefProcess_BP1 a bdi:BeliefProcess ;
    bdi:generates :Belief_payment_request .
```

**阶段2：信念到三元组**
```turtle
# Mental deliberation produces new RDF output
:Intention_pay a bdi:Intention ;
    bdi:specifies :Plan_payment .

:PlanExecution_PE1 a bdi:PlanExecution ;
    bdi:satisfies :Plan_payment ;
    bdi:bringsAbout :WorldState_payment_complete .
```

## 按层级选择表示法

| C4 层级 | 表示法 | 心智状态表示 |
|----------|----------|----------------------------|
| L1 上下文 | ArchiMate | 智能体边界、外部感知源 |
| L2 容器 | ArchiMate | BDI 推理引擎、信念存储、计划执行器 |
| L3 组件 | UML | 心智状态管理器、过程处理器 |
| L4 代码 | UML/RDF | 信念/愿望/意图类、本体实例 |

## 论证与可解释性

心智实体链接到支撑证据，实现可追溯的推理：

```turtle
:Belief_B1 a bdi:Belief ;
    bdi:isJustifiedBy :Justification_J1 .

:Justification_J1 a bdi:Justification ;
    rdfs:comment "Official announcement received via email" .

:Intention_I1 a bdi:Intention ;
    bdi:isJustifiedBy :Justification_J2 .

:Justification_J2 a bdi:Justification ;
    rdfs:comment "Location precondition satisfied" .
```

## 时间维度

心智状态在有界时间段内持续存在：

```turtle
:Belief_B1 a bdi:Belief ;
    bdi:hasValidity :TimeInterval_TI1 .

:TimeInterval_TI1 a bdi:TimeInterval ;
    bdi:hasStartTime :TimeInstant_9am ;
    bdi:hasEndTime :TimeInstant_11am .
```

查询特定时刻活跃的心智状态：

```sparql
SELECT ?mentalState WHERE {
    ?mentalState bdi:hasValidity ?interval .
    ?interval bdi:hasStartTime ?start ;
              bdi:hasEndTime ?end .
    FILTER(?start <= "2025-01-04T10:00:00"^^xsd:dateTime && 
           ?end >= "2025-01-04T10:00:00"^^xsd:dateTime)
}
```

## 组合式心智实体

复杂心智实体可分解为组成部分，以实现选择性更新：

```turtle
:Belief_meeting a bdi:Belief ;
    rdfs:comment "Meeting at 10am in Room 5" ;
    bdi:hasPart :Belief_meeting_time , :Belief_meeting_location .

# Update only location component
:BeliefProcess_update a bdi:BeliefProcess ;
    bdi:modifies :Belief_meeting_location .
```

## 集成模式

### Logic Augmented Generation (LAG)

用本体约束增强 LLM 输出：

```python
def augment_llm_with_bdi_ontology(prompt, ontology_graph):
    ontology_context = serialize_ontology(ontology_graph, format='turtle')
    augmented_prompt = f"{ontology_context}\n\n{prompt}"
    
    response = llm.generate(augmented_prompt)
    triples = extract_rdf_triples(response)
    
    is_consistent = validate_triples(triples, ontology_graph)
    return triples if is_consistent else retry_with_feedback()
```

### SEMAS 规则转换

将 BDI 本体映射为可执行的产生式规则：

```prolog
% Belief triggers desire formation
[HEAD: belief(agent_a, store_open)] / 
[CONDITIONALS: time(weekday_afternoon)] » 
[TAIL: generate_desire(agent_a, buy_groceries)].

% Desire triggers intention commitment
[HEAD: desire(agent_a, buy_groceries)] / 
[CONDITIONALS: belief(agent_a, has_shopping_list)] » 
[TAIL: commit_intention(agent_a, buy_groceries)].
```

## 指导原则

1. 将世界状态建模为独立于智能体视角的配置，为心智状态提供指称基底。

2. 区分持续体（持久的心智状态）与历时体（时间性的心智过程），与 DOLCE 本体对齐。

3. 将目标视为描述而非心智状态，保持认知层与规划层的分离。

4. 使用 `hasPart` 关系构建部分整体结构，实现选择性信念更新。

5. 通过 `atTime` 或 `hasValidity` 将每个心智实体与时间构造关联。

6. 使用双向属性对（`motivates`/`isMotivatedBy`、`generates`/`isGeneratedBy`）实现灵活查询。

7. 将心智实体链接到 `Justification` 实例，实现可解释性与可信度。

8. 通过以下步骤实现 T2B2T：(1) 将 RDF 转换为信念，(2) 执行 BDI 推理，(3) 将心智状态投影回 RDF。

9. 对心智过程定义存在性限制（例如 `BeliefProcess ⊑ ∃generates.Belief`）。

10. 复用已建立的 ODP（EventCore、Situation、TimeIndexedSituation、BasicPlan、Provenance）以实现互操作性。

## 能力问题

使用以下 SPARQL 查询验证实现：

```sparql
# CQ1: What beliefs motivated formation of a given desire?
SELECT ?belief WHERE {
    :Desire_D1 bdi:isMotivatedBy ?belief .
}

# CQ2: Which desire does a particular intention fulfill?
SELECT ?desire WHERE {
    :Intention_I1 bdi:fulfils ?desire .
}

# CQ3: Which mental process generated a belief?
SELECT ?process WHERE {
    ?process bdi:generates :Belief_B1 .
}

# CQ4: What is the ordered sequence of tasks in a plan?
SELECT ?task ?nextTask WHERE {
    :Plan_P1 bdi:hasComponent ?task .
    OPTIONAL { ?task bdi:precedes ?nextTask }
} ORDER BY ?task
```

## 反模式

1. **混淆心智状态与世界状态**：心智状态引用世界状态，它们本身不是世界状态。

2. **缺少时间边界**：每个心智状态都应有有效区间，以支持历时推理。

3. **扁平信念结构**：对复杂信念应使用 `hasPart` 进行组合式建模。

4. **隐式论证**：始终将心智实体链接到显式的论证实例。

5. **意图直接映射到行动**：意图指定包含任务的计划；行动执行任务。

## 集成

- **RDF 处理**：在解析外部 RDF 上下文后应用，构建认知表示
- **语义推理**：结合本体推理推断隐式的心智状态关系
- **多智能体通信**：与 FIPA ACL 集成，实现跨平台信念共享
- **时间上下文**：与时间推理协调，追踪心智状态演化
- **可解释 AI**：馈入解释系统，追踪从感知经审慎到行动的过程
- **神经符号 AI**：在 LAG 管道中应用，用认知结构约束 LLM 输出

## 参考文献

详见 `references/` 目录：
- `bdi-ontology-core.md` - 核心本体模式与类定义
- `rdf-examples.md` - 完整的 RDF/Turtle 示例
- `sparql-competency.md` - 完整的能力问题 SPARQL 查询
- `framework-integration.md` - SEMAS、JADE、LAG 集成模式

主要来源：
- Zuppiroli et al. "The Belief-Desire-Intention Ontology" (2025)
- Rao & Georgeff "BDI agents: From theory to practice" (1995)
- Bratman "Intention, plans, and practical reason" (1987)

## 限制
- 仅当任务明确匹配上述描述的范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
