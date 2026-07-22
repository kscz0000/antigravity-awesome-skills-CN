# 数据管道正确性 —— DataLoader 中的静默错误训练源，而非模型

`throughput-profiling.md` 负责让 dataloader **快**；本文档负责让它**正确**——那些不报错但让训练在错误数据上"成功"的 bug：暗中不变的增强、跨 worker/GPU 重复的流、崩溃或错误填充的 collate、以及静默偏移输入分布的预处理。每条条目都是**症状 → 根因 → 修复**并附带精确旋钮。

边界：**verifying-dl-experiments** 负责*判断*"这是否泄露 / 指标是否有效"；本文档负责*机制*（DataLoader / Dataset / transform 实际做了什么）。当数据 bug 导致训练"能跑但学不动"时，交叉检查 `convergence-debugging.md`——**O1（过拟合单个 batch）** 可以从坏数据中隔离坏循环。

跳转方式：`grep -in '<keyword>' references/training/data-pipeline.md`（如 `worker`、`worker_init_fn`、`numpy`、`seed`、`iterabledataset`、`get_worker_info`、`collate`、`pin_memory`、`spawn`、`lambda`、`__len__`、`drop_last`、`cache`、`bgr`、`totensor`、`normalize`、`set_epoch`、`shuffle`）。

## 目录

- **DataLoader worker RNG（增强重复 bug）** — DP1 numpy-RNG 跨 worker 重复 · DP2 IterableDataset 跨 worker+rank 重复 · DP3 不均匀分片 DDP 卡死
- **Dataset / collate / DataLoader 约束** — DP4 变长样本 collate · DP5 pin_memory 自定义类型 · DP6 spawn 破坏 lambda · DP7 错误的 __len__ · DP8 size-1 batch 杀死 BN · DP9 内存缓存 OOM · DP15 /dev/shm Bus error
- **输入预处理 / 标签 / shuffle** — DP10 归一化统计量空间/拆分+RGB/BGR · DP11 cv2 BGR · DP12 ToTensor 不除 255 · DP13 Normalize 在 ToTensor 之前 · DP14 shuffle/sampler + set_epoch
- **指针** — throughput-profiling.md、convergence-debugging.md、distributed-launch.md、verifying-dl-experiments（技能）

---

## DataLoader worker RNG —— 增强重复 bug

