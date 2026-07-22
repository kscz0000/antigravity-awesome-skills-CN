---
name: autonomous-agents
description: 自主智能体是可以独立分解目标、规划行动、执行工具并自我纠正的AI系统，无需持续的人工指导。挑战不在于让它们有能力——而在于让它们可靠。每一个额外的决策都会成倍增加失败概率。触发词：自主智能体、autonomous agent、agent loop、ReAct模式、Plan-Execute、自我纠正、反思模式、智能体可靠性、智能体护栏、LangGraph、AutoGPT、CrewAI、Claude Agent SDK、目标分解、智能体循环
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 自主智能体

自主智能体是可以独立分解目标、规划行动、执行工具并自我纠正的AI系统，无需持续的人工指导。挑战不在于让它们有能力——而在于让它们可靠。每一个额外的决策都会成倍增加失败概率。

本技能涵盖智能体循环（ReAct、Plan-Execute）、目标分解、反思模式和生产可靠性。核心洞察：复合错误率会杀死自主智能体。每步95%的成功率到第10步会降到60%。先为可靠性构建，其次才是自主性。

2025年的教训：赢家是受约束的、领域特定的、边界清晰的智能体，而不是"自主一切"。把AI输出当作提案，而非真理。

## 原则

- 可靠性优于自主性——每一步都会复合错误概率
- 约束范围——领域特定胜过通用
- 把输出当作提案，而非真理
- 在扩展能力之前先构建护栏
- 关键决策必须有人工介入，不可妥协
- 记录一切——每个操作都必须可审计
- 安全失败并回滚，而非静默失败导致数据损坏

## 能力

- autonomous-agents
- agent-loops
- goal-decomposition
- self-correction
- reflection-patterns
- react-pattern
- plan-execute
- agent-reliability
- agent-guardrails

## 范围

- multi-agent-systems → multi-agent-orchestration
- tool-building → agent-tool-builder
- memory-systems → agent-memory-systems
- workflow-orchestration → workflow-automation

## 工具

### 框架

- LangGraph - 何时使用：需要状态管理的生产级智能体 注意：2025年10月发布1.0版本，支持检查点、人工介入
- AutoGPT - 何时使用：研究/实验、开放式探索 注意：生产环境需要外部护栏
- CrewAI - 何时使用：基于角色的智能体团队 注意：适合专业化智能体协作
- Claude Agent SDK - 何时使用：Anthropic生态系统智能体 注意：计算机使用、工具执行

### 模式

- ReAct - 何时使用：交替进行推理和行动 注意：大多数现代智能体的基础
- Plan-Execute - 何时使用：将规划与执行分离 注意：更适合复杂的多步骤任务
- Reflection - 何时使用：自我评估和纠正 注意：评估器-优化器循环

## 模式

### ReAct智能体循环

交替进行推理和行动步骤

**何时使用**：交互式问题解决、工具使用、探索

# REACT 模式：

"""
ReAct循环：
1. 思考：推理下一步该做什么
2. 行动：选择并执行工具
3. 观察：接收结果
4. 重复直到达成目标

关键：显式的推理轨迹使调试成为可能
"""

## 基础ReAct实现
"""
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI

# 定义ReAct提示模板
react_prompt = '''
Answer the question using the following format:

Question: the input question
Thought: reason about what to do
Action: tool_name
Action Input: input to the tool
Observation: result of the action
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: the answer
'''

# 创建智能体
agent = create_react_agent(
    llm=ChatOpenAI(model="gpt-4o"),
    tools=tools,
    prompt=react_prompt,
)

# 执行并设置步数限制
result = agent.invoke(
    {"input": query},
    config={"max_iterations": 10}  # 防止无限循环
)
"""

