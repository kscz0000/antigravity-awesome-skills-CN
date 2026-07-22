---
name: context-window-management
description: 管理 LLM 上下文窗口的策略，包括摘要、裁剪、路由和避免上下文腐化
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 上下文窗口管理

管理 LLM 上下文窗口的策略，包括摘要、裁剪、路由和避免上下文腐化

## 能力

- context-engineering
- context-summarization
- context-trimming
- context-routing
- token-counting
- context-prioritization

## 前置条件

- Knowledge: LLM 基础知识, Tokenization 基础, 提示词工程
- Skills_recommended: prompt-engineering

## 范围

- Does_not_cover: RAG 实现细节, 模型微调, 嵌入模型
- Boundaries: 聚焦于上下文优化, 涵盖策略而非具体实现

## 生态系统

### 主要工具

- tiktoken - OpenAI 的分词器，用于计算 token 数量
- LangChain - 框架，提供上下文管理工具
- Claude API - 200K+ 上下文，支持缓存

## 模式

### 分层上下文策略

基于上下文大小的不同策略

**适用场景**: 构建任何多轮对话系统

interface ContextTier {
    maxTokens: number;
    strategy: 'full' | 'summarize' | 'rag';
    model: string;
}

const TIERS: ContextTier[] = [
    { maxTokens: 8000, strategy: 'full', model: 'claude-3-haiku' },
    { maxTokens: 32000, strategy: 'full', model: 'claude-3-5-sonnet' },
    { maxTokens: 100000, strategy: 'summarize', model: 'claude-3-5-sonnet' },
    { maxTokens: Infinity, strategy: 'rag', model: 'claude-3-5-sonnet' }
];

async function selectStrategy(messages: Message[]): ContextTier {
    const tokens = await countTokens(messages);

    for (const tier of TIERS) {
        if (tokens <= tier.maxTokens) {
            return tier;
        }
    }
    return TIERS[TIERS.length - 1];
}

async function prepareContext(messages: Message[]): PreparedContext {
    const tier = await selectStrategy(messages);

    switch (tier.strategy) {
        case 'full':
            return { messages, model: tier.model };

        case 'summarize':
            const summary = await summarizeOldMessages(messages);
            return { messages: [summary, ...recentMessages(messages)], model: tier.model };

        case 'rag':
            const relevant = await retrieveRelevant(messages);
            return { messages: [...relevant, ...recentMessages(messages)], model: tier.model };
    }
}

### 序列位置优化

将重要内容放在开头和结尾

**适用场景**: 构建包含大量上下文的提示词

// LLM 对开头和结尾的内容赋予更高权重
// 利用这一特性构建提示词结构

function buildOptimalPrompt(components: {
    systemPrompt: string;
    criticalContext: string;
    conversationHistory: Message[];
    currentQuery: string;
}): string {
    // 开头: 系统指令（始终放在最前面）
    const parts = [components.systemPrompt];

    // 关键上下文: 紧随系统指令之后（高优先级）
    if (components.criticalContext) {
        parts.push(`## 关键上下文\n${components.criticalContext}`);
    }

    // 中间: 对话历史（权重较低）
    // 如果很长则摘要，保留最近消息的完整内容
    const history = components.conversationHistory;
    if (history.length > 10) {
        const oldSummary = summarize(history.slice(0, -5));
        const recent = history.slice(-5);
        parts.push(`## 早期对话（摘要）\n${oldSummary}`);
        parts.push(`## 最近消息\n${formatMessages(recent)}`);
    } else {
        parts.push(`## 对话\n${formatMessages(history)}`);
    }

    // 结尾: 当前查询（高时效性）
    // 在此重申关键要求
    parts.push(`## 当前请求\n${components.currentQuery}`);

    // 最后: 关键约束提醒
    parts.push(`注意: ${extractKeyConstraints(components.systemPrompt)}`);

    return parts.join('\n\n');
}

### 智能摘要

按重要性摘要，而非仅按时间顺序

**适用场景**: 上下文超出最优大小

interface MessageWithMetadata extends Message {
    importance: number;  // 0-1 重要性评分
    hasCriticalInfo: boolean;  // 用户偏好、决策
    referenced: boolean;  // 是否被后续引用
}

