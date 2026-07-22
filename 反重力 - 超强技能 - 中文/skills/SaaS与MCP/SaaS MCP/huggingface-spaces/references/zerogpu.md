# ZeroGPU

每当 Space 以 ZeroGPU（`zero-a10g` flavor）为目标时阅读此文件。SKILL.md 的 3 条规则总结是一个起点；本文件涵盖了足以调试和设计的模型细节。

有关数值限制（每档每日配额分钟数、每日运行次数上限、当前支持的 GPU、支持的 Python / torch 版本）：https://huggingface.co/docs/hub/spaces-zerogpu。这些值会随时间变化，故意不纳入本技能。

## 心智模型

ZeroGPU Space 以**两个进程**运行：

- **主 web 进程** — 长生命周期。导入 `app.py`，启动 Gradio。不持有 VRAM，并且在启动"pack"步骤之后，主进程也不再持有模型权重。
- **GPU worker** — 短生命周期。每个 `@spaces.GPU` 请求时 fork（或在温暖时复用）。最终会被 ZeroGPU 调度器在另一个 Space 需要该 slot 时杀死。你的代码从不主动杀死自己的 worker。

`import spaces` 在主进程中 monkey-patch `torch.cuda.*`，使得 `.to("cuda")` 和 `torch.cuda.is_available()` 在模块作用域内工作**而无需**真实 GPU。模块级的 `model.to("cuda")` 被拦截：张量数据在物理上仍保留在主进程 RAM 中，此时注册了一个呈现为 CUDA 的"伪"张量。在启动"pack"步骤中，后端通过 `O_DIRECT` 将原始 CPU 张量写入磁盘并释放 RAM。pack 后，主进程任何地方都不持有权重。

当 `@spaces.GPU` 调用到达时，调度器将其路由到 worker：

- **冷 worker** — 从主进程 fork；torch 未被 patch；初始化真实 CUDA；通过双缓冲流水线将权重从磁盘流式传输到 pinned host，再到 VRAM。这就是冷启动成本。
- **暖 worker** — 与同一 slot 绑定的活跃 worker；跳过初始化；权重从前一次调用保留在 VRAM 上。

当另一个 Space 需要该 slot 时，暖 worker 最终会死亡。在低流量 Space 上偶尔的冷启动是正常的。

## 三条规则

### 1. 在任何触碰 CUDA 的 import 之前 `import spaces`

```python
import spaces      # FIRST
import torch       # then this
```

如果在 `import spaces` 之前有东西初始化了 CUDA，patch 就无法应用，你会得到 `RuntimeError: CUDA has been initialized before importing the spaces package`。对于在 import 时急切初始化 CUDA 的库（例如 `numba.cuda`、通过 numba 的 NeMo），在 import 之前设置 disable 环境变量：

```python
import os
os.environ.setdefault("NUMBA_DISABLE_CUDA", "1")
import spaces
```

### 2. 在模块作用域加载模型，`.to("cuda")` 提前执行

```python
pipe = DiffusionPipeline.from_pretrained("...", torch_dtype=torch.bfloat16).to("cuda")
```

**不要**在 `@spaces.GPU` 内懒加载。劫持是为模块级放置设计的；延迟它会将数十秒的 checkpoint I/O + dtype 转换 + GPU 移动放在每个冷请求中。

使用**字符串 `"cuda"`** — 永远不要使用整数设备 id。ZeroGPU 每次请求重新分配设备 id，因此 `.to(0)`、`device_map={"": 0}`、`torch.cuda.set_device(0)` 都会静默破坏。

对于普通的 `from_pretrained` 加载，使用 `.to("cuda")`，**而不是** `device_map="cuda"`（后者通过 `accelerate.set_module_tensor_to_device` 路由，并在加载时调用 `torch._C._cuda_init()`，绕过劫持）。例外是 ZeroGPU 感知的加载器 — 特别是 `bitsandbytes` 量化路径；`from_pretrained(..., quantization_config=BitsAndBytesConfig(...))` 可以与 `device_map="cuda"` 一起使用。

**预加载多个变体**（例如 base + refiner、image + video 模型）只要它们的组合 VRAM 适合就没问题。在模块作用域按顺序将它们全部加载到 dict 中，然后按请求键入。不要在请求之间卸载/重新加载 — 那会将加载成本重新放回给用户。

