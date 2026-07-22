---
name: polars
description: 快速内存 DataFrame 库，适用于可装入 RAM 的数据集。当 pandas 太慢但数据仍能放入内存时使用。支持惰性求值、并行执行、Apache Arrow 后端。最适合 1-100GB 数据集、ETL 管道、pandas 加速替代。对于超出内存的数据请使用 dask 或 vaex。触发词：Polars、DataFrame、数据处理、pandas替代、ETL管道、惰性求值、并行计算、Apache Arrow、数据转换、列式存储。
license: https://github.com/pola-rs/polars/blob/main/LICENSE
metadata:
    skill-author: K-Dense Inc.
    risk: unknown
    source: community
---

# Polars

## 适用场景

- 需要比 pandas 更快的内存 DataFrame 工作流，且数据仍能放入 RAM。
- 正在构建受益于惰性求值和并行执行的 ETL、分析或转换管道。
- 需要基于 Apache Arrow 语义的表达式化表格操作。

## 概述

Polars 是一个基于 Apache Arrow 构建的极速 DataFrame 库，支持 Python 和 Rust。使用 Polars 的表达式化 API、惰性求值框架和高性能数据操作能力，实现高效数据处理、pandas 迁移和数据管道优化。

## 快速入门

### 安装与基本使用

安装 Polars：
```python
uv pip install polars
```

基本 DataFrame 创建和操作：
```python
import polars as pl

# 创建 DataFrame
df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NY", "LA", "SF"]
})

# 选择列
df.select("name", "age")

# 过滤行
df.filter(pl.col("age") > 25)

# 添加计算列
df.with_columns(
    age_plus_10=pl.col("age") + 10
)
```

## 核心概念

### 表达式

表达式是 Polars 操作的基础构建块。它们描述对数据的转换，可以组合、复用和优化。

**核心原则：**
- 使用 `pl.col("column_name")` 引用列
- 链式方法构建复杂转换
- 表达式是惰性的，仅在上下文（select、with_columns、filter、group_by）中执行

**示例：**
```python
# 基于表达式的计算
df.select(
    pl.col("name"),
    (pl.col("age") * 12).alias("age_in_months")
)
```

### 惰性求值 vs 立即求值

**立即求值（DataFrame）：** 操作立即执行
```python
df = pl.read_csv("file.csv")  # 立即读取
result = df.filter(pl.col("age") > 25)  # 立即执行
```

**惰性求值（LazyFrame）：** 操作构建查询计划，执行前优化
```python
lf = pl.scan_csv("file.csv")  # 尚未读取
result = lf.filter(pl.col("age") > 25).select("name", "age")
df = result.collect()  # 现在执行优化后的查询
```

**何时使用惰性求值：**
- 处理大型数据集
- 复杂查询管道
- 只需要部分列/行
- 性能至关重要

**惰性求值的优势：**
- 自动查询优化
- 谓词下推
- 投影下推
- 并行执行

如需详细了解概念，加载 `references/core_concepts.md`。

## 常用操作

### 选择列（Select）
选择和操作列：
```python
# 选择特定列
df.select("name", "age")

# 使用表达式选择
df.select(
    pl.col("name"),
    (pl.col("age") * 2).alias("double_age")
)

# 选择匹配模式的所有列
df.select(pl.col("^.*_id$"))
```

### 过滤行（Filter）
按条件过滤行：
```python
# 单条件
df.filter(pl.col("age") > 25)

# 多条件（比使用 & 更清晰）
df.filter(
    pl.col("age") > 25,
    pl.col("city") == "NY"
)

# 复杂条件
df.filter(
    (pl.col("age") > 25) | (pl.col("city") == "LA")
)
```

### 添加列（With Columns）
添加或修改列，同时保留现有列：
```python
# 添加新列
df.with_columns(
    age_plus_10=pl.col("age") + 10,
    name_upper=pl.col("name").str.to_uppercase()
)

# 并行计算（所有列并行计算）
df.with_columns(
    pl.col("value") * 10,
    pl.col("value") * 100,
)
```

### 分组聚合（Group By and Aggregations）
分组数据并计算聚合：
```python
# 基本分组
df.group_by("city").agg(
    pl.col("age").mean().alias("avg_age"),
    pl.len().alias("count")
)

# 多个分组键
df.group_by("city", "department").agg(
    pl.col("salary").sum()
)

# 条件聚合
df.group_by("city").agg(
    (pl.col("age") > 30).sum().alias("over_30")
)
```

如需详细了解操作模式，加载 `references/operations.md`。

## 聚合与窗口函数

### 聚合函数
`group_by` 上下文中的常用聚合：
- `pl.len()` - 计数行数
- `pl.col("x").sum()` - 求和
- `pl.col("x").mean()` - 平均值
- `pl.col("x").min()` / `pl.col("x").max()` - 极值
- `pl.first()` / `pl.last()` - 首值/末值

### 使用 `over()` 的窗口函数
在保留行数的同时应用聚合：
```python
# 为每行添加分组统计
df.with_columns(
    avg_age_by_city=pl.col("age").mean().over("city"),
    rank_in_city=pl.col("salary").rank().over("city")
)

# 多个分组列
df.with_columns(
    group_avg=pl.col("value").mean().over("category", "region")
)
```

