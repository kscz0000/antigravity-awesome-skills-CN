# 训练任务可靠性原则

## 目录
- 原则 1：使用前务必验证
- 原则 2：可靠性优先于性能
- 原则 3：创建原子化、自包含脚本
- 原则 4：提供清晰的错误上下文
- 原则 5：用已知正确的输入测试正常路径
- 总结：可靠性检查清单（起飞前、脚本质量、任务配置）
- 原则冲突时

---

这些原则源自真实的生产故障和成功修复。遵循它们可防止常见故障模式，确保任务可靠执行。

## 原则 1：使用前务必验证

**规则：** 绝不假设仓库、数据集或资源存在。先用工具验证。

### 防止什么

- **不存在的数据集** — 数据集不存在时任务立即失败
- **名称拼写错误** — 如 "argilla-dpo-mix-7k" vs "ultrafeedback_binarized"
- **路径错误** — 旧仓库或已移动的仓库、已重命名的文件
- **缺失依赖** — 未记录的要求

### 如何应用

**提交任何任务前：**

```python
# 验证数据集存在
dataset_search({"query": "dataset-name", "author": "author-name", "limit": 5})
hub_repo_details(["author/dataset-name"], repo_type="dataset")

# 验证模型存在
hub_repo_details(["org/model-name"], repo_type="model")

# 检查脚本/文件路径（基于 URL 的脚本）
# 使用前验证：https://github.com/user/repo/blob/main/script.py
```

**能捕获错误的示例：**

```python
# ❌ 错误：假设数据集存在
hf_jobs("uv", {
    "script": """...""",
    "env": {"DATASET": "trl-lib/argilla-dpo-mix-7k"}  # 不存在！
})

# ✅ 正确：先验证
dataset_search({"query": "argilla dpo", "author": "trl-lib"})
# 会显示："trl-lib/ultrafeedback_binarized" 是正确名称

hub_repo_details(["trl-lib/ultrafeedback_binarized"], repo_type="dataset")
# 使用前确认存在
```

### 实施清单

- [ ] 训练前检查数据集存在
- [ ] 提交前验证脚本 URL 有效
- [ ] 检查资源是否有近期更新/重命名
- [ ] 检查数据集格式

**时间成本：** 5-10 秒
**节省时间：** 数小时的失败任务时间 + 调试

---

## 原则 2：可靠性优先于性能

**规则：** 默认选择最可能成功的方案，而非理论上最快的。

### 防止什么

- **硬件不兼容** — 在某些 GPU 上失败的功能
- **不稳定优化** — 导致崩溃的加速方案
- **复杂配置** — 更多故障点
- **构建系统问题** — 不可靠的编译方法

### 如何应用

**选择可靠性：**

```python
# ❌ 风险：激进优化可能失败
TrainingArguments(
    torch_compile=True,  # 在 T4、A10G GPU 上可能失败
    optim="adamw_bnb_8bit",  # 需要特定配置
    dataloader_num_workers=8,  # 小实例上可能 OOM
    ...
)

# ✅ 安全：经过验证的默认值
TrainingArguments(
    # torch_compile=True,  # 注释并备注："在 H100 上启用可获得 20% 加速"
    optim="adamw_torch",  # 标准，始终可用
    fp16=True,  # 在 T4/A10G 上稳定且快速
    dataloader_num_workers=4,  # 保守，可靠
    ...
)
```

### 真实案例

**`torch.compile` 故障：**
- 为 H100 上"20% 加速"而添加
- **在 T4-medium 上致命失败**，报错信息晦涩
- 被误诊为数据集问题（浪费数小时）
- **修复：** 默认禁用，作为可选注释添加

**结果：** 可靠性 > 20% 性能提升

### 实施清单

- [ ] 默认使用经过验证的标准配置
- [ ] 注释掉性能优化并附硬件说明
- [ ] 使用稳定的构建系统（CMake > make）
- [ ] 生产前在目标硬件上测试
- [ ] 记录已知不兼容性
- [ ] 需要时提供"安全"和"快速"两种变体

**性能损失：** 最好情况 10-20%
**可靠性收益：** 95%+ 成功率 vs 60-70%

---

## 原则 3：创建原子化、自包含脚本

**规则：** 脚本应作为完整的独立单元运行。不要为了"简化"而删除部分内容。

### 防止什么

- **缺失依赖** — 删除了"不必要"但实际需要的包
- **不完整流程** — 跳过了看似多余的步骤
- **环境假设** — 需要预设置的脚本
- **部分失败** — 某些部分正常，其他部分静默失败

### 如何应用

**完整的依赖规格：**

