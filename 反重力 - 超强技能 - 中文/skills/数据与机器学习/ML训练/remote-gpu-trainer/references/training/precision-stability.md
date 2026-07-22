# 数值精度与训练稳定性 — 先让它跑起来，再阻止它发散

在租用 GPU 上让深度学习运行算出*有限*数字的机制，以及在 loss 变 NaN 或 spike 时调试的机制。本层负责**让它跑起来 + 发散的机制**；它不负责*收敛数字是否真实* / cuDNN 非确定性作为指标误差 — 那是 **verifying-dl-experiments** 的职责（在每个"这是 bug 还是真实效果"的分支处交叉引用，**必需**）。

快速跳转：`grep -in '<keyword>' references/training/precision-stability.md`（例如 `tf32`、`bf16`、`scaler`、`nan`、`anomaly`、`z-loss`、`clip`、`warmup`、`qk`、`deterministic`）。

## 目录

- **精度选择** — P1 fp32/tf32/fp16/bf16 决策 · P2 TF32 默认关闭脚枪 · P3 H100/A100/V100 能力
- **AMP 机制** — P4 autocast 范围 · P5 GradScaler（仅 fp16） · P6 bf16 不需要 scaler · P7 scaler 下的梯度裁剪
- **NaN / Inf** — P8 NaN 从哪来 · P9 异常检测 · P10 fp16 溢出 vs 下溢 · P11 坏数据 NaN
- **Loss spike / 发散** — P12 LR + warmup · P13 梯度裁剪 · P14 跳过批次 · P15 z-loss · P16 qk-norm · P17 初始化
- **梯度** — P18 爆炸/消失诊断
- **复现** — P19 确定性旋钮（交叉链接）
- **指针** — gotchas_universal.md, multinode.md, spot-resilience.md

---

## 精度选择

### P1 — 选择哪个精度：fp32 / TF32 / fp16 / bf16

**症状**：不确定用哪个 `dtype` 训练；运行要么慢（fp32），要么容易 NaN（fp16）。

**根因**：四种模式在动态范围、尾数精度和 tensor core 速度之间权衡。fp16 只有 5 位指数（最大约 65504），所以容易*溢出*和*下溢*；bf16 保持 fp32 的 8 位指数（与 fp32 相同范围）但只有 7 位尾数，所以从不需要 loss scaling，但每个值更粗糙。TF32 是 fp32 存储模式，在 tensor core 上以 10 位尾数运行矩阵乘法。

**修复 — 默认阶梯（PyTorch 2.x）**：
1. 在 Ampere+（A100/H100/4090/...）上使用 **bf16 autocast** — 现代默认；与 fp32 相同范围，无 GradScaler，健壮。`torch.autocast("cuda", dtype=torch.bfloat16)`。
2. 为剩余的 fp32 矩阵乘法（非 autocast 路径）启用 **TF32** — `torch.set_float32_matmul_precision("high")`。免费提速，对大多数网络收敛影响可忽略（P2）。
3. **仅在**没有 bf16 tensor core 的卡上（V100/T4/2080Ti）使用 **fp16 autocast + GradScaler** — 需要 scaler（P5），且容易溢出。
4. **纯 fp32** 作为诊断回退：如果运行出现 NaN，*首先*证明它在 fp32 下是有限的，再归咎于模型。fp32 隔离"这是数值 bug 还是模型 bug"。

bf16 处理大点积/注意力 logits 比 fp16 好，fp16 会饱和并触发 scaler 步跳过。URL：https://docs.pytorch.org/docs/2.12/amp.html · https://www.runpod.io/articles/guides/fp16-bf16-fp8-mixed-precision-speed-up-my-model-training

### P2 — TF32 自 PyTorch 1.12 起默认关闭用于矩阵乘法 — "为什么 A100 慢"脚枪

**症状**：fp32（或 autocast 但 fp32 矩阵乘法密集）运行在 A100/H100 上比预期慢约 2–4 倍；代码没有问题。

