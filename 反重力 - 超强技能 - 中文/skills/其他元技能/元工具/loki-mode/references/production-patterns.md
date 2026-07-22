# 生产模式参考

来自 Hacker News 讨论和真实世界部署的实践者测试模式。这些模式代表了生产中真正有效的方法，而非理论框架。

---

## 概述

本参考整合了来自以下方面的实战洞察：
- 关于生产中自主智能体的 HN 讨论（2025）
- 使用 LLM 编程的实践者经验
- Simon Willison 的 Superpowers 编码智能体模式
- 多智能体编排的真实世界部署

---

## 生产中真正有效的方法

### 人在回路 (HITL) 是不可妥协的

**关键洞察：** "零家公司没有人在回路"对于面向客户的应用。

```yaml
hitl_patterns:
  always_human:
    - 面向客户的响应
    - 金融交易
    - 安全关键操作
    - 法律/合规决策

  automation_candidates:
    - 内部工具
    - 开发者辅助
    - 数据预处理
    - 代码生成（带审查）

  implementation:
    - 分类层路由到人工 vs 自动化
    - 置信度阈值触发升级
    - 所有自动化决策的审计追踪
```

### 窄范围制胜

**关键洞察：** 成功的智能体在紧密约束的领域内运作。

```yaml
scope_constraints:
  max_steps_before_review: 3-5
  task_characteristics:
    - 具体、明确的目标
    - 预分类的输入
    - 确定性的成功标准
    - 可验证的输出

  successful_domains:
    - 邮件扫描和分类
    - 发票处理
    - 代码重构（有边界）
    - 文档生成
    - 测试编写

  failure_prone_domains:
    - 开放式功能实现
    - 新颖算法设计
    - 安全关键代码
    - 跨系统集成
```

### 基于置信度的路由

**关键洞察：** 将智能体视为预处理器，而非决策者。

```python
def confidence_based_routing(agent_output):
    """
    基于置信度路由，而非能力。
    基于生产实践者模式。
    """
    confidence = agent_output.confidence_score

    if confidence >= 0.95:
        # 高置信度：自动批准并记录
        return AutoApprove(audit_log=True)

    elif confidence >= 0.70:
        # 中等置信度：快速人工审查
        return HumanReview(priority="normal", timeout="1h")

    elif confidence >= 0.40:
        # 低置信度：详细人工审查
        return HumanReview(priority="high", context="full")

    else:
        # 极低置信度：立即升级
        return Escalate(reason="low_confidence", require_senior=True)
```

### 分类先于自动化

**关键洞察：** 在处理前先分离输入。

```yaml
classification_first:
  step_1_classify:
    workable:
      - 清晰的需求
      - 现有的模式
      - 有可用的测试覆盖
    non_workable:
      - 模糊的需求
      - 新颖的架构
      - 缺少依赖
    escalate_immediately:
      - 安全问题
      - 合规要求
      - 面向客户的变更

  step_2_route:
    workable: "自动化流水线"
    non_workable: "人工澄清"
    escalate: "高级审查"
```

### 确定性外循环

**关键洞察：** 用基于规则的验证包装智能体输出。

```python
def deterministic_validation_loop(task, max_attempts=3):
    """
    只在真正存在歧义的地方使用 LLM。
    用确定性规则包装。
    """
    for attempt in range(max_attempts):
        # LLM 处理模糊部分
        output = agent.execute(task)

        # 确定性验证（非 LLM）
        validation_errors = []

        # 规则：必须有测试
        if not output.has_tests:
            validation_errors.append("缺少测试")

        # 规则：必须通过 lint
        lint_result = run_linter(output.code)
        if lint_result.errors:
            validation_errors.append(f"Lint 错误：{lint_result.errors}")

        # 规则：必须编译
        compile_result = compile_code(output.code)
        if not compile_result.success:
            validation_errors.append(f"编译错误：{compile_result.error}")

        # 规则：测试必须通过
        if output.has_tests:
            test_result = run_tests(output.code)
            if not test_result.all_passed:
                validation_errors.append(f"测试失败：{test_result.failures}")

        if not validation_errors:
            return output

        # 将错误反馈以重试
        task = task.with_feedback(validation_errors)

    return FailedResult(reason="超过最大尝试次数")
```

---

## 上下文工程模式

### 上下文筛选优于自动选择

**关键洞察：** 手动选择提供哪些文件和信息。

```yaml
context_curation:
  principles:
    - "少即是多" - 聚焦上下文胜过全面上下文
    - 手动选择优于自动 RAG
    - 积极删除过时信息

  anti_patterns:
    - 将整个代码库倾倒到上下文中
    - 依赖自动上下文选择
    - 无限期积累对话历史

  implementation:
    per_task_context:
      - 2-5 个最相关的文件
      - 具体函数，而非整个模块
      - 仅最近的变更（过去 1-2 天）
      - 清晰的成功标准

    context_budget:
      target: "< 10k tokens 用于上下文"
      reserve: "90% 用于模型推理"
```

