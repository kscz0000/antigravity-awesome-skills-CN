---
name: ai-md
description: "将人工编写的 CLAUDE.md 转换为 AI 原生的结构化标签格式。经 4 个模型实战验证。相同规则，更少 token，更高合规率。触发词：CLAUDE.md转换、AI原生格式、规则优化、系统提示词压缩、LLM指令优化、结构化标签、token节省、规则合规率"
risk: safe
source: community
date_added: "2026-03-11"
---

# AI.MD v4 — 完整的 AI 原生转换系统

## 何时使用此技能

- 当你的 CLAUDE.md 很长但 AI 仍然忽略你的规则时使用
- 当冗长的系统指令导致 token 使用量过高时使用
- 当你想优化任何 LLM 系统提示词以提高合规率时使用
- 当在 AI 工具之间迁移规则时使用（Claude、Codex、Gemini、Grok）

## AI.MD 是什么？

AI.MD 是一种方法论，用于将人工编写的 `CLAUDE.md`（或任何 LLM 系统指令）
转换为结构化标签格式，使 AI 模型更可靠地遵循，同时使用更少的 token。

**我们证明的悖论：** 用自然语言添加更多规则会降低合规率。
将相同的规则转换为结构化格式可以恢复甚至超越原有合规率。

```
人工散文（6条规则，1行）  → AI 遵循其中 4 条
结构化标签（6条规则，6行） → AI 遵循全部 6 条
相同内容。不同格式。不同结果。
```

---

## 为什么有效：LLM 实际如何处理指令

LLM 不会"阅读"——它们会**关注**。理解这一点会改变一切。

### 机制 1：注意力分割

当多条规则共享一行时，模型的注意力平均分配给所有 token。
每条规则只获得一部分注意力权重。有些规则会丢失。

当每条规则有自己的行时，模型将其作为独立单元处理。
每条规则获得完整的注意力权重。

```
# 一行 = 注意力分成 5 份（有些规则降至接近零权重）
EVIDENCE: no-fabricate no-guess | 禁用詞:應該是/可能是 → 先拿數據 | Read/Grep→行號 curl→數據 | "好像"/"覺得"→自己先跑test | guess=shame-wall

# 五行 = 每条规则获得完整注意力
EVIDENCE:
  core: no-fabricate | no-guess | unsure=say-so
  banned: 應該是/可能是/感覺是/推測 → 先拿數據
  proof: all-claims-need(data/line#/source) | Read/Grep→行號 | curl→數據
  hear-doubt: "好像"/"覺得" → self-test(curl/benchmark) → 禁反問user
  violation: guess → shame-wall
```

### 机制 2：零推理标签

自然语言迫使模型从上下文中**推理**含义。
标签**声明**含义明确。无需推理 = 不会误解。

```
# AI 必须推理：(防搞混) 修饰什么？例外适用于什么？
GATE-1: 收到任務→先用一句話複述(防搞混)(長對話中每個新任務都重新觸發) | 例外: signals命中「處理一下」=直接執行

# AI 直接读取标签：trigger→action→exception。零歧义。
GATE-1 複述:
  trigger: new-task
  action: first-sentence="你要我做的是___"
  persist: 長對話中每個新任務都重新觸發
  exception: signal=處理一下 → skip
  yields-to: GATE-3
```

关键洞察：像 `trigger:` `action:` `exception:` 这样的标签在所有语言中都有效。
模型不需要解析中文/日文/英文语法来理解结构。
**标签是人类与 AI 之间的通用语言。**

### 机制 3：语义锚定

带标签的子项创建**可匹配的标签**。当用户输入包含关键词时，
模型直接将其匹配到相应的标签——就像哈希表查找，
而不是全文搜索。

```
# 埋没：AI 扫描整个句子，可能错过连接
加新功能→第一句問schema | 新增API/endpoint=必確認health-check.py覆蓋

# 锚定：标签 "new-api:" 直接匹配用户说"加個 API"
MOAT:
  new-feature: 第一句問schema/契約/關聯
  new-api: 必確認health-check.py覆蓋(GATE-5)
```

