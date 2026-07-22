---
title: 为步骤配置重试以处理瞬时故障
impact: HIGH
impactDescription: 自动重试无需手写代码即可处理瞬时故障
tags: step, retry, exponential-backoff, resilience
---

## 为步骤配置重试以处理瞬时故障

步骤失败时可以使用指数退避自动重试。这能处理网络问题等瞬时故障。

**错误（手写重试逻辑）：**

```python
@DBOS.step()
def fetch_data():
    # 手写重试逻辑容易出错
    for attempt in range(3):
        try:
            return requests.get("https://api.example.com").json()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
```

**正确（使用内置重试）：**

```python
@DBOS.step(retries_allowed=True, max_attempts=10, interval_seconds=1.0, backoff_rate=2.0)
def fetch_data():
    # 自动处理重试
    return requests.get("https://api.example.com").json()
```

重试参数：
- `retries_allowed`：启用自动重试（默认：False）
- `max_attempts`：最大重试次数（默认：3）
- `interval_seconds`：重试之间的初始间隔（默认：1.0）
- `backoff_rate`：指数退避的乘数（默认：2.0）

使用默认值时，重试间隔依次为：1s、2s、4s、8s、16s……

参考：[可配置重试](https://docs.dbos.dev/python/tutorials/step-tutorial#configurable-retries)
