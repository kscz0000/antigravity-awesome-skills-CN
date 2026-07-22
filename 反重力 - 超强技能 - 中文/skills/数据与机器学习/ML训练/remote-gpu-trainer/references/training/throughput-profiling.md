# 吞吐与性能分析 — 让训练跑得快，找到那一个瓶颈

如何判断租用 GPU *为什么*没喂饱（GPU 瓶颈 vs 数据瓶颈 vs 通信瓶颈），然后按成本顺序应用正确的加速 — 从免费的 dataloader 旋钮到 `torch.compile` 和融合注意力。本层负责*让它跑得快 + 定位机械瓶颈*；**verifying-dl-experiments** 负责*结果数字是否正确*。在任何加速可能改变科学结论的位置交叉引用它（**必需**）— 一个改变数值的内核、一次精度切换、丢弃样本以"跑更快"。

> **将运行适配到机器 — 然后为任何比较固定它。** 自动调整 batch/`num_workers` 以匹配测量的 GPU/VRAM/vCPU（Phase 0）来用好卡片对一个独立作业来说没问题；但对于消融或基线 vs 变体的比较，**在所有单元中固定相同的 batch** — 按机器自动最大化会静默改变一个变量并破坏可比性（**verifying-dl-experiments**，必需）。

快速跳转：`grep -in '<keyword>' references/training/throughput-profiling.md`（例如 `bound`、`workers`、`compile`、`recompile`、`flash`、`sdpa`、`nsys`、`py-spy`、`channels_last`、`tf32`、`overlap`）。

## 目录

- **先诊断** — T1 三路分类（GPU/数据/通信瓶颈） · T2 利用率骗人指针 · T3 廉价 CPU/GPU 忙闲分流
- **Dataloader（GPU 饿死的第一大原因）** — T4 num_workers · T5 persistent_workers · T6 pin_memory + non_blocking · T7 prefetch_factor · T8 IO瓶颈 vs CPU变换瓶颈
- **免费/近免费旋钮** — T9 TF32 + 矩阵乘法精度 · T10 cudnn.benchmark · T11 channels_last · T12 set_to_none + 禁用调试API
- **为速度的混合精度** — T13 bf16/fp16 吞吐
- **内核** — T14 SDPA / FlashAttention · T15 torch.compile 收益 · T16 torch.compile 重编译陷阱
- **内存↔速度权衡** — T17 激活检查点速度代价 · T18 批次大小 vs 吞吐
- **性能分析器** — T19 torch.profiler（是否数据瓶颈） · T20 nsys / Nsight Systems · T21 py-spy（实时，无需重启） · T22 内存快照指针
- **多GPU / 多节点通信** — T23 DDP/FSDP 计算-通信重叠
- **指针** — gotchas_universal.md U8/U21/U24/U25/U38 · oom-memory.md · distributed-launch.md · multinode.md · verifying-dl-experiments（技能）

---

## 先诊断 — 不要盲目调参

### T1 — 三路分类：GPU瓶颈 vs 数据瓶颈 vs 通信瓶颈（碰旋钮前先决定）

**症状**：训练"慢"，本能是随机改模型或批次大小。

**根因**：吞吐量在任一时刻恰好被三种资源之一限制；每种修复互不相关，所以猜测浪费计费时间（原则 #1）。

**修复 — 每种一次廉价读数分类**（启发式：util 持续 >90% ⇒ GPU 瓶颈；低/波动 ⇒ 其他；CPU+GPU 都低 ⇒ I/O — https://apxml.com/courses/planning-optimizing-ai-infrastructure/chapter-5-strategies-for-performance-optimization/identifying-performance-bottlenecks）：
- **GPU 瓶颈**（好情况）：util 高*且* SM 时钟/功耗高（T2）；加 worker 无效。仅剩杠杆：内核（T14–T15）、精度（T13）、更大的卡。
- **数据瓶颈**：util 低但非零或锯齿波动，主机 CPU 忙于 `DataLoader`/变换；trace 显示 GPU 空闲间隙与 CPU 数据工作对齐（T19）。去 T4–T8。
- **通信瓶颈**（仅多 GPU/节点）：每 GPU util 高，扩展效率差；时间花在 `nccl:all_reduce`/`all_gather` 未与计算重叠。去 T23。

最高信号仪表是**性能分析器 trace**（T19）— 在改变任何东西之前读它。

