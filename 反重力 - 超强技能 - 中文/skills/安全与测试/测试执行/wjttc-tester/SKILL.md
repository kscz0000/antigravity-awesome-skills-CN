---
name: wjttc-tester
description: F1 启发的测试执行器 + 报告器。运行测试计划、查找并复现缺陷、审查测试套件的信号完整性，然后提交一份带层级裁定的 WJTTC 报告（Brake/Engine/Aero/Tyre/Pit）。适用于需要测试代码、验证功能、复现故障或产出测试报告等场景。
risk: unknown
source: https://github.com/Wolfe-Jam/faf-skills/tree/main/skills/wjttc-tester
source_repo: Wolfe-Jam/faf-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/Wolfe-Jam/faf-skills/blob/main/LICENSE
---

# WJTTC 锦标赛测试器

**"我们把东西打破，让别人永远不必知道它们曾经坏过。"**

将 F1 启发的标准应用到软件测试。刹车必须在比赛节奏下完美工作，生产环境中的代码亦应如此。此技能负责**执行**测试计划并**提交报告** —— 它是车手，不是工程师。要规划并生成测试套件，请使用 **wjttc-builder**。

## 适用场景

- 运行已有的或刚写好的测试计划，并报告结果
- 复现报告中的缺陷并定位根因
- 边界情况 / 错误处理 / 回归验证
- 审查测试套件的 CI 信号是否仍值得信任
- 产出带层级裁定的 WJTTC 报告

## WJTTC 五个层级

按故障影响半径对每项测试分类。前三项确定严重程度；Tyre 与 Pit 覆盖耐久性与发布门禁。

| 层级 | 符号 | 含义 | 示例 |
|------|--------|---------|----------|
| **Brake** | 🚨 | 生命攸关 —— 失败即灾难 | 数据丢失、鉴权绕过、支付错误、无确认即执行破坏性操作 |
| **Engine** | ⚡ | 性能攸关 —— 结果错误 / 体验糟糕 | API 准确性、数据转换、计算、格式合规、性能 |
| **Aero** | 🏁 | 打磨与边界 —— 轻微不便 | UI 瑕疵、罕见的消息格式、可选功能的边界、文档 |
| **Tyre** | 🛞 | 负载下耐久 —— 随时间退化 | 压力/容量、并发、内存增长、大输入 |
| **Pit** | 🔧 | 发布门禁 —— 让你得以继续前行的停站 | 冒烟/回归套件、CI 全绿、已提交 WJTTC 报告 |

先测 Brake。刹车不灵，其他一切都不重要。

## 第 0 步 —— 信号完整性预审（在新增/运行任何内容之前执行）

**红灯 CI 是一份契约：必须始终意味着"停下、查看、修复"。** 一套覆盖率高但红灯飘忽的测试套件，比一套更小但零误报的套件**更**不可信 —— 因为团队已经不再看红灯。修复信号，再去新增测试。

**方法** —— 对过去 30 天的 CI 失败进行分类：

| 桶 | 定义 | 裁定 |
|--------|-----------|---------|
| **真实缺陷** | 红灯对应真实缺陷；通过代码变更修复 | ✓ 信号有效 |
| **飘忽** | 时序/网络/并发噪音；重跑通过，无代码变更 | ✗ 测试设计缺陷 |
| **基础设施** | 缺少密钥、runner 镜像变更、上游依赖 —— 与代码无关 | ✗ 工作流设计缺陷 |

**信号完整性评分：** `SI = 真实缺陷数 / (真实缺陷数 + 飘忽数 + 基础设施数) × 100`

| SI % | 裁定 | 行动 |
|------|---------|--------|
| 100% | ✪ | 保持 —— 典范级信号 |
| 95–99% | ★ 锦标赛级 | 立刻标注任何飘忽项 |
| 85–94% | ◇ 可接受 | 本迭代安排修复飘忽类问题 |
| 70–84% | ● 侵蚀中 | 停止新增测试 —— 先修复飘忽 |
| <70% | ○ 信号失效 | 阻塞合并，直至信号恢复 |

**发现即消除：** 在共享 runner 上做硬性绝对时间性能断言（`expect(t).toBeLessThan(30)`）→ 移至非阻塞工作流；主套件内的网络调用 → 在边界处打桩；无显式顺序的并发测试；缺少密钥就硬性失败的步骤 → 灰度跳过。

**逆向规则：** 绿灯 CI 通过但实际有缺陷，同样是违规。若真实缺陷在绿灯下漏出，必须在修复落地**之前**先写好回归测试。

**对话才是真正的门禁。** CI 只是人 + AI 审查的支撑基础设施；飘忽的 CI 浪费审查的带宽。信号完整性让 CI 对得起这场对话。

## 执行循环

