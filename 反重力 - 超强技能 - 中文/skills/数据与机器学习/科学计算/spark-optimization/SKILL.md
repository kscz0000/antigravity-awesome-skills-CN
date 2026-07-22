---
name: spark-optimization
description: "通过分区策略、缓存、Shuffle 优化和内存调优来优化 Apache Spark 作业。当需要提升 Spark 性能、调试慢作业或扩展数据处理管道时使用。触发词：Spark 优化、Spark 性能、Shuffle 优化、数据倾斜、Spark 调优、spark-optimization、Spark 内存调优"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Apache Spark 优化

优化 Apache Spark 作业的生产级模式，包括分区策略、内存管理、Shuffle 优化和性能调优。

## 不适用场景

- 任务与 Apache Spark 优化无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关的最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 适用场景

- 优化慢速 Spark 作业
- 调优内存和 Executor 配置
- 实现高效的分区策略
- 调试 Spark 性能问题
- 为大规模数据集扩展 Spark 管道
- 减少 Shuffle 和数据倾斜

## 核心概念

### 1. Spark 执行模型

```
Driver Program
    ↓
Job (triggered by action)
    ↓
Stages (separated by shuffles)
    ↓
Tasks (one per partition)
```

### 2. 关键性能因素

| 因素 | 影响 | 解决方案 |
|--------|--------|----------|
| **Shuffle** | 网络 I/O、磁盘 I/O | 最小化宽依赖转换 |
| **数据倾斜** | 任务耗时不均匀 | 加盐、广播 Join |
| **序列化** | CPU 开销 | 使用 Kryo、列式格式 |
| **内存** | GC 压力、溢写 | 调优 Executor 内存 |
| **分区数** | 并行度 | 合理设置分区数 |

## 快速上手

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# 创建优化的 Spark 会话
spark = (SparkSession.builder
    .appName("OptimizedJob")
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
    .config("spark.sql.adaptive.skewJoin.enabled", "true")
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    .config("spark.sql.shuffle.partitions", "200")
    .getOrCreate())

# 使用优化设置读取数据
df = (spark.read
    .format("parquet")
    .option("mergeSchema", "false")
    .load("s3://bucket/data/"))

# 高效转换
result = (df
    .filter(F.col("date") >= "2024-01-01")
    .select("id", "amount", "category")
    .groupBy("category")
    .agg(F.sum("amount").alias("total")))

result.write.mode("overwrite").parquet("s3://bucket/output/")
```

## 模式

### 模式1：最优分区

```python
# 计算最优分区数
def calculate_partitions(data_size_gb: float, partition_size_mb: int = 128) -> int:
    """
    最优分区大小：128MB - 256MB
    太少：资源利用不足，内存压力大
    太多：任务调度开销大
    """
    return max(int(data_size_gb * 1024 / partition_size_mb), 1)

# 重新分区以均匀分布
df_repartitioned = df.repartition(200, "partition_key")

# 合并分区以减少分区数（无 Shuffle）
df_coalesced = df.coalesce(100)

# 利用谓词下推进行分区裁剪
df = (spark.read.parquet("s3://bucket/data/")
    .filter(F.col("date") == "2024-01-01"))  # Spark 会将此过滤下推

# 写入时分区以优化未来查询
(df.write
    .partitionBy("year", "month", "day")
    .mode("overwrite")
    .parquet("s3://bucket/partitioned_output/"))
```

### 模式2：Join 优化

```python
from pyspark.sql import functions as F
from pyspark.sql.types import *

# 1. 广播 Join - 适用于小表关联
# 最佳场景：一侧数据量 < 10MB（可配置）
small_df = spark.read.parquet("s3://bucket/small_table/")  # < 10MB
large_df = spark.read.parquet("s3://bucket/large_table/")  # TB 级

# 显式广播提示
result = large_df.join(
    F.broadcast(small_df),
    on="key",
    how="left"
)

# 2. Sort-Merge Join - 大表默认方式
# 需要 Shuffle，但可处理任意大小
result = large_df1.join(large_df2, on="key", how="inner")

# 3. 桶 Join - 预排序，Join 时无需 Shuffle
# 写入分桶表
(df.write
    .bucketBy(200, "customer_id")
    .sortBy("customer_id")
    .mode("overwrite")
    .saveAsTable("bucketed_orders"))

# Join 分桶表（无 Shuffle！）
orders = spark.table("bucketed_orders")
customers = spark.table("bucketed_customers")  # 相同的桶数
result = orders.join(customers, on="customer_id")

# 4. 倾斜 Join 处理
# 启用 AQE 倾斜 Join 优化
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")