### 信息抽象

**关键洞察：** 总结而非喂入完整数据。

```python
def abstract_for_agent(raw_data, task_context):
    """
    设计保留决策相关信息的抽象。
    基于实践者洞察。
    """
    # 错误：喂入 10,000 行数据库
    # raw_data = db.query("SELECT * FROM users")

    # 正确：总结为决策相关信息
    summary = {
        "query_status": "success",
        "total_results": len(raw_data),
        "sample": raw_data[:5],
        "schema": extract_schema(raw_data),
        "statistics": {
            "null_count": count_nulls(raw_data),
            "unique_values": count_uniques(raw_data),
            "date_range": get_date_range(raw_data)
        }
    }

    return summary
```

### 每任务单独对话

**关键洞察：** 新鲜上下文比积累的会话产生更好的结果。

```yaml
conversation_management:
  new_conversation_triggers:
    - 不同领域（后端 -> 前端）
    - 新功能 vs bug 修复
    - 完成主要任务后
    - 当错误积累时（连续 3+ 个）

  preserve_across_sessions:
    - CLAUDE.md / CONTINUITY.md
    - 架构决策
    - 关键约束

  discard_between_sessions:
    - 调试尝试
    - 放弃的方法
    - 中间草稿
```

---

## 技能系统模式

### 按需技能加载

**关键洞察：** 技能保持休眠，直到模型主动寻找它们。

```yaml
skills_architecture:
  core_interaction: "< 2k tokens"
  skill_loading: "通过搜索按需加载"

  implementation:
    skill_discovery:
      - Shell 脚本搜索技能文件
      - 模型按名称请求特定技能
      - 仅在需要时加载技能

    skill_structure:
      name: "unique-skill-name"
      trigger: "激活技能的模式"
      content: "详细指令"
      dependencies: ["other-skills"]

  benefits:
    - 最小基础上下文
    - 可扩展且不臃肿
    - 技能可独立更新
```

### 用于上下文隔离的子智能体

**关键洞察：** 通过隔离上下文嘈杂的子任务来防止大量 token 浪费。

```python
async def context_isolated_search(query, codebase_path):
    """
    使用子智能体进行 grep/搜索以防止上下文污染。
    基于 Simon Willison 的模式。
    """
    # 主智能体保持专注
    # 子智能体处理嘈杂的文件搜索

    search_agent = spawn_subagent(
        role="codebase-searcher",
        context_limit="10k tokens",
        permissions=["read-only"]
    )

    results = await search_agent.execute(
        task=f"查找与以下相关的文件：{query}",
        codebase=codebase_path
    )

    # 仅返回相关路径，而非完整内容
    return FilteredResults(
        paths=results.relevant_files[:10],
        summaries=results.file_summaries,
        confidence=results.relevance_scores
    )
```

---

## 执行前规划

### 显式的计划-然后-编码工作流

**关键洞察：** 让模型在不立即编写代码的情况下阐述详细计划。

```yaml
plan_then_code:
  phase_1_planning:
    outputs:
      - spec.md: "详细需求"
      - todo.md: "标记的任务 [BUG], [FEAT], [REFACTOR]"
      - approach.md: "实现策略"
    constraints:
      - 此阶段无代码
      - 继续前需人工审查
      - 清晰的成功标准

  phase_2_review:
    checks:
      - 计划解决所有需求
      - 方法可行
      - 无缺失依赖
      - 已指定测试

  phase_3_implementation:
    constraints:
      - 严格按计划执行
      - 一次一个任务
      - 每次变更后测试
      - 立即报告偏差
```

---

## 多智能体编排模式

### 事件驱动协调

**关键洞察：** 从同步提示链转向异步、解耦的系统。

```yaml
event_driven_orchestration:
  problems_with_synchronous:
    - 不扩展
    - 将编排与提示逻辑混合
    - 单点故障破坏整个链
    - 无重试/恢复机制

  async_architecture:
    message_queue:
      - 智能体通过事件通信
      - 解耦执行
      - 自然的重试/死信处理

    state_management:
      - 持久化任务状态
      - 检查点/恢复能力
      - 清晰的数据所有权

    error_handling:
      - 每智能体重试策略
      - 熔断器
      - 优雅降级
```

### 策略优先强制

**关键洞察：** 在运行时而非仅训练时治理智能体行为。

