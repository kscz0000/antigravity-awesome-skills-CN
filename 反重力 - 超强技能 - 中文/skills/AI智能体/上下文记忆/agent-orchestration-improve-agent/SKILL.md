---
name: agent-orchestration-improve-agent
description: "通过性能分析、提示词工程和持续迭代系统化改进现有智能体。触发词：智能体优化、agent优化、提示词改进、性能调优、agent improvement、prompt engineering、迭代优化、智能体改进"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 智能体性能优化工作流

通过性能分析、提示词工程和持续迭代系统化改进现有智能体。

[扩展思考：智能体优化需要数据驱动的方法，结合性能指标、用户反馈分析和高级提示词工程技术。成功取决于系统化评估、针对性改进以及严格的测试，并具备生产安全的回滚能力。]

## 使用此技能的场景

- 改进现有智能体的性能或可靠性
- 分析失败模式、提示词质量或工具使用情况
- 运行结构化 A/B 测试或评估套件
- 为智能体设计迭代优化工作流

## 不适用场景

- 从零构建全新智能体
- 没有可用的指标、反馈或测试用例
- 任务与智能体性能或提示词质量无关

## 操作说明

1. 建立基线指标并收集代表性示例。
2. 识别失败模式并优先处理高影响修复。
3. 应用提示词和工作流改进，设定可衡量目标。
4. 通过测试验证，分阶段受控发布变更。

## 安全注意事项

- 避免在未进行回归测试的情况下部署提示词变更。
- 如果质量或安全指标出现回退，快速回滚。

## 第一阶段：性能分析与基线指标

使用 context-manager 进行历史数据收集，全面分析智能体性能。

### 1.1 收集性能数据

```
Use: context-manager
Command: analyze-agent-performance $ARGUMENTS --days 30
```

收集的指标包括：

- 任务完成率（成功 vs 失败任务）
- 响应准确性和事实正确性
- 工具使用效率（正确工具、调用频率）
- 平均响应时间和 token 消耗
- 用户满意度指标（修正次数、重试次数）
- 幻觉事件和错误模式

### 1.2 用户反馈模式分析

识别用户交互中的重复模式：

- **修正模式**：用户持续修改输出的位置
- **澄清请求**：常见的歧义区域
- **任务放弃**：用户放弃的节点
- **追问**：响应不完整的信号
- **正面反馈**：需要保留的成功模式

### 1.3 失败模式分类

按根因对失败进行分类：

- **指令误解**：角色或任务混淆
- **输出格式错误**：结构或格式问题
- **上下文丢失**：长对话退化
- **工具误用**：错误或低效的工具选择
- **约束违规**：安全或业务规则违反
- **边缘情况处理**：异常输入场景

### 1.4 基线性能报告

生成量化基线指标：

```
Performance Baseline:
- Task Success Rate: [X%]
- Average Corrections per Task: [Y]
- Tool Call Efficiency: [Z%]
- User Satisfaction Score: [1-10]
- Average Response Latency: [Xms]
- Token Efficiency Ratio: [X:Y]
```

## 第二阶段：提示词工程改进

使用 prompt-engineer 智能体应用高级提示词优化技术。

### 2.1 思维链增强

实现结构化推理模式：

```
Use: prompt-engineer
Technique: chain-of-thought-optimization
```

- 添加显式推理步骤："让我们一步步来处理..."
- 包含自检验检查点："在继续之前，验证..."
- 对复杂任务实现递归分解
- 添加推理轨迹可见性用于调试

### 2.2 少样本示例优化

从成功交互中精选高质量示例：

- **选择多样化示例**覆盖常见用例
- **包含边缘情况**，特别是之前失败的
- **同时展示正面和负面示例**并附带解释
- **按从简单到复杂排序示例**
- **为示例标注**关键决策点

示例结构：

```
Good Example:
Input: [User request]
Reasoning: [Step-by-step thought process]
Output: [Successful response]
Why this works: [Key success factors]

Bad Example:
Input: [Similar request]
Output: [Failed response]
Why this fails: [Specific issues]
Correct approach: [Fixed version]
```

### 2.3 角色定义精炼

强化智能体身份和能力：

- **核心目的**：清晰的单句使命
- **专业领域**：具体知识范围
- **行为特征**：个性和交互风格
- **工具熟练度**：可用工具及使用时机
- **约束条件**：智能体不应做的事
- **成功标准**：如何衡量任务完成

### 2.4 Constitutional AI 集成

实现自我修正机制：

```
Constitutional Principles:
1. Verify factual accuracy before responding
2. Self-check for potential biases or harmful content
3. Validate output format matches requirements
4. Ensure response completeness
5. Maintain consistency with previous responses
```

