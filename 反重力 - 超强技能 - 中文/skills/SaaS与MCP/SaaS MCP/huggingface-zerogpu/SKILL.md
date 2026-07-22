---
name: huggingface-zerogpu
description: 使用 Gradio Spaces 和 Hugging Face Spaces ZeroGPU 进行 AI 演示与 GPU 计算。当编写或审查使用 `@spaces.GPU` 的代码、为 ZeroGPU Space 配置 `python_version` 或 `requirements.txt`，或处理 ZeroGPU 特有的代码约束（基于 pickle 的进程……）时使用。触发词：ZeroGPU、HuggingFace、@spaces.GPU、Gradio Spaces、GPU 配额、duration。
risk: unknown
source: https://github.com/huggingface/skills/tree/main/skills/huggingface-zerogpu
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

# Hugging Face ZeroGPU
## 何时使用

当你需要使用 Gradio Spaces 和 Hugging Face Spaces ZeroGPU 进行 AI 演示与 GPU 计算时，请使用本技能。在编写或审查使用 `@spaces.GPU` 的代码、为 ZeroGPU Space 配置 `python_version` 或 `requirements.txt`，或处理 ZeroGPU 特有的代码约束（基于 pickle 的进程……）时使用。


针对使用 **ZeroGPU** 硬件在 Hugging Face Spaces 上运行 ML 演示的规则与模式。涵盖 `@spaces.GPU`、duration 与 quota 调优、进程隔离、CUDA 可用性模型、并发安全以及 CUDA 构建约束。

## 适用范围

本技能适用于 **使用 ZeroGPU 硬件的 Gradio SDK Spaces**。Docker 和 Static Spaces 无法调度到 ZeroGPU，Streamlit 应用现在以 Docker Spaces 方式运行——因此本技能仅适用于 Gradio。有关通用 Gradio 编码（组件、布局、事件监听器），请参阅本仓库中的 `huggingface-gradio` 技能。权威的 ZeroGPU 文档位于 https://huggingface.co/docs/hub/spaces-zerogpu ——请参考该文档了解当前的后端 GPU、运行时版本列表以及层级阈值，这些信息会随时变化。

## 参考文件

| 参考文件 | 阅读时机 |
|-----------|--------------|
| `references/concurrency.md` | 编写 ZeroGPU 代码时与 SKILL.md 一起阅读——处理器默认并行运行 |
| `references/how-zerogpu-works.md` | 推理冷启动、worker 复用、为什么模块级预热无法延续到请求中，或为什么返回 CUDA tensor 会导致调用挂起时 |
| `references/how-quota-works.md` | 选择 `duration` 值、调试 `illegal duration` 与 `quota exceeded` 错误，或解释为什么默认 60s 会阻塞短任务时 |
| `references/cuda-and-deps.md` | 安装 CUDA 相关包（例如 `flash-attn`）、固定 torch 配套包版本，或解读 wheel 文件名标签时 |

## 硬件

ZeroGPU 提供两种 GPU 大小，对应后端物理 GPU 的一个分片：

| `size` | 后端 GPU 分片 | 配额消耗 |
|--------|----------------------|------------|
| `large` *（默认）* | 半卡 | 1x |
| `xlarge` | 整卡 | 2x |

默认的 `large` 只占用物理 GPU 的一半，因此显存带宽和算力都显著低于整卡规格。只有当工作负载确实需要额外显存或算力时，才使用 `xlarge`。

