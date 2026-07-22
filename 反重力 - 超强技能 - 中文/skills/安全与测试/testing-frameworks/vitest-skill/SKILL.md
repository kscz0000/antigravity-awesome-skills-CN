---
name: vitest-skill
description: '生成 JavaScript/TypeScript 的 Vitest 测试，具备 Vite 原生速度。Jest 兼容 API，支持 ESM 和 HMR。涉及"Vitest"、"vi.mock"、"vitest.config"时使用。触发词：Vitest、vi.mock、vi.fn、Vite test、vitest config。'
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/vitest-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Vitest 测试技能
## 适用场景

当你需要生成 JavaScript/TypeScript 的 Vitest 测试（具备 Vite 原生速度）时使用本技能。提供 Jest 兼容的 API，原生支持 ESM 和 HMR。涉及"Vitest"、"vi.mock"、"vitest.config"时启用。触发词：Vitest、vi.mock、vi.fn、Vite test、vitest config。


## 核心模式

### 基础测试

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Calculator } from './calculator';

describe('Calculator', () => {
  let calc: Calculator;
  beforeEach(() => { calc = new Calculator(); });

  it('adds two numbers', () => {
    expect(calc.add(2, 3)).toBe(5);
  });

  it('throws on divide by zero', () => {
    expect(() => calc.divide(10, 0)).toThrow();
  });
});
```

### Mock 写法（用 vi 取代 jest）

```typescript
import { vi } from 'vitest';

// Mock module
vi.mock('./database', () => ({
  getUser: vi.fn().mockResolvedValue({ name: 'Alice' }),
  saveUser: vi.fn().mockResolvedValue(true),
}));

// Mock function
const mockFn = vi.fn();
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ data: 'test' });

// Spy
const spy = vi.spyOn(console, 'log').mockImplementation(() => {});
expect(spy).toHaveBeenCalledWith('message');
spy.mockRestore();

// Timers
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.runAllTimers();
vi.useRealTimers();
```

### 源码内测试

```typescript
// src/math.ts — tests alongside code!
export function add(a: number, b: number) { return a + b; }
export function multiply(a: number, b: number) { return a * b; }

if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest;
  it('adds', () => { expect(add(2, 3)).toBe(5); });
  it('multiplies', () => { expect(multiply(3, 4)).toBe(12); });
}
```

### 快照测试

```typescript
it('serializes user', () => {
  expect(serializeUser(user)).toMatchSnapshot();
});

it('inline snapshot', () => {
  expect(serializeUser(user)).toMatchInlineSnapshot(`
    { "name": "Alice", "email": "alice@test.com" }
  `);
});
```

### React 组件测试

```typescript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Button from './Button';

describe('Button', () => {
  it('renders with label', () => {
    render(<Button label="Click me" />);
    expect(screen.getByText('Click me')).toBeDefined();
  });
});
```

### 反模式

| 反例 | 正例 | 原因 |
|-----|------|-----|
| `jest.fn()` | `vi.fn()` | Vitest 默认使用 `vi` 作为测试工具命名空间 |
| `jest.mock()` | `vi.mock()` | 命名空间不同（vi 取代 jest） |
| 缺少类型安全 | TypeScript + strict | Vitest 以 TypeScript 优先，原生支持类型推断 |

## 速查表

| 任务 | 命令 |
|------|---------|
| 单次运行 | `npx vitest run` |
| 监听模式 | `npx vitest`（默认） |
| UI 界面 | `npx vitest --ui` |
| 覆盖率 | `npx vitest --coverage` |
| 指定文件 | `npx vitest run src/math.test.ts` |
| 过滤用例 | `npx vitest run -t "adds"` |

## vitest.config.ts（配置文件示例）

```typescript
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: { provider: 'v8', reporter: ['text', 'html'] },
    include: ['src/**/*.{test,spec}.{js,ts,tsx}'],
    includeSource: ['src/**/*.{js,ts}'],
  },
});
```

## 进阶模式 → `reference/playbook.md`

| § | 章节 | 行数范围 |
|---|---------|-------|
| 1 | 生产环境配置 | Config、workspace、setup file |
| 2 | Mock 模式 | vi.mock、spies、timers、fetch |
| 3 | React Testing Library | 组件、hooks、providers |
| 4 | 快照与内联快照 | 文件、内联、自定义序列化 |
| 5 | 表驱动测试 | test.each、describe.each |
| 6 | 源码内测试 | 与源码同址的测试 |
| 7 | API / 集成测试 | 使用 fetch 的服务端测试 |
| 8 | CI/CD 集成 | GitHub Actions、脚本 |
| 9 | 调试速查 | 10 个常见问题 |
| 10 | 最佳实践清单 | 13 项 |

## 局限说明

- 仅当任务与上游来源及本地项目上下文明确匹配时使用本技能。
- 在应用变更前，请核实命令、生成的代码、依赖、凭证以及外部服务行为。
- 示例不能替代特定环境下的测试、安全审查，也不能替代对破坏性或高成本操作的用户审批。