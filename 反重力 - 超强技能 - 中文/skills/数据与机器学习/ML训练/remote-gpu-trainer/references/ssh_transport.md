# SSH 传输 — 密钥、keepalive、可恢复复制、通过 stdin 传递密钥

每个 `ssh-rental` profile（AutoDL、RunPod、vast.ai、Lambda、Paperspace、中国平台、裸 SSH）的平台无关 SSH + 文件传输基底。一次性配置使后续命令简短且无密码，加上在脆弱网络和短期租赁中存活的复制/密钥模式。具体主机、端口和凭据位置是 **profile 事实** — 本文件拥有*机制*，profile（`profiles/<platform>.md` §1/§3/§8）拥有*值*。

跳转：`grep -in '<keyword>' references/ssh_transport.md`（如 `keepalive`、`rsync`、`stdin`、`crlf`）。

## 目录

1. 密钥生成
2. 将公钥推送到实例
3. `~/.ssh/config` 别名 + keepalive 调优
4. 验证别名
5. 可恢复复制 — rsync vs scp，以及为什么用 rsync
6. 按目录批量下载循环
7. 通过 stdin 移动密钥 — 永远不要内联密钥，永远不放在持久 FS 上
8. CRLF — Windows 上编写的 `.sh` 在 Linux 上崩溃
9. 两种 SSH 风格 — 代理/基础 SSH 无法 `scp`
10. 传输陷阱（症状 → 根因 → 修复）

---

## 1. 密钥生成

如果 `~/.ssh/id_ed25519` 已存在则跳过。

```bash
ssh-keygen -t ed25519 -C "<label>"
# 保存路径：Enter 使用默认 ~/.ssh/id_ed25519
# 密码短语：可选（Enter 无密码，或设置一个 + 使用 ssh-agent）
```

`ed25519` 比 RSA 更短更安全；每个租赁平台都接受两者。一个本地密钥在所有实例间复用 — 生成一次，将**公钥**半（§2）推送到每个机器。私钥半（`~/.ssh/id_ed25519`，无 `.pub`）永远不离开本地机器，**永远不**放到租赁机、共享 FS 或云智能体上（云调度器在隔离沙箱中运行，无法访问它 — 将私钥放入其中是密钥泄漏；参见 `references/monitoring_patterns.md`）。

## 2. 将公钥推送到实例

从平台的 web 控制台 / API 复制连接字符串；格式为
`ssh -p <PORT> root@connect.<region>.<provider>.com`。推送公钥一次：

```bash
ssh-copy-id -p <PORT> root@connect.<region>.<provider>.com
# 输入平台提供的密码一次
```

如果 `ssh-copy-id` 缺失（Windows 原生 shell 常见），手动追加密钥：

```bash
cat ~/.ssh/id_ed25519.pub          # 复制整行
ssh -p <PORT> root@connect.<region>.<provider>.com
# 在远程：
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "<粘贴公钥行>" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit
```

测试：重新运行 `ssh …` 行应**无需**密码提示即可连接。

## 3. `~/.ssh/config` 别名 + keepalive 调优

每个实例一个配置块将 `ssh -p <PORT> root@connect.<region>.<provider>.com` 变为 `ssh <alias>`，
并内嵌 keepalive 选项以保持长监控/传输连接不中断。

```ssh-config
Host proj-1
    HostName connect.<region>.<provider>.com
    Port <PORT>
    User root
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 120
    TCPKeepAlive yes
    # LogLevel VERBOSE   # 取消注释以调试拒绝/挂起的连接

Host proj-2
    HostName connect.<region>.<provider>.com
    Port <PORT>
    User root
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 120
```

**命名**：`<project>-<index>`（如 `proj-1`、`proj-2`）在扇出循环中读起来干净；避免裸 `gpu1`。**为什么是三个 keepalive 选项**：

