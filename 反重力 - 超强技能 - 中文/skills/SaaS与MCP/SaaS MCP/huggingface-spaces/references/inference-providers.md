# Inference Providers — 何时不托管模型

某些 Space 完全不需要 GPU。如果模型通过 HF Inference Providers（Cerebras、Fireworks、Together、Replicate、OpenRouter 等）可用，则 Space 可以是代理到托管端点的薄 Gradio shell：

- 零 VRAM，没有 `@spaces.GPU`，没有模型下载。
- 适用于 ZeroGPU 放不下的模型（120B+）。
- 硬件可以是 `cpu-basic` — 完全不需要 GPU。

## 何时使用此模式

- **大模型的无状态聊天或文本完成**。
- **用户想要前沿规模模型的公共 demo**，显然不适合单个 48 GB MIG。
- **用户想要快速交付某些东西**，而不用担心量化/分片。

## 何时不使用此模式

- 模型在任何 Inference Provider 上都不可用。通过以下方式检查：
  ```bash
  curl "https://huggingface.co/api/models/<ns>/<repo>?expand[]=inferenceProviderMapping"
  ```
- Space 需要**自定义解码**（特殊采样、工具使用、检索、跨调用有状态或交互的任何内容）。
- Space 需要**多模态**，超出提供者公开的范围。
- 用户明确希望拥有推理栈（模型加载、解码、性能调优）。

对于这些，请自己在 ZeroGPU 上托管模型 — 参见 [`zerogpu.md`](zerogpu.md)。

## 两种计费模式

根据谁为推理付费来选择。

### 模式 A — Space 创建者付费（简单）

将 `HF_TOKEN` 设置为 Space 密钥。Space 直接使用 `InferenceClient`。每次访问者的调用都向 Space 创建者的账户计费。

```python
import os, gradio as gr
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=os.environ["HF_TOKEN"], provider="fireworks-ai")

def chat(msg, history):
    return client.chat_completion(
        model="<org>/<model>",
        messages=[*history, {"role": "user", "content": msg}],
        max_tokens=512,
    ).choices[0].message.content

gr.ChatInterface(chat).launch()
```

当你希望用户"点击就试试"时使用 — 无登录摩擦。成本由你承担。

### 模式 B — 访问者付费（公共 demo 推荐）

`gr.LoginButton` + `gr.load("models/...")` 与 `accept_token=button`。每个访问者使用他们的 HF 账户登录；推理向**他们的**账户计费。

```python
import gradio as gr

with gr.Blocks(fill_height=True) as demo:
    with gr.Sidebar():
        button = gr.LoginButton("Sign in")
    gr.load("models/<org>/<model>", accept_token=button, provider="fireworks-ai")
demo.launch()
```

README frontmatter 需要：

```yaml
hf_oauth: true
hf_oauth_scopes:
  - inference-api
```

这是**公共 demo 的推荐模式** — 在成本方面可持续，访问者可以使用他们自己的提供者配额（大多数人已付费或免费获得）。

## 硬件

`cpu-basic`。没有 GPU。不要放 `--flavor zero-a10g` — 那会浪费付费赠款。

## 反模式：包装提供者调用的 `@spaces.GPU`

如果你确实使用 Inference Providers，请**不要**将调用包装在 `@spaces.GPU` 中。装饰器会为整个 `duration=` 在你的 Space 上预留一个 GPU slot，但该函数没有 GPU 工作 — 只是向外的 HTTP 调用。你会无缘无故地消耗自己的 ZeroGPU 配额。

提供者代理 Space 需要 `cpu-basic` 硬件和零个 `@spaces.GPU`。