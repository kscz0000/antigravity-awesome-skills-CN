---
name: shadcn
description: 管理 shadcn/ui 组件和项目，提供构建现代设计系统的上下文、文档和使用模式。触发词：shadcn、shadcn/ui、UI组件库、设计系统、组件添加、shadcn组件、shadcn初始化、shadcn CLI
user-invocable: false
risk: safe
source: https://github.com/shadcn-ui/ui/tree/main/skills/shadcn
date_added: "2026-03-07"
---

# shadcn/ui

一个用于构建 UI、组件和设计系统的框架。组件通过 CLI 以源代码形式添加到用户项目中。

> **重要提示：** 所有 CLI 命令必须使用项目的包管理器运行：`npx shadcn@latest`、`pnpm dlx shadcn@latest` 或 `bunx --bun shadcn@latest` —— 根据项目的 `packageManager` 选择。下方示例使用 `npx shadcn@latest`，但请替换为项目正确的运行器。

## 何时使用

- 从 shadcn/ui 或社区注册表添加新组件时使用。
- 样式化、组合或调试现有 shadcn/ui 组件时使用。
- 初始化新项目或切换设计系统预设时使用。
- 获取组件文档、示例和 API 参考时使用。

## 当前项目上下文

```json
!`npx shadcn@latest info --json 2>/dev/null || echo '{"error": "No shadcn project found. Run shadcn init first."}'`
```

上方的 JSON 包含项目配置和已安装组件。使用 `npx shadcn@latest docs <component>` 获取任何组件的文档和示例 URL。

## 原则

1. **优先使用现有组件。** 编写自定义 UI 前先使用 `npx shadcn@latest search` 检查注册表。也要检查社区注册表。
2. **组合而非重造。** 设置页面 = Tabs + Card + 表单控件。仪表盘 = Sidebar + Card + Chart + Table。
3. **优先使用内置变体。** `variant="outline"`、`size="sm"` 等。
4. **使用语义化颜色。** `bg-primary`、`text-muted-foreground` —— 绝不使用 `bg-blue-500` 等原始值。

## 关键规则

这些规则**始终强制执行**。每条规则都链接到包含错误/正确代码对的文件。

### 样式与 Tailwind → [styling.md](./rules/styling.md)

- **`className` 仅用于布局，不用于样式。** 绝不覆盖组件颜色或排版。
- **禁止 `space-x-*` 或 `space-y-*`。** 使用带 `gap-*` 的 `flex`。垂直堆叠使用 `flex flex-col gap-*`。
- **宽高相等时使用 `size-*`。** 使用 `size-10` 而非 `w-10 h-10`。
- **使用 `truncate` 简写。** 而非 `overflow-hidden text-ellipsis whitespace-nowrap`。
- **禁止手动 `dark:` 颜色覆盖。** 使用语义化令牌（`bg-background`、`text-muted-foreground`）。
- **使用 `cn()` 处理条件类名。** 不要手动编写模板字符串三元表达式。
- **覆盖层组件禁止手动 `z-index`。** Dialog、Sheet、Popover 等自行处理堆叠。

### 表单与输入 → [forms.md](./rules/forms.md)

- **表单使用 `FieldGroup` + `Field`。** 绝不使用带 `space-y-*` 或 `grid gap-*` 的原始 `div` 作为表单布局。
- **`InputGroup` 使用 `InputGroupInput`/`InputGroupTextarea`。** `InputGroup` 内禁止使用原始 `Input`/`Textarea`。
- **输入框内的按钮使用 `InputGroup` + `InputGroupAddon`。**
- **选项集（2-4 个选择）使用 `ToggleGroup`。** 不要循环 `Button` 并手动管理激活状态。
- **使用 `FieldSet` + `FieldLegend` 分组相关复选框/单选按钮。** 不要使用带标题的 `div`。
- **字段验证使用 `data-invalid` + `aria-invalid`。** `Field` 上设置 `data-invalid`，控件上设置 `aria-invalid`。禁用状态：`Field` 上设置 `data-disabled`，控件上设置 `disabled`。

### 组件结构 → [composition.md](./rules/composition.md)

