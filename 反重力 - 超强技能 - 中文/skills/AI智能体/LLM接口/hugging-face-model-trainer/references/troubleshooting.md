# TRL 训练任务故障排除

在 Hugging Face Jobs 上使用 TRL 训练时的常见问题和解决方案。

## 训练在"Starting training..."步骤挂起

**问题：** 任务启动但在训练步骤挂起 - 从不进展，从不超时，就停在那里。

**根本原因：** 使用 `eval_strategy="steps"` 或 `eval_strategy="epoch"` 但未向 trainer 提供 `eval_dataset`。

**解决方案：**

**选项 A：提供 eval_dataset（推荐）**
```python
# 创建 train/eval 分割
dataset_split = dataset.train_test_split(test_size=0.1, seed=42)

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset_split["train"],
    eval_dataset=dataset_split["test"],  # ← 启用 eval_strategy 时必须提供
    args=SFTConfig(
        eval_strategy="steps",
        eval_steps=50,
        ...
    ),
)
```

**选项 B：禁用评估**
```python
trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,
    # 没有 eval_dataset
    args=SFTConfig(
        eval_strategy="no",  # ← 显式禁用
        ...
    ),
)
```

**预防：**
- 始终创建 train/eval 分割以便更好地监控
- 使用 `dataset.train_test_split(test_size=0.1, seed=42)`
- 查看示例脚本：`scripts/train_sft_example.py` 包含正确的 eval 设置

## 任务超时

**问题：** 任务在训练完成前终止，所有进度丢失。

**解决方案：**
- 增加 timeout 参数（如 `"timeout": "4h"`）
- 减少 `num_train_epochs` 或使用更小的数据集切片
- 使用更小的模型或启用 LoRA/PEFT 以加快训练
- 为估计时间添加 20-30% 缓冲以应对加载/保存开销

**预防：**
- 始终先进行快速演示运行以估计时间
- 使用 `scripts/estimate_cost.py` 获取时间估计
- 通过 Trackio 或日志密切监控首次运行

## 模型未保存到 Hub

**问题：** 训练完成但模型未出现在 Hub 上 - 所有工作丢失。

**检查：**
- [ ] 训练配置中设置 `push_to_hub=True`
- [ ] 指定了 `hub_model_id` 含用户名（如 `"username/model-name"`）
- [ ] 任务提交中设置 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
- [ ] 用户对目标仓库有写入权限
- [ ] Token 有写入权限（在 https://huggingface.co/settings/tokens 检查）
- [ ] 训练脚本在最后调用 `trainer.push_to_hub()`

**参阅：** `references/hub_saving.md` 了解详细的 Hub 认证故障排除

## 内存不足（OOM）

**问题：** 任务失败并显示 CUDA 内存不足错误。

**解决方案（按优先级）：**
1. **减小批次大小：** 降低 `per_device_train_batch_size`（尝试 4 → 2 → 1）
2. **增加梯度累积：** 提高 `gradient_accumulation_steps` 以保持有效批次大小
3. **禁用评估：** 移除 `eval_dataset` 和 `eval_strategy`（节省约 40% 内存，适合演示）
4. **启用 LoRA/PEFT：** 使用 `peft_config=LoraConfig(r=8, lora_alpha=16)` 仅训练适配器（较小 rank = 更少内存）
5. **使用更大的 GPU：** 从 `t4-small` → `l4x1` → `a10g-large` → `a100-large` 切换
6. **启用梯度检查点：** 在配置中设置 `gradient_checkpointing=True`（较慢但节省内存）
7. **使用更小的模型：** 尝试更小的变体（如 0.5B 而非 3B）

**内存指南：**
- T4 (16GB)：<1B 模型配合 LoRA
- A10G (24GB)：1-3B 模型配合 LoRA，<1B 全量微调
- A100 (40GB/80GB)：7B+ 模型配合 LoRA，3B 全量微调

## 参数命名问题

**问题：** `TypeError: SFTConfig.__init__() got an unexpected keyword argument 'max_seq_length'`

**原因：** TRL 配置类使用 `max_length`，而非 `max_seq_length`。

**解决方案：**
```python
# ✅ 正确 - TRL 使用 max_length
SFTConfig(max_length=512)
DPOConfig(max_length=512)

# ❌ 错误 - 这将失败
SFTConfig(max_seq_length=512)
```

**注意：**大多数 TRL 配置不需要显式 max_length - 默认值（1024）效果良好。仅在需要特定值时设置。

## 数据集格式错误

**问题：** 训练因数据集格式错误或缺少字段而失败。

**解决方案：**
1. **检查格式文档：**
   ```python
   hf_doc_fetch("https://huggingface.co/docs/trl/dataset_formats")
   ```

