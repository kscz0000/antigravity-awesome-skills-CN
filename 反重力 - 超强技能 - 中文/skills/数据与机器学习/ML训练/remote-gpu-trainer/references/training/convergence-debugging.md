# 收敛与优化调试 —— 程序能跑、不崩溃，但学不动（或学得很差）

其他训练层文档覆盖的是**崩溃**的运行（`oom-memory.md`）、**NaN**（`precision-stability.md`）、**卡死**（`distributed-launch.md`）或**慢**（`throughput-profiling.md`）。
本文档负责更安静、也远更常见的故障：任务干干净净跑到结束，但**loss 平坦、下降过慢、或模型欠拟合**——而且 bug 出在优化连线而非硬件上。每条条目都是**症状 → 根因 → 修复**并附带精确旋钮。**始终从 O1（过拟合单个 batch）开始**——它能在五分钟内区分"循环坏了"和"模型/数据弱"，并告诉你需要本文档的哪一半。

边界：**verifying-dl-experiments**（在每个"结果是否真实"的分支处**必需**）负责崩溃、泄露、指标有效性、训练 vs 验证泛化和种子解释；本文档负责正确外观的循环为何不收敛的*机制*。NaN / loss 飙升 / LR 过**高**住在隔壁 `precision-stability.md`（P8–P18）——本文档是 LR 过**低** / 不动 / 接线错误的那一侧。

跳转方式：`grep -in '<keyword>' references/training/convergence-debugging.md`（如 `overfit`、`requires_grad`、`no_grad`、`optimizer`、`weight decay`、`adamw`、`lr finder`、`scheduler`、`accum`、`cross entropy`、`bcewithlogits`、`nllloss`、`freeze`、`batchnorm`、`discriminative`、`lora`、`update ratio`、`dead relu`）。

## 目录

- **根本没在学（从这里开始）** — O1 过拟合单个 batch · O2 参数不在优化器中 · O3 loss 与计算图脱离 · O4 zero_grad/backward/step 顺序 · O5 train()/eval() 模式
- **优化器 / LR / 权重衰减 / 调度** — O6 AdamW vs Adam+无衰减组 · O7 LR 过低+查找器 · O8 调度器顺序/步频 · O9 梯度累积除法 · O10 AdamW eps 在 bf16 下 · O11 fused/foreach
- **损失函数陷阱** — O12 双重 softmax · O13 BCEWithLogits · O14 CE 标签格式 · O15 填充 token 的 loss 归约 · O16 NLLLoss 需要 log_softmax
- **微调 / 迁移** — O17 冻结但仍在优化器中 · O18 冻结 BN 的 running stats · O19 差异化 LR / 遗忘 · O20 strict=False 的形状不匹配 · O21 LoRA/PEFT 接线
- **训练动态仪表盘（装上它让故障可见）** — O22 更新/权重比 · O23 实际 LR · O24 GradScaler 缩放 · O25 死 ReLU 比例 · O26 权重/梯度/激活直方图
- **指针** — precision-stability.md、distributed-launch.md、verifying-dl-experiments（技能）

---

## 根本没在学 —— 第一小时分诊

