# 按领域训练陷阱 — LLM / 视觉 / 扩散 / RL / 多模态

当"能跑但结果可疑"的问题位于**领域惯例**而非通用数值精度或数据加载时。每个条目都是 `症状 → 根因 → 修复`。通用调试层（OOM、多 GPU 挂起、精度/NaN、吞吐、检查点、收敛、数据管道）位于同级文件；本文件**仅**添加领域特有的内容 — 那些跨领域通用的条目属于那八个通用文件。

跳转：`grep -in '<keyword>' references/training/by-domain.md`（例如 `categorical`、`logit`、`diffusion`、`ema`、`vq`、`kl`、`reward`、`rlhf`、`clip`、`multimodal`、`lora`）。

## 目录

- **LLM（预训练 / 微调）** — DF1 loss≠质量 · DF2 EMA-权重 · DF3 tokenizer-PAD · DF4 embedding-缩放 · DF5 LM-损失-偏移 · DF6 LoRA-合并-钩子
- **视觉（分类 / 检测 / 分割）** — DF7 BN-冻结-漂移 · DF8 分类头-不匹配 · DF9 检测-Anchor-偏差 · DF10 分割-忽略-索引
- **扩散（生成模型）** — DF11 噪声-调度-不匹配 · DF12 VAE-梯度-泄漏 · DF13 CFG-无分类器-退化 · DF14 时间步-采样-偏差 · DF15 EMA-推理-偏移
- **RL / RLHF** — DF16 reward-缩放 · DF17 KL-惩罚-崩溃 · DF18 价值-函数-初始化 · DF19 GAE-λ-方差 · DF20 旧策略-概率-零
- **多模态** — DF21 模态-不平衡 · DF22 CLIP-温度-固定 · DF23 对齐-投影-未训练

---

## LLM（预训练 / 微调）

### DF1 — 训练 loss 下降但输出是乱码 / "重复同一 token"

**症状**：验证 loss 也在降，但生成输出是重复的、无意义的、或退化到单一 token 循环。

**根因**：自回归 LM 的交叉熵 loss 衡量*下一个 token 预测的校准度*，而非*连贯性*。极低的 loss 仍可对应退化的输出模式 — 尤其当：(a) 数据集很小/重复，模型记忆而非泛化；(b) 采样温度=0 或 top-k=1，强制每步选最高概率 token；(c) 重复惩罚为 0 或不存在。

**修复**：用多种采样设置（temperature=0.7–1.0, top_k=50, top_p=0.9）评估生成质量，不只看 loss。增加重复惩罚（frequency_penalty / presence_penalty）。对于小数据集微调，正则化（dropout, weight decay）和早停防止记忆。使用 **verifying-dl-experiments** 确认生成质量，不只是 loss 曲线。

### DF2 — 微调后 EMA 权重比原始权重差

**症状**：用 EMA（指数移动平均）权重评估时效果比用训练权重差 — 特别是在 LoRA 微调后。

**根因**：LoRA 的低秩适配器在训练初期变化剧烈，EMA 的慢速更新（通常 β=0.999）使影子权重严重滞后于实际适配器权重。对于短微调（<1000 步），EMA 几乎没追上。

**修复**：短微调时使用更快的 EMA 衰减（β=0.99 或 0.9），或不使用 EMA。如果必须使用 EMA，至少等待 2× 衰减时间的步数后才用它评估。对于 LoRA，考虑 EMA 只应用于基础模型权重（如果基础模型已冻结，则 EMA 就是基础模型本身 — 无需额外 EMA）。

### DF3 — Tokenizer PAD token 导致训练崩溃或 NaN

**症状**：loss 突然跳到极大值或 NaN；调查发现 PAD token 的 embedding 被梯度更新破坏。

**根因**：许多 tokenizer 没有 PAD token（如 LLaMA 的原始 tokenizer）；`tokenizer.pad_token = tokenizer.eos_token` 的设置让 PAD 共享 EOS 的 embedding，但 attention mask 未正确屏蔽 PAD 位置，导致梯度流向 EOS embedding 并破坏它。

