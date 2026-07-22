# LTX 参考

LTX 系列涵盖 `LTX-Video`（0.9.x 系列）、`LTX-2` 和 `LTX-2.3`。它们都针对 text-to-video、image-to-video 和 video-to-video。

Diffusers 支持在不同版本之间有所不同：

| 基础模型系列         | Diffusers 支持                        | 通过 diffusers 加载 LoRA？ |
|---------------------------|------------------------------------------|-----------------------------|
| `Lightricks/LTX-Video` (0.9.x) | 是 — `LTXPipeline`、`LTXImageToVideoPipeline`、`LTXConditionPipeline` | 是 |
| `Lightricks/LTX-2`        | 是 — 来自 `diffusers.pipelines.ltx2` 的 `LTX2Pipeline` | 是（最近的 diffusers） |
| `Lightricks/LTX-2.3`      | 部分 — diffusers 支持整体仍然有限，因此原始的 `Lightricks/LTX-2.3` 仓库仍可通过本机路径使用。Diffusers 转换的变体存在于 `dg845/LTX-2.3-Diffusers` 和 `dg845/LTX-2.3-Distilled-Diffusers`，支持通过标准 pipeline 的常规 LoRA、通过 `LTX2InContextPipeline` 的 IC LoRA，以及通过 `LTX2HDRPipeline` 的 HDR IC-LoRA（PR #13572，2026-05-15 合并；需要 `git+https://github.com/huggingface/diffusers`） | 在 diffusers 变体上是 — 标准 `load_lora_weights` + `set_adapters`。某些配置仍需要本机路径。 |

当对 LTX-2.3 有疑问时，请检查 LoRA 的模型卡以获取示例片段。如果它从 `ltx_video` 或本机模块导入而不是从 `diffusers`，请使用本机路径。

## Pipelines（diffusers 路径）

> **在使用此表之前，请根据基础模型在 Hub 上的自身卡片进行验证。** 此表是尽力而为的，可能滞后于最新发布（LTX 发展很快）。基础模型 Hub 页面上的 diffusers 代码片段是权威来源。程序请参见 `SKILL.md` 阶段 2。

| 任务                    | Pipeline                          | Pretrained ID                                        |
|-------------------------|-----------------------------------|------------------------------------------------------|
| Text-to-video           | `LTXPipeline`                     | `Lightricks/LTX-Video`                               |
| Image-to-video          | `LTXImageToVideoPipeline`         | `Lightricks/LTX-Video`                               |
| Video-to-video / 关键帧 | `LTXConditionPipeline`         | `Lightricks/LTX-Video-0.9.5` 或更高                |
| 空间放大         | `LTXLatentUpsamplePipeline`       | `Lightricks/ltxv-spatial-upscaler-0.9.8`             |
| LTX-2 T2V/I2V           | `LTX2Pipeline`                    | `Lightricks/LTX-2`                                   |
| LTX-2.3 in-context (IC LoRA) | `LTX2InContextPipeline`     | `dg845/LTX-2.3-Distilled-Diffusers`（推荐用于 demo；非蒸馏的 `dg845/LTX-2.3-Diffusers` 也可用） |

`LTXConditionPipeline` 是 V2V 的主力——它接受一个 `LTXVideoCondition`（或列表）加上可选的第一帧图像，并产生以输入为条件的视频。

## 必需依赖项

LTX pipeline 需要超出标准 diffusers/transformers/peft 集合的额外内容，因为视频输出需要文件格式支持：

- **`imageio`** 和 **`imageio-ffmpeg`** — `diffusers.utils.export_to_video` 所必需。没有它们，即使模型加载成功，视频导出会运行时失败。始终包含两者。
- **`sentencepiece`** — 某些 LTX 变体使用的 T5 文本编码器所必需。如果在启动时看到与 tokenizer 相关的 ImportError，请包含它。
- **`av`** — `pyav`，在读取非平凡格式的输入视频时有用。包含用于通过 `load_video` 接受视频输入的 V2V pipeline。

对于 LTX-2 和 LTX-2.3，通常需要来自 git 的最新 diffusers，因为 pipeline 类（`LTX2Pipeline`、conditioning API）在 pip 发布之前就已经存在：

```
git+https://github.com/huggingface/diffusers
```

对于 LTX-2.3 本机路径：

```
git+https://github.com/Lightricks/LTX-Video.git
```

