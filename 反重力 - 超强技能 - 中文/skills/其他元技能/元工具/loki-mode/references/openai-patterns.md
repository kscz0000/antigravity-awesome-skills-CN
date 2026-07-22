# OpenAI 智能体模式参考

来自 OpenAI 的 Agents SDK、Deep Research 和自主智能体框架的研究支持模式。

---

## 概述

OpenAI 的智能体生态系统为 Loki Mode 提供了四个关键的架构创新：

1. **追踪跨度** - 带跨度类型的分层事件追踪
2. **护栏与触发线** - 带早期终止的输入/输出验证
3. **交接回调** - 智能体转移期间的数据准备
4. **多层降级** - 模型和工作流级别的故障恢复

---

## 追踪跨度架构

### 跨度类型（Agents SDK 模式）

每个操作都包装在类型化跨度中以实现可观测性：

```yaml
span_types:
  agent_span:
    - 包装整个智能体执行
    - 包含：agent_name、instructions_hash、model

  generation_span:
    - 包装 LLM API 调用
    - 包含：model、tokens_in、tokens_out、latency_ms

  function_span:
    - 包装工具/函数调用
    - 包含：function_name、arguments、result、success

  guardrail_span:
    - 包装验证检查
    - 包含：guardrail_name、triggered、blocking

  handoff_span:
    - 包装智能体间转移
    - 包含：from_agent、to_agent、context_passed

  custom_span:
    - 用户定义的操作
    - 包含：operation_name、metadata
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
      "to_agent": "backend-dev",
      "context_passed": ["task_spec", "related_files"]
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
        └── {trace_id}.json # 按日期归档的追踪
```

---

## 护栏与触发线系统

### 输入护栏

在智能体执行**之前**运行以验证用户输入：

```python
@input_guardrail(blocking=True)
async def validate_task_scope(input, context):
    """
    阻断项目范围外的任务。
    基于 OpenAI Agents SDK 模式。
    """
    # 检查任务是否引用项目外的文件
    if references_external_paths(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="任务引用项目根目录外的路径"
        )

    # 检查不允许的操作
    if contains_destructive_operation(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="破坏性操作需要人工批准"
        )

    return GuardrailResult(tripwire_triggered=False)
```

### 输出护栏

在智能体执行**之后**运行以验证结果：

```python
@output_guardrail
async def validate_code_quality(output, context):
    """
    阻断低质量代码输出。
    """
    if output.type == "code":
        issues = run_static_analysis(output.content)
        critical = [i for i in issues if i.severity == "critical"]

        if critical:
            return GuardrailResult(
                tripwire_triggered=True,
                reason=f"发现严重问题：{critical}"
            )

    return GuardrailResult(tripwire_triggered=False)
```

### 执行模式

| 模式 | 行为 | 使用场景 |
|------|----------|----------|
| **阻断式** | 护栏在智能体开始前完成 | 敏感操作、昂贵模型 |
| **并行式** | 护栏与智能体同时运行 | 快速检查、可接受的 token 损失 |

```python
# 阻断模式：防止 token 消耗
@input_guardrail(blocking=True, run_in_parallel=False)
async def expensive_validation(input):
    # 智能体在此完成前不会启动
    pass

# 并行模式：更快但失败时可能浪费 token
@input_guardrail(blocking=True, run_in_parallel=True)
async def fast_validation(input):
    # 与智能体启动同时运行
    pass
```

### 触发线异常

当触发线触发时，执行立即停止：

```python
class InputGuardrailTripwireTriggered(Exception):
    """输入验证失败时抛出。"""
    pass

class OutputGuardrailTripwireTriggered(Exception):
    """输出验证失败时抛出。"""
    pass

# 在智能体循环中：
try:
    result = await run_agent(task)
except InputGuardrailTripwireTriggered as e:
    log_blocked_attempt(e)
    return early_exit(reason=str(e))
except OutputGuardrailTripwireTriggered as e:
    rollback_changes()
    return retry_with_constraints(e.constraints)
```

### 分层防御策略

> "将护栏视为分层防御机制。虽然单个护栏不太可能提供足够的保护，但多个专门的护栏一起使用会创建更有韧性的智能体。" - OpenAI Agents SDK

```yaml
guardrail_layers:
  layer_1_input:
    - scope_validation      # 任务在范围内吗？
    - pii_detection         # 包含敏感数据吗？
    - injection_detection   # 提示注入尝试吗？

  layer_2_pre_execution:
    - cost_estimation       # 会超出预算吗？
    - dependency_check      # 依赖项可用吗？
    - conflict_detection    # 会与进行中的工作冲突吗？

  layer_3_output:
    - static_analysis       # 代码质量问题？
    - secret_detection      # 输出中有秘密吗？
    - spec_compliance       # 匹配 OpenAPI 规范吗？

  layer_4_post_action:
    - test_validation       # 测试通过吗？
    - review_approval       # 审查通过吗？
    - deployment_safety     # 可以安全部署吗？
```

---

## 交接回调

### on_handoff 模式

在智能体之间转移时准备数据：

