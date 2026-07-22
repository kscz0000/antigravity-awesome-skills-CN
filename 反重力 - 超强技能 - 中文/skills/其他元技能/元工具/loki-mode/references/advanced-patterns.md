# 高级智能体模式参考

来自 2025-2026 年文献的研究支持模式，用于增强多智能体编排。

---

## 记忆架构（MIRIX/A-Mem/MemGPT 研究）

### 三层记忆系统

```
+------------------------------------------------------------------+
| 情景记忆（特定事件）                                                |
| - 发生了什么、何时、何地                                            |
| - 带时间戳的完整交互追踪                                            |
| - 存储于：.loki/memory/episodic/                                   |
+------------------------------------------------------------------+
| 语义记忆（泛化知识）                                                |
| - 抽象模式和事实                                                   |
| - 与上下文无关的知识                                               |
| - 存储于：.loki/memory/semantic/                                   |
+------------------------------------------------------------------+
| 程序记忆（习得技能）                                                |
| - 如何做事                                                        |
| - 成功的动作序列                                                   |
| - 存储于：.loki/memory/skills/                                     |
+------------------------------------------------------------------+
```

### 情景到语义的固化

**协议：** 完成任务后，将特定经验固化为通用知识。

```python
def consolidate_memory(task_result):
    """
    将情景（发生了什么）转化为语义（事物如何运作）。
    基于 MemGPT 和 Voyager 模式。
    """
    # 1. 存储原始情景追踪
    episodic_entry = {
        "timestamp": now(),
        "task_id": task_result.id,
        "context": task_result.context,
        "actions": task_result.action_log,
        "outcome": task_result.outcome,
        "errors": task_result.errors
    }
    save_to_episodic(episodic_entry)

    # 2. 提取可泛化模式
    if task_result.success:
        pattern = extract_pattern(task_result)
        if pattern.is_generalizable():
            semantic_entry = {
                "pattern": pattern.description,
                "conditions": pattern.when_to_apply,
                "actions": pattern.steps,
                "confidence": pattern.success_rate,
                "source_episodes": [task_result.id]
            }
            save_to_semantic(semantic_entry)

    # 3. 若有错误，创建反模式
    if task_result.errors:
        anti_pattern = {
            "what_failed": task_result.errors[0].message,
            "why_failed": analyze_root_cause(task_result),
            "prevention": generate_prevention_rule(task_result),
            "severity": classify_severity(task_result.errors)
        }
        save_to_learnings(anti_pattern)
```

### Zettelkasten 启发的笔记链接（A-Mem 模式）

每条记忆笔记都是原子的并链接到相关笔记：

```json
{
  "id": "note-2026-01-06-001",
  "content": "Express 路由处理器在严格模式下需要显式返回类型",
  "type": "semantic",
  "links": [
    {"to": "note-2026-01-05-042", "relation": "derived_from"},
    {"to": "note-2026-01-06-003", "relation": "related_to"}
  ],
  "tags": ["typescript", "express", "strict-mode"],
  "confidence": 0.95,
  "usage_count": 12
}
```

---

## 多智能体反思（MAR 模式）

### 问题：思维退化

单智能体自我批评导致在迭代中重复相同的缺陷推理。

### 解决方案：基于角色的批评者之间的结构化辩论

```
+------------------+     +------------------+     +------------------+
| 实现者            |     | 怀疑者            |     | 倡导者            |
| (创建工作)        | --> | (挑战它)          | --> | (捍卫优点)        |
+------------------+     +------------------+     +------------------+
        |                        |                        |
        v                        v                        v
+------------------------------------------------------------------+
| 综合者                                                             |
| - 权衡所有观点                                                     |
| - 识别有效关切与假阴性                                             |
| - 产出带证据的最终裁决                                             |
+------------------------------------------------------------------+
```

### 反迎合协议（CONSENSAGENT）

**问题：** 智能体相互强化彼此的响应，而不是批判性地参与。

**解决方案：**

