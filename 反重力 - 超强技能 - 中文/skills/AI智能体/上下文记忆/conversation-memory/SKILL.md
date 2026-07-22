---
name: conversation-memory
description: LLM 对话的持久化记忆系统，包括短期记忆、长期记忆和基于实体的记忆
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 对话记忆

LLM 对话的持久化记忆系统，包括短期记忆、长期记忆和基于实体的记忆

## 能力

- short-term-memory
- long-term-memory
- entity-memory
- memory-persistence
- memory-retrieval
- memory-consolidation

## 前置条件

- Knowledge: LLM 对话模式、数据库基础、键值存储
- Skills_recommended: context-window-management, rag-implementation

## 范围

- Does_not_cover: 知识图谱构建、语义搜索实现、数据库管理
- Boundaries: 聚焦于 LLM 的记忆模式，涵盖存储和检索策略

## 生态系统

### Primary_tools

- Mem0 - AI 应用的记忆层
- LangChain Memory - LangChain 中的记忆工具
- Redis - 用于会话记忆的内存数据存储

## 模式

### 分层记忆系统

不同用途的不同记忆层级

**何时使用**: 构建任何对话式 AI

interface MemorySystem {
    // Buffer: 当前对话（在上下文中）
    buffer: ConversationBuffer;

    // Short-term: 近期交互（会话级）
    shortTerm: ShortTermMemory;

    // Long-term: 跨会话持久化
    longTerm: LongTermMemory;

    // Entity: 关于人物、地点、事物的事实
    entity: EntityMemory;
}

class TieredMemory implements MemorySystem {
    async addMessage(message: Message): Promise<void> {
        // 始终添加到缓冲区
        this.buffer.add(message);

        // 提取实体
        const entities = await extractEntities(message);
        for (const entity of entities) {
            await this.entity.upsert(entity);
        }

        // 检查是否值得记忆
        if (await isMemoryWorthy(message)) {
            await this.shortTerm.add({
                content: message.content,
                timestamp: Date.now(),
                importance: await scoreImportance(message)
            });
        }
    }

    async consolidate(): Promise<void> {
        // 将重要的短期记忆移至长期记忆
        const memories = await this.shortTerm.getOld(24 * 60 * 60 * 1000);
        for (const memory of memories) {
            if (memory.importance > 0.7 || memory.referenced > 2) {
                await this.longTerm.add(memory);
            }
            await this.shortTerm.remove(memory.id);
        }
    }

    async buildContext(query: string): Promise<string> {
        const parts: string[] = [];

        // 相关的长期记忆
        const longTermRelevant = await this.longTerm.search(query, 3);
        if (longTermRelevant.length) {
            parts.push('## 相关记忆\n' +
                longTermRelevant.map(m => `- ${m.content}`).join('\n'));
        }

        // 相关实体
        const entities = await this.entity.getRelevant(query);
        if (entities.length) {
            parts.push('## 已知实体\n' +
                entities.map(e => `- ${e.name}: ${e.facts.join(', ')}`).join('\n'));
        }

        // 近期对话
        const recent = this.buffer.getRecent(10);
        parts.push('## 近期对话\n' + formatMessages(recent));

        return parts.join('\n\n');
    }
}

### 实体记忆

存储和更新关于实体的事实

**何时使用**: 需要记住关于人物、地点、事物的详细信息

interface Entity {
    id: string;
    name: string;
    type: 'person' | 'place' | 'thing' | 'concept';
    facts: Fact[];
    lastMentioned: number;
    mentionCount: number;
}

interface Fact {
    content: string;
    confidence: number;
    source: string;  // 来源消息 ID
    timestamp: number;
}

class EntityMemory {
    async extractAndStore(message: Message): Promise<void> {
        // 使用 LLM 提取实体和事实
        const extraction = await llm.complete(`
            从此消息中提取实体和事实。
            返回 JSON: { "entities": [
                { "name": "...", "type": "...", "facts": ["..."] }
            ]}

            消息: "${message.content}"
        `);

        const { entities } = JSON.parse(extraction);
        for (const entity of entities) {
            await this.upsert(entity, message.id);
        }
    }