### 3. 装饰 Gradio 绑定的函数

ZeroGPU 的启动扫描遍历 Gradio 注册的事件处理器，查找 `@spaces.GPU` 标记的函数。如果你装饰了 `inner_helper` 但绑定的是 `click(fn=outer)`，则会出现 `RuntimeError: No @spaces.GPU function detected during startup`。始终装饰传递给事件处理器的函数。

```python
@spaces.GPU(duration=60)
def generate(prompt):
    return pipe(prompt).images[0]

btn.click(fn=generate, inputs=prompt_box, outputs=image_out)
```

## 规格 duration

`@spaces.GPU(duration=N)` 意味着"预留 N 秒 GPU 时间"。两种失败模式：

- **`ZeroGPU illegal duration`** — `N` 超过访问者的档位上限。降低 `duration` 是唯一的修复。
- **`ZeroGPU quota exceeded`** — 访问者的剩余配额小于 `requested`。比较方式是 `requested vs remaining`，而不是 `actual vs remaining` — 所以一个 10 秒的任务如果使用默认的 60 秒，只要访问者的剩余配额降至 60 秒以下就会被阻止。

更小的 `duration` 在队列中也排名**更高**。这两个原因都倾向于声明实际的最坏情况，而不是舒适的余量。

**挑选值 — 不要猜测。** 过高的 duration 可以干净部署但在第一次调用时出错；过低的会静默截断。方法论：

1. 用占位符（例如 180 秒）发布。
2. 用 `time.perf_counter()` 进行测量，并将秒数作为响应返回。
3. 通过 `gradio_client` 运行 2-3 次代表性调用。
4. 设置 `duration = round(measured_max × 1.4)`。

对于输入相关的运行时，传递**可调用对象**：

```python
def _estimate(prompt, steps, *args, **kwargs):
    # Swallow extras with *args, **kwargs — Gradio passes progress= positionally
    # and a strict signature will raise "takes 5 positional arguments but 6 were given"
    return min(240, 60 + int(steps * 3.5))

@spaces.GPU(duration=_estimate)
def generate(prompt, steps, ..., progress=gr.Progress(track_tqdm=True)):
    ...
```

## 规格内存：`large` vs `xlarge`

`size="large"`（默认）是后备卡的一半（Blackwell 上 48 GB）。`size="xlarge"` 是整张卡（96 GB），每秒消耗 **2× 配额** — 还有更高的队列等待。除非工作负载真正 OOM，否则使用 `large`。

粗略 VRAM 规格：

| 模式 | 内存规则 | 7B | 27B | 70B |
|------|------------|------|------|------|
| bf16 | `params × 2` GB | 14 GB ✓ large | 54 GB → xlarge | 140 GB → quant + xlarge |
| int8 | `params × 1` GB | 7 GB ✓ large | 27 GB ✓ large | 70 GB → xlarge |
| 4-bit (NF4 / int4) | `params × ~0.55` GB | 4 GB ✓ large | 15 GB ✓ large | 40 GB ✓ large |

数字仅适用于权重；激活和 KV cache 会叠加（对于长上下文影响显著）。

## 量化

ZeroGPU 支持两种量化栈：**`bitsandbytes`**（transformers 的即插即用，经验丰富）和 **`torchao`**（torch 原生，较新，安装较小）。根据你的模型 `from_pretrained` 实际接线选择；如果两者都可以，对于 transformers LLM 默认使用 `bitsandbytes`，对于 diffusers 使用 `torchao`。

### bitsandbytes (NF4 / int8)

```python
import spaces, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb,
    device_map="cuda",            # OK here — bnb's loader is ZeroGPU-aware
    dtype=torch.bfloat16,
).eval()
```

这是在 ZeroGPU 模块作用域使用 `device_map="cuda"` **安全**的唯一情况（bitsandbytes 的加载器路径清晰拦截）。对于非 bnb 加载，坚持使用 `.to("cuda")`。

`load_in_8bit=True` 将 4-bit 块替换为 int8 — 同样的劫持安全加载器。更大但质量更高，没有 `compute_dtype` 旋钮。

