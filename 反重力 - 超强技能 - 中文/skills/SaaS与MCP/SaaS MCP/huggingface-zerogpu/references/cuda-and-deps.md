# ZeroGPU 上的 CUDA 依赖

在 ZeroGPU 上安装 CUDA 相关包的详细指南。SKILL.md 给出了结论——由于 ZeroGPU 构建阶段没有 `nvcc`，wheel 是推荐路径。本文档涵盖 wheel 文件名标签解读、kernels-community 回退以及 torch 家族配套包的漂移问题。

## 当 PyPI 上没有可用 wheel 时

常见的应对办法，按优先级排序：

1. **通过直链 URL 使用预构建 wheel。** 对于 `flash-attn`，上游项目在 https://github.com/Dao-AILab/flash-attention/releases 维护了相当完整的矩阵——请优先去那里查找并固定匹配的 wheel URL。
2. **自行构建 wheel 并托管**（例如托管到一个公开的 HF Hub 仓库），适用于没有上游 wheel 匹配 Space 环境的情况。
3. **使用 kernels-community 内核**（见下文）——它会自动处理 ABI 匹配，无需版本固定。

## 解读 CUDA wheel 文件名

形如下面的 wheel 文件名

```
flash_attn-2.8.0.post2+cu12torch2.8cxx11abiFALSE-cp312-cp312-linux_x86_64.whl
```

编码了四个构建时的选择：

| Tag | 含义 |
|-----|---------|
| `cu12` | CUDA 主版本 |
| `torch2.8` | wheel 编译时所基于的 torch 主次版本 |
| `cxx11abiFALSE` | C++ 标准库 ABI 选择（`TRUE` 或 `FALSE`） |
| `cp312-cp312` | CPython 版本（3.12） |

wheel 编译出的 C-extension 一旦在安装时这些标签中任何一项发生漂移，都会在 ABI/符号不匹配时抛出 `ImportError`。

如果把 wheel URL 直接交给 pip 而不固定周围环境，pip 可能把 `torch` 解析到与该 wheel 构建目标不同的版本，Space 将在首次导入时失败。因此：

- 在 `requirements.txt` 中固定 `torch==X.Y.Z` 以匹配 wheel 的 `torch2.X` 标签。
- 在 Space frontmatter 中设置 `python_version:` 以匹配 `cp3XX` 标签。
- 对照 wheel 检查运行时的 cxx11-ABI 选项；若不确定，请尝试另一种 ABI 的 wheel。

## 在不确定时优先选择 kernels-community

如果你不确定 ZeroGPU 运行时的 torch / Python / ABI 组合，与其使用原始 wheel URL，不如优先选择 [kernels-community](https://huggingface.co/kernels-community) 内核（例如 `kernels-community/flash-attn2`）。kernels 运行时会为你处理 ABI 匹配，因此 Space 中无需任何版本固定。

## torch 家族配套包的漂移

`torchvision`、`torchaudio`、`torchcodec` 及类似配套包都基于特定的 `torch` 主次版本（以及 CUDA 主版本）构建。在 ZeroGPU 上，运行时所支持的 `torch` 列表落后于 PyPI，因此项目通常会固定一个非最新的 `torch`——而一个裸的 `uv add <side-car>` 可能悄悄解析到针对其他 `torch`/CUDA 版本的较新发布，从而出现 ABI/导入失败，即便 `uv lock` 看似成功通过。

实测到的（2026-04）情况，当 `torch==2.9.1` 被固定时：

- `torchaudio` 解析到了 `2.11.0`，该版本针对 torch 2.11 / CUDA 13。`2.11.0` 这个发布 **删除了之前每个发布都有的 `Requires-Dist: torch==X.Y.Z` 那一行**，因此 uv 看不到约束就直接选上了它。
- `torchcodec` 解析到了一个针对 torch 2.11 的发布。PyPI 上没有任何 torchcodec 发布声明 `torch` 依赖；兼容性表只存在于项目 README 中。
- `torchvision` 之所以恰好能正确解析，是因为 torchvision 仍然声明了 `Requires-Dist: torch==X.Y.Z`。哪些配套包会受影响会随时间变化——把所有 torch 家族包都视为嫌疑对象，不要只盯着这几种。

### 在 add/upgrade 时进行验证

每次 `uv add <torch-side-car>` 或 `uv lock --upgrade` 之后，请验证解析到的版本针对的 `torch` 主次版本与已固定的版本一致。由于 PyPI 元数据不总是够用，需要两步回退：

1. 查询 PyPI 上解析到版本的 `requires_dist`：
   ```bash
   curl -s https://pypi.org/pypi/<pkg>/<version>/json \
     | python3 -c "import json,sys,re; rd=json.load(sys.stdin)['info'].get('requires_dist') or []; print('\n'.join(x for x in rd if re.match(r'^torch(?![a-z])', x)) or '(no torch constraint declared)')"
   ```
   若出现且与已固定的 torch 匹配的 `torch==X.Y.Z` 行，那就是好的。若出现但与已固定的 torch 不匹配，说明该配套包是错的——请显式固定它。
2. 如果查询输出 `(no torch constraint declared)`，说明 PyPI 元数据无话可说，不应依赖。请回退到项目自己的兼容性表（GitHub README / 文档站）——例如 torchcodec 在 https://github.com/pytorch/torchcodec 维护了这样一份表。请从该表中挑选对应已固定 torch 主次版本的配套包版本，并显式固定。

### 预防性固定

在确定配套包的正确版本后，请在 `pyproject.toml` 中与 torch 一起固定，防止 uv 在之后的 `uv lock --upgrade` 中产生漂移。给定的 torch 主次版本所对应的配套包版本号每次发布都会变化；每次都要重新验证，不要照抄旧项目中的对应关系。
