---
name: doubt-driven-development
description: 在每一个非平凡决策落地之前，先用全新上下文的对抗式审查进行质询。当正确性比速度更重要时、当你在陌生的代码中工作时、当风险较高（生产、安全敏感逻辑、不可逆操作）时、或者任何自信的判断都可能掩盖盲区时使用。触发词：对抗式审查、怀疑驱动开发、新鲜上下文审查、跨模型升级、CLAIM、ARTIFACT、CONTRACT、RECONCILE、STOP、doubt cycle。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/doubt-driven-development
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# 怀疑驱动开发

## 概述

自信的答案不等于正确的答案。在长会话中，上下文会悄悄堆积，把假设伪装成"事实"，没人注意到。怀疑驱动开发（doubt-driven development）是一种纪律：在任何非平凡输出落地之前，物色一位全新上下文（fresh-context）的审查者——其立场偏向**反驳**而非赞同。

这不是 `/review`。`/review` 是对已完成产物的裁决。这是一种"在飞行中"的姿态：非平凡决策在偏离航向仍可低成本修正的窗口内，就被交叉质询。

## 适用场景

当以下条件**至少一项**满足时，决策就是**非平凡**的：

- 引入或修改了分支逻辑
- 跨越模块或服务的边界
- 断言了类型系统或编译器无法验证的属性（线程安全、幂等性、顺序、不变量）
- 其正确性依赖于未来读者看不到的上下文
- 其爆炸半径不可逆（生产部署、数据迁移、公开 API 变更）

在以下情形应用本技能：

- 即将在不确定下做出架构决策
- 即将提交非平凡的代码
- 即将断言非显而易见的事实（"这是安全的""这能扩展""这符合规范"）
- 在你没有完全理解的代码中工作

**不应使用的情形：**

- 机械操作（重命名、格式化、文件移动）
- 遵循明确、无歧义的用户指令
- 阅读或概括已有代码
- 正确性显而易见的一行变更
- 纯工具操作（运行测试、列出文件）
- 用户明确要求速度优先于验证

若对每一次按键都心存怀疑，你什么也交付不了。本技能仅适用于上文定义的非平凡决策。

## 加载约束

本技能是为**主会话编排者**设计的，由其 Step 3（DOUBT，下文详述）来派生一位全新上下文的审查者。

- **不要把本技能加到某个 persona 的 `skills:` frontmatter 中。** 会按 Step 3 行动的 persona 会再派生另一位 persona —— 这正是 `references/orchestration-patterns.md` 明令禁止的编排反模式（"personas 不能调用其他 personas"）。
- **若你在子智能体（subagent）上下文中应用本技能**（Claude Code 禁止嵌套派生子智能体），优先做法是向用户说明怀疑驱动无法在嵌套环境中运行，交由主会话处理。仅在最后手段下，存在一种降级的自我提问后备方案：将 ARTIFACT + CONTRACT 重写为新的自提问提示，与先前的推理之间设置硬性的心智分隔，然后走完 Step 1–5。这**不是新鲜上下文审查**（你带着自己的上下文），所以应将结果标记为降级，并在用户可达时优先升级。

## 流程

应用本技能时，复制以下清单：

```
Doubt cycle:
- [ ] Step 1: CLAIM — 写出主张及"为何重要"
- [ ] Step 2: EXTRACT — 抽出工件 + 契约，去掉推理
- [ ] Step 3: DOUBT — 以对抗式提示调用全新上下文的审查者
- [ ] Step 4: RECONCILE — 对照工件文本逐条归类发现
- [ ] Step 5: STOP — 满足停止条件（发现琐碎、3 轮循环、或用户覆盖）
```

### Step 1: CLAIM —— 把要落地的东西说清楚

用两到三行给决策取名：

```
CLAIM: "The new caching layer is thread-safe under the
        read-heavy workload described in the spec."
WHY THIS MATTERS: a race here corrupts user data and is
                  hard to detect in QA.
```

如果你无法用这么紧凑的篇幅写下来，那你拥有的不是决策，而是一种"感觉"。先把它说出来，再去审视它。

