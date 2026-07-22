---
name: unslop-review
description: '改写代码审查评论，让其读起来像人类队友写的。砍掉企业 AI 式的开场白（"我注意到..."、"我在想是否也许..."、"也许值得考虑..."）。每条评论直接给出：位置、问题、具体修复方案。涉及代码审查、PR 评论、人工化、去 AI 化、审查评论改写、反馈润色等场景时使用。'
risk: unknown
source: https://github.com/MohamedAbdallah-14/unslop/tree/main/plugins/unslop/skills/unslop-review
source_repo: MohamedAbdallah-14/unslop
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/MohamedAbdallah-14/unslop/blob/main/LICENSE
---

# Unslop 审查
## 适用场景

改写代码审查评论，让其读起来像人类队友写的，而非企业 AI 式的客套。砍掉开场白（"我注意到..."、"我在想是否也许..."、"也许值得考虑..."）。每条评论直接给出：位置、问题、具体修复方案。


## 目的

改写或生成 PR 审查评论，听起来像队友说话，不像礼貌机器。对问题直言不讳，对修复给出具体方案，对人保持善意。

## 触发方式

`/unslop-review`、`/review`、"review this PR"、"code review"、"humanize review"、"de-slop this comment"、"make this feedback sound human"。审查 pull request 时自动触发。

## 格式

默认形式：`L<行号>: <严重性前缀> <观察>. <修复>.`

严重性前缀（可选，但在涉及严重性时建议使用）：
- `bug:` — 代码已坏或即将坏
- `risk:` — 当前能用，明天脆弱（性能、竞态、缺测试）
- `nit:` — 风格、命名、死代码、"顺手改一下"
- `q:` — 真诚提问，不是变相抱怨

多文件：`<文件>:L<行号>: <严重性> <观察>. <修复>.`

跨行范围：`L88-140: ...`（问题跨多行时使用）。

## 规则

### 删掉

- 开场白："I noticed that..."、"It seems like..."、"It looks like to me..."
- 层层对冲："I was wondering if perhaps we might want to potentially..."
- 礼貌填充："I would kindly suggest..."、"just a small suggestion..."
- 每条评论都先夸："Nice work on this function but..."、"Great pattern, however..."
- 复述 diff："Here on line 42 you have a function called `getUser` which returns..."
- 单纯评价不给修复："This is bad" 后无任何建议

### 保留

- 精确行号和行号范围
- 用反引号包裹的标识符：`findUser`、`req.body.id`
- 具体修复或具体问题
- "为什么"只在修复方案不明显时给出

### 语气

像人说话，不像企业公文。"This throws if X" 不要写成 "It may potentially be worth considering that this could throw under certain conditions."。校准过的不确定性可以（"I think"、"probably"）——表演式的委婉不行。

### 自动展开完整说明（使用完整段落，不要一句话）

- 安全相关发现（CVE 级别、认证、密钥）
- 需要真正讨论的架构分歧
- 给新贡献者的上手上下文
- 当答案确实是"没问题"时

以上场景用一小段完整说明，其余恢复简洁风格。

## 示例

### 差 → 好

- 差：`I would kindly suggest that we might want to potentially consider adding a null check here as it could maybe lead to issues in some scenarios.`
- 好：`L42: bug: \`findUser\` 在无匹配时返回 undefined。在访问 \`user.email\` 前加守卫，或者直接 404 早退。`

- 差：`Great work on this implementation! However, I think we could potentially enhance readability by considering a refactor of this function.`
- 好：`L88-140: nit: 这个函数把校验、I/O 和映射混在一起。拆开之后，主流程会更清楚。需要的话我可以一起拆。`

- 差：`I noticed that there's no retry logic here which could be problematic.`
- 好：`L23: risk: 没有 429 的重试。用 \`withBackoff(3)\` 包一下，避免丢掉合法请求。`

- 差：`This implementation leverages a robust caching strategy.`
- 好：（删掉——空洞的夸赞。如果缓存确实值得说，具体讲讲为什么。）

### 通过

如果改动扎实且你提不出具体问题：单独一行写 `LGTM`。不要加任何客套。

## 边界

- 只生成评论。不提交 commit，不 `git push`，不自动批准，不跑 linter。
- 输出可直接粘贴：每行一条评论，或用清晰分隔的列表。
- 严重性必须诚实。不要把 `bug` 降级为 `nit` 来软化措辞。

## 局限

- 仅当任务明确匹配其上游来源和本地项目上下文时使用。
- 在应用更改前，验证命令、生成的代码、依赖、凭据和外部服务行为。
- 不要把示例当作环境专属测试、安全审查或用户对破坏性/高成本操作的批准来使用。