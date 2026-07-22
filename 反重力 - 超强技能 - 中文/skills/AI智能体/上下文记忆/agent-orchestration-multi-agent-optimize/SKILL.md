---
name: agent-orchestration-multi-agent-optimize
description: "通过协调式性能分析、工作负载分配和成本感知编排优化多智能体系统。触发词：多智能体优化、agent编排优化、智能体性能调优、多代理协调、agent orchestration、multi-agent optimization、智能体吞吐量、智能体延迟优化、成本感知编排"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 多智能体优化工具包

## 使用此技能的场景

- 改善多智能体协调、吞吐量或延迟
- 分析智能体工作流以识别瓶颈
- 为复杂工作流设计编排策略
- 优化成本、上下文使用或工具效率

## 不适用场景

- 只需要调优单个智能体提示词
- 没有可衡量的指标或评估数据
- 任务与多智能体编排无关

## 操作指引

1. 建立基线指标和目标性能目标。
2. 分析智能体工作负载并识别协调瓶颈。
3. 增量应用编排变更和成本控制。
4. 通过可重复测试和回滚验证改进效果。

## 安全须知

- 避免在未进行回归测试的情况下部署编排变更。
- 逐步推出变更以防止系统级回归。

## 角色：AI 驱动的多智能体性能工程专家

### 背景

多智能体优化工具是一个先进的 AI 驱动框架，通过智能、协调的智能体优化全面提升系统性能。利用前沿的 AI 编排技术，该工具提供了跨多个领域的性能工程综合解决方案。

### 核心能力

- 智能多智能体协调
- 性能分析和瓶颈识别
- 自适应优化策略
- 跨领域性能优化
- 成本和效率追踪

## 参数处理

该工具通过灵活的输入参数处理优化参数：

- `$TARGET`: 要优化的主要系统/应用
- `$PERFORMANCE_GOALS`: 具体的性能指标和目标
- `$OPTIMIZATION_SCOPE`: 优化深度（quick-win 快速见效、comprehensive 全面）
- `$BUDGET_CONSTRAINTS`: 成本和资源限制
- `$QUALITY_METRICS`: 性能质量阈值

## 1. 多智能体性能分析

### 分析策略

- 跨系统层的分布式性能监控
- 实时指标收集和分析
- 持续性能特征追踪

#### 分析智能体

1. **数据库性能智能体**
   - 查询执行时间分析
   - 索引使用追踪
   - 资源消耗监控

2. **应用性能智能体**
   - CPU 和内存分析
   - 算法复杂度评估
   - 并发和异步操作分析

3. **前端性能智能体**
   - 渲染性能指标
   - 网络请求优化
   - Core Web Vitals 监控

### 分析代码示例

```python
def multi_agent_profiler(target_system):
    agents = [
        DatabasePerformanceAgent(target_system),
        ApplicationPerformanceAgent(target_system),
        FrontendPerformanceAgent(target_system)
    ]

    performance_profile = {}
    for agent in agents:
        performance_profile[agent.__class__.__name__] = agent.profile()

    return aggregate_performance_metrics(performance_profile)
```

## 2. 上下文窗口优化

### 优化技术

- 智能上下文压缩
- 语义相关性过滤
- 动态上下文窗口调整
- Token 预算管理

### 上下文压缩算法

```python
def compress_context(context, max_tokens=4000):
    # 使用基于嵌入的截断进行语义压缩
    compressed_context = semantic_truncate(
        context,
        max_tokens=max_tokens,
        importance_threshold=0.7
    )
    return compressed_context
```

## 3. 智能体协调效率

### 协调原则

- 并行执行设计
- 最小化智能体间通信开销
- 动态工作负载分配
- 容错智能体交互

### 编排框架

```python
class MultiAgentOrchestrator:
    def __init__(self, agents):
        self.agents = agents
        self.execution_queue = PriorityQueue()
        self.performance_tracker = PerformanceTracker()

    def optimize(self, target_system):
        # 并行智能体执行与协调优化
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(agent.optimize, target_system): agent
                for agent in self.agents
            }

            for future in concurrent.futures.as_completed(futures):
                agent = futures[future]
                result = future.result()
                self.performance_tracker.log(agent, result)
```

## 4. 并行执行优化

### 关键策略

- 异步智能体处理
- 工作负载分区
- 动态资源分配
- 最小化阻塞操作

## 5. 成本优化策略

### LLM 成本管理

- Token 使用追踪
- 自适应模型选择
- 缓存和结果复用
- 高效提示词工程

### 成本追踪示例

```python
class CostOptimizer:
    def __init__(self):
        self.token_budget = 100000  # 月度预算
        self.token_usage = 0
        self.model_costs = {
            'gpt-5': 0.03,
            'claude-4-sonnet': 0.015,
            'claude-4-haiku': 0.0025
        }

    def select_optimal_model(self, complexity):
        # 基于任务复杂度和预算的动态模型选择
        pass
```

## 6. 延迟降低技术

### 性能加速

- 预测性缓存
- 预热智能体上下文
- 智能结果记忆化
- 减少往返通信

## 7. 质量与速度权衡

### 优化谱系

- 性能阈值
- 可接受的降级幅度
- 质量感知优化
- 智能妥协选择

## 8. 监控与持续改进

### 可观测性框架

- 实时性能仪表盘
- 自动化优化反馈循环
- 机器学习驱动的改进
- 自适应优化策略

## 参考工作流

### 工作流 1：电商平台优化

1. 初始性能分析
2. 智能体优化
3. 成本和性能追踪
4. 持续改进循环

### 工作流 2：企业 API 性能增强

1. 全面系统分析
2. 多层智能体优化
3. 迭代性能精炼
4. 成本高效扩展策略

## 关键注意事项

- 优化前后始终进行测量
- 优化过程中保持系统稳定性
- 平衡性能收益与资源消耗
- 实施渐进式、可逆的变更

目标优化：$ARGUMENTS

## 局限性
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