**映射策略：**
- `group_to_rows`（默认）：保留原始行顺序
- `explode`：更快但会将行分组在一起
- `join`：创建列表列

## 数据 I/O

### 支持的格式
Polars 支持读写：
- CSV、Parquet、JSON、Excel
- 数据库（通过连接器）
- 云存储（S3、Azure、GCS）
- Google BigQuery
- 多文件/分区文件

### 常用 I/O 操作

**CSV：**
```python
# 立即求值
df = pl.read_csv("file.csv")
df.write_csv("output.csv")

# 惰性求值（大文件推荐）
lf = pl.scan_csv("file.csv")
result = lf.filter(...).select(...).collect()
```

**Parquet（性能推荐）：**
```python
df = pl.read_parquet("file.parquet")
df.write_parquet("output.parquet")
```

**JSON：**
```python
df = pl.read_json("file.json")
df.write_json("output.json")
```

如需完整的 I/O 文档，加载 `references/io_guide.md`。

## 数据转换

### 连接（Joins）
合并 DataFrame：
```python
# 内连接
df1.join(df2, on="id", how="inner")

# 左连接
df1.join(df2, on="id", how="left")

# 不同列名连接
df1.join(df2, left_on="user_id", right_on="id")
```

### 拼接（Concatenation）
堆叠 DataFrame：
```python
# 垂直拼接（堆叠行）
pl.concat([df1, df2], how="vertical")

# 水平拼接（添加列）
pl.concat([df1, df2], how="horizontal")

# 对角拼接（不同 schema 的并集）
pl.concat([df1, df2], how="diagonal")
```

### 透视与逆透视（Pivot and Unpivot）
重塑数据：
```python
# 透视（宽格式）
df.pivot(values="sales", index="date", columns="product")

# 逆透视（长格式）
df.unpivot(index="id", on=["col1", "col2"])
```

如需详细的转换示例，加载 `references/transformations.md`。

## 从 Pandas 迁移

Polars 提供了比 pandas 显著的性能提升和更简洁的 API。主要区别：

### 概念差异
- **无索引**：Polars 仅使用整数位置
- **严格类型**：无静默类型转换
- **惰性求值**：通过 LazyFrame 实现
- **默认并行**：操作自动并行化

### 常用操作对照

| 操作 | Pandas | Polars |
|------|--------|--------|
| 选择列 | `df["col"]` | `df.select("col")` |
| 过滤 | `df[df["col"] > 10]` | `df.filter(pl.col("col") > 10)` |
| 添加列 | `df.assign(x=...)` | `df.with_columns(x=...)` |
| 分组 | `df.groupby("col").agg(...)` | `df.group_by("col").agg(...)` |
| 窗口 | `df.groupby("col").transform(...)` | `df.with_columns(...).over("col")` |

### 关键语法模式

**Pandas 顺序执行（慢）：**
```python
df.assign(
    col_a=lambda df_: df_.value * 10,
    col_b=lambda df_: df_.value * 100
)
```

**Polars 并行执行（快）：**
```python
df.with_columns(
    col_a=pl.col("value") * 10,
    col_b=pl.col("value") * 100,
)
```

如需完整的迁移指南，加载 `references/pandas_migration.md`。

## 最佳实践

### 性能优化

1. **对大型数据集使用惰性求值：**
   ```python
   lf = pl.scan_csv("large.csv")  # 不要使用 read_csv
   result = lf.filter(...).select(...).collect()
   ```

2. **避免在热路径中使用 Python 函数：**
   - 保持在表达式 API 内以实现并行化
   - 仅在必要时使用 `.map_elements()`
   - 优先使用 Polars 原生操作

3. **对超大数据使用流式处理：**
   ```python
   lf.collect(streaming=True)
   ```

4. **尽早选择所需列：**
   ```python
   # 好：尽早选择列
   lf.select("col1", "col2").filter(...)

   # 差：先过滤所有列
   lf.filter(...).select("col1", "col2")
   ```

5. **使用适当的数据类型：**
   - 低基数字符串使用 Categorical
   - 适当的整数大小（i32 vs i64）
   - 时间数据使用日期类型

### 表达式模式

**条件操作：**
```python
pl.when(condition).then(value).otherwise(other_value)
```

**跨多列的列操作：**
```python
df.select(pl.col("^.*_value$") * 2)  # 正则模式
```

**空值处理：**
```python
pl.col("x").fill_null(0)
pl.col("x").is_null()
pl.col("x").drop_nulls()
```

如需更多最佳实践和模式，加载 `references/best_practices.md`。

## 资源

本技能包含完整的参考文档：

### references/
- `core_concepts.md` - 表达式、惰性求值和类型系统的详细说明
- `operations.md` - 所有常用操作的综合指南及示例
- `pandas_migration.md` - 从 pandas 迁移到 Polars 的完整指南
- `io_guide.md` - 所有支持格式的数据 I/O 操作
- `transformations.md` - 连接、拼接、透视和重塑操作
- `best_practices.md` - 性能优化技巧和常用模式

当用户需要特定主题的详细信息时，按需加载这些参考文档。

## 限制

- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