- `ServerAliveInterval 60` — 每 60 秒发送一个应用层心跳，这样路径上的 NAT/空闲超时不会静默断开停泊的连接（在 `scp` 中途，或一个打开的监视器）。
- `ServerAliveCountMax 120` — 在声明链路死亡前容忍最多 120 个未响应心跳（≈2 小时的网络不稳定存活）。对于*有界*监视器，降低它（如 3），使其在抖动时自杀死而非挂起 — 参见 `references/monitoring_patterns.md` 中的短连接轮询。
- `TCPKeepAlive yes` — 让 OS 也发送 TCP 层 keepalive，捕获不优雅消失的对端。

当 profile 重新签发实例时端口会变化（`ssh-rental` 机器在重建时分配新端口） — 每次创建/重建后更新 `Port` 行，然后重新运行 §4。

## 4. 验证别名

```bash
for a in proj-1 proj-2 proj-3 proj-4; do
    echo "=== $a ==="
    ssh -o ConnectTimeout=10 "$a" "hostname; date"
done
```

每个应打印不同的主机名。然后环境探测（SKILL.md Phase 1）：
`ssh <alias> 'python -c "import torch;print(torch.cuda.is_available())"'`。

## 5. 可恢复复制 — rsync vs scp，以及为什么用 rsync

`scp` 为整个传输打开**一个** SSH 流且**无法恢复**：中途任何抖动都会中止整个运行，重新运行从零开始。`rsync` 比较源/目标并只传输增量，所以掉线后重新运行**继续**而非重启 — 在按小时计费的机器上，这是 130 GB pull 在第 45 分钟抖动时最重要的属性。

**对大型或多文件传输优先使用 `rsync`：**

```bash
rsync -avz --partial --inplace --progress \
    -e ssh \
    <alias>:/root/autodl-tmp/checkpoints/ /path/to/local/checkpoints/
```

- `-a` 归档（递归 + 保留权限/时间/符号链接），`-v` 详细，`-z` 在线路上压缩。
- `--partial` 在中断时保留部分传输的文件，下次运行从中断处恢复（没有它，rsync 删除部分并从头重传）。
- `--inplace` 直接写入目标文件（恢复友好；避免在紧张的本地磁盘上做完整临时副本）。如果原子替换现有目标比可恢复性更重要，则去掉它。
- 失败后重新运行**相同**命令 — 那*就是*恢复（原则 #7）。

仅在**单个小文件**（一个配置、一个 < ~1 GB 的检查点）时使用裸 `scp`，恢复无所谓。对于大型*树*，即使 `scp` 用户也应回退到**按目录循环**（§6），这样一个目录的失败不会丢失其余。如果远程镜像上缺少 `rsync`，`apt-get install rsync`（在线时）或使用 §6 循环。

> 批量下载停滞重试阶梯（HF/ModelScope 镜像切换、`timeout … && break` 循环）是*从互联网下载*关注点，不是主机↔主机复制 — 那部分在 `references/china-network.md`。

## 6. 按目录批量下载循环

对于大型目录树（许多运行/检查点目录），将每个目录包装在**自己的** SSH 会话中，这样一个断开只丢失那个目录，重新运行**跳过已完成的目录**：

→ `scripts/download_loop.sh`（参数化 `LOCAL_TARGET`、`REMOTE_ALIAS`、`REMOTE_PATH`）。

其结构，以及每个部分为何重要：

- **列出一次，按目录复制** — 每个 `scp -r <alias>:<remote>/$d ./` 是独立会话；一个失败 ≠ 整个传输丢失（`scp` 单流陷阱，§5）。
- **大小阈值跳过** — 目录已 ≥ 阈值计为完成并被跳过；部分目录被移除并重新拉取。因此重新运行整个脚本是幂等且可恢复的。
- **每个目录的 `ConnectTimeout` + §3 的 keepalive 标志**在每次 `scp` 上，这样挂起的会话自杀死而非阻塞循环。

