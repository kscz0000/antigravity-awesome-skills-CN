# 中国网络 + 模型下载参考

在**GFW 后的任何 GPU 机器**上拉取代码、包和模型权重的通用配方 — AutoDL、矩池云、恒源云、Featurize、揽睿星舟或裸中国 SSH 实例。整个问题简化为**四个正交的环境变量开关**（镜像、缓存位置、恢复层级、代理范围）；都不需要编辑训练代码。本文件拥有 CN 特定的传输切换和停滞重试；**必需：**`huggingface-skills:hf-cli` 拥有其下层的通用 `hf download` / `hf upload` 动词。

通用陷阱（inode 上限、静默同步、符号链接缓存）在此**不**重述 — 参见 `references/gotchas_universal.md`。AutoDL 固定形式位于 `profiles/autodl.md`。

跳转：`grep -in '<keyword>' references/china-network.md`（如 `mirror`、`HF_ENDPOINT`、`hfd`、`no_proxy`、`hf_transfer`、`decision`）。

## 目录

1. 镜像表 — PyPI / conda / HuggingFace / 备用 Hub
2. 环境开关板 — 四个开关 + 导入时陷阱 + 缓存重定向
3. 可恢复下载阶梯 — 三个层级 + `hf_transfer` 注意事项
4. `no_proxy` 陷阱 — 修复一个域的代理会破坏所有其他域
5. 决策规则 + `scripts/setup-china-mirrors.sh`

---

## 1. 镜像表

交换*源*，不是工作流。相同的包名，相同的 repo ID — 只有端点变化。逐字使用；在每个 CN 平台上完全相同。

| 通道 | 设置 | 端点 |
|---|---|---|
| **PyPI** | `pip config set global.index-url <url>` 或 `pip install -i <url> pkg` | 清华 TUNA `https://pypi.tuna.tsinghua.edu.cn/simple` · 阿里云 `https://mirrors.aliyun.com/pypi/simple` · 中科大 `https://pypi.mirrors.ustc.edu.cn/simple` |
| **conda** | `~/.condarc` 中的 channels（TUNA Anaconda） | `https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main` + `.../free` + `cloud/` channels (pytorch, conda-forge) |
| **HuggingFace** | `export HF_ENDPOINT=https://hf-mirror.com` | 即插即用反向代理 — 相同 repo ID，相同 `hf download` / `from_pretrained` 调用 |
| **备用模型 Hub** | ModelScope CLI / SDK | `pip install modelscope`; `modelscope download <id>` 或 `snapshot_download(id, ...)` — 通常在国内托管相同的 Qwen / GLM / Llama 权重 |

**conda 陷阱 — 永远不要镜像 `pytorch-nightly`。** TUNA（和每个 CN Anaconda 镜像）同步稳定的 `pytorch` channel 但**不携带 `pytorch-nightly`** — 将 nightly channel 指向镜像会静默解析到过时或缺失的构建。仅从官方 channel 安装 nightly（通过真正的代理如果机器离线），只镜像稳定 channels。

来源：HF-Mirror `https://hf-mirror.com/`; TUNA PyPI `https://mirrors.tuna.tsinghua.edu.cn/help/pypi/`;
TUNA Anaconda `https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/`; ModelScope client
`https://github.com/modelscope/modelscope_hub`。

---

## 2. 环境开关板 + 导入时陷阱

以下所有内容**仅是环境变量** — 无代码编辑。在每个 shell 中导出一次（或烘焙到 `scripts/setup-china-mirrors.sh`，§5），在触及网络之前。

```bash
# --- 镜像路由 ---
export HF_ENDPOINT=https://hf-mirror.com           # 必须在任何 HF 导入之前（见下方陷阱）
# --- 缓存离开小型释放时重置的系统盘，到数据盘上 ---
export HF_HOME=/path/to/datadisk/hf                 # hub/, datasets/ 等的父目录
export HF_HUB_CACHE=/path/to/datadisk/hf/hub        # 具体的模型 blob 缓存
export MODELSCOPE_CACHE=/path/to/datadisk/modelscope
# --- 在脆弱 CN 链路上保持 hf_transfer 关闭（见 §3）---
export HF_HUB_ENABLE_HF_TRANSFER=0
```

