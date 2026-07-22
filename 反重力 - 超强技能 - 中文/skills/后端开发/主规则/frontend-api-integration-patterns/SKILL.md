---
name: frontend-api-integration-patterns
description: "前端应用与后端 API 集成的生产级模式，包括竞态条件处理、请求取消、重试策略、错误标准化和 UI 状态管理。当用户要求'前端 API 集成'、'API 调用模式'、'请求取消'、'竞态条件处理'、'重试策略'时使用。"
category: frontend
risk: safe
source: community
date_added: "2026-04-23"
author: avij1109
tags:
  - frontend
  - api-integration
  - javascript
  - react
  - async
tools:
  - claude
  - cursor
  - gemini
  - codex
---

# Frontend API Integration Patterns

## 概述

本技能提供前端应用与后端 API 集成的生产级模式。

大多数前端问题不是因为 API 难以调用，而是**异步行为处理不当**——导致竞态条件、过期数据、重复请求和糟糕的用户体验。

本技能关注**正确性、韧性和用户体验**，而不仅仅是让 API 调用能跑通。

---

## 何时使用本技能

* 将前端应用（React、React Native、Vue 等）连接到后端 API
* 集成 ML/AI 端点（`/predict`、`/recommend`）
* 处理 UI 中的异步数据
* 修复过期数据、UI 闪烁或重复请求
* 设计可扩展的前端 API 层

---

## 核心模式

### 1. API 层（关注点分离）

集中 API 逻辑并标准化错误。

```js id="k1m7r2"
export class ApiError extends Error {
  constructor(message, status, payload = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
  }
}

export const apiClient = async (url, options = {}) => {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    let payload = null;
    try {
      payload = await res.json();
    } catch (_) {}

    throw new ApiError(
      payload?.message || "Request failed",
      res.status,
      payload
    );
  }

  // handle empty responses safely (e.g. 204 No Content)
  if (res.status === 204) return null;

  const text = await res.text();
  return text ? JSON.parse(text) : null;
};
```

---

### 2. 竞态安全的状态管理

防止过期响应覆盖新数据。

```js id="y7p4ha"
useEffect(() => {
  let cancelled = false;

  const load = async () => {
    try {
      setLoading(true);
      setError(null);

      const result = await getUser();

      if (!cancelled) setData(result);
    } catch (err) {
      if (!cancelled) setError(err.message);
    } finally {
      if (!cancelled) setLoading(false);
    }
  };

  load();

  return () => {
    cancelled = true;
  };
}, []);
```

> 对于非 fetch 的异步逻辑，使用取消标志。对于网络请求，优先使用 AbortController。

---

### 3. 请求取消（AbortController）

取消进行中的请求，避免内存泄漏和过期更新。

```js id="l9x2pw"
useEffect(() => {
  const controller = new AbortController();

  const load = async () => {
    try {
      const data = await getUser({ signal: controller.signal });
      setData(data);
    } catch (err) {
      if (err.name === "AbortError") return;
      setError(err.message);
    }
  };

  load();
  return () => controller.abort();
}, [userId]);
```

---

### 4. 带指数退避的重试

仅对瞬时故障（5xx 或网络错误）进行重试。

```js id="8n3zcf"
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const fetchWithBackoff = async (fn, retries = 3, delay = 300) => {
  try {
    return await fn();
  } catch (err) {
    const isAbort = err.name === "AbortError";
    const isHttpError = typeof err.status === "number";
    const isRetryable = !isAbort && (!isHttpError || err.status >= 500);

    if (retries <= 0 || !isRetryable) throw err;

    const nextDelay = delay * 2 + Math.random() * 100;
    await sleep(nextDelay);

    return fetchWithBackoff(fn, retries - 1, nextDelay);
  }
};
```

---

### 5. 防抖 API 调用

避免过多的 API 调用（例如搜索输入框）。

```js id="i2r7wq"
const useDebounce = (value, delay = 400) => {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);

  return debounced;
};
```

---

### 6. 请求去重

防止跨组件的重复 API 调用。

```js id="x8v4km"
const inFlight = new Map();

export const dedupedFetch = (key, fn) => {
  if (inFlight.has(key)) return inFlight.get(key);

  const promise = fn().finally(() => inFlight.delete(key));
  inFlight.set(key, promise);
  return promise;
};
```

---

## 示例

### 示例 1：带取消的 ML 预测

```js id="n5q2pt"
const controllerRef = useRef(null);

const handlePredict = async (input) => {
  controllerRef.current?.abort();
  controllerRef.current = new AbortController();

  try {
    const result = await fetchWithBackoff(() =>
      apiClient("/predict", {
        method: "POST",
        body: JSON.stringify({ text: input }),
        signal: controllerRef.current.signal,
      })
    );

    setOutput(result);
  } catch (err) {
    if (err.name === "AbortError") return;
    setError(err.message);
  }
};
```

---

### 示例 2：防抖搜索

```js id="w4z8yn"
const debouncedQuery = useDebounce(query, 400);

useEffect(() => {
  if (!debouncedQuery) return;

  const controller = new AbortController();

  searchAPI(debouncedQuery, { signal: controller.signal })
    .then(setResults)
    .catch((err) => {
      if (err.name !== "AbortError") {
        setError("Search failed. Please try again.");
      }
    });

  return () => controller.abort();
}, [debouncedQuery]);
```

---

### 示例 3：乐观 UI 更新

```js id="q2k9hz"
const deleteItem = async (id) => {
  const previous = items;

  setItems((curr) => curr.filter((item) => item.id !== id));

  try {
    await apiClient(`/items/${id}`, { method: "DELETE" });
  } catch (err) {
    setItems(previous);
    setError("Delete failed. Please try again.");
  }
};
```

---

## 最佳实践

* ✅ 在专用层中集中 API 逻辑
* ✅ 使用自定义错误类标准化错误
* ✅ 始终处理加载、错误和成功状态
* ✅ 使用 AbortController 进行请求取消
* ✅ 仅对瞬时故障（5xx）进行重试
* ✅ 对输入驱动的 API 使用防抖
* ✅ 对相同请求进行去重

---

## 反模式

* ❌ 重试 4xx 错误
* ❌ 没有请求取消（内存泄漏）
* ❌ 易产生竞态条件的状态更新
* ❌ 静默吞掉错误
* ❌ 对多个请求使用全局加载/错误状态
* ❌ 在组件中重复直接调用 API

---

## 常见陷阱

**问题：** UI 显示过期数据
**解决方案：** 使用取消机制或防护过期响应

**问题：** 输入时 API 调用过多
**解决方案：** 使用防抖 + 取消

**问题：** 多个组件产生重复请求
**解决方案：** 使用请求去重

**问题：** 重试时服务器过载
**解决方案：** 使用指数退避

**问题：** 组件卸载后状态更新
**解决方案：** 使用 AbortController 清理

---

## 局限性

* 这些示例使用原生 JavaScript 模式；使用 React Query、SWR、Apollo、Relay 或类似工具时，请适配到框架的数据获取库。
* 除非后端提供幂等性键或其他防重复机制，否则不要重试非幂等变更操作。
* 不要在前端代码中暴露特权 API 密钥；通过后端代理敏感请求。

---

## 其他资源

* https://developer.mozilla.org/en-US/docs/Web/API/AbortController
* https://react.dev
* https://axios-http.com

---
