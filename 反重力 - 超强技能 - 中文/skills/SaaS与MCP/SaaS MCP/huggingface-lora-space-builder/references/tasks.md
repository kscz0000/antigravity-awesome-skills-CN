# 任务：按任务的基线 UI 模式

本文件描述每个任务类别的 *基线* UI 形状。在确定 LoRA 的任务后使用它，作为起始骨架。然后阅读 `adapting-to-the-lora.md` 以将实际 UI 塑形到特定 LoRA——基线很少是正确的最终答案。

五个任务：text-to-image、image-to-image、text-to-video、image-to-video、video-to-video。

## 所有任务的通用项

- 布局：两列 `gr.Row`，`equal_height=True`。输入在左，输出在右。
- 一个主 `gr.Button("Generate", variant="primary", size="lg")`。除非做有意义不同的事情，否则没有次要按钮。
- 一个 `Advanced` accordion（`gr.Accordion("Advanced", open=False)`）用于高级用户控件，大多数用户永远不会触及（seed、randomize seed、高级采样器参数）。
- 始终包含一个 seed 控件与 "Randomize seed" 复选框，并返回实际使用的 seed 以及结果，以便用户可以复现。
- 连接 `prompt.submit` 以及按钮点击以进行文本输入，因此回车键可以工作。
- 使用 `gr.Progress(track_tqdm=True)` 以显示 diffusers 的内部进度条。

## Text-to-image (T2I)

**输入：** prompt（`gr.Textbox`，`lines=2`，带示例占位符）。宽高比或分辨率控件。可选：用于支持它的模型的负向 prompt。

**输出：** `gr.Image`（如果返回多个则 `gr.Gallery`）。

**标准高级控件：** seed、randomize seed、num inference steps、guidance scale。对于少步 LoRA（Lightning、Turbo、schnell）完全隐藏 steps 和 guidance。

**宽高比处理：** 提供常见宽高比的下拉菜单，宽/高自动派生。将尺寸对齐到模型的原生 bucket 大小（大多数 diffusion transformer 为 16，较旧的基于 UNet 的为 8）。将宽/高显示为只读。

**Examples：** 将示例 prompt 从 LoRA 模型卡提升到 `gr.Examples` 块。使用 `cache_examples=True, cache_mode="lazy"`，以便缓存推迟到首次点击而不是在构建时在 ZeroGPU 上失败。

## Image-to-image (I2I)

**输入：** 输入图像（`gr.Image(type="pil")` 或 `numpy` 取决于你的处理需求）、指令或 prompt（`gr.Textbox`）。

**输出：** `gr.Image`。对于编辑 LoRA，考虑使用 `gr.ImageSlider`（内置）进行前后对比，而不是单独的图像。

**分辨率处理：** 对于指令编辑 pipeline（Qwen-Image-Edit、Flux Kontext、Flux.2 Klein），将输入调整到模型 bucket 大小的最近倍数，保留宽高比。除非 LoRA 期望特定宽高比，否则不要裁剪。

**验证：** 当输入为空时抛出 `gr.Error("Please upload an image first.")`。考虑在加载图像之前禁用 Generate（`run_button.interactive = False`，在 `input_image.change` 上翻转）。

**子任务变体在这里变化很大。** 阅读 `adapting-to-the-lora.md`——重新打光、换脸、对象移动、风格转换、指令编辑、inpainting 都属于"I2I"但需要不同的 UI。

## Text-to-video (T2V)

**输入：** prompt。持续时间滑块（通常 1–10 秒，取决于模型的最大值）。分辨率/宽高比选择器。

**输出：** `gr.Video(autoplay=True)`。设置 `format="mp4"` 并显式选择 fps（24 是安全的默认值；某些模型更喜欢 16 或 30）。

**标准高级控件：** seed、randomize seed、fps。蒸馏视频模型的步骤通常被锁定。

**持续时间感知：** 设置 `@spaces.GPU(duration=...)` 舒适地超过预期生成时间。对于 5 秒 720p 视频，180+ 秒 GPU 时间是现实的。在 UI 中告诉用户生成需要一段时间（"生成 5 秒视频需要约 2 分钟"）。

**帧数计算：** 大多数视频扩散模型希望帧数为 `8k+1` 或类似。从 `duration * fps` 计算 `num_frames` 并四舍五入到最近的有效值，而不是传递任意帧。基础模型参考文件说明每个模型的有效值。

## Image-to-video (I2V)

**输入：** 输入图像（取决于 LoRA，第一帧或风格参考）、描述动作的 prompt。持续时间。

**输出：** `gr.Video`。

**宽高比：** 从输入图像自动检测并对齐到模型的最近 bucket。将所选分辨率显示为信息文本。

**变体：** 一些 I2V LoRA 使用输入图像作为字面第一帧；其他将其用作风格参考并从 prompt 生成新的第一帧。模型卡通常说明哪种。两者的 UI 相似；区别在于如何将 `image=` 传递给 pipeline，以及"用作第一帧"切换是否有意义。

## Video-to-video (V2V)

**输入：** 至少一个源视频。几乎总是还有 prompt。通常根据 LoRA 的功能还有额外输入（外观参考图像、mask、控制视频等）。

**输出：** `gr.Video`。对于在输入上执行预处理（姿态提取、深度估计、padding）的 LoRA，将预处理后的中间结果显示为结果旁边的第二个较小视频，以便用户看到模型实际看到的内容。

