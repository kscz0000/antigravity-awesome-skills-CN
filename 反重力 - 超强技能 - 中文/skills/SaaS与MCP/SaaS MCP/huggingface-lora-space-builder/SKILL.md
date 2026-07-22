---
name: huggingface-lora-space-builder
description: 为用户提供的 LoRA 在 Hugging Face Spaces 上构建并发布 Gradio 演示。当用户要求创建、生成、上线或发布 Space、demo、Gradio 应用或 playground 来展示 LoRA 时使用——包括 Qwen-Image、Qwen-Image-Edit、LTX-Video、Wan、FLUX、SDXL 等模型的 LoRA。触发词：LoRA Space、Gradio demo、Space 构建、Space 发布、HuggingFace Space、LoRA 演示、playground。
risk: unknown
source: https://github.com/huggingface/skills/tree/main/skills/huggingface-lora-space-builder
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

# Gradio LoRA Space 构建器
## 何时使用

当用户需要在 Hugging Face Spaces 上为某个用户提供的 LoRA 构建并发布一个 Gradio 演示时，请使用本技能。当有人要求创建、生成、上线或发布某个 LoRA 的 Space、demo、Gradio 应用或 playground 时——包括 Qwen-Image、Qwen-Image-Edit、LTX-Video、Wan、FLUX、SDXL 或其他模型的 LoRA——均可使用本技能。


在 Hugging Face Spaces 上构建并发布一个使用用户提供的 LoRA 进行推理的 Gradio 演示。每当有人要求创建、生成、上线或发布某个 LoRA 的 "Space"、"demo"、"Gradio 应用" 或 "playground" 时都可使用——无论基础模型是 Qwen-Image、Qwen-Image-Edit、LTX 还是其他扩散模型。当有人描述了他们训练或在 Hub 上托管的 LoRA 并希望分享时也可使用。默认目标是 ZeroGPU 硬件，默认推理库是 `diffusers`（前提是基础模型支持它）。

输出是一个真实已发布的 Space（默认私有），用户可以在浏览器中试用，而不是一个本地脚本。

## 这些 demo 中"好"的标准

demo 应该针对这个特定的 LoRA 量身定制，而不是在通用模板上简单挂接 LoRA。两个任务相同的 LoRA 可能仍需要不同的 demo：一个姿态控制视频 LoRA 和一个外绘视频 LoRA 都是输入视频并输出视频，但用户提供的输入、预处理和控制完全不同。识别这一点是本技能的核心工作。

具体来说，一个好的 demo 应当具备：

- 加载快、运行快——最小化的模型加载、合理的步数、每次调用不浪费算力。
- UI 仅包含该 LoRA 所需的控件，不多也不少。多余的滑块是负担而非特性。
- 向用户展示过程——进度、有用的中间输出、所用 seed、输入缺失时的明确报错。
- 尊重 LoRA 自身模型卡的推荐：触发词、推荐步数、推荐 guidance scale、推荐 LoRA scale、示例输入。
- 在需要创造力的地方发挥创造性——交互式画布、前后对比滑块、中间处理的并排预览——而在简洁合适的地方保持简洁。

## 工作流

按顺序完成以下阶段。一个阶段收集的信息决定下一个阶段。

1. 收集挑选 pipeline 和设计 UI 所需的 LoRA 信息。
2. 选择基础 pipeline 和推理配方。
3. 为这个特定 LoRA 的任务和输入设计 UI。
4. 同时编写 `app.py`、`requirements.txt` 和 `README.md`；将三者一次性呈现给用户以待批量审批。
5. 发布 Space（私有）。

不要跨多轮对话逐步追问问题。把问题集中起来批量问。

---

## 阶段 1 — 收集 LoRA 信息

必需：Hub 上的一个 LoRA 仓库（例如 `username/my-lora`）。

**首先，尝试在不使用 token 的情况下读取仓库。** 如果成功，仓库是公开的——继续。如果失败并返回 401/403，仓库是私有/受限的，需要已认证的会话来读取。**不要立即索要 token。** 先检查用户是否已经通过认证。

```python
from huggingface_hub import HfApi, get_token

cached_token = get_token()  # picks up HF_TOKEN env var or cached CLI login
if cached_token:
    try:
        info = HfApi().whoami(token=cached_token)
        username = info["name"]
        # info also has fine-grained token scope info if applicable
    except Exception:
        cached_token = None  # token exists but is invalid/expired
```

