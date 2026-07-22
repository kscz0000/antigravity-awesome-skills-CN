# 测试反模式

**适用场景：** 编写或修改测试、添加 mock、或想在生产代码中添加仅测试使用的方法时，加载此参考文档。

## 概述

测试必须验证真实行为，而非 mock 行为。Mock 是隔离手段，不是被测对象。

**核心原则：** 测代码做了什么，不是 mock 做了什么。

**遵循严格的 TDD 可以防止这些反模式。**

## 铁律

```
1. 永远不要测试 mock 行为
2. 永远不要在生产类中添加仅测试使用的方法
3. 永远不要在不理解依赖关系的情况下 mock
```

## 反模式 1：测试 mock 行为

**违规写法：**
```typescript
// ❌ BAD: Testing that the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**为什么是错的：**
- 你在验证 mock 能用，不是组件能用
- mock 存在时测试通过，移除就失败
- 对真实行为毫无说明

**协作伙伴的质疑：** "我们是在测 mock 的行为吗？"

**正确写法：**
```typescript
// ✅ GOOD: Test real component or don't mock it
test('renders sidebar', () => {
  render(<Page />);  // Don't mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});

// OR if sidebar must be mocked for isolation:
// Don't assert on the mock - test Page's behavior with sidebar present
```

### 门禁函数

```
断言任何 mock 元素之前：
  问自己："我在测真实组件行为，还是在测 mock 存不存在？"

  如果在测 mock 存不存在：
    停下来 — 删掉断言或取消 mock

  改为测试真实行为
```

## 反模式 2：在生产类中添加仅测试使用的方法

**违规写法：**
```typescript
// ❌ BAD: destroy() only used in tests
class Session {
  async destroy() {  // Looks like production API!
    await this._workspaceManager?.destroyWorkspace(this.id);
    // ... cleanup
  }
}

// In tests
afterEach(() => session.destroy());
```

**为什么是错的：**
- 生产类被仅测试使用的代码污染
- 如果在生产环境误调会很危险
- 违反 YAGNI 和关注点分离原则
- 混淆了对象生命周期和实体生命周期

**正确写法：**
```typescript
// ✅ GOOD: Test utilities handle test cleanup
// Session has no destroy() - it's stateless in production

// In test-utils/
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}

// In tests
afterEach(() => cleanupSession(session));
```

### 门禁函数

```
向生产类添加任何方法之前：
  问自己："这个方法只有测试在用吗？"

  如果是：
    停下来 — 不要添加
    放到测试工具中

  问自己："这个类拥有这个资源的生命周期吗？"

  如果不是：
    停下来 — 方法放错类了
```

## 反模式 3：不理解就 mock

**违规写法：**
```typescript
// ❌ BAD: Mock breaks test logic
test('detects duplicate server', () => {
  // Mock prevents config write that test depends on!
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // Should throw - but won't!
});
```

**为什么是错的：**
- 被 mock 的方法有测试依赖的副作用（写配置）
- 为了"安全"过度 mock 破坏了实际行为
- 测试因错误原因通过，或莫名其妙失败

**正确写法：**
```typescript
// ✅ GOOD: Mock at correct level
test('detects duplicate server', () => {
  // Mock the slow part, preserve behavior test needs
  vi.mock('MCPServerManager'); // Just mock slow server startup

  await addServer(config);  // Config written
  await addServer(config);  // Duplicate detected ✓
});
```

### 门禁函数

```
mock 任何方法之前：
  停下来 — 先别 mock

  1. 问自己："真实方法有什么副作用？"
  2. 问自己："这个测试依赖这些副作用吗？"
  3. 问自己："我完全理解这个测试需要什么吗？"

  如果依赖副作用：
    在更低层级 mock（实际的慢操作/外部操作）
    或使用保留必要行为的测试替身
    不要 mock 测试依赖的高层方法

  如果不确定测试依赖什么：
    先用真实实现跑一遍测试
    观察实际需要发生什么
    然后在正确的层级添加最小 mock

  危险信号：
    - "我 mock 这个以防万一"
    - "这个可能很慢，最好 mock"
    - 不理解依赖链就 mock
```

## 反模式 4：不完整的 mock

**违规写法：**
```typescript
// ❌ BAD: Partial mock - only fields you think you need
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // Missing: metadata that downstream code uses
};

// Later: breaks when code accesses response.metadata.requestId
```

**为什么是错的：**
- **部分 mock 隐藏结构性假设** — 你只 mock 了你知道的字段
- **下游代码可能依赖你没包含的字段** — 静默失败
- **测试通过但集成失败** — mock 不完整，真实 API 完整
- **虚假信心** — 测试对真实行为毫无证明

**铁律：** mock 完整的数据结构（如同真实存在），而不是只 mock 当前测试用到的字段。

**正确写法：**
```typescript
// ✅ GOOD: Mirror real API completeness
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
  // All fields real API returns
};
```

### 门禁函数

```
创建 mock 响应之前：
  检查："真实 API 响应包含哪些字段？"

  行动：
    1. 从文档/示例中查看实际 API 响应
    2. 包含系统下游可能消费的所有字段
    3. 验证 mock 完全匹配真实响应结构

  关键：
    如果你在创建 mock，你必须理解完整结构
    当代码依赖被省略的字段时，部分 mock 会静默失败

  如果不确定：包含所有文档记录的字段
```

## 反模式 5：事后补测试

**违规写法：**
```
✅ 实现完成
❌ 没写测试
"可以测试了"
```

**为什么是错的：**
- 测试是实现的一部分，不是可选的后续步骤
- TDD 本可以发现这些问题
- 没有测试就不能声称完成

**正确写法：**
```
TDD 循环：
1. 写失败的测试
2. 实现让测试通过
3. 重构
4. 然后才能声称完成
```

## mock 变得过于复杂时

**警告信号：**
- mock 准备代码比测试逻辑还长
- 为了通过测试 mock 了一切
- mock 缺少真实组件有的方法
- mock 一改测试就挂

**协作伙伴的质疑：** "我们这里真的需要用 mock 吗？"

**考虑：** 用真实组件的集成测试通常比复杂 mock 更简单。

## TDD 如何防止这些反模式

**TDD 为什么有效：**
1. **先写测试** → 强迫你思考到底在测什么
2. **看着它失败** → 确认测试测的是真实行为，不是 mock
3. **最少实现** → 仅测试使用的方法不会悄悄混入
4. **真实依赖** → 你在 mock 之前就看到测试实际需要什么

**如果你在测 mock 行为，说明你违反了 TDD** — 你在没看到测试对真实代码失败的情况下就加了 mock。

## 速查表

| 反模式 | 修复方式 |
|--------------|-----|
| 对 mock 元素断言 | 测试真实组件或取消 mock |
| 生产类中仅测试使用的方法 | 移到测试工具中 |
| 不理解就 mock | 先理解依赖，最小化 mock |
| 不完整的 mock | 完整镜像真实 API |
| 事后补测试 | TDD — 先写测试 |
| 过于复杂的 mock | 考虑集成测试 |

## 危险信号

- 断言检查 `*-mock` 测试 ID
- 方法只在测试文件中被调用
- mock 准备代码占测试的 50% 以上
- 移除 mock 测试就失败
- 说不清为什么需要 mock
- "以防万一"就 mock

## 底线

**Mock 是隔离工具，不是被测对象。**

如果 TDD 发现你在测 mock 行为，说明你走偏了。

修复方式：测试真实行为，或质疑你为什么要 mock。