### Step 2: EXTRACT —— 提取最小可审单元

全新上下文的审查者需要的是**工件（artifact）**和**契约（contract）**，而不是思考过程。

- 代码：差异或函数本身 —— 不是整个文件
- 决策：用 3–5 句话描述提案，外加它必须满足的约束
- 断言：主张本身加上理应支持它的证据（与 Step 1 的 CLAIM 块保持区分 —— 那是编排者本人待审视的假设）

剥离你的推理。若你交出的是结论，得到的也只能是对结论的确认。可审单元必须小到审查者一次通读就能装进脑子 —— 如果是 500 行的 PR，先拆分。

### Step 3: DOUBT —— 调用全新上下文的审查者

给审查者的提示语**必须是对抗式的**。措辞决定了答案。

```
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Existing conventions this might break
- Failure modes under unexpected input

Do NOT validate. Do NOT summarize. Find issues, or state
explicitly that you cannot find any after thorough examination.

ARTIFACT: <paste artifact>
CONTRACT: <paste contract>
```

**只传 ARTIFACT + CONTRACT，绝不要传 CLAIM。** 把自己的结论递给审查者，会让它偏向于认同。审查者必须独立判断工件是否满足契约。

在 Claude Code 中，`agents/` 目录下的角色化审查者天生以隔离上下文启动，可直接复用 —— 参见 `agents/` 的人员名册与领域匹配。

**上面的对抗式提示语优先于 persona 的默认响应形态。** 例如 `code-reviewer` 之类的 persona 默认会同时给出优点与缺陷的平衡裁决；而怀疑驱动要的是"只输出问题"。在调用时把上面的对抗式提示原样粘进去，以覆盖 persona 的默认行为。若某个 persona 的响应形态无法干净地覆盖，则退回通用子智能体，直接使用对抗式提示。

#### 跨模型升级

单一模型的审查者会与原作者共享盲点 —— 一个更冷、架构不同的模型能抓住它们。怀疑驱动本就是非平凡决策才启用，所以在此范围内提供跨模型本身就是技能价值的一部分，不是可选的摩擦。

**交互式会话中：始终主动提出，绝不静默跳过。**

**Step 1：询问用户**

Step 3 的单模型审查完成之后、进入 RECONCILE 之前，停下来问：

> *"Single-model review complete. Want a cross-model second opinion? Options: Gemini CLI, Codex CLI, manual external review (you paste it elsewhere), or skip."*

这个问题在每一次交互式怀疑周期中都是强制的 —— 即便工件看起来风险不高。由**用户**决定代价是否值得。智能体的职责是把选择摆到台面上。

**Step 2：若用户选了某个 CLI —— 先验证，再调用**

1. 检查工具是否在 PATH 中（`which gemini`、`which codex`）。
2. 在传入完整提示前先跑一下（`gemini --version` 或等价命令）—— 陈旧或损坏的二进制可能通过 `which`，却在真实输入上失败。
3. 与用户确认精确的调用方式，包括必需旗标、认证、环境变量（如 API 密钥）。各家实现差异大，绝不假设。
4. 只传 ARTIFACT + CONTRACT + 对抗式提示。不带会话上下文，不带 CLAIM。
5. 注意 shell 转义。工件若包含引号、`$(...)` 或反引号，优先用 stdin（`echo … | gemini`）或 heredoc，而不是内联的 `-p "…"`。拿不准时，先请用户确认调用方式再执行。
6. 将输出带入 Step 4（RECONCILE）。

**绝不要把工件插值到带 shell 引号的位置。** 代码、Markdown、审查提示常常包含反引号、`$(...)` 和引号字符，要么会把提示截断，要么会执行嵌入的 shell。把完整提示写到文件、用 stdin 传入。

示例形态（旗标请以本机实际安装的工具为准 —— 不同实现、不同版本语法各异）：

