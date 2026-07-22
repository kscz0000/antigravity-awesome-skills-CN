---
name: postgresql-optimization
description: "PostgreSQL 数据库优化工作流，涵盖查询调优、索引策略、性能分析和生产数据库管理。当用户要求优化 PostgreSQL 查询、设计索引策略或分析数据库性能时使用。"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# PostgreSQL 优化工作流

## 概述

PostgreSQL 数据库优化的专业工作流，涵盖查询调优、索引策略、性能分析、vacuum 管理和生产数据库运维。

## 使用场景

适用场景：
- 优化慢查询
- 设计索引策略
- 分析数据库性能
- 调优 PostgreSQL 配置
- 管理生产数据库

## 工作流阶段

### 阶段 1：性能评估

#### 调用技能
- `database-optimizer` - 数据库优化
- `postgres-best-practices` - PostgreSQL 最佳实践

#### 操作步骤
1. 检查数据库版本
2. 审查配置
3. 分析慢查询
4. 检查资源使用情况
5. 识别瓶颈

#### 复制粘贴提示词
```
Use @database-optimizer to assess PostgreSQL performance
```

### 阶段 2：查询分析

#### 调用技能
- `sql-optimization-patterns` - SQL 优化
- `postgres-best-practices` - PostgreSQL 模式

#### 操作步骤
1. 运行 EXPLAIN ANALYZE
2. 识别扫描类型
3. 检查连接策略
4. 分析执行时间
5. 寻找优化机会

#### 复制粘贴提示词
```
Use @sql-optimization-patterns to analyze and optimize queries
```

### 阶段 3：索引策略

#### 调用技能
- `database-design` - 索引设计
- `postgresql` - PostgreSQL 索引

#### 操作步骤
1. 识别缺失索引
2. 创建 B-tree 索引
3. 添加复合索引
4. 考虑部分索引
5. 审查索引使用情况

#### 复制粘贴提示词
```
Use @database-design to design PostgreSQL indexing strategy
```

### 阶段 4：查询优化

#### 调用技能
- `sql-optimization-patterns` - 查询调优
- `sql-pro` - SQL 专家

#### 操作步骤
1. 重写低效查询
2. 优化连接
3. 在合适的地方添加 CTE
4. 实现分页
5. 测试改进效果

#### 复制粘贴提示词
```
Use @sql-optimization-patterns to optimize SQL queries
```

### 阶段 5：配置调优

#### 调用技能
- `postgres-best-practices` - 配置
- `database-admin` - 数据库管理

#### 操作步骤
1. 调优 shared_buffers
2. 配置 work_mem
3. 设置 effective_cache_size
4. 调整 checkpoint 设置
5. 配置 autovacuum

#### 复制粘贴提示词
```
Use @postgres-best-practices to tune PostgreSQL configuration
```

### 阶段 6：维护

#### 调用技能
- `database-admin` - 数据库维护
- `postgresql` - PostgreSQL 维护

#### 操作步骤
1. 调度 VACUUM
2. 运行 ANALYZE
3. 检查表膨胀
4. 监控 autovacuum
5. 审查统计信息

#### 复制粘贴提示词
```
Use @database-admin to schedule PostgreSQL maintenance
```

### 阶段 7：监控

#### 调用技能
- `grafana-dashboards` - 监控仪表盘
- `prometheus-configuration` - 指标采集

#### 操作步骤
1. 搭建监控
2. 创建仪表盘
3. 配置告警
4. 追踪关键指标
5. 审查趋势

#### 复制粘贴提示词
```
Use @grafana-dashboards to create PostgreSQL monitoring
```

## 优化检查清单

- [ ] 慢查询已识别
- [ ] 索引已优化
- [ ] 配置已调优
- [ ] 维护已排程
- [ ] 监控已激活
- [ ] 性能已提升

## 质量门禁

- [ ] 查询性能已提升
- [ ] 索引有效
- [ ] 配置已优化
- [ ] 维护已自动化
- [ ] 监控已就位

## 相关工作流包

- `database` - 数据库运维
- `cloud-devops` - 基础设施
- `performance-optimization` - 性能优化

## 限制条件
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家评审的替代品
- 如果缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清