```python
def anti_sycophancy_review(implementation, reviewers):
    """
    防止审查者只是互相附和。
    基于 CONSENSAGENT 研究。
    """
    # 1. 独立审查阶段（看不到其他审查）
    independent_reviews = []
    for reviewer in reviewers:
        review = reviewer.review(
            implementation,
            visibility="blind",  # 不能看到其他审查
            prompt_suffix="保持怀疑。列出具体顾虑。"
        )
        independent_reviews.append(review)

    # 2. 辩论阶段（现在揭示审查）
    if has_disagreement(independent_reviews):
        debate_result = structured_debate(
            reviews=independent_reviews,
            max_rounds=2,
            require_evidence=True  # 必须引用具体代码/行
        )
    else:
        # 全部同意 - 运行魔鬼代言人检查
        devil_review = devil_advocate_agent.review(
            implementation,
            prompt="找出其他审查者遗漏的问题。持反对意见。"
        )
        independent_reviews.append(devil_review)

    # 3. 带有效性检查的综合
    return synthesize_with_validity_alignment(independent_reviews)

def synthesize_with_validity_alignment(reviews):
    """
    研究显示有效性对齐推理最能预测改进。
    """
    findings = []
    for review in reviews:
        for concern in review.concerns:
            findings.append({
                "concern": concern.description,
                "evidence": concern.code_reference,  # 必须有证据
                "severity": concern.severity,
                "is_valid": verify_concern_is_actionable(concern)
            })

    # 过滤到仅有效、有证据的顾虑
    return [f for f in findings if f["is_valid"] and f["evidence"]]
```

### 异构团队组成

**研究发现：** 多样化团队比同质化团队表现好 4-6%。

```yaml
review_team:
  - role: "security_analyst"
    model: opus
    expertise: ["OWASP", "auth", "injection"]
    personality: "paranoid"

  - role: "performance_engineer"
    model: sonnet
    expertise: ["complexity", "caching", "async"]
    personality: "pragmatic"

  - role: "maintainability_advocate"
    model: opus
    expertise: ["SOLID", "patterns", "readability"]
    personality: "perfectionist"
```

---

## 分层规划（GoalAct/TMS 模式）

### 带分层执行的全局规划

**研究：** GoalAct 使用此模式实现了 12.22% 的成功率提升。

```
+------------------------------------------------------------------+
| 全局规划器                                                         |
| - 维护总体目标和策略                                               |
| - 根据进度持续更新计划                                             |
| - 分解为高级技能                                                   |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| 高级技能                                                           |
| - searching、coding、testing、writing、deploying                   |
| - 每个技能有定义的进入/退出条件                                     |
| - 降低执行层的规划复杂度                                           |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| 本地执行器                                                         |
| - 在技能上下文中执行特定动作                                       |
| - 向全局规划器报告进度                                             |
| - 若受阻可请求技能升级                                             |
+------------------------------------------------------------------+
```

### 思维管理系统（TMS）

**用于长视野任务：**

```python
class ThoughtManagementSystem:
    """
    基于 TMS 研究用于长视野自主任务。
    启用动态优先级和自适应策略。
    """

    def __init__(self, completion_promise):
        self.goal_hierarchy = self.decompose_goal(completion_promise)
        self.active_thoughts = PriorityQueue()
        self.completed_thoughts = []
        self.blocked_thoughts = []

    def decompose_goal(self, goal):
        """
        带自我批评的分层目标分解。
        """
        # 第 0 层：终极目标
        hierarchy = {"goal": goal, "subgoals": []}

        # 第 1 层：阶段级子目标
        phases = self.identify_phases(goal)
        for phase in phases:
            phase_node = {"goal": phase, "subgoals": []}

            # 第 2 层：任务级子目标
            tasks = self.identify_tasks(phase)
            for task in tasks:
                phase_node["subgoals"].append({"goal": task, "subgoals": []})

            hierarchy["subgoals"].append(phase_node)

        return hierarchy

    def iterate(self):
        """
        带自我批评的单次迭代。
        """
        # 1. 选择最高优先级思维
        thought = self.active_thoughts.pop()

        # 2. 执行思维
        result = self.execute(thought)

        # 3. 自我批评：这是否有进展？
        critique = self.self_critique(thought, result)

        # 4. 根据批评调整策略
        if critique.made_progress:
            self.completed_thoughts.append(thought)
            self.generate_next_thoughts(thought, result)
        elif critique.is_blocked:
            self.blocked_thoughts.append(thought)
            self.escalate_or_decompose(thought)
        else:
            # 无进展，未受阻 - 需要不同方法
            thought.attempts += 1
            thought.alternative_strategy = critique.suggested_alternative
            self.active_thoughts.push(thought)
```

---

## Iter-VF：迭代验证优先

