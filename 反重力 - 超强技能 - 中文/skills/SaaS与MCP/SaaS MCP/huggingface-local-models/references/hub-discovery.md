# llama.cpp 的 Hugging Face URL 工作流

优先使用仅依赖 URL 的工作流。不要为了查找 GGUF 文件、选择量化方案或构建 `llama-server` 命令而必须使用 `hf` 或 API 客户端。

## 目录

- 核心 URL
- 搜索与 llama.cpp 兼容的模型
- 通过 local-app 页面获取推荐量化方案
- 通过 tree API 确认精确文件
- 构建命令
- 示例：`unsloth/Qwen3.6-35B-A3B-GGUF`
- 注意事项

## 核心 URL

```text
Search:
https://huggingface.co/models?apps=llama.cpp&sort=trending

Search with text:
https://huggingface.co/models?search=<term>&apps=llama.cpp&sort=trending

Search with size bounds:
https://huggingface.co/models?search=<term>&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending

Repo local-app view:
https://huggingface.co/<repo>?local-app=llama.cpp

Repo tree API:
https://huggingface.co/api/models/<repo>/tree/main?recursive=true

Repo file tree:
https://huggingface.co/<repo>/tree/main
```

## 1. 搜索与 llama.cpp 兼容的模型

从 `apps=llama.cpp` 的模型页面开始。

可使用：

- `search=<term>` 指定模型系列名，例如 `Qwen`、`Gemma`、`Phi` 或 `Mistral`
- 在用户有硬件限制时使用 `num_parameters=min:0,max:24B` 等参数
- 在用户希望看到当下热门仓库时使用 `sort=trending`

如果用户尚未选定模型系列，不要从随机的 GGUF 仓库入手。先搜索，再精选。

示例：https://huggingface.co/models?search=Qwen&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending

## 2. 通过 local-app 页面获取推荐量化方案

打开：

```text
https://huggingface.co/<repo>?local-app=llama.cpp
```

按顺序提取：

1. 精确的 `Use this model` 代码片段（如果以文本形式可见）
2. 从抓取的页面文本或 HTML 中提取 `Hardware compatibility` 段落：
   - 量化标签
   - 文件大小
   - 按位深分组
3. 片段中展示的额外启动参数，例如 `--jinja`

当 HF local-app 片段可见时，将其视为权威来源。

通过直接读取 URL 本身来完成此操作，而不是假设浏览器中渲染的 UI。如果抓取的页面源码未暴露 `Hardware compatibility`，请说明该段未以文本形式可见，并回退到 tree API 加上 `quantization.md` 中给出的通用建议。

## 3. 通过 tree API 确认精确文件

打开：

```text
https://huggingface.co/api/models/<repo>/tree/main?recursive=true
```

将 JSON 响应视为仓库清单的权威来源。

保留满足以下条件的条目：

- `type` 为 `file`
- `path` 以 `.gguf` 结尾

使用以下字段：

- `path`：文件名和子目录
- `size`：字节数
- 可选 `lfs.size`：确认 LFS 负载大小

将文件分为：

- 量化后的单文件检查点，例如 `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
- 投影器权重，通常为 `mmproj-*.gguf`
- BF16 分片文件，通常位于 `BF16/` 下
- 其他所有文件

除非用户要求，否则忽略：

- `README.md`
- imatrix 或校准数据 blob

仅当 API 端点失败或用户希望查看网页视图时，才将 `https://huggingface.co/<repo>/tree/main` 作为人工备用入口。

## 4. 构建命令

首选顺序：

1. 复制 local-app 页面中 HF 给出的精确片段
2. 若页面给出清晰的量化标签，使用简写形式：

```bash
llama-server -hf <repo>:<QUANT>
```

3. 若需要从 tree API 中指定某个具体文件，使用文件指定形式：

```bash
llama-server --hf-repo <repo> --hf-file <filename.gguf>
```

4. 若使用 CLI 而非服务器，则使用：

```bash
llama-cli -hf <repo>:<QUANT>
```

当仓库使用自定义标签或非标准命名而可能使 `:<QUANT>` 产生歧义时，使用文件指定形式。

## 5. 示例：`unsloth/Qwen3.6-35B-A3B-GGUF`

使用以下 URL：

```text
https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF?local-app=llama.cpp
https://huggingface.co/api/models/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main?recursive=true
https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main
```

在 local-app 页面，硬件兼容性段落可能暴露如下条目：

- `UD-IQ4_XS` - 17.7 GB
- `UD-Q4_K_S` - 20.9 GB
- `UD-Q4_K_M` - 22.1 GB
- `UD-Q5_K_M` - 26.5 GB
- `UD-Q6_K` - 29.3 GB
- `Q8_0` - 36.9 GB

通过 tree API 可以确认如下精确文件名：

- `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
- `Qwen3.6-35B-A3B-UD-Q5_K_M.gguf`
- `Qwen3.6-35B-A3B-UD-Q6_K.gguf`
- `Qwen3.6-35B-A3B-Q8_0.gguf`
- `mmproj-F16.gguf`

针对此仓库的良好最终输出：

```text
Repo: unsloth/Qwen3.6-35B-A3B-GGUF
Recommended quant from HF: UD-Q4_K_M (22.1 GB)
llama-server: llama-server --hf-repo unsloth/Qwen3.6-35B-A3B-GGUF --hf-file Qwen3.6-35B-A3B-UD-Q4_K_M.gguf
Other GGUFs:
- Qwen3.6-35B-A3B-UD-Q5_K_M.gguf - 26.5 GB
- Qwen3.6-35B-A3B-UD-Q6_K.gguf - 29.3 GB
- Qwen3.6-35B-A3B-Q8_0.gguf - 36.9 GB
Projector:
- mmproj-F16.gguf - 899 MB
```

## 注意事项

- 仓库自有的量化标签很重要。除非页面本身就改写了，否则不要将 `UD-Q4_K_M` 改写为 `Q4_K_M`。
- `mmproj` 文件是多模态模型的投影器权重，而非主语言模型检查点。
- 如果 HF 硬件兼容性面板缺失（用户未配置硬件档案，或抓取的页面源码未暴露该面板），仍可使用 tree API 加上 `quantization.md` 中的通用量化建议。
- 如果仓库中已有 GGUF，请不要直接跳转到转换工作流。