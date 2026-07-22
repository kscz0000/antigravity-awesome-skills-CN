---
name: prompt-caching
description: LLM 提示词缓存策略，涵盖 Anthropic prompt caching、响应缓存和 CAG（Cache Augmented Generation）。触发词：prompt caching、缓存提示词、response cache、cag、cache augmented
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Prompt Caching

LLM 提示词缓存策略，涵盖 Anthropic prompt caching、响应缓存和 CAG（Cache Augmented Generation）

## 能力

- prompt-cache
- response-cache
- kv-cache
- cag-patterns
- cache-invalidation

## 前置要求

- 知识：缓存基础、LLM API 使用、哈希函数
- 推荐技能：context-window-management

## 范围

- 不涵盖：CDN 缓存、数据库查询缓存、静态资源缓存
- 边界：聚焦 LLM 专用缓存，覆盖提示词缓存和响应缓存

## 生态系统

### 核心工具

- Anthropic Prompt Caching — Claude API 原生提示词缓存
- Redis — 内存级响应缓存
- OpenAI Caching — OpenAI API 自动缓存

## 模式

### Anthropic Prompt Caching

利用 Claude 原生提示词缓存处理重复前缀

**适用场景**：使用 Claude API 且系统提示词或上下文保持稳定时

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

// Cache the stable parts of your prompt
async function queryWithCaching(userQuery: string) {
    const response = await client.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1024,
        system: [
            {
                type: "text",
                text: LONG_SYSTEM_PROMPT,  // Your detailed instructions
                cache_control: { type: "ephemeral" }  // Cache this!
            },
            {
                type: "text",
                text: KNOWLEDGE_BASE,  // Large static context
                cache_control: { type: "ephemeral" }
            }
        ],
        messages: [
            { role: "user", content: userQuery }  // Dynamic part
        ]
    });

    // Check cache usage
    console.log(`Cache read: ${response.usage.cache_read_input_tokens}`);
    console.log(`Cache write: ${response.usage.cache_creation_input_tokens}`);

    return response;
}

// Cost savings: 90% reduction on cached tokens
// Latency savings: Up to 2x faster

### 响应缓存

对相同或相似查询缓存完整的 LLM 响应

**适用场景**：同一查询被反复提问时

import { createHash } from 'crypto';
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

class ResponseCache {
    private ttl = 3600;  // 1 hour default

    // Exact match caching
    async getCached(prompt: string): Promise<string | null> {
        const key = this.hashPrompt(prompt);
        return await redis.get(`response:${key}`);
    }

    async setCached(prompt: string, response: string): Promise<void> {
        const key = this.hashPrompt(prompt);
        await redis.set(`response:${key}`, response, 'EX', this.ttl);
    }

    private hashPrompt(prompt: string): string {
        return createHash('sha256').update(prompt).digest('hex');
    }

    // Semantic similarity caching
    async getSemanticallySimilar(
        prompt: string,
        threshold: number = 0.95
    ): Promise<string | null> {
        const embedding = await embed(prompt);
        const similar = await this.vectorCache.search(embedding, 1);

        if (similar.length && similar[0].similarity > threshold) {
            return await redis.get(`response:${similar[0].id}`);
        }
        return null;
    }

    // Temperature-aware caching
    async getCachedWithParams(
        prompt: string,
        params: { temperature: number; model: string }
    ): Promise<string | null> {
        // Only cache low-temperature responses
        if (params.temperature > 0.5) return null;

        const key = this.hashPrompt(
            `${prompt}|${params.model}|${params.temperature}`
        );
        return await redis.get(`response:${key}`);
    }
}

### Cache Augmented Generation (CAG)

将文档预缓存到提示词中，替代 RAG 检索

**适用场景**：文档语料库稳定且能放入上下文窗口时

// CAG: Pre-compute document context, cache in prompt
// Better than RAG when:
// - Documents are stable
// - Total fits in context window
// - Latency is critical

class CAGSystem {
    private cachedContext: string | null = null;
    private lastUpdate: number = 0;