async function smartSummarize(
    messages: MessageWithMetadata[],
    targetTokens: number
): Message[] {
    // 按重要性排序，相同分数保持原顺序
    const sorted = [...messages].sort((a, b) =>
        (b.importance + (b.hasCriticalInfo ? 0.5 : 0) + (b.referenced ? 0.3 : 0)) -
        (a.importance + (a.hasCriticalInfo ? 0.5 : 0) + (a.referenced ? 0.3 : 0))
    );

    const keep: Message[] = [];
    const summarizePool: Message[] = [];
    let currentTokens = 0;

    for (const msg of sorted) {
        const msgTokens = await countTokens([msg]);
        if (currentTokens + msgTokens < targetTokens * 0.7) {
            keep.push(msg);
            currentTokens += msgTokens;
        } else {
            summarizePool.push(msg);
        }
    }

    // 摘要低重要性消息
    if (summarizePool.length > 0) {
        const summary = await llm.complete(`
            摘要以下消息，保留：
            - 任何用户偏好或决策
            - 可能被后续引用的关键事实
            - 对话的整体流程

            消息：
            ${formatMessages(summarizePool)}
        `);

        keep.unshift({ role: 'system', content: `[早期上下文: ${summary}]` });
    }

    // 恢复原始顺序
    return keep.sort((a, b) => a.timestamp - b.timestamp);
}

### Token 预算分配

在上下文组件间分配 token 预算

**适用场景**: 需要可预测的上下文管理

interface TokenBudget {
    system: number;      // 系统提示词
    criticalContext: number;  // 用户偏好、关键信息
    history: number;     // 对话历史
    query: number;       // 当前查询
    response: number;    // 预留给响应
}

function allocateBudget(totalTokens: number): TokenBudget {
    return {
        system: Math.floor(totalTokens * 0.10),      // 10%
        criticalContext: Math.floor(totalTokens * 0.15),  // 15%
        history: Math.floor(totalTokens * 0.40),     // 40%
        query: Math.floor(totalTokens * 0.10),       // 10%
        response: Math.floor(totalTokens * 0.25),    // 25%
    };
}

async function buildWithBudget(
    components: ContextComponents,
    modelMaxTokens: number
): PreparedContext {
    const budget = allocateBudget(modelMaxTokens);

    // 裁剪/摘要各组件以适应预算
    const prepared = {
        system: truncateToTokens(components.system, budget.system),
        criticalContext: truncateToTokens(
            components.criticalContext, budget.criticalContext
        ),
        history: await summarizeToTokens(components.history, budget.history),
        query: truncateToTokens(components.query, budget.query),
    };

    // 重新分配未使用的预算
    const used = await countTokens(Object.values(prepared).join('\n'));
    const remaining = modelMaxTokens - used - budget.response;

    if (remaining > 0) {
        // 将额外预算分配给历史（对话中最有价值的部分）
        prepared.history = await summarizeToTokens(
            components.history,
            budget.history + remaining
        );
    }

    return prepared;
}

## 验证检查

### 未计算 Token 数量

严重程度: WARNING

消息: 构建上下文时未计算 token 数量。可能超出模型限制。

修复操作: 发送前计算 token，实现预算分配

### 朴素消息截断

严重程度: WARNING

消息: 截断消息而未摘要。关键上下文可能丢失。

修复操作: 摘要旧消息而非简单删除

### 硬编码 Token 限制

严重程度: INFO

消息: 硬编码 token 限制。建议按模型配置。

修复操作: 使用配置中的模型特定限制

### 无上下文管理策略

严重程度: WARNING

消息: LLM 调用缺少上下文管理策略。

修复操作: 实现上下文管理：预算、摘要或 RAG

## 协作

### 委托触发

- retrieval|rag|search -> rag-implementation (需要检索系统)
- memory|persistence|remember -> conversation-memory (需要记忆存储)
- cache|caching -> prompt-caching (需要缓存优化)

### 完整上下文系统

技能: context-window-management, rag-implementation, conversation-memory, prompt-caching

工作流:

```
1. 设计上下文策略
2. 为大型语料库实现 RAG
3. 设置记忆持久化
4. 添加缓存以提升性能
```

## 相关技能

配合使用: `rag-implementation`, `conversation-memory`, `prompt-caching`, `llm-npc-dialogue`

## 使用时机
- User mentions or implies: context window
- User mentions or implies: token limit
- User mentions or implies: context management
- User mentions or implies: context engineering
- User mentions or implies: long context
- User mentions or implies: context overflow

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不应替代环境特定的验证、测试或专家评审。
- 若缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清。