**这是适配最重要的地方。** "V2V" 本身几乎不告诉你关于 UI 的任何信息。姿态控制、深度控制、canny 控制、外绘、内绘、风格转换、运动传输、帧插值和放大都是 V2V，都需要不同的 UI。在设计之前始终阅读 `adapting-to-the-lora.md` 和每个基础模型的文件。

**常见模式：**

- 预处理预览：一个小 `gr.Video(height=240)` 显示提取的姿态/深度/canny/加 padding 的视频。在输入更改时更新它，以便用户在单击 Generate 之前看到预处理的结果。
- 运动传输 LoRA 的双输入布局：源视频 + 外观图像，清晰标记。
- 仅当 LoRA 实际更改宽高比（外绘）时才使用宽高比选择器。对于姿态/深度/canny 控制，输出宽高比匹配输入。

## 选择组件

按顺序走过这个阶梯。在适合 LoRA 输入形状的第一级停止。

**1. 内置 Gradio 组件。** 几乎总是首选：

- `gr.ImageSlider` — 内置的前后对比，用于编辑 LoRA。
- `gr.ImageEditor` — 上传 + 在图像上绘画。任何"输入形状"是"通过绘画表达的图像区域"的 LoRA 的正确选择——在红色高亮区域上训练的对象移除、在彩色笔触上训练的重新打光、涂鸦条件编辑。使用 `gr.Brush(default_color="#ff0000", colors=["#ff0000"])` 约束画笔，以便用户只能以 LoRA 训练的颜色绘画；编辑器返回 `{"background", "layers", "composite"}`，`composite` 是你传递给 pipeline 的内容。在生产中由 `linoyts/QIE-2509-Object-Remover-Bbox-v3`（qie-2509-object-remover）使用——不要因为 LoRA 是"用 bbox 训练"而仅为这些任务使用 `gradio_image_annotation`；面向用户的形状是绘制的区域，而不是字面的框。
- `@gr.render` — 基于输入更改形状的 UI（例如，仅在上传输入时显示额外控件）。
- `gr.Examples` — 可点击的示例输入。几乎总是值得包含。从 LoRA 的模型卡提升。
- `gr.BrowserState` — 跨会话持久化用户偏好（首选宽高比、上次 seed 等）。
- `gr.DeepLinkButton` — 将特定生成共享为 URL。

**2. Hub 自定义组件。** 一个 `pip install` 和一个 import，无需维护 JS：

- `gradio_image_annotation` — 图像之上的 bbox/点注释。当 LoRA 在字面上需要框 *坐标* 作为结构化输入时（例如拖放"从框 A 移动到框 B"的 LoRA、区域标记编辑）才正确。当 LoRA 想要绘制的区域时错误——请改用 `gr.ImageEditor`。
- `gradio_imageslider` — 带额外控件的前后对比滑块的替代品。
- `gradio_modal` — 模态对话框。
- `gradio_rangeslider` — 双柄范围滑块。

在进一步向下走之前，浏览其余部分：https://www.gradio.app/custom-components/gallery。

**3. 创造模式（自定义 HTML/JS）。** 当内置和 Hub 自定义组件都不够时——点集、笔触、轨迹、带元数据的区域选择、3D 旋转小工具、时间轴 scrubber，任何用户在媒体之上操作物体的场景。参见 `creative-mode.md` 获取 Gradio 原语、JS↔Python 通信契约和陷阱。不要跳过第二级到这一级——`gradio_image_annotation` 已经涵盖了许多看起来需要自定义 HTML 的内容。

主题：默认为 `gr.themes.Citrus()`。

在默认使用普通组件或猜测自定义组件之前，访问 https://www.gradio.app/docs 获取当前 Gradio 文档。

## Gradio 6.x 陷阱

当前的 `sdk_version`（撰写时为 6.x — 使用 `pip index versions gradio` 验证）更改了几件事，旧版配方会出错。失败很容易被忽视，因为它们发生在 Space 首次导入时，而不是你在本地写文件时。

- **`theme=` 和 `css=` 已从 `gr.Blocks(...)` 移至 `demo.launch(...)`。** 将它们传递给 `Blocks` 现在会发出弃用警告，并且样式静默不应用。始终：

  ```python
  with gr.Blocks(title="...") as demo:
      ...

  if __name__ == "__main__":
      demo.launch(theme=gr.themes.Citrus(), css=CSS)
  ```

  Space 将 `app.py` 作为 `__main__` 运行，因此 `launch()` 调用执行。

- **某些组件 kwargs 已被删除。** `gr.Image` 不再接受 `show_download_button`（同一更改影响少数其他组件）。Space 在导入时失败，报 `TypeError: __init__() got an unexpected keyword argument 'show_download_button'` — 直到容器实际启动才暴露。如有疑问，在传递非显而易见的 kwargs 之前，访问当前文档以获取特定组件。

- **Space 运行的 Gradio 版本由 README YAML 中的 `sdk_version:` 设置，*而不是* 由 `requirements.txt` 设置。** 在 `requirements.txt` 中固定 `gradio` 最好是被忽略，最坏会导致运行时版本不匹配；在 README 中设置一次版本，并针对该版本编写 `app.py`。

如果首次构建在 Gradio 组件上以 `TypeError` 或签名不匹配失败，这是最常见的原因 — 读取 `/logs/container`（构建）或 `/logs/run`（运行时），查看 `app.py` 中的行，并检查当前组件签名。