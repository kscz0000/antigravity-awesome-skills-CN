# 自主适配方法

本参考文档定义了自适应自迭代的安全基础。

## 范围

在人类明确批准补丁应用工作流之前，自适应迭代仅作为提案存在。当前实现可执行以下操作：

- 读取一个用户提供的本地源文件；
- 在存储证据摘录前对敏感文本进行脱敏；
- 总结重复出现的偏好与操作信号；
- 生成包含目标文件、风险、测试与回滚方案的适配提案；
- 由已审核的补丁起草一条待审批账本条目，内容涵盖补丁 SHA-256、目标文件、目标基线哈希、验证命令与回滚元数据；
- 在补丁哈希、审批、目标白名单与目标基线哈希检查通过后，通过 `adapt-apply` 对已批准的补丁执行试运行；
- 仅当操作员传入 `--apply` 且审批账本明确记录了审核人、原因、补丁哈希、目标文件、目标文件 SHA-256 基线、验证命令与回滚方案时，才可应用补丁；
- 当 `--run-verification` 失败时，默认自动回滚已应用的补丁，除非操作员明确传入 `--no-rollback-on-failure`。

不得执行以下操作：

- 默认扫描 shell 历史、浏览器历史、聊天记录、邮件或私有目录；
- 由单条评论推断出永久性的用户记忆；
- 在扫描或提案生成阶段写入源文件；
- 在缺少显式 `--apply` 的情况下通过 `adapt-apply` 写入源文件；
- 应用目标文件超出提案与审批白名单范围的补丁；
- 当已批准的目标文件自审核人记录其基线 SHA-256 以来发生变化时，应用该补丁；
- 默认保留验证失败但已完成应用的补丁；
- 将提案视为已完成的实现证据。

## 流程

1. `adapt-scan` 读取显式源路径，并写入 `reports/user_patterns.json` 与 `reports/user_patterns.md`。
2. `adapt-propose` 读取模式报告，并写入 `reports/adaptation_proposals.json` 与 `reports/adaptation_proposals.md`。
3. 审核人决定是否值得实现某个提案。
4. `adapt-apply --write-template` 创建 `reports/adaptation_approval_ledger.json` 与 `reports/adaptation_regression_report.json`，以便在任何补丁应用之前预先建立审核界面。
5. `adapt-apply --prepare-approval --proposal-id <id> --patch-file <patch>` 起草一条 `pending-review` 审批条目。该步骤既不批准补丁，也不应用补丁。
6. 人类审核人将草稿决策修改为 `approved`，填写审核人、原因、审批日期与可选的过期时间，同时保持生成的补丁与目标基线哈希不变。
7. `adapt-apply --proposal-id <id> --patch-file <patch>` 默认执行试运行，并记录补丁、目标、审批、回归与回滚证据。
8. `adapt-apply --apply --run-verification` 仅在审批、补丁哈希、白名单、目标基线哈希、`git apply --check` 与安全回归命令检查全部通过后，才能写入文件。
9. 若补丁应用后某条验证命令失败，`adapt-apply` 默认执行 `git apply -R <patch>`，并在 `reports/adaptation_regression_report.json` 中记录 `failed-rolled-back` 状态与回滚证据。

## 证据标准

每条提案应包含：

- 触发该提案的重复模式；
- 脱敏后的摘录，绝不包含未脱敏的原始内容；
- 目标文件与变更意图；
- 风险等级与边界；
- 验证命令；
- 回滚方案；
- 明确的 `proposal-only` 状态。

每次批准的应用应包含：

- 审核人、原因、审批日期与可选的过期时间；
- 精确的补丁 SHA-256；
- 目标文件白名单；
- 每个补丁目标的目标文件 SHA-256 基线，已批准的新文件则标注为 `__absent__`；
- 仅限于本地 `make` 目标或本地 Python 验证脚本的回归命令；
- 回滚命令或方案；
- 若应用后回归失败，需附回滚结果。

## 审核边界

自适应循环可提升迭代质量，但无法替代常规审核。任何涉及触发行为、报告、打包、遥测、隐私或治理的提案，仍须通过与人工设计的变更相同的测试与发布关卡。`adapt-apply` 的证据能够证明已批准的补丁路径已经过检查或应用；但它无法使外部或人工证据达到世界级完备。