如果 `from_pretrained` 对于最近的 LTX 变体失败并报类未找到错误，请切换到 git diffusers。

## 默认加载（T2V）

```python
import torch
from diffusers import LTXPipeline
from diffusers.utils import export_to_video

pipe = LTXPipeline.from_pretrained(
    "Lightricks/LTX-Video",
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")
pipe.load_lora_weights("user/my-ltx-lora")
```

## 默认加载（通过 LTXConditionPipeline 的 V2V）

```python
import torch
from diffusers import LTXConditionPipeline
from diffusers.pipelines.ltx.pipeline_ltx_condition import LTXVideoCondition
from diffusers.utils import load_video, export_to_video

pipe = LTXConditionPipeline.from_pretrained(
    "Lightricks/LTX-Video-0.9.5",
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")
pipe.load_lora_weights("user/my-ltx-vlora")

video = load_video("input.mp4")
condition = LTXVideoCondition(video=video, frame_index=0)

frames = pipe(
    conditions=[condition],
    prompt="...",
    negative_prompt="worst quality, jittery, blurry",
    width=768, height=512,
    num_frames=121,
    num_inference_steps=50,
).frames[0]
export_to_video(frames, "out.mp4", fps=24)
```

## LTX-2（diffusers 路径）

```python
from diffusers.pipelines.ltx2 import LTX2Pipeline
pipe = LTX2Pipeline.from_pretrained("Lightricks/LTX-2", torch_dtype=torch.bfloat16)
```

LTX-2 支持两阶段 pipeline（基础 + 潜变量放大）以获得生产质量。对于 demo，单阶段 pipeline 通常足够且更快。

**不要默认为 IC-LoRA 启用两阶段 —— 检查模型卡。** 常见的 LTX-2.3 两阶段配方将阶段 2 作为 x2 潜变量放大 + 细化运行，**禁用 IC-LoRA**（`disable_lora()`），在裸基础上重新渲染 —— 这重新降级了 LoRA 条件化的细节（文本、身份）。两阶段是否合适是按 LoRA 而定的，根据模型卡：例如 *In/Out-painting* 模型卡明确表示"两个任务都使用两阶段 pipeline"，而 *Ingredients* 模型卡推荐单次 30 步配方且从不提及两阶段。单阶段是更安全的 demo 默认，除非模型卡要求两阶段。

## 推理默认值

- **分辨率**：通常是 32 的倍数。常见尺寸：768×512、1216×704、704×480。
- **帧数**：通常 `8k+1`（例如 121、161、257）。从 `duration_seconds * fps` 计算并四舍五入。
- **fps**：默认为 24；一些 LoRA 以不同的速率训练（16、30）—— 检查模型卡。
- **`num_inference_steps`**：非蒸馏为 30–50。蒸馏 checkpoint（名称中查找"distilled"）通常以 8–12 运行。
- **`negative_prompt`**：LTX 对负向 prompt 敏感。一个好的默认值：`"worst quality, inconsistent motion, blurry, jittery, distorted"`。
- **蒸馏 IC-LoRA — 也要禁用音频 guidance，而不仅仅是 `guidance_scale`。** `LTX2InContextPipeline` 计算 `do_classifier_free_guidance = guidance_scale > 1 OR audio_guidance_scale > 1`，并且 **`audio_guidance_scale` 默认为 `7.0`**。因此 `guidance_scale=1.0` 是不够的 —— CFG 通过音频保持开启（并且 `stg_scale` 默认开启），这使得相对于 in-context 参考 token 的前向传递加倍/错误批处理（错误的配方，有时是运行时错误）。对于蒸馏的 IC-LoRA，请传递所有四个：`pipe(..., guidance_scale=1.0, stg_scale=0.0, audio_guidance_scale=1.0, audio_stg_scale=0.0)`。

## 帧数辅助函数

```python
def num_frames_for_duration(seconds, fps=24, base=8):
    raw = seconds * fps
    return ((int(raw) - 1) // base) * base + 1
```

## 本机 pipeline 路径（LTX-2.3 后备）

当 diffusers 路径不起作用时，或者对于 diffusers 可能尚不支持的特定条件，本机仓库是后备。首先尝试在 diffusers 路径上使用 `LTX2InContextPipeline`（参见上面的 IC-LoRA 部分）。

**本机仓库取决于模型生成 —— 根据 LoRA 的基础模型（以及其模型卡片段的导入）选择：**

