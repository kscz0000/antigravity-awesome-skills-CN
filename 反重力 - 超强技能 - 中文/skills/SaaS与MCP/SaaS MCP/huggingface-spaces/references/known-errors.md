# 已知错误

在尝试自己的修复之前检查这是否是已知问题。条目按 `runtime.errorMessage`、构建日志或 Python traceback 中实际出现的子字符串作为键 — grep 此文件以查找你看到的错误。

如果你遇到了此处未列出的内容并弄清楚了修复方法，请让你的用户将其 PR 回来，以便未来的运行受益。

---

## 构建 / 配置错误

这些来自应用启动之前的 Space 构建管道。通过 `hf spaces logs <id> --build --tail 500` 读取 — 查找**第一个**错误，而不是最后一个。

### `CONFIG_ERROR: torch version in requirements.txt is not compatible with ZeroGPU`

**原因**：`requirements.txt` 将 `torch==X.Y.Z` 固定到了支持集（`2.8.0`、`2.9.1`、`2.10.0`、`2.11.0`）之外的版本。
**修复**：取消固定 torch（首选 — 运行时预装最新支持的版本），或固定到支持的值之一。

### `Cannot install … because these package versions have conflicting dependencies` / `ResolutionImpossible`

**原因**：某个依赖与 README 中 `sdk_version:` 固定的 Gradio SDK 冲突。最常见的是 `pydantic`、`uvicorn`、`huggingface_hub` 或 `jinja2` 被固定到 SDK 不再接受的旧值。
**修复**：取消固定违规者。对于 `gradio[mcp]`，`uvicorn>=0.31.1` 和 `pydantic>=2.11.10` 是必需的。

### 构建在依赖解析中挂起 > 10 分钟

**原因**：pip 在深层版本空间中回溯。
**修复**：固定冲突的传递依赖。`--build` 日志会显示是哪一个。如果预期有大量下载，则将 README frontmatter 中的 `startup_duration_timeout: 1h` 调高。

### `ModuleNotFoundError: No module named 'pkg_resources'`

**原因**：setuptools 81 删除了 `pkg_resources`；旧包的 `setup.py` 导入它。
**修复**：升级或取消固定违规者。典型的罪魁祸首：`deepspeed==0.15.x`（仅用于训练 — 通常可以安全地从推理 Spaces 中删除）、`openai-whisper==20231117`。

### `400 Bad Request` 来自 `create_repo` / `upload_file` 期间的 `/api/validate-yaml`

**原因**：README frontmatter 未通过服务器验证。最常见：`short_description` 超过（未记录的）字符上限 — 目标 ≤ 60。
**修复**：缩短 `short_description`。长描述放在 README 正文中。还要仔细检查 `colorFrom`/`colorTo` 是 `red|yellow|green|blue|indigo|purple|pink|gray` 之一。

### `403 Forbidden` 来自 `create_repo` 与 `space_hardware="zero-a10g"`

**原因**：用户未使用 PRO / Team / Enterprise，因此 API 在创建时拒绝 ZeroGPU。
**修复**：不带 `space_hardware=` 重试。让 `hardware:` 远离 README frontmatter（反正会被静默忽略）。Space 是在 CPU 上创建的；将用户指向 PRO 升级或[社区赠款](grants.md)。

### `403 Forbidden` 来自 `create_commit(..., create_pr=True)`

**原因**：上游 Space 已禁用 Discussions。
**修复**：请维护者启用 Discussions，或在有写访问权限时直接推送。

---

## 启动 / RUNTIME_ERROR

这些来自 `hf spaces logs <id> --tail 500`。

### `RuntimeError: CUDA has been initialized before importing the spaces package`

