---
name: senior-frontend
description: 面向 React、Next.js、TypeScript 和 Tailwind CSS 应用的前端开发技能。当需要构建 React 组件、优化 Next.js 性能、分析打包体积、搭建前端项目、实现无障碍或审查前端代码质量时使用。触发词：前端开发、React组件、Next.js优化、打包分析、前端脚手架、无障碍、前端代码审查、Tailwind CSS
risk: safe
source: https://github.com/alirezarezvani/claude-skills
date_added: "2026-03-07"
---

# 高级前端

面向 React/Next.js 应用的前端开发模式、性能优化和自动化工具。

## 适用场景
- 使用 TypeScript 和 Tailwind CSS 搭建新的 React 或 Next.js 项目时使用。
- 生成新组件或自定义 Hook 时使用。
- 分析和优化前端应用的打包体积时使用。
- 实现或审查高级 React 模式（如复合组件、渲染属性）时使用。
- 确保无障碍合规性和实施健壮的测试策略时使用。

## 目录

- [项目脚手架](#项目脚手架)
- [组件生成](#组件生成)
- [打包分析](#打包分析)
- [React 模式](#react-模式)
- [Next.js 优化](#nextjs-优化)
- [无障碍与测试](#无障碍与测试)

---

## 项目脚手架

使用 TypeScript、Tailwind CSS 和最佳实践配置生成新的 Next.js 或 React 项目。

### 工作流：创建新的前端项目

1. 使用项目名称和模板运行脚手架工具：

   ```bash
   python scripts/frontend_scaffolder.py my-app --template nextjs
   ```

2. 添加可选功能（认证、API、表单、测试、Storybook）：

   ```bash
   python scripts/frontend_scaffolder.py dashboard --template nextjs --features auth,api
   ```

3. 进入项目目录并安装依赖：

   ```bash
   cd my-app && npm install
   ```

4. 启动开发服务器：
   ```bash
   npm run dev
   ```

### 脚手架选项

| 选项                 | 说明                                               |
| -------------------- | -------------------------------------------------- |
| `--template nextjs`  | Next.js 14+，含 App Router 和 Server Components    |
| `--template react`   | React + Vite，含 TypeScript                         |
| `--features auth`    | 添加 NextAuth.js 认证                               |
| `--features api`     | 添加 React Query + API 客户端                       |
| `--features forms`   | 添加 React Hook Form + Zod 校验                     |
| `--features testing` | 添加 Vitest + Testing Library                       |
| `--dry-run`          | 预览文件但不创建                                    |

### 生成的项目结构（Next.js）

```
my-app/
├── app/
│   ├── layout.tsx        # 根布局，含字体配置
│   ├── page.tsx          # 首页
│   ├── globals.css       # Tailwind + CSS 变量
│   └── api/health/route.ts
├── components/
│   ├── ui/               # Button、Input、Card
│   └── layout/           # Header、Footer、Sidebar
├── hooks/                # useDebounce、useLocalStorage
├── lib/                  # utils (cn)、constants
├── types/                # TypeScript 接口
├── tailwind.config.ts
├── next.config.js
└── package.json
```

---

## 组件生成

生成带 TypeScript、测试和 Storybook stories 的 React 组件。

### 工作流：创建新组件

1. 生成客户端组件：

   ```bash
   python scripts/component_generator.py Button --dir src/components/ui
   ```

2. 生成服务端组件：

   ```bash
   python scripts/component_generator.py ProductCard --type server
   ```

3. 生成带测试和 story 文件的组件：

   ```bash
   python scripts/component_generator.py UserProfile --with-test --with-story
   ```

4. 生成自定义 Hook：
   ```bash
   python scripts/component_generator.py FormValidation --type hook
   ```

### 生成器选项

| 选项            | 说明                                       |
| --------------- | ------------------------------------------ |
| `--type client` | 客户端组件，带 'use client'（默认）        |
| `--type server` | 异步服务端组件                              |
| `--type hook`   | 自定义 React Hook                           |
| `--with-test`   | 包含测试文件                                |
| `--with-story`  | 包含 Storybook story                        |
| `--flat`        | 直接在输出目录创建，不建子目录              |
| `--dry-run`     | 预览但不创建文件                            |

### 生成的组件示例

```tsx
"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

interface ButtonProps {
  className?: string;
  children?: React.ReactNode;
}

export function Button({ className, children }: ButtonProps) {
  return <div className={cn("", className)}>{children}</div>;
}
```

---

## 打包分析

分析 package.json 和项目结构，发现打包优化机会。

### 工作流：优化打包体积

1. 对项目运行分析器：

   ```bash
   python scripts/bundle_analyzer.py /path/to/project
   ```

2. 查看健康评分和问题：

   ```
   Bundle Health Score: 75/100 (C)

   HEAVY DEPENDENCIES:
     moment (290KB)
       Alternative: date-fns (12KB) or dayjs (2KB)

     lodash (71KB)
       Alternative: lodash-es with tree-shaking
   ```

3. 应用推荐的修复方案，替换重量级依赖。

4. 使用详细模式重新运行以检查导入模式：
   ```bash
   python scripts/bundle_analyzer.py . --verbose
   ```

### 打包评分解读

| 评分   | 等级 | 行动                         |
| ------ | ---- | ---------------------------- |
| 90-100 | A    | 打包已充分优化               |
| 80-89  | B    | 有小幅优化空间               |
| 70-79  | C    | 替换重量级依赖               |
| 60-69  | D    | 多个问题需要关注             |
| 0-59   | F    | 打包体积存在严重问题         |

### 检测到的重量级依赖

分析器会识别以下常见的重量级包：

| 包名          | 大小  | 替代方案                         |
| ------------- | ----- | -------------------------------- |
| moment        | 290KB | date-fns (12KB) 或 dayjs (2KB)   |
| lodash        | 71KB  | lodash-es 配合 tree-shaking      |
| axios         | 14KB  | 原生 fetch 或 ky (3KB)           |
| jquery        | 87KB  | 原生 DOM APIs                    |
| @mui/material | 大    | shadcn/ui 或 Radix UI            |

---

## React 模式

参考：`references/react_patterns.md`

### 复合组件

在相关组件之间共享状态：

```tsx
const Tabs = ({ children }) => {
  const [active, setActive] = useState(0);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = TabList;
Tabs.Panel = TabPanel;

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab>One</Tabs.Tab>
    <Tabs.Tab>Two</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel>Content 1</Tabs.Panel>
  <Tabs.Panel>Content 2</Tabs.Panel>
</Tabs>;
```

### 自定义 Hook

提取可复用的逻辑：

```tsx
function useDebounce<T>(value: T, delay = 500): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 300);
```

### 渲染属性

共享渲染逻辑：

```tsx
function DataFetcher({ url, render }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(url)
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, [url]);

  return render({ data, loading });
}

// Usage
<DataFetcher
  url="/api/users"
  render={({ data, loading }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
/>;
```

---

## Next.js 优化

参考：`references/nextjs_optimization_guide.md`

### 服务端 vs 客户端组件

默认使用 Server Components。仅在需要以下功能时添加 'use client'：

- 事件处理器（onClick、onChange）
- 状态管理（useState、useReducer）
- 副作用（useEffect）
- 浏览器 API

```tsx
// Server Component (default) - no 'use client'
async function ProductPage({ params }) {
  const product = await getProduct(params.id); // Server-side fetch

  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} /> {/* Client component */}
    </div>
  );
}

// Client Component
("use client");
function AddToCartButton({ productId }) {
  const [adding, setAdding] = useState(false);
  return <button onClick={() => addToCart(productId)}>Add</button>;
}
```

### 图片优化

```tsx
import Image from 'next/image';

// Above the fold - load immediately
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
/>

// Responsive image with fill
<div className="relative aspect-video">
  <Image
    src="/product.jpg"
    alt="Product"
    fill
    sizes="(max-width: 768px) 100vw, 50vw"
    className="object-cover"
  />
</div>
```

### 数据获取模式

```tsx
// Parallel fetching
async function Dashboard() {
  const [user, stats] = await Promise.all([getUser(), getStats()]);
  return <div>...</div>;
}

// Streaming with Suspense
async function ProductPage({ params }) {
  return (
    <div>
      <ProductDetails id={params.id} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>
    </div>
  );
}
```

---

## 无障碍与测试

参考：`references/frontend_best_practices.md`

### 无障碍检查清单

1. **语义化 HTML**：使用正确的元素（`<button>`、`<nav>`、`<main>`）
2. **键盘导航**：所有交互元素可聚焦
3. **ARIA 标签**：为图标和复杂控件提供标签
4. **颜色对比度**：普通文本最低 4.5:1
5. **焦点指示器**：可见的焦点状态

```tsx
// Accessible button
<button
  type="button"
  aria-label="Close dialog"
  onClick={onClose}
  className="focus-visible:ring-2 focus-visible:ring-blue-500"
>
  <XIcon aria-hidden="true" />
</button>

// Skip link for keyboard users
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### 测试策略

```tsx
// Component test with React Testing Library
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("button triggers action on click", async () => {
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Click me</Button>);

  await userEvent.click(screen.getByRole("button"));
  expect(onClick).toHaveBeenCalledTimes(1);
});

// Test accessibility
test("dialog is accessible", async () => {
  render(<Dialog open={true} title="Confirm" />);

  expect(screen.getByRole("dialog")).toBeInTheDocument();
  expect(screen.getByRole("dialog")).toHaveAttribute("aria-labelledby");
});
```

---

## 快速参考

### 常用 Next.js 配置

```js
// next.config.js
const nextConfig = {
  images: {
    remotePatterns: [{ hostname: "cdn.example.com" }],
    formats: ["image/avif", "image/webp"],
  },
  experimental: {
    optimizePackageImports: ["lucide-react", "@heroicons/react"],
  },
};
```

### Tailwind CSS 工具类

```tsx
// Conditional classes with cn()
import { cn } from "@/lib/utils";

<button
  className={cn(
    "px-4 py-2 rounded",
    variant === "primary" && "bg-blue-500 text-white",
    disabled && "opacity-50 cursor-not-allowed",
  )}
/>;
```

### TypeScript 模式

```tsx
// Props with children
interface CardProps {
  className?: string;
  children: React.ReactNode;
}

// Generic component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```

---

## 资源

- React 模式：`references/react_patterns.md`
- Next.js 优化：`references/nextjs_optimization_guide.md`
- 最佳实践：`references/frontend_best_practices.md`

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来寻求澄清。
