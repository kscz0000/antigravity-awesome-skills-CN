---
name: product-manager-toolkit
description: "现代产品管理必备工具与框架，覆盖从发现到交付的全流程。触发词：产品管理、PM工具、需求文档、PRD、功能优先级、RICE评分、用户访谈、路线图、产品策略、MVP、产品发现、用户故事、MoSCoW"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Product Manager Toolkit

现代产品管理必备工具与框架，覆盖从发现到交付的全流程。

## 快速开始

### 功能优先级排序
```bash
python scripts/rice_prioritizer.py sample  # Create sample CSV
python scripts/rice_prioritizer.py sample_features.csv --capacity 15
```

### 访谈分析
```bash
python scripts/customer_interview_analyzer.py interview_transcript.txt
```

### PRD 创建
1. 从 `references/prd_templates.md` 选择模板
2. 基于发现阶段的工作填写各章节
3. 与利益相关方评审
4. 在 PM 工具中做版本管理

## 核心工作流

### 功能优先级流程

1. **收集功能需求**
   - 客户反馈
   - 销售请求
   - 技术债务
   - 战略举措

2. **RICE 评分**
   ```bash
   # Create CSV with: name,reach,impact,confidence,effort
   python scripts/rice_prioritizer.py features.csv
   ```
   - **Reach（覆盖面）**：每季度受影响的用户数
   - **Impact（影响力）**：massive/high/medium/low/minimal
   - **Confidence（置信度）**：high/medium/low
   - **Effort（工作量）**：xl/l/m/s/xs（人月）

3. **组合分析**
   - 审视速赢机会与战略押注
   - 检查工作量分布
   - 对照战略目标验证

4. **生成路线图**
   - 季度产能规划
   - 依赖关系映射
   - 利益相关方对齐

### 客户发现流程

1. **开展访谈**
   - 采用半结构化形式
   - 聚焦问题而非方案
   - 经许可后录音

2. **分析洞察**
   ```bash
   python scripts/customer_interview_analyzer.py transcript.txt
   ```
   提取内容：
   - 痛点及严重程度
   - 功能需求及优先级
   - 待完成任务（Jobs to be done）
   - 情感分析
   - 关键主题与引述

3. **综合发现**
   - 归类相似痛点
   - 跨访谈识别模式
   - 映射到机会领域

4. **验证方案**
   - 创建方案假设
   - 用原型测试
   - 度量实际行为与预期的偏差

### PRD 开发流程

1. **选择模板**
   - **标准 PRD**：复杂功能（6-8 周）
   - **单页 PRD**：简单功能（2-4 周）
   - **功能简报**：探索阶段（1 周）
   - **Agile Epic**：基于 Sprint 的交付

2. **组织内容**
   - 问题 → 方案 → 成功指标
   - 明确标注范围外内容
   - 清晰的验收标准

3. **协同评审**
   - 工程评估可行性
   - 设计评估体验
   - 销售评估市场验证
   - 支持评估运营影响

## 核心脚本

### rice_prioritizer.py
基于 RICE 框架的高级实现，支持组合分析。

**功能特性**：
- RICE 评分计算
- 组合平衡分析（速赢 vs 战略押注）
- 季度路线图生成
- 团队产能规划
- 多种输出格式（text/json/csv）

**使用示例**：
```bash
# Basic prioritization
python scripts/rice_prioritizer.py features.csv

# With custom team capacity (person-months per quarter)
python scripts/rice_prioritizer.py features.csv --capacity 20

# Output as JSON for integration
python scripts/rice_prioritizer.py features.csv --output json
```

### customer_interview_analyzer.py
基于 NLP 的访谈分析工具，提取可操作洞察。

**能力范围**：
- 痛点提取与严重程度评估
- 功能需求识别与分类
- Jobs-to-be-done 模式识别
- 情感分析
- 主题提取
- 竞品提及
- 关键引述识别

**使用示例**：
```bash
# Analyze single interview
python scripts/customer_interview_analyzer.py interview.txt

# Output as JSON for aggregation
python scripts/customer_interview_analyzer.py interview.txt json
```

## 参考文档

### prd_templates.md
适配不同场景的多种 PRD 格式：

1. **标准 PRD 模板**
   - 完整的 11 章节格式
   - 适合重大功能
   - 包含技术规格

2. **单页 PRD**
   - 简洁格式，快速对齐
   - 聚焦问题/方案/指标
   - 适合小型功能

3. **Agile Epic 模板**
   - 基于 Sprint 的交付
   - 用户故事映射
   - 聚焦验收标准

4. **功能简报**
   - 轻量探索
   - 假设驱动
   - PRD 前置阶段