**导入时陷阱 — `HF_ENDPOINT` 在导入时读取一次。** `huggingface_hub` / `transformers` /
`datasets` 在被**导入**的那一刻快照 `HF_ENDPOINT`。在导入*之后*设置它（或在第一个 `import transformers` 后运行的 notebook 单元格中）是无操作的 — 库已缓存了国际端点，每次下载都走慢路径。两种安全形式：

```bash
# 在命令上内联 — 解释器启动前环境已设置：
HF_ENDPOINT=https://hf-mirror.com python train.py
# 或在封装器中导出，在所有 python 调用之上：
export HF_ENDPOINT=https://hf-mirror.com   # 然后稍后：python -m src.train ...
```

**缓存重定向 — 为什么重要。** 大多数 CN 镜像搭配一个小型释放时重置系统盘和一个更大的持久数据盘。保持默认时，`~/.cache/huggingface` 落在系统盘上，要么填满它（使下载崩溃），要么在 `/root` 为临时的平台上**在重启时被擦除**。将 `HF_HOME` / `HF_HUB_CACHE` / `MODELSCOPE_CACHE` 重定向到数据盘将模型存储与检查点绑定到相同的磁盘预算纪律（原则 #5；每个 profile 中的生存矩阵）。

来源：HF-Mirror `https://hf-mirror.com/`; ModelScope client
`https://github.com/modelscope/modelscope_hub`。

---

## 3. 可恢复下载阶梯

批量权重拉取是 CN 链路上典型的不稳定步骤 — 停滞**不是**永久失败，以下每个层级在多次杀死间积累进度。按文件大小和不稳定性升级。

**层级 1 — `hf download <repo> --resume-download`（默认）。**
将部分 blob 写为 `*.incomplete`；重新运行相同命令从字节偏移恢复。最适合约 10 GB 以下的单 repo。包装在 `timeout … && break` 重试循环中，这样停滞自恢复：

```bash
#!/usr/bin/env bash
set -u
for _ in $(seq 1 20); do
  timeout 600 hf download "$REPO" --local-dir "$DIR" --resume-download && break
  echo "停滞，重试中（进度已保存）"; sleep 5
done
```

（底层动词 — `hf download --resume-download`、`hf cache verify` — 属于 **必需：**
`huggingface-skills:hf-cli`；本阶梯仅包装它们，加上 CN 镜像路由 + 停滞重试。）

**层级 2 — `hfd.sh` (aria2 多连接) 用于任何 > 10 GB 的单文件。**
`hfd.sh`（HF-Mirror 配套脚本）用每个文件多个并行连接驱动 `aria2c` — 在拥挤的晚间链路上对大型 `.safetensors` 分片明显快于单流 CLI 且更抗停滞。当一个文件超过约 10 GB 时使用它：

```bash
./hfd.sh "$REPO" --tool aria2c -x 8     # 每文件 8 个连接，重新运行时恢复
```

**层级 3 — ModelScope `snapshot_download` (HTTP-Range 恢复)。**
当模型在 ModelScope 上存在时（大多数 CN 来源的模型都有），在国内拉取 — `snapshot_download`
做每文件 HTTP-Range 恢复、带退避的每文件重试和 SHA256 验证，全部走一条从不触及 GFW 的国内路线：

```python
from modelscope import snapshot_download
snapshot_download("Org/Model", local_dir="/path/to/datadisk/model")
```

注意：ModelScope 写入普通目录且**不**填充 HF 缓存，所以
`from_pretrained("Org/Model")` 找不到它 — 将加载指向本地目录。

**`hf_transfer` 注意事项 — 在脆弱 CN 网络上保持 `HF_HUB_ENABLE_HF_TRANSFER=0`。**
`hf_transfer` 是一个 Rust 加速器，在快速稳定的链路上有帮助，但它有一个**文档化的无错误挂起**，恰好在 CN 运维遭遇的不稳定带宽条件下 — 下载卡死无进展无异常，击败上面每个重试循环。在任何 CN 机器上默认**关闭**；仅在路由被验证快速稳定后才启用。

来源：hf CLI resume `https://github.com/huggingface/huggingface_hub/issues/3580`; hf_transfer hang
`https://github.com/huggingface/hf_transfer/issues/30`; ModelScope download
`https://deepwiki.com/modelscope/modelscope/3.1-model-download-and-caching`。

---

## 4. `no_proxy` 陷阱

