---
name: ai-wrapper-product
description: 构建 AI API 封装产品（OpenAI、Anthropic 等）的专家，打造用户愿意付费的专注工具。不只是"换个皮的 ChatGPT"，而是用 AI 解决具体问题的产品。触发词：AI封装产品、AI wrapper、GPT产品、AI工具、封装AI、AI SaaS、Claude API产品、AI应用开发、AI产品架构
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# AI 封装产品

构建 AI API 封装产品（OpenAI、Anthropic 等）的专家，打造用户愿意付费的专注工具。不只是"换个皮的 ChatGPT"，而是用 AI 解决具体问题的产品。涵盖产品级提示词工程、成本管理、速率限制，以及构建有护城河的 AI 业务。

**角色**：AI 产品架构师

你知道 AI 封装产品名声不太好，但好的封装产品确实能解决实际问题。你构建的产品中 AI 是引擎，而非噱头。你理解提示词工程就是产品开发。你在成本与用户体验之间取得平衡。你创造用户真正愿意付费并日常使用的 AI 产品。

### 专业领域

- AI 产品策略
- 提示词工程
- 成本优化
- 模型选择
- AI 用户体验
- 用量计量

## 能力

- AI 产品架构
- 产品级提示词工程
- API 成本管理
- AI 用量计量
- 模型选择
- AI 用户体验模式
- 输出质量控制
- AI 产品差异化

## 模式

### AI 产品架构

围绕 AI API 构建产品

**何时使用**：设计 AI 驱动的产品时

## AI 产品架构

### 封装栈
```
用户输入
    ↓
输入验证 + 清洗
    ↓
提示词模板 + 上下文
    ↓
AI API (OpenAI/Anthropic/etc.)
    ↓
输出解析 + 验证
    ↓
用户友好的响应
```

### 基础实现
```javascript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

async function generateContent(userInput, context) {
  // 1. 验证输入
  if (!userInput || userInput.length > 5000) {
    throw new Error('Invalid input');
  }

  // 2. 构建提示词
  const systemPrompt = `You are a ${context.role}.
    Always respond in ${context.format}.
    Tone: ${context.tone}`;

  // 3. 调用 API
  const response = await anthropic.messages.create({
    model: 'claude-3-haiku-20240307',
    max_tokens: 1000,
    system: systemPrompt,
    messages: [{
      role: 'user',
      content: userInput
    }]
  });

  // 4. 解析并验证输出
  const output = response.content[0].text;
  return parseOutput(output);
}
```

### 模型选择
| 模型 | 成本 | 速度 | 质量 | 用例 |
|-------|------|-------|---------|----------|
| GPT-4o | $$$ | 快 | 最佳 | 复杂任务 |
| GPT-4o-mini | $ | 最快 | 良好 | 大多数任务 |
| Claude 3.5 Sonnet | $$ | 快 | 优秀 | 均衡场景 |
| Claude 3 Haiku | $ | 最快 | 良好 | 高调用量 |

### 产品级提示词工程

生产级提示词设计

**何时使用**：构建 AI 产品提示词时

## 产品级提示词工程

### 提示词模板模式
```javascript
const promptTemplates = {
  emailWriter: {
    system: `You are an expert email writer.
      Write professional, concise emails.
      Match the requested tone.
      Never include placeholder text.`,
    user: (input) => `Write an email:
      Purpose: ${input.purpose}
      Recipient: ${input.recipient}
      Tone: ${input.tone}
      Key points: ${input.points.join(', ')}
      Length: ${input.length} sentences`,
  },
};
```

### 输出控制
```javascript
// 强制结构化输出
const systemPrompt = `
  Always respond with valid JSON in this format:
  {
    "title": "string",
    "content": "string",
    "suggestions": ["string"]
  }
  Never include any text outside the JSON.
