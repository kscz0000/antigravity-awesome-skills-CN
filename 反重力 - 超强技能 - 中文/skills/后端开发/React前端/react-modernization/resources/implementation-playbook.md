# React 现代化实施手册

本文件包含技能引用的详细模式、清单和代码示例。

# React 现代化

精通 React 版本升级、class 到 hooks 迁移、并发特性采用及 codemod 自动化重构。

## 使用场景

- 将 React 应用升级到最新版本
- 将 class 组件迁移为使用 hooks 的函数组件
- 采用并发 React 特性（Suspense、transitions）
- 使用 codemod 进行自动化重构
- 现代化状态管理模式
- 迁移到 TypeScript
- 利用 React 18+ 特性提升性能

## 版本升级路径

### React 16 → 17 → 18

**各版本破坏性变更：**

**React 17：**
- 事件委托变更
- 移除事件池
- Effect 清理时机
- JSX 转换（无需 import React）

**React 18：**
- 自动批处理
- 并发渲染
- Strict Mode 变更（双重调用）
- 新的 root API
- 服务端 Suspense

## Class 到 Hooks 迁移

### 状态管理
```javascript
// Before: Class component
class Counter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      count: 0,
      name: ''
    };
  }

  increment = () => {
    this.setState({ count: this.state.count + 1 });
  }

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={this.increment}>Increment</button>
      </div>
    );
  }
}

// After: Functional component with hooks
function Counter() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  const increment = () => {
    setCount(count + 1);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  );
}
```

### 生命周期方法到 Hooks
```javascript
// Before: Lifecycle methods
class DataFetcher extends React.Component {
  state = { data: null, loading: true };

  componentDidMount() {
    this.fetchData();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.id !== this.props.id) {
      this.fetchData();
    }
  }

  componentWillUnmount() {
    this.cancelRequest();
  }

  fetchData = async () => {
    const data = await fetch(`/api/${this.props.id}`);
    this.setState({ data, loading: false });
  };

  cancelRequest = () => {
    // Cleanup
  };

  render() {
    if (this.state.loading) return <div>Loading...</div>;
    return <div>{this.state.data}</div>;
  }
}

// After: useEffect hook
function DataFetcher({ id }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    const fetchData = async () => {
      try {
        const response = await fetch(`/api/${id}`);
        const result = await response.json();

        if (!cancelled) {
          setData(result);
          setLoading(false);
        }
      } catch (error) {
        if (!cancelled) {
          console.error(error);
        }
      }
    };

    fetchData();

    // Cleanup function
    return () => {
      cancelled = true;
    };
  }, [id]); // Re-run when id changes

  if (loading) return <div>Loading...</div>;
  return <div>{data}</div>;
}
```

### Context 和 HOC 到 Hooks
```javascript
// Before: Context consumer and HOC
const ThemeContext = React.createContext();

class ThemedButton extends React.Component {
  static contextType = ThemeContext;

  render() {
    return (
      <button style={{ background: this.context.theme }}>
        {this.props.children}
      </button>
    );
  }
}

// After: useContext hook
function ThemedButton({ children }) {
  const { theme } = useContext(ThemeContext);

  return (
    <button style={{ background: theme }}>
      {children}
    </button>
  );
}

// Before: HOC for data fetching
function withUser(Component) {
  return class extends React.Component {
    state = { user: null };

    componentDidMount() {
      fetchUser().then(user => this.setState({ user }));
    }

    render() {
      return <Component {...this.props} user={this.state.user} />;
    }
  };
}

// After: Custom hook
function useUser() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser().then(setUser);
  }, []);

  return user;
}

function UserProfile() {
  const user = useUser();
  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

## React 18 并发特性

### 新的 Root API
```javascript
// Before: React 17
import ReactDOM from 'react-dom';

ReactDOM.render(<App />, document.getElementById('root'));

// After: React 18
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

### 自动批处理
```javascript
// React 18: All updates are batched
function handleClick() {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Only one re-render (batched)
}

// Even in async:
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Still batched in React 18!
}, 1000);

// Opt out if needed
import { flushSync } from 'react-dom';

flushSync(() => {
  setCount(c => c + 1);
});
// Re-render happens here
setFlag(f => !f);
// Another re-render
```

### 过渡
```javascript
import { useState, useTransition } from 'react';

function SearchResults() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    // Urgent: Update input immediately
    setQuery(e.target.value);

    // Non-urgent: Update results (can be interrupted)
    startTransition(() => {
      setResults(searchResults(e.target.value));
    });
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <Results data={results} />
    </>
  );
}
```

