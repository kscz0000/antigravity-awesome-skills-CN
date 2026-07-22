# Qwen-Image 和 Qwen-Image-Edit 参考

Qwen-Image 系列在 `diffusers` 中得到完全支持。基础和编辑变体都通过标准的 `load_lora_weights` 接口接受 LoRA。

## Pipelines

> **在使用此表之前，请根据基础模型在 Hub 上的自身卡片进行验证。** 此表是尽力而为的，可能滞后于最新发布。基础模型 Hub 页面上的 diffusers 代码片段是哪个 pipeline 类导入的权威来源。程序请参见 `SKILL.md` 阶段 2。

| 基础模型                            | Pipeline 类                | 任务                                |
|---------------------------------------|-------------------------------|-------------------------------------|
| `Qwen/Qwen-Image`                     | `QwenImagePipeline`           | Text-to-image                       |
| `Qwen/Qwen-Image-Edit`                | `QwenImageEditPipeline`       | 图像编辑（指令驱动）  |
| `Qwen/Qwen-Image-Edit-2509`           | `QwenImageEditPlusPipeline`   | 图像编辑，多图像输入    |
| `Qwen/Qwen-Image-Edit-2511`           | `QwenImageEditPlusPipeline`   | 图像编辑，最新变体       |

2509 和 2511 变体使用与原始 `QwenImageEditPipeline` *不同的* pipeline 类 — 它们接受输入图像列表并具有不同的默认参数。不要假设同一系列中的变体共享一个 pipeline 类。针对 2511 训练的 LoRA 加载到 `QwenImageEditPipeline` 上会产生错误输出；失败是静默的（没有异常），因此对照基础模型卡验证是捕获它的唯一方法。

2511 变体将几个流行的社区 LoRA 集成到基础中，这可能意味着针对早期 Qwen-Image-Edit 训练的 LoRA 在加载到 2511 上时行为会微妙地不同；如果 LoRA 的模型卡指定了它训练于哪个 Edit 变体，请匹配它。

## 必需依赖项

Qwen-Image 和 Qwen-Image-Edit pipeline 需要超出标准 diffusers/transformers/peft 集合的额外内容，因为文本编码器是 `Qwen2_5_VLForConditionalGeneration`（Qwen 2.5-VL）：

- **`torchvision`** — `Qwen2VLVideoProcessor` 所需，文本编码器的处理器传递性地引入。缺少它会导致启动时的 `ImportError`（"Qwen2VLVideoProcessor requires the Torchvision library"）。对于任何 Qwen-Image Space，始终包含在 `requirements.txt` 中。
- **`sentencepiece`** — 某些 Qwen tokenizer 路径所需。如果在启动时看到与 tokenizer 相关的 ImportError，请包含它。

特别是 2511 变体通常需要来自 git 的最新 `diffusers`，因为 `QwenImageEditPlusPipeline` 和 2511 特定的修复在 pip 发布之前就已经存在：

```
git+https://github.com/huggingface/diffusers
```

如果 `from_pretrained("Qwen/Qwen-Image-Edit-2511", ...)` 失败并报类未找到或属性错误，请将需求切换到 git。

## 默认加载（T2I）

```python
import torch
from diffusers import QwenImagePipeline

pipe = QwenImagePipeline.from_pretrained(
    "Qwen/Qwen-Image",
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")
pipe.load_lora_weights("user/my-qwen-lora")
```

`pytorch_lora_weights.safetensors` 是约定的文件名。如果仓库有不同的名称，请传递 `weight_name="..."`。

对于多个 adapter 或当你希望在推理时控制 LoRA scale，请使用 `set_adapters`：

```python
pipe.load_lora_weights("user/my-qwen-lora", adapter_name="mylora")
pipe.set_adapters(["mylora"], adapter_weights=[0.9])
```

## 默认加载（图像编辑）

对于原始 `Qwen-Image-Edit`：

```python
import torch
from diffusers import QwenImageEditPipeline

pipe = QwenImageEditPipeline.from_pretrained(
    "Qwen/Qwen-Image-Edit",
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")
pipe.load_lora_weights("user/my-qwen-edit-lora")
```

对于 `Qwen-Image-Edit-2509` 和 `Qwen-Image-Edit-2511`：

