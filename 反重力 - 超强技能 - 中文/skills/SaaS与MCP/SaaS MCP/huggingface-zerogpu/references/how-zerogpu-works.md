# ZeroGPU 的运行机制

ZeroGPU 上模型权重、进程与 worker 复用的概念性生命周期。在推理冷启动、为什么模块级预热无法延续到请求中、为什么返回 CUDA tensor 会让调用挂起、或为什么 `gr.State` 的变更不会跨 worker 边界保留时很有用。

关于具体数值限制（每个 Space 的并发 slot 数、按层级的队列优先级等），请参考 [ZeroGPU 文档](https://huggingface.co/docs/hub/spaces-zerogpu)——这些数值会随时间变化，且本技能刻意不收录。

## 两类进程，两种生命周期

一个 ZeroGPU Space 以 **两个独立的进程** 方式运行：

- **主 web 进程** —— 长生命周期。负责导入 `app.py`、启动 Gradio，并在 Space 的整个生命周期内保持运行。它既不占用 VRAM，在启动的 "pack" 步骤之后也不再在 RAM 中持有模型权重。
- **GPU worker 进程** —— 短生命周期。为每次 `@spaces.GPU` 请求 fork 出来（如果是热 worker 则复用）。运行任务，最终会被 ZeroGPU 调度器在另一个 Space 需要该 GPU slot 时杀掉。你的 Space 代码永远不会主动杀掉自己的 worker。

## 模块级 `.to("cuda")` 被捕获到磁盘

当 `import spaces` 处于活动状态时，模块级的 `model.to("cuda")` 会被拦截。该调用会被改写为 `to("cpu")`，因此在此刻 tensor 数据物理上仍位于主进程 RAM 中。一个"伪造的"、对外表现为 CUDA 的 tensor 会与原始的 CPU tensor 一同被注册。

在启动的 "pack" 步骤，后端通过直接 I/O（`O_DIRECT`）将这些原始的 CPU tensor 写入磁盘，然后释放对应的 RAM。pack 之后，主进程在任何地方都不再持有模型权重——数据只存在于磁盘上。

这就是为什么模块级的 `pipe(...)` / `model.generate(...)` / `model(...)` 调用不会真正在 GPU 上运行：主进程上没有附加 GPU，pack 之后也没有可计算的权重。这样的调用要么会失败，要么在那些伪造的 tensor 上悄悄回退到 CPU。

## Worker 初始化：磁盘 → pinned memory → VRAM

当一个 `@spaces.GPU` 调用到达时，调度器会把它路由给一个 worker：

1. **冷 worker** —— 从主进程 fork 出来。被 patch 过的 torch 会被反向 patch，真正的 CUDA 完成初始化，权重从磁盘 offload 目录读入 pinned 主机内存，再通过双缓冲流水线流式加载到 VRAM（本质上就是每一批的 `pin_memory().cuda(non_blocking=True)`）。这就是"冷启动"成本。
2. **热 worker（复用）** —— 调度器若报告同一 GPU slot 上有空闲的存活 worker，就会复用它。初始化被跳过；权重继续保留在前一次调用后还在 VRAM 中的状态。一次突发内后续的请求都会走这条路径。

热 worker 终会被调度器在另一个 Space 需要该 GPU slot 时杀掉。此后下一次调用又要付出 disk → VRAM 的开销。低流量的 Space 偶尔出现冷启动是正常的。

## 为什么模块级预热不起作用

一个常见的本能反应是在模块级调用 `pipe("warmup")` 来"准备"模型。这在 ZeroGPU 上不起作用：

- 在模块级，没有真实的 GPU 被附加。pack 之后伪造的 CUDA tensor 不再有数据，因此 `pipe(...)` 要么失败，要么悄悄跑在与真实 GPU 不同的东西上。
- 即便你把预热包在 `@spaces.GPU` 里，跑预热的那个 worker 最终也会在第一次真实用户请求到达之前被杀——给他们留下的依然是一个冷 worker。

正确的做法是在模块级采用急切加载（`pipe = pipeline(..., device="cuda")`），并接受一段静默期后的首次用户请求会撞上一个冷 worker。ZeroGPU 上冷启动很快，因为这得益于 pinned-memory 磁盘流水线；它不是免费的，但也不是"几分钟的模型下载"。

## 为什么返回 CUDA tensor 会让调用挂起

主进程永远没有 CUDA 上下文——它没有附加 GPU，并且其 torch 从未初始化 CUDA。当 worker 返回一个 CUDA tensor 时，在主进程中反序列化它会触发 `torch.cuda._lazy_init()`，这会尝试在主进程中初始化 CUDA。ZeroGPU 会阻断这一步，调用因此挂起。

解法纯粹在客户端：返回之前先转到 CPU（`.cpu()`、`.cpu().numpy()` 等）。参见 SKILL.md 中的"进程隔离与 Pickle"。

## 为什么 `gr.State` 不会跨边界按引用共享

Worker 进程是独立 fork 出来的，并通过 pickle 与主进程交换数据。`gr.State` 的值在每次 yield 时都会跨越这条边界，因此 `@spaces.GPU` 生成器内部的变更只在该 worker 内可见，直到被变更后的状态被显式 yield 回去。主进程每次都会拿到一份新反序列化的拷贝——`id()` 不同，就地变更也跨边界不可见。

实际影响与并行处理器相关的问题，请分别参见 SKILL.md 中的"进程隔离与 Pickle"以及 `references/concurrency.md`。