**修复**：添加一个**新的** PAD token（`tokenizer.add_special_tokens({'pad_token': '<pad>'})`）并调整 `model.resize_token_embeddings(len(tokenizer))`，而非复用 EOS。确保 `labels` 中 PAD 位置设为 `-100`（`ignore_index`）。如果必须共享 EOS，在训练中冻结 `model.get_input_embeddings().weight[eos_token_id]`。

### DF4 — Embedding 层缩放因子缺失或错误

**症状**：模型输出偏离或 loss 偏高；特别是从原始权重转换或跨框架加载时。

**根因**：某些架构（如原始 Transformer、GPT-2 风格）对 embedding 输出乘以 `sqrt(d_model)` 缩放；在加载权重或修改代码时遗漏此缩放会使所有后续层的输入尺度偏移 `sqrt(d_model)` 倍。

**修复**：确认模型定义中 embedding 层后是否有 `math.sqrt(d_model)` 乘法。检查点加载时确保缩放因子一致。这是一个**初始化尺度**问题 — 如果预训练时有的缩放微调时被移除，所有权重都不匹配。

### DF5 — LM 损失的 label 偏移（shift logits vs shift labels）

**症状**：训练 loss 异常低（模型似乎完美预测），但生成完全不正确；或 loss 异常高且不收敛。

**根因**：自回归 LM 的交叉熵需要将预测（logits）和目标（labels）对齐：logits[t] 预测 tokens[t+1]。两种实现方式：(a) `shift_logits = logits[:, :-1]`, `shift_labels = labels[:, 1:]`（移位 logits）；(b) `shift_labels = labels[:, :-1]`, `shift_logits = logits[:, 1:]`（移位 labels）。混淆两者导致预测和目标错位一个位置 — 要么 loss 虚低（预测"下一个的下一个"），要么 loss 虚高。

**修复**：统一使用一种约定并坚持。HF Transformers 使用 `(shift_logits, shift_labels) = (logits[:, :-1, :], labels[:, 1:])`。验证时：取一个小 batch，手动检查 `logits[0, t]` 的 argmax 是否等于 `labels[0, t+1]`。

### DF6 — LoRA 合并钩子在保存/加载时导致权重重复

**症状**：合并 LoRA 后（`model.merge_and_unload()`）保存的权重比原始模型大，或加载合并后的模型时参数量翻倍。

**根因**：某些框架的 `merge_and_unload` 未正确移除 LoRA 的钩子/适配器，导致保存时既保存了合并后的基础权重又保存了适配器权重。

**修复**：合并后、保存前，检查 `model.named_modules()` 确认没有残留的 LoRA 层。使用 `peft` 库时，`model.merge_and_unload()` 后再 `model.save_pretrained()`。验证保存的模型文件大小与原始基础模型一致（仅权重变化，无适配器开销）。

---

## 视觉（分类 / 检测 / 分割）

### DF7 — 冻结 BN 但训练时仍在更新 running_mean/running_var

**症状**：冻结 backbone 的 BN 层后，评估时准确率持续下降；BN 的 running statistics 被小 batch 的噪声漂移。

**根因**：`model.eval()` 设置 BN 为使用 running statistics，但 `requires_grad=False` 只冻结了 γ/β 参数 — `running_mean`/`running_var` 仍在训练模式下被更新。需要显式将 BN 设为 eval 模式。

**修复**：对冻结的 BN 层调用 `bn.eval()`（或 `bn.track_running_stats = False`），使其在训练期间也使用预训练的 running statistics。不要依赖 `requires_grad=False` 来阻止 BN 更新。

### DF8 — 分类头类别数与预训练不匹配时静默加载

**症状**：微调到不同类别数时，模型不报错但准确率极低；`load_state_dict` 的 `strict=False` 或 HF 的 `ignore_mismatched_sizes=True` 静默重初始化分类头。

