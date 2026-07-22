---
name: source-driven-development
description: 将每个实现决策锚定于官方文档。当你需要基于权威来源、附带引用的代码，且不受过时模式影响时使用。适用于任何正确性至关重要的框架或库的开发场景。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/source-driven-development
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# Source-Driven Development

## 概述

每个框架相关的代码决策都必须有官方文档作为依据。不要凭记忆实现——要验证、要引用，让用户看到你的来源。训练数据会过时，API 会被废弃，最佳实践会演进。本技能确保用户得到可信赖的代码，因为每个模式都能追溯到一个用户可以核查的权威来源。

## 何时使用

- 用户希望代码遵循某个框架的当前最佳实践
- 构建样板代码、启动代码或将在项目中复制的模式
- 用户明确要求有文档支撑的、经过验证的或"正确"的实现
- 实现框架推荐方式很重要的功能（表单、路由、数据获取、状态管理、认证）
- 审查或改进使用框架特定模式的代码
- 任何时候你准备凭记忆编写框架相关的代码

**何时不使用：**

- 正确性不依赖于特定版本（重命名变量、修复拼写错误、移动文件）
- 在所有版本中逻辑行为相同的纯逻辑（循环、条件、数据结构）
- 用户明确要求速度优先于验证（"快速做就行"）

## 流程

```
DETECT ──→ FETCH ──→ IMPLEMENT ──→ CITE
  │          │           │            │
  ▼          ▼           ▼            ▼
 什么       获取       遵循         展示
 技术栈？   相关文档   文档中的模式   你的来源
```

### 步骤 1：检测技术栈和版本

读取项目的依赖文件以识别确切版本：

```
package.json    → Node/React/Vue/Angular/Svelte
composer.json   → PHP/Symfony/Laravel
requirements.txt / pyproject.toml → Python/Django/Flask
go.mod          → Go
Cargo.toml      → Rust
Gemfile         → Ruby/Rails
```

明确说明你发现了什么：

```
STACK DETECTED:
- React 19.1.0 (from package.json)
- Vite 6.2.0
- Tailwind CSS 4.0.3
→ Fetching official docs for the relevant patterns.
```

如果版本缺失或模糊，**询问用户**。不要猜测——版本决定了哪些模式是正确的。

### 步骤 2：获取官方文档

获取你要实现的功能对应的特定文档页面。不是首页，不是完整文档——而是相关页面。

**来源层级（按权威性排序）：**

| 优先级 | 来源 | 示例 |
|----------|--------|---------|
| 1 | 官方文档 | react.dev, docs.djangoproject.com, symfony.com/doc |
| 2 | 官方博客 / 变更日志 | react.dev/blog, nextjs.org/blog |
| 3 | Web 标准参考 | MDN, web.dev, html.spec.whatwg.org |
| 4 | 浏览器/运行时兼容性 | caniuse.com, node.green |

**非权威来源——绝不可作为主要来源引用：**

- Stack Overflow 回答
- 博客文章或教程（即使很流行）
- AI 生成的文档或摘要
- 你自己的训练数据（这正是关键所在——要验证它）

**获取内容要精准：**

```
BAD:  Fetch the React homepage
GOOD: Fetch react.dev/reference/react/useActionState

BAD:  Search "django authentication best practices"
GOOD: Fetch docs.djangoproject.com/en/6.0/topics/auth/
```

获取后，提取关键模式，并注意任何废弃警告或迁移指南。

当官方来源之间相互冲突时（例如迁移指南与 API 参考相矛盾），向用户揭示差异，并根据检测到的版本验证哪种模式实际有效。

### 步骤 3：按文档模式实现

编写与文档展示一致的代码：

- 使用文档中的 API 签名，而非记忆中的
- 如果文档展示了新的实现方式，使用新方式
- 如果文档废弃了某个模式，不使用已废弃的版本
- 如果文档未覆盖某个内容，将其标记为未验证

**当文档与现有项目代码冲突时：**

```
CONFLICT DETECTED:
The existing codebase uses useState for form loading state,
but React 19 docs recommend useActionState for this pattern.
(Source: react.dev/reference/react/useActionState)

Options:
A) Use the modern pattern (useActionState) — consistent with current docs
B) Match existing code (useState) — consistent with codebase
→ Which approach do you prefer?
```

揭示冲突。不要静默选择某一方。

### 步骤 4：引用来源

每个框架特定的模式都要附带引用。用户必须能够验证每个决策。

**在代码注释中：**

```typescript
// React 19 form handling with useActionState
// Source: https://react.dev/reference/react/useActionState#usage
const [state, formAction, isPending] = useActionState(submitOrder, initialState);
```

**在对话中：**

```
I'm using useActionState instead of manual useState for the
form submission state. React 19 replaced the manual
isPending/setIsPending pattern with this hook.

Source: https://react.dev/blog/2024/12/05/react-19#actions
"useTransition now supports async functions [...] to handle
pending states automatically"
```

**引用规则：**

- 完整 URL，不使用短链接
- 尽可能使用带锚点的深层链接（例如 `/useActionState#usage` 而非 `/useActionState`）——锚点在文档重构时比顶级页面更持久
- 当引用支持非显而易见的决策时，引用相关段落
- 推荐平台特性时包含浏览器/运行时支持数据
- 如果找不到某个模式的文档，明确说明：

```
UNVERIFIED: I could not find official documentation for this
pattern. This is based on training data and may be outdated.
Verify before using in production.
```

对你无法验证的内容坦诚，比虚假的自信更有价值。

## 常见自我辩解

| 自我辩解 | 现实 |
|---|---|
| "我对这个 API 很有信心" | 信心不是证据。训练数据中包含看似正确但在当前版本下会出错的过时模式。请验证。 |
| "获取文档浪费 token" | 凭空编造 API 浪费更多。用户调试了一个小时，然后发现函数签名已经变了。一次获取能避免数小时的返工。 |
| "文档里不会有我需要的内容" | 如果文档没覆盖，这本身就是有价值的信息——该模式可能不是官方推荐的。 |
| "我提一下可能过时就行了" | 免责声明没有帮助。要么验证并引用，要么明确标记为未验证。模棱两可是最差的选择。 |
| "这是简单任务，不需要查" | 使用了错误模式的简单任务会变成模板。用户把你的废弃表单处理器复制到十个组件中，之后才发现存在现代写法。 |

## 危险信号

- 不检查该版本文档就编写框架相关的代码
- 对 API 使用"我相信"或"我认为"，而非引用来源
- 在不知道适用哪个版本的情况下实现某个模式
- 引用 Stack Overflow 或博客文章而非官方文档
- 因为训练数据中出现过就使用已废弃的 API
- 实现前不读取 `package.json` / 依赖文件
- 交付框架相关决策的代码却不附带来源引用
- 只需要一个页面时却获取了整个文档站点

## 验证清单

使用源驱动开发实现后：

- [ ] 框架和库版本已从依赖文件中识别
- [ ] 已为框架特定模式获取官方文档
- [ ] 所有来源均为官方文档，而非博客文章或训练数据
- [ ] 代码遵循当前版本文档中展示的模式
- [ ] 非平凡的决策包含带完整 URL 的来源引用
- [ ] 未使用已废弃的 API（已对照迁移指南检查）
- [ ] 文档与现有代码之间的冲突已向用户揭示
- [ ] 任何无法验证的内容已明确标记为未验证

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用更改之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代为针对特定环境的测试、安全审查，或用户对破坏性或高成本操作的审批。