### O1 — 在调任何东西之前先跑过拟合单个 batch 的冒烟测试（规范正确性测试）
**症状**：训练"能跑"（无报错、正常吞吐）但 loss 在初始值附近平坦或游荡不下降，无论换什么 LR/优化器/架构。你在盲目调超参，因为没有任何东西证明循环本身能学习。
**根因**：循环在 forward 到权重更新之间的某个地方坏了（O2–O5 中的任何一个，或标签/形状 bug），而没有任何单一测试能把"这段代码能不能记忆"从"这是模型/数据问题"中分离出来。
**修复**：取一个固定的 mini-batch（2 个样本就够了），在**同一个 batch** 上循环 forward/backward/step 数百次——正确的循环会把训练 loss 驱动到 ~0。测试期间**关闭**增强、shuffle、dropout 和权重衰减。还要"验证初始 loss"（如 softmax CE 应从 `-log(1/n_classes)` 附近开始然后下降）。如果无法达到 ~0，*"某处有 bug，我们不能继续"*——在碰超参之前先调试循环（O2–O5）。（冒烟测试的*内容/解读* → **verifying-dl-experiments**；这里是机械门控。）([Karpathy, "A Recipe for Training Neural Networks"](https://karpathy.github.io/2019/04/25/recipe/))

### O2 — Loss 从第 0 步就平坦，`step()` 后权重字节级一致 → 参数不在优化器中
**症状**：过拟合单个 batch 失败；快照的参数在 `optimizer.step()` 前后不变；grad-norm 甚至可能非零。无报错。
**根因**：优化器更新的**不同**张量集合与模型 forward 使用的不同。四种原因：(a) 参数有 `requires_grad=False` 所以 `.grad` 保持 `None`，`step()` 跳过它们；(b) 某个子模块/头从未传入优化器的参数迭代器；(c) 优化器在 `model.to(device)` **之前**从 `model.parameters()` 构建，所以它持有过时的 CPU 张量而模型在 GPU 副本上 forward；(d) 冻结/解冻切换了 `requires_grad` 但在优化器中留下了错误的集合。
**修复**：在 `model.to(device)` **之后**构建优化器。断言它看到每个可训练参数：`opt_ids={id(p) for g in optimizer.param_groups for p in g['params']}; assert all(id(p) in opt_ids for p in model.parameters() if p.requires_grad)`。启动时记录 `sum(p.requires_grad for p in model.parameters())`。探针：`w0=next(model.parameters()).clone(); <一步>; assert not torch.equal(w0, next(model.parameters()))`。([autograd notes](https://docs.pytorch.org/docs/stable/notes/autograd.html), [torch.optim](https://docs.pytorch.org/docs/stable/optim.html), [stale-optimizer-after-.to bug](https://github.com/pytorch/xla/issues/1623))

### O3 — `backward()` 是空操作 / 抛出 "does not require grad" → loss 与计算图脱离
**症状**：过拟合失败，每个 `p.grad is None`；或者 `loss.backward()` 抛出 *"element 0 of tensors does not require grad and does not have a grad_fn"*。
**根因**：loss 张量在 `backward` 之前被从 autograd 切断了。常见切断方式：(a) 训练的 forward+loss 在 `with torch.no_grad():` / `@torch.inference_mode()` 内运行——来自 eval 遗留的——*"no-grad 模式下的计算永远不会记录到反向图中"*；(b) 在 loss 路径上调用 `.item()` / `.detach()` / `.cpu().numpy()` / `float(loss)`（如反向传播累积的 `total_loss += loss.item()`）；(c) 网络中间从 numpy 重建张量；(d) 传给 `backward()` 的是指标而非可微 loss。
**修复**：在 `backward` 之前，`assert loss.requires_grad and loss.grad_fn is not None`。保持可微 loss 张量与日志标量分开（记录 `loss.item()`，反向传播原始张量）。仅将 `no_grad`/`inference_mode` 用于 eval。`backward` 之后，断言至少一个 `p.grad is not None`。([autograd notes](https://docs.pytorch.org/docs/stable/notes/autograd.html))

### O4 — `zero_grad` / `backward` / `step` 顺序错误，或缺少 `step()`
**症状**：过拟合失败；权重从未移动，或尽管梯度非零但训练不稳定。
**根因**：PyTorch 的约定是*"梯度默认累加；为防止重复计数，我们每次迭代显式清零"*，`backward` 存入 `.grad`，`step` 读取 `.grad`。失败模式：(a) 遗漏 `optimizer.step()` → 梯度已计算，权重从未更新；(b) `zero_grad()` 放在 `backward()` **之后** → 擦除新鲜梯度；(c) `step()` 在 `backward()` **之前** → 在过时/零梯度上 step；(d) 从未调用 `zero_grad` → 所有迭代的梯度持续累加 → 有效 LR 爆炸。
**修复**：规范顺序，严格为——`optimizer.zero_grad(set_to_none=True)` → forward → `loss=loss_fn(out,y)` → `loss.backward()` → `optimizer.step()`（AMP 下：`scaler.scale(loss).backward()` → `scaler.step(optimizer)` → `scaler.update()`）。梯度累积是唯一例外（O9）：每个 micro-step 都 `backward`，仅在边界处 `step`+`zero_grad`。([optimization tutorial](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html), [torch.optim](https://docs.pytorch.org/docs/stable/optim.html))

### O5 — 忘记 `model.train()` / 留着 `model.eval()` → Dropout 和 BatchNorm 处于错误模式
**症状**：两种表现——(1) 在 `eval()` 下训练：BN 使用冻结的 running stats 且从不更新它们，Dropout 关闭 → 欠拟合 / loss 几乎不动；(2) 在 `train()` 下评估：BN 使用嘈杂的逐 batch 统计量且 Dropout 激活 → 验证 loss 运行间闪烁且比训练差。
**根因**：`train()`/`eval()` 设置一个逐模块标志，*"仅对某些模块有效...如 Dropout、BatchNorm"*（`eval()` == `train(False)`）。在 eval 模式下 BN 切换到存储的 `running_mean/var` 并**停止**更新它们；Dropout 变为恒等。新的 `nn.Module` 默认为 `train()`，但任何之前的 `.eval()`（复用对象、推理辅助函数、没有切回的验证循环）都会持续。
**修复**：显式括起各阶段——每个训练 epoch 顶部 `model.train()`；每次验证/测试 `model.eval()` + `with torch.no_grad():`；恢复训练前再次 `model.train()`。构建/加载后，训练循环前 `assert model.training`。（冻结 backbone 的 BN 是不同的轴 → O18；小 batch BN → 按领域 V7。）([nn.Module.train/eval](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html))

---

## 优化器 / 学习率 / 权重衰减 / 调度

### O6 — 权重衰减"没用" / Norm 增益不稳定 → 耦合的 `Adam(weight_decay=)` + 衰减 bias 和 Norm
**症状**：`torch.optim.Adam` 上的 `weight_decay` 相比文献的 AdamW 方案几乎不正则化（或有害）；或从头训练的 transformer/CNN 在"相同"wd 下比参考差；或小模型在 LayerNorm/BN 增益和 bias 被缩向 0 时不稳定。
**根因**：(1) `Adam` 的 `weight_decay` 是经典 **L2**——加入梯度，所以它经过 Adam 的 `1/(sqrt(v)+eps)` 预条件器，历史梯度大的参数得到**更少**衰减；预期强度与 `wd` 解耦。**AdamW** 直接对权重施加解耦衰减（`θ ← θ − lr·wd·θ`），在动量路径之外——均匀且与 lr 无关。它们在相同 `wd` 下**不可**互换。(2) 衰减 1-D 参数（bias、LayerNorm/BN weight & bias）把 Norm 增益缩向 0——它们没有过拟合容量，缩小它们会损害训练。
**修复**：使用 `torch.optim.AdamW`，而非 `Adam(weight_decay=...)`。分成两个参数组，无衰减组设 `weight_decay=0.0`——nanoGPT 的规则：衰减 `p.dim()>=2`（矩阵乘/嵌入权重），不衰减 `p.dim()<2`（所有 bias + 所有 LayerNorm 权重）；HF/timm 按名称排除（`bias`、`LayerNorm.weight`）。([AdamW doc](https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html), [Loshchilov & Hutter 2017 "Decoupled Weight Decay"](https://arxiv.org/abs/1711.05101), [nanoGPT configure_optimizers](https://github.com/karpathy/nanoGPT/blob/master/model.py))

### O7 — Loss 缓慢爬行无 NaN → LR 过**低**；用 LR 范围测试找到有效区间
**症状**：没有发散、没有 NaN、梯度有限——loss 就是极慢下降或高平台；吞吐量没问题但模型"学不动"。常在从不同 batch/优化器配方复制 LR 或默认极小"安全"LR 后出现。（P12 过高飙升的镜像。）
**根因**：LR 远低于有效区间，每次更新只是 loss 曲面曲率的微不足道的分数，优化缓慢爬行。自适应优化器的可用区间很窄且依赖架构，所以猜测的 LR 通常差 1-2 个数量级。可与梯度消失区分——grad-norm 健康，只是未被充分施加。
**修复**：跑一次 **LR 范围测试**（Smith）——从极小 LR 开始，每 batch 几何递增，跑约 100–1000 步，画 loss vs LR，选取 loss 开始发散前约 1 个数量级处。工具：`pytorch-lr-finder` `LRFinder(model,opt,crit).range_test(loader,end_lr=1,num_iter=100)`、fast.ai `learn.lr_find()`、Lightning `Tuner(trainer).lr_find()`。每当 batch size / 优化器 / 架构变化时重跑——区间会移动；然后确认 LR 在 warmup 后不触发 P12 飙升。([Smith 2015 "Cyclical Learning Rates"](https://arxiv.org/abs/1506.01186), [pytorch-lr-finder](https://github.com/davidtvs/pytorch-lr-finder), [Smith 2018 disciplined-approach](https://arxiv.org/abs/1803.09820))

### O8 — `lr_scheduler.step()` 在 `optimizer.step()` 之前 → 跳过第一个 LR；逐步 vs 逐 epoch 步频
**症状**：PyTorch 警告 *"Detected call of `lr_scheduler.step()` before `optimizer.step()`"* 且 LR 曲线偏移一格；或以优化器步数设定的余弦/warmup 调度几乎不动（按 epoch 步进）或在一个 epoch 内衰减到 ~0（按步设定的调度在累积下按 batch 步进）。
**根因**：(1) 自 PyTorch 1.1 起，调度器必须在优化器**之后**步进——*"如果在优化器更新之前调用 scheduler.step()...将跳过学习率调度的第一个值。"* (2) 调度器每 `.step()` 推进一格；围绕 **优化器**步数的 `total_steps`/`num_training_steps` 构建的调度器（OneCycleLR、HF `get_cosine_schedule_with_warmup`、Lightning `interval='step'`）必须每个优化器步步进，而在累积下"优化器步"不等于一个 batch。
**修复**：顺序为 `optimizer.step(); scheduler.step()`。按其 `total_steps` 计算时的粒度步进——warmup/cosine/OneCycle 按优化器步（在 `if (i+1)%accum==0` 块内，**不是**每个 micro-batch），仅 epoch 调度器按 epoch。HF `Trainer` 自动步进——不要手动再步进。([torch.optim — scheduler order](https://docs.pytorch.org/docs/stable/optim.html), [OneCycleLR](https://docs.pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.OneCycleLR.html))

### O9 — 梯度累积产生有效 N×LR → 将 loss 除以 `accum_steps`（并按 token 归一化）
**症状**：从 batch `B` 切换到（micro-batch `B/N` × N 次累积）"使用相同配置"后训练更激进/发散——loss/梯度幅度 ~N× 过大，即你默默获得了 N× 的 LR。对于 token 任务，当 micro-batch 持有不等数量的非填充 token 时，即使 `/N` 后累积的 loss 仍与未累积运行不同。
**根因**：每个 micro-batch 的 loss 是 `reduction='mean'`；`backward` 在 N 个 micro-batch 上**累加**梯度，所以累积梯度 = N 个均值梯度的 SUM = N× 全 batch 均值梯度 → 在其上 step ≈ N× LR。更微妙的是：将每个均值 loss 除以 N 在 micro-batch 有不同有效 token 数时仍会错误加权（均值之均值 ≠ 总 loss / 总 token 数）——HF 在 2024 年在 `transformers` 中发现并修复了这个问题。
**修复**：backward 前除——`loss = loss_fn(out,y) / accum_steps; loss.backward()`，仅在边界处 `step()`/`zero_grad()`。对于 token 级 loss，按累积窗口内的**总**非填充 token 数归一化（累积 `reduction='sum'`，除以总 token 数），而非均值之均值。DDP 下将非边界 micro-step 包在 `with model.no_sync():` 中跳过 all-reduce（正确性中性，性能收益）。（DeepSpeed 在某些配置下重复计数累积 → D18；world_size×batch → D11。）([HF "Fixing Gradient Accumulation"](https://huggingface.co/blog/gradient_accumulation), [DDP no_sync](https://docs.pytorch.org/docs/stable/notes/ddp.html))

### O10 — `AdamW(eps=1e-8)` 在 bf16/fp16 下下溢 → `v` 很小时的无限更新
**症状**：fp32 下稳定的运行一旦优化器数学用半精度就出现更新飙升/NaN；或 AdamW 表现得像 `eps=0`（二阶矩 `v` 很小时更新巨大）。在使用 fp16 优化器状态或 foreach/8-bit 路径以降低精度计算 `sqrt(v)+eps` 时最明显。
**根因**：AdamW 更新为 `θ -= lr·m̂/(sqrt(v̂)+eps)`。默认 `eps=1e-8` 是 fp32 值；在 fp16（以及 bf16 的 7 位尾数较轻程度）下 `1e-8` 舍入为 **0**——*"如果你使用 1e-8 作为默认值并使用 16 位，它会舍入为零。"* 当 `eps≈0`，`v̂≈0` 的参数获得无限步长。（与 GradScaler 分开，后者保护激活/梯度，不保护这个分母。）
**修复**：在半精度优化器数学下提高 eps——`eps=1e-7`（pytorch#26218 对 fp16 的提议）至 bf16 的 `1e-6`；或将优化器状态/主权重保持在 **fp32**（FSDP `MixedPrecision`、DeepSpeed bf16 保留 fp32 主权重）使默认 eps 保持有意义。相关：`betas=(0.9,0.999)` 对 `v` 做约 1000 步平均——对短微调太慢；`0.95` 是常见 LLM 规模二阶矩选择。([pytorch#26218](https://github.com/pytorch/pytorch/issues/26218), [AdamW doc](https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html))

### O11 — `fused=True` 的 AdamW 在 AMP/FSDP 下崩溃；`foreach` 膨胀峰值内存
**症状**：`AdamW(fused=True)` 在 GradScaler / bf16-mixed / FSDP 下抛出异常（如在 `_foreach_sub_` of `device_found_inf`）或误步；**或**默认 `foreach` 路径在优化器步时 OOM，而 forward/backward 时模型装得下。
**根因**：(1) fused AdamW 在一个 CUDA kernel 内通过 `found_inf` 做 unscale + step + inf/NaN 检查；特定版本的 bug（pytorch#140514, Lightning#21435）来自这些管道 / FSDP 交互——fused 仍是实验路径。(2) `foreach`（未设置时的 CUDA 默认）通过一次性为**所有**参数分配中间变量来水平融合，在 step 时提高峰值内存 vs for-loop 路径。
**修复**：在 AMP/FSDP/bf16-mixed 下遇到 fused 错误/可疑步进时，回退到 `fused=False`（让 `foreach` 默认）或升级到修复后的版本——在信任 fused 之前确认 loss 曲线一致。如果 **step** 时 OOM，设 `foreach=False` 使用低峰值 for-loop 路径（更慢，更省内存；见 oom-memory）。有意选择：fused 正确时最快，foreach 比 for-loop 快但峰值更高。([pytorch#140514](https://github.com/pytorch/pytorch/issues/140514), [Lightning#21435](https://github.com/Lightning-AI/pytorch-lightning/issues/21435), [AdamW doc](https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html))

---

## 损失函数陷阱

### O12 — `nn.CrossEntropyLoss` 前的 `softmax`/`log_softmax` → 双重 softmax → 梯度稀释，学习缓慢/不学习
**症状**：带 softmax（或 log_softmax）最终层的模型训练远慢于预期，在远高于应有值处平台化，或者对数概率被压到极端值使有效 LR 极小。在 `CrossEntropyLoss` 的原始 logits 上训练相同的架构效果明显更好。
**根因**：`nn.CrossEntropyLoss` 内部计算 `log_softmax`——*"此准则将 nn.LogSoftmax 和 nn.NLLLoss 组合在一个类中。"* 在原始 logits 上再加一层 softmax 就是双重 softmax：`log(softmax(softmax(z)))`。外层将已经压缩的 [0,1] 概率进一步压缩到狭窄范围，log 后产生极值（近 0 概率 → 大负 log），梯度变得极小。形状匹配，所以没有错误——只是训练退化了。
**修复**：将原始 logits 直接传入 `nn.CrossEntropyLoss`——移除任何显式 `softmax`/`log_softmax` 最终层。仅在推理时应用 softmax 获取概率。如果你需要不同形式的标签（one-hot、soft 标签）见 O14。([CrossEntropyLoss doc](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html))

### O13 — 手动 `sigmoid` + `nn.BCELoss` → 数值不稳定的二分类/多标签分类；对不平衡数据，`BCEWithLogitsLoss` + `pos_weight`
**症状**：多标签或二分类的 loss 是 NaN 或不稳定——手动 `sigmoid` + `nn.BCELoss` 在 sigmoid 输出接近 0 时对 `log(0)` 下溢。或者 loss 不为 NaN 但对罕见正例类收敛到平凡的全负解。普通 BCE 还对正负样本等权 → 罕见正例数据驱动平凡的全负解。
**修复**：将**原始 logits** 传入 `nn.BCEWithLogitsLoss`——它用 log-sum-exp 技巧融合 sigmoid+BCE，避免 `log(0)`。移除显式 sigmoid（仅在推理时应用）。对不平衡数据传入 `pos_weight = #neg/#pos` 按类别（`>1` 提高召回率，`<1` 提高精确率）。Target 必须是 **float**，与 logits 相同形状。([BCEWithLogitsLoss doc](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html), [numerical-stability thread](https://discuss.pytorch.org/t/numerical-stability-of-bcewithlogitsloss/8246))（不平衡*策略* → 按领域 V6。）

### O14 — `CrossEntropyLoss` 的 target 格式：long `(N,)` 索引在 `[0,C)` vs float `(N,C)` soft；差一错误 → device-side assert
**症状**：以下任一——`RuntimeError: 0D or 1D target tensor expected, multi-target not supported`（one-hot target）；`expected scalar type Long but found Float`；`IndexError: Target N is out of bounds` / CUDA `device-side assert ... t >= 0 && t < n_classes`（标签 `== C`，或标签 `1..C`，或任意 id）；或看似合理但不收敛的 loss。
**根因**：`nn.CrossEntropyLoss` 有**两种** target 格式。**类别索引**格式：target 形状 `(N,)`（比 `(N,C,...)` 输入少一个维度），dtype `long`，每个值在 `[0,C)` 中。`(N,C)` 的 target 被读作多个 target（"multi-target"）；值 `==C`（从 1 索引类别的差一错误）或不连续 id 触发边界断言——在 CUDA 上是**异步** device-side assert，可能在后续不相关行浮出。**类别概率**格式（soft/smoothed/mixup）：target 必须是 float，相同形状 `(N,C,...)`，和为 1。混淆两者就是错误。
**修复**：硬标签 → `targets.long()` 形状 `(N,)`；将 id 重映射到连续 `0..C-1`（`{orig:i for i,orig in enumerate(sorted(set(labels)))}`；若 1 索引则减 1）；`assert targets.min()>=0 and targets.max()<C`。标准路径不要做 one-hot。用 `CUDA_LAUNCH_BLOCKING=1`（或在 CPU 重跑）调试不透明的 CUDA assert 以定位真实行。Soft 标签 → float `(N,C)` 分布（不要手动 log_softmax）。用 `ignore_index` 处理填充，而非越界哨兵值（O15）。([CrossEntropyLoss doc](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html), ["Target N out of bounds" + remap](https://discuss.huggingface.co/t/indexerror-target-4-is-out-of-bounds/10213))

### O15 — 填充 token 的 loss：`reduction='mean'` 在 PAD 上平均 → 稀释的、依赖长度的 loss
**症状**：seq/NLP 模型的 loss 从第 0 步就看起来异常小，且随 batch 中填充量缩放（更多填充 → 更低 loss）；模型对真实 token 学得不足；改变 batch size 或 max-length 会改变相同数据的 loss 量级。
**根因**：默认 `reduction='mean'` 将 loss 总和除以**总**元素计数，**包括**填充位置，所以真实 token 的 loss 与（近零的）填充贡献平均——按填充比例缩小了报告的 loss 和真实 token 上的有效梯度。未掩码的填充 target 也贡献真实梯度，教模型预测填充。
**修复**：跳过填充。最简单：`nn.CrossEntropyLoss(ignore_index=PAD_ID)`——*"loss 在非忽略 target 上平均"*（对有效位置求和，除以有效计数）。否则计算 `reduction='none'`，乘以 0/1 掩码，除以 `mask.sum()`（有效 token），**不是** `mask.numel()`：`loss=(per_tok*mask).sum()/mask.sum().clamp(min=1)`。先将 logits 重塑为 `(N*T,C)`，targets 为 `(N*T,)`。（掩码输入/注意力 → 按领域 L1/L2；这里负责 loss **分母**。）([CrossEntropyLoss doc](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html), [ignore_index nuance pytorch#63004](https://github.com/pytorch/pytorch/issues/63004))

### O16 — `nn.NLLLoss` 传入原始 logits（无 `log_softmax`）→ 静默错误的 loss
**症状**：模型使用 `nn.NLLLoss` 但前面没有 `LogSoftmax`/`F.log_softmax`（或只有普通 `Softmax`）：训练"能跑"无报错但 loss 无意义/不收敛，准确率卡在随机水平。
**根因**：`nn.NLLLoss` **不**计算 softmax——*"输入...应包含 log-probabilities。"* 它只是收集 `-input[target]`。原始 logits → 它取反一个任意尺度的值；softmax **概率**（非 log）→ 它取反一个 `[0,1]` 中的值，产生微小的、尺度不当的 loss。两种情况都不是交叉熵且梯度错误，但形状合法所以 PyTorch 无法捕获。
**修复**：在 `nn.NLLLoss` 前立即放 `F.log_softmax(logits, dim=1)`（或 `nn.LogSoftmax(dim=1)` 最终层）（类别维度 = 1 对于 `(N,C)`）。更简单且不易错：去掉 NLLLoss+LogSoftmax，对原始 logits使用 `nn.CrossEntropyLoss`（O12），它融合两者。永远不要将 NLLLoss 与普通（非 log）Softmax 配对。([NLLLoss doc](https://docs.pytorch.org/docs/stable/generated/torch.nn.NLLLoss.html))

---

## 微调 / 迁移

### O17 — "冻结"的层还在变化 → `requires_grad=False` 但仍在优化器中
**症状**：你在 backbone 上设了 `requires_grad=False`（或在从 `model.parameters()` 构建优化器**之后**设置），但冻结的权重每步还在移动；预训练特征漂移和退化，尽管没有真实梯度流过。
**根因**：优化器是否接触某个参数由 `param.grad is None` 决定，**不是** `param.requires_grad`。如果冻结参数在优化器中，`backward()` 后其 `.grad` 通常是**零张量**（非 `None`），而 SGD/Adam 在更新*之前*应用**权重衰减**（`+wd·param`）和**动量/Adam 缓冲区**——所以即使在零梯度上参数也移动。`requires_grad=False` 只阻止梯度*累积*；它不会将参数从优化器中移除。
**修复**：在构造时排除冻结参数——`optim.SGD([p for p in model.parameters() if p.requires_grad], lr=...)`（或按模块参数组）。如果在构建优化器后冻结，重建它，或每步对冻结参数设 `param.grad=None`。正确冻结 = `requires_grad=False` **且**不在任何优化器参数组中（以及 Norm 层见 O18）。([forum: WD/momentum on zero grad](https://discuss.pytorch.org/t/parameters-with-requires-grad-false-are-updated-during-training/90096), [pytorch#679](https://github.com/pytorch/pytorch/issues/679))

### O18 — 冻结的 backbone 留在 `.train()` 中 → BatchNorm `running_mean/var` 静默漂移
**症状**：backbone "冻结"了（`requires_grad=False`）但验证准确率不稳定/比训练差，或 `eval()` vs `train()` 模式推理结果不一致；小 batch 微调使情况更糟。冻结的特征 batch 间持续偏移。
**根因**：BatchNorm 有两种状态——可学习仿射（`gamma/beta`，由 `requires_grad` 门控）和**不可学习**的 `running_mean/running_var` 缓冲区，每当模块处于训练模式时由 **forward pass 更新**（默认 `momentum=0.1`），独立于 `requires_grad` 和优化器。留在 `.train()` 中的冻结 backbone 因此用你的（通常很小、域偏移的）batch 统计量覆盖预训练 BN 统计量——所以"冻结"的特征提取器并不冻结。
**修复**：在 `model.train()` 后将冻结的 Norm 层设为 eval 模式：`for m in backbone.modules():
    if isinstance(m,(nn.BatchNorm1d,nn.BatchNorm2d,nn.BatchNorm3d)): m.eval()`——或将它们构建为 `track_running_stats=False`。每个 epoch 重新应用，因为顶层 `model.train()` 会翻转子模块回去。([BatchNorm2d doc](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html))（通用 train/eval 模式 bug → O5；小 batch BN → 按领域 V7。）

### O19 — 全局单一 LR 毁坏预训练特征（灾难性遗忘）→ 差异化 LR + 逐步解冻
**症状**：用单一 LR 微调要么（过高）在前几次更新就摧毁预训练表示且准确率崩溃到冻结特征基线以下，要么（过低）随机新头无法移动。两者都是同一种错误配置。
**根因**：在 step 0，backbone 接近好的最优但新头是随机的，所以其大的初始 loss 产生大梯度，在单一高 LR 下，传播到并覆盖低层预训练层（灾难性遗忘）。单一 LR 无法同时小到保留早期层又大到拟合头——修复是分组 LR，不是更多数据。
**修复**：差异化微调——逐层参数组 LR 向输入方向衰减（头最高，stem 最低），如 `AdamW([{'params':head,'lr':1e-3},{'params':backbone,'lr':1e-5}])`。结合**逐步解冻**（先训练头并冻结 backbone，然后从深到浅解冻）和 LR **warmup**，使随机头在梯度传到 backbone 前稳定下来。([Howard & Ruder 2018, ULMFiT — discriminative fine-tuning + gradual unfreezing](https://arxiv.org/abs/1801.06146))（通用过高 LR 飙升 → P12。）

### O20 — `load_state_dict(strict=False)` 在替换头上仍然 RuntimeError → 形状 ≠ 键不匹配
**症状**：你为新的 `num_classes` 替换了分类器并传 `strict=False` 期望它跳过头，但加载仍然崩溃：`RuntimeError: ... size mismatch for fc.weight: copying a param with shape [1000,...] ..., the shape in current model is [N,...]`。
**根因**：`strict=False` 仅放宽**存在性**检查——它容忍 `missing_keys`/`unexpected_keys`。它**不**放宽张量形状兼容性：任何在 checkpoint 和模型中**都**存在的键，若形状不同（正是你的旧 vs 新头 `fc.weight/bias`）仍会抛出。所以 `strict=False` 是必要的但非充分的，当头保持相同名称时。
**修复**：加载前丢弃不兼容的头条目，然后非严格加载——`sd={k:v for k,v in ckpt.items() if not k.startswith('fc.')}; missing,unexpected = model.load_state_dict(sd, strict=False)`——检查 `missing/unexpected` 确认只有头缺失。或给新头不同的属性名使其永远不冲突。（匹配架构的保存/恢复 → checkpoint-resume C1–C18。）([load_state_dict doc](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.load_state_dict), [forum: strict=False ≠ shape](https://discuss.pytorch.org/t/when-load-state-dict-strict-false-do-not-work/82301))

### O21 — LoRA/PEFT "几乎不训练"或重载随机 → `target_modules` 不匹配，头/Norm 不在 `modules_to_save` 中
**症状**：`get_peft_model(...)` 后，`print_trainable_parameters()` 显示 ~0%（或远少于预期）且 loss 不降；或 PEFT 分类器在 `save_pretrained` 后重载了一个**随机**头 / 指标偏移。
**根因**：(a) LoRA 只包装名称匹配 `target_modules` 的模块，而名称是架构特定的（Llama 的 `q_proj/v_proj` vs BERT 的 `query/value` vs resnet 的 `convolution`）——错误/缺失的名称不注入适配器，PEFT 只警告 "no modules matched"，你什么都没训练。(b) 新初始化的任务头（`score`/`classifier`）或基础模型 BatchNorm 的 `running_mean/var` 除非列在 `modules_to_save` 中**不会**被保存——重载恢复基础模型的随机头/原始 BN 统计量 → 垃圾/不可复现输出。
**修复**：用 `[n for n,_ in model.named_modules()]` 枚举真实名称并设 `LoraConfig(target_modules=[...])`（或 `'all-linear'`）；用 `model.print_trainable_parameters()` 和看到 `lora.Linear` 层来确认。将新头和任何基础 Norm 层添加到 `modules_to_save`（如 `modules_to_save=['classifier','normalization']`）——或传入正确的 `task_type`（PEFT 自动添加标准头）。([PEFT troubleshooting](https://huggingface.co/docs/peft/developer_guides/troubleshooting))

---

## 训练动态仪表盘 —— 装上它让故障可见

### O22 — 更新与权重 L2 比率 ≈ 1e-3（信号最强的 LR 旋钮）
**症状**：loss 几乎不动（步进不足）或抖动（步进过度），而裸 grad-norm 无法告诉你哪种——它不是相对于权重的尺度。
**根因**：重要的是**实际更新**相对于参数自身量级的大小——`ratio = ||lr·update|| / ||W||`，在每个张量 `step()` **之后**测量（所以它折叠了 lr、动量、Adam 的预条件、权重衰减）。CS231n 的经验法则：这应该约为 `1e-3`。更低 → LR 太低（权重几乎不变）；更高（`1e-2..1e-1`）→ LR 太高。因为是逐张量的，它暴露了单独缩放不当的层（一个 embedding 移动速度比 trunk 快 100×），而全局 grad-norm 会隐藏。
**修复**：每 K 步记录一次——在 `step()` 前快照 `w0={n:p.detach().clone() for n,p in model.named_parameters()}`，然后每名称计算 `(p.detach()-w0[n]).norm()/(w0[n].norm()+1e-12)`。杠杆：`<<1e-3` → 提高该组的 LR；`>>1e-3` → 降低 LR / 延长 warmup。按参数组追踪，而非仅全局。([CS231n "Neural Networks 3"](https://cs231n.github.io/neural-networks-3/))（补充 P12/P18。）

### O23 — 记录**实际**逐步 LR，而非配置值
**症状**：你记录 `cfg.lr`（常数）所以仪表盘 LR 是平的——但你用的是 warmup+余弦。你看不到 warmup、衰减、重启或冻结的调度器；与 LR 相关的 loss 行为（爬升时飙升、触底时停滞）不可见。
**根因**：有效 LR 存在于 `optimizer.param_groups[i]['lr']` 中，由 `scheduler.step()` 每步重写（差异化/无衰减 LR 时按组）。失败模式：画配置标量（从不变化）；或 O8 顺序 bug 跳过第一个值。还有 `get_lr()` 返回"前进一步"的值——读取它而非 `get_last_lr()` 会记录错误数字。
**修复**：记录 `scheduler.get_last_lr()`（一个列表——每个参数组一个；如果用差异化 LR 则全部记录）或直接读 `optimizer.param_groups[0]['lr']`，每步。不要用 `get_lr()` 做日志。如果记录的 LR 在应该爬升/衰减时平坦，你的调度器没被步进（或步进节奏错误 → O8）。([torch.optim](https://docs.pytorch.org/docs/stable/optim.html), [lr_scheduler source — get_last_lr](https://github.com/pytorch/pytorch/blob/main/torch/optim/lr_scheduler.py))

### O24 — GradScaler 缩放趋向 0 = 静默的持续 fp16 溢出
**症状**：fp16-AMP 运行看起来健康（loss 打印、无崩溃）但没有学习或静默跳过很多优化器步——因为你从未画过 `scaler.get_scale()` 且 loss-scale 已从 65536 坩塌到 ~1（或锯齿状下降）。
**根因**：GradScaler 调整乘性 loss-scale：遇到任何 inf/NaN 梯度时乘以 `backoff_factor=0.5` **并跳过**该 `step()`；经过 `growth_interval=2000` 个干净步后乘以 `growth_factor=2.0`（`init_scale=65536`）。早期几次回退是正常校准（P5/P10），但持续减半并保持低位的缩放意味着 forward 持续产生 `> fp16 的 65504` 的值 → 梯度溢出 → 每步都跳过 → 权重冻结而 loss 看似合理。配置 "fp16" 什么都告诉你；只有实时缩放能揭示它。
**修复**：将 `scaler.get_scale()` 和跳过步计数器添加到仪表盘。健康：早期校准后的高位平台（`2^13..2^16`）。不健康：向 1 单调衰减，或步计数不随迭代计数推进。坍塌时的杠杆：切换 **fp16 → bf16**（无需 scaler；fp32 指数范围吸收大激活——最高杠杆），或通过嵌套 `autocast(enabled=False)` 将溢出倾向的块（最终 logits / 注意力）保持在 fp32，加上 z-loss / qk-norm（P15/P16）。不要通过降低 `init_scale` 来"修复"。([torch.amp GradScaler](https://docs.pytorch.org/docs/stable/amp.html))（机制 → P5/P10。）

### O25 — 死 ReLU / 零激活比例上升 → 网络的一部分永久关闭
**症状**：容量悄悄消失——某层输出越来越全零，loss 在应有水平上方平台化，增加宽度没用。无崩溃；只是欠拟合。最坏情况网络退化为常数函数。
**根因**：一个 ReLU 的预激活被驱动为对所有输入约负时输出 0，且该处**零**局部梯度，所以反向传播不给其输入权重发送信号——单元卡死且不可恢复。由过高 LR（大更新将权重/bias 推到深度负值）或大负偏置触发。一旦层的大部分死亡，梯度无法流过，容量就没了。同样的形状（饱和 → ~0 梯度 → 冻结区域）适用于 sigmoid/tanh 尾部。
**修复**：用 forward hook 检测每层激活的零/饱和比例——ReLU 用 `(out==0).float().mean()`（或 tanh/sigmoid 用 `|out|>0.99`），每 K 步每层记录。健康：稳定的适度死亡比例（ReLU 设计上就是稀疏的）。不健康：训练过程中比例攀升或某层钉在 ~100% 死亡。杠杆，按顺序：(1) 降低 LR（主要原因）；(2) ReLU → LeakyReLU / GELU / SiLU 使负区域保留梯度；(3) 修复初始化 / 大负偏置。([CS231n "Neural Networks 1" — dying ReLU](https://cs231n.github.io/neural-networks-1/))（*输出*为常数由 verifying-dl-experiments 负责；这里是内部机制。）

### O26 — 没有权重/梯度/激活直方图 → 标量范数隐藏双峰/饱和/坍缩分布
**症状**：标量仪表盘（loss、一个 grad-norm）看起来正常但模型表现不佳或不稳定——均值/范数隐藏了形状：激活漂移到饱和尾部、权重坍缩到 0 处的尖峰（层在死亡，O25）、或梯度分布长出胖尾异常值，在标量上都读作不起眼的数值。
**根因**：范数和均值是有损摘要——健康的展布和双峰/全饱和/全零分布可以有相同的 L2 范数。诊断信号是**训练过程中形状的变化**，标量无法展示。
**修复**：定期（每几百步——直方图有开销）为每层的**权重**、其**梯度**（`backward` 后、`zero_grad` 前）和关键**激活**（forward hook）记录 `SummaryWriter.add_histogram(tag, values, global_step)`。解读时间演化：权重坍缩到尖峰 = 层在死亡；梯度直方图坍缩到 ~0 = 消失（杠杆：残差/norm/初始化，P17）；胖尾 = clip + 降低 LR（P13/P12）；激活游走到饱和尾部 = 初始化/归一化修复（P17）。与上述标量配对使用。([SummaryWriter.add_histogram](https://docs.pytorch.org/docs/stable/tensorboard.html), [Karpathy recipe — visualize weights/activations](https://karpathy.github.io/2019/04/25/recipe/))

---

## 指针 —— 其他地方编录的相关机制

- **NaN / loss 飙升 / LR 过高 / 梯度爆炸 / z-loss / qk-norm / 初始化与 norm 位置 / 确定性** → `references/training/precision-stability.md`（P8–P19）。本文档是 LR 过低 / 不动的一侧；那个是爆炸的一侧。
- **优化器步的 OOM / 激活检查点 / LoRA-QLoRA 内存** → `references/training/oom-memory.md`（M5, M12–M13）。
- **N-GPU 有效 batch × LR、DeepSpeed 累积重复计数、find_unused_parameters** → `references/training/distributed-launch.md`（D11, D18, D8）。
- **模仿"学不动"的 DataLoader 正确性问题（worker RNG、collate、标签、shuffle）** → `references/training/data-pipeline.md`。
- **收敛的数字是否真实**（崩溃、泄露、训练 vs 验证、指标有效性、种子纪律）→ **verifying-dl-experiments**（**必需**——上述每个"结果是否真实"的分支）。
