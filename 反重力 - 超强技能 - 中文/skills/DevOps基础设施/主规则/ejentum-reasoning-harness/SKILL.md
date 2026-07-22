---
name: ejentum-reasoning-harness
description: "MCP 服务器，暴露四种认知模式（reasoning、code、anti-deception、memory）。每次调用都返回一个工程化脚手架（失败模式、操作流程、抑制向量、证伪测试），供智能体在生成前吸收。触发词：reasoning harness、cognitive harness、anti-deception、scaffold、suppression vectors、falsification test、sycophancy、hallucination drift、attention decay、reasoning decay、long-horizon agent。"
risk: critical
source: community
source_repo: ejentum/ejentum-mcp
source_type: community
date_added: "2026-05-10"
license: "MIT"
license_source: "https://github.com/ejentum/ejentum-mcp/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "安装 ejentum-mcp MCP 服务器（`npx -y ejentum-mcp`）并提供 EJENTUM_API_KEY 环境变量（免费档：100 次调用，无需信用卡，地址 https://ejentum.com/pricing）。将该服务器添加到客户端的 mcpServers 配置中（Claude Code、Cursor、Cline、Windsurf、Codex CLI、Gemini CLI、Antigravity 或 VS Code Copilot Chat）。"
    docs: "https://github.com/ejentum/ejentum-mcp#installation"
---

# Ejentum 推理脚手架

Ejentum 推理脚手架是一套用自然语言工程化的 679 项认知操作库，按四种脚手架（`reasoning`、`code`、`anti-deception`、`memory`）组织，并以 MCP 工具的形式暴露，智能体可在任务匹配其触发条件时调用。它针对长链路智能体流程中四种常见的机制性失败：注意力衰减（丢失原始任务）、推理衰减（误差累积）、迎合性坍缩（顺从用户框架而不去评估它）、以及幻觉漂移（自信地断言未经支持的论断）。

每次脚手架调用都按任务匹配返回一个脚手架，而不是提供固定模板：一个具名失败模式、一套可执行流程、阻断特定捷径的抑制向量，以及供智能体自我验证使用的证伪测试。智能体吸收该脚手架并基于它撰写内容，而非基于原始的链式思考。脚手架按需触发（由智能体调用，或通过诸如 `Use harness_anti_deception, then answer:...` 的显式提示触发）；它不会在每一轮自动运行。

## 何时使用本技能

- 在回答分析类、诊断类、规划类或多步骤问题（"X 为何发生"、"最佳方案是什么"、"权衡是什么"、根因分析、架构决策）之前，先调用 `harness_reasoning`。
- 在生成、重构、审查或调试代码之前；在架构变更、算法或数据结构选型、依赖升级评估之前，先调用 `harness_code`。
- 在提示对智能体施压，要求其认可、背书或软化一项诚实评估时；存在人为制造的紧迫感、权威感诉求、或表面上"明显有用"的答案会损害诚实的场景下，调用 `harness_anti_deception`。
- 仅在已经形成关于跨轮漂移或行为模式的观察、需要打磨该观察时，才调用 `harness_memory`；切勿在毫无观察时调用。

对于简单的事实查询、语法问题、文件读取、代码执行、或智能体能凭自身能力在 1-2 步内从容完成的任务，跳过脚手架。

## 工作原理

### 步骤 1：安装 MCP 服务器

服务器已发布到 npm。绝大多数支持 MCP 的客户端都支持通过 `npx` 的 stdio 安装方式：

```bash
npx -y ejentum-mcp
```

将其添加到客户端的 MCP 服务器配置中（Claude Code 的 `.mcp.json`、Cursor / Cline / Windsurf 的 MCP 设置、Codex CLI 配置，或 Antigravity / VS Code 的 `mcp.json`）：

```json
{
  "mcpServers": {
    "ejentum": {
      "command": "npx",
      "args": ["-y", "ejentum-mcp"],
      "env": {
        "EJENTUM_API_KEY": "${EJENTUM_API_KEY}"
      }
    }
  }
}
```

