# 调试和迭代

如何廉价迭代、读取日志和 smoke-test。Dev 模式 + SSH 作为最后手段（在底部介绍）。

## 阶梯

选择最适合该变更的最便宜的更新机制。使用高一级的阶梯会浪费每个周期 30 秒到 15 分钟。

| 阶梯 | 何时 | 命令 | 成本 |
|---|---|---|---|
| 1. 热重载 | 纯 Python 编辑的 Gradio Space（SDK 6.1+），**没有新依赖** | `hf spaces hot-reload <id> -f app.py` | 数秒，无重建 |
| 2. `hf upload` | 热重载无法处理的纯代码变更（`gr.Server`、Streamlit、Docker 入口点、非 Python 文件） | `hf upload <id> . --include '<file>'` | 30–90 秒应用重启 |
| 3. 完全重建 | `requirements.txt`、`Dockerfile`、README frontmatter 或硬件变更 | `hf upload <id> . && hf spaces logs <id> --build --follow` | 1–15 分钟 |
| 4. 工厂重启 | 容器处于不一致状态（损坏的 pip 环境等） | `hf spaces restart <id> --factory-reboot` | 完整重建 + 冷启动 |

### 热重载的工作原理

`hf spaces hot-reload <id> -f app.py` 通过 `jurigged`（内置在 `spaces` 包内）就地修补正在运行的 Python 进程，然后使用热重载标记将更改提交到仓库，告诉平台跳过其通常的重启。数秒，无需重建。

清晰适用于函数体更改和新的顶级符号。**不会**重新运行模块级导入或一次性初始化 — 模型在 `app.py` 首次运行时已加载，jurigged 不会重新执行该加载。新的 pip 依赖、README frontmatter、`Dockerfile` 和硬件变更需要完全重建（第 3 级阶梯）。

独立于 dev 模式。在 CLI 中标记为实验性。需要 Gradio SDK 6.1+。

### 陷阱

- **热重载会污染工厂重启。** 仅热重载的提交留下的运行时元数据仅在热进程存活时有效。在此之上使用 `--factory-reboot` 可能会失败并显示 `fatal: could not read Username for 'https://huggingface.co'`。恢复方法：先推送任何普通的 `hf upload` 提交（甚至是一行空操作），然后重启。
- **`runtime.sha` 在重启时滞后于仓库 SHA。** `hf upload` 成功 → 仓库更新 → `hf spaces info` 仍会在 `runtime` 下报告**先前**提交的 SHA，持续数分钟，直到新容器加载。轮询 `runtime.sha`，而不仅仅是 `stage`，并且在它翻转之前不要发出另一次重启。
- **并发上传或上传时重启会冲突。** 等待一个完成。
- 对于任何依赖 Space 的 Python / torch / CUDA 环境的东西，**"让我先在本地试试"**。Space 环境是唯一重要的环境。`python3 -m py_compile app.py` 是推送前值得做的最大本地检查。

## 读取日志

```bash
hf spaces info <id> --expand runtime           # stage at a glance
hf spaces logs <id> --build --follow           # build log, live
hf spaces logs <id> --follow                   # run log, live
hf spaces logs <id> --build --tail 500         # bigger window — default is small
```

在构建日志中查找**第一个**错误，而不是最后一个。第一个之后的级联错误是噪音。

状态机（终态以**粗体**显示）：

```
BUILDING → APP_STARTING → RUNNING
                      ↘ RUNTIME_ERROR
        ↘ BUILD_ERROR
        ↘ CONFIG_ERROR
```

有关阶段特定的查找，请参见 [`known-errors.md`](known-errors.md)。

## Smoke-test 模式

Space 在通过 `gradio_client` 针对实时 URL 的调用端到端运行之前不算完成。按顺序四个步骤 — 在另一个终端中持续运行 `hf spaces logs <id> --follow`，以便任何静默回退（模型跳到不同尺寸、缺少可选依赖、dtype downgrade）都会浮出水面。

### A. 还活着吗？

```bash
hf spaces info <id> --expand runtime --format json \
  | python3 -c "import json,sys; r=json.load(sys.stdin)['runtime']; \
                print(r['stage'], r.get('hardware','?'))"
# expect: RUNNING zero-a10g
```

