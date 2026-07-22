---
name: hyperexecute-skill
description: "端到端运营 HyperExecute，用于 TestMu AI/LambdaTest 云测试执行：分析项目、创建 YAML、本地验证、运行 CLI 作业、调试故障及对接 CI。涉及 HyperExecute、hyperexecute.yaml、HyperExecute CLI、autosplit、矩阵执行时使用"
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/hyperexecute-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# HyperExecute 运维
## 适用场景

涉及 HyperExecute 端到端运营（TestMu AI/LambdaTest 云测试执行）时使用：分析项目、创建 YAML、本地验证、运行 CLI 作业、调试故障及对接 CI。当用户提到 HyperExecute、hyperexecute.yaml、HyperExecute CLI、autosplit、矩阵执行等关键词时触发。


## 快速开始

1. 定位 HyperExecute CLI。如未安装，在用户明确批准自主 HyperExecute 会话前需先询问再下载。
2. CLI 可用时运行 `hyperexecute analyze`；仅在无法使用 CLI 时以本地检查作为备选。
3. 根据分析输出、项目测试命令及 `reference/` 中的模板，创建或修复 `hyperexecute.yaml`。
4. 运行 `node scripts/doctor.js --config hyperexecute.yaml` 和 `node scripts/validate-config.js hyperexecute.yaml`。
5. 使用官方 CLI 验证：`./hyperexecute --user "$LT_USERNAME" --key "$LT_ACCESS_KEY" --config hyperexecute.yaml --validate`。
6. 除非用户已明确选择自主 HyperExecute 会话，否则在启动真实云作业前需确认。
7. 遇到故障时，下载日志/产物/报告，参考 `reference/troubleshooting.md`。

## 运维规则

- 以官方 HyperExecute CLI 为分析、验证、执行、日志、报告和产物的唯一权威来源。
- 从本地环境变量或 CI 密钥中读取 `LT_USERNAME` 和 `LT_ACCESS_KEY`；禁止在 YAML 或文档中硬编码凭据。
- `--job-secret-file` 仅用于作业级额外密钥，优先放在仓库外或被 `.gitignore`/`.hyperexecuteignore` 忽略的路径。
- 优先使用模板驱动的 YAML，而非生成脚本，因为测试命令、路径和 payload 边界因项目而异。
- 本地安全检查自动执行；真实 HyperExecute 云作业仅在确认后执行，除非用户已选择自主模式。
- 自主模式下：先验证，再运行，检查输出，按需下载日志/产物，仅在可操作的配置/环境修复时重试。

## 工作流

- 首次运行：分析项目 → 编写 YAML → 运行辅助检查 → 运行 CLI 验证 → 请求确认后启动云作业。
- 调试：复现失败的 CLI 命令，按需加 `--verbose`，下载日志/产物/报告，逐个修复原因。
- CI：使用 CI 密钥，在执行前增加验证阶段，设置 `CI=true` 减少日志噪音，保留失败作业的下载产物。
- 性能：首次成功运行后，调优 `autosplit`、`concurrency`、缓存键、重试、智能排序及矩阵/混合范围。

## 辅助脚本

- `scripts/doctor.js`：检查 CLI 就绪状态、凭据、配置文件是否存在及可选的官方验证。
- `scripts/validate-config.js`：在官方 CLI 验证前，对常见配置错误进行轻量检查。
- `scripts/build-command.js`：使用环境变量引用，输出安全的验证/运行/调试/下载命令。
- `scripts/summarize-artifacts.js`：汇总已下载的日志、报告和产物，便于分类排查。

## 参考资料

- CLI 用法和标志：[reference/cli.md](https://github.com/LambdaTest/agent-skills/tree/main/hyperexecute-skill/reference/cli.md)
- YAML 模式：[reference/yaml-patterns.md](https://github.com/LambdaTest/agent-skills/tree/main/hyperexecute-skill/reference/yaml-patterns.md)
- 框架配方：[reference/frameworks.md](https://github.com/LambdaTest/agent-skills/tree/main/hyperexecute-skill/reference/frameworks.md)
- CI/CD 集成：[reference/ci-cd.md](https://github.com/LambdaTest/agent-skills/tree/main/hyperexecute-skill/reference/ci-cd.md)
- 安全规则：[reference/security.md](https://github.com/LambdaTest/agent-skills/tree/main/hyperexecute-skill/reference/security.md)
- 故障排查：[reference/troubleshooting.md](https://github.com/LambdaTest/agent-skills/tree/main/hyperexecute-skill/reference/troubleshooting.md)

## 限制

- 仅在任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，验证命令、生成的代码、依赖项、凭据及外部服务行为。
- 示例不能替代环境特定的测试、安全审查或用户对破坏性/高成本操作的批准。