    async upsert(entity: ExtractedEntity, sourceId: string): Promise<void> {
        const existing = await this.store.get(entity.name.toLowerCase());

        if (existing) {
            // 合并事实，避免重复
            for (const fact of entity.facts) {
                if (!this.hasSimilarFact(existing.facts, fact)) {
                    existing.facts.push({
                        content: fact,
                        confidence: 0.9,
                        source: sourceId,
                        timestamp: Date.now()
                    });
                }
            }
            existing.lastMentioned = Date.now();
            existing.mentionCount++;
            await this.store.set(existing.id, existing);
        } else {
            // 创建新实体
            await this.store.set(entity.name.toLowerCase(), {
                id: generateId(),
                name: entity.name,
                type: entity.type,
                facts: entity.facts.map(f => ({
                    content: f,
                    confidence: 0.9,
                    source: sourceId,
                    timestamp: Date.now()
                })),
                lastMentioned: Date.now(),
                mentionCount: 1
            });
        }
    }
}

### 记忆感知提示

在提示中包含相关记忆

**何时使用**: 在带有记忆上下文的情况下调用 LLM

async function promptWithMemory(
    query: string,
    memory: MemorySystem,
    systemPrompt: string
): Promise<string> {
    // 检索相关记忆
    const relevantMemories = await memory.longTerm.search(query, 5);
    const entities = await memory.entity.getRelevant(query);
    const recentContext = memory.buffer.getRecent(5);

    // 构建记忆增强提示
    const prompt = `
${systemPrompt}

## 用户上下文
${entities.length ? `关于用户的已知信息:\n${entities.map(e =>
    `- ${e.name}: ${e.facts.map(f => f.content).join('; ')}`
).join('\n')}` : ''}

${relevantMemories.length ? `相关的过往交互:\n${relevantMemories.map(m =>
    `- [${formatDate(m.timestamp)}] ${m.content}`
).join('\n')}` : ''}

## 近期对话
${formatMessages(recentContext)}

## 当前查询
${query}
    `.trim();

    const response = await llm.complete(prompt);

    // 从响应中提取新记忆
    await memory.addMessage({ role: 'assistant', content: response });

    return response;
}

## 陷阱

### 记忆存储无限增长，系统变慢

严重程度: 高

场景: 系统随时间变慢，成本增加

症状:
- 记忆检索缓慢
- 存储成本高
- 延迟随时间增加

原因:
每条消息都存储为记忆。
没有清理或整合机制。
在数百万条记录上检索。

推荐修复:

// 实现记忆生命周期管理

class ManagedMemory {
    // 限制
    private readonly SHORT_TERM_MAX = 100;
    private readonly LONG_TERM_MAX = 10000;
    private readonly CONSOLIDATION_INTERVAL = 24 * 60 * 60 * 1000;

    async add(memory: Memory): Promise<void> {
        // 存储前评估重要性
        const score = await this.scoreImportance(memory);
        if (score < 0.3) return;  // 不存储低重要性内容

        memory.importance = score;
        await this.shortTerm.add(memory);

        // 检查限制
        await this.enforceShortTermLimit();
    }

    async enforceShortTermLimit(): Promise<void> {
        const count = await this.shortTerm.count();
        if (count > this.SHORT_TERM_MAX) {
            // 整合: 将重要的移至长期记忆，删除其余
            const memories = await this.shortTerm.getAll();
            memories.sort((a, b) => b.importance - a.importance);

            const toKeep = memories.slice(0, this.SHORT_TERM_MAX * 0.7);
            const toConsolidate = memories.slice(this.SHORT_TERM_MAX * 0.7);

            for (const m of toConsolidate) {
                if (m.importance > 0.7) {
                    await this.longTerm.add(m);
                }
                await this.shortTerm.remove(m.id);
            }
        }
    }

    async scoreImportance(memory: Memory): Promise<number> {
        const factors = {
            hasUserPreference: /prefer|like|don't like|hate|love/i.test(memory.content) ? 0.3 : 0,
            hasDecision: /decided|chose|will do|won't do/i.test(memory.content) ? 0.3 : 0,
            hasFactAboutUser: /my|I am|I have|I work/i.test(memory.content) ? 0.2 : 0,
            length: memory.content.length > 100 ? 0.1 : 0,
            userMessage: memory.role === 'user' ? 0.1 : 0,
        };

        return Object.values(factors).reduce((a, b) => a + b, 0);
    }
}

### 检索到的记忆与当前查询不相关

严重程度: 高

场景: 记忆被包含在上下文中但没有帮助

