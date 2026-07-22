# 训练任务的可靠性原则

这些原则源自真实的生产失败和成功修复。遵循它们可以防止常见的失败模式，确保任务可靠执行。

## 原则 1：使用前始终验证

**规则：** 永远不要假设仓库、数据集或资源存在。先用工具验证。

### 它能防止的问题

- **不存在的数据集** - 数据集不存在时任务立即失败
- **名称拼写错误** - 像 "argilla-dpo-mix-7k" vs "ultrafeedback_binarized" 这样的简单错误
- **路径错误** - 旧仓库或已移动的仓库、重命名的文件
- **缺少依赖** - 未文档化的要求

### 如何应用

**提交任何任务之前：**

```python
# 验证数据集存在
dataset_search({"query": "dataset-name", "author": "author-name", "limit": 5})
hub_repo_details(["author/dataset-name"], repo_type="dataset")

# 验证模型存在
hub_repo_details(["org/model-name"], repo_type="model")

# 检查脚本/文件路径（用于基于 URL 的脚本）
# 使用前验证：https://github.com/user/repo/blob/main/script.py
```

**原本可以捕获错误的示例：**

```python
# ❌ 错误：假设数据集存在
hf_jobs("uv", {
    "script": """...""",
    "env": {"DATASET": "trl-lib/argilla-dpo-mix-7k"}  # 不存在！
})

# ✅ 正确：先验证
dataset_search({"query": "argilla dpo", "author": "trl-lib"})
# 将显示："trl-lib/ultrafeedback_binarized" 是正确的名称

hub_repo_details(["trl-lib/ultrafeedback_binarized"], repo_type="dataset")
# 在使用前确认存在
```

### 实施检查清单

- [ ] 训练前检查数据集存在
- [ ] 微调前验证基础模型存在
- [ ] GGUF 转换前确认适配器模型存在
- [ ] 提交前测试脚本 URL 是否有效
- [ ] 验证仓库中的文件路径
- [ ] 检查资源的最近更新/重命名

**时间成本：** 5-10 秒  
**节省的时间：** 数小时的失败任务时间 + 调试

---

## 原则 2：可靠性优先于性能

**规则：** 默认选择最可能成功的方案，而非理论上最快的。

### 它能防止的问题

- **硬件不兼容** - 某些 GPU 上失败的功能
- **不稳定的优化** - 加速但导致崩溃
- **复杂的配置** - 更多失败点
- **构建系统问题** - 不可靠的编译方法

### 如何应用

**选择可靠性：**

```python
# ❌ 风险高：激进的优化可能会失败
SFTConfig(
    torch_compile=True,  # 在 T4、A10G GPU 上可能失败
    optim="adamw_bnb_8bit",  # 需要特定设置
    fp16=False,  # 可能导致训练不稳定
    ...
)

# ✅ 安全：经过验证的默认值
SFTConfig(
    # torch_compile=True,  # 带注释禁用："在 H100 上启用可提速 20%"
    optim="adamw_torch",  # 标准，始终有效
    fp16=True,  # 稳定且快速
    ...
)
```

**对于构建流程：**

```python
# ❌ 不可靠：使用 make（依赖平台）
subprocess.run(["make", "-C", "/tmp/llama.cpp", "llama-quantize"], check=True)

# ✅ 可靠：使用 CMake（一致、有文档）
subprocess.run([
    "cmake", "-B", "/tmp/llama.cpp/build", "-S", "/tmp/llama.cpp",
    "-DGGML_CUDA=OFF"  # 禁用 CUDA 以获得更快、更可靠的构建
], check=True)

subprocess.run([
    "cmake", "--build", "/tmp/llama.cpp/build",
    "--target", "llama-quantize", "-j", "4"
], check=True)
```

### 真实案例

**`torch.compile` 失败：**
- 在 H100 上为"提速 20%"而添加
- **在 T4-medium 上发生致命失败**，错误信息晦涩
- 被误诊为数据集问题（浪费数小时）
- **修复：** 默认禁用，作为可选注释添加

**结果：** 可靠性 > 20% 的性能提升

### 实施检查清单

- [ ] 默认使用经过验证的标准配置
- [ ] 注释掉性能优化并附上硬件说明
- [ ] 使用稳定的构建系统（CMake > make）
- [ ] 在生产前在目标硬件上测试
- [ ] 记录已知的兼容性问题
- [ ] 在需要时提供"安全"和"快速"变体

**性能损失：** 最佳情况下 10-20%  
**可靠性提升：** 95%+ 成功率 vs 60-70%

---

## 原则 3：创建原子化、自包含的脚本

**规则：** 脚本应作为完整的、独立的单元工作。不要为了"简化"而删除部分。

### 它能防止的问题

- **缺少依赖** - 删除了"不必要"但实际需要的包
- **不完整的流程** - 跳过看似冗余的步骤
- **环境假设** - 需要预先设置的脚本
- **部分失败** - 部分工作，其他静默失败

### 如何应用

**完整的依赖规范：**

```python
# ❌ 不完整：通过删除依赖"简化"
# /// script
# dependencies = [
#     "transformers",
#     "peft",
#     "torch",
# ]
# ///

# ✅ 完整：所有依赖显式声明
# /// script
# dependencies = [
#     "transformers>=4.36.0",
#     "peft>=0.7.0",
#     "torch>=2.0.0",
#     "accelerate>=0.24.0",
#     "huggingface_hub>=0.20.0",
#     "sentencepiece>=0.1.99",  # 分词器所需
#     "protobuf>=3.20.0",        # 分词器所需
#     "numpy",
#     "gguf",
# ]
# ///
```

**完整的构建流程：**