**根因**：分类头（`fc.weight`, `fc.bias`）的维度从 `num_pretrained_classes` 变为 `num_target_classes`，权重被随机重初始化但无警告。

**修复**：显式处理分类头替换 — 先加载 backbone 权重（`strict=True` 或精确匹配），然后手动替换分类头。检查 `load_state_dict` 返回的 `missing_keys` / `unexpected_keys` 确认只有分类头被重初始化。

### DF9 — 检测模型的 Anchor 偏差未与数据集匹配

**症状**：目标检测 loss 不收敛或收敛到高值；小目标完全漏检。

**根因**：Anchor-based 检测器（YOLO, SSD, RetinaNet）的先验框需要与数据集的 bbox 尺寸分布匹配。使用默认 Anchor（如 COCO 上的）在其他数据集（医学影像、卫星图等）上偏差很大。

**修复**：在训练集上 k-means 聚类 bbox 得到数据集特定的 Anchor 尺寸，然后设置对应的 bias 初始化。YOLO 系列通常提供 Anchor 聚类脚本。对于 Anchor-free 检测器（CenterNet, FCOS）此问题不存在。

### DF10 — 分割的 ignore_index 与数据集标签不匹配

**症状**：分割 loss 计算异常；某些类别完全无法学习；或 ignore 区域的像素仍贡献梯度。

**根因**：`ignore_index`（通常 255 或 -1）必须与数据集标注中的"忽略"像素值一致。某些数据集用 0 表示背景、用 255 表示忽略边界；另一些用 -1。如果 `ignore_index` 设错了值，要么忽略了不该忽略的像素，要么没忽略该忽略的。

**修复**：检查数据集标注的实际值范围，确认 `ignore_index` 与标注中的"忽略"值一致。在 DataLoader 的 collate 函数中统一将忽略标签映射到 `ignore_index`。

---

## 扩散（生成模型）

### DF11 — 噪声调度不匹配（训练 vs 推理 / 不同框架）

**症状**：推理生成模糊、颜色偏移、或结构错乱；训练 loss 正常但 FID 很差。

**根因**：扩散模型的噪声调度（β 序列、α 累积、时间步映射）必须训练和推理完全一致。不同框架（DDPM vs LDM vs diffusers）的默认调度不同（linear vs scaled_linear vs cosine）；混用导致噪声水平不匹配。

**修复**：保存训练时的 `noise_scheduler` 配置（β_start, β_end, β_schedule, num_train_timesteps, prediction_type），推理时加载相同配置。`diffusers` 库通过 `scheduler_config.json` 自动处理；手写实现需要手动对齐。跨框架转换时（如 LDM → diffusers），必须验证 `α_cumprod` 序列逐值匹配。

### DF12 — VAE 梯度泄漏到冻结的编码器

**症状**：训练 LoRA 微调扩散模型时显存超出预期；冻结的 VAE encoder 仍在计算梯度。

**根因**：即使 `requires_grad_(False)` 冻结了 VAE 参数，如果计算图中有从可训练部分到 VAE 输出的梯度路径，PyTorch 仍会为中间结果保留梯度。

**修复**：在 VAE encoder 输出后显式 `.detach()`：`latents = vae.encode(images).latent_dist.sample().detach()`。或者在 `torch.no_grad()` 上下文中运行 VAE 编码。推理时同理：`with torch.no_grad(): latents = vae.encode(images).latent_dist.sample()`。

### DF13 — 无分类器引导（CFG）退化：conditioning_dropout 与 guidance_scale 不匹配

**症状**：高 guidance_scale 时生成质量反而下降（过饱和、伪影）；或 CFG 完全无效（有引导和无引导输出相同）。

**根因**：CFG 的训练时需要随机丢弃条件（conditioning_dropout，通常 10%），推理时才用 guidance_scale > 1。如果训练时从未丢弃条件，模型没学过"无条件"预测，推理时 CFG 的方向引导是噪声。反之，conditioning_dropout 过高（>50%）使模型过度偏向无条件预测。

