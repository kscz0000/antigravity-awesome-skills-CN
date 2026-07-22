# 组件组合

## 目录

- 项目始终在其 Group 组件内
- 提示框使用 Alert
- 空状态使用 Empty 组件
- Toast 通知使用 sonner
- 选择覆盖层组件
- Dialog、Sheet 和 Drawer 始终需要 Title
- Card 结构
- Button 没有 isPending 或 isLoading 属性
- TabsTrigger 必须在 TabsList 内
- Avatar 始终需要 AvatarFallback
- 使用 Separator 而非原始 hr 或 border div
- 使用 Skeleton 作为加载占位符
- 使用 Badge 而非自定义样式的 span

---

## 项目始终在其 Group 组件内

绝不要将项目直接渲染在内容容器内。

**错误：**

```tsx
<SelectContent>
  <SelectItem value="apple">Apple</SelectItem>
  <SelectItem value="banana">Banana</SelectItem>
</SelectContent>
```

**正确：**

```tsx
<SelectContent>
  <SelectGroup>
    <SelectItem value="apple">Apple</SelectItem>
    <SelectItem value="banana">Banana</SelectItem>
  </SelectGroup>
</SelectContent>
```

这适用于所有基于 Group 的组件：

| Item | Group |
|------|-------|
| `SelectItem`、`SelectLabel` | `SelectGroup` |
| `DropdownMenuItem`、`DropdownMenuLabel`、`DropdownMenuSub` | `DropdownMenuGroup` |
| `MenubarItem` | `MenubarGroup` |
| `ContextMenuItem` | `ContextMenuGroup` |
| `CommandItem` | `CommandGroup` |

---

## 提示框使用 Alert

```tsx
<Alert>
  <AlertTitle>Warning</AlertTitle>
  <AlertDescription>Something needs attention.</AlertDescription>
</Alert>
```

---

## 空状态使用 Empty 组件

```tsx
<Empty>
  <EmptyHeader>
    <EmptyMedia variant="icon"><FolderIcon /></EmptyMedia>
    <EmptyTitle>No projects yet</EmptyTitle>
    <EmptyDescription>Get started by creating a new project.</EmptyDescription>
  </EmptyHeader>
  <EmptyContent>
    <Button>Create Project</Button>
  </EmptyContent>
</Empty>
```

---

## Toast 通知使用 sonner

```tsx
import { toast } from "sonner"

toast.success("Changes saved.")
toast.error("Something went wrong.")
toast("File deleted.", {
  action: { label: "Undo", onClick: () => undoDelete() },
})
```

---

## 选择覆盖层组件

| 用例 | 组件 |
|----------|-----------|
| 需要输入的聚焦任务 | `Dialog` |
| 破坏性操作确认 | `AlertDialog` |
| 带详情或筛选器的侧边面板 | `Sheet` |
| 移动端优先的底部面板 | `Drawer` |
| 悬停时快速显示信息 | `HoverCard` |
| 点击时的小型上下文内容 | `Popover` |

---

## Dialog、Sheet 和 Drawer 始终需要 Title

`DialogTitle`、`SheetTitle`、`DrawerTitle` 是无障碍必需的。视觉隐藏时使用 `className="sr-only"`。

```tsx
<DialogContent>
  <DialogHeader>
    <DialogTitle>Edit Profile</DialogTitle>
    <DialogDescription>Update your profile.</DialogDescription>
  </DialogHeader>
  ...
</DialogContent>
```

---

## Card 结构

使用完整组合 —— 不要把所有内容都塞进 `CardContent`：

```tsx
<Card>
  <CardHeader>
    <CardTitle>Team Members</CardTitle>
    <CardDescription>Manage your team.</CardDescription>
  </CardHeader>
  <CardContent>...</CardContent>
  <CardFooter>
    <Button>Invite</Button>
  </CardFooter>
</Card>
```

---

## Button 没有 isPending 或 isLoading 属性

使用 `Spinner` + `data-icon` + `disabled` 组合：

```tsx
<Button disabled>
  <Spinner data-icon="inline-start" />
  Saving...
</Button>
```

---

## TabsTrigger 必须在 TabsList 内

绝不要直接在 `Tabs` 中渲染 `TabsTrigger` —— 始终包装在 `TabsList` 中：

```tsx
<Tabs defaultValue="account">
  <TabsList>
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
  </TabsList>
  <TabsContent value="account">...</TabsContent>
</Tabs>
```

---

## Avatar 始终需要 AvatarFallback

始终包含 `AvatarFallback` 用于图片加载失败时：

```tsx
<Avatar>
  <AvatarImage src="/avatar.png" alt="User" />
  <AvatarFallback>JD</AvatarFallback>
</Avatar>
```

---

## 使用现有组件而非自定义标记

| 而非 | 使用 |
|---|---|
| `<hr>` 或 `<div className="border-t">` | `<Separator />` |
| 带 styled divs 的 `<div className="animate-pulse">` | `<Skeleton className="h-4 w-3/4" />` |
| `<span className="rounded-full bg-green-100 ...">` | `<Badge variant="secondary">` |