# 严重倾斜时手动加盐
def salt_join(df_skewed, df_other, key_col, num_salts=10):
    """添加盐值以分散倾斜的键"""
    # 在倾斜侧添加盐值
    df_salted = df_skewed.withColumn(
        "salt",
        (F.rand() * num_salts).cast("int")
    ).withColumn(
        "salted_key",
        F.concat(F.col(key_col), F.lit("_"), F.col("salt"))
    )

    # 在另一侧展开所有盐值
    df_exploded = df_other.crossJoin(
        spark.range(num_salts).withColumnRenamed("id", "salt")
    ).withColumn(
        "salted_key",
        F.concat(F.col(key_col), F.lit("_"), F.col("salt"))
    )

    # 使用加盐后的键进行 Join
    return df_salted.join(df_exploded, on="salted_key", how="inner")
```

### 模式3：缓存与持久化

```python
from pyspark import StorageLevel

# 多次复用 DataFrame 时缓存
df = spark.read.parquet("s3://bucket/data/")
df_filtered = df.filter(F.col("status") == "active")

# 缓存到内存（默认 MEMORY_AND_DISK）
df_filtered.cache()

# 或使用指定存储级别
df_filtered.persist(StorageLevel.MEMORY_AND_DISK_SER)

# 强制物化
df_filtered.count()

# 在多个操作中复用
agg1 = df_filtered.groupBy("category").count()
agg2 = df_filtered.groupBy("region").sum("amount")

# 使用完毕后释放缓存
df_filtered.unpersist()

# 存储级别说明：
# MEMORY_ONLY - 最快，但可能放不下
# MEMORY_AND_DISK - 必要时溢写到磁盘（推荐）
# MEMORY_ONLY_SER - 序列化存储，省内存但多耗 CPU
# DISK_ONLY - 内存紧张时使用
# OFF_HEAP - Tungsten 堆外内存

# 复杂血统时使用检查点
spark.sparkContext.setCheckpointDir("s3://bucket/checkpoints/")
df_complex = (df
    .join(other_df, "key")
    .groupBy("category")
    .agg(F.sum("amount")))
df_complex.checkpoint()  # 切断血统并物化
```

### 模式4：内存调优

```python
# Executor 内存配置
# spark-submit --executor-memory 8g --executor-cores 4

# 内存分布（8GB Executor）：
# - spark.memory.fraction = 0.6（60% = 4.8GB 用于执行 + 存储）
#   - spark.memory.storageFraction = 0.5（4.8GB 的 50% = 2.4GB 用于缓存）
#   - 剩余 2.4GB 用于执行（Shuffle、Join、排序）
# - 40% = 3.2GB 用于用户数据结构和内部元数据

spark = (SparkSession.builder
    .config("spark.executor.memory", "8g")
    .config("spark.executor.memoryOverhead", "2g")  # 非 JVM 内存
    .config("spark.memory.fraction", "0.6")
    .config("spark.memory.storageFraction", "0.5")
    .config("spark.sql.shuffle.partitions", "200")
    # 内存密集型操作
    .config("spark.sql.autoBroadcastJoinThreshold", "50MB")
    # 防止大规模 Shuffle 时 OOM
    .config("spark.sql.files.maxPartitionBytes", "128MB")
    .getOrCreate())

# 监控内存使用
def print_memory_usage(spark):
    """打印当前内存使用情况"""
    sc = spark.sparkContext
    for executor in sc._jsc.sc().getExecutorMemoryStatus().keySet().toArray():
        mem_status = sc._jsc.sc().getExecutorMemoryStatus().get(executor)
        total = mem_status._1() / (1024**3)
        free = mem_status._2() / (1024**3)
        print(f"{executor}: {total:.2f}GB total, {free:.2f}GB free")
```

### 模式5：Shuffle 优化

```python
# 减少 Shuffle 数据量
spark.conf.set("spark.sql.shuffle.partitions", "auto")  # 配合 AQE
spark.conf.set("spark.shuffle.compress", "true")
spark.conf.set("spark.shuffle.spill.compress", "true")

# Shuffle 前预聚合
df_optimized = (df
    # 先局部聚合（Combiner）
    .groupBy("key", "partition_col")
    .agg(F.sum("value").alias("partial_sum"))
    # 再全局聚合
    .groupBy("key")
    .agg(F.sum("partial_sum").alias("total")))

# 使用 Map 端操作避免 Shuffle
# 差：每次 distinct 都触发 Shuffle
distinct_count = df.select("category").distinct().count()

# 好：近似 distinct（无 Shuffle）
approx_count = df.select(F.approx_count_distinct("category")).collect()[0][0]