如果 `requested_hardware` 是 `cpu-basic` 而你期望 GPU，则你的 `--flavor` 被静默拒绝。通过 `hf spaces settings <id> --hardware zero-a10g` 修复。

### B. 启动后日志干净吗？

```bash
hf spaces logs <id> --tail 200
```

确认模型加载完成，没有 import 警告，没有"falling back to CPU" / dtype-downgrade 消息，没有平台原谅的失败健康检查。在调用 API 之前执行此操作 — 许多静默失败（加载错误模型的配置拼写错误、缺少可选依赖、出错但未使启动崩溃的一次性初始化）仅在此处可见。

### C. API 实际工作吗？

默认 — 同步的 `gr.Interface` / `gr.Blocks` / `gr.ChatInterface` / `gr.Server` `@app.api`：

```python
from gradio_client import Client, handle_file
import os

c = Client("<ns>/<name>", token=os.environ["HF_TOKEN"],
           httpx_kwargs={"timeout": 600})   # ≥ @spaces.GPU duration + 60s

print(c.view_api())                          # discover endpoints — don't guess api_name

result = c.predict(
    handle_file("test.png"),                 # file inputs need handle_file()
    "short prompt",
    api_name="/generate",                    # matches @app.api(name=...) or the function name
)
```

**流式端点**（函数使用 `yield` 或 `TextIteratorStreamer`） — `.predict()` 仅返回最终值。通过 `.submit()` 迭代块：

```python
job = c.submit("short prompt", api_name="/chat")
for chunk in job: print(chunk, end="")
# or job.result() for the final value
```

**`gr.Server` 自定义 `@app.get/post(...)` 路由**不会出现在 `view_api()` 中。使用普通 HTTP 调用它们：

```python
import httpx
r = httpx.post(f"https://<subdomain>.hf.space/your_route",
               json={...}, timeout=600,
               headers={"Authorization": f"Bearer {os.environ['HF_TOKEN']}"})
```

**OAuth-gated Spaces**（`hf_oauth: true` + `gr.LoginButton`） — 匿名 `Client` 无法进行身份验证。登录后进行交互式测试，或捕获会话令牌并通过 `httpx_kwargs={"headers": {...}}` 传递。

**MCP server 模式**（`launch(mcp_server=True)`） — 不同的协议。使用 MCP 客户端。

### D. 输出字节和日志看起来正确吗？

HTTP 200 ≠ 正确的输出。嗅探返回的文件以及调用期间发出的运行日志。

```python
head = open(path, "rb").read(16)
# b'glTF...'          → glb
# b'\x89PNG'          → png
# b'\xff\xd8'         → jpeg
# b'RIFF...WEBP'      → webp
# b'RIFF...WAVE'      → wav
# head[4:8]==b'ftyp'  → mp4
# b'ply\n'            → ply
```

对于文本：非空，并非全是 `<think>...</think>`（思维模型泄漏），长度合理。对于图像：返回的尺寸与请求的尺寸匹配（某些模型会跳到最近的预设）。

同时查看 tail 的运行日志 — 静默回退（模型快照分辨率、缺少可选依赖回退到更慢的路径、dtype downgrade）仅在此处显示。

### 不要做的事

- **不要启动 Playwright / 无头浏览器**来验证后端逻辑。Gradio UI 调用与 `gradio_client` 相同的 API — 一次 `predict` 测试两者。
- **不要构建 mock 模式 + 本地服务器测试装置**。本地绿 ≠ Space 绿。
- **不要使用完整预算输入进行 smoke-test。** 能锻炼 GPU 代码路径的最小输入 — 短提示、小图像、低步数。你在验证连线，而不是质量。

## 在 Space 上迭代，而不是本地

Space 环境是唯一重要的：Python、torch、CUDA、文件路径、环境变量、gradio 版本、`spaces` 劫持都与你笔记本电脑上的不同。

工作流：

