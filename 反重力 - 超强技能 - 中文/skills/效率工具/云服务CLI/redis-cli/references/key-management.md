# 键管理

## 目录

- [SCAN 系列](#scan-系列)
- [内置扫描模式](#内置扫描模式)
- [大键分析](#大键分析)
- [内存使用分析](#内存使用分析)
- [组合分析](#组合分析keystats)
- [热键检测](#热键检测)
- [键过期管理](#键过期管理)
- [批量插入](#批量插入)

## SCAN 系列

SCAN 系列提供生产安全的集合迭代。与 `KEYS *` 或 `SMEMBERS` 在大型数据集上会阻塞服务器不同，SCAN 增量返回小批量数据。

### SCAN 命令参考

| 命令 | 迭代对象 | 语法 |
|------|----------|------|
| `SCAN` | 数据库中的键 | `SCAN cursor [MATCH pattern] [COUNT count] [TYPE type]` |
| `SSCAN` | Set 的成员 | `SSCAN key cursor [MATCH pattern] [COUNT count]` |
| `HSCAN` | Hash 的字段 | `HSCAN key cursor [MATCH pattern] [COUNT count] [NOVALUES]` |
| `ZSCAN` | Sorted Set 的成员 | `ZSCAN key cursor [MATCH pattern] [COUNT count]` |

### SCAN 工作原理

1. 使用游标 `0` 开始迭代
2. 每次调用返回 `[new_cursor, [elements...]]`
3. 在下一次调用中使用 `new_cursor`
4. 当游标返回 `0` 时迭代完成

```
# Full iteration example
SCAN 0 MATCH user:* COUNT 100
# Returns: 1) "42"  2) ["user:1", "user:5", "user:23"]
SCAN 42 MATCH user:* COUNT 100
# Returns: 1) "0"   2) ["user:88", "user:91"]    ← iteration complete (cursor=0)
```

### SCAN 选项

**MATCH pattern** — 在检索*之后*应用的 Glob 风格过滤（非服务端过滤）：
- `*` 匹配任意序列
- `?` 匹配单个字符
- `[ae]` 匹配字符之一
- 重要：由于 MATCH 在检索后应用，某些迭代可能返回空结果。增加 `COUNT` 来补偿。

**COUNT n** — 每次调用元素数量的提示（默认：10）：
- 这是一个*提示*，不是保证
- 对于编码为 ziplist/intset 的小型集合，无论 COUNT 如何，所有元素可能在一次调用中返回
- 键空间（SCAN）始终使用哈希表，更可预测地遵循 COUNT
- 可以在调用之间更改 COUNT 而不影响迭代正确性

**TYPE type** — 按数据类型过滤（仅 SCAN，Redis 6.0+）：
- `SCAN 0 TYPE hash` 仅返回 hash 键
- 类型与 `TYPE` 命令返回的字符串相同：`string`、`list`、`set`、`zset`、`hash`、`stream`
- 与 MATCH 一样，在检索后应用

**NOVALUES** — 仅返回字段名，不含值（仅 HSCAN）：
- `HSCAN myhash 0 NOVALUES` 仅返回字段名，节省大型 Hash 的带宽

### SCAN 保证

完整迭代（游标 0 → 0）提供：

1. **完整性**：在整个迭代期间存在的所有元素至少被返回一次
2. **无误报**：在迭代期间从未存在的元素不会被返回

### SCAN 限制

- 元素可能被返回**多次** — 需在应用中处理去重
- 迭代期间添加或移除的元素可能出现也可能不出现 — 行为未定义
- 有效游标仅为 `0`（开始）或之前 SCAN 调用返回的值
- 如果集合增长速度快于 SCAN 推进速度，迭代可能永不终止

### Redis Cluster 中的 SCAN

在集群模式下，SCAN 仅迭代当前节点槽范围内的键。redis-cli 中的 `--scan` 选项自动处理跨所有节点的集群迭代。

模式匹配对暗示单个槽的模式进行了优化。例如，`{a}h*llo` 仅扫描槽 15495 中的键（hash tag `{a}`）。

## 内置扫描模式

redis-cli 提供封装 SCAN 命令的内置扫描模式：

```bash
# List all keys
redis-cli --scan

# Filter by glob pattern
redis-cli --scan --pattern 'user:*'
redis-cli --scan --pattern '*-11*'

# Control batch size
redis-cli --scan --count 100

# Add delay between SCAN calls (reduce server load)
redis-cli --scan --pattern 'user:*' -i 0.01

# Count keys matching a pattern
redis-cli --scan --pattern 'session:*' | wc -l

# Chain with other tools
redis-cli --scan --pattern 'cache:*' | head -20
redis-cli --scan --pattern 'temp:*' | while read key; do redis-cli DEL "$key"; done
```

## 大键分析

扫描整个键空间以查找元素最多的键（基于复杂度）。

```bash
# Find biggest keys by element count
redis-cli --bigkeys

# Throttle scanning (0.01 sec per 100 SCAN calls)
redis-cli --bigkeys -i 0.01

# Filter by pattern
redis-cli --bigkeys --pattern 'user:*'
```

输出示例：
```
# Scanning the entire keyspace...
Biggest   list found "bikes:finished" has 1 items
Biggest string found "all_bikes" has 36 bytes
Biggest   hash found "bike:1:stats" has 3 fields
Biggest stream found "race:france" has 4 entries

-------- summary -------
Total key length in bytes is 495 (avg len 9.00)

1 lists with 1 items (01.82% of keys, avg size 1.00)
16 strings with 149 bytes (29.09% of keys, avg size 9.31)
```

报告每种类型的最大键、每种类型的键占比和平均大小。可在集群副本上运行。

## 内存使用分析

扫描内存消耗最多的键。

```bash
# Find keys by memory consumption
redis-cli --memkeys

# With throttling
redis-cli --memkeys -i 0.01

# Custom sample count for nested types
redis-cli --memkeys --memkeys-samples 10
```

输出类似 `--bigkeys`，但报告字节大小而非元素计数。

## 组合分析（--keystats）

组合 `--bigkeys` 和 `--memkeys` 及分布数据。

```bash
redis-cli --keystats
redis-cli --keystats --top 20         # Show top 20 keys
redis-cli --keystats --cursor 12345   # Resume from a previous scan
redis-cli --keystats -i 0.01          # Throttled
```

输出包含：
- 按内存排名的前 N 个键大小
- 每种类型的最大键（按大小和按元素数量）
- 键大小的百分位分布
- 每种类型的统计（总键数、百分比、总大小、平均大小）

## 热键检测

识别频繁访问的键。需要将 `maxmemory-policy` 设置为 LFU 变体。

```bash
redis-cli --hotkeys
```

## 键过期管理

### 设置过期

```bash
# Set TTL in seconds
redis-cli EXPIRE mykey 3600

# Set TTL in milliseconds
redis-cli PEXPIRE mykey 5000

# Set expiry at specific Unix timestamp
redis-cli EXPIREAT mykey 1735689600

# Conditional expiry (Redis 7.0+)
redis-cli EXPIRE mykey 3600 NX        # Only if no current expiry
redis-cli EXPIRE mykey 3600 XX        # Only if already has expiry
redis-cli EXPIRE mykey 3600 GT        # Only if new TTL > current TTL
redis-cli EXPIRE mykey 3600 LT        # Only if new TTL < current TTL
```

### 检查过期

```bash
redis-cli TTL mykey                    # Seconds remaining (-1=none, -2=not exists)
redis-cli PTTL mykey                   # Milliseconds remaining
redis-cli EXPIRETIME mykey             # Unix timestamp of expiry
```

### 移除过期

```bash
redis-cli PERSIST mykey                # Make key permanent
```

### Hash 字段过期（Redis 7.4+）

```bash
redis-cli HEXPIRE myhash 3600 FIELDS 2 field1 field2
redis-cli HTTL myhash 2 field1 field2
redis-cli HPERSIST myhash FIELDS 2 field1 field2
```

### 过期行为

- 使用 `SET`、`GETSET` 或 `*STORE` 命令设置键会清除任何现有的 TTL
- `DEL`、`RENAME` 和 `MOVE` 会转移或清除 TTL
- 对已有 TTL 的键使用 `EXPIRE` 会更新超时时间
- 过期键被惰性删除或主动采样（约每秒 10 次，随机采样 20 个键）

## 批量插入

要将数据批量加载到 Redis，使用管道模式，这比逐条命令快得多。

```bash
# Generate Redis protocol from data and pipe it
cat data.txt | redis-cli --pipe

# With custom timeout (default 30 seconds)
cat data.txt | redis-cli --pipe --pipe-timeout 60

# The input file must use Redis protocol format:
# *<args>\r\n$<len>\r\n<arg>\r\n...
#
# Example for SET key value:
# *3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n
```

有关从 CSV 或其他数据源生成协议文件，请参阅[官方批量插入指南](https://redis.io/docs/latest/develop/clients/patterns/bulk-loading/)。
