# Spaces 的 requirements.txt

关于固定什么、保留什么、从哪里获取 CUDA wheel 以及哪些 torch 边车会静默漂移的规则。

## 预装的内容（不要列出）

Gradio SDK 基础镜像已在每个硬件等级上预装这些 — 在 `requirements.txt` 中列出它们会导致解析失败，或者更糟糕的是让 pip 静默地将运行时移出兼容性：

| 包 | 固定规则 |
|---|---|
| `gradio` | 不要列出。由 README frontmatter 中的 `sdk_version:` 锁定；在此处的固定会被忽略或破坏。 |
| `spaces` | 不要列出。平台固定；用户固定总是失败。 |
| `huggingface_hub` | 默认不要列出。仅当旧版 `gradio<5` 导入已删除的 `HfFolder` 符号时作为变通方法固定（参见 [`known-errors.md`](known-errors.md)）。 |
| `torch` | **可固定，但仅在 `{2.8.0, 2.9.1, 2.10.0, 2.11.0}` 范围内。** 范围外的任何版本都会导致 `CONFIG_ERROR: torch version in requirements.txt is not compatible`。默认不固定（运行时预装 2.11），但在以下情况下固定是合适的：(a) 特定版本已知对你的模型有效，(b) 你正在匹配 CUDA 扩展 wheel 的 `torch2.X` 标签，或 (c) 某个依赖否则会将 torch 拖出支持集。固定 torch 时，还要将 `torchvision` / `torchaudio` 固定到匹配的 minor — 参见下面的"Torch 族边车漂移"部分。 |

## 列出什么

你实际 `import` 的所有内容，包括经常被遗忘的：

- `torchvision`、`torchaudio` — **未**预装。保持不固定；pip 针对已安装的 `torch` major.minor 进行解析。
- `accelerate` — 无论何时使用 `device_map=` 都必需。列出它也会消除 `low_cpu_mem_usage=False` 警告。
- `sentencepiece` — 大多数 LLM 分词器所必需；很少作为传递依赖。
- `einops` — `flash_attn.layers.rotary` 和许多模型仓库所必需。
- 域库：`diffusers`、`transformers`、`safetensors`、`pillow`、`numpy` 等。

如果研究仓库附带 Python 包目录（`models/`、`pipeline/` 等），只需将该目录与 Space 的其余部分一起上传 — 整个仓库根作为 `/home/user/app` 可导入。**不要**尝试从 `requirements.txt` 引用本地路径。

## 固定 torch

ZeroGPU 仅接受 `2.8.0`、`2.9.1`、`2.10.0`、`2.11.0`。默认不固定（运行时预装最新）。在该集合内固定是允许的 — 有时也是必要的：

- 特定 torch 已知对你的模型有效（数值、注意力内核可用性等）。
- 直接 URL CUDA wheel 编码了 `torch2.X` 标签（参见下面的"预构建 CUDA wheel"）— 将 torch 固定到匹配。
- 某个依赖的 `setup.py` 否则会将 torch 降级到支持集之外。

`2.8.0` 是对拒绝现代 torch 的旧要求的最安全回退。`2.10.0` / `2.11.0` 是新代码的甜点。固定 torch 时，还要将 `torchvision` / `torchaudio` 固定到匹配的 minor — 参见边车漂移部分。

当某个依赖会静默降级 torch 时（例如某些 `demucs`、`audiocraft` 的分支固定 `torchaudio<2.1`），从 `app.py` 使用 `--no-deps` 安装违规者，而不是围绕它固定 torch：

```python
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps",
                "git+https://github.com/facebookresearch/demucs"], check=True)
import spaces  # safe now — torch wasn't touched
```

将违规者的实际运行时依赖列在 `requirements.txt` 中。

## Torch 族边车漂移

`torchvision`、`torchaudio`、`torchcodec` 是针对特定 `torch` major.minor 构建的。将它们不固定地列出**通常**有效，但有两种已知的漂移模式：

