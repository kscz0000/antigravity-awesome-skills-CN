# Pipeline 选项参考

使用 `pipeline()` 函数的 `PretrainedModelOptions` 参数配置模型加载和推理的指南。

## 目录

1. [概述](#概述)
2. [基本选项](#基本选项)
3. [模型加载选项](#模型加载选项)
4. [设备和性能选项](#设备和性能选项)
5. [常见配置模式](#常见配置模式)

## 概述

`pipeline()` 函数接受三个参数：

```javascript
import { pipeline } from '@huggingface/transformers';

const pipe = await pipeline(
  'task-name',           // 1. Task type (e.g., 'sentiment-analysis')
  'model-id',            // 2. Model identifier (optional, uses default if null)
  options                // 3. PretrainedModelOptions (optional)
);
```

第三个参数 `options` 用于配置模型的加载和执行方式。

### 可用选项

```typescript
interface PretrainedModelOptions {
  // Progress tracking
  progress_callback?: (info: ProgressInfo) => void;
  
  // Model configuration
  config?: PretrainedConfig;
  
  // Cache and loading
  cache_dir?: string;
  local_files_only?: boolean;
  revision?: string;
  
  // Model-specific settings
  subfolder?: string;
  model_file_name?: string;
  
  // Device and performance
  device?: DeviceType | Record<string, DeviceType>;
  dtype?: DataType | Record<string, DataType>;
  
  // External data format (large models)
  use_external_data_format?: boolean | number | Record<string, boolean | number>;
  
  // ONNX Runtime settings
  session_options?: InferenceSession.SessionOptions;
}
```

## 基本选项

### 进度回调

追踪模型下载和加载进度。**注意：** 模型包含多个文件（模型权重、配置、分词器等），每个文件独立报告进度：

```javascript
const fileProgress = {};

const pipe = await pipeline('sentiment-analysis', null, {
  progress_callback: (info) => {
    if (info.status === 'progress') {
      fileProgress[info.file] = info.progress;
      console.log(`${info.file}: ${info.progress.toFixed(1)}%`);
    }
    
    if (info.status === 'done') {
      console.log(`✓ ${info.file} complete`);
    }
  }
});
```

**进度信息类型：**

```typescript
type ProgressInfo = {
  status: 'initiate' | 'download' | 'progress' | 'done' | 'ready';
  name: string;       // Model id or path
  file: string;       // File being processed
  progress?: number;  // Percentage (0-100, only for 'progress' status)
  loaded?: number;    // Bytes downloaded (only for 'progress' status)
  total?: number;     // Total bytes (only for 'progress' status)
};
```

**示例：浏览器多文件加载 UI**

```javascript
const statusDiv = document.getElementById('status');
const progressContainer = document.getElementById('progress-container');
const fileProgressBars = {};

const pipe = await pipeline('image-classification', null, {
  progress_callback: (info) => {
    if (info.status === 'progress') {
      // Create progress bar for each file if not exists
      if (!fileProgressBars[info.file]) {
        const fileDiv = document.createElement('div');
        fileDiv.innerHTML = `
          <div class="file-name">${info.file}</div>
          <div class="progress-bar">
            <div class="progress-fill" style="width: 0%"></div>
          </div>
        `;
        progressContainer.appendChild(fileDiv);
        fileProgressBars[info.file] = fileDiv.querySelector('.progress-fill');
      }
      
      // Update progress bar
      fileProgressBars[info.file].style.width = `${info.progress}%`;
      
      const mb = (info.loaded / 1024 / 1024).toFixed(2);
      const totalMb = (info.total / 1024 / 1024).toFixed(2);
      statusDiv.textContent = `${info.file}: ${mb}/${totalMb} MB`;
    }
    
    if (info.status === 'ready') {
      statusDiv.textContent = 'Model ready!';
    }
  }
});
```

更多进度追踪示例参见本节上方的示例。

### 自定义配置

覆盖模型的默认配置：

```javascript
import { pipeline } from '@huggingface/transformers';

const pipe = await pipeline('text-generation', 'model-id', {
  config: {
    max_length: 512,
    temperature: 0.8,
    // ... other config options
  }
});
```

**适用场景：**
- 覆盖默认生成参数
- 调整模型特定设置
- 无需修改模型文件即可测试不同配置

## 模型加载选项

### 缓存目录

指定下载模型的缓存位置：

```javascript
// Node.js: Custom cache location
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  cache_dir: './my-custom-cache'
});
```

**默认行为：**
- 未指定时使用 `env.cacheDir`（默认：`./.cache`）
- 仅在 `env.useFSCache = true` 时生效（Node.js）
- 浏览器缓存使用 Cache API（通过 `env.cacheKey` 配置）



### 仅本地文件

禁止任何网络请求：

```javascript
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  local_files_only: true
});
```

**适用场景：**
- 离线应用
- 隔离网络环境
- 使用预下载模型测试
- 生产部署中捆绑模型

**重要提示：**
- 模型必须已缓存或本地可用
- 本地找不到模型时会抛出错误
- 需要 `env.allowLocalModels = true`



### 模型版本

指定特定的模型版本（git 分支、标签或 commit）：

```javascript
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  revision: 'v1.0.0'  // Use specific version
});

// Or use a branch
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  revision: 'experimental'
});

// Or use a commit hash
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  revision: 'abc123def456'
});
```

**默认值：** `'main'`（最新版本）

**适用场景：**
- 生产环境锁定稳定版本
- 测试实验性功能
- 使用特定模型版本复现结果
- 使用开发中的模型

**重要提示：**
- 仅适用于远程模型（Hugging Face Hub）
- 本地文件路径时忽略
- 每个版本独立缓存

### 模型子目录

指定模型仓库中的子目录：

```javascript
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  subfolder: 'onnx'  // Default: 'onnx'
});
```

**默认值：** `'onnx'`

**适用场景：**
- 自定义模型仓库结构
- 同一仓库中多个模型变体
- 组织偏好



### 模型文件名

指定自定义模型文件名（不含 `.onnx` 扩展名）：

```javascript
const pipe = await pipeline('text-generation', 'model-id', {
  model_file_name: 'decoder_model_merged'
});
// Loads: decoder_model_merged.onnx
```

**适用场景：**
- 非标准文件名的模型
- 选择特定模型变体
- 编码器-解码器模型的独立文件

**注意：** 目前仅对纯编码器或纯解码器模型有效。



## 设备和性能选项

### 设备选择

选择模型运行位置：

```javascript
// Run on CPU (WASM - default)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  device: 'wasm'
});

// Run on GPU (WebGPU)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  device: 'webgpu'
});
```

**常用设备：**
- `'wasm'` - WebAssembly（CPU，兼容性最好）
- `'webgpu'` - WebGPU（GPU，浏览器中更快）
- `'cpu'` - CPU
- `'gpu'` - 自动检测 GPU
- `'cuda'` - NVIDIA CUDA（带 GPU 的 Node.js）

完整列表参见 [devices.js 源码](https://github.com/huggingface/transformers.js/blob/main/src/utils/devices.js)。

**按组件选择设备：**

对于包含多个组件的模型（编码器-解码器、视觉-编码器-解码器等）：

```javascript
const pipe = await pipeline('automatic-speech-recognition', 'model-id', {
  device: {
    encoder: 'webgpu',    // Run encoder on GPU
    decoder: 'wasm'       // Run decoder on CPU
  }
});
```

**WebGPU 要求：**
- Chrome/Edge 113+
- 启用 chrome://flags/#enable-unsafe-webgpu（如需要）
- 足够的 GPU 内存



### 数据类型（量化）

控制模型精度和大小：

```javascript
// Full precision (largest, most accurate)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'fp32'
});

// Half precision (balanced)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'fp16'
});

// 8-bit quantization (smaller, faster)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'q8'
});

// 4-bit quantization (smallest, fastest)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'q4'
});
```

**常用数据类型：**
- `'fp32` - 32位浮点（全精度）
- `'fp16'` - 16位浮点（半精度）
- `'q8'` - 8位量化（良好平衡）
- `'q4'` - 4位量化（最大压缩）
- `'int8'` - 8位整数
- `'uint8'` - 8位无符号整数

完整列表参见 [dtypes.js 源码](https://github.com/huggingface/transformers.js/blob/main/src/utils/dtypes.js)。

**按组件选择数据类型：**

```javascript
const pipe = await pipeline('automatic-speech-recognition', 'model-id', {
  dtype: {
    encoder: 'fp32',  // Encoder at full precision
    decoder: 'q8'     // Decoder quantized
  }
});
```

**权衡：**

| 数据类型 | 模型大小 | 速度 | 精度 | 适用场景 |
|-----------|----------|------|------|----------|
| `fp32` | 最大 | 最慢 | 最高 | 研究，最高质量 |
| `fp16` | 中等 | 中等 | 高 | 生产，GPU 推理 |
| `q8` | 小 | 快 | 良好 | 生产，CPU 推理 |
| `q4` | 最小 | 最快 | 可接受 | 边缘设备，实时应用 |



### 外部数据格式

对于 >= 2GB 的模型，ONNX 使用外部数据格式：

```javascript
// Automatically detect and load external data
const pipe = await pipeline('text-generation', 'large-model-id', {
  use_external_data_format: true
});

// Specify number of external data chunks
const pipe = await pipeline('text-generation', 'large-model-id', {
  use_external_data_format: 5  // Load 5 chunks (model.onnx_data_0 to _4)
});
```

**工作原理：**
- >= 2GB 的模型将权重拆分为独立文件
- 主文件：`model.onnx`（仅结构）
- 数据文件：`model.onnx_data` 或 `model.onnx_data_0`、`model.onnx_data_1` 等

**默认行为：**
- `false` - 无外部数据（< 2GB 模型）
- `true` - 自动加载外部数据
- `number` - 加载指定数量的外部数据块

**最大块数：** 100（由 `MAX_EXTERNAL_DATA_CHUNKS` 定义）

**按组件的外部数据：**

```javascript
const pipe = await pipeline('text-generation', 'large-model-id', {
  use_external_data_format: {
    encoder: true,
    decoder: 3  // Decoder has 3 external data chunks
  }
});
```



### Session 选项

高级 ONNX Runtime 配置：

```javascript
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  session_options: {
    executionProviders: ['webgpu', 'wasm'],
    graphOptimizationLevel: 'all',
    enableCpuMemArena: true,
    enableMemPattern: true,
    executionMode: 'sequential',
    logSeverityLevel: 2,
    logVerbosityLevel: 0
  }
});
```

**常用 session 选项：**

| 选项 | 描述 | 默认值 |
|------|------|--------|
| `executionProviders` | 执行提供程序有序列表 | `['wasm']` |
| `graphOptimizationLevel` | 图优化：`'disabled'`、`'basic'`、`'extended'`、`'all'` | `'all'` |
| `enableCpuMemArena` | 启用 CPU 内存竞技场以加速内存分配 | `true` |
| `enableMemPattern` | 启用内存模式优化 | `true` |
| `executionMode` | `'sequential'` 或 `'parallel'` | `'sequential'` |
| `logSeverityLevel` | 0=详细，1=信息，2=警告，3=错误，4=致命 | `2` |
| `freeDimensionOverrides` | 覆盖动态维度（如 `{ batch_size: 1 }`） | - |

**适用场景：**
- 针对特定硬件微调性能
- 调试模型执行问题
- 覆盖动态形状
- 控制内存使用



## 常见配置模式

### 开发环境

带进度追踪的快速迭代：

```javascript
import { pipeline } from '@huggingface/transformers';

const pipe = await pipeline('sentiment-analysis', null, {
  progress_callback: (info) => {
    if (info.status === 'progress') {
      console.log(`${info.file}: ${info.progress.toFixed(1)}%`);
    }
  }
});
```

### 生产环境（GPU）

使用 WebGPU + fp16 获得更好性能：

```javascript
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  device: 'webgpu',
  dtype: 'fp16'
});
```

### 生产环境（CPU）

使用量化减小体积并加速 CPU 推理：

```javascript
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'q8'  // or 'q4' for even smaller
});
```

### 离线/本地

禁止网络请求，仅使用本地模型：

```javascript
import { pipeline, env } from '@huggingface/transformers';

env.allowLocalModels = true;
env.localModelPath = './models/';

const pipe = await pipeline('sentiment-analysis', 'model-id', {
  local_files_only: true
});
```

### 按组件配置

对于编码器-解码器模型，分别配置每个组件：

```javascript
const pipe = await pipeline('automatic-speech-recognition', 'model-id', {
  device: {
    encoder: 'webgpu',
    decoder: 'wasm'
  },
  dtype: {
    encoder: 'fp16',
    decoder: 'q8'
  }
});
```

## 相关文档

- [配置参考](./CONFIGURATION.md) - 使用 `env` 对象的环境配置
- [文本生成指南](./TEXT_GENERATION.md) - 文本生成选项和流式输出
- [模型架构](./MODEL_ARCHITECTURES.md) - 支持的模型和选择技巧
- [主技能指南](../SKILL.md) - Transformers.js 入门

## 最佳实践

1. **进度回调**：大模型使用 `progress_callback` 显示下载进度
2. **量化**：CPU 推理使用 `q8` 或 `q4` 以减小体积并提升速度
3. **设备选择**：可用时使用 `webgpu` 获得更好性能
4. **离线优先**：生产环境使用 `local_files_only: true` 避免运行时下载
5. **版本锁定**：使用 `revision` 锁定模型版本以确保可复现部署
6. **内存管理**：使用完毕始终调用 `pipe.dispose()` 释放 pipeline

---

本文档涵盖 `pipeline()` 函数的所有可用选项。环境级配置（远程主机、全局缓存设置、WASM 路径）参见[配置参考](./CONFIGURATION.md)。
