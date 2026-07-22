# Spot / 抢占容错

使作业在被随机瞬间杀死后仍能存活 — 乘坐便宜 50–90% 的 spot/preemptible/interruptible 层的代价。整个层简化为**原则 #8**（`references/principles.md`）：在 Young/Daly 定时器上将完整状态检查点到持久存储，启动时无条件加载最新状态，原子写入，将抢占信号仅视为机会性的最后一次刷新。本文件是深度形式：按平台的宽限窗口、带计算示例的间隔公式、原子写入恢复配方和注释版 Python 骨架。

跳转：`grep -in '<keyword>' references/spot-resilience.md`。

## 目录

1. 抢占信号 + 宽限窗口（按平台）
2. 检查点间隔 — Young/Daly 公式
3. 原子写入恢复配方
4. 托管 spot 框架移动机器；检查点加载恢复状态
5. Python 检查点/恢复骨架

---

## 1. 抢占信号 + 宽限窗口（按平台）

宽限窗口决定设计：它决定信号检查点是否甚至可行，或者定时器是否是*唯一*的持久性。**宽限窗口不是安全网** — 参见下表后破坏设计的陷阱。具体按平台的可达性/计费细节位于各 `profiles/<platform>.md` §4；这是跨平台信号映射。

| 平台 | 检测信号 | 宽限窗口 | 含义 |
|---|---|---|---|
| **AWS EC2 Spot** | IMDS `http://169.254.169.254/latest/meta-data/spot/instance-action`（404=无，200=待处理）；再平衡推荐提前约 10–20 分钟 | **约 120 秒** | 信号时刷新*小*检查点可行；大检查点仍靠定时器 |
| **GCP Spot** | metadata 抢占标志 + ACPI G2 Soft Off → shutdown 脚本 | **约 30 秒** 默认（可配至 120 秒，预览） | 定时器优先；仅当检查点写入 < 窗口时信号刷新 |
| **GCP Preemptible（旧版）** | 相同信号，**另有硬性 24 小时上限**与容量无关 | 约 30 秒 **+ 24 小时斩首** | 长运行优先用 Spot；Preemptible 即使空闲也在 24 小时死亡 |
| **Azure Spot** | IMDS Scheduled Events `/metadata/scheduledevents`，事件类型 `Preempt` | **≥30 秒**（Preempt 是短事件；其他给 ≥5 分钟） | 定时器优先 |
| **Slurm 抢占 / 挂钟时间** | `SIGTERM`（然后 `SIGKILL`）；用 `#SBATCH --signal=B:SIGTERM@360` 批处理步骤在杀死前约 360 秒获得 SIGTERM | **SIGTERM → 约 30 秒** 默认；通过 `--signal` 前导时间加宽 | `--requeue` + 脚本内 SIGTERM trap 检查点，然后在重新排队时恢复 |
| **RunPod Spot** | OS **SIGTERM → SIGKILL**（也"可中断无通知"） | **约 5 秒** | 远不够刷新大检查点 — 定时器是唯一真正的持久性 |
| **vast.ai Interruptible** | **无信号** — 基于出价；出价被超过的瞬间实例*暂停*（进程被杀死） | **约 0 秒（突然）** | 纯定时器；假设每次冷重启 + 重载 |

**陷阱 — 破坏设计的那一个。**
症状：一个"捕获 SIGTERM，将 40 GB 检查点刷新到持久存储"的处理器在 AWS（120 秒）上测试正常，但在 RunPod（5 秒）/ vast.ai（0 秒）上作业在刷新完成前就死了。根因：将宽限窗口视为*主要*持久性机制 — 它跨平台从 2 分钟到约 0 秒不等，所以任何需要超过几秒的处理器都是抛硬币。修复：在**周期性定时器上检查点到持久存储**（§2）；将信号 trap **仅**作为机会性的"如果有时间保存最终部分检查点"奖励，永远不作为安全网。

**陷阱 — GCP Preemptible 24 小时斩首。**
症状：Preemptible VM 上的多日运行在 24 小时整点死亡，即使没人回收它。根因：旧版 Preemptible 有硬性 24 小时最大运行时间；Spot VM 没有上限。修复：任何超过一天的运行使用 **Spot，不是 Preemptible**。

