# 适配 demo 到特定的 LoRA

任务类别（T2I、I2I、T2V、I2V、V2V）为你提供一个起始形状。它不能给你一个 UI。同一任务类别中的两个 LoRA 可能需要非常不同的 demo。本文件是关于从"我知道任务"到"我知道这个 demo 应该是什么样子"的推理。

## 核心问题

对于每个 LoRA，问：**这个 LoRA 实际上需要用户提供什么，用户提供的最自然方式是什么？**

这些是不同的问题。模型可能需要姿态视频作为条件。这并不意味着用户必须提供姿态视频——他们可以提供常规视频，由 demo 从中提取姿态。模型可能需要黑边视频用于外绘。这并不意味着用户上传预先加黑边的视频——他们上传正常视频并选择宽高比，由 demo 添加边框。

demo 的工作是在用户拥有的（视频、照片、想法）和模型需要的（姿态条件、加 padding 的帧、带 mask 的潜变量、前缀了触发词的 prompt）之间进行翻译。

## 解读 LoRA 需要的内容

来源，按有用程度排序：

1. **模型卡的示例代码片段——用于 *参数*。** 如果 README 有一个 Python 块显示如何调用 LoRA，信任其推理参数：pipeline 类、步数、guidance scale、true CFG、LoRA scale、dtype、分辨率、负向 prompt。信任其输入：如果它传入 `image=...`，则 demo 接受图像；如果它传入 `image=...` 和 `mask_image=...`，则 demo 需要两者。

   **对于 *加载机制*，将片段视为信号而非指令。** 优先使用标准的 diffusers 路径：`pipe.load_lora_weights(repo_id, weight_name=...)`。这是经过维护且经过良好测试的路径，当 diffusers + PEFT 足够新时，它处理 DoRA、rsLoRA、自定义 target modules 和大多数格式变体。如果模型卡使用其他方式——`PeftModel.from_pretrained(pipe.transformer, ...)`、`diffsynth_engine`、自定义导入、手动 state-dict 手术——这是调查的标志，而不是复制的标志。

   模型卡作者采用非标准加载路径的原因通常不通用：训练时的约定、环境怪癖（旧版 diffusers/PEFT 版本、CPU offload 模式），甚至是格式错误的配置在其设置中静默通过但在别处崩溃。（真实示例：一个 `adapter_config.json` 中有 `task_type: "DIFFUSION"` 在某些 PEFT 版本上本地工作但在当前 PEFT 上崩溃，因为 PEFT 的 `TaskType` 枚举只包含 NLP 任务；diffusers 的加载器通过直接读取 safetensors 来绕过此验证。）

   自定义推理路径在 ZeroGPU 上确实 *可以* 工作（LTX-2.3 本机 pipeline 是一个真实的例子）。但默认使用 diffusers，因为它是标准的、最新的、经过维护的路径。只有在 `load_lora_weights` 明显无法处理此 LoRA 时才采用模型卡的加载方式——如果采用，则将其移植到 ZeroGPU 约束（模块级 `.to('cuda')`，不使用 `enable_model_cpu_offload`）。

2. **触发词和 prompt 模式。** "在 prompt 开头使用触发词 X" → 自动将 `X` 前置到用户的 prompt，而不是要求他们输入。"Prompt 应将场景描述为 Y" → 添加 prompt 格式示例或占位符。如果 LoRA 期望嵌入在 prompt 中的结构化输入（如边界框坐标或命名区域），UI 应为用户生成该结构，而不是要求他们直接输入。

3. **仓库中的示例媒体。** 示例输出告诉你 LoRA 做什么。示例输入告诉你用户必须提供什么。*配对* 的输入+输出示例（输入视频 → 输出视频、输入图像 → 输出图像）告诉你转换是什么。将这些提升到 `gr.Examples` 中，以便用户可以点击浏览。

4. **模型的任务族。** 姿态条件模型需要姿态图。深度条件模型需要深度图。外绘模型需要带 mask 区域的加 padding 帧。每个都暗示预处理。

5. **推荐的超参数。** 步数、guidance scale、true CFG、LoRA scale。将推荐值作为默认值烘焙进去。仅当 LoRA 的行为在一定范围内对值敏感时才暴露滑块（例如 LoRA scale 0.7–1.3 产生明显不同的结果）；否则只是杂乱。

当模型卡没有这些内容时，你有三种选择：

