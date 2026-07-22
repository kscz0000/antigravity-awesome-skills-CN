---
source: "https://github.com/huggingface/skills/tree/main/skills/transformers-js"
name: transformers-js
description: 在 Node.js 或浏览器中使用 Transformers.js 运行 JavaScript/TypeScript 版 Hugging Face 模型。触发词：Transformers.js、JS机器学习、浏览器ML、Node.js模型、Hugging Face JS
license: Apache-2.0
risk: unknown
metadata:
  author: huggingface
  version: "3.8.1"
  category: machine-learning
  repository: https://github.com/huggingface/transformers.js
compatibility: 需要 Node.js 18+ 或支持 ES modules 的现代浏览器。WebGPU 需要兼容的浏览器/环境。从 Hugging Face Hub 下载模型需要网络连接（使用本地模型时可选）。
---

# Transformers.js - JavaScript 机器学习

Transformers.js 可在浏览器和 Node.js 环境中直接运行最先进的机器学习模型，无需服务器。

## 适用场景

需要以下能力时使用此技能：
- 在 JavaScript 中运行 ML 模型进行文本分析、生成或翻译
- 执行图像分类、目标检测或分割
- 实现语音识别或音频处理
- 构建多模态 AI 应用（文生图、图生文等）
- 在浏览器端运行模型，无需后端

## 安装

### NPM 安装
```bash
npm install @huggingface/transformers
```

### 浏览器使用（CDN）
```javascript
<script type="module">
  import { pipeline } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers';
</script>
```

## 核心概念

### 1. Pipeline API
Pipeline API 是使用模型最简单的方式，它将预处理、模型推理和后处理整合在一起：

```javascript
import { pipeline } from '@huggingface/transformers';

// Create a pipeline for a specific task
const pipe = await pipeline('sentiment-analysis');

// Use the pipeline
const result = await pipe('I love transformers!');
// Output: [{ label: 'POSITIVE', score: 0.999817686 }]

// IMPORTANT: Always dispose when done to free memory
await classifier.dispose();
```

**⚠️ 内存管理：** 所有 pipeline 使用完毕后必须调用 `pipe.dispose()` 释放内存，防止内存泄漏。不同环境的清理模式参见[代码示例](./references/EXAMPLES.md)。

### 2. 模型选择
可通过第二个参数指定自定义模型：

```javascript
const pipe = await pipeline(
  'sentiment-analysis',
  'Xenova/bert-base-multilingual-uncased-sentiment'
);
```

**查找模型：**

在 Hugging Face Hub 浏览可用的 Transformers.js 模型：
- **全部模型**: https://huggingface.co/models?library=transformers.js&sort=trending
- **按任务筛选**: 添加 `pipeline_tag` 参数
  - 文本生成: https://huggingface.co/models?pipeline_tag=text-generation&library=transformers.js&sort=trending
  - 图像分类: https://huggingface.co/models?pipeline_tag=image-classification&library=transformers.js&sort=trending
  - 语音识别: https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&library=transformers.js&sort=trending

**提示：** 按任务类型筛选、按趋势/下载量排序，并查看模型卡片中的性能指标和使用示例。

### 3. 设备选择
选择模型运行位置：

```javascript
// Run on CPU (default for WASM)
const pipe = await pipeline('sentiment-analysis', 'model-id');

// Run on GPU (WebGPU - experimental)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  device: 'webgpu',
});
```

### 4. 量化选项
控制模型精度与性能的平衡：

```javascript
// Use quantized model (faster, smaller)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'q4',  // Options: 'fp32', 'fp16', 'q8', 'q4'
});
```

## 支持的任务

**注意：** 以下示例展示基本用法。

### 自然语言处理

#### 文本分类
```javascript
const classifier = await pipeline('text-classification');
const result = await classifier('This movie was amazing!');
```

#### 命名实体识别（NER）
```javascript
const ner = await pipeline('token-classification');
const entities = await ner('My name is John and I live in New York.');
```

#### 问答
```javascript
const qa = await pipeline('question-answering');
const answer = await qa({
  question: 'What is the capital of France?',
  context: 'Paris is the capital and largest city of France.'
});
```

#### 文本生成
```javascript
const generator = await pipeline('text-generation', 'onnx-community/gemma-3-270m-it-ONNX');
const text = await generator('Once upon a time', {
  max_new_tokens: 100,
  temperature: 0.7
});
```