**真实证明：** 这个特定技术修复了一个在所有模型上连续失败 5 次的测试用例。
标签 `new-api:` 让 Codex T5 在第一次尝试时就从 ❌→✅。

---

## 转换过程：当你给我一个 CLAUDE.md 时会发生什么

这是我将自然语言指令转换为 AI.MD 格式时使用的确切思维模型。

### 阶段 1：理解——像编译器一样阅读，而不是像人类

我阅读 CLAUDE.md **就像在构建状态机**，而不是阅读文档。

对于每个句子，我问：
1. **这是一个触发器吗？**（什么输入激活此行为？）
2. **这是一个动作吗？**（AI 应该做什么？）
3. **这是一个约束吗？**（AI 不应该做什么？）
4. **这是元数据吗？**（优先级、时机、持久性、例外？）
5. **这是人类解释吗？**（规则存在的原因——删除这个）

示例分析：

```
输入："收到任務→先用一句話複述(防搞混)(長對話中每個新任務都重新觸發) | 例外: signals命中「處理一下」=直接執行"

分解：
  ├─ TRIGGER:    "收到任務" → new-task
  ├─ ACTION:     "先用一句話複述" → first-sentence="你要我做的是___"
  ├─ DELETE:     "(防搞混)" → 人类动机，AI 不需要这个
  ├─ METADATA:   "(長對話中每個新任務都重新觸發)" → persist: every-new-task
  └─ EXCEPTION:  "例外: signals命中「處理一下」=直接執行" → exception: signal=處理一下 → skip
```

### 阶段 2：分解——将每个 `|` 和 `()` 拆分为原子规则

合规失败的头号原因是**复合规则**。
一行中有 3 条用 `|` 分隔的规则，对 AI 来说看起来像 1 条指令。
它需要是 3 条独立的指令。

**拆分器测试：** 如果你可以在句子的两部分之间放"AND"，
它们就是独立的规则，必须在不同的行上。

```
# 输入：一个隐藏了 4 条规则的句子
禁用詞:應該是/可能是→先拿數據 | "好像"/"覺得"→自己先跑test(不是問user)→有數據才能決定

# 分析：我发现 4 条隐藏规则
规则 1：某些词被禁止 → 改用数据
规则 2：听到怀疑词 → 运行自测
规则 3：不要向用户要数据 → 自己查找
规则 4：偏好声明 → 接受前需要 A/B 对比

# 输出：4 条原子规则
banned: 應該是/可能是/感覺是/推測 → 先拿數據
hear-doubt: "好像"/"覺得" → self-test(curl/benchmark)
self-serve: 禁反問user(自己查)
compare: "覺得A比B好" → A/B實測先行
```

### 阶段 3：标签——分配功能标签

每个原子规则获得一个声明其功能的标签。
我使用约 12 种标签类型的标准词汇：

| 标签 | 声明什么 | 何时使用 |
|-------|-----------------|-------------|
| `trigger:` | 什么输入激活此规则 | 每个门控/规则都需要一个 |
| `action:` | AI 必须做什么 | 核心行为 |
| `exception:` | 何时不执行 | 覆盖情况 |
| `not-triggered:` | 显式负面示例 | 防止过度触发 |
| `format:` | 输出格式约束 | 位置、结构要求 |
| `priority:` | 覆盖关系 | 规则冲突时 |
| `yields-to:` | 哪个门控优先 | 门控间优先级 |
| `persist:` | 跨轮次持久性 | 在对话流中存活的规则 |
| `timing:` | 工作流中的时机 | 之前/之后/期间约束 |
| `violation:` | 违反的后果 | 问责机制 |
| `banned:` | 禁止的词/行为 | 硬性禁止列表 |
| `policy:` | 决策启发式 | 需要判断时 |

**标签选择技术：** 我选择一个标签，如果另一个 AI 模型
（不是被指令的那个）只看到标签就能理解这个规则的功能，那就是正确的标签。
如果 `trigger:` 不需要阅读其他内容就能清楚地告诉你"这是激活规则的内容"，
它就是正确的标签。

