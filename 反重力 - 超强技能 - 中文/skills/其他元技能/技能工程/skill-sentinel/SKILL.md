---
name: skill-sentinel
description: "技能生态系统的审计与演进。涵盖代码质量、安全、成本、缺口、重复、依赖和健康报告。触发词：审计技能、技能质量、检查技能生态系统、技能健康、重复技能、优化技能、skill sentinel"
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- governance
- audit
- quality
- skill-health
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Skill Sentinel

## 概述

技能生态系统的审计与演进。涵盖代码质量、安全、成本、缺口、重复、依赖和健康报告。

## 使用场景

- 当用户提到"审计技能"或相关话题时
- 当用户提到"技能质量"或相关话题时
- 当用户提到"检查技能生态系统"或相关话题时
- 当用户提到"技能生态系统健康"或相关话题时
- 当用户提到"重复技能"或相关话题时
- 当用户提到"优化技能"或相关话题时

## 不适用场景

- 任务与 skill sentinel 无关
- 有更简单、更具体的工具可以处理该请求
- 用户需要没有领域专业知识的通用协助

## 工作原理

元智能体，负责监控、审计和演进技能生态系统。从 7 个维度分析所有技能，识别问题，提出改进建议，并推荐新的专业技能。

## 快速概览

| 领域 | 脚本 | 功能 |
|------|------|------|
| **发现** | `scanner.py` | 自动发现所有技能 |
| **质量** | `analyzers/code_quality.py` | 复杂度、文档字符串、错误处理 |
| **安全** | `analyzers/security.py` | 密钥、SQL 注入、HTTPS |
| **性能** | `analyzers/performance.py` | API 调用、缓存、重试 |
| **治理** | `analyzers/governance_audit.py` | 速率限制、审计日志、确认机制 |
| **文档** | `analyzers/documentation.py` | SKILL.md、触发词、参考文件 |
| **依赖** | `analyzers/dependencies.py` | requirements.txt、版本 |
| **跨技能** | `analyzers/cross_skill.py` | 重复、共享模式 |
| **成本** | `cost_optimizer.py` | Token、冗余度、输出 |
| **推荐** | `recommender.py` | 缺口分析、新技能 |
| **报告** | `report_generator.py` | 结构化 Markdown |
| **编排** | `run_audit.py` | CLI 主入口 |

## 目录结构

```
C:\Users\renat\skills\skill-sentinel\
├── SKILL.md
├── scripts/
│   ├── requirements.txt
│   ├── config.py
│   ├── db.py
│   ├── governance.py
│   ├── scanner.py
│   ├── analyzers/
│   │   ├── code_quality.py
│   │   ├── security.py
│   │   ├── performance.py
│   │   ├── governance_audit.py
│   │   ├── documentation.py
│   │   ├── dependencies.py
│   │   └── cross_skill.py
│   ├── recommender.py
│   ├── cost_optimizer.py
│   ├── report_generator.py
│   └── run_audit.py
├── references/
│   ├── analysis_criteria.md
│   ├── security_patterns.md
│   ├── skill_template.md
│   └── schema.md
└── data/
    ├── sentinel.db
    └── reports/
```

## 安装

```bash
pip install -r C:\Users\renat\skills\skill-sentinel\scripts\requirements.txt
```

## 主要命令

```bash

## 完整审计所有技能

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py

## 仅审计单个技能

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --skill instagram

## 仅获取新技能推荐

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --recommend

## 与上次审计比较（趋势分析）

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --compare

## JSON 格式输出（用于后续处理）

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --format json

## 查看审计历史

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --history

## 发现可用技能

python C:\Users\renat\skills\skill-sentinel\scripts\scanner.py

## 查看 Sentinel 审计日志

python C:\Users\renat\skills\skill-sentinel\scripts\governance.py

## 检查数据库

python C:\Users\renat\skills\skill-sentinel\scripts\db.py
```

## 1. 代码质量（权重：20%）

- 每个函数的圈复杂度（阈值：10）
- 函数大小（阈值：50 行）
- 文件大小（阈值：500 行）
- 文档字符串覆盖率
- 错误处理模式（裸 except、宽泛 except）

## 2. 安全（权重：20%）

- 硬编码密钥（token、密码、API 密钥）
- SQL 注入（查询中使用 f-string）
- 不安全的 HTTP URL
- 日志中的 token
- 输入验证

## 3. 性能（权重：15%）

- API 的指数退避重试
- 超时配置
- HTTP 连接复用
- N+1 查询
- 异步/并发

## 4. 治理（权重：15%）

- 级别 0：无
- 级别 1：操作日志
- 级别 2：日志 + 速率限制
- 级别 3：完整（+ 两步确认）
- 级别 4：高级（+ 告警和趋势）

## 5. 文档（权重：15%）

- SKILL.md 含 frontmatter（name、description、version）
- 触发关键词（中文和英文）
- 必需和推荐章节
- 参考文件

## 6. 依赖（权重：15%）

- requirements.txt 是否存在
- 版本是否锁定
- 已导入 vs 已列出的依赖
- 已列出 vs 已导入的依赖

## 7. 跨技能（全局分析）

- 技能间重复模块
- 共享的数据库模式
- 不一致的治理
- 提取机会

## 成本优化

除了 7 个维度，sentinel 还分析成本影响：
- SKILL.md 大小（每次激活消耗的 token）
- 无索引的大型参考文件
- 脚本的冗余输出
- 缺少结构化 JSON 输出

## 缺口分析与推荐

推荐器通过与 20 个类别的分类法比较，识别生态系统中缺失的能力，并为建议的新技能生成即用的 SKILL.md 模板。

## Sentinel 自身治理

sentinel 自身也践行其理念：
- 所有审计记录在 action_log 中
- score_history 中的分数历史用于趋势分析
- 报告保存在 data/reports/

## 常见工作流

**1. 生态系统首次审计：**
```
python run_audit.py
```
生成包含分数、发现项和推荐的完整报告。

**2. 监控随时间的演进：**
```
python run_audit.py --compare
```
显示审计之间的分数变化。

**3. 部署前验证单个技能：**
```
python run_audit.py --skill nome-da-skill
```
聚焦审计，包含特定发现项。

**4. 确定下一个要创建的技能：**
```
python run_audit.py --recommend
```
缺口分析，附带即用模板。

## 报告格式

在 `data/reports/` 中生成的报告包含：
1. 执行摘要（分数表）
2. 趋势（如有上次审计）
3. 按严重级别分类的发现项（严重/高/中/低/信息）
4. 按技能分析（详细）
5. 新技能推荐
6. 优先级排序的行动计划

## 参考资料

技术详情请查阅：
- `references/analysis_criteria.md` - 评分标准
- `references/security_patterns.md` - 安全模式
- `references/skill_template.md` - 新技能模板
- `references/schema.md` - 数据库 Schema

## 最佳实践

- 提供关于项目和需求的清晰、具体的上下文
- 在应用到生产代码前审查所有建议
- 结合其他互补技能进行综合分析

## 常见陷阱

- 将此技能用于其领域专业之外的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 相关技能

- `skill-installer` - 增强分析的互补技能

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