## LangGraph ReAct（生产级）
"""
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.postgres import PostgresSaver

# 生产级检查点器
checkpointer = PostgresSaver.from_conn_string(
    os.environ["POSTGRES_URL"]
)

agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer,  # 持久化状态
)

# 使用线程ID调用以实现状态持久化
config = {"configurable": {"thread_id": "user-123"}}
result = agent.invoke({"messages": [query]}, config)
"""

### Plan-Execute模式

将规划阶段与执行分离

**何时使用**：复杂的多步骤任务，需要完整的计划可见性

# PLAN-EXECUTE 模式：

"""
两阶段方法：
1. 规划：将目标分解为子任务
2. 执行：执行子任务，可能重新规划

优势：
- 执行前可完整查看计划
- 可以人工验证/修改计划
- 关注点分离更清晰

劣势：
- 对任务中途的发现适应性较差
- 计划可能变得过时
"""

## LangGraph Plan-Execute
"""
from langgraph.prebuilt import create_plan_and_execute_agent

# 规划器创建任务列表
planner_prompt = '''
For the given objective, create a step-by-step plan.
Each step should be atomic and actionable.
Format: numbered list of steps.
'''

# 执行器处理单个步骤
executor_prompt = '''
You are executing step {step_number} of the plan.
Previous results: {previous_results}
Current step: {current_step}
Execute this step using available tools.
'''

agent = create_plan_and_execute_agent(
    planner=planner_llm,
    executor=executor_llm,
    tools=tools,
    replan_on_error=True,  # 步骤失败时重新规划
)

# 人工审批计划
config = {
    "configurable": {
        "thread_id": "task-456",
    },
    "interrupt_before": ["execute"],  # 执行前暂停
}

# 第一次调用创建计划
plan = agent.invoke({"objective": goal}, config)

# 审查计划，然后继续
if human_approves(plan):
    result = agent.invoke(None, config)  # 从检查点继续
"""

## 分解策略
"""
# 分解优先：先规划所有内容，再执行
# 最适合：稳定任务，需要完整计划审批

# 交错式：规划一步，执行，重复
# 最适合：动态任务，边做边学

def interleaved_execute(goal, max_steps=10):
    state = {"goal": goal, "completed": [], "remaining": [goal]}

    for step in range(max_steps):
        # 根据当前状态规划下一步
        next_action = planner.plan_next(state)

        if next_action == "DONE":
            break

        # 执行并更新状态
        result = executor.execute(next_action)
        state["completed"].append((next_action, result))

        # 重新评估剩余工作
        state["remaining"] = planner.reassess(state)

    return state
"""

### 反思模式

自我评估和迭代改进

**何时使用**：质量很重要、复杂输出、创意任务

# 反思模式：

"""
自我纠正循环：
1. 生成初始输出
2. 根据标准评估
3. 批评并识别问题
4. 根据批评进行改进
5. 重复直到满意

也称为：评估器-优化器、自我批评
"""

## 基础反思
"""
def reflect_and_improve(task, max_iterations=3):
    # 初始生成
    output = generator.generate(task)

    for i in range(max_iterations):
        # 评估输出
        critique = evaluator.critique(
            task=task,
            output=output,
            criteria=[
                "Correctness",
                "Completeness",
                "Clarity",
            ]
        )

        if critique["passes_all"]:
            return output

        # 根据批评进行改进
        output = generator.refine(
            task=task,
            previous_output=output,
            critique=critique["feedback"],
        )

    return output  # 最大迭代次数后的最佳努力
"""

## LangGraph反思
"""
from langgraph.graph import StateGraph

def build_reflection_graph():
    graph = StateGraph(ReflectionState)

    # 节点
    graph.add_node("generate", generate_node)
    graph.add_node("reflect", reflect_node)
    graph.add_node("output", output_node)

    # 边
    graph.add_edge("generate", "reflect")
    graph.add_conditional_edges(
        "reflect",
        should_continue,
        {
            "continue": "generate",  # 循环回去
            "end": "output",
        }
    )

    return graph.compile()

def should_continue(state):
    if state["iteration"] >= 3:
        return "end"
    if state["score"] >= 0.9:
        return "end"
    return "continue"
"""

