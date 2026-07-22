---
name: huggingface-spaces
description: 在 Hugging Face Spaces 上构建、部署和维护应用程序 — Gradio / Docker / Static SDK、ZeroGPU 和专用硬件、模型加载、调试、buckets、推理提供者、社区赠款。当用户要求在 Hugging Face 上创建或托管应用、移植代码到 Spaces、调试运行时错误、选择硬件/SDK 或向 Spaces 推送代码时使用。触发关键词：huggingface spaces、hf spaces、gradio space、docker space、static space、ZeroGPU、space deployment、space sdk、gr.Interface、gr.Blocks、@spaces.GPU、hf spaces hardware、hf upload、space bucket、space secrets。
risk: unknown
source: https://github.com/huggingface/skills/tree/main/skills/huggingface-spaces
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

# Hugging Face Spaces
## 何时使用

当你需要在 Hugging Face Spaces 上构建、部署和维护应用程序时使用本技能 — Gradio / Docker / Static SDK、ZeroGPU 和专用硬件、模型加载、调试、buckets、推理提供者、社区赠款。当用户要求在 Hugging Face 上创建或托管应用、移植代码到 Spaces、调试运行时错误、选择硬件/SDK 或向 Spaces 推送代码时使用。触发关键词：huggingface spaces、hf spaces、gradio space、docker space、static space、ZeroGPU、space deployment、space sdk、gr.Interface、gr.Blocks、@spaces.GPU、hf spaces hardware、hf upload、space bucket、space secrets。


Hugging Face Spaces 托管机器学习应用程序。目前已有 100 万+；每个 Space 都是一个 git 仓库。本技能涵盖它们的创建、构建、调试和维护。

## 0. 准备

正式开始之前：

1. 检查 `hf` CLI 已安装：`which hf`。如果未安装，运行 `pip install -U huggingface_hub`。
2. 检查用户已登录：`hf auth whoami`。如果未登录，请他们在本会话运行 `! hf auth login` — 他们需要一个具备写权限的 token，地址 https://huggingface.co/settings/tokens。
3. 记下 `whoami` 中的 `canPay` 和 `isPro` 标志 — 它们控制下文的硬件选项。

`hf-cli` 技能教授所有 `hf` 命令，是本技能的推荐伴侣。使用 `hf skills add hf-cli` 安装（添加 `--claude --global` 也可同时安装到用户级的 Claude Code）。

## 1. Space 是什么

Space 是一个 git 仓库，有三种可选 SDK：

- **Gradio** — 大多数 Space。Python，快速迭代，支持 ZeroGPU。
- **Docker** — 任意容器。当你需要非 Python 栈或预构建模板时使用（Streamlit、Argilla、Shiny 等 — 完整列表见 https://huggingface.co/docs/hub/spaces-sdks-docker）。**不支持** ZeroGPU。
- **Static** — 纯 HTML，或在部署时构建的 React/Svelte/Vue 项目。用于浏览器端 ML（transformers.js / WebGPU / WebAssembly / onnxruntime-web）、项目页面、交互式报告，或编排其他 Space 的 Space。无需硬件。

### 硬件等级

免费、无创建者成本：**`cpu-basic`** 和 **`zero-a10g`**（ZeroGPU）。Static Space 也免费且不需要硬件。

**`cpu-basic`** — 2 vCPU / 16 GB。用于数据可视化、API 代理 Space、小型 CPU 绑定模型。

**ZeroGPU (`zero-a10g`)** — 在 NVIDIA RTX PRO 6000 Blackwell（sm_120）上的动态、每请求 GPU 分配。两种规格：`large`（半 MIG，48 GB，1× 配额）和 `xlarge`（全卡，96 GB，2× 配额）。Space 创建者免费；Space 访问者消耗自己的每日配额（~5 分钟免费 / 40 分钟 Pro / 60 分钟 Enterprise）。**仅 Gradio**、**PyTorch 优先**。要求创建者位于 PRO / Team / Enterprise 计划。

**专用 GPU**（T4、L4、A10G、L40S、A100、H200）— 按小时向 Space 创建者计费。列表 + 价格：`hf spaces hardware`。只有创建者可以挂载这些，且仅当 `canPay=True` 时。当 ZeroGPU 真的不合适时使用 — 非 PyTorch 主模型且初始化很重、超大模型长上下文推理等。

如果非 PRO 用户有想要 ZeroGPU 的用例，仍然可以构建：创建一个 `cpu-basic` Space，针对 ZeroGPU 编写应用代码，推送，然后申请社区赠款。参见 [`references/grants.md`](references/grants.md)。