```python
# ❌ 不完整：假设构建工具已存在
subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp.git", "/tmp/llama.cpp"])
subprocess.run(["make", "-C", "/tmp/llama.cpp", "llama-quantize"])  # 失败：无 gcc/make

# ✅ 完整：安装所有要求
subprocess.run(["apt-get", "update", "-qq"], check=True)
subprocess.run(["apt-get", "install", "-y", "-qq", "build-essential", "cmake"], check=True)
subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp.git", "/tmp/llama.cpp"])
# ... 然后构建
```

### 真实案例

**`sentencepiece` 失败：**
- 原始脚本包含它：工作正常
- "简化"版本删除它："看起来不是必需的"
- **GGUF 转换静默失败** - 分词器无法转换
- 难以调试：没有明显的错误消息
- **修复：** 恢复所有原始依赖

**结果：** 没有经过彻底测试，不要删除依赖

### 实施检查清单

- [ ] PEP 723 头部中所有依赖带版本号
- [ ] 系统包由脚本安装
- [ ] 不假设预先存在的环境
- [ ] 没有"可选"但实际必需的步骤
- [ ] 在干净环境中测试脚本
- [ ] 记录每个依赖的用途

**复杂度：** 脚本略长  
**可靠性：** 脚本每次都"能工作"

---

## 原则 4：提供清晰的错误上下文

**规则：** 当事情失败时，明确指出哪里出了问题以及如何修复。

### 如何应用

**包装 subprocess 调用：**

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
        print("警告:", result.stderr)
except subprocess.CalledProcessError as e:
    print(f"❌ 命令失败！")
    print("STDOUT:", e.stdout)
    print("STDERR:", e.stderr)
    raise
```

**验证输入：**

```python
# ❌ 不清晰：稍后失败并出现晦涩错误
model = load_model(MODEL_NAME)

# ✅ 清晰：快速失败并显示明确消息
if not MODEL_NAME:
    raise ValueError("未设置 MODEL_NAME 环境变量！")

print(f"正在加载模型: {MODEL_NAME}")
try:
    model = load_model(MODEL_NAME)
    print(f"✅ 模型加载成功")
except Exception as e:
    print(f"❌ 模型加载失败: {MODEL_NAME}")
    print(f"错误: {e}")
    print("提示：检查模型是否在 Hub 上存在")
    raise
```

### 实施检查清单

- [ ] 用 try/except 包装外部调用
- [ ] 失败时打印 stdout/stderr
- [ ] 及早验证环境变量
- [ ] 添加进度指示符（✅、❌、🔄）
- [ ] 为常见失败提供提示
- [ ] 在开始时记录配置

---

## 原则 5：在已知的良好输入上测试正常路径

**规则：** 在生产中使用新代码前，使用你知道能工作的输入进行测试。

### 如何应用

**已知良好的测试输入：**

```python
# 训练用
TEST_DATASET = "trl-lib/Capybara"  # 小型、格式良好、广泛使用
TEST_MODEL = "Qwen/Qwen2.5-0.5B"  # 小型、快速、可靠

# GGUF 转换用
TEST_ADAPTER = "evalstate/qwen-capybara-medium"  # 已知工作的模型
TEST_BASE = "Qwen/Qwen2.5-0.5B"  # 兼容的基础模型
```

**测试工作流：**

1. 先用已知良好的输入测试
2. 如果成功，再尝试生产输入
3. 如果生产失败，你就知道是输入的问题（而非代码）
4. 隔离差异

### 实施检查清单

- [ ] 维护已知良好的测试模型/数据集列表
- [ ] 先用测试输入测试新脚本
- [ ] 记录输入"良好"的原因
- [ ] 保持测试任务便宜（小型模型、短超时）
- [ ] 仅在测试成功后才进入生产

**时间成本：** 测试运行 5-10 分钟  
**节省的调试时间：** 数小时

---

## 总结：可靠性检查清单

提交任何任务之前：

### 预检
- [ ] **已验证** 所有仓库/数据集存在（hub_repo_details）
- [ ] 如果是新代码，**已用**已知良好输入测试
- [ ] **使用** 经过验证的硬件/配置
- [ ] **包含** PEP 723 头部中的所有依赖
- [ ] **已安装** 系统要求（构建工具等）
- [ ] **设置** 合适的超时（非默认 30m）
- [ ] **已配置** Hub 推送与 HF_TOKEN
- [ ] **已添加** 清晰的错误处理

### 脚本质量
- [ ] 自包含（无需外部设置）
- [ ] 列出完整依赖
- [ ] 构建工具由脚本安装
- [ ] 包含进度指示符
- [ ] 错误消息清晰
- [ ] 在开始时记录配置

### 任务配置
- [ ] 超时 > 预计运行时间 + 30% 缓冲
- [ ] 硬件适合模型大小
- [ ] secrets 包含 HF_TOKEN
- [ ] 环境变量正确设置
- [ ] 费用已估算且可接受

**遵循这些原则可将任务成功率从约 60-70% 提升到约 95%+**

---

## 当原则冲突时

有时可靠性和性能会冲突。以下是选择方法：

| 场景 | 选择 | 理由 |
|----------|--------|-----------|
| 演示/测试 | 可靠性 | 快速失败比慢速成功更糟糕 |
| 生产（首次运行）| 可靠性 | 优化前先证明有效 |
| 生产（已验证）| 性能 | 验证后可安全优化 |
| 时间紧迫 | 可靠性 | 失败比慢速运行造成更多延迟 |
| 成本敏感 | 平衡 | 用小模型测试，然后优化 |

**通用规则：** 可靠性优先，优化第二。

---

## 进一步阅读

- `troubleshooting.md` - 常见问题和修复
- `training_patterns.md` - 经过验证的训练配置
- `gguf_conversion.md` - 生产 GGUF 工作流
