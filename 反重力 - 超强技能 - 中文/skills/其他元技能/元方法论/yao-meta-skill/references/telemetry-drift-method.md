# 遥测与漂移方法

遥测把真实使用转化为下一轮迭代队列。默认必须保持本地优先、仅元数据。

## 使用时机

技能属于生产级、库级、治理级、团队分发，或被多个工作流反复调用时，使用遥测漂移循环。

不要采集原始 prompt、模型输出、对话记录、笔记、消息或私有文件。如果审阅者需要示例，请单独存储脱敏后的测试夹具，并作为评测证据而非遥测引用。

## 事件契约

本地事件流为 `reports/telemetry_events.jsonl`，字段做了有意的收敛：

```json
{
  "event": "skill_activation",
  "skill": "example-skill",
  "version": "2.0.0",
  "source": "yao_cli",
  "command": "quickstart",
  "activation_type": "implicit",
  "outcome": "accepted",
  "failure_type": "none",
  "timestamp": "2026-06-13T10:00:00Z"
}
```

允许的事件：`skill_activation`、`skill_output`、`script_run`、`review_event`。

允许的 source：`manual`、`yao_cli`、`external`、`unknown`。

允许的 outcome：`accepted`、`edited`、`rejected`、`missed`、`failed`、`reviewed`、`unknown`。

允许的 failure_type：`wrong_trigger`、`under_trigger`、`bad_output`、`missing_resource`、`script_error`、`review_overdue`、`none`。

`source` 与 `command` 是元数据字段。它们可以表明 `yao.py` 运行了 `quickstart`、`validate`、`output-exec` 等子命令，但不得包含参数、prompt 文本、文件内容、模型输出、对话记录或审阅者笔记。

## CLI 采集

`scripts/yao.py` 可自动记录仅含元数据的 `script_run` 事件。该能力是可选的，以保持发版证据的可复现性，并避免意外的本地写入：

```bash
YAO_CLI_TELEMETRY=1 python3 scripts/yao.py validate .
```

可选的目标路径覆盖：

```bash
YAO_CLI_TELEMETRY=1 \
YAO_CLI_TELEMETRY_EVENTS=/tmp/yao-telemetry.jsonl \
python3 scripts/yao.py output-exec
```

在子命令前可使用等价的全局开关：

```bash
python3 scripts/yao.py --record-cli-telemetry validate .
python3 scripts/yao.py --no-cli-telemetry validate .
```

成功的 CLI 运行记录 `event=script_run`、`source=yao_cli`、`outcome=accepted`、`failure_type=none`。失败的 CLI 运行记录 `outcome=failed` 与 `failure_type=script_error`。命令名仅归一化为子命令本身，永远不记录命令参数。

## 外部客户端发送

外部客户端、浏览器扩展、编辑器适配器或包装脚本，可在导入到聚合漂移报告前，向本地暂存一次写入一条已脱敏的事件：

```bash
python3 scripts/yao.py telemetry-emit . \
  --event skill_activation \
  --activation-type explicit \
  --outcome accepted \
  --command browser-extension
```

默认写入 `.yao/telemetry_spool/external_events.jsonl`。当客户端需要不同的本地交接路径时，使用 `--output-jsonl`：

```bash
python3 scripts/yao.py telemetry-emit . \
  --output-jsonl /tmp/external-client-events.jsonl \
  --event skill_output \
  --activation-type manual \
  --outcome edited \
  --command browser-plugin
```

使用 `--dry-run` 在不写入暂存的情况下校验拟提交的事件。发送器与导入使用同一份仅元数据契约：不接受 prompt、输入、输出、对话、消息、笔记、原文、参数或未知字段。

客户端完成一批后，导入暂存：

```bash
python3 scripts/yao.py telemetry-import . --input-jsonl .yao/telemetry_spool/external_events.jsonl
```

## 客户端 Hook 配方

使用 `telemetry-hooks` 生成可审计的 Browser、Chrome、VS Code、CLI 包装与 provider-adapter Hook 配方：

```bash
python3 scripts/yao.py telemetry-hooks .
```

报告写入到：

- `reports/telemetry_hook_recipes.json`
- `reports/telemetry_hook_recipes.md`

每条配方包含 dry-run 命令、发送命令、目标本地暂存、触发点与隐私契约。报告中有意将 `native_auto_capture=false`：它证明本地 Hook 契约与仅元数据命令形态，而非证明宿主客户端已原生集成。