```bash
# Write the adversarial prompt + ARTIFACT + CONTRACT to a temp file first.
# Then pipe via stdin so shell metacharacters in the artifact stay inert.

# Codex (read-only sandbox keeps the CLI from writing to your workspace):
codex exec --sandbox read-only -C <repo-path> - < /tmp/doubt-prompt.md

# Gemini ('--approval-mode plan' is read-only; '-p ""' triggers non-interactive
# mode and the prompt is read from stdin):
gemini --approval-mode plan -p "" < /tmp/doubt-prompt.md
```

只读沙箱是承重的关键细节：怀疑工件本身可能含有指令（无论是故意的还是意外的 prompt 注入），而跨模型 CLI 若不沙箱化就会对你的工作区执行这些指令。

**Step 3：若 CLI 不可用或失败**

明确把失败摆到台面上。提议：手动执行、换一个工具、或跳过。不要默默回退到单模型 —— 用户应当知道跨模型没有发生。

**Step 4：若用户选择跳过**

在输出中承认这次跳过（*"Proceeding with single-model findings only"*），然后继续 RECONCILE。跳过本身没问题；无声地跳过才不行。

**非交互式上下文**（CI、`/loop`、autonomous-loop、定时运行）：

- 跨模型**跳过**，且跳过必须在输出中明示：*"Cross-model skipped: non-interactive context."*
- **未经用户明确授权，绝不调用外部 CLI** —— 这是承重的安全属性。

跨模型会增加成本、延迟与工具脆弱性。智能体每次循环都把选择摆上桌；用户决定这次工件是否值得。

### Step 4: RECONCILE —— 把发现折叠回来

审查者的输出是数据，不是裁决。**你仍是编排者。** 在归类每一条发现之前，先重读工件文本对照 —— 走形式地盖橡皮章与忽视它，是同一种失败模式。

对每一条发现，按下列**优先级顺序**归类（命中即停）：

1. **契约误读** —— 审查者标记此点，正是因为你给的 CONTRACT 不清晰或不完备。先修契约，下一轮再归类。
2. **有效 + 可行动** —— 真实问题，需要改动工件。改完，重启循环。
3. **有效的权衡** —— 问题真实，但修复成本高于接受成本。把权衡明确写出来，让用户看到。
4. **噪声** —— 审查者标记的东西，在它没看到的上下文里其实是正确的。记下、继续，并问自己：若把那段上下文加进契约，能否避免这次误报？

全新审查者也可能因为缺少上下文而错。不要因为"新"就一味服从。

### Step 5: STOP —— 有界循环，而非无限递归

满足以下任一条件即停止：

- 下一次迭代只返回琐碎或已考量过的发现，**或者**
- 已完成 3 轮循环（升级到用户，不要独自进入第 4 轮），**或者**
- 用户明确说"ship it"

若 3 轮之后审查者仍抛出实质性问题，工件可能尚未就绪。把这一点摆给用户 —— 三轮未解决已是关于工件本身的信息，不是继续循环的理由。

若工件很大，让 3 轮"明显不够"：那说明工件太大 —— 回到 Step 2 拆解。不要抬高上限。

## 常见借口

| 借口 | 现实 |
|---|---|
| "我有把握，跳过怀疑步骤" | 在新颖问题上，自信与正确性的相关性很差。越是确信的时刻，盲点越容易藏身。 |
| "派生审查者代价高" | 在生产里调试一笔错误的提交，代价更高。怀疑检查是有界的，缺陷却不是。 |
| "审查者只会抠细节" | 那是因为没限定范围。把提示语收敛为"会让该工件违反契约的问题"。 |
| "我等做完了再用 `/review` 来怀疑" | `/review` 是最后一道闸。怀疑驱动在方向尚可纠正的早期抓错方向 —— 等到 PR 阶段已晚。 |
| "每一步都怀疑，我就交付不了了" | 本技能针对的是非平凡决策，而非每次按键。回头看"不应使用"一节。 |
| "两种意见总比一种好" | 当第二种意见掌握更少上下文、只产出噪声时就不见得。要调和，不要盲从。 |
| "审查者反对，所以我错了" | 审查者缺少你的上下文 —— 分歧是信息，不是裁决。重读工件、归类，再决定。 |
| "跨模型总是更好" | 跨模型能抓住单一模型与自身共享的盲点，但它有成本与工具脆弱性。交互式怀疑周期里每次都主动提供 —— 用户决定这次工件是否值得。智能体的职责是把选择摆上桌，而不是替用户拍板。 |
| "用户点头过一次，我就能反复调用 CLI" | 每次调用都是一次新的授权。工件、提示、旗标每次都在变 —— 每次运行前都要与用户重新确认具体命令。 |

