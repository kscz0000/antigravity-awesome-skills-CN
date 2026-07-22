---
name: testing-patterns
description: "Jest 测试模式、工厂函数、Mock 策略及 TDD 工作流。适用于编写单元测试、创建测试工厂或遵循 TDD 红绿重构循环。触发词：单元测试、测试工厂、TDD、Jest、Mock、测试模式、红绿重构。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 测试模式与工具集

## 测试理念

**测试驱动开发（TDD）：**
- 先写失败的测试
- 实现最少代码让测试通过
- 通过后再重构
- 没有失败的测试就不写生产代码

**行为驱动测试：**
- 测试行为，而非实现细节
- 聚焦公开 API 和业务需求
- 避免测试实现细节
- 用描述性测试名称表达行为

**工厂模式：**
- 创建 `getMockX(overrides?: Partial<X>)` 函数
- 提供合理的默认值
- 允许覆盖特定属性
- 保持测试 DRY 且可维护

## 测试工具

### 自定义渲染函数

创建自定义渲染函数，用必要的 Provider 包裹组件：

```typescript
// src/utils/testUtils.tsx
import { render } from '@testing-library/react-native';
import { ThemeProvider } from './theme';

export const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <ThemeProvider>{ui}</ThemeProvider>
  );
};
```

**用法：**
```typescript
import { renderWithTheme } from 'utils/testUtils';
import { screen } from '@testing-library/react-native';

it('should render component', () => {
  renderWithTheme(<MyComponent />);
  expect(screen.getByText('Hello')).toBeTruthy();
});
```

## 工厂模式

### 组件 Props 工厂

```typescript
import { ComponentProps } from 'react';

const getMockMyComponentProps = (
  overrides?: Partial<ComponentProps<typeof MyComponent>>
) => {
  return {
    title: 'Default Title',
    count: 0,
    onPress: jest.fn(),
    isLoading: false,
    ...overrides,
  };
};

// Usage in tests
it('should render with custom title', () => {
  const props = getMockMyComponentProps({ title: 'Custom Title' });
  renderWithTheme(<MyComponent {...props} />);
  expect(screen.getByText('Custom Title')).toBeTruthy();
});
```

### 数据工厂

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

const getMockUser = (overrides?: Partial<User>): User => {
  return {
    id: '123',
    name: 'John Doe',
    email: 'john@example.com',
    role: 'user',
    ...overrides,
  };
};

// Usage
it('should display admin badge for admin users', () => {
  const user = getMockUser({ role: 'admin' });
  renderWithTheme(<UserCard user={user} />);
  expect(screen.getByText('Admin')).toBeTruthy();
});
```

## Mock 模式

### Mock 模块

```typescript
// Mock entire module
jest.mock('utils/analytics');

// Mock with factory function
jest.mock('utils/analytics', () => ({
  Analytics: {
    logEvent: jest.fn(),
  },
}));

// Access mock in test
const mockLogEvent = jest.requireMock('utils/analytics').Analytics.logEvent;
```

### Mock GraphQL Hooks

```typescript
jest.mock('./GetItems.generated', () => ({
  useGetItemsQuery: jest.fn(),
}));

const mockUseGetItemsQuery = jest.requireMock(
  './GetItems.generated'
).useGetItemsQuery as jest.Mock;

// In test
mockUseGetItemsQuery.mockReturnValue({
  data: { items: [] },
  loading: false,
  error: undefined,
});
```

## 测试结构

```typescript
describe('ComponentName', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('should render component with default props', () => {});
    it('should render loading state when loading', () => {});
  });

  describe('User interactions', () => {
    it('should call onPress when button is clicked', async () => {});
  });

  describe('Edge cases', () => {
    it('should handle empty data gracefully', () => {});
  });
});
```

## 查询模式

```typescript
// Element must exist
expect(screen.getByText('Hello')).toBeTruthy();

// Element should not exist
expect(screen.queryByText('Goodbye')).toBeNull();

// Element appears asynchronously
await waitFor(() => {
  expect(screen.findByText('Loaded')).toBeTruthy();
});
```

## 用户交互模式

```typescript
import { fireEvent, screen } from '@testing-library/react-native';

it('should submit form on button click', async () => {
  const onSubmit = jest.fn();
  renderWithTheme(<LoginForm onSubmit={onSubmit} />);

  fireEvent.changeText(screen.getByLabelText('Email'), 'user@example.com');
  fireEvent.changeText(screen.getByLabelText('Password'), 'password123');
  fireEvent.press(screen.getByTestId('login-button'));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalled();
  });
});
```

## 需要避免的反模式

### 测试 Mock 行为而非真实行为

```typescript
// Bad - testing the mock
expect(mockFetchData).toHaveBeenCalled();

// Good - testing actual behavior
expect(screen.getByText('John Doe')).toBeTruthy();
```

### 不使用工厂函数

```typescript
// Bad - duplicated, inconsistent test data
it('test 1', () => {
  const user = { id: '1', name: 'John', email: 'john@test.com', role: 'user' };
});
it('test 2', () => {
  const user = { id: '2', name: 'Jane', email: 'jane@test.com' }; // Missing role!
});

// Good - reusable factory
const user = getMockUser({ name: 'Custom Name' });
```

## 最佳实践

1. **始终使用工厂函数** 生成 props 和数据
2. **测试行为，而非实现**
3. **使用描述性测试名称**
4. **用 describe 块组织测试**
5. **测试间清理 mock**
6. **保持测试聚焦** — 每个测试只验证一个行为

## 运行测试

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific file
npm test ComponentName.test.tsx
```

## 与其他技能的配合

- **react-ui-patterns**：测试所有 UI 状态（loading、error、empty、success）
- **systematic-debugging**：修复 bug 前先写复现测试

## 适用场景
本技能适用于执行概览中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清。