# 减少分区时使用 coalesce 代替 repartition
df_reduced = df.coalesce(10)  # 无 Shuffle

# 使用压缩优化 Shuffle
spark.conf.set("spark.io.compression.codec", "lz4")  # 快速压缩
```

### 模式6：数据格式优化

```python
# Parquet 优化
(df.write
    .option("compression", "snappy")  # 快速压缩
    .option("parquet.block.size", 128 * 1024 * 1024)  # 128MB 行组
    .parquet("s3://bucket/output/"))

# 列裁剪 - 只读取需要的列
df = (spark.read.parquet("s3://bucket/data/")
    .select("id", "amount", "date"))  # Spark 只读取这些列

# 谓词下推 - 在存储层过滤
df = (spark.read.parquet("s3://bucket/partitioned/year=2024/")
    .filter(F.col("status") == "active"))  # 下推到 Parquet 读取器

# Delta Lake 优化
(df.write
    .format("delta")
    .option("optimizeWrite", "true")  # Bin-packing
    .option("autoCompact", "true")  # 合并小文件
    .mode("overwrite")
    .save("s3://bucket/delta_table/"))

# Z-Order 排序优化多维查询
spark.sql("""
    OPTIMIZE delta.`s3://bucket/delta_table/`
    ZORDER BY (customer_id, date)
""")
```

### 模式7：监控与调试

```python
# 启用详细指标
spark.conf.set("spark.sql.codegen.wholeStage", "true")
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

# 查看执行计划
df.explain(mode="extended")
# 模式：simple、extended、codegen、cost、formatted

# 获取物理计划统计信息
df.explain(mode="cost")

# 监控任务指标
def analyze_stage_metrics(spark):
    """分析最近的 Stage 指标"""
    status_tracker = spark.sparkContext.statusTracker()

    for stage_id in status_tracker.getActiveStageIds():
        stage_info = status_tracker.getStageInfo(stage_id)
        print(f"Stage {stage_id}:")
        print(f"  Tasks: {stage_info.numTasks}")
        print(f"  Completed: {stage_info.numCompletedTasks}")
        print(f"  Failed: {stage_info.numFailedTasks}")

# 识别数据倾斜
def check_partition_skew(df):
    """检查分区倾斜"""
    partition_counts = (df
        .withColumn("partition_id", F.spark_partition_id())
        .groupBy("partition_id")
        .count()
        .orderBy(F.desc("count")))

    partition_counts.show(20)

    stats = partition_counts.select(
        F.min("count").alias("min"),
        F.max("count").alias("max"),
        F.avg("count").alias("avg"),
        F.stddev("count").alias("stddev")
    ).collect()[0]

    skew_ratio = stats["max"] / stats["avg"]
    print(f"Skew ratio: {skew_ratio:.2f}x (>2x indicates skew)")
```

## 配置速查表

```python
# 生产配置模板
spark_configs = {
    # 自适应查询执行（AQE）
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",

    # 内存
    "spark.executor.memory": "8g",
    "spark.executor.memoryOverhead": "2g",
    "spark.memory.fraction": "0.6",
    "spark.memory.storageFraction": "0.5",

    # 并行度
    "spark.sql.shuffle.partitions": "200",
    "spark.default.parallelism": "200",

    # 序列化
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
    "spark.sql.execution.arrow.pyspark.enabled": "true",

    # 压缩
    "spark.io.compression.codec": "lz4",
    "spark.shuffle.compress": "true",

    # 广播
    "spark.sql.autoBroadcastJoinThreshold": "50MB",

    # 文件处理
    "spark.sql.files.maxPartitionBytes": "128MB",
    "spark.sql.files.openCostInBytes": "4MB",
}
```

## 最佳实践

### 应该做的
- **启用 AQE** — 自适应查询执行能处理许多问题
- **使用 Parquet/Delta** — 带压缩的列式格式
- **广播小表** — 小表关联时避免 Shuffle
- **监控 Spark UI** — 检查倾斜、溢写、GC
- **合理设置分区数** — 每个分区 128MB - 256MB

### 不应该做的
- **不要 collect 大数据集** — 保持数据分布式
- **不要滥用 UDF** — 优先使用内置函数
- **不要过度缓存** — 内存是有限的
- **不要忽视数据倾斜** — 它会主导作业耗时
- **不要用 `.count()` 判断是否存在** — 使用 `.take(1)` 或 `.isEmpty()`

## 参考资料

- [Spark 性能调优](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
- [Spark 配置](https://spark.apache.org/docs/latest/configuration.html)
- [Databricks 优化指南](https://docs.databricks.com/en/optimizations/index.html)

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