### T2 — `nvidia-smi` GPU-Util % 骗人；关联时钟 + 功耗 → gotchas_universal.md U21

100% 利用率可能隐藏一个饿死的 GPU（少量小内核读为 100%）。完整诊断 — 通过 `nvidia-smi dmon -s pucvmet -d 1` 关联 `clocks.current.sm` + 内存带宽利用率 + 功耗，以及散热/功耗节流减速 — 在 **gotchas_universal.md U21/U23**；在断定运行是 GPU 瓶颈之前先读它。*0% 利用率但仍在运行*（CPU 数据瓶颈）的反面是 **U38**，属于 verifying-dl-experiments。

### T3 — 还没接性能分析器时的廉价分流：主机 CPU 忙吗？

**症状**：需要 30 秒回答"GPU 还是数据？"然后才能插桩。

**修复**：同时观察 GPU 和 CPU 约 10 秒 —
```bash
nvidia-smi dmon -s pu -d 1 -c 10          # 每秒 SM% + 功耗；锯齿/低 = 饿死
top -b -n 1 | grep -i python | head        # 一个 worker 约占 100% CPU = CPU变换瓶颈
```
GPU SM% 高且稳定 ⇒ GPU 瓶颈（到此为止，去内核/精度）。GPU SM% 锯齿波动同时一个 python worker CPU 满载 ⇒ 数据瓶颈（T4–T8）。都空闲 ⇒ I/O 瓶颈（暂存到 NVMe，U8）。然后用真实 trace 确认（T19）再投入修复。**GPU SM% 低同时*多个* python 线程在少数核心上抖动（不是一个 worker 满载）⇒ 算子内线程过度订阅**在 vCPU 切片上，不是数据瓶颈 — 将 `OMP_NUM_THREADS` 限制为 cgroup 配额（gotchas_universal.md **U40**），不要加 dataloader worker。

---

## Dataloader — 租用 GPU 空闲的第一大原因

部分饿死的旋钮集（及其顺序）在 **gotchas_universal.md U24**；本节是每个旋钮的*为什么/何时*。每个解决*不同*的故障，所以按症状应用，不要盲目全抄。

### T4 — `num_workers`：0 意味着主进程串行加载（默认就饿死 GPU）

**症状**：`DataLoader(num_workers=0)`（默认）— 每个批次在主线程获取，GPU 等待整个获取过程。

**根因**：`num_workers=0` 时"数据将在主进程中加载" — 数据准备和计算之间无重叠（https://docs.pytorch.org/docs/2.12/data.html）。

**修复**：设 `num_workers > 0` 异步加载，将获取与 GPU 步重叠。从 `cores − 1` 开始，但**按每 worker 内存而非 CPU 数量调整** — 每个 worker `fork` 完整复制数据集中的任何大对象；太多会 OOM cgroup 并裸 `Killed`（二次陷阱 + 调整规则在 **gotchas_universal.md U9**）。不单调：超过喂饱 GPU 的点后，额外 worker 只增加内存和启动开销。

### T5 — `persistent_workers=True`：停止每个 epoch 付 worker 启动开销

**症状**：每个 **epoch 开始**时有明显停顿（尤其是短 epoch / 多 epoch）；worker 重生时 GPU 空闲。

**根因**：默认 `persistent_workers=False` 在数据集被消费一次后关闭所有 worker 并**下个 epoch 重新 fork** — 每次重新导入、重新打开文件、重建数据集对象（https://docs.pytorch.org/docs/2.12/data.html）。

**修复**：`persistent_workers=True` 在 epoch 间保持 worker Dataset 实例存活，消除每 epoch 重生开销。需要 `num_workers > 0`。当 epoch 短或数据集 `__init__` 很重（加载索引/清单）时收益最大。

### T6 — `pin_memory=True` + `non_blocking=True`：重叠主机→设备拷贝

**症状**：H2D 拷贝（`x.to('cuda')`）位于获取和前向之间的关键路径上。

**根因**：可分页内存张量必须由驱动通过固定缓冲区分段后才能 DMA；同步 `.to(device)` 阻塞步骤。"使用 GPU 时最好设 `pin_memory=True`"（https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html）。