```python
import torch
from diffusers import QwenImageEditPlusPipeline

pipe = QwenImageEditPlusPipeline.from_pretrained(
    "Qwen/Qwen-Image-Edit-2511",  # or 2509
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")
pipe.load_lora_weights("user/my-qwen-edit-lora")
```

`QwenImageEditPlusPipeline` 接受 `image=<PIL>` 或 `image=[<PIL>, <PIL>, ...]` 用于多图像编辑。`QwenImageEditPipeline` 接受单个图像。两个之间的默认参数略有不同 —— 参见下面的"推理默认值"。

## 推理默认值

对于非蒸馏的 Qwen-Image：
- `num_inference_steps`：默认 50；LoRA 的模型卡可能推荐更低。
- `true_cfg_scale`：典型 4.0。
- `width`/`height`：16 的倍数，理想情况下长轴为 1024 或 1328。

对于 Qwen-Image-Edit（原始）：
- `num_inference_steps`：通常 30–50，蒸馏变体通常更少。
- `true_cfg_scale`：典型 4.0。
- 输入图像在内部调整大小；传递合理的分辨率（长边 1024px）即可。

对于 Qwen-Image-Edit-2509 / 2511（`QwenImageEditPlusPipeline`）：
- `num_inference_steps`：2511 典型为 40；2509 为 50。
- `true_cfg_scale`：4.0。
- `guidance_scale`：1.0（新 pipeline 使用 `true_cfg_scale` 作为活动 CFG；标准 `guidance_scale` 保持在 1.0）。
- 输入是一个或多个 PIL 图像的列表。

对于 Lightning / 少步 LoRA（例如 `lightx2v/Qwen-Image-Lightning-*`）：
- `num_inference_steps`：4 或 8（阅读 LoRA 的模型卡 —— 它们提供 4 步和 8 步变体）。
- `true_cfg_scale`：通常 1.0（CFG 禁用）。
- 通常带有自定义调度器配置 —— 参见 lightx2v README 以获取要使用的确切 `FlowMatchEulerDiscreteScheduler` 配置。

## 分辨率桶

Qwen-Image 使用 16 像素对齐的分辨率。当用户选择宽高比时，将 `width` 和 `height` 计算为 16 的倍数。一个辅助函数：

```python
def round_to_bucket(w, h, multiple=16):
    return (w // multiple) * multiple, (h // multiple) * multiple
```

对于图像编辑 pipeline，在保留宽高比的同时将输入图像调整到最近的桶；不要裁剪。

## ZeroGPU duration 指南

- 1024×1024 的标准 50 步 Qwen-Image T2I：60–90 秒。
- 4 步 Lightning Qwen-Image：15–25 秒。
- Qwen-Image-Edit 30 步：60–90 秒。

相应地设置 `@spaces.GPU(duration=...)`。

## Qwen-Image 上的常见 LoRA 模式

- **风格 LoRA（T2I）。** 标准加载。通常存在触发词。UI：prompt + 宽高比。
- **主题 / 角色 LoRA（T2I）。** 标准加载。几乎总是存在触发词。UI：在代码中自动前置触发的 prompt，可能有一个突出触发词的示例 prompt。
- **光照 / 美学 LoRA（T2I）。** 通常与推荐的 LoRA scale ≠ 1.0 配对 —— 检查模型卡。
- **编辑 LoRA（image-to-image，在 Qwen-Image-Edit 上）。** 烘焙的具体指令。LoRA 可能需要特定的指令措辞 —— 匹配模型卡的模式。UI：输入图像 + 指令文本框。
- **Lightning 蒸馏 LoRA。** 将步数和 CFG 锁定到推荐值；隐藏滑块。

## 需要注意的事项

- **VAE 内存。** 对于 1328×1328 输出，加载后考虑 `pipe.enable_vae_tiling()` 和 `pipe.enable_vae_slicing()`。对于较小的分辨率，保持关闭以避免质量损失。
- **不要在 ZeroGPU 上编译 transformer。** `torch.compile` 不会工作；ZeroGPU 上的加速选项仅限于减少步数或使用 FP8 蒸馏变体。
- **负向 prompt 起作用**，但默认值通常是空字符串。除非 LoRA 的行为实际上受益，否则不要在 UI 中公开负向 prompt。