**根因**：`torch.backends.cuda.matmul.allow_tf32` 在 **1.7–1.11 默认为 True**，然后在 **1.12+ 翻转为 False**（非 DL 用户的精度损失投诉）。所以全新 PyTorch 2.x 环境在 tensor core 的慢路径上以完整 fp32 运行矩阵乘法，除非重新启用 TF32。卷积的 TF32（`cudnn.allow_tf32`）是单独的旋钮，默认启用。

**修复**：在启动时一次性重新启用 —
```python
torch.set_float32_matmul_precision("high")   # 推荐：为 fp32 矩阵乘法启用 TF32（或 bf16x3）
# 等效旧版，仍可工作：
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
```
`"high"` = TF32；`"highest"` = 真正 fp32（默认）；`"medium"` = 更粗糙。HF Trainer 暴露 `--tf32 1`。大多数网络用 TF32 与 fp32 收敛一致。URL：https://github.com/pytorch/pytorch/pull/76509 · https://docs.pytorch.org/docs/stable/generated/torch.set_float32_matmul_precision.html · https://docs.pytorch.org/docs/2.12/notes/numerical_accuracy.html

### P3 — 显卡能力决定选择：bf16 需要 Ampere+；V100/T4 只有 fp16

**症状**：bf16 训练意外地慢（无报错），或配置在旧卡上选择 bf16 落入慢路径。

**根因**：快速 bf16 tensor core 随 **Ampere（A100、RTX 30xx）** 到来；Hopper（H100/H200）增加原生 **FP8**。**V100/T4/RTX 20xx 有 fp16 tensor core 但没有快速 bf16**（以模拟/慢速运行）。租用环境随机分配空闲的卡，所以正确的精度是*每次租用*的事实，不是常量。

**修复**：运行时根据能力分支，永不硬编码 —
```python
use_bf16 = torch.cuda.is_bf16_supported()    # Ampere+ 上为 True
amp_dtype = torch.bfloat16 if use_bf16 else torch.float16
```
在 V100/T4 上使用 fp16+GradScaler（P5）。FP8（H100）通过 Transformer Engine / `torchao` 选择启用，不是普通 autocast（超范围）。在 Phase 0 将卡型号记录在 `nvidia-smi` 旁边。
URL：https://www.e2enetworks.com/blog/nvidia-a100-vs-h100-vs-h200-gpu-comparison

---

## AMP 机制

### P4 — autocast：只包裹前向 + loss，绝不包裹反向，绝不 `.half()` 模型

**症状**：dtype 不匹配错误，或 AMP 无加速，或梯度看起来不对。

**根因**：autocast 是一个上下文，在区域内按操作转换*符合条件的操作*；手动 `.half()` 模型或包裹反向传播会与之冲突。

**修复**：
```python
for x, y in loader:
    optimizer.zero_grad(set_to_none=True)
    with torch.autocast("cuda", dtype=amp_dtype):   # 仅前向 + loss
        out = model(x); loss = loss_fn(out, y)
    # 反向在 autocast 之外：
    loss.backward()                                 # （fp16 需加 scaler，P5）
    optimizer.step()
```
保持模型和优化器在 fp32；不要调用 `model.half()`。使用新 API `torch.amp.autocast("cuda", ...)` / `torch.amp.GradScaler("cuda")` — `torch.cuda.amp.*` 在 PyTorch 2.x 中**已弃用**。autocast 状态是线程局部的（在每个 DDP/DataParallel worker 线程内重新进入）。
URL：https://docs.pytorch.org/docs/2.12/amp.html

### P5 — GradScaler：fp16 必需，用于阻止梯度*下溢*

**症状（无 scaler，fp16）**：loss 看起来正常但模型不学习 — 小梯度在 fp16 极小的次正规范围内被冲为零。

**根因**：fp16 的窄范围将小梯度下溢为零。GradScaler 在反向传播前将 loss 乘以一个大因子（将梯度推入可表示范围），然后在步之前反缩放并**自适应调整因子**：遇到任何 inf/NaN 梯度时*跳过优化器步*并将缩放因子减半（回退 0.5）；经过 `growth_interval`（默认 2000）个干净步后将其翻倍（增长 2.0）。