### 阶段 4：结构——构建架构

我将规则组织成层次结构：

```
<gates>    = 硬性停止（任何动作前必须检查）
<rules>    = 行为指导（如何行动）
<rhythm>   = 工作流模式（何时做什么）
<conn>     = 连接字符串（事实——永不压缩）
<ref>      = 按需引用（需要时才加载）
<learn>    = 演化规则（系统如何改进）
```

**为什么这个顺序很重要：**
门控排在最前面，因为它们必须在其他任何东西之前被检查。
模型从上到下处理指令。优先级 = 位置。

**分组技术：** 共享一个域的规则成为一个标题下的子项。

```
# 扁平（差）：7 条不相关的规则，模型同等对待
1. no guessing
2. backup before editing
3. use tables for output
4. check health after deploy
5. don't say "應該是"
6. test before reporting
7. all claims need proof

# 分组（好）：3 个域，模型理解层次
EVIDENCE:               ← 域：真实性
  core: no-guess
  banned: 應該是
  proof: all-claims-need-data

SCOPE:                  ← 域：安全性
  pre-change: backup
  pre-run: check-health

OUTPUT:                 ← 域：格式
  format: tables+numbers
```

### 阶段 5：解决——处理冲突和边缘情况

这是最关键且最不明显的阶段。自然语言指令
经常包含**隐藏冲突**，人类用直觉解决，但 AI 无法解决。

**技术：冲突检测矩阵**

我检查每对门控/规则的冲突：

```
GATE-1 (複述: 重复任务) vs GATE-3 (保護檔: 先备份)
→ 冲突：如果用户说"edit .env"，AI 应该先重复任务，还是先备份？
→ 解决：priority: GATE-3 > GATE-1（安全先于礼貌）
             yields-to: GATE-3（在 GATE-1 中显式声明）

GATE-4 (報結論: 引用证据) vs bug-close (記錄根因: 写根因)
→ 冲突：bug-close 要求陈述根因，但 GATE-4 禁止确定性声明
→ 解决：timing: GATE-4 是结论前刹车；bug-close 是验证后记录
             GATE-4 not-triggered 当 bug 已验证时

EVIDENCE (no-guess) vs 用户说"處理一下"（直接做）
→ 冲突：AI 应该验证假设还是立即执行？
→ 解决：signal "處理一下" = 用户已决定，跳过确认
```

**技术：非触发列表**

对于任何可能过度触发的规则，我添加显式负面示例：

```
GATE-4 報結論:
  trigger: 最終歸因/根因判定/不可逆建議
  not-triggered: 中間進度數字 | 純指標查詢 | 工具原始輸出 | 已知事實 | 轉述文件
```

这是在发现 Gemini 2.5 Pro 在简单的数字查询上持续触发 GATE-4
如"成功率怎麼樣?"后添加的。添加 `not-triggered: 純指標查詢` 立即修复了它。

### 阶段 6：测试——多模型验证（不可协商）

**这不是可选的。** 每次转换必须由 2+ 个不同的 LLM 模型验证。

为什么？因为对 Claude 完美有效的格式可能会让 GPT 困惑，反之亦然。
AI.MD 的全部意义在于它跨模型有效。

**我们开发的考试协议：**

1. 编写 8 个模拟真实用户行为的测试输入（不是教科书示例）
2. 包含"陷阱"问题，其中两条规则冲突
3. 包含"负面"测试，规则不应触发
4. 不要提示正在测试哪些规则（AI 不应该知道）
5. 独立运行每个模型
6. 评分每个答案：✅ 完全合规，⚠️ 部分，❌ 错过
7. 如果任何模型的分数在转换后下降 → 恢复该特定更改

**我们使用的 8 问题模板：**