**关键洞察：** 仅验证提取的答案，而非整个思维过程。

```python
def iterative_verify_first(task, max_iterations=3):
    """
    基于 Iter-VF 研究：验证答案，保持马尔可夫过程。
    避免上下文溢出和错误累积。
    """
    for iteration in range(max_iterations):
        # 1. 生成解决方案
        solution = generate_solution(task)

        # 2. 提取具体答案/输出
        answer = extract_answer(solution)

        # 3. 仅验证答案（非推理链）
        verification = verify_answer(
            answer=answer,
            spec=task.spec,
            tests=task.tests
        )

        if verification.passes:
            return solution

        # 4. 马尔可夫重试：仅带错误信息的新上下文
        task = create_fresh_task(
            original=task,
            error=verification.error,
            attempt=iteration + 1
            # 注意：不要包含之前的推理链
        )

    return FailedResult(task, "Max iterations reached")
```

---

## 协作结构

### 何时使用每种结构

| 结构 | 使用时机 | Loki Mode 应用 |
|-----------|----------|----------------------|
| **集中式** | 需要一致性、单一事实来源 | 编排器用于阶段管理 |
| **去中心化** | 需要容错、并行执行 | 智能体群用于实现 |
| **分层式** | 有清晰分解的复杂任务 | 全局规划器 -> 技能 -> 执行器 |

### 竞合模式

**智能体在替代方案上竞争，在共识上合作：**

```python
def coopetition_decision(agents, decision_point):
    """
    竞争阶段：生成多样化替代方案
    合作阶段：就最佳选项达成共识
    """
    # 竞争：每个智能体独立提议解决方案
    proposals = []
    for agent in agents:
        proposal = agent.propose(
            decision_point,
            visibility="blind"  # 不能偷看其他提议
        )
        proposals.append(proposal)

    # 合作：协作评估
    if len(set(p.approach for p in proposals)) == 1:
        # 一致 - 可能是好方案
        return proposals[0]

    # 多种方法 - 结构化辩论
    for proposal in proposals:
        proposal.pros = evaluate_pros(proposal)
        proposal.cons = evaluate_cons(proposal)
        proposal.evidence = gather_evidence(proposal)

    # 带理由要求的投票
    winner = ranked_choice_vote(
        proposals,
        require_justification=True
    )

    return winner
```

---

## 渐进复杂度升级

**从简单开始，仅在需要时升级：**

```
第 1 级：单智能体，直接执行
   |
   +-- 成功？ --> 完成
   |
   +-- 失败？ --> 升级
           |
           v
第 2 级：单智能体 + 自验证循环
   |
   +-- 成功？ --> 完成
   |
   +-- 3 次尝试后失败？ --> 升级
           |
           v
第 3 级：多智能体审查
   |
   +-- 成功？ --> 完成
   |
   +-- 持续问题？ --> 升级
           |
           v
第 4 级：分层规划 + 分解
   |
   +-- 成功？ --> 完成
   |
   +-- 根本性阻碍？ --> 人工升级
```

---

## 关键研究发现总结

### 什么有效

1. **异构团队**比同质化表现好 4-6%
2. **Iter-VF**（仅验证答案）防止上下文溢出
3. **情景到语义固化**实现真正学习
4. **反迎合措施**（盲审、魔鬼代言人）提高准确率 30%+
5. **全局规划**配本地执行提高成功率 12%+

### 什么无效

1. **深度辩论链** - 1-2 轮后收益递减
2. **置信度可见性** - 导致过度自信级联
3. **完整推理链审查** - 导致错误累积
4. **同质化审查团队** - 错失多样化失败模式
5. **过度设计的编排** - 模型升级超越收益

---

## 来源

- [Multi-Agent Collaboration Mechanisms Survey](https://arxiv.org/abs/2501.06322)
- [CONSENSAGENT: Anti-Sycophancy Framework](https://aclanthology.org/2025.findings-acl.1141/)
- [GoalAct: Global Planning + Hierarchical Execution](https://arxiv.org/abs/2504.16563)
- [A-Mem: Agentic Memory System](https://arxiv.org/html/2502.12110v11)
- [Multi-Agent Reflexion (MAR)](https://arxiv.org/html/2512.20845)
- [Iter-VF: Iterative Verification-First](https://arxiv.org/html/2511.21734v1)
- [Awesome Agentic Patterns](https://github.com/nibzard/awesome-agentic-patterns)