**流式输出和对话：** 参见 **[文本生成指南](./references/TEXT_GENERATION.md)**，包含：
- 使用 `TextStreamer` 逐 token 流式输出
- 对话格式（system/user/assistant 角色）
- 生成参数（temperature、top_k、top_p）
- 浏览器和 Node.js 示例
- React 组件和 API 端点

#### 翻译
```javascript
const translator = await pipeline('translation', 'Xenova/nllb-200-distilled-600M');
const output = await translator('Hello, how are you?', {
  src_lang: 'eng_Latn',
  tgt_lang: 'fra_Latn'
});
```

#### 摘要
```javascript
const summarizer = await pipeline('summarization');
const summary = await summarizer(longText, {
  max_length: 100,
  min_length: 30
});
```

#### 零样本分类
```javascript
const classifier = await pipeline('zero-shot-classification');
const result = await classifier('This is a story about sports.', ['politics', 'sports', 'technology']);
```

### 计算机视觉

#### 图像分类
```javascript
const classifier = await pipeline('image-classification');
const result = await classifier('https://example.com/image.jpg');
// Or with local file
const result = await classifier(imageUrl);
```

#### 目标检测
```javascript
const detector = await pipeline('object-detection');
const objects = await detector('https://example.com/image.jpg');
// Returns: [{ label: 'person', score: 0.95, box: { xmin, ymin, xmax, ymax } }, ...]
```

#### 图像分割
```javascript
const segmenter = await pipeline('image-segmentation');
const segments = await segmenter('https://example.com/image.jpg');
```

#### 深度估计
```javascript
const depthEstimator = await pipeline('depth-estimation');
const depth = await depthEstimator('https://example.com/image.jpg');
```

#### 零样本图像分类
```javascript
const classifier = await pipeline('zero-shot-image-classification');
const result = await classifier('image.jpg', ['cat', 'dog', 'bird']);
```

### 音频处理

#### 自动语音识别
```javascript
const transcriber = await pipeline('automatic-speech-recognition');
const result = await transcriber('audio.wav');
// Returns: { text: 'transcribed text here' }
```

#### 音频分类
```javascript
const classifier = await pipeline('audio-classification');
const result = await classifier('audio.wav');
```

#### 文本转语音
```javascript
const synthesizer = await pipeline('text-to-speech', 'Xenova/speecht5_tts');
const audio = await synthesizer('Hello, this is a test.', {
  speaker_embeddings: speakerEmbeddings
});
```

### 多模态

#### 图像描述（图生文）
```javascript
const captioner = await pipeline('image-to-text');
const caption = await captioner('image.jpg');
```

#### 文档问答
```javascript
const docQA = await pipeline('document-question-answering');
const answer = await docQA('document-image.jpg', 'What is the total amount?');
```

#### 零样本目标检测
```javascript
const detector = await pipeline('zero-shot-object-detection');
const objects = await detector('image.jpg', ['person', 'car', 'tree']);
```

### 特征提取（Embeddings）

```javascript
const extractor = await pipeline('feature-extraction');
const embeddings = await extractor('This is a sentence to embed.');
// Returns: tensor of shape [1, sequence_length, hidden_size]

// For sentence embeddings (mean pooling)
const extractor = await pipeline('feature-extraction', 'onnx-community/all-MiniLM-L6-v2-ONNX');
const embeddings = await extractor('Text to embed', { pooling: 'mean', normalize: true });
```

## 查找和选择模型

### 浏览 Hugging Face Hub

在 Hugging Face Hub 上发现兼容的 Transformers.js 模型：

**基础 URL（全部模型）：**
```
https://huggingface.co/models?library=transformers.js&sort=trending
```

**按任务筛选**，使用 `pipeline_tag` 参数：