> **后端 GPU 随时可能更换。** ZeroGPU 已经历过多次跨代迁移；较旧的资料可能提到 A100 或 H200，但这些都已过时。如需了解当前后端 GPU 以及各 size 的精确显存容量，请在规划工作负载前查阅 [ZeroGPU 文档](https://huggingface.co/docs/hub/spaces-zerogpu)。

## 基本模式

```python
import spaces
import torch
from transformers import pipeline

pipe = pipeline("text-generation", model="...", device="cuda")

@spaces.GPU
def generate(prompt: str) -> str:
    return pipe(prompt, max_new_tokens=100)[0]["generated_text"]
```

关键规则：

1. **在模块级实例化模型**并立即调用 `.to("cuda")`。ZeroGPU 透明地处理实际的设备映射（见下方 CUDA 可用性模型）。
2. **用 `@spaces.GPU` 装饰 GPU 函数**。该装饰器在 ZeroGPU 之外是 no-op，因此在所有环境中保留它都是安全的。
3. **将 `duration` 设为符合现实最坏情况工作负载的值**（默认 60s）。平台会用 `requested duration` 与用户的 `remaining quota` 进行预检查——而不是与实际运行时间相比——因此一个 10 秒的任务如果保留 60s 默认值，一旦用户剩余配额降到 60s 以下就会失败并报 `quota exceeded`。声明更小的 `duration` 在节点级队列中也能获得更高排名。详见下文"Duration and Quota"。
4. **`torch.compile` 不受支持。** 请改用 PyTorch [ahead-of-time compilation (AoTI)](https://huggingface.co/blog/zerogpu-aoti)（torch 2.8+）。
5. **谨慎使用 `size="xlarge"`。** 它占用整个后端 GPU，但消耗 2x 配额，且通常排队更久。

```python
@spaces.GPU(duration=120)
def generate_image(prompt: str):
    return pipe(prompt).images[0]
```

## CUDA 可用性模型

实际的 GPU 访问 **仅** 在 `@spaces.GPU` 装饰的函数内部可用。在这些函数之外，GPU 不会附加到进程。

然而，`import spaces` 会 **对 `torch` 进行 monkey-patch**，从而：

- `torch.cuda.is_available()` 在全局范围内返回 `True`。
- 模块级的 `.to("cuda")` / `device="cuda"` 调用不会报错并成功。

这是有意为之的。模块级的 `model.to("cuda")` 调用会向 ZeroGPU 后端注册 tensor，后端会在启动的 "pack" 步骤将它们写入磁盘 offload 目录，并释放相应的 RAM。当 `@spaces.GPU` 调用到达时，一个 fork 出的 GPU worker 进程通过 pinned-memory 流水线将这些权重从磁盘流式加载到 VRAM。热 worker（在同一个 GPU slot 上跨请求复用）会让权重常驻 GPU，跳过 disk → VRAM 这一步。用户层面的规则就是：在模块级写 `device="cuda"`，它就能工作——完整生命周期请参考 `references/how-zerogpu-works.md`。

| 操作 | 位置 | 原因 |
|--------|-------|-----|
| `model.to("cuda")` / `pipe(..., device="cuda")` | **模块级** | ZeroGPU 注册 tensor 并管理设备迁移 |
| 实际的 CUDA 计算（推理等） | **`@spaces.GPU` 内部** | 真实 GPU 仅在装饰的调用期间附加 |
| 基于 `torch.cuda.is_available()` 进行分支判断 | 避免依赖 | 由于 monkey-patch，它始终返回 `True` |

不要在模块级运行推理或 CUDA kernel——真实 GPU 没有附加，操作要么悄悄落到 CPU 上，要么直接失败。

### 设备选择惯用法仍然有效

在 ZeroGPU 下，标准惯用法依然正确：

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModel.from_pretrained("...").to(device)
```

- **ZeroGPU** —— `is_available()` 为 `True`（被 monkey-patch），因此模型会被注册以便自动设备迁移。
- **独立 GPU Spaces / 本地 GPU** —— `is_available()` 真实为 `True`。
- **CPU Spaces / 本地 CPU** —— 解析为 `"cpu"`。

不要硬编码 `device="cuda"`——这在纯 CPU 环境下会出错。

### 急切加载是默认的正确选择

在模块级加载模型，而不是延迟到首次请求。Space 进程在任何用户到达之前启动，所以冷启动成本只支付一次。延迟加载（`global model; if model is None: ...`、`@lru_cache` 包装器、首次调用才实例化的工厂函数）只是把成本推到了首位用户身上。

## 本地开发：只需安装 `spaces`

不要将 `import spaces` 包在 `try/except` 里，也不要为本地运行把 `spaces.GPU` 重定义成 no-op 回退。在 ZeroGPU 之外，`spaces` 包本身就是真正的 no-op：

- 重型行为（CUDA monkey-patching、client init、启动钩子）由 `SPACES_ZERO_GPU` 环境变量门控，仅在 ZeroGPU 上设置。
- 在 ZeroGPU 之外，`@spaces.GPU` 返回未被装饰的函数原样。
- 顶层 `import spaces` 只执行轻量导入。

Gradio SDK 基础镜像在每个硬件层级上都会安装 `spaces`。因此，即便把 Space 复制到独立 GPU（T4、L4、A10G 等）或 CPU basic 之上，也无需改动代码——`import spaces` 依然成功，`@spaces.GPU` 变成透明的 passthrough。

### 反模式

```python
try:
    import spaces
except ImportError:
    class spaces:  # type: ignore
        @staticmethod
        def GPU(func=None, **kwargs):
            return func if func else (lambda f: f)
```

问题：

1. 回退必须模拟每一种 `@spaces.GPU` 调用形态——裸装饰器、`duration=...`、`size=...`、生成器、`aoti_*` 帮助函数——会随着 `spaces` API 的增长而漂移。
2. 它把 `spaces` 从 `requirements.txt` 中隐藏，即使 Space 在部署时需要它。
3. 它在解决一个并不存在的问题：本地运行时真实的包已经是 no-op。

### 应该这么做

将 `spaces` 加入依赖并无条件导入：

```python
import spaces

@spaces.GPU
def generate(prompt: str) -> str:
    ...
```

## Duration and Quota

当你声明 `@spaces.GPU(duration=N)` 时，会发生三件事：

1. **层级上限检查**——每个访客层级都有一个每次调用的 `duration` 上限。声明的 `duration` 大于该上限会立即失败并报 `ZeroGPU illegal duration`，与剩余配额无关。（层级数字随时间变化——请参见 [ZeroGPU 文档](https://huggingface.co/docs/hub/spaces-zerogpu)）。
2. **配额预检查**——平台会比较 `requested duration` 和用户的 `remaining quota`。若 `remaining < requested`，则调用失败并报 `ZeroGPU quota exceeded`——即便实际工作本可以容纳。错误消息会显示具体数字，例如 `"60s requested vs. 30s left"`。因此一个 10 秒的任务如果保留 60s 默认值，当用户剩余配额降到 60s 以下时就会被阻塞。
3. **队列优先级**——队列是节点级的（同一节点上所有 Space 的请求会竞争 GPU slot），声明的 `duration` 越短，排名越高。

这三点都倾向于声明尽可能小、贴近现实的 `duration`——即便对于短任务也是如此。在一个 10 秒任务上显式写 `@spaces.GPU(duration=15)` 可以避免过早的 `quota exceeded` 拒绝，同时在队列中获得更高排名。

> **`xlarge` 让请求翻倍。** 当 `size="xlarge"` 时，`requested = N * 2`，层级上限检查和配额预检查都一样。因此 `@spaces.GPU(duration=60, size="xlarge")` 内部就是一个 120s 的请求。

### 动态 duration 应对可变工作负载

对于运行时取决于输入的工作负载，可以传入一个可调用对象来对每次请求进行估算。一个静态的较大 `duration` 会把低层级用户挡在外面（其层级上限可能小于该静态值），并且对轻输入来说会无谓地预留配额。

```python
def estimate_duration(prompt, steps):
    return int(steps * 3.5)

@spaces.GPU(duration=estimate_duration)
def generate(prompt, steps):
    return pipe(prompt, num_inference_steps=steps).images[0]
```

关于 `illegal duration` 与 `quota exceeded` 的全部区分、每日运行次数上限、24 小时配额窗口以及 pay-as-you-go 计费，请参见 `references/how-quota-works.md`。

## 进程隔离与 Pickle

被 `@spaces.GPU` 装饰的函数运行在 ZeroGPU 调度器管理的 **独立进程** 中。参数和返回值通过 **pickle 序列化** 跨越进程边界。

由此带来的影响：

- **仅可 pickle 的对象** 才能传入或返回。打开的文件句柄、数据库连接、锁、lambda 以及含有不可 pickle 状态的闭包都会抛出 `PicklingError`。
- **不要直接返回 CUDA tensor。** 在主进程中反序列化 CUDA tensor 会触发 `torch.cuda._lazy_init()`，ZeroGPU 会阻断它。请先转到 CPU：返回 `tensor.cpu()` 或 `tensor.cpu().numpy()`。
- CPU tensor、numpy 数组、PIL 图像以及普通 Python 对象都可以正常使用。
- 大对象会产生序列化开销。优先返回轻量类型（tensor、数组、文件路径、base64 字符串），而不是复杂对象图。

### 跨边界的 `gr.State` 语义

由于处理器运行在独立进程中，`gr.State` 的值 **每次 yield 都会被 pickle**——它们不是按引用共享的。

- 生成器收到的是该状态的 **一份拷贝**（`id()` 与调用方不同）。
- 在生成器内的就地变更 **对其他处理器不可见**，直到被变更后的状态被显式 yield 回去。
- 对一个 `gr.State` 槽位 yield `gr.update()` **会跳过该次更新**——其他处理器仍会看到 yield 之前的值。
- 每次 yield 返回 state 对象都会通过 pickle 产生一份 **新的拷贝**。

实用建议：

- **不要在 ZeroGPU 上假设 `gr.State` 具有引用语义。** 在生成器中变更 state 并期望另一个处理器看到这些变更的代码，会悄悄地用过期的数据。
- **每次 yield 包含 `gr.State` 值都会触发一次完整的 pickle 往返。** 对于较大的 state（模型会话、帧缓冲），应尽量减少 yield 它的次数——理想情况是在末尾 yield 一次。中间 yield 时使用 `gr.update()` 作为 state 槽位的值。
- **state 内的 CUDA tensor 在 yield 前必须转回 CPU**——这与上面提到的 `torch.cuda._lazy_init()` 问题相同。

## 并发

在 ZeroGPU 上处理器 **默认并发运行**。这不是可选项。在单用户测试下能正常工作的代码，在生产中可能悄悄地损坏或泄漏数据。

有三条规则。完整讲解与示例见 `references/concurrency.md`。

1. **无可变全局状态。** 并发请求会互相覆盖。
2. **不要使用固定的输出文件路径。** 并发请求会互相覆盖同一文件。改用 `tempfile` 来生成唯一路径。
3. **只读全局是安全的。** 在启动时加载一次、请求期间只读的模型对象、tokenizer、配置是安全的，也推荐这种用法。

## 调用粒度

每次进入 `@spaces.GPU` 函数都带有不可忽略的开销——跨进程边界的 pickle 往返、worker 预热、CUDA 重新附加，以及节点级队列的一次完整通过。在热循环内部调用被装饰的函数会把这些开销成倍放大，并增加新的失败模式：靠后的迭代可能拿不到 GPU slot，让整个工作半途卡住。

装饰应该装饰拥有循环的外层函数，而不是循环内每次迭代的工作函数：

```python
# Avoid — N GPU entries for N frames
def process_video(frames):
    return [process_frame(f) for f in frames]

@spaces.GPU(duration=...)
def process_frame(frame):
    ...

# Prefer — one GPU entry for the whole video
@spaces.GPU(duration=...)
def process_video(frames):
    return [process_frame(f) for f in frames]

def process_frame(frame):
    ...
```

如果循环中既有较重的 CPU 工作又有 GPU 工作，给整个循环加装饰会把 CPU 耗时也算进用户的配额。当这部分成本客观存在时，将 GPU 工作集中批处理、让 CPU 的前后处理留在装饰器外，是一种需要按情况采用的优化——而不是默认做法。

## CUDA 构建约束

HF Space 在纯 CPU 环境中构建 Docker 镜像。**在 ZeroGPU 上，构建阶段没有 `nvcc`**，因为基础镜像是 `python:3.13`（独立 GPU Spaces 使用 `nvidia/cuda:*-devel-*`，在构建阶段有 `nvcc`）。因此，对一个只能以 sdist 形式发布的 CUDA 相关包——例如裸 `flash-attn`——无法通过 `requirements.txt` 安装到 ZeroGPU 上。只有预构建的 wheel 才能使用。

ZeroGPU **运行时** 自 2025-07 起从 CUDA devel 镜像挂载 `nvcc` 到 `/cuda-image`（最初是为支持 AoTI 而加的）。这让 `torch.export` / AoTI 流程在 `@spaces.GPU` 调用内部得以实现。

**结论**：所有 CUDA 相关包都应通过预构建 wheel 安装。如果 PyPI 上没有可用的 wheel，就在外部构建（例如托管到 HF Hub）并固定其 URL。对于 `flash-attn`，上游发布页面提供了相当完整的 wheel 矩阵，覆盖大部分 Python × CUDA × torch 组合。

关于 wheel 标签的解读（cxx11 ABI、`cu12torch2.X`、`cp3XX`）、torch 家族配套包漂移以及 kernels-community 回退，请参见 `references/cuda-and-deps.md`。

## 示例缓存

`gr.Examples` 的行为与环境相关。在 ZeroGPU 上尤其如此：

- `cache_examples` 默认为 `True`（Spaces 设置 `GRADIO_CACHE_EXAMPLES=true`）。
- `cache_mode` 默认为 `"lazy"`（Spaces 仅在 ZeroGPU 上设置 `GRADIO_CACHE_MODE=lazy`）。

ZeroGPU 默认采用 `lazy`，因为急切缓存会在应用启动时预先运行每个示例，但 ZeroGPU 在启动时 **没有附加 GPU**——只有请求处理期间才会有。对 GPU 绑定的示例进行急切缓存在那里会失败。

当 `cache_examples=True` 时，`run_on_click` / `run_examples_on_click` 参数会被悄悄忽略。如果你的应用依赖于"仅点击填充"行为，请显式设置 `cache_examples=False` 来保留它。

要在本地复现 ZeroGPU 的示例缓存行为：

```bash
GRADIO_CACHE_EXAMPLES=true GRADIO_CACHE_MODE=lazy python app.py
```

## 依赖管理

### 在 README frontmatter 中固定 `python_version`

对 ZeroGPU 而言，固定 `python_version` **几乎是必需的**。运行时默认当前是 Python 3.10，因此本地若使用 3.11+ 的环境，在 Space 上不显式指定就会安装失败。请固定到 ZeroGPU 支持的版本（3.12 是一个合理的默认值）；权威的支持列表位于 [ZeroGPU 文档](https://huggingface.co/docs/hub/spaces-zerogpu)——不要硬编码完整列表，参考文档即可。

```yaml
# README.md frontmatter
python_version: "3.12"
```

`"3.12"` 和 `"3.12.12"` 两种形式都可以接受。

### 不要在 `requirements.txt` 中固定 `spaces`

Space 平台会固定自己的 `spaces` 版本。`requirements.txt` 中的冲突固定会在构建时导致 pip 解析失败。

> **规则**：不要在 `requirements.txt` 中包含 `spaces`。

实现方式取决于你的工具链：

- **手写 `requirements.txt`**：直接省略 `spaces`。
- **uv**（由 `pyproject.toml` 管理）：在 `pyproject.toml` 中声明 `spaces`，让 uv 共同解析其传递性约束（尤其是 `spaces` 固定的 `psutil`），然后在导出时排除它：
  ```bash
  uv export --no-hashes --no-dev --no-emit-package spaces -o requirements.txt
  ```
  若 `pyproject.toml` 中没有 `spaces`，uv 看不到其传递性约束，在构建时可能解析到不兼容的版本。
- **pip-tools**（`pip-compile`）/**Poetry**：使用对应的排除机制。

### 固定 `torch` 以匹配 wheel 标签

如果通过直链 URL 安装一个 CUDA 相关 wheel，wheel 文件名中会编码它所构建的 `torch` 主次版本（例如 `cu12torch2.8`）。请在 `requirements.txt` 中固定 `torch==X.Y.Z` 以匹配——否则 pip 可能把 `torch` 解析到与该 wheel 的构建目标不同的版本，Space 在首次导入时就会失败。详情与 kernels-community 的备选方案见 `references/cuda-and-deps.md`。

## 限制

- 仅当任务明确匹配本技能对应的上游产品或 API 范围时才使用它。
- 在做出改动前，请根据当前的官方文档核实命令、API 行为、定价、配额、凭证以及部署带来的影响。
- 不要把生成的示例当作针对特定环境的测试、安全审查或破坏性/高成本操作的用户审批的替代品。
