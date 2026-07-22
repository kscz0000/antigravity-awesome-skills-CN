---
name: frontend-ui-engineering
description: 构建生产级质量的 UI。用于构建或修改用户界面时使用。用于创建组件、实现布局、管理状态，或当输出需要看起来和体验上是生产级质量而非 AI 生成时使用。触发词：前端 UI 工程、production UI、生产级 UI、设计系统、可访问性、组件架构、响应式设计、WCAG、React 组件、UI 设计。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/frontend-ui-engineering
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# 前端 UI 工程

## 概述

构建可访问、高性能且视觉精致的生产级用户界面。目标是让 UI 看起来像由一家顶级公司的具有设计意识的工程师所打造——而不是 AI 生成的。这意味着真正遵循设计系统、正确的可访问性、经过深思熟虑的交互模式，并且没有千篇一律的"AI 美学"。

## 使用场景

- 构建新的 UI 组件或页面
- 修改现有的用户界面
- 实现响应式布局
- 添加交互或状态管理
- 修复视觉或 UX 问题

## 组件架构

### 文件结构

将与一个组件相关的所有内容就近放置：

```
src/components/
  TaskList/
    TaskList.tsx          # Component implementation
    TaskList.test.tsx     # Tests
    TaskList.stories.tsx  # Storybook stories (if using)
    use-task-list.ts      # Custom hook (if complex state)
    types.ts              # Component-specific types (if needed)
```

### 组件模式

**优先采用组合而非配置：**

```tsx
// Good: Composable
<Card>
  <CardHeader>
    <CardTitle>Tasks</CardTitle>
  </CardHeader>
  <CardBody>
    <TaskList tasks={tasks} />
  </CardBody>
</Card>

// Avoid: Over-configured
<Card
  title="Tasks"
  headerVariant="large"
  bodyPadding="md"
  content={<TaskList tasks={tasks} />}
/>
```

**保持组件职责单一：**

```tsx
// Good: Does one thing
export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <li className="flex items-center gap-3 p-3">
      <Checkbox checked={task.done} onChange={() => onToggle(task.id)} />
      <span className={task.done ? 'line-through text-muted' : ''}>{task.title}</span>
      <Button variant="ghost" size="sm" onClick={() => onDelete(task.id)}>
        <TrashIcon />
      </Button>
    </li>
  );
}
```

**将数据获取与展示分离：**

```tsx
// Container: handles data
export function TaskListContainer() {
  const { tasks, isLoading, error } = useTasks();

  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorState message="Failed to load tasks" retry={refetch} />;
  if (tasks.length === 0) return <EmptyState message="No tasks yet" />;

  return <TaskList tasks={tasks} />;
}

// Presentation: handles rendering
export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul role="list" className="divide-y">
      {tasks.map(task => <TaskItem key={task.id} task={task} />)}
    </ul>
  );
}
```

## 状态管理

**选择能解决问题的最简单方案：**

```
Local state (useState)           → Component-specific UI state
Lifted state                     → Shared between 2-3 sibling components
Context                          → Theme, auth, locale (read-heavy, write-rare)
URL state (searchParams)         → Filters, pagination, shareable UI state
Server state (React Query, SWR)  → Remote data with caching
Global store (Zustand, Redux)    → Complex client state shared app-wide
```

**避免超过 3 层以上的 prop drilling**。如果你正在通过不使用 prop 的组件向下传递，请引入 context 或重构组件树。

## 遵循设计系统

### 避免 AI 美学

AI 生成的 UI 有可识别的模式。全部避免它们：

| AI 默认 | 为什么是问题 | 生产级质量 |
|---|---|---|
| 到处都是紫色/靛蓝 | 模型默认为视觉上"安全"的调色板，使每个应用看起来都一样 | 使用项目实际的颜色调色板 |
| 过度的渐变 | 渐变增加视觉噪音，与大多数设计系统冲突 | 扁平或微妙的渐变，符合设计系统 |
| 一切都圆角（rounded-2xl） | 最大圆角传达"友好"，但忽略了真实设计中圆角层级的意义 | 来自设计系统的一致圆角 |
| 通用 hero 区域 | 模板驱动的布局，与实际内容或用户需求无关 | 内容优先的布局 |
| Lorem ipsum 风格的文案 | 占位文本隐藏了真实内容暴露出的布局问题（长度、换行、溢出） | 真实的占位内容 |
| 到处都是超大内边距 | 一律慷慨的内边距破坏视觉层级且浪费屏幕空间 | 一致的间距比例 |
| 千篇一律的卡片网格 | 均匀的网格是布局偷懒，无视信息优先级和扫读模式 | 目标驱动的布局 |
| 重阴影设计 | 分层阴影增加的深度会与内容竞争，并在低端设备上拖慢渲染 | 微妙阴影或无阴影，除非设计系统明确要求 |

### 间距与布局

使用一致的间距比例。不要凭空造值：

```css
/* Use the scale: 0.25rem increments (or whatever the project uses) */
/* Good */  padding: 1rem;      /* 16px */
/* Good */  gap: 0.75rem;       /* 12px */
/* Bad */   padding: 13px;      /* Not on any scale */
/* Bad */   margin-top: 2.3rem; /* Not on any scale */
```

### 排版

尊重类型层级：