**原因**：某些东西在主进程中触发 CUDA init，发生在 `import spaces` 之前。通常是错误的导入顺序；有时是第三方库在导入时急切初始化 CUDA（例如 `numba.cuda`）。
**修复**：重新排序，使 `import spaces` 成为第一个。对于使用 numba 的栈（NeMo、RAPIDS 部分）：
```python
import os
os.environ.setdefault("NUMBA_DISABLE_CUDA", "1")
import spaces
```

### `RuntimeError: No @spaces.GPU function detected during startup`

**原因**：绑定到 `.click(fn=...)` / `.submit(...)` 的函数未被装饰。装饰内部 helper 不算 — 启动扫描仅遍历 Gradio 注册的处理器。
**修复**：装饰 Gradio 绑定的函数。如果这与另一个装饰器冲突，请显式包装：
```python
@spaces.GPU(duration=60)
def gpu_inner(...): ...
def gradio_handler(...): return gpu_inner(...)
```
（或者直接装饰 `gradio_handler`。）

### `ImportError: cannot import name 'HfFolder' from 'huggingface_hub'`

**原因**：旧 gradio（`4.44` 及类似版本）从 `huggingface_hub` 导入 `HfFolder`，该符号在最近的 hub 版本中已被删除。
**修复**：两种选项。
- 在 `requirements.txt` 中固定 `huggingface-hub==0.25.0`（使旧 gradio 保持快乐）。
- 将 README 中的 `sdk_version` 升级到 `5.x` 或 `6.x`（还会修复许多其他 API 中断）。
如果 Gradio 自定义组件锁定了 major（`gradio-image-prompter`、`gradio_litmodel3d` 等），请使用 `--no-deps` 安装它，以免其 `gradio<5.0` 需求约束。

### `ImportError: cannot import name 'is_traceable_wrapper_subclass' from 'torch.utils._python_dispatch'`

**原因**：具有 `torchaudio<2.1` / `torch<2` 的 `setup.py` 的依赖（例如 `demucs`、`audiocraft`）静默降级了 torch。构建成功，应用启动，然后 `import spaces` 在缺失的 torch 符号上死掉。
**修复**：在 `import spaces` 之前，使用 `--no-deps` 从 `app.py` 安装违规者：
```python
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps",
                "git+https://github.com/facebookresearch/demucs"], check=True)
import spaces
```
将其实际运行时依赖（demucs 的 `dora-search einops julius lameenc openunmix pyyaml tqdm`）列在 `requirements.txt` 中。

### `_pickle.UnpicklingError: Weights only load failed`

**原因**：torch 2.6 中 `torch.load` 仅权重的默认翻转为 `True`。对 numpy/object globals 进行 pickle 的旧检查点失败。
**修复**：对于受信任的上游检查点，在包导入之前进行 monkey-patch：
```python
import torch
_orig = torch.load
torch.load = lambda *a, **k: _orig(*a, **{**k, "weights_only": k.get("weights_only", False)})
```

### 卡在 `ZeroGPU init – 10.0%` 然后 60 秒超时

**原因**：某个库在父进程中调用了 `cuInit`，污染了 fork（最常见的是通过 NeMo 的 `numba.cuda`）。实际的 `@spaces.GPU` 主体从未启动。
**修复**：将 `os.environ.setdefault("NUMBA_DISABLE_CUDA", "1")` 放在 `app.py` 的第一行，在 `import spaces` 之前。

### `RUNTIME_ERROR` 紧跟在长时间 `APP_STARTING` 之后，日志稀疏

**原因**：启动超过了 `startup_duration_timeout`（默认 30 分钟）。大型模型加载通常会触发此问题。
**修复**：将 README frontmatter 中的 `startup_duration_timeout: 1h` 调高。对于 Gradio 6，还通过 `hf spaces variables add <id> --env GRADIO_SSR_MODE=false` 设置 `GRADIO_SSR_MODE=false`，以避免慢启动期间的 SSR 健康检查超时。

### `RUNNING` 但公共 URL 返回 404