**修复 — 标准fp16循环**：
```python
scaler = torch.amp.GradScaler("cuda")
for x, y in loader:
    optimizer.zero_grad(set_to_none=True)
    with torch.autocast("cuda", dtype=torch.float16):
        loss = loss_fn(model(x), y)
    scaler.scale(loss).backward()
    scaler.step(optimizer)     # 内部反缩放；发现 inf/NaN 则跳过步
    scaler.update()            # 自适应缩放因子
```
训练早期 scaler 校准时的"跳过步"警告是**正常的**；*持续*每步跳过 = 真正的溢出（去 P10）。URL：https://github.com/pytorch/pytorch/blob/main/docs/source/notes/amp_examples.rst · https://docs.pytorch.org/docs/2.12/amp.html

### P6 — bf16 不需要 GradScaler（加一个是无用的，不是有害的）

**症状**：复制的 fp16 配方把 GradScaler 带入了 bf16 运行 — 浪费开销，不是崩溃或错误结果。

**根因**：bf16 有 fp32 的指数范围，所以梯度不会下溢 → loss scaling 是不必要的，scaler 的跳过/回退机制是死代码（缩放再反缩放相消，且永远找不到溢出来跳过）。

**修复**：bf16 时完全不用 scaler — 简单的 `loss.backward(); optimizer.step()`。只有 fp16（和 V100/T4 路径）使用 GradScaler。
URL：https://docs.pytorch.org/docs/2.12/amp.html

### P7 — GradScaler 下的梯度裁剪：先 `unscale_` 否则裁剪的是缩放后的梯度

**症状**：fp16 AMP 下 `clip_grad_norm_` 无效，或在错误量级上裁剪。

**根因**：在 scaler 内部梯度仍被乘以（大的）缩放因子，所以裁剪到 `max_norm=1.0` 实际上是裁剪到 `1.0 × scale` — 等于没裁剪。

**修复**：先 `scaler.unscale_(optimizer)` 一次，然后裁剪，然后 `scaler.step`：
```python
scaler.scale(loss).backward()
scaler.unscale_(optimizer)                                  # 梯度现在在真实量级
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
scaler.step(optimizer); scaler.update()
```
`unscale_` 每步幂等（调用一次）。bf16 时直接 `clip_grad_norm_` — 无需 unscale。
URL：https://github.com/pytorch/pytorch/blob/main/docs/source/notes/amp_examples.rst

---

## NaN / Inf

### P8 — NaN 从哪来：四种算术根源

**症状**：loss 在 N 步后打印 `nan`（或 `inf`）；之前一切正常。

**根因** — NaN/Inf 由坏输入上的*有限*操作集合产生：
- `log(x)` / `log_softmax` 当 `x ≤ 0`（例如 `sigmoid` 输出达到 0 时的 `log`）。
- `sqrt(x)` / `x ** 0.5` 当 `x < 0`，或其在 `x = 0` 的梯度（`d/dx sqrt = 1/(2√x) → inf`）。
- 除法 `a / b` 当 `b → 0`（无 epsilon 的归一化，BatchNorm/LayerNorm 中方差 ≈ 0）。
- `exp(x)` 溢出 → `inf`，然后 `inf − inf` / `inf / inf → nan`。
- fp16 溢出（P10）：值超过 65504 → `inf` → 梯度 → NaN。

**修复 — 让操作稳定，不要掩盖它**：
- 永远不要手写 `log(softmax(x))` — 用 `F.log_softmax` / `F.cross_entropy`（融合的，log-sum-exp 稳定的）。
- 在不稳定操作内部加 epsilon：`torch.log(x + 1e-8)`、`torch.sqrt(x + 1e-12)`、`a / (b + 1e-8)`。
- 在危险操作前 clamp：`log` 前 `x.clamp(min=1e-7)`；手动 softmax 前 clamp logits。
- 在优化器/归一化中使用 `eps`（AdamW `eps=1e-8`；如果 `v` 很小且步爆炸则适当提高）。

URL：https://docs.pytorch.org/docs/stable/generated/torch.log.html · https://medium.com/better-ml/loss-spikes-in-training-causes-detection-and-mitigations-ed66e591b1a1