然后：

- 如果存在有效的已缓存 token *且* 它能读取该仓库，使用它。不需要询问。
- 如果没有已缓存 token，或已缓存 token 无法读取该私有仓库，向用户索要 token——一次性，并附上下面的说明。

当需要索取 token 时（且只有在你确实需要询问时）：

> 我需要一个具有 **write** 权限的 Hugging Face 访问 token（用于在 LoRA 为私有/受限时读取它，并用于发布 Space）。请前往 https://huggingface.co/settings/tokens 创建一个并粘贴到这里。

同一个 token 将在最后阶段重复用于发布，因此这是一次性的请求。

**然后读取仓库中的内容：**

- 列出仓库文件（`huggingface_hub.HfApi().list_repo_files(repo_id)`）。寻找 `.safetensors`、`README.md`、示例图像/视频、多个 checkpoint。
- 获取模型卡（`huggingface_hub.ModelCard.load(repo_id)`）。`data` 字典含有结构化字段；`text` 含 README 正文。
- 如果存在多个 `.safetensors` 文件，选择正确的那个——参见 `references/zerogpu-and-publishing.md` 中的"选择 LoRA 权重文件"。简而言之：README 推荐的文件优先，其次是 `pytorch_lora_weights.safetensors`，再次是最新训练 checkpoint，否则询问。

**从模型卡中，尽量确定：**

- **基础模型**——`base_model` 字段，或 README 中文本提及的内容。通常存在。用它来挑选 pipeline 参考文件（参见阶段 2）。
- **任务**——若设置了 `pipeline_tag`，否则根据基础模型和 README 文本推断。本技能处理五个任务：`text-to-image`、`image-to-image`、`text-to-video`、`image-to-video`、`video-to-video`。
- **触发词**——常称为 "trigger word"、"instance prompt"、"activation word"；有时嵌入在示例 prompt 中。
- **推荐的推理配方**——步数、guidance scale、true CFG scale、LoRA scale、分辨率。许多 LoRA 卡包含 Python 代码片段；信任其 *参数*（步数、guidance、CFG、LoRA scale、dtype）。至于 *加载机制*，参见 `adapting-to-the-lora.md`——优先使用 `pipe.load_lora_weights(...)` 而不是代码片段使用的任何加载方式。
- **示例 prompt 和示例媒体**——用作 UI 中的 Gradio examples。
- **子任务/特定用例**——对于图像编辑和视频 LoRA，"这个 LoRA 实际上做什么"与任务类别同样重要。一个重新打光 LoRA、一个换脸 LoRA 和一个风格 LoRA 可能都属于 image-to-image，但每个的 UI 都不同。

**当无法推断时，向用户询问——一次性，集中在一个批次中。** 把问题格式化以使回答毫不费力。对于任务类别，将五个选项列为编号选择。对于子任务，给出一行描述（"这个 LoRA 做什么？例如 '给肖像重新打光'、'应用漫画风格'、'将视频扩展到更宽的宽高比'"）。如果你已经能根据基础模型或 README 有信心地推断出来，就不要问。

如果模型卡完全没有有用的信息——没有基础模型、没有任务、没有示例——清晰地说出来："模型卡没有可用信息。我需要你告诉我：(1) 基础模型，(2) 这个 LoRA 做什么，(3) 如果你知道的话，推荐的步数和 guidance scale。"

---

## 阶段 2 — 选择基础 pipeline

这里要决定两件事：加载哪个参考文件，以及使用哪个 pipeline 类。这不是同一个问题——一个基础模型系列文件（例如 `qwen-image.md`）涵盖多个变体，而同一系列中的变体并不总是共享一个 pipeline 类。弄错了会导致 Space 加载但产生错误输出，或在启动时失败。

**步骤 1 — 为该基础模型系列加载参考文件。**

- `references/base-models/qwen-image.md` — 涵盖 Qwen-Image 和 Qwen-Image-Edit 系列（text-to-image 和 image-to-image）。
- `references/base-models/ltx.md` — 涵盖 LTX 系列（text-to-video、image-to-video、video-to-video，包括 IC-LoRA）。
- `references/base-models/krea-2.md` — 涵盖 Krea 2（K2），text-to-image（在 RAW 上训练，在 Turbo 蒸馏 checkpoint 上运行推理/LoRA）。