## 浏览器原生宿主

`scripts/telemetry_native_host.py` 实现 Browser/Chrome 原生消息机制的本地端。它在 stdio 上接受带长度前缀的 JSON 消息，使用同一份仅元数据遥测契约进行校验，将通过的事件追加到本地暂存，并拒绝原始 prompt、output、transcript、message、note 字段。

无需安装浏览器即可烟雾测试一条消息：

```bash
python3 scripts/telemetry_native_host.py . \
  --message-json '{"event":"skill_activation","activation_type":"explicit","outcome":"accepted","failure_type":"none","command":"chrome-native-host"}'
```

为操作员安装的扩展生成本地启动器与 Chrome 原生消息清单：

```bash
python3 scripts/telemetry_native_host.py . \
  --write-launcher /tmp/yao-telemetry-host.sh \
  --write-manifest /tmp/yao-telemetry-host.json \
  --allowed-origin chrome-extension://aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/
```

这是一个可执行的原生宿主桥接器与清单生成器。它依然不证明用户的浏览器/Chrome 扩展已实际安装或正在发送事件。

## 外部客户端导入

外部客户端、浏览器扩展、编辑器适配器或包装脚本，可通过 `telemetry-import` 交接已脱敏的 JSONL：

```bash
python3 scripts/yao.py telemetry-import . \
  --input-jsonl /tmp/external-client-events.jsonl \
  --command browser-extension
```

导入器在缺失 `source` 时默认填充为 `external`，缺失 `command` 时填充为 `external-client`。它会在写入前校验整个 JSONL 文件。若任意一行包含原始内容字段、不受支持的 source、不受支持的 outcome、不受支持的 failure_type、未知字段、格式错误的 JSON 或不安全的命令名，则整批导入被拒绝，且既有本地事件流保持不变。

使用 `--dry-run` 在不写入 `reports/telemetry_events.jsonl` 也不刷新聚合报告的情况下校验外部批次：

```bash
python3 scripts/yao.py telemetry-import . --input-jsonl /tmp/external-client-events.jsonl --dry-run
```

## 隐私规则

原始 JSONL 事件日志属于本地证据，不应随技能包分发。可分发的产物是聚合报告：

- `reports/adoption_drift_report.json`
- `reports/adoption_drift_report.md`

包构建者应排除 `reports/telemetry_events.jsonl`。根仓库同样忽略此原始事件流，以免本地使用证据意外成为普通源码历史的一部分。

## 发版解读

- `no-data`：对首个脚手架可接受，但对治理级发版审查属于警告。
- `low`：存在事件，且没有漂移失败信号。
- `medium`：存在至少一个 missed trigger、wrong trigger、bad output、script error 或 review overdue 信号。
- `high`：存在多个漂移信号；在判定技能达到发版就绪前，应将其转化为评测用例或治理动作。

## 迭代循环

1. 通过 `adoption-drift --record-event` 手动记录，或通过 `yao.py` CLI 的可选自动采集，或通过 `telemetry-emit` 客户端 Hook，或通过 `telemetry-hooks` 生成的客户端配方，或通过校验后的外部 JSONL 导入，本地采集仅含元数据的事件。
2. 渲染 `reports/adoption_drift_report.md`。
3. 将 missed trigger 转化为 trigger 评测用例。
4. 将 bad output 转化为 Output Eval 断言与失败分类条目。
5. 将 script error 转化为非交互式烟雾测试。
6. 将 review overdue 信号反馈到 Skill Atlas 与负责人复审。
7. 让 Skill Atlas 仅读取 `reports/adoption_drift_report.json`，并发布组合层级的 `skill_atlas/drift_signals.json`。

## Review Studio 角色

Review Studio 应将聚合遥测关卡呈现为运转中的循环，而非原始日志。阻塞意味着遥测契约被违反。警告意味着证据缺失或漂移信号需要跟进用例。

## Skill Atlas 角色

Skill Atlas 使用聚合的采纳漂移报告对组合工作排序。它应对可操作的 production/library/governed 技能暴露 no-data 警告，并对 missed trigger、wrong trigger、bad output、missing resource、script error、review overdue 计数暴露漂移警告。它不得检查原始 JSONL 遥测，也不得将不可操作的示例/夹具信号作为发版阻塞项。