---

## 2. 检查点间隔 — Young/Daly 公式

间隔是**公式，不是猜测。** 最小化总挂钟浪费（杀死后回滚重算 **加上** 检查点写入开销）的最优检查点间隔是 Young/Daly 结果：

```
W = sqrt(2 * mu * C)
```

- `mu` = 两次抢占间平均时间（MTBF），秒。
- `C`  = 写入一个检查点到持久存储的时间，秒。
- `W`  = 检查点间隔（每 `W` 秒写一个检查点）。

**计算示例。** 检查点写入耗时 `C = 30 秒`；实例平均每 `mu = 3 小时 = 10800 秒` 被抢占。则：

```
W = sqrt(2 * 10800 * 30) = sqrt(648000) ≈ 805 秒 ≈ 13.4 分钟  →  约每 13 分钟检查点一次
```

更高的抢占率（更小的 `mu`）→ 更短的间隔。更慢的检查点（更大的 `C`）→ 更长的间隔（每次保存成本更高，所以分摊到更多进度上）。

**将 W 向下取整到迭代/epoch 边界。** Young/Daly 假设检查点可以在*任意*瞬间拍摄，但真实迭代训练只能在 step 或 epoch 边界快照。所以将 `W` 转换为整数迭代次数并*向下取整*：在约 2 秒/迭代时，`805 秒 → 402 次迭代 → 每 400 次迭代检查点`。向下取整检查点比最优稍频繁，这是安全方向。

**分布式乘数。** 有 `N` 个 worker 时，一次抢占浪费 `N×` 计算（整个组回滚），所以分布式作业应比单 GPU 的 `W` 建议的更频繁地检查点。

---

## 3. 原子写入恢复配方

两种失败模式将"我有检查点"变成"我的恢复坏了"：**部分权重保存**和**被杀死时损坏的检查点**。本配方修复两者。

**保存完整训练状态，不只是模型权重。** 只恢复权重的恢复会静默重启 epoch、重新洗牌数据并降低准确度。检查点必须包含：

- 模型 `state_dict`
- 优化器 `state_dict`
- LR-scheduler `state_dict`
- epoch **和** 全局 step/iteration 计数器
- RNG 状态（Python `random`、NumPy、`torch` 和 CUDA）
- 数据加载器位置（sampler epoch / 可恢复 sampler 偏移）

**原子写入：tmp → fsync → os.replace。** 写入中途的抢占损坏文件，朴素覆盖可能留下零个良好检查点。`os.replace` 映射到同一文件系统上的原子 POSIX `rename(2)`（且与 `os.rename` 不同，在 Windows 上也原子覆盖），所以：

1. 将整个状态写入 `latest.pt.tmp`。
2. 对文件（和目录）`fsync` 使字节在重命名前落盘。
3. `os.replace("latest.pt.tmp", "latest.pt")` — 交换是全有或全无。
4. 保留前一个 `latest.pt` 直到新的提交；任意时刻的杀死留下一个完好文件。

**检查点到平台的持久位置，不是本地暂存**（原则 #4）。托管替换节点是*全新的* — 不在云桶 / 网络卷 / 共享 FS 上的东西都没了。在本地磁盘跨暂停持久的市场化机器上，仍定期镜像到持久存储。

**启动时无条件加载最新状态。** 对首次启动（无检查点 → 从头开始）和每次抢占后重启（检查点存在 → 恢复）使用*相同代码路径*。这正是使作业幂等的原因：**相同的启动命令**运行任意次数收敛到相同的最终状态，这正是原则 #7 的"重试相同配置"实际恢复进度而非从零重启的方式。

---

## 4. 托管 spot 框架移动机器；检查点加载恢复状态

托管框架在抢占时**自动配置替换** — 但它们从头重启**进程**。框架移动机器；§3/§5 中编写的检查点加载是恢复进度的东西。这是最常被误解的一点：框架**不会**自行恢复训练。