## 危险信号

- 为一次重命名或格式化变更派生一个全新上下文的审查者
- 不重读工件文本，就把审查者的输出当成权威
- 循环超过 3 轮却不升级到用户
- 提示审查者"这是不是好的"而非"找问题"
- 在高压高风险决策下跳过怀疑
- 在未变更的工件上重新派生全新上下文审查者（你会得到同样的发现；这只是在拖时间）
- **怀疑作秀（可观察的信号）**：连续 2 轮以上审查者抛出实质性问题，但你归类为可行动的发现数量为零。你是在确认，不是在怀疑。停下来并升级。
- 仅在提交之后才怀疑 —— 那是 `/review`，不是怀疑驱动开发
- 硬编码外部 CLI 调用，却没有先与用户确认工具存在、已配置、并接受那条具体语法
- **在交互式怀疑周期中静默跳过跨模型。** 即便不推荐，也必须把选项摆出来。跳过本身没问题；无声地跳过才不行。
- 外部 CLI 出错或不可用时默默回退 —— 暴露失败，由用户决定如何转向
- 审查者输入中剥离了 CONTRACT
- 把 CLAIM 传给审查者（会偏向认同）

## 与其他技能的交互

- **`code-review-and-quality` / `/review`**：互补关系。`/review` 是事后对 PR 的裁决；怀疑驱动是"在飞行中"对每次决策的审视。两者并用。
- **`source-driven-development`**：SDD 针对的是**关于框架的事实**，对照官方文档核验；怀疑驱动针对的是**你关于工件的推理**。SDD 检查 API 是否存在；怀疑驱动检查你是否在该契约下用对了它。
- **`test-driven-development`**：TDD 的 RED 步骤就是把怀疑落到实处 —— 一个失败的测试就是一次反驳尝试。当 TDD 适用时，那个失败的测试*就*是关于行为断言的怀疑步骤。
- **`debugging-and-error-review`**：当审查者抛出真实失败模式时，进入调试技能定位并修复。
- **仓储编排规则**（`references/orchestration-patterns.md`）：本技能由主会话编排。persona 调用另一个 persona 是反模式 B —— 参见上文"加载约束"。

## 验证

在应用怀疑驱动开发之后：

- [ ] 每一项非平凡决策（按上文定义）都被显式命名为 CLAIM，再落地
- [ ] 每件非平凡工件至少经过一次全新上下文审查（TDD 的 RED 产生的失败测试，对行为断言满足此条；参见"与其他技能的交互"）
- [ ] 审查者收到的是 ARTIFACT + CONTRACT —— 而不是 CLAIM，也不是你的推理
- [ ] 审查者的提示语是对抗式的（"找问题"），而非确认式的（"是不是好"）
- [ ] 发现对照工件文本（而非橡皮章）逐条归类，遵循优先级：契约误读 / 可行动 / 权衡 / 噪声
- [ ] 满足了某一项停止条件（发现琐碎、3 轮循环、用户覆盖）
- [ ] 在交互式模式下，向用户**显式提供**了跨模型选项（无论工件风险高低），且回应被记录在输出中
- [ ] 在非交互式模式下，跳过了跨模型并明示跳过
- [ ] 任何外部 CLI 调用前，先做了 PATH 检查、能用的二进制测试、与用户确认语法、获得显式运行授权

## 局限

- 仅在任务与上游来源和本地项目上下文明确匹配时使用本技能。
- 应用变更前，先核验命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要把示例当作环境专属测试、安全审查或用户在破坏性、昂贵操作前的授权的替代。
