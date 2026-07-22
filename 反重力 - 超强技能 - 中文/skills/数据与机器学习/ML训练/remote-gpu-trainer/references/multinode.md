# 多节点 NCCL 与弹性训练陷阱 — 进阶

**单机用户跳过整个文件。** 这里没有任何内容适用于单实例 — 一个节点，无论多少 GPU，通过 NVLink/PCIe 运行 DDP/FSDP，永远不涉及节点间 NCCL 传输、fabric-manager 或 rendezvous 逻辑。本文件**仅**适用于跨越 ≥2 个租用实例的作业（多节点 DDP、FSDP、流水线/张量并行或弹性训练）。它假设 checkpoint-to-durable + 幂等恢复骨架已就位（`references/principles.md` #8；节奏 + 原子写入见 `references/spot-resilience.md`）— 多节点只改变*进程组如何形成和断开*，永远不改变恢复机制。

这些全部是 **[P] 平台/拓扑相关**陷阱。通用陷阱（磁盘、OOM、CRLF、静默同步、spot 宽限）在此**不**重复 — 见 `references/gotchas_universal.md`。

## 目录

- **Fabric-manager** — 一个坏节点在 NCCL 初始化时卡住整个作业（MN1）
- **NIC 选择** — NCCL 选中 docker0/loopback/慢速 NIC（MN2）
- **超时遮蔽** — 默认 1800 秒掩盖了落后者/死亡 rank（MN3）
- **MTU 不匹配** — 巨型帧静默丢弃，小消息正常（MN4）
- **弹性重启 ≠ 状态恢复** — torchrun `--max-restarts`（MN5）
- **弹性 Horovod pause-below-min-np** — 暂停然后报错（MN6）
- **首发检查清单** — 拉起一个健康的多节点组

快速跳转：`grep -in <keyword> references/multinode.md`（例如 `grep -in fabric references/multinode.md`）。

---

## MN1 — 一个节点上 Fabric-manager 宕机导致整个作业在 NCCL 初始化时卡死

**症状。** 启动多节点作业；每个 rank 打印到 NCCL 初始化后冻结 — 无 traceback、无进展、无 OOM，只在第一次集合通信处静默卡死。杀死后重新启动重现完全相同的卡死。相同代码的单节点运行完全正常。

**根因。** 在基于 NVSwitch 的节点（HGX/DGX A100/H100）上，`nvidia-fabricmanager` 必须在**每个**节点上运行且健康，NVLink/NVSwitch 路由才能建立。一个节点上 fabric-manager 停止、崩溃或版本不匹配，无法建立其 NVLink fabric，因此其 rank 永远无法加入集合通信 — 而因为 NCCL 初始化是**全局屏障**，所有健康节点都在等待那个永远到不了的节点。故障是全局的；原因仅在一个节点上。

**修复。**
- 启动前在**每个**节点上检查 fabric-manager，不仅是头节点：
  `systemctl status nvidia-fabricmanager`（或 `nvidia-smi -q | grep -i fabric`）。它必须是 `active (running)` 且版本必须与该节点的驱动匹配。
- 将静默卡死转为可诊断状态：启动时加 `NCCL_DEBUG=INFO`（可选 `NCCL_DEBUG_SUBSYS=INIT,NET`）。
  日志中**先停住**的那个节点（在其他节点打印拓扑之前）就是罪魁祸首。
- 在租用环境中修复是运维性的，不是重插：如果允许则重启服务（`systemctl restart nvidia-fabricmanager`），否则**停掉那个实例，重新租用另一台机器** — fabric-manager 启动不了的通常是病态主机（与 `references/gotchas_universal.md` 中的 Xid 硬件故障逻辑重叠）。

URL: https://support.crusoecloud.com/hc/en-us/articles/46061806112155-NCCL-Hangs-and-Multi-Node-Training-Stalls-Caused-by-Failed-nvidia-fabricmanager

---

## MN2 — NCCL 选择了错误的 NIC（docker0 / loopback / 慢速接口）

**症状。** 多节点初始化永远卡住，或者连接了但节点间带宽慢 10 倍（allreduce 占据步时间主导；单节点吞吐正常）。`NCCL_DEBUG=INFO` 显示 NCCL 绑定到 `docker0`、`lo`、或 1 GbE 管理 NIC 而非快速数据面接口。

**根因。** NCCL 自动发现网络接口，在无引导时可能选中不可路由的网桥（`docker0`）、环回接口、或慢速管理 NIC — 这些都不在真实节点间传输流量。作业要么永远连不上（不可路由），要么走错误的慢路径。