```
h1 → Page title (one per page)
h2 → Section title
h3 → Subsection title
body → Default text
small → Secondary/helper text
```

不要跳过标题级别。不要将标题样式用于非标题内容。

### 颜色

- 使用语义化的颜色 token：`text-primary`、`bg-surface`、`border-default`——而不是原始十六进制值
- 确保足够的对比度（正文 4.5:1，大字号文本 3:1）
- 不要仅依赖颜色传递信息（同时使用图标、文字或图案）

## 可访问性（WCAG 2.1 AA）

每个组件都必须满足以下标准：

### 键盘导航

```tsx
// Every interactive element must be keyboard accessible
<button onClick={handleClick}>Click me</button>        // ✓ Focusable by default
<div onClick={handleClick}>Click me</div>               // ✗ Not focusable
<div role="button" tabIndex={0} onClick={handleClick}    // ✓ But prefer <button>
     onKeyDown={e => {
       if (e.key === 'Enter') handleClick();
       if (e.key === ' ') e.preventDefault();
     }}
     onKeyUp={e => {
       if (e.key === ' ') handleClick();
     }}>
  Click me
</div>
```

### ARIA 标签

```tsx
// Label interactive elements that lack visible text
<button aria-label="Close dialog"><XIcon /></button>

// Label form inputs
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Or use aria-label when no visible label exists
<input aria-label="Search tasks" type="search" />
```

### 焦点管理

```tsx
// Move focus when content changes
function Dialog({ isOpen, onClose }: DialogProps) {
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) closeRef.current?.focus();
  }, [isOpen]);

  // Trap focus inside dialog when open
  return (
    <dialog open={isOpen}>
      <button ref={closeRef} onClick={onClose}>Close</button>
      {/* dialog content */}
    </dialog>
  );
}
```

### 有意义的空状态与错误状态

```tsx
// Don't show blank screens
function TaskList({ tasks }: { tasks: Task[] }) {
  if (tasks.length === 0) {
    return (
      <div role="status" className="text-center py-12">
        <TasksEmptyIcon className="mx-auto h-12 w-12 text-muted" />
        <h3 className="mt-2 text-sm font-medium">No tasks</h3>
        <p className="mt-1 text-sm text-muted">Get started by creating a new task.</p>
        <Button className="mt-4" onClick={onCreateTask}>Create Task</Button>
      </div>
    );
  }

  return <ul role="list">...</ul>;
}
```

## 响应式设计

先为移动端设计，再向上扩展：

```tsx
// Tailwind: mobile-first responsive
<div className="
  grid grid-cols-1      /* Mobile: single column */
  sm:grid-cols-2        /* Small: 2 columns */
  lg:grid-cols-3        /* Large: 3 columns */
  gap-4
">
```

在这些断点测试：320px、768px、1024px、1440px。

## 加载与过渡

```tsx
// Skeleton loading (not spinners for content)
function TaskListSkeleton() {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading tasks">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="h-12 bg-muted animate-pulse rounded" />
      ))}
    </div>
  );
}

// Optimistic updates for perceived speed
function useToggleTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleTask,
    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previous = queryClient.getQueryData(['tasks']);

      queryClient.setQueryData(['tasks'], (old: Task[]) =>
        old.map(t => t.id === taskId ? { ...t, done: !t.done } : t)
      );

      return { previous };
    },
    onError: (_err, _taskId, context) => {
      queryClient.setQueryData(['tasks'], context?.previous);
    },
  });
}
```

## 另请参阅

关于详细的可访问性要求与测试工具，请参阅 `references/accessibility-checklist.md`。

## 常见自我辩解

| 自我辩解 | 现实 |
|---|---|
| "可访问性是个 nice-to-have" | 在许多司法管辖区它是法律要求，也是工程质量标准。 |
| "我们之后再做响应式" | 给现有 UI 改造响应式比从一开始就构建要难 3 倍。 |
| "设计还没定，所以我先跳过样式" | 使用设计系统默认值。无样式的 UI 给评审者留下糟糕的第一印象。 |
| "这只是原型" | 原型最终会变成生产代码。一开始就把基础打对。 |
| "AI 美学暂时没问题" | 它传达的是低质量。从一开始就使用项目实际的设计系统。 |

## 危险信号

- 组件超过 200 行（需要拆分）
- 内联样式或随意编造的像素值
- 缺少错误状态、加载状态或空状态
- 没有键盘导航测试
- 仅用颜色作为状态指示（仅红/绿，没有文字或图标）
- 千篇一律的"AI 观感"（紫色渐变、超大卡片、模板化布局）

## 验证

构建 UI 完成后：

- [ ] 组件渲染时控制台无报错
- [ ] 所有交互元素都支持键盘访问（在页面中按 Tab 键）
- [ ] 屏幕阅读器能传达页面的内容和结构
- [ ] 响应式：在 320px、768px、1024px、1440px 下都正常
- [ ] 已处理加载、错误与空状态
- [ ] 遵循项目的设计系统（间距、颜色、排版）
- [ ] 在开发工具或 axe-core 中没有可访问性警告

## 局限

- 仅在任务明确匹配其上游来源与本地项目上下文时使用此技能
- 在应用更改前验证命令、生成的代码、依赖、凭据以及外部服务的行为
- 不要将示例作为环境特定测试、安全审查或破坏性/高成本操作的用户批准的替代
