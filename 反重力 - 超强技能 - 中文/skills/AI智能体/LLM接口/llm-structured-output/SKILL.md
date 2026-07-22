---
name: llm-structured-output
description: >
  使用 response_format、tool_use 和 schema 约束解码，从 OpenAI、Anthropic 与 Google API 的 LLM 中可靠获取 JSON、枚举和类型化对象。当用户要求从 LLM 提取结构化数据、使用 response_format / json_schema、通过 tool_use 提取数据或修复 LLM 输出格式异常时使用。
risk: safe
source: community
date_added: "2026-03-12"
---

# LLM 结构化输出

## 本技能用途

从 LLM API 响应中提取经过类型化和校验的数据，而不是解析自由文本。本技能覆盖三种主流方式：OpenAI 的 `response_format` 与 JSON Schema、Anthropic 的 `tool_use` 块用于结构化提取，以及 Google Gemini 的 `responseSchema`。你将了解每种方式在何时有效、何时会失败，以及如何围绕 schema 验证失败构建重试逻辑——这类问题在所有生产系统中都不可避免。

## 何时使用本技能

- 用户需要从 LLM 响应中提取结构化数据（JSON 对象、数组、枚举）
- 用户正在构建需要把 LLM 输出直接接入代码的流水线（数据库写入、API 调用、UI 渲染）
- 用户询问 OpenAI 的 `response_format`、`json_mode`、`json_object` 或 `json_schema`
- 用户询问如何使用 Anthropic 的 `tool_use` 或 `tool_result` 块提取数据（而不是实际执行工具）
- 用户询问 `openai` npm 包中与 Zod schema 配合使用的 `zodResponseFormat()`
- 用户需要使用 `instructor`、`marvin` 或手动校验，将 LLM 输出解析为 Pydantic 模型
- 用户收到的 LLM 响应出现 JSON 格式错误、字段缺失或类型错误，需要修复方案
- 用户询问本地模型中的 `controlled generation`、`constrained decoding` 或 `grammar-based sampling`

以下情况不应使用本技能：

- 用户需要自由文本生成（摘要、文章、对话）
- 用户询问将 Zod 用于表单校验或 API 输入校验（应改用 `zod-validation-expert`）
- 用户需要通过提示工程提升文本质量（而不是输出结构）
- 用户想要调用真实外部工具/API（本技能讨论的是将 `tool_use` 作为结构化输出技巧，而不是真正的工具编排）

## 核心工作流

1. 先确定目标 schema。向用户确认需要提取哪些字段，并为每个字段定义类型、是否必填、以及适用的枚举值。没有具体 schema，就不进入下一步。

2. 选择适合提供商的方法：
   - **OpenAI (gpt-4o, gpt-4o-mini)：** 使用 `response_format: { type: "json_schema", json_schema: { ... } }`。这会启用结构化输出，并通过约束解码保证 schema 一致性。
   - **Anthropic (Claude)：** 定义一个工具，把目标 schema 作为 `input_schema`，并设置 `tool_choice: { type: "tool", name: "extract_data" }`。Claude 会在 `tool_use` 内容块中返回结构化数据。
   - **Google (Gemini)：** 使用 `generationConfig.responseSchema` 配合 JSON Schema 对象，并设置 `responseMimeType: "application/json"`。
   - **本地模型 (llama.cpp, vLLM)：** 使用 GBNF 语法或 `--json-schema` 标志，在 token 层面进行约束解码。

3. 用用户的编程语言编写 schema 定义。Python 中使用 Pydantic `BaseModel`；TypeScript 中使用 Zod schema 并配合 `zodResponseFormat()` 转换；原始 API 调用则直接写 JSON Schema。

4. 在 schema 中加入字段级描述。每个字段都应有 `description`，告诉模型应该填什么内容。模型会把这些描述当作隐式提示指令——例如，描述为 `"The user's sentiment as positive, negative, or neutral"` 的字段，通常比没有上下文的 `sentiment: str` 表现更好。

5. 在系统提示中强化结构要求。告诉模型它的工作是数据提取，而不是对话。例如：`"You are a data extraction system. Analyze the input and return the requested fields. Do not include explanations outside the JSON structure."`

6. 如果使用 OpenAI 的 `json_schema` 模式，请在 schema 定义中设置 `"strict": true`。这会激活约束解码，使模型只能输出符合 schema 的 token。缺少 `strict: true` 时，模型仍可能生成无效 JSON。

7. 如果使用 Anthropic 的 `tool_use` 方式，请从 `response.content` 中找到 `type == "tool_use"` 的块，并读取其 `input` 字段以提取结构化数据。不要解析文本块——结构化数据只存在于 `tool_use` 块中。

