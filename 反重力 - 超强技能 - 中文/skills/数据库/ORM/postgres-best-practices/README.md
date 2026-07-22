# Postgres 最佳实践 - 贡献者指南

本仓库包含针对 AI 智能体和 LLM 优化的 Postgres 性能优化规则。

## 快速开始

```bash
# 安装依赖
cd packages/postgres-best-practices-build
npm install

# 验证现有规则
npm run validate

# 构建 AGENTS.md
npm run build
```

## 创建新规则

1. **选择分类前缀**：
   - `query-` 查询性能（CRITICAL）
   - `conn-` 连接管理（CRITICAL）
   - `security-` 安全与 RLS（CRITICAL）
   - `schema-` Schema 设计（HIGH）
   - `lock-` 并发与锁（MEDIUM-HIGH）
   - `data-` 数据访问模式（MEDIUM）
   - `monitor-` 监控与诊断（LOW-MEDIUM）
   - `advanced-` 高级特性（LOW）

2. **复制模板**：
   ```bash
   cp rules/_template.md rules/query-your-rule-name.md
   ```

3. **按模板结构填写内容**

4. **验证并构建**：
   ```bash
   npm run validate
   npm run build
   ```

5. **检查**生成的 `AGENTS.md`

## 仓库结构

```
skills/postgres-best-practices/
├── SKILL.md           # 智能体技能清单
├── AGENTS.md          # [自动生成] 编译后的规则文档
├── README.md          # 本文件
├── metadata.json      # 版本和元数据
└── rules/
    ├── _template.md      # 规则模板
    ├── _sections.md      # 分类定义
    ├── _contributing.md  # 编写指南
    └── *.md              # 各规则文件

packages/postgres-best-practices-build/
├── src/               # 构建系统源码
├── package.json       # NPM 脚本
└── test-cases.json    # [自动生成] 测试产物
```

## 规则文件结构

完整模板参见 `rules/_template.md`。关键要素：

````markdown
---
title: 清晰、面向操作的标题
impact: CRITICAL|HIGH|MEDIUM-HIGH|MEDIUM|LOW-MEDIUM|LOW
impactDescription: 量化收益（如"快 10-100 倍"）
tags: 相关, 关键词
---

## [标题]

[1-2 句说明]

**错误（描述问题）：**

```sql
-- 说明哪里有问题的注释
[错误的 SQL 示例]
```
````

**正确（描述方案）：**

```sql
-- 说明为什么这样更好的注释
[正确的 SQL 示例]
```

```
## 编写指南

详细指南参见 `rules/_contributing.md`。核心原则：

1. **展示具体转换** — "把 X 改成 Y"，而非抽象建议
2. **错误优先结构** — 先展示问题，再给出方案
3. **量化影响** — 包含具体指标（快 10 倍、小 50%）
4. **示例自包含** — 完整、可运行的 SQL
5. **语义化命名** — 使用有意义的名称（users、email），而非（table1、col1）

## 影响等级

| 等级 | 改善幅度 | 示例 |
|------|---------|------|
| CRITICAL | 10-100x | 缺失索引、连接耗尽 |
| HIGH | 5-20x | 索引类型错误、分区不当 |
| MEDIUM-HIGH | 2-5x | N+1 查询、RLS 优化 |
| MEDIUM | 1.5-3x | 冗余索引、统计信息过期 |
| LOW-MEDIUM | 1.2-2x | VACUUM 调优、配置调整 |
| LOW | 增量改善 | 高级模式、边界情况 |
```
