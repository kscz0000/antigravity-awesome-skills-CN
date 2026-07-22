# 广告创意生成式 AI 工具

使用 AI 图像生成器、视频生成器和基于代码的视频工具规模化生产广告视觉素材的参考指南。

---

## 何时使用生成式工具

| 需求 | 工具类别 | 最佳选择 |
|------|----------|----------|
| 静态广告图片（横幅、社交） | 图像生成 | Nano Banana Pro、Flux、Ideogram |
| 带文字叠加的广告图片 | 图像生成（支持文字） | Ideogram、Nano Banana Pro |
| 短视频广告（6-30秒） | 视频生成 | Veo、Kling、Runway、Sora、Seedance |
| 带配音的视频广告 | 视频生成 + 语音 | Veo/Sora（原生），或 Runway + ElevenLabs |
| 广告配音音轨 | 语音生成 | ElevenLabs、OpenAI TTS、Cartesia |
| 多语言广告版本 | 语音生成 | ElevenLabs、PlayHT |
| 品牌声音克隆 | 语音生成 | ElevenLabs、Resemble AI |
| 产品样机和变体 | 图像生成 + 参考 | Flux（多图参考） |
| 模板化视频广告规模化生产 | 基于代码的视频 | Remotion |
| 个性化视频（姓名、数据） | 基于代码的视频 | Remotion |
| 品牌一致的变体 | 图像生成 + 风格参考 | Flux、Ideogram、Nano Banana Pro |

---

## 图像生成

### Nano Banana Pro (Gemini)

Google DeepMind 的图像生成模型，通过 Gemini API 提供。

**最适合：** 高质量广告图片、产品视觉素材、文字渲染
**API：** Gemini API（Google AI Studio、Vertex AI）
**定价：** ~$0.04/图（Gemini 2.5 Flash Image），~$0.24/4K图（Nano Banana Pro）

**优势：**
- 图像内文字渲染能力强（标志、标题）
- 原生图像编辑（用提示词修改现有图像）
- 通过用于文本生成的同一 Gemini API 提供
- 支持在一个模型中同时生成和编辑

**广告创意用例：**
- 从文本描述生成社交媒体广告图片
- 创建产品样机变体
- 编辑现有广告图片（更换背景、改变颜色）
- 生成内嵌标题文字的图像

**API 示例：**
```bash
# 使用 Gemini API 进行图像生成
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
    "contents": [{"parts": [{"text": "Create a clean, modern social media ad image for a project management tool. Show a laptop with a kanban board interface. Bright, professional, 16:9 ratio."}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }'
```

**文档：** [Gemini Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)

---

### Flux (Black Forest Labs)

开放权重图像生成模型，通过 Replicate 和 BFL 原生 API 提供 API 访问。

**最适合：** 照片级真实图像、品牌一致变体、多参考图生成
**API：** Replicate、BFL API、fal.ai
**定价：** ~$0.01-0.06/图，取决于模型和分辨率

**模型变体：**
| 模型 | 速度 | 质量 | 成本 | 最适合 |
|------|------|------|------|--------|
| Flux 2 Pro | ~6秒 | 最高 | $0.015/MP | 最终生产素材 |
| Flux 2 Flex | ~22秒 | 高 + 编辑 | $0.06/MP | 迭代编辑 |
| Flux 2 Dev | ~2.5秒 | 良好 | $0.012/MP | 快速原型 |
| Flux 2 Klein | 最快 | 良好 | 最低 | 大批量生成 |

**优势：**
- 多图参考（最多8张图）实现广告间一致的身份
- 产品一致性——同一产品在不同场景中
- 从参考图像进行风格迁移
- 开放权重 Dev 模型支持自托管

**广告创意用例：**
- 生成50+个保持产品/人物身份一致的广告变体
- 创建产品场景图（你的 SaaS 在不同设备上）
- 使用参考图像匹配现有品牌资产风格
- 快速 A/B 测试图像变体

