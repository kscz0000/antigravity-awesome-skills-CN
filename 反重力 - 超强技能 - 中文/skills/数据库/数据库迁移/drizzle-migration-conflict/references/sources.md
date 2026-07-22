# 来源参考

最近核对时间：2026-06-18。

当答案依赖上游 Drizzle 行为、社区脚本或 CI 平台行为时，请参考本文件。Drizzle Kit 迁移内部实现可能发生变化，因此解决实际冲突时，应优先参考当前官方文档和项目所安装的 `drizzle-kit` 版本，而不是凭记忆判断。

## 官方与半官方 Drizzle 来源

| 来源 | 链接 | 用途 | 可信度 |
| --- | --- | --- | --- |
| Discussion 1104 | https://github.com/drizzle-team/drizzle-orm/discussions/1104 | 关于旧式 `_journal.json` 与快照冲突的原始团队协作讨论线程。有助于理解为什么并行生成的迁移会分歧。 | Drizzle GitHub 讨论；有用但可能包含过时评论。 |
| Discussion 2832 | https://github.com/drizzle-team/drizzle-orm/discussions/2832 | 迁移目录结构重新设计与背后的理由。用于理解旧式扁平结构为何对 git 不友好。 | Drizzle GitHub 讨论；设计背景可能早于当前发布版本的行为。 |
| Discussion 5005 | https://github.com/drizzle-team/drizzle-orm/discussions/5005 | 较新版本 Drizzle Kit 中的可交换迁移检查、`drizzle-kit check` 及冲突行为。 | 对当前方向价值较高；需结合已安装版本进行核对。 |
| Discussion 5581 | https://github.com/drizzle-team/drizzle-orm/discussions/5581 | 实用的"以父分支为真源"修复工作流。 | 社区工作流；操作手册良好，仍需结合仓库状态核对。 |
| Generate docs | https://orm.drizzle.team/docs/drizzle-kit-generate | Drizzle Kit 如何从 schema 与快照派生迁移。 | 官方文档。 |
| Check docs | https://orm.drizzle.team/docs/drizzle-kit-check | 面向团队工作流的迁移一致性检查。 | 官方文档。 |
| Migration overview | https://orm.drizzle.team/docs/migrations | 通用迁移概念以及当前官方迁移概览。 | 官方文档。 |

## 社区脚本

以下脚本仅作参考。在未提供 dry-run 模式并获得用户显式确认前，不要将其破坏性行为照搬进通用智能体工作流。

| 来源 | 链接 | 用途 | 注意事项 |
| --- | --- | --- | --- |
| Legacy undo script | https://gist.github.com/anthonyjoeseph/102c0e3ea8496fe111029a8b8a95cc3a | 展示旧式 Drizzle 迁移产物在合并时的撤销工作流。 | 假设为旧式结构，所用 git/文件操作可能丢弃本地已生成文件。 |
| Legacy repair script | https://gist.github.com/anthonyjoeseph/6b99beb34d494acd1dfc83a192ed9388 | 检测旧式迁移编号重复，可通过移除孤儿已生成文件进行修复。 | `FORCE_FIX` 具破坏性；除非用户确认，否则仅复用其只读检查部分。 |
| Earlier repair variant | https://gist.github.com/gburtini/7e34842c567dd80ee834de74e7b79edd | 用于了解历史背景和比较冲突检测逻辑。 | 早期变体存在的注意事项已在新分支中修正；不要单独依赖它。 |

## CI 与合并队列来源

| 来源 | 链接 | 用途 | 注意事项 |
| --- | --- | --- | --- |
| GitHub merge queue docs | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue | 说明合并队列行为，以及为什么必需检查也需对 `merge_group` 事件运行。 | 合并队列仅串行化合并；它本身不会重新生成 Drizzle 迁移。 |

## 与版本相关的指引

在对真实仓库给出高置信度建议前：

1. 先从 `package.json` 与锁文件中检查本地 `drizzle-kit` 版本。
2. 检查迁移输出使用的是旧式扁平结构还是目录式结构。
3. 如果允许执行命令且依赖已安装，应使用仅本地的包管理器命令。优先使用 `pnpm exec drizzle-kit --version`、`yarn exec drizzle-kit --version` 或 `npm exec --no-install drizzle-kit -- --version`。不要使用裸 `npx` 来探测版本，因为它可能下载或解析到不同的包。
4. 如果可以使用联网浏览且用户要求当前指引，请重新打开官方文档及与所安装版本最相关的讨论。
5. 如果本地结果与这些来源存在冲突，以本地仓库状态为准，并显式报告该不一致。
