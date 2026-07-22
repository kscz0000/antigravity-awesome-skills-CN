# Krea 2 参考

Krea 2（K2）是一个 flow-matching **text-to-image** 模型：一个 12B dense DiT（分组查询注意力）配合 **Qwen3-VL** 文本编码器（多层特征聚合）和 **Qwen-Image VAE**（`AutoencoderKLQwenImage`）。Pipeline 类：`Krea2Pipeline`。它作为两个协同工作的 checkpoint 发布：

| 仓库 | 角色 | 用途 |
|------|------|------|
| [`krea/Krea-2-Turbo`](https://huggingface.co/krea/Krea-2-Turbo) | 8 步 **蒸馏** | **推理 / demo** |
| [`krea/Krea-2-Raw`](https://huggingface.co/krea/Krea-2-Raw) | 基础，非蒸馏 | **LoRA 训练** —— *不* 用于推理 |

**对于 LoRA Space，加载 Turbo。** Krea 2 LoRA 是 *在 RAW 上训练但在 Turbo 上运行*（它们"在 Turbo 上表现强烈"），RAW 明确不是用于推理的——如果直接加载，预计质量较差。因此 demo 几乎总是应使用 `krea/Krea-2-Turbo`。官方 LoRA 卡确认了这一点（"要在 `krea/Krea-2-Turbo` 上使用"）。

> 需要包含 `Krea2Pipeline` 的 `diffusers` 构建（两个仓库均为 `library_name: diffusers`）。如果 `from diffusers import Krea2Pipeline` 失败，则安装的 `diffusers` 早于集成——更新它。

## 必需依赖项

- 包含 `Krea2Pipeline` 的 `diffusers`。
- 足够新的 `transformers` 以支持 **Qwen3-VL**（文本编码器是 `Qwen3VLModel`，例如 `Qwen/Qwen3-VL-4B-Instruct`）。
- **`torchvision`** — Qwen3-VL 处理器传递性地引入；缺少它会导致启动时的 `ImportError`。始终包含它。
- 如果在启动时看到与 tokenizer 相关的 ImportError，则需要 `sentencepiece`。

## 默认加载 + LoRA（Turbo）

```python
import torch
from diffusers import Krea2Pipeline

pipe = Krea2Pipeline.from_pretrained("krea/Krea-2-Turbo", torch_dtype=torch.bfloat16).to("cuda")
pipe.transformer.load_lora_adapter("user/my-krea2-lora", weight_name="my_lora.safetensors")
pipe.transformer.set_adapters("default", weights=1.0)

# include the LoRA's trigger word(s) from its card
image = pipe(
    "a deer grazing in a forest, <trigger words>",
    num_inference_steps=8, guidance_scale=0.0,
    generator=torch.Generator("cuda").manual_seed(0),
).images[0]
```

Krea 2 LoRA 通过 **transformer 的** adapter API 加载（`pipe.transformer.load_lora_adapter(...)` + `pipe.transformer.set_adapters("default", weights=1.0)`），根据官方 LoRA 卡——而不是 pipeline 级别的 `pipe.load_lora_weights`。尊重 LoRA 的 **触发词** 和推荐权重（默认 1.0）。

## 推理配方

- **Turbo（demo 默认）：** `num_inference_steps=8`，**`guidance_scale=0.0`**（禁用 guidance），LoRA 权重 `1.0`。
- **RAW：** 仅用于训练——不要发布 RAW 推理 demo；其质量故意较低（它是可塑的基础，你对其进行微调，然后在 Turbo 上运行）。

## `guidance_scale` 约定（陷阱）

Krea 2 在 **`guidance_scale > 0`** 时启用 guidance，并将速度计算为 `cond + guidance_scale * (cond − uncond)`（≡ 通常的 CFG 公式，scale 为 `1 + guidance_scale`）。因此 Turbo 通过 **`guidance_scale=0.0`** 禁用 guidance——而不是 `1.0`。

## 分辨率

`height`/`width` 必须可被 **16** 整除（`vae_scale_factor * patch_size`）；否则 pipeline 会向上舍入到 16 的倍数（带警告）。默认 1024×1024。

## ZeroGPU duration

标准 T2I：在模块作用域放置模块，`pipe.to("cuda")`，不使用 `torch.compile`。Turbo 8 步 1024² 是快的（≈ 20–40s）——将 `@spaces.GPU(duration=...)` 设置为舒适地超过该值。12B DiT + Qwen3-VL 编码器适合 ZeroGPU；如果在默认大小上 OOM，请尝试 `@spaces.GPU(size="xlarge")`。

## 需要注意的事项

- **对于 demo，加载 Turbo 而不是 RAW。** RAW 是训练基础，不用于推理。
- **`guidance_scale=0` 禁用 guidance**（Krea 约定，与 `1.0` 表示"关闭"的 pipeline 不同）。Turbo = 8 步，`guidance_scale=0.0`。
- **LoRA 使用 `pipe.transformer.load_lora_adapter` + `set_adapters("default", …)`**（transformer 级别），并具有 **触发词** —— 阅读模型卡。
- **新 pipeline → 更新 diffusers** 如果 `from diffusers import Krea2Pipeline` 失败。