# ZeroGPU 和发布

ZeroGPU 是默认的硬件目标。它是一个共享的无服务器 GPU 池：GPU 在每个请求时分配，在 `@spaces.GPU` 函数调用期间持有，然后释放。对 demo 代码形状的关键影响：

## ZeroGPU 规则

**模型在模块级别放在 `cuda` 上，而不是在 GPU 函数内懒加载。**

```python
import torch
import spaces
from diffusers import QwenImagePipeline

pipe = QwenImagePipeline.from_pretrained("Qwen/Qwen-Image", torch_dtype=torch.bfloat16)
pipe.to("cuda")
pipe.load_lora_weights("user/my-lora")

@spaces.GPU(duration=60)
def generate(prompt):
    return pipe(prompt).images[0]
```

ZeroGPU 使用一种 CUDA 仿真模式，允许 `.to("cuda")` 在 `@spaces.GPU` 函数之外的启动期间工作。模块级放置明显快于延迟放置，因为 CUDA 传输针对启动时放置进行了优化。不鼓励在 `@spaces.GPU` 内进行懒加载。

**`@spaces.GPU` 装饰器包装需要 GPU 的函数。**

默认 duration 是 60 秒。为更长的任务设置更高：`@spaces.GPU(duration=120)` 或 `@spaces.GPU(duration=300)`。如果任务可靠地完成得更快，则设置更低——更低的 duration 意味着更高的队列优先级。对于 duration 随输入变化的任务，传递一个函数：`@spaces.GPU(duration=lambda *args: ...)`。

**GPU 大小：`large`（默认，48GB VRAM）或 `xlarge`（96GB，完整 Blackwell）。** 当单个推理需要超过 48GB 时，使用 `@spaces.GPU(size="xlarge")` 指定——大型基础视频模型、高分辨率生成或重型多阶段 pipeline。`xlarge` 每秒消耗 2× 的每日配额并且排队时间更长，因此仅在 `large` 实际 OOM 时才使用它。

典型的 duration：

- 少步 T2I（4-8 步）：30-60 秒。
- 标准 T2I（20-50 步）：60-90 秒。
- I2I / 指令编辑：60-90 秒。
- 短视频（3-5 秒）：120-180 秒。
- 长视频 / 多阶段：180-300 秒。

**不要使用 `torch.compile`。** 它与 ZeroGPU 的进程模型不兼容（GPU 进程按调用 fork）。该装饰器在 ZeroGPU 之外是无操作的，因此 `pipe(...)` 在两种环境中都以未编译方式运行。

**在 GPU 函数顶部验证输入。** 在 `@spaces.GPU` 函数内引发 `gr.Error(...)` 仍会消耗一些 GPU 配额用于分配。在执行实际工作之前进行验证，或将验证移到由 UI 调用的非装饰函数中。

**在 `gr.Examples` 上使用 `cache_examples=True` 与 `cache_mode="lazy"`。** 普通的 `cache_examples=True` 在构建时运行函数，在 GPU 被分配之前，会失败。`cache_mode="lazy"` 将缓存推迟到用户首次单击每个示例时——GPU 可用，并且后续单击立即返回缓存结果。

**不要从受控路径之外初始化 CUDA。** `pipe.to("cuda")` 没问题（CUDA 仿真处理）。在模块级别直接调用 `torch.cuda.something()` 可能会破坏进程模型——如有疑问，请在 GPU 函数内执行或跳过它。

