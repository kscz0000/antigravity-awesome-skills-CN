---
name: gemini-omni-flash-api
description: 使用此技能可通过官方 google-genai SDK 完成生成式视频编辑、文生视频、参考图像的视频生成以及首帧到视频的过渡动画。包含使用 ffmpeg 预处理/优化高分辨率或长时长源视频的工作流。触发词：gemini-omni-flash、video editing、text to video、image to video、first-frame-to-video、视频编辑、文生视频、图生视频、参考图像视频、Interactions API、Files API、google-genai。
risk: unknown
source: https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-omni-flash-api
source_repo: google-gemini/gemini-skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/google-gemini/gemini-skills/blob/main/LICENSE
---

# Gemini Omni Flash 技能
## 适用场景

需要使用此技能通过官方 google-genai SDK 完成生成式视频编辑、文生视频、参考图像的视频生成以及首帧到视频的过渡动画时使用。包含使用 ffmpeg 预处理/优化高分辨率或长时长源视频的工作流。


本技能使用 Gemini Omni Flash 模型（`gemini-omni-flash-preview`）执行文生视频、图生视频以及视频编辑。

> [!WARNING]
> **重要地区限制**：上传用于视频编辑的视频在 EEA、瑞士、英国以及美国部分地区**不可用**。如果视频到视频的编辑快速完成但输出为空（`total_output_tokens: 0` 或没有视频内容），通常就是受到该限制影响。

## 核心能力

1. **视频编辑与精修**：编辑已有视频（最长 10 秒），应用风格变换，或执行 inpainting/outpainting。
2. **文生视频**：根据文本提示生成视频。
3. **首帧到视频**：根据单张输入图像生成视频。
4. **参考图像生成**：使用图像中的风格、角色或物体作为参考，引导视频生成。

## 工作流

1. **分析需求**：明确目标任务（例如首帧到视频、参考引导编辑）并识别所需的输入媒体资源。
2. **运行 SDK 脚本**：

   * 直接运行对应的工具脚本（`scripts/video/generate_video.py` 或 `scripts/upload_file.py`）。
   * 配置参数如 `--aspect-ratio`（例如 `16:9`、`9:16`）和 `--duration`（`3` 到 `10` 之间的整数，例如 `3`、`5`、`10`）。

3. **获取并处理输出**：输出保存到本地文件系统（例如 `media/`）。将完成的媒体路径反馈给用户。

## 参考文档