如果基础模型不在这些文件中，本技能尚无一线支持。告诉用户，并询问他们是希望类比进行（使用最接近模型的配方并调整）还是停止。不要默默猜测。

**步骤 2 — 核对 pipeline 类与基础模型自身模型卡是否一致。此步骤为强制项，不可省略。**

一个基础模型的新变体可能使用相同的 pipeline 类但仓库路径不同，或使用全新的 pipeline 类。不要只信任参考文件的表格——它是尽力而为的，可能滞后于最新发布。在确定之前请验证：

```python
from huggingface_hub import ModelCard
base_card = ModelCard.load(base_model_id)
# Read base_card.text — find the diffusers inference snippet, note the pipeline class it imports.
```

基础模型卡的 diffusers 代码片段中导入的类是真正的权威。值得关注的真实示例：

- `Qwen-Image-Edit` 使用 `QwenImageEditPipeline`。`Qwen-Image-Edit-2509` 和 `Qwen-Image-Edit-2511` 使用 `QwenImageEditPlusPipeline`——不同的类、不同的默认参数、接受图像列表而不是单张图像。针对 2511 训练的 LoRA 加载到 `QwenImageEditPipeline` 上会产生错误输出。
- LTX-Video 使用 `LTXPipeline`/`LTXImageToVideoPipeline`/`LTXConditionPipeline`。LTX-2 使用来自不同模块路径的 `LTX2Pipeline`。LTX-2.3 有时需要 diffusers 之外的本机 pipeline。

如果基础模型卡根本没有 diffusers 代码片段，回退到参考文件的表格——并告诉用户你在回退，以防他们知道表格中未涵盖的信息。

此验证的成本是一次 Hub 拉取和几秒钟的阅读时间。跳过它的代价是上面描述的失败模式——一个"能跑"的 Space 静悄悄地使用了错误的类。

**步骤 3 — Diffusers 与本机 pipeline。** 当基础模型有 diffusers pipeline 类时，默认使用 `diffusers`。Qwen-Image、Qwen-Image-Edit 和大部分 LTX 都属于这种情况。一些 LTX 变体（特别是带有特定 IC-LoRA 的 LTX-2.3）需要本机 pipeline；LTX 参考文件会说明何时需要。Diffusers 提供标准的 `load_lora_weights` / `set_adapters` 语义；本机路径需要 LoRA 特定的粘合代码。

---

## 阶段 3 — 为该 LoRA 设计 UI

不要伸手就拿模板。根据 LoRA 的任务和输入推理出 UI。

阅读 `references/tasks.md` 以获取每个任务的基线 UI 模式（T2I、I2I、T2V、I2V、V2V 的标准输入/输出是什么样的）。

然后阅读 `references/adapting-to-the-lora.md`，它涉及 *思考这个特定 LoRA 需要什么*——超越任务类别。该文件是本技能中最重要的文件。同一任务可能需要非常不同的 UI：一个姿态控制的 LTX LoRA 需要视频输入和姿态提取预览；外绘 LTX LoRA 需要宽高比选择器和黑边预览；重新打光 Flux LoRA 需要图像和画布画笔来指明在哪里添加光线。这些都不能简化为"V2V 模板"或"I2I 模板"。

**编写 UI 前的自查。** 写一句话描述用户使用这个 Space 在 10 秒内会做什么。如果这句话不能将此 LoRA 与同一任务的任何其他 LoRA 区分开来，那么 UI 还没有足够成型。

通过自查的示例：

- "上传视频，选择目标宽高比，点击生成；模型填充空白边缘。"
- "在想要打光的位置绘制彩色笔触，选择光照风格，点击生成；模型重新为照片打光。"
- "上传一个人物运动的视频和另一个角色的图像；模型生成该角色做出该动作的视频。"

未通过的示例：

- "输入 prompt 并点击生成。"（通用 T2I——说得更具体些。）
- "上传图像和指令。"（通用编辑——什么样的编辑？）

**Gradio 组件的新鲜度。** Gradio 的组件集在不断演进。在默认使用普通组件之前，考虑是否有更新的组件更合适——例如 `gr.ImageSlider` 用于编辑 LoRA 的前后对比，`gr.BrowserState` 用于持久化用户偏好，`@gr.render` 用于基于输入变化的 UI。如果你不确定某个组件是否存在或其签名，请访问 https://www.gradio.app/docs 获取最新的 Gradio 文档，而不是猜测。