添加批判-修订循环：

- 初始响应生成
- 根据原则自我批判
- 检测到问题时自动修订
- 输出前最终验证

### 2.5 输出格式调优

优化响应结构：

- **结构化模板**用于常见任务
- **动态格式化**基于复杂度
- **渐进式披露**用于详细信息
- **Markdown 优化**提升可读性
- **代码块格式化**带语法高亮
- **表格和列表生成**用于数据展示

## 第三阶段：测试与验证

具备 A/B 对比的全面测试框架。

### 3.1 测试套件开发

创建代表性测试场景：

```
Test Categories:
1. Golden path scenarios (common successful cases)
2. Previously failed tasks (regression testing)
3. Edge cases and corner scenarios
4. Stress tests (complex, multi-step tasks)
5. Adversarial inputs (potential breaking points)
6. Cross-domain tasks (combining capabilities)
```

### 3.2 A/B 测试框架

对比原始智能体与改进后智能体：

```
Use: parallel-test-runner
Config:
  - Agent A: Original version
  - Agent B: Improved version
  - Test set: 100 representative tasks
  - Metrics: Success rate, speed, token usage
  - Evaluation: Blind human review + automated scoring
```

统计显著性测试：

- 最小样本量：每个变体 100 个任务
- 置信水平：95% (p < 0.05)
- 效应量计算 (Cohen's d)
- 未来测试的功效分析

### 3.3 评估指标

全面评分框架：

**任务级指标：**

- 完成率（二元成功/失败）
- 正确性评分（0-100% 准确度）
- 效率评分（实际步骤 vs 最优步骤）
- 工具使用适当性
- 响应相关性和完整性

**质量指标：**

- 幻觉率（每响应的事实错误数）
- 一致性评分（与先前响应的对齐度）
- 格式合规性（符合指定结构）
- 安全评分（约束遵守度）
- 用户满意度预测

**性能指标：**

- 响应延迟（首个 token 时间）
- 总生成时间
- Token 消耗（输入 + 输出）
- 单任务成本（API 使用费用）
- 内存/上下文效率

### 3.4 人工评估协议

结构化人工审查流程：

- 盲评（评估者不知道版本）
- 带明确标准的标准化评分表
- 每个样本多位评估者（评估者间信度）
- 定性反馈收集
- 偏好排序（A vs B 对比）

## 第四阶段：版本控制与部署

具备监控和回滚能力的安全发布。

### 4.1 版本管理

系统化版本策略：

```
Version Format: agent-name-v[MAJOR].[MINOR].[PATCH]
Example: customer-support-v2.3.1

MAJOR: Significant capability changes
MINOR: Prompt improvements, new examples
PATCH: Bug fixes, minor adjustments
```

维护版本历史：

- 基于 Git 的提示词存储
- 带改进详情的变更日志
- 每版本性能指标
- 记录回滚流程

### 4.2 分阶段发布

渐进式部署策略：

1. **Alpha 测试**：内部团队验证（5% 流量）
2. **Beta 测试**：选定用户（20% 流量）
3. **金丝雀发布**：逐步增加（20% → 50% → 100%）
4. **全量部署**：满足成功标准后
5. **监控期**：7 天观察窗口

### 4.3 回滚流程

快速恢复机制：

```
Rollback Triggers:
- Success rate drops >10% from baseline
- Critical errors increase >5%
- User complaints spike
- Cost per task increases >20%
- Safety violations detected

Rollback Process:
1. Detect issue via monitoring
2. Alert team immediately
3. Switch to previous stable version
4. Analyze root cause
5. Fix and re-test before retry
```

### 4.4 持续监控

实时性能追踪：

- 关键指标仪表盘
- 异常检测告警
- 用户反馈收集
- 自动化回归测试
- 每周性能报告

## 成功标准

智能体改进成功的标志：

- 任务成功率提升 ≥15%
- 用户修正减少 ≥25%
- 安全违规无增加
- 响应时间保持在基线 10% 以内
- 单任务成本增加不超过 5%
- 正面用户反馈增加

## 部署后审查

生产使用 30 天后：

1. 分析累积性能数据
2. 与基线和目标对比
3. 识别新的改进机会
4. 记录经验教训
5. 规划下一轮优化周期

## 持续改进循环

建立定期改进节奏：

- **每周**：监控指标并收集反馈
- **每月**：分析模式并规划改进
- **每季度**：带新能力的主要版本更新
- **每年**：战略审查和架构更新

记住：智能体优化是一个迭代过程。每个周期都建立在之前的经验之上，逐步提升性能，同时保持稳定性和安全性。

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