* **Interactions API**：Gemini Omni Flash 模型（`gemini-omni-flash-preview`）的所有操作与状态管理均通过 [Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview) 完成。
* **Files API**：输入媒体文件（例如参考图像和视频）必须先通过 [Files API](https://ai.google.dev/gemini-api/docs/interactions/files) 上传，然后才能在生成任务中引用。上传后的文件 URI 和 MIME 类型随后会包含在 `interactions.create` 的输入 parts 数组中。
* **[Interactions API 技能参考](https://github.com/google-gemini/gemini-skills/blob/main/skills/gemini-interactions-api/SKILL.md)**：Interactions API 的平台级通用指南、最新模型规格以及 SDK 使用规则。

## 依赖与前置条件

* **Python SDK（`google-genai`）**：需要 `google-genai >= 2.10.0`（Python）以支持新的 `interactions` 客户端属性。安装或升级命令：
  ```bash
  pip install -U google-genai
  ```
* **Python 运行时**：需要 **Python >= 3.10**（以兼容现代 `google-genai` SDK 的类型与方法）。
* **ffmpeg 与 ffprobe**：`prep_video.py`、`inspect_video.py` 以及 `generate_video.py`（在使用 `--strip-audio` 去除音频时）需要系统 `PATH` 中已安装 `ffmpeg` 和 `ffprobe` 可执行文件。

## 可用脚本

使用以下 Python 脚本通过 Files API 上传媒体、使用 ffmpeg 准备输入视频，并通过 Interactions API 生成视频输出。

1. **[upload_file.py](scripts/upload_file.py)**：将本地媒体（图像和视频）上传到 Files API 并轮询直至状态为 `ACTIVE`。如果上传的视频大于 25MB，脚本会输出带有提示信息的警告，建议 Gemini Omni Flash 针对 10 秒、720p/24fps 的视频进行优化，并推荐先使用 `prep_video.py` 预处理以加快上传速度。

   ```bash
   ./scripts/upload_file.py path/to/image.png
   ```

2. **[generate_video.py](scripts/video/generate_video.py)**：执行端到端的视频生成并下载输出视频。脚本会先检测并上传本地媒体引用（图像或视频），再调用 Interactions API。大于 25MB 的视频资源会触发预处理建议，但不会阻塞上传。

   * **文生视频**：

     ```bash
     ./scripts/video/generate_video.py "A close-up of a cat drinking tea" --output media/cat_tea.mp4
     ```

   * **图生视频（首帧与参考）**：

     ```bash
     ./scripts/video/generate_video.py "The waves crash against the shore." --image reference.png --output media/waves.mp4
     ```

   * **视频插值**：

     提供恰好两张关键帧图像，生成它们之间的过渡视频：

     ```bash
     ./scripts/video/generate_video.py "A smooth timelapse from sunrise to sunset" --image start.png --image end.png --output media/interpolation.mp4
     ```

   * **视频编辑（保留原始音频）**：

     ```bash
     ./scripts/video/generate_video.py "Transform the style to Japanese anime" --video input.mp4 --output media/anime_style.mp4
     ```

   * **视频编辑（从头重新生成所有音频）**：

     ```bash
     ./scripts/video/generate_video.py "Transform the style to Japanese anime" --video input.mp4 --strip-audio --output media/anime_style_new_audio.mp4
     ```

   * **轮次式视频编辑（编辑上一次交互）**：

     通过传入 interaction ID 编辑先前的视频生成结果，无需重新上传资源：

     ```bash
     ./scripts/video/generate_video.py "Change the setting to a snowy winter wonderland." --previous-interaction-id "abc123xyz..." --output media/winter_wonderland.mp4
     ```

   * **并行批量执行（提示词文件）**：从按行组织的文本文件中并发运行多个提示词：

     ```bash
     ./scripts/video/generate_video.py --prompts-file prompts.txt --concurrency 3
     ```

   * **并行批量执行（JSON 配置）**：并发执行已完整配置的、不同类型的生成与编辑任务：

     ```bash
     ./scripts/video/generate_video.py --batch jobs.json --concurrency 3
     ```

     *`jobs.json` 示例：*

     ```json
     [
       {
         "prompt": "Transform the style to Japanese anime.",
         "video": "input.mp4",
         "output": "media/anime_style.mp4",
         "strip_audio": false,
         "aspect_ratio": "16:9"
       },
       {
         "prompt": "A smooth timelapse from sunrise to sunset.",
         "image": ["start.png", "end.png"],
         "output": "media/interpolation.mp4"
       }
     ]
     ```

3. **[inspect_video.py](scripts/video/inspect_video.py)**：检查本地视频文件（使用 `ffprobe`），查看时长、分辨率、帧率（FPS）、是否存在音频流以及格式详情。

   ```bash
   ./scripts/video/inspect_video.py media/output.mp4
   ```

   * 获取预解析后的结构化 JSON 摘要：

     ```bash
     ./scripts/video/inspect_video.py media/output.mp4 --json
     ```

   * 获取完整、未修改的 `ffprobe` 原始 JSON 转储：

     ```bash
     ./scripts/video/inspect_video.py media/output.mp4 --raw
     ```

4. **[prep_video.py](scripts/video/prep_video.py)**：对任意视频文件进行归一化、裁剪与格式化处理，使其符合 Gemini Omni Flash 生成与编辑的常规限制。支持基于时间码的裁剪、可选的帧率转换以及对大视频的等比缩放（横屏最大 1280x720，竖屏最大 720x1280），在避免拉伸的同时优化上传时长。如果视频长于 10 秒且脚本以交互模式运行（在 TTY 中），会提示用户选择保留前 10 秒、最后 10 秒，或输入自定义时间码（默认前 10 秒）。

   * **裁剪前 10 秒（默认）**：

    ```bash
     ./scripts/video/prep_video.py path/to/source.mp4
     ```

     或显式指定起点与时长：

     ```bash
     ./scripts/video/prep_video.py path/to/source.mp4 --start 0 --duration 10
     ```

   * **裁剪最后 10 秒**（根据源视频时长自动计算起点）：

     ```bash
     ./scripts/video/prep_video.py path/to/source.mp4 --start last
     ```

   * **从指定时间码（MM:SS 或 HH:MM:SS）开始裁剪 10 秒**：

     ```bash
     ./scripts/video/prep_video.py path/to/source.mp4 --start 00:03 --output media/custom.mp4
     ```

   * **自定义帧率与分辨率**：

     ```bash
     ./scripts/video/prep_video.py path/to/source.mp4 --fps 30 --resolution 1920x1080
     ```

   * **去除音频以便重新生成音频**：

     ```bash
     ./scripts/video/prep_video.py path/to/source.mp4 --strip-audio --output media/video_with_no_audio.mp4
     ```

## 在提示词中使用标签设置图像角色

可以在提示词中使用标签，明确每个上传媒体是首帧还是参考。

### 1. 简单标签（推荐）

对于图像角色从提示词中就能清楚判别的简单场景，可以直接将图像绑定到角色：

* **`<FIRST_FRAME>`**：将该图像作为视频的起始帧，例如：`<FIRST_FRAME> a woman is walking`
* **`<IMAGE_REF_N>`**：将该图像作为参考，例如：`in the style of <IMAGE_REF_0> a woman <IMAGE_REF_1> is walking`（结合第一张图的风格参考与第二张图的主体参考）。图像引用编号从 0 开始。

使用 6 张参考图像的示例：

```none
[0-3s] A studio fashion sequence. Starting with woman <IMAGE_REF_0>, she is holding <IMAGE_REF_1>
[3-6s] Then we see the man <IMAGE_REF_2> holding <IMAGE_REF_3>
[6-10s] And finally another woman <IMAGE_REF_4> who is holding <IMAGE_REF_5> while walking.
```

### 2. 显式声明来源与参考

对于多图像、多角色的复杂场景，可以使用显式前缀标签，并配以自然语言指令后缀。

* **声明来源与参考图像**：
  * `[# Sources <FIRST_FRAME>@Image1]` 会将第一张图作为起始帧。
  * `[# References <IMAGE_REF_0>@Image1]` 会将第一张图作为参考。
  * `[# References <IMAGE_REF_1>@Image2]` 会将第二张图作为参考。
  * `[# References <IMAGE_REF_0>@Image1 <IMAGE_REF_1>@Image2]` 会同时将这两张图作为参考。
  * `[# Sources <FIRST_FRAME>@Image1] [# References <IMAGE_REF_0>@Image2]` 会将第一张图作为起始帧、第二张图作为参考。
* **引导指令**：在提示词末尾添加引导指令：
  * 起始帧：`"Use the given image as the starting frame."`
  * 参考图像：`"Use the given image(s) as references for video generation. The images should not be used as literal initial frames."`

* *扩展提示词示例*：

  ```none
  [# Sources <FIRST_FRAME>@Image1] [# References <IMAGE_REF_0>@Image2] a woman <IMAGE_REF_0> is walking. Use Image1 as the starting frame. Use Image2 as a reference for the video generation.
  ```

## 视频编辑中的音频处理

编辑包含音频的源视频时，必须在保留原始音频和从头重新生成音频之间二选一。

* **保留原始音频**：默认情况下，Gemini Omni Flash 会保留现有音频层（虽然生成过程中可能会略有改动或适配）。当希望保留原始背景音乐、对白或音效时使用。
* **从头重新生成所有音频**：如果希望 Gemini Omni Flash 完全重新创建与新视觉风格或提示词相匹配的音频层，则**必须**上传已剥离音频流的视频。如果仍包含任何音频流，Gemini Omni Flash 会尝试保留/修改它，而不是从头重新生成。

  * 使用 `scripts/video/prep_video.py` 预处理或执行 `scripts/video/generate_video.py` 时，使用 `--strip-audio`（或 `-a`）。
  * 这会强制 Gemini Omni Flash 执行完整的音频生成。

## 提示 Gemini Omni Flash 的技巧

### 单场景

默认情况下，Gemini Omni Flash 会尝试用几个不同镜头生成视频，并基于提示词构建有趣的故事。

如果需要输出的视频只包含单个场景，必须在提示词中明确要求：

* In a single unbroken scene（单个不间断场景）
* In a single continuous shot（单个连续镜头）
* No scene cuts（无场景切换）

示例：

```none
Continuous, unbroken handheld shot of a fluffy tabby cat sitting on a sunny windowsill, looking out into a leafy garden. The cat's tail twitches slowly, and its ears rotate slightly toward ambient noises. Sunbeams illuminate dust motes in the air. Sound design: Gentle breeze, distant bird chirps, quiet mechanical purring. No dialogue.
```

### 移除不需要的元素

如果生成结果包含不想要的内容，可以在提示词中加入简单的否定项来规避：

* No dialogue（无对白）
* No embellishments（无装饰元素）
* No extra sound effects（无额外音效）

### 编辑用的提示词

编辑任务中简单提示词效果最好。过于详细的提示词反而会带来意料之外的变化。

示例：

* Make this video anime（把这段视频改成动漫风格）
* Make the phone invisible（让手机消失）
* Put a fashionable hat on this person（给人物戴一顶时尚帽子）
* Change the lighting to be more dramatic（把光线调得更戏剧化）
* Change the text on the sign to say "Gemini Omni Flash"（将标牌上的文字改为 "Gemini Omni Flash"）
* Add a cat that jumps onto his lap, he begins to pet it（加一只跳到他膝盖上的猫，他开始抚摸它）

当只编辑视频的某个具体方面时，加入 "Keep everything else the same"（其他部分保持不变）会很有帮助。

### 音频的提示

默认情况下模型会尝试为视频生成合适的音轨。这并不总是符合预期。可以在提示词中描述你想要的音频类型。如果希望视频中包含音乐，这一点尤其重要：

* Include calm background music（加入平静的背景音乐）
* The video has a high energy techno beat（视频配有高能的电子节拍）
* The audio is a low tinny radio broadcast in the background, playing a song（背景是低沉单薄的电台广播，正在播放一首歌）
* Audio design: [a description of the audio you want]（音频设计：[对你想要音频的描述]）

### 时间点控制

可以通过提示词指定事件在视频中的特定时间发生，无需精确语法，直接使用自然语言即可。这在自定义场景切换、节奏控制或快节奏镜头序列时尤其有用。

简单示例：

* after 3 seconds, a woman enters the scene（3 秒后，一位女性进入场景）
* at 5s the chorus starts in the background audio（在 5 秒时，背景音中开始出现副歌）
* every 2s cut to a new frame（每 2 秒切换到一个新画面）
* in a rapid fire sequence, every half a second (12 frames at 24fps) change the scene to a new location（在快节奏镜头序列中，每半秒（24fps 下 12 帧）切换场景到新地点）

也可以使用时间码语法：

```none
[0-3s] A person is walking
[3-6s] They stop and turn around
[6-10s] They start running
```

### Meta 提示

与其在提示词中直接指定所有细节，不如让模型关注某些特定方面。可以将以下提示词原样交给 Gemini Omni Flash：

* Consider micro-detail, expression and timing to create a very rich, detailed but entirely natural scene.（关注微观细节、表情和节奏，创建一个非常丰富、细致而又完全自然的场景。）
* Be extremely detailed in your descriptions of characters and environments. Apply costume design principles to characters. Be very specific about the people, items and objects in the scene.（对角色和环境的描述要极其细致。对角色应用服装设计原则。对场景中的人物、物品、对象要非常具体。）
* Include plenty of appropriate detail in the background elements to make the scene feel realistic and natural.（在背景元素中加入足够且合适的细节，让场景显得真实自然。）
* Make a rapid fire video that shows a different rare [thing] every 1s, upbeat music, include text to label the thing.（制作一个快节奏视频，每 1 秒展示一种不同的稀有 [物品]，配以欢快的音乐，并用文字标注该物品。）

### 视频中的文字效果非常好

与之前的视频模型不同，Gemini Omni Flash 视频中的文字渲染效果非常好。可以在视频中加入不少文字，它会以正确且清晰可读的方式呈现。如果视频中天然就包含文字（哪怕只是背景元素），建议明确指定文字内容。

示例：

* One word on the screen at a time: "did, you, know, that, Omni, can, do, awesome, text?" Each word appears for 1s with a different animated style. No dialogue.（屏幕上一次只显示一个词："did, you, know, that, Omni, can, do, awesome, text?" 每个词以不同的动画样式显示 1 秒。无对白。）
* There is a street sign that says: "This is an AI generation by Omni", there is a storefront that says: "All you need AI", there's a car with the number plate: "OMN111"（有一块写着 "This is an AI generation by Omni" 的路牌，一家写着 "All you need AI" 的店铺，以及一辆车牌为 "OMN111" 的汽车）

## 限制

- 仅在任务与上游产品或 API 范围明确匹配时使用此技能。
- 在变更前，请根据当前官方文档核实命令、API 行为、定价、配额、凭据以及部署效果。
- 不要将生成示例作为环境专属测试、安全审查或用户对破坏性/高成本操作的批准的替代。