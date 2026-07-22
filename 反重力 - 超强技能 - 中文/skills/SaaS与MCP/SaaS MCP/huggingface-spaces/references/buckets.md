# 使用 Buckets 的持久存储

Space 是无状态的。所有数据在重启/重建时都会被擦除。对于必须存活的状态（用户上传、生成、动态提要、日志、增长的数据库）：挂载 HF **Bucket** — 位于 `hf://buckets/<ns>/<bucket>` 的类似 S3 的对象存储。

Buckets 是付费的（按 TB 存储）。在创建之前检查 `whoami.canPay` 并与用户确认。价格 + 免费层：https://huggingface.co/storage。

完整文档：https://huggingface.co/docs/hub/storage-buckets。

## 创建 + 挂载

```bash
hf buckets create <ns>/<bucket-name>                                # --private optional
hf spaces volumes set <ns>/<space> -v hf://buckets/<ns>/<bucket-name>:/data
```

之后，对 Space 中 `/data/` 的写入是持久的。读取通过 Xet 存储后端来自 bucket。

要使 bucket 文件公开可寻址：将 bucket 保留为公共。公共 bucket 文件在 `https://huggingface.co/buckets/<ns>/<bucket>/resolve/<path>` 提供（HTTP 302 重定向到签名的 CDN URL）。Space 写入一次，公共 URL 永远有效 — 无需流式代理。

## 写持久、读快模式

对于提要样式的 Space（例如用户保存生成并浏览公共时间线的社区 jam），不要在每个请求上重新扫描磁盘。模块级磁盘扫描 → 内存列表 → 每个写入都追加到两者：

```python
import os, json, uuid
from datetime import datetime, timezone

BUCKET_ID = "<ns>/<bucket-name>"
BUCKET_URL = f"https://huggingface.co/buckets/{BUCKET_ID}/resolve"
_feed = []

def _load_feed():
    root = "/data/songs"
    if not os.path.isdir(root):
        return
    for sid in os.listdir(root):
        meta = f"{root}/{sid}/meta.json"
        if os.path.isfile(meta):
            _feed.append(json.load(open(meta)))
    _feed.sort(key=lambda s: s["created_at"], reverse=True)

_load_feed()                                       # one scan at startup

@app.api(name="save", time_limit=60)
def save(audio_bytes: bytes, title: str):
    sid = uuid.uuid4().hex[:12]
    d = f"/data/songs/{sid}"; os.makedirs(d, exist_ok=True)
    open(f"{d}/audio.wav", "wb").write(audio_bytes)
    meta = {"id": sid, "title": title,
            "url": f"{BUCKET_URL}/songs/{sid}/audio.wav",
            "created_at": datetime.now(timezone.utc).isoformat()}
    json.dump(meta, open(f"{d}/meta.json", "w"))
    _feed.insert(0, meta)                          # cache stays current — no re-scan
    return meta

@app.api(name="feed", concurrency_limit=10)
def feed(): return _feed[:50]                      # zero disk I/O
```

使用此模式的参考 Space：https://huggingface.co/spaces/victor/ace-step-jam

## 反模式：bucket 作为模型权重缓存

**不要**`snapshot_download(..., local_dir="/data/weights")` 并从那里加载检查点。Bucket I/O 速度为 S3；在 `from_pretrained` 期间从 `/data` 读取 22 GB `safetensors` 会停滞超过任何 `@spaces.GPU` duration 上限。

对于模型权重，让 HF Hub 在每次冷启动时重新下载到本地容器磁盘。使用 `HF_HUB_ENABLE_HF_TRANSFER=1`（默认在运行时设置）这是快速的 — 通常比在请求时通过 bucket I/O 流式传输相同字节快得多。

Bucket I/O 适用于偶尔的元数据读取（上面的提要模式）或保存用户信息。它**不**适合作为模型加载器在每次冷启动时流式传输千兆字节的路径。

## 缓存重定向

`/home/user/.cache` 在 ZeroGPU 上是只读的。在 `app.py` 的顶部重定向瞬态缓存，在使用它们的任何库导入之前：

```python
import os
os.environ.setdefault("HF_HOME", "/data/.cache/huggingface")   # or /tmp on non-bucket Spaces
os.environ.setdefault("HF_MODULES_CACHE", "/tmp/hf_modules")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
```

缺少重定向会在首次 matplotlib / transformers / diffusers 导入时静默失败。

## 从 Space 写入访问

Space 的 `HF_TOKEN` 密钥需要对 bucket 的写权限。通过 Space UI 中的 Settings → Secrets 设置，或 `hf spaces secrets set <id> HF_TOKEN=<token>`。

## 安全说明

公共 bucket 文件在其 resolve URL 上永远公开可访问。**不要将 PII 写入**公共 bucket。如果你需要持久但私有的存储（例如需要 HF 登录的每用户历史记录），请将 bucket 保留为私有并通过你自己 Space 的身份验证控制读取。