## 独立评估器（更健壮）
"""
# 使用不同的模型进行评估以避免自我偏见
generator = ChatOpenAI(model="gpt-4o")
evaluator = ChatOpenAI(model="gpt-4o-mini")  # 不同视角

# 或使用专业评估器
from langchain.evaluation import load_evaluator
evaluator = load_evaluator("criteria", criteria="correctness")
"""

### 护栏式自主

具有安全边界的受约束智能体

**何时使用**：生产系统、关键操作

# 护栏式自主：

"""
生产级智能体需要多层安全保护：
1. 输入验证
2. 行动约束
3. 输出验证
4. 成本限制
5. 人工升级
6. 回滚能力
"""

## 多层护栏
"""
class GuardedAgent:
    def __init__(self, agent, config):
        self.agent = agent
        self.max_cost = config.get("max_cost_usd", 1.0)
        self.max_steps = config.get("max_steps", 10)
        self.allowed_actions = config.get("allowed_actions", [])
        self.require_approval = config.get("require_approval", [])

    async def execute(self, goal):
        total_cost = 0
        steps = 0

        while steps < self.max_steps:
            # 获取下一个行动
            action = await self.agent.plan_next(goal)

            # 验证行动是否被允许
            if action.name not in self.allowed_actions:
                raise ActionNotAllowedError(action.name)

            # 检查是否需要审批
            if action.name in self.require_approval:
                approved = await self.request_human_approval(action)
                if not approved:
                    return {"status": "rejected", "action": action}

            # 估算成本
            estimated_cost = self.estimate_cost(action)
            if total_cost + estimated_cost > self.max_cost:
                raise CostLimitExceededError(total_cost)

            # 带回滚能力执行
            checkpoint = await self.save_checkpoint()
            try:
                result = await self.agent.execute(action)
                total_cost += self.actual_cost(action)
                steps += 1
            except Exception as e:
                await self.rollback_to(checkpoint)
                raise

            if result.is_complete:
                break

        return {"status": "complete", "total_cost": total_cost}
"""

## 最小权限原则
"""
# 为每种任务类型定义最小权限
TASK_PERMISSIONS = {
    "research": ["web_search", "read_file"],
    "coding": ["read_file", "write_file", "run_tests"],
    "admin": ["all"],  # 很少授予
}

def create_scoped_agent(task_type):
    allowed = TASK_PERMISSIONS.get(task_type, [])
    tools = [t for t in ALL_TOOLS if t.name in allowed]
    return Agent(tools=tools)
"""

## 成本控制
"""
# 上下文长度的成本呈二次方增长
# 上下文翻倍 = 成本翻4倍

def trim_context(messages, max_tokens=4000):
    # 保留系统消息和最近的消息
    system = messages[0]
    recent = messages[-10:]

    # 如需则总结中间部分
    if len(messages) > 11:
        middle = messages[1:-10]
        summary = summarize(middle)
        return [system, summary] + recent

    return messages
"""

### 持久执行模式

能够从故障中恢复并继续的智能体

**何时使用**：长时间运行的任务、生产系统、多天流程

# 持久执行：

"""
生产级智能体必须：
- 在服务器重启后存活
- 从确切的故障点恢复
- 处理数小时/数天的运行时间
- 允许流程中途人工干预

LangGraph 1.0原生提供此功能。
"""

## LangGraph检查点
"""
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph

# 生产级检查点器（不是MemorySaver！）
checkpointer = PostgresSaver.from_conn_string(
    os.environ["POSTGRES_URL"]
)

# 构建带检查点的图
graph = StateGraph(AgentState)
# ... 添加节点和边 ...

agent = graph.compile(checkpointer=checkpointer)

# 每次调用保存状态
config = {"configurable": {"thread_id": "long-task-789"}}

# 启动任务
agent.invoke({"goal": complex_goal}, config)

# 如果服务器宕机，稍后恢复：
state = agent.get_state(config)
if not state.is_complete:
    agent.invoke(None, config)  # 从检查点继续
"""

