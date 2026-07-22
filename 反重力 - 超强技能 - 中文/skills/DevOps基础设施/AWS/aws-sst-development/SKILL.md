---
name: aws-sst-development
description: SST v4（Ion）专家，基于 Pulumi 框架以代码方式管理 AWS 资源。用于编写或编辑 sst.config.ts、构建 infra/ 模块（sst.aws.Function/Bucket/Dynamo/Cron/Service/Router、sst.Secret、sst.Linkable、原生 aws.* Pulumi 资源）、连接资源链接……触发词：SST、SST v4、Ion、Pulumi、sst.config.ts、infra、sst.aws、AWS 基础设施即代码
risk: unknown
source: https://github.com/zxkane/aws-skills/tree/main/plugins/aws-iac/skills/aws-sst-development
source_repo: zxkane/aws-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/zxkane/aws-skills/blob/main/LICENSE
---

# 适用于 AWS 的 SST v4
## 适用场景

当你需要 SST v4（Ion）专家——基于 Pulumi 框架以代码方式管理 AWS 资源时，请使用本技能。用于编写或编辑 sst.config.ts、构建 infra/ 模块（sst.aws.Function/Bucket/Dynamo/Cron/Service/Router、sst.Secret、sst.Linkable、原生 aws.* Pulumi 资源）、连接资源链接……


SST v4（即"Ion"引擎）是一个由 Pulumi 支持的 IaC 框架：你用 TypeScript 描述 AWS 资源，SST/Pulumi 会把它们协调部署到你的 AWS 账户中。它为你提供了一套高级的 `sst.aws.*` 组件（Function、Bucket、Dynamo、Cron、Service……），每个组件都会展开为多个底层资源，同时还有一个万能逃生口，可以使用任何原生 Pulumi 的 `aws.*` 资源来覆盖长尾需求。本技能沉淀了一套经过生产验证的写法，涵盖在 AWS 上编写、链接、测试、部署与排障 SST 栈——这些经验来自真实的多栈项目，每一条教训都是用一次生产事故换来的。

**SST 与 Pulumi 是第三方软件——不确定时请用 Context7 校验当前语法**
（针对 `sst` 或 `pulumi-aws` 使用 `resolve-library-id` → `query-docs`）来确认组件的配置项。AWS 一侧的事实（服务限额、模型 ID、IAM action 名称、区域可用性）请使用 AWS 文档 MCP 校验，绝不要凭记忆。这里的模式讲的是 *how*（怎么做），官方文档讲的是 *what*（是什么）。

## 被调用时

先判断当前所处场景，再跳转到对应参考文档：

| 场景 | 跳转 |
|------|------|
| 新建项目，或在已有 SST 应用中添加资源/模块 | **编写** → `references/authoring.md` |
| 把一个模块的输出接到另一个模块（链接、SSM、IAM 作用域） | **编写** → `references/authoring.md` § Sharing |
| 为基础设施编写测试，防止变更悄无声息地破坏现有功能 | **测试** → `references/testing.md` |
| 正在执行部署，或部署刚失败 | **部署/运维** → `references/deploy-and-troubleshoot.md` |
| 在不同的 Pulumi 类型之间迁移资源，或重命名物理名称 | **部署/运维** → `references/deploy-and-troubleshoot.md` § Migrations |

编辑前务必先阅读对应的参考文档——它们承载着每条规则背后的 *why*（为什么），这比规则本身更重要。

## 摸底：先读仓库，再动手

SST 项目结构是约定俗成的，但并不完全相同。开始编辑前，先快速画出地图，让你的改动贴合项目风格，而不是与之对抗：

