---
# 元数据：技能标识、风险等级、来源、许可证等基础信息
# 名称：本技能名为 redis-cli，对应 Redis 命令行界面工具
name: redis-cli
# 描述：本技能提供 Redis 命令行界面 redis-cli 的完整中文参考与使用指南
description: Redis 命令行界面（redis-cli）参考与使用指南。当用户提到 redis-cli、Redis CLI、Redis 命令行工具、Redis 客户端命令行，或任何涉及从命令行查询、检查、调试、管理、监控、调优、诊断、键空间扫描、SCAN 迭代、INFO 统计、SLOWLOG 慢日志分析、ACL 用户管理、副本复制配置、集群节点管理、持久化备份恢复、Pub/Sub 订阅发布、Lua 脚本调试执行、CSV/JSON 数据导出、客户端连接控制、配置运行时调整、性能延迟基线测量等 Redis 日常运维与开发任务时使用此技能。常见触发词：redis-cli、Redis CLI、Redis 命令行、Redis 查询、Redis 调试、Redis 管理、Redis 监控、Redis 检查、Redis 诊断、Redis 调优、键值读写、SCAN 扫描、键空间扫描、KEYS 命令、BIGKEYS 大键分析、MEMKEYS 内存分析、INFO 统计、SLOWLOG 慢日志、ACL 用户管理、ACL 权限、副本配置 REPLICAOF、集群节点 CLUSTER、RDB 备份、AOF 重写、订阅频道 SUBSCRIBE、Lua 脚本 EVAL、CSV 输出、JSON 输出、客户端连接 CLIENT KILL、CONFIG SET 配置、延迟分析 LATENCY、连接管理、Redis 7、Redis 8 等...
# 风险等级：未知风险等级（保留原值）
risk: unknown
# 上游源码仓库地址
source: https://github.com/chaunsin/agent-skills/tree/master/skills/redis-cli
# 上游仓库所有者与名称
source_repo: chaunsin/agent-skills
# 来源类型：社区贡献
source_type: community
# 加入日期：2026 年 7 月 1 日
date_added: 2026-07-01
# 开源许可证：Apache 2.0
license: Apache-2.0
# 许可证源文件原始链接地址（完整 URL 保留原样）
license_source: https://github.com/chaunsin/agent-skills/blob/master/LICENSE
---

# redis-cli — Redis 命令行界面
## 何时使用

当需要 redis 命令行界面（redis-cli）参考与使用指南时使用此技能。当用户提到 redis-cli、Redis CLI，或任何涉及从命令行查询、检查、调试或管理 Redis 的任务时使用此技能。触发词：键值读写、SCAN、键空间扫描...


redis-cli 是与 Redis 交互的主要命令行工具。它支持两种模式：**命令行执行**（执行一条命令后退出）和**交互模式**（带 Tab 补全、历史记录和提示的 REPL）。它还提供了用于监控、延迟分析、键空间扫描和数据导入/导出的特殊模式。

