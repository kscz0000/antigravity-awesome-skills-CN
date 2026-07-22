---
name: remotion-best-practices
description: "Remotion 最佳实践 - React 中的视频创作。触发词：remotion、video、react、animation、composition"
risk: safe
source: community
tags: "remotion, video, react, animation, composition"
date_added: "2026-02-27"
---

## 使用场景
当处理 Remotion 代码时，使用此技能获取领域特定知识。

## 使用方法

阅读各个规则文件以获取详细说明和代码示例：

- [rules/3d.md](rules/3d.md) - 使用 Three.js 和 React Three Fiber 在 Remotion 中创建 3D 内容
- [rules/animations.md](rules/animations.md) - Remotion 的基础动画技能
- [rules/assets.md](rules/assets.md) - 将图像、视频、音频和字体导入 Remotion
- [rules/audio.md](rules/audio.md) - 在 Remotion 中使用音频和声音 - 导入、剪辑、音量、速度、音调
- [rules/calculate-metadata.md](rules/calculate-metadata.md) - 动态设置合成时长、尺寸和属性
- [rules/can-decode.md](rules/can-decode.md) - 使用 Mediabunny 检查视频是否可被浏览器解码
- [rules/charts.md](rules/charts.md) - Remotion 的图表和数据可视化模式
- [rules/compositions.md](rules/compositions.md) - 定义合成、静态图像、文件夹、默认属性和动态元数据
- [rules/display-captions.md](rules/display-captions.md) - 在 Remotion 中显示字幕，支持 TikTok 风格页面和单词高亮
- [rules/extract-frames.md](rules/extract-frames.md) - 使用 Mediabunny 从视频中提取特定时间戳的帧
- [rules/fonts.md](rules/fonts.md) - 在 Remotion 中加载 Google Fonts 和本地字体
- [rules/get-audio-duration.md](rules/get-audio-duration.md) - 使用 Mediabunny 获取音频文件的时长（秒）
- [rules/get-video-dimensions.md](rules/get-video-dimensions.md) - 使用 Mediabunny 获取视频文件的宽度和高度
- [rules/get-video-duration.md](rules/get-video-duration.md) - 使用 Mediabunny 获取视频文件的时长（秒）
- [rules/gifs.md](rules/gifs.md) - 在 Remotion 时间轴中同步显示 GIF
- [rules/images.md](rules/images.md) - 使用 Img 组件在 Remotion 中嵌入图像
- [rules/import-srt-captions.md](rules/import-srt-captions.md) - 使用 @remotion/captions 将 .srt 字幕文件导入 Remotion
- [rules/lottie.md](rules/lottie.md) - 在 Remotion 中嵌入 Lottie 动画
- [rules/measuring-dom-nodes.md](rules/measuring-dom-nodes.md) - 在 Remotion 中测量 DOM 元素尺寸
- [rules/measuring-text.md](rules/measuring-text.md) - 测量文本尺寸、将文本适配容器并检查溢出
- [rules/sequencing.md](rules/sequencing.md) - Remotion 的序列模式 - 延迟、剪辑、限制项目时长
- [rules/tailwind.md](rules/tailwind.md) - 在 Remotion 中使用 TailwindCSS
- [rules/text-animations.md](rules/text-animations.md) - Remotion 的排版和文本动画模式
- [rules/timing.md](rules/timing.md) - Remotion 中的插值曲线 - 线性、缓动、弹簧动画
- [rules/transcribe-captions.md](rules/transcribe-captions.md) - 在 Remotion 中转录音频生成字幕
- [rules/transitions.md](rules/transitions.md) - Remotion 的场景过渡模式
- [rules/trimming.md](rules/trimming.md) - Remotion 的剪辑模式 - 裁剪动画的开头或结尾
- [rules/videos.md](rules/videos.md) - 在 Remotion 中嵌入视频 - 剪辑、音量、速度、循环、音调

## 限制条件
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。