    async buildCachedContext(documents: Document[]): Promise<void> {
        // Pre-process and format documents
        const formatted = documents.map(d =>
            `## ${d.title}\n${d.content}`
        ).join('\n\n');

        // Store with timestamp
        this.cachedContext = formatted;
        this.lastUpdate = Date.now();
    }

    async query(userQuery: string): Promise<string> {
        // Use cached context directly in prompt
        const response = await client.messages.create({
            model: "claude-sonnet-4-20250514",
            max_tokens: 1024,
            system: [
                {
                    type: "text",
                    text: "You are a helpful assistant with access to the following documentation.",
                    cache_control: { type: "ephemeral" }
                },
                {
                    type: "text",
                    text: this.cachedContext!,  // Pre-cached docs
                    cache_control: { type: "ephemeral" }
                }
            ],
            messages: [{ role: "user", content: userQuery }]
        });

        return response.content[0].text;
    }

    // Periodic refresh
    async refreshIfNeeded(documents: Document[]): Promise<void> {
        const stale = Date.now() - this.lastUpdate > 3600000;  // 1 hour
        if (stale) {
            await this.buildCachedContext(documents);
        }
    }
}

// CAG vs RAG decision matrix:
// | Factor           | CAG Better | RAG Better |
// |------------------|------------|------------|
// | Corpus size      | < 100K tokens | > 100K tokens |
// | Update frequency | Low | High |
// | Latency needs    | Critical | Flexible |
// | Query specificity| General | Specific |

## 锋利边缘

### 缓存未命中导致延迟尖峰，且有额外开销

严重程度：HIGH

场景：缓存未命中时响应变慢，比不缓存还慢

症状：
- 缓存未命中时响应缓慢
- 缓存命中率低于 50%
- 延迟比不缓存时更高

为什么会出问题：
缓存检查增加延迟。
缓存写入增加更多延迟。
未命中 + 开销 > 不缓存。

推荐修复：

// Optimize for cache misses, not just hits

class OptimizedCache {
    async queryWithCache(prompt: string): Promise<string> {
        const cacheKey = this.hash(prompt);

        // Non-blocking cache check
        const cachedPromise = this.cache.get(cacheKey);
        const llmPromise = this.queryLLM(prompt);

        // Race: use cache if available before LLM returns
        const cached = await Promise.race([
            cachedPromise,
            sleep(50).then(() => null)  // 50ms cache timeout
        ]);

        if (cached) {
            // Cancel LLM request if possible
            return cached;
        }

        // Cache miss: continue with LLM
        const response = await llmPromise;

        // Async cache write (don't block response)
        this.cache.set(cacheKey, response).catch(console.error);

        return response;
    }
}

// Alternative: Probabilistic caching
// Only cache if query matches known high-frequency patterns
class SelectiveCache {
    private patterns: Map<string, number> = new Map();

    shouldCache(prompt: string): boolean {
        const pattern = this.extractPattern(prompt);
        const frequency = this.patterns.get(pattern) || 0;

        // Only cache high-frequency patterns
        return frequency > 10;
    }

    recordQuery(prompt: string): void {
        const pattern = this.extractPattern(prompt);
        this.patterns.set(pattern, (this.patterns.get(pattern) || 0) + 1);
    }
}

### 缓存响应随时间推移变得不正确

严重程度：HIGH

场景：用户从缓存中获取到过时或错误的信息

症状：
- 用户报告信息错误
- 回答与当前数据不符
- 用户投诉响应过时

为什么会出问题：
源数据已变更。
没有缓存失效机制。
动态数据使用了过长的 TTL。

推荐修复：

// Implement proper cache invalidation

class InvalidatingCache {
    // Version-based invalidation
    private cacheVersion = 1;

    getCacheKey(prompt: string): string {
        return `v${this.cacheVersion}:${this.hash(prompt)}`;
    }

    invalidateAll(): void {
        this.cacheVersion++;
        // Old keys automatically become orphaned
    }