权威参考：https://huggingface.co/docs/hub/spaces-overview

## 2. 先查找现有 demo

在决定如何构建任何东西之前，先搜索已有的实现：

```bash
hf spaces search "<model name or task>" --sdk gradio --limit 10
```

如果有人构建过类似的 Space，阅读它的 `app.py` 和 `requirements.txt` — 这能给你可工作的模式。省去大量盲目迭代。在承诺某个方案之前，向用户提及你发现了什么。

## 3. 决定 SDK 和硬件

首先遵循用户的明确请求。如果他们含糊不清：

- **公共 ML demo 的默认**：Gradio + ZeroGPU。除非下面有适用情况，否则使用此选项。
- **模型的唯一推理路径是非 PyTorch**（ONNX / TF / JAX / vLLM 作为主模型，且初始化很重）：专用 GPU。
  - 但是：torch 主流程中的边缘非 torch 工具（小 ONNX 预处理器、TF 工具）在 ZeroGPU 上没问题。劫持只修补 torch；在 `@spaces.GPU` 内初始化非 torch 库，并承担每次调用的短暂初始化开销。
- **小型 / CPU 绑定模型，或 API 代理 Space**：`cpu-basic`（`hardware`-free 不适用于 Gradio）。
- **浏览器端 ML 或项目页面**：Static。
- **非 Python 栈的容器**：Docker。

### 模型来源

- **GitHub 仓库** — 本地克隆以阅读结构。如果它已经有 Gradio demo，最小可行路径是将其适配到 ZeroGPU（参见 [`references/zerogpu.md`](references/zerogpu.md)）。否则：阅读 README + 推理代码，优先选择 PyTorch 路径，估算 VRAM（bf16 ≈ `params_B × 2` GB；48 GB 在 bf16 下可容纳 ≤24B 参数，量化后可容纳更大 — 关于 ZeroGPU 量化的内容参见 [`references/zerogpu.md`](references/zerogpu.md)）。
- **HF 模型仓库** — 阅读其 README，关注任何链接的 GitHub。
- **论文 / 博客文章** — 寻找官方或非官方实现。除非很简单或用户明确要求，否则不要重新实现。
- **含糊的请求** — 先搜索 Spaces；展示结果。

如果模型真的放不下，检查 **Inference Providers** 作为替代方案：参见 [`references/inference-providers.md`](references/inference-providers.md)。这避免了完全托管模型。

## 4. 创建 Space

```bash
hf repos create <namespace>/<name> --type space --space-sdk <gradio|docker|static> \
    [--flavor zero-a10g|cpu-basic|<paid-flavor>] \
    [--secrets KEY=val] [--env KEY=val] \
    --public|--private|--protected \
    --exist-ok
```

- `--space-sdk` 是必需的。
- `--flavor` 选择硬件。`zero-a10g` 是 ZeroGPU 的（旧版）标识符。`cpu-basic` 则省略。运行 `hf spaces hardware` 获取完整的付费列表和价格。
- 可见性：`--public`（任何人都可查看）、`--private`（仅你）、`--protected`（应用可访问但 git 仓库 / Files 标签私有）。
- `--secrets KEY=val` 成为 Space 内部的环境变量，对访问者**不可见**。用于 API key、gated 仓库 token（`HF_TOKEN=hf_…`）等。也可稍后通过 `hf spaces secrets set <id> KEY=val` 设置。
- `--env KEY=val` **对访问者可见** — 仅用于非敏感配置（`GRADIO_SSR_MODE=false`、`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 等）。

> 注意：README YAML 中的 `hardware:` 会被静默忽略 — 硬件只能通过创建时的 `--flavor` 设置，或稍后通过 `hf spaces settings <id> --hardware <name>` 设置。

## 5. 构建应用

Space 现已存在于 `https://huggingface.co/spaces/<namespace>/<name>` 但为空。

### README.md frontmatter

始终必需：

```yaml
---
title: ...
emoji: 🚀                # pick something representative
colorFrom: blue          # red|yellow|green|blue|indigo|purple|pink|gray (only these)
colorTo: indigo
sdk: gradio              # gradio | docker | static
sdk_version: 6.15.1      # latest stable unless you have a reason*
app_file: app.py         # gradio only (docker / static use Dockerfile / index.html)
short_description: ...   # ≤ 60 chars (server rejects longer)
python_version: "3.12"   # ZeroGPU officially supports 3.10.13 and 3.12.12
startup_duration_timeout: 30m   # default; bump to 1h for big LLMs / heavy downloads
---
```