| 任务 | URL |
|------|-----|
| **文本生成** | https://huggingface.co/models?pipeline_tag=text-generation&library=transformers.js&sort=trending |
| **文本分类** | https://huggingface.co/models?pipeline_tag=text-classification&library=transformers.js&sort=trending |
| **翻译** | https://huggingface.co/models?pipeline_tag=translation&library=transformers.js&sort=trending |
| **摘要** | https://huggingface.co/models?pipeline_tag=summarization&library=transformers.js&sort=trending |
| **问答** | https://huggingface.co/models?pipeline_tag=question-answering&library=transformers.js&sort=trending |
| **图像分类** | https://huggingface.co/models?pipeline_tag=image-classification&library=transformers.js&sort=trending |
| **目标检测** | https://huggingface.co/models?pipeline_tag=object-detection&library=transformers.js&sort=trending |
| **图像分割** | https://huggingface.co/models?pipeline_tag=image-segmentation&library=transformers.js&sort=trending |
| **语音识别** | https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&library=transformers.js&sort=trending |
| **音频分类** | https://huggingface.co/models?pipeline_tag=audio-classification&library=transformers.js&sort=trending |
| **图生文** | https://huggingface.co/models?pipeline_tag=image-to-text&library=transformers.js&sort=trending |
| **特征提取** | https://huggingface.co/models?pipeline_tag=feature-extraction&library=transformers.js&sort=trending |
| **零样本分类** | https://huggingface.co/models?pipeline_tag=zero-shot-classification&library=transformers.js&sort=trending |

**排序选项：**
- `&sort=trending` - 近期最热门
- `&sort=downloads` - 总下载量最多
- `&sort=likes` - 社区最受欢迎
- `&sort=modified` - 最近更新

### 选择合适的模型

选择模型时需考虑以下因素：

**1. 模型大小**
- **小型（< 100MB）**：速度快，适合浏览器，精度有限
- **中型（100MB - 500MB）**：性能均衡，适合大多数场景
- **大型（> 500MB）**：精度高，速度慢，更适合 Node.js 或高性能设备

**2. 量化**
模型通常提供不同量化级别：
- `fp32` - 全精度（最大，最精确）
- `fp16` - 半精度（更小，仍然精确）
- `q8` - 8位量化（更小，轻微精度损失）
- `q4` - 4位量化（最小，明显精度损失）

**3. 任务兼容性**
查看模型卡片了解：
- 支持的任务（部分模型支持多种任务）
- 输入/输出格式
- 语言支持（多语言 vs 仅英文）
- 许可证限制

**4. 性能指标**
模型卡片通常展示：
- 准确率分数
- 基准测试结果
- 推理速度
- 内存需求

### 示例：查找文本生成模型

```javascript
// 1. Visit: https://huggingface.co/models?pipeline_tag=text-generation&library=transformers.js&sort=trending

// 2. Browse and select a model (e.g., onnx-community/gemma-3-270m-it-ONNX)

// 3. Check model card for:
//    - Model size: ~270M parameters
//    - Quantization: q4 available
//    - Language: English
//    - Use case: Instruction-following chat

// 4. Use the model:
import { pipeline } from '@huggingface/transformers';

const generator = await pipeline(
  'text-generation',
  'onnx-community/gemma-3-270m-it-ONNX',
  { dtype: 'q4' } // Use quantized version for faster inference
);

const output = await generator('Explain quantum computing in simple terms.', {
  max_new_tokens: 100
});

await generator.dispose();
```

### 模型选择技巧

1. **从小模型开始**：先用小模型测试，需要时再升级
2. **检查 ONNX 支持**：确保模型有 ONNX 文件（在模型仓库中查找 `onnx` 文件夹）
3. **阅读模型卡片**：模型卡片包含使用示例、限制和基准测试
4. **本地测试**：在你的环境中测试推理速度和内存占用
5. **社区模型**：查找 `Xenova`（Transformers.js 维护者）或 `onnx-community` 的模型
6. **版本锁定**：生产环境中使用特定 git commit 确保稳定性：
   ```javascript
   const pipe = await pipeline('task', 'model-id', { revision: 'abc123' });
   ```

## 高级配置

### 环境配置（`env`）

`env` 对象提供对 Transformers.js 执行、缓存和模型加载的全面控制。

**快速概览：**

```javascript
import { env } from '@huggingface/transformers';

// View version
console.log(env.version); // e.g., '3.8.1'

// Common settings
env.allowRemoteModels = true;  // Load from Hugging Face Hub
env.allowLocalModels = false;  // Load from file system
env.localModelPath = '/models/'; // Local model directory
env.useFSCache = true;         // Cache models on disk (Node.js)
env.useBrowserCache = true;    // Cache models in browser
env.cacheDir = './.cache';     // Cache directory location
```

**配置模式：**