### torchao

```python
import spaces, torch
from diffusers import DiffusionPipeline
from torchao.quantization import quantize_, Int8WeightOnlyConfig

pipe = DiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16).to("cuda")
quantize_(pipe.transformer, Int8WeightOnlyConfig())   # mutates in place
```

`torchao` 更灵活（细粒度每模块量化、`Int4WeightOnlyConfig`、`Float8WeightOnlyConfig` 等），也可与 diffusers 的 `from_pretrained(..., quantization_config=TorchAoConfig(...))` 集成一起工作。无 CUDA 构建依赖 — 作为 wheel 安装。

### 注意力后端

默认 `attn_implementation="sdpa"` — torch 原生，到处可用。仅当上游仓库默认使用 FA 后端或强烈推荐时才使用 FA 后端。如果它在 Blackwell 上中断，则回退到 SDPA。

**Flash Attention 2** 通过 `multimodalart/zerogpu-blackwell-wheels` 中的预构建 wheel 工作（[`requirements.md`](requirements.md)）。wheel 的真实 `flash_attn_2_cuda` 也满足 xformers 的 import-time 探测。

**Flash Attention 3** 当前无法在 Blackwell sm_120 上使用。`kernels-community/flash-attn3`、`vllm-flash-attn3` 和 `sgl-flash-attn3` 都失败，提示 `no kernel image is available` 或 `NotImplementedError`。请使用 SDPA 或 FA2。

**xformers** 可通过预构建 wheel 获得 — 自动分派在 sm_120 上选择 FA2，无需 monkey-patch。

## 并发

处理器**默认并发**运行。三条规则：

1. **无可变全局状态。** 处理器写入模块级 dict / list 时会相互竞争。
2. **无固定输出路径。** 两个并发调用写入 `output.png` 会相互冲突（并在用户之间泄露数据）。使用 `tempfile.NamedTemporaryFile(suffix=...)`。
3. **只读全局变量是安全的** — 一次加载的模型、分词器、配置，仅在处理器内读取。

## 进程隔离和 pickle

`@spaces.GPU` 在单独的 fork 中运行。参数和返回值通过 pickle 跨越：

- **只能传入/传出可 pickle 的对象。** 文件句柄、锁、lambda、对不可 pickle 状态的闭包 → `PicklingError`。
- **永远不要返回 CUDA 张量。** 在主进程中 unpickle 会触发 `torch.cuda._lazy_init()`，ZeroGPU 会阻止该调用 → 调用挂起。在返回前转换为 CPU：`return tensor.cpu()` 或 `.cpu().numpy()`。
- CPU 张量、numpy 数组、PIL 图像、普通 Python 对象都能正常工作。
- `gr.SelectData` 是一个特殊情况 — 其 `__getattr__` 在 pickle 下递归。在一个未装饰的薄包装中提取你需要的字段（`evt.index[0]` 等），将普通值传递给 `@spaces.GPU` 函数。

### 跨 fork 的 `gr.State`

`gr.State` 在每次 yield 时被 pickle。处理器接收一个**副本**：

- fork 内的原地变更对其他处理器不可见，除非你显式将变更后的值 `yield` 回去。
- 为状态 slot yield `gr.update()` **会跳过**该更新 — 其他处理器继续看到 yield 前的值。
- 对于大型状态，最小化 yield 它的频率 — 理想情况下仅在末尾 yield 一次。
- 状态中的 CUDA 张量在 yield 之前必须转为 CPU（同样的 `_lazy_init` 问题）。

## 生成器和流式传输

`@spaces.GPU` 支持生成器函数 — 渐进式 UI 更新的首选：

```python
@spaces.GPU(duration=120)
def generate(prompt):
    yield gr.update(value=None, label="Starting…")
    for step in range(num_steps):
        latent = step_fn(...)
        yield gr.update(value=preview(latent), label=f"Step {step+1}/{num_steps}")
    yield gr.update(value=final_image, label="Done")
```

`gr.Progress(track_tqdm=True)` 和 `yield` 相互竞争 — 选择一个。

对于 diffusers `callback_on_step_end` **内部**的流式预览，在装饰器内部使用线程 + 队列（forks 共享线程）：

