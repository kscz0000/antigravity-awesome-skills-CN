# 高级功能

## 目录

- [Lua 脚本](#lua-脚本)
- [Pub/Sub 模式](#pubsub-模式)
- [管道模式](#管道模式)
- [CSV 和 JSON 输出](#csv-和-json-输出)
- [从其他程序获取输入](#从其他程序获取输入)
- [集群管理](#集群管理)

## Lua 脚本

Redis 支持服务端 Lua 脚本用于原子性多命令操作。

### 运行脚本

```bash
# Run script from file with --eval
redis-cli --eval /tmp/script.lua key1 key2 , arg1 arg2 arg3

# The comma separates KEYS[] from ARGV[]:
# key1, key2 → KEYS[1], KEYS[2]
# arg1, arg2, arg3 → ARGV[1], ARGV[2], ARGV[3]

# Inline EVAL
redis-cli EVAL "return redis.call('SET', KEYS[1], ARGV[1])" 1 mykey myvalue

# EVALSHA (use SHA1 hash of cached script)
redis-cli EVALSHA <sha1> numkeys key [key ...] arg [arg ...]
```

### Lua 脚本示例

```lua
-- Conditional SET (only if value matches)
local current = redis.call('GET', KEYS[1])
if current == ARGV[1] then
  return redis.call('SET', KEYS[1], ARGV[2])
end
return nil

-- Atomic counter reset
local old = redis.call('GET', KEYS[1])
redis.call('SET', KEYS[1], ARGV[1])
return old

-- Multi-key operation
local results = {}
for i = 1, #KEYS do
  results[i] = redis.call('GET', KEYS[i])
end
return results
```

### Lua 调试器

```bash
# Enable debugger (--ldb)
redis-cli --ldb --eval /tmp/script.lua key1 , arg1

# Synchronous mode (blocks server — for debugging only)
redis-cli --ldb-sync-mode --eval /tmp/script.lua key1 , arg1
```

**异步模式**（默认）：调试期间服务器继续服务其他客户端。脚本更改在调试后从服务器内存回滚。

**同步模式**：服务器被阻塞。脚本更改持久化在服务器内存中。仅在开发环境使用。

### 脚本管理

```bash
redis-cli SCRIPT EXISTS sha1 [sha1 ...]    # Check if scripts are cached
redis-cli SCRIPT FLUSH [ASYNC|SYNC]        # Clear script cache
redis-cli SCRIPT LOAD script               # Cache script, return SHA1
redis-cli SCRIPT KILL                      # Kill running script (only if no write)
```

### Function API（Redis 7.0+）

Function 是脚本的持久化替代方案：

```bash
redis-cli FUNCTION LOAD "redis.register_function('myfunc', function(keys, args) ... end)"
redis-cli FCALL myfunc 0 arg1 arg2
redis-cli FUNCTION LIST
redis-cli FUNCTION DELETE myfunc
redis-cli FUNCTION FLUSH [ASYNC|SYNC]
redis-cli FUNCTION DUMP                    # Serialize all functions
redis-cli FUNCTION RESTORE serialized-data # Restore functions
```

## Pub/Sub 模式

redis-cli 可以发布和订阅 Redis Pub/Sub 频道。

### 订阅

```bash
# Subscribe to specific channels
redis-cli SUBSCRIBE channel1 channel2

# Pattern subscription
redis-cli PSUBSCRIBE '*'

# Read published messages (blocks until Ctrl-C)
# Output format:
# 1) "pmessage"    — message type
# 2) "*"           — pattern matched
# 3) "mychannel"   — channel name
# 4) "mymessage"   — message content
```

### 发布

```bash
redis-cli PUBLISH mychannel "Hello World"
```

### 检查 Pub/Sub

```bash
redis-cli PUBSUB CHANNELS [pattern]        # List active channels
redis-cli PUBSUB NUMSUB [channel ...]       # Subscriber count per channel
redis-cli PUBSUB NUMPAT                     # Pattern subscription count
redis-cli PUBSUB SHARDCHANNELS [pattern]    # List shard channels
redis-cli PUBSUB SHARDNUMSUB [channel ...]  # Shard channel subscriber count
```

### 分片 Pub/Sub（Redis 7.0+）

分片 Pub/Sub 将消息路由到拥有频道槽的集群节点，提供更好的可扩展性：

```bash
redis-cli SSUBSCRIBE shardchannel
redis-cli SUNSUBSCRIBE shardchannel
redis-cli SPUBLISH shardchannel "message"
```

## 管道模式

从 stdin 传输原始 Redis 协议到服务器。这是批量插入数据最快的方式。

```bash
# Basic pipe mode
cat data.protocol | redis-cli --pipe

# Custom timeout (seconds)
cat data.protocol | redis-cli --pipe --pipe-timeout 60

# Zero timeout (wait forever)
cat data.protocol | redis-cli --pipe --pipe-timeout 0
```

### 协议格式

管道文件中的每条命令必须使用 Redis 协议：

```
*<number-of-arguments>\r\n
$<length-of-argument>\r\n
<argument-data>\r\n
```

示例 — `SET mykey myvalue`：
```
*3\r\n$3\r\nSET\r\n$5\r\nmykey\r\n$7\r\nmyvalue\r\n
```

管道模式比逐条命令快得多，因为它批量处理网络往返。有关生成协议文件，请参阅[批量插入指南](https://redis.io/docs/latest/develop/clients/patterns/bulk-loading/)。

## CSV 和 JSON 输出

### CSV 输出

用于数据导出的单命令 CSV 输出：

```bash
redis-cli --csv LRANGE mylist 0 -1
# "d","c","b","a"

redis-cli --csv HGETALL user:1
# "name","Alice","age","30"
```

**注意：** `--csv` 按命令工作，不适用于导出整个数据库。

### JSON 输出

使用 RESP3 协议的 JSON 输出：

```bash
# JSON output (uses RESP3 by default)
redis-cli --json HGETALL user:1
# {"name": "Alice", "age": "30"}

# Use with RESP2 if needed
redis-cli --json -2 HGETALL user:1

# ASCII-safe quoted strings (no Unicode)
redis-cli --quoted-json GET mykey
```

### 管道命令到其他工具

```bash
# Format and filter output
redis-cli --raw GET mykey | jq .

# Export to file
redis-cli --csv LRANGE mylist 0 -1 > output.csv

# Use with grep
redis-cli MONITOR | grep "SET"
```

## 从其他程序获取输入

### 从 stdin 读取最后一个参数（-x）

```bash
# Set key to contents of a file
cat /etc/services | redis-cli -x SET net_services

# Check the stored value
redis-cli GETRANGE net_services 0 50
```

### 从 stdin 读取标记参数（-X）

```bash
# Dump and restore a key atomically
redis-cli -D "" --raw dump mykey > /tmp/mykey.dump
redis-cli -X dump_tag restore mykey2 0 dump_tag replace < /tmp/mykey.dump
```

### 管道多条命令

```bash
# Execute commands from a text file
cat /tmp/commands.txt | redis-cli

# commands.txt format (one command per line):
# SET item:3374 100
# INCR item:3374
# APPEND item:3374 xxx
# GET item:3374
```

### 持续输入数据

```bash
# Generate keys continuously
while true; do
  echo "SET timestamp:$(date +%s) $(date -Iseconds)"
done | redis-cli --pipe
```

## 集群管理

redis-cli 通过 `--cluster` 子命令提供内置集群管理，以及用于底层控制的直接集群命令。

### redis-cli 集群操作

```bash
# Create a new cluster (interactive prompts for replication)
redis-cli --cluster create host1:port1 host2:port2 host3:port3 --cluster-replicas 1

# Check cluster state
redis-cli --cluster check host1:port1

# Show cluster info
redis-cli --cluster info host1:port1

# Reshard (move slots between nodes)
redis-cli --cluster reshard host1:port1 --cluster-from <node-id> --cluster-to <node-id> --cluster-slots <n>

# Rebalance slots across all nodes
redis-cli --cluster rebalance host1:port1

# Add a node to the cluster
redis-cli --cluster add-node new-host:new-port existing-host:existing-port
# As replica:
redis-cli --cluster add-node new-host:new-port existing-host:existing-port --cluster-slave --cluster-master-id <id>

# Remove a node
redis-cli --cluster del-node host:port <node-id>

# Fix cluster issues (missing slots, etc.)
redis-cli --cluster fix host:port

# Execute command on all cluster nodes
redis-cli --cluster call host:port <command>

# List all --cluster subcommands
redis-cli --cluster help
```

使用 `-c` 标志在 redis-cli 中启用集群模式（自动跟随 `-ASK` 和 `-MOVED` 重定向）：

```bash
redis-cli -c -h cluster-node -p 6379
```

### 集群命令（直接）

```bash
# Cluster state and topology
redis-cli CLUSTER INFO                        # Cluster state overview (O(1))
redis-cli CLUSTER NODES                       # Full node topology (O(N))
redis-cli CLUSTER SHARDS                      # Shard/node mapping (O(N), Redis 7.0+)

# Slot management
redis-cli CLUSTER KEYSLOT key                 # Hash slot for a key (O(1))
redis-cli CLUSTER ADDSLOTS slot [slot ...]    # Assign slots to node (O(N))
redis-cli CLUSTER DELSLOTS slot [slot ...]    # Unbind slots (O(N))
redis-cli CLUSTER SETSLOT slot IMPORTING|node-id|MIGRATING|STABLE  # Slot migration (O(1))

# Node management
redis-cli CLUSTER MEET ip port [bus-port]     # Join cluster (O(1))
redis-cli CLUSTER FORGET node-id              # Remove node (O(1))
redis-cli CLUSTER REPLICATE node-id           # Become replica of node (O(1))
redis-cli CLUSTER RESET [HARD|SOFT]           # Reset cluster state (O(N))

# Failover
redis-cli CLUSTER FAILOVER [FORCE|TAKEOVER]   # Manual failover (O(1))
redis-cli CLUSTER SAVECONFIG                  # Save config to disk (O(1))

# Node identification
redis-cli CLUSTER MYID                        # Current node ID (O(1))
redis-cli CLUSTER MYSHARDID                   # Current shard ID (O(1))
```

**行为说明：**
- Redis Cluster 有 16384 个哈希槽分布在主节点上
- `CLUSTER SLOTS` 自 Redis 7.0 起已弃用 — 请改用 `CLUSTER SHARDS`
- 交互模式中使用 `redis-cli -c` 实现透明集群重定向
- `CLUSTER FORGET` 在 Redis 7.2+ 中通过 gossip 自动传播
