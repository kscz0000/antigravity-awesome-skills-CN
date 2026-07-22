# 前端界面（Next.js + Weaviate 后端）

## 速查表

| 项目         | 取值                                                                                       |
| ------------ | ------------------------------------------------------------------------------------------- |
| **技术栈**    | Next.js（App Router）、Tailwind v4、shadcn/ui、Framer Motion、react-icons、ai-sdk            |
| **Node**     | v25.3.0+                                                                                    |
| **后端**      | `NEXT_PUBLIC_BACKEND_HOST`（默认：`localhost:8000`）                                          |
| **应用类型**  | 单页应用；主视图就地更新，不进行整页导航                                                      |
| **布局**      | shadcn Sidebar（左侧） + 主内容区；侧边栏按钮按功能切换主视图                                  |

---

## 安装步骤（按顺序执行）

### 1. Next.js

- **命令：** `npx create-next-app@latest . --yes`（在仓库根目录运行；沙箱中可能需要 `required_permissions: ["all"]`）
- **结果：** TypeScript、ESLint、Tailwind v4、App Router、Turbopack，`@/*` → `./*`，不含 `src/`。应用位于 `app/`，静态资源位于 `public/`。
- **脚本：** `dev` | `build` | `start` | `lint`。开发服务器：http://localhost:3000。
- **路由：** `app/layout.tsx`、`app/page.tsx`。导入别名：`@/` = 项目根。
- **参考：** [Next.js App Router Installation](https://nextjs.org/docs/app/getting-started/installation) — 请对照最新文档核对。

### 2. shadcn/ui

- **前置条件：** Next.js + Tailwind v4 + App Router + `@/*`，无 `src/`。
- **初始化：** `npx shadcn@latest init -t next -y -b zinc --no-src-dir`
- **添加组件：** `npx shadcn@latest add button -y`（例如 `card`、`dialog`、`input`；`-o` 表示覆盖）。
- **产物：** `components.json`、`lib/utils.ts`（cn）、`app/globals.css`（tw-animate、shadcn/tailwind.css、CSS 变量）。UI 位于 `components/ui/<name>.tsx`。导入方式：`import { Button } from "@/components/ui/button"`。
- **参考：** [shadcn Next.js](https://ui.shadcn.com/docs/installation/next) | [CLI](https://ui.shadcn.com/docs/cli)。

### 3. Framer Motion

```bash
npm i framer-motion
```

- **参考：** [Framer Motion](https://motion.dev/)

### 4. AI SDK（可选）

注意：仅在为聊天机器人应用构建对话式用户界面时安装。它能够让你通过 `useChat()` 流式接收来自后端的响应。

- **时机：** 仅当应用需要聊天界面（例如 query-agent 或 chatbot 流程）时才添加此步骤。
- **技术栈：** 使用 [Vercel AI SDK](https://ai-sdk.dev/docs/introduction)（`ai` + `@ai-sdk/*`）。使用 `useChat` 及 SDK UI 原语实现聊天视图。
- **参考：** [AI SDK – useChat](https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat) | [Next.js App Router setup](https://ai-sdk.dev/docs/getting-started/nextjs-app-router) — 请按最新文档完成安装与接入。

```bash
npm i ai @ai-sdk/react zod
```

### 5. 环境变量

**必填：**

```bash
NEXT_PUBLIC_BACKEND_HOST="localhost:8000"
```

非本地部署时，请改用真实的后端主机地址。

---

## 规范（必须遵循）

### 技术栈与结构

- **UI：** 仅使用 **shadcn 组件**完成布局与交互元素（按钮、卡片、输入框、对话框等）。不要引入其他 UI 库。
- **架构：** **SPA** — 单一主页面，主视图就地更新。除非必要，避免整页导航。
- **图标：** 仅使用 **react-icons**；为保持一致性，建议统一采用一套（例如 `react-icons/fa` 或 `react-icons/hi`）。
- **动画：** 仅使用 **Framer Motion**。不要引入其他动画库。

### 视觉风格

- **目标：** 极简、简洁、干净，避免杂乱、粗边框或噪点背景。
- **美学：** "液态玻璃" — 磨砂、半透明；柔和模糊；轻量化边框与阴影；轻盈而有层次。可酌情使用 `backdrop-blur`、半透明填充与细腻渐变。

### 动效

- **风格：** 含蓄、有弹性、目的明确（淡入、悬停、进入/退出）。优先使用弹簧物理效果，避免线性/ease-out。

### 布局

1. **左侧：** shadcn **Sidebar** 组件。
2. **右侧：** 主内容区。
3. **导航：** 每个后端功能对应一个侧边栏按钮（例如 data explorer、chat）。点击仅切换主视图。

### 响应式

- 布局与组件必须在小屏和大屏下都能正常使用。

---

## 文档（请对照当前版本核对）

- [FastAPI](https://fastapi.tiangolo.com/) | [GitHub](https://github.com/fastapi/fastapi)
- [Node.js](https://nodejs.org/en)
- [Next.js](https://nextjs.org/docs)
- [Tailwind (Next.js)](https://tailwindcss.com/docs/installation/framework-guides/nextjs)
- [shadcn components](https://ui.shadcn.com/docs/components)
- [react-icons](https://react-icons.github.io/react-icons)
- [Framer Motion](https://motion.dev/)
- [AI SDK](https://ai-sdk.dev/docs/introduction)