```
T1: 简单任务（GATE-1 是否触发？）
T2: 数据库写入尝试（GATE-2 是否捕获？）
T3: 受保护文件编辑（GATE-3 是否在 GATE-1 之前触发？）
T4: 根因分析（GATE-4 是否要求所有 4 个问题？）
T5: 业务 API 添加（AI 是否提到 health-check.py？）
T6: 用户说"好像X比Y好"（AI 是否运行对比还是直接接受？）
T7: 用户说"處理一下"（AI 是否跳过 GATE-1 确认？）
T8: 简单指标查询（GATE-4 是否不触发？）
```

---

## 实战测试中发现的特殊技术

### 技术 1：双语标签策略

标签用英文，输出字符串用用户语言。
英文标签更短，且被所有模型更普遍理解。
但 AI 产生的实际文本必须保持在用户语言中。

```
action: first-sentence="你要我做的是___"    ← AI 输出中文
format: must-be-line-1                      ← 结构约束用英文
banned: 應該是/可能是                        ← 禁止词保持在原始语言
```

**为什么有效：** 英文标签词汇（`trigger`、`action`、`exception`）直接映射
到每个模型训练数据中的概念。中文语法标签（觸發條件、執行動作、例外情況）
在模型间标准化程度较低。

### 技术 2：状态机门控

不要将规则视为扁平列表，而是将其建模为**状态机**：
- 每个门控有一个 `trigger`（输入状态）
- 每个门控有一个 `action`（转换）
- 门控有 `priority`（多个匹配时哪个先触发）
- 门控有 `yields-to`（显式冲突解决）

这给 AI 一个清晰的执行模型：
```
输入到达 → 先检查 GATE-3（最高优先级）→ 检查 GATE-1 → 检查 GATE-2 → ...
```

而不是：
```
输入到达 → 读取所有规则 → 尝试找出哪个适用 → 可能错过一个
```

### 技术 3：XML 章节标签用于语义边界

使用 `<gates>`、`<rules>`、`<rhythm>`、`<conn>` 作为章节分隔符
创建硬边界，防止规则渗透（模型混淆规则属于哪个章节）。

```xml
<gates label="硬性閘門 | 優先序: gates>rules>rhythm | 缺一項=STOP">
...gates here...
</gates>

<rules>
...rules here...
</rules>
```

开始标签上的 `label` 属性作为章节级指令：
"这些是硬性门控，这是它们的优先级，缺少 = 停止"

### 技术 4：交叉引用而非重复

当相同概念出现在多条规则中时，不要重复它。
使用交叉引用标签。

```
# 差：health-check 在 3 个地方提到
GATE-5: ...check health-check.py...
MOAT: ...must check health-check.py...
SCOPE: ...verify health-check.py exists...

# 好：单一真相来源 + 交叉引用
GATE-5 驗收:
  checks:
    新增API → 確認health-check.py覆蓋

MOAT:
  new-api: 必確認health-check.py覆蓋(GATE-5)    ← 交叉引用，非重复
```

### 技术 5："做什么而非为什么"原则

删除所有解释规则为什么存在的文本。
AI 需要知道做什么，而不是为什么。

```
# 删除这些人类解释：
(防搞混)                     → 动机
(不是大爆破,是每次順手一點)    → 隐喻
(想清楚100倍後才做現在的)     → 背景故事
(因為用戶是非工程師)          → 理由

# 只保留可执行的指令：
action: first-sentence="你要我做的是___"
refactor: 同區塊連續第3次修改 → extract
```

每个删除的解释都节省 token，并消除可能让模型困惑的噪音
关于它实际应该做什么。

---

## 两阶段工作流

### 阶段 1：预览——测量，不要触碰

```bash
echo "=== 当前 Token 消耗 ==="
claude_md=$(wc -c < ~/.claude/CLAUDE.md 2>/dev/null || echo 0)
rules=$(cat ~/.claude/rules/*.md 2>/dev/null | wc -c || echo 0)
total=$((claude_md + rules))
tokens=$((total / 4))
echo "CLAUDE.md:     $claude_md bytes"
echo "rules/*.md:    $rules bytes"
echo "Total:         $total bytes ≈ $tokens tokens/turn"
echo "50-turn session: ≈ $((tokens * 50)) tokens on instructions alone"
```