**修复。** 在**所有**节点上显式固定传输（每个 rank 上相同环境变量）：
- `export NCCL_SOCKET_IFNAME=<real-iface>` — 前缀过滤；例如 `eth`、`ens`、`bond`。用前导 `^` 排除坏的：`NCCL_SOCKET_IFNAME=^docker0,lo`。
- 在 RDMA/InfiniBand fabric 上固定 HCA：`export NCCL_IB_HCA=mlx5`（活跃适配器前缀）。
- **无 RDMA（仅 TCP 租用）：** `export NCCL_IB_DISABLE=1` 使 NCCL 停止探测不存在的 IB，干净地回退到 socket 路径，而不是卡在 IB 发现上。
- 用 `NCCL_DEBUG=INFO` 确认所选接口 — `NET/Socket` 或 `NET/IB` 行命名了绑定设备；验证它是快速数据面 NIC，不是网桥。

URL: https://github.com/NVIDIA/nccl/issues/1580

---

## MN3 — 默认 1800 秒 NCCL 超时掩盖了落后者或死亡 rank

**症状。** 正在运行的作业在集合通信处冻结恰好 **30 分钟**，然后以 `Watchdog ... collective ... timed out` / `NCCL timeout` 错误死亡 — 或者更糟，因为看门狗关闭而卡更久。真正的故障（一个 rank OOM、崩溃、或落后）发生在 30 分钟前并被埋没了。

**根因。** NCCL 的默认集合超时为 **1800 秒**。当一个 rank 死亡或卡住时，其他 rank 在集合通信中等待完整的 30 分钟窗口才有所表现 — 所以症状出现在原因之后半小时，而且瞬态落后者可能触发本应挺过的硬中止。

**修复。**
- **对死亡 rank 快速失败：** `export NCCL_ASYNC_ERROR_HANDLING=1`（较新 PyTorch：`TORCH_NCCL_ASYNC_ERROR_HANDLING=1`），使崩溃/不可达的 rank 迅速拆除组而非等待超时 — 存活 rank 在接近真正故障点处获得可操作的错误。
- **双向审慎调整超时窗口。** 真正慢的集合通信（巨大 allreduce、慢 checkpoint 屏障）需要**更长**超时以避免误中止：通过进程组初始化提高（`torch.distributed.init_process_group(..., timeout=timedelta(minutes=60))`）。要更早暴露卡住的落后者，则降低它。默认值很少适合真实作业 — 有目的地设置它。
- 配合 MN1 的 `NCCL_DEBUG=INFO` 使超时错误指明哪个 rank 失联。

URL: https://repost.aws/questions/QURXddiuikQLesRDGz39RhIw/nccl-socket-timeout-when-using-large-dataset-in-multi-node-pretraining

---

## MN4 — 巨型帧 MTU 不匹配静默丢弃大型 NCCL 帧

**症状。** 小集合通信正常（rendezvous 成功、小张量 allreduce 正常），但作业在发送**大**负载时卡住或抛出传输错误 — 大梯度桶、第一次大 allreduce、或模型广播。中断与消息**大小**相关，而非与涉及的 rank 相关。

**根因。** 容器接口配置为巨型帧（MTU 9000），但它连接的主机 veth / 网桥仍为 1500（或反之）。小包通过较小的 MTU 限制正常通过；超大帧在不匹配的跳点被静默丢弃，无应用层错误，所以 NCCL 等待永远不到达的数据。常见于容器化租用环境中容器 MTU 和主机网桥 MTU 被独立设置的情况。

**修复。**
- 端到端匹配 MTU：将**主机 veth/网桥**设置为与容器接口相同的 MTU（9000 ↔ 9000，或都降到 1500）。用 `ip link show` 检查容器和主机两侧。
- 快速确认节点间路径确实能传巨型帧：
  `ping -M do -s 8972 <other-node-ip>`（8972 = 9000 − 28 字节头）。如果失败但 `-s 1472` 成功，说明大帧被丢弃 → 修复 MTU，不要归咎于 NCCL。
- 如果租用环境中主机网桥 MTU 无法更改，将容器接口**降**到 1500 以匹配 — 统一但较小的 MTU 可行；不匹配的不行。

URL: https://github.com/moby/moby/issues/4378

---

## MN5 — torchrun / TorchElastic `--max-restarts` 重启进程组但不恢复训练状态

**症状。** 一个 worker 死亡（抢占、瞬态故障）；torchrun 的 `--max-restarts=N` 忠实地重新运行 rendezvous 并重启**所有** worker — 但训练从 **step 0**（或错误的 epoch）恢复，静默丢弃了故障前的进度。重启"成功了"但运行被倒退了数小时。

