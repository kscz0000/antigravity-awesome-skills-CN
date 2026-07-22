---
name: radix-ui-design-system
description: "使用 Radix UI 原语构建无障碍设计系统。无头组件定制、主题策略与复合组件模式，打造生产级 UI 库。触发词：Radix UI、设计系统、无障碍组件、无头组件、主题系统、复合组件、UI 库、headless、a11y、设计系统构建"
risk: safe
source: self
date_added: "2026-02-27"
---

# Radix UI 设计系统

使用 Radix UI 原语构建生产级、无障碍的设计系统，完全掌控定制化，零样式束缚。

## 概述

Radix UI 提供无样式的无障碍组件（原语），你可以按需定制以匹配任何设计系统。本技能指导你使用 Radix UI 构建可扩展的组件库，聚焦无障碍优先设计、主题架构和可组合模式。

**核心优势：**
- **天生无头**：完全掌控样式，无需与默认样式对抗
- **内置无障碍**：符合 WAI-ARIA 标准，支持键盘导航和屏幕阅读器
- **可组合原语**：用简单积木搭建复杂组件
- **框架无关**：与 React 配合使用，但样式可适配任何框架

## 适用场景

- 从零创建自定义设计系统
- 构建无障碍 UI 组件库
- 实现复杂交互组件（Dialog、Dropdown、Tabs 等）
- 从有样式组件库迁移到无样式原语
- 使用 CSS 变量或 Tailwind 搭建主题系统
- 需要完全掌控组件行为和样式
- 构建需要 WCAG 2.1 AA/AAA 合规的应用

## 不适用场景

- 需要开箱即用的预制样式组件（请用 shadcn/ui、Mantine 等）
- 构建无交互的简单静态页面
- 项目未使用 React 16.8+（Radix 依赖 hooks）
- 需要 React 之外的框架组件

---

## 核心原则

### 1. 无障碍优先

每个 Radix 原语都以无障碍为基石：

- **键盘导航**：完整的键盘支持（Tab、方向键、Enter、Escape）
- **屏幕阅读器**：正确的 ARIA 属性和实时区域
- **焦点管理**：自动焦点捕获和恢复
- **禁用状态**：正确处理 disabled 和 aria-disabled

**原则**：永远不要覆盖无障碍功能。增强，而非替换。

### 2. 无头架构

Radix 提供**行为**，你提供**外观**：

```tsx
// ❌ Don't fight pre-styled components
<Button className="override-everything" />

// ✅ Radix gives you behavior, you add styling
<Dialog.Root>
  <Dialog.Trigger className="your-button-styles" />
  <Dialog.Content className="your-modal-styles" />
</Dialog.Root>
```

### 3. 组合优于配置

用简单原语搭建复杂组件：

```tsx
// Primitive components compose naturally
<Tabs.Root>
  <Tabs.List>
    <Tabs.Trigger value="tab1">Tab 1</Tabs.Trigger>
    <Tabs.Trigger value="tab2">Tab 2</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="tab1">Content 1</Tabs.Content>
  <Tabs.Content value="tab2">Content 2</Tabs.Content>
</Tabs.Root>
```

---

## 快速上手

### 安装

```bash
# Install individual primitives (recommended)
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu

# Or install multiple at once
npm install @radix-ui/react-{dialog,dropdown-menu,tabs,tooltip}

# For styling (optional but common)
npm install clsx tailwind-merge class-variance-authority
```

### 基础组件模式

每个 Radix 组件都遵循这个模式：

