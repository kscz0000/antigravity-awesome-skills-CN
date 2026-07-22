# 工具编排模式参考

受 NVIDIA ToolOrchestra、OpenAI Agents SDK 和多智能体协调研究启发的研究支持模式。

---

## 概述

有效的工具编排需要四项关键创新：
1. **追踪跨度** - 分层事件跟踪（OpenAI SDK 模式）
2. **效率指标** - 跟踪每个任务的计算成本
3. **奖励信号** - 结果、效率和偏好奖励用于学习
4. **动态选择** - 根据任务复杂度调整智能体数量和类型

---

## 追踪跨度架构（OpenAI SDK 模式）

### 跨度类型

每个操作都包装在类型化跨度中以实现可观测性：

```yaml
span_types:
  agent_span:     # 包装整个智能体执行
  generation_span: # 包装 LLM API 调用
  function_span:  # 包装工具/函数调用
  guardrail_span: # 包装验证检查
  handoff_span:   # 包装智能体间转移
  custom_span:    # 用户定义的操作
```

### 分层追踪结构

```json
{
  "trace_id": "trace_abc123def456",
  "workflow_name": "implement_feature",
  "group_id": "session_xyz789",
  "spans": [
    {
      "span_id": "span_001",
      "parent_id": null,
      "type": "agent_span",
      "agent_name": "orchestrator",
      "started_at": "2026-01-07T10:00:00Z",
      "ended_at": "2026-01-07T10:05:00Z",
      "children": ["span_002", "span_003"]
    },
    {
      "span_id": "span_002",
      "parent_id": "span_001",
      "type": "guardrail_span",
      "guardrail_name": "input_validation",
      "triggered": false,
      "blocking": true
    },
    {
      "span_id": "span_003",
      "parent_id": "span_001",
      "type": "handoff_span",
      "from_agent": "orchestrator",
      "to_agent": "backend-dev"
    }
  ]
}
```

### 存储位置

```
.loki/traces/
├── active/
│   └── {trace_id}.json     # 当前运行的追踪
└── completed/
    └── {date}/
        └── {trace_id}.json # 已归档的追踪
```

完整追踪实现请参阅 `references/openai-patterns.md`。

---

## 效率指标系统

### 为什么跟踪效率？

ToolOrchestra 通过显式优化效率，相比 GPT-5 实现了 70% 的成本降低。Loki Mode 应跟踪：

- 每个**任务的 Token 使用量**（输入 + 输出）
- 每个**任务的墙上时钟时间**
- 每个**任务生成的智能体数**
- 成功前的**重试次数**

### 效率跟踪模式

```json
{
  "task_id": "task-2026-01-06-001",
  "correlation_id": "session-abc123",
  "started_at": "2026-01-06T10:00:00Z",
  "completed_at": "2026-01-06T10:05:32Z",
  "metrics": {
    "wall_time_seconds": 332,
    "agents_spawned": 3,
    "total_agent_calls": 7,
    "retry_count": 1,
    "retry_reasons": ["test_failure"],
    "recovery_rate": 1.0,
    "model_usage": {
      "haiku": {"calls": 4, "est_tokens": 12000},
      "sonnet": {"calls": 2, "est_tokens": 8000},
      "opus": {"calls": 1, "est_tokens": 6000}
    }
  },
  "outcome": "success",
  "outcome_reason": "tests_passed_after_fix",
  "efficiency_score": 0.85,
  "efficiency_factors": ["used_haiku_for_tests", "parallel_review"],
  "quality_pillars": {
    "tool_selection_correct": true,
    "tool_reliability_rate": 0.95,
    "memory_retrieval_relevant": true,
    "goal_adherence": 1.0
  }
}
```

**为什么要捕获这些指标？**（基于多智能体研究）