**ZeroGPU 需要 PRO/Team/Enterprise。** 免费层级用户可以创建 README 中带有 `hardware: zero-a10g` 的 Space，但它会回退到 CPU。如果用户不在支持的计划上，请提及这一点并指出两条路径：升级到 PRO（直接解锁 ZeroGPU），或申请 [community GPU grant](https://huggingface.co/docs/hub/spaces-gpus#community-gpu-grants)（通过 Space 的硬件设置请求免费的付费 GPU 硬件，需经批准）。

## HF Hub 模式

### 身份验证 — 首先检查，仅在需要时询问

不要反射性地索要 token。检查用户是否已经通过认证，并且仅在没有可用会话时提示。

```python
from huggingface_hub import HfApi, get_token

def resolve_auth():
    """Returns (token, username) or (None, None) if no usable auth."""
    cached = get_token()  # picks up HF_TOKEN env var or cached CLI login
    if not cached:
        return None, None
    try:
        info = HfApi().whoami(token=cached)
        return cached, info["name"]
    except Exception:
        return None, None  # token exists but is invalid/expired
```

决策树：

- **用户已经通过认证且 LoRA 仓库是公开的**：使用现有 token。在发布之前向用户确认用户名（"我会发布到 `{username}` — 确认？"）。
- **用户已经通过认证且 LoRA 仓库是私有的**：尝试 `api.repo_info(repo_id, token=cached)`。如果成功，现有 token 具有正确的权限——继续。如果失败（token 无法访问该仓库），索要具有更广泛访问权限的 token。
- **没有缓存的 token**：询问用户。一次询问，附上说明："我需要一个具有 **write** 权限的 Hugging Face 访问 token。在 https://huggingface.co/settings/tokens 创建一个并粘贴到这里。" 同一个 token 将重复用于发布。

在登录用户的本地环境中使用 `huggingface-cli login` 的 Hugging Face Space 上的默认流程，或在任何设置了 `HF_TOKEN` 的环境中，*不* 需要询问用户的 token。询问是后备，不是默认。

### 读取 LoRA 仓库

```python
from huggingface_hub import HfApi, ModelCard

api = HfApi(token=hf_token)  # token may be None for public repos

try:
    info = api.repo_info(repo_id)  # 401/403 → private/gated; need token
except Exception as e:
    # Handle private/gated repo case
    ...

files = api.list_repo_files(repo_id)
card = ModelCard.load(repo_id, token=hf_token)
base_model = card.data.get("base_model")
pipeline_tag = card.data.get("pipeline_tag")
readme_text = card.text
```

### 选择 LoRA 权重文件

许多 LoRA 仓库包含单个 `.safetensors` 文件，选择是微不足道的。但有些包含多个——变体（4 步 / 8 步蒸馏、FP16 与 BF16、不同 rank）、训练历史 checkpoint（`epoch-10.safetensors`、`epoch-20.safetensors`），或真正不同的方法（`lora.safetensors` + `lora_dora.safetensors`）。按此顺序选择，在第一个匹配处停止：

1. **README 推荐特定文件。** 这是最强的信号——如果作者费心命名一个文件，那就是选择。在推理片段中寻找文件名（特别是 `weight_name="..."` 参数）、在"recommended"或"best"标注中、在对变体进行排名的比较表中，或在任何类似"将 X 用于 Y"的散文中。如果 README 清楚地指向一个文件，请使用它而不询问。
2. **没有 README 推荐，并且 `pytorch_lora_weights.safetensors` 存在于仓库根目录。** 使用它。这是 diffusers 约定，也是安全的默认。
3. **都不是，但多个文件看起来像训练 checkpoint**（文件名包含 `epoch-N`、`step-N`、`checkpoint-N` 等模式，或像 `lora-1.safetensors`、`lora-2.safetensors`、`lora-3.safetensors` 的数字进度）。默认为编号最高/最新的一个，但在响应中提及选择，以便用户可以覆盖："仓库有 epoch-10、epoch-20、epoch-30；使用 epoch-30 — 如果你想要不同的，请告诉我。"
4. **否则** — 文件看起来像替代变体（`*-4steps` 与 `*-8steps`、`*-fp16` 与 `*-bf16`、`lora` 与 `lora_dora`），或名称不透明（`v2.safetensors`、`final.safetensors`、`output.safetensors`），或没有明确的"latest"。询问，附上基于文件名暗示的每个选项的一行描述。不要盲目选择——错误的选择会产生一个正在工作的 Space，它静默地使用错误的权重。

此推理发生在阶段 1。然后将所选文件名通过 `weight_name="..."` 传递给 `app.py` 中的 `load_lora_weights`。

### 在 `app.py` 中加载私有 LoRA

```python
import os
pipe.load_lora_weights("user/private-lora", token=os.environ["HF_TOKEN"])
```

### 创建和发布 Space

```python
from huggingface_hub import HfApi, SpaceHardware

api = HfApi(token=hf_token)
username = api.whoami()["name"]
repo_id = f"{username}/{space_name}"

api.create_repo(
    repo_id=repo_id,
    repo_type="space",
    space_sdk="gradio",
    space_hardware=SpaceHardware.ZERO_A10G,
    private=True,
    exist_ok=True,
)

# Set HF token as a Space secret if the LoRA or base model is private/gated
api.add_space_secret(repo_id=repo_id, key="HF_TOKEN", value=hf_token)

# Upload files
for path in ["app.py", "requirements.txt", "README.md"]:
    api.upload_file(
        path_or_fileobj=path,
        path_in_repo=path,
        repo_id=repo_id,
        repo_type="space",
    )
```

Space 在推送文件后会自动开始构建。

### `SpaceHardware.ZERO_A10G`

字符串值是 `"zero-a10g"`。这是 ZeroGPU 在 A10G 上运行时的遗留名称；实际硬件是 NVIDIA RTX Pro 6000 Blackwell，但标识符保留下来。`SpaceHardware.ZERO_A10G` 和字面量 `"zero-a10g"` 都可以使用。为了清晰起见，优先使用枚举。

如果 `create_repo` 拒绝硬件（通常是因为用户不在 PRO 上），不带 `space_hardware=` 重试，无论如何设置 README 的 `hardware: zero-a10g`，并告诉用户 Space 将运行在 CPU 上，直到他们升级到 PRO 或申请 [community GPU grant](https://huggingface.co/docs/hub/spaces-gpus#community-gpu-grants)（请求表单位于 Space 的硬件设置中）。

### 更新现有 Space

如果用户已有要更新的 Space（而不是新建），则在现有仓库上使用 `exist_ok=True` 的 `create_repo` 是无操作。`upload_file` 会覆盖。现有的 secrets 和硬件设置保留不变。不要删除并重新创建 Space — 他们会失去 stars、评论和任何自定义配置。

## 发布之后

Space URL 是 `https://huggingface.co/spaces/{repo_id}`。构建日志在 `https://huggingface.co/spaces/{repo_id}/logs/container`。运行时日志在 `https://huggingface.co/spaces/{repo_id}/logs/run`。

与用户分享 URL 时：

- 注意 Space 是私有的 — 他们需要登录才能查看。
- 注意首次构建需要几分钟时间。
- 主动提供在失败时查看日志的帮助。
- 不要添加冗长的后记 — 他们想要单击链接，而不是阅读更多文本。

**确认重新部署实际上线后再进行测试。** 仅推送 `app.py` *不会* 更改 Space 报告的 `runtime.stage` — 旧副本继续提供 "RUNNING" 服务，而新构建会交换进来，因此 `gradio_client` 测试可以静默地命中 **陈旧代码**。要确定：推送 → `api.restart_space(repo)` → 轮询直到 stage 离开并返回 RUNNING → 在启动日志（`/logs/run`）中 grep 一个唯一的 `[VERSION] …` 标记，你在模块作用域打印了 → 然后测试。还要设置 `demo.launch(show_error=True)`，以便 `gradio_client` 显示真实的 traceback 而不是通用的 `AppError`。

## 发布时失败（构建开始之前）

这些发生在 `create_repo` 或 `upload_file` 期间，*在* Space 构建管道运行之前。通过阅读异常进行诊断，而不是容器日志（容器尚未启动）。

- **`HfHubHTTPError: 400 Bad Request` 来自 `https://huggingface.co/api/validate-yaml`。** README 的 YAML frontmatter 未能通过服务器端验证。最常见的原因是 `short_description` 超过服务器的长度上限（上限没有文档记录并且可能更改；目标约 60 个字符让你远离问题）。其他原因包括字段名拼写错误（`hardware` 与 `hardwre`）、`colorFrom`/`colorTo` 中的颜色值无效、未识别的 `hardware` 字符串或格式错误的 `models:` 列表。修复：打开 `README.md`，缩短 `short_description`，仔细检查其他 YAML 字段，重试。如果用户为 Space 提供了长描述，请将长版本放在 YAML 下方的 README 正文中 — 这是散文的正确位置。

- **`HfHubHTTPError: 403 Forbidden` on `create_repo` with `space_hardware="zero-a10g"`。** 用户的账户无法在创建时请求 ZeroGPU（通常是因为他们不在 PRO/Team/Enterprise 上）。修复：不带 `space_hardware` 参数重试 `create_repo`；保留 `hardware: zero-a10g` 在 README YAML 中。Space 在 CPU 上创建。指出用户脱离 CPU 的两条路径：升级到 PRO（自动将 Space 提升到 ZeroGPU），或申请 [community GPU grant](https://huggingface.co/docs/hub/spaces-gpus#community-gpu-grants)（通过 Space 的硬件设置请求）。

- **`HfHubHTTPError: 401/403` on `upload_file`。** Token 缺少 write 权限。修复：向用户索要具有 write 权限的 token（或使用对该特定 Space 具有 write 权限的细粒度 token）。

- **`RepositoryNotFoundError` on `upload_file` 紧接在 `create_repo` 之后。** 竞争条件；非常罕见。修复：在 create 和 upload 之间使用小的 `time.sleep(1)`，或重试 upload。

## 常见构建失败

- **`load_lora_weights` 中的 `weight_name` 不匹配。** 仓库中的实际文件命名不同。修复：`api.list_repo_files(repo_id)` 查找真实文件名；显式传递 `weight_name=`。
- **基础模型受限，无 token。** 基础模型（例如 `black-forest-labs/FLUX.1-dev`）需要接受许可证。修复：确保用户已在 Hub 上接受许可证，并将 token 设置为 Space secret。
- **Diffusers 版本对于 pipeline 类太旧。** 基础模型在最新固定 diffusers 之后发布。修复：将 `requirements.txt` 中的 `diffusers` 更改为 `git+https://github.com/huggingface/diffusers`。
- **首次请求时 CUDA OOM。** 模型对于默认 `large` 大小可用的 48GB VRAM 来说太大。按优先顺序排列的解决方案：选择更小或量化的变体（FP8、更小的 checkpoint）；请求 `@spaces.GPU(size="xlarge")` 以获得完整的 96GB（消耗 2× 配额并且排队时间更长）；启用模型 offloading（`pipe.enable_model_cpu_offload()` — 与 ZeroGPU 的进程模型冲突，仅作为最后手段）。
- **`cache_examples=True` 失败。** ZeroGPU 上构建时 GPU 不可用。修复：添加 `cache_mode="lazy"`，以便缓存在首次用户点击时发生，而不是在构建时。
- **免费层级用户，硬件未分配。** Space 回退到 CPU。构建成功但推理慢得无法使用。修复：用户升级到 PRO，或删除 `hardware: zero-a10g` 并使用 CPU。