## 7. 通过 stdin 移动密钥 — 永远不要内联密钥，永远不放在持久 FS 上

将凭据**放在命令中**（`ssh host "echo 'KEY' > …"` 或 `scp key.txt host:…`）会将值泄漏到 shell 历史、智能体记录和钩子日志中。将其放在**共享/持久 FS** 上更糟：值对每个共同租户持久存在，且某些平台的上传分类器*阻止或损坏*匹配已知密钥模式的文件 — 所以写入跨实例 FS 的凭据可能静默无法到达。**通过 stdin 将凭据推送到每个机器的每实例系统磁盘**，使值从文件→管道→文件流动，不出现在任何命令文本或输出中：

```bash
# 精确流式传输一个凭据块 — 值永远不出现在命令行中
grep -A 2 "machine api.<provider>.com" ~/.netrc \
  | ssh <alias> 'umask 077; cat > /root/.netrc && chmod 600 /root/.netrc'
```

```bash
# 或单个令牌，相同原则（stdin 进，文件出，chmod 600）
printf '%s\n' "$TOKEN_FROM_ENV" \
  | ssh <alias> 'umask 077; cat > /root/.<service>_key && chmod 600 /root/.<service>_key'
```

使其安全的规则：

- **一个块，不是整个文件。** 流式传输单个 `machine …` 段，永远不是整个 `~/.netrc` — 它携带不相关机器的凭据，安全钩子（正确地）阻止复制整个文件。
- **引用，永远不回显。** 从环境变量（`$TOKEN_FROM_ENV`）或密钥环获取令牌；永远不要将字面值粘贴到命令中。
- **每实例系统磁盘，不是共享 FS。** 写入 `/root/.<service>_key`（易失但私有），不是跨实例持久挂载。封装器在启动前读取它并导出环境变量（如 `export WANDB_API_KEY=$(cat /root/.wandb_key)`）。
- **按能力验证，不是回显值：**
  `ssh <alias> 'python -c "import wandb; print(wandb.Api(timeout=20).default_entity)"'`。

## 8. CRLF — Windows 上编写的 `.sh` 在 Linux 上崩溃

症状 → 根因 → 修复：

- **症状**：同步的启动器静默不做任何事（空日志）；手动运行报错 `set: -: invalid option`、`cd: /path\r: No such file or directory` 或 `syntax error near unexpected token $'do\r'` — 每行"以 `\r` 结尾"。
- **根因**：Windows `core.autocrlf=true`（或 `git archive` 以工作树 EOL 导出）以 CRLF 写入 `.sh`；Linux `bash` 将尾随 `\r` 视为每个 token 的一部分。（`.py` 不受影响 — Python 的通用换行符容忍 CRLF；具体破坏的是 `bash`/`.sh`。）
- **修复**：添加 `.gitattributes` 包含 `*.sh text eol=lf`，这样 `git archive`/checkout 总是发出 LF；作为即时在机器上的解除，`sed -i 's/\r$//' scripts/*.sh`。

`scripts/` 中的每个 shell 脚本以 LF 发送并以 `#!/usr/bin/env bash` + `set -u` 开头；编写新脚本时保持该约定。**永远不要**在传输或轮询脚本的 `grep` 正则中放置未加引号的 `|` — shell 将其拆分为管道命令，第一个读取 stdin → 永远挂起（`references/monitoring_patterns.md`）。

## 9. 两种 SSH 风格 — 代理/基础 SSH 无法 `scp`

一些 `ssh-rental` 平台暴露**两种** SSH 端点，差异决定了文件传输是否有效：

- **直接 TCP SSH** — 到容器的真实 TCP 端口（上面 `connect.<region>.<provider>.com:<PORT>` 形式）。完整 `scp`/`rsync`/`sftp` 工作。这是本文件中每个传输假设的方式。
- **代理 / "基础" SSH** — 中继或 web 终端 SSH（RunPod 和 vast.ai 上默认暴露的端点常见）。它只承载**交互式 shell**：`scp`/`rsync`/`sftp` 失败（通常报 `subsystem request failed` 或握手挂起），因为代理不转发 SFTP 子系统。