**当内置组件和 Hub 自定义组件都不够时——创造模式。** 如果 LoRA 的自然输入形状没有任何 Gradio 组件（内置或 Hub 上的）能很好地表达——点集、笔触、轨迹、带元数据的多区域注释、3D 旋转小工具、时间轴 scrubber、任何用户在媒体之上操作物体的场景——降级到通过 `gr.HTML` 的自定义 HTML/JS。参见 `references/creative-mode.md` 中的 Gradio 原语（`gr.HTML`、`head=` 注入、`elem_id` 寻址、两种 JS↔Python 状态同步方法）、定义 JSON 线协议的相关约束，以及陷阱。不要仅仅因为会看起来很酷就选择创造模式——只有当 LoRA 的输入形状要求时才选择它。在完全定制之前，也不要跳过上面那级 Hub 自定义组件（例如 `gradio_image_annotation`）。

**`gr.Examples` 用于媒体输入的 Space。** 当没有合适的示例媒体可从模型自身仓库获得时，从共享输入池中拉取——按模态拆分以便 HF 数据集查看器能渲染正确的缩略图：图像见 [`linoyts/repo-to-space-example-inputs`](https://huggingface.co/datasets/linoyts/repo-to-space-example-inputs)，视频见 [`linoyts/repo-to-space-example-videos`](https://huggingface.co/datasets/linoyts/repo-to-space-example-videos)。两者均为 CC0，含 `categories` + 自然语言 `caption` 元数据，每个数据集的 README 中都有相同的过滤/排名配方。选择 2–3 个适合任务的，预处理为模型期望的形状，并将其副本嵌入 Space。设置 `cache_examples=True, cache_mode="lazy"`，使首次点击在不运行时构建示例的情况下缓存（参见 `references/zerogpu-and-publishing.md`）。

---

## 阶段 4 — 编写 Space 文件

编写之前，具体地告诉用户即将发生什么——说出实际的文件名。不是"我将编写这三个文件"，而是类似：

> "现在我将编写发布 Space 所需的三个文件： **`app.py`**（Gradio 演示和推理代码）、 **`requirements.txt`**（Python 依赖项）、 **`README.md`**（Space 配置，包括 ZeroGPU 硬件设置）。然后我会将三者一起呈现给你审阅，然后再发布。"

这能让用户对要生成的内容有明确预期。不要只说"三个文件"而不指出文件名——这样很模糊，表明对交付物缺乏承诺。

三个文件是紧密耦合的：`requirements.txt` 由 `app.py` 导入的内容决定，`README.md` YAML frontmatter 设置的 SDK 版本、硬件和 Space 标题必须与之匹配。同时编写它们，然后在发布之前一次性 **批量** 展示给用户审批。

阅读 `references/zerogpu-and-publishing.md` 获取 ZeroGPU 规则。其中不明显的规则包括：

- 模型在模块级别放在 `cuda` 上（在 GPU 函数内不懒加载）。ZeroGPU 有一个 CUDA 仿真使其在预分配时能工作，并且模块级放置明显快于延迟放置。
- 运行推理的函数用 `@spaces.GPU(duration=...)` 装饰。选择适合任务的 duration——图像生成用短的，视频用长的。
- 不要使用 `torch.compile`——它与 ZeroGPU 的进程模型不兼容。

### `app.py`

从阶段 1–3 决定的片段组合而来。不要从模板粘贴。每个部分的存在都因为它是必需的：

- 导入——`gradio as gr`、`torch`、`spaces`、pipeline 类、任何预处理需要的。
- 常量——`LORA_REPO`、`BASE_MODEL`、推荐步数、guidance、LoRA scale、触发词。
- 模块级模型加载——pipeline `from_pretrained`、`.to("cuda")`、`load_lora_weights`。如果 LoRA 仓库是私有的，传入 `token=os.environ["HF_TOKEN"]`。
- 预处理函数（如果有）——姿态提取、padding、mask 构建等。CPU 代码可以在模块级别运行；GPU 代码需要放在 `@spaces.GPU` 函数内。
- 推理函数——用 `@spaces.GPU(duration=...)` 装饰。验证输入，应用触发词，构建 pipeline kwargs，返回输出。
- Gradio Blocks——来自阶段 3 的 UI，连接到推理函数。

常见需要正确处理的：

- 返回实际使用的 seed 和结果，以便用户可以复现。
- 在推理函数上使用 `gr.Progress(track_tqdm=True)` 以显示 diffusers 的内部进度条。
- 验证输入——在必需输入缺失时抛出 `gr.Error("Please upload an image first.")`，而不是让 pipeline 报出莫名其妙的错误。
- 在 `gr.Examples` 上，使用 `cache_examples=True, cache_mode="lazy"`——普通的 `cache_examples=True` 在构建时运行示例，在 ZeroGPU 上会失败；懒加载模式将缓存推迟到首次用户点击时。

### `requirements.txt`

不要附带一个固定的最小列表并指望它能工作。"最小"列表适用于普通 T2I LoRA，但一旦基础模型具有视觉语言文本编码器、视频输出或任何非平凡的预处理，它就会失败。**根据 Space 实际需要派生 `requirements.txt`**，按以下顺序：

1. **`app.py` 中的每个顶级非标准库导入。** 如果 `app.py` 执行 `import cv2`，则 `requirements.txt` 中有 `opencv-python`。如果它执行 `from controlnet_aux import OpenposeDetector`，则 `requirements.txt` 中有 `controlnet-aux`。机械地遍历导入。（注意下一段的排除项——某些导入是运行时内置的，不需要列出。）
2. **基础模型参考的"必需依赖项"小节所说的内容。** 每个基础模型文件列出了 pipeline 引入的非显而易见的额外内容——Qwen-Image 的 `torchvision`（Qwen 2.5-VL 文本编码器）、LTX 的 `imageio[ffmpeg]`（视频导出）等。包括所有这些。这些是导入时不会拾取的依赖，因为 pipeline 的组件在加载时传递性地导入它们。
3. **LoRA 自身模型卡明确提到的安装内容。** 如果 LoRA README 有自己的 `pip install` 块，从那里提取依赖项。
4. **diffusers/ML 栈：** `diffusers`、`transformers`、`accelerate`、`peft`、`safetensors`。默认为不带版本固定。如果基础模型参考说模型需要从 git 安装 `diffusers`（近期发布经常需要——Qwen-Image-Edit-2511 是一个当前示例），则将 `diffusers` 切换为 `git+https://github.com/huggingface/diffusers`。

**不要列在 `requirements.txt` 中的内容：**

- **`gradio`** — 由 `README.md` YAML frontmatter 中的 `sdk_version:` 字段控制，而不是由 `requirements.txt` 控制。在 requirements 中列出它最好是被忽略，最坏会导致与 SDK 的版本冲突。仅在 README 中设置版本。
- **`torch`** — 由 Space 运行时提供。仅当需要固定特定版本时才添加（很少见，通常表明其他地方有问题）。
- **`spaces`** — 由 Space 运行时提供。仅当需要固定特定版本时才添加。
- **`huggingface_hub`** — 由 Space 运行时提供。仅当需要固定特定版本时才添加。

这四个在 ZeroGPU 容器中预装。无论如何列出它们都是"宁滥勿缺"的本能——对于非基线依赖这是对的，但对于基线依赖这是错的，因为固定版本会与运行时的托管版本冲突。

**对其余所有内容保持"宁滥勿缺"的偏好。** Space 实际不使用的包只会导致构建稍慢一些。缺少必需包会导致启动时崩溃，用户更难诊断。这些代价是不对称的——促使此规则产生的测试失败正是第二种。

**但有两个特定的依赖不能不加思索地添加**，因为它们在 ZeroGPU 上经常引起更多问题而不是解决问题：

- `xformers` — 固定到特定的 torch 版本，是频繁的冲突源头。ZeroGPU 运行时附带 torch 2.8+，因此任何固定版本的 `xformers` 必须支持该版本。Blackwell 上的额外陷阱：xformers 的 FA3 派发错误地限制硬件（FA3 内核仅在 Hopper 上为 `sm_90a`，但派发器限制条件为 `device_capability >= (9, 0)`，这也匹配 Blackwell）并在 kernel 启动时崩溃并报 `CUDA invalid argument`。如果使用 xformers attention 的 Space 遇到此问题，请在模块加载时禁用 FA3 派发：

  ```python
  try:
      from xformers.ops.fmha import _set_use_fa3
      _set_use_fa3(False)
  except Exception:
      pass
  ```

  仅当 `app.py` 实际使用 `xformers` 时才包含它。
- `flash-attn` — 需要构建步骤，经常无法安装。与 `xformers` 相同的 torch 2.8+ 对齐警告。仅当 `app.py` 实际使用它时才包含。

**仅当有理由时固定其他版本**（例如，已知的不兼容性，或匹配模型卡中的配方）。

### `README.md`

Space 由 `README.md` 顶部的 YAML frontmatter 配置。该 frontmatter 是选择 ZeroGPU 的地方。

```
---
title: <human-readable title>
emoji: 🎨
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: <current Gradio version>
app_file: app.py
pinned: false
hardware: zero-a10g
short_description: <one short line for the Space tile, ~60 chars max>
models:
  - <base model repo>
  - <lora repo>
---

# <title>

A short description with links to the LoRA and base model.
```

关键字段：

- `sdk: gradio` — ZeroGPU 必需。
- `sdk_version` — 匹配你所针对的 Gradio 版本。查询当前版本（`pip index versions gradio`，或查看 https://www.gradio.app）而不是猜测。
- `hardware: zero-a10g` — ZeroGPU 的遗留字符串。实际硬件是 NVIDIA RTX Pro 6000 Blackwell，但标识符是 `zero-a10g`。ZeroGPU 适用于 PRO、Team 和 Enterprise 账户；如果用户未订阅，Space 将回退到 CPU。如果你怀疑他们不在 PRO 上，请提及这一点。
- `models:` — 列出基础和 LoRA 仓库。这启用 Hub 缓存和发现。
- `short_description` — 出现在 Space 磁贴上。**保持简短（约 60 个字符或更少）。** Hub 的 YAML 验证器以 `https://huggingface.co/api/validate-yaml` 的 400 响应拒绝过长的值，这在 `create_repo` 或 `upload_file` 期间会显示为 `HfHubHTTPError`。确切的服务器端限制没有文档记录并且可能会更改，因此目标是磁贴可见长度范围而不是推到上限。如果你确实遇到 400，修复几乎总是缩短此字段。描述 Space 功能的一句话就足够了——YAML 下面的 README 正文是放置较长文本的合适位置。

### 单一批量审批 — 操作顺序很重要

这里的纪律是 **先编写所有三个文件，然后在一条消息中将它们一起展示。** 不是"写 `app.py` → 讨论它 → 写 `requirements` → 讨论它 → 写 `README` → 讨论它"。那种节奏即使你没有明确请求审批，也会产生三次审批时刻，因为用户在每个文件后都被要求做出反应。

具体来说：

1. **连续编写 `app.py`、`requirements.txt` 和 `README.md`，中间没有任何插入的散文。** 文件之间没有评论。没有"现在我写下一个"。没有描述你正在生成的每个文件是做什么的。只是三个文件，背靠背。
2. **然后，在一条消息中，一次性请求涵盖全部三个的审批。** 类似这样的内容："这是 Space — `app.py`（N 行）、`requirements.txt` 和 `README.md`。审阅并确认以发布，或告诉我需要更改什么。"
3. 用户一次性响应，涵盖他们想要在任何三个文件中更改的内容。

要避免的：

- 在编写 `app.py` 后但在编写其他文件之前走过其结构或设计选择。评论要么在写之前的公告（阶段 4 开始），要么在所有三个文件存在之后的单一审批消息中。
- 询问"准备好下一个了吗？"或"要我继续 requirements 吗？"——那些是隐式的逐文件审批。
- 内联显示一个文件并提供"准备好后显示下一个"——同样的陷阱。
- 将三个文件中的任何一个视为可选或后续文件。它们作为一个交付物一起产生。

如果用户在看到第一个文件后用反馈或问题打断，那没问题——响应它——但规则仍然适用：下次你生成代码时，所有剩余的文件一起生成，而不是一次一个。

---

## 阶段 5 — 发布 Space

使用阶段 1 中的认证会话。默认为 **私有**，这样用户可以在将其公开之前审查 Space。在创建之前向用户确认目标用户名："我会发布到 `{username}/{space_name}` — 确认吗？"

```python
from huggingface_hub import HfApi, SpaceHardware

api = HfApi(token=hf_token)
username = api.whoami()["name"]
repo_id = f"{username}/{space_name}"

api.create_repo(
    repo_id=repo_id,
    repo_type="space",
    space_sdk="gradio",
    space_hardware=SpaceHardware.ZERO_A10G,
    private=True,
    exist_ok=True,
)

# Upload files
for path in ["app.py", "requirements.txt", "README.md"]:
    api.upload_file(path_or_fileobj=path, path_in_repo=path,
                    repo_id=repo_id, repo_type="space")
```

如果 LoRA 仓库本身是私有/受限的，Space 在运行时需要 token 来下载 LoRA。将其设置为 Space secret：

```python
api.add_space_secret(repo_id=repo_id, key="HF_TOKEN", value=HF_TOKEN)
```

…在 `app.py` 中，使用 `token=os.environ["HF_TOKEN"]` 加载 LoRA。

**上传后**，在分享之前运行下面的 smoke-test — 构建异步运行，静默失败（错误的 `weight_name`、缺少依赖、错误的 pipeline 类）仅在首次推理时出现。**一旦 smoke-test 通过**，分享 Space URL（`https://huggingface.co/spaces/{repo_id}`）并告诉用户 Space 是私有的 — 他们需要登录才能查看它。请注意，构建需要几分钟；如果失败，日志在 `https://huggingface.co/spaces/{repo_id}/logs/container`。

**发布时失败（构建开始之前）：**

- **`HfHubHTTPError: 400 Bad Request` 来自 `https://huggingface.co/api/validate-yaml`**，发生在 `create_repo` 或 `upload_file` 期间。README YAML 未能通过服务器端验证。最常见的原因是 `short_description` 太长；有时是杂散字段或格式错误的值。修复：将 `short_description` 缩短到约 60 个字符并重试。如果缩短不起作用，请查找字段名中的拼写错误或无效值（例如 `colorFrom`/`colorTo` 中不支持的颜色、无效的 `hardware` 字符串）。
- **403 on `create_repo`** 与 `space_hardware="zero-a10g"`：用户不在 PRO/Team/Enterprise 上，因此无法在创建时请求 ZeroGPU。修复：在不带 `space_hardware` 的情况下重试 `create_repo`，在 README YAML 中保留 `hardware: zero-a10g` — Space 在 CPU 上创建。用户然后可以升级到 PRO（自动提升到 ZeroGPU）或申请 [community GPU grant](https://huggingface.co/docs/hub/spaces-gpus#community-gpu-grants)（通过 Space 的硬件设置请求）。
- **401/403 on `upload_file`**：token 没有 write 权限。修复：向用户索要具有 write 权限的 token。

**常见构建失败（构建开始之后）：**

- LoRA `weight_name` 在 `load_lora_weights` 中不匹配 → 通过 `list_repo_files` 检查实际文件名。
- 基础模型受限且 token 未设置为 Space secret。
- ZeroGPU 未分配（用户不在 PRO 上） → Space 回退到 CPU 并且慢得无法使用。
- Diffusers 版本不识别 pipeline 类 → 在 `requirements.txt` 中固定到 git diffusers。
- 模块加载时缺少依赖 → 参见上面的 `requirements.txt` 派生规则；最常见的情况是 Qwen-Image 文本编码器的传递性依赖（如 `torchvision`）。

如果构建失败，主动读取日志并提出修复建议。

---

## 阶段 6 — 对 Space 进行 Smoke-test

在声明 Space 完成并将 URL 交给用户之前，端到端地测试一次。几种失败模式（错误的 `weight_name`、错误的 pipeline 类、缺少传递性依赖、受限基础模型的 token 问题）构建干净但仅在首次推理时显现。`gradio` Python 包附带一个 CLI 来做到这一点——`gradio info` 返回端点签名，`gradio predict` 运行实际推理。两者都随 Space 已经需要的 `gradio` pip 依赖一起提供，因此它们在本技能运行的任何环境中都可用。

**步骤 1 — 等待构建。** `create_repo` 立即返回，但容器镜像仍在构建。轮询 `HfApi().get_space_runtime(repo_id).stage` 直到它达到 `RUNNING`：

```python
import time
from huggingface_hub import HfApi
api = HfApi(token=hf_token)
while True:
    stage = api.get_space_runtime(repo_id).stage
    if stage == "RUNNING": break
    if stage in {"BUILD_ERROR", "RUNTIME_ERROR", "CONFIG_ERROR"}:
        raise RuntimeError(f"Build failed: {stage}. Logs: https://huggingface.co/spaces/{repo_id}/logs/container")
    time.sleep(15)
```

如果构建失败，获取容器日志（`https://huggingface.co/spaces/{repo_id}/logs/container`），阅读 traceback，并提出修复建议。不要对未运行的 Space 运行 `gradio info` ——它会挂起或报 503。

**步骤 2 — 验证端点签名。** `gradio info {repo_id} --token {hf_token}` 返回暴露的端点及其参数类型。阅读输出并确认：(a) 端点存在（默认是 `/predict`，但 Blocks Space 通常有来自 Python 函数名的自定义名称），(b) 按顺序的参数与 `app.py` 声明的匹配，(c) 文件类型参数按预期显示 `"type": "filepath"`。如果其中任何一项不正确，面向用户的 UI 仍可能看起来正确，但 API 调用将失败 — 修复并重新上传。

**步骤 3 — 运行一次真实推理。** 选择最轻量可行的输入——来自 LoRA 卡的最简单示例，或一个 `gr.Examples` 条目。对于私有 Space 传入 `--token`。对于文件输入，payload 使用 `{"path": "...", "meta": {"_type": "gradio.FileData"}}`。

```bash
# Text-to-image:
gradio predict {repo_id} /predict '{"prompt": "...", "aspect_ratio": "1:1", ...}' --token $HF_TOKEN

# Image-to-image (file input):
gradio predict {repo_id} /predict '{"input_image": {"path": "/tmp/sample.jpg", "meta": {"_type": "gradio.FileData"}}, "prompt": "..."}' --token $HF_TOKEN
```

如果你没有用于 I2I 的本地样本图像，请从 LoRA 仓库获取一个（`hf_hub_download(repo_id, filename="example.png")`）或从基础模型卡获取。

**创造模式 Space 的警告。** `gradio info` 和 `gradio predict` 仅测试 Python 端点——它们不告诉你 `gr.HTML` 组件中的自定义 JS 是否工作。如果 Space 使用创造模式（参见 `references/creative-mode.md`），在 API smoke-test 通过后，**在浏览器中打开 Space URL 并验证一次交互**，然后再分享。服务器端绿灯加上 JS 损坏是这些最常见的失败模式。

**步骤 4 — 解读结果。**

- **成功返回且输出看起来合理** → 完成。分享 URL。
- **HTTPError 503 / "Space is sleeping"** → Space 在步骤 1 和 3 之间关机。唤醒它（`api.restart_space(repo_id)`）并重试。
- **推理错误提到 `weight_name` / `safetensors`** → `app.py` 中的 LoRA 文件名与 LoRA 仓库中的实际文件不匹配。重新检查 `list_repo_files`，修复 `weight_name=`，重新上传 `app.py`。
- **推理错误提到缺少 pipeline 类或属性** → diffusers 版本太旧。将 `requirements.txt` 切换到 `git+https://github.com/huggingface/diffusers` 并重新上传。
- **模块加载时的 `ImportError`** → 缺少依赖。将其添加到 `requirements.txt` 并重新上传。运行时日志（`/logs/run`）会指出缺少的包。
- **OOM** → 降低默认分辨率或步数，或选择更小的基础变体。
- **超时/挂起** → 提高 `@spaces.GPU(duration=...)` 并重新上传。

smoke-test 的存在是为了将这些从"用户发现并报告回来"转变为"你发现并在他们看到之前修复"。不要因为构建变绿而跳过它 — 绿构建推理中断是具有非平凡 pipeline 的 Space 最常见的失败模式。

---

## 应避免的事项

- 适用于所有 LoRA 的通用"一个 demo"模板。本技能的全部意义在于量身定制。
- 在 GPU 函数内懒加载模型。在 ZeroGPU 上很慢，并将启动错误隐藏到第一次请求。
- `torch.compile`。在 ZeroGPU 上不支持。
- 在 ZeroGPU 上使用 `cache_examples=True` 而不带 `cache_mode="lazy"`。
- 将 LoRA 权重上传到 Space 仓库。在运行时从 LoRA 自己的 Hub 仓库拉取。
- 直到最后才询问 HF token，然后才发现 LoRA 一直是私有的，你无法读取模型卡。
- 暴露所有 diffusers 旋钮。选择对这个 LoRA 重要的 1–3 个控件。
- Space 发布后在聊天回复中写冗长的前言。Space URL 才是交付物；保持结尾简洁。

## 局限性

- 仅当任务明显匹配其上游产品或 API 范围时才使用本技能。
- 在进行更改之前，请根据当前官方文档验证命令、API 行为、定价、配额、凭证和部署效果。
- 不要将生成的示例视为特定环境测试、安全审查或用户对破坏性或昂贵操作的批准的替代品。