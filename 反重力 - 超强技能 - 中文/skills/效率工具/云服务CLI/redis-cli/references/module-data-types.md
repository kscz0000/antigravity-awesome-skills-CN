# 模块数据类型

Redis 模块数据类型命令集合，涵盖 JSON 文档、Vector Sets 向量集合、概率数据结构（BLOOM/CUCKOO/TOPK/CMS/TDIGEST）、TimeSeries 时序数据库，以及全文搜索模块 RediSearch。这些模块在 Redis 原生类型之上提供更专业的数据建模能力。

## 目录

- [JSON（RedisJSON 模块）](#jsonredisjson-模块)
- [Vector Sets（向量集合，Redis 8.0+）](#vector-setsredis-80)
- [Bloom Filter（布隆过滤器）](#bloom-filter)
- [Cuckoo Filter（杜鹃过滤器）](#cuckoo-filter)
- [Top-K（Top-K 频繁项）](#top-k)
- [Count-Min Sketch（计数最小草图）](#count-min-sketch)
- [T-Digest（T-Digest 分位数）](#t-digest)
- [TimeSeries（时间序列）](#timeseries)
- [全文搜索（RediSearch）](#全文搜索redisearch)

## JSON（RedisJSON 模块，Redis 原生 JSON 类型支持）

```
JSON.SET key $ value [NX|XX]           # Set JSON value at path
JSON.GET key [path [path ...]]         # Get JSON value
JSON.MGET key [key ...] $              # Multi-get
JSON.DEL key [path]                    # Delete JSON value
JSON.TYPE key [path]                   # Get type at path
JSON.STRLEN key [path]                 # String length
JSON.OBJLEN key [path]                 # Object key count
JSON.OBJKEYS key [path]                # Object keys
JSON.ARRLEN key [path]                 # Array length
JSON.ARRAPPEND key path value [...]    # Append to array
JSON.ARRPOP key [path [index]]         # Pop from array
JSON.ARRINSERT key path index value [...]  # Insert into array
JSON.ARRINDEX key path value [start [stop]]  # Find index of value
JSON.ARRTRIM key path start stop       # Trim array to range
JSON.NUMINCRBY key path value          # Increment number
JSON.NUMMULTBY key path value          # Multiply number
JSON.STRAPPEND key [path] value        # Append to string
JSON.STRLEN key [path]                 # String length
JSON.CLEAR key [path]                  # Clear container (array/object)
JSON.FORGET key [path]                 # Alias for JSON.DEL
JSON.MSET key path value [key path value ...]  # Multi-set
JSON.TOGGLE key [path]                 # Toggle boolean value
JSON.MERGE key path value              # Merge JSON
JSON.RESP key [path]                   # Get as RESP protocol
```

## Vector Sets（Redis 8.0+）

Vector sets 存储带关联向量的元素，并使用 HNSW（分层可导航小世界）图支持近似最近邻（ANN）相似性搜索。适用于语义搜索、推荐系统和 AI 嵌入存储。

```
# Write
VADD key [REDUCE dim] (FP32 | VALUES num) vector element [CAS] [NOQUANT|Q8|BIN] [EF ef] [SETATTR json] [M numlinks]
                                        # Add element with vector              O(log(N))

VREM key element                       # Remove element                        O(log(N))

# Similarity search
VSIM key (ELE | FP32 | VALUES num) (vector | element) [WITHSCORES] [WITHATTRIBS] [COUNT n]
        [EPSILON delta] [EF ef] [FILTER expr] [FILTER-EF max] [TRUTH] [NOTHREAD]
                                        # Find similar elements                 O(log(N))

# Read
VEMB key element [RAW]                 # Get vector for element                O(1)
VRANGE key start end [count]           # Lexicographic range iteration         O(log(K)+M)
VCARD key                              # Element count                         O(1)
VDIM key                               # Vector dimensionality                 O(1)
VISMEMBER key element                  # Check element exists                  O(1)
VLINKS key element [WITHSCORES]        # HNSW graph neighbors                  O(1)
VRANDMEMBER key [count]                # Random element(s)                     O(N)
VSETATTR key element "{ json }"        # Set JSON attributes                   O(1)
VGETATTR key element                   # Get JSON attributes                   O(1)
VINFO key                              # Vector set metadata                   O(1)
```

**VADD 向量输入：**
- `VALUES 3 0.1 1.2 0.5 my-element` — 字符串浮点数，平台无关
- `FP32 <blob> my-element` — 二进制 32 位浮点 blob，必须为小端序

**VADD 量化选项**（互斥，在首次 VADD 时设置）：
- `NOQUANT` — 不量化，全精度（内存最多）
- `Q8` — 有符号 8 位整数量化（默认，平衡性好）
- `BIN` — 二值量化（最快，内存最少，召回率较低）

**VSIM 输入模式：**
- `ELE element` — 按集合中已有元素搜索
- `VALUES num v1 v2 ...` — 按浮点向量搜索
- `FP32 <blob>` — 按二进制向量搜索

**VSIM 关键选项：**
- `WITHSCORES` — 包含相似度分数（1 = 完全相同，0 = 完全相反）
- `WITHATTRIBS` — 包含每个结果的 JSON 属性
- `COUNT n` — 限制结果数（默认 10）
- `EPSILON delta` — 仅返回距离 < delta 的元素（相似度 > 1-delta）
- `EF ef` — 搜索探索因子（越高 = 召回率越好，越慢）
- `FILTER expr` — 按属性表达式过滤（如 `".year > 2020"`）
- `TRUTH` — 精确线性扫描 O(N)，用于基准测试召回质量

**VRANGE 迭代**（Redis 8.4+）：
无状态字典序迭代。`start`/`end` 使用 `[` 包含，`(` 排除，`-` 最小值，`+` 最大值：
```
VRANGE mykey - + 10        # First 10 elements
VRANGE mykey (last + 10    # Next 10 after "last"
VRANGE mykey - + -1        # All elements (caution: may be slow)
```

## Bloom Filter

用于成员测试的概率数据结构。返回"可能在集合中"或"肯定不在集合中"。空间高效，可配置误报率。

```
# Create with custom parameters (optional — auto-created on first ADD)
BF.RESERVE key error_rate capacity [EXPANSION expansion] [NONSCALING]

# Write
BF.ADD key item                        # Add single item                 O(k)
BF.MADD key item [item ...]            # Add multiple items              O(k*n)

# Query
BF.EXISTS key item                     # Check if item exists            O(k)
BF.MEXISTS key item [item ...]         # Check multiple items            O(k*n)

# Info
BF.INFO key                            # Filter metadata (capacity, size, expansion, etc.)

# Persistence
BF.SCANDUMP key iter                   # Incremental dump (iter 0 = start)
BF.LOADCHUNK key iter data             # Incremental restore
```

**行为说明：**
- `BF.ADD` 返回 1 表示项被添加（新的），0 表示可能已存在（EXISTS 的误报不代表它被添加了）
- Bloom filter 可能产生误报但不会产生漏报
- `BF.RESERVE` 允许预先控制误报率和容量；不使用则采用默认值
- 使用 `BF.SCANDUMP`/`BF.LOADCHUNK` 对大型过滤器进行增量备份/恢复

## Cuckoo Filter

Bloom filter 的替代方案，额外支持删除项和计数。支持"肯定在集合中"或"可能不在集合中"语义。

```
# Create (optional — auto-created on first ADD)
CF.RESERVE key capacity [BUCKETSIZE bucketsize] [MAXITERATIONS maxiterations] [EXPANSION expansion]

# Write
CF.ADD key item                        # Add item                        O(k+i)
CF.ADDNX key item                      # Add only if not exists          O(k+i)

# Delete
CF.DEL key item                        # Delete item                     O(k+i)

# Query
CF.EXISTS key item                     # Check if item exists            O(k+i)
CF.MEXISTS key item [item ...]         # Check multiple items            O(k*n)

# Count
CF.COUNT key item                      # Count occurrences               O(k+i)

# Info
CF.INFO key                            # Filter metadata

# Persistence
CF.SCANDUMP key iter                   # Incremental dump
CF.LOADCHUNK key iter data             # Incremental restore
```

**行为说明：**
- 与 Bloom filter 不同，Cuckoo filter 支持删除（`CF.DEL`）
- Cuckoo filter 可以包含同一项多次
- `CF.ADD` 总是成功（允许重复）；使用 `CF.ADDNX` 进行唯一插入
- `CF.COUNT` 返回项被添加的次数（受误报影响）

## Top-K

跟踪数据流中最频繁的 K 个元素。适用于热点检测和趋势项。

```
# Create (required before use)
TOPK.RESERVE key topk [width depth decay]

# Write
TOPK.ADD key item [item ...]           # Add items, returns expelled items if any   O(n*k)

# Query
TOPK.QUERY key item [item ...]         # Check if items are in top-K                O(n)
TOPK.COUNT key item [item ...]         # Get estimated counts                       O(n)
TOPK.LIST key                          # Return full top-K list                     O(k)
TOPK.INCRBY key item count [item count ...]  # Increment item counts              O(n*k)

# Info
TOPK.INFO key                          # Sketch metadata (k, width, depth, decay)
```

**行为说明：**
- `TOPK.RESERVE` 参数：`topk` = 跟踪的顶部元素数，`width`/`depth` = 草图维度，`decay` = 概率衰减
- `TOPK.ADD` 对每个进入 top-K 的添加返回被淘汰的元素，或 nil
- 结果是近似的 — top-K 列表中的项不保证是实际 top-K

## Count-Min Sketch（计数最小草图，频率估算）

估算数据流中项的频率，精度可配置。适用于计数出现次数而无需存储每个项。

```
# Create (required before use, two methods)
CMS.INITBYDIM key width depth          # Create by explicit dimensions
CMS.INITBYPROB key error_rate probability  # Create by error/probability targets

# Write
CMS.INCRBY key item increment [item increment ...]  # Increment counts   O(n)

# Query
CMS.QUERY key item [item ...]          # Get estimated counts            O(n)

# Info
CMS.INFO key                           # Sketch metadata (width, depth, total)

# Merge
CMS.MERGE destkey numkeys key [key ...] [WEIGHTS weight [weight ...]]  # Merge sketches
```

**行为说明：**
- `CMS.INITBYPROB` 更推荐 — 指定期望的 `error_rate`（精度）和 `probability`（置信度）
- `CMS.QUERY` 返回高估值（不会低估）— 计数包含哈希冲突的误报
- `CMS.MERGE` 合并多个草图；适用于聚合分布式计数器

## T-Digest

估算数据流中的分位数（百分位数）。适用于延迟百分位数、值分布和直方图分析。

```
# Create (required before use)
TDIGEST.CREATE key [COMPRESSION compression]

# Write
TDIGEST.ADD key value [value ...]      # Add observations                O(N)

# Quantile queries
TDIGEST.QUANTILE key quantile [quantile ...]   # Value at quantile(s)    O(log(N))
TDIGEST.CDF key value [value ...]              # CDF: P(X <= value)      O(log(N))

# Rank queries
TDIGEST.RANK key value [value ...]             # Approximate rank        O(log(N))
TDIGEST.REVRANK key value [value ...]          # Reverse rank            O(log(N))
TDIGEST.BYRANK key rank [rank ...]             # Value at rank           O(log(N))
TDIGEST.BYREVRANK key rank [rank ...]          # Value at reverse rank   O(log(N))

# Statistics
TDIGEST.MIN key                        # Minimum value                   O(1)
TDIGEST.MAX key                        # Maximum value                   O(1)
TDIGEST.TRIMMED_MEAN key low high      # Mean of values between quantiles  O(N)

# Management
TDIGEST.INFO key                       # Sketch metadata (capacity, merged/unmerged nodes, total weight)
TDIGEST.MERGE destkey numkeys key [key ...]  # Merge sketches           O(N)
TDIGEST.RESET key                      # Reset to empty                  O(1)
```

**行为说明：**
- `COMPRESSION` 控制精度与内存的权衡（默认：100，越高越精确）
- `TDIGEST.QUANTILE 0.5` 返回近似中位数
- `TDIGEST.CDF` 返回小于等于给定值的观测比例
- `TDIGEST.MERGE` 后，目标草图提供合并数据的分位数估算

## TimeSeries

存储和查询时序数据（传感器读数、指标、金融数据）。时间戳为 64 位整数毫秒。支持聚合、压缩规则和基于标签的过滤。

```
# Create
TS.CREATE key [RETENTION ms] [ENCODING COMPRESSED|UNCOMPRESSED] [CHUNK_SIZE bytes]
            [DUPLICATE_POLICY BLOCK|FIRST|LAST|MIN|MAX|SUM]
            [IGNORE maxTimeDiff maxValDiff]
            [LABELS label value ...]                              # O(1)

# Write
TS.ADD key timestamp value [RETENTION ms] [ON_DUPLICATE policy]  # O(1), creates series if missing
       [LABELS label value ...]
       # timestamp: Unix ms, or * for server time
TS.MADD key timestamp value [key timestamp value ...]             # O(N), batch add
TS.INCRBY key value [TIMESTAMP ts] [RETENTION ms] [LABELS ...]   # O(1), counter/gauge
TS.DECRBY key value [TIMESTAMP ts] [RETENTION ms] [LABELS ...]   # O(1), decrement

# Single-series query
TS.GET key [LATEST]                                               # Latest sample           O(1)
TS.RANGE key from to [LATEST] [FILTER_BY_TS ts...]               # Range query             O(n/m+k)
          [FILTER_BY_VALUE min max] [COUNT n]
          [ALIGN align] [AGGREGATION fn bucketDuration]
          [BUCKETTIMESTAMP bt] [EMPTY]
TS.REVRANGE key from to [...]                                     # Same, descending order

# Multi-series query (filter by labels)
TS.MGET [LATEST] [WITHLABELS | SELECTED_LABELS lbl...]            # Latest from each series O(N)
        FILTER label=value [...]
TS.MRANGE from to [LATEST] [FILTER_BY_TS ts...]                  # Range across series     O(n/m+k)
          [FILTER_BY_VALUE min max] [WITHLABELS | SELECTED_LABELS lbl...]
          [COUNT n] [ALIGN align] [AGGREGATION fn bucketDuration]
          FILTER label=value [...] [GROUPBY label REDUCE reducer]
TS.MREVRANGE from to [...]                                        # Same, descending order

# Index
TS.QUERYINDEX filterExpr...                                       # List keys by labels     O(N)

# Compaction rules
TS.CREATERULE source dest AGGREGATION fn bucketDuration            # O(1), dest must exist
TS.DELETERULE source dest                                         # O(1)

# Management
TS.ALTER key [RETENTION ms] [LABELS label value ...]              # O(1)
TS.INFO key                                                       # Series metadata         O(1)
TS.DEL key from to                                                # Delete range            O(N)
```

**聚合函数：** `AVG`、`SUM`、`MIN`、`MAX`、`RANGE`、`COUNT`、`FIRST`、`LAST`、`STD.P`、`STD.S`、`VAR.P`、`VAR.S`、`TWA`（时间加权平均）、`countNaN`、`countAll`（Redis 8.6+）

**时间戳：** 范围查询中使用 `-` 表示最早，`+` 表示最新。

**标签过滤语法：** `label=value`（精确匹配）、`label!=(value1,value2)`（排除）、`label=(v1,v2)`（OR）、`label=`（存在性）。过滤器为合取（AND）关系。

**DUPLICATE_POLICY**（在 TS.CREATE 上）：如何处理重复时间戳：
- `BLOCK` — 拒绝重复（默认）
- `FIRST` — 保留第一个值
- `LAST` — 保留最新值
- `MIN` / `MAX` / `SUM` — 聚合

**压缩：** `TS.CREATERULE` 在数据到达时自动计算聚合。仅处理规则创建之后添加的数据。目标键必须已存在。

## 全文搜索（RediSearch，二级索引与全文检索模块）

对 Redis Hash 和 JSON 文档的全文搜索、二级索引和聚合。

```
# Index management
FT.CREATE index [ON HASH|JSON] [PREFIX count prefix...]
  [FILTER filter] [LANGUAGE lang] [TEMPORARY seconds]
  [NOOFFSETS] [NOHL] [NOFIELDS] [NOFREQS]
  [STOPWORDS count word...]
  [SKIPINITIALSCAN]
  SCHEMA field [AS alias] TEXT|TAG|NUMERIC|GEO|VECTOR|GEOSHAPE
               [SORTABLE [UNF]] [NOINDEX] [...]                # O(K) create, O(N) scan

FT.ALTER index [SKIPINITIALSCAN] SCHEMA ADD field ...           # Add fields             O(N)
FT.INFO index                                                   # Index stats            O(1)
FT.DROPINDEX index [DD]                                         # Drop index (DD=del docs) O(1)/O(N)

# Aliases
FT.ALIASADD alias index                                         # Create alias           O(1)
FT.ALIASDEL alias                                               # Remove alias           O(1)
FT.ALIASUPDATE alias index                                      # Point alias to index   O(1)

# Search
FT.SEARCH index query [NOCONTENT] [VERBATIM] [WITHSCORES]       # O(N) for single-word
  [FILTER field min max ...] [GEOFILTER field lon lat radius unit]
  [RETURN count field [AS name] ...]
  [SUMMARIZE [FIELDS count field...] [FRAGS n] [LEN n] [SEPARATOR s]]
  [HIGHLIGHT [FIELDS count field...] [TAGS open close]]
  [SLOP slop] [INORDER] [LANGUAGE lang] [EXPANDER exp]
  [SCORER scorer] [EXPLAINSCORE] [PAYLOAD payload]
  [SORTBY field [ASC|DESC]] [LIMIT offset count]
  [PARAMS nargs name value ...] [DIALECT dialect]
  [TIMEOUT ms]

# Aggregation pipeline
FT.AGGREGATE index query [VERBATIM]                             # Non-deterministic
  [LOAD count field ...] [TIMEOUT ms]
  [GROUPBY nargs prop... [REDUCE fn nargs arg... [AS name]]...]
  [SORTBY nargs prop [ASC|DESC]... [MAX n]]
  [APPLY expression AS name]...
  [LIMIT offset count] [FILTER filter]
  [WITHCURSOR [COUNT n] [MAXIDLE ms]]
  [PARAMS nargs name value ...] [DIALECT dialect]

# Dictionary
FT.DICTADD dict word [word ...]                                 # Add words              O(1)
FT.DICTDEL dict word [word ...]                                 # Remove words           O(1)
FT.DICTDUMP dict                                                # List words             O(N)

# Synonyms
FT.SYNUPDATE index groupid [SKIPINITIALSCAN] term [term ...]    # O(1)
FT.SYNDUMP index                                                # O(N)

# Suggestions
FT.SUGADD key string score [INCR] [PAYLOAD payload]             # O(1)
FT.SUGGET key prefix [FUZZY] [WITHSCORES] [WITHPAYLOADS]        # O(n)
      [MAX num] [DIALECT dialect]
FT.SUGDEL key string                                            # O(1)
FT.SUGLEN key                                                   # O(1)

# Other
FT._LIST                                                        # List all indexes       O(N)
FT.TAGVALS index field                                          # Distinct tag values    O(N)
FT.PROFILE index query [LIMITED] [DIALECT dialect]              # Query profiling
FT.EXPLAIN index query [DIALECT dialect]                        # Show query execution plan
FT.SPELLCHECK index query [DISTANCE d] [DIALECT dialect]        # Spell check
FT.CONFIG SET key value                                         # Set runtime config
FT.CONFIG GET key                                               # Get runtime config

# Cursors (for paginated FT.AGGREGATE)
FT.CURSOR READ index cursor [COUNT count]                       # Read next page
FT.CURSOR DEL index cursor                                      # Delete cursor
```

**FT.CREATE 字段类型：**
- `TEXT` — 全文可搜索，支持词干提取、语音匹配
- `TAG` — 精确匹配标签（类别、ID）
- `NUMERIC` — 范围查询（价格、时间戳）
- `GEO` — 地理坐标（经度、纬度）
- `VECTOR` — 向量相似性（KNN、cosine/L2/IP）
- `GEOSHAPE` — 几何形状（SPHERICAL|FLAT）

**查询语法（DIALECT 2+）：**
- `hello world` — 词的并集（OR）
- `"hello world"` — 精确短语
- `@field:term` — 字段特定搜索
- `@price:[100 200]` — 数值范围
- `@location:[-122.41 37.77 5 km]` — 地理半径
- `*=>[KNN 10 @vec $blob]` — 向量相似性（KNN）
- `-term` — 排除词
- `~term` — 可选词
- `*` — 匹配所有文档

**FT.AGGREGATE 管道阶段：** `GROUPBY` + `REDUCE` → `SORTBY` → `APPLY` → `LIMIT` → `FILTER`。可用 reducer：`COUNT`、`SUM`、`MIN`、`MAX`、`AVG`、`COUNT_DISTINCT`、`COUNT_DISTINCTISH`、`QUANTILE`、`STDDEV`、`FIRST_VALUE`、`RANDOM_SAMPLE`、`TOLIST`。

**行为说明：**
- 向量查询和现代查询语法请使用 `DIALECT 2+`
- `FT.SEARCH` 返回 `[total_count, doc_id, field, value, ...]` 数组
- 不带 `SORTBY` 时，分页（`LIMIT`）结果不确定
- `FT.CREATE` 使用 `PREFIX` 自动索引匹配的键；新键在写入时被索引
- 在集群模式下，索引和文档必须在同一分片上（使用 hash tags）
- `SORTABLE` 字段增加内存使用但启用快速排序
- 每个索引最多 1024 个字段，128 个 TEXT 字段