    // Content-hash invalidation
    async setWithContentHash(
        key: string,
        response: string,
        sourceContent: string
    ): Promise<void> {
        const contentHash = this.hash(sourceContent);
        await this.cache.set(key, {
            response,
            contentHash,
            timestamp: Date.now()
        });
    }

    async getIfValid(
        key: string,
        currentSourceContent: string
    ): Promise<string | null> {
        const cached = await this.cache.get(key);
        if (!cached) return null;

        // Check if source content changed
        const currentHash = this.hash(currentSourceContent);
        if (cached.contentHash !== currentHash) {
            await this.cache.delete(key);
            return null;
        }

        return cached.response;
    }

    // Event-based invalidation
    onSourceUpdate(sourceId: string): void {
        // Invalidate all caches that used this source
        this.invalidateByTag(`source:${sourceId}`);
    }
}

### 因前缀变更导致提示词缓存失效

严重程度：MEDIUM

场景：提示词相似但缓存未命中

症状：
- 缓存命中率低于预期
- 缓存创建 token 数高，读取 token 数低
- 相似提示词未命中缓存

为什么会出问题：
Anthropic 缓存要求精确前缀匹配。
前缀中包含时间戳或动态内容。
消息顺序不同。

推荐修复：

// Structure prompts for optimal caching

class CacheOptimizedPrompts {
    // WRONG: Dynamic content in cached prefix
    buildPromptBad(query: string): SystemMessage[] {
        return [
            {
                type: "text",
                text: `You are helpful. Current time: ${new Date()}`,  // BREAKS CACHE!
                cache_control: { type: "ephemeral" }
            }
        ];
    }

    // RIGHT: Static prefix, dynamic at end
    buildPromptGood(query: string): SystemMessage[] {
        return [
            {
                type: "text",
                text: STATIC_SYSTEM_PROMPT,  // Never changes
                cache_control: { type: "ephemeral" }
            },
            {
                type: "text",
                text: STATIC_KNOWLEDGE_BASE,  // Rarely changes
                cache_control: { type: "ephemeral" }
            }
            // Dynamic content goes in messages, NOT system
        ];
    }

    // Prefix ordering matters
    buildWithConsistentOrder(components: string[]): SystemMessage[] {
        // Sort components for consistent ordering
        const sorted = [...components].sort();
        return sorted.map((c, i) => ({
            type: "text",
            text: c,
            cache_control: i === sorted.length - 1
                ? { type: "ephemeral" }
                : undefined  // Only cache the full prefix
        }));
    }
}

## 验证检查

### 缓存高温度响应

严重程度：WARNING

消息：正在缓存高温度响应，响应具有不确定性。

修复操作：仅缓存 temperature <= 0.5 的响应

### 缓存未设置 TTL

严重程度：WARNING

消息：缓存未设置 TTL，可能无限期提供过期数据。

修复操作：根据数据新鲜度要求设置合适的 TTL

### 缓存前缀中包含动态内容

严重程度：WARNING

消息：缓存前缀中包含动态内容，将导致缓存未命中。

修复操作：将动态内容移出 cache_control 块

### 缺少缓存指标

严重程度：INFO

消息：缓存未设置命中/未命中追踪，无法衡量效果。

修复操作：添加缓存命中/未命中的指标和日志

## 协作

### 委派触发条件

- context window|token -> context-window-management（需要上下文优化）
- rag|retrieval -> rag-implementation（需要检索系统）
- memory -> conversation-memory（需要记忆持久化）

### 高性能 LLM 系统

技能：prompt-caching、context-window-management、rag-implementation

工作流：

```
1. 分析查询模式
2. 为稳定前缀实现提示词缓存
3. 为高频查询添加响应缓存
4. 对稳定文档集考虑使用 CAG
5. 监控并优化命中率
```

## 相关技能

搭配使用效果好：`context-window-management`、`rag-implementation`、`conversation-memory`

## 适用场景
- 用户提到或暗示：prompt caching
- 用户提到或暗示：cache prompt
- 用户提到或暗示：response cache
- 用户提到或暗示：cag
- 用户提到或暗示：cache augmented

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