1. **`sst.config.ts`** — 应用名称、`home`、provider/region、`defaultTags`、任何全局 `$transform`（Node 运行时锁定、bundle 修补），以及 `run()` 导入 `infra/` 模块的顺序。导入顺序 *就是* 依赖顺序，请务必遵守。
2. **`infra/`** — 一个文件对应一个领域（storage、functions、api、observability……）。这里才是资源的声明处。看看是否有一个 `infra/CLAUDE.md` —— 这些项目会把 IaC 专用规则放在那里，它是最值得首先阅读的文件，没有之一。
3. **`infra/tests/`** — 源码级 Vitest 断言，用来锁定资源不变量。如果存在，你的改动必须让它们继续通过，并且很可能需要新增一条断言。
4. **`package.json` / `.nvmrc`** — 包管理器（npm 还是 pnpm）、Node 版本，以及实际安装的 `sst`/`pulumi` 版本。

运行 `npx sst version` 来确认你用的是 v4/Ion（其特征是 `$config` + `.sst/platform/`）。v2/v3（即"SST Classic"，基于 CDK）是一个不同的框架——上面这些模式并不适用。

## 约定：哪些是普适的，哪些是可调的

本技能所基于的项目都共享一套精心设计的内部风格。其中的部分是 **普适的**（对任何 SST v4 + AWS 项目都成立——任何地方都要遵循）；另一部分是 **项目自定义的**（这些项目选择的合理默认值——为保持一致性可以采纳，但要意识到某个具体项目可能不同）。

**普适原则 —— 适用于任何 SST v4 + AWS 项目：**

- **在唯一一处主动管控 Node 运行时。** 不要把它交给当前安装的 SST 默认版本决定。惯用法是在 `run()` 中写一个全局的 `$transform(sst.aws.Function, (args) => { args.runtime ??= "nodejs24.x" })`——这里用 `??=` 是正确的（transform 在组件自身的默认值生效之前运行，所以它只在用户没有显式设置时填值）。较新版本的 SST 已经默认使用较新的 Node 运行时，所以先检查当前安装版本的默认值（用 Context7）；transform 其实是版本独立的保险丝，避免未来某次 SST 降级悄悄地把你的运行时一并改了。详见 `references/authoring.md`。
- **绝不要把 Pulumi 的 `Output<T>` 直接插到普通 JS 模板字符串里。** 用 `$interpolate`（或 `pulumi.interpolate`）。一个裸的顶层 `` `${bucket.arn}/*` `` 会把 `Output` 字符串化为 `[Output<T>]` 占位符，并生成一个损坏的 ARN，要到部署时才会报错（类型检查和 `sst dev` 都正常）。修复方法就是 `$interpolate`​`` `${bucket.arn}/*` ``。这种坑已经引发过生产部署中断。详见 `references/authoring.md` § Outputs。
- **在不同 Pulumi *类型* 之间迁移资源，默认拆成两个 PR** —— Pulumi 是先创建后销毁，所以对于那些有唯一性约束的 AWS 名称（bucket、IAM role、gateway），旧资源还持有该名称，新建就会以 `ConflictException` 失败。两次连续的部署（先拆除，再重建）是稳妥的默认做法；`aliases:` / `pulumi import` / 状态手术可以在某些情况下桥接身份，但必须有审阅过的方案。详见 `references/deploy-and-troubleshoot.md` § Migrations。
- **优先使用带类型的 `sst.aws.*` / `aws.*` 资源，而不是 `aws.cloudcontrol.Resource` 这个万能逃生口。** CloudControl 的输出是弱类型字符串，并且 `oneOf` 字段无法干净地更新 patch。只有在尚无对应类型化资源时才使用它，并且一旦官方推出类型化资源就要及时迁移掉。

**项目自定义默认值 —— 为保持一致性可以采纳，但每个仓库请自行确认：**

