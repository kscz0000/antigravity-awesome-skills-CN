# 文本生成指南

使用 Transformers.js 生成文本的指南，包括流式输出和对话格式。

## 目录

1. [基本生成](#基本生成)
2. [流式输出](#流式输出)
3. [对话格式](#对话格式)
4. [生成参数](#生成参数)
5. [模型选择](#模型选择)
6. [最佳实践](#最佳实践)

## 基本生成

```javascript
import { pipeline } from '@huggingface/transformers';

const generator = await pipeline(
  'text-generation',
  'onnx-community/Qwen2.5-0.5B-Instruct',
  { dtype: 'q4' }
);

const result = await generator('Once upon a time', {
  max_new_tokens: 100,
  temperature: 0.7,
});

console.log(result[0].generated_text);

// Clean up when done
await generator.dispose();
```

## 流式输出

在生成过程中逐 token 流式输出以改善用户体验。了解流式输出后，可将其与对话格式等功能组合使用。

### Node.js

```javascript
import { pipeline, TextStreamer } from '@huggingface/transformers';

const generator = await pipeline(
  'text-generation',
  'onnx-community/Qwen2.5-0.5B-Instruct',
  { dtype: 'q4' }
);

const streamer = new TextStreamer(generator.tokenizer, {
  skip_prompt: true,
  skip_special_tokens: true,
  callback_function: (token) => {
    process.stdout.write(token);
  },
});

await generator('Tell me a story', {
  max_new_tokens: 200,
  temperature: 0.7,
  streamer,
});
```

### 浏览器

```html
<!DOCTYPE html>
<html>
<body>
  <textarea id="prompt" placeholder="Enter prompt..."></textarea>
  <button onclick="generate()">Generate</button>
  <div id="output"></div>

  <script type="module">
    import { pipeline, TextStreamer } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1';
    
    const generator = await pipeline(
      'text-generation',
      'onnx-community/Qwen2.5-0.5B-Instruct',
      { dtype: 'q4' }
    );
    
    window.generate = async function() {
      const prompt = document.getElementById('prompt').value;
      const outputDiv = document.getElementById('output');
      outputDiv.textContent = '';
      
      const streamer = new TextStreamer(generator.tokenizer, {
        skip_prompt: true,
        skip_special_tokens: true,
        callback_function: (token) => {
          outputDiv.textContent += token;
        },
      });
      
      await generator(prompt, {
        max_new_tokens: 200,
        temperature: 0.7,
        streamer,
      });
    };
  </script>
</body>
</html>
```

### React

```jsx
import { useState, useRef, useEffect } from 'react';
import { pipeline, TextStreamer } from '@huggingface/transformers';

function StreamingGenerator() {
  const generatorRef = useRef(null);
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async (prompt) => {
    if (!prompt) return;
    
    setLoading(true);
    setOutput('');
    
    // Load model on first generate
    if (!generatorRef.current) {
      generatorRef.current = await pipeline(
        'text-generation',
        'onnx-community/Qwen2.5-0.5B-Instruct',
        { dtype: 'q4' }
      );
    }
    
    const streamer = new TextStreamer(generatorRef.current.tokenizer, {
      skip_prompt: true,
      skip_special_tokens: true,
      callback_function: (token) => {
        setOutput((prev) => prev + token);
      },
    });

    await generatorRef.current(prompt, {
      max_new_tokens: 200,
      temperature: 0.7,
      streamer,
    });
    
    setLoading(false);
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (generatorRef.current) {
        generatorRef.current.dispose();
      }
    };
  }, []);

  return (
    <div>
      <button onClick={() => handleGenerate('Tell me a story')} disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>
      <div>{output}</div>
    </div>
  );
}
```

## 对话格式

使用结构化消息进行对话。适用于基本生成和流式输出（只需添加 `streamer` 参数）。

### 单轮对话

```javascript
import { pipeline } from '@huggingface/transformers';

const generator = await pipeline(
  'text-generation',
  'onnx-community/Qwen2.5-0.5B-Instruct',
  { dtype: 'q4' }
);

const messages = [
  { role: 'system', content: 'You are a helpful assistant.' },
  { role: 'user', content: 'How do I create an async function?' }
];

const result = await generator(messages, {
  max_new_tokens: 256,
  temperature: 0.7,
});

console.log(result[0].generated_text);
```

### 多轮对话

```javascript
const conversation = [
  { role: 'system', content: 'You are a helpful assistant.' },
  { role: 'user', content: 'What is JavaScript?' },
  { role: 'assistant', content: 'JavaScript is a programming language...' },
  { role: 'user', content: 'Can you show an example?' }
];

const result = await generator(conversation, {
  max_new_tokens: 200,
  temperature: 0.7,
});

// To add streaming, just pass a streamer:
// streamer: new TextStreamer(generator.tokenizer, {...})
```

## 生成参数

### 常用参数

```javascript
await generator(prompt, {
  // Token limits
  max_new_tokens: 512,        // Maximum tokens to generate
  min_new_tokens: 0,          // Minimum tokens to generate
  
  // Sampling
  temperature: 0.7,           // Randomness (0.0-2.0)
  top_k: 50,                  // Consider top K tokens
  top_p: 0.95,                // Nucleus sampling
  do_sample: true,            // Use random sampling (false = always pick most likely token)
  
  // Repetition control
  repetition_penalty: 1.0,    // Penalty for repeating (1.0 = no penalty)
  no_repeat_ngram_size: 0,    // Prevent repeating n-grams
  
  // Streaming
  streamer: streamer,         // TextStreamer instance
});
```

### 参数效果

**Temperature：**
- 低（0.1-0.5）：更聚焦、更确定性
- 中（0.6-0.9）：创造力和连贯性平衡
- 高（1.0-2.0）：更有创造力、更随机

```javascript
// Focused output
await generator(prompt, { temperature: 0.3, max_new_tokens: 100 });

// Creative output
await generator(prompt, { temperature: 1.2, max_new_tokens: 100 });
```

**采样方法：**

```javascript
// Greedy (deterministic)
await generator(prompt, { 
  do_sample: false,
  max_new_tokens: 100 
});

// Top-k sampling
await generator(prompt, { 
  top_k: 50,
  temperature: 0.7,
  max_new_tokens: 100 
});

// Top-p (nucleus) sampling
await generator(prompt, { 
  top_p: 0.95,
  temperature: 0.7,
  max_new_tokens: 100 
});
```

## 模型选择

在 Hugging Face Hub 浏览可用的文本生成模型：

**https://huggingface.co/models?pipeline_tag=text-generation&library=transformers.js&sort=trending**

### 选择技巧

- **小模型（< 1B 参数）**：速度快，浏览器友好，使用 `dtype: 'q4'`
- **中型模型（1-3B 参数）**：质量/速度均衡，使用 `dtype: 'q4'` 或 `fp16`
- **大模型（> 3B 参数）**：高质量，速度慢，Node.js 最佳，使用 `dtype: 'fp16'`

查看模型卡片了解：
- 参数量和模型大小
- 支持的语言
- 基准测试分数
- 许可证限制

## 最佳实践

1. **模型大小**：浏览器用量化模型（`q4`），服务器用大模型（`fp16`）
2. **流式输出**：使用流式输出改善用户体验 — 显示进度且响应感更强
3. **Token 限制**：设置 `max_new_tokens` 防止无限生成
4. **Temperature**：根据场景调参（创意：0.8-1.2，事实：0.3-0.7）
5. **内存**：使用完毕始终调用 `dispose()`
6. **缓存**：加载一次模型，多次请求复用

## 相关文档

- [Pipeline 选项](./PIPELINE_OPTIONS.md) - 配置 pipeline 加载
- [配置参考](./CONFIGURATION.md) - 环境设置
- [代码示例](./EXAMPLES.md) - 不同运行时的更多示例
- [主技能指南](../SKILL.md) - 入门指南