**原因**：Space 是私有的。匿名 Client / 浏览器命中返回 404。
**修复**：进行身份验证。`gradio_client.Client(space, token=os.environ["HF_TOKEN"])`。关键字参数是 `token=`，而不是 `hf_token=`。

### `workload was not healthy after 30 min`

**原因**：基础设施端调度或确实无法及时完成的构建。
**修复**：通常无法在代码中解决。如果预期有大量下载，则调高 `startup_duration_timeout`；否则等待或报告。

### 退出代码 128 / containerd / 调度失败

**原因**：HF 基础设施故障。
**修复**：`hf spaces restart <id> --factory-reboot`。如果持续，稍后重试或报告。无法在代码中修复。

---

## 推理时错误

这些出现在请求运行时的 `hf spaces logs <id> --follow` 中。

### `ZeroGPU illegal duration`

**原因**：`@spaces.GPU(duration=N)` 大于访问者档位的每次调用上限。
**修复**：降低 `N`。档位上限在 [ZeroGPU docs](https://huggingface.co/docs/hub/spaces-zerogpu) 中。

### `ZeroGPU quota exceeded (X requested vs Y left)`

**原因**：访问者的剩余配额 < `requested duration`。比较方式是 `requested vs remaining`，而不是 `actual vs remaining` — 一个 10 秒的任务如果使用默认的 60 秒，只要访问者的剩余配额降至 60 秒以下就会被阻止。
**修复**：将 `duration` 降低到实际的最坏情况。对于输入相关的运行时，使用可调用估算器。

### `RuntimeError: NVML_SUCCESS == r INTERNAL ASSERT FAILED at .../CUDACachingAllocator.cpp`

**原因**：在瞬时内存峰值下的分配器碎片（高分辨率像素空间操作、大型注意力激活、SR 模型、视频 DiT）。不是干净的 OOM。
**修复**：在 `app.py` 的**最顶部**设置可扩展段，任何 torch import 之前：
```python
import os
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
import spaces
import torch
```
通常是替换降低分辨率或迁移到 `xlarge` 的单行修复。

### 首次 `@spaces.GPU` 入口调用永远挂起

**原因**：装饰的函数返回了 CUDA 张量。在主进程中对其进行 unpickle 会触发 `torch.cuda._lazy_init()`，ZeroGPU 会阻止该调用。
**修复**：在返回之前转换为 CPU：`return tensor.cpu()` 或 `.cpu().numpy()`。对于 `gr.State`，在 yield 之前清除。

### `PicklingError` 出现在调用入口

**原因**：跨 fork 边界的参数包含不可 pickle 的对象 — 文件句柄、锁、lambda、闭包或 `gr.SelectData`。
**修复**：在未装饰的薄包装中提取可 pickle 的字段，将普通值传递给 `@spaces.GPU` 函数。对于 `gr.SelectData`，在装饰器外部提取 `evt.index[0]`、`evt.index[1]` 等。

### `RecursionError` 出现在 `gr.SelectData.__getattr__` 内

**原因**：与上面相同 — `gr.SelectData` 无法在 pickle 中存活。
**修复**：同样 — 在跨边界之前提取其字段。

### `CUDA error … flash_fwd_launch_template.h: no kernel image is available for execution on the device`（或 `:188: invalid argument`）

**原因**：加载了 Flash Attention 3 内核 — 通过 `kernels-community/{flash-attn3,vllm-flash-attn3,sgl-flash-attn3}` 直接加载，或通过自动分派到 FA3 的旧 `xformers` wheel 间接加载。FA3 没有 Blackwell sm_120 构建。
**修复**：使用 `attn_implementation="sdpa"`，或使用来自 `multimodalart/zerogpu-blackwell-wheels` 的 FA2 wheel 的 `"flash_attention_2"`。对于 xformers，来自同一数据集的预构建 wheel 自动分派到 FA2 — 无需 monkey-patch。

### `NotImplementedError: sgl_flash_attn3 is only supported on sm80 and above with CUDA >= 12.3`

**原因**：`kernels-community/sgl-flash-attn3` 在运行时拒绝 sm_120，尽管错误措辞如此。与上面 FA3 条目的根本原因相同。
**修复**：相同 — SDPA 或 FA2。

### `ImportError: cannot import name 'flash_attn_varlen_func' from 'flash_attn'` / 模型坚持使用 `attn_implementation="flash_attention_2"`

**原因**：模型在模块顶部导入 flash_attn 而没有逃生通道，并且运行时未提供它。
**修复**：从 `multimodalart/zerogpu-blackwell-wheels` 安装预构建的 `flash_attn-2.8.3-cp310-cp310-linux_x86_64.whl`。需要 README 中的 `python_version: "3.10"`（wheel 仅 cp310）。真实的 `flash_attn_2_cuda` 也满足 xformers 的 `flash_attn_gpu` 探测。

对于不是硬导入的 transformers `AutoModel` 样式配置，将 `attn_implementation="flash_attention_2"` 替换为 `"sdpa"`。Torch 原生，零依赖。

### `selective_scan_cuda.so undefined symbol` / `_torchaudio.abi3.so undefined symbol`

**原因**：固定到旧 torch ABI 的直接 URL 预构建 CUDA wheel（`cu12torch2.4cxx11abiFALSE` 等）— 将在当前运行时上无法加载。
**修复**：从 `requirements.txt` 中删除 URL 固定的 wheel。使用来自 `multimodalart/zerogpu-blackwell-wheels`、kernels-community 或上游发布页面的 torch 当前 wheel。

### `TypeError: 'dict' object is not hashable` 出现在 `jinja2/utils.py:get` 内

**原因**：旧 gradio (4.44) + 现代 starlette / jinja2 缓存冲突。
**修复**：固定 `jinja2<3.2` + `starlette<0.40`（保持旧 gradio），或将 `sdk_version` 升级到 5.0 之后。

---

## Smoke-test / 客户端错误

### `Client.__init__() got an unexpected keyword argument 'hf_token'`

**原因**：较旧的 `gradio_client` API 使用 `hf_token=`；当前使用 `token=`。
**修复**：`Client(space, token=os.environ["HF_TOKEN"])`。

### `httpx.ReadTimeout` 在 `client.predict(...)` 上

**原因**：默认超时对于 GPU duration 来说太小。
**修复**：`Client(..., httpx_kwargs={"timeout": 600})`。将其设置为至少 `@spaces.GPU(duration=N)` 加上 60 秒。

### `404` 出现在看似有效的端点名称上

**原因**：流式端点（函数使用 `yield`），或不出现在 `view_api()` 中的自定义 `gr.Server` `@app.get/post` 路由。
**修复**：对于流式，使用 `client.submit(...).result()`（或迭代作业）。对于自定义路由，直接使用 `httpx.post(base_url + "/route", ...)` — 绕过 `gradio_client`。

### 结果文件看起来为空 / 尺寸错误

**原因**：HTTP 200 ≠ 正确的输出。模型跳到不同尺寸，或命中了错误的端点。
**修复**：嗅探返回文件的魔数字节（`glTF`、`\x89PNG`、`RIFF…WEBP`、`RIFF…WAVE`、`[4:8]==b"ftyp"`）并检查返回的尺寸是否与请求的匹配。

---

## 提交新条目

如果你遇到了不在本文件中的错误并弄清楚了修复方法，请让你的用户将其 PR 回来。格式：

- 一个 1 行标题，其中包含代理将 grep 的确切错误子字符串。
- **原因**：一句话关于触发了什么。
- **修复**：具体的命令或代码。如果修复需要超过 5 行的叙述，请指向另一个参考文件（例如 [`debugging.md`](debugging.md)、[`zerogpu.md`](zerogpu.md)）以获取更深入的内容。