```tsx
import * as Dialog from '@radix-ui/react-dialog';

export function MyDialog() {
  return (
    <Dialog.Root>
      {/* Trigger the dialog */}
      <Dialog.Trigger asChild>
        <button className="trigger-styles">Open</button>
      </Dialog.Trigger>

      {/* Portal renders outside DOM hierarchy */}
      <Dialog.Portal>
        {/* Overlay (backdrop) */}
        <Dialog.Overlay className="overlay-styles" />
        
        {/* Content (modal) */}
        <Dialog.Content className="content-styles">
          <Dialog.Title>Title</Dialog.Title>
          <Dialog.Description>Description</Dialog.Description>
          
          {/* Your content here */}
          
          <Dialog.Close asChild>
            <button>Close</button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

## 主题策略

### 策略 1：CSS 变量（框架无关）

**最适合**：最大可移植性，SSR 友好

```css
/* globals.css */
:root {
  --color-primary: 220 90% 56%;
  --color-surface: 0 0% 100%;
  --radius-base: 0.5rem;
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

[data-theme="dark"] {
  --color-primary: 220 90% 66%;
  --color-surface: 222 47% 11%;
}
```

```tsx
// Component.tsx
<Dialog.Content 
  className="
    bg-[hsl(var(--color-surface))]
    rounded-[var(--radius-base)]
    shadow-[var(--shadow-lg)]
  "
/>
```

### 策略 2：Tailwind + CVA（Class Variance Authority）

**最适合**：Tailwind 项目，变体丰富的组件

```tsx
// button.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // Base styles
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

interface ButtonProps extends VariantProps<typeof buttonVariants> {
  children: React.ReactNode;
}

export function Button({ variant, size, children }: ButtonProps) {
  return (
    <button className={cn(buttonVariants({ variant, size }))}>
      {children}
    </button>
  );
}
```

### 策略 3：Stitches（CSS-in-JS）

**最适合**：运行时主题，作用域样式

```tsx
import { styled } from '@stitches/react';
import * as Dialog from '@radix-ui/react-dialog';

const StyledContent = styled(Dialog.Content, {
  backgroundColor: '$surface',
  borderRadius: '$md',
  padding: '$6',
  
  variants: {
    size: {
      small: { width: '300px' },
      medium: { width: '500px' },
      large: { width: '700px' },
    },
  },
  
  defaultVariants: {
    size: 'medium',
  },
});
```

---

## 组件模式

### 模式 1：带 Context 的复合组件

**适用场景**：在原语各部分之间共享状态

```tsx
// Select.tsx
import * as Select from '@radix-ui/react-select';
import { CheckIcon, ChevronDownIcon } from '@radix-ui/react-icons';

export function CustomSelect({ items, placeholder, onValueChange }) {
  return (
    <Select.Root onValueChange={onValueChange}>
      <Select.Trigger className="select-trigger">
        <Select.Value placeholder={placeholder} />
        <Select.Icon>
          <ChevronDownIcon />
        </Select.Icon>
      </Select.Trigger>

      <Select.Portal>
        <Select.Content className="select-content">
          <Select.Viewport>
            {items.map((item) => (
              <Select.Item 
                key={item.value} 
                value={item.value}
                className="select-item"
              >
                <Select.ItemText>{item.label}</Select.ItemText>
                <Select.ItemIndicator>
                  <CheckIcon />
                </Select.ItemIndicator>
              </Select.Item>
            ))}
          </Select.Viewport>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
}
```

### 模式 2：用 `asChild` 实现多态组件

**适用场景**：渲染为不同元素而不丢失行为

```tsx
// ✅ Render as Next.js Link but keep Radix behavior
<Dialog.Trigger asChild>
  <Link href="/settings">Open Settings</Link>
</Dialog.Trigger>

// ✅ Render as custom component
<DropdownMenu.Item asChild>
  <YourCustomButton icon={<Icon />}>Action</YourCustomButton>
</DropdownMenu.Item>
```

**`asChild` 的意义**：避免无障碍树中出现嵌套 button/link 的问题。

### 模式 3：受控 vs 非受控

```tsx
// Uncontrolled (Radix manages state)
<Tabs.Root defaultValue="tab1">
  <Tabs.Trigger value="tab1">Tab 1</Tabs.Trigger>
</Tabs.Root>

// Controlled (You manage state)
const [activeTab, setActiveTab] = useState('tab1');

<Tabs.Root value={activeTab} onValueChange={setActiveTab}>
  <Tabs.Trigger value="tab1">Tab 1</Tabs.Trigger>
</Tabs.Root>
```

**原则**：需要与外部状态（URL、Redux 等）同步时使用受控模式。

### 模式 4：Framer Motion 动画

```tsx
import * as Dialog from '@radix-ui/react-dialog';
import { motion, AnimatePresence } from 'framer-motion';

export function AnimatedDialog({ open, onOpenChange }) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal forceMount>
        <AnimatePresence>
          {open && (
            <>
              <Dialog.Overlay asChild>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="dialog-overlay"
                />
              </Dialog.Overlay>
              
              <Dialog.Content asChild>
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className="dialog-content"
                >
                  {/* Content */}
                </motion.div>
              </Dialog.Content>
            </>
          )}
        </AnimatePresence>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

## 常用原语速查

### Dialog（模态框）

```tsx
<Dialog.Root> {/* State container */}
  <Dialog.Trigger /> {/* Opens dialog */}
  <Dialog.Portal> {/* Renders in portal */}
    <Dialog.Overlay /> {/* Backdrop */}
    <Dialog.Content> {/* Modal content */}
      <Dialog.Title /> {/* Required for a11y */}
      <Dialog.Description /> {/* Required for a11y */}
      <Dialog.Close /> {/* Closes dialog */}
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

### Dropdown Menu（下拉菜单）

```tsx
<DropdownMenu.Root>
  <DropdownMenu.Trigger />
  <DropdownMenu.Portal>
    <DropdownMenu.Content>
      <DropdownMenu.Item />
      <DropdownMenu.Separator />
      <DropdownMenu.CheckboxItem />
      <DropdownMenu.RadioGroup>
        <DropdownMenu.RadioItem />
      </DropdownMenu.RadioGroup>
      <DropdownMenu.Sub> {/* Nested menus */}
        <DropdownMenu.SubTrigger />
        <DropdownMenu.SubContent />
      </DropdownMenu.Sub>
    </DropdownMenu.Content>
  </DropdownMenu.Portal>
</DropdownMenu.Root>
```

### Tabs（标签页）

```tsx
<Tabs.Root defaultValue="tab1">
  <Tabs.List>
    <Tabs.Trigger value="tab1" />
    <Tabs.Trigger value="tab2" />
  </Tabs.List>
  <Tabs.Content value="tab1" />
  <Tabs.Content value="tab2" />
</Tabs.Root>
```

### Tooltip（工具提示）

```tsx
<Tooltip.Provider delayDuration={200}>
  <Tooltip.Root>
    <Tooltip.Trigger />
    <Tooltip.Portal>
      <Tooltip.Content side="top" align="center">
        Tooltip text
        <Tooltip.Arrow />
      </Tooltip.Content>
    </Tooltip.Portal>
  </Tooltip.Root>
</Tooltip.Provider>
```

### Popover（弹出层）

```tsx
<Popover.Root>
  <Popover.Trigger />
  <Popover.Portal>
    <Popover.Content side="bottom" align="start">
      Content
      <Popover.Arrow />
      <Popover.Close />
    </Popover.Content>
  </Popover.Portal>
</Popover.Root>
```

---

## 无障碍检查清单

### 每个组件必须具备：

- [ ] **焦点管理**：所有交互元素上可见的焦点指示器
- [ ] **键盘导航**：完整的键盘支持（Tab、方向键、Enter、Esc）
- [ ] **ARIA 标签**：为屏幕阅读器提供有意义的标签
- [ ] **颜色对比度**：WCAG AA 最低标准（文本 4.5:1，UI 3:1）
- [ ] **错误状态**：通过 `aria-invalid` 和 `aria-describedby` 提供清晰的错误信息
- [ ] **加载状态**：异步操作期间正确使用 `aria-busy`

### Dialog 专项：
- [ ] `Dialog.Title` 已存在（屏幕阅读器必需）
- [ ] `Dialog.Description` 提供上下文信息
- [ ] 打开时焦点被限制在模态框内
- [ ] Escape 键关闭对话框
- [ ] 关闭后焦点回到触发元素

### Dropdown 专项：
- [ ] 方向键导航项目
- [ ] 输入搜索可用
- [ ] 首尾项循环行为
- [ ] 选中状态同时用视觉和 ARIA 表示

---

## 最佳实践

### ✅ 推荐做法

1. **始终使用 `asChild` 避免多余的 wrapper div**
   ```tsx
   <Dialog.Trigger asChild>
     <button>Open</button>
   </Dialog.Trigger>
   ```

2. **提供语义化 HTML**
   ```tsx
   <Dialog.Content asChild>
     <article role="dialog" aria-labelledby="title">
       {/* content */}
     </article>
   </Dialog.Content>
   ```

3. **使用 CSS 变量做主题**
   ```css
   .dialog-content {
     background: hsl(var(--surface));
     color: hsl(var(--on-surface));
   }
   ```

4. **组合原语构建复杂组件**
   ```tsx
   function CommandPalette() {
     return (
       <Dialog.Root>
         <Dialog.Content>
           <Combobox /> {/* Radix Combobox inside Dialog */}
         </Dialog.Content>
       </Dialog.Root>
     );
   }
   ```

### ❌ 避免做法

1. **不要跳过无障碍部分**
   ```tsx
   // ❌ Missing Title and Description
   <Dialog.Content>
     <div>Content</div>
   </Dialog.Content>
   ```

2. **不要与原语对抗**
   ```tsx
   // ❌ Overriding internal behavior
   <Dialog.Content onClick={(e) => e.stopPropagation()}>
   ```

3. **不要混合受控和非受控**
   ```tsx
   // ❌ Inconsistent state management
   <Tabs.Root defaultValue="tab1" value={activeTab}>
   ```

4. **不要忽略键盘导航**
   ```tsx
   // ❌ Disabling keyboard behavior
   <DropdownMenu.Item onKeyDown={(e) => e.preventDefault()}>
   ```

---

## 实战示例

### 示例 1：Command Palette（命令面板）

```tsx
import * as Dialog from '@radix-ui/react-dialog';
import { Command } from 'cmdk';

export function CommandPalette() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
          <Command>
            <Command.Input placeholder="Type a command..." />
            <Command.List>
              <Command.Empty>No results found.</Command.Empty>
              <Command.Group heading="Suggestions">
                <Command.Item>Calendar</Command.Item>
                <Command.Item>Search Emoji</Command.Item>
              </Command.Group>
            </Command.List>
          </Command>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### 示例 2：带图标的下拉菜单

```tsx
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import { DotsHorizontalIcon } from '@radix-ui/react-icons';

export function ActionsMenu() {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="icon-button" aria-label="Actions">
          <DotsHorizontalIcon />
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content className="dropdown-content" align="end">
          <DropdownMenu.Item className="dropdown-item">
            Edit
          </DropdownMenu.Item>
          <DropdownMenu.Item className="dropdown-item">
            Duplicate
          </DropdownMenu.Item>
          <DropdownMenu.Separator className="dropdown-separator" />
          <DropdownMenu.Item className="dropdown-item text-red-500">
            Delete
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

### 示例 3：Radix Select + React Hook Form 表单

```tsx
import * as Select from '@radix-ui/react-select';
import { useForm, Controller } from 'react-hook-form';

interface FormData {
  country: string;
}

export function CountryForm() {
  const { control, handleSubmit } = useForm<FormData>();

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <Controller
        name="country"
        control={control}
        render={({ field }) => (
          <Select.Root onValueChange={field.onChange} value={field.value}>
            <Select.Trigger className="select-trigger">
              <Select.Value placeholder="Select a country" />
              <Select.Icon />
            </Select.Trigger>
            
            <Select.Portal>
              <Select.Content className="select-content">
                <Select.Viewport>
                  <Select.Item value="us">United States</Select.Item>
                  <Select.Item value="ca">Canada</Select.Item>
                  <Select.Item value="uk">United Kingdom</Select.Item>
                </Select.Viewport>
              </Select.Content>
            </Select.Portal>
          </Select.Root>
        )}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## 常见问题排查

### 问题：Dialog 按 Escape 键不关闭

**原因**：`onEscapeKeyDown` 事件被阻止，或 `open` 状态未同步

**解决方案**：
```tsx
<Dialog.Root open={open} onOpenChange={setOpen}>
  {/* Don't prevent default on escape */}
</Dialog.Root>
```

### 问题：Dropdown 菜单定位偏移

**原因**：父容器设置了 `overflow: hidden` 或 transform

**解决方案**：
```tsx
// Use Portal to render outside overflow container
<DropdownMenu.Portal>
  <DropdownMenu.Content />
</DropdownMenu.Portal>
```

### 问题：动画不生效

**原因**：Portal 内容被立即卸载

**解决方案**：
```tsx
// Use forceMount + AnimatePresence
<Dialog.Portal forceMount>
  <AnimatePresence>
    {open && <Dialog.Content />}
  </AnimatePresence>
</Dialog.Portal>
```

### 问题：`asChild` 导致 TypeScript 报错

**原因**：多态组件的类型推断问题

**解决方案**：
```tsx
// Explicitly type your component
<Dialog.Trigger asChild>
  <button type="button">Open</button>
</Dialog.Trigger>
```

---

## 性能优化

### 1. 代码分割

```tsx
// Lazy load heavy primitives
const Dialog = lazy(() => import('@radix-ui/react-dialog'));
const DropdownMenu = lazy(() => import('@radix-ui/react-dropdown-menu'));
```

### 2. Portal 容器复用

```tsx
// Create portal container once
<Tooltip.Provider>
  {/* All tooltips share portal container */}
  <Tooltip.Root>...</Tooltip.Root>
  <Tooltip.Root>...</Tooltip.Root>
</Tooltip.Provider>
```

### 3. 记忆化

```tsx
// Memoize expensive render functions
const SelectItems = memo(({ items }) => (
  items.map((item) => <Select.Item key={item.value} value={item.value} />)
));
```

---

## 与流行工具集成

### shadcn/ui（基于 Radix 构建）

shadcn/ui 是基于 Radix + Tailwind 的即用型组件集合。

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add dialog
```

**何时用 shadcn vs 原始 Radix**：
- 用 shadcn：快速原型开发，标准设计
- 用原始 Radix：完全定制，独特设计

### Radix Themes（官方样式化系统）

```tsx
import { Theme, Button, Dialog } from '@radix-ui/themes';

function App() {
  return (
    <Theme accentColor="crimson" grayColor="sand">
      <Button>Click me</Button>
    </Theme>
  );
}
```

---

## 相关技能

- `@tailwind-design-system` - Tailwind + Radix 集成模式
- `@react-patterns` - React 组合模式
- `@frontend-design` - 整体前端架构
- `@accessibility-compliance` - WCAG 合规测试

---

## 资源

### 官方文档
- [Radix UI Docs](https://www.radix-ui.com/primitives)
- [Radix Colors](https://www.radix-ui.com/colors) - 无障碍颜色系统
- [Radix Icons](https://www.radix-ui.com/icons) - 图标库

### 社区资源
- [shadcn/ui](https://ui.shadcn.com) - 组件集合
- [Radix UI Discord](https://discord.com/invite/7Xb99uG) - 社区支持
- [CVA Documentation](https://cva.style/docs) - 变体管理

### 示例
- [Radix Playground](https://www.radix-ui.com/primitives/docs/overview/introduction#try-it-out)
- [shadcn/ui Source](https://github.com/shadcn-ui/ui) - 生产级示例

---

## 快速参考

### 安装
```bash
npm install @radix-ui/react-{primitive-name}
```

### 基础模式
```tsx
<Primitive.Root>
  <Primitive.Trigger />
  <Primitive.Portal>
    <Primitive.Content />
  </Primitive.Portal>
</Primitive.Root>
```

### 关键 Props
- `asChild` - 渲染为子元素
- `defaultValue` - 非受控默认值
- `value` / `onValueChange` - 受控状态
- `open` / `onOpenChange` - 打开状态
- `side` / `align` - 定位

---

**记住**：Radix 给你**行为**，你赋予它**美**。无障碍内置，定制无上限。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