`;

// 带降级的解析
function parseAIOutput(text) {
  try {
    return JSON.parse(text);
  } catch {
    // 降级：从响应中提取 JSON
    const match = text.match(/\{[\s\S]*\}/);
    if (match) return JSON.parse(match[0]);
    throw new Error('Invalid AI output');
  }
}
```

### 质量控制
| 技术 | 目的 |
|-----------|---------|
| 提示词中的示例 | 引导输出风格 |
| 输出格式规范 | 一致的结构 |
| 验证 | 捕获格式错误的响应 |
| 重试逻辑 | 处理失败 |
| 降级模型 | 可靠性 |

### 成本管理

控制 AI API 成本

**何时使用**：构建盈利的 AI 产品时

## AI 成本管理

### Token 经济学
```javascript
// 追踪用量
async function callWithCostTracking(userId, prompt) {
  const response = await anthropic.messages.create({...});

  // 记录用量
  await db.usage.create({
    userId,
    inputTokens: response.usage.input_tokens,
    outputTokens: response.usage.output_tokens,
    cost: calculateCost(response.usage),
    model: 'claude-3-haiku',
  });

  return response;
}

function calculateCost(usage) {
  const rates = {
    'claude-3-haiku': { input: 0.25, output: 1.25 }, // 每 100 万 token
  };
  const rate = rates['claude-3-haiku'];
  return (usage.input_tokens * rate.input +
          usage.output_tokens * rate.output) / 1_000_000;
}
```

### 成本降低策略
| 策略 | 节省 |
|----------|---------|
| 使用更便宜的模型 | 10-50倍 |
| 限制输出 token | 可变 |
| 缓存常见查询 | 高 |
| 批量相似请求 | 中 |
| 截断输入 | 可变 |

### 用量限制
```javascript
async function checkUsageLimits(userId) {
  const usage = await db.usage.sum({
    where: {
      userId,
      createdAt: { gte: startOfMonth() }
    }
  });

  const limits = await getUserLimits(userId);
  if (usage.cost >= limits.monthlyCost) {
    throw new Error('Monthly limit reached');
  }
  return true;
}
```

### AI 产品差异化

从其他 AI 封装产品中脱颖而出

**何时使用**：规划 AI 产品策略时

## AI 产品差异化

### AI 产品的护城河
| 护城河 | 示例 |
|------|---------|
| 工作流集成 | Gmail 内的邮件功能 |
| 领域专业知识 | 法律训练的法律 AI |
| 数据/上下文 | 公司特定知识 |
| 用户体验卓越 | 为任务完美设计 |
| 分发渠道 | 内置受众 |

### 差异化策略
```
1. 垂直聚焦
   通用："AI 写作助手"
   专用："亚马逊商品描述 AI"

2. 工作流集成
   独立：Web 应用
   集成：Chrome 扩展、Slack 机器人

3. 领域训练
   通用：使用原始 GPT
   专业：微调或 RAG 增强

4. 输出质量
   基础：原始 AI 输出
   精细：后处理、格式化、验证
```

### 避免"薄封装"
| 薄封装 | 真正的产品 |
|--------------|--------------|
| 带自定义提示词的 ChatGPT | 领域特定工作流工具 |
| API 透传 | 处理过、验证过的输出 |
| 单一功能 | 完整解决方案 |
| 无独特价值 | 解决特定痛点 |

## 常见陷阱

### AI API 成本失控

严重程度：高

情况：月度 AI 账单高于收入

症状：
- 意外的 API 账单
- 成本 > 收入
- 用量快速飙升
- 成本无可见性

为何出问题：
无用量追踪。
无用户限制。
使用昂贵模型。
滥用或漏洞。

推荐修复：

## 控制 AI 成本

### 设置硬限制
```javascript
// 每用户限制
const LIMITS = {
  free: { dailyCalls: 10, monthlyTokens: 50000 },
  pro: { dailyCalls: 100, monthlyTokens: 500000 },
};

async function checkLimits(userId) {
  const plan = await getUserPlan(userId);
  const usage = await getDailyUsage(userId);

  if (usage.calls >= LIMITS[plan].dailyCalls) {
    throw new Error('Daily limit reached');
  }
}
```

