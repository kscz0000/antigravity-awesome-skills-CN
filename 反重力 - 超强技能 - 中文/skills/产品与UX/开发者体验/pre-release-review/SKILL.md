---
name: pre-release-review
description: "执行只读的发布前审查，覆盖部署就绪度、迁移、配置、密钥、发布顺序、回滚风险和发布阻塞项。当用户要求'发布审计'、'发布前审查'、'上线评审'、'部署就绪检查'时使用。"
category: operations
risk: safe
source: community
source_repo: chaunsin/agent-skills
source_type: community
date_added: "2026-06-29"
author: chaunsin
tags: [release, deploy-readiness, ci-cd, rollback, production]
tools: [git, gh, rg]
license: "Apache-2.0"
license_source: "https://github.com/chaunsin/agent-skills/blob/master/LICENSE"
---
# 发布前审查

使用此技能执行只读的生产环境发布就绪审查。目标是在 CI/CD 或手动发布步骤开始之前，发现缺失的部署材料、不安全的顺序、配置缺口、数据迁移缺口和模糊的生产风险，从而缩短发布时间并减少协调失误。

## 适用场景

- 用户要求发布审计、发布前审查、上线评审或部署就绪检查时使用。
- 发布 tag、部署生产服务或合并发布分支之前使用。
- PR 或 git 范围可能涉及迁移、环境变更、队列、缓存行为、对象存储资源或服务契约变更时使用。
- 用户询问某个变更是否安全发布并需要只读风险报告时使用。

## 不可协商规则

- 不修改源代码、配置、迁移文件、密钥、部署文件或生成文件。
- 不执行迁移、清除或预热缓存、上传资源、触发 CI/CD、部署服务、发布 tag、轮换密钥或更改远程基础设施。
- 输出简洁报告，仅列出已确认的问题和需要确认的合理风险。不要用正常的清单项淹没读者。
- 按优先级从高到低排列发现结果。
- 每个条目包含：模块、发现内容、证据、推断负责人、风险和建议操作。
- 绝不泄露私钥、账号密码、token、证书、cookie 或完整密钥值。仅报告文件路径、行号、变量名、密钥类型和脱敏提示。
- 如果证据不完整但风险可能阻塞生产，列为待确认项。

## 必读参考

- 分析发现之前先读取 `references/checklist.md`，确保不遗漏重要的发布领域。
- 编写最终报告前先读取 `references/report-template.md`，保持优先级、负责人推断、密钥脱敏和输出格式一致。

## 项目指引发现

在解读发布差异之前，查找项目本地指引文件（如仓库根目录和相关服务目录中的 `AGENTS.md`、`CLAUDE.md`）。存在时读取它们，使审查遵循用户的项目约定：服务边界、发布规则、验证预期、所有权提示和已知运维约束。

- 将项目指引视为解读风险的上下文依据，而非执行变更操作的许可。
- 若项目指引与本技能不可协商的安全规则冲突，以本技能的只读、不泄露密钥规则为准。
- 若相关指引文件无法读取，仅在影响发布审查时在"无法验证"部分注明限制。

## 范围选择

判定风险前确定审查范围。在报告中说明所选范围。

1. 若用户提供 PR URL 或 PR 编号，优先审查该 PR 差异。
   - `gh` 可用且已认证时，使用 `gh pr view` 和 `gh pr diff` 等只读命令。
   - 因缺少工具、认证或网络限制无法拉取 PR 时，如实告知并请求本地分支、patch 或明确的 git 范围。不得臆造 PR 内容。
2. 若用户提供明确的 `base..head` 范围，直接使用。
3. 若仅提供 head commit，将该 commit 可达的上一个可用 release tag 与 head commit 比较。
4. 若未提供范围，将上一个可用 release tag 与 `HEAD` 比较。
5. 仔细选择上一个可用 release tag：
   - 当仓库有明显的可见 release tag 约定时优先采用，如语义版本号、`v*` 或 `release-*`。若命名混用，需声明假设。
   - 若 `HEAD` 正好位于一个或多个 tag 上，将这些 tag 视为当前发布点并与更早可达的 release tag 比较，而非与 `HEAD` 自身的 tag 比较。
   - 若不存在可用的前序 release tag，审查最近 5 条提交并明确警告这是降级方案——无可用前序 release tag，审计仅覆盖最近 5 条提交；建议后续审查采用基于 PR 或 tag 的范围。

## 只读证据收集

仅运行安全检查命令，根据仓库和当前权限调整。常用命令如下：

```bash
git status --short
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
rg --files -g 'AGENTS.md' -g 'CLAUDE.md'
git tag --merged HEAD --sort=-creatordate
git tag --points-at HEAD
git for-each-ref --sort=-creatordate --format="%(refname:short) %(objectname:short)" refs/tags
git describe --tags --abbrev=0 HEAD
git diff --name-status <base>..<head>
git diff --stat <base>..<head>
git log --oneline --decorate --no-merges <base>..<head>
git diff -U3 <base>..<head> -- <path>
git blame -L <start>,<end> -- <path>
git log --format="%h %an %s" -- <path>
rg -n "<pattern>" .
```

