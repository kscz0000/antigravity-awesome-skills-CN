# ZeroGPU 的 duration 与 quota 检查机制

`duration` 校验与配额预检查的工作机制。在选择 `duration` 值、调试 `illegal duration` 与 `quota exceeded` 错误，以及理解为什么 60s 默认值对短任务过于悲观时很有用。

关于按层级的具体阈值（免费、Pro、Team、Enterprise 配额分钟数）、每日配额窗口长度、每日运行次数上限以及 pay-as-you-go 定价，请参考 [ZeroGPU 文档](https://huggingface.co/docs/hub/spaces-zerogpu)——这些数值会随时间变化，且本技能刻意不收录。

## `duration` 实际请求的是什么

传给 `@spaces.GPU(duration=N)` 的任何值（或未指定时的默认 60s）都会成为平台用以校验的 `requested duration`。对于 `xlarge`，请求在内部会被翻倍：

```
requested = N * 2 if size == "xlarge" else N
```

因此 `@spaces.GPU(duration=60, size="xlarge")` 在内部就是一个 120 秒的请求——无论是下面的层级上限检查还是配额预检查，都按此处理。

## 两种不同的错误模式

调度器在调用运行前可能返回两种失败消息：

| 错误 | 触发条件 | 应对方法 |
|---|---|---|
| **`ZeroGPU illegal duration`** | `requested duration > 访客层级的每次调用上限` | 降低 `duration`。登录或升级层级。**等待无效。** |
| **`ZeroGPU quota exceeded`** | `remaining quota < requested duration`，或达到每日运行次数上限 | 等待配额窗口重置。对于 Pro / Team / Enterprise，pay-as-you-go 额度可以填补超出部分。 |

`quota exceeded` 的错误文本中包含具体数字，例如：

```
You have exceeded your Pro ZeroGPU quota
(60s requested vs. 30s left). Try again in 1:23:45.
```

比较的是 **`requested` 与 `remaining`**——而不是 `actual run time` 与 `remaining`。一个 10 秒的任务如果保留默认的 60s 就会请求 60s 的配额；一旦 `remaining < 60s`，即便实际工作本可以容纳，调用也会失败。

## 为什么默认 60s 对短任务过于悲观

`spaces` 包里的 `DEFAULT_SCHEDULE_DURATION` 是 **60 秒**。因此，未装饰的 `@spaces.GPU`（或 `@spaces.GPU()` 不带 `duration=`）会请求 60s 的配额。

对于一个实际只跑 ~10 秒的任务：

- 用户的 60s 配额会被一次性预留。
- 一旦其剩余配额降到 60s 以下，Space 对他们就会失败——尽管如果请求贴近实际，他们本可以再多跑很多个 10s 的任务。
- 你的调用在队列中的排名也会低于那些声明了更小 duration 的等价调用。

解决办法是显式声明贴近现实的 duration：

```python
@spaces.GPU(duration=15)
def fast_task(...):
    ...
```

对于运行时取决于输入的工作负载，可以使用一个可调用对象（每请求估算器）：

```python
def estimate_duration(prompt, steps):
    return int(steps * 3.5)

@spaces.GPU(duration=estimate_duration)
def variable_task(prompt, steps):
    ...
```

这样既能为轻输入节省配额，又在需要时为重输入预留更多。

## 配额窗口：从首次使用起固定的 24 小时

配额窗口的 TTL 在新窗口的首次调用到达时设置，此后无条件倒数——它既不是滑动窗口，也不是按日历日重置，也不会因为后续使用而延长。一个用户在 14:00 调用一次，那么他的下一次重置时间就是次日的 14:00，与中间使用得多少无关。

关于具体层级阈值、每日运行次数上限以及 pay-as-you-go 计费费率，请参考 [ZeroGPU 文档](https://huggingface.co/docs/hub/spaces-zerogpu)。

## 队列优先级

队列是 **节点级别** 的——同一物理节点上每个 Space 的请求都会竞争该节点的 GPU slot。在排队的请求中，**声明的 `duration` 越短，排名越高**。因此，对每次请求给出紧凑的 `duration` 估算能一举两得：既节省用户配额，又能让请求在队列中提前。
