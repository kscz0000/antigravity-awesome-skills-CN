# 检查与监控

## 目录

- [INFO 命令](#info-命令)
- [持续统计模式](#持续统计模式)
- [MONITOR 命令](#monitor-命令)
- [延迟分析](#延迟分析)
- [RDB 备份](#rdb-备份)
- [副本模式](#副本模式)
- [LRU 模拟](#lru-模拟)
- [慢日志](#慢日志)

## INFO 命令

返回以节组织的键值对格式的服务器信息和统计。

```bash
# All default sections
redis-cli INFO

# Specific sections
redis-cli INFO server
redis-cli INFO memory
redis-cli INFO keyspace
redis-cli INFO replication
redis-cli INFO clients
redis-cli INFO stats
redis-cli INFO persistence
redis-cli INFO cpu
redis-cli INFO commandstats
redis-cli INFO latencystats
redis-cli INFO cluster
redis-cli INFO modules

# Multiple sections (Redis 7.0+)
redis-cli INFO memory keyspace

# All sections including hidden ones
redis-cli INFO all

# Everything including debug sections
redis-cli INFO everything
```

### 关键 INFO 节

**server** — Redis 版本、进程 ID、运行时间、架构、TCP 端口、配置文件
**memory** — 已用内存、峰值内存、碎片率、系统总内存
**keyspace** — 每个数据库的键计数（如 `db0:keys=1000,expires=50,avg_ttl=3600`）
**clients** — 已连接客户端、阻塞客户端、最大客户端数
**replication** — 角色（主节点/副本）、已连接副本、复制偏移量
**stats** — 总连接数、已处理命令数、键空间命中/未命中
**persistence** — RDB/AOF 状态、上次保存时间、当前保存进度
**cpu** — Redis 消耗的用户/系统 CPU 时间

### 常用 INFO 查询

```bash
# Check memory usage and fragmentation
redis-cli INFO memory | grep -E "used_memory_human|fragmentation_ratio"

# Monitor keyspace changes
redis-cli INFO keyspace

# Check replication health
redis-cli INFO replication | grep -E "role|connected_slaves|master_repl_offset"

# Track hit rate
redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses"

# Watch specific metric over time
redis-cli -r -1 -i 5 INFO memory | grep used_memory_human
```

## 持续统计模式

每秒更新的服务器统计滚动显示（可用 `-i` 配置）。

```bash
redis-cli --stat

# Change update interval
redis-cli --stat -i 5    # every 5 seconds
```

输出列：
```
------- data ------ --------------------- load -------------------- - child -
keys       mem      clients blocked requests            connections
506        1015.00K 1       0       24 (+0)             7
506        1015.00K 1       0       25 (+1)             7
```

- **keys**：总键数
- **mem**：内存使用
- **clients**：已连接客户端
- **blocked**：阻塞的客户端
- **requests**：已处理的总请求数（括号内为与上一行的增量）
- **connections**：启动以来的总连接数

括号中的增量便于发现流量突增。

## MONITOR 命令

实时流式传输 Redis 服务器处理的所有命令。

```bash
redis-cli MONITOR
```

输出格式：
```
1460100081.165665 [0 127.0.0.1:51706] "set" "shipment:8000736522714:status" "sorting"
1460100083.053365 [0 127.0.0.1:51707] "get" "shipment:8000736522714:status"
```

字段：`timestamp [db client_addr] "command" "arg1" "arg2" ...`

**警告：** MONITOR 增加显著开销（每条命令还会发送给 MONITOR 客户端）。避免在繁忙的生产服务器上长时间运行。

用于调试 — 通过 grep 管道过滤：
```bash
redis-cli MONITOR | grep "SET"
redis-cli MONITOR | grep "user:"
```

## 延迟分析

Redis 为不同诊断场景提供多种延迟工具。

### 基本延迟（--latency）

持续发送 PING 并测量往返时间（100 次/秒）：

```bash
redis-cli --latency
# min: 0, max: 1, avg: 0.19 (427 samples)
```

统计以毫秒为单位。当不在 TTY 中（或使用 `--raw`）时，采样 1 秒后输出一行结果并退出。

### 延迟历史（--latency-history）

与 `--latency` 相同，但每 15 秒重置统计（可配置）：

```bash
redis-cli --latency-history
redis-cli --latency-history -i 30    # 30-second windows
```

### 延迟分布（--latency-dist）

延迟分布的彩色频谱可视化：

```bash
redis-cli --latency-dist
```

需要 xterm 256 色终端。默认 1 秒间隔，使用 `-i` 更改。

### 内在延迟（--intrinsic-latency）

测量系统基线延迟（内核调度器、虚拟机监控器），而非 Redis 本身。

```bash
# Run ON THE SAME MACHINE as Redis, not remotely
redis-cli --intrinsic-latency 5
```

参数为测试持续秒数。输出：
```
Max latency so far: 739 microseconds.
65433042 total runs (avg latency: 0.0764 microseconds).
Worst run took 9671x longer than the average latency.
```

这告诉你此系统上可达到的最低延迟。Redis 无法超越此基线。

### LATENCY 命令（Redis 内部）

Redis 内部也会跟踪慢事件：

```bash
redis-cli LATENCY LATEST              # Latest latency spikes per event
redis-cli LATENCY HISTORY event-name  # Time-series data for an event
redis-cli LATENCY GRAPH event-name    # ASCII graph of latency over time
redis-cli LATENCY RESET [event ...]   # Reset latency data
redis-cli LATENCY DOCTOR              # Diagnose latency issues
```

常见事件名称：`command`、`fork`、`rdb-unlink`、`aof-write`、`aof-fsync-always`。

## RDB 备份

从远程 Redis 实例传输 RDB 转储文件到本地机器。

```bash
redis-cli --rdb /tmp/dump.rdb
# SYNC sent to master, writing 13256 bytes to '/tmp/dump.rdb'
# Transfer finished with success.
```

检查退出码确认错误：
```bash
redis-cli --rdb /tmp/dump.rdb
echo $?    # 0 = success, non-zero = error
```

**仅函数 RDB**（跳过键数据）：
```bash
redis-cli --functions-rdb /tmp/functions.rdb
```

适用于自动化备份脚本和定时任务。RDB 文件可被任何 Redis 实例加载。

## 副本模式

模拟副本以检查来自主节点的复制流：

```bash
redis-cli --replica
```

输出以 CSV 格式显示复制命令：
```
SYNC with master, discarding 13256 bytes of bulk transfer...
SYNC done. Logging commands from master.
"PING"
"SELECT","0"
"SET","last_name","Enigk"
"INCR","mycounter"
```

适用于调试复制问题和了解发送给副本的数据。

## LRU 模拟

模拟缓存行为以帮助确定最佳 `maxmemory` 设置。

```bash
# Simulate 10 million keys with LRU eviction
redis-cli --lru-test 10000000
```

前置条件：
- 在 redis.conf 中配置 `maxmemory`（如 `100mb`）
- 设置 `maxmemory-policy` 为 `allkeys-lru`
- **警告**：此测试使用管道并给服务器施压 — 切勿在生产实例上使用

输出显示命中/未命中率：
```
156000 Gets/sec | Hits: 4552 (2.92%) | Misses: 151448 (97.08%)
153750 Gets/sec | Hits: 12906 (8.39%) | Misses: 140844 (91.61%)
```

使用此工具根据键数量和访问模式（80-20 幂律分布）找到合适的 `maxmemory` 值。未命中率 >10% 通常意味着需要更多内存。

## 慢日志

慢日志记录超过配置执行时间阈值的命令。调试不明延迟时应首先使用的工具。

### 配置

```bash
# Check current slowlog settings
redis-cli CONFIG GET slowlog*

# slowlog-log-slower-than: threshold in microseconds (negative = disabled)
# slowlog-max-len: maximum number of entries to keep (ring buffer)
redis-cli CONFIG SET slowlog-log-slower-than 10000   # 10ms
redis-cli CONFIG SET slowlog-max-len 128
```

### 查询

```bash
# Get recent slow log entries (default: 10)
redis-cli SLOWLOG GET
redis-cli SLOWLOG GET 20              # Last 20 entries

# Each entry format:
# 1) id            — unique entry ID
# 2) timestamp     — Unix timestamp
# 3) duration      — execution time in microseconds
# 4) command       — array: [cmd, arg1, arg2, ...]
# 5) client        — client address:port
# 6) client_name   — client name (via CLIENT SETNAME)

# Get entry count
redis-cli SLOWLOG LEN

# Reset (clear all entries)
redis-cli SLOWLOG RESET
```

### 常用 SLOWLOG 查询

```bash
# Find slowest commands
redis-cli SLOWLOG GET 50 | grep -E "^\d+\)|^\d+\) \(integer\)"

# Monitor slow log continuously
redis-cli -r -1 -i 10 SLOWLOG GET 5

# Combine with LATENCY for deeper analysis
redis-cli LATENCY LATEST
redis-cli SLOWLOG GET 10
```