\* 使用旧版 Gradio 的原因：自定义组件锁定了它，或者你正在适配现有 demo 且不想为 5.x→6.x 的破坏性变更重写。如果需要 5.x，选择 `5.50.0`（该系列的最新版本；仍然支持自定义组件）。

所有 frontmatter 选项：https://huggingface.co/docs/hub/spaces-config-reference

### 最小 ZeroGPU Gradio 应用

```python
import spaces           # MUST come before torch / diffusers / transformers
import torch
import gradio as gr
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("<repo>", torch_dtype=torch.bfloat16).to("cuda")

@spaces.GPU(duration=60)
def generate(prompt):
    return pipe(prompt).images[0]

gr.Interface(fn=generate, inputs=gr.Text(), outputs=gr.Image()).launch()
```

三条规则 — 完整论述见 [`references/zerogpu.md`](references/zerogpu.md)：

1. **`import spaces` 在 torch / 任何触碰 CUDA 的 import 之前。** 它会 monkey-patch `torch.cuda.*`；一旦 CUDA 在主进程中初始化，就已经太晚了。
2. **在模块作用域加载模型，`.to("cuda")` 提前执行。** ZeroGPU 会拦截调用，将权重打包到磁盘，并在首次 `@spaces.GPU` 入口时流式传输到 VRAM。在装饰器内部懒加载会让每个用户都付出代价。
3. **装饰 Gradio 绑定的函数。** 将 `duration` 估算为实际的最坏情况（更小 = 更高的队列优先级和更严格的配额检查）。对于与输入相关的运行时，传入可调用对象。

### requirements.txt

简短版本：

- **不要列出**：`gradio`、`spaces`、`huggingface_hub`（已预装且由平台管理；固定它们会导致解析失败或静默破坏 ZeroGPU 运行时）。
- **如果使用则列出**：`torchvision`、`torchaudio`（未预装），以及其他一切（`diffusers`、`transformers`、`accelerate`、`sentencepiece` 等）。
- ZeroGPU 仅接受 torch `2.8.0`、`2.9.1`、`2.10.0`、`2.11.0`。默认保持 torch 不固定（运行时预装最新版）。仅当某个依赖强制时才固定。
- 对于预构建的 CUDA 扩展 wheel（`flash_attn`、`xformers`、`pytorch3d`、`nvdiffrast`、`diff_gaussian_rasterization`、`torchmcubes`）：使用 `https://huggingface.co/datasets/multimodalart/zerogpu-blackwell-wheels/tree/main/wheels` 中的预构建 Blackwell wheel。完整映射 + 注意事项见 [`references/requirements.md`](references/requirements.md)。

### 各 SDK 深入内容

- **Gradio 模式**（主题、`gr.Examples`、流式、自定义 HTML 组件、`gr.Server`）：[`references/gradio.md`](references/gradio.md)。
- **Docker**：https://huggingface.co/docs/hub/spaces-sdks-docker。示例：`hf spaces list --filter docker`。
- **Static**：https://huggingface.co/docs/hub/spaces-sdks-static。对于构建好的 SPA，在 frontmatter 中设置 `app_build_command: npm run build` 和 `app_file: dist/index.html`。
- **ZeroGPU 细节**（装饰器语义、规格、AoTI、生成器、并发、跨 worker 边界的 pickle / `gr.State`）：[`references/zerogpu.md`](references/zerogpu.md) — 当 Space 以 ZeroGPU 为目标时阅读此文件。


## 6. 在 Space 上迭代，而不是本地

尝试根据用户需求在本地构建候选发布版并推送 — 然后使用实时 URL 作为你的测试循环。Space 环境是唯一重要的环境；不要尝试在本地测试。`python3 -m py_compile app.py` 是推送前值得做的最大本地检查。

推送后，为每个变更选择最便宜的更新机制 — 纯 Python 编辑用 hot-reload，hot-reload 无法触及的纯代码文件用 `hf upload`，只有当 `requirements.txt` / `Dockerfile` / README frontmatter 实际变更时才完全重建。完整阶梯 + 陷阱（hot-reload 中毒导致 factory reboot、runtime.sha 滞后等）见 [`references/debugging.md`](references/debugging.md)。

## 7. 验证

不要只信任 `RUNNING` — 应用可能在运行但已损坏。按顺序四步：