```python
async def on_handoff_to_backend_dev(handoff_context):
    """
    当编排器交接给 backend-dev 智能体时调用。
    获取接收智能体需要的上下文。
    """
    # 预取相关文件
    relevant_files = await find_related_files(handoff_context.task)

    # 加载架构上下文
    architecture = await read_file(".loki/specs/architecture.md")

    # 获取受影响区域的最近变更
    recent_commits = await git_log(paths=relevant_files, limit=10)

    return HandoffData(
        files=relevant_files,
        architecture=architecture,
        recent_changes=recent_commits,
        constraints=handoff_context.constraints
    )

# 注册回调
handoff(
    to_agent=backend_dev,
    on_handoff=on_handoff_to_backend_dev
)
```

### 交接上下文转移

```json
{
  "handoff_id": "ho_abc123",
  "from_agent": "orchestrator",
  "to_agent": "backend-dev",
  "timestamp": "2026-01-07T10:05:00Z",
  "context": {
    "task_id": "task-001",
    "goal": "实现用户认证端点",
    "constraints": [
      "使用 src/auth/ 中的现有认证模式",
      "保持向后兼容性",
      "添加速率限制"
    ],
    "pre_fetched": {
      "files": ["src/auth/middleware.ts", "src/routes/index.ts"],
      "architecture": "...",
      "recent_changes": [...]
    }
  },
  "return_expected": true,
  "timeout_seconds": 600
}
```

---

## 多层降级系统

### 模型级降级

```python
async def execute_with_model_fallback(task, preferred_model):
    """
    尝试首选模型，失败时降级到替代方案。
    基于 OpenAI 安全模式。
    """
    fallback_chain = {
        "opus": ["sonnet", "haiku"],
        "sonnet": ["haiku", "opus"],
        "haiku": ["sonnet"]
    }

    models_to_try = [preferred_model] + fallback_chain.get(preferred_model, [])

    for model in models_to_try:
        try:
            result = await run_agent(task, model=model)
            if result.success:
                return result
        except RateLimitError:
            log_warning(f"{model} 速率限制，尝试降级")
            continue
        except ModelUnavailableError:
            log_warning(f"{model} 不可用，尝试降级")
            continue

    # 所有模型都失败
    return escalate_to_human(task, reason="所有模型降级都已耗尽")
```

### 工作流级降级

```python
async def execute_with_workflow_fallback(task):
    """
    如果复杂工作流失败，降级到更简单的操作。
    """
    # 首先尝试完整工作流
    try:
        return await full_implementation_workflow(task)
    except WorkflowError as e:
        log_warning(f"完整工作流失败：{e}")

    # 降级到更简单的方法
    try:
        return await simplified_workflow(task)
    except WorkflowError as e:
        log_warning(f"简化工作流失败：{e}")

    # 最后手段：分解并逐个尝试
    try:
        subtasks = decompose_task(task)
        results = []
        for subtask in subtasks:
            result = await execute_single_step(subtask)
            results.append(result)
        return combine_results(results)
    except Exception as e:
        return escalate_to_human(task, reason=f"所有工作流失败：{e}")
```

### 降级决策树

```
任务执行
    |
    +-- 尝试首选方法
    |   |
    |   +-- 成功？ --> 完成
    |   |
    |   +-- 速率限制？ --> 尝试链中的下一个模型
    |   |
    |   +-- 错误？ --> 尝试更简单的工作流
    |
    +-- 所有工作流失败？
    |   |
    |   +-- 分解为子任务
    |   |
    |   +-- 逐个执行
    |
    +-- 仍然失败？
        |
        +-- 升级给人工
        +-- 记录详细失败上下文
        +-- 保存状态以便恢复
```

---

## 基于置信度的人工升级

### 置信度评分

```python
def calculate_confidence(task_result):
    """
    基于多个信号评分置信度 0-1。
    低置信度触发人工审查。
    """
    signals = []

    # 测试覆盖率信号
    if task_result.test_coverage >= 0.9:
        signals.append(1.0)
    elif task_result.test_coverage >= 0.7:
        signals.append(0.7)
    else:
        signals.append(0.3)

    # 审查共识信号
    if task_result.review_unanimous:
        signals.append(1.0)
    elif task_result.review_majority:
        signals.append(0.7)
    else:
        signals.append(0.3)

    # 重试次数信号
    retry_penalty = min(task_result.retry_count * 0.2, 0.8)
    signals.append(1.0 - retry_penalty)

    return sum(signals) / len(signals)

# 升级阈值
CONFIDENCE_THRESHOLD = 0.6

if calculate_confidence(result) < CONFIDENCE_THRESHOLD:
    escalate_to_human(
        task,
        reason="低置信度分数",
        context=result
    )
```

### 自动升级触发器

```yaml
human_escalation_triggers:
  # 基于重试
  - condition: retry_count > 3
    action: pause_and_escalate
    reason: "多次失败表明需求不明确"

  # 基于领域
  - condition: domain in ["payments", "auth", "pii"]
    action: require_approval
    reason: "敏感领域需要人工审查"

  # 基于置信度
  - condition: confidence_score < 0.6
    action: pause_and_escalate
    reason: "对解决方案质量置信度低"

  # 基于时间
  - condition: wall_time > expected_time * 3
    action: pause_and_escalate
    reason: "任务耗时远超预期"

  # 基于成本
  - condition: tokens_used > budget * 0.8
    action: pause_and_escalate
    reason: "接近 token 预算限制"
```

