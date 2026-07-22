---
name: vibe-code-cleanup
description: "面向 vibe-coded 全栈应用（Next.js、React、Node.js 等）的安全生产清理与加固。删除死引用、未使用文件和坏掉的引用，同时不破坏路由或 API。"
category: fullstack
risk: safe
source: self
source_type: self
date_added: "2026-05-31"
author: Whoisabhishekadhikari
tags: [cleanup, refactor, nextjs, production, vibe-code, fullstack, nodejs]
tools: [claude, cursor, gemini, claude-code]
version: 1.0.0
---

# Vibe-Code 清理 —— 生产重构技能

面向 AI 生成 / vibe-coded 全栈应用的安全、增量式清理工作流。
目标是让代码库达到生产就绪状态，同时不破坏任何已经能跑通的东西。

## 适用场景

- 应用快速搭建完成、跑得通，但存在坏掉的引用、重复逻辑、死代码、不清晰的环境变量或脆弱的发布卫生时。
- 上线或交接前，将探索性代码转换为可维护的生产基线。
- 清理必须保留现有行为、避免对路由、API、鉴权、数据模型或集成做大范围重写时。

## 核心理念

> **外科手术，而不是爆破拆除。** 只删有证据证明是死代码的部分，其他一律保留。

绝不：
- 为了表面美化重写能跑通的系统
- 重命名可能已被索引或缓存的路由、slug 或 API 端点
- 改动工具的输入/输出、API 契约、数据库 schema 或鉴权流程
- 删除未经验证确实未被使用的文件
- 在一次提交中做大范围横扫式改动

始终：
- 改动要小、要精准、要可逆
- 每完成一批有意义的改动都要验证
- 优先用共享 helper 代替复制粘贴的代码块
- 保持向后兼容

---

## 第 1 步 — 侦察（动手前先读）

动手改任何东西之前，先摸清代码库：

```bash
# List all pages/routes
find . -type f \( -name 'page.js' -o -name 'page.jsx' -o -name 'page.ts' -o -name 'page.tsx' \)
find pages -type f \( -name '*.js' -o -name '*.jsx' -o -name '*.ts' -o -name '*.tsx' \) | rg -v '/_' | sort

# Find broken imports (TS projects)
npx tsc --noEmit 2>&1 | head -80

# Find unused exports (optional, for larger projects)
npx ts-prune 2>/dev/null | head -40

# Check for console.log / debug leftovers
grep -r "console\.log\|debugger\|TODO\|FIXME\|HACK" --include="*.{js,ts,jsx,tsx}" -l
```

把你发现的东西记录下来。此时先别动。

---

## 第 2 步 — 先修复坏掉的引用

坏掉的引用会导致构建失败，必须优先修复。

```bash
# TypeScript: list all errors
npx tsc --noEmit 2>&1

# Common patterns to fix:
# - Missing file (file was deleted or renamed)
# - Wrong relative path (../lib vs ../../lib)
# - Named export that doesn't exist
```

**修复原则：** 修复引用关系。除非已确认所有地方都没用到，否则不要删除被引用的文件。

---

## 第 3 步 — 识别死代码（删除前必须验证）

一个文件/导出只有在以下条件全部满足时才可安全删除：
1. 没有任何其他文件引用它（已用 grep 确认）
2. 没有出现在配置、sitemap 或路由清单中
3. 不是对外公开的 URL（page.js、route.js）

```bash
# Check if a file is imported anywhere
grep -r "from.*my-file\|require.*my-file" --include="*.{js,ts,jsx,tsx}" .

# Check if a component is used anywhere  
grep -r "MyComponent" --include="*.{js,ts,jsx,tsx}" .
```

---

## 第 4 步 — 将重复逻辑合并到 helper

寻找在 3 处及以上重复出现的模式（metadata 块、API fetch 包装、错误处理器）。

**适合合并的目标：**
- 页面级 SEO metadata（Open Graph、Twitter cards、canonical）
- 带错误处理的 fetch 包装
- 重复的工具函数（slugify、formatDate、truncate）

**不适合合并的目标（保持原样）：**
- 一次性的业务逻辑
- 契约不同的路由处理器
- 任何触及数据库 schema 或鉴权的东西

**共享 metadata helper 模式（Next.js）：**
```js
// lib/socialMetadata.js
export function buildPageMetadata({ title, description, path, image }) {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'https://yourdomain.com';
  const imageUrl = image?.startsWith('http') ? image : `${baseUrl}${image}`;
  
  return {
    title,
    description,
    openGraph: {
      title,
      description,
      url: `${baseUrl}${path}`,
      images: [{ url: imageUrl, width: 1200, height: 630, alt: title }],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: [imageUrl],
    },
    alternates: {
      canonical: `${baseUrl}${path}`,
    },
  };
}
```

---

## 第 5 步 — 环境变量审计

```bash
# List all env vars used in code
grep -r "process\.env\." --include="*.{js,ts,jsx,tsx}" . | grep -oP 'process\.env\.\w+' | sort -u

# Compare against .env.example or .env.local
cat .env.example 2>/dev/null || cat .env.local 2>/dev/null
```

标记出代码里用到但 `.env.example` 里没有的环境变量。绝不要把密钥提交进版本控制。

---

## 第 6 步 — 每批改动后都要验证

每完成一批有意义的清理改动后都要跑这些：

```bash
# TypeScript check
npx tsc --noEmit

# Lint
npx eslint . --ext .js,.jsx,.ts,.tsx --max-warnings 0

# Build (catches runtime issues TypeScript misses)
npm run build

# Tests (if present)
npm test -- --runInBand --passWithNoTests
```

如果构建或类型检查挂掉 → 先回退上一批，再继续。

---

## 第 7 步 — 提交策略

每次提交应当是一个单一的逻辑单元：

```text
fix: remove broken import in app/blog/page.js
refactor: consolidate social metadata into lib/socialMetadata.js  
chore: remove verified-unused utils/oldHelper.js
fix: standardize env var references to NEXT_PUBLIC_BASE_URL
```

不要把 UI 改动 + 逻辑改动 + 文件删除打包进同一次提交。提交越小，回滚越容易。

---

## 哪些东西不要动

除非存在已验证的 bug，否则把以下区域视为禁区：

| 区域 | 原因 |
|------|------|
| 路由 slug / 页面路径 | 可能已被 Google 索引 |
| API 路由契约 | 调用方依赖确切的形状 |
| 数据库 schema / Prisma 模型 | 需要迁移 |
| 鉴权流程逻辑 | 安全敏感 |
| 第三方集成配置 | key / webhook 与环境绑定 |
| 能跑通的工具页面 | 用户面功能 |

---

## 清理清单

- [ ] TypeScript 错误已修复
- [ ] 没有坏掉的引用
- [ ] 死代码已删除（grep 已验证）
- [ ] 为重复模式（3+ 处）创建了共享 helper
- [ ] 没有硬编码的密钥或仅本地的 URL
- [ ] 所有环境变量都在 `.env.example` 中有文档
- [ ] 构建通过
- [ ] 测试通过（或不存在测试）
- [ ] Lint 通过
- [ ] 每次提交范围清晰、可解释

## 局限

- 无法仅凭代码推断产品意图；删除路由、组件、API 契约或数据模型前必须先确认行为。
- 清理应分小批、经过 review 后再应用，因为大范围重构可能掩盖回归。
- 除非有明确需求和测试，否则不要改动鉴权、计费、持久化或第三方集成行为。