### P9 — 找到确切操作：异常检测 + 廉价前向钩子

**症状**：loss 是 NaN 但堆栈跟踪指向 `loss.backward()`，而非导致它的操作。

**根因**：默认 NaN 在被*消费*的地方显现，而非在*产生*的地方。

**修复 — 两种工具，从廉价到精确**：
- **前向 NaN 钩子（廉价，可常驻）** — 在每个模块上注册以捕获*第一个*发出 NaN 的层：
  ```python
  for name, m in model.named_modules():
      m.register_forward_hook(lambda mod, i, o, n=name:
          print(f"NaN in {n}") if torch.is_tensor(o) and not torch.isfinite(o).all() else None)
  ```
- **`torch.autograd.set_detect_anomaly(True)`（昂贵，仅调试用）** — 记录每个反向操作的回溯并在第一个反向 NaN 处抛出，指向创建它的*前向*行。
  ```python
  with torch.autograd.detect_anomaly():   # 或 set_detect_anomaly(True, check_nan=True)
      loss.backward()
  ```
  文档警告它会"减慢你的程序"（大约一个数量级）— 用于*定位*，然后在正式运行中关掉，永远不要在线上启用。URL：https://docs.pytorch.org/docs/2.12/autograd.html

### P10 — fp16 溢出 vs 下溢：读 GradScaler 信号

**症状（fp16）**：loss → inf/NaN；或 scaler 跳过*每一步*且缩放因子向 0 坍缩。

**根因**：一个前向激活超过 fp16 的 65504 上限 → `inf` → NaN 梯度 → scaler 找不到避免溢出的缩放因子，所以永远回退。常见于注意力 logits 和大残差和中。（不同于下溢，scaler 通过 P5 *修复*下溢。）

**修复**：切换 fp16 → **bf16**（P1）— 其 fp32 范围吸收大值；这是最有效的单一修复。如果 bf16 不可用（V100/T4）：通过嵌套 `torch.autocast("cuda", enabled=False)` 区域将易溢出块（最终 logits、注意力分数、loss）保持在 **fp32**，并应用 z-loss（P15）/ qk-norm（P16）阻止 logits 增长。
URL：https://medium.com/better-ml/loss-spikes-in-training-causes-detection-and-mitigations-ed66e591b1a1

### P11 — 来自*数据*的 NaN，不是数学

**症状**：NaN 出现在特定可复现的步（总是第 4137 步），不是渐进的。

**根因**：一个损坏的样本 — NaN/Inf 像素、全零目标、标签在 `[0, C)` 之外、空序列、自定义变换中的除以零。数学没问题；输入有毒。

**修复**：在数据边界做防护 — `assert torch.isfinite(x).all(), f"non-finite input @ step {step}"`（大声失败，带索引）。可复现步 NaN ⇒ 检查*那个批次*（为 loader 设种子，导出索引）；*步变化的* NaN ⇒ 数值/LR 问题（P12），不是数据。先检查数据 — 检查*内容*属于 **verifying-dl-experiments**（交叉链接**必需**）。
URL：https://arxiv.org/pdf/2311.03938

---

## Loss spike / 发散

### P12 — Loss spike / 发散：LR 太高或 warmup 太短

**症状**：训练稳定，然后 loss 跳跃几个数量级（spike），有时恢复，有时发散到 NaN — 最常出现在早期，或在快速 LR 上升后。

**根因**：如果 LR 上升太快或起始太高，早期更新落在激活范数和优化器二阶矩（`v`）稳定之前，冲入尖锐的 loss 区域 → 梯度范数爆炸 → spike。持续的**梯度范数**上升通常在 loss spike 前几步就*先行出现*。

**修复 — 按廉价程度排序**：
1. **延长 warmup**（线性从 0 增到峰值，如步数的 1–10%）；warmup 是对 LR 敏感性的最大杠杆。
2. **降低峰值 LR** 约 3–10 倍并重试。
3. **每步记录梯度范数**作为早期预警信号 — spike 在击中 loss 前可从激活/梯度范数缩放中预测。
4. 从 spike 前*最后好的* checkpoint 恢复（不要在发散区域继续训练）。