**A. 还活着吗？** 阶段 + 硬件：
```bash
hf spaces info <ns>/<name> --expand runtime
```

**B. 启动后日志干净？** 阅读运行日志以确认启动完成且没有警告或静默回退：
```bash
hf spaces logs <ns>/<name> --tail 200
```
查找模型加载完成、没有 import 警告、没有"falling back to CPU" / dtype downgrade 消息、没有 `RUNNING` 掩盖半损坏应用的情况。

**C. API 实际响应。** 在另一个终端中持续 tailing 日志（`hf spaces logs <ns>/<name> --follow`），调用端点：
```python
from gradio_client import Client, handle_file
import os
c = Client("<ns>/<name>", token=os.environ["HF_TOKEN"], httpx_kwargs={"timeout": 600})
print(c.view_api())                    # discover endpoints — don't guess
result = c.predict(..., api_name="/generate")
```

**D. 嗅探输出和日志。** HTTP 200 ≠ 正确的输出。两者都检查：
```python
head = open(result, "rb").read(16)
# glTF / \x89PNG / RIFF…WEBP / RIFF…WAVE / [4:8]==b"ftyp" → png/jpg/webp/wav/mp4
```
同时查看调用期间发出的运行日志 — 静默回退（模型跳到不同尺寸、缺少可选依赖、dtype downgrade）只会出现在那里。

完整 smoke-test 模式（流式端点、OAuth-gated Space、`gr.Server` 自定义路由）：[`references/debugging.md`](references/debugging.md)。

## 8. 永久存储（buckets）

Space 是无状态的 — `/data` 会在重启时被擦除。如果 Space 需要持久化用户上传、生成、日志，或与长期存储交互，挂载一个 **bucket**：

```bash
hf buckets create <ns>/<bucket-name>                                          # --private optional
hf spaces volumes set <ns>/<space> -v hf://buckets/<ns>/<bucket-name>:/data   # read-write at /data
```

Buckets 是付费存储；检查 `canPay` 并与用户确认。完整模式（读快 / 写持久、公共 bucket URL、模型缓存反模式）：[`references/buckets.md`](references/buckets.md)。

## 9. 当事情出错时

操作顺序：

1. 阅读日志：`hf spaces logs <id> --build --follow`（构建错误）或 `hf spaces logs <id> --follow`（运行时错误）。查找**第一个**错误，而不是最后一个。
2. 在 [`references/known-errors.md`](references/known-errors.md) 中 grep 错误字符串。在尝试自己的修复之前检查这是否是已知问题 — 最常见的 ZeroGPU / Gradio / 依赖错误在那里都有 1-2 行修复。
3. 使用 [`references/debugging.md`](references/debugging.md) 中最便宜的阶梯进行迭代。绝大多数问题通过读日志 + smoke-test 循环解决；交互式 dev 模式 + SSH 是重型最后手段。

如果你解决的错误不在 known-errors 列表中，建议用户将其 PR 回本技能，以便未来的运行受益。

---

## 参考索引

| 何时阅读 | 文件 |
|---|---|
| **ZeroGPU 工作原理** + 正确模式（装饰器、规格、pickle、生成器、实时、AoTI） | [`references/zerogpu.md`](references/zerogpu.md) |
| **迭代 + 调试**：日志、阶梯、smoke testing（以及作为最后手段的 dev 模式 + SSH） | [`references/debugging.md`](references/debugging.md) |
| **错误字符串查找** — 所有错误症状（Spaces、ZeroGPU、Gradio、依赖）的唯一位置 | [`references/known-errors.md`](references/known-errors.md) |
| 固定依赖、选择 wheel、torch 族对齐 | [`references/requirements.md`](references/requirements.md) |
| `gr.Examples` 缓存、主题、自定义 HTML 组件、`gr.Server` | [`references/gradio.md`](references/gradio.md) |
| 永久存储、公共 bucket URL | [`references/buckets.md`](references/buckets.md) |
| 社区赠款申请（非 PRO 需要 ZeroGPU） | [`references/grants.md`](references/grants.md) |
| 提供者代理（通过 Cerebras / Fireworks / Together 等实现的零 VRAM 大 LLM） | [`references/inference-providers.md`](references/inference-providers.md) |

## 限制

- 仅当任务明确匹配其上游产品或 API 范围时才使用本技能。
- 在进行更改之前，根据最新的官方文档验证命令、API 行为、价格、配额、凭证和部署效果。
- 不要将生成的示例视为特定环境测试、安全审查或用户对破坏性或昂贵操作批准的替代品。