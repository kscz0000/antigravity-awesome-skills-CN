---
name: code-showcase-testing-patterns
description: Jest 测试模式、工厂函数、模拟策略与 TDD 工作流。在编写单元测试、创建测试工厂或遵循 TDD 红绿重构循环时使用。触发词：Jest、测试模式、工厂函数、mock、模拟、TDD、测试驱动开发、红绿重构。
risk: unknown
source: https://github.com/ChrisWiles/claude-code-showcase/tree/main/.claude/skills/testing-patterns
source_repo: ChrisWiles/claude-code-showcase
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ChrisWiles/claude-code-showcase/blob/main/LICENSE
---

# 测试模式与工具
## 使用时机

当你需要 Jest 测试模式、工厂函数、模拟策略以及 TDD 工作流时使用本技能。在编写单元测试、创建测试工厂，或遵循 TDD 红绿重构循环时使用。


## 测试理念

**测试驱动开发（TDD）：**
- 先编写一个失败的测试
- 编写最少的代码使其通过
- 测试通过后再进行重构
- 没有失败的测试，绝不写生产代码

**行为驱动测试：**
- 测试行为，而非实现细节
- 聚焦于公共 API 与业务需求
- 避免测试实现细节
- 使用能描述行为的、清晰的测试名称

**工厂模式：**
- 创建 `getMockX(overrides?: Partial<X>)` 形式的函数
- 提供合理的默认值
- 允许覆盖指定属性
- 保持测试简洁（DRY）且易于维护

## 测试工具

### 自定义 Render 函数

创建一个自定义 render，将组件包裹在必需的 Provider 中：

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

// 在测试中使用
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

// 用法
it('should display admin badge for admin users', () => {
  const user = getMockUser({ role: 'admin' });
  renderWithTheme(<UserCard user={user} />);
  expect(screen.getByText('Admin')).toBeTruthy();
});
```

## Mock 模式

### Mock 模块

```typescript
// Mock 整个模块
jest.mock('utils/analytics');

// 使用工厂函数 Mock
jest.mock('utils/analytics', () => ({
  Analytics: {
    logEvent: jest.fn(),
  },
}));

// 在测试中访问 mock
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

// 在测试中
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
// 元素必须存在
expect(screen.getByText('Hello')).toBeTruthy();

// 元素不应存在
expect(screen.queryByText('Goodbye')).toBeNull();

// 元素异步出现
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

## 应避免的反模式

### 测试 mock 的行为而非真实行为

```typescript
// 错误——在测试 mock 本身
expect(mockFetchData).toHaveBeenCalled();

// 正确——测试真实行为
expect(screen.getByText('John Doe')).toBeTruthy();
```

### 不使用工厂

```typescript
// 错误——重复且不一致的测试数据
it('test 1', () => {
  const user = { id: '1', name: 'John', email: 'john@test.com', role: 'user' };
});
it('test 2', () => {
  const user = { id: '2', name: 'Jane', email: 'jane@test.com' }; // Missing role!
});

// 正确——可复用的工厂
const user = getMockUser({ name: 'Custom Name' });
```

## 最佳实践

1. **始终对 props 和数据使用工厂函数**
2. **测试行为，而非实现**
3. **使用描述性的测试名称**
4. **使用 describe 块组织测试**
5. **在每个测试之间清空 mock**
6. **保持测试聚焦**——每个测试只覆盖一个行为

## 运行测试

```bash
# 运行全部测试
npm test

# 运行并产出覆盖率
npm run test:coverage

# 运行指定文件
npm test ComponentName.test.tsx
```

## 与其他技能的协同

- **react-ui-patterns**：覆盖所有 UI 状态（加载、错误、空、成功）
- **systematic-debugging**：在修复 Bug 之前先编写能复现该 Bug 的测试

## 使用限制

- 仅当任务明确匹配其上游来源与本地项目上下文时使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要将示例视为针对特定环境的测试、安全审查或对破坏性/高成本操作的授权替代品。
