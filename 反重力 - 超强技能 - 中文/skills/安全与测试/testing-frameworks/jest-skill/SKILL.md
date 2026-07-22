---
name: jest-skill
description: '生成 JavaScript 或 TypeScript 的 Jest 单元测试与集成测试，涵盖 Mock、快照、异步测试和 React 组件测试。当用户提到 "Jest"、"describe/it/expect"、"jest.mock"、"toMatchSnapshot" 时使用。触发词："Jest"、"expect().toBe()"、"jest.mock"、...'
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/jest-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Jest 测试技能
## 使用时机

当你需要为 JavaScript 或 TypeScript 项目生成 Jest 单元测试和集成测试时，使用此技能。内容涵盖 Mock 函数/模块、快照测试、异步测试以及 React 组件测试。当用户提到 "Jest"、"describe/it/expect"、"jest.mock"、"toMatchSnapshot" 时触发。触发词包括："Jest"、"expect().toBe()"、"jest.mock"、...


## 核心模式

### 基础测试

```javascript
describe('Calculator', () => {
  let calc;
  beforeEach(() => { calc = new Calculator(); });

  test('adds two numbers', () => {
    expect(calc.add(2, 3)).toBe(5);
  });

  test('throws on division by zero', () => {
    expect(() => calc.divide(10, 0)).toThrow('Division by zero');
  });
});
```

### 匹配器

```javascript
expect(value).toBe(exact);                 // === 严格相等
expect(value).toEqual(object);             // 深度相等
expect(value).toBeTruthy();
expect(value).toBeNull();
expect(value).toBeGreaterThan(3);
expect(value).toBeCloseTo(0.3, 5);
expect(str).toMatch(/regex/);
expect(arr).toContain(item);
expect(arr).toHaveLength(3);
expect(obj).toHaveProperty('name');
expect(obj).toMatchObject({ name: 'Alice' });
expect(() => fn()).toThrow(CustomError);
```

### Mock

```javascript
// Mock 函数
const mockFn = jest.fn();
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ data: 'test' });
expect(mockFn).toHaveBeenCalledWith('arg1');
expect(mockFn).toHaveBeenCalledTimes(1);

// Mock 模块
jest.mock('./database');
const db = require('./database');
db.getUser.mockResolvedValue({ name: 'Alice' });

// 带实现的 Mock
jest.mock('./api', () => ({
  fetchUsers: jest.fn().mockResolvedValue([{ name: 'Alice' }]),
}));

// Spy（间谍函数）
const spy = jest.spyOn(console, 'log').mockImplementation();
expect(spy).toHaveBeenCalledWith('expected');
spy.mockRestore();

// 假定时器
jest.useFakeTimers();
jest.advanceTimersByTime(1000);
jest.useRealTimers();
```

### 异步测试

```javascript
test('fetches users', async () => {
  const users = await fetchUsers();
  expect(users).toHaveLength(3);
});

test('resolves with data', () => {
  return expect(fetchData()).resolves.toEqual({ data: 'value' });
});

test('rejects with error', () => {
  return expect(fetchBadData()).rejects.toThrow('not found');
});
```

### React 组件测试（Testing Library）

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import LoginForm from './LoginForm';

test('submits login form', async () => {
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  fireEvent.change(screen.getByLabelText('Email'), {
    target: { value: 'user@test.com' },
  });
  fireEvent.change(screen.getByLabelText('Password'), {
    target: { value: 'password123' },
  });
  fireEvent.click(screen.getByRole('button', { name: /login/i }));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'user@test.com', password: 'password123',
    });
  });
});
```

### 快照测试

```javascript
test('renders correctly', () => {
  const tree = renderer.create(<Button label="Click" />).toJSON();
  expect(tree).toMatchSnapshot();
});
// 更新命令：jest --updateSnapshot
```

### 反模式

| 不推荐 | 推荐 | 原因 |
|-----|------|------|
| `expect(x === y).toBe(true)` | `expect(x).toBe(y)` | 错误信息更清晰 |
| 异步测试缺少 `await` | 始终使用 `await` | 否则会吞掉失败 |
| 所有内容都做快照 | 仅对 UI 做快照，逻辑用断言 | 快照疲劳 |

## 快速参考

| 任务 | 命令 |
|------|---------|
| 运行全部 | `npx jest` |
| 监听模式 | `npx jest --watch` |
| 覆盖率报告 | `npx jest --coverage` |
| 更新快照 | `npx jest --updateSnapshot` |
| 运行单个文件 | `npx jest tests/calc.test.js` |
| 单个测试 | `test.only('name', () => {})` |

## 深入模式

生产级进阶模式请参阅 `reference/playbook.md`：

| 章节 | 内容 |
|---------|--------------|
| §1 生产环境配置 | Node + React 配置、路径别名、覆盖率阈值 |
| §2 Mock 深度解析 | 模块/部分/手动 Mock、Spy、定时器、环境变量 |
| §3 异步模式 | Promise、拒绝、事件发射器、流 |
| §4 test.each | 数组方式、标签模板、describe.each 表驱动测试 |
| §5 自定义匹配器 | toBeWithinRange、toBeValidEmail、TypeScript 声明 |
| §6 React Testing Library | userEvent、Hooks、Context Provider |
| §7 快照测试 | 组件快照、内联快照、属性匹配器 |
| §8 API 服务测试 | Mock axios、CRUD 模式、错误处理 |
| §9 全局配置 | 多项目配置、数据库搭建与清理 |
| §10 CI/CD | 带覆盖率门禁的 GitHub Actions |
| §11 调试排查表 | 10 个常见问题及修复方案 |
| §12 最佳实践 | 15 条生产级检查清单 |

## 局限性

- 仅在任务明确匹配上游源码和本地项目上下文时才使用此技能。
- 应用变更前，请验证命令、生成代码、依赖项、凭据以及外部服务行为。
- 不要将示例替代为针对特定环境的测试、安全审查或对破坏性/高成本操作的用户审批。