2. **训练前验证数据集：**
   ```bash
   uv run https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py \
     --dataset <dataset-name> --split train
   ```
   或通过 hf_jobs：
   ```python
   hf_jobs("uv", {
       "script": "https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py",
       "script_args": ["--dataset", "dataset-name", "--split", "train"]
   })
   ```

3. **验证字段名：**
   - **SFT：** 需要 "messages" 字段（对话），或 "text" 字段，或 "prompt"/"completion"
   - **DPO：** 需要 "chosen" 和 "rejected" 字段
   - **GRPO：** 需要仅 prompt 格式

4. **检查数据集分割：**
   - 确保分割存在（如 `split="train"`）
   - 预览数据集：`load_dataset("name", split="train[:5]")`

## 导入/模块错误

**问题：** 任务失败并显示 "ModuleNotFoundError" 或导入错误。

**解决方案：**
1. **添加带依赖的 PEP 723 头部：**
   ```python
   # /// script
   # dependencies = [
   #     "trl>=0.12.0",
   #     "peft>=0.7.0",
   #     "transformers>=4.36.0",
   # ]
   # ///
   ```

2. **验证确切格式：**
   - 必须有 `# ///` 分隔符（`#` 后有空格）
   - 依赖必须是有效的 PyPI 包名称
   - 检查拼写和版本约束

3. **先在本地测试：**
   ```bash
   uv run train.py  # 测试依赖是否正确
   ```

## 认证错误

**问题：** 推送到 Hub 时任务失败，出现认证或权限错误。

**解决方案：**
1. **验证认证：**
   ```python
   mcp__huggingface__hf_whoami()  # 检查谁已认证
   ```

2. **检查 token 权限：**
   - 访问 https://huggingface.co/settings/tokens
   - 确保 token 有 "write" 权限
   - Token 不能是 "read-only"

3. **验证任务中的 token：**
   ```python
   "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # 必须在任务配置中
   ```

4. **检查仓库权限：**
   - 用户必须对目标仓库有写入权限
   - 如果是组织仓库，用户必须是具有写入权限的成员
   - 仓库必须存在或用户必须有创建权限

## 任务卡住或未启动

**问题：** 任务长时间显示 "pending" 或 "starting"。

**解决方案：**
- 在 Jobs 仪表盘检查状态：https://huggingface.co/jobs
- 验证硬件可用性（某些 GPU 类型可能有队列）
- 如果某个 flavor 使用率高，尝试不同的硬件 flavor
- 检查账户计费问题（Jobs 需要付费计划）

**典型启动时间：**
- CPU 任务：10-30 秒
- GPU 任务：30-90 秒
- 如果 >3 分钟：可能排队或卡住

## 训练损失未下降

**问题：** 训练运行但损失保持不变或未改善。

**解决方案：**
1. **检查学习率：** 可能太低（尝试 2e-5 到 5e-5）或太高（尝试 1e-6）
2. **验证数据集质量：** 检查样本确保它们合理
3. **检查模型大小：** 非常小的模型可能没有任务能力
4. **增加训练步数：** 可能需要更多 epoch 或更大数据集
5. **验证数据集格式：** 错误的格式可能导致训练降级

## 日志未出现

**问题：** 无法看到训练日志或进度。

**解决方案：**
1. **等待 30-60 秒：** 初始日志可能会延迟
2. **通过 MCP 工具检查日志：**
   ```python
   hf_jobs("logs", {"job_id": "your-job-id"})
   ```
3. **使用 Trackio 进行实时监控：** 参阅 `references/trackio_guide.md`
4. **验证任务实际在运行：**
   ```python
   hf_jobs("inspect", {"job_id": "your-job-id"})
   ```

## 检查点/恢复问题

**问题：** 无法从检查点恢复或检查点未保存。

**解决方案：**
1. **启用检查点保存：**
   ```python
   SFTConfig(
       save_strategy="steps",
       save_steps=100,
       hub_strategy="every_save",  # 推送每个检查点
   )
   ```

2. **验证检查点推送到 Hub：** 检查模型仓库的检查点文件夹

3. **从检查点恢复：**
   ```python
   trainer = SFTTrainer(
       model="username/model-name",  # 可以是检查点路径
       resume_from_checkpoint="username/model-name/checkpoint-1000",
   )
   ```

## 获取帮助

如果问题持续存在：

1. **查阅 TRL 文档：**
   ```python
   hf_doc_search("your issue", product="trl")
   ```

2. **查阅 Jobs 文档：**
   ```python
   hf_doc_fetch("https://huggingface.co/docs/huggingface_hub/guides/jobs")
   ```

3. **查看相关指南：**
   - `references/hub_saving.md` - Hub 认证问题
   - `references/hardware_guide.md` - 硬件选择和规格
   - `references/training_patterns.md` - Eval 数据集要求
   - SKILL.md "处理脚本" 部分 - 脚本格式和 URL 问题

4. **在 HF 论坛提问：** https://discuss.huggingface.co/
