# 连接与 CLI 选项

## 目录

- [连接方式](#连接方式)
- [CLI 标志参考](#cli-标志参考)
- [环境变量](#环境变量)
- [SSL/TLS 配置](#ssltls-配置)
- [交互模式](#交互模式)
- [字符串引号与转义](#字符串引号与转义)

## 连接方式

### 基本连接

默认情况下，redis-cli 连接到 `127.0.0.1:6379`，不使用密码。

```bash
# Default connection
redis-cli

# Custom host and port
redis-cli -h redis15.localnet.org -p 6390 PING

# Password authentication
redis-cli -a myUnguessablePazzzzzword123 PING

# ACL-style authentication (Redis 6+)
redis-cli --user admin --pass myPassword PING

# Specific database number
redis-cli -n 2 DBSIZE
```

### URI 连接

```bash
# Full URI format
redis-cli -u redis://user:password@host:port/dbnum PING

# Without username (use "default")
redis-cli -u redis://default:password@localhost:6379/0 PING

# TLS scheme
redis-cli -u rediss://default:password@redis.example.com:6380/0 PING

# Minimal URI
redis-cli -u redis://localhost:6379 PING
```

URI 中的用户名、密码和数据库编号是可选的。使用 TLS 时，请使用 `rediss://` 方案。

### IPv4/IPv6 优先

```bash
redis-cli -4 PING   # Prefer IPv4
redis-cli -6 PING   # Prefer IPv6
```

## CLI 标志参考

```
Usage: redis-cli [OPTIONS] [cmd [arg [arg ...]]]

Connection:
  -h <hostname>      Server hostname (default: 127.0.0.1)
  -p <port>          Server port (default: 6379)
  -t <timeout>       Connection timeout in seconds (decimals allowed, default: 0 = no limit)
  -s <socket>        Unix socket (overrides hostname and port)
  -a <password>      Password (also via REDISCLI_AUTH env var)
  --user <username>  ACL username (requires -a)
  --pass <password>  Alias of -a
  --askpass          Prompt for password from STDIN (ignores -a and REDISCLI_AUTH)
  -u <uri>           Connection URI: redis://user:password@host:port/dbnum
  -n <db>            Database number

Protocol:
  -2                 Start in RESP2 protocol mode
  -3                 Start in RESP3 protocol mode

Execution:
  -r <repeat>        Execute command N times (-1 for infinite)
  -i <interval>      Seconds between repeated commands (supports decimals like 0.1)
                     Also used in --scan, --stat, --bigkeys, --memkeys, --keystats
  -x                 Read last argument from STDIN
  -X <tag>           Read tagged argument from STDIN

Output:
  --raw              Raw output (no type prefixes, default when not TTY)
  --no-raw           Force human-readable output even when piping
  --csv              CSV output format
  --json             JSON output (default RESP3, use -2 for RESP2)
  --quoted-json      JSON with ASCII-safe quoted strings
  -d <delimiter>     Delimiter between response bulks in raw mode (default: \n)
  -D <delimiter>     Delimiter between responses in raw mode (default: \n)

Cluster:
  -c                 Enable cluster mode (follow -ASK and -MOVED redirections)

Behavior:
  -e                 Return non-zero exit code on command failure
  --verbose          Verbose output
  --no-auth-warning  Suppress password-on-CLI warning
  --quoted-input     Force input handling as quoted strings
  --show-pushes <yn> Print RESP3 PUSH messages (default: yes in TTY)

Special Modes:
  --stat             Continuous server stats
  --latency          Continuous latency sampling
  --latency-history  Latency tracking over time (15s windows, change with -i)
  --latency-dist     Latency spectrum visualization (requires xterm 256 colors)
  --lru-test <keys>  Simulate LRU cache workload
  --replica          Simulate replica, show commands from master
  --rdb <filename>   Transfer RDB dump from remote server
  --functions-rdb <filename>  RDB dump with functions only
  --pipe             Transfer raw Redis protocol from stdin
  --pipe-timeout <n> Pipe mode timeout in seconds (default: 30, 0 = forever)
  --bigkeys          Scan for keys with many elements
  --memkeys          Scan for keys consuming memory
  --memkeys-samples <n>  Memory sampling count
  --keystats         Combined bigkeys + memkeys with distribution
  --keystats-samples <n> Key stats sampling count
  --hotkeys          Find hot keys (requires *lfu maxmemory-policy)
  --scan             List keys using SCAN
  --pattern <pat>    Pattern for --scan, --bigkeys, --memkeys, --keystats, --hotkeys
  --quoted-pattern <pat>  Same as --pattern, but accepts quoted binary-safe strings
  --count <count>    COUNT hint for scan operations
  --cursor <n>       Start scan at cursor (after Ctrl-C)
  --top <n>          Display top N key sizes (default: 10, with --keystats)
  --intrinsic-latency <sec>  Measure system baseline latency
  --eval <file>      Execute Lua script
  --ldb              Enable Lua debugger with --eval
  --ldb-sync-mode    Synchronous Lua debugger (blocks server)
  --cluster <cmd>    Cluster management command

Examples:
  redis-cli -u redis://default:PASSWORD@localhost:6379/0
  cat /etc/passwd | redis-cli -x set mypasswd
  redis-cli -D "" --raw dump key > key.dump && redis-cli -X dump_tag restore key2 0 dump_tag replace < key.dump
  redis-cli -r 100 lpush mylist x
  redis-cli -r 100 -i 1 info | grep used_memory_human:
  redis-cli --eval myscript.lua key1 key2 , arg1 arg2 arg3
```

## 环境变量

| 变量 | 用途 |
|------|------|
| `REDISCLI_AUTH` | 认证密码（优先于 `-a` 标志） |
| `REDISCLI_HISTFILE` | 自定义历史文件路径（默认：`~/.rediscli_history`，设为 `/dev/null` 禁用） |
| `REDISCLI_RCFILE` | 自定义偏好文件路径（默认：`~/.redisclirc`） |
| `HOME` | `.rediscli_history` 和 `.redisclirc` 的基础目录 |

**安全提示**：始终优先使用 `REDISCLI_AUTH` 而非 `-a <password>`。`-a` 标志会在 shell 历史记录和进程列表（`ps aux`）中暴露密码。

## SSL/TLS 配置

```bash
# Enable TLS with trusted CA
redis-cli --tls --cacert /path/to/ca.crt -h redis.example.com PING

# CA certificate directory
redis-cli --tls --cacertdir /etc/ssl/certs -h redis.example.com PING

# Client certificate authentication (mutual TLS)
redis-cli --tls --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -h redis.example.com PING
```

## 交互模式

### 启动

不带参数运行 `redis-cli` 进入交互模式：

```
$ redis-cli
127.0.0.1:6379> PING
PONG
```

提示符显示 `host:port[db_number]`，切换数据库或连接到其他服务器时会更新。

### 连接管理

```
CONNECT <host> <port>    # Connect to different instance
SELECT <db>              # Switch database (prompt updates to show db number)
QUIT                     # Exit redis-cli
```

断开连接时，redis-cli 自动尝试重新连接。它会重新选择上次的数据库，但会丢失其他状态（如 MULTI/EXEC 事务）。

### 编辑与历史

- **行编辑**：内置 linenoise 库 — 无外部依赖
- **历史记录**：上下箭头键访问之前的命令。存储在 `~/.rediscli_history`
- **Tab 补全**：按 TAB 补全命令名称
- **语法提示**：输入命令名称后显示（用 `:set hints` / `:set nohints` 切换）
- **反向搜索**：`Ctrl+R` 搜索历史

### 偏好设置

通过交互模式中的 `:set` 命令或 `~/.redisclirc` 设置：

```
:set hints          # Enable syntax hints
:set nohints        # Disable syntax hints
```

### 帮助系统

```
HELP @<category>     # Show all commands in a category
HELP <command>       # Show help for a specific command

# Available categories:
# @generic, @string, @list, @set, @sorted_set, @hash,
# @pubsub, @transactions, @connection, @server, @scripting,
# @hyperloglog, @cluster, @geo, @stream
```

### 屏幕控制

```
CLEAR               # Clear terminal screen
```

### 重复命令

在命令前加数字以重复执行：

```
5 INCR mycounter    # Execute INCR mycounter 5 times
```

## 字符串引号与转义

当字符串值包含空格或不可打印字符时，使用引号：

**双引号字符串**支持转义序列：
- `\"` `\\` `\n` `\r` `\t` `\b` `\a` `\xhh`（十六进制）

**单引号字符串**为字面值，仅转义：
- `\'` `\\`

```
SET mykey "Hello\nWorld"           # Two lines: Hello / World
GET mykey
# Hello
# World

AUTH user ">^8T>6Na{u|jp>+v\"55\@_"  # Escaped quotes in password
```

当输出目标不是终端时，redis-cli 自动使用原始输出模式（无 `(integer)` 等类型前缀）。可用 `--raw` 或 `--no-raw` 强制切换。
