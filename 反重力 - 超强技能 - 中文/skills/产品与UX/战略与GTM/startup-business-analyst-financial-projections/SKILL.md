---
name: startup-business-analyst-financial-projections
description: '创建详细的3-5年财务模型，包含收入、成本、现金流和情景分析
  '
risk: unknown
source: community
date_added: '2026-02-27'
---

# 财务预测

创建全面的3-5年财务模型，包含收入预测、成本结构、人力规划、现金流分析和三情景建模（保守、基准、乐观），用于创业财务规划和融资。

## 适用场景

- 处理财务预测相关任务或工作流
- 需要财务预测的指导、最佳实践或检查清单

## 不适用场景

- 任务与财务预测无关
- 需要超出此范围的其他领域或工具

## 指导说明

- 明确目标、约束条件和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，请打开 `resources/implementation-playbook.md`

## 此命令的功能

此命令构建完整的财务模型，包括：
1. 基于队列的收入预测
2. 详细成本结构（COGS、S&M、R&D、G&A）
3. 按岗位的人力规划
4. 月度现金流分析
5. 关键指标（CAC、LTV、Burn Rate、Runway）
6. 三情景分析

## Claude 执行步骤

调用此命令时，请按以下步骤执行：

### 第1步：收集模型输入

向用户收集关键信息：

**商业模式：**
- 收入模式（SaaS、交易平台、交易型等）
- 定价结构（层级、平均价格）
- 目标客户群

**起点数据：**
- 当前 MRR/ARR（如有）
- 当前客户数量
- 当前团队规模
- 当前现金余额

**增长假设：**
- 预期月新增客户数
- 客户留存率/流失率
- 平均合同价值（ACV）
- 销售周期长度

**成本假设：**
- 毛利率或 COGS 占比
- S&M 预算或 CAC 目标
- 当前 Burn Rate（如适用）

**融资：**
- 计划融资（金额、时间点）
- 投前/投后估值

### 第2步：调用 startup-financial-modeling 技能

startup-financial-modeling 技能提供框架，可参考以下内容：
- 收入建模方法
- 成本结构模板
- 人力规划指导
- 情景分析方法

### 第3步：构建收入模型

**使用队列分析法：**

每月追踪：
1. 新增客户数
2. 留存客户数（应用流失率）
3. 各队列收入（客户数 × ARPU）
4. 扩展收入（追加销售）

**公式：**
```
MRR (Month N) = Σ across all cohorts:
  (Cohort Size × Retention Rate × ARPU) + Expansion
```

**预测粒度：**
- 第1-2年：月度明细
- 第3年：季度明细
- 第4-5年：年度汇总

### 第4步：建模成本结构

拆分运营费用：

**1. 销售成本（COGS）**
- 托管/基础设施（占收入百分比或固定费用）
- 支付处理费（占收入百分比）
- 可变客户支持成本
- 第三方服务

目标毛利率：
- SaaS：75-85%
- 交易平台：60-70%
- 电商：40-60%

**2. 销售与营销（S&M）**
- 销售团队薪酬
- 营销项目
- 工具和软件
- 目标：占收入的 40-60%（早期阶段）

**3. 研发（R&D）**
- 工程团队
- 产品管理
- 设计
- 目标：占收入的 30-40%

**4. 管理费用（G&A）**
- 高管团队
- 财务、法务、人力资源
- 办公和设施
- 目标：占收入的 15-25%

### 第5步：规划人力

制定按岗位的招聘计划：

**参考 team-composition-analysis 技能获取：**
- 各阶段所需岗位
- 薪酬基准
- 招聘速度假设

**每个岗位的信息：**
- 职位名称和部门
- 入职日期（月/季度）
- 基本工资
- 全包成本（工资 × 1.3-1.4）
- 股权授予

**追踪部门比例：**
- 工程：占团队 40-50%
- 销售与营销：25-35%
- 管理：10-15%
- 产品/客户成功：10-15%

### 第6步：计算现金流

月度现金流预测：

```
Beginning Cash Balance
+ Cash Collected (revenue, consider payment terms)
- Operating Expenses
- CapEx
= Ending Cash Balance

Monthly Burn = Revenue - Expenses (if negative)
Runway = Cash Balance / Monthly Burn Rate
```

**包含融资事件：**
- 融资时间点
- 融资金额
- 资金用途
- 对现金余额的影响

### 第7步：计算关键指标

按月/季度计算：

**单位经济模型：**
- CAC（S&M 支出 / 新客户数）
- LTV（ARPU × 毛利率 / 流失率）
- LTV:CAC 比率（目标 > 3.0）
- CAC 回收期（目标 < 18 个月）