**修复**：`DataLoader(pin_memory=True)` 分配页锁定批次，**然后**用 `x = x.to(device, non_blocking=True)` 传输，使拷贝在拷贝流上异步运行并重叠计算。两半都需要 — 仅 `pin_memory` 仍阻塞；`non_blocking` 无固定内存时静默回退到阻塞拷贝。消耗主机内存（固定页不可换出）— 如果压力 cgroup 则回退（U9）。

### T7 — `prefetch_factor`：当获取时间有突发时加深队列

**症状**：开了 worker，GPU 仍周期性停顿 — 每 *N* 步（N = `num_workers`）有长空闲间隙，因为所有 worker 都在忙于生成下一批次当 GPU 请求时（https://docs.pytorch.org/tutorials/intermediate/tensorboard_profiler_tutorial.html）。

**根因**：`prefetch_factor` 在 `num_workers>0` 时默认 **2**（0 时为 None）— "2 意味着所有 worker 预取的总批次数为 `2 * num_workers`"（https://docs.pytorch.org/docs/2.12/data.html）。浅队列无法吸收每样本获取/解码时间的方差尖峰。

**修复**：提高 `prefetch_factor`（3–4）使 worker 跑在前面并隐藏突发 — 代价是更多常驻批次在内存中（重新检查 U9）。这是一个*平滑*旋钮，不是乘数：如果**平均**获取速率低于 GPU 消费速率，加多少深度都没用 — 修复速率（worker T4、GPU 变换 T8、NVMe U8）。

### T8 — IO瓶颈 vs CPU变换瓶颈是不同的数据瓶颈情况（不同修复）

**症状**：数据瓶颈（T1），但加 worker 几乎无效。

**根因 — 拆分情况**：
- **IO 瓶颈**：字节从网络/HDD/对象存储慢速到达；worker 坐在 `read` 中。将工作集暂存到实例本地 **NVMe**（HDD→NVMe 差距可达约 35 倍）= **gotchas_universal.md U8**；大量小文件的事务死亡 + **分片为 tar / WebDataset** 修复 = **U25**。
- **CPU 变换瓶颈**：重的逐样本增强（resize/decode/FFT）饱和 CPU；worker CPU 满载（T3），受核心数限制。将变换移到 **GPU**（NVIDIA DALI、`torchvision.transforms.v2` 在张量上、kornia）利用空闲 GPU 周期。*0% 利用率*串行变换变体是 **U38**，属于 verifying-dl-experiments **必需**（它也负责 GPU 侧变换是否改变了数据分布）。

**修复**：读 trace（T19）— 时间在 `read`/`stat` ⇒ U8/U25；时间在变换函数 ⇒ 移到 GPU。

---

## 免费/近免费旋钮（在任何机器上启动时设一次）

### T9 — TF32 / `set_float32_matmul_precision("high")` — "为什么 A100 慢"脚枪

Ampere+ 上任何 fp32 矩阵乘法路径的最大免费提速；**自 PyTorch 1.12 起默认关闭**。决策和确切旋钮（`torch.set_float32_matmul_precision("high")`、旧版 `allow_tf32` 标志、HF Trainer 的 `--tf32 1`、收敛影响）由 **references/training/precision-stability.md P2** 负责（交叉链接到那里；不要重复）。如果全新 PyTorch 2.x 租用环境的 fp32 密集运行慢 2–4 倍且无 bug，这是第一嫌疑。

### T10 — `cudnn.benchmark=True`：自动调优卷积算法（仅固定输入形状）

**症状**：卷积密集网络（CNN/UNet）比预期慢；输入形状恒定。

**根因**：默认 cuDNN 选择通用卷积算法；自动调优器对每个新形状的第一个批次做基准测试并缓存最快的（https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html）。

**修复**：启动时 `torch.backends.cudnn.benchmark = True` 一次。**仅在输入形状稳定时有帮助** — 可变形状（动态分辨率、不等长批次）会为每个新形状重新调优并*损失*时间。权衡：它是**非确定性的**（按首次批次时序选择），所以与确定性旋钮冲突 — 是否为干净数据点启用由 precision-stability P19 / verifying-dl-experiments（U36，**必需**）决定。

### T11 — `channels_last`：AMP 下卷积网络的免费 Tensor Core 提速

**症状**：混合精度下的 CNN 未命中 Tensor Core；吞吐低于卡的潜力。

**根因**：默认 NCHW 连续布局在 Tensor Core 卷积前后强制布局转置。

