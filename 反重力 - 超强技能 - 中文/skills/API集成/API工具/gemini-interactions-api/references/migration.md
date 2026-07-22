# 迁移参考

如何将现有 Gemini API 代码迁移到 Interactions API，以及在不同模型代次之间升级。涵盖执行迁移操作的 Agent 工作流。

如需查看覆盖所有功能领域（文本生成、多轮对话、流式输出、函数调用、结构化输出、Grounding、多模态）的完整迁移前后代码示例，请拉取完整迁移指南：https://ai.google.dev/gemini-api/docs/migrate-to-interactions.md.txt

## 确认迁移范围

**任何编辑前，请先确认范围。** 如果用户请求未明确指定单个文件、某个具体目录或一份明确文件清单，请先询问，不要开始编辑。

即便是"迁移我的代码"、"升级到 gemini 3"、"切换到 Interactions API"这样的命令式请求，范围仍然不明确。请询问：

> 在开始编辑前，能否确认范围？
> 1. 整个项目
> 2. 某个子目录（例如 `src/`、`api/`）
> 3. 某个具体文件或文件清单

**评估范围规模（大型仓库）。** 提问前先获取每个目录的命中数：

```sh
rg -l "generate_content\|generateContent\|gemini-2\.0\|gemini-1\.5\|gemini-2\.5\|gemini-3-flash-preview\|thinking_budget\|temperature" --type-not md | cut -d/ -f1 | sort | uniq -c | sort -rn
```

在提问中给出分布情况（例如 *"在 3 个目录中共找到 42 处引用：src/（28）、tests/（10）、scripts/（4）。需要迁移哪些？"*）。

**仅在范围已经明确时才可直接进行**：用户已指定具体文件（如"迁移 `app.py`"）、指向某个目录（如"迁移 `src/` 下所有内容"），或是在前序对话中已确认过范围。

## API 迁移：`generateContent` → `Interactions`

从 `generateContent` 迁移到 Interactions API 的核心变化：

| 项目 | `generateContent` | Interactions API |
|------|----------------|-----------------|
| **SDK 方法** | `client.models.generate_content()` | `client.interactions.create()` |
| **响应文本** | `response.text` | `interaction.steps[-1].content[0].text` |
| **多轮对话** | 手动维护历史数组或 `client.chats.create()` | `previous_interaction_id=interaction.id` |
| **流式输出** | `generate_content_stream()` / `:streamGenerateContent` | `stream=True` + `step.delta` 事件 |
| **结构化输出** | 在 `GenerateContentConfig` 内设置 `config.response_format` | 顶层 `response_format` 数组 |
| **函数调用** | `candidates[0].content.parts[0].function_call` | `interaction.steps` 中的 `function_call` 步骤 |
| **搜索 Grounding** | 候选对象上的 `groundingMetadata` | `google_search_call`/`google_search_result` 步骤 + 内联 `annotations` |
| **配置 / 类型** | `types.GenerateContentConfig(...)`、`types.Tool(...)`、`types.Content(...)`、`types.Part.*` | 不再使用。Interactions API 使用纯 Python 字典和直接参数，具体格式请查阅功能文档。 |
| **REST 端点** | `POST /v1beta/models/{model}:generateContent` | `POST /v1beta/interactions` |
| **SDK 包名** | `google-genai` ≥ 1.x 或旧版 `google-generativeai` | `google-genai` ≥ 2.0.0 |

