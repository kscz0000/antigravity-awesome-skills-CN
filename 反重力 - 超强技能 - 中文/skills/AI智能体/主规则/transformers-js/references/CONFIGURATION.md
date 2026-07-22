# 环境配置参考

使用 `env` 对象配置 Transformers.js 行为的完整指南。

## 目录

1. [概述](#概述)
2. [远程模型配置](#远程模型配置)
3. [本地模型配置](#本地模型配置)
4. [缓存配置](#缓存配置)
5. [WASM 配置](#wasm-配置)
6. [常见配置模式](#常见配置模式)
7. [环境最佳实践](#环境最佳实践)

## 概述

`env` 对象提供对 Transformers.js 执行、缓存和模型加载的全面控制：

```javascript
import { env } from '@huggingface/transformers';

// View current version
console.log(env.version); // e.g., '3.8.1'
```

### 可用属性

```typescript
interface TransformersEnvironment {
  // Version info
  version: string;
  
  // Backend configuration
  backends: {
    onnx: Partial<ONNXEnv>;
  };
  
  // Remote model settings
  allowRemoteModels: boolean;
  remoteHost: string;
  remotePathTemplate: string;
  
  // Local model settings
  allowLocalModels: boolean;
  localModelPath: string;
  useFS: boolean;
  
  // Cache settings
  useBrowserCache: boolean;
  useFSCache: boolean;
  cacheDir: string | null;
  useCustomCache: boolean;
  customCache: CacheInterface | null;
  useWasmCache: boolean;
  cacheKey: string;
}
```

## 远程模型配置

控制从远程源加载模型的方式（默认：Hugging Face Hub）。

### 禁用远程加载

```javascript
import { env } from '@huggingface/transformers';

// Force local-only mode (no network requests)
env.allowRemoteModels = false;
```

**适用场景：** 离线应用、安全要求或隔离网络环境。

### 自定义模型主机

```javascript
import { env } from '@huggingface/transformers';

// Use your own CDN or model server
env.remoteHost = 'https://cdn.example.com/models';

// Customize the URL pattern
// Default: '{model}/resolve/{revision}/{file}'
env.remotePathTemplate = 'custom/{model}/{file}';
```

**适用场景：** 自托管模型、使用 CDN 加速下载或企业代理。

### 示例：私有模型服务器

```javascript
import { env, pipeline } from '@huggingface/transformers';

// Configure custom model host
env.remoteHost = 'https://models.mycompany.com';
env.remotePathTemplate = '{model}/{file}';

// Models will be loaded from:
// https://models.mycompany.com/my-model/model.onnx
const pipe = await pipeline('sentiment-analysis', 'my-model');
```

## 本地模型配置

控制从本地文件系统加载模型。

### 启用本地模型

```javascript
import { env } from '@huggingface/transformers';

// Enable local file system loading
env.allowLocalModels = true;

// Set the base path for local models
env.localModelPath = '/path/to/models/';
```

**默认值：**
- 浏览器：`allowLocalModels = false`，`localModelPath = '/models/'`
- Node.js：`allowLocalModels = true`，`localModelPath = '/models/'`

### 文件系统控制

```javascript
import { env } from '@huggingface/transformers';

// Disable file system usage entirely (Node.js only)
env.useFS = false;
```

### 示例：本地模型目录结构

```
/app/models/
├── onnx-community/
│   ├── Supertonic-TTS-ONNX/
│   │   ├── config.json
│   │   ├── tokenizer.json
│   │   ├── model.onnx
│   │   └── ...
│   └── yolo26l-pose-ONNX/
│       ├── config.json
│       ├── preprocessor_config.json
│       ├── model.onnx
│       └── ...
```

```javascript
env.allowLocalModels = true;
env.localModelPath = '/app/models/';
env.allowRemoteModels = false; // Offline mode

const classifier = await pipeline('sentiment-analysis', 'Xenova/distilbert-base-uncased-finetuned-sst-2-english');
```

## 缓存配置

Transformers.js 支持多种缓存策略以提升性能和减少网络使用。

### 快速配置

```javascript
import { env } from '@huggingface/transformers';

// Browser cache (Cache API)
env.useBrowserCache = true; // default: true
env.cacheKey = 'my-app-transformers-cache'; // default: 'transformers-cache'

// Node.js filesystem cache
env.useFSCache = true; // default: true
env.cacheDir = './custom-cache-dir'; // default: './.cache'

// Custom cache implementation
env.useCustomCache = true;
env.customCache = new CustomCache(); // Implement Cache API interface

// WASM binary caching
env.useWasmCache = true; // default: true
```

### 禁用缓存

```javascript
import { env } from '@huggingface/transformers';

// Disable all caching (re-download on every load)
env.useFSCache = false;
env.useBrowserCache = false;
env.useWasmCache = false;
env.cacheDir = null;
```

完整缓存文档包括：
- 浏览器 Cache API 详情和存储限制
- Node.js 文件系统缓存结构和管理
- 自定义缓存实现（Redis、数据库、S3）
- 缓存清理和监控策略
- 最佳实践和故障排除

参见 **[缓存参考](./CACHE.md)**

## WASM 配置

配置 ONNX Runtime Web Assembly 后端设置。

### 基本 WASM 设置

```javascript
import { env } from '@huggingface/transformers';

// Set custom WASM paths
env.backends.onnx.wasm.wasmPaths = 'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/';

// Configure number of threads (Node.js only)
env.backends.onnx.wasm.numThreads = 4;

// Enable/disable SIMD (single instruction, multiple data)
env.backends.onnx.wasm.simd = true;
```

### 代理配置

```javascript
import { env } from '@huggingface/transformers';

// Configure proxy for WASM downloads
env.backends.onnx.wasm.proxy = true;
```

### 自托管 WASM 文件

```javascript
import { env } from '@huggingface/transformers';

// Host WASM files on your own server
env.backends.onnx.wasm.wasmPaths = '/static/wasm/';
```

**必需文件：**
- `ort-wasm.wasm` - 主 WASM 二进制文件
- `ort-wasm-simd.wasm` - 启用 SIMD 的 WASM 二进制文件
- `ort-wasm-threaded.wasm` - 多线程 WASM 二进制文件
- `ort-wasm-simd-threaded.wasm` - SIMD + 多线程 WASM 二进制文件

## 常见配置模式

### 开发环境

```javascript
import { env } from '@huggingface/transformers';

// Fast iteration with caching
env.allowRemoteModels = true;
env.useBrowserCache = true; // Browser
env.useFSCache = true;      // Node.js
env.cacheDir = './.cache';
```

### 生产环境（本地模型）

```javascript
import { env } from '@huggingface/transformers';

// Secure, offline-capable setup
env.allowRemoteModels = false;
env.allowLocalModels = true;
env.localModelPath = '/app/models/';
env.useFSCache = false; // Models already local
```

### 离线优先应用

```javascript
import { env } from '@huggingface/transformers';

// Try local first, fall back to remote
env.allowLocalModels = true;
env.localModelPath = './models/';
env.allowRemoteModels = true;
env.useFSCache = true;
env.cacheDir = './cache';
```

### 自定义 CDN

```javascript
import { env } from '@huggingface/transformers';

// Use your own model hosting
env.remoteHost = 'https://cdn.example.com/ml-models';
env.remotePathTemplate = '{model}/{file}';
env.useBrowserCache = true;
```

### 内存受限环境

```javascript
import { env } from '@huggingface/transformers';

// Minimize disk/memory usage
env.useFSCache = false;
env.useBrowserCache = false;
env.useWasmCache = false;
env.cacheDir = null;
```

### 测试/CI 环境

```javascript
import { env } from '@huggingface/transformers';

// Predictable, isolated testing
env.allowRemoteModels = false;
env.allowLocalModels = true;
env.localModelPath = './test-fixtures/models/';
env.useFSCache = false;
```



## 环境最佳实践

### 1. 尽早配置

在加载任何模型之前设置 `env` 属性：

```javascript
import { env, pipeline } from '@huggingface/transformers';

// ✓ Good: Configure before loading
env.allowRemoteModels = false;
env.localModelPath = '/app/models/';
const pipe = await pipeline('sentiment-analysis');

// ✗ Bad: Configuring after loading may not take effect
const pipe = await pipeline('sentiment-analysis');
env.allowRemoteModels = false; // Too late!
```

### 2. 使用环境变量

```javascript
import { env } from '@huggingface/transformers';

// Configure based on environment
env.allowRemoteModels = process.env.NODE_ENV === 'development';
env.cacheDir = process.env.MODEL_CACHE_DIR || './.cache';
env.localModelPath = process.env.LOCAL_MODELS_PATH || '/app/models/';
```

### 3. 优雅处理错误

```javascript
import { pipeline, env } from '@huggingface/transformers';

try {
  env.allowRemoteModels = false;
  const pipe = await pipeline('sentiment-analysis', 'my-model');
} catch (error) {
  if (error.message.includes('not found')) {
    console.error('Model not found locally. Enable remote models or download the model.');
  }
  throw error;
}
```

### 4. 记录配置

```javascript
import { env } from '@huggingface/transformers';

console.log('Transformers.js Configuration:', {
  version: env.version,
  allowRemoteModels: env.allowRemoteModels,
  allowLocalModels: env.allowLocalModels,
  localModelPath: env.localModelPath,
  cacheDir: env.cacheDir,
  useFSCache: env.useFSCache,
  useBrowserCache: env.useBrowserCache
});
```

## 相关文档

- **[缓存参考](./CACHE.md)** - 缓存完整指南（浏览器、Node.js、自定义实现）
- [Pipeline 选项](./PIPELINE_OPTIONS.md) - 配置 pipeline 加载的 `progress_callback`、`device`、`dtype` 等
- [模型架构](./MODEL_ARCHITECTURES.md) - 支持的模型和架构
- [代码示例](./EXAMPLES.md) - 不同运行时的代码示例
- [主技能指南](../SKILL.md) - 入门和常见用法