**修复**：将模型和输入转为 `memory_format=torch.channels_last` — `model = model.to(memory_format=torch.channels_last)` 和 `x = x.to(memory_format=torch.channels_last)`。优化使用 Tensor Core + AMP 的卷积网络（https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html）。标记为实验性且仅对 CNN 有效（纯 transformer 无收益）。无数值变化 — 纯布局提速。

### T12 — `set_to_none` + 禁用调试 API（两个免费的每步开销要移除）

- **`optimizer.zero_grad(set_to_none=True)`**（PyTorch 2.0 起**默认**）替代零填充 — 赋 `None` 跳过每参数的内存写入内核，让下次反向传播写新值（https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html）。边界情况：步间读取 `.grad` 的代码必须容忍 `None`。
- **为正式运行关掉调试 API** — `torch.autograd.set_detect_anomaly(True)`、`torch.autograd.profiler.profile`、`gradcheck` 增加逐操作簿记（异常检测慢约 10 倍，precision-stability P9）。长启动前 grep `detect_anomaly` / 残留的 `with profile(` 包裹（https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html）；NaN 排查后容易忘关。

---

## 为速度的混合精度

### T13 — bf16/fp16 是吞吐杠杆，不只是内存杠杆

**症状**：fp32 训练未充分利用 Tensor Core；GPU 有 bf16/fp16 tensor core。

**根因**：16 位矩阵乘法在 Tensor Core 上以高得多的 FLOP/s 运行且减半激活读写带宽 — 在内存节省*之上*的提速（oom-memory.md M6）。

**修复**：在 Ampere+ 上 `torch.autocast("cuda", dtype=torch.bfloat16)`（现代默认；无 GradScaler — precision-stability P6）或 HF `TrainingArguments` 的 `bf16=True`。完整精度决策（bf16 vs fp16 vs V100/T4 仅 fp16 路径、GradScaler 机制、NaN/溢出）由 **references/training/precision-stability.md P1–P10** 负责（交叉链接；不要重复）。*内存*角度和激活桶数学在 **oom-memory.md M6**。切换后 NaN/发散是数值问题 → precision-stability / verifying-dl-experiments（**必需**）。

---

## 内核 — GPU 被喂饱后剩余的杠杆

### T14 — SDPA / FlashAttention：停止物化 O(seq²) 注意力矩阵

**症状**：transformer 受注意力限制；长序列慢且占内存；或 `flash_attn` "已安装"但运行没变快。

**根因**：eager/`math` 注意力路径物化完整的 `seq×seq` 分数矩阵。融合的 **FlashAttention** / **memory-efficient** 后端从不这样做，但 PyTorch 的 `scaled_dot_product_attention` 在融合内核输入约束不满足时**静默回退到慢 `math` 后端** — 错误的 dtype、头维度、mask 形状 — "如果融合实现不可用，将发出警告"（https://docs.pytorch.org/docs/2.12/generated/torch.nn.functional.scaled_dot_product_attention.html）。

**修复**：
- 使用 `F.scaled_dot_product_attention(q,k,v)`（或 `attn_implementation="sdpa"`，HF 2.1.1+ 默认），它自动选择 FlashAttention / memory-efficient / cuDNN / math。给它 **fp16/bf16** 输入 — 融合后端需要 16 位（fp32 时运行的是 `math` 回退）。
- **强制验证**快速后端而非信任静默：
  ```python
  from torch.nn.attention import sdpa_kernel, SDPBackend
  with sdpa_kernel(backends=[SDPBackend.FLASH_ATTENTION]):   # 不可用时大声报错
      out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
  ```
- **从源码安装 `flash_attn` 是陷阱**：没有 `ninja`（`pip install ninja`）时 CUDA 扩展单线程编译约 2 小时；有 ninja 在 64 核机器上约 3–5 分钟。核心多但 `<96 GB` 内存时 ninja 过度并行化导致编译 OOM — 限制 `MAX_JOBS=4 pip install flash-attn --no-build-isolation`。优先用匹配 `cuXX/torchYY/cpZZ` 三元组的**预编译 wheel**（https://github.com/Dao-AILab/flash-attention/issues/1038，https://pypi.org/project/flash-attn/）。torch/CUDA 不匹配是 **gotchas_universal.md U28**。融合内核是否改变输出（因果 mask 边界情况）是数值检查 → verifying-dl-experiments（**必需**）。

