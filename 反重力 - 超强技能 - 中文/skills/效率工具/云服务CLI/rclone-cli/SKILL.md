---
name: rclone-cli
description: rclone 命令行云存储管理工具的参考与使用指南。涉及 rclone，或任何基于终端的云文件操作任务（如上传、下载、同步、复制、移动、挂载或远程管理）时使用本技能。触发词：S3 兼容存储、AWS、Azure、OneDrive、Google Drive、Dropbox、mount、sync、copy、crypt、bisync、cron 备份。
risk: unknown
source: https://github.com/chaunsin/agent-skills/tree/master/skills/rclone-cli
source_repo: chaunsin/agent-skills
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/chaunsin/agent-skills/blob/master/LICENSE
---

# rclone — 云存储的瑞士军刀
## 适用场景

需要 rclone 命令行云存储管理工具的参考与使用指南时使用本技能。涉及 rclone，或任何基于终端的云文件操作任务（如上传、下载、同步、复制、移动、挂载或远程管理）时即触发。触发词：S3 兼容存储、AWS、Azure、OneDrive、Google Drive、Dropbox、mount、sync、copy、crypt、bisync、cron 备份。


Rclone 是一个用于管理云存储文件的命令行程序，是云厂商网页存储界面的功能丰富替代品。已有超过 70 款云存储产品支持 rclone，涵盖 S3 对象存储、企业与个人文件存储服务以及标准传输协议。

Rclone 提供与 Unix 命令 rsync、cp、mv、mount、ls、ncdu、tree、rm、cat 对应的强大云端等价物。它始终保留时间戳并校验校验和，可在最近一个完整文件处断点续传。

