# 信任安全方法

信任检查能让技能在安装与评审时更安全，尤其当技能内含脚本或需要分发给团队时。

## 何时运行

在以下场景运行信任报告：

- 技能包含脚本
- 技能将分发给团队
- 软件包可能从注册表或插件安装
- 技能读取外部文件、使用网络访问或调用外部命令
- 成熟度等级为 library 或 governed

## V0 检查项

- 明显的密钥模式
- 脚本的帮助输出与交互式提示
- 执行级 `--help` 冒烟检查
- 依赖锁定
- 运行时信任元数据
- 具备网络访问能力的脚本
- 具备网络访问能力脚本的有界主机策略
- 高权限能力的评审者批准权限策略
- 适配器契约与元数据回退边界的打包目标运行时权限探针
- 源契约完整性摘要

## 脚本接口规则

`scripts/` 下的每个 Python 文件都作为软件包信任面的一部分接受审查。

- CLI 脚本应使用 `argparse`，以便评审者和安装者在执行前运行 `python3 scripts/name.py --help`。
- 信任报告对使用 `argparse` 的 CLI 脚本执行 `python3 scripts/name.py --help`，设置较短超时，并记录通过/失败证据。
- 仅供导入的模块应在文件顶部附近声明 `SCRIPT_INTERFACE = "internal-module"`。
- 内部模块还应声明 `SCRIPT_INTERFACE_REASON`，简要说明哪个 CLI 或渲染器导入了它们。
- 信任报告将内部模块保留在脚本清单中，但将其排除在 CLI 帮助面警告之外。
- 默认情况下，未显式声明为内部模块的 Python 文件被视为 CLI 脚本。
- 没有 `argparse` 的 CLI 脚本不进行冒烟执行，仍以帮助面警告形式可见。

## 网络策略规则

具备网络访问能力的脚本在分发给团队前必须受机器可读策略约束。

- 策略文件放在 `security/network_policy.json`。
- 在 `scripts` 下为每个具备网络访问能力的脚本添加一条记录。
- 声明 `allowed_hosts`、`allowed_path_prefixes`、用途、超时、认证模式以及自定义主机行为。
- 默认仅允许 HTTPS，并拒绝自定义主机，除非通过 CLI 标志或环境变量显式覆盖。
- 信任报告比对每个脚本中的 HTTPS URL 字面量与 `allowed_hosts`；缺失或不匹配的条目会以评审者可见的警告保留。

## 权限审批规则

高权限能力在 governed 发布前必须获得批准。

- 批准记录放在 `security/permission_policy.json`。
- 覆盖信任报告检测到的每个所需能力：若存在 `network`、`file_write`、`subprocess` 和 `interactive`。
- 每条批准必须包含 `decision: approved`、`reviewer`、`scope`、`reason`、`expires_at`、`evidence` 和 `target_enforcement`。
- Review Studio 将这些检查以 `permission-gates` 关卡形式呈现。
- 缺失、无效或过期的批准会阻断 governed 模式。在较宽松模式下仍以可见警告保留。

## 运行时权限探针规则

权限审批验证评审者意图。运行时权限探针在打包后验证生成的目标适配器。

- 在 `cross_packager.py` 之后运行 `python3 scripts/probe_runtime_permissions.py . --package-dir dist`。
- 探针写入 `reports/runtime_permission_probes.json` 和 `reports/runtime_permission_probes.md`。
- 通过探针要求每个目标适配器都携带 `permission_contract`、`target_permission_contract`、已声明的能力、原生强制布尔值、表示说明和操作员说明。
- 当 `reports/install_simulation.json` 与同一软件包目录匹配时，探针还会报告来自安装模拟的安装器强制计数。这证明本地软件包安装器关卡已接入，但不计为目标客户端的原生强制。
- 若某目标无原生强制，探针必须明确标记元数据回退，并将残余风险保留为评审者可见。
- Review Studio 将其以 `permission-runtime` 关卡形式呈现。

## 发布规则

高风险密钥或不受限的远程内联执行会阻断 governed 发布。警告对评审者可见，但除非发布负责人判定目标环境需要更严格策略，否则不阻断 v0。

## 哈希范围

`package_sha256` 是稳定的源契约摘要，而非生成的归档摘要。它覆盖技能入口点、元数据、脚本、references、evals、runtime、templates、安全说明、Skill IR 以及根目录控制文件。它故意排除生成的 `reports/`、打包的 `dist/` 归档以及原始本地遥测，以避免报告渲染或本地采用日志篡改信任指纹。

分发归档的校验和使用软件包验证或注册表审计报告。
