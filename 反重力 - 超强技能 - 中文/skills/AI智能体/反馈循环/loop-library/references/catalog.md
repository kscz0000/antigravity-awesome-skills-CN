# 已发布循环库目录

由 `scripts/loop-data.mjs` 生成（目录更新于 2026-06-19）。
在线目录：https://signals.forwardfuture.ai/loop-library/catalog.md
机器可读目录：https://signals.forwardfuture.ai/loop-library/catalog.json

按目标、触发条件、产出物、证据、分类或关键词搜索。将适配和新设计视为未发布，除非它们出现在上述在线目录 URL 中。

## 001 — [文档清扫](https://signals.forwardfuture.ai/loop-library/loops/overnight-docs-sweep/)

- 分类：工程
- 适用场景：当实现变更可能使 README、安装指南、API 参考、示例或运维手册落后时使用。
- 提示词：当需要文档检查时，全面审查代码库，确保所有文档反映当前实现。更新过时文档，验证变更，然后发起拉取请求。
- 验证：文档与当前实现一致。以可审查的拉取请求结束。
- 关键词：AI 编码智能体、文档审计、文档漂移、文档维护、拉取请求工作流
- 相关：[生产错误清扫](https://signals.forwardfuture.ai/loop-library/loops/production-error-sweep/)、[架构满意度循环](https://signals.forwardfuture.ai/loop-library/loops/architecture-satisfaction-loop/)

## 002 — [架构满意度循环](https://signals.forwardfuture.ai/loop-library/loops/architecture-satisfaction-loop/)

- 分类：工程
- 适用场景：当进行有意识的架构重构，目标可以用具体术语描述，且当前系统可以在每次有意义的变更后测试时使用。
- 提示词：重构直到架构令人满意。在每个重要步骤后，实时测试系统、运行自动审查并提交。在 /tmp/refactor-{projectname}.md 中追踪进度。
- 验证：架构令人满意且检查通过。每个重要步骤都进行了实时测试、自动审查和提交。
- 关键词：AI 编码智能体、架构重构、自动审查、增量重构、编码智能体工作流
- 相关：[文档清扫](https://signals.forwardfuture.ai/loop-library/loops/overnight-docs-sweep/)、[50ms 页面加载循环](https://signals.forwardfuture.ai/loop-library/loops/sub-50ms-page-load-loop/)

## 003 — [50ms 页面加载循环](https://signals.forwardfuture.ai/loop-library/loops/sub-50ms-page-load-loop/)

- 分类：工程
- 适用场景：当产品有一组已定义的路由、稳定的性能测试工具和映射到特定指标与环境的 50ms 目标时使用。
- 提示词：持续优化代码速度。每次重要变更后，在相同可重复测试条件下测量每个页面的加载性能。持续到每个页面加载时间低于 50ms。
- 验证：每个页面加载时间低于 50ms。使用相同基准测试并确认无回归。
- 关键词：AI 编码智能体、页面加载优化、性能基准、Web 性能工作流、50ms 页面加载
- 相关：[架构满意度循环](https://signals.forwardfuture.ai/loop-library/loops/architecture-satisfaction-loop/)、[生产错误清扫](https://signals.forwardfuture.ai/loop-library/loops/production-error-sweep/)

## 004 — [生产错误清扫](https://signals.forwardfuture.ai/loop-library/loops/production-error-sweep/)

- 分类：工程
- 适用场景：当智能体可以读取生产遥测数据、将故障追溯到仓库、运行相关测试并准备可审查修复时，作为计划可靠性检查使用。
- 提示词：审查生产日志中的错误。如果发现可操作的问题，追溯到根因、修复、验证修复并发起拉取请求。如果没有可操作的错误，不做变更即停止。
- 验证：可操作的生产错误已修复并验证。以拉取请求结束，或在无可操作错误时停止。
- 关键词：AI 编码智能体、生产日志审查、错误分诊、根因分析、可靠性工作流
- 相关：[文档清扫](https://signals.forwardfuture.ai/loop-library/loops/overnight-docs-sweep/)、[50ms 页面加载循环](https://signals.forwardfuture.ai/loop-library/loops/sub-50ms-page-load-loop/)

## 005 — [100% 测试覆盖循环](https://signals.forwardfuture.ai/loop-library/loops/100-percent-test-coverage-loop/)

- 分类：工程
- 适用场景：当 100% 覆盖率是明确的项目要求，且仓库有可信赖的覆盖率命令、明确排除项和可重复运行的测试套件时使用。
- 提示词：添加测试直到达到 100% 测试覆盖率。
- 验证：完整测试套件在 100% 覆盖率下通过。使用项目的覆盖率报告作为真实来源。
- 关键词：AI 编码智能体、100% 测试覆盖率、测试覆盖率工作流、自动化测试、编码智能体提示词
- 相关：[架构满意度循环](https://signals.forwardfuture.ai/loop-library/loops/architecture-satisfaction-loop/)、[生产错误清扫](https://signals.forwardfuture.ai/loop-library/loops/production-error-sweep/)

## 006 — [SEO/GEO 可见性循环](https://signals.forwardfuture.ai/loop-library/loops/seo-geo-visibility-loop/)

- 分类：内容
- 适用场景：当网站有一组已定义的优先页面和目标问题，且每次变更后可以重新运行相同的技术爬取和搜索可见性检查时使用。
- 提示词：对可爬取性、索引、页面意图、标题、内链、结构化数据、来源引用和答案优先内容运行 SEO/GEO 审计。按预期影响排列差距，修复最高杠杆的问题，然后跨搜索引擎和 AI 问答引擎重新运行相同的爬取和目标查询基准。重复直到没有关键技术问题，每个优先查询映射到一个清晰的答案就绪页面，且基准显示没有高影响差距需要修复。
- 验证：优先页面可索引、答案就绪且技术健全。可重复的爬取和查询基准未发现剩余高影响差距。
- 关键词：SEO 审计、生成式引擎优化、GEO 工作流、AI 搜索可见性、问答引擎优化
- 相关：[文档清扫](https://signals.forwardfuture.ai/loop-library/loops/overnight-docs-sweep/)、[生产错误清扫](https://signals.forwardfuture.ai/loop-library/loops/production-error-sweep/)

## 007 — [日志覆盖循环](https://signals.forwardfuture.ai/loop-library/loops/exhaustive-logging-coverage-loop/)

- 分类：工程
- 适用场景：当重要的用户流程、服务边界、后台任务或故障路径因系统日志不完整或不一致而难以追踪时使用。
- 提示词：审查系统日志，添加缺失的覆盖，直到每个重要路径都产生有用的、经过测试的日志。
- 验证：每个重要路径都发出有用的、经过测试的日志。具有代表性的成功和失败测试证明覆盖而不暴露敏感数据。
- 关键词：AI 编码智能体、结构化日志、可观测性覆盖、日志测试、生产诊断
- 相关：[生产错误清扫](https://signals.forwardfuture.ai/loop-library/loops/production-error-sweep/)、[100% 测试覆盖循环](https://signals.forwardfuture.ai/loop-library/loops/100-percent-test-coverage-loop/)

## 008 — [夜间变更日志循环](https://signals.forwardfuture.ai/loop-library/loops/nightly-changelog-sweep/)

- 分类：工程
- 适用场景：当项目变更足够频繁，用户侧发布说明可能与已合并的拉取请求、提交、部署和产品变更脱节时使用。
- 提示词：每晚审查前一天的变更，将用户需要知道的内容更新到变更日志。
- 验证：前一天每个与用户相关的变更都已记录。变更日志已更新并验证，或无变更结果已记录。
- 关键词：AI 编码智能体、夜间变更日志、发布说明工作流、变更日志自动化、每日仓库审查
- 相关：[文档清扫](https://signals.forwardfuture.ai/loop-library/loops/overnight-docs-sweep/)、[仓库清理循环](https://signals.forwardfuture.ai/loop-library/loops/repository-cleanup-loop/)

## 009 — [质量连胜循环](https://signals.forwardfuture.ai/loop-library/loops/quality-streak-loop/)

- 分类：评估
- 适用场景：当产品质量需要严格的连续成功标准，且失败应永久改进测试和基准套件时使用。
- 提示词：测试真实场景。当一个失败时，记录它，添加回归和基准覆盖，修复它，并重新开始连胜。连续 [N] 个成功后停止。
- 验证：最近 [N] 个真实场景连续通过。每个早期失败都已记录、修复，并由回归和基准覆盖保护。
- 关键词：AI 产品评估、质量连胜、回归测试、基准覆盖、真实场景
- 相关：[全产品评估循环](https://signals.forwardfuture.ai/loop-library/loops/full-product-evaluation-loop/)、[100% 测试覆盖循环](https://signals.forwardfuture.ai/loop-library/loops/100-percent-test-coverage-loop/)

## 010 — [全产品评估循环](https://signals.forwardfuture.ai/loop-library/loops/full-product-evaluation-loop/)

- 分类：评估
- 适用场景：当质量必须跨完整功能集而非狭窄回归或少数精选示例来衡量时，用于端到端产品评估。
- 提示词：创建覆盖每个主要能力的 [N] 个真实场景。测试前定义明确的成功标准并选择一致的评估方法，如通过/失败检查或评分标准。在相同条件下运行每个场景并记录每个结果的证据。修复未达标项的根本原因，重新运行受影响场景，然后重新运行完整集合。持续到每个场景都达到原始质量标准。
- 验证：[N] 个场景中每一个都达到定义的质量标准。最终评估运行在原始条件下覆盖每个主要能力。
- 关键词：AI 产品评估、全产品测试、响应评分、质量基准、功能覆盖
- 相关：[质量连胜循环](https://signals.forwardfuture.ai/loop-library/loops/quality-streak-loop/)、[生产数据清理循环](https://signals.forwardfuture.ai/loop-library/loops/production-data-cleanup-loop/)

## 011 — [测试套件速度循环](https://signals.forwardfuture.ai/loop-library/loops/test-suite-speed-loop/)

- 分类：工程
- 适用场景：当慢测试延迟了本地反馈或持续集成，且项目有稳定的运行时间和覆盖率测量命令时使用。
- 提示词：在不降低覆盖率或改变行为的前提下，尽可能快地优化测试套件。
- 验证：套件更快，无覆盖率或行为回归。可重复计时、完整通过套件和原始覆盖率报告证明结果。
- 关键词：AI 编码智能体、测试套件性能、更快的 CI、测试优化、覆盖率保持
- 相关：[100% 测试覆盖循环](https://signals.forwardfuture.ai/loop-library/loops/100-percent-test-coverage-loop/)、[50ms 页面加载循环](https://signals.forwardfuture.ai/loop-library/loops/sub-50ms-page-load-loop/)

## 012 — [仓库清理循环](https://signals.forwardfuture.ai/loop-library/loops/repository-cleanup-loop/)

- 分类：工程
- 适用场景：当废弃分支、旧工作树、不清晰的拉取请求或未合并提交导致难以确定哪个仓库状态仍然重要时使用。
- 提示词：检查本地和远程分支、拉取请求、提交和工作树。恢复有价值的工作并清理所有过时内容，直到仓库是最新且有组织的。
- 验证：有价值的工作已恢复，剩余仓库状态是有意的。分支、拉取请求、提交和工作树是当前的、有负责人的或带证据安全移除的。
- 关键词：AI 编码智能体、仓库清理、git worktree 审计、分支卫生、拉取请求分诊
- 相关：[过期安全批量发布循环](https://signals.forwardfuture.ai/loop-library/loops/stale-safe-batch-release-loop/)、[夜间变更日志循环](https://signals.forwardfuture.ai/loop-library/loops/nightly-changelog-sweep/)

## 013 — [过期安全批量发布循环](https://signals.forwardfuture.ai/loop-library/loops/stale-safe-batch-release-loop/)

- 分类：运维
- 适用场景：当多个分支或拉取请求可能同时就绪，且发布必须避免过时工作树、部分叠加和不完整变更时使用。
- 提示词：审查待处理变更和拉取请求，排除过时或未完成的工作，合并有效变更并一起发布。
- 验证：仅当前、完整的变更进入合并发布。发布的版本是包含每个选定变更的最新集成分支。
- 关键词：AI 发布运维、批量发布、过时代码防护、拉取请求协调、部署安全
- 相关：[仓库清理循环](https://signals.forwardfuture.ai/loop-library/loops/repository-cleanup-loop/)、[发布后基线循环](https://signals.forwardfuture.ai/loop-library/loops/post-release-baseline-loop/)

## 014 — [生产数据清理循环](https://signals.forwardfuture.ai/loop-library/loops/production-data-cleanup-loop/)

- 分类：运维
- 适用场景：当生产数据集包含不再匹配产品、策略、分类法或质量定义的记录，且分类器允许了它们通过时使用。
- 提示词：审查生产记录，移除不符合允许定义的任何内容，改进分类逻辑，并验证剩余数据。
- 验证：每个剩余记录符合允许的定义。具有代表性的分类测试和清理后审计证明保留数据有效。
- 关键词：AI 数据运维、生产数据清理、分类逻辑、数据质量审计、回归示例
- 相关：[全产品评估循环](https://signals.forwardfuture.ai/loop-library/loops/full-product-evaluation-loop/)、[日志覆盖循环](https://signals.forwardfuture.ai/loop-library/loops/exhaustive-logging-coverage-loop/)

## 015 — [发布后基线循环](https://signals.forwardfuture.ai/loop-library/loops/post-release-baseline-loop/)

- 分类：运维
- 适用场景：在发布后立即使用，当未来的回归或改进需要对照现在生产中的确切版本来衡量时。
- 提示词：当前发布完成后，运行标准基准并将结果记录为新基线。
- 验证：新基线属于已完成的发布。版本、环境、基准版本、条件和结果一起记录。
- 关键词：AI 发布运维、发布后基准、性能基线、发布验证、基准历史
- 相关：[过期安全批量发布循环](https://signals.forwardfuture.ai/loop-library/loops/stale-safe-batch-release-loop/)、[测试套件速度循环](https://signals.forwardfuture.ai/loop-library/loops/test-suite-speed-loop/)

## 016 — [工单到 PR 就绪循环](https://signals.forwardfuture.ai/loop-library/loops/ticket-to-pr-ready-loop/)

- 分类：工程
- 适用场景：当真实但松散编写的工单、Bug 报告或客户投诉需要变为有边界的工程变更且具备足够证据以便快速审查时使用。
- 提示词：将工单、Bug 报告、失败行为或客户投诉转化为可审查的补丁。在最小的代表性环境中复现失败，证明根因，做最小的可信修复，并重新运行原始复现加相关回归测试。如果两次认真尝试后仍无法复现，说明情况。不要将无关重构折叠进补丁。以原因、变更文件、前后证明、风险和拉取请求摘要结束。
- 验证：失败已修复、验证并准备审查。修复前问题可复现，修复后不再复现，相关回归检查通过。
- 关键词：AI 编码智能体、工单到拉取请求、Bug 复现、根因分析、可审查补丁
- 相关：[生产错误清扫](https://signals.forwardfuture.ai/loop-library/loops/production-error-sweep/)、[质量连胜循环](https://signals.forwardfuture.ai/loop-library/loops/quality-streak-loop/)

## 017 — [客户 AI 部署循环](https://signals.forwardfuture.ai/loop-library/loops/customer-ai-deployment-loop/)

- 分类：运维
- 适用场景：当 AI 工作流必须在真实客户流程中运行，且需要验证、审批、渐进推出、监控和明确业务结果时使用。
- 提示词：当客户请求 AI 工作流、报告失败或到达运维审查时运行。选择一个优先事项，如丰富线索、起草邮件、总结会议或更新 CRM。定义负责人、输入、审批、成功指标和 ROI 假设。在真实客户数据上试运行，修复最小已验证问题，然后通过批准的阶段发布并监控生产。以结果、证据、客户更新、经验教训和下次审查结束。
- 验证：一个客户优先事项达到已证明的终止状态。工作流到达约定的推出阶段、一个生产问题被修复，或一个阻塞问题被升级并有负责人和下一步。
- 关键词：客户 AI 部署、AI 工作流推出、审批门控、生产监控、AI ROI
- 相关：[全产品评估循环](https://signals.forwardfuture.ai/loop-library/loops/full-product-evaluation-loop/)、[质量连胜循环](https://signals.forwardfuture.ai/loop-library/loops/quality-streak-loop/)

## 018 — [产品更新播客循环](https://signals.forwardfuture.ai/loop-library/loops/product-update-podcast-loop/)

- 分类：内容
- 适用场景：当产品发布足够频繁，用户会受益于关于变更内容和用法的简短定期音频解释时使用。
- 提示词：每晚审查公开发布的产品变更，仅选择用户需要知道的。对照产品、文档或发布说明验证每一项。使用 Jellypod MCP 将批准的变更转化为三到五分钟的播客，解释变更了什么、为什么重要以及如何尝试。检查脚本和音频的准确性、清晰度和发音。如果没有有意义的内容发布，不制作节目。发布前询问。以草稿节目、来源和审查结果结束。
- 验证：节目准确覆盖每个有意义的公开更新。以可审查的三到五分钟节目结束，或在无有意义发布时确认的无节目结果。
- 关键词：AI 播客工作流、产品更新播客、Jellypod MCP、发布沟通、编辑自动化
- 相关：[夜间变更日志循环](https://signals.forwardfuture.ai/loop-library/loops/nightly-changelog-sweep/)、[发布后基线循环](https://signals.forwardfuture.ai/loop-library/loops/post-release-baseline-loop/)

## 019 — [Clodex 对抗审查循环](https://signals.forwardfuture.ai/loop-library/loops/clodex-adversarial-review-loop/)

- 分类：工程
- 适用场景：当 Claude 正在构建有意义的代码变更且 Codex 应独立审查每个修复轮次时使用 Clodex。
- 提示词：运行 /clodex [task] think hard --max-iter 5 --threshold medium。Claude 规划任务、实现它、发起拉取请求、向 Codex 请求对抗审查、修复高于接受严重度的发现并重复。保持分支、PR、发现、结论和迭代状态可恢复。当 Codex 批准、仅剩已接受发现、进展停滞或达到迭代上限时停止。绝不将错误或耗尽的运行描述为已批准。以 PR、检查、结论和剩余发现结束。
- 验证：拉取请求达到配置的审查标准。Codex 批准它或仅剩明确接受的发现；错误、停滞和耗尽限制如实报告。
- 关键词：Clodex、Codex 对抗审查、Claude Code 插件、审查修复循环、拉取请求自动化
- 相关：[架构满意度循环](https://signals.forwardfuture.ai/loop-library/loops/architecture-satisfaction-loop/)、[过期安全批量发布循环](https://signals.forwardfuture.ai/loop-library/loops/stale-safe-batch-release-loop/)

## 020 — [Loop Harness 验证循环](https://signals.forwardfuture.ai/loop-library/loops/loop-harness-verification-loop/)

- 分类：工程
- 适用场景：当周期性仓库任务应无人值守运行但不允许一个智能体同时生成和批准相同输出时使用。
- 提示词：使用 Loop Harness 进行计划的仓库工作，如 CI 分诊、Issue 整理、依赖更新或文档同步。设置 [重试限制]，然后启动隔离的 git worktree。让一个 Claude 会话暂存补丁或出箱消息，让第二个 Claude 会话根据明确标准验证它。仅在通过后交付；否则保留发现并在限制内重试。以源版本、暂存输出、验证结果、交付状态和下次运行结束。
- 验证：仅独立验证的输出被交付。第二个智能体通过释放配置的输出；失败的验证保留证据且不产生外部变更。
- 关键词：Loop Harness、计划编码智能体、git worktree 隔离、第二智能体验证、自主智能体工作流
- 相关：[Clodex 对抗审查循环](https://signals.forwardfuture.ai/loop-library/loops/clodex-adversarial-review-loop/)、[文档清扫](https://signals.forwardfuture.ai/loop-library/loops/overnight-docs-sweep/)

## 021 — [波音 747 基准](https://signals.forwardfuture.ai/loop-library/loops/boeing-747-benchmark/)

- 分类：设计
- 适用场景：作为具体的 Three.js 视觉基准使用，或将相同的捕获-批评模式适配到另一个渲染主题。
- 提示词：构建前选择参考图像、评分标准、[视觉阈值] 和 [预算]。用 Three.js 基本元素构建尽可能逼真的波音 747，然后创建截取九个可重复角度的装置。每次变更后，渲染并评分相同视图，让批评者识别最弱特征，在不回归更强视图的情况下修复它。保留最佳版本。在达到阈值、进展停滞或预算耗尽时停止。以模型、九个渲染、分数、剩余差距和运行摘要结束。
- 验证：波音 747 从所有九个角度满足视觉标准。相同的相机装置和标准显示每个所需视图达到预设阈值，或运行报告停滞、预算耗尽和剩余差距。
- 关键词：波音 747 基准、Three.js 智能体工作流、视觉自验证、3D 重建循环、相机检查系统
- 相关：[质量连胜循环](https://signals.forwardfuture.ai/loop-library/loops/quality-streak-loop/)、[全产品评估循环](https://signals.forwardfuture.ai/loop-library/loops/full-product-evaluation-loop/)

## 022 — [War Loops：前端重建](https://signals.forwardfuture.ai/loop-library/loops/war-loops-frontend-designer/)

- 分类：设计
- 适用场景：当授权界面必须从 URL 或图像重建，并以外观、动效和响应行为评判时使用 War Loops。
- 提示词：将 War Loops 指向授权的 URL 或图像。用真实浏览器捕获它并记录布局、样式、内容、动效和响应行为。构建静态 Pencil 镜像和动态 Forge 版本。在桌面、平板和移动尺寸下将两者与源比较；仅修复最弱的保真信号。当每个门控通过、进展停滞或捕获被阻止时停止。以构建、规格、渲染、分数和剩余差距结束。
- 验证：构建在所有三个保真轴上与源匹配。静态外观、体验动效和响应重排通过其门控，或运行报告停滞或捕获被阻止。
- 关键词：War Loops、自主前端设计器、前端保真、视觉评估循环、响应动效匹配
- 相关：[全产品评估循环](https://signals.forwardfuture.ai/loop-library/loops/full-product-evaluation-loop/)、[50ms 页面加载循环](https://signals.forwardfuture.ai/loop-library/loops/sub-50ms-page-load-loop/)

## 023 — [自我改进冠军循环](https://signals.forwardfuture.ai/loop-library/loops/self-improving-champion-loop/)

- 分类：评估
- 适用场景：当低成本迭代有用但最终验收必须使用新样本时，用于调整提示词、策略或配置。
- 提示词：改进提示词、策略或配置。支持助手的系统提示词是一个例子。保存冠军、其分数、工作集、未接触的保留案例、必须通过的检查和 [预算]。每轮根据记录的失败更改一件事。仅当挑战者在保留集上以 [margin] 击败冠军且不削弱必须通过的检查时才推广挑战者；否则保留冠军。在达到目标、预算限制或无进展时停止。返回胜者、分数、实验日志和剩余失败。
- 验证：返回最佳保留测试冠军。每个挑战者都有日志，接受的变更在未接触案例上击败前一冠军且不削弱必须通过的检查。
- 关键词：自我改进循环、冠军挑战者评估、Goodhart 防护、独立评估门控、有界优化工作流
- 相关：[全产品评估循环](https://signals.forwardfuture.ai/loop-library/loops/full-product-evaluation-loop/)、[质量连胜循环](https://signals.forwardfuture.ai/loop-library/loops/quality-streak-loop/)

## 024 — [魔鬼代言人循环](https://signals.forwardfuture.ai/loop-library/loops/devils-advocate-design-loop/)

- 分类：评估
- 适用场景：在承诺架构、接口、推出计划或其他受益于结构化对抗审查的重要设计之前使用。
- 提示词：在承诺架构、接口或推出计划之前，让批评者论证它是错误的。在仓库本地日志 .agent-reviews/redteam.md 中记录每个异议、影响和状态。构建者必须修复并验证每个高影响弱点或记录为何接受；批评者可以重新开启缺乏支持的回答。当没有高影响异议剩余或相同问题在没有新证据的情况下重复两轮时停止。以决策、已解决和已接受的异议、证据和任何僵局结束。
- 验证：没有高影响异议保持开放。每个记录的异议被验证为已解决或有证据明确接受，或最终报告如实记录两轮僵局。
- 关键词：魔鬼代言人循环、对抗设计审查、批评者-构建者工作流、架构异议日志、红队设计流程
- 相关：[架构满意度循环](https://signals.forwardfuture.ai/loop-library/loops/architecture-satisfaction-loop/)、[Clodex 对抗审查循环](https://signals.forwardfuture.ai/loop-library/loops/clodex-adversarial-review-loop/)

## 025 — [全新克隆循环](https://signals.forwardfuture.ai/loop-library/loops/fresh-clone-loop/)

- 分类：工程
- 适用场景：用于测试仓库的入门指南在干净环境中无需未记录帮助是否可用。
- 提示词：将 [仓库] 克隆到一次性环境中，仅按其 README 操作到文档中的就绪状态，如运行应用或构建包。当步骤失败或假设缺失知识时，记录差距、修复设置或文档问题、丢弃环境并重新开始。不在尝试之间携带依赖、配置、凭证或修复。当一个不间断的全新克隆达到该状态、进展停滞或 [预算] 耗尽时停止。返回确切命令、已关闭差距和剩余阻塞。
- 验证：干净环境仅使用 README 达到文档就绪状态。最终运行仅使用入门指南且无需未说明的依赖、配置或手动修复。
- 关键词：全新克隆循环、README 验证、开发者入门测试、干净环境设置、仓库文档工作流
- 相关：[文档清扫](https://signals.forwardfuture.ai/loop-library/loops/overnight-docs-sweep/)、[仓库清理循环](https://signals.forwardfuture.ai/loop-library/loops/repository-cleanup-loop/)

## 026 — [Infinite Clickbait 缩略图循环](https://signals.forwardfuture.ai/loop-library/loops/infinite-clickbait-loop/)

- 分类：设计
- 适用场景：当视频主题和素材集已准备好，但缩略图需要几轮结构化构思和评判才能投入生产时使用。
- 提示词：为 [视频]，使用 [批准素材] 制作十个缩略图概念。在真实 YouTube 尺寸下按 [灵感频道] 为清晰度、好奇心、情感吸引力、对比度和准确性评分每个。取前三名，改进每个最弱维度，并在相同标准下重新评分。持续迭代最强概念直到它通过 [质量阈值] 或 [预算] 耗尽。拒绝视频无法兑现的任何内容。返回胜者、两名亚军、预览、最终分数和理由。
- 验证：一个准确的缩略图通过固定的质量阈值。胜者在相同条件下得分超过替代方案，在真实尺寸下保持清晰，并准确代表视频。
- 关键词：Infinite Clickbait、YouTube 缩略图循环、缩略图迭代工作流、点击诱饵评分标准、AI 视觉设计
- 相关：[波音 747 基准](https://signals.forwardfuture.ai/loop-library/loops/boeing-747-benchmark/)、[全产品评估循环](https://signals.forwardfuture.ai/loop-library/loops/full-product-evaluation-loop/)

## 027 — [autonomy-loop 构建者-审查者循环](https://signals.forwardfuture.ai/loop-library/loops/autonomy-loop/)

- 分类：工程
- 适用场景：当仓库有确定性的测试、构建和 lint 门控，且有适合重复构建者-审查者交接的任务时使用 autonomy-loop。
- 提示词：在测试、构建和 lint 门控通过后，使用 autonomy-loop 进行 [仓库任务]。运行 /autonomy-loop:autonomy-init，然后在单独的 worktree 中启动构建者和审查者。构建者读取 LOOP-STATE.md，做一个有边界变更，并添加红前绿后测试。审查者重新运行门控并通过回退或变异修复来证明测试。仅在两者都通过时接受；将受保护或重复失败的工作留给人类。以提交、门控证据、测试证明、信任级别和风险结束。
- 验证：每个接受的波次通过 autonomy-loop 的测试证明门控。新测试在没有变更时失败、有变更时通过，每个配置的门控通过，受保护的生产变更保持人类门控。
- 关键词：autonomy-loop、对抗代码审查、变异测试、构建者审查者工作流、Claude Code 循环
- 相关：[Clodex 对抗审查循环](https://signals.forwardfuture.ai/loop-library/loops/clodex-adversarial-review-loop/)、[Loop Harness 验证循环](https://signals.forwardfuture.ai/loop-library/loops/loop-harness-verification-loop/)

## 028 — [Codex 完成合约循环](https://signals.forwardfuture.ai/loop-library/loops/codex-completion-contract-loop/)

- 分类：工程
- 适用场景：用于长时间运行的 Codex 工作、拉取请求、运行时检查或用户可见产出物，其中看似合理的部分结果可能被误认为已完成。
- 提示词：运行 $goal-planner-codex [task] 用于长时间运行的 Codex 工作，其中部分工作可能被误认为已完成。落地 PR 并验证生产是一个例子。行动前定义每个必需结果及其证据。每个有边界动作后，将需求标记为已证明、薄弱、缺失或矛盾。仅当所有都已证明时完成 Goal；否则以阻塞、停滞或耗尽停止。创建 Goal 状态前询问。以需求到证据表、状态、负责人和下一步结束。
- 验证：每个 Codex Goal 需求都有当前、充足的证据。最终审计不包含薄弱、缺失或矛盾的必需项；否则工作保持开放、阻塞或耗尽。
- 关键词：Codex Goal、完成合约、证据审计、完成定义、虚假完成防护
- 相关：[工单到 PR 就绪循环](https://signals.forwardfuture.ai/loop-library/loops/ticket-to-pr-ready-loop/)、[质量连胜循环](https://signals.forwardfuture.ai/loop-library/loops/quality-streak-loop/)

## 029 — [Revolve 版本化实验循环](https://signals.forwardfuture.ai/loop-library/loops/revolve-self-improvement-loop/)

- 分类：评估
- 适用场景：当实验必须跨会话保持可比和可恢复时，使用 Revolve 改进提示词、策略、工作流、模型配置、代码路径或数据集。
- 提示词：使用 Revolve 改进支持提示词、代码路径或可测试主体。在 revolve/ 中定义目标和 [预算]，冻结测试和评分，检查点当前版本并记录基线。每轮测试一个假设；仅保留明确的、无回归的胜利。如果评估变更，开启新版本并重新运行基线。更改线上文件前询问。在成功、无进展、阻塞或预算耗尽时停止。返回最佳检查点、比较、回滚和下一步。
- 验证：最佳 Revolve 检查点在一个评估版本内获胜。现任和候选有可比的记录运行，接受的变更通过每个守卫，回滚可用，线上推广有批准。
- 关键词：Revolve、智能体自我改进、检查点评估、版本化实验、证据驱动推广
- 相关：[自我改进冠军循环](https://signals.forwardfuture.ai/loop-library/loops/self-improving-champion-loop/)、[全产品评估循环](https://signals.forwardfuture.ai/loop-library/loops/full-product-evaluation-loop/)