- **项目始终在其 Group 内。** `SelectItem` → `SelectGroup`。`DropdownMenuItem` → `DropdownMenuGroup`。`CommandItem` → `CommandGroup`。
- **使用 `asChild`（radix）或 `render`（base）作为自定义触发器。** 通过 `npx shadcn@latest info` 检查 `base` 字段。→ [base-vs-radix.md](./rules/base-vs-radix.md)
- **Dialog、Sheet 和 Drawer 始终需要 Title。** `DialogTitle`、`SheetTitle`、`DrawerTitle` 是无障碍必需的。视觉隐藏时使用 `className="sr-only"`。
- **使用完整 Card 组合。** `CardHeader`/`CardTitle`/`CardDescription`/`CardContent`/`CardFooter`。不要把所有内容都塞进 `CardContent`。
- **Button 没有 `isPending`/`isLoading`。** 使用 `Spinner` + `data-icon` + `disabled` 组合。
- **`TabsTrigger` 必须在 `TabsList` 内。** 绝不直接在 `Tabs` 中渲染触发器。
- **`Avatar` 始终需要 `AvatarFallback`。** 用于图片加载失败时。

### 使用组件而非自定义标记 → [composition.md](./rules/composition.md)

- **编写自定义标记前先使用现有组件。** 编写带样式的 `div` 前检查组件是否存在。
- **提示框使用 `Alert`。** 不要构建自定义样式的 div。
- **空状态使用 `Empty`。** 不要构建自定义空状态标记。
- **Toast 通过 `sonner`。** 使用 `sonner` 的 `toast()`。
- **使用 `Separator`** 而非 `<hr>` 或 `<div className="border-t">`。
- **使用 `Skeleton`** 作为加载占位符。不要使用自定义 `animate-pulse` div。
- **使用 `Badge`** 而非自定义样式的 span。

### 图标 → [icons.md](./rules/icons.md)

- **`Button` 中的图标使用 `data-icon`。** 图标上设置 `data-icon="inline-start"` 或 `data-icon="inline-end"`。
- **组件内图标禁止添加尺寸类。** 组件通过 CSS 处理图标尺寸。不要添加 `size-4` 或 `w-4 h-4`。
- **图标作为对象传递，而非字符串键。** 使用 `icon={CheckIcon}`，而非字符串查找。

### CLI

- **绝不手动解码或获取预设代码。** 直接传递给 `npx shadcn@latest init --preset <code>`。

## 关键模式

这些是区分正确 shadcn/ui 代码的最常见模式。边缘情况请参阅上方链接的规则文件。

```tsx
// 表单布局：FieldGroup + Field，而非 div + Label。
<FieldGroup>
  <Field>
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" />
  </Field>
</FieldGroup>

// 验证：Field 上 data-invalid，控件上 aria-invalid。
<Field data-invalid>
  <FieldLabel>Email</FieldLabel>
  <Input aria-invalid />
  <FieldDescription>Invalid email.</FieldDescription>
</Field>

// 按钮中的图标：data-icon，无尺寸类。
<Button>
  <SearchIcon data-icon="inline-start" />
  Search
</Button>

// 间距：gap-*，而非 space-y-*。
<div className="flex flex-col gap-4">  // 正确
<div className="space-y-4">           // 错误

// 相等尺寸：size-*，而非 w-* h-*。
<Avatar className="size-10">   // 正确
<Avatar className="w-10 h-10"> // 错误

// 状态颜色：Badge 变体或语义化令牌，而非原始颜色。
<Badge variant="secondary">+20.1%</Badge>    // 正确
<span className="text-emerald-600">+20.1%</span> // 错误
```

## 组件选择

| 需求                       | 使用                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------------------- |
| 按钮/操作              | 带适当变体的 `Button`                                                                   |
| 表单输入                | `Input`, `Select`, `Combobox`, `Switch`, `Checkbox`, `RadioGroup`, `Textarea`, `InputOTP`, `Slider` |
| 2-4 个选项之间切换 | `ToggleGroup` + `ToggleGroupItem`                                                                   |
| 数据展示               | `Table`, `Card`, `Badge`, `Avatar`                                                                  |
| 导航                 | `Sidebar`, `NavigationMenu`, `Breadcrumb`, `Tabs`, `Pagination`                                     |
| 覆盖层                   | `Dialog`（模态框）, `Sheet`（侧边面板）, `Drawer`（底部抽屉）, `AlertDialog`（确认框）       |
| 反馈                   | `sonner`（toast）, `Alert`, `Progress`, `Skeleton`, `Spinner`                                        |
| 命令面板            | `Dialog` 内的 `Command`                                                                           |
| 图表                     | `Chart`（封装 Recharts）                                                                            |
| 布局                     | `Card`, `Separator`, `Resizable`, `ScrollArea`, `Accordion`, `Collapsible`                          |
| 空状态               | `Empty`                                                                                             |
| 菜单                      | `DropdownMenu`, `ContextMenu`, `Menubar`                                                            |
| 提示/信息              | `Tooltip`, `HoverCard`, `Popover`                                                                   |

