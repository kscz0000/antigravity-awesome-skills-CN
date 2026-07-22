---
title: "Cache"
description: "rclone cache 远程存储的文档"
versionIntroduced: "v1.39"
---

> **官方文档：** [https://rclone.org/cache/](https://rclone.org/cache/)
# Cache

`cache` 远程存储封装了另一个已存在的远程存储，并为 `rclone mount` 等长时间运行的任务存储文件结构及其数据。

它已被**弃用**，因此不推荐在新的安装中使用，并可能在某个时候被移除。

## 状态

cache 后端代码可以工作，但目前没有维护者，因此存在一些[未修复的 bug](https://github.com/rclone/rclone/issues?q=is%3Aopen+is%3Aissue+label%3Abug+label%3A%22Remote%3A+Cache%22)。

cache 后端最终将被淘汰，取而代之的是与 rclone 更紧密集成的 VFS 缓存层。

在此之前，我们建议仅在你发现离不开它时才使用 cache 后端。网上有许多文档描述使用 cache 后端来减少 API 调用，但这些文档大多已过时，在这些场景下 cache 后端不再需要了。

## 配置

要开始使用，你只需拥有一个可以用 `cache` 配置的已存在远程存储。

以下是如何创建一个名为 `test-cache` 的远程存储的示例。首先运行：

```console
rclone config
```

这将引导你完成交互式设置过程：

```text
No remotes found, make a new one?
n) New remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
n/r/c/s/q> n
name> test-cache
Type of storage to configure.
Choose a number from below, or type in your own value
[snip]
XX / Cache a remote
   \ "cache"
[snip]
Storage> cache
Remote to cache.
Normally should contain a ':' and a path, e.g. "myremote:path/to/dir",
"myremote:bucket" or maybe "myremote:" (not recommended).
remote> local:/test
Optional: The URL of the Plex server
plex_url> http://127.0.0.1:32400
Optional: The username of the Plex user
plex_username> dummyusername
Optional: The password of the Plex user
y) Yes type in my own password
g) Generate random password
n) No leave this optional password blank
y/g/n> y
Enter the password:
password:
Confirm the password:
password:
The size of a chunk. Lower value good for slow connections but can affect seamless reading.
Default: 5M
Choose a number from below, or type in your own value
 1 / 1 MiB
   \ "1M"
 2 / 5 MiB
   \ "5M"
 3 / 10 MiB
   \ "10M"
chunk_size> 2
How much time should object info (file size, file hashes, etc.) be stored in cache. Use a very high value if you don't plan on changing the source FS from outside the cache.
Accepted units are: "s", "m", "h".
Default: 5m
Choose a number from below, or type in your own value
 1 / 1 hour
   \ "1h"
 2 / 24 hours
   \ "24h"
 3 / 24 hours
   \ "48h"
info_age> 2
The maximum size of stored chunks. When the storage grows beyond this size, the oldest chunks will be deleted.
Default: 10G
Choose a number from below, or type in your own value
 1 / 500 MiB
   \ "500M"
 2 / 1 GiB
   \ "1G"
 3 / 10 GiB
   \ "10G"
chunk_total_size> 3
Remote config
--------------------
[test-cache]
remote = local:/test
plex_url = http://127.0.0.1:32400
plex_username = dummyusername
plex_password = *** ENCRYPTED ***
chunk_size = 5M
info_age = 48h
chunk_total_size = 10G
```

然后你可以这样使用它，

列出你的驱动器顶层的目录

```console
rclone lsd test-cache:
```

列出你的驱动器中的所有文件

```console
rclone ls test-cache:
```

启动一个带缓存的挂载

```console
rclone mount --allow-other test-cache: /var/tmp/test-cache
```

### 写入功能

### 离线上传

为了使通过 cache 写入更可靠，后端现在支持此功能，可以通过指定 `cache-tmp-upload-path` 来激活。

使用此功能时，文件会经历以下状态：

1. 上传开始（通常通过在 cache 远程存储上复制文件来启动）
2. 当复制到临时位置完成后，文件成为缓存远程存储的一部分，外观和行为与任何其他文件相同（包括读取）
3. 在 `cache-tmp-wait-time` 过去后且文件排在队列首位时，使用 `rclone move` 将文件移动到云存储提供商
4. 上传期间仍然可以读取文件，但大多数修改操作将被禁止
5. 移动完成后，文件解锁以允许修改，变得与任何其他常规文件一样
6. 如果文件在通过 `cache` 读取时实际已从临时路径删除，则 `cache` 将直接将源切换到云存储提供商，而不会中断读取（不过可能会有短暂中断）

文件按顺序上传，同一时间只上传一个文件。上传将存储在队列中，并根据添加顺序处理。队列和临时存储在重启后持久保留，但可以在启动时使用 `--cache-db-purge` 标志清除。

### 写入支持

通过 `cache` 支持写入。一个注意事项是，挂载的 cache 远程存储不会为上传操作添加任何重试或回退机制。这将取决于被封装远程存储的实现。考虑使用 `离线上传` 来实现可靠的写入。

一个特殊情况由 `cache-writes` 覆盖，启用时会在上传的同时缓存文件数据，使上传完成后立即可以从缓存存储中获取。

### 读取功能

#### 多连接

为应对运行 rclone 的本地 PC 与云存储提供商之间的高延迟，cache 远程存储可以将多个请求拆分为对云存储提供商的较小文件块请求，并在本地合并，使数据几乎可以在读取器需要之前立即可用。

这类似于在线播放媒体文件时的缓冲。rclone 会停留在当前标记附近，但始终尽最大努力保持提前并预先准备数据。

#### Plex 集成

与 Plex 有直接集成，允许 cache 在读取期间检测文件是否正在播放。这帮助 cache 根据需要调整对云存储提供商的查询方式。

扫描时将使用最少数量的工作线程（1），而在确认播放期间，cache 将部署配置数量的工作线程。

此集成为未来将探索的额外性能改进打开了大门。

**注意：** 如果未配置 Plex 选项，`cache` 将以其配置的选项运行，不会调整任何设置。

如何启用？运行 `rclone config` 并在你的远程存储中添加所有 Plex 选项（端点、用户名和密码），它将自动启用。

受影响的设置：

- `cache-workers`：确认播放期间使用*配置值*，其他所有时间使用 *1*

##### 证书验证

当 Plex 服务器配置为仅接受安全连接时，可以使用 `.plex.direct` URL 来确保证书验证成功。这些 URL 由 Plex 内部用于安全连接到 Plex 服务器。

这些 URL 的格式如下：

`https://ip-with-dots-replaced.server-hash.plex.direct:32400/`

`ip-with-dots-replaced` 部分可以是任何 IPv4 地址，其中点号替换为短横线，例如 `127.0.0.1` 变为 `127-0-0-1`。

要获取 `server-hash` 部分，最简单的方法是访问

<https://plex.tv/api/resources?includeHttps=1&X-Plex-Token=your-plex-token>

此页面将列出你账户的所有可用 Plex 服务器，每台服务器至少有一个 `.plex.direct` 链接。复制一个 URL 并将 IP 地址替换为所需地址。这可以用作 `plex_url` 值。

### 已知问题

#### 挂载与 --dir-cache-time

--dir-cache-time 控制在挂载层工作的第一级目录缓存。作为与 `cache` 后端独立的缓存机制，它将根据配置的时间管理自己的条目。

为避免出现目录缓存有过时数据而 cache 有正确数据的情况，尝试将 `--dir-cache-time` 设为比 `--cache-info-age` 更短的时间。默认值已按此方式配置。

#### Windows 支持 - 实验性

Windows `mount` 功能仍有一些需要调查的问题。目前应将其视为实验性的，对此操作系统的修复正在陆续推出。

大多数问题似乎与 Linux 各发行版和 Windows 之间文件系统的差异有关，因为 cache 严重依赖文件系统。

非常欢迎任何关于 cache 在此操作系统上行为的报告或反馈。

- [Issue #1935](https://github.com/rclone/rclone/issues/1935)
- [Issue #1907](https://github.com/rclone/rclone/issues/1907)
- [Issue #1834](https://github.com/rclone/rclone/issues/1834)

#### 限流风险

cache 后端的未来迭代将利用云存储提供商的连接池功能来同步，同时使通过它写入更能容忍故障。

有几项增强功能正在跟踪中，以添加这些功能，但与此同时，一个合理的担忧是：过期的缓存列表可能导致云存储提供商对非常大的挂载的重复查询进行限流或封禁。

一些建议：

- 不要为条目信息使用非常短的间隔（`--cache-info-age`）
- 虽然写入尚未优化，但你仍然可以通过 `cache` 写入，这给了你同时将文件添加到缓存的优势（如果配置为这样做）。

未来的增强：

- [Issue #1937](https://github.com/rclone/rclone/issues/1937)
- [Issue #1936](https://github.com/rclone/rclone/issues/1936)

#### cache 与 crypt

一个常见场景是使用 `crypt` 远程存储在云存储提供商上加密保存数据。`crypt` 使用类似的技术封装现有远程存储，并无缝处理此转换。

按以下顺序封装远程存储存在一个问题：
**避免：** cloud remote -> crypt -> cache

在测试中，按此顺序排列时我遇到了很多封禁。我怀疑这可能与 crypt 在云存储提供商上打开文件的方式有关，使它认为我们在下载完整文件而不是小块数据。按此顺序组织远程存储会产生更好的结果：
**推荐：** cloud remote -> cache -> crypt

#### 绝对远程路径

`cache` 无法区分被封装远程存储的相对路径和绝对路径。在 `remote` 配置设置和命令行中给出的任何路径都将原样传递给被封装远程存储，但在磁盘上存储块数据时，路径将通过移除前导 `/` 字符变为相对路径。

此行为对大多数后端类型无关紧要，但有些后端中前导 `/` 会改变有效目录，例如在 `sftp` 后端中，以 `/` 开头的路径相对于 SSH 服务器的根目录，而不以 `/` 开头的路径相对于用户主目录。因此 `sftp:bin` 和 `sftp:/bin` 将共享同一个缓存文件夹，即使它们在 SSH 服务器上代表不同的目录。

### Cache 与远程控制 (--rc)

Cache 支持 rclone 中新的 `--rc` 模式，可以通过以下端点进行远程控制：默认情况下，如果你不添加该标志，监听器是禁用的。

### rc cache/expire

从缓存后端清除一个远程存储。支持目录或文件。如果 cache 被 crypt 封装，它同时支持加密和未加密的文件名。

参数：

- **remote** = 远程存储路径 **（必填）**
- **withData** = true/false 是否同时删除缓存数据（块数据） *（可选，默认为 false）*

<!-- autogenerated options start - DO NOT EDIT - instead edit fs.RegInfo in backend/cache/cache.go and run make backenddocs to verify --> <!-- markdownlint-disable-line line-length -->
### 标准选项

以下是 cache（缓存远程存储）特有的标准选项。

#### --cache-remote

要缓存的远程存储。

通常应包含一个 ':' 和一个路径，例如 "myremote:path/to/dir"、"myremote:bucket" 或 "myremote:"（不推荐）。

Properties:

- Config:      remote
- Env Var:     RCLONE_CACHE_REMOTE
- Type:        string
- Required:    true

#### --cache-plex-url

Plex 服务器的 URL。

Properties:

- Config:      plex_url
- Env Var:     RCLONE_CACHE_PLEX_URL
- Type:        string
- Required:    false

#### --cache-plex-username

Plex 用户的用户名。

Properties:

- Config:      plex_username
- Env Var:     RCLONE_CACHE_PLEX_USERNAME
- Type:        string
- Required:    false

#### --cache-plex-password

Plex 用户的密码。

**注意** 输入必须经过混淆处理 — 参见 [rclone obscure](/commands/rclone_obscure/)。

Properties:

- Config:      plex_password
- Env Var:     RCLONE_CACHE_PLEX_PASSWORD
- Type:        string
- Required:    false

#### --cache-chunk-size

块的大小（部分文件数据）。

较慢的连接使用较小的值。如果更改了块大小，任何已下载的块将失效，需要清除 cache-chunk-path，否则会出现意外的 EOF 错误。

Properties:

- Config:      chunk_size
- Env Var:     RCLONE_CACHE_CHUNK_SIZE
- Type:        SizeSuffix
- Default:     5Mi
- Examples:
  - "1M"
    - 1 MiB
  - "5M"
    - 5 MiB
  - "10M"
    - 10 MiB

#### --cache-info-age

缓存文件结构信息（目录列表、文件大小、时间等）的时长。

如果所有写操作都通过缓存进行，则可以安全地将此值设得很大，因为缓存存储也会实时更新。

Properties:

- Config:      info_age
- Env Var:     RCLONE_CACHE_INFO_AGE
- Type:        Duration
- Default:     6h0m0s
- Examples:
  - "1h"
    - 1 小时
  - "24h"
    - 24 小时
  - "48h"
    - 48 小时

#### --cache-chunk-total-size

块数据在本地磁盘上可占用的总大小。

如果缓存超过此值，则将开始删除最旧的块数据，直到低于此值。

Properties:

- Config:      chunk_total_size
- Env Var:     RCLONE_CACHE_CHUNK_TOTAL_SIZE
- Type:        SizeSuffix
- Default:     10Gi
- Examples:
  - "500M"
    - 500 MiB
  - "1G"
    - 1 GiB
  - "10G"
    - 10 GiB

### 高级选项

以下是 cache（缓存远程存储）特有的高级选项。

#### --cache-plex-token

用于认证的 Plex 令牌 — 通常自动设置。

Properties:

- Config:      plex_token
- Env Var:     RCLONE_CACHE_PLEX_TOKEN
- Type:        string
- Required:    false

#### --cache-plex-insecure

连接到 Plex 服务器时跳过所有证书验证。

Properties:

- Config:      plex_insecure
- Env Var:     RCLONE_CACHE_PLEX_INSECURE
- Type:        string
- Required:    false

#### --cache-db-path

存储文件结构元数据 DB 的目录。

远程存储名称用作 DB 文件名。

Properties:

- Config:      db_path
- Env Var:     RCLONE_CACHE_DB_PATH
- Type:        string
- Default:     "$HOME/.cache/rclone/cache-backend"

#### --cache-chunk-path

缓存块文件的目录。

部分文件数据（块）在本地存储的路径。远程存储名称将附加到最终路径。

此配置跟随 "--cache-db-path"。如果你为 "--cache-db-path" 指定了自定义位置但没有为 "--cache-chunk-path" 指定，则 "--cache-chunk-path" 将使用与 "--cache-db-path" 相同的路径。

Properties:

- Config:      chunk_path
- Env Var:     RCLONE_CACHE_CHUNK_PATH
- Type:        string
- Default:     "$HOME/.cache/rclone/cache-backend"

#### --cache-db-purge

启动时清除此远程存储的所有缓存数据。

Properties:

- Config:      db_purge
- Env Var:     RCLONE_CACHE_DB_PURGE
- Type:        bool
- Default:     false

#### --cache-chunk-clean-interval

缓存执行块存储清理的频率。

默认值对大多数人来说应该没问题。如果你发现缓存频繁超过 "cache-chunk-total-size"，则尝试降低此值以强制更频繁地执行清理。

Properties:

- Config:      chunk_clean_interval
- Env Var:     RCLONE_CACHE_CHUNK_CLEAN_INTERVAL
- Type:        Duration
- Default:     1m0s

#### --cache-read-retries

从缓存存储读取时重试的次数。

由于从缓存流读取与下载文件数据是独立的，读取器可能会到达缓存中没有更多数据的位置。大多数情况下，如果缓存无法再提供文件数据，这可能表示连接问题。

对于非常慢的连接，将此值增加到流能够提供数据的程度，但体验会非常卡顿。

Properties:

- Config:      read_retries
- Env Var:     RCLONE_CACHE_READ_RETRIES
- Type:        int
- Default:     10

#### --cache-workers

并行下载块数据的工作线程数。

较高的值意味着更多的并行处理（需要更好的 CPU）和对云存储提供商更多的并发请求。这会影响多个方面，如云存储提供商 API 限制、运行 rclone 的硬件上的更大压力，但也意味着流将更流畅，数据对读取器来说将更快可用。

**注意**：如果启用了可选的 Plex 集成，则此设置将根据执行的读取类型进行调整，此处指定的值将用作最大工作线程数。

Properties:

- Config:      workers
- Env Var:     RCLONE_CACHE_WORKERS
- Type:        int
- Default:     4

#### --cache-chunk-no-memory

禁用流式传输期间存储块的内存缓存。

默认情况下，cache 在流式传输期间也会将文件数据保留在 RAM 中，以尽可能快地提供给读取器。

此临时数据在被读取后即被逐出，且存储的块数不超过工作线程数。然而，根据其他设置（如 "cache-chunk-size" 和 "cache-workers"），如果有并行流（同时读取多个文件），此内存占用可能会增加。

如果硬件允许，使用此功能可在流式传输期间提供更好的整体性能，但如果本地机器上 RAM 不足，也可以禁用。

Properties:

- Config:      chunk_no_memory
- Env Var:     RCLONE_CACHE_CHUNK_NO_MEMORY
- Type:        bool
- Default:     false

#### --cache-rps

限制对源文件系统的每秒请求数（-1 禁用）。

此设置对 cache 向云存储提供商远程发出的每秒请求数施加硬性限制，并尝试通过在读取之间设置等待来遵守该值。

如果你发现通过 cache 在云存储提供商上被禁止或限制，并且知道较小的每秒请求数可以让你正常工作，则可以使用此设置。

所有其他设置的良好平衡应使此设置无用，但它可用于更特殊的情况。

**注意**：这将限制流式传输期间的请求数，但对云存储提供商的其他 API 调用（如目录列表）仍将正常通过。

Properties:

- Config:      rps
- Env Var:     RCLONE_CACHE_RPS
- Type:        int
- Default:     -1

#### --cache-writes

通过文件系统写入时缓存文件数据。

如果你需要在上传文件后立即通过 cache 读取它们，可以启用此标志，使数据在上传期间同时存储到缓存存储中。

Properties:

- Config:      writes
- Env Var:     RCLONE_CACHE_WRITES
- Type:        bool
- Default:     false

#### --cache-tmp-upload-path

保留临时文件直到上传的目录。

这是 cache 用作需要上传到云存储提供商的新文件临时存储的路径。

指定值将启用此功能。不指定则完全禁用，文件将直接上传到云存储提供商。

Properties:

- Config:      tmp_upload_path
- Env Var:     RCLONE_CACHE_TMP_UPLOAD_PATH
- Type:        string
- Required:    false

#### --cache-tmp-wait-time

文件在上传前应在本地缓存中存储多长时间。

这是文件在被选中上传之前必须在临时位置 _cache-tmp-upload-path_ 中等待的时长。

注意，同一时间只上传一个文件，如果为此目的形成了队列，上传可能需要更长时间才能开始。

Properties:

- Config:      tmp_wait_time
- Env Var:     RCLONE_CACHE_TMP_WAIT_TIME
- Type:        Duration
- Default:     15s

#### --cache-db-wait-time

等待 DB 可用的时长 — 0 为无限等待。

同一时间只有一个进程可以打开 DB，因此 rclone 在报错之前会等待此时长以等待 DB 变为可用。

如果设为 0，则将无限等待。

Properties:

- Config:      db_wait_time
- Env Var:     RCLONE_CACHE_DB_WAIT_TIME
- Type:        Duration
- Default:     1s

#### --cache-description

远程存储的描述。

Properties:

- Config:      description
- Env Var:     RCLONE_CACHE_DESCRIPTION
- Type:        string
- Required:    false

## 后端命令

以下是 cache 后端特有的命令。

运行方式：

```console
rclone backend COMMAND remote:
```

下面的帮助将解释每个命令接受什么参数。

参见 [backend](/commands/rclone_backend/) 命令获取更多关于如何传递选项和参数的信息。

这些可以在运行中的后端上使用 rc 命令 [backend/command](/rc/#backend-command) 来运行。

### stats

以 JSON 格式打印缓存后端的统计信息。

```console
rclone backend stats remote: [options] [<arguments>+]
```

<!-- autogenerated options stop -->