URL：https://arxiv.org/pdf/2309.14322 · https://apxml.com/courses/how-to-build-a-large-language-model/chapter-24-identifying-mitigating-training-instabilities/stabilization-techniques-revisited

### P13 — 梯度裁剪：标准护栏（以及持续裁剪意味着什么）

**症状**：偶发的梯度范数 spike；或在单个坏批次后 NaN。

**根因**：一个病态批次（稀有 embedding ID、异常样本）产生过大的全局梯度范数导致冲过头。

**修复**：每步裁剪全局梯度范数 — `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)`，transformer 典型 `max_norm` ∈ [0.5, 1.0]（在 scaler 下：P7）。**诊断**：如果裁剪在*每步*都活跃或需要极低阈值才能稳定，那是更深层问题的症状（LR 太高 P12、坏初始化 P17、架构问题），不是修复 — 追根因。全局范数裁剪将*所有*梯度按比例缩小，所以一个 embedding 密集的批次可能限制其他所有参数 — 如果 embedding 主导，考虑按模块裁剪。
URL：https://medium.com/better-ml/loss-spikes-in-training-causes-detection-and-mitigations-ed66e591b1a1

### P14 — 跳过批次：当此步非有限时丢弃更新

**症状**：每几千步一个坏批次让整个运行 NaN；重启浪费数小时。

**根因**：优化器应用了非有限梯度并永久损坏了权重。

**修复**：以有限性作为优化器步的门控（fp16 的 GradScaler 已在内部做此，P5；bf16 需显式实现）：
```python
loss.backward()
gnorm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
if torch.isfinite(gnorm):
    optimizer.step()
else:
    optimizer.zero_grad(set_to_none=True)   # 跳过此批次，保持权重完整
    skipped += 1
```
记录 `skipped` 计数器 — *上升的*跳过率意味着系统性问题（P12/P10），不是零星坏数据。自适应 spike 裁剪（ZClip）和 spike 时的动量重置（SPAM）为大规模运行自动化了这一过程。URL：https://arxiv.org/pdf/2504.02507 · https://arxiv.org/pdf/2501.06842

### P15 — z-loss：阻止 softmax logits 无限漂移

**症状**：训练缓慢失稳；softmax 归一化因子/输出 logits 随时间增长并最终溢出（在 fp16/bf16 中尤为严重）；"输出 logits 与 log-probs 脱离"的故障模式。

**根因**：没有东西锚定 pre-softmax logits 的绝对尺度，所以它们向上漂移；大 logits 导致数值不稳定且（在低精度下）溢出 → 崩溃。

**修复**：添加辅助 **z-loss** = `1e-4 · (log Z)²`，其中 `Z` 是 softmax 分母（`log Z = logsumexp(logits)`），将 `log Z` 拉向 0：
```python
logits = model(x)
z = torch.logsumexp(logits, dim=-1)
loss = F.cross_entropy(logits, y) + 1e-4 * (z ** 2).mean()
```
系数 **1e-4** 是 PaLM/ST-MoE 的值；太大会让 z-loss 主导。LLM 预训练的标准做法；也是 MoE 路由不稳定性的推荐修复。URL：https://medium.com/dair-ai/papers-explained-50-palm-480e72fa3fd5 · https://arxiv.org/pdf/2202.08906 · https://arxiv.org/pdf/2309.14322

### P16 — qk-norm：在高 LR 下扼杀注意力 logits 增长

**症状**：transformer 仅在高 LR 时发散；不稳定性追溯到注意力分数（Q·Kᵀ）在 softmax 前增长过大。

**根因**："注意力层中 logits 的增长" — transformer 两种主导不稳定性模式之一（另一种是输出 logits 发散，P15）。无界的注意力 logits 使 softmax 饱和。

**修复**：应用 **QK-LayerNorm** — 在点积前对 query 和 key 逐头做 LayerNorm。结合 z-loss（P15）+ warmup（P12），它让小模型在 LR *跨越多个数量级*时训练到相似 loss，即消除了大部分 LR 敏感性。URL：https://arxiv.org/pdf/2309.14322