- **从先例推断。** 如果相同基础模型存在类似的 LoRA，请研究它们的 demo。
- **询问用户。** 一次性、批量询问，带具体问题："这个 LoRA 有触发词吗？推荐的步数是多少？有示例 prompt 吗？"
- **使用基础模型的合理默认值。** 比前两种差；仅当其他方法都不可用时才回退到此。

## 验证 pipeline 类

pipeline 类在阶段 2 中决定，而不是在这里。程序（阅读基础模型自身的卡片，信任其 diffusers 代码片段胜过参考表）在 `SKILL.md` 的"阶段 2 — 选择基础 pipeline"中。在此提及作为指针，因为跳过该验证是发布破损 Space 的最常见方式之一——如有疑问，请重新阅读阶段 2。

## 从"LoRA 需要什么"到 UI 形状

对于 LoRA 期望作为输入的每个事物，决定：

- **用户从哪里获得这个？** 姿态视频——从常规视频提取，或接受预提取的姿态视频，或两者都接受？宽高比——选择器、宽/高滑块，或从输入自动？参考图像——单独的槽位，或嵌入"拖放到此处"区域？

- **是否可以将更自然的输入转换为这个？** 几乎总是可以。用户有视频，而不是姿态视频。用户想要"更宽"，而不是"在这些特定坐标处填充黑条"。demo 弥补了这一差距。

- **是否应向用户显示中间结果？** 通常是——姿态提取预览、letterbox 预览、生成的 mask 预览。显示中间结果建立信任（"是的，模型正在按我预期的那样进行条件处理"）并帮助用户迭代。但每次用户更改设置都需要 10 秒才能生成的预览比没有预览更糟糕。

- **允许用户实际驱动这个 LoRA 的最小控件集是什么？** 超出此范围的都是杂乱。一个只擅长一种特定转换的 LoRA 可能只需要一个输入槽位和一个生成按钮。

## 推理应用的示例

**姿态控制视频 LoRA（V2V）。**
模型以姿态视频为条件。用户拥有常规视频。demo 接受视频，提取姿态，可选地接受外观参考图像（用于"角色看起来像 *这个*，做 *那个* 动作"），运行推理，返回视频。姿态提取显示为预览，以便用户知道正在使用什么。宽高比选择器无关紧要——输出与源匹配。

**外绘视频 LoRA（V2V）。**
模型填充带黑边的帧。用户有视频并希望它更宽/更高。demo 接受视频，接受目标宽高比（下拉菜单：16:9、9:16、1:1 等），用黑边 padding 帧到该宽高比，显示加 padding 的第一帧的预览，运行推理。没有外观参考——LoRA 的工作是扩展，而不是转换。如果 LoRA 的模型卡提到伽马校正有助于暗场景，则将其作为 Advanced 切换公开。

**重新打光图像 LoRA（I2I）。**
模型基于 prompt 重新打光。用户有照片和想要的光照想法。demo 接受图像，接受画布画笔（用户在其中绘制彩色笔触以指示光源位置），接受光照风格下拉菜单（"golden hour"、"neon"、"studio"），接受可选的背景更改，构建 prompt，运行推理。画笔颜色和位置成为结构化的 prompt 内容。

**风格图像 LoRA（T2I）。**
模型以特定风格生成图像。用户有 prompt。demo 接受 prompt（自动前置触发词），接受宽高比，运行推理。这就是整个 UI。没有参考图像，没有画布，没有预处理——LoRA 完成工作。

**边界框拖放 LoRA（I2I）。**
模型在图像上绘制的两个边界框之间移动和调整对象大小。用户有图像和意图（"将那个花瓶从这里移到那里"）。demo 接受图像，允许用户使用自定义画布组件直接在图像上绘制两个框（红色源框、绿色目标框），运行推理。框成为模型期望的结构化输入。

**保留身份的 I2V。**
模型在保留身份的同时为角色制作动画。用户有静态照片和动作意图。demo 接受图像（角色），接受 prompt（动作），运行推理。如果模型还接受驱动视频作为动作，则将其作为替代输入模式而不是第二个必需输入公开。

所有这些中的模式：从用户 *拥有* 什么和他们 *想要* 什么出发，构建弥合到模型需要什么的 UI。

## 改变 UI 形状的因素

来自模型卡或 LoRA 行为的信号，应改变 UI：