**效率指标：**
- Burn Multiple（净消耗 / 净新增 ARR）- 目标 < 2.0
- Magic Number（净新增 ARR / S&M 支出）- 目标 > 0.5
- Rule of 40（增长率% + 利润率%）- 目标 > 40%

**现金指标：**
- 月度 Burn Rate
- Runway（月数）
- 现金效率

### 第8步：创建三情景分析

构建保守、基准和乐观预测：

**保守情景（P10）：**
- 新客户：比基准低 30%
- 流失率：比基准高 20%
- 定价：比基准低 15%
- CAC：比基准高 25%

**基准情景（P50）：**
- 最可能的假设
- 主要规划情景

**乐观情景（P90）：**
- 新客户：比基准高 30%
- 流失率：比基准低 20%
- 定价：比基准高 15%
- CAC：比基准低 25%

### 第9步：生成财务模型报告

创建包含表格的完整 Markdown 报告：

**第1节：执行摘要**
- 3-5年财务概览
- 规模化时的关键指标
- 融资需求

**第2节：模型假设**
- 收入模型和定价
- 增长假设
- 成本结构假设
- 人力计划摘要

**第3节：收入预测**
月度/季度表格展示：
```
| Month | New Customers | Total Customers | MRR | ARR | Growth % |
|-------|---------------|-----------------|-----|-----|----------|
```

**第4节：成本明细**
```
| Department | Year 1 | Year 2 | Year 3 | % Revenue |
|------------|--------|--------|--------|-----------|
| COGS       | $X     | $Y     | $Z     | XX%       |
| S&M        | $X     | $Y     | $Z     | XX%       |
| R&D        | $X     | $Y     | $Z     | XX%       |
| G&A        | $X     | $Y     | $Z     | XX%       |
```

**第5节：人力计划**
```
| Department | Current | Year 1 | Year 2 | Year 3 |
|------------|---------|--------|--------|--------|
| Engineering| X       | Y      | Z      | W      |
```

**第6节：现金流分析**
```
| Quarter | Revenue | Expenses | Net Burn | Cash Balance | Runway |
|---------|---------|----------|----------|--------------|--------|
```

**第7节：关键指标**
```
| Metric | Year 1 | Year 2 | Year 3 | Target |
|--------|--------|--------|--------|--------|
| CAC | $X | $Y | $Z | <$A |
| LTV | $X | $Y | $Z | >$B |
| Burn Multiple | X | Y | Z | <2.0 |
```

**第8节：情景分析**
```
| Scenario | Year 3 ARR | Customers | Burn | Runway |
|----------|------------|-----------|------|--------|
| Conservative | $X | Y | $Z | W mo |
| Base | $X | Y | $Z | W mo |
| Optimistic | $X | Y | $Z | W mo |
```

**第9节：融资需求**
- 所需金额
- 资金用途分解
- 待实现里程碑
- 预期估值影响

**第10节：验证**
- 已执行的合理性检查
- 基准对比
- 风险因素
- 需监控的假设

### 第10步：保存模型

提供保存为 Markdown 文件的选项：
- 建议文件名：`financial-projections-YYYY-MM-DD.md`
- 提示用户可转换为 Excel/Sheets
- 提供关键计算公式

## 财务模型最佳实践

**推荐做法：**
- 使用基于队列的收入模型
- 包含 3 种情景
- 展示月度明细（第1-2年）
- 计算关键指标
- 对照基准验证
- 记录所有假设
- 展示现金流和 Runway
- 包含融资里程碑

**避免事项：**
- 对增长过于乐观
- 低估成本
- 忽略全包薪酬成本
- 忽视现金流时间差
- 跳过情景分析
- 使用静态人力规划
- 忘记验证

## 与其他命令的集成

配合使用效果更佳：
- `/market-opportunity` - 使用 SOM 作为收入上限
- `/business-case` - 将预测纳入商业案例

## 使用示例

```
User: /financial-projections

Claude: I'll create a comprehensive financial model for your startup. Let me gather the key inputs.

What's your business model?
→ "B2B SaaS, subscription-based"

Current state?
→ "$50K MRR, 100 customers, 5-person team, $500K cash"

Growth assumptions?
→ "Expect 15% MoM growth, 10% monthly churn, $500 ACV"

[Claude builds complete model with all sections]
```

## 备注

- 模型构建耗时 45-90 分钟
- 产出为全面的规划工具
- 建议每月更新以跟踪实际数据
- 可与投资人和董事会分享
- 用于融资演示文稿
- 作为预算和招聘决策的基础

## 局限性
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为特定环境验证、测试或专家评审的替代品
- 如缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清