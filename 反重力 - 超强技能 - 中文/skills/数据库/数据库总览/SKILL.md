---
name: database
description: "数据库开发与运维工作流，涵盖 SQL、NoSQL、数据库设计、迁移、优化和数据工程。触发词：数据库设计、数据库迁移、查询优化、数据管道、数据库运维、数据质量、SQL优化、NoSQL、PostgreSQL、MongoDB、Redis、数据仓库"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# 数据库工作流套件

## 概述

综合性数据库工作流，涵盖数据库设计、开发、优化、迁移和数据工程。包括 SQL、NoSQL 和现代数据平台。

## 何时使用此工作流

在以下场景使用此工作流：
- 设计数据库模式
- 实施数据库迁移
- 优化查询性能
- 搭建数据管道
- 管理数据库运维
- 实施数据质量保障

## 工作流阶段

### 阶段 1：数据库设计

#### 调用技能
- `database-architect` - 数据库架构
- `database-design` - 模式设计
- `postgresql` - PostgreSQL 设计
- `nosql-expert` - NoSQL 设计

#### 操作步骤
1. 收集需求
2. 设计模式
3. 定义关系
4. 规划索引策略
5. 可扩展性设计

#### 复制粘贴提示词
```
Use @database-architect to design database schema
```

```
Use @postgresql to design PostgreSQL schema
```

### 阶段 2：数据库实施

#### 调用技能
- `prisma-expert` - Prisma ORM
- `database-migrations-sql-migrations` - SQL 迁移
- `neon-postgres` - 无服务器 Postgres

#### 操作步骤
1. 设置数据库连接
2. 配置 ORM
3. 创建迁移
4. 实现模型
5. 设置种子数据

#### 复制粘贴提示词
```
Use @prisma-expert to set up Prisma ORM
```

```
Use @database-migrations-sql-migrations to create migrations
```

### 阶段 3：查询优化

#### 调用技能
- `database-optimizer` - 数据库优化
- `sql-optimization-patterns` - SQL 优化
- `postgres-best-practices` - PostgreSQL 优化

#### 操作步骤
1. 分析慢查询
2. 审查执行计划
3. 优化索引
4. 重构查询
5. 实施缓存

#### 复制粘贴提示词
```
Use @database-optimizer to optimize database performance
```

```
Use @sql-optimization-patterns to optimize SQL queries
```

### 阶段 4：数据迁移

#### 调用技能
- `database-migration` - 数据库迁移
- `framework-migration-code-migrate` - 代码迁移

#### 操作步骤
1. 规划迁移策略
2. 创建迁移脚本
3. 测试迁移
4. 执行迁移
5. 验证数据完整性

#### 复制粘贴提示词
```
Use @database-migration to plan database migration
```

### 阶段 5：数据管道开发

#### 调用技能
- `data-engineer` - 数据工程
- `data-engineering-data-pipeline` - 数据管道
- `airflow-dag-patterns` - Airflow 工作流
- `dbt-transformation-patterns` - dbt 转换

#### 操作步骤
1. 设计数据管道
2. 搭建数据摄入
3. 实现转换逻辑
4. 配置调度
5. 设置监控

#### 复制粘贴提示词
```
Use @data-engineer to design data pipeline
```

```
Use @airflow-dag-patterns to create Airflow DAGs
```

### 阶段 6：数据质量

#### 调用技能
- `data-quality-frameworks` - 数据质量
- `data-engineering-data-driven-feature` - 数据驱动特性

#### 操作步骤
1. 定义质量指标
2. 实施验证
3. 设置监控
4. 创建告警
5. 文档化标准

#### 复制粘贴提示词
```
Use @data-quality-frameworks to implement data quality checks
```

### 阶段 7：数据库运维

#### 调用技能
- `database-admin` - 数据库管理
- `backup-automation` - 备份自动化

#### 操作步骤
1. 设置备份
2. 配置复制
3. 监控性能
4. 规划容量
5. 实施安全措施

#### 复制粘贴提示词
```
Use @database-admin to manage database operations
```

## 数据库技术工作流

### PostgreSQL
```
Skills: postgresql, postgres-best-practices, neon-postgres, prisma-expert
```

### MongoDB
```
Skills: nosql-expert, azure-cosmos-db-py
```

### Redis
```
Skills: bullmq-specialist, upstash-qstash
```

### 数据仓库
```
Skills: clickhouse-io, dbt-transformation-patterns
```

## 质量门控

- [ ] 模式已设计并审查
- [ ] 迁移已测试
- [ ] 性能基准已达标
- [ ] 备份已配置
- [ ] 监控已就位
- [ ] 文档已完成

## 相关工作流套件

- `development` - 应用开发
- `cloud-devops` - 基础设施
- `ai-ml` - AI/ML 数据管道
- `testing-qa` - 数据测试

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代环境特定的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清。