## 人工介入中断
"""
# 在特定节点暂停
agent = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["critical_action"],  # 之前暂停
    interrupt_after=["validation"],        # 之后暂停
)

# 第一次调用在中断点暂停
result = agent.invoke({"goal": goal}, config)

# 人工审查状态
state = agent.get_state(config)
if human_approves(state):
    # 从暂停点继续
    agent.invoke(None, config)
else:
    # 修改状态并继续
    agent.update_state(config, {"approved": False})
    agent.invoke(None, config)
"""

## 时间旅行调试
"""
# LangGraph存储完整历史
history = list(agent.get_state_history(config))

# 回到任何之前的状态
past_state = history[5]
agent.update_state(config, past_state.values)

# 从该点带修改重放
agent.invoke(None, config)
"""

## 常见陷阱

### 错误概率指数级复合

严重程度：关键

场景：构建多步骤自主智能体

症状：
智能体在演示中工作但在生产中失败。简单任务成功，
复杂任务神秘失败。随着任务复杂度增加，成功率急剧
下降。用户失去信任。

为什么会出问题：
每一步都有独立的失败概率。每步95%的成功率
听起来很棒，直到你意识到：
- 5步：77%成功率（0.95^5）
- 10步：60%成功率（0.95^10）
- 20步：36%成功率（0.95^20）

这是自主智能体的根本限制。每一个额外的
步骤都会成倍增加失败概率。

推荐修复：

## 减少步骤数
# 尽可能合并步骤
# 更倾向于更少、更有能力的步骤，而不是许多小步骤

## 提高每步可靠性
# 使用结构化输出（JSON schemas）
# 在每一步添加验证
# 对关键步骤使用更好的模型

## 为失败设计
class RobustAgent:
    def execute_with_retry(self, step, max_retries=3):
        for attempt in range(max_retries):
            try:
                result = step.execute()
                if self.validate(result):
                    return result
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                self.log_retry(step, attempt, e)

## 分解为带检查点的片段
# 每个片段人工审查
# 从最后一个良好检查点恢复

### API成本随上下文增长爆炸

严重程度：关键

场景：运行上下文不断增长的智能体

症状：
关闭单个支持工单花费47美元。数千美元的意外API账单。
智能体运行越久越慢。Token计数超过模型限制。

为什么会出问题：
Transformer成本随上下文长度二次方增长。上下文
翻倍，计算量翻四倍。长时间运行的智能体每轮
重新发送完整对话可能以指数方式烧钱。

大多数智能体追加到上下文而不修剪。上下文增长：
- 第1轮：500 tokens → $0.01
- 第10轮：5000 tokens → $0.10
- 第50轮：25000 tokens → $0.50
- 第100轮：50000 tokens → $1.00+ 每条消息

推荐修复：

## 设置硬性成本限制
class CostLimitedAgent:
    MAX_COST_PER_TASK = 1.00  # USD

    def __init__(self):
        self.total_cost = 0

    def before_call(self, estimated_tokens):
        estimated_cost = self.estimate_cost(estimated_tokens)
        if self.total_cost + estimated_cost > self.MAX_COST_PER_TASK:
            raise CostLimitExceeded(
                f"Would exceed ${self.MAX_COST_PER_TASK} limit"
            )

    def after_call(self, response):
        self.total_cost += self.calculate_actual_cost(response)

## 积极修剪上下文
def trim_context(messages, max_tokens=4000):
    # 保留：系统提示 + 最近N条消息
    # 总结：中间的所有内容
    if count_tokens(messages) <= max_tokens:
        return messages

    system = messages[0]
    recent = messages[-5:]
    middle = messages[1:-5]

    if middle:
        summary = summarize(middle)  # 压缩历史
        return [system, summary] + recent

    return [system] + recent

