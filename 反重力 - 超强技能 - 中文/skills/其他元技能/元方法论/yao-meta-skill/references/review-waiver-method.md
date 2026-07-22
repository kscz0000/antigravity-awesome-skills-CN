# 审查豁免方法

审查豁免使人类对风险的接受变得显式。它们不是隐藏问题的方式；而是为某个有界发布窗口中、审查者有意接受的告警级风险提供的本地审计记录。

## 使用时机

在以下情况使用豁免：

- Review Studio 显示一个已被理解并有意接受的告警。
- 在发布前无法在不带来更糟糕权衡的前提下修复该告警。
- 审查者能够给出原因、范围、证据和到期日期。

不要在 v0 中对阻塞门使用豁免。阻塞门必须在声明生产、库、治理或公开发布就绪之前被修复。在治理模式下，缺失或无效的高权限审批属于阻塞门，应当在 `security/permission_policy.json` 中修复，而不是通过豁免绕过。

## 必填字段

每条豁免都必须包含：

- `gate_key`：被接受的 Review Studio 门。
- `decision`：`accepted-risk`、`false-positive` 或 `temporary-exception`。
- `reviewer`：承担责任的人类或团队。
- `reason`：至少 20 个字符的具体原因。
- `created_at`：ISO 日期。
- `expires_at`：ISO 日期。
- `evidence`：可选的路径或备注，用于解释该决定。
- `scope`：默认为 `current-release`。

## 门键策略

豁免台账必须显式跟踪 Review Studio 的门全集：

- `review_studio_gate_keys`：Review Studio 能够渲染的所有门。
- `waiverable_gate_keys`：可被有界人类接受的告警级门。
- `non_waivable_gate_keys`：不得通过豁免接受的门。

当 Review Studio 新增或重命名门时，需在同一次变更中更新豁免门策略及其测试。`review-waivers` 与 `world-class-evidence` 保持不可豁免：前者本身就是豁免机制，后者只能由已接受的台账证据来满足。

## 发布语义

- 无效的豁免记录会阻塞 Review Studio。
- 过期的豁免记录保持可见，但不再覆盖告警。
- 处于生效状态的豁免仅覆盖其明确指定的那一个门键。
- 没有生效豁免的告警仍以告警形式保持可见。
- 原始用户提示、输出、凭据及私有会话记录不得存储在豁免原因中。

## 命令

渲染或校验台账：

```bash
python3 scripts/render_review_waivers.py .
```

新增一条有界审批：

```bash
python3 scripts/yao.py review-waivers . \
  --add-waiver \
  --gate-key trust-report \
  --reviewer "Yao Team" \
  --reason "Network-capable scripts are documented and bounded for this release." \
  --expires-at 2026-09-30
```

对于非治理发布（其中 `permission-gates` 仅作为告警），同一命令可将 `--gate-key` 指定为 `permission-gates`。治理发布则必须改为在 `security/permission_policy.json` 中提供 reviewer、scope、reason、expiry、evidence 以及 target-enforcement 字段。

Review Studio 读取 `reports/review_waivers.json` 并链接到 `reports/review_waivers.md`。

## 候选操作

豁免报告还会基于本地证据展示当前的候选操作：

- 可豁免的告警候选，例如由待定的审查者决定或缺失的供应商支撑运行导致的 `output-lab` 告警
- 不可豁免的边界，特别是 `world-class-evidence`，其中待定的台账证据无法通过豁免转化为完成

豁免可以使一个有界的告警在发布窗口内可审计。它不能算作供应商支撑证据、人类裁定、原生运行时强制、外部遥测或公开的 world-class 就绪。