# 数据查询命令

Redis 中查询和操作数据的完整命令参考，按数据类型组织。每条命令包含语法、复杂度和关键行为说明。

## 目录

- [String](#string)
- [Hash](#hash)
- [List](#list)
- [Set](#set)
- [Sorted Set](#sorted-set)
- [Stream](#stream)
- [Bitmap 与 Bitfield](#bitmap-与-bitfield)
- [HyperLogLog](#hyperloglog)
- [Geospatial](#geospatial)
- [键操作](#键操作)
- [数据库操作](#数据库操作)
- [事务](#事务)

## String

String 是最基础的 Redis 类型，最多可存储 512MB。可以存储文本、数字（用于 INCR/DECR）或二进制数据。

```
# Read / Write
GET key                                # Get value                        O(1)
SET key value [EX sec|PX ms|EXAT ts|PXAT ms|KEEPTTL]  # Set with optional expiry  O(1)
SET key value [NX|XX]                  # NX=only if not exists, XX=exists O(1)
SET key value GET                      # Set and return old value         O(1)
GETSET key newvalue                    # [Deprecated 6.2] Use SET key value GET
GETDEL key                             # Get then delete                  O(1)
GETEX key [EX sec|PX ms|PERSIST]       # Get and set/remove expiry        O(1)

# Multi-key
MGET key [key ...]                     # Get multiple values              O(N)
MSET key value [key value ...]         # Set multiple values              O(N)
MSETNX key value [key value ...]       # Set if NONE exist                O(N)

# Numeric operations (value must be integer or float)
INCR key                               # +1                               O(1)
INCRBY key increment                   # +N                               O(1)
INCRBYFLOAT key increment              # +float                           O(1)
DECR key                               # -1                               O(1)
DECRBY key decrement                   # -N                               O(1)

# String manipulation
STRLEN key                             # Length in bytes                  O(1)
GETRANGE key start end                 # Substring                        O(N)
SETRANGE key offset value              # Overwrite at position            O(N)
APPEND key value                       # Append to string                 O(1)
SUBSTR key start end                   # Alias for GETRANGE               O(N)

# Conditional set (Redis 8.4+)
SET key value IFEQ expected-value      # Set only if current value matches
SET key value IFNE expected-value      # Set only if current value differs
SET key value IFDEQ expected-digest    # Set only if digest matches (hash comparison)
SET key value IFDNE expected-digest    # Set only if digest differs
```

**行为说明：**
- `SET` 会覆盖任何现有值（无论类型），并清除任何现有的 TTL
- `SET NX` 常用于分布式锁
- `INCR`/`DECR` 在值不是有效整数时会失败；小数请使用 `INCRBYFLOAT`
- `GETRANGE` 从 0 开始索引；负数索引从末尾计数（-1 = 最后一个字符）
- 空字符串使用约 56 字节开销（`MEMORY USAGE`）

## Hash

Hash 将字符串字段映射到字符串值 — 非常适合表示对象。小型 Hash 使用内存高效的 ziplist 编码存储。

```
# Read
HGET key field                         # Get field value                  O(1)
HMGET key field [field ...]            # Get multiple fields              O(N)
HGETALL key                            # Get all fields and values        O(N)
HKEYS key                              # Get all field names              O(N)
HVALS key                              # Get all values                   O(N)
HLEN key                               # Number of fields                 O(1)
HEXISTS key field                      # Check field exists               O(1)
HRANDFIELD key [count [WITHVALUES]]    # Random field(s)                  O(N)

# Write
HSET key field value [field value ...] # Set one or more fields           O(N)
HSETNX key field value                 # Set field only if not exists     O(1)
HDEL key field [field ...]             # Delete fields                    O(N)

# Numeric
HINCRBY key field increment            # Increment integer field          O(1)
HINCRBYFLOAT key field increment       # Increment float field            O(1)

# Iterate
HSCAN key cursor [MATCH pat] [COUNT n] [NOVALUES]  # Incremental iterate O(1)/call

# Field-level expiry (Redis 7.4+)
HEXPIRE key seconds [NX|XX|GT|LT] FIELDS numfields field [field ...]  # Set field TTL
HPEXPIRE key milliseconds [NX|XX|GT|LT] FIELDS numfields field [field ...]  # Set field TTL (ms)
HTTL key numfields field [field ...]               # Get field TTL
HPERSIST key [NX|XX|GT|LT] FIELDS numfields field [field ...]  # Remove field TTL
```

**行为说明：**
- `HGETALL` 返回交替的字段-值对：`[field1, value1, field2, value2, ...]`
- `HGETALL` 对不存在的键返回空列表
- `HGETALL` 和 `HKEYS` 中字段顺序不确定
- `HSCAN` 加 `NOVALUES` 仅返回字段名（节省带宽）
- 小型 Hash 使用 `HGETALL` 效率高；大型 Hash 优先使用 `HSCAN`
- Hash 最小长度为 0（删除最后一个字段后的空 Hash）

## List

List 是有序字符串序列，以链表实现，头部/尾部操作快速。适用于队列、栈和时间线。

```
# Read
LRANGE key start stop                  # Get range (0 -1 = all)          O(N)
LLEN key                               # List length                      O(1)
LINDEX key index                       # Get by index (0-based)           O(N)
LPOS key value [RANK rank] [COUNT n] [MAXLEN len]  # Find position   O(N)
LMPOP numkeys key [key ...] LEFT|RIGHT [COUNT count]  # Pop from multiple lists  O(N+M)

# Write (push)
LPUSH key element [element ...]        # Push to head                     O(N) for N elements
RPUSH key element [element ...]        # Push to tail                     O(N) for N elements
LPUSHX key element                     # Push to head if exists           O(1)
RPUSHX key element                     # Push to tail if exists           O(1)
LINSERT key BEFORE|AFTER pivot element # Insert relative to pivot        O(N)

# Write (pop)
LPOP key [count]                       # Pop from head                    O(N) for count
RPOP key [count]                       # Pop from tail                    O(N) for count
BLPOP key [key ...] timeout            # Blocking pop from head           O(N)
BRPOP key [key ...] timeout            # Blocking pop from tail           O(N)

# Move
LMOVE source destination LEFT|RIGHT LEFT|RIGHT  # Atomic move       O(1)
BLMOVE src dest L|R L|R timeout       # Blocking move                    O(1)
RPOPLPUSH source destination           # [Deprecated 6.2] Use LMOVE       O(1)

# Modify
LSET key index element                 # Set at index                     O(N)
LREM key count element                 # Remove occurrences               O(N+M)
LTRIM key start stop                   # Keep only range                  O(N)
```

**行为说明：**
- `LRANGE key 0 -1` 返回所有元素；`LRANGE key 0 9` 返回前 10 个
- 负数索引从末尾计数：`-1` 是最后一个元素
- `LPUSH` 多个元素时从左到右推入，最终顺序是反序的
- `LPOP`/`RPOP` 带 count（Redis 6.2+）返回数组；不带 count 返回单个元素或 nil
- `LTRIM` 常与 `LPUSH` 组合使用以维护有上限的列表
- `BLPOP`/`BRPOP` 阻塞客户端直到数据可用或超时（0 = 永久等待）

## Set

Set 是无序的唯一字符串集合。适用于成员检查、去重和集合运算。

```
# Read
SMEMBERS key                           # Get all members                  O(N)
SCARD key                              # Member count                     O(1)
SISMEMBER key member                   # Check membership                 O(1)
SMISMEMBER key member [member ...]     # Multi-membership check           O(N)
SRANDMEMBER key [count]                # Random member(s)                 O(N)
SSCAN key cursor [MATCH pat] [COUNT n] # Incremental iterate              O(1)/call

# Write
SADD key member [member ...]           # Add members                      O(N)
SREM key member [member ...]           # Remove members                   O(N)
SPOP key [count]                       # Remove and return random         O(N)
SMOVE source dest member               # Move member between sets         O(1)

# Set operations
SINTER key [key ...]                   # Intersection                     O(N*M)
SINTERCARD numkeys key [key ...] [LIMIT limit]  # Intersection cardinality  O(N*M)
SINTERSTORE dest key [key ...]         # Intersection → new set           O(N*M)
SUNION key [key ...]                   # Union                            O(N)
SUNIONSTORE dest key [key ...]         # Union → new set                  O(N)
SDIFF key [key ...]                    # Difference (first - rest)        O(N)
SDIFFSTORE dest key [key ...]          # Difference → new set             O(N)
```

**行为说明：**
- `SMEMBERS` 返回所有成员；大型集合请使用 `SSCAN`
- `SRANDMEMBER` 正数 count 返回不重复元素（可能少于 count，如果 count > 集合大小）
- `SRANDMEMBER` 负数 count 可能返回重复元素（始终返回恰好 count 个元素）
- `SPOP` 从集合中移除元素；`SRANDMEMBER` 不移除
- `SDIFF` 从第一个键开始计算差集 — 顺序很重要

## Sorted Set

Sorted Set（zset）将成员映射到分数。成员唯一，按分数排序，分数相同则按字典序。适用于排行榜、排名和优先队列。

```
# Read by index
ZRANGE key start stop [WITHSCORES]               # By rank              O(log(N)+M)
ZRANGESTORE dest src start stop                   # Store range          O(log(N)+M)

# Read by score
ZRANGE key min max BYSCORE [WITHSCORES] [LIMIT offset count]  # By score O(log(N)+M)
ZCOUNT key min max                                # Count in score range O(log(N))
ZLEXCOUNT key min max                             # Count in lex range   O(log(N))

# Read by lexicographic order (all members must have same score)
ZRANGE key min max BYLEX [LIMIT offset count]     # By lex              O(log(N)+M)

# Member lookup
ZSCORE key member                                 # Get score            O(1)
ZRANK key member                                  # Get rank (ascending) O(log(N))
ZREVRANK key member                               # Get rank (descending)O(log(N))
ZMSCORE key member [member ...]                   # Multi-score get      O(N)

# Aggregate info
ZCARD key                                         # Member count         O(1)
ZRANDMEMBER key [count [WITHSCORES]]              # Random member(s)     O(N)

# Iterate
ZSCAN key cursor [MATCH pat] [COUNT n]            # Incremental iterate  O(1)/call

# Pop extremes
ZPOPMIN key [count]                               # Remove lowest scored O(log(N)*count)
ZPOPMAX key [count]                               # Remove highest scoredO(log(N)*count)
BZPOPMIN key [key ...] timeout                    # Blocking pop min     O(log(N))
BZPOPMAX key [key ...] timeout                    # Blocking pop max     O(log(N))
ZMPOP numkeys key [key ...] MIN|MAX [COUNT count] # Pop from multiple    O(K)+O(M*log(N))

# Write
ZADD key [NX|XX] [GT|LT] [CH] score member [score member ...]  # Add/update  O(log(N))
ZREM key member [member ...]                      # Remove members       O(M*log(N))
ZINCRBY key increment member                      # Increment score      O(log(N))

# Remove by range
ZREMRANGEBYRANK key start stop                    # Remove by rank       O(log(N)+M)
ZREMRANGEBYSCORE key min max                      # Remove by score      O(log(N)+M)
ZREMRANGEBYLEX key min max                        # Remove by lex        O(log(N)+M)

# Set operations
ZUNIONSTORE dest numkeys key [key ...] [WEIGHTS w...] [AGGREGATE SUM|MIN|MAX]
ZINTERSTORE dest numkeys key [key ...] [WEIGHTS w...] [AGGREGATE SUM|MIN|MAX]
ZUNION numkeys key [key ...] [WITHSCORES]         # Union result
ZINTER numkeys key [key ...] [WITHSCORES]         # Intersection result
ZINTERCARD numkeys key [key ...] [LIMIT limit]    # Intersection count
ZDIFF numkeys key [key ...] [WITHSCORES]          # Difference result
ZDIFFSTORE dest numkeys key [key ...]             # Difference → new set
```

**行为说明：**
- `ZRANGE` 替代了 `ZRANGEBYSCORE`、`ZRANGEBYLEX`、`ZREVRANGE`、`ZREVRANGEBYSCORE`、`ZREVRANGEBYLEX`（均自 Redis 6.2 起弃用）
- 基于索引：`0` 是最低分，`-1` 是最高分；`REV` 标志反转顺序
- 基于分数：使用 `-inf` 和 `+inf` 表示无界范围；`(` 前缀表示排除：`(1 10` = 分数 >1 且 <=10
- 基于字典序：使用 `[` 包含，`(` 排除：`[a (z` = 成员 >= "a" 且 < "z"
- `ZADD` 选项：`NX`（仅添加新成员）、`XX`（仅更新已有成员）、`GT`（仅当新分数 > 当前分数）、`LT`（仅当新分数 < 当前分数）、`CH`（返回变更元素数量）
- `WITHSCORES` 返回交替的成员、分数对

## Stream

Stream 是仅追加的日志数据结构，带有消费者组用于消息处理。

```
# Write
XADD key [NOMKSTREAM] [MAXLEN|MINID [=|~] threshold [LIMIT count]] *|ID field value [field value ...]
                                        # Add entry                            O(1)
XADD key [KEEPREF|DELREF|ACKED] ...     # Reference control (Redis 8.2+)
XADD key [IDMPAUTO pid | IDMP pid iid] ...  # Idempotent add (Redis 8.6+)

# Read
XRANGE key start end [COUNT count]                 # Read by ID range     O(N)
XREVRANGE key end start [COUNT count]              # Reverse read         O(N)
XREAD [COUNT count] [BLOCK ms] STREAMS key [key ...] ID [ID ...]  # Read new entries
XLEN key                                           # Entry count          O(1)

# Consumer groups
XGROUP CREATE key groupname ID|$ [MKSTREAM]        # Create group
XREADGROUP GROUP group consumer [COUNT n] [BLOCK ms] [NOACK] STREAMS key [key ...] ID [ID ...]
XPENDING key group                                 # Pending messages info
XACK key group ID [ID ...]                         # Acknowledge message
XCLAIM key group consumer min-idle-time ID [ID ...] [IDLE ms] [TIME ms] [RETRYCOUNT n] [FORCE] [JUSTID]
XAUTOCLAIM key group consumer min-idle-time start [COUNT count] [JUSTID]

# Info
XINFO STREAM key                                   # Stream info
XINFO GROUPS key                                   # Consumer group info
XINFO CONSUMERS key group                          # Consumer info

# Management
XTRIM key MAXLEN|MINID [=|~] threshold [LIMIT count]  # Trim stream
XDEL key ID [ID ...]                               # Delete entries
XSETID key last-idle                               # Set last ID
```

**行为说明：**
- `XADD` 使用 `*` 自动生成格式为 `TIMESTAMP-SEQUENCE` 的 ID
- `XRANGE key - +` 返回所有条目；使用 `COUNT` 限制数量
- `XREAD BLOCK 0 STREAMS mystream $` 阻塞直到新条目到达（`$` = 最新 ID）
- 消费者组允许多个消费者协作处理一个 stream
- 使用 `XREADGROUP ... STREAMS key >` 读取新的未分配消息

## Bitmap 与 Bitfield

Bitmap 是被视为位数组的字符串。Bitfield 提供在位偏移量上对任意宽度整数的原子操作。

```
# Bitmap operations
SETBIT key offset value                # Set bit at offset                O(1)
GETBIT key offset                      # Get bit at offset                O(1)
BITCOUNT key [start end [BYTE|BIT]]    # Count set bits                   O(N)
BITPOS key bit [start [end [BYTE|BIT]]]  # Find first set/unset bit       O(N)
BITOP AND|OR|XOR|NOT dest key [key ...] # Bitwise operations              O(N)

# Bitfield operations
BITFIELD key [GET type offset] [SET type offset value] [INCRBY type offset increment] [OVERFLOW WRAP|SAT|FAIL]
```

## HyperLogLog

HyperLogLog 提供近似基数计数，标准误差约 0.81%，使用固定内存（约 12KB）。

```
PFADD key element [element ...]        # Add elements                     O(1)
PFCOUNT key [key ...]                  # Estimate unique count            O(1) per key
PFMERGE destkey sourcekey [sourcekey ...]  # Merge HyperLogLogs            O(N)
```

## Geospatial

Geospatial 命令在带有 GEO 特定包装的 Sorted Set 上操作。

```
GEOADD key [NX|XX] longitude latitude member [longitude latitude member ...]  # Add geo entry
GEOPOS key member [member ...]         # Get coordinates                  O(N)
GEODIST key member1 member2 [m|km|ft|mi]  # Distance between two members  O(log(N))
GEOHASH key member [member ...]        # Get geohash strings              O(N)
GEORADIUS key longitude latitude radius m|km|ft|mi [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count] [ASC|DESC]  # [Deprecated 6.2]
GEORADIUSBYMEMBER key member radius m|km|ft|mi [...]  # [Deprecated 6.2]
GEOSEARCH key [FROMMEMBER member|FROMLONLAT lon lat] [BYRADIUS radius m|km|ft|mi|BYBOX width height m|km|ft|mi] [ASC|DESC] [COUNT count [ANY]] [WITHCOORD] [WITHDIST] [WITHHASH]
GEOSEARCHSTORE dest key [...]          # Store search results             O(N)
```

**注意：** `GEORADIUS` 和 `GEORADIUSBYMEMBER` 已弃用。请改用 `GEOSEARCH`。

## 键操作

### 调试

```
DEBUG OBJECT key                       # Internal debug info (rl:refcount, lru, lru_seconds_idle, etc.)  O(1)
DEBUG SEGFAULT                        # Crash server (debugging only, never in production)
```

`DEBUG OBJECT` 返回内部元数据，如引用计数、LRU 空闲时间、编码和序列化长度。可用于诊断内存和逐出问题。

```
EXISTS key [key ...]                   # Check existence (returns count)   O(N) for multi
TYPE key                               # Data type (string|list|set|zset|hash|stream|none) O(1)
RENAME key newkey                      # Rename key                       O(1)
RENAMENX key newkey                    # Rename if target not exists      O(1)
COPY key newkey [DB db] [REPLACE]      # Copy key                        O(N)
DEL key [key ...]                      # Delete keys                      O(N)
UNLINK key [key ...]                   # Async delete (non-blocking)      O(1)
TOUCH key [key ...]                    # Update last access time          O(N)
MOVE key db                            # Move key to another database     O(1)
RANDOMKEY                              # Return a random key              O(1)

# Expiry
EXPIRE key seconds [NX|XX|GT|LT]      # Set TTL in seconds               O(1)
PEXPIRE key milliseconds [NX|XX|GT|LT]# Set TTL in ms                    O(1)
EXPIREAT key timestamp [NX|XX|GT|LT]  # Set expiry at Unix timestamp     O(1)
PEXPIREAT key ms-timestamp [NX|XX|GT|LT]  # Set expiry at ms-timestamp   O(1)
TTL key                                # Get TTL in seconds (-1=none, -2=not exists) O(1)
PTTL key                               # Get TTL in ms                    O(1)
EXPIRETIME key                         # Expiry as Unix timestamp         O(1)
PERSIST key                            # Remove expiry                    O(1)

# Object introspection
DUMP key                               # Serialize value                  O(N)
RESTORE key ttl serialized-value [REPLACE] [ABSTTL] [IDLETIME sec] [FREQ freq]  # Deserialize
OBJECT REFCOUNT key                    # Reference count                  O(1)
OBJECT ENCODING key                    # Internal encoding                O(1)
OBJECT IDLETIME key                    # Seconds since last access        O(1)
OBJECT FREQ key                        # Access frequency (LFU)           O(1)
MEMORY USAGE key [SAMPLES count]       # Memory in bytes                  O(N)
SORT key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC|DESC] [ALPHA] [STORE dest]
SORT_RO key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC|DESC] [ALPHA]  # Read-only sort (Redis 7.0+)
```

**过期选项说明：**
- `NX` — 仅当键没有过期时间时设置
- `XX` — 仅当键已有过期时间时设置
- `GT` — 仅当新 TTL 大于当前 TTL 时设置
- `LT` — 仅当新 TTL 小于当前 TTL 时设置

## 数据库操作

```
DBSIZE                                 # Total keys in database           O(1)
FLUSHDB [ASYNC|SYNC]                   # Delete all keys in current DB    O(N)
FLUSHALL [ASYNC|SYNC]                  # Delete all keys in all DBs       O(N)
SWAPDB index1 index2                   # Swap two databases               O(N)
SELECT index                           # Switch database                  O(1)
SCAN cursor [MATCH pattern] [COUNT count] [TYPE type]  # Incremental key iteration O(1)/call
```

## 事务

```
MULTI                                  # Start transaction
... commands ...
EXEC                                   # Execute all queued commands
DISCARD                                # Discard queued commands

WATCH key [key ...]                    # Watch keys for conditional exec
UNWATCH                                # Unwatch all keys
```

**行为说明：**
- `MULTI` 和 `EXEC` 之间的命令被排队并原子性执行
- 如果 `WATCH` 检测到被监视的键发生变化，`EXEC` 返回 nil（事务中止）
- Redis 事务不支持回滚 — 如果一条命令失败，其余命令仍会执行