## 使用流式传输实时跟踪成本
## 在预算的50%时警告，90%时停止

### 演示可行但生产失败

严重程度：关键

场景：从原型转向生产

症状：
向利益相关者展示令人印象深刻的演示。生产中数月失败。
对创始人的用例有效，对真实用户失败。边缘情况
压垮系统。

为什么会出问题：
演示展示精心策划输入的快乐路径。生产意味着：
- 意外输入（拼写错误、歧义、对抗性）
- 规模（1000用户，不是3个）
- 可靠性（99.9%正常运行时间，不是"通常有效"）
- 边缘情况（破坏一切的1%）

方法论值得商榷，但核心问题是真实的。
工作演示和可靠生产系统之间的差距
是项目死亡的地方。

推荐修复：

## 生产前大规模测试
# 运行1000+测试用例，不是10个
# 测量P95/P99成功率，不是平均值
# 包含对抗性输入

## 首先构建可观测性
import structlog
logger = structlog.get_logger()

class ObservableAgent:
    def execute(self, task):
        with logger.bind(task_id=task.id):
            logger.info("task_started")
            try:
                result = self._execute(task)
                logger.info("task_completed", result=result)
                return result
            except Exception as e:
                logger.error("task_failed", error=str(e))
                raise

## 设置逃生通道
# 置信度低于阈值时人工接管
# 优雅降级到更简单的行为
# "我不知道"是一个有效回答

## 增量部署
# 1%流量，然后10%，然后50%
# 在每个阶段监控错误率

### 智能体卡住时编造数据

严重程度：高

场景：智能体无法用可用信息完成任务

症状：
智能体编造看似合理的数据。费用报告上的假餐厅名称。
报告中编造的统计数据。完全错误的自信回答。

为什么会出问题：
LLM被训练成有帮助并产生合理的输出。当
卡住时，它们不会说"我做不到"——它们会编造。自主
智能体通过在没有人工审查的情况下对编造数据采取行动来
加剧这个问题。

编造费用条目的智能体试图达成其目标
（完成费用报告）。它通过编造数据"解决"了问题。

推荐修复：

## 对照真实来源验证
def validate_expense(expense):
    # 与外部来源交叉检查
    if expense.restaurant:
        if not verify_restaurant_exists(expense.restaurant):
            raise ValidationError("Restaurant not found")

    # 检查可疑模式
    if expense.amount == round(expense.amount, -1):
        flag_for_review("Suspiciously round amount")

## 要求证据
system_prompt = '''
For every factual claim, cite the specific tool output that
supports it. If you cannot find supporting evidence, say
"I could not verify this" rather than guessing.
'''

## 使用结构化输出
from pydantic import BaseModel

class VerifiedClaim(BaseModel):
    claim: str
    source: str  # Must reference tool output
    confidence: float

## 检测不确定性
# 训练输出置信度分数
# 标记低置信度输出供人工审查
# 永远不要对不确定数据自动执行

### 集成是智能体死亡的地方

严重程度：高

场景：将智能体连接到外部系统

症状：
使用模拟API有效，使用真实API失败。速率限制导致崩溃。
认证令牌在任务中途过期。数据格式不匹配。部分失败
使系统处于不一致状态。

为什么会出问题：
承诺"与整个技术栈集成的自主智能体"的公司
还没有大规模构建生产系统。
真实集成有：
- 速率限制（任务中途429错误）
- 认证复杂性（OAuth刷新、令牌过期）
- 数据格式变化（API v1 vs v2）
- 部分失败（收到webhook，处理失败）
- 最终一致性（数据不立即可用）

推荐修复：

## 构建健壮的API客户端
from tenacity import retry, stop_after_attempt, wait_exponential