- **区域 `ap-northeast-1`**、`home: "aws"`，以及 `defaultTags` 携带 `Project` / `Stage` / `ManagedBy: "sst"`。
- **按 Stage 区分的生命周期**：`removal: stage === "prod" ? "retain" : "remove"` 以及 `protect: stage === "prod"`，让 prod 资源在栈拆除时得以保留，非 prod 的预览环境则能自动清理。
- **以 SSM Parameter Store 作为图外（out-of-graph）契约**，置于 `/{app}/{stage}/{domain}/...` 前缀之下——用于那些不在 Pulumi 图内的消费者（CI 脚本、平级应用、运维人员）。对于 *同应用* 的 Lambda，优先用 SST 的 `link:`（它会建立真正的依赖边并授予 IAM 权限）；同应用间的共享不要绕道 SSM。详见 `references/authoring.md` § Sharing。
- **`run()` 内惰性加载 `await import("./infra/<module>")`**，让 `sst dev` 的热重载保持轻盈。（测试时，模块导出仍会执行其顶层的 `new sst.aws.*`，除非它被包成一个工厂函数——测试基础设施的方法见 `references/testing.md`。）
- **每个 infra 模块都配源码级 Vitest 测试** —— 是一套轻量的、内部风格的回归网，断言的是 *源码文本*（资源名、索引形状、IAM 作用域）。这是有意做出的选择，不是 SST 的限制：当模块真的有逻辑时，Pulumi *是* 支持运行时 mock（`@pulumi/pulumi/runtime`）来做行为级图测试的。源码断言并不能替代预览部署 + 冒烟测试。详见 `references/testing.md`。
- **可观测性门禁**：每个新 Lambda/队列/定时任务在合并前都要配上告警和结构化日志。是否强制执行取决于项目，但作为廉价保险是值得的。详见 `references/deploy-and-troubleshoot.md` § Observability。

每当你引入一条约定，请明确说明它属于哪一类（"这是普适的"还是"对齐本仓库的风格"），让用户能从容地决定是否覆盖项目自定义的那部分。

## 工作节奏

1. **摸底**（见上文）——梳理配置、模块、测试、工具链。
2. **验证语法** —— 任何不显然的细节，都用 Context7 / AWS 文档 MCP 校验。不要凭直觉去猜组件的配置项名。
3. **按 `references/authoring.md` 编写**资源/模块。匹配周围文件的注释密度与命名风格——这些项目对 *why* 的注释很重，在一个注释密集的文件里写一个简短的单行注释，会显得像一次回退。
4. **测试** —— 新增或更新源码级断言（`references/testing.md`），然后跑 `npx vitest`（或仓库的 `test` 脚本）。跑 `npx sst diff` 和/或 `tsc --noEmit`，把类型与计划错误挡在部署之前。
5. **按 `references/deploy-and-troubleshoot.md` 部署/运维**。在执行任何 `sst deploy` 之前，先用 `aws sts get-caller-identity` 确认目标账户。
6. **清理**所有导出的状态文件——它们包含账户 ID 和 ARN，绝不能遗留在 `/tmp` 或聊天记录里。

## 什么是好的成果

- 改动是在合适的 `infra/` 模块中，能满足需求的最小 diff，并按依赖顺序挂入 `run()`。
- 每个 Lambda 通过全局 transform 拿到正确的运行时（除非有意识地偏离——例如 Python 函数，否则不要手动设置 `runtime`）。
- 跨资源引用使用 `link:`（图内）和/或 `$interpolate` 作用域的 IAM；对外输出的供其他工具消费的值，按阶段前缀发布到 SSM。
- 新增基础设施配有对应的源码级测试，且既有测试套件保持全绿。
- 你通过文档 MCP 核实了 AWS 一侧的事实，并通过 Context7（而非凭记忆）核实了 SST/Pulumi 的语法。
- 任何不可逆的操作（部署、`sst remove`、资源类型迁移）都已告知用户其目标账户，并且迁移按两次 PR 而不是一次来规划。

## 使用限制

- 仅当任务明确匹配本技能的上游来源与本地项目上下文时再使用。
- 在应用改动前，校验命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要把示例当作环境专属测试、安全审查，或对破坏性/高成本操作的审批依据。