### Suspense 数据获取
```javascript
import { Suspense } from 'react';

// Resource-based data fetching (with React 18)
const resource = fetchProfileData();

function ProfilePage() {
  return (
    <Suspense fallback={<Loading />}>
      <ProfileDetails />
      <Suspense fallback={<Loading />}>
        <ProfileTimeline />
      </Suspense>
    </Suspense>
  );
}

function ProfileDetails() {
  // This will suspend if data not ready
  const user = resource.user.read();
  return <h1>{user.name}</h1>;
}

function ProfileTimeline() {
  const posts = resource.posts.read();
  return <Timeline posts={posts} />;
}
```

## Codemod 自动化

### 运行 React Codemod
```bash
# Install jscodeshift
npm install -g jscodeshift

# React 16.9 codemod (rename unsafe lifecycle methods)
npx react-codeshift <transform> <path>

# Example: Rename UNSAFE_ methods
npx react-codeshift --parser=tsx \
  --transform=react-codeshift/transforms/rename-unsafe-lifecycles.js \
  src/

# Update to new JSX Transform (React 17+)
npx react-codeshift --parser=tsx \
  --transform=react-codeshift/transforms/new-jsx-transform.js \
  src/

# Class to Hooks (third-party)
npx codemod react/hooks/convert-class-to-function src/
```

### 自定义 Codemod 示例
```javascript
// custom-codemod.js
module.exports = function(file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);

  // Find setState calls
  root.find(j.CallExpression, {
    callee: {
      type: 'MemberExpression',
      property: { name: 'setState' }
    }
  }).forEach(path => {
    // Transform to useState
    // ... transformation logic
  });

  return root.toSource();
};

// Run: jscodeshift -t custom-codemod.js src/
```

## 性能优化

### useMemo 和 useCallback
```javascript
function ExpensiveComponent({ items, filter }) {
  // Memoize expensive calculation
  const filteredItems = useMemo(() => {
    return items.filter(item => item.category === filter);
  }, [items, filter]);

  // Memoize callback to prevent child re-renders
  const handleClick = useCallback((id) => {
    console.log('Clicked:', id);
  }, []); // No dependencies, never changes

  return (
    <List items={filteredItems} onClick={handleClick} />
  );
}

// Child component with memo
const List = React.memo(({ items, onClick }) => {
  return items.map(item => (
    <Item key={item.id} item={item} onClick={onClick} />
  ));
});
```

### 代码分割
```javascript
import { lazy, Suspense } from 'react';

// Lazy load components
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

## TypeScript 迁移

```typescript
// Before: JavaScript
function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}

// After: TypeScript
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
}

function Button({ onClick, children }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>;
}

// Generic components
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <>{items.map(renderItem)}</>;
}
```

## 迁移清单

```markdown
### 迁移前
- [ ] 逐步更新依赖（不要一次性全部更新）
- [ ] 审查发布说明中的破坏性变更
- [ ] 设置测试套件
- [ ] 创建功能分支

### Class → Hooks 迁移
- [ ] 识别需要迁移的 class 组件
- [ ] 从叶子组件开始（无子组件）
- [ ] 将 state 转换为 useState
- [ ] 将生命周期转换为 useEffect
- [ ] 将 context 转换为 useContext
- [ ] 提取自定义 hooks
- [ ] 全面测试

### React 18 升级
- [ ] 先升级到 React 17（如需要）
- [ ] 将 react 和 react-dom 更新到 18
- [ ] 如使用 TypeScript 则更新 @types/react
- [ ] 切换到 createRoot API
- [ ] 使用 StrictMode 测试（双重调用）
- [ ] 解决并发渲染问题
- [ ] 在合适的地方采用 Suspense/Transitions

### 性能
- [ ] 识别性能瓶颈
- [ ] 在合适的地方添加 React.memo
- [ ] 对昂贵操作使用 useMemo/useCallback
- [ ] 实现代码分割
- [ ] 优化重渲染

### 测试
- [ ] 更新测试工具（React Testing Library）
- [ ] 使用 React 18 特性测试
- [ ] 检查控制台警告
- [ ] 性能测试
```

## 资源

- **references/breaking-changes.md**: 特定版本的破坏性变更
- **references/codemods.md**: Codemod 使用指南
- **references/hooks-migration.md**: 全面的 hooks 模式
- **references/concurrent-features.md**: React 18 并发特性
- **assets/codemod-config.json**: Codemod 配置
- **assets/migration-checklist.md**: 逐步清单
- **scripts/apply-codemods.sh**: 自动化 codemod 脚本

## 最佳实践

1. **渐进式迁移**：不要一次性迁移所有内容
2. **全面测试**：每个步骤都要进行充分测试
3. **使用 Codemod**：自动化重复性转换
4. **从简单开始**：从叶子组件入手
5. **利用 StrictMode**：尽早发现问题
6. **监控性能**：迁移前后都要测量
7. **记录变更**：保留迁移日志

## 常见陷阱

- 忘记 useEffect 依赖
- 过度使用 useMemo/useCallback
- useEffect 中未处理清理
- 混用 class 和函数组件模式
- 忽略 StrictMode 警告
- 破坏性变更假设