8. 在应用代码中对响应做 schema 校验。即便使用了约束解码，也应先用 Pydantic 的 `model_validate()` 或 Zod 的 `.parse()` 校验，再把数据传给下游。这能捕获 schema 一致性本身无法发现的语义问题（空字符串、越界数值等）。

9. 为验证失败构建重试循环。验证失败时，把原始输入、失败输出和验证错误一起发回模型，并附上类似指令：`"Your previous output failed validation: {error}. Fix the output."`。重试上限建议设为 3 次。

10. 对每次结构化输出调用做日志记录，至少包含：输入、原始响应、解析结果和所有验证错误。当生产环境的结构化输出失败时，你需要这些日志来判断问题是来自 schema 设计、提示词，还是模型行为退化。

## 示例

### 示例 1：OpenAI 结构化输出配合 Pydantic (Python)

```python
from pydantic import BaseModel, Field
from openai import OpenAI
from enum import Enum

class Sentiment(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class ReviewAnalysis(BaseModel):
    sentiment: Sentiment = Field(description="Overall sentiment of the review")
    key_topics: list[str] = Field(description="Main topics mentioned, max 5")
    purchase_intent: bool = Field(description="Whether the reviewer would buy again")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Model confidence 0-1")

client = OpenAI()
response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract structured review analysis."},
        {"role": "user", "content": "This laptop is amazing. The battery lasts forever and the keyboard feels great. Definitely buying the next version."}
    ],
    response_format=ReviewAnalysis,
)
result = response.choices[0].message.parsed
# result.sentiment == Sentiment.positive
# result.key_topics == ["battery life", "keyboard"]
# result.purchase_intent == True
```

### 示例 2：Anthropic tool_use 结构化提取 (Python)

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a data extraction system. Use the provided tool to return structured data.",
    tools=[{
        "name": "extract_invoice",
        "description": "Extract invoice fields from text",
        "input_schema": {
            "type": "object",
            "properties": {
                "vendor_name": {"type": "string", "description": "Company that issued the invoice"},
                "total_amount": {"type": "number", "description": "Total amount in USD"},
                "line_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "quantity": {"type": "integer"},
                            "unit_price": {"type": "number"}
                        },
                        "required": ["description", "quantity", "unit_price"]
                    }
                }
            },
            "required": ["vendor_name", "total_amount", "line_items"]
        }
    }],
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=[{"role": "user", "content": "Invoice from Acme Corp: 3x Widget A at $10 each, 1x Widget B at $25. Total: $55."}]
)
# Find the tool_use block — do NOT parse text blocks
tool_block = next(b for b in response.content if b.type == "tool_use")
invoice = tool_block.input
# invoice["vendor_name"] == "Acme Corp"
# invoice["total_amount"] == 55.0
```

### 示例 3：TypeScript 配合 Zod + zodResponseFormat

```typescript
import OpenAI from "openai";
import { z } from "zod";
import { zodResponseFormat } from "openai/helpers/zod";

const EventSchema = z.object({
  event_name: z.string().describe("Name of the event"),
  date: z.string().describe("ISO 8601 date string"),
  location: z.string().describe("City and venue"),
  attendee_count: z.number().int().describe("Expected number of attendees"),
  is_virtual: z.boolean().describe("Whether the event is online-only"),
});