**官方资源：** [rclone.org](https://rclone.org/) | [文档](https://rclone.org/docs/) | [命令](https://rclone.org/commands/) | [安装](https://rclone.org/install/) | [论坛](https://forum.rclone.org/) | [GitHub](https://github.com/rclone/rclone)

## 环境准备

使用 rclone 前，先确认已安装：

```bash
# Check if rclone is installed
rclone --version

# If not found, run the install script:
# See scripts/install.sh in this skill's directory
sudo -v ; curl https://rclone.org/install.sh | sudo bash

# Or for beta version:
sudo -v ; curl https://rclone.org/install.sh | sudo bash -s beta
```

离线或手动安装请使用本技能目录下捆绑的脚本 `scripts/install.sh`。

## 安全警告

> **重要**：rclone 功能极其强大，可能对云存储数据造成不可逆的修改或删除。
> 请重点关注以下安全准则：

- 运行 `sync`、`move`、`delete`、`purge` 命令时，**务必先使用 `--dry-run`**。它会展示将要执行的操作而不会真正执行。
- 学习 rclone 期间**使用 `--interactive` / `-i` 参数**，避免误删数据。它会在每次执行破坏性操作前要求确认。
- **绝不要在命令行中以明文暴露凭据**。请使用 `rclone config` 安全存储凭据，或改用环境变量。
- **私钥与令牌**（S3 secret key、服务账号 JSON、OAuth 令牌）绝不能提交到版本控制或写入日志。配置文件 `~/.config/rclone/rclone.conf` 含敏感数据，请用 `chmod 600` 保护。
- **`rclone purge` 会忽略所有过滤器**——它会删除指定路径下的全部内容，请极其谨慎使用。
- **`rclone sync` 会让目标端与源端完全一致**——目标端有而源端没有的文件将被**删除**。请始终先用 `--dry-run` 验证。
- **远程控制 API**（`--rc`）默认应仅绑定到 localhost。若不加认证（`--rc-htpasswd`）就对外暴露，任何人都能控制你的 rclone 实例。
- **挂载操作**在写入过程中若被中断可能导致数据丢失。更安全的写入请使用 `--vfs-cache-mode full`。

## 速查表

### 配置

```bash
# Interactive configuration (recommended)
rclone config

# Show current config (redacts secrets by default)
rclone config show

# Show full config including secrets (DANGEROUS — do not share output)
rclone config show --redacted=false

# List configured remotes
rclone listremotes

# Create a remote non-interactively
rclone config create myremote s3 provider=AWS env_auth=true region=us-east-1

# Update existing remote
rclone config update myremote region=us-west-2
```

### 基本语法

```
rclone subcommand [options] source:path dest:path
```

源路径与目标路径采用 `remote:path` 语法。本地路径直接写 `/path/to/dir` 即可。

### 核心命令

```bash
# List files
rclone ls remote:path                    # list all objects with size
rclone lsd remote:path                   # list directories
rclone lsl remote:path                   # list with size, modtime, path
rclone lsf remote:path                   # list in flexible format
rclone size remote:path                  # total size and object count
rclone tree remote:path                  # tree view

# Copy (does not delete files at destination)
rclone copy /local/path remote:path      # local to remote
rclone copy remote:path /local/path      # remote to local
rclone copy remote1:path remote2:path    # remote to remote (server-side if possible)

# Sync (makes destination identical to source — DELETES extra files at dest)
rclone sync --dry-run /local/path remote:path    # ALWAYS dry-run first!
rclone sync -i /local/path remote:path           # interactive mode

# Move (copies then deletes source)
rclone move /local/path remote:path

# Delete operations
rclone delete remote:path                # delete contents of path
rclone purge remote:path                 # delete path AND all contents (ignores filters!)

# Check integrity
rclone check /local/path remote:path     # compare source and dest
rclone checksum remote:path              # verify checksums
rclone cryptcheck crypt:path             # verify encrypted remote

# Directory operations
rclone mkdir remote:path                 # create directory
rclone rmdir remote:path                 # remove empty directory
rclone rmdirs remote:path                # remove empty directories recursively

# Other useful commands
rclone cat remote:path/file.txt          # output file to stdout
rclone dedupe remote:path                # interactively find/delete duplicates
rclone about remote:                     # get quota information
rclone version                           # show version
```

### 过滤

过滤规则决定 rclone 处理哪些文件。务必结合 `--dry-run` 与 `-vv` 进行测试。

```bash
# Include only specific patterns
rclone copy /src /dst --include "*.jpg"
rclone copy /src /dst --include-from filter-file.txt

# Exclude specific patterns
rclone copy /src /dst --exclude "*.tmp"
rclone copy /src /dst --exclude-from exclude-file.txt

# Use filter rules (preferred when mixing include/exclude)
rclone sync /src /dst --filter "+ *.jpg" --filter "- *"
rclone sync /src /dst --filter-from rules.txt

# Size-based filtering
rclone copy /src /dst --min-size 1M --max-size 10G

# Age-based filtering
rclone copy /src /dst --min-age 7d --max-age 30d

# IMPORTANT: Do NOT mix --include, --exclude, and --filter flags.
# Use --filter exclusively when combining rules.
```

过滤模式语法：
- `*` 匹配任意非分隔符序列
- `**` 匹配任意序列（包括分隔符）
- `?` 匹配单个非分隔符
- `{a,b}` 匹配多个备选模式
- `{{regexp}}` 使用 Go 正则匹配

### 全局参数（最常用）

```bash
# Verbosity
-v                                        # info level
-vv                                       # debug level (shows filter matches)
--log-level LEVEL                         # DEBUG|INFO|NOTICE|ERROR

# Safety
--dry-run                                 # preview without doing anything
-i, --interactive                         # ask before each operation
--ignore-existing                         # skip files that exist at dest
-I, --ignore-times                        # transfer all, ignore modtime/size

# Transfer control
--transfers N                             # parallel transfers (default 4)
--checkers N                              # parallel checks (default 8)
--bwlimit RATE                            # bandwidth limit (e.g. 10M)
--max-transfer SIZE                       # stop after transferring this much
-c, --checksum                            # use checksum instead of modtime
--size-only                               # compare by size only

# Performance
--multi-thread-streams N                  # multi-thread downloads (default 4)
-P, --progress                            # show real-time progress

# Config
--config STRING                           # config file path
-C, --no-check-dest                       # skip dest check on copy
```

### 挂载

```bash
# Basic mount
rclone mount remote:path /mnt/remote

# Recommended mount with caching
rclone mount remote:path /mnt/remote \
  --vfs-cache-mode full \
  --vfs-cache-max-size 10G \
  --vfs-read-chunk-size 128M

# Unmount
fusermount -u /mnt/remote                # Linux
umount /mnt/remote                        # macOS
```

### 服务

```bash
rclone serve http remote:path             # HTTP file server
rclone serve webdav remote:path           # WebDAV server
rclone serve sftp remote:path             # SFTP server
rclone serve ftp remote:path              # FTP server
rclone serve s3 remote:path               # S3-compatible server
rclone serve dlna remote:path             # DLNA media server
rclone serve restic remote:path           # Restic backup backend
rclone serve docker remote:path           # Docker registry
```

### 加密（Crypt 远程）

```bash
# Configure encrypted remote wrapping another remote
rclone config
# Choose "crypt" type, point to an existing remote (e.g., "drive:private")

# Use crypt remote — files are encrypted/decrypted transparently
rclone copy /local/files crypt:path
rclone ls crypt:path

# Check integrity of encrypted files
rclone cryptcheck crypt:path
```

## 详细参考文件

如需更深入的信息，请查阅以下参考文件：

这些文件由官方基于 Hugo 的 rclone 文档转换而来，源路径为
`testdata/rclone/docs/`。若仍残留 Hugo shortcode 或模板语法，视作转换缺陷：
在据此回答前，请将其替换为普通 Markdown、静态表格或官方 URL。

| 文件 | 内容 | 阅读时机 | 官方链接 |
|------|---------|-------------|---------------|
| `references/usage.md` | 完整使用指南：语法、配置、远程路径、参数 | 理解 rclone 的高级行为 | [文档](https://rclone.org/docs/) |
| `references/flags.md` | 完整全局参数参考 | 查询具体参数选项 | [参数](https://rclone.org/flags/) |
| `references/filtering.md` | 过滤、包含/排除、模式 | 构建复杂过滤规则 | [过滤](https://rclone.org/filtering/) |
| `references/rc.md` | 远程控制 / HTTP API | 通过 API 程序化控制 rclone | [RC API](https://rclone.org/rc/) |
| `references/bisync.md` | 两条路径间的双向同步 | 配置双向同步 | [双向同步](https://rclone.org/bisync/) |
| `references/crypt.md` | 加密远程配置 | 配置加密云存储 | [加密](https://rclone.org/crypt/) |
| `references/cache.md` | 缓存后端与目录缓存 | 通过缓存优化性能 | [缓存](https://rclone.org/cache/) |
| `references/chunker.md` | 透明文件分块 | 在受限远端处理大文件 | [分块](https://rclone.org/chunker/) |
| `references/union.md` | Union 后端（合并多个远端） | 组合多个存储后端 | [Union](https://rclone.org/union/) |
| `references/combine.md` | Combine 后端（统一命名空间） | 多远端的统一视图 | [Combine](https://rclone.org/combine/) |
| `references/hasher.md` | 用于校验和处理的 Hasher 后端 | 为远端添加哈希支持 | [Hasher](https://rclone.org/hasher/) |
| `references/overview.md` | 云存储系统功能对比 | 对比厂商能力 | [概览](https://rclone.org/overview/) |
| `references/install.md` | 详细安装说明 | 排查安装问题 | [安装](https://rclone.org/install/) |
| `references/docker.md` | Docker 使用指南 | 在 Docker 中运行 rclone | [Docker](https://rclone.org/docker/) |
| `references/faq.md` | 常见问题 | 排查常见问题 | [FAQ](https://rclone.org/faq/) |
| `references/commands/` | 各命令的详细文档 | 查阅具体命令用法 | [命令](https://rclone.org/commands/) |

### 常用厂商参考

为配置特定云存储厂商，当 `references/providers/` 下存在对应文件时请阅读。
部分虚拟/后端类厂商（如 `crypt`、`cache`、`chunker`、`union`、`combine`、`hasher`）
属于跨厂商后端而非单一云服务，因此作为顶层文件存放在 `references/` 中。
- `s3.md` — Amazon S3 / 兼容存储（[官方](https://rclone.org/s3/)）
- `drive.md` — Google Drive（[官方](https://rclone.org/drive/)）
- `dropbox.md` — Dropbox（[官方](https://rclone.org/dropbox/)）
- `onedrive.md` — Microsoft OneDrive（[官方](https://rclone.org/onedrive/)）
- `azureblob.md` — Azure Blob Storage（[官方](https://rclone.org/azureblob/)）
- `b2.md` — Backblaze B2（[官方](https://rclone.org/b2/)）
- `googlecloudstorage.md` — Google Cloud Storage（[官方](https://rclone.org/googlecloudstorage/)）
- `sftp.md` — SFTP（[官方](https://rclone.org/sftp/)）
- `webdav.md` — WebDAV（[官方](https://rclone.org/webdav/)）
- `swift.md` — OpenStack Swift（[官方](https://rclone.org/swift/)）
- `ftp.md` — FTP（[官方](https://rclone.org/ftp/)）
- 以及其他 60+ 厂商——每个厂商在 `https://rclone.org/<name>/` 都有一页

### 命令参考

如需详细命令文档，请阅读 `references/commands/` 下对应文件：
- `rclone_copy.md`、`rclone_sync.md`、`rclone_move.md` — 传输命令
- `rclone_mount.md` — FUSE 挂载
- `rclone_serve_*.md` — 各种 serve 模式
- `rclone_config*.md` — 配置管理
- `rclone_bisync.md` — 双向同步
- 以及其他 80+ 命令——每个命令在 `https://rclone.org/commands/<command>/` 都有一页

## 常用工作流

### 初次设置
```bash
rclone config          # interactive setup wizard
rclone lsd remote:     # verify connection works
```

### 本地备份到云端
```bash
rclone sync --dry-run -P /home/user/documents remote:backup/documents
# Review dry-run output carefully, then:
rclone sync -P /home/user/documents remote:backup/documents
```

### 云到云迁移
```bash
rclone copy --dry-run -P source_remote:path dest_remote:path
rclone copy -P --transfers 8 source_remote:path dest_remote:path
```

### 从云端恢复
```bash
rclone copy --dry-run remote:backup/documents /home/user/restored
rclone copy -P remote:backup/documents /home/user/restored
```

### 限速传输
```bash
rclone copy --bwlimit 10M -P /data remote:backup
```

### 加密备份
```bash
# First configure a crypt remote wrapping your storage remote
rclone config
# Then use the crypt remote for all operations
rclone sync -P /sensitive-data crypt:backup
```

### 定时备份（cron）
```bash
# Add to crontab (daily at 2am):
0 2 * * * rclone sync -P /data remote:backup >> /var/log/rclone.log 2>&1
```

## 局限性

- 仅在任务明确匹配其上游来源与本地项目上下文时使用本技能。
- 在执行变更前，请验证命令、生成的代码、依赖、凭据以及外部服务行为。
- 示例不能替代针对具体环境的测试、安全审查，或针对破坏性或高成本操作的用户授权。