- **少步推理（≤ 8 步）。** 隐藏步数滑块——在这种状态下模型是配方锁定的。CFG 通常也是 1.0。锁定这些默认值而不是公开它们。
- **推荐的 LoRA scale ≠ 1.0** 或对 scale 敏感的行为。公开一个以推荐值为中心的 LoRA scale 滑块。
- **多个参考输入。** 两个图像槽位，清晰标记（例如"appearance"和"pose source"），并有帮助文本解释每个的角色。
- **可选输入。** 明确将可选项设为可选——占位符文本、标签中的"(optional)"，demo 可在没有它的情况下运行。
- **多阶段 pipeline**（例如 extract + generate、generate + refine）。显示阶段进度（`progress(0.3, desc="Extracting pose...")` 然后 `progress(0.6, desc="Generating...")`）。否则用户在长时间生成期间盯着空白进度条。
- **输出是视频 > 5 秒。** 提高 `@spaces.GPU(duration=...)` 并在 UI 中警告用户生成需要更长时间。
- **LoRA 期望结构化的 prompt 内容**（坐标、区域标签、命名实体）。构建一个生成该结构的小 UI，而不是要求用户直接输入。

## 不改变 UI 形状的因素

- 基础模型身份，仅用于确定 pipeline 类。Qwen-Image 风格 LoRA 和 Flux 风格 LoRA 可以有相同的 UI。
- 纯性能细节（dtype、device map、attention 实现）。这些属于模型加载代码，不属于 UI。
- LoRA 的训练数据组成。有趣，但不是承重墙。

## LoRA 加载失败时

当 `pipe.load_lora_weights(...)` 失败时，正确的做法是阅读错误并识别失败的 *类别*。每个类别有不同的修复路径。不要猜测——不同的错误对 LoRA 在 diffusers 路径上是否仍然可恢复意味着不同的事情。

**不要预防性地调用转换实用程序。** `load_lora_weights` 已经在内部为它知道的格式调用适当的转换器。在没有错误之前调用 `convert_state_dict_to_diffusers` 或类似工具在常见情况下是多余的，并且如果你猜错了会有风险——你可能会破坏本可以正常加载的 state dict。

失败类别：

- **配置验证失败**（错误提到 `task_type`、`peft_type`、"Invalid task type"、`PeftConfig`，或来自 `peft/config.py` 的任何内容）：safetensors 权重本身可能没问题；`adapter_config.json` 是问题所在。修复路径：显式传递 `weight_name=` 以便 `load_lora_weights` 直接读取 safetensors 而不经过 PEFT 的严格配置解析器；或下载 safetensors 并通过 state dict 加载。回退到 `PeftModel.from_pretrained` *不会* 有帮助——该路径在相同的配置上崩溃。

- **缺失键 / 意外键**（"Loading adapter weights from state_dict led to missing keys" 或 "led to unexpected keys"）：state dict 的键命名与 diffusers 加载器期望的不匹配。这通常意味着 LoRA 使用非 diffusers 约定（kohya、ComfyUI、OneTrainer、自定义训练脚本）训练，或使用自定义 target modules。修复路径：尝试 diffusers 的内置转换实用程序（`convert_state_dict_to_diffusers`、`diffusers.loaders` 中特定于基础模型的转换器）；如果这些没有帮助，格式可能尚未支持——向用户清晰地说明这一点，而不是静默使用部分加载。

- **形状不匹配错误**：LoRA 的张量形状与基础模型的不匹配。通常意味着 LoRA 是针对与正在使用的基础模型不同的变体训练的（例如在 Qwen-Image-Edit 上训练但加载到 Qwen-Image，或在 FLUX.1-dev 上训练但加载到 FLUX.1-schnell）。修复：仔细检查模型卡的 `base_model` 字段并切换到正确的基础。

- **加载或首次推理期间的 OOM**：这并非真正的加载失败——LoRA 已加载但合并的基础 + LoRA + activations 不适合。修复路径涉及 `pipe.enable_vae_tiling()`、更小的分辨率、FP8/量化基础变体。不在本节范围内。

- **某些权重缺失键**（例如文本编码器 LoRA 缺失但 transformer LoRA 存在）：通常是一个仅针对一个组件的部分覆盖 LoRA。可能实际上是有意的并且可能仍然有效——生成测试图像并查看 LoRA 效果是否存在。

当这些都不适用且 `load_lora_weights` 根本不起作用时，回退到非 diffusers 路径成为一个真正的选择。此时模型卡的片段变得更有用——但要移植到 ZeroGPU 约束（不使用 `enable_model_cpu_offload`、模块级 `.to('cuda')`、模型在 `@spaces.GPU` 之外的 `cuda` 上）。