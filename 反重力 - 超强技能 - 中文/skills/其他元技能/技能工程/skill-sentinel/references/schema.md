# 数据库 Schema - Sentinel

数据库：`data/sentinel.db`（SQLite，WAL 模式）

## 表

### audit_runs
每次审计执行的记录。

| 列 | 类型 | 说明 |
|--------|------|-----------|
| id | INTEGER PK | 自增主键 |
| started_at | TEXT | ISO 8601 时间戳 |
| completed_at | TEXT | 完成时间戳 |
| skills_scanned | INTEGER | 技能数量 |
| total_findings | INTEGER | 发现总数 |
| overall_score | REAL | 生态系统平均得分 |
| report_path | TEXT | 报告 .md 路径 |
| status | TEXT | running / completed / failed |

### skill_snapshots
每次审计中每个技能的状态。

| 列 | 类型 | 说明 |
|--------|------|-----------|
| id | INTEGER PK | 自增主键 |
| audit_run_id | INTEGER FK | 引用 audit_runs |
| skill_name | TEXT | 技能名称 |
| skill_path | TEXT | 文件系统路径 |
| version | TEXT | SKILL.md 版本 |
| file_count | INTEGER | Python 文件数 |
| line_count | INTEGER | 总行数 |
| overall_score | REAL | 综合得分 |
| code_quality | REAL | 代码质量得分 |
| security | REAL | 安全性得分 |
| performance | REAL | 性能得分 |
| governance | REAL | 治理得分 |
| documentation | REAL | 文档得分 |
| dependencies | REAL | 依赖得分 |
| raw_metrics | TEXT | 详细指标 JSON |

### findings
个别问题与建议。

| 列 | 类型 | 说明 |
|--------|------|-----------|
| id | INTEGER PK | 自增主键 |
| audit_run_id | INTEGER FK | 引用 audit_runs |
| skill_name | TEXT | 受影响技能 |
| dimension | TEXT | code_quality/security 等 |
| severity | TEXT | critical/high/medium/low/info |
| category | TEXT | 具体分类 |
| title | TEXT | 简短标题 |
| description | TEXT | 详细描述 |
| file_path | TEXT | 受影响文件 |
| line_number | INTEGER | 受影响行号 |
| recommendation | TEXT | 修正建议 |
| effort | TEXT | low/medium/high |
| impact | TEXT | low/medium/high |

### skill_recommendations
新技能建议。

| 列 | 类型 | 说明 |
|--------|------|-----------|
| id | INTEGER PK | 自增主键 |
| audit_run_id | INTEGER FK | 引用 audit_runs |
| suggested_name | TEXT | 建议名称 |
| rationale | TEXT | 理由 |
| capabilities | TEXT | JSON 数组：能力列表 |
| priority | TEXT | critical/high/medium/low |
| skill_md_draft | TEXT | SKILL.md 草稿 |

### score_history
用于趋势分析的得分历史。

| 列 | 类型 | 说明 |
|--------|------|-----------|
| id | INTEGER PK | 自增主键 |
| audit_run_id | INTEGER FK | 引用 audit_runs |
| skill_name | TEXT | 技能名称 |
| dimension | TEXT | 维度 |
| score | REAL | 记录的得分 |
| recorded_at | TEXT | 时间戳 |

### action_log
Sentinel 的自治操作日志。

| 列 | 类型 | 说明 |
|--------|------|-----------|
| id | INTEGER PK | 自增主键 |
| action | TEXT | 操作类型 |
| params | TEXT | JSON：参数 |
| result | TEXT | JSON：结果 |
| created_at | TEXT | 时间戳 |

## 索引

- `idx_snapshots_run` - skill_snapshots(audit_run_id)
- `idx_snapshots_skill` - skill_snapshots(skill_name)
- `idx_findings_run` - findings(audit_run_id)
- `idx_findings_skill` - findings(skill_name)
- `idx_findings_severity` - findings(severity)
- `idx_findings_dim` - findings(dimension)
- `idx_history_skill` - score_history(skill_name)
- `idx_history_time` - score_history(recorded_at)
- `idx_action_log_time` - action_log(created_at)