## 优先级框架

### RICE 框架
```
Score = (Reach × Impact × Confidence) / Effort

Reach: # of users/quarter
Impact: 
  - Massive = 3x
  - High = 2x
  - Medium = 1x
  - Low = 0.5x
  - Minimal = 0.25x
Confidence:
  - High = 100%
  - Medium = 80%
  - Low = 50%
Effort: Person-months
```

### 价值-工作量矩阵
```
         Low Effort    High Effort
         
High     QUICK WINS    BIG BETS
Value    [Prioritize]   [Strategic]
         
Low      FILL-INS      TIME SINKS
Value    [Maybe]       [Avoid]
```

### MoSCoW 方法
- **Must Have（必须有）**：上线的关键要素
- **Should Have（应该有）**：重要但非关键
- **Could Have（可以有）**：锦上添花
- **Won't Have（不做）**：超出范围

## 发现框架

### 客户访谈指南
```
1. Context Questions (5 min)
   - Role and responsibilities
   - Current workflow
   - Tools used

2. Problem Exploration (15 min)
   - Pain points
   - Frequency and impact
   - Current workarounds

3. Solution Validation (10 min)
   - Reaction to concepts
   - Value perception
   - Willingness to pay

4. Wrap-up (5 min)
   - Other thoughts
   - Referrals
   - Follow-up permission
```

### 假设模板
```
We believe that [building this feature]
For [these users]
Will [achieve this outcome]
We'll know we're right when [metric]
```

### 机会解决方案树
```
Outcome
├── Opportunity 1
│   ├── Solution A
│   └── Solution B
└── Opportunity 2
    ├── Solution C
    └── Solution D
```

## 指标与分析

### 北极星指标框架
1. **识别核心价值**：对用户来说最重要的价值是什么？
2. **可量化**：可度量、可追踪
3. **可行动**：团队能对其产生影响
4. **先行指标**：能预测业务成功

### 漏斗分析模板
```
Acquisition → Activation → Retention → Revenue → Referral

Key Metrics:
- Conversion rate at each step
- Drop-off points
- Time between steps
- Cohort variations
```

### 功能成功指标
- **采纳率**：使用该功能的用户占比
- **使用频率**：每用户每时间段的使用次数
- **使用深度**：功能能力被使用的比例
- **留存率**：随时间持续使用的情况
- **满意度**：该功能的 NPS/CSAT 评分

## 最佳实践

### 写好 PRD
1. 从问题出发，而非方案
2. 前置清晰的成功指标
3. 明确标注范围外内容
4. 使用可视化（线框图、流程图）
5. 技术细节放附录
6. 版本管理变更

### 有效优先级排序
1. 速赢与战略押注搭配
2. 考虑机会成本
3. 考量依赖关系
4. 预留 20% 缓冲应对突发
5. 每季度复盘
6. 决策沟通要清晰

### 客户发现技巧
1. 连问 5 个"为什么"
2. 关注过去行为，而非未来意图
3. 避免引导性问题
4. 在客户环境中访谈
5. 留意情绪反应
6. 用数据验证

### 利益相关方管理
1. 明确 RACI 决策矩阵
2. 定期异步更新
3. 用演示代替文档
4. 及早回应顾虑
5. 公开庆祝成果
6. 坦诚从失败中学习

## 常见陷阱

1. **方案先行思维**：还没理解问题就跳到功能设计
2. **分析瘫痪**：过度研究却迟迟不交付
3. **功能工厂**：只管发布功能却不衡量影响
4. **忽视技术债务**：不为平台健康分配时间
5. **利益相关方突袭**：没有提前和持续地沟通
6. **指标表演**：优化虚荣指标而非真实价值

## 集成对接

本工具包支持与以下工具集成：
- **分析工具**：Amplitude、Mixpanel、Google Analytics
- **路线图工具**：ProductBoard、Aha!、Roadmunk
- **设计工具**：Figma、Sketch、Miro
- **开发工具**：Jira、Linear、GitHub
- **研究工具**：Dovetail、UserVoice、Pendo
- **协作工具**：Slack、Notion、Confluence

## 速查命令

```bash
# Prioritization
python scripts/rice_prioritizer.py features.csv --capacity 15

# Interview Analysis
python scripts/customer_interview_analyzer.py interview.txt

# Create sample data
python scripts/rice_prioritizer.py sample

# JSON outputs for integration
python scripts/rice_prioritizer.py features.csv --output json
python scripts/customer_interview_analyzer.py interview.txt json
```

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不可将输出视为环境特定验证、测试或专家评审的替代品。
- 当所需输入、权限、安全边界或成功标准缺失时，应停下来要求澄清。