```python
@spaces.GPU(duration=180)
def generate(prompt, num_steps):
    q = queue.Queue()
    DONE = object()
    def cb(pipe, step, t, kw):
        q.put((step, taef1_preview(kw["latents"])))
        return kw
    def run():
        out = pipeline(prompt=prompt, num_inference_steps=num_steps,
                       callback_on_step_end=cb,
                       callback_on_step_end_tensor_inputs=["latents"])
        q.put((DONE, out))
    threading.Thread(target=run, daemon=True).start()
    while True:
        idx, payload = q.get()
        if idx is DONE: break
        yield gr.update(value=payload, label=f"Step {idx+1}/{num_steps}")
```

**不要**在 `@spaces.GPU` 内使用 `ProcessPoolExecutor` / `multiprocessing.Pool` — 守护进程 fork 无法产生子进程（`AssertionError: daemonic processes are not allowed to have children`）。仅使用线程。

## 编译

`torch.compile` 在 ZeroGPU 上**不支持**。使用 PyTorch ahead-of-time inductor（AoTI），从 torch 2.8+ 开始支持。完整指南：https://huggingface.co/blog/zerogpu-aoti。`spaces` 包暴露 `aoti_capture`、`aoti_compile`、`aoti_apply`、`aoti_blocks_load` 用于该工作流。

## 本地开发

**不要**用 `try/except` 包装 `import spaces` 并使用 no-op 回退。在 ZeroGPU 之外，`spaces` 包*已经*是真正的 no-op — 重型行为由 `SPACES_ZERO_GPU=1` 控制，仅在 ZeroGPU 上设置。`@spaces.GPU` 在其他地方返回未装饰的函数不变。Gradio 基础镜像在每个硬件等级上都安装了 `spaces`，因此在 T4 / A10G / CPU 上的副本无需代码更改也能工作。

也就是说：**在 Space 上迭代，而不是本地。** Space 环境（Python、torch、CUDA、驱动程序、环境变量）与你的不同；通过本地测试不能证明 Space 工作。尽早推送 — 即使应用尚未完全完善 — 并使用阶梯（[`debugging.md`](debugging.md)）针对实时 URL。

## 内存压力的分配器配置

如果你的工作负载遇到瞬时分配峰值（高分辨率像素空间操作、大型注意力激活、SR 模型、视频 DiT）并看到：

```
RuntimeError: NVML_SUCCESS == r INTERNAL ASSERT FAILED at .../CUDACachingAllocator.cpp
```

在 `app.py` 的**最顶部**设置可扩展段，任何 torch import 之前：

```python
import os
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
import spaces
import torch
```

通常对看似 OOM 的问题是单行修复。参见 [`known-errors.md`](known-errors.md)。

## 示例缓存

ZeroGPU 上 `gr.Examples` 的默认值：

- `cache_examples=True`
- `cache_mode="lazy"`（eager 会在启动时预运行示例，但启动时没有附加 GPU）

不要在 ZeroGPU 上将其覆盖为 `cache_mode="eager"` — 它会失败或耗尽创建者的每日配额。缓存由示例的**文件路径**（而非内容哈希）键控：原地重新生成资产会提供陈旧的缓存输出。如果要替换示例文件，请提升 `cache_version` 常量。

## 实时会话

对于实时应用（网络摄像头、音频流），每调用 fork 模型过于昂贵。ZeroGPU 支持可复用的"实时会话" — 一个 GPU 分配在许多小请求间摊销。参考 Spaces：

- https://huggingface.co/spaces/diffusers/unofficial-SDXL-Turbo-i2i-t2i
- https://huggingface.co/spaces/huggingface-projects/rf-detr-realtime-webcam

## 当事情出错时

对于特定错误字符串（CUDA init 顺序、illegal duration、分配器断言、PicklingError、返回 CUDA 张量……）：[`known-errors.md`](known-errors.md)。它涵盖了 ZeroGPU 特定模式以及所有其他内容，是本技能的唯一错误查询位置。

当日志端点无法解释失败（设备端断言、特定 shape 下的 OOM、pickle 中的竞争条件）时，dev 模式 + SSH 是最后手段工具 — 参见 [`debugging.md`](debugging.md)。