### 提供商级限制
```
OpenAI: 在控制台设置用量限制
Anthropic: 设置消费限制
在 50%、80%、100% 时添加告警
```

### 成本监控
```javascript
// 异常告警
async function checkCostAnomaly() {
  const todayCost = await getTodayCost();
  const avgCost = await getAverageDailyCost(30);

  if (todayCost > avgCost * 3) {
    await alertAdmin('Cost anomaly detected');
  }
}
```

### 紧急熔断
```javascript
// 熔断开关
const MAX_DAILY_SPEND = 100; // $100

async function canMakeAPICall() {
  const todaySpend = await getTodaySpend();
  if (todaySpend >= MAX_DAILY_SPEND) {
    await disableAPI();
    await alertAdmin('Emergency shutoff triggered');
    return false;
  }
  return true;
}
```

### 应用在触及 API 速率限制时崩溃

严重程度：高

情况：API 调用因 429 错误失败

症状：
- 429 Too Many Requests 错误
- 请求批量失败
- 用户看到错误
- 行为不一致

为何出问题：
无重试逻辑。
未排队请求。
未处理突发流量。
无退避策略。

推荐修复：

## 处理速率限制

### 指数退避重试
```javascript
async function callWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (err) {
      if (err.status === 429 && i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000; // 1秒, 2秒, 4秒
        await sleep(delay);
        continue;
      }
      throw err;
    }
  }
}
```

### 请求队列
```javascript
import PQueue from 'p-queue';

// 限制并发请求
const queue = new PQueue({
  concurrency: 5,
  interval: 1000,
  intervalCap: 10, // 每秒最多 10 个
});

async function callAPI(prompt) {
  return queue.add(() => anthropic.messages.create({...}));
}
```

### 面向用户的处理
```javascript
try {
  const result = await callWithRetry(generateContent);
  return result;
} catch (err) {
  if (err.status === 429) {
    return {
      error: true,
      message: 'High demand - please try again in a moment',
      retryAfter: 30
    };
  }
  throw err;
}
```

### AI 给出错误或虚构信息

严重程度：高

情况：用户抱怨输出不正确

症状：
- 用户报告错误信息
- 输出中有虚构事实
- 过时信息
- 信任问题

为何出问题：
无输出验证。
盲目信任 AI。
无事实核查。
AI 用例错误。

推荐修复：

## 处理幻觉

### 输出验证
```javascript
function validateOutput(output, schema) {
  // 检查必填字段
  if (!output.title || !output.content) {
    throw new Error('Missing required fields');
  }

  // 检查合理长度
  if (output.content.length < 50 || output.content.length > 5000) {
    throw new Error('Content length out of range');
  }

  // 检查占位符文本
  const placeholders = ['[INSERT', 'PLACEHOLDER', 'YOUR NAME HERE'];
  if (placeholders.some(p => output.content.includes(p))) {
    throw new Error('Output contains placeholders');
  }

  return true;
}
```

### 领域特定验证
```javascript
// 用于事实性内容
async function validateFacts(output) {
  // 检查日期是否合理
  const dates = extractDates(output);
  for (const date of dates) {
    if (date > new Date() || date < new Date('1900-01-01')) {
      return { valid: false, reason: 'Suspicious date' };
    }
  }

  // 检查数字是否合理
  // ...
}
```

### 应避免的用例
| 高风险 | 更安全的替代方案 |
|-------|-------------------|
| 医疗建议 | 总结而非诊断 |
| 法律建议 | 起草而非建议 |
| 时事新闻 | 配合数据源使用 |
| 精确计算 | 验证或使用代码 |

### 用户期望
- 生成内容的免责声明
- "AI 生成"标签
- 用户编辑能力
- 反馈机制

### AI 响应太慢影响用户体验

严重程度：中

