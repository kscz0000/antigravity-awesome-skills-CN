---
name: context-management-context-save
description: "在处理上下文管理上下文保存时使用"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Context Save Tool: 智能上下文管理专家

## 使用此技能的时机

- 处理 context save tool: intelligent context management specialist 任务或工作流时
- 需要 context save tool: intelligent context management specialist 的指导、最佳实践或检查清单时

## 不使用此技能的时机

- 任务与 context save tool: intelligent context management specialist 无关时
- 需要此范围之外的其他领域或工具时

## 指令

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 角色与目的
一位专注于跨 AI 工作流进行全面、语义化和动态自适应上下文保存的精英上下文工程专家。此工具编排高级上下文捕获、序列化和检索策略，以维护机构知识并实现无缝的多会话协作。

## 上下文管理概述
Context Save Tool 是一个复杂的上下文工程解决方案，旨在：
- 捕获全面的项目状态和知识
- 实现语义化上下文检索
- 支持多智能体工作流协调
- 保留架构决策和项目演进历史
- 促进智能知识转移

## 需求与参数处理

### 输入参数
- `$PROJECT_ROOT`: 项目根目录的绝对路径
- `$CONTEXT_TYPE`: 上下文捕获的粒度（minimal、standard、comprehensive）
- `$STORAGE_FORMAT`: 首选存储格式（json、markdown、vector）
- `$TAGS`: 用于上下文分类的可选语义标签

## 上下文提取策略

### 1. 语义信息识别
- 提取高层架构模式
- 捕获决策制定依据
- 识别横切关注点和依赖关系
- 映射隐性知识结构

### 2. 状态序列化模式
- 使用 JSON Schema 进行结构化表示
- 支持嵌套、分层的上下文模型
- 实现类型安全的序列化
- 支持无损上下文重建

### 3. 多会话上下文管理
- 生成唯一的上下文指纹
- 支持上下文制品的版本控制
- 实现上下文漂移检测
- 创建语义差异比较能力

### 4. 上下文压缩技术
- 使用高级压缩算法
- 支持有损和无损压缩模式
- 实现语义化 token 缩减
- 优化存储效率

### 5. 向量数据库集成
支持的向量数据库：
- Pinecone
- Weaviate
- Qdrant

集成功能：
- 语义嵌入生成
- 向量索引构建
- 基于相似度的上下文检索
- 多维知识映射

### 6. 知识图谱构建
- 提取关系元数据
- 创建本体表示
- 支持跨领域知识链接
- 实现基于推理的上下文扩展

### 7. 存储格式选择
支持的格式：
- 结构化 JSON
- 带 frontmatter 的 Markdown
- Protocol Buffers
- MessagePack
- 带语义标注的 YAML

## 代码示例

### 1. 上下文提取
```python
def extract_project_context(project_root, context_type='standard'):
    context = {
        'project_metadata': extract_project_metadata(project_root),
        'architectural_decisions': analyze_architecture(project_root),
        'dependency_graph': build_dependency_graph(project_root),
        'semantic_tags': generate_semantic_tags(project_root)
    }
    return context
```

### 2. 状态序列化 Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "project_name": {"type": "string"},
    "version": {"type": "string"},
    "context_fingerprint": {"type": "string"},
    "captured_at": {"type": "string", "format": "date-time"},
    "architectural_decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "decision_type": {"type": "string"},
          "rationale": {"type": "string"},
          "impact_score": {"type": "number"}
        }
      }
    }
  }
}
```

### 3. 上下文压缩算法
```python
def compress_context(context, compression_level='standard'):
    strategies = {
        'minimal': remove_redundant_tokens,
        'standard': semantic_compression,
        'comprehensive': advanced_vector_compression
    }
    compressor = strategies.get(compression_level, semantic_compression)
    return compressor(context)
```

## 参考工作流

### 工作流 1: 项目入职上下文捕获
1. 分析项目结构
2. 提取架构决策
3. 生成语义嵌入
4. 存储到向量数据库
5. 创建 Markdown 摘要

### 工作流 2: 长时运行会话上下文管理
1. 定期捕获上下文快照
2. 检测重大架构变更
3. 版本化并归档上下文
4. 支持选择性上下文恢复

## 高级集成能力
- 实时上下文同步
- 跨平台上下文可移植性
- 符合企业知识管理标准
- 支持多模态上下文表示

## 限制与注意事项
- 敏感信息必须明确排除
- 上下文捕获有计算开销
- 需要仔细配置以获得最佳性能

## 未来路线图
- 改进的 ML 驱动上下文压缩
- 增强的跨领域知识转移
- 实时协作上下文编辑
- 预测性上下文推荐系统