**本文件中最高价值的陷阱。** 一个为到达 `huggingface.co` 而添加的 Clash / VPN 代理**同时破坏了每个国内镜像** — `pip`、TUNA index、ModelScope、云内 OSS 全部被路由到海外出口节点，产生 `ProxyError` 或数分钟的停滞（原则 #7：代理加速一条路由并减慢其他路由）。

**症状** → 导出 `http_proxy`/`https_proxy` 以修复 HF 后，`pip install` 和 ModelScope 下载挂起或抛出 `ProxyError`，而 `huggingface.co` 现在正常了。
**根因** → 代理是全局的；在直连路线上很快的国内镜像现在被拖到海外再回来。
**修复** → 用 `no_proxy` 允许列表豁免每个国内主机，注意这些库的怪癖：

- **前导点域名，无 `*` 通配符。** `requests` 遵守 `no_proxy` 但**不**展开 `*` — 使用 `.modelscope.cn`（前导点匹配域和所有子域），永远不要 `*.modelscope.cn`。
- **同时设置 `no_proxy` 和 `NO_PROXY`。** 不同的库读取不同的大小写；将两者设为相同值。
- **列出 `127.0.0.1` 和 `localhost`。** 它们是不同的条目；省略任何一个会让回环调用（TensorBoard、本地 API）被代理。
- **`pip` 忽略自身连接的 `no_proxy`** — 传递 `pip install --proxy ""` 强制 pip 走直连路线，无视继承的代理环境。

```bash
# 仅在代理存在时导出此内容（见下方）：
DOMESTIC=".tuna.tsinghua.edu.cn,.aliyun.com,.aliyuncs.com,.ustc.edu.cn,.modelscope.cn,.tencentyun.com"
export no_proxy="127.0.0.1,localhost,${DOMESTIC}"
export NO_PROXY="$no_proxy"
```

**没有代理的干净机器不需要 `no_proxy`。** `no_proxy` 仅取消路由已设置的代理。在刚租用的没有导出 `http_proxy`/`https_proxy` 的机器上，添加 `no_proxy` 无效 — **仅**在导出代理的同一时间添加它（§5 的"真正海外代理"分支），并在代理取消设置时清除它。

来源：requests `no_proxy` `https://github.com/psf/requests/issues/4871`; no_proxy guide
`https://www.browserstack.com/guide/no_proxy-environment-variable`; Clash pip ProxyError
`https://github.com/clash-verge-rev/clash-verge-rev/issues/2607`。

---

## 5. 决策规则 + 交付

**按顺序选择到达权重的最便宜路线：**

1. **hf-mirror 优先** — `HF_ENDPOINT=https://hf-mirror.com`。即插即用，相同 repo ID，无需代理，无需 `no_proxy` 管理。一切的默认。
2. **ModelScope** 如果镜像上缺失模型或镜像路线不稳定 — 相同的 Qwen / GLM / Llama 权重在国内，层级 3 恢复，不穿越 GFW。
3. **`hfd.sh`** 用于任何在稳定但慢的链路上的 > 10 GB 单文件 — aria2 多连接。
4. **真正的海外代理仅当模型*仅*在 `huggingface.co` 上存在**且镜像和 ModelScope 都没有时。代理开启的那一刻，**立即应用 §4 的 `no_proxy` 块**，这样国内镜像继续工作 — 拉取完成后取消设置两者。

**永远不要**反射性地使用代理：它是最慢、最脆弱的选项，也是会破坏其他一切的选项。镜像 → 备用 hub → 多连接 → 代理，按此优先顺序。

**交付 `scripts/setup-china-mirrors.sh`** — 编排器将其 `scp` 到机器上并在首次连接时 `source`。它将 §1（PyPI + conda 镜像）、§2（四个环境开关 + 缓存重定向离开系统盘）和 §3 默认（`HF_HUB_ENABLE_HF_TRANSFER=0`）烘焙到一个幂等步骤中，§4 代理块保留为注释（仅在罕见代理分支时添加）。编写时使用 `#!/usr/bin/env bash` +
`set -u`，正斜杠路径，且**任何 `grep` 中不要未加引号的 `|`**（正则中未加引号的管道读取 stdin 并永久挂起安装）。

来源：HF-Mirror `https://hf-mirror.com/`; ModelScope `https://github.com/modelscope/modelscope_hub`。
