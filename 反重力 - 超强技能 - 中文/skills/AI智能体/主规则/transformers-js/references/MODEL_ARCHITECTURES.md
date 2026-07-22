# 支持的模型架构

本文档列出 Transformers.js 当前支持的模型架构。

## 自然语言处理

### 文本模型
- **ALBERT** - 轻量级 BERT 自监督学习模型
- **BERT** - Transformer 双向编码器表示
- **CamemBERT** - 基于 RoBERTa 的法语语言模型
- **CodeGen** - 代码生成模型
- **CodeLlama** - 专注代码的 Llama 模型
- **Cohere** - 用于 RAG 的 Command-R 模型
- **DeBERTa** - 解码增强的 BERT（解耦注意力）
- **DeBERTa-v2** - DeBERTa 改进版
- **DistilBERT** - BERT 蒸馏版（更小、更快）
- **GPT-2** - 生成式预训练 Transformer 2
- **GPT-Neo** - 开源 GPT-3 替代方案
- **GPT-NeoX** - 更大的 GPT-Neo 模型
- **LLaMA** - Meta AI 大语言模型
- **Mistral** - Mistral AI 语言模型
- **MPNet** - 掩码与置换预训练
- **MobileBERT** - 面向移动设备的压缩 BERT
- **RoBERTa** - 鲁棒优化的 BERT
- **T5** - 文本到文本迁移 Transformer
- **XLM-RoBERTa** - 多语言 RoBERTa

### 序列到序列
- **BART** - 去噪序列到序列预训练
- **Blenderbot** - 开放域聊天机器人
- **BlenderbotSmall** - 更小的 Blenderbot 变体
- **M2M100** - 多对多多语言翻译
- **MarianMT** - 神经机器翻译
- **mBART** - 多语言 BART
- **NLLB** - No Language Left Behind（200 种语言）
- **Pegasus** - 基于提取间隔句的预训练

## 计算机视觉

### 图像分类
- **BEiT** - 图像 Transformer 的 BERT 预训练
- **ConvNeXT** - 现代 ConvNet 架构
- **ConvNeXTV2** - 改进的 ConvNeXT
- **DeiT** - 数据高效图像 Transformer
- **DINOv2** - 自监督视觉 Transformer
- **DINOv3** - 最新 DINO 迭代
- **EfficientNet** - 高效卷积网络
- **MobileNet** - 面向移动端的轻量模型
- **MobileViT** - 移动端视觉 Transformer
- **ResNet** - 残差网络
- **SegFormer** - 语义分割 Transformer
- **Swin** - 移位窗口 Transformer
- **ViT** - 视觉 Transformer

### 目标检测
- **DETR** - 检测 Transformer
- **D-FINE** - 目标检测的细粒度分布精炼
- **DINO** - 改进去噪锚框的 DETR
- **Grounding DINO** - 开放集目标检测
- **YOLOS** - You Only Look at One Sequence

### 分割
- **CLIPSeg** - 文本提示图像分割
- **Mask2Former** - 通用图像分割
- **SAM** - Segment Anything Model
- **EdgeTAM** - 端侧 Track Anything Model

### 深度与姿态
- **DPT** - 密集预测 Transformer
- **Depth Anything** - 单目深度估计
- **Depth Pro** - 精确的单目度量深度
- **GLPN** - 全局-局部路径深度网络

## 音频

### 语音识别
- **Wav2Vec2** - 自监督语音表示
- **Whisper** - 鲁棒语音识别（多语言）
- **HuBERT** - 自监督语音表示学习

### 音频处理
- **Audio Spectrogram Transformer** - 音频分类
- **DAC** - Descript Audio Codec

### 文本转语音
- **SpeechT5** - 统一语音和文本预训练
- **VITS** - 对抗学习的条件变分自编码器

## 多模态

### 视觉-语言
- **CLIP** - 对比语言-图像预训练
- **Chinese-CLIP** - CLIP 中文版
- **ALIGN** - 大规模噪声图文对
- **BLIP** - 引导式语言-图像预训练
- **Florence-2** - 统一视觉基础模型
- **LLaVA** - 大语言和视觉助手
- **Moondream** - 微型视觉-语言模型

### 文档理解
- **DiT** - 文档图像 Transformer
- **Donut** - 无 OCR 文档理解
- **LayoutLM** - 文档理解预训练
- **TrOCR** - 基于 Transformer 的 OCR

### 音频-语言
- **CLAP** - 对比语言-音频预训练

## Embeddings 与相似度

- **Sentence Transformers** - 句子嵌入
- **all-MiniLM** - 高效句子嵌入
- **all-mpnet-base** - 高质量句子嵌入
- **E5** - 微软文本嵌入
- **BGE** - 通用嵌入模型
- **nomic-embed** - 长上下文嵌入

## 专用模型

### 代码
- **CodeBERT** - 代码预训练模型
- **GraphCodeBERT** - 代码结构理解
- **StarCoder** - 代码生成

### 科学
- **SciBERT** - 科学文本
- **BioBERT** - 生物医学文本

### 检索
- **ColBERT** - 基于 BERT 的上下文化晚期交互
- **DPR** - 密集段落检索

## 模型选择技巧

### 文本任务
- **小巧快速**：DistilBERT、MobileBERT
- **均衡**：BERT-base、RoBERTa-base
- **高精度**：RoBERTa-large、DeBERTa-v3-large
- **多语言**：XLM-RoBERTa、mBERT

### 视觉任务
- **移动端/浏览器**：MobileNet、EfficientNet-B0
- **均衡**：DeiT-base、ConvNeXT-tiny
- **高精度**：Swin-large、DINOv2-large

### 音频任务
- **语音识别**：Whisper-tiny（快速）、Whisper-large（精确）
- **音频分类**：Audio Spectrogram Transformer

### 多模态
- **视觉-语言**：CLIP（通用）、Florence-2（全面）
- **文档 AI**：Donut、LayoutLM
- **OCR**：TrOCR

## 在 Hugging Face Hub 上查找模型

搜索兼容模型：
```
https://huggingface.co/models?library=transformers.js
```

按任务筛选：
```
https://huggingface.co/models?pipeline_tag=text-classification&library=transformers.js
```

检查 ONNX 支持：在模型仓库中查找 `onnx/` 文件夹。