---

## AGENTS.md 集成

### 读取目标项目的 AGENTS.md

```python
async def load_project_context():
    """
    如果存在，从目标项目读取 AGENTS.md。
    基于 OpenAI/AAIF 标准。
    """
    agents_md_locations = [
        "AGENTS.md",
        ".github/AGENTS.md",
        "docs/AGENTS.md"
    ]

    for location in agents_md_locations:
        if await file_exists(location):
            content = await read_file(location)
            return parse_agents_md(content)

    # 未找到 AGENTS.md - 使用默认值
    return default_project_context()

def parse_agents_md(content):
    """
    从 AGENTS.md 提取结构化指导。
    """
    sections = parse_markdown_sections(content)

    return ProjectContext(
        build_commands=sections.get("build", []),
        test_commands=sections.get("test", []),
        code_style=sections.get("code style", {}),
        architecture_notes=sections.get("architecture", ""),
        deployment_notes=sections.get("deployment", ""),
        security_notes=sections.get("security", "")
    )
```

### 上下文优先级

```
1. AGENTS.md（最接近当前文件，monorepo 感知）
2. CLAUDE.md（Claude 特定指令）
3. .loki/CONTINUITY.md（会话状态）
4. 包级文档
5. README.md（通用项目信息）
```

---

## 推理模型指导

### 何时使用扩展思考

基于 OpenAI 的 o3/o4-mini 模式：

```yaml
use_extended_reasoning:
  always:
    - 系统架构设计
    - 安全漏洞分析
    - 复杂调试（多文件、根因不明确）
    - API 设计决策
    - 性能优化策略

  sometimes:
    - 代码审查（仅针对关键/复杂变更）
    - 重构规划（当存在多种方法时）
    - 集成设计（当跨越系统边界时）

  never:
    - 简单 bug 修复
    - 文档更新
    - 单元测试编写
    - 格式化/linting
    - 文件操作
```

### 回溯模式

```python
async def execute_with_backtracking(task, max_backtracks=3):
    """
    允许智能体回溯并尝试不同的方法。
    基于 Deep Research 的自适应规划。
    """
    attempts = []

    for attempt in range(max_backtracks + 1):
        # 考虑之前的失败生成方法
        approach = await plan_approach(
            task,
            failed_approaches=attempts
        )

        result = await execute_approach(approach)

        if result.success:
            return result

        # 记录失败的方法以供学习
        attempts.append({
            "approach": approach,
            "failure_reason": result.error,
            "partial_progress": result.partial_output
        })

        # 回溯：重置到干净状态
        await rollback_to_checkpoint(task.checkpoint_id)

    return FailedResult(
        reason="超过最大回溯次数",
        attempts=attempts
    )
```

---

## 会话状态管理

### 自动状态持久化

```python
class Session:
    """
    自动对话历史和状态管理。
    灵感来自 OpenAI Agents SDK Sessions。
    """

    def __init__(self, session_id):
        self.session_id = session_id
        self.state_file = f".loki/state/sessions/{session_id}.json"
        self.history = []
        self.context = {}

    async def save_state(self):
        state = {
            "session_id": self.session_id,
            "history": self.history,
            "context": self.context,
            "last_updated": now()
        }
        await write_json(self.state_file, state)

    async def load_state(self):
        if await file_exists(self.state_file):
            state = await read_json(self.state_file)
            self.history = state["history"]
            self.context = state["context"]

    async def add_turn(self, role, content, metadata=None):
        self.history.append({
            "role": role,
            "content": content,
            "metadata": metadata,
            "timestamp": now()
        })
        await self.save_state()
```

---

## 来源

**OpenAI 官方：**
- [Agents SDK 文档](https://openai.github.io/openai-agents-python/)
- [构建智能体实用指南](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [构建智能体轨道](https://developers.openai.com/tracks/building-agents/)
- [AGENTS.md 规范](https://agents.md/)

**Deep Research & 推理：**
- [介绍 Deep Research](https://openai.com/index/introducing-deep-research/)
- [Deep Research 系统卡片](https://cdn.openai.com/deep-research-system-card.pdf)
- [介绍 o3 和 o4-mini](https://openai.com/index/introducing-o3-and-o4-mini/)
- [推理最佳实践](https://platform.openai.com/docs/guides/reasoning-best-practices)

**安全与监控：**
- [思维链监控](https://openai.com/index/chain-of-thought-monitoring/)
- [智能体构建者安全](https://platform.openai.com/docs/guides/agent-builder-safety)
- [使用计算机的智能体](https://openai.com/index/computer-using-agent/)

**标准与互操作性：**
- [智能体 AI 基础](https://openai.com/index/agentic-ai-foundation/)
- [OpenAI 开发者 2025](https://developers.openai.com/blog/openai-for-developers-2025/)
