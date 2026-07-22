# 并发安全

Gradio 处理器在 ZeroGPU 上 **默认并行运行**。在单用户测试下能正常工作的代码，在生产中可能悄悄地损坏或泄漏数据。始终假设处理器是并发执行的。

## 不要使用可变全局状态

Per-request 或 per-user 的数据不能存放在模块级可变变量中。并发请求会互相覆盖。

```python
# BAD — concurrent requests overwrite each other
results = {}

def process(text):
    results["output"] = expensive_compute(text)  # race condition
    return results["output"]
```

```python
# GOOD — pure function, no shared mutable state
def process(text):
    return expensive_compute(text)
```

对于必须在单个用户会话内持久化的状态，请使用 `gr.State`：

```python
with gr.Blocks() as demo:
    history = gr.State(value=[])

    def add_message(msg, hist):
        hist.append(msg)
        return hist, hist

    btn.click(fn=add_message, inputs=[msg, history], outputs=[chatbot, history])
```

请注意，在 ZeroGPU 上，`gr.State` 会在每次 yield 时被 pickle 跨 worker 边界——相关影响请参见 SKILL.md 中的 "进程隔离与 Pickle"。

## 不要使用固定的输出文件路径

硬编码的输出文件名会让并发请求互相覆盖文件。这会损坏输出，更糟的是可能把一个用户的数据泄漏给另一个用户。

```python
# BAD — concurrent calls clobber the same file
def generate_image(prompt):
    image = pipe(prompt).images[0]
    image.save("output.png")
    return "output.png"
```

```python
# GOOD — unique path per invocation
import tempfile

def generate_image(prompt):
    image = pipe(prompt).images[0]
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        image.save(f.name)
        return f.name
```

同样的规则也适用于任何中间文件（音频、视频、CSV 导出）。每次调用都应生成唯一的路径。

## 只读全局是安全的

在启动时加载一次、请求期间只读的模型对象、tokenizer 和配置是安全的，也推荐采用这种做法。这是 ZeroGPU 的标准模式：在模块级加载，在 `@spaces.GPU` 处理器内读取。

```python
# SAFE — loaded once at module scope, read-only during requests
model = load_model().to("cuda")
tokenizer = load_tokenizer()

@spaces.GPU
def predict(text):
    tokens = tokenizer(text, return_tensors="pt").to("cuda")
    return model.generate(**tokens)
```

"无可变全局状态"这条规则针对的是处理器 *写入* 全局，而不包括读取。只从全局读取的处理器是并发安全的。