```python
class PolicyEngine:
    """
    智能体行为的运行时治理。
    基于自主控制平面模式。
    """

    def __init__(self, policies):
        self.policies = policies

    async def enforce(self, agent_action, context):
        for policy in self.policies:
            result = await policy.evaluate(agent_action, context)

            if result.blocked:
                return BlockedAction(
                    reason=result.reason,
                    policy=policy.name,
                    remediation=result.suggested_action
                )

            if result.modified:
                agent_action = result.modified_action

        return AllowedAction(agent_action)

# 示例策略
policies = [
    NoProductionDataDeletion(),
    NoSecretsInCode(),
    MaxTokenBudget(limit=100000),
    RequireTestsForCode(),
    BlockExternalNetworkCalls(in_sandbox=True)
]
```

### 仿真层

**关键洞察：** 在部署到真实环境之前评估变更。

```yaml
simulation_layer:
  purpose: "在安全环境中测试智能体行为"

  implementation:
    sandbox_environment:
      - 隔离容器
      - 模拟的外部服务
      - 合成数据
      - 完整审计日志

    validation_checks:
      - 先在沙箱中运行测试
      - 将输出与预期比较
      - 检查策略违规
      - 测量资源消耗

    promotion_criteria:
      - 所有测试通过
      - 无策略违规
      - 资源使用在限制内
      - 人工批准（对于敏感变更）
```

---

## 评估与基准测试

### 当前基准测试的问题

**关键洞察：** LLM 作为评判者会产生共同的盲点。

```yaml
benchmark_problems:
  llm_judge_issues:
    - 相同架构 = 相同的失败模式
    - 数学错误被接受为正确
    - "什么都不做"基线 38% 的时间通过

  contamination:
    - 发布的基准测试成为训练目标
    - 过拟合特定数据集
    - 虚高的分数不反映真实性能

  solutions:
    held_back_sets: "90% 公开，10% 私有"
    human_evaluation: "最终发布结果需要人工"
    production_testing: "A/B 测试衡量实际价值"
    objective_outcomes: "具有可验证结果的仿真环境"
```

### 实用评估方法

```python
def evaluate_agent_change(before_agent, after_agent, task_set):
    """
    面向生产的评估。
    基于 HN 实践者建议。
    """
    results = {
        "before": [],
        "after": [],
        "human_preference": []
    }

    for task in task_set:
        # 运行两个智能体
        before_result = before_agent.execute(task)
        after_result = after_agent.execute(task)

        # 客观指标（非 LLM 评判）
        results["before"].append({
            "tests_pass": run_tests(before_result),
            "lint_clean": run_linter(before_result),
            "time_taken": before_result.duration,
            "tokens_used": before_result.tokens
        })

        results["after"].append({
            "tests_pass": run_tests(after_result),
            "lint_clean": run_linter(after_result),
            "time_taken": after_result.duration,
            "tokens_used": after_result.tokens
        })

        # 抽样进行人工审查
        if random.random() < 0.1:  # 10% 抽样
            results["human_preference"].append({
                "task": task,
                "before": before_result,
                "after": after_result,
                "pending_review": True
            })

    return EvaluationReport(results)
```

---

## 成本与 Token 经济学

### 真实世界成本模式

```yaml
cost_patterns:
  claude_code:
    heavy_use: "大型代码库上 $25/1-2 小时"
    api_range: "$1-5/小时，取决于效率"
    max_tier: "$200/月 通常需要 2-3 个订阅"

  token_economics:
    sub_agents_multiply_cost: "每个复制上下文"
    example: "5 任务并行作业 = 每个子任务 50,000+ tokens"

  optimization:
    context_isolation: "对嘈杂任务使用子智能体"
    information_abstraction: "总结，不要倾倒"
    fresh_conversations: "主要任务后重置"
    skill_on_demand: "仅在需要时加载"
```

---

## 来源

**Hacker News 讨论：**
- [自主智能体在生产中真正有效的方法](https://news.ycombinator.com/item?id=44623207)
- [2025 年夏天用 LLM 编程](https://news.ycombinator.com/item?id=44623953)
- [Superpowers：我如何使用编码智能体](https://news.ycombinator.com/item?id=45547344)
- [两周后的 Claude Code 体验](https://news.ycombinator.com/item?id=44596472)
- [AI 智能体基准测试已损坏](https://news.ycombinator.com/item?id=44531697)
- [如何编排多智能体工作流](https://news.ycombinator.com/item?id=45955997)
- [上下文工程 vs 提示工程](https://news.ycombinator.com/item?id=44427757)

**Show HN 项目：**
- [自我进化智能体仓库](https://news.ycombinator.com/item?id=45099226)
- [智能体技能包管理器](https://news.ycombinator.com/item?id=46422264)
- [Wispbit - AI 代码审查智能体](https://news.ycombinator.com/item?id=44722603)
- [Agtrace - AI 编码智能体监控](https://news.ycombinator.com/item?id=46425670)