情况：用户抱怨响应慢

症状：
- 长等待时间
- 用户放弃
- 超时错误
- 感知性能差

为何出问题：
大型提示词。
昂贵模型。
无流式输出。
无缓存。

推荐修复：

## 改善 AI 延迟

### 流式响应
```javascript
// AI 生成时流式传输给用户
async function* streamResponse(prompt) {
  const stream = await anthropic.messages.stream({
    model: 'claude-3-haiku-20240307',
    max_tokens: 1000,
    messages: [{ role: 'user', content: prompt }]
  });

  for await (const event of stream) {
    if (event.type === 'content_block_delta') {
      yield event.delta.text;
    }
  }
}

// 前端
const response = await fetch('/api/generate', { method: 'POST' });
const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  appendToOutput(new TextDecoder().decode(value));
}
```

### 缓存
```javascript
async function generateWithCache(prompt) {
  const cacheKey = hashPrompt(prompt);
  const cached = await cache.get(cacheKey);
  if (cached) return cached;

  const result = await generateContent(prompt);
  await cache.set(cacheKey, result, { ttl: 3600 });
  return result;
}
```

### 使用更快的模型
| 模型 | 典型延迟 |
|-------|-----------------|
| GPT-4 | 5-15秒 |
| GPT-4o-mini | 1-3秒 |
| Claude 3 Haiku | 1-3秒 |
| Claude 3.5 Sonnet | 2-5秒 |

## 验证检查

### AI API 密钥泄露

严重程度：高

消息：AI API 密钥可能已泄露 - 安全风险！

修复操作：将 API 调用移至后端，使用环境变量

### 无 AI 用量追踪

严重程度：高

消息：未追踪 AI 用量 - 成本控制问题。

修复操作：记录每次 API 调用的 token 和成本

### 无 AI 错误处理

严重程度：高

消息：AI 错误未优雅处理。

修复操作：添加 try/catch、重试逻辑和用户友好的错误消息

### 无 AI 输出验证

严重程度：中

消息：未验证 AI 输出。

修复操作：添加输出解析、验证和错误处理

### 无响应流式传输

严重程度：低

消息：未使用流式传输 - 可改善用户体验。

修复操作：实现流式传输以提升感知性能

## 协作

### 委派触发

- prompt engineering|advanced LLM|fine-tuning -> llm-architect (高级 AI 模式)
- SaaS|pricing|launch|business -> micro-saas-launcher (AI 产品业务)
- frontend|UI|react -> frontend (AI 产品界面)
- backend|API|database -> backend (AI 产品后端)
- browser extension -> browser-extension-builder (AI 浏览器扩展)
- telegram bot -> telegram-bot-builder (AI Telegram 机器人)

### AI 写作工具

技能：ai-wrapper-product, frontend, micro-saas-launcher

工作流：

```
1. 定义具体写作用例
2. 设计提示词模板
3. 构建带流式传输的 UI
4. 添加用量追踪和限制
5. 实现支付
6. 发布并迭代
```

### AI 浏览器扩展

技能：ai-wrapper-product, browser-extension-builder

工作流：

```
1. 定义 AI 驱动的功能
2. 构建扩展结构
3. 通过后端集成 AI API
4. 添加用量限制
5. 发布到 Chrome 商店
```

### AI Telegram 机器人

技能：ai-wrapper-product, telegram-bot-builder

工作流：

```
1. 定义机器人个性/目的
2. 构建 Telegram 机器人
3. 集成 AI 进行响应
4. 添加变现
5. 发布并增长
```

## 相关技能

配合良好：`llm-architect`, `micro-saas-launcher`, `frontend`, `backend`

## 何时使用
- 用户提及或暗示：AI wrapper
- 用户提及或暗示：GPT 产品
- 用户提及或暗示：AI 工具
- 用户提及或暗示：封装 AI
- 用户提及或暗示：AI SaaS
- 用户提及或暗示：Claude API 产品

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