**文档：** [Replicate Flux](https://replicate.com/black-forest-labs/flux-2-pro), [BFL API](https://docs.bfl.ml/)

---

### Ideogram

专注于图像内排版和文字渲染。

**最适合：** 带文字的广告横幅、品牌图形、带标题的社交广告图片
**API：** Ideogram API、Runware
**定价：** ~$0.06/图（API），~$0.009/图（订阅）

**优势：**
- 业内最佳文字渲染（约90%准确率，而大多数工具约30%）
- 风格参考系统（上传最多3张参考图）
- 43亿种风格预设，保持一致的品牌美学
- 擅长标志和品牌排版

**广告创意用例：**
- 生成标题文字直接嵌入图像的广告横幅
- 创建带品牌文字叠加的社交媒体图形
- 制作保持排版一致的多款设计变体
- 无需设计师参与每次迭代即可生成宣传物料

**文档：** [Ideogram API](https://developer.ideogram.ai/), [Ideogram](https://ideogram.ai/)

---

### 其他图像工具

| 工具 | 最适合 | API 状态 | 备注 |
|------|--------|----------|------|
| **DALL-E 3** (OpenAI) | 通用图像生成 | 官方 API | 集成于 ChatGPT，文字渲染良好 |
| **Midjourney** | 艺术感、高审美图像 | 无官方公开 API | 基于 Discord；存在非官方 API 但有封号风险 |
| **Stable Diffusion** | 自托管、可定制 | 开源 | 最适合有 GPU 基础设施的团队 |

---

## 视频生成

### Google Veo

Google DeepMind 的视频生成模型，通过 Gemini API 和 Vertex AI 提供。

**最适合：** 带原生音频的高质量视频广告、社交竖版视频
**API：** Gemini API、Vertex AI
**定价：** ~$0.15/秒（Veo 3.1 Fast），~$0.40/秒（Veo 3.1 Standard）

**能力：**
- 最长60秒，1080p
- 原生音频生成（对话、音效、环境音）
- 9:16竖版输出，适用于 Stories/Reels/Shorts
- 可升级至4K
- 文生视频和图生视频

**广告创意用例：**
- 从文本描述生成短视频广告（15-30秒）
- 为 TikTok、Reels、Shorts 创建竖版视频广告
- 制作带配音的产品演示
- 用同一提示词生成不同风格的多个视频变体

**文档：** [Veo on Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/video/overview)

---

### Kling (Kuaishou)

支持音视频同步生成和镜头控制的视频生成工具。

**最适合：** 电影感视频广告、较长内容、音画同步视频
**API：** Kling API、PiAPI、fal.ai
**定价：** ~$0.09/秒（通过 fal.ai 第三方）

**能力：**
- 最长3分钟，1080p/30-48fps
- 音视频同步生成（Kling 2.6）
- 文生视频和图生视频
- 运动和镜头控制

**广告创意用例：**
- 较长的产品解说视频
- 带同步音频的电影感品牌视频
- 将产品图片动画化为视频广告

**文档：** [Kling AI Developer](https://klingai.com/global/dev/model/video)

---

### Runway

具有强大可控性的视频生成和编辑平台。

**最适合：** 可控视频生成、风格一致内容、编辑现有素材
**API：** Runway Developer Portal

**能力：**
- Gen-4：跨镜头保持角色/场景一致性
- 运动笔刷和镜头控制
- 带参考图的图生视频
- 视频到视频风格迁移

**广告创意用例：**
- 生成跨场景保持角色/产品一致的视频广告
- 将现有素材风格迁移以匹配品牌美学
- 延展或重混现有视频内容

**文档：** [Runway API](https://docs.dev.runwayml.com/)

---

### Sora 2 (OpenAI)

OpenAI 的视频生成模型，支持同步音频。

**最适合：** 带对话和声音的高保真视频
**API：** OpenAI API
**定价：** 提供免费层；Pro 版 $0.10-0.50/秒，取决于分辨率

**能力：**
- 最长60秒，带同步音频
- 对话、音效和环境音
- sora-2（快速）和 sora-2-pro（质量）变体
- 文生视频和图生视频

**广告创意用例：**
- 视频证言和说话人风格广告
- 带解说的产品演示视频
- 叙事性品牌视频

**文档：** [OpenAI Video Generation](https://platform.openai.com/docs/guides/video-generation)

---

### Seedance 2.0 (ByteDance)

ByteDance 的视频生成模型，支持音视频同步生成和多模态输入。

**最适合：** 快速、低成本带原生音频的视频广告、多模态参考输入
**API：** BytePlus（官方）、Replicate、WaveSpeedAI、fal.ai（第三方）；OpenAI 兼容 API 格式
**定价：** ~$0.10-0.80/分钟，取决于分辨率（估计比 Sora 2 单片段便宜10-100倍）

**能力：**
- 最长20秒，最高2K分辨率
- 音视频同步生成（双分支扩散 Transformer）
- 文生视频和图生视频
- 最多12个参考文件的多模态输入
- OpenAI 兼容 API 结构

**广告创意用例：**
- 低成本大批量短视频广告生产
- 一次性生成带同步配音和音效的视频广告
- 多参考图生成（输入产品图片、品牌资产、风格参考）
- 快速迭代视频广告概念

**文档：** [Seedance](https://seed.bytedance.com/en/seedance2_0)

---

### Higgsfield

全栈视频创作平台，具有电影级镜头控制。

**最适合：** 社交视频广告、电影风格、移动优先内容
**平台：** [higgsfield.ai](https://higgsfield.ai/)

**能力：**
- 50+种专业镜头运动（推拉摇移、FPV无人机镜头）
- 图生视频动画
- 内置编辑、转场和关键帧
- 一站式工作流：图像生成、动画、编辑

**广告创意用例：**
- 带电影感的社交媒体视频广告
- 将产品图片动画化为动态视频
- 用不同镜头风格创建多个视频变体
- 社交活动快速产出视频内容

---

### 视频工具对比

| 工具 | 最大时长 | 音频 | 分辨率 | API | 最适合 |
|------|----------|------|--------|-----|--------|
| **Veo 3.1** | 60秒 | 原生 | 1080p/4K | Gemini | 竖版社交视频 |
| **Kling 2.6** | 3分钟 | 原生 | 1080p | 第三方 | 较长电影感内容 |
| **Runway Gen-4** | 10秒 | 无 | 1080p | 官方 | 可控、一致 |
| **Sora 2** | 60秒 | 原生 | 1080p | 官方 | 对话为主 |
| **Seedance 2.0** | 20秒 | 原生 | 2K | 官方 + 第三方 | 低成本大批量 |
| **Higgsfield** | 可变 | 有 | 1080p | 基于 Web | 社交、移动优先 |

---

## 语音与音频生成

为视频广告叠加逼真的配音、为产品演示添加解说，或为 Remotion 渲染的视频生成音频。这些工具将广告脚本转化为自然的语音轨道。

### 何时使用语音工具

许多视频生成器（Veo、Kling、Sora、Seedance）现在已包含原生音频。在以下情况使用独立语音工具：

- **为静音视频添加配音** — Runway Gen-4 和 Remotion 生成静音输出
- **品牌声音一致性** — 为所有广告克隆特定声音
- **多语言版本** — 同一广告脚本支持20+种语言
- **脚本迭代** — 无需重新拍摄视频即可重新录制配音
- **精确控制** — 精确的时机、情感和节奏

---

### ElevenLabs

逼真语音生成和声音克隆的市场领导者。

**最适合：** 最自然的配音、品牌声音克隆、多语言
**API：** REST API，支持流式传输
**定价：** ~$0.12-0.30/千字符，取决于套餐；起价 $5/月

**能力：**
- 29+种语言，自然的口音和语调
- 从短音频片段（即时）或较长录音（专业版）克隆声音
- 情感和风格控制
- 流式传输支持实时生成
- 数百种预置声音库

**广告创意用例：**
- 为视频广告生成配音轨道
- 克隆品牌代言人的声音用于所有广告变体
- 用一个脚本制作10+种语言的同一广告
- A/B 测试不同声音风格（权威 vs 友好 vs 紧迫）

**API 示例：**
```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Stop wasting hours on manual reporting. Try DataFlow free for 14 days.",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
  }' --output voiceover.mp3
```

**文档：** [ElevenLabs API](https://elevenlabs.io/docs/api-reference/text-to-speech)

---

### OpenAI TTS

内置在 OpenAI API 中的简单、经济实惠的文本转语音。

**最适合：** 快速配音、规模化成本效益、简单集成
**API：** OpenAI API（与 GPT/DALL-E 同一 SDK）
**定价：** $15/百万字符（标准），$30/百万字符（HD）；使用 gpt-4o-mini-tts 约 $0.015/分钟

**能力：**
- 13种内置声音（无自定义克隆）
- 多种语言
- 实时流式传输
- HD 质量选项
- 简单 API — 你已经在用于 GPT 的同一 SDK

**广告创意用例：**
- 为草稿/测试版广告快速、低成本配音
- 大批量低成本解说
- 在投资高端配音前原型测试广告音频

**文档：** [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech)

---

### Cartesia Sonic

为实时应用构建的超低延迟语音生成。

**最适合：** 实时语音、最低延迟、情感表现力
**API：** REST + WebSocket 流式传输
**定价：** 起价 $5/月；按量付费 $0.03/分钟起

**能力：**
- 40ms 首音频延迟（同类最快）
- 15+种语言
- 非语言表现力：笑声、呼吸、情感语调
- Sonic Turbo 实现更低延迟
- 流式 API 支持实时生成

**广告创意用例：**
- 创意迭代期间的实时广告预览
- 带动态解说的交互式演示视频
- 需要自然笑声、叹息或情感反应的广告

**文档：** [Cartesia Sonic](https://docs.cartesia.ai/build-with-cartesia/tts-models/latest)

---

### Voicebox (开源)

由 Qwen3-TTS 驱动的免费、本地优先语音合成工作室。ElevenLabs 的开源替代方案。

**最适合：** 免费声音克隆、本地/私密生成、零成本批量生产
**API：** 本地 REST API，地址 `http://localhost:8000`
**定价：** 免费（MIT 许可证）。完全在你的机器上运行。
**技术栈：** Tauri (Rust) + React + FastAPI (Python)

**能力：**
- 通过 Qwen3-TTS 从短音频样本克隆声音
- 多语言支持（英语、中文，更多语言计划中）
- 多轨道时间线编辑器，用于编排对话
- 通过 MLX Metal 加速在 Apple Silicon 上实现4-5倍更快推理
- 本地 REST API 支持程序化生成
- 无云依赖 — 所有处理在设备上完成

**广告创意用例：**
- 为所有广告变体免费克隆品牌代言人声音
- 批量生成配音，无按字符收费
- 当广告内容敏感或未发布时进行私密/本地生成
- 在使用付费服务前原型测试声音变体

**API 示例：**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Stop wasting hours on manual reporting.", "profile_id": "abc123", "language": "en"}'
```

**安装：** macOS 和 Windows 桌面应用可在 [voicebox.sh](https://voicebox.sh) 获取，或从源码构建：
```bash
git clone https://github.com/jamiepine/voicebox.git
cd voicebox && make setup && make dev
```

**文档：** [GitHub](https://github.com/jamiepine/voicebox)

---

### 其他语音工具

| 工具 | 最适合 | 差异化 | API |
|------|--------|--------|-----|
| **PlayHT** | 大型声音库、低延迟 | 900+种声音，<300ms延迟，超逼真 | [play.ht](https://play.ht/) |
| **Resemble AI** | 企业级声音克隆 | 本地部署、实时语音转语音 | [resemble.ai](https://www.resemble.ai/) |
| **WellSaid Labs** | 合规、商业安全声音 | 来自有偿演员的声音，商业使用安全 | [wellsaid.io](https://www.wellsaid.io/) |
| **Fish Audio** | 经济实惠、情感控制 | 比 ElevenLabs 便宜约50-70%，情感标签 | [fish.audio](https://fish.audio/) |
| **Murf AI** | 非技术团队 | 基于浏览器的工作室，200+种声音 | [murf.ai](https://murf.ai/) |
| **Google Cloud TTS** | Google 生态、规模化 | 220+种声音，40+种语言，企业级 SLA | [Google TTS](https://cloud.google.com/text-to-speech) |
| **Amazon Polly** | AWS 生态、成本 | 神经网络声音、SSML 控制、大批量便宜 | [Amazon Polly](https://aws.amazon.com/polly/) |

---

### 语音工具对比

| 工具 | 质量 | 克隆 | 语言 | 延迟 | 价格/千字符 |
|------|------|------|------|------|-------------|
| **ElevenLabs** | 最佳 | 是（即时 + 专业） | 29+ | ~200ms | $0.12-0.30 |
| **OpenAI TTS** | 良好 | 否 | 13+ | ~300ms | $0.015-0.030 |
| **Cartesia Sonic** | 很好 | 否 | 15+ | ~40ms | ~$0.03/分钟 |
| **PlayHT** | 很好 | 是 | 140+ | <300ms | ~$0.10-0.20 |
| **Fish Audio** | 良好 | 是 | 13+ | ~200ms | ~$0.05-0.10 |
| **WellSaid** | 很好 | 否（演员声音） | 英语 | ~300ms | 定制定价 |
| **Voicebox** | 良好 | 是（本地） | 2+ | 本地 | 免费（开源） |

### 选择语音工具

```
需要广告配音？
├── 需要克隆特定品牌声音？
│   ├── 最佳质量 → ElevenLabs
│   ├── 企业/本地部署 → Resemble AI
│   └── 经济实惠 → Fish Audio、PlayHT
├── 需要多语言（同一广告，多种语言）？
│   ├── 最多语言 → PlayHT（140+）
│   └── 最佳质量 → ElevenLabs（29+）
├── 需要免费/开源/本地？
│   └── Voicebox（MIT，在你的机器上运行）
├── 需要便宜、快速、够用？
│   └── OpenAI TTS（$0.015/分钟）
├── 需要商业安全许可？
│   └── WellSaid Labs（演员有偿声音）
└── 需要实时/交互？
    └── Cartesia Sonic（40ms TTFA）
```

### 工作流：语音 + 视频

```
1. 撰写广告脚本（使用 ad-creative 技能撰写文案）
2. 用 ElevenLabs/OpenAI TTS 生成配音
3. 生成或渲染视频：
   a. 从 Runway/Remotion 生成静音视频 → 叠加语音轨道
   b. 或使用带原生音频的 Veo/Sora/Seedance（跳过单独配音）
4. 如需单独叠加，用 ffmpeg 合并：
   ffmpeg -i video.mp4 -i voiceover.mp3 -c:v copy -c:a aac output.mp4
5. 生成变体（不同脚本、声音或语言）
```

---

## 基于代码的视频：Remotion

对于模板化、数据驱动的规模化视频广告，Remotion 是最佳选择。与从提示词生成独特视频的 AI 视频生成器不同，Remotion 使用 React 代码从模板和数据渲染确定性的、品牌完美的视频。

**最适合：** 模板化广告变体、个性化视频、品牌一致的生产
**技术栈：** React + TypeScript
**定价：** 个人/小团队免费；4人以上团队需要商业许可
**文档：** [remotion.dev](https://www.remotion.dev/)

### 为什么用 Remotion 做广告

| AI 视频生成器 | Remotion |
|---------------|----------|
| 每次输出独特 | 确定性、像素完美 |
| 基于提示词，控制较少 | 对每一帧完全代码控制 |
| 难以精确匹配品牌 | 精确的品牌颜色、字体、间距 |
| 一次生成一个 | 从数据批量渲染数百个 |
| 无法插入动态数据 | 用姓名、价格、统计数据个性化 |

### 广告创意用例

**1. 动态产品广告**
输入产品 JSON 数组，为每个产品渲染独特的视频广告：
```tsx
// 简化的 Remotion 产品广告组件
export const ProductAd: React.FC<{
  productName: string;
  price: string;
  imageUrl: string;
  tagline: string;
}> = ({productName, price, imageUrl, tagline}) => {
  return (
    <AbsoluteFill style={{backgroundColor: '#fff'}}>
      <Img src={imageUrl} style={{width: 400, height: 400}} />
      <h1>{productName}</h1>
      <p>{tagline}</p>
      <div className="price">{price}</div>
      <div className="cta">Shop Now</div>
    </AbsoluteFill>
  );
};
```

**2. A/B 测试视频变体**
用不同标题、CTA 或配色方案渲染同一模板：
```tsx
const variations = [
  {headline: "Save 50% Today", cta: "Get the Deal", theme: "urgent"},
  {headline: "Join 10K+ Teams", cta: "Start Free", theme: "social-proof"},
  {headline: "Built for Speed", cta: "Try It Now", theme: "benefit"},
];
// 程序化渲染所有变体
```

**3. 个性化外联视频**
生成称呼潜在客户姓名的视频，用于冷启动外联或销售。

**4. 社交广告批量生产**
以不同宽高比渲染相同内容：
- 1:1 用于信息流
- 9:16 用于 Stories/Reels
- 16:9 用于 YouTube

### 广告创意的 Remotion 工作流

```
1. 在 React 中设计模板（或用 AI 生成组件）
2. 定义数据模式（产品、标题、CTA、图片）
3. 将数据数组输入模板
4. 批量渲染所有变体
5. 上传到广告平台
```

### 快速开始

```bash
# 创建新的 Remotion 项目
npx create-video@latest

# 渲染单个视频
npx remotion render src/index.ts MyComposition out/video.mp4

# 从数据批量渲染
npx remotion render src/index.ts MyComposition --props='{"data": [...]}'
```

---

## 选择合适的工具

### 决策树

```
需要视频广告？
├── 模板化、数据驱动（相同结构，不同数据）
│   └── 使用 Remotion
├── 从提示词生成独特创意（探索性）
│   ├── 需要对话/配音？ → Sora 2、Veo 3.1、Kling 2.6、Seedance 2.0
│   ├── 需要跨场景一致性？ → Runway Gen-4
│   ├── 需要竖版社交视频？ → Veo 3.1（原生 9:16）
│   ├── 需要低成本大批量？ → Seedance 2.0
│   └── 需要电影感镜头？ → Higgsfield、Kling
└── 两者都要 → AI 生成用于主视觉创意，Remotion 用于变体

需要图像广告？
├── 需要图像内文字/标题？ → Ideogram
├── 需要变体间产品一致性？ → Flux（多参考）
├── 需要快速迭代现有图像？ → Nano Banana Pro
├── 需要最高视觉质量？ → Flux Pro、Midjourney
└── 需要低成本大批量？ → Flux Klein、Nano Banana
```

### 100个广告变体的成本对比

| 方案 | 工具 | 大致成本 |
|------|------|----------|
| 100张静态图片 | Nano Banana Pro | ~$4-24 |
| 100张静态图片 | Flux Dev | ~$1-2 |
| 100张静态图片 | Ideogram API | ~$6 |
| 100个15秒视频 | Veo 3.1 Fast | ~$225 |
| 100个15秒视频 | Remotion（模板化） | ~$0（自托管渲染） |
| 10个主视觉视频 + 90个模板化 | Veo + Remotion | ~$22 + 渲染时间 |

### 规模化广告生产的推荐工作流

1. **用 AI 生成主视觉创意**（Nano Banana、Flux、Veo）—— 高质量、探索性
2. **在 Remotion 中构建模板**，基于获胜的创意模式
3. **用 Remotion 批量生产变体**，使用数据（产品、标题、CTA）
4. **迭代** —— 用 AI 工具探索新角度，用 Remotion 实现规模化

这种混合方法让你同时拥有 AI 生成器的创意探索能力和基于代码渲染的一致性与规模化。

---

## 平台特定图片规格

生成广告图片时，请求正确的尺寸：

| 平台 | 广告位 | 宽高比 | 推荐尺寸 |
|------|--------|--------|----------|
| Meta 信息流 | 单图 | 1:1 | 1080x1080 |
| Meta Stories/Reels | 竖版 | 9:16 | 1080x1920 |
| Meta 轮播 | 方形 | 1:1 | 1080x1080 |
| Google 展示 | 横版 | 1.91:1 | 1200x628 |
| Google 展示 | 方形 | 1:1 | 1200x1200 |
| LinkedIn 信息流 | 横版 | 1.91:1 | 1200x627 |
| LinkedIn 信息流 | 方形 | 1:1 | 1200x1200 |
| TikTok 信息流 | 竖版 | 9:16 | 1080x1920 |
| Twitter/X 信息流 | 横版 | 16:9 | 1200x675 |
| Twitter/X 卡片 | 横版 | 1.91:1 | 800x418 |

在生成提示词中包含这些尺寸，避免需要裁剪或调整大小。