**官方资源：** [Redis CLI 文档](https://redis.io/docs/latest/develop/tools/cli/) | [命令参考](https://redis.io/commands/) | [下载](https://redis.io/downloads/)

## 前置条件

```bash
# Check if redis-cli is installed
redis-cli --version

# Install options:

# macOS (Homebrew)
brew install redis

# Ubuntu / Debian
sudo apt install redis-tools

# CentOS / RHEL
sudo yum install redis

# Alpine
apk add redis

# Build from source (binary only)
make redis-cli
# Binary at: src/redis-cli

# Docker (no installation needed)
docker run -it --rm redis redis-cli -h <host> -p <port> PING
```

## 安全注意事项

> **重要提示**：Redis 提供强大的操作能力，可能不可逆地修改或删除数据。
> 请密切注意以下安全准则：

- **切勿在生产环境中通过 `-a` 传递密码** — 在 shell 历史记录和进程列表中可见。请改用 `REDISCLI_AUTH` 环境变量。
- **`KEYS *` 会阻塞服务器** — 在大型数据库上务必使用 `SCAN` 替代。
- **`MONITOR` 会记录所有命令** — 包括敏感数据，谨慎使用，切勿在生产服务器上长时间运行。
- **`FLUSHALL` / `FLUSHDB` 不可逆** — 执行前务必用 `CLIENT LIST` 或 `INFO keyspace` 确认目标数据库。
- **写入操作期间使用 `--rdb` 传输** — 在繁忙服务器上可能产生不一致的快照。

## 快速参考

### 连接

```bash
# Basic connection (default: 127.0.0.1:6379)
redis-cli
redis-cli -h redis15.localnet.org -p 6390 PING

# With password (prefer REDISCLI_AUTH env var for security)
redis-cli -a myUnguessablePazzzzzword123 PING

# URI connection
redis-cli -u redis://user:password@host:port/dbnum PING

# TLS
redis-cli --tls --cacert /path/to/ca.crt -h redis.example.com PING

# Specific database
redis-cli -n 2 DBSIZE

# IPv4/IPv6 preference
redis-cli -4 PING   # prefer IPv4
redis-cli -6 PING   # prefer IPv6
```

### 命令行模式与交互模式

```bash
# Command-line mode: execute one command and exit
redis-cli INCR mycounter
redis-cli GET mykey

# Interactive mode: type commands at the prompt
redis-cli
127.0.0.1:6379> PING
PONG
127.0.0.1:6379> SELECT 2
OK
127.0.0.1:6379[2]> DBSIZE
(integer) 1
```

提示符显示 `host:port[db]`。使用 `CONNECT <host> <port>` 在交互模式下切换实例。

### 数据查询速查表

**String 操作** (O(1)):
```
GET key                        # Get value
SET key value [NX|XX] [EX sec|PX ms|KEEPTTL]  # Set with conditions/TTL
SET key value GET              # Set new, return old value
GETSET key newvalue            # [Use SET key value GET instead]
MGET key1 key2 ...             # Get multiple values
INCR key                       # Increment integer (+1)
INCRBY key 10                  # Increment by amount
STRLEN key                     # String length
GETRANGE key 0 50              # Substring
```

**Hash 操作**:
```
HGET key field                 # Get field value            O(1)
HMGET key f1 f2                # Get multiple fields        O(N)
HGETALL key                    # Get all fields/values      O(N)
HKEYS key                      # Get all field names        O(N)
HLEN key                       # Number of fields           O(1)
HEXISTS key field              # Check field exists         O(1)
HSCAN key 0 [MATCH pat]        # Iterate hash fields        O(1) per call
```

**List 操作**:
```
LRANGE key 0 -1                # Get all elements           O(N)
LLEN key                       # List length                O(1)
LINDEX key 0                   # Get by index               O(N)
LPOS key value                 # Find element position      O(N)
```

**Set 操作**:
```
SMEMBERS key                   # Get all members            O(N)
SCARD key                      # Set cardinality            O(1)
SISMEMBER key member           # Check membership           O(1)
SMISMEMBER key m1 m2           # Multi-membership check     O(N)
SSCAN key 0 [MATCH pat]        # Iterate set members        O(1) per call
```

**Sorted Set 操作**:
```
ZRANGE key 0 -1 [WITHSCORES]           # By index              O(log(N)+M)
ZRANGE key -inf +inf BYSCORE           # By score range        O(log(N)+M)
ZRANGE key [a [z BYLEX                 # By lexicographic      O(log(N)+M)
ZCARD key                               # Member count          O(1)
ZSCORE key member                       # Get score             O(1)
ZRANK key member                        # Get rank              O(log(N))
ZSCAN key 0 [MATCH pat]                 # Iterate members       O(1) per call
```

**键检查**:
```
EXISTS key [key ...]           # Check existence (O(N) for multi) — returns count
TYPE key                       # Data type: string|list|set|zset|hash|stream  O(1)
TTL key                        # Seconds until expiry (-1=none, -2=not exists)  O(1)
PTTL key                       # Milliseconds until expiry                      O(1)
MEMORY USAGE key [SAMPLES n]   # Memory consumption in bytes                    O(N)
OBJECT ENCODING key            # Internal encoding (ziplist, hashtable, etc.)   O(1)
OBJECT IDLETIME key            # Seconds since last access                      O(1)
DBSIZE                         # Total keys in current database                 O(1)
RANDOMKEY                      # Return a random key                            O(1)
```

### 键扫描（生产安全）

基于 SCAN 的迭代不会阻塞服务器，而 `KEYS *` 在生产环境中应避免使用。

```bash
# redis-cli built-in scan mode
redis-cli --scan                          # List all keys
redis-cli --scan --pattern 'user:*'       # Filter by pattern
redis-cli --scan --pattern '*:12345*'     # Glob patterns
redis-cli --scan --count 100              # Batch size hint

# Programmatic SCAN in interactive mode
SCAN 0 MATCH user:* COUNT 100
# Returns: 1) next_cursor  2) [keys...]
# Continue with: SCAN <next_cursor> MATCH user:* COUNT 100
# Iteration complete when cursor returns 0

# Count keys matching a pattern
redis-cli --scan --pattern 'session:*' | wc -l
```

SCAN 保证：完整迭代（游标 0 → 游标 0）始终返回整个迭代期间存在的所有元素。元素可能出现多次 — 需在应用中处理去重。

### 服务器检查

```bash
# Real-time stats (updates every second, use -i to change interval)
redis-cli --stat

# Server information
redis-cli INFO server             # Server details
redis-cli INFO memory             # Memory usage
redis-cli INFO keyspace           # Database key counts
redis-cli INFO replication        # Replication status
redis-cli INFO all                # Everything

# Key space analysis
redis-cli --bigkeys               # Find largest keys by element count
redis-cli --memkeys               # Find largest keys by memory usage
redis-cli --keystats              # Combined bigkeys + memkeys with distribution

# Latency analysis
redis-cli --latency               # Continuous latency sampling
redis-cli --latency-history       # Latency over time (15s windows)
redis-cli --latency-dist          # Latency spectrum visualization
redis-cli --intrinsic-latency 5   # System baseline latency (run on Redis host)
```

### 输出控制

```bash
# Raw output (no type prefixes) — default when piping
redis-cli --raw GET mykey
redis-cli GET mykey > /tmp/output.txt    # auto raw mode

# Human-readable (force) when piping
redis-cli --no-raw GET mykey | cat

# CSV output
redis-cli --csv LRANGE mylist 0 -1

# JSON output (RESP3, use -2 for RESP2)
redis-cli --json HGETALL user:1

# Read last argument from stdin
cat /etc/services | redis-cli -x SET net_services

# Pipe commands from file
cat /tmp/commands.txt | redis-cli
```

### 重复执行命令

```bash
# Run command N times
redis-cli -r 5 INCR counter

# Run with delay (seconds, supports decimals)
redis-cli -r -1 -i 1 INFO | grep rss_human    # infinite, every 1s

# Interactive: prefix with count
5 INCR mycounter    # runs 5 times
```

### 服务器管理

```bash
# ACL management
redis-cli ACL LIST                                    # List all users
redis-cli ACL SETUSER admin on >pwd ~* +@all          # Create admin user
redis-cli ACL SETUSER readonly on >pwd ~* +@read      # Create read-only user
redis-cli ACL DELUSER username                        # Delete user
redis-cli ACL DRYRUN username GET key                 # Test user permission
redis-cli ACL GENPASS                                 # Generate random password

# Client management
redis-cli CLIENT LIST                                 # List all connections
redis-cli CLIENT KILL ADDR ip:port                    # Disconnect client
redis-cli CLIENT PAUSE 5000 WRITE                     # Pause writes for 5s
redis-cli CLIENT SETNAME my-app                       # Name current connection

# Configuration
redis-cli CONFIG GET maxmemory                        # Read config
redis-cli CONFIG SET maxmemory 100mb                  # Set config at runtime
redis-cli CONFIG REWRITE                              # Persist to redis.conf
redis-cli CONFIG RESETSTAT                            # Reset INFO counters

# Replication acknowledgment
redis-cli WAIT 2 5000                                 # Wait for 2 replicas (5s timeout)
redis-cli WAITAOF 1 1 5000                            # Wait for AOF fsync (Redis 7.2+)

# Persistence
redis-cli BGSAVE                                      # Background RDB save
redis-cli BGREWRITEAOF                                # Background AOF rewrite
redis-cli LASTSAVE                                    # Last save timestamp

# Replication
redis-cli REPLICAOF host port                         # Become replica
redis-cli REPLICAOF NO ONE                            # Promote to master

# Server lifecycle
redis-cli SHUTDOWN SAVE                               # Save and stop
redis-cli SHUTDOWN NOSAVE                             # Stop without saving

# Slow log
redis-cli SLOWLOG GET 10                              # Recent slow commands
redis-cli SLOWLOG LEN                                 # Entry count
redis-cli SLOWLOG RESET                               # Clear entries

# Cluster management
redis-cli --cluster check host:port                   # Check cluster health
redis-cli --cluster reshard host:port                 # Move slots between nodes
redis-cli -c -h cluster-node PING                     # Cluster-aware connection
```

## 详细参考文件

| 文件 | 内容 | 何时阅读 |
|------|------|----------|
| `references/connection-and-options.md` | 完整连接选项、CLI 标志、SSL/TLS、环境变量、交互模式功能（补全、历史、偏好）、RESP 协议版本 | 配置连接、设置 TLS、自定义 CLI 行为 |
| `references/data-query-commands.md` | 核心数据类型命令：String、Hash、List、Set、Sorted Set、Stream、Bitmap、HyperLogLog、Geospatial，以及键操作、数据库操作和事务 | 查找核心命令语法、理解命令选项和返回值 |
| `references/module-data-types.md` | 模块数据类型：JSON（RedisJSON）、Vector Sets（Redis 8.0+）、Bloom Filter、Cuckoo Filter、Top-K、Count-Min Sketch、T-Digest、TimeSeries（TS.*）、全文搜索 / RediSearch（FT.*）— 含完整命令语法和行为说明 | 使用 Redis 模块数据类型、相似性搜索、概率数据结构、时序数据、全文搜索 |
| `references/key-management.md` | SCAN 系列详情（SCAN/SSCAN/HSCAN/ZSCAN）、大键分析（--bigkeys、--memkeys、--keystats）、键过期（EXPIRE、TTL、PERSIST）、键空间模式、批量插入 | 扫描数据库、分析键分布、管理键生命周期 |
| `references/inspection-and-monitoring.md` | INFO 各节、MONITOR、--stat 模式、延迟工具（--latency、--latency-history、--latency-dist、--intrinsic-latency）、RDB 备份、副本模式、LRU 模拟 | 监控 Redis 实例、调试性能、创建备份 |
| `references/advanced-features.md` | Lua 脚本（--eval、--ldb）、Pub/Sub 模式、管道模式、CSV/JSON 输出、字符串引号和转义、从 stdin 获取输入、远程 RDB 传输、集群管理（--cluster 子命令、集群命令） | 运行脚本、订阅频道、批量数据操作、管理 Redis Cluster |
| `references/server-administration.md` | ACL 管理（ACL SETUSER/DELUSER/LIST/CAT/GENPASS）、客户端管理（CLIENT LIST/KILL/PAUSE/TRACKING）、配置（CONFIG GET/SET/REWRITE）、复制确认（WAIT/WAITAOF）、持久化（SAVE/BGSAVE/BGREWRITEAOF）、复制设置（REPLICAOF）、服务器生命周期（SHUTDOWN/FAILOVER） | 管理用户和权限、控制客户端连接、运行时配置、确保写入持久性、持久化管理、复制设置 |

## 常见工作流

### 探索未知数据库

```bash
# Step 1: Basic stats
redis-cli INFO keyspace
redis-cli DBSIZE

# Step 2: Find big keys and memory usage
redis-cli --bigkeys
redis-cli --memkeys

# Step 3: Sample keys and inspect types
redis-cli --scan | head -20
redis-cli TYPE <key>
redis-cli TTL <key>

# Step 4: Read data based on type
redis-cli HGETALL <hash_key>
redis-cli LRANGE <list_key> 0 -1
redis-cli ZRANGE <zset_key> 0 -1 WITHSCORES
```

### 实时监控

```bash
# Live server stats
redis-cli --stat -i 2

# Watch memory specifically
redis-cli -r -1 -i 5 INFO memory | grep used_memory_human

# Monitor all commands (caution: high overhead)
redis-cli MONITOR

# Continuous latency
redis-cli --latency-history -i 5
```

### 查询特定键模式

```bash
# Count keys by pattern
redis-cli --scan --pattern 'session:*' | wc -l

# Find and inspect hash keys
redis-cli --scan --pattern 'user:*' | while read key; do
  echo "=== $key ==="
  redis-cli HGETALL "$key"
done

# Check TTL of matching keys
redis-cli --scan --pattern 'cache:*' | while read key; do
  redis-cli TTL "$key"
done
```

## 外部参考

- [Redis CLI 文档](https://redis.io/docs/latest/develop/tools/cli/)
- [Redis 命令参考](https://redis.io/commands/)
- [Redis 数据类型](https://redis.io/docs/latest/develop/data-types/)
- [Redis 协议规范](https://redis.io/docs/latest/develop/reference/protocol-spec/)
- [Redis 批量插入](https://redis.io/docs/latest/develop/clients/patterns/bulk-loading/)
- [Redis Lua 调试器](https://redis.io/docs/latest/develop/programmability/lua-debugging/)

## 限制

- 仅当任务明确匹配其上游源和本地项目上下文时使用此技能。
- 在应用变更前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定测试、安全审查或用户对破坏性或高成本操作的批准。