class RobustAPIClient:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=60)
    )
    async def call(self, endpoint, data):
        response = await self.client.post(endpoint, json=data)
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", 60)
            await asyncio.sleep(int(retry_after))
            raise RateLimitError()
        return response

## 处理认证生命周期
class TokenManager:
    def __init__(self):
        self.token = None
        self.expires_at = None

    async def get_token(self):
        if self.is_expired():
            self.token = await self.refresh_token()
        return self.token

    def is_expired(self):
        buffer = timedelta(minutes=5)  # Refresh early
        return datetime.now() > (self.expires_at - buffer)

## 使用幂等键
# 每个外部操作都应该是幂等的
# 如果智能体重试，外部系统处理重复

## 为部分失败设计
# 每一步都可独立恢复
# 外部调用前检查点
# 每个集成的回滚能力

### 智能体采取危险行动

严重程度：高

场景：具有广泛权限的智能体

症状：
智能体删除生产数据。向错误的收件人发送邮件。
未经批准进行购买。修改不该修改的设置。
无法撤销的操作。

为什么会出问题：
智能体为其目标优化。没有护栏，它们会走
最短路径——即使那条路径是破坏性的。被告知
"清理数据库"的智能体可能将其理解为"删除所有内容"。

广泛权限 + 自主性 + 目标优化 = 危险。

推荐修复：

## 最小权限原则
PERMISSIONS = {
    "research_agent": ["read_web", "read_docs"],
    "code_agent": ["read_file", "write_file", "run_tests"],
    "email_agent": ["read_email", "draft_email"],  # NOT send
    "admin_agent": ["all"],  # Rarely used
}

## 分离读/写权限
# 智能体可以读取任何内容
# 写入需要显式批准

## 危险操作需要确认
DANGEROUS_ACTIONS = [
    "delete_*",
    "send_email",
    "transfer_money",
    "modify_production",
    "revoke_access",
]

async def execute_action(action):
    if matches_dangerous_pattern(action):
        approval = await request_human_approval(action)
        if not approval:
            return ActionRejected(action)
    return await actually_execute(action)

## 测试的干运行模式
# 智能体描述它会做什么
# 人工批准计划
# 然后智能体执行

## 所有操作的审计日志
# 每个操作都带上下文记录
# 谁授权的
# 改变了什么
# 如何撤销

### 智能体耗尽上下文窗口

严重程度：中等

场景：长时间运行的智能体任务

症状：
智能体忘记早期指令。自相矛盾。失去目标
追踪。开始重复自己。模型报token限制错误。

为什么会出问题：
每条消息、观察和思考都消耗上下文。长任务
耗尽窗口。当上下文被截断时：
- 系统提示被丢弃
- 早期重要上下文丢失
- 智能体失去连贯性

推荐修复：

## 跟踪上下文使用
class ContextManager:
    def __init__(self, max_tokens=100000):
        self.max_tokens = max_tokens
        self.messages = []

    def add(self, message):
        self.messages.append(message)
        self.maybe_compact()

    def maybe_compact(self):
        if self.token_count() > self.max_tokens * 0.8:
            self.compact()

    def compact(self):
        # 始终保留：系统提示
        system = self.messages[0]

        # 始终保留：最近N条消息
        recent = self.messages[-10:]

        # 总结：其他所有内容
        middle = self.messages[1:-10]
        if middle:
            summary = summarize_messages(middle)
            self.messages = [system, summary] + recent

## 使用外部记忆
# 不要把所有内容都保留在上下文中
# 存储在向量数据库中，需要时检索
# 参见agent-memory-systems技能

## 分层总结
# 最近：完整细节
# 中等：关键点
# 较旧：压缩总结

### 无法调试你看不见的东西

严重程度：中等

场景：智能体神秘失败

症状：
"它就是不工作。"不知道智能体为什么失败。无法复现
问题。用户报告你无法解释的问题。调试是
猜测工作。