```javascript
// Development: Fast iteration with remote models
env.allowRemoteModels = true;
env.useFSCache = true;

// Production: Local models only
env.allowRemoteModels = false;
env.allowLocalModels = true;
env.localModelPath = '/app/models/';

// Custom CDN
env.remoteHost = 'https://cdn.example.com/models';

// Disable caching (testing)
env.useFSCache = false;
env.useBrowserCache = false;
```

所有配置选项、缓存策略、缓存管理、预下载模型等完整文档，参见：

**→ [配置参考](./references/CONFIGURATION.md)**

### 使用 Tensor

```javascript
import { AutoTokenizer, AutoModel } from '@huggingface/transformers';

// Load tokenizer and model separately for more control
const tokenizer = await AutoTokenizer.from_pretrained('bert-base-uncased');
const model = await AutoModel.from_pretrained('bert-base-uncased');

// Tokenize input
const inputs = await tokenizer('Hello world!');

// Run model
const outputs = await model(inputs);
```

### 批量处理

```javascript
const classifier = await pipeline('sentiment-analysis');

// Process multiple texts
const results = await classifier([
  'I love this!',
  'This is terrible.',
  'It was okay.'
]);
```

## 浏览器注意事项

### WebGPU 使用
WebGPU 在浏览器中提供 GPU 加速：

```javascript
const pipe = await pipeline('text-generation', 'onnx-community/gemma-3-270m-it-ONNX', {
  device: 'webgpu',
  dtype: 'fp32'
});
```

**注意**：WebGPU 处于实验阶段。请检查浏览器兼容性，遇到问题时提交 issue。

### WASM 性能
浏览器默认使用 WASM 执行：

```javascript
// Optimized for browsers with quantization
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'q8'  // or 'q4' for even smaller size
});
```

### 进度追踪和加载指示器

模型可能很大（从几 MB 到数 GB），包含多个文件。通过向 `pipeline()` 函数传递回调来追踪下载进度：

```javascript
import { pipeline } from '@huggingface/transformers';

// Track progress for each file
const fileProgress = {};

function onProgress(info) {
  console.log(`${info.status}: ${info.file}`);
  
  if (info.status === 'progress') {
    fileProgress[info.file] = info.progress;
    console.log(`${info.file}: ${info.progress.toFixed(1)}%`);
  }
  
  if (info.status === 'done') {
    console.log(`✓ ${info.file} complete`);
  }
}

// Pass callback to pipeline
const classifier = await pipeline('sentiment-analysis', null, {
  progress_callback: onProgress
});
```

**进度信息属性：**

```typescript
interface ProgressInfo {
  status: 'initiate' | 'download' | 'progress' | 'done' | 'ready';
  name: string;      // Model id or path
  file: string;      // File being processed
  progress?: number; // Percentage (0-100, only for 'progress' status)
  loaded?: number;   // Bytes downloaded (only for 'progress' status)
  total?: number;    // Total bytes (only for 'progress' status)
}
```

完整示例包括浏览器 UI、React 组件、CLI 进度条和重试逻辑，参见：