- `torchaudio==2.11.0`（及更高版本）**删除了其 `Requires-Dist: torch==X.Y.Z` 行**。当 torch 固定为 2.10 时，pip 静默将 torchaudio 解析为 2.11.0，并在 ABI 不匹配上导入失败。
- `torchcodec` 在 PyPI 元数据中完全不声明 torch 依赖。

在 `pip install` 或 `uv lock --upgrade` 之后验证：

```bash
curl -s https://pypi.org/pypi/<pkg>/<version>/json \
  | python3 -c "import json,sys,re; rd=json.load(sys.stdin)['info'].get('requires_dist') or []; \
                print('\n'.join(x for x in rd if re.match(r'^torch(?![a-z])', x)) or '(no torch constraint)')"
```

当 PyPI 静默时，回退到项目的 README 兼容性表（torchcodec 的在 https://github.com/pytorch/torchcodec）。

## 预构建 CUDA wheel — Blackwell wheel 数据集

对于没有与 ZeroGPU torch / cuda / cxx11-abi 单元匹配的上游 wheel 的 CUDA 扩展包，使用规范预构建 wheel 在：

> https://huggingface.co/datasets/multimodalart/zerogpu-blackwell-wheels

Wheel 位于 `wheels/<cell>/<package>-<ver>-<tag>.whl`。当前单元：

- `pt212-cu130-cp310` — 针对 torch 2.12 / CUDA 13.0 / Python 3.10 构建。**适用于实时 ZeroGPU 运行时（torch 2.11）** 的以下所有包。
- `pt212-cu130-cp312`、`pt212-cu130-cp313` — 其他 Python 版本上的相同矩阵。
- `pt28-cu128-cp310` — 针对停留在 torch 2.8 / CUDA 12.8 的 Space 的较旧回退。

在 `requirements.txt` 中通过直接 URL 引用：

```
https://huggingface.co/datasets/multimodalart/zerogpu-blackwell-wheels/resolve/main/wheels/pt212-cu130-cp310/<wheel>
```

### 每包状态

针对实时运行时 + 以前发布运行时补丁的真实 Spaces 进行经验验证：

| 包 | Wheel | 替换 | 注意事项 |
|---|---|---|---|
| `xformers` | `xformers-0.0.34+3da0fc92.d20260528-cp39-abi3-linux_x86_64.whl` | MEA→SDPA monkey-patch 垫片；Cutlass-force 垫片 | `Requires: torch>=2.10`。自动分派在 sm_120 上选择 FA2 (`fa2F@2.5.7-pt`)。经典 Cutlass / FA3 仍然拒绝 sm_120，但自动分派现在从不选择它们。 |
| `flash_attn` | `flash_attn-2.8.3-cp310-cp310-linux_x86_64.whl` | 提交的 `flash_attn/` 存根包；`sys.modules["flash_attn"] = ...` 注入 | **仅 cp310** — 需要 README 中的 `python_version: "3.10"`。需要 `einops` 用于 `flash_attn.layers.rotary`。真实的 `flash_attn_2_cuda` 满足 xformers 的 `hasattr(flash_attn.flash_attn_interface, "flash_attn_gpu")` 探测。 |
| `pytorch3d` | `pytorch3d-0.7.9-cp310-cp310-linux_x86_64.whl` | `@spaces.GPU` 内的运行时 `pip install git+...pytorch3d.git` | 需要列出 `numpy`、`iopath`、`fvcore`。元数据中没有 torch 固定；在 torch 2.11 上干净加载。 |
| `nvdiffrast` | `nvdiffrast-0.4.0-cp310-cp310-linux_x86_64.whl` | 使用 `TORCH_CUDA_ARCH_LIST=12.0` 的运行时构建 | 需要 `numpy`。0.4.0 中的 `RasterizeGLContext` 是 `RasterizeCudaContext` 的弃用别名 — 没有无头 GL 陷阱。 |
| `diff_gaussian_rasterization` | `diff_gaussian_rasterization-0.0.0-cp310-cp310-linux_x86_64.whl` | 来自 `graphdeco-inria/diff-gaussian-rasterization.git` 的运行时构建 | **仅上游 Inria API**（返回 2 元组 `(color, radii)`）。**不**匹配 ashawkey 分支（包含 alpha+depth 的 4 元组），后者由 `ashawkey/LGM`、`dylanebert/LGM-mini` 等使用。分支需要自己的 wheel。 |
| `torchmcubes` | `torchmcubes-0.1.0-cp310-cp310-linux_x86_64.whl` | 运行时 `pip install git+...torchmcubes.git` | **仅 sm_120**（较旧 arch 没有 fatbin）。适用于 ZeroGPU / Blackwell；不可移植到专用 T4 / L4 / A10G Space。 |