**修复**：训练时设置 `conditioning_dropout=0.1`（10% 概率将条件替换为空/unconditional embedding）。推理时 guidance_scale=7.5 是常见起点。如果训练时未使用 conditioning_dropout，推理时设 guidance_scale=1.0（等价于无 CFG）。

### DF14 — 时间步采样偏差（离散 vs 连续、偏移采样）

**症状**：模型对特定时间步范围生成质量好但对其他范围差；低噪声步骤（细节步骤）比高噪声步骤（结构步骤）效果差。

**根因**：均匀采样离散时间步 {0, 1, ..., T-1} 在连续时间域 [0, 1) 上不是均匀的。对数正态采样（偏移采样）更关注对感知质量更重要的中低噪声步骤，但需要与训练策略一致。

**修复**：训练和推理使用相同的时间步采样策略。`diffusers` 的 `OffsetNoise`（对 latent 加小偏移）改善对暗色/亮色的处理。对于高分辨率生成（如 SDXL），使用偏移采样（`shifted_noise_schedule`）对低噪声步骤更密集采样。

### DF15 — EMA 推理偏移：训练的 EMA 与非 EMA 模型不匹配

**症状**：用 EMA 权重推理时图像颜色/风格偏移；与非 EMA 权重生成的结果不一致但 EMA 版本不一定更好。

**根因**：EMA 衰减率 β 的选择影响推理质量 — 过高的 β（0.9999）使 EMA 严重滞后于最近训练进展，偏移模型的最佳状态。过低的 β（0.9）使 EMA 基本等于当前模型，失去平滑效果。

**修复**：典型值 β=0.999 对长训练有效；短微调时用 β=0.99。保存检查点时同时保存 EMA 和非 EMA 权重，推理时比较两者选择更优的。验证 EMA 效果：用同一 prompt 对比 EMA vs 非 EMA 的 FID/CLIP 分数。

---

## RL / RLHF

### DF16 — Reward 模型输出尺度与策略训练不匹配

**症状**：PPO/GRPO 训练不稳定，reward 分数震荡或发散；策略在几步后退化。

**根因**：reward 模型输出的绝对值范围可能与 PPO 的 value function 预期不匹配。如果 reward 量级远大于 value baseline（或反之），advantage 估计偏大导致策略更新过度。

**修复**：训练 reward 模型后统计其输出分布（mean, std, min, max）；在 PPO 中对 reward 做标准化（`reward = (reward - mean) / std`）或使用 reward scaling/whitening。PPO 的 `value_loss_coef` 和 `clip_range` 需要适配 reward 量级。

### DF17 — KL 惩罚崩溃（惩罚项主导 loss 或完全无效）

**症状**：策略输出退化到参考模型的复制（KL 惩罚过大），或策略偏离参考模型太远产生乱码（KL 惩罚过小）。

**根因**：KL 惩罚系数需要与 reward 量级平衡。固定系数 `β` 在训练过程中 reward 增长时会被压倒；自适应系数（如 KL controller）如果目标 KL 设定不当也会失效。

**修复**：使用自适应 KL controller（目标 KL 约为 6–10 nats 对 LLM 常见）；如果 KL 持续超标，增大 `β`；如果 KL 始终远低于目标，减小 `β`。监控 KL 散度曲线 — 应缓慢增长到目标附近稳定，而非单调递增或始终为零。

### DF18 — Value function 初始化不当导致 PPO 初期不稳定

**症状**：PPO 前几十个 update step loss 震荡剧烈；value loss 量级远大于 policy loss。

**根因**：value head 随机初始化的输出与实际 return 范围差异很大，导致初期 value loss 巨大，梯度主导整个更新。