**修复**：对任何代码/数据/检查点传输，使用**直接 TCP** 端点 — RunPod 上暴露 TCP 端口（`ssh root@<ip> -p <PORT>` 形式，不是代理的 `ssh <pod>@ssh.runpod.io` 形式）；vast.ai 上使用实例的直接 SSH 端口。每个 profile 的 §3 NETWORK 说明哪个端点是哪个以及重启时端口是否变化。如果只有代理 SSH 可用，改为带外传输（将结果从机器上推送到对象存储 / HF Hub 然后从那里拉取）。

## 10. 传输陷阱（症状 → 根因 → 修复）

通用陷阱（磁盘满、inode、OOM、静默同步）在此**不**重复 — 参见 `references/gotchas_universal.md`。这些是传输特定的。

**T1 — `pkill`/`kill` 后 SSH 立即 exit 255 / "Connection reset"。**
症状：`ssh <alias> 'pkill -9 -f src.train'` 返回 `Connection reset by peer`，exit 255。→ 根因：杀死进程树破坏 PTY 链；SSH 客户端收到 EOF 并退出 — 同一 one-liner 中 kill 之后的任何内容永远不会运行。→ 修复：这是**正常现象，不是错误**。重新 ssh 验证（`ssh <alias> "pgrep -af src.train | head -1 || echo CLEAN"`）。将 kill 和 relaunch 拆分为**两个** ssh 调用 — 永远不要在一个命令中 `pkill X; relaunch X`，relaunch 随会话一起被丢弃。

**T2 — 大型 `scp -r` 在 30–60 分钟时以 "Read from remote host … reset by peer" 断开。**
症状：130 GB 的 `scp -r` 在传输中途中止；本地树只有前几个目录，其余消失。→ 根因：整个传输使用一个 SSH 流；任何抖动杀死它且 `scp` 不恢复。→ 修复：使用 `rsync --partial`（§5）或按目录循环（§6） — 每个目录一个独立会话，重新运行跳过已完成的目录。

**T3 — `.sh` 在 Windows→Linux 同步后"以 `\r` 结尾"。**
参见 §8（`.gitattributes` `*.sh text eol=lf`；在机器上 `sed -i 's/\r$//'`）。

**T4 — 凭据泄漏到历史/共享 FS，或其 FS 上传静默失败。**
症状：粘贴到 `ssh`/`scp` 命令中的密钥落入记录和钩子日志；密钥 scp 到共享 FS "成功"但文件缺失或损坏。→ 根因：值出现在命令行中；且某些平台的 FS 分类器阻止/损坏凭据形状的上传。→ 修复：§7 — 通过 stdin 流式传输一个块到每实例磁盘，按能力验证不是按回显。

**T5 — `scp dest open "/root/x/": Failure` 立即发生。**
症状：（通常是并行/后台的）`scp big.tar <alias>:/root/x/` 立即失败，因为目标目录不存在 — 一个本应 `mkdir` 它的兄弟命令运行更晚或被阻塞。→ 根因：传输假设了一个*不同*命令应该创建的目录（并行设置竞争）。→ 修复：使每次传输自足 — 在同一命令中创建目标：
`ssh <alias> 'mkdir -p /root/x' && scp … || retry`。永远不要假设兄弟创建了目标。

**T6 — 实例重建后 `Host key verification failed`。**
症状：相同 `connect.<region>.<provider>.com` 主机，新主机密钥，SSH 拒绝。→ 根因：重建的容器在重用的主机名/端口上呈现不同的主机密钥。→ 修复：
`ssh-keygen -R '[connect.<region>.<provider>.com]:<PORT>'`，然后重新连接（重新接受新密钥）。
