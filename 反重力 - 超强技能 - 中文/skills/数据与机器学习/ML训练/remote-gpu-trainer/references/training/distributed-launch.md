# 启动与调试多 GPU / 多节点训练 — torchrun · Accelerate · DeepSpeed · DDP · FSDP

选择启动器、正确设置 rank/world-size 环境变量、选择并行策略（DDP vs FSDP vs ZeRO），以及在 8 个进程静默冻结时找到*哪个* rank 发散了。本层负责*让分布式作业跑起来、不卡死、不静默错分片*；**verifying-dl-experiments** 负责*结果数字是否正确*（LR 随 world size 静默重新缩放、或重启后从 step 0 恢复的运行，是它的关注范围）。在任何启动修复改变了有效批次大小、LR 或精度的位置交叉引用它（**必需**）。

单机多 GPU 是通过 NVLink/PCIe 运行 DDP/FSDP，属于本文件范围。**跨节点**传输（NCCL NIC、fabric-manager、超时、MTU、弹性重启）在 `references/multinode.md`（跨 ≥2 实例的作业**必需**）— 本文件到机器之间的网线处结束。

快速跳转：`grep -in '<keyword>' references/training/distributed-launch.md`（例如 `rdzv`、`local_rank`、`unused`、`hang`、`desync`、`fsdp`、`zero`、`state_dict`、`port`、`barrier`、`accelerate`）。

## 目录

- **启动器与环境** — D1 torchrun 环境契约 · D2 standalone vs rendezvous · D3 LOCAL_RANK-device bug · D4 端口冲突 · D5 accelerate launch · D6 deepspeed 启动器 · D7 选择启动器
- **DDP** — D8 find_unused_parameters · D9 不均匀输入-Join · D10 SyncBN 与缓冲区 · D11 有效批次/LR
- **FSDP** — D12 包装策略 · D13 分片策略 · D14 混合精度 · D15 state_dict 类型
- **DeepSpeed** — D16 ZeRO 阶段 · D17 config.json 旋钮 · D18 auto 与 engine.backward
- **卡死调试**（最高价值） — D19 反同步调试工具包 · D20 单 rank 发散 · D21 rank 条件集合通信 · D22 dataloader 长度不匹配 · D23 eval/print/save 单 rank
- **指针** — 跨节点 NCCL/NIC/超时 → multinode.md · OOM/分片适配 → oom-memory.md · spot 重启 → spot-resilience.md

---

## 启动器与环境

### D1 — 每个启动器必须满足的 rank/world-size 环境契约

**症状**：在 4 GPU 机器上裸跑 `python train.py` 只用**一个** GPU；或 `init_process_group` 永远卡住因为 `MASTER_ADDR`/`RANK` 从未被设置。

**根因**：`torch.distributed` 从**环境变量**读取拓扑，而非 GPU 数量。裸 `python` 不设置任何变量，所以进程组永远无法形成。

