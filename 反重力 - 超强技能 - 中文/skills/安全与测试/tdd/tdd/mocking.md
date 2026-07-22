# 何时使用 Mock

只在**系统边界**处使用 mock：

- 外部 API（支付、邮件等）
- 数据库（有时——优先用测试库）
- 时间 / 随机性
- 文件系统（有时）

不要 mock：

- 你自己的类 / 模块
- 内部协作者
- 任何你能控制的东西

## 为易测试而设计

在系统边界处，把接口设计得易于 mock：

**1. 使用依赖注入**

把外部依赖传进来，而不是在内部创建：

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. 优先采用 SDK 风格的接口，而非通用的 fetcher**

为每一种外部操作写专门的函数，而不是用一个通用函数加条件分支：

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK 风格意味着：
- 每个 mock 只返回一种结构
- 测试准备中没有条件分支
- 更容易看出一个测试覆盖了哪些端点
- 每个端点都有类型安全