**根因。** TorchElastic 仅保证**worker 组**被重建：它重新运行 c10d rendezvous，重新推导 `world_size`/`rank`，并重启每个 worker 进程。它**不**持久化或重新加载训练状态 — 那完全是脚本的责任。带 `--max-restarts` 但没有脚本内 load-latest-checkpoint 的重启只是在每次重启时从头运行 `main()`。

**修复。**
- 每 epoch（或每 N 步）的快照才是恢复状态的东西，完全遵循 `references/principles.md` #8：**原子地**写入完整状态（模型 + 优化器 + LR 调度器 + epoch/step + RNG + 数据加载器位置）（`tmp`→`fsync`→`os.rename`），并**在每次启动顶部无条件加载最新 checkpoint**，使 torchrun 重启是恢复而非重新开始。节奏公式 + 原子写入细节见 `references/spot-resilience.md`。
- 使用托管在 `host:port` 上的 c10d rendezvous 后端（无 etcd 依赖）；将 `--max-restarts` 设为足以承受预期抢占次数，而不是 0。
- **必需：** 将恢复后的运行视为*相同配置的恢复*，绝不是手动修改后的重新启动 — 静默重启或重新洗牌的运行正是 `verifying-dl-experiments` 要防范的污染；在信任任何重启后指标前，根据加载的 checkpoint 确认恢复的 step/epoch。

URL: https://docs.pytorch.org/tutorials/beginner/ddp_series_fault_tolerance.html

---

## MN6 — 弹性 Horovod 在 `--min-np` 以下暂停，然后在 `HOROVOD_ELASTIC_TIMEOUT` 时报错

**症状。** 在弹性 Horovod 下（`horovodrun -np 8 --min-np 4 --max-np 12`），足够多的 worker 被抢占使存活数低于 `--min-np`；作业**没有**立即失败 — 它看起来卡住了（暂停、无进展）— 然后几分钟后以超时错误死亡。等待立即失败的操作员错过了暂停窗口。

**根因。** 弹性 Horovod 在可用 worker 低于 `--min-np` 时**暂停**（不失败），等待容量回归。只有在 `HOROVOD_ELASTIC_TIMEOUT`（默认 **600 秒**）经过后仍未恢复到 `--min-np` 时才报错。所以过高的 `--min-np` 将一个常见的数次抢占事件变成了 10 分钟静默等待后的硬失败。

**修复。**
- 将 `--min-np` 设得**足够低**，使典型的并发抢占次数不会突破它 — 存活者通过成员变更继续训练而非暂停。
- 如果 spot 层的容量恢复通常慢于 600 秒，提高 `HOROVOD_ELASTIC_TIMEOUT`，使临时容量下降恢复而非中止。
- **将 LR 缩放和数据分片固定到 `--max-np`，而非存活 worker 数** — 否则有效学习率和分片分配在每次成员变更时漂移，静默损坏运行（`verifying-dl-experiments` 关注点：来自 LR 静默重新缩放的运行的指标不是干净的数据点）。

URL: https://horovod.readthedocs.io/en/stable/elastic_include.html

---

## 首发检查清单 — 拉起一个健康的多节点组

在信任任何多节点吞吐数据之前按此顺序运行；它廉价地隔离 MN1–MN4（不需要完整作业）：

- [ ] **每个**节点：`systemctl status nvidia-fabricmanager` → `active (running)`，版本与驱动匹配（MN1）。
- [ ] 所有 rank 上导出相同的 NCCL 环境变量：`NCCL_SOCKET_IFNAME`、`NCCL_IB_HCA`（或 `NCCL_IB_DISABLE=1`），以及选定的 `init_process_group` 超时（MN2、MN3）。
- [ ] 节点间 MTU 路径检查：`ping -M do -s 8972 <other-node-ip>` 成功，或两端都固定为 1500（MN4）。
- [ ] 首次真实启动加 `NCCL_DEBUG=INFO` + `NCCL_ASYNC_ERROR_HANDLING=1`；确认每个 rank 的 `NET/...` 行命名的是快速数据面 NIC，不是网桥（MN2、MN3）。
- [ ] 脚本内的 load-latest-checkpoint 验证在重启时触发，**然后**才依赖 `--max-restarts` / 弹性成员恢复（MN5、MN6；骨架见 `references/principles.md` #8）。
- [ ] 分布式作业比单 GPU 更频繁 checkpoint — 一次抢占浪费 N× 计算；节奏见 `references/spot-resilience.md`。

关于跨节点扇出*sweep*（独立单元，非一个跨多节点的作业），参见 `references/parallel_ablation.md` + **必需** `superpowers:dispatching-parallel-agents`，不是本文件。