### T15 — `torch.compile`：融合内核 + 削减启动开销（一行，真实收益）

**症状**：大量小逐点/逐元素操作；Python/启动开销在大矩阵乘法间主导。

**根因**：eager 分别启动每个操作；Inductor 将相邻操作融合为 Triton 内核并（在 CUDA graph 模式下）消除每步启动开销，跨步复用执行计划。

**修复**：包裹模型 — `model = torch.compile(model)`。模式（https://huggingface.co/docs/transformers/en/perf_torch_compile）：
- `default` — 平衡速度/内存。
- `mode="reduce-overhead"` — 使用 **CUDA graphs** 消除 Python 开销（最适合大量微小操作 / 小批次 / 推理），代价是略多内存。
- `mode="max-autotune"` — 最长编译，最快稳态。
- HF `TrainingArguments(torch_compile=True, torch_compile_mode="reduce-overhead")`。

报告约 2.2× 平均推理提速；训练收益真实但依赖模型。**前几步很慢** — 编译在首次调用时延迟进行（https://huggingface.co/docs/transformers/en/perf_torch_compile）；从任何吞吐测量中排除预热。开发时设 `fullgraph=True` 让图中断大声暴露而非静默损失速度。编译后的*数字*是否匹配 eager → verifying-dl-experiments（**必需**）。

### T16 — `torch.compile` 重编译陷阱：可变形状静默吹掉缓存 → 回退 eager

**症状**：编译后运行比 eager *更慢*，或周期性卡顿；吞吐从不稳定。常见于可变 batch/seq-len、动态填充或每步变化的形状。

**根因**：编译在追踪的形状上创建**守卫**；新形状违反守卫触发**重编译**。超过重编译上限（`torch._dynamo.config.recompile_limit`，默认 **8**；旧版 `cache_size_limit`）后 Dynamo **停止编译该函数并以 eager 运行** — 付出所有编译成本却得不到任何收益（https://docs.pytorch.org/docs/stable/compile/programming_model.recompilation.html，https://github.com/pytorch/pytorch/issues/93457）。

**修复**：
- **看到它**：`TORCH_LOGS=recompiles python train.py` 日志哪个函数重编译和失败的守卫；`TORCH_LOGS=graph_breaks` 和 `torch._dynamo.explain(...)` 定位图中断（https://docs.pytorch.org/docs/stable/torch.compiler_troubleshooting.html）。
- **驯服形状**：填充/桶化为少数固定形状使守卫停止触发；或标记可变维度为动态 — `torch.compile(model, dynamic=True)`（或 `mark_dynamic` / `TORCH_COMPILE_DYNAMIC_SOURCES`）编译一个形状通用图而非每个尺寸一个。`dynamic=False` 为每个不同尺寸强制重新编译（仅在真正少数形状时使用）（https://docs.pytorch.org/docs/stable/compile/programming_model.html）。
- **最后手段**：仅当少数*稳定*的额外形状确实存在时提高 `torch._dynamo.config.recompile_limit` — 提高它来掩盖真正无界形状只会抖动。

---

## 内存 ↔ 速度权衡

### T17 — 激活检查点以约 20–30% 计算换内存（了解代价）

**症状**：梯度/激活检查点开着"为了安全"但训练慢 — 而模型其实不用它也能装下。

**修复**：检查点在反向传播中**重新计算**激活而非存储 — 以约 **20–30% 额外计算**换大幅内存削减（https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html，oom-memory.md M7）。**仅在激活确实 OOM 时启用**（完整理由 + `use_reentrant=False` / `use_cache=False` 陷阱 = **oom-memory.md M7**）；如果不用它也能装，关掉它是免费的约 25% 提速。在边界上，只检查点最*少/最重*的需要适配的块，不是整个模型。

### T18 — 更大的 micro-batch ≈ 更好的 GPU 利用率（直到碰内存墙）

**症状**：微小批次喂不饱 GPU；利用率和吞吐都低但 VRAM 大多空闲（小批次未填满 Tensor Core 且摊薄启动/同步开销差）。

**修复**：提高 micro-batch 向 VRAM 极限靠拢；如果结果依赖则用梯度累积保持**有效**批次固定（`batch 4 × accum 16` 优于 `batch 1 × accum 64` — oom-memory.md M5）。精度/有效批次影响（LR 缩放、累积 loss 加权）→ verifying-dl-experiments（**必需**）。与并发作业一起调整 + `expandable_segments` = **gotchas_universal.md U10** / oom-memory.md M8。