### 模式

```
# requirements.txt
numpy
einops
https://huggingface.co/datasets/multimodalart/zerogpu-blackwell-wheels/resolve/main/wheels/pt212-cu130-cp310/flash_attn-2.8.3-cp310-cp310-linux_x86_64.whl
https://huggingface.co/datasets/multimodalart/zerogpu-blackwell-wheels/resolve/main/wheels/pt212-cu130-cp310/xformers-0.0.34+3da0fc92.d20260528-cp39-abi3-linux_x86_64.whl
```

```yaml
# README frontmatter — pin Python to match wheel cell
python_version: "3.10"
```

**不要**从 `@spaces.GPU` 启动时安装这些。以前的"在首次 GPU 获取时 subprocess.check_call pip install"模式现在严格比 wheel URL 差 — 冷启动更慢，吃掉 `duration` 预算，破坏可重现性，并且构建有时会超过 `@spaces.GPU(duration=1500)` 上限。

### 当你需要数据集中没有的 wheel 时

按优先顺序排列的三种选项：

1. **kernels-community** — https://huggingface.co/kernels-community 为你处理 ABI 匹配。通常是最简单的路径；无需版本固定。
2. **上游 wheel 矩阵** — 例如 flash-attention 的发布页面在 https://github.com/Dao-AILab/flash-attention/releases 提供了相当完整的 `cu12 / torch / Python` 矩阵。将 `requirements.txt` 中的 `torch==X.Y.Z` 固定为与 wheel 的 `torch2.X` 标签匹配。
3. **自己构建并在 HF Hub 上托管。** 最后手段 — 参见 [`debugging.md`](debugging.md) 了解在 wheel 正在构建时作为权宜之计的 `@spaces.GPU` 源构建模式。

## 读取 CUDA wheel 文件名

```
flash_attn-2.8.3+cu130torch2.12cxx11abiFALSE-cp310-cp310-linux_x86_64.whl
```

| 标签 | 含义 |
|---|---|
| `cu130` | CUDA major 版本（13.0） |
| `torch2.12` | wheel 针对其编译的 torch major.minor |
| `cxx11abiFALSE` | C++ stdlib ABI 选择（`TRUE` 或 `FALSE`） |
| `cp310-cp310` | CPython 版本（3.10） |

其中任何一个 ABI / 符号不匹配都会在首次导入时导致 `ImportError`。将 `torch` 固定为匹配 `torch2.X`。将 `python_version:` 设置为匹配 `cp3XX`。

## 不要固定 `xformers`

在 `requirements.txt` 中保留原样（或使用上面的预构建 URL）。Pip 选择与你已安装的 torch 匹配的 wheel。

## 不要固定 `spaces`

即使 `uv export` 产生它，也要使用 `--no-emit-package spaces` 排除它。平台始终固定自己的版本。

## 具体关于 Python 版本

固定 `python_version:` 实际上是必需的：

- ZeroGPU 官方支持 **3.10.13** 和 **3.12.12**。
- 运行时默认是 3.10。
- 固定到 `cp3XX` wheel 矩阵（例如 `cp310` flash_attn wheel）会强制匹配的 Python。

`"3.12"` 和 `"3.12.12"` 形式在 YAML 中都被接受。