- **SkyPilot Managed Jobs** — 最强的跨云推荐（在不同区域/云重新配置以追逐容量，然后重新运行任务）。注意：它仅自动恢复抢占/硬件故障 — 用户代码非零退出**不**自动恢复。
- **AWS SageMaker Managed Spot** — 设置 `use_spot_instances=True` + `checkpoint_s3_uri`；SageMaker 在训练期间将检查点目录同步到 S3 并在重启时复制回来（节省约 90%）。陷阱：**`max_wait` 必须大于 `max_run`** — `max_wait` 覆盖等待容量 *加上* 运行时间 *加上* 中断间隔；设得太紧作业在恢复中途被杀死。

通用多云自动故障转移**超出本技能范围** — 用 SkyPilot/dstack 做那个，然后回到这里使*代码*正确恢复，使它们的恢复实际落在进度上。对于弹性 / 多节点层（torchrun `--max-restarts`、Elastic Horovod）参见 `references/multinode.md`；相同不变量成立 — 框架重启进程，每 epoch 快照恢复状态。

---

## 5. Python 检查点/恢复骨架

阅读此获取算法；适配到训练脚本。形状是平台无关的 — 只有 `DURABLE_DIR` 按 profile 变化（§8 脚本覆盖）。

```python
import os, random, signal, time
import numpy as np
import torch

DURABLE_DIR = os.environ["DURABLE_DIR"]   # profile 提供的桶/FS/卷挂载，不是本地暂存
CKPT = os.path.join(DURABLE_DIR, "latest.pt")
CKPT_EVERY_ITERS = 400                     # = round_down(Young/Daly W / sec_per_iter); 见第 2 节

def save_full_state(model, opt, sched, epoch, step):
    """原子写入：tmp -> fsync -> os.replace。任意时刻的杀死留下一个完好文件。"""
    state = {
        "model": model.state_dict(),
        "opt": opt.state_dict(),
        "sched": sched.state_dict(),
        "epoch": epoch, "step": step,        # 恢复精确位置，不是 epoch 开始
        "rng_python": random.getstate(),
        "rng_numpy": np.random.get_state(),
        "rng_torch": torch.get_rng_state(),
        "rng_cuda": torch.cuda.get_rng_state_all(),
    }
    tmp = CKPT + ".tmp"
    with open(tmp, "wb") as f:
        torch.save(state, f)
        f.flush()
        os.fsync(f.fileno())                 # 字节在重命名前落盘
    os.replace(tmp, CKPT)                     # POSIX 原子交换；前文件在此返回前有效

def load_latest_if_any(model, opt, sched):
    """无条件加载最新：相同命令恢复或从头开始。返回 (epoch, step)。"""
    if not os.path.exists(CKPT):
        return 0, 0                          # 首次运行，无检查点 -> 从头开始
    s = torch.load(CKPT, map_location="cpu")
    model.load_state_dict(s["model"])
    opt.load_state_dict(s["opt"])
    sched.load_state_dict(s["sched"])
    random.setstate(s["rng_python"])
    np.random.set_state(s["rng_numpy"])
    torch.set_rng_state(s["rng_torch"])
    torch.cuda.set_rng_state_all(s["rng_cuda"])
    return s["epoch"], s["step"]             # 调用者跳过数据加载器到此位置

# --- 机会性最后刷新仅此而已；不是安全网（第 1 节）---
_preempted = {"flag": False}
def _on_sigterm(signum, frame):
    _preempted["flag"] = True                # 设置标志；在下一个安全边界刷新，不要在这里阻塞
signal.signal(signal.SIGTERM, _on_sigterm)

def train(model, opt, sched, dataloader, total_epochs):
    start_epoch, start_step = load_latest_if_any(model, opt, sched)
    step = start_step
    for epoch in range(start_epoch, total_epochs):
        for batch in dataloader:             # 可恢复 sampler 应快进到 start_step
            # ... forward / backward / opt.step() / sched.step() ...
            step += 1
            if step % CKPT_EVERY_ITERS == 0 or _preempted["flag"]:
                save_full_state(model, opt, sched, epoch, step)
                if _preempted["flag"]:
                    return                   # 宽限窗口可能约 0 秒；刷新后干净退出
```

在信任恢复路径前验证它：在 epoch 中途杀死进程，重新启动*相同*命令，确认 step/epoch/loss 是继续而非重置。信任**加载的**检查点，不是"已恢复"的日志行（原则 #3）。