1. **范围** —— 它应做什么？正常路径、边界、失败模式、性能目标、各自的层级。
2. **审计信号**（第 0 步），再去信任或扩展套件。
3. **运行**每项测试：搭建环境、准备数据、执行、观察实际值与预期值、记录通过/失败/阻塞、失败时取证。
4. **复现**每个失败以确定能复现；定位根因；记下修复方案。
5. **层级覆盖检查** —— 确认每项测试都已分层：
   ```bash
   faf wjttc --path tests          # audit tier coverage (vendor-neutral)
   faf wjttc --strict --json       # CI gate: non-zero if any test is untiered
   ```
6. **报告** —— 提交 WJTTC 报告（见下），再呈现层级裁定。

## WJTTC 报告格式

将报告保存到被测项目的 **`./wjttc-reports/`** 目录下（或用户指定的路径）。绝不写入绝对路径或个人路径。文件命名 `YYYY-MM-DD-{project}-{feature}-tests.yaml`。

```yaml
---
# WJTTC Test Report
project: "project-name"
feature: "feature-being-tested"
date: "2026-06-26"
tier: "Engine"            # Brake | Engine | Aero | Tyre | Pit
result: "PASS"            # PASS | FAIL | BLOCKED
environment: "OS, runtime version, key deps"
---

## Summary
objective: What was tested
totals: { total: 25, passed: 23, failed: 2, blocked: 0, pass_rate: "92%" }

## Failures
- name: "Long-string handling"
  tier: "Engine ⚡"
  status: "FAIL"
  steps: ["...", "..."]
  expected: "Handle gracefully"
  actual: "Crash"
  error: "RangeError: ..."
  root_cause: "Unbounded buffer"
  fix: "Cap input length / stream"

## Edge cases
- { case: "Empty string", input: "''", expected: "error", actual: "error", status: "PASS" }
- { case: "Unicode", input: "🏎️", expected: "stored", actual: "stored", status: "PASS" }

## Performance
- { op: "file read",  target: "<50ms", actual: "18ms", status: "PASS" }
- { op: "parse YAML", target: "<50ms", actual: "12ms", status: "PASS" }

## Bugs found
- id: 1
  title: "..."
  severity: "Brake"      # tier doubles as severity
  reproducibility: "Always"
  impact: "Who is affected, how serious"
  fix: "..."

## Coverage
tested:     ["happy path", "edges", "error handling", "perf"]
not_tested: ["concurrent access", "files >100MB"]

## Verdict
tier: "◆ Silver"          # from the tier table below
to_next: ["Fix 2 failing Engine tests", "Add Tyre concurrency tests"]
```

## 层级裁定

将通过率（或 SI 评分）映射到唯一的标准 FAF 层级阶梯。没有第二套阶梯，没有奖牌。

| 分数 | 层级 | 符号 |
|-------|------|--------|
| 100% | Trophy | ✪ |
| 99% | Gold | ★ |
| 95% | Silver | ◆ |
| 85% | Bronze | ◇ |
| 70% | Green | ● |
| 55% | Yellow | ● |
| 1% | Red | ○ |
| 0% | White | ♡ |

FAF 评分是**确定性**的 —— 同样的输入，同样的分数。测试报告也应同样可证伪：每个裁定都可追溯到一次可复现的运行。**FAF 不撒谎。**

## WJTTC 方法笔记

- **用真实数据测**，而非只用过清洗的输入 —— 脱敏的生产数据、混乱的输入、贴近生产的容量。
- **记录每一次失败**，以便可复现：失败的是什么、如何复现、为何重要、如何修复。
- **先分层再测试** —— 严重程度就是层级，所以先分流；`faf wjttc` 强制任何未分层的测试不得通过。
- **接入 CI**，配合 TAF 收据，让报告成为记录的一部分，而非一次性产物：
  ```bash
  faf taf setup --write     # create .github/workflows/taf.yml (test receipts)
  faf score --json          # deterministic score snapshot for the receipt
  ```

## 发布前快速清单

- [ ] 已审计信号完整性（SI ≥ 85%）
- [ ] Brake 测试通过 —— 零容忍
- [ ] 边界 + 错误处理已测
- [ ] Tyre：负载/并发下表现稳定
- [ ] `faf wjttc --strict` 全绿 —— 每项测试都已分层
- [ ] 回归（Pit）套件通过
- [ ] WJTTC 报告已提交至 `./wjttc-reports/`
- [ ] 通过率 ≥ 85%（◇ Bronze，可上生产）

## 资源

- Website: https://faf.one · Skills Site: https://skills.faf.one
- faf-cli: https://github.com/Wolfe-Jam/faf-cli
- 兄弟技能：**wjttc-builder**（规划并生成测试套件）

---

*由 wolfejam.dev 用 🧡 制作 —— "我们把东西打破，让别人永远不必知道它们曾经坏过。"*

## 局限性

- 仅当任务明确匹配其上游来源与本地项目上下文时，才使用此技能。
- 在应用变更之前，请验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要把示例当作特定环境下的测试、安全审查，或针对破坏性/高成本操作的用户授权的替代。