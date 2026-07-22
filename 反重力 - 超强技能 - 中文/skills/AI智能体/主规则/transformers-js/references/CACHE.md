# 缓存参考

Transformers.js 模型在不同环境下的缓存策略完整指南。

## 目录

1. [概述](#概述)
2. [浏览器缓存](#浏览器缓存)
3. [Node.js 缓存](#nodejs-缓存)
4. [自定义缓存实现](#自定义缓存实现)
5. [缓存配置](#缓存配置)

## 概述

Transformers.js 模型可能很大（从几 MB 到数 GB），因此缓存对性能至关重要。不同环境的缓存策略不同：

- **浏览器**：使用 Cache API（浏览器缓存存储）
- **Node.js**：使用文件系统缓存，路径为 `~/.cache/huggingface/`
- **自定义**：实现自己的缓存（数据库、云存储等）

### 默认行为

```javascript
import { pipeline } from '@huggingface/transformers';

// First load: downloads model
const pipe = await pipeline('sentiment-analysis');

// Subsequent loads: uses cached model
const pipe2 = await pipeline('sentiment-analysis'); // Fast!
```

缓存是**自动的**，默认启用。模型在首次下载后即被缓存。

## 浏览器缓存

### 使用 Cache API

在浏览器环境中，Transformers.js 使用 [Cache API](https://developer.mozilla.org/en-US/docs/Web/API/Cache) 存储模型：

```javascript
import { env, pipeline } from '@huggingface/transformers';

// Browser cache is enabled by default
console.log(env.useBrowserCache); // true

// Load model (cached automatically)
const classifier = await pipeline('sentiment-analysis');
```

**工作原理：**

1. 从 Hugging Face Hub 下载模型文件
2. 文件存储在浏览器的 Cache Storage 中
3. 后续加载从缓存读取（无网络请求）
4. 缓存在页面刷新和浏览器会话间持久化

### 缓存位置

浏览器缓存存储在：
- **Chrome/Edge**：DevTools → Application 标签 → Cache Storage
- **Firefox**：`about:cache` → Storage
- **Safari**：Web Inspector → Storage 标签

### 禁用浏览器缓存

```javascript
import { env } from '@huggingface/transformers';

// Disable browser caching (not recommended)
env.useBrowserCache = false;

// Models will be re-downloaded on every page load
```

**适用场景：** 测试、开发或调试缓存问题。

### 浏览器存储限制

浏览器有存储配额限制：

- **Chrome**：可用磁盘空间的约 60%（但可能回收数据）
- **Firefox**：可用磁盘空间的约 50%
- **Safari**：每个源约 1GB（超出时会提示）

**提示：** 使用 [Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API) 监控存储用量：

```javascript
if ('storage' in navigator && 'estimate' in navigator.storage) {
  const estimate = await navigator.storage.estimate();
  const percentUsed = (estimate.usage / estimate.quota) * 100;
  console.log(`Storage: ${percentUsed.toFixed(2)}% used`);
  console.log(`Available: ${((estimate.quota - estimate.usage) / 1024 / 1024).toFixed(2)} MB`);
}
```

## Node.js 缓存

### 文件系统缓存

在 Node.js 中，模型缓存到文件系统：

```javascript
import { env, pipeline } from '@huggingface/transformers';

// Default cache directory (Node.js)
console.log(env.cacheDir); // './.cache' (relative to current directory)

// Filesystem cache is enabled by default
console.log(env.useFSCache); // true

// Load model (cached to disk)
const classifier = await pipeline('sentiment-analysis');
```

### 默认缓存位置

**默认行为：**
- 缓存目录：`./.cache`（相对于 Node.js 进程运行目录）
- 使用 Hugging Face 工具时的完整默认路径：`~/.cache/huggingface/`

**注意：** 性能优化中提到的"模型自动缓存到 `~/.cache/huggingface/`"是 Hugging Face Python 工具的惯例。在 Transformers.js 的 Node.js 版本中，默认路径为 `./.cache`，除非另行配置。

### 自定义缓存目录

```javascript
import { env, pipeline } from '@huggingface/transformers';

// Set custom cache directory
env.cacheDir = '/var/cache/transformers';

// Or use environment variable (Node.js convention)
env.cacheDir = process.env.HF_HOME || '~/.cache/huggingface';

// Now load model
const classifier = await pipeline('sentiment-analysis');
// Cached to: /var/cache/transformers/models--Xenova--distilbert-base-uncased-finetuned-sst-2-english/
```

**路径模式：** `models--{organization}--{model-name}/`

### 禁用文件系统缓存

```javascript
import { env } from '@huggingface/transformers';

// Disable filesystem caching (not recommended)
env.useFSCache = false;

// Models will be re-downloaded on every load
```

**适用场景：** 测试、CI/CD 环境或使用临时存储的容器。

## 自定义缓存实现

为特定存储后端实现自定义缓存。

### 自定义缓存接口

```typescript
interface CacheInterface {
  /**
   * Check if a URL is cached
   */
  match(url: string): Promise<Response | undefined>;
  
  /**
   * Store a URL and its response
   */
  put(url: string, response: Response): Promise<void>;
}
```

### 示例：云存储缓存（S3）

```javascript
import { env, pipeline } from '@huggingface/transformers';
import { S3Client, GetObjectCommand, PutObjectCommand } from '@aws-sdk/client-s3';
import { Readable } from 'stream';

class S3Cache {
  constructor(bucket, region = 'us-east-1') {
    this.bucket = bucket;
    this.s3 = new S3Client({ region });
  }

  async match(url) {
    const key = this.urlToKey(url);
    
    try {
      const command = new GetObjectCommand({
        Bucket: this.bucket,
        Key: key
      });
      const response = await this.s3.send(command);
      
      // Convert stream to buffer
      const chunks = [];
      for await (const chunk of response.Body) {
        chunks.push(chunk);
      }
      const body = Buffer.concat(chunks);
      
      return new Response(body, {
        status: 200,
        headers: JSON.parse(response.Metadata.headers || '{}')
      });
    } catch (error) {
      if (error.name === 'NoSuchKey') return undefined;
      throw error;
    }
  }

  async put(url, response) {
    const key = this.urlToKey(url);
    const clonedResponse = response.clone();
    const body = Buffer.from(await clonedResponse.arrayBuffer());
    const headers = JSON.stringify(Object.fromEntries(response.headers.entries()));

    const command = new PutObjectCommand({
      Bucket: this.bucket,
      Key: key,
      Body: body,
      Metadata: { headers }
    });
    
    await this.s3.send(command);
  }

  urlToKey(url) {
    // Convert URL to S3 key (remove protocol, replace slashes)
    return url.replace(/^https?:\/\//, '').replace(/\//g, '_');
  }
}

// Configure S3 cache
env.useCustomCache = true;
env.customCache = new S3Cache('my-transformers-cache', 'us-east-1');
env.useFSCache = false;

// Use S3 cache
const classifier = await pipeline('sentiment-analysis');
```

## 缓存配置

### 环境变量

使用环境变量配置缓存：

```javascript
import { env } from '@huggingface/transformers';

// Configure cache directory from environment
env.cacheDir = process.env.TRANSFORMERS_CACHE || './.cache';

// Disable caching in CI/CD
if (process.env.CI === 'true') {
  env.useFSCache = false;
  env.useBrowserCache = false;
}

// Production: use pre-cached models
if (process.env.NODE_ENV === 'production') {
  env.allowRemoteModels = false;
  env.allowLocalModels = true;
  env.localModelPath = process.env.MODEL_PATH || '/app/models';
}
```

### 配置模式

#### 开发环境：启用全部缓存

```javascript
import { env } from '@huggingface/transformers';

env.allowRemoteModels = true;
env.useFSCache = true;         // Node.js
env.useBrowserCache = true;    // Browser
env.cacheDir = './.cache';
```

#### 生产环境：仅本地模型

```javascript
import { env } from '@huggingface/transformers';

env.allowRemoteModels = false;
env.allowLocalModels = true;
env.localModelPath = '/app/models';
env.useFSCache = true;
```

#### 测试环境：禁用缓存

```javascript
import { env } from '@huggingface/transformers';

env.useFSCache = false;
env.useBrowserCache = false;
env.allowRemoteModels = true; // Download every time
```

#### 混合模式：缓存 + 远程回退

```javascript
import { env } from '@huggingface/transformers';

// Try local cache first, fall back to remote
env.allowRemoteModels = true;
env.allowLocalModels = true;
env.useFSCache = true;
env.localModelPath = './models';
```

---

## 总结

Transformers.js 提供灵活的缓存选项：

- **浏览器**：Cache API（自动，持久化）
- **Node.js**：文件系统缓存（默认 `./.cache`，可配置）
- **自定义**：自行实现（数据库、云存储等）

**关键要点：**

1. 缓存默认启用且自动运行
2. 加载模型**之前**配置缓存
3. 浏览器使用 Cache API，Node.js 使用文件系统
4. 自定义缓存支持高级存储后端
5. 监控缓存大小并制定清理策略
6. 生产部署时预下载模型

更多配置选项参见：
- [配置参考](./CONFIGURATION.md)
- [Pipeline 选项](./PIPELINE_OPTIONS.md)