### P17 — 初始化与归一化放置

**症状**：无论 LR 如何，前几百步就发散；或在深层堆叠中信号消失（P18）。

**根因**：残差流随深度累积方差；默认初始化可能使早期激活/梯度过大（spike）或过小（消失）。归一化/embedding 初始化尺度很重要。

**修复**：按 `1/√(2·n_layers)` 缩放残差分支初始化（GPT-2 风格）；深层 transformer 优先用 pre-LN 而非 post-LN；以小 std（约 0.02）初始化 embedding。不确定时，复制*已知可用*配置的初始化+归一化方案，而非盲目调参。URL：https://arxiv.org/pdf/2309.14322

---

## 梯度

### P18 — 梯度爆炸 vs 消失：通过记录范数诊断

**症状**：loss NaN/发散（爆炸）或 loss 停滞且模型永远不学习（消失）。

**根因**：逐层梯度范数爆炸（爆炸：深层网络、高 LR、无裁剪）或衰减至约 0（消失：饱和激活、坏初始化 P17、过深的无归一化堆叠）。

**修复 — 先测量**：
```python
total = sum(p.grad.detach().norm()**2 for p in model.parameters() if p.grad is not None) ** 0.5
# 每步记录 `total`；追查罪魁层时也记录逐层范数
```
- **爆炸**（范数 ↑↑）：梯度裁剪（P13）、降低 LR（P12）、更长 warmup、bf16 替代 fp16（P10）。
- **消失**（范数 → 0）：残差连接、归一化层、更好初始化（P17）、非饱和激活（GELU/SiLU 替代深层 sigmoid/tanh 堆叠）、检查 LR 是否*太低*。

梯度范数轨迹是最廉价、最高信号的稳定性仪表 — 从第 1 步开始记录。
URL：https://apxml.com/courses/how-to-build-a-large-language-model/chapter-24-identifying-mitigating-training-instabilities/stabilization-techniques-revisited

---

## 可复现性

### P19 — 确定性/可复现旋钮 — 设置它们，但*解释*是委托的

**症状**：相同配置 + 种子在运行间给出略不同的 loss/指标。

**根因**：非确定性 CUDA 内核 + `cudnn.benchmark` 自动调优每次运行选择不同算法；TF32/AMP 在此之上增加低阶噪声。

**修复 — 机械旋钮（在此设置）**：
```python
torch.manual_seed(s); np.random.seed(s); random.seed(s)
torch.use_deterministic_algorithms(True)        # 可能需要 CUBLAS_WORKSPACE_CONFIG=:4096:8
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False          # benchmark=True 以速度换确定性
```
**运行间差异是"真实效果 vs cuDNN 非确定性"，以及完整确定性方法论，由 verifying-dl-experiments 负责（交叉链接必需）** — 在 `references/gotchas_universal.md` 中编目为 **U36**。本层只确保旋钮*被设置和记录*。确定性有速度代价 — 只在必须干净的数据点上启用，不是每个临时运行。
URL：https://docs.pytorch.org/docs/stable/notes/randomness.html

---

## 指针 — 相邻层，不要在此重复

- **`references/gotchas_universal.md`** — 伪装成数值问题的*基础设施*故障模式：**U6** 磁盘满导致 `torch.save` 崩溃、**U9** cgroup-OOM（裸 `Killed`，不是 NaN）、**U28** CUDA/驱动/torch 构建不匹配（`no kernel image` ≠ 精度 bug）、**U10/U11** VRAM OOM。在追逐"数值"幽灵之前先排除基础设施。
- **`verifying-dl-experiments`**（**必需**交叉链接）— 负责*数字是否真实*：检查**内容**、cuDNN 非确定性作为指标误差（U36）、坍缩/常量输出诊断、"bug vs 真实效果"。本文件让训练*运行并保持有限*；那个技能判断收敛结果是否*真实*。
- **`references/spot-resilience.md`** — 检查点节奏，使发散-恢复（P12）丢失最少工作。
- **`references/multinode.md`** — 多节点运行中 DDP 的 NCCL/精度交互（all-reduce dtype、loss-scale 同步）；单机用户跳过。
