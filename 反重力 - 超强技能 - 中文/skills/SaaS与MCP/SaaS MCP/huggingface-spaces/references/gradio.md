# Spaces 的 Gradio

特定于在 Space 内运行 Gradio 的模式和怪癖。假设你已经熟悉 stock Gradio 组件和 `gr.Blocks` / `gr.Interface`。

有关更深入的 Gradio API 指南 — 组件、布局、事件监听器、chatbot、Gradio 5→6 迁移 — 使用专用 `huggingface-gradio` 技能。使用 `hf skills add huggingface-gradio` 安装（添加 `--claude --global` 也可同时安装到用户级的 Claude Code）。

有关 ZeroGPU 特定的装饰器 + worker 语义，参见 [`zerogpu.md`](zerogpu.md)。

## 主题和布局

- 默认主题偏好：`gr.themes.Soft()`。替代方案：无主题，或 `gr.themes.Citrus()`。选择一次，不要过度样式化。
- 对于不需要全宽的应用，使用 CSS 约束它们在 4K 显示器上可读：
  ```python
  CSS = """
  #col-container { max-width: 1100px; margin: 0 auto; }
  .dark .gradio-container { color: var(--body-text-color); }
  """
  with gr.Blocks(theme=gr.themes.Soft(), css=CSS) as demo: ...
  ```
  暗黑模式覆盖修复了重复出现的 Gradio bug，其中暗色文本继承未设置的颜色。
- 如果 Gradio 6 自己的断点与你对抗，则使用 `!important` 限制宽度 — 针对 `main`、`.gradio-container` 和内部可填充包装器，否则宽度上限但左对齐。

## 大多数 demo 收敛到的最小布局

```python
with gr.Row():
    prompt = gr.Textbox(show_label=False, placeholder="…", container=False, scale=4)
    run = gr.Button("Run", variant="primary", scale=1)
output = gr.Image(...)
with gr.Accordion("Advanced settings", open=False):
    ...
```

内联 Textbox 上的 `container=False` 删除了默认的外部边框，以获得更紧凑的外观。

## `gr.Markdown` 作为介绍

简洁。标题、一行描述、一个链接部分。不要过度解释它的工作原理 — 那是模型卡片的用途。

## `gr.Examples`

不会让人们绊倒的模式：

```python
gr.Examples(
    examples=[
        ["a cat sitting on a windowsill", 42],
        ["mountains at sunset, photorealistic", 7],
    ],
    inputs=[prompt, seed],
    outputs=output,
    fn=generate,
    cache_examples=True,
    cache_mode="lazy",
)
```

为什么是这些标志：

- `cache_examples=True` 使示例点击即时（每个访问者没有重新推理）。
- **`cache_mode="lazy"`** — 在每个示例的首次用户点击时缓存。**在 ZeroGPU 上是必需的**（Gradio 在 ZeroGPU 上的默认值已通过 `GRADIO_CACHE_MODE=lazy` 为 lazy）。Eager 会在应用启动时预运行每个示例，但 ZeroGPU 在启动时没有附加 GPU — 它会失败并耗尽创建者的每日配额。
- `cache_examples=True` 静默禁用 `run_on_click` / `run_examples_on_click`。如果你的应用依赖仅点击行为，请设置 `cache_examples=False`。

缓存键是**示例行的文件路径**，而不是内容哈希。原地重新生成资产会永远提供陈旧的缓存输出。如果替换示例文件，则提升 `cache_version` 标记或擦除 `.gradio/cached_examples/<id>/`。

热重载（第 1 级阶梯）**不会**重建缓存。`cache_version` 提升需要真正的提交 + 重启。

## 流式传输和生成器

`gr.Interface(fn=...)` 和 `.click(fn=...)` 都接受生成器函数。每个 `yield` 推送一个新值：

```python
@spaces.GPU(duration=120)
def generate(prompt):
    yield gr.update(value=None, label="Starting…")
    for k in range(num_steps):
        yield gr.update(value=preview(k), label=f"Step {k+1}/{num_steps}")
    yield gr.update(value=final, label="Done")
```

使用 `gr.update(label=...)` 进行状态叙述 — 感觉像状态行而无需单独的组件。

