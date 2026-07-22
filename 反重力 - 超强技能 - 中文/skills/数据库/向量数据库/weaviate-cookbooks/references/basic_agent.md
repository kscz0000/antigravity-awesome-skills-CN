# 基础 Agent Cookbook

使用 DSPy 构建具备结构化输出的工具调用型 AI Agent。
如需 RAG 工具、记忆与框架集成，请参阅[此处](./agentic_rag.md)。



如需参考的文档：
- DSPy 签名：https://dspy.ai/learn/programming/signatures/
- DSPy 语言模型：https://dspy.ai/learn/programming/language_models/
- LiteLLM 服务商：https://docs.litellm.ai/docs/

## 核心规则

- 使用 `venv` 创建虚拟环境。
- 使用 `uv` 进行 Python 项目与依赖管理。
- 不要手动编写 `pyproject.toml` 或 `uv.lock`；由 `uv` 生成/更新。
- 使用的安装命令为：`uv add dspy python-dotenv`
- 依据用户规格定制本 cookbook；未给出时主动向用户询问细节。

## 环境变量规则

必填：
- 一项 LLM 服务商 API 密钥（例如 `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`GEMINI_API_KEY`）
- `WEAVIATE_URL`
- `WEAVIATE_API_KEY`

可选：
- `environment_requirements.md` 中列出的对应服务商密钥

若用户明确要求构建非 Weaviate 的 Agent，则可以省略 `WEAVIATE_URL` 与 `WEAVIATE_API_KEY`。

## Agent 响应签名

由 LLM 在选择工具时返回的结构化输出定义。

```python
import dspy
from typing import Any, Dict

class AgentResponse(dspy.Signature):

    # Input Fields
    history: dspy.History = dspy.InputField()
    user_prompt: str = dspy.InputField()
    available_tools: str = dspy.InputField()

    # Output Fields
    response: str = dspy.OutputField(
        description="The response to the user's prompt whilst the tool is running. Update the user on the progress of their request (if a tool is picked), or the final response to the user (if no tool is picked)."
    )
    tool: str | None = dspy.OutputField(
        description="The tool that needs to be used. Return None if no tool is needed."
    )
    tool_inputs: Dict[str, Any] | None = dspy.OutputField(
        description=(
            "The inputs for the tool. Return an empty dictionary (still include the field) if no inputs are needed. "
            "The key is the name of the input, the value is the value of the input."
        )
    )
```

可按需扩展 `AgentResponse`：添加 `confidence: float` 用于确定性打分，`requires_clarification: bool` 用于追问确认，或修改 `description` 文案以塑造特定领域下的 Agent 行为。

## Router Agent（单步）

将 Agent 响应封装到一个管理对话历史与工具执行的类中。

```python
from typing import Callable, List, Tuple

class RouterAgent:
    def __init__(self, model: str, tools: List[Callable] = []):
        self.tools: list[Callable] = tools
        self.model = dspy.LM(model)
        self.agent = dspy.ChainOfThought(AgentResponse)
        self.conversation_history = dspy.History(messages=[])

    def add_conversation_history(self, message: str, response: dspy.Prediction):
        self.conversation_history.messages.append({"user_prompt": message, **response})

    def get_tools_and_descriptions(self) -> str:
        return "\n".join(
            [
                f"{tool.__name__}:\nDescription: {tool.__doc__ or ''}\nInputs: { {k: v for k, v in tool.__annotations__.items() if k != 'return'} }"
                for tool in self.tools
            ]
        )

    def get_response(self, user_prompt: str) -> Tuple[str, str | None]:
        result = self.agent(
            history=self.conversation_history,
            user_prompt=user_prompt,
            available_tools=self.get_tools_and_descriptions(),
            lm=self.model,
        )
        self.add_conversation_history(message=user_prompt, response=result)
        if result.tool and result.tool.lower() not in ["null", "none"]:
            tool_function = next(
                (tool for tool in self.tools if tool.__name__ == result.tool), None
            )
            if tool_function is None:
                raise ValueError(f"Tool {result.tool} not found")
            tool_inputs = {k: v for k, v in result.tool_inputs.items() if k != "return"}
            tool_result = tool_function(**tool_inputs)
        else:
            tool_result = None
        return result.response, tool_result
```

用法：

```python
router = RouterAgent(
    model="<model_name>",  # e.g. claude-sonnet-4-5, gpt-5.2, gemini-2.5-pro
    tools=[your_tool_function]
)
response, tool_result = router.get_response("user query here")
```

## 工具设计

工具即 Python 函数。Agent 通过读取 `__name__`、`__doc__`、`__annotations__` 来决定何时调用它们。

```python
def your_tool(param1: str, param2: int) -> str:
    """Clear description of what this tool does and when to use it."""
    # tool logic here
    return "result as string"