对于 PR，仅在有权限且允许时使用 `gh pr view` 和 `gh pr diff`。不得绕过网络、认证、沙箱或审批限制。命令无法运行时，在报告"无法验证"部分记录限制。

## 审查流程

1. 确认 git 仓库根目录、当前分支、脏状态和选定的比较范围。
2. 收集变更文件名、文件状态、diff 统计、摘要和涉及的服务。
3. 检查相关差异，不只依赖文件名。
4. 用清单将变更代码映射到生产需求：
   - schema 变更 → 迁移、索引、seed 数据和数据回填
   - 配置读取 → 环境变量示例、部署密钥、feature flag 和运行时配置
   - 缓存 key 或 TTL 变更 → 失效策略、预热和兼容性工作
   - 队列生产者/消费者 → topic 设置、DLQ、幂等性和部署顺序
   - 资源引用 → 对象存储、CDN、模板、证书和权限
   - 服务契约变更 → 部署序列、向后兼容性和回滚风险
5. 尽量通过 `git blame` 推断变更行的负责人；否则使用该文件或 commit 近期的 `git log` 作者。标记为"推断负责人"，不含邮箱地址。
6. 使用 `references/report-template.md` 将每个发现分类为 P0、P1 或 P2。
7. 尽量使用用户的语言编写最终报告。结论值严格使用 `BLOCKED`、`NEEDS_CONFIRMATION` 或 `NO_BLOCKER_FOUND`。

## 脏工作区处理

默认仅审查已提交的范围。除非用户明确要求包含工作区变更，否则不得静默混入未提交或未跟踪的更改。

- 始终报告工作区是否为脏状态。
- 若脏文件或未跟踪文件涉及发布相关区域（如迁移、部署配置、环境示例、CI/CD、密钥、缓存、队列、资源或服务契约），添加一条 P2 待确认项，说明这些变更已排除在已提交范围审查之外，必须在发布前单独提交、丢弃或审查。
- 若用户明确要求包含脏工作区变更，使用 `git diff` 和 `git diff --name-status` 等只读命令检查，并明确标注为未提交证据。

## 证据要求

每个发现都应引用具体证据：

- 文件路径和行号（可用时）
- commit hash 或 PR 引用（行证据不足时）
- 命令限制（证据无法收集时）
- diff 关系，例如"schema 变更但无对应迁移文件"

不得因没有文件匹配某模式就断言某事安全。对无法从本地仓库证据确认的区域使用"未验证"。

## 发现与验证限制区分

将发布确认项与中性工具限制分开：

- 发布确认项是与 diff 关联的生产风险，例如新的环境变量但其生产值无法验证、schema 变更且迁移状态不明、新队列的基础设施未确认。归类为 P1 或 P2，结论设为 `NEEDS_CONFIRMATION`（除非同时存在 P0）。
- "无法验证"条目是中性限制，例如 diff 未引入特定发布需求时的远程访问缺失或部署平台凭据缺失。中性限制本身不会改变结论。
- 若某限制阻碍了发布关键 diff 变更的确认，将其提升为 P1/P2 发现而非仅留在"无法验证"中。
- 仅当从可用证据中未发现任何 P0-P2 发现或发布确认项时才使用 `NO_BLOCKER_FOUND`。报告中仍可包含中性验证限制。

## 输出规则

- 先展示 P0 和 P1 发现，然后是 P2 确认项。
- 不列正常常通过的清单类别。
- 仅当 diff 涉及多个服务、异步 worker、迁移、队列、缓存或公共合约时，才包含服务部署顺序章节。
- 若未发现 P0 阻塞项但有 P1/P2 确认项，使用 `NEEDS_CONFIRMATION`。
- 若无 P0-P2 发现，列出已审查范围和中性验证限制。
- 保持报告足够简短，便于发布经理立即采取行动。

## 局限性

- 本技能为只读模式，不执行部署、tag 发布、运行迁移、轮换密钥或修改基础设施。
- 可根据现有证据识别发布风险，但无权访问相关部署系统、密钥库、数据库、队列、缓存或可观测系统时无法证明生产状态。
- 不能替代高风险生产变更的服务负责人审批。

## 测试提示词

使用以下提示词验证技能行为：

- "执行发布前审查，告诉我这次生产部署是否有风险。"
- "发布前审查 PR #123。检查迁移、配置和缓存工作。"
- "这个仓库没有 tag。使用默认策略审计发布就绪度。"
- "检查 v1.2.3..HEAD 是否存在后端上线阻塞项。"