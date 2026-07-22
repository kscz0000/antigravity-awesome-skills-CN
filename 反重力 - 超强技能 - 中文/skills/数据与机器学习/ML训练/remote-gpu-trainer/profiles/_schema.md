# 平台 Profile Schema

每个 `profiles/<platform>.md` 用**相同的8个章节、相同的顺序**描述一个平台，以便
可扫描、可对比。Profile 拥有所有*慢变化的、平台专属的*底层信息，由 SKILL.md 各阶段委托调用。它**不**描述具体作业（那是下面的可移植作业请求），也绝不重复通用陷阱（它们在 `references/gotchas_universal.md` 中——只链接，不重述）。

从 SkyPilot / dstack / Ray 借用的设计规则：**硬件是约束，不是 SKU。** 作业请求 `gpu: A100:8`；Profile 负责将其映射到该平台的实例类型。**密钥仅通过环境变量名或文件路径引用——绝不内联密钥。**

---

## `profiles/<platform>.md` 的必需结构

每个 Profile 以紧凑的 frontmatter 块（机器可读的事实）开始，然后是8个正文章节。

```yaml
---
platform: <name>            # 例如 runpod
kind: ssh-rental            # ssh-rental | cloud-api | kubernetes | slurm
meter_stop_verb: terminate  # 停止计费的动作（stop | terminate | destroy | release | 关机 | manual）
meter_stop_irreversible: true
detach_primitive: tmux      # tmux | sbatch | k8s-job | nohup | kaggle-commit
spot_available: true
spot_grace: ~5s             # SIGTERM→SIGKILL 窗口，或 n/a
shared_fs: false            # 是否有跨实例共享文件系统？
inode_cap: none             # ~200K | none | host-dependent
free_egress: true           # 下载/上传到外部网络是否免费？
china_mirror_needed: false  # 是否在 GFW 之后？
host_driver_cuda_max: "12.x"
local_nvme: true
---
```

### 1. LAUNCH
入口（Web 控制台 / CLI / REST API / SSH），规范的创建命令，以及**环境契约**——Python 环境是什么（预构建 base？你选择的 Docker 镜像？Lambda Stack？）。如果适用，声明规则"镜像/base 就是环境——不要在租赁机上 `conda create`"。

### 2. STORAGE MODEL  *(生存矩阵 — 原则 #4)*
列出每个存储层级的路径、速度和容量/inode 上限。然后是**生存矩阵**：

| 层级 | 路径 | 关机后存活？ | 释放后存活？ | 容量 |
|---|---|---|---|---|

声明任何共享/网络卷的地域/机房锁定。指出 §5 拆除动词下检查点必须写入的挂载点。

### 3. NETWORK
出口/代理情况，中国镜像相关性（如适用则链接 `references/china-network.md`），端口/服务如何暴露（TB/Jupyter），以及 **SSH 风格**——注意代理/basic SSH 是否无法 `scp`/`rsync`（此时需要 direct-TCP）以及端口是否在重启时变化。

### 4. SPOT / INTERRUPTION + RESUME  *(原则 #7/#8)*
中断模型（spot 竞价？容量？自动关机计时器？自动释放？），**检测信号 + 宽限期**，以及恢复钩子。链接 `references/spot-resilience.md` 了解节奏公式。

### 5. TEARDOWN / BILLING  *(原则 #9 + 铁律)*
确切说明**什么操作停止计费**（stop vs terminate vs destroy vs 关机），每种操作保留什么，什么是**不可逆的**，以及费用陷阱（例如"stop 仍以2倍费率收取存储费"）。这是最容易出错的章节——必须精确。

### 6. DAEMON TOOL
脱离原语（`tmux` / `sbatch` / Job manifest / commit），是否在实例重启时存活（不仅仅是 SSH 断开），以及任何原生队列/调度器。注意 `tmux` 是否需要 `apt install` 或是否不存在（使用 `nohup … </dev/null >log 2>&1 &`）。

### 7. TOP GOTCHAS  (4–8 条，平台专属)
仅列出*平台专属*的陷阱，症状 → 根因 → 修复。通用陷阱只引用不重复。为每条分配稳定本地 ID（例如 `RP1`、`VAST2`）。

### 8. SCRIPT OVERRIDES
为该平台参数化 `scripts/` 模板所需的确切值：
`DATA_DIR=`（快速暂存）· `DURABLE_DIR=`（在拆除后存活）· `PROXY_HOOK=` · `CRED_FILE=`（文件路径；`""` 表示密钥是环境变量/secret）· `SCRATCH=`（要清理的内容）· `HF_HOME=` · `DETACH=`。
模板读取的就是这些环境变量名。另外两个旋钮是*派生*而非按平台设置的：`RUN_ONE`（队列运行器到 `run_one.sh` 的路径）默认为 `$DURABLE_DIR/run_one.sh`，`PROJECT_REPO_DIR`（*本次运行*代码所在位置）是每次运行的值——见下方"可移植作业请求"；仅在布局不同时才显式设置。

---

## 可移植作业请求（不在 Profile 中——按运行保存）

作业单独描述，以便*同一*作业可针对任何 Profile 运行。在 `references/parallel_ablation.md` 中记录；格式：

```yaml
resources:
  gpu: {name: A100, count: 8, memory: 40GB+}   # 约束（范围可接受），不是平台 SKU
  disk: 200GB
candidates: [autodl, china, runpod]            # 有序回退 → "描述一次，到处运行"
file_mounts: {/data: {source: ..., mode: MOUNT_CACHED}}   # MOUNT | COPY | MOUNT_CACHED
run: "bash run_queue.sh queue.txt"
```

启动器将作业解析到 Profile；Profile 提供路径/动词，作业提供工作负载。将它们分离正是 Profile 可跨所有作业复用的关键。
