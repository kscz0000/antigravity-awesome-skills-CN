# 好测试与坏测试

## 好测试

**集成风格**：通过真实接口测试，而非 mock 内部组件。

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特征：

- 测的是用户 / 调用方关心的行为
- 只使用公共 API
- 能扛住内部重构
- 描述 WHAT，而非 HOW
- 每个测试只做一条逻辑断言

## 坏测试

**实现细节测试**：与内部结构紧耦合。

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

危险信号：

- mock 内部协作者
- 测试私有方法
- 在调用次数 / 顺序上断言
- 没有行为变化就因重构而挂掉
- 测试名字描述的是 HOW 而非 WHAT
- 绕过接口、通过外部手段验证

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```