**修复**：通过 `torchrun` 启动，它会为每个进程设置完整契约 ([torchrun 文档](https://docs.pytorch.org/docs/2.12/elastic/run.html))：

| 变量 | 含义 |
|---|---|
| `RANK` | 全局 rank `0..WORLD_SIZE-1`（整个作业内唯一） |
| `LOCAL_RANK` | **本节点内**的 rank — 绑定到 GPU（`cuda:LOCAL_RANK`），不是 `RANK`（D3） |
| `WORLD_SIZE` | 总 worker 数 = `nnodes × nproc_per_node` |
| `LOCAL_WORLD_SIZE` | 本节点上的 worker 数 |
| `GROUP_RANK` | 节点的 rank（`0..nnodes-1`） |
| `MASTER_ADDR` / `MASTER_PORT` | 托管 c10d TCP store 的 rank-0 的 FQDN + 端口 |

脚本读取它们（`int(os.environ["LOCAL_RANK"])`），调用 `init_process_group(backend="nccl")`（GPU 用 NCCL；CPU 用 `gloo`），并在分配任何 CUDA 张量前 `set_device(LOCAL_RANK)`。

### D2 — 单节点用 `--standalone`；多节点需要共享 rendezvous id+端点

**症状**：将单节点 `torchrun` 命令复制到第二个节点，要么在 init 时卡住，要么两个节点各自形成独立的 1 节点组。

**根因**：单节点和多节点使用**不同的 rendezvous**。`--standalone` 在 localhost 自托管 rendezvous（无需协调）；多节点要求每个节点指向*同一个*外部 rendezvous 服务器且使用*同一个* job id。

**修复** ([torchrun 文档](https://docs.pytorch.org/docs/2.12/elastic/run.html))：
```bash
# 单节点，4 GPU — 自包含，无需管理 addr/port
torchrun --standalone --nnodes=1 --nproc-per-node=4 train.py

# 多节点：每个节点上运行相同命令；仅环境派生的 node-rank 不同
torchrun --nnodes=2 --nproc-per-node=8 \
         --rdzv-id=$JOB_ID --rdzv-backend=c10d \
         --rdzv-endpoint=$HEAD_IP:29400 train.py
```
`c10d` 是推荐后端（无 etcd 依赖）。`--nnodes=1:4` 启用弹性缩放。跨节点网络健康（NIC 固定、fabric-manager、超时）见 `references/multinode.md`。

### D3 — 所有进程落在 GPU 0 上（`RANK` vs `LOCAL_RANK` bug）

**症状**：多节点时，节点 1 的所有进程堆积到 `cuda:0` 并 OOM，而 GPU 1-7 空闲；单节点时看起来正常。

**根因**：脚本做了 `torch.cuda.set_device(RANK)`。单节点时 `RANK==LOCAL_RANK` 所以 bug 隐藏；2 节点作业的节点 1 上 `RANK` 是 8-15 但节点只有 GPU 0-7，所以 `set_device` 回绕/冲突，所有流量汇聚到设备 0。

**修复**：**始终用 `LOCAL_RANK` 索引本地设备**，绝不用 `RANK`：`torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))`。`RANK` 选择*数据分片*；`LOCAL_RANK` 选择*物理 GPU*。

### D4 — 在一个节点上启动第二个作业时 `RuntimeError: Address already in use`

**症状**：同一机器上第二个 `torchrun`（如并行消融单元）立即死于 `errno 98: Address already in use`。

**根因**：两个作业默认都用 `MASTER_PORT=29500`；c10d TCP store 无法绑定第一个作业已占用的端口 ([pytorch#85604](https://github.com/pytorch/pytorch/issues/85604))。

**修复**：给每个共存作业唯一端口**且**互不重叠的 GPU：
```bash
CUDA_VISIBLE_DEVICES=0,1 torchrun --standalone --nproc-per-node=2 --master-port=29500 train.py &
CUDA_VISIBLE_DEVICES=2,3 torchrun --standalone --nproc-per-node=2 --master-port=29600 train.py &
```
或使用 `--rdzv-endpoint=localhost:0` 让 torchrun 选一个空闲端口。跨实例扇出单元 → `references/parallel_ablation.md`。

### D5 — HF Accelerate：`accelerate launch` 读取配置，不是 torchrun 标志

**症状**：`accelerate launch train.py` 虽有 4 张卡但只跑单 GPU，因为没有配置或 `compute_environment` 默认为单进程。

**根因**：Accelerate 封装相同的环境契约（D1）但从 `~/.cache/huggingface/accelerate/default_config.yaml`（由 `accelerate config` 生成）或 CLI 标志读取 ([启动文档](https://huggingface.co/docs/accelerate/en/basic_tutorials/launch))。

**修复**：生成一次配置，然后对着它启动 — 在无头租用环境中，直接写 YAML 而非交互式 `accelerate config`：
```bash
accelerate launch --multi_gpu --num_processes=4 --mixed_precision=bf16 train.py
# 或一个已检入的 YAML（可复现、可 diff）：
accelerate launch --config_file configs/acc_fsdp.yaml train.py
```
切换 DDP↔FSDP↔DeepSpeed 只是配置切换 — 训练脚本不变。同样的 `--num_machines`/`--machine_rank`/`--main_process_ip` 映射到多节点（D2 领域）。

### D6 — DeepSpeed：`deepspeed` 启动器 vs `accelerate launch`，以及 `hostfile`

**症状**：多节点 `deepspeed train.py` 找不到另一台主机，或 `--num_gpus` 被忽略。

**根因**：`deepspeed` 启动器从 `hostfile`（`worker-1 slots=8`）发现节点，与 torchrun 的 rendezvous 不同。在 HF 下，通常更干净的方式是让 `accelerate launch`（搭配 DeepSpeed 插件/配置）来驱动 ([HF DeepSpeed](https://huggingface.co/docs/accelerate/en/usage_guides/deepspeed))。

**修复**：单节点 `deepspeed --num_gpus=8 train.py --deepspeed ds_config.json`；多节点 `deepspeed --hostfile=hostfile --num_gpus=8 train.py ...`。使用 HF Trainer/Accelerate 时，通过 `--config_file` 传递配置让它生成 worker — 不要混用两种启动器。

### D7 — 选择哪个启动器 / 并行策略 — 一句话决策

- **模型装得下单 GPU，只想要更多吞吐** → **DDP**（`torchrun`），最简单、最快。每个 rank 持有完整副本。
- **模型装不下（参数+优化器+梯度 ≈ 18 B/参数，见 oom-memory.md M1）** → 分片：**FSDP**（PyTorch 原生）或 **DeepSpeed ZeRO**（更丰富的卸载）。分片适配阶梯 → `references/training/oom-memory.md` M9。
- **HF 生态 / Trainer** → **Accelerate** 作为启动器；翻转一个配置字段选择 DDP/FSDP/ZeRO。
- **需要分别 CPU/NVMe 卸载参数和优化器，或 ZeRO-Infinity** → **DeepSpeed**（FSDP1 卸载是全有或全无；[HF 概念指南](https://github.com/huggingface/accelerate/blob/main/docs/source/concept_guides/fsdp_and_deepspeed.md)）。

---

## DDP

### D8 — `find_unused_parameters` — "Expected to have finished reduction" 错误 vs 静默卡死

**症状**：`RuntimeError: Expected to have finished reduction in the prior iteration before starting a new one. ... parameters that were not used in producing loss` ([HF 讨论](https://discuss.huggingface.co/t/runtimeerror-expected-to-have-finished-reduction-in-the-prior-iteration-before-starting-a-new-one-this-error-indicates-that-your-module-has-parameters-that-were-not-used-in-producing-loss/64760))。

**根因**：DDP 在每个参数上注册 allreduce 钩子并每步等待*全部*完成。如果某个分支（冻结头、条件层）不产生梯度，其桶永远不触发，reduction 永远完不成。

**修复 — 按优先级**：
1. **最佳**：让每个输出都参与 loss（通常真正的 bug 是丢失/断开的头）。
2. 如果某个分支*确实*在某些步中未使用，`DDP(model, find_unused_parameters=True)` — 但它每步增加完整图遍历且**可能大幅变慢** ([PyTorch 论坛](https://discuss.pytorch.org/t/process-got-stuck-when-set-find-unused-parameters-true-in-ddp/106078))。仅在 (1) 不可能时使用。
3. 如果返回值是 dict/list，DDP 可能无法定位输出张量 — 展平或简化 `forward` 返回。
> 设置 `find_unused_parameters=True` 来*掩盖*真正 bug 只会隐藏问题 — 确认参数确实是有意不用的，不要让诊断静默。

### D9 — Rank 批次数不等 → 最后一步卡死（不均匀输入）

**症状**：训练完成一个 epoch 的大部分后在**最后一个批次冻结**；某个 rank 样本数少，已退出循环，而其他 rank 永远等在 allreduce ([PyTorch 论坛](https://discuss.pytorch.org/t/understanding-distributedsampler-and-dataloader-drop-last/206271))。

**根因**：DDP 假设每个 rank 运行**相同数量的集合通信**。`DistributedSampler` 通过填充（`drop_last=False`）或丢弃（`drop_last=True`）来均衡，但自定义采样器、per-rank 过滤或 `IterableDataset` 可能导致计数不均 — 短的 rank 停止调用 allreduce。

**修复**：
- 使用 `DistributedSampler`（默认均衡）并在每个 rank 上设置**相同的** `drop_last`。
- 真正的不均匀输入（变长、无法填充）：用 **Join** 上下文管理器包裹循环 — `from torch.distributed.algorithms.join import Join; with Join([model]): for batch in loader: ...` — 它镜像缺失 rank 的集合通信，使完成的 rank 不会死锁 ([Join 教程](https://docs.pytorch.org/tutorials/advanced/generic_join.html))。
- 每个 epoch 总是调用 `sampler.set_epoch(epoch)`，否则每个 epoch 看到相同的洗牌（静默正确性 bug — **verifying-dl-experiments** **必需**）。

### D10 — BatchNorm 统计量跨 rank 发散；缓冲区未同步

**症状**：DDP 在相同有效批次下比单 GPU 收敛更差，或评估不稳定 — 每个 rank 只在其本地分片上计算了 BN 统计量。

**根因**：DDP all-reduce **梯度**，不是**缓冲区**（BN 运行均值/方差）。小的每 GPU 批次下，每个副本的 BN 统计量有噪声且不一致。

**修复**：在包装前将 BN 转为同步 BN：`model = nn.SyncBatchNorm.convert_sync_batchnorm(model)` 然后 `DDP(model, ...)`。每个 BN 层增加一次集合通信（有代价），但 BN 统计量变为全局的。（指标是否*需要* SyncBN 由 **verifying-dl-experiments** 判断。）

### D11 — N 个 GPU 静默 N× 有效批次（LR 现在错了）

**症状**：从 1→8 GPU 使训练发散或停滞；loss 曲线形状不同即使"相同配置"。

**根因**：DDP 保持每 GPU 批次大小，所以**有效批次 = per_gpu_batch × world_size**。为 1-GPU 批次调的 LR 现在不匹配（通常欠缩放）。这是最常见且最静默的多 GPU 回归。

**修复**：随有效批次缩放 LR（线性缩放规则作为基线，加 warmup）并在运行清单中记录 `world_size`、每 GPU 批次和有效批次。**这改变了科学结论** — 声明它；将 1-GPU 基线与 LR 未缩放的 8-GPU 运行比较不是干净的数据点（**verifying-dl-experiments** **必需**）。

---

## FSDP（全分片数据并行）

### D12 — FSDP 将整个模型包装为一个单元 → 无内存节省（包装策略）

**症状**：启用了 FSDP 但 VRAM 几乎没降 vs DDP，或在 all-gather 一个巨大平面参数时 OOM。

**根因**：没有 `auto_wrap_policy` 时，FSDP 将**整个模型作为一个 FSDP 单元** — 必须一次 all-gather 所有参数，使分片失效 ([FSDP 教程](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html))。

**修复**：按 transformer 块包装，使一次只 all-gather 一个块的参数：
```python
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
import functools
policy = functools.partial(transformer_auto_wrap_policy,
                           transformer_layer_cls={LlamaDecoderLayer})
```
在 Accelerate 下设置 `fsdp_auto_wrap_policy: TRANSFORMER_BASED_WRAP` + `fsdp_transformer_layer_cls_to_wrap: LlamaDecoderLayer` ([HF FSDP](https://huggingface.co/docs/accelerate/en/usage_guides/fsdp))。FSDP2（`fully_shard`）是当前 API；包装原则相同。

### D13 — 分片策略：FULL_SHARD vs SHARD_GRAD_OP vs HYBRID

**症状**：FSDP 受通信限制（allgather/reducescatter 占据步时间主导），或仍然 OOM。

**根因**：策略权衡内存与通信。`FULL_SHARD`（默认，== ZeRO-3）分片参数+梯度+优化器 — 最大内存节省，最大通信。`SHARD_GRAD_OP`（== ZeRO-2）仅分片梯度+优化器，保持参数常驻 — 更少通信，更多内存。

**修复**：按瓶颈约束选择 — OOM → `FULL_SHARD`；通信瓶颈但装得下 → `SHARD_GRAD_OP`。在**多节点**作业中，节点内 NVLink 快但跨节点慢，`HYBRID_SHARD` 在节点内分片、跨节点复制（减少跨节点流量；配合 `references/multinode.md` NIC 调优）。

### D14 — FSDP 混合精度：loss 发散或缓冲区保持 fp32

**症状**：bf16 FSDP 运行在 bf16 DDP 正常的地方发散；或 BN/位置缓冲区静默以错误 dtype 运行。

**根因**：FSDP 混合精度是**按张量类别显式设置**的，通过 `MixedPrecision(param_dtype, reduce_dtype, buffer_dtype)` — 不是单个 AMP 标志。设置 `param_dtype=bf16` 但保留 `reduce_dtype=fp32`（或反之）会改变梯度 reduction 精度；FSDP 保持 fp32 主权重并转换为 bf16 用于前向 ([pytorch#146114](https://github.com/pytorch/pytorch/issues/146114))。

**修复**：有意设置全部三个 — 安全默认值是 `param_dtype=bf16, reduce_dtype=fp32`（保持 reduction 在 fp32 以稳定），并显式设置 `buffer_dtype` 使缓冲区不漂移。分片训练**优先 bf16 而非 fp16**（不需要 loss scaler）。数值正确性检查由 **verifying-dl-experiments** 负责；本条目只确保 dtype *被设置*，而非留为隐式。

### D15 — Checkpoint OOM 或保存了无法加载的分片（state_dict 类型）

**症状**：`FSDP.state_dict()` 在 rank 0 上 OOM 主机内存；或每个 rank 写了 `.pt` 但在不同 world size 下重载失败。

**根因**：FSDP 有三种 state-dict 类型。`FULL_STATE_DICT` 将整个模型 gather + unflatten 到**rank-0 CPU**（峰值主机内存，单写入者）；`SHARDED_STATE_DICT` 每 rank 写一个分片（可缩放，但与布局绑定）；`LOCAL_STATE_DICT` 是原始平面参数 ([HF FSDP](https://huggingface.co/docs/accelerate/en/usage_guides/fsdp))。

**修复**：
- 大模型 / 需要可缩放恢复：通过 Distributed Checkpoint (DCP) 使用 **`SHARDED_STATE_DICT`** — 每个 rank 保存其分片，重载可重新分片到任意 world size。
- 需要单个可移植文件（导出/推理）：`FULL_STATE_DICT` 搭配 `rank0_only=True, offload_to_cpu=True`，使只有 rank 0 在 CPU 上物化（避免全 rank OOM）。FSDP2 使用 `broadcast_from_rank0=True` 在 rank 0 上加载完整字典然后分片出去。
- 原子写入 + 启动时加载最新是恢复脊骨，无论哪种类型 → `references/spot-resilience.md` 和 `references/multinode.md` MN5（torchrun 重启恢复*组*，永远不恢复*状态*）。

---

## DeepSpeed

### D16 — ZeRO 阶段选择（1/2/3）及各阶段分片什么

**症状**：ZeRO 启用但仍 OOM，或通信开销大但内存不需要。

**根因**：各阶段跨数据并行 rank 逐步分片更多 ([DeepSpeed ZeRO](https://www.deepspeed.ai/tutorials/zero/))：
**阶段 1** = 优化器状态 · **阶段 2** = + 梯度 · **阶段 3** = + 参数（== FSDP `FULL_SHARD`）。

**修复**：用能装下的最小阶段 — 阶段 2 是*几乎*装得下的模型的常见甜蜜点；阶段 3 用于梯度分片后仍装不下的；只在阶段 3 单独仍 OOM 时加 **ZeRO-Offload**（CPU）或 **ZeRO-Infinity**（NVMe）（每种卸载用大量减速换容量 → `references/training/oom-memory.md` M10）。

### D17 — `ds_config.json` 中真正重要的旋钮

**症状**：配置已应用但行为未变，或初始化时出现晦涩的 key 错误。

**根因**：DeepSpeed 从 JSON 读取，且一旦提供 `deepspeed_config_file`，多个 Accelerate/Trainer 字段会被**忽略** ([HF Accelerate DeepSpeed](https://huggingface.co/docs/accelerate/en/usage_guides/deepspeed))。

**修复** — 关键配置项：
```jsonc
{
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {"device": "cpu"},      // 或 "nvme"
    "offload_param":     {"device": "cpu"}
  },
  "bf16": {"enabled": true},                       // 优先于 fp16（无需 loss-scale 调参）
  "gradient_accumulation_steps": "auto",           // 让 HF 从 Trainer 填充
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_clipping": "auto"
}
```
当 JSON 存在时，`gradient_accumulation_steps`、`gradient_clipping`、`zero_stage`、`offload_*_device` 和 `mixed_precision` 从 Accelerate 配置中**被 JSON 覆盖** — 在 JSON 中设置它们，不要在两个地方设置。

### D18 — `"auto"` 不匹配和 `loss.backward()` vs `engine.backward()`

**症状**：优化器步数远少于预期（梯度累积被重复计算），或关于未缩放梯度的 `RuntimeError`。

**根因**：两个陷阱。(a) 在 Trainer/Accelerate 配置**和** JSON 中同时将 `gradient_accumulation_steps` 设为非 `"auto"` 值会相乘。(b) 使用 DeepSpeed 自带 AMP 时，梯度缩放在引擎内部 — 直接调用 `loss.backward()` 而非 `model_engine.backward(loss)` 会跳过缩放 ([DeepSpeed engine](https://github.com/microsoft/DeepSpeed/blob/master/deepspeed/runtime/engine.py))。

**修复**：在**一个**地方设置累积（JSON 中用 `"auto"`，让 HF 填充）；手动循环中调用 `model_engine.backward(loss); model_engine.step()` — DeepSpeed 下绝不要直接 `loss.backward()` / `optimizer.step()`。

---

## 卡死调试 — 调试冻结的分布式作业（最高价值章节）

分布式卡死**没有回溯** — 每个 rank 坐在集合通信里等待一个永远不会调用它的 peer。要做的就是识别*哪个* rank 发散了和*哪个*集合通信不匹配。（不同于**单进程**消失 — OOM/重启/SSH-HUP/杀死见 `gotchas_universal.md` U3；跨节点原因 — fabric-manager、错误 NIC、MTU、掩盖真正故障的 1800 秒 NCCL 超时 — 见 `references/multinode.md` MN1-MN4。）

### D19 — 反同步调试工具包：将静默冻结变为具名不匹配

**症状**：所有 rank 冻结，GPU 100% SM 利用但 0% 内存利用（自旋等待），无输出。

**根因**：集合通信反同步 — rank 入队了*不同*的集合通信，或一个 rank 从未到达其他 rank 阻塞的集合通信。

**修复 — 设置这些并重新启动卡死的作业**：
- `export TORCH_DISTRIBUTED_DEBUG=DETAIL` + `export TORCH_CPP_LOG_LEVEL=INFO` → 不匹配时 PyTorch 打印 `Detected mismatch between collectives on ranks`，命名每个 rank 的操作 + 序列号 ([PyTorch 论坛](https://discuss.pytorch.org/t/torch-distributed-collectives-call-logging/172726))。（DETAIL 本身产生集合通信 — 用于*诊断*，生产环境移除；它会干扰时序。）
- `export NCCL_DEBUG=INFO`（或 `WARN`）→ 日志**先停住**的节点（在其他节点打印拓扑之前）是罪魁祸首。
- `export TORCH_NCCL_ASYNC_ERROR_HANDLING=1`（旧版 PyTorch：`NCCL_ASYNC_ERROR_HANDLING=1`）→ 死亡的 rank *迅速*拆除组，而非每个 rank 等待 1800 秒 NCCL 超时（`references/multinode.md` MN3）。
- **飞行记录器**（`TORCH_NCCL_TRACE_BUFFER_SIZE=2000`）导出每个 rank 最近 N 次集合通信及堆栈跟踪 — 读取它可看到哪个 rank 的队列落后一个集合通信。

### D20 — 一个 rank 发散（NaN/OOM）且存活者等它而卡死

**症状**：训练运行了一段时间后冻结；一个 rank 的最后日志显示 NaN、OOM 或数据/CUDA 错误，其余卡在 allreduce。

**根因**：崩溃或提前 `return` 的 rank **停止调用集合通信**；其他 rank 阻塞。崩溃是原因，卡死是症状 — 没有异步错误处理（D19）时，它在 30 分钟后才以超时形式出现，远离原因。

**修复**：配合 `TORCH_NCCL_ASYNC_ERROR_HANDLING=1`，组在真正故障附近中止。然后修复*发散的 rank*，不是卡死 — 常见根因：一个分片碰到坏样本（rank 相关数据）、per-rank OOM 来自不均匀序列长度（最长批次落在某个 rank → `oom-memory.md` M16）、或 LR/精度导致的 NaN。不要通过降低批次大小来"修复"一个实际上是某个 rank 数据 bug 的卡死。

### D21 — rank 条件集合通信（`if rank == 0:` 死锁）

**症状**：可复现地在*相同*位置卡死 — 通常是验证、日志或检查点保存。

**根因**：一个集合通信（或 `dist.barrier()`，或隐含集合通信的操作如 `all_gather`、SyncBN、或指标 `all_reduce`）被放在 rank 条件分支内。Rank 0 调用它；其他 rank 跳过；所有人死锁。经典案例是"只在 rank 0 保存/日志"，其中保存路径触发集合通信 ([Lightning#19604](https://github.com/Lightning-AI/pytorch-lightning/issues/19604))。

**修复**：集合通信必须在**所有 rank 上无条件运行**。只限制*副作用*，不限制集合通信：在每个 rank 上计算指标的 `all_reduce`，然后 `if rank == 0: log(value)`。`barrier()` 必须被每个 rank 到达或都不到达。审查每个 `if rank/local_rank == 0` 块中的隐藏集合通信。

### D22 — Dataloader 长度跨 rank 不匹配（以及 `set_epoch` 洗牌 bug）

**症状**：epoch 末尾卡死（D9 的机制），或每个 epoch 训练在完全相同的数据顺序上。

**根因**：两个相关的 dataloader 故障。(a) 每个 rank `len(loader)` 不等 → 短的 rank 停止调用集合通信。(b) 忘记 `sampler.set_epoch(epoch)` → `DistributedSampler` 每个 epoch 重新洗牌结果相同。

**修复**：所有 rank 上相同的 `batch_size`/`drop_last`/采样器；每个 epoch 调用 `set_epoch`；真正不均匀数据使用 **Join**（D9）。洗牌陈旧是正确性 bug — **verifying-dl-experiments** **必需**。

### D23 — `print` / `tqdm` / eval / `torch.save` 交织看起来像卡死（但不总是）

**症状**：8 个 rank 的日志混乱交织；或评估期间明显冻结但只有 rank 0 应该在工作。

**根因**：默认**每个 rank 执行一切** — 8× 打印、8× 评估、8 个 race 写同一个检查点文件（损坏它）。如果评估/保存路径包含集合通信且*也*被 rank 门控，就是 D21 死锁；否则只是嘈杂 + 浪费 + 文件竞争。

**修复**：将纯副作用（日志、进度条、文件写入）限制在 `if rank == 0:` — 但将任何集合通信放在门控*外面*（D21。仅从 rank 0 写检查点，写到临时路径，原子重命名（`references/spot-resilience.md`），然后 `dist.barrier()`（在**所有** rank 上）再让其他 rank 读取文件。真正的卡死 vs 嘈杂但有进展通过飞行记录器 / 步计数器（D19）区分，而非通过日志汤。

---

## 指针 — 其他地方已处理，不要重复

- **跨节点网络**（NCCL NIC 固定、`nvidia-fabricmanager`、掩盖死亡 rank 的 1800 秒超时、巨型帧 MTU、torchrun/Horovod 弹性重启恢复*组*而非*状态*）→ `references/multinode.md`（≥2 实例**必需**）。
- **分片以适配 OOM 的模型**（FSDP/ZeRO 阶梯按成本排列、激活检查点、卸载、LoRA/QLoRA、阅读 OOM 堆栈）→ `references/training/oom-memory.md`。
- **重启恢复机制**（原子写入、加载最新、节奏、抢占信号）→ `references/spot-resilience.md`；脊骨是 `references/principles.md` #8。
- **单进程消失**（OOM vs 重启 vs SSH-HUP vs 手动杀死）→ `references/gotchas_universal.md` U3；**`num_workers` 的 cgroup 主机内存 OOM** → U9；**DDP 运行崩溃后的僵尸 VRAM** → U11。
- **结果数字是否真实**（LR 重新缩放的运行、从 0 重启的运行、洗牌陈旧、SyncBN 必要性、精度变更）→ **verifying-dl-experiments**（在上面每个"此修复改变科学结论"注释处**必需**）。