1. **捕获意图，而非仅操作** ([Hashrocket](https://hashrocket.substack.com/p/the-hidden-cost-of-well-fix-it-later))
   - "UX 债务变成数据债务" - 记录操作而不记录意图会创建无用的分析

2. **跟踪恢复率** ([Assessment Framework, arXiv 2512.12791](https://arxiv.org/html/2512.12791v1))
   - `recovery_rate = successful_retries / total_retries`
   - 论文发现"完美的工具排序但仅 33% 的策略遵守率" - 表面指标掩盖了失败

3. **分布式追踪** ([Maxim AI](https://www.getmaxim.ai/articles/best-practices-for-building-production-ready-multi-agent-systems/))
   - `correlation_id`：链接会话中的所有任务以实现端到端追踪
   - 对于调试多智能体协调失败至关重要

4. **工具可靠性与选择分离** ([Stanford/Harvard](https://www.marktechpost.com/2025/12/24/this-ai-paper-from-stanford-and-harvard-explains-why-most-agentic-ai-systems-feel-impressive-in-demos-and-then-completely-fall-apart-in-real-use/))
   - `tool_selection_correct`：我们是否选择了正确的工具？
   - `tool_reliability_rate`：工具是否按预期工作？（即使正确选择，工具也可能失败）
   - 关键洞察："工具使用可靠性"是演示到部署差距的主要原因

5. **超越结果的质量支柱** ([Assessment Framework](https://arxiv.org/html/2512.12791v1))
   - `memory_retrieval_relevant`：情景/语义检索是否有帮助？
   - `goal_adherence`：我们是否保持在任务上？（0.0-1.0 分数）

### 效率分数计算

```python
def calculate_efficiency_score(metrics, task_complexity):
    """
    0-1 分数，越高越高效。
    基于 ToolOrchestra 的效率奖励信号。
    """
    # 按复杂度的基线期望
    baselines = {
        "trivial": {"time": 60, "agents": 1, "retries": 0},
        "simple": {"time": 180, "agents": 2, "retries": 0},
        "moderate": {"time": 600, "agents": 4, "retries": 1},
        "complex": {"time": 1800, "agents": 8, "retries": 2},
        "critical": {"time": 3600, "agents": 12, "retries": 3}
    }

    baseline = baselines[task_complexity]

    # 计算组件分数（1.0 = 达到基线，>1 = 更好，<1 = 更差）
    time_score = min(1.0, baseline["time"] / max(metrics["wall_time_seconds"], 1))
    agent_score = min(1.0, baseline["agents"] / max(metrics["agents_spawned"], 1))
    retry_score = 1.0 - (metrics["retry_count"] / (baseline["retries"] + 3))

    # 加权平均（时间最重要）
    return (time_score * 0.5) + (agent_score * 0.3) + (retry_score * 0.2)
```

### 标准原因代码

使用一致的代码以启用模式分析：

```yaml
outcome_reasons:
  success:
    - tests_passed_first_try
    - tests_passed_after_fix
    - review_approved
    - spec_validated
  partial:
    - tests_partial_pass
    - review_concerns_minor
    - timeout_partial_work
  failure:
    - tests_failed
    - review_blocked
    - dependency_missing
    - timeout_no_progress
    - error_unrecoverable

retry_reasons:
  - test_failure
  - lint_error
  - type_error
  - review_rejection
  - rate_limit
  - timeout
  - dependency_conflict

efficiency_factors:
  positive:
    - used_haiku_for_simple
    - parallel_execution
    - cached_result
    - first_try_success
    - spec_driven
  negative:
    - used_opus_for_simple
    - sequential_when_parallel_possible
    - multiple_retries
    - missing_context
    - unclear_requirements
```

### 存储位置

```
.loki/metrics/
├── efficiency/
│   ├── 2026-01-06.json      # 每日效率日志
│   └── aggregate.json        # 按任务类型的运行平均值
└── rewards/
    ├── outcomes.json         # 任务成功/失败记录
    └── preferences.json      # 用户偏好信号
```

---

## 奖励信号框架

### 三种奖励类型（ToolOrchestra 模式）

```
+------------------------------------------------------------------+
| 1. 结果奖励                                                        |
|    - 任务是否成功？二元 + 质量等级                                   |
|    - 信号：+1.0（成功），0.0（部分），-1.0（失败）                   |
+------------------------------------------------------------------+
| 2. 效率奖励                                                        |
|    - 我们是否明智地使用了资源？                                      |
|    - 信号：0.0 到 1.0 基于效率分数                                   |
+------------------------------------------------------------------+
| 3. 偏好奖励                                                        |
|    - 用户是否喜欢方法/结果？                                         |
|    - 信号：从用户行为推断（接受/拒绝/修改）                           |
+------------------------------------------------------------------+
```

### 结果奖励实现

```python
def calculate_outcome_reward(task_result):
    """
    基于任务完成状态的结果奖励。
    """
    if task_result.status == "completed":
        # 评估完成质量
        if task_result.tests_passed and task_result.review_passed:
            return 1.0  # 完全成功
        elif task_result.tests_passed:
            return 0.7  # 测试通过但审查有顾虑
        else:
            return 0.3  # 已完成但有问题

    elif task_result.status == "partial":
        return 0.0  # 部分完成，无奖励

    else:  # failed
        return -1.0  # 失败的负奖励
```

### 偏好奖励实现

```python
def infer_preference_reward(task_result, user_actions):
    """
    从任务完成后的用户行为推断用户偏好。
    基于隐式反馈模式。
    """
    signals = []

    # 正向信号
    if "commit" in user_actions:
        signals.append(0.8)  # 用户提交了我们的更改
    if "deploy" in user_actions:
        signals.append(1.0)  # 用户部署了我们的更改
    if "no_edits" in user_actions:
        signals.append(0.6)  # 用户没有修改我们的输出

    # 负向信号
    if "revert" in user_actions:
        signals.append(-1.0)  # 用户回滚了我们的更改
    if "manual_fix" in user_actions:
        signals.append(-0.5)  # 用户必须修复我们的工作
    if "retry_different" in user_actions:
        signals.append(-0.3)  # 用户要求不同的方法

    # 中性（无信号）
    if not signals:
        return None

    return sum(signals) / len(signals)
```

### 学习的奖励聚合

```python
def aggregate_rewards(outcome, efficiency, preference):
    """
    将奖励合并为单一学习信号。
    权重基于 ToolOrchestra 发现。
    """
    # 结果最重要（必须成功）
    # 效率次之（成功后优化）
    # 偏好第三（与用户风格对齐）

    weights = {
        "outcome": 0.6,
        "efficiency": 0.25,
        "preference": 0.15
    }

    total = outcome * weights["outcome"]
    total += efficiency * weights["efficiency"]

    if preference is not None:
        total += preference * weights["preference"]
    else:
        # 如果无偏好信号则重新分配权重
        total = total / (1 - weights["preference"])

    return total
```

---

## 动态智能体选择

### 任务复杂度分类

```python
def classify_task_complexity(task):
    """
    分类任务以确定智能体分配。
    基于 ToolOrchestra 的工具选择灵活性。
    """
    complexity_signals = {
        # 文件范围信号
        "single_file": -1,
        "few_files": 0,       # 2-5 个文件
        "many_files": +1,     # 6-20 个文件
        "system_wide": +2,    # 20+ 个文件

        # 变更类型信号
        "typo_fix": -2,
        "bug_fix": 0,
        "feature": +1,
        "refactor": +1,
        "architecture": +2,

        # 领域信号
        "documentation": -1,
        "tests_only": 0,
        "frontend": 0,
        "backend": 0,
        "full_stack": +1,
        "infrastructure": +1,
        "security": +2,
    }

    score = 0
    for signal, weight in complexity_signals.items():
        if task.has_signal(signal):
            score += weight

    # 将分数映射到复杂度级别
    if score <= -2:
        return "trivial"
    elif score <= 0:
        return "simple"
    elif score <= 2:
        return "moderate"
    elif score <= 4:
        return "complex"
    else:
        return "critical"
```

### 按复杂度的智能体分配

```yaml
# 智能体分配策略
# 模型选择：Opus=规划，Sonnet=开发，Haiku=单元测试/监控
complexity_allocations:
  trivial:
    max_agents: 1
    planning: null         # 无需规划
    development: haiku
    testing: haiku
    review: skip           # 简单任务无需审查
    parallel: false

  simple:
    max_agents: 2
    planning: null         # 无需规划
    development: haiku
    testing: haiku
    review: single         # 一次快速审查
    parallel: false

  moderate:
    max_agents: 4
    planning: sonnet       # Sonnet 用于中等规划
    development: sonnet
    testing: haiku         # 单元测试始终用 haiku
    review: standard       # 3 个并行审查者
    parallel: true

  complex:
    max_agents: 8
    planning: opus         # Opus 仅用于复杂规划
    development: sonnet    # Sonnet 用于实现
    testing: haiku         # 单元测试仍用 haiku
    review: deep           # 3 个审查者 + 魔鬼代言人
    parallel: true

  critical:
    max_agents: 12
    planning: opus         # Opus 用于关键规划
    development: sonnet    # Sonnet 用于实现
    testing: sonnet        # 功能/E2E 测试用 sonnet
    review: exhaustive     # 多轮审查
    parallel: true
    human_checkpoint: true # 暂停等待人工审查
```

### 动态选择算法

```python
def select_agents_for_task(task, available_agents):
    """
    根据任务需求动态选择智能体。
    受 ToolOrchestra 可配置工具选择启发。
    """
    complexity = classify_task_complexity(task)
    allocation = COMPLEXITY_ALLOCATIONS[complexity]

    # 1. 识别所需智能体类型
    required_types = identify_required_agents(task)

    # 2. 过滤到所需类型的可用智能体
    candidates = [a for a in available_agents if a.type in required_types]

    # 3. 按过去表现评分候选者
    for agent in candidates:
        agent.selection_score = get_agent_performance_score(
            agent,
            task_type=task.type,
            complexity=complexity
        )

    # 4. 选择前 N 个智能体直到分配限制
    candidates.sort(key=lambda a: a.selection_score, reverse=True)
    selected = candidates[:allocation["max_agents"]]

    # 5. 根据复杂度分配模型
    for agent in selected:
        if agent.role == "reviewer":
            agent.model = "opus"  # 审查始终用 opus
        else:
            agent.model = allocation["model"]

    return selected

def get_agent_performance_score(agent, task_type, complexity):
    """
    基于类似任务的历史表现评分智能体。
    使用之前执行的奖励信号。
    """
    history = load_agent_history(agent.id)

    # 过滤到类似任务
    similar = [h for h in history
               if h.task_type == task_type
               and h.complexity == complexity]

    if not similar:
        return 0.5  # 无历史则中性分数

    # 平均过去奖励
    return sum(h.aggregate_reward for h in similar) / len(similar)
```

---

## 工具使用分析

### 跟踪工具有效性

```json
{
  "tool_analytics": {
    "period": "2026-01-06",
    "by_tool": {
      "Grep": {
        "calls": 142,
        "success_rate": 0.89,
        "avg_result_quality": 0.82,
        "common_patterns": ["error handling", "function def"]
      },
      "Task": {
        "calls": 47,
        "success_rate": 0.94,
        "avg_efficiency": 0.76,
        "by_subagent_type": {
          "general-purpose": {"calls": 35, "success": 0.91},
          "Explore": {"calls": 12, "success": 1.0}
        }
      }
    },
    "insights": [
      "Explore agent 100% success - use more for codebase search",
      "Grep success drops to 0.65 for regex patterns - simplify searches"
    ]
  }
}
```

### 持续改进循环

```
+------------------------------------------------------------------+
| 1. 收集                                                           |
|    记录每个任务：使用的智能体、调用的工具、结果                       |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
| 2. 分析                                                           |
|    每周聚合：什么有效？什么无效？                                    |
|    识别高奖励与低奖励任务中的模式                                    |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
| 3. 适应                                                           |
|    基于分析更新选择算法                                             |
|    将成功模式存储到语义记忆                                         |
+------------------------------------------------------------------+
          |
          v
+------------------------------------------------------------------+
| 4. 验证                                                           |
|    A/B 测试新选择策略                                               |
|    测量效率改进                                                     |
+------------------------------------------------------------------+
          |
          +-----------> 循环回到收集
```

---

## 与 RARV 循环的集成

编排模式在每个阶段与 RARV 集成：

```
推理 (REASON):
├── 检查类似过去任务的效率指标
├── 分类任务复杂度
└── 选择适当的智能体分配

行动 (ACT):
├── 按分配调度智能体
├── 跟踪开始时间和资源使用
└── 记录工具调用和智能体交互

反思 (REFLECT):
├── 计算结果奖励（是否有效？）
├── 计算效率奖励（资源使用）
└── 记录到指标存储

验证 (VERIFY):
├── 运行验证检查
├── 若失败：负结果奖励，带学习重试
├── 若通过：从用户行为推断偏好奖励
└── 更新智能体表现分数
```

---

## 关键指标仪表板

在 `.loki/metrics/dashboard.json` 中跟踪这些指标：

```json
{
  "dashboard": {
    "period": "rolling_7_days",
    "summary": {
      "tasks_completed": 127,
      "success_rate": 0.94,
      "avg_efficiency_score": 0.78,
      "avg_outcome_reward": 0.82,
      "avg_preference_reward": 0.71,
      "avg_recovery_rate": 0.87,
      "avg_goal_adherence": 0.93
    },
    "quality_pillars": {
      "tool_selection_accuracy": 0.91,
      "tool_reliability_rate": 0.93,
      "memory_retrieval_relevance": 0.84,
      "policy_adherence": 0.96
    },
    "trends": {
      "efficiency": "+12% vs previous week",
      "success_rate": "+3% vs previous week",
      "avg_agents_per_task": "-0.8 (improving)",
      "recovery_rate": "+5% vs previous week"
    },
    "top_performing_patterns": [
      "Haiku for unit tests (0.95 success, 0.92 efficiency)",
      "Explore agent for codebase search (1.0 success)",
      "Parallel review with opus (0.98 accuracy)"
    ],
    "areas_for_improvement": [
      "Complex refactors taking 2x expected time",
      "Security review efficiency below baseline",
      "Memory retrieval relevance below 0.85 target"
    ]
  }
}
```

---

## 多维评估

基于 [测量失衡研究 (arXiv 2506.02064)](https://arxiv.org/abs/2506.02064)：

> "技术指标主导评估（83%），而以人为中心（30%）、安全（53%）和经济（30%）仍然边缘化"

**Loki Mode 跟踪四个评估轴：**

| 轴 | 指标 | 当前覆盖 |
|------|---------|------------------|
| **技术** | success_rate, efficiency_score, recovery_rate | 完整 |
| **以人为中心** | preference_reward, goal_adherence | 部分 |
| **安全** | policy_adherence, quality_gates_passed | 完整（通过审查系统） |
| **经济** | model_usage, agents_spawned, wall_time | 完整 |

---

## 来源

**OpenAI Agents SDK:**
- [Agents SDK Documentation](https://openai.github.io/openai-agents-python/) - 核心原语：智能体、交接、护栏、追踪
- [Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) - 编排模式
- [Building Agents Track](https://developers.openai.com/tracks/building-agents/) - 官方开发者指南
- [AGENTS.md Specification](https://agents.md/) - 智能体指令标准
- [Tracing Documentation](https://openai.github.io/openai-agents-python/tracing/) - 跨度类型和可观测性

**效率与编排：**
- [NVIDIA ToolOrchestra](https://github.com/NVlabs/ToolOrchestra) - 带 RL 的多轮工具编排
- [ToolScale Dataset](https://huggingface.co/datasets/nvidia/ToolScale) - 训练数据合成

**评估框架：**
- [Assessment Framework for Agentic AI (arXiv 2512.12791)](https://arxiv.org/html/2512.12791v1) - 四支柱评估模型
- [Measurement Imbalance in Agentic AI (arXiv 2506.02064)](https://arxiv.org/abs/2506.02064) - 多维评估
- [Adaptive Monitoring for Agentic AI (arXiv 2509.00115)](https://arxiv.org/abs/2509.00115) - AMDM 算法

**最佳实践：**
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - 简洁性、透明性、工具工程
- [Maxim AI: Production Multi-Agent Systems](https://www.getmaxim.ai/articles/best-practices-for-building-production-ready-multi-agent-systems/) - 编排模式、分布式追踪
- [UiPath: Agent Builder Best Practices](https://www.uipath.com/blog/ai/agent-builder-best-practices) - 单一职责、评估
- [Stanford/Harvard: Demo-to-Deployment Gap](https://www.marktechpost.com/2025/12/24/this-ai-paper-from-stanford-and-harvard-explains-why-most-agentic-ai-systems-feel-impressive-in-demos-and-then-completely-fall-apart-in-real-use/) - 工具可靠性作为关键失败模式

**安全与推理：**
- [Chain of Thought Monitoring](https://openai.com/index/chain-of-thought-monitoring/) - CoT 可监控性用于安全
- [Agent Builder Safety](https://platform.openai.com/docs/guides/agent-builder-safety) - 人机回路模式
- [Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) - 行业标准（MCP、AGENTS.md、goose）