如需查看完整的迁移前后代码示例，请拉取 [迁移指南](https://ai.google.dev/gemini-api/docs/migrate-to-interactions.md.txt)，或阅读 Interactions API 中各功能的文档页面。

## 模型迁移

### 已废弃模型

| 模型 | 状态 | 可直接替换为 |
|-------|--------|-------------------|
| `gemini-2.0-flash` | 已废弃 | `gemini-3.5-flash` |
| `gemini-2.0-flash-lite` | 已废弃 | `gemini-3.1-flash-lite` |
| `gemini-1.5-pro` | 已废弃 | `gemini-3.5-flash` |
| `gemini-1.5-flash` | 已废弃 | `gemini-3.5-flash` |

### 现存旧模型（建议迁移）

| 现有模型 | 推荐目标 | 原因 |
|--------------|-------------------|-----|
| `gemini-2.5-flash-lite` | `gemini-3.1-flash-lite` | 最新 Flash-lite，支持 Interactions API |
| `gemini-2.5-flash` | `gemini-3.5-flash` | 最新 Flash，支持 Interactions API |
| `gemini-2.5-pro` | `gemini-3.1-pro-preview` | 最新 Pro，1M 上下文，支持复杂推理 |
| `gemini-3-flash-preview` | `gemini-3.5-flash` | 最新 Flash，支持 Interactions API |

> **说明：** 在 Interactions API 中，模型升级一般可直接替换 —— 改一下模型字符串并验证即可。破坏性变更发生在 **API 层面**（generateContent → Interactions），而不是模型代次之间。

## 迁移清单

每项都打了标签：**`[BLOCKS]`** 项如果遗漏会导致错误或行为异常；**`[TUNE]`** 项属于质量 / 性能调优。

### API 迁移（generateContent → Interactions）

- [ ] 更新 SDK：`google-genai` ≥ 2.0.0（Python） / `@google/genai` ≥ 2.0.0（JS）
- [ ] 将 `client.models.generate_content()` 替换为 `client.interactions.create()`
- [ ] 将 `response.text` 替换为 `interaction.steps[-1].content[0].text`
- [ ] 将 `response.candidates[0].content.parts` 替换为遍历 `interaction.steps`
- [ ] 将 `client.chats.create()` / 手动历史 替换为 `previous_interaction_id`
- [ ] 移除所有 `types.*` 包装类（`GenerateContentConfig`、`Tool`、`Content`、`Part`） —— Interactions API 使用纯字典，具体格式请查阅功能文档。
- [ ] 将 `response_format` 从 `GenerateContentConfig` 移到顶层参数
- [ ] 将 `generate_content_stream()` 替换为 `stream=True` + 基于 step 的事件处理
- [ ] 更新函数调用：从基于 candidates 的方式改为基于 step 的工具生命周期
- [ ] REST：将端点改为 `/v1beta/interactions`
- [ ] REST：添加 `Api-Revision: 2026-05-20` 请求头（SDK ≥ 2.0.0 会自动设置）
- [ ] 将 `google-generativeai`（Python）替换为 `google-genai` ≥ 2.0.0
- [ ] 将 `@google/generative-ai`（JS）替换为 `@google/genai` ≥ 2.0.0
- [ ] 更新所有 import 语句以匹配新的包名

### 模型字符串更新

- [ ] 将 `gemini-2.0-*` 模型字符串替换为当前等价模型
- [ ] 将 `gemini-1.5-*` 模型字符串替换为当前等价模型
- [ ] 考虑将 `gemini-3-flash-preview` 升级为 `gemini-3.5-flash`
- [ ] 考虑将 `gemini-2.5-flash` 升级为 `gemini-3.5-flash`
- [ ] 考虑将 `gemini-2.5-flash-lite` 升级为 `gemini-3.1-flash-lite`
- [ ] 考虑将 `gemini-2.5-pro` 升级为 `gemini-3.1-pro-preview`

### 迁移到 Gemini 3.5

如果用户要求迁移到 Gemini 3.5，请使用本清单。完整变更说明请拉取 [Gemini 3.5 新特性指南](https://ai.google.dev/gemini-api/docs/interactions/whats-new-gemini-3.5.md.txt)。

- [ ] 将模型名更新为 `gemini-3.5-flash`
- [ ] 从配置中移除 `temperature`、`top_p`、`top_k`
- [ ] 将 `thinking_budget` 替换为 `thinking_level`（`minimal`、`low`、`medium`、`high`）

---

## 验证迁移

更新完成后，运行一次抽检确认 Interactions API 工作正常：

1. 调用一次简单的 `client.interactions.create()`
2. 断言 `interaction.steps` 非空
3. 断言至少有一个 step 的 `type == "model_output"` 且包含非空文本
4. 多轮场景下，验证 `previous_interaction_id` 能在多轮之间保持上下文

如需验证代码片段，请拉取 [迁移指南](https://ai.google.dev/gemini-api/docs/migrate-to-interactions.md.txt)。