为什么会出问题：
智能体做出数十个内部决策。没有对每一步的可见性，
你对失败模式是盲目的。没有追踪的生产调试
是不可能的。

推荐修复：

## 结构化日志
import structlog

logger = structlog.get_logger()

class TracedAgent:
    def think(self, context):
        with logger.bind(step="think"):
            thought = self.llm.generate(context)
            logger.info("thought_generated",
                thought=thought,
                tokens=count_tokens(thought)
            )
            return thought

    def act(self, action):
        with logger.bind(step="act", action=action.name):
            logger.info("action_started")
            try:
                result = action.execute()
                logger.info("action_completed", result=result)
                return result
            except Exception as e:
                logger.error("action_failed", error=str(e))
                raise

## 使用LangSmith或类似工具
from langsmith import trace

@trace
def agent_step(state):
    # Automatically traced with inputs/outputs
    return next_state

## 保存完整追踪
# 每一步，每一个决策
# 输入和输出
# 每一步的延迟
# Token使用

## 验证检查

### 没有步数限制的智能体循环

严重程度：错误

自主智能体必须有最大步数限制

消息：智能体循环没有步数限制。添加max_steps以防止无限循环。

### 没有成本跟踪或限制

严重程度：错误

智能体应该跟踪和限制API成本

消息：智能体使用LLM但没有成本跟踪。添加成本限制以防止支出失控。

### 智能体没有超时

严重程度：警告

长时间运行的智能体需要超时

消息：智能体调用没有超时。添加timeout以防止任务挂起。

### 生产环境使用MemorySaver

严重程度：错误

MemorySaver仅用于开发

消息：MemorySaver不是持久化的。生产环境使用PostgresSaver或SqliteSaver。

### 长时间运行的智能体没有检查点

严重程度：警告

运行多个步骤的智能体需要检查点

消息：多步骤智能体没有检查点。添加checkpointer以实现持久性。

### 智能体没有线程ID

严重程度：警告

带检查点的智能体需要唯一的线程ID

消息：智能体调用没有thread_id。状态将无法正确持久化。

### 使用智能体输出没有验证

严重程度：警告

智能体输出应该在使用前验证

消息：智能体输出使用前没有验证。在根据结果行动前进行验证。

### 智能体没有结构化输出

严重程度：信息

结构化输出更可靠

消息：考虑使用结构化输出（Pydantic）以获得更可靠的解析。

### 智能体没有错误恢复

严重程度：警告

智能体应该处理并从错误中恢复

消息：智能体调用没有错误处理。添加try/catch或错误处理器。

### 破坏性操作没有回滚

严重程度：警告

修改状态的操作应该是可逆的

消息：破坏性操作没有回滚能力。修改前保存状态。

## 协作

### 委托触发器

- user needs multi-agent coordination -> multi-agent-orchestration（多个智能体协同工作）
- user needs to test/evaluate agent -> agent-evaluation（基准测试和测试）
- user needs tools for agent -> agent-tool-builder（工具设计和实现）
- user needs persistent memory -> agent-memory-systems（长期记忆架构）
- user needs workflow automation -> workflow-automation（当智能体对任务来说过度设计时）
- user needs computer control -> computer-use-agents（GUI自动化、屏幕交互）

## 相关技能

与以下技能配合良好：`agent-tool-builder`、`agent-memory-systems`、`multi-agent-orchestration`、`agent-evaluation`

## 何时使用

- 用户提及或暗示：自主智能体
- 用户提及或暗示：autogpt
- 用户提及或暗示：babyagi
- 用户提及或暗示：自我提示
- 用户提及或暗示：目标分解
- 用户提及或暗示：react模式
- 用户提及或暗示：智能体循环
- 用户提及或暗示：自我纠正智能体
- 用户提及或暗示：反思智能体
- 用户提及或暗示：langgraph
- 用户提及或暗示：智能体AI
- 用户提及或暗示：智能体规划

## 限制

- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