```

关键规则：
- 文档字符串直接影响 Agent 何时选择该工具。请尽量具体，例如 "Get current weather conditions for a city" 比 "Get weather" 更好。
- 类型注解用于引导 Agent 传入的参数。对于 `filters: List[Dict]` 等复杂类型，可能需要在文档字符串中补充说明。
- 返回字符串或可序列化为字符串的数据。


## 顺序多步 Agent

对于需要连续多次工具调用的任务，需添加一个 followup 签名并循环执行。

Followup 签名（接收上一步的 `tool_output`）：

```python
class AgentFollowup(dspy.Signature):

    # Input Fields
    history: dspy.History = dspy.InputField()
    user_prompt: str = dspy.InputField()
    tool_output: str = dspy.InputField(description="The output of the previous tool.")
    available_tools: str = dspy.InputField(
        description="The available tools and their descriptions."
    )

    # Output Fields
    response: str = dspy.OutputField(
        description="The response to the user's prompt whilst the tool is running. Update the user on the progress of their request (if a tool is picked), or the final response to the user (if no tool is picked)."
    )
    tool: str | None = dspy.OutputField(
        description="The tool that needs to be used. Return None if no tool is needed."
    )
    tool_inputs: Dict[str, Any] | None = dspy.OutputField(
        description="The inputs for the tool. Return an empty dictionary (still include the field) if no inputs are needed. The key is the name of the input, the value is the value of the input.",
    )
```

改造 `RouterAgent`，使其循环到 Agent 不再请求工具为止：

```python
class RouterAgent:
    def __init__(self, model: str, tools: List[Callable] = []):
        self.tools: list[Callable] = tools
        self.model = dspy.LM(model)
        self.agent = dspy.ChainOfThought(AgentResponse)
        self.followup_agent = dspy.ChainOfThought(AgentFollowup)
        self.conversation_history = dspy.History(messages=[])

    def add_conversation_history(self, message: str, response: dspy.Prediction):
        self.conversation_history.messages.append({"user_prompt": message, **response})

    def get_tools_and_descriptions(self) -> str:
        return "\n".join(
            [
                f"{tool.__name__}:\nDescription: {tool.__doc__ or ''}\nInputs: { {k: v for k, v in tool.__annotations__.items() if k != 'return'} }"
                for tool in self.tools
            ]
        )

    def get_response(self, user_prompt: str) -> str:
        result = self.agent(
            history=self.conversation_history,
            user_prompt=user_prompt,
            available_tools=self.get_tools_and_descriptions(),
            lm=self.model,
        )
        self.add_conversation_history(message=user_prompt, response=result)

        max_iter = 10
        iter = 0

        while result.tool is not None and result.tool.lower() not in ["null", "none"]:
            iter += 1
            if iter > max_iter:
                break

            tool_function = next(
                (tool for tool in self.tools if tool.__name__ == result.tool), None
            )
            if tool_function is None:
                raise ValueError(f"Tool {result.tool} not found")

            tool_inputs = {k: v for k, v in result.tool_inputs.items() if k != "return"}
            tool_result = tool_function(**tool_inputs)

            result = self.followup_agent(
                history=self.conversation_history,
                tool_output=tool_result,
                available_tools=self.get_tools_and_descriptions(),
                lm=self.model,
            )
            self.add_conversation_history(message=tool_result, response=result)

        return result.response
```

`max_iter` 控制强制终止前允许的工具调用次数。复杂多步任务可适当调高，需要限制成本或避免失控循环时可降低。

## 用户特定定制

若未明确说明，请在实施对应策略前就以下要点向用户确认：

**LLM 框架**

可使用 DSPy（兼容所有 LiteLLM 服务商）或 LiteLLM 本身。

- DSPy：https://dspy.ai/learn/programming/language_models/
- LiteLLM：https://docs.litellm.ai/docs/

或者，用户也可以使用单一模型服务商。用户将使用哪家服务商？

- OpenAI（https://platform.openai.com/docs/libraries）
- Anthropic（https://platform.claude.com/docs/）
- Google GenAI（https://ai.google.dev/gemini-api/docs/libraries）
- 其他（如本地托管模型），请自行合理判断

这些可能需要额外的安装步骤。

**模型选型**

用户将使用哪些模型？可考虑混合策略：用能力较强的模型处理主 Agent 路由，用更便宜的模型处理记忆生成等辅助任务。

**工具**

用户需要哪些工具？请列出它们的功能、输入与预期输出。Agent 的能力上限由其工具决定。

**单步 vs 多步**

用户需要每个查询只调用一次工具，还是希望 Agent 按顺序串联多个工具？仅在用例确有需要时才使用多步。

## 故障排查

- DSPy 签名中关于缺失字段的告警：请确保所有输入字段都已传入，或将可选字段显式标注。
- 找不到工具的错误：确认工具函数名与 Agent 输出的名称完全一致。
- Agent 陷入死循环：降低 `max_iter`，或加入更明确的终止条件。
- 其他问题：请查阅官方库/包文档，并充分利用网络搜索进行排查。

## 完成标准

- 编写测试脚本，使用测试数据分别验证每个函数是否独立工作。验证完成后清理临时测试，或使用 pytest 构建正式测试套件（需安装）。
- 用户已完成应用规格的确认。