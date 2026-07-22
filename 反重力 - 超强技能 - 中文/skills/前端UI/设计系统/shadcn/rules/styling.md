# 样式与自定义

主题、CSS 变量和添加自定义颜色请参阅 [customization.md](../customization.md)。

## 目录

- 语义化颜色
- 优先使用内置变体
- className 仅用于布局
- 禁止 space-x-* / space-y-*
- 相等时优先使用 size-* 而非 w-* h-*
- 优先使用 truncate 简写
- 禁止手动 dark: 颜色覆盖
- 使用 cn() 处理条件类名
- 覆盖层组件禁止手动 z-index

---

## 语义化颜色

**错误：**

```tsx
<div className="bg-blue-500 text-white">
  <p className="text-gray-600">Secondary text</p>
</div>
```

**正确：**

```tsx
<div className="bg-primary text-primary-foreground">
  <p className="text-muted-foreground">Secondary text</p>
</div>
```

---

## 状态/状态指示器禁止使用原始颜色值

对于正面、负面或状态指示器，使用 Badge 变体、语义化令牌如 `text-destructive`，或定义自定义 CSS 变量 —— 不要使用原始 Tailwind 颜色。

**错误：**

```tsx
<span className="text-emerald-600">+20.1%</span>
<span className="text-green-500">Active</span>
<span className="text-red-600">-3.2%</span>
```

**正确：**

```tsx
<Badge variant="secondary">+20.1%</Badge>
<Badge>Active</Badge>
<span className="text-destructive">-3.2%</span>
```

如果需要语义化令牌中不存在的成功/正面颜色，使用 Badge 变体或询问用户是否向主题添加自定义 CSS 变量（请参阅 [customization.md](../customization.md)）。

---

## 优先使用内置变体

**错误：**

```tsx
<Button className="border border-input bg-transparent hover:bg-accent">
  Click me
</Button>
```

**正确：**

```tsx
<Button variant="outline">Click me</Button>
```

---

## className 仅用于布局

使用 `className` 进行布局（如 `max-w-md`、`mx-auto`、`mt-4`），**而非**覆盖组件颜色或排版。要更改颜色，使用语义化令牌、内置变体或 CSS 变量。

**错误：**

```tsx
<Card className="bg-blue-100 text-blue-900 font-bold">
  <CardContent>Dashboard</CardContent>
</Card>
```

**正确：**

```tsx
<Card className="max-w-md mx-auto">
  <CardContent>Dashboard</CardContent>
</Card>
```

要自定义组件外观，按以下顺序优先使用这些方法：
1. **内置变体** —— `variant="outline"`、`variant="destructive"` 等。
2. **语义化颜色令牌** —— `bg-primary`、`text-muted-foreground`。
3. **CSS 变量** —— 在全局 CSS 文件中定义自定义颜色（请参阅 [customization.md](../customization.md)）。

---

## 禁止 space-x-* / space-y-*

改用 `gap-*`。`space-y-4` → `flex flex-col gap-4`。`space-x-2` → `flex gap-2`。

```tsx
<div className="flex flex-col gap-4">
  <Input />
  <Input />
  <Button>Submit</Button>
</div>
```

---

## 相等时优先使用 size-* 而非 w-* h-*

使用 `size-10` 而非 `w-10 h-10`。适用于图标、头像、骨架屏等。

---

## 优先使用 truncate 简写

使用 `truncate` 而非 `overflow-hidden text-ellipsis whitespace-nowrap`。

---

## 禁止手动 dark: 颜色覆盖

使用语义化令牌 —— 它们通过 CSS 变量处理亮/暗色。使用 `bg-background text-foreground` 而非 `bg-white dark:bg-gray-950`。

---

## 使用 cn() 处理条件类名

使用项目中的 `cn()` 工具处理条件或合并类名。不要在 className 字符串中手动编写三元表达式。

**错误：**

```tsx
<div className={`flex items-center ${isActive ? "bg-primary text-primary-foreground" : "bg-muted"}`}>
```

**正确：**

```tsx
import { cn } from "@/lib/utils"

<div className={cn("flex items-center", isActive ? "bg-primary text-primary-foreground" : "bg-muted")}>
```

---

## 覆盖层组件禁止手动 z-index

`Dialog`、`Sheet`、`Drawer`、`AlertDialog`、`DropdownMenu`、`Popover`、`Tooltip`、`HoverCard` 自行处理堆叠。绝不要添加 `z-50` 或 `z-[999]`。