| 基础模型 | 本机仓库 | 包 / 导入 | Pipeline 类 |
|---|---|---|---|
| `LTX-Video` (0.9.x) | `github.com/Lightricks/LTX-Video` | `ltx_video` | `from ltx_video.pipelines import LTXPipeline` |
| `LTX-2`、`LTX-2.3` | `github.com/Lightricks/LTX-2` | `ltx-core` + `ltx-pipelines`（可编辑） | `ltx_pipelines.ic_lora.ICLoraPipeline`、`TI2VidOneStagePipeline`、… |

对于 0.9.x 系列，模式如下所示：

```bash
# in requirements.txt
git+https://github.com/Lightricks/LTX-Video.git
```

```python
from ltx_video.pipelines import LTXPipeline as NativeLTXPipeline
# ... model loading per the native repo's README
```

本机路径不使用 `load_lora_weights`。相反，LoRA 通常在 pipeline 构造时接入，通常通过 LoRA 配置列表或通过指向融合的 checkpoint。

当 LoRA 的模型卡有一个使用本机仓库的 Python 片段时，请按字面复制其构造模式。本机 API 比 diffusers 的 API 变化更频繁，所以不要释义。

### ZeroGPU 上的 LTX-2.x 本机路径 — 陷阱

对于 `LTX-2` / `LTX-2.3`（`ltx-core` + `ltx-pipelines` 仓库），在运行时在 `app.py` 中克隆 + `pip install -e packages/ltx-core packages/ltx-pipelines` 并固定提交。在 ZeroGPU 上有三件事会引起问题：

- **本机加载器绕过 ZeroGPU 虚拟化 → 启动时出现"No CUDA GPUs available"。** 本机 safetensors 加载器执行 `safe_open(path, device="cuda")` 并在 safetensors 自己的 C++ 内复制 host→device（`cudaMemcpy`），**绕过 `torch.Tensor.to`** —— ZeroGPU 修补以虚拟化 + 打包模块作用域权重的调用。没有任何东西打包，模块作用域放置引发 *"No CUDA GPUs are available."* 修复：monkeypatch 加载器以在 CPU 上打开然后使用 `.to` 移动：
  ```python
  with safetensors.safe_open(shard, framework="pt", device="cpu") as f:
      value = f.get_tensor(name).to(device=device)   # torch path → ZeroGPU-virtualisable
  ```
  还要：将 attention 修补为 **SDPA**（FA3 在 Blackwell ZeroGPU 上崩溃），并且**永远不要在模块作用域调用 `torch.cuda.*` / `get_device_capability()`**（它会污染虚拟化）。
- **本机两阶段固定两个 22B transformer → offload-disk 溢出。** `ICLoraPipeline` 构建两个独立的 `ModelLedger`（阶段 1 带有 LoRA，阶段 2 不带），每个加载其**自己的**完整 transformer。CLI 按顺序加载它们，但 ZeroGPU 在模块作用域固定所有权重，因此启用阶段 2 会固定**两者**（约 143G）并使 offload disk 溢出（`OSError: [Errno 28] No space left on device`，约 96G 上限）。对于 demo：固定阶段 1，然后让阶段 2 **重用阶段 1 的固定模块**（`for n in [...]: setattr(s2, n, getattr(s1, n))`），以便只有一个 transformer 常驻（约 71G）。
- **`ICLoraPipeline` 仅限蒸馏。** 根据 LTX-2 `ltx-pipelines` 指南，IC-LoRA 推理以仅蒸馏模式运行（固定的 8 步 sigmas，没有 `num_inference_steps`/`guidance_scale`/`negative_prompt`）；文档未描述非蒸馏 IC-LoRA 或 IC-LoRA + CFG/STG（guidance 仅存在于完整模型 pipeline（如 `TI2VidOneStagePipeline`）上，在两阶段中仅存在于阶段 1）。因此，如果模型卡推荐 *非蒸馏* 配方（例如在 `…-dev` 基础上有 30 步 + guidance + STG），则没有适用于它的现成 IC-LoRA pipeline —— 使用支持的蒸馏 `ICLoraPipeline` 并注意配方差异，或回退到 diffusers `LTX2InContextPipeline`（它公开 steps/guidance）。

## IC-LoRA（in-context 条件化）

LTX IC-LoRA 将模型条件化为参考视频以及第一帧图像。diffusers 路径使用 `LTX2InContextPipeline` 与标准 `load_lora_weights` + `set_adapters`。