症状:
- 上下文中的记忆看起来随机
- 用户询问已在记忆中的内容
- 不相关上下文导致混乱

原因:
简单的关键词匹配。
没有相关性评分。
包含所有检索到的记忆。

推荐修复:

// 智能记忆检索

async function retrieveRelevant(
    query: string,
    memories: MemoryStore,
    maxResults: number = 5
): Promise<Memory[]> {
    // 1. 语义搜索
    const candidates = await memories.semanticSearch(query, maxResults * 3);

    // 2. 结合上下文评估相关性
    const scored = await Promise.all(candidates.map(async (m) => {
        const relevanceScore = await llm.complete(`
            用 0-1 评分此记忆与查询的相关性。
            查询: "${query}"
            记忆: "${m.content}"
            只返回数字。
        `);
        return { ...m, relevance: parseFloat(relevanceScore) };
    }));

    // 3. 过滤低相关性
    const relevant = scored.filter(m => m.relevance > 0.5);

    // 4. 排序并限制
    return relevant
        .sort((a, b) => b.relevance - a.relevance)
        .slice(0, maxResults);
}

### 一个用户的记忆可被另一个用户访问

严重程度: 严重

场景: 用户看到来自另一个用户会话的信息

症状:
- 用户看到其他用户的信息
- 隐私投诉
- 合规违规

原因:
记忆存储中没有用户隔离。
共享记忆命名空间。
跨用户检索。

推荐修复:

// 严格的用户记忆隔离

class IsolatedMemory {
    private getKey(userId: string, memoryId: string): string {
        // 按用户命名空间化所有键
        return `user:${userId}:memory:${memoryId}`;
    }

    async add(userId: string, memory: Memory): Promise<void> {
        // 验证 userId 已认证
        if (!isValidUserId(userId)) {
            throw new Error('Invalid user ID');
        }

        const key = this.getKey(userId, memory.id);
        memory.userId = userId;  // 标记用户
        await this.store.set(key, memory);
    }

    async search(userId: string, query: string): Promise<Memory[]> {
        // 关键: 在查询中按用户过滤
        return await this.store.search({
            query,
            filter: { userId: userId },  // 强制过滤
            limit: 10
        });
    }

    async delete(userId: string, memoryId: string): Promise<void> {
        const memory = await this.get(userId, memoryId);
        // 删除前验证所有权
        if (memory.userId !== userId) {
            throw new Error('Access denied');
        }
        await this.store.delete(this.getKey(userId, memoryId));
    }

    // 用户数据导出 (GDPR 合规)
    async exportUserData(userId: string): Promise<Memory[]> {
        return await this.store.getAll({ userId });
    }

    // 用户数据删除 (GDPR 合规)
    async deleteUserData(userId: string): Promise<void> {
        const memories = await this.exportUserData(userId);
        for (const m of memories) {
            await this.store.delete(this.getKey(userId, m.id));
        }
    }
}

## 验证检查

### 记忆中没有用户隔离

严重程度: 严重

消息: 记忆操作没有用户隔离。隐私漏洞。

修复操作: 在所有记忆操作中添加 userId，检索时按用户过滤

### 没有重要性过滤

严重程度: 警告

消息: 存储记忆时没有重要性过滤。可能导致记忆爆炸。

修复操作: 存储前评估重要性，过滤低重要性内容

### 只有存储没有检索

严重程度: 警告

消息: 存储记忆但没有检索逻辑。记忆不会被使用。

修复操作: 实现记忆检索并包含在提示中

### 没有记忆清理

严重程度: 信息

消息: 没有记忆清理机制。存储将无限增长。

修复操作: 基于时间/重要性实现整合和清理

## 协作

### 委托触发

- context window|token -> context-window-management (需要上下文优化)
- rag|retrieval|vector -> rag-implementation (需要检索系统)
- cache|caching -> prompt-caching (需要缓存策略)

### 完整记忆系统

技能: conversation-memory, context-window-management, rag-implementation

工作流:

```
1. 设计记忆层级
2. 实现存储和检索
3. 与上下文管理集成
4. 添加整合和清理
```

## 相关技能

配合使用: `context-window-management`, `rag-implementation`, `prompt-caching`, `llm-npc-dialogue`

## 何时使用
- User mentions or implies: conversation memory
- User mentions or implies: remember
- User mentions or implies: memory persistence
- User mentions or implies: long-term memory
- User mentions or implies: chat history

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