然后：读取所有自动加载的文件。识别冗余、散文开销和重复规则。

**继续前询问用户："要精简吗？"**

### 阶段 2：精简——带安全网转换

1. **备份**：`cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak-pre-distill`
2. **阶段 1-5**：运行上述完整转换过程
3. **阶段 6**：运行多模型测试（最少 2 个模型，8 个问题）
4. **报告**：显示前后分数

```
=== AI.MD 转换完成 ===

Before: {old} bytes ({old_score} compliance)
After:  {new} bytes ({new_score} compliance)
Saved:  {percent}% bytes, +{delta} compliance points

Backup: ~/.claude/CLAUDE.md.bak-pre-distill
Restore: cp ~/.claude/CLAUDE.md.bak-pre-distill ~/.claude/CLAUDE.md
```

---

## AI 原生模板

```xml
# PROJECT-NAME | lang:xx | for-AI-parsing | optimize=results-over-format

<user>
identity, tone, signals, decision-style (key: value pairs)
</user>

<gates label="硬性閘門 | 優先序: gates>rules>rhythm | 缺一項=STOP">

GATE-1 name:
  trigger: ...
  action: ...
  exception: ...
  yields-to: ...

GATE-2 name:
  trigger: ...
  action: ...
  policy: ...

</gates>

<rules>

RULE-NAME:
  core: ...
  banned: ...
  hear-X: ... → action
  violation: ...

</rules>

<rhythm>
workflow patterns as key: value pairs
</rhythm>

<conn>
connection strings (keep exact — NEVER compress facts/credentials/URLs)
</conn>

<ref label="on-demand Read only">
file-path → purpose
</ref>

<learn>
how system evolves over time
</learn>
```

---

## 反模式

| 不要 | 改为 | 原因 |
|-------|------------|-----|
| CLAUDE.md 中的人类散文 | 结构化标签 | 散文需要推理；标签是直接的 |
| 一行多条规则 | 每行一个概念 | 注意力在密集行上分割 |
| 括号解释 | 删除它们 | AI 需要"做什么"而非"为什么" |
| 同一规则在 3 个地方 | 单一来源 + 交叉引用 | 重复可能分化并造成困惑 |
| 20+ 条扁平规则 | 5-7 个带子项的域 | 层次结构帮助模型组织行为 |
| 不测试就压缩 | 用 2+ 模型验证 | 对 Claude 有效的可能对 GPT 失败 |
| 假设格式不重要 | 测试它——确实重要 | 相同内容，不同格式 = 不同合规率 |
| 仅中文标签 | 英文标签 + 原生输出 | 英文标签在模型间更通用 |
| 扁平规则列表 | 带优先级的状态机 | 清晰的执行顺序防止遗漏规则 |

---

## 真实世界结果

2026-03 测试，washinmura.jp CLAUDE.md，5 轮，4 个模型：

| 轮次 | 变更 | Codex (GPT-5.3) | Gemini 2.5 Pro | Claude Opus 4.6 |
|-------|--------|-----------------|----------------|-----------------|
| R1（基准散文） | — | 8/8 | 7/8 | 8/8 |
| R2（添加规则） | +gates +examples | 7/8 | 6/8 | — |
| R3（优化散文） | +exceptions +non-triggers | 6/8 | 6.5/8 | — |
| R4（AI 原生转换） | 结构化标签 | **8/8** | **7/8** | **8/8** |

关键发现：
1. **更多散文规则 = 更差合规率**（R1→R3：随着规则增长分数下降）
2. **结构化格式 = 恢复并超越**（R4：尽管规则更多，回到最高分）
3. **跨模型一致性**：对一个模型有效的格式对所有模型都有效（Grok 除外）
4. **语义锚定**：`new-api:` 标签修复是影响最大的单一变更

**令人不安的真相：你精心编写的漂亮 CLAUDE.md
可能正在损害你的 AI 性能。结构 > 散文。永远如此。**

## 局限性
- 仅当任务明确匹配上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并请求澄清。
