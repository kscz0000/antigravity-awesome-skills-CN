---
name: expo-examples
description: Expo 官方示例项目 — expo/examples 仓库中约 70 个 `with-*` 集成示例（Stripe、Clerk、Supabase、OpenAI、maps、Reanimated、SQLite、Skia、NativeWind 等）。在将第三方库或服务集成到现有 Expo 应用中、且需要官方推荐的集成范例时使用。触发词：expo 示例、with-stripe、with-clerk、with-maps、官方示例、集成范例、Expo Router 集成
risk: unknown
source: https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-examples
source_repo: expo/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/expo/skills/blob/main/LICENSE
---

# Expo 示例集
## 使用时机

当你需要 expo 的官方示例项目 — 即 expo/examples 仓库中约 70 个 `with-*` 集成（Stripe、Clerk、Supabase、OpenAI、maps、Reanimated、SQLite、Skia、NativeWind 等）时，使用本技能。当你要将第三方库或服务集成到现有 Expo 应用中、并希望使用官方推荐的范例时，也请使用本技能。


[expo/examples](https://github.com/expo/examples) 是 Expo 官方维护的约 70 个 **集成示例** 库 — 目录以 `with-<library>` 命名（如 `with-stripe`、`with-maps`），每个目录围绕 **一个** 库或服务构建。它们不是完整应用：而是 **managed** 工程（没有 `ios/`/`android/` 目录 — 原生配置通过 config plugins 完成），典型示例是 **约 100–200 行的单屏页面**。从中挖掘官方推荐的集成 *模式* — 即依赖集合、`app.json` config plugins、以及 Expo 针对当前 SDK 维护的最小接入方式 — 然后将其适配到用户应用中。不要指望从中照搬应用架构。

在自行编写集成之前，先去看示例。（类型 — 全栈、展示类、入门模板 — 见 `./references/catalog.md`。）

## 两种模式

1. **借鉴 / 适配**（最常见）— 用户已有项目。找到匹配的示例，阅读其关键文件，然后将 *模式* 套用到他们的代码中。
2. **脚手架** — 从零开始。直接从某个示例起步创建一个新项目。

## 工作流

### 1. 找到合适的示例

将用户需求映射到示例名称（如 支付 → `with-stripe`，身份认证 → `with-clerk`）。`./references/catalog.md` 是一个按类别组织的快照，便于快速分诊 — 但它会过时，所以请与实时列表核对：

```bash
# 实时示例名称：
gh api repos/expo/examples/contents --jq '.[] | select(.type=="dir" and (.name|startswith(".")|not)) | .name'
# 别名（重命名后的）+ 已弃用（已移除/迁移）的示例 — 推荐前请先检查：
gh api repos/expo/examples/contents/meta.json --jq '.content' | base64 -d
```

`meta.json` 是重命名或废弃信息的权威来源（已弃用的示例已从仓库树中移除，但仍在此处列出，每条都附有 `message`）。如果某个示例位于其 `deprecated` 映射中，请不要推荐它 — 按照 `message` 指引找到现代路径。如果位于 `aliases` 中，请使用 `destination`。

### 2a. 借鉴模式 — 只读不写用户项目

最常见情形：用户已有应用，想看看 Expo 是如何实现某功能的。将示例作为 **参考资料** 阅读，然后手工套用其模式 — 永远不要在用户项目之上脚手架整个示例。

**首先，一次性列出整个示例的目录树。** 集成代码常常嵌套存在（例如 Stripe 的服务端路由位于 `app/api/`），单层目录会漏掉重要文件：

```bash
gh api 'repos/expo/examples/git/trees/master?recursive=1' \
  --jq '.tree[].path | select(startswith("with-stripe/"))'
```

**然后按优先级阅读高信号文件：** `README.md`（搭建步骤）→ `package.json`（依赖）→ `app.json`（config plugins / 权限）→ 目录树揭示出的集成代码 → `.env`（所需的密钥）。每个文件：

```bash
gh api repos/expo/examples/contents/with-stripe/utils/stripe-server.ts --jq '.content' | base64 -d
# 没有 gh？原始 URL（分支为 master）：
curl -s https://raw.githubusercontent.com/expo/examples/master/with-stripe/utils/stripe-server.ts
```

**要读的文件不止一两个？** 许多集成分布在服务端路由、客户端 provider 和配置中（Stripe 就是这样）。跳过逐文件调用 — 把整个示例拉到 **一个临时/已 gitignore 的目录（不要放在用户项目中）**，然后用 Grep/Read 自由阅读，再手工套用：

```bash
npx degit expo/examples/with-stripe /tmp/expo-ref/with-stripe   # 干净拷贝，无 git 历史
# 没有 degit 时的回退方案（sparse-checkout，无需完整 ~64 MB 克隆）：
git clone --depth 1 --filter=blob:none --sparse https://github.com/expo/examples.git /tmp/expo-ref/examples \
  && (cd /tmp/expo-ref/examples && git sparse-checkout set with-stripe)
```

从那里用 Grep/Read 读取；用完后删除该临时目录。

### 2b. 脚手架模式 — 从示例创建新项目

```bash
npx create-expo --example with-stripe   # 简写：  npx create-expo -e with-stripe
bun create expo --example with-stripe    # 使用 bun
```

### 3. 适配进用户应用 — 非破坏式（关键）

当用户已有应用时，**只添加示例引入的内容；永远不要覆盖他们原有的配置。**

- **版本对齐 — 不要直接复制固定版本号。** 示例跟随的是 **最新** SDK，因此其 `package.json` 中的固定版本与较老项目不匹配。仅用 `npx expo install <pkg>` 添加 *缺失的* 依赖（它会解析与 SDK 匹配的版本），而不是直接复制固定版本号。
- **合并配置，不要替换。** 仅添加示例中引入、而用户配置中缺失的 `app.json`/`app.config.*` plugins 和权限 — 保留他们原有的配置块完整。
- **移植集成代码。**
- **重建环境变量**，按照示例的 `.env` 结构 — 它只包含占位符，绝不包含真实可用的密钥。

**完成标准** 是：集成代码已移植，且示例所需的每一个依赖、config plugin、权限和环境变量都在用户应用中得到落实 — 而不是仅仅 *看起来* 接好了。

## 注意事项

- **默认分支是 `master`，** 不是 `main`（影响原始 URL 和 sparse checkout）。
- **一键部署。** 每个示例都有一个启动 URL：`https://launch.expo.dev/?github=https://github.com/expo/examples/tree/master/<example>`。

## 相关技能

- Tailwind / NativeWind 样式 → `expo-tailwind-setup`
- 原生 UI 组件 → `building-native-ui`
- 编写原生模块 → `expo-module`
- 在采用最新 SDK 示例前先升级 SDK → `upgrading-expo`

## 参考资料

- `./references/catalog.md` — 示例库的分类快照，便于快速分诊。

## 使用限制

- 仅在任务明确匹配其上游产品或 API 范围时使用本技能。
- 在进行任何改动之前，请对照当前官方文档核对命令、API 行为、价格、配额、凭证和部署影响。
- 不要把生成的示例当作环境特定测试、安全审查，或对破坏性 / 高成本操作的审批的替代品。