const client = new OpenAI();
const completion = await client.beta.chat.completions.parse({
  model: "gpt-4o-2024-08-06",
  messages: [
    { role: "system", content: "Extract event details from the text." },
    { role: "user", content: "Tech Summit 2025 in Austin at the Convention Center on March 15th. Expecting 2000 attendees, in-person only." },
  ],
  response_format: zodResponseFormat(EventSchema, "event_extraction"),
});
const event = completion.choices[0].message.parsed;
// event.event_name === "Tech Summit 2025"
// event.is_virtual === false
```

## 绝对不要做的事

1. **不要在没有 schema 的情况下使用 `response_format: { type: "json_object" }`。** 这是 OpenAI 的旧版 JSON 模式，它只能保证输出是合法 JSON，但不能保证符合 schema。模型可能在你期望 `{"name": str, "age": int}` 时返回 `{"result": "hello"}`。应始终使用 `json_schema` 并提供完整 schema 定义。

2. **不要通过解析 Anthropic 的文本块来获取结构化数据。** 当使用 `tool_choice` 强制结构化输出时，数据位于 `tool_use` 内容块中，而不是任何 `text` 块。解析 `response.content[0].text` 只会得到空字符串或对话式开头，绝不会得到你想要的数据。

3. **不要定义缺少描述的 schema 字段。** 一个名为 `status` 但没有描述的字段，可能指 HTTP 状态、订单状态或评论状态。模型会把字段描述当作提取指令使用，省略描述就相当于删掉了一半提示。

4. **不要在 strict 模式 schema 中使用 `additionalProperties: true`。** OpenAI 的 strict 模式要求 schema 中每个对象都设置 `additionalProperties: false`。如果设置为 `true` 或省略，API 会在请求阶段返回 400 错误，你根本不会拿到响应。

5. **不要把提取指令只放在 user message 中，而忽略 system prompt。** system prompt 对行为指令有更高权重。如果把"提取以下字段"只放在 user message 并与源文本并列，模型需要在指令和数据之间分配注意力。正确做法是：system prompt 定义行为，user message 只提供输入数据。

6. **不要假设结构化输出就等于正确输出。** 约束解码只能保证响应符合 schema 的类型与结构，但无法保证值本身正确。如果源文本存在歧义，模型仍然可能对负面评论返回 `{"sentiment": "positive"}`。因此在 schema 校验之后，还要在应用代码中做语义校验。

7. **不要在未测试的情况下使用递归或深度嵌套 schema。** 递归类型（`$ref` 指向同一定义）和超过 3 层的 schema 会显著增加解码延迟，并提高模型在完成 JSON 结构前触达 `max_tokens` 的概率。应尽量把嵌套 schema 扁平化。

## 边界情况

1. **源文本过长，超出上下文窗口。** 当输入文本过长时，模型可能会截断读取，导致提取结果不完整。应把长文档拆分为多个片段，分别提取，然后在应用代码中合并结果。不要依赖模型在单次调用中处理 50 页文档。

2. **模型返回 `refusal` 而非结构化数据。** OpenAI 的结构化输出在模型认为请求不安全时，可能返回 `refusal` 字段。在访问 `.parsed` 之前，应先检查 `response.choices[0].message.refusal`。如果 `refusal` 不为 `None`，则解析数据将为 `None`，直接访问会抛出错误。

3. **数组字段在源文本有数据时仍返回空。** 当字段描述过于模糊时，模型有时会对数组字段返回 `[]`。解决方法是让描述更具指令性，例如：`"List of all product names mentioned in the text. Return at least one if any product is referenced."`。

4. **枚举值因大小写不匹配导致校验失败。** 如果你定义枚举为 `["Active", "Inactive"]`，但模型返回 `"active"`，校验就会失败。可以在 schema 中统一小写所有枚举值，或在校验前增加归一化步骤。OpenAI 的 strict 模式严格区分大小写；Anthropic 不一定。

5. **结构化输出的流式传输。** OpenAI 支持流式结构化输出，部分 JSON 会分块到达。你不能把中间块直接解析为完整 JSON，应使用 `openai` SDK 的内置部分解析，或缓存到流结束后再解析。Anthropic 的 `tool_use` 块会在单个 `content_block_stop` 事件中完整到达，不需要手动拼接。

## 最佳实践

1. **从能解决问题的最简 schema 开始。** 3-5 个字段的扁平对象通常比 20+ 字段的嵌套 schema 更准确。如果需要复杂数据，可以分两轮提取：先提取顶层实体，再对每个实体发起第二次调用提取详情。

2. **对分类数据使用枚举，而不是自由字符串。** 字段 `mood: str` 可以返回任何内容，而 `mood: Literal["happy", "sad", "neutral", "angry"]` 会把模型限制在固定值内。这样下游解析逻辑可以降到最低。

3. **在生产环境锁定模型版本。** `gpt-4o` 是别名，OpenAI 发布新版本时可能变化。结构化输出行为也可能随版本变化。建议显式使用 `gpt-4o-2024-08-06`，确保 schema + 提示组合在你主动升级前保持稳定。

4. **在部署前用 20+ 条真实输入测试 schema 变更。** 添加字段、修改类型或调整描述，都可能破坏原本能正常工作的提取结果。建议构建包含真实输入和预期输出的测试套件，并在每次 schema 变更后运行。这是结构化输出场景中的单元测试。

5. **在 Pydantic 模型中为可选字段设置 `default` 值。** 如果字段可能在源文本中没有对应数据，应在 Pydantic 中定义为 `Optional[str] = None`，或在 Zod 中使用 `.optional()`。缺少默认值时，模型可能会被迫为无答案字段编造内容。

6. **把提取 schema 和应用 schema 分开。** LLM 提取 schema 应该匹配模型能稳定产出的内容；应用数据库 schema 可能包含计算字段、外键或其他约束。两者之间的映射应在应用代码中完成，而不是要求 LLM 理解你的数据库结构。

## 使用限制

- 仅在任务明确符合上述范围时使用本技能。
- 不要把输出结果当作环境专属校验、测试或专家评审的替代。
- 如果缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。