---

## 性能分析器 — 测量瓶颈，不要猜

### T19 — `torch.profiler`：数据瓶颈 vs 计算瓶颈的权威裁定

**症状**：需要*证明*时间花在哪里（哪种 T1 情况），而非从利用率推断。

**修复 — 计划性分析几步**（https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html）：
```python
from torch.profiler import profile, schedule, ProfilerActivity, tensorboard_trace_handler
with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    schedule=schedule(wait=1, warmup=1, active=3),     # 跳过预热；记录3步
    on_trace_ready=tensorboard_trace_handler("./tb_trace"),
    record_shapes=True, with_stack=True,
) as prof:
    for step, batch in enumerate(loader):
        train_step(batch); prof.step()
        if step >= 6: break
print(prof.key_averages().table(sort_by="self_cuda_time_total", row_limit=15))
```
**读它**：大的 **GPU 时间线间隙**且 CPU 忙于 `DataLoader`/变换 ⇒ **数据瓶颈**（T4–T8）；TensorBoard "Performance Recommendation" 面板直接命名 DataLoader（https://docs.pytorch.org/tutorials/intermediate/tensorboard_profiler_tutorial.html）。密集的 GPU 时间线 ⇒ GPU 瓶颈；按 `self_cuda_time_total` 排序找最热内核（T14/T15）。`nccl:*` 中未重叠的时间 ⇒ 通信瓶颈（T23）。在远程机器上写 trace 本地查看 — 用原始 `export_chrome_trace("trace.json")` 在 `chrome://tracing` 打开；`scp` 下来（references/ssh_transport.md），不要通过 ssh 运行查看器。

### T20 — `nsys` / Nsight Systems：当间隙在 PyTorch 视野之下时的系统级时间线

**症状**：torch.profiler 显示 GPU 空闲间隙但不知道*为什么*（CPU 启动延迟、隐藏的同步、一次 memcpy、内核启动风暴）；或想要 CUDA-API + NVTX + OS-runtime 在一条时间线上。

**根因**：torch.propiler 看到 PyTorch 操作；`nsys` 追踪整个系统 — CUDA API、内核、memcpy、NVTX 范围、OS-runtime — 所以它暴露 PyTorch 看不到的启动瓶颈和 CPU↔GPU 同步。"CUDA HW 行中的周期性间隙是 GPU 空闲的时刻 — 红旗"（https://docs.lxp.lu/howto/pytorch-profiling-with-nsight/）。

**修复 — 在机器上分析有界窗口，本地查看**（标准 PyTorch 配方，https://gist.github.com/mcarilli/376821aa1a7182dfcf59928a7cde3223）：
```bash
nsys profile -w true -t cuda,nvtx,osrt,cudnn,cublas -s cpu \
  --capture-range=cudaProfilerApi -x true -o report python train.py
```
在脚本中，限制窗口使 `.nsys-rep` 保持小：
```python
torch.cuda.profiler.cudart().cudaProfilerStart()   # 预热后
# ... 几步，可选包裹在 torch.cuda.nvtx.range_push/pop ...
torch.cuda.profiler.cudart().cudaProfilerStop()
```
`scp` 下载 `.nsys-rep`，在 Nsight Systems GUI 中打开。Nsight **Systems** 找*哪个*内核慢；Nsight **Compute**（`ncu`）找*为什么*（占用率、带宽、warp 阻塞）— 但 `ncu` 很重，保留给一个热内核（https://www.spheron.network/blog/gpu-profiling-ai-workloads-nsight-compute-pytorch-profiler-guide/）。

### T21 — `py-spy`：无需重启、无需代码修改分析实时训练进程

**症状**：一个长运行神秘变慢或看似挂起；重启加性能分析器会浪费数小时且可能不复现。

**根因**：一个 Python 侧瓶颈或死锁（慢变换、锁、阻塞集合通信）需要*原位*检查。