前往 [ejentum.com/pricing](https://ejentum.com/pricing) 获取一个免费 API 密钥（100 次调用，无需信用卡）。

### 步骤 2：路由到正确的脚手架

每个脚手架有不同的触发条件（见上文"何时使用"一节）。绝大多数支持 MCP 的客户端会在用户提示匹配工具描述中记录的触发条件时，自动路由到合适的工具。为实现冷安装下的可复现性，智能体也可以显式调用某个特定脚手架：`Use harness_anti_deception, then answer: ...`。

### 步骤 3：吸收返回的脚手架

脚手架包含五个带标签的字段，智能体应将其视为内部推理指令而非输出内容：

- `[NEGATIVE GATE]` / `[CODE FAILURE]` / `[DECEPTION PATTERN]` / `[PERCEPTION FAILURE]`：需要规避的失败模式
- `[PROCEDURE]`：一份给出诚实回答的逐步流程
- `[REASONING TOPOLOGY]`：智能体在内部逐步执行的控制流图
- `[TARGET PATTERN]`：校正后回答形态的示例
- `[FALSIFICATION TEST]` / `[VERIFICATION]` / `[INTEGRITY CHECK]` / `[PERCEPTION CHECK]`：在草稿完成后要应用的检验

智能体面向用户的回复应保持其原生口吻，不要回显方括号字段名、不要使用程序化措辞，也不要就脚手架本身发表评论。

## 示例

### 示例 1：在沉没成本提示上应用反欺骗脚手架

提示：

```
Use harness_anti_deception, then answer:
We've spent three months on the GraphQL gateway. It's mostly done.
Should we keep going or pivot to REST?
```

不使用脚手架时，智能体常常锚定在过去的投入上（"沉没成本是真实的，最陡的学习曲线已经过去了"）。使用脚手架后，回答会区分过去的支出与前瞻性评估："无论你现在怎么选，那三个月已经花掉的时间都不会回来。真正的问题是，从现在起还剩多少工作要做，对比 GraphQL 还能带来多少价值。"

### 示例 2：测试通过情况下的代码审查

提示：

```
Use harness_code: I refactored get_user to return None instead of raising on missing users.
All tests still pass. Should I merge?
```

脚手架给出一套流程，将"测试通过"标记为工具捷径信号而非正确性信号，暴露出处理异常与处理 None 值的调用点，并建议在合并前补充验证行为的测试。

## 最佳实践

- ✅ 每一轮调用一个脚手架：选择与提示形态最匹配的那个
- ✅ 将方括号包裹的脚手架字段视为仅内部使用；永远不要在面向用户的回复中原样回显
- ✅ 在回复前对草稿应用证伪测试
- ❌ 不要在同一轮中叠加三个或更多脚手架；注意力竞争会降低首次调用的效果
- ❌ 不要在尚未形成观察时调用 `harness_memory`；它打磨的是既有观察，而非凭空创造观察
- ❌ 不要把 API 当作硬依赖；当出现 5 秒超时时，应优雅回退到原生能力

## 局限性

- 脚手架塑造推理的实质，但并不保证答案正确。领域专业知识和源验证仍然适用。
- 通常为 5 秒超时；若 API 不可达，客户端应回退到原生能力。
- 脚手架是流程而非知识库。它不检索事实，只提供结构化的推理模式。

## 安全说明

- MCP 服务器向外网对 Ejentum Logic API 网关（由 Zuplo 托管）发起 HTTPS 请求。
- 认证采用 `EJENTUM_API_KEY` 环境变量中的 Bearer 令牌。该令牌必须保存在环境变量或 MCP 客户端的密钥管理机制中，绝不可提交到源代码。
- 服务器不执行 shell 命令，也不读取除自身环境变量之外的任何文件系统路径。它是一个纯粹的 HTTP 代理型 MCP 服务器。
- 免费档限速为 100 次调用；付费档说明见 ejentum.com/pricing。