### DP1 — 跨 worker 和每个 epoch 的"随机"增强完全相同 → numpy 全局 RNG 通过 `fork` 继承
**症状**：`num_workers>0` 时，不同 worker 发出**相同**的随机增强参数（相同裁剪坐标、翻转、噪声），且完全相同的随机序列**每个 epoch 重复**。增强多样性坍塌到 ~`1/num_workers`；模型泛化变差但无可见原因——无崩溃、无警告。（一项审计在 >95% 的带自定义数据集的检查仓库中发现了此问题。）
**根因**：DataLoader 通过 `fork`（Linux 默认）生成 worker，所以每个 worker 继承了父进程 NumPy 全局 RNG 状态的**相同**副本。PyTorch 自动为每个 worker 的 **torch** RNG（和 Python `random`）设定种子为 `base_seed+worker_id`，但它**不**触及 numpy 的全局 RNG——所以 `__getitem__`/transforms 中的 `np.random.*` 在跨 worker 间相同，且因为 worker 从未改变的父状态重新生成，每个 epoch 也相同。
**修复**：传入一个 `worker_init_fn`，从 torch 已有的逐 worker 种子重新设定 numpy 种子：`def wif(_): np.random.seed(torch.initial_seed() % 2**32)`。`torch.initial_seed()` = `base_seed+worker_id`，且 `base_seed` 每 epoch 重抽，给出跨 worker **和**跨 epoch 的多样性。**两个陷阱**：(a) 从常量设定种子（`np.random.seed(42+worker_id)`）重新打破 epoch 多样性——每个 epoch 重置到相同起点；(b) **不要**在 `worker_init_fn` 中调用 `torch.manual_seed(CONST)`——它会覆盖 torch 正确的逐 worker 偏移。最干净的做法：将增强 RNG 路由通过 torch（`torch.rand`/`torch.Generator`），它自动按 worker 设种——然后不需要 `worker_init_fn`。使用 `persistent_workers=True` 时 init 只运行一次，所以从 epoch 计数器变化而非依赖 base_seed 重抽。([tanelp "PyTorch+NumPy, you're making a mistake"](https://tanelp.github.io/posts/a-bug-that-plagues-thousands-of-open-source-ml-projects/), [PyTorch "Randomness in multi-process data loading"](https://docs.pytorch.org/docs/stable/notes/randomness.html))

### DP2 — `IterableDataset` 每个样本产出 N×（每个 worker）或 world_size×（每个 rank）→ 未分片
**症状**：带 `num_workers=N` 的 `IterableDataset` 每个样本产出 **N 次**（一个"epoch"长 N×，样本在 batch 内重复）；DDP 下每个 **rank** 流出**相同**数据，所以 `all_reduce` 平均相同梯度，模型看到 `world_size×` 更少的唯一样本尽管用了更多 GPU。常被误读为数据集太大或收敛太慢。
**根因**：**同一个** `IterableDataset` 对象被复制到每个 worker **和**每个 rank；与 map-style 数据集不同，没有 `Sampler` 分发不相交的索引（`DistributedSampler` **不**适用于 `IterableDataset`）。除非 `__iter__` 自己分区流，否则所有消费者迭代相同序列。`get_worker_info()` 只知道进程内 worker，不知道 rank。
**修复**：在 `__iter__` 内按**两个**维度分片。Worker：`wi=torch.utils.data.get_worker_info()`，然后保留 `idx % wi.num_workers == wi.id` 的记录（或连续范围）。Rank：加入 `dist.get_rank()`/`get_world_size()`——`global_id = rank*num_workers + worker_id`，`global_world = world_size*num_workers`，保留 `idx % global_world == global_id`。使用 HF `datasets` 时，`datasets.distributed.split_dataset_by_node(ds, rank, world_size)` 分配不相交的逐 rank 分片，然后 `num_workers` 处理内部分割。([PyTorch data — IterableDataset multi-worker](https://docs.pytorch.org/docs/stable/data.html), [HF datasets#5360 — DDP duplication](https://github.com/huggingface/datasets/issues/5360))

### DP3 — DDP 下不均匀的 `IterableDataset` 分片长度 → NCCL 卡死 / 静默样本丢失
**症状**：正确按 rank 分片 `IterableDataset` 后，训练间歇性在 epoch 的**最后一个 batch** 处**卡死**（NCCL 集合超时），或某些 rank 多跑一步。
**根因**：流式分片很少被 `world_size*num_workers` 整除；当一个 rank 的迭代器耗尽而其他还在产出时，完成的 rank 跳过其 `backward`/all-reduce，其余永远阻塞等待缺席的集合。与 map-style 的 `DistributedSampler`（填充到统一长度）不同，`IterableDataset` 分片没有自动长度均衡。
**修复**：让每个 rank 跑**相同**步数——(a) 计算全局最小步数/epoch 并让所有 rank 在那里停止（丢弃参差不齐的尾部），(b) 通过循环样本填充短分片，或 (c) 用 `model.join()`（DDP `join` 上下文管理器）包裹，它为提前完成的 rank 影子集合操作。设 `drop_last=True` 丢弃 worker 内不均匀的最后 micro-batch。（Map-style 的 `set_epoch` 卡死是*不同*原因 → D22。）([PyTorch data](https://docs.pytorch.org/docs/stable/data.html), [HF datasets#5360](https://github.com/huggingface/datasets/issues/5360))

---

## Dataset / collate / DataLoader 约束

### DP4 — `default_collate` 在变长样本上 "stack expects each tensor to be equal size" → 自定义 `collate_fn`
**症状**：迭代在 batch 组装时崩溃——`RuntimeError: stack expects each tensor to be equal size, but got [..] at entry 0 and [..] at entry 1`——针对变长序列、变 bbox 数量或不同大小图像/掩码。`batch_size=1` 可用；错误仅在 `batch_size>1` 时出现。
**根因**：默认 collate 用 `torch.stack(batch, 0)` 对同键张量打包，要求每个非 batch 维度的形状相同。变长样本违反此要求，所以 stack 抛出——bug 出在 collate 胶水而非模型或数据集。
**修复**：传入 `DataLoader(..., collate_fn=my_collate)`。序列：`pad_sequence(seqs, batch_first=True, padding_value=pad_id)` + 发出长度/注意力掩码（然后掩码 loss → O15，按领域 L2）。检测式变长 target：将它们保持为逐样本张量的 Python **列表**而非堆叠（Faster-RCNN/DETR 约定）。不同大小图像：填充到 batch 最大 H/W（NestedTensor / pad+mask）。([PyTorch data — custom collate_fn](https://docs.pytorch.org/docs/stable/data.html), [forum: variable bbox counts](https://discuss.pytorch.org/t/dataloader-collate-fn-throws-runtimeerror-stack-expects-each-tensor-to-be-equal-size-in-response-to-variable-number-of-bounding-boxes/117952))

### DP5 — `pin_memory=True` 在自定义 batch 类型上静默无效 → 必须定义 `.pin_memory()`
**症状**：将 batch 包装在自定义类（`Batch` 对象、图 batch、dataclass）中并设 `pin_memory=True` 后，异步 H2D 拷贝（`.to('cuda', non_blocking=True)`）不再重叠——吞吐量退化到阻塞拷贝——或 pinning 看起来没起作用。
**根因**：DataLoader 的 pin 步骤只知道如何 pin 张量和它递归进入的内置容器（`list/tuple/dict`）。用户定义的 batch 类型是不透明的，所以其内部张量保持可分页；后续 `non_blocking=True` 拷贝静默回退到**同步**（T6 重叠丢失）。PyTorch 的约定：*"要为自定义 batch 或数据类型启用内存 pinning，请在自定义类型上定义 `pin_memory()` 方法。*"
**修复**：实现 `def pin_memory(self): self.x=self.x.pin_memory(); self.y=self.y.pin_memory(); return self`（返回 `self`）——pin worker 每 batch 调用它。然后保持 `pin_memory=True` 并用 `.to(device, non_blocking=True)` 传输。([PyTorch data — Memory Pinning](https://docs.pytorch.org/docs/stable/data.html))（pinned-memory *性能*机制 → throughput T6。）

### DP6 — `num_workers>0` 在 `spawn` 启动方法下（Windows/macOS）破坏 lambda/闭包
**症状**：在 Windows/macOS 上，`num_workers>0` 抛出 `AttributeError: Can't pickle local object '<locals>.<lambda>'`；或更糟，它继续但 transform 静默消失（样本返回未增强的）。相同代码在 `num_workers=0` 或 Linux 上正常运行。
**根因**：Windows/macOS 默认使用 `spawn`——每个 worker 启动一个新解释器，通过 **pickle** 重建 dataset/collate/transforms。Lambda、嵌套函数和闭包不可 pickle → 硬 pickle 错误，或（pytorch/vision#8066）transform 在序列化期间被丢弃。Linux 的 `fork` 复制活动内存，掩盖了 bug。
**修复**：让 worker 重建的一切成为顶层可导入的可调用对象——用模块级 `def` 替换 `collate_fn=lambda b: ...` 和 lambda transform；用 `functools.partial(top_level_fn, ...)` 绑定参数而非闭包；参数化 transform 使用顶层可调用类。保持主脚本代码在 `if __name__ == '__main__':` 下。应急：`num_workers=0` 绕过 pickle。([vision#8066 — transforms lost under spawn](https://github.com/pytorch/vision/issues/8066), [PyTorch data — platform-specific](https://docs.pytorch.org/docs/stable/data.html))

### DP7 — 错误的 `Dataset.__len__` → `__getitem__` 越界：IndexError，或静默取模回绕
**症状**：(a) epoch 中途 `__getitem__` 抛出 `IndexError`/`KeyError`；或 (b) 无错误但训练静默看到重复/跳过的样本——当 `__getitem__` 做 `self.items[idx % len(...)]` 或索引更短的列表导致过长索引回绕时。
**根因**：map-style 约定——`__len__()` 必须等于有效键的数量，默认 `RandomSampler` 从 `range(len(dataset))` 抽取索引。如果 `__len__` 从与 `__getitem__` 索引不同的/过时的来源计算（计数文件但索引过滤列表、差一错误、缓存长度），sampler 请求结构无法提供的索引。防御性的 `idx % N` 把响亮的 IndexError 变成静默的正确性 bug。
**修复**：从**相同**集合计算 `__len__` 和 `__getitem__`（在 `__init__` 中物化保留索引列表，通过它索引）。移除任何 `idx % N`/clamping——让越界索引抛出异常。一次性检查：`assert len(ds)==<expected>`；`ds[len(ds)-1]` 可用且 `ds[len(ds)]` 抛出异常。([pytorch#45040](https://github.com/pytorch/pytorch/issues/45040), [PyTorch data — map-style contract](https://docs.pytorch.org/docs/stable/data.html))

### DP8 — size-1 的最后 batch 崩溃 BatchNorm → 训练 loader 上设 `drop_last=True`
**症状**：训练跑完 epoch 大部分后在**最后**一个 batch 处崩溃，报 `ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, C, ...])`。发生在 `len(dataset) % batch_size == 1` 时。
**根因**：`nn.BatchNorm*` 在训练模式下计算每通道均值/方差；单样本加平凡空间大小时每通道计数为 1，方差未定义，`F.batch_norm` 抛出异常（0.3 以来的有意防护）。默认 `DataLoader(drop_last=False)` 保留那个参差不齐的最后 batch。
**修复**：**训练** loader 上 `DataLoader(..., drop_last=True)` 丢弃不完整的最后 batch（标准修复）。如果无法丢弃数据的替代方案：将 BatchNorm 换成 `nn.GroupNorm`/`nn.LayerNorm`（无 batch 统计量依赖），或冻结 BN 到 eval（O18）。**评估** loader 保持 `drop_last=False`（你需要每个样本）并依赖 `model.eval()`。（小 batch BN *质量* → V7；逐 rank batch 计数均衡 → D9；这是单进程 size-1 崩溃。）([pytorch#4534](https://github.com/pytorch/pytorch/issues/4534))

### DP9 — 内存中 `Dataset` 缓存增长到 host-OOM（且在 `fork` worker 下甚至不共享）
**症状**：RAM 在迭代/epoch 间稳步攀升直到裸 `Killed`（exit 137，无 traceback）——通常来自一个延迟缓存解码样本的 Dataset（`if idx not in self.cache: self.cache[idx]=load(idx)`）。`num_workers>0` 时增长是**逐 worker**的且缓存没有加速。
**根因**：两个复合效应——(1) 缓存无界：每个请求过的索引都常驻，所以一个 epoch 缓存整个解码后的数据集；(2) 在 Linux `fork` 下，每个 worker 是写时复制，所以写 `self.cache[idx]=...` 会将触及的 Python 对象页面复制到该 worker 的**私有**内存——对兄弟不可见，所以缓存既复制（RAM × ~`num_workers`）又对跨 worker 复用无用。
**修复**：不要在 `__getitem__` 中累积无界 Python 对象。选项：(a) 在 `__init__` 中预计算到单个 `np.memmap` / Arrow / LMDB / `.npy` 并读取切片（OS 页面缓存**是**跨 forked worker 共享的）；(b) 限制缓存（`functools.lru_cache(maxsize=...)` 或环形缓冲区）；(c) 存入共享内存（`Tensor.share_memory_()`）。优先使用 numpy/Arrow 缓冲区而非 `list`/`dict` 以避免写时复制页面抖动。（静态 `num_workers × 大张量` 启动乘数 → U9；这是*训练期间增长*的表亲。）([pytorch#13246 — worker memory replication](https://github.com/pytorch/pytorch/issues/13246), [PyTorch data — multi-process memory caveat](https://docs.pytorch.org/docs/stable/data.html))

---

## 输入预处理 / 标签 / shuffle

### DP10 — 归一化应用在错误的空间/拆分上，或统计量与通道顺序未对齐 → 准确率静默崩塌
**症状**：模型加载运行无报错，但预训练 backbone 得分远低于其报告数字，或你的验证准确率比训练低几点且无明显原因；预测系统性偏倚（通道顺序错误时红↔蓝混淆）。
**根因**：逐通道均值/标准差是正确的数字应用在错误的空间或顺序上。(1) 统计量必须在**仅训练拆分**上计算并在 eval 时原样复用（sklearn 约定：在 train 上 `fit_transform`，在 test/整个集合上 `transform`——永远不再 `fit`）。(2) torchvision 预训练权重期望输入已缩放到 `[0,1]`，**RGB** 顺序，然后用 ImageNet `mean=[0.485,0.456,0.406]`/`std=[0.229,0.224,0.225]` 归一化。那个均值向量是 **RGB 索引**的，所以传入 BGR 张量（cv2 默认，DP11）会把 R 统计量对齐到 B 通道。
**修复**：在训练集上计算统计量一次，eval 时复用相同常量/transform。对于 torchvision 预训练模型不要手写——使用 `weights.transforms()`（如 `ResNet50_Weights.IMAGENET1K_V2.transforms()`），它捆绑了 resize + 到 `[0,1]` + RGB + 精确的 Normalize。（泄露*判断*由 verifying-dl-experiments 负责；这里是机制。）([sklearn "Common pitfalls" — fit on train only](https://scikit-learn.org/stable/common_pitfalls.html), [torchvision models — input contract](https://docs.pytorch.org/vision/stable/models.html))（扩展 V1。）

### DP11 — `cv2` 加载的图像（BGR）传入 RGB 训练的模型 → 通道互换
**症状**：混合使用 `cv2` 做 I/O 和 PIL/torchvision 训练（RGB）模型的管道：无异常，但对颜色敏感的预测退化；可视化数组时红色呈现为蓝色。常在切换加载器（PIL→cv2）且准确率在零逻辑变更下下降时才浮现。
**根因**：`cv2.imread`/`VideoCapture` 返回 **BGR** 通道顺序，而 `PIL.Image` 和基本上每个 ImageNet 预训练模型都假设 **RGB**。索引通道 0 为"红色"现在读到蓝色。两者都是合法的 `HxWx3 uint8` 数组，所以什么都不报错——模型只是看到一致的颜色互换分布。
**修复**：cv2 加载后立即转换——`img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`（或 `img = img[:, :, ::-1].copy()`——`.copy()` 重要，负步长视图会破坏 `torch.from_numpy`）。或切换 I/O 到 `torchvision.io.read_image`/PIL（RGB）。端到端保持一个通道约定并在数据集边界断言它。([BGR↔RGB / cvtColor](https://note.nkmk.me/en/python-opencv-bgr-rgb-cvtcolor/), [torchvision models — RGB](https://docs.pytorch.org/vision/stable/models.html))

### DP12 — `transforms.ToTensor` 对非 `uint8` 输入不 ÷255 → 激活值大 255×
**症状**：loss 从第 0 步就巨大或 NaN，或激活/梯度极大，当输入来自 float numpy 数组、`.npy`、16位/HDR 图像（PIL 模式 `I`/`F`）或已在 `[0,1]` 中的张量。相同模型在 `uint8` PNG 上运行正常。
**根因**：`transforms.ToTensor()` 仅当源是列出模式的 PIL Image **或** `dtype==uint8` 的 numpy 数组时缩放到 `[0,1]`（÷255）。其他所有情况（float32/64、int32、exotic PIL 模式）它**不做**缩放直接转换——所以 `0..255` 的 float numpy 数组保持 `0..255`，而已经缩放过一次的 `uint8` 数组被再 ÷255（→ `0..0.004`）。
**修复**：不要依赖 `ToTensor` 做非 uint8 缩放。对 float 输入显式缩放：`t = torch.from_numpy(arr).float() / 255.0`（或 16 位的正确最大值）。v2 API 中优先用 `transforms.v2.ToImage()` + `transforms.v2.ToDtype(torch.float32, scale=True)`，其中 `scale=True` 使缩放显式且 dtype 感知。检查：紧接其后 `assert 0.0 <= x.max() <= 1.0`。([ToTensor doc — "tensors are returned without scaling" for other cases](https://docs.pytorch.org/vision/stable/generated/torchvision.transforms.ToTensor.html))

### DP13 — `transforms.Normalize` 在 `Compose` 中放在 `ToTensor` 之前 → TypeError（它需要 float CHW 张量）
**症状**：数据集构建或第一个 `__getitem__` 抛出 `TypeError: tensor should be a torch tensor. Got <class 'PIL.Image.Image'>`（或 `img should be Tensor`）。
**根因**：`transforms.Normalize` 操作 float 张量形状 `(C,H,W)`，沿 dim 0 减去长度 `C` 的均值 / 除以长度 `C` 的标准差；它不能消费 PIL Image 或 HWC 数组。在 `Compose` 中步骤从上到下运行，所以 `Normalize` 必须在 `ToTensor`（产生 float CHW 张量）**之后**。PIL 域操作（Resize/Crop/flip）必须在 `ToTensor` **之前**。
**修复**：管道排序——PIL 操作 → `ToTensor()` → `Normalize(mean, std)`，如 `Compose([Resize(256), CenterCrop(224), ToTensor(), Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])])`。`mean`/`std` 长度必须等于通道数（3 RGB，1 灰度）。([torchvision transforms — Compose order](https://docs.pytorch.org/vision/stable/transforms.html))

### DP14 — DataLoader 静默取消 shuffle → `shuffle=True`+sampler 冲突；`DistributedSampler` 不调 `set_epoch` 回放单一顺序
**症状**：两种 shuffle 失败——(a) 加任何 sampler 就立刻 `ValueError: sampler option is mutually exclusive with shuffle`；(b) 无错误，但 DDP 下每个 epoch 以**完全相同**的顺序迭代数据，所以训练 loss 曲线看起来异常周期性 / 过度记忆且 shuffle "没用"。
**根因**：(a) `DataLoader.__init__` 强制互斥——`shuffle` 为你选择 sampler（`True`→`RandomSampler`，`False`→`SequentialSampler`），所以同时传入两者矛盾；`batch_sampler` 同样与 `batch_size`/`shuffle`/`sampler`/`drop_last` 互斥。(b) `DistributedSampler` 从以 `self.seed + self.epoch` 设种的生成器派生每个 epoch 的排列，而 `self.epoch` 保持 **0** 直到调用 `sampler.set_epoch(epoch)`——所以不调用时每个 epoch 用 `seed+0` → 字节级相同的顺序。
**修复**：(a) 当你必须使用 sampler（DistributedSampler、WeightedRandomSampler）时，设 `shuffle=False` 让 sampler 控制顺序。(b) 在每个 epoch **开始**迭代前调用 `train_sampler.set_epoch(epoch)`（Lightning/Accelerate 替你做；原生 torchrun 是你的责任）。通过记录 epoch 0 vs 1 的前几个索引验证——它们必须不同。（DDP `set_epoch` **卡死**是不同故障 → D22。）([DataLoader source — shuffle/sampler exclusivity](https://github.com/pytorch/pytorch/blob/main/torch/utils/data/dataloader.py), [DistributedSampler.set_epoch](https://docs.pytorch.org/docs/stable/data.html))

### DP15 — `Bus error` / DataLoader worker 被杀 → `/dev/shm` 耗尽（租赁容器经典问题）
**症状**：`DataLoader worker (pid N) is killed by signal: Bus error`，或 `RuntimeError: unable to write to file </torch_...>` / `received 0 items of ancdata`——在**租赁容器**上而相同代码在工作站上运行正常。通常 `num_workers>0`，常在 epoch 中途。
**根因**：PyTorch 通过**共享内存**（`/dev/shm`）传递 worker 张量。Docker 默认 `/dev/shm` 为 **64 MB**，很多租赁环境继承此值，几个 worker 移动正常 batch 就耗尽它，内核 SIGBUS 杀死一个 worker。这是*共享内存*耗尽——不是 host-RAM OOM（裸 `Killed` / exit-137 → `gotchas_universal.md` U9）也不是死锁。
**修复**：启动时扩大——`docker run --shm-size=8g`（或 `--ipc=host`）；在无法设置的地方（固定租赁），切换 IPC 策略 `torch.multiprocessing.set_sharing_strategy("file_system")`（fd 传递，更慢但无上限）和/或降低 `num_workers`。标志：`df -h /dev/shm` 显示微小上限——启动前检查它。([PyTorch multiprocessing shm note](https://docs.pytorch.org/docs/stable/notes/multiprocessing.html), [pytorch#5040](https://github.com/pytorch/pytorch/issues/5040))

---

## 指针 —— 其他地方编录的相关机制

- **DataLoader 速度（num_workers / prefetch / pin-overlap / GPU-starvation）** → `references/training/throughput-profiling.md`（T4–T8），`references/gotchas_universal.md`（U8, U24）。
- **"能跑但学不动"的循环接线 + 损失函数 + 标签格式 bug** → `references/training/convergence-debugging.md`（O1 先过拟合单个 batch；O14 CrossEntropyLoss target 格式）。
- **IterableDataset/DDP 启动、`set_epoch` 卡死、SyncBatchNorm、不均匀输入** → `references/training/distributed-launch.md`（D9, D10, D22）。
- **来自 worker fork-复制大启动张量的 host-RAM OOM** → `references/gotchas_universal.md`（U9）。
- **数据是否泄露 / 指标是否有效 / 拆分是否污染** → **verifying-dl-experiments**（**必需**——负责判断；本文档负责机制）。