```python
# ❌ 不完整：通过删除依赖来"简化"
# /// script
# dependencies = [
#     "transformers",
#     "torch",
#     "datasets",
# ]
# ///

# ✅ 完整：所有依赖显式列出
# /// script
# dependencies = [
#     "transformers>=5.2.0",
#     "accelerate>=1.1.0",
#     "albumentations>=1.4.16",  # 数据增强 + bbox 处理必需
#     "timm",                     # 视觉骨干网络必需
#     "datasets>=4.0",
#     "torchmetrics",             # mAP/mAR 计算必需
#     "pycocotools",              # COCO 评估必需
#     "trackio",                  # 指标监控必需
#     "huggingface_hub",
# ]
# ///
```

### 真实案例

**`albumentations` 故障：**
- 原始脚本有它：增强和 bbox 裁剪正常工作
- "简化"版删除了它："训练不是严格需要"
- **训练在 bbox 增强时崩溃** — 没有 COCO 格式 bbox 处理的回退方案
- 难以调试：错误出现在数据加载中，而非增强设置中
- **修复：** 恢复所有原始依赖

**结果：** 未经充分测试不要删除依赖

### 实施清单

- [ ] PEP 723 头中列出所有依赖并锁定版本
- [ ] 脚本安装所有系统包
- [ ] 不假设预存在环境
- [ ] 不有"可选"但实际必需的步骤
- [ ] 在干净环境中测试脚本
- [ ] 记录每个依赖的用途

**复杂度：** 脚本稍长
**可靠性：** 脚本每次"直接能用"

---

## 原则 4：提供清晰的错误上下文

**规则：** 出错时，让问题所在和修复方法一目了然。

### 如何应用

**封装子进程调用：**

```python
# ❌ 不清晰：静默失败
subprocess.run([...], check=True, capture_output=True)

# ✅ 清晰：显示失败内容
try:
    result = subprocess.run(
        [...],
        check=True,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("Warnings:", result.stderr)
except subprocess.CalledProcessError as e:
    print(f"❌ Command failed!")
    print("STDOUT:", e.stdout)
    print("STDERR:", e.stderr)
    raise
```

**验证输入：**

```python
# ❌ 不清晰：后续才报晦涩错误
model = load_model(MODEL_NAME)

# ✅ 清晰：快速失败并给出明确信息
if not MODEL_NAME:
    raise ValueError("MODEL_NAME environment variable not set!")

print(f"Loading model: {MODEL_NAME}")
try:
    model = load_model(MODEL_NAME)
    print(f"✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load model: {MODEL_NAME}")
    print(f"Error: {e}")
    print("Hint: Check that model exists on Hub")
    raise
```

### 实施清单

- [ ] 用 try/except 封装外部调用
- [ ] 失败时打印 stdout/stderr
- [ ] 尽早验证环境变量
- [ ] 添加进度指示器（✅、❌、🔄）
- [ ] 包含常见故障的提示
- [ ] 启动时记录配置

---

## 原则 5：用已知正确的输入测试正常路径

**规则：** 在生产环境使用新代码前，用已知能工作的输入测试。

## 总结：可靠性检查清单

提交任何任务前：

### 起飞前检查
- [ ] **已验证**所有仓库/数据集存在（hub_repo_details）
- [ ] **已测试**新代码用已知正确的输入
- [ ] **正在使用**经过验证的硬件/配置
- [ ] **已包含**PEP 723 头中的所有依赖
- [ ] **已安装**系统要求（构建工具等）
- [ ] **已设置**合适的超时（非默认 30 分钟）
- [ ] **已配置**带 HF_TOKEN 的 Hub 推送（login() + hub_token）
- [ ] **已添加**清晰的错误处理

### 脚本质量
- [ ] 自包含（无需外部设置）
- [ ] 列出完整依赖
- [ ] 脚本安装构建工具
- [ ] 包含进度指示器
- [ ] 错误信息清晰
- [ ] 启动时记录配置

### 任务配置
- [ ] 超时 > 预期运行时间 + 30% 缓冲
- [ ] 硬件适合模型大小
- [ ] Secrets 包含 HF_TOKEN（语法见 SKILL.md 指令 #2）
- [ ] 脚本在 `Trainer()` 初始化前调用 `login(token=hf_token)` 并设置 `training_args.hub_token = hf_token`
- [ ] 环境变量正确设置
- [ ] 成本已估算且可接受

**遵循这些原则可将任务成功率从约 60-70% 提升到约 95%+**

---

## 原则冲突时

有时可靠性和性能冲突。选择方法：

| 场景 | 选择 | 理由 |
|------|------|------|
| 演示/测试 | 可靠性 | 快速失败比慢速成功更糟 |
| 生产（首次运行） | 可靠性 | 优化前先证明可行 |
| 生产（已验证） | 性能 | 验证后可安全优化 |
| 时间紧迫 | 可靠性 | 失败比慢运行造成更多延误 |
| 成本紧迫 | 平衡 | 用小模型测试，再优化 |

**通用规则：** 可靠性优先，性能其次。

---
