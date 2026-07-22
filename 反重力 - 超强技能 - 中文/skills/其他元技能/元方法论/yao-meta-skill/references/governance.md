# 治理模型

本项目将重要技能视为被治理的资产，而非一次性提示词文件。

## 目标

- 让共享技能长期保持可信
- 让所有权归属明确
- 避免技能包过时或过于庞大
- 定义技能何时应该演进、拆分或退役

## 必需的治理元数据

对于可复用或库级别的技能，`manifest.json` 应包含：

- `name`
- `version`
- `owner`
- `updated_at`
- `review_cadence`
- `status`
- `maturity_tier`
- `lifecycle_stage`

## 允许的取值

### `status`

- `experimental`
- `active`
- `deprecated`

### `maturity_tier`

- `scaffold`
- `production`
- `library`
- `governed`

### `lifecycle_stage`

- `scaffold`
- `production`
- `library`
- `governed`

### `review_cadence`

- `monthly`
- `quarterly`
- `semiannual`
- `annual`
- `per-release`

## 治理规则

### 1. 必须有 Owner

任何预期被复用的技能都必须有一个具名的 owner 或负责团队。

### 2. 必须声明评审频率

如果一个技能是共享的，它必须声明应该多久评审一次。

### 3. 成熟度应与严谨度匹配

- `scaffold`：轻量、个人、低治理
- `production`：可复用的团队技能，带有验证
- `library`：经过精心策划的共享技能，具有明确的打包规范与评测
- `governed`：关键或元层面的技能，对回归、维护和评审有明确要求

### 4. 弃用技能需要明确意图

弃用的技能应在相邻文档或 manifest 扩展中包含弃用说明或替代引用。

### 5. 漂移必须可观测

重要技能应保留：

- 回归历史
- 可见的评测结果
- 已知的反模式或失败模式

## 治理动作

通过治理评审来决定一个技能是否应：

- 保持原样
- 收紧触发边界
- 拆分为兄弟技能
- 将细节迁移到 `references/`
- 将脆弱逻辑迁移到 `scripts/`
- 被弃用或替换

## 治理成熟度评分

`scripts/governance_check.py` 同时会计算一个满分 `100` 的成熟度得分。

### 评分区间

治理检查器除了声明的 manifest 层级外，还会计算一个评分区间。评分区间是一种诊断输出，并不能替代声明的生命周期层级。

- `90-100`：governed
- `80-89`：production
- `65-79`：reusable
- `45-64`：emerging
- `<45`：draft

### 各声明层级的建议最低分

- `scaffold`：无硬性下限
- `production`：`80`
- `library`：`85`
- `governed`：`90`

### 评分维度

- 元数据完整性
- 所有权与评审频率
- 边界与评测证据
- 运营资产
- 维护证据

该得分并不能替代人工评审。它是一个快速信号，用于表明一个共享技能在结构上是否足以被信任、维护和审计。当声明的层级所声称的严谨度超出当前得分所能支撑的水平时，`scripts/governance_check.py` 会发出警告。

## 为什么这件事很重要

大多数技能系统在创建之后就停止了。世界级的技能系统还会持续管理：

- 所有权
- 漂移
- 成熟度
- 弃用
- 持续质量的证据