## 关键字段

注入的项目上下文包含以下关键字段：

- **`aliases`** → 使用实际的别名前缀进行导入（如 `@/`、`~/`），绝不硬编码。
- **`isRSC`** → 当为 `true` 时，使用 `useState`、`useEffect`、事件处理器或浏览器 API 的组件需要在文件顶部添加 `"use client"`。在建议指令时始终引用此字段。
- **`tailwindVersion`** → `"v4"` 使用 `@theme inline` 块；`"v3"` 使用 `tailwind.config.js`。
- **`tailwindCssFile`** → 定义自定义 CSS 变量的全局 CSS 文件。始终编辑此文件，绝不创建新文件。
- **`style`** → 组件视觉处理（如 `nova`、`vega`）。
- **`base`** → 原语库（`radix` 或 `base`）。影响组件 API 和可用属性。
- **`iconLibrary`** → 决定图标导入。`lucide` 使用 `lucide-react`，`tabler` 使用 `@tabler/icons-react` 等。绝不假设 `lucide-react`。
- **`resolvedPaths`** → 组件、工具、钩子等的精确文件系统路径。
- **`framework`** → 路由和文件约定（如 Next.js App Router vs Vite SPA）。
- **`packageManager`** → 用于任何非 shadcn 依赖安装（如 `pnpm add date-fns` vs `npm install date-ffs`）。

完整字段参考请参阅 [cli.md → `info` 命令](./cli.md)。

## 组件文档、示例和用法

运行 `npx shadcn@latest docs <component>` 获取组件文档、示例和 API 参考的 URL。获取这些 URL 以获取实际内容。

```bash
npx shadcn@latest docs button dialog select
```

**创建、修复、调试或使用组件时，始终先运行 `npx shadcn@latest docs` 并获取 URL。** 这确保使用正确的 API 和使用模式，而非猜测。

## 工作流程