**注意**：`gr.Progress(track_tqdm=True)` 和 `yield` 部分输出相互冲突 — 选择一种流式机制。

## 有用的 UX 细节

- GPU 函数中的 `progress=gr.Progress(track_tqdm=True)` 提供免费的 tqdm 驱动进度条。
- 将"Randomize seed"复选框与 seed 输入配对，并写回实际使用的 seed，以便用户可以确定性地重新运行：
  ```python
  randomize = gr.Checkbox(label="Randomize seed", value=True)
  seed = gr.Number(label="Seed", value=0, precision=0)

  @spaces.GPU
  def gen(..., seed, randomize_seed):
      if randomize_seed:
          seed = random.randint(0, 2**31 - 1)
      seed = int(seed)
      yield ..., gr.update(value=seed)   # write back into the Seed input
      ...

  run.click(gen, inputs=[..., seed, randomize], outputs=[..., seed])
  ```

## 自定义 HTML 组件

Stock Gradio 组件涵盖 95% 的情况。当它们不涵盖时，`gr.HTML(...)` 允许你在不离开 Gradio Space 的情况下构建上下文相关的自定义 UI（无需切换到 Docker）。

指南：https://www.gradio.app/guides/custom-HTML-components
使用 3D 相机角度选择器的示例（这在上下文中是有意义的）：https://huggingface.co/spaces/multimodalart/qwen-image-multiple-angles-3d-camera

如果 stock 组件涵盖需求，请不要选择此选项。

## 自定义前端 — `gr.Server`

对于具有自己的 HTML/JS 的完全自定义前端，同时保持 Gradio 的队列 + GPU 调度：

```python
from gradio import Server
from fastapi.responses import HTMLResponse

app = Server(title="my-app")

@spaces.GPU(duration=60)
def _run_gpu(prompt): return inference(prompt)

@app.api(name="generate", concurrency_limit=1, time_limit=180)
def generate(prompt: str) -> str:
    return _run_gpu(prompt)        # @app.api wraps, doesn't stack with @spaces.GPU

@app.get("/", response_class=HTMLResponse)
async def homepage():
    return open("index.html").read()

demo = app                          # HF runtime expects `demo`
if __name__ == "__main__":
    demo.launch(ssr_mode=False)
```

实际提供自定义 `/` 路由所需：

```bash
hf spaces variables add <ns>/<name> --env GRADIO_SSR_MODE=false
```

`launch(ssr_mode=False)` 在 HF 上被忽略 — 必须是环境变量。

有效的 `@app.api` kwargs：`name`、`description`、`concurrency_limit`、`concurrency_id`、`queue`、`batch`、`max_batch_size`、`api_visibility`、`time_limit`、`stream_every`。

**不要在同一函数上堆叠 `@spaces.GPU` 和 `@app.api`** — 会静默破坏请求流。将它们放在单独的函数上。

**两个上限协调**：`@spaces.GPU(duration=N)` 和 `@app.api(time_limit=M)` 都适用；较低者获胜。将 `time_limit` 设置为所有模式下的最大 duration — 过低的 `time_limit` 即使 GPU duration 允许也会杀死请求。

热重载（[`debugging.md`](debugging.md) 中的第 1 级阶梯）**不**适用于 `gr.Server` — 始终使用 `hf upload` 或提交。

参考 Space：https://huggingface.co/spaces/huggingface-projects/rf-detr-realtime-webcam

## 慢启动 Gradio（大型模型 Space）

对于需要 10-20 分钟加载权重的 Space：

- 在 README frontmatter 中设置 `startup_duration_timeout: 1h`（默认 30 分钟）。
- 禁用 SSR：`hf spaces variables add <id> --env GRADIO_SSR_MODE=false`。否则 SSR 健康检查会在应用完成加载之前超时。

## 不要

- `gr.Button(text="X")` — `text=` 已被删除；使用 `gr.Button("X")`。
- `gr.Button(type="button")` — 删除该 kwarg。
- `.click(..., _js=share_js)` — 重命名为 `js=`。
- `.style(height=...)` — 在 gradio 4+ 中已删除。
- `gr.ImageMask(brush_color=...)` — kwarg 已被删除。
- 在 gradio 4.x 上 `demo.launch(mcp_server=True)` — 仅在 5+ 上有效。