**修复**：初始化 value head 的最后一层 bias 为训练数据的平均 return 值（或 0 如果未知）；缩小 value head 最后一层权重（`nn.init.orthogonal_(layer.weight, gain=0.01)`）。某些实现用 value loss 的 running mean 做 reward whitening 来缓解。

### DF19 — GAE λ 对方差-偏差权衡的影响

**症状**：训练震荡（高方差）或收敛到次优策略（高偏差）；调整学习率无济于事。

**根因**：GAE（广义优势估计）的 λ 控制方差-偏差权衡：λ=0 为纯 TD（低方差高偏差），λ=1 为蒙特卡洛（高方差低偏差）。不合适的 λ 使优势估计质量差。

**修复**：LLM RLHF 中常用 λ=0.95。如果训练不稳定（方差高），降低 λ（如 0.9）；如果策略保守不探索（偏差高），增大 λ（如 0.98）。γ（折扣因子）也影响 — 通常 γ=1.0 对 LLM（无折扣，完整 episode）。

### DF20 — 旧策略概率为零导致 PPO ratio 爆炸

**症状**：PPO loss 突然 NaN 或 inf；调查发现 `ratio = new_prob / old_prob` 中 `old_prob ≈ 0`。

**根因**：当旧策略对某 token 分配极低概率但新策略分配较高概率时，ratio → ∞，即使有 clip 也可能在某些实现中产生数值问题。

**修复**：在 ratio 计算中加数值稳定化：`ratio = torch.exp(new_logp - old_logp)`（对数域相减而非概率域相除），然后 `ratio = torch.clamp(ratio, 1-clip, 1+clip)`。确保 `old_logp` 和 `new_logp` 都不包含 -inf（检查 mask）。这在词汇量大或序列长时特别重要。

---

## 多模态

### DF21 — 模态间学习速率不平衡（视觉编码器 vs 语言模型）

**症状**：多模态模型微调时，视觉特征被"遗忘"（视觉问答退化）或语言生成能力下降。

**根因**：视觉编码器和语言模型的最优学习率差异可达 10–100×。统一学习率要么太大（破坏预训练语言模型），要么太小（视觉适配器学不动）。

**修复**：使用差异化学习率 — 视觉编码器 lr 小（1e-5 量级），语言模型 lr 更小（1e-6 量级），适配器/投影层 lr 大（1e-4 量级）。在 PyTorch 中通过参数组实现：`[{'params': vision_params, 'lr': 1e-5}, {'params': llm_params, 'lr': 1e-6}, {'params': adapter_params, 'lr': 1e-4}]`。

### DF22 — CLIP 温度参数被固定但应学习

**症状**：CLIP 风格的对比学习 loss 不收敛或收敛到次优；temperature 过大导致 soft label 过于平滑，过小导致梯度消失。

**根因**：CLIP 的 temperature 参数（`logit_scale`）控制 softmax 的锐度。某些实现将其固定为预训练值，但微调时数据分布变化可能需要不同的 temperature。

**修复**：将 `logit_scale` 设为可学习参数（`nn.Parameter(torch.ones([]) * math.log(1/0.07))`），并加入适当的 weight decay。CLIP 原始实现中 temperature 是可学习的。如果固定，需要手动调优 — 典型值 0.07 对应 `logit_scale ≈ 2.66`。

### DF23 — 多模态对齐投影层未被训练

**症状**：多模态模型（如 LLaVA）的视觉输入完全无效；模型只依赖语言输入，忽略图像。

**根因**：视觉-语言投影层（MLP 或 Q-Former）在微调时被意外冻结，或学习率组中遗漏了它，导致视觉特征无法映射到语言模型的嵌入空间。

**修复**：确认投影层在参数组中且学习率合理（通常与适配器同级）。检查 `requires_grad=True`。在微调脚本中显式列出投影层参数：`[p for n, p in model.named_parameters() if 'proj' in n or 'mm_proj' in n]`。验证时：输入纯噪声图像，确认输出与有意义的图像不同 — 如果相同说明视觉输入被忽略。