1. **获取项目上下文** —— 已在上方注入。如需刷新可再次运行 `npx shadcn@latest info`。
2. **先检查已安装组件** —— 运行 `add` 前，始终检查项目上下文中的 `components` 列表或列出 `resolvedPaths.ui` 目录。不要导入尚未添加的组件，也不要重新添加已安装的组件。
3. **查找组件** —— `npx shadcn@latest search`。
4. **获取文档和示例** —— 运行 `npx shadcn@latest docs <component>` 获取 URL，然后获取它们。使用 `npx shadcn@latest view` 浏览尚未安装的注册表项目。要预览已安装组件的更改，使用 `npx shadcn@latest add --diff`。
5. **安装或更新** —— `npx shadcn@latest add`。更新现有组件时，使用 `--dry-run` 和 `--diff` 先预览更改（见下方[更新组件](#更新组件)）。
6. **修复第三方组件中的导入** —— 从社区注册表（如 `@bundui`、`@magicui`）添加组件后，检查添加的非 UI 文件中是否有硬编码的导入路径如 `@/components/ui/...`。这些不会匹配项目的实际别名。使用 `npx shadcn@latest info` 获取正确的 `ui` 别名（如 `@workspace/ui/components`）并相应重写导入。CLI 会重写其自身 UI 文件的导入，但第三方注册表组件可能使用与项目不匹配的默认路径。
7. **审查添加的组件** —— 从任何注册表添加组件或块后，**始终读取添加的文件并验证其正确性**。检查缺失的子组件（如没有 `SelectGroup` 的 `SelectItem`）、缺失的导入、错误的组合或违反[关键规则](#关键规则)的情况。同时将任何图标导入替换为项目上下文中的 `iconLibrary`（如注册表项目使用 `lucide-react` 但项目使用 `hugeicons`，则交换导入和图标名称）。在继续之前修复所有问题。
8. **注册表必须明确** —— 当用户要求添加块或组件时，**不要猜测注册表**。如果未指定注册表（如用户说"添加登录块"但未指定 `@shadcn`、`@tailark` 等），询问使用哪个注册表。绝不要代表用户默认使用某个注册表。
9. **切换预设** —— 先询问用户：**重新安装**、**合并**还是**跳过**？
   - **重新安装**：`npx shadcn@latest init --preset <code> --force --reinstall`。覆盖所有组件。
   - **合并**：`npx shadcn@latest init --preset <code> --force --no-reinstall`，然后运行 `npx shadcn@latest info` 列出已安装组件，对每个已安装组件使用 `--dry-run` 和 `--diff` 进行[智能合并](#更新组件)。
   - **跳过**：`npx shadcn@latest init --preset <code> --force --no-reinstall`。仅更新配置和 CSS，保留组件原样。

## 更新组件

当用户要求从上游更新组件同时保留本地更改时，使用 `--dry-run` 和 `--diff` 进行智能合并。**绝不要手动从 GitHub 获取原始文件 —— 始终使用 CLI。**

1. 运行 `npx shadcn@latest add <component> --dry-run` 查看所有受影响的文件。
2. 对每个文件，运行 `npx shadcn@latest add <component> --diff <file>` 查看上游与本地的差异。
3. 根据差异对每个文件做出决定：
   - 无本地更改 → 安全覆盖。
   - 有本地更改 → 读取本地文件，分析差异，应用上游更新同时保留本地修改。
   - 用户说"全部更新" → 使用 `--overwrite`，但先确认。
4. **未经用户明确批准，绝不使用 `--overwrite`。**

## 快速参考

```bash
# 创建新项目。
npx shadcn@latest init --name my-app --preset base-nova
npx shadcn@latest init --name my-app --preset a2r6bw --template vite

# 创建 monorepo 项目。
npx shadcn@latest init --name my-app --preset base-nova --monorepo
npx shadcn@latest init --name my-app --preset base-nova --template next --monorepo

# 初始化现有项目。
npx shadcn@latest init --preset base-nova
npx shadcn@latest init --defaults  # 快捷方式：--template=next --preset=base-nova

# 添加组件。
npx shadcn@latest add button card dialog
npx shadcn@latest add @magicui/shimmer-button
npx shadcn@latest add --all

# 添加/更新前预览更改。
npx shadcn@latest add button --dry-run
npx shadcn@latest add button --diff button.tsx
npx shadcn@latest add @acme/form --view button.tsx

# 搜索注册表。
npx shadcn@latest search @shadcn -q "sidebar"
npx shadcn@latest search @tailark -q "stats"

# 获取组件文档和示例 URL。
npx shadcn@latest docs button dialog select

# 查看注册表项目详情（尚未安装的项目）。
npx shadcn@latest view @shadcn/button
```

**命名预设：** `base-nova`、`radix-nova`
**模板：** `next`、`vite`、`start`、`react-router`、`astro`（均支持 `--monorepo`）和 `laravel`（不支持 monorepo）
**预设代码：** 以 `a` 开头的 Base62 字符串（如 `a2r6bw`），来自 [ui.shadcn.com](https://ui.shadcn.com)。

## 详细参考

- [rules/forms.md](./rules/forms.md) —— FieldGroup、Field、InputGroup、ToggleGroup、FieldSet、验证状态
- [rules/composition.md](./rules/composition.md) —— Groups、覆盖层、Card、Tabs、Avatar、Alert、Empty、Toast、Separator、Skeleton、Badge、Button 加载
- [rules/icons.md](./rules/icons.md) —— data-icon、图标尺寸、图标作为对象传递
- [rules/styling.md](./rules/styling.md) —— 语义化颜色、变体、className、间距、尺寸、truncate、暗色模式、cn()、z-index
- [rules/base-vs-radix.md](./rules/base-vs-radix.md) —— asChild vs render、Select、ToggleGroup、Slider、Accordion
- [cli.md](./cli.md) —— 命令、标志、预设、模板
- [customization.md](./customization.md) —— 主题、CSS 变量、扩展组件

## 限制

- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，停止并请求澄清。