1. 决定 SDK + 硬件。编写最小的 `app.py` / `Dockerfile` + `requirements.txt` + README frontmatter — 刚好够让入口点加载。
2. 立即推送。不要先构建 Playwright / mock 测试装置。
3. 一旦 `RUNNING`：针对真实 Space 使用 `gradio_client` 验证。那是你的测试循环。
4. 通过最便宜的阶梯迭代。

`python3 -m py_compile app.py` 是值得做的最大本地检查。

## 最后手段：dev 模式 + SSH

仅在以下情况使用：

- 失败是非确定性的（设备端断言、特定 shape 下的 OOM、竞争条件）。
- 你需要 `CUDA_LAUNCH_BLOCKING=1` 或 `gdb` 来定位 CUDA 错误。
- 你将消耗 4+ 个构建周期从外部尝试各种变体。

读取日志 + grep [`known-errors.md`](known-errors.md) + 紧凑的 `gradio_client` smoke 循环解决了绝大多数问题。Dev 模式是一把重锤。

### 先决条件

1. **PRO / Team / Enterprise 计划** — dev 模式是付费功能。
2. **在用户的 HF 个人资料上注册的 SSH 密钥。** 没有这个，SSH 会拒绝连接。如果用户还没有，他们需要：
   - 在本地生成密钥对：`ssh-keygen -t ed25519 -f ~/.ssh/hf_dev -N ''`（无密码短语可保持自动化简单；如果用户偏好可以选择其他方式）。
   - 在 https://huggingface.co/settings/keys 添加**公钥**（`~/.ssh/hf_dev.pub`）。
   - 将**私钥**（`~/.ssh/hf_dev`）保留在他们将从中 SSH 的机器上。
3. **Space 必须处于 `RUNNING` 或 `RUNTIME_ERROR`** 状态，然后 dev 模式才允许进入 — 而不是 `BUILD_ERROR`。如果处于构建错误，先推送一个干净启动的存根 `app.py`（例如 `import gradio as gr; gr.Interface(lambda: 'ok', None, 'text').launch()`），然后启用 dev 模式。

### 启用

目前还没有 `huggingface_hub` Python 包装器 — 使用 REST 端点：

```bash
curl -s -X POST \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  "https://huggingface.co/api/spaces/<ns>/<space>/dev-mode" \
  -d '{"enabled": true}'
```

### SSH 进入

```bash
ssh -i ~/.ssh/hf_dev -o BatchMode=yes -o StrictHostKeyChecking=accept-new \
    <ns>-<space>@ssh.hf.space
```

用户名是 `<namespace>-<space>` **小写**，用 `-` 替换 `/`。Space 名称中的点也变成连字符。

### 在 VM 内

它是 `/home/user/app/` 中的普通容器。你可以编辑文件、`pip install`、运行重现、交互式调用 `@spaces.GPU` 装饰的函数（它们获得真实的 GPU 窗口）。

**裸终端中的 `nvidia-smi` 会失败**，提示 `NVML: Unknown Error`。这是预期的 — ZeroGPU 仅在 `@spaces.GPU` 调用内部公开真实 GPU。不要假设 GPU 已损坏。

**`/home/user/app/` 中的编辑在**重启、睡眠或 dev-mode-disable 后**不会保留**。只有提交会保留。

### 在容器内 smoke-test 修复

在退出 dev 模式之前，验证修复在真实 GPU 窗口下确实有效：

```bash
cat > /home/user/app/_devtest.py <<'PY'
import spaces, torch
from app import predict   # or whatever your @spaces.GPU function is
print(predict(<realistic-args>))
PY
python3 _devtest.py
```

### 持久化 + 退出

从容器内部提交 + 推送（首先 `git config user.email / user.name`；HF git remote 可用）。然后禁用 dev 模式：

```bash
curl -s -X POST -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  "https://huggingface.co/api/spaces/<ns>/<space>/dev-mode" \
  -d '{"enabled": false}'
```

**Factory-reboot** 以应用推送状态（在 dev 模式下 Space 不会在提交时重建）：

```python
from huggingface_hub import HfApi
HfApi(token=HF_TOKEN).restart_space("<ns>/<space>", factory_reboot=True)
```

然后重新运行容器外的 smoke test。Dev 模式成功**不**保证重建后成功 — 不同的镜像、不同的进程树。