**修复 — 按 PID 附加，零插桩**（https://github.com/benfred/py-spy）：
```bash
py-spy dump --pid <PID>            # 一次性每个线程的栈 → 它现在卡在哪里
py-spy top  --pid <PID>            # 实时"哪个函数消耗时间"（Unix top 风格）
py-spy record -o prof.svg --pid <PID>   # 一个窗口的火焰图
```
"被分析的程序不需要导入、装饰器或重启。"在租用机器的运行中，`py-spy dump` 立刻区分*挂起*进程（卡在 `recv`/锁/`all_reduce`）和*慢*进程（忙于变换）— 配合"是否真的挂了？"检查（gotchas_universal.md U17，verifying-dl-experiments **必需**）。可能需要 `--native` 查看 C 扩展帧和 `sudo`/`SYS_PTRACE` 才能附加。

### T22 — CUDA 内存快照/可视化器 → oom-memory.md M19

对于*什么分配了内存*（不是时间），`torch.cuda.memory._record_memory_history` 快照 + https://pytorch.org/memory_viz 时间线由 **references/training/oom-memory.md M19/M18** 负责。它是内存工具，不是吞吐工具 — 在此列出仅为使性能分析器菜单完整。不要重复。

---

## 多 GPU / 多节点通信

### T23 — 计算-通信重叠：DDP 默认重叠；调优桶，注意破坏者

**症状**：扩展效率差 — 每 GPU 利用率高，但 N 个 GPU 远未达到 N× 吞吐；trace 显示 `all_reduce`/`all_gather` *未*与反向计算重叠。

**根因**：DDP 通过桶化梯度并在就绪时在单独 CUDA 流上启动每个桶的 reduce 来重叠梯度 all-reduce 与反向传播（https://github.com/pytorch/pytorch/issues/67570。当某些东西强制同步时重叠*中断*：未使用参数重计算、默认关闭的 `find_unused_parameters=True`、步骤中的 `.item()`/print/`.cpu()`、或太小/太大的桶。

**修复（单机，DDP/FSDP — 启动/分片机制在 references/training/distributed-launch.md，必需）**：
- 调优 `bucket_cap_mb`（DDP）将梯度块批成更少、更大的 all-reduce；设 `gradient_as_bucket_view=True` 减少一次拷贝。桶太小 = 启动开销；太大 = 延迟重叠。
- FSDP：启用 `backward_prefetch`（在当前反向期间预取下一层的 all-gather）和 `forward_prefetch` 使通信隐藏在计算下；内存紧张时设 `limit_all_gathers`。
- 移除每步主机同步（每步 `loss.item()`、print、急切 `.cpu()`）它们序列化流。

**节点间**传输（NCCL 选择错误 NIC、fabric-manager 挂起、1800 秒超时掩盖落后者、MTU 不匹配）是 **references/multinode.md**（≥2 实例**必需**）— 跨机器的通信"变慢"通常是其中之一，不是桶大小调优。world size 变化是否静默重新缩放有效批次/LR 是科学问题 → verifying-dl-experiments（**必需**）。

---

## 指针 — 其他地方收录的吞吐陷阱（不要重复）

- **gotchas_universal.md** — **U8** 将热数据暂存到本地 NVMe（IO 瓶颈） · **U21** `nvidia-smi` 利用率骗人（+ **U23** 散热/功耗节流） · **U24** dataloader 饿死旋钮顺序 · **U25** 数百万小文件 → 分片为 tar/WebDataset · **U38** GPU 0% 利用率 CPU 数据瓶颈（属于 verifying-dl）。
- **references/training/oom-memory.md** — M5 micro-batch/梯度累积 · M6 bf16 激活 · M7 激活检查点内存理由 · M8 `expandable_segments` · M19 内存快照/可视化器。
- **references/training/precision-stability.md** — P1–P10 精度决策 + AMP 机制 · P2 TF32 关闭脚枪 · P19 确定性 vs `cudnn.benchmark` 速度权衡。
- **references/training/distributed-launch.md** — torchrun/Accelerate/DeepSpeed 启动、DDP/FSDP 分片、以及反同步/卡死工具包（本文件 T23 所在的启动基板）。
- **references/multinode.md** — 节点间 NCCL/NIC/fabric/超时/MTU（机器之间的网线）。单机用户跳过。
- **verifying-dl-experiments**（**必需**）— 负责*数字是否真实*：内核/精度/编译切换是否改变了结果、丢弃样本或 GPU 侧变换是否改变了分布、0% 利用率诊断（U38）、确定性（U36）。本文件让训练*快*；那个技能判断*更快的结果是否仍然真实*。