常见类型：

- **姿态 / 深度 / canny IC-LoRA**：参考视频必须在作为条件传递之前预处理为控制信号（姿态骨架、深度图、边缘图）。传递具有外观信息的原始视频会泄漏颜色/风格。
- **外绘 IC-LoRA**：输入视频用黑边 padding 到目标宽高比并作为条件传递。模型填充黑色区域。
- **帧插值 / 扩展 IC-LoRA**：输入是一组稀疏的关键帧；模型填充中间或扩展。
- **音频驱动的唇形同步 IC-LoRA**：接受参考视频和新音轨；模型重新同步唇部动作以匹配新音频。UI 需要视频输入和音频输入（例如用于视频翻译、画外音替换、多语言配音）。

每个都意味着 demo 中不同的预处理和不同的 UI 形状（用于外绘的宽高比选择器、用于姿态控制的姿态预览、用于关键帧扩展的帧对输入）。阅读 `references/adapting-to-the-lora.md` 并将 UI 塑形为特定的 IC-LoRA。

## 量化陷阱（仅限 LTX-2.3 本机路径）

在本机路径上，一些 LTX-2.3 IC-LoRA 附带 FP8 量化策略，在模型加载时使用 Triton CUDA kernel 将 LoRA delta 融合到 transformer 权重中。ZeroGPU 在模块加载时没有真正的 CUDA（只有仿真层）—— 这可能会在启动时崩溃 Space。diffusers 路径通过 `LTX2InContextPipeline` 不会遇到这种情况：LoRA 通过 PEFT 作为单独的 adapter 权重加载，并在运行时应用，而不是在加载时融合到基础 transformer 中。

当用户在本机路径上遇到此问题时的两种解决方法：

- **跳过 LoRA 融合阶段的量化。** LTX-2.3 具有两阶段 pipeline；仅将量化应用于第二（非 LoRA）阶段。设置 `stage_1_quantization=None`。
- **将 LoRA 预融合到独立 checkpoint。** 下载基础 + LoRA，在开发 GPU 上融合，将融合的 checkpoint 推送到用户命名空间下的 Hub，并让 Space 在没有 LoRA 的情况下加载融合的 checkpoint。

当用户计划重复演示同一 LoRA 时，第二种方法更可取 —— Space 启动快得多。

## LTX 的 ZeroGPU duration 指南

- 短 T2V（3 秒，24fps，蒸馏）：60–90 秒。
- 标准 T2V（5 秒，50 步）：120–180 秒。
- I2V：与相同持续时间的 T2V 类似。
- 带预处理的 V2V（姿态提取等）：为预处理开销添加 10–30 秒。将 duration 设置为 180+。
- LTX-2.3 两阶段：240–360 秒。

将 `@spaces.GPU(duration=...)` 设置为舒适地超过预期生成时间。

## 需要注意的事项

- **最新 pipeline 通常需要 git diffusers。** 对于最近几周发布的任何 LTX 变体，在 `requirements.txt` 中固定到 `git+https://github.com/huggingface/diffusers`。
- **`git+diffusers` 是移动的目标 —— 验证 LTX2 输出质量。** 裸 `@main` 继承那里的任何内容。LTX2 文本连接器存在 token 反转回归（PR #13564），该回归打乱了 prompt token/寄存器 —— 降级 prompt 遵循性和精细细节（例如屏幕上的乱码文本），在短 prompt 上最差 —— 直到 **PR #13931（2026-06-19 合并）** 修复了它。如果 LTX2 输出看起来弱或乱码，请确认已安装的 diffusers 提交 **在 #13931 之后**，并优先固定到已知良好的提交（`git+https://github.com/huggingface/diffusers@<sha>`）而不是裸 `@main`，以实现可复现性。
- **不要 `torch.compile`。** LTX 在 ZeroGPU 上无需它就足够快；编译无论如何都不兼容。
- **`enable_vae_tiling()` 用于更高分辨率。** LTX VAE 内存随分辨率增长；对于任一轴上高于 768px 的输出，启用平铺。
- **负向 prompt 比图像模型更重要。** 除非 LoRA 的模型卡另有说明，否则不要使用空的 negative_prompt 发布。
- **帧率不匹配会产生故障。** 如果 LoRA 以 24 fps 训练而 demo 传递 30，则动作看起来错误。使用 LoRA 的推荐 fps。