**→ [Pipeline 选项 - 进度回调](./references/PIPELINE_OPTIONS.md#progress-callback)**

## 错误处理

```javascript
try {
  const pipe = await pipeline('sentiment-analysis', 'model-id');
  const result = await pipe('text to analyze');
} catch (error) {
  if (error.message.includes('fetch')) {
    console.error('Model download failed. Check internet connection.');
  } else if (error.message.includes('ONNX')) {
    console.error('Model execution failed. Check model compatibility.');
  } else {
    console.error('Unknown error:', error);
  }
}
```

## 性能优化

1. **复用 Pipeline**：创建一次 pipeline，多次推理复用
2. **使用量化**：从 `q8` 或 `q4` 开始以获得更快推理速度
3. **批量处理**：尽量一次处理多个输入
4. **缓存模型**：模型自动缓存（详见 **[缓存参考](./references/CACHE.md)**，涵盖浏览器 Cache API、Node.js 文件系统缓存和自定义实现）
5. **大模型用 WebGPU**：对受益于 GPU 加速的模型使用 WebGPU
6. **控制上下文长度**：文本生成时限制 `max_new_tokens` 避免内存问题
7. **释放资源**：使用完毕调用 `pipe.dispose()` 释放内存

## 内存管理

**重要：** 使用完毕必须调用 `pipe.dispose()` 防止内存泄漏。

```javascript
const pipe = await pipeline('sentiment-analysis');
const result = await pipe('Great product!');
await pipe.dispose();  // ✓ Free memory (100MB - several GB per model)
```

**何时释放：**
- 应用关闭或组件卸载时
- 加载不同模型之前
- 长时间运行的应用中批量处理完成后

模型占用大量内存并持有 GPU/CPU 资源。释放对浏览器内存限制和服务器稳定性至关重要。

详细模式（React 清理、服务器、浏览器）参见 **[代码示例](./references/EXAMPLES.md)**

## 故障排除

### 找不到模型
- 确认模型存在于 Hugging Face Hub
- 检查模型名称拼写
- 确保模型有 ONNX 文件（在模型仓库中查找 `onnx` 文件夹）

### 内存问题
- 使用更小的模型或量化版本（`dtype: 'q4'`）
- 减小批量大小
- 用 `max_length` 限制序列长度

### WebGPU 错误
- 检查浏览器兼容性（Chrome 113+、Edge 113+）
- 如果 `fp32` 失败，尝试 `dtype: 'fp16'`
- WebGPU 不可用时回退到 WASM

## 参考文档

### 本技能
- **[Pipeline 选项](./references/PIPELINE_OPTIONS.md)** - 配置 `pipeline()` 的 `progress_callback`、`device`、`dtype` 等
- **[配置参考](./references/CONFIGURATION.md)** - 全局 `env` 配置（缓存和模型加载）
- **[缓存参考](./references/CACHE.md)** - 浏览器 Cache API、Node.js 文件系统缓存和自定义缓存实现
- **[文本生成指南](./references/TEXT_GENERATION.md)** - 流式输出、对话格式和生成参数
- **[模型架构](./references/MODEL_ARCHITECTURES.md)** - 支持的模型和选择技巧
- **[代码示例](./references/EXAMPLES.md)** - 不同运行时的实际实现

### 官方 Transformers.js
- 官方文档: https://huggingface.co/docs/transformers.js
- API 参考: https://huggingface.co/docs/transformers.js/api/pipelines
- 模型中心: https://huggingface.co/models?library=transformers.js
- GitHub: https://github.com/huggingface/transformers.js
- 示例: https://github.com/huggingface/transformers.js/tree/main/examples

## 最佳实践

1. **始终释放 Pipeline**：使用完毕调用 `pipe.dispose()` — 防止内存泄漏的关键
2. **优先使用 Pipeline**：除非需要精细控制，否则使用 pipeline API
3. **先本地测试**：部署前用小输入测试模型
4. **关注模型大小**：注意 Web 应用的模型下载体积
5. **处理加载状态**：显示进度指示器以改善用户体验
6. **版本锁定**：生产环境锁定特定模型版本以确保稳定性
7. **错误边界**：始终用 try-catch 包裹 pipeline 调用
8. **渐进增强**：为不支持的浏览器提供回退方案
9. **复用模型**：加载一次，多次使用 — 不要重复创建 pipeline
10. **优雅关闭**：服务器端在 SIGTERM/SIGINT 时释放模型

## 快速参考：任务 ID

| 任务 | 任务 ID |
|------|---------|
| 文本分类 | `text-classification` 或 `sentiment-analysis` |
| Token 分类 | `token-classification` 或 `ner` |
| 问答 | `question-answering` |
| 掩码填充 | `fill-mask` |
| 摘要 | `summarization` |
| 翻译 | `translation` |
| 文本生成 | `text-generation` |
| 文本到文本生成 | `text2text-generation` |
| 零样本分类 | `zero-shot-classification` |
| 图像分类 | `image-classification` |
| 图像分割 | `image-segmentation` |
| 目标检测 | `object-detection` |
| 深度估计 | `depth-estimation` |
| 图像到图像 | `image-to-image` |
| 零样本图像分类 | `zero-shot-image-classification` |
| 零样本目标检测 | `zero-shot-object-detection` |
| 自动语音识别 | `automatic-speech-recognition` |
| 音频分类 | `audio-classification` |
| 文本转语音 | `text-to-speech` 或 `text-to-audio` |
| 图生文 | `image-to-text` |
| 文档问答 | `document-question-answering` |
| 特征提取 | `feature-extraction` |
| 句子相似度 | `sentence-similarity` |

---

此技能可将最先进的机器学习能力直接集成到 JavaScript 应用中，无需单独的 ML 服务器或 Python 环境。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
