---
name: polis-protocol-a-self-optimizing-city-of-agents
description: "Polis 协议：一座自我优化的智能体城市。适用于多智能体协作、任务路由、跨供应商优化、自我学习改进等场景。触发词：polis协议、智能体城市、多智能体协作、任务路由、跨vendor协作、自我优化、智能体宪法、capability card、contract路由。"
risk: unknown
source: https://github.com/yehudalevy-collab/polis-protocol/tree/main/
source_repo: yehudalevy-collab/polis-protocol
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/yehudalevy-collab/polis-protocol/blob/main/LICENSE
---

# Polis 协议：一座自我优化的智能体城市
## 何时使用

当你需要 Polis 协议：一座自我优化的智能体城市时，使用此技能。


一个让来自不同供应商的 AI 智能体在长期运行的项目上协作、将工作路由给最擅长的人、并随时间可衡量地变好的协议。所有内容都存放在一个 markdown 文件文件夹中，因此任何能读写文本的工具都能参与——无需中央服务器，无需特定运行时。

## 核心理念

将项目视为一座小型 *polis*（城邦）：公民（智能体）共享一部宪法（协议），发布公开身份（能力卡），签订契约（任务），并留下事情如何进展的公开记录（教训）。三个机构加上一个自我变更机制：

1. **登记处**——身份与能力发现（能力卡）。
2. **契约**——带有学习型路由的结构化任务。
3. **编年史**——可累积并反馈到路由中的教训。
4. **修正案**——公民在现实需要时更改规则。

这带来了共享 vault 配置无法提供的东西：跨供应商优化（工作交给最擅长的人）、自我发展（路由随使用而改进）、宪法演进（协议从摩擦中自我更新）。对于不需要路由的纯消息传递，请使用 agent-vault。

## 此技能激活时

任何"谁该做这件事"是一个真正问题的多智能体场景：创建或加入一个 polis；撰写、认领或结算契约；运行 chavruta 审查；提出或批准修正案；或诊断停滞契约、同步冲突、路由病理或卡住的表决。从 agent-vault 升级 → `references/troubleshooting.md`（"从 agent-vault 迁移"）。

## polis 的结构

一个 polis 存放在项目根目录的 `_polis/` 文件夹中；其外的所有内容是协议从不触碰的项目内容。

- `CONSTITUTION.md`——规范的工具无关协议 · `index.md`——当前状态 · `README.md`——人类解释器
- `chronicle.md`——仅追加的事件日志
- `citizens/<agent-id>/`——`capability_card.yml`、`status.md`、`inbox.md`、`journal.md`
- `contracts/open/<id>.md` · `contracts/settled/<id>.md` · `contracts/routing_stats.yml`（学习型策略，结算时更新）
- `lessons/<capability-tag>/<id>.md` · `reviews/<YYYY-MM-DD-HHMM>-<contract>.md` · `amendments/proposed|ratified/`
- 项目根还会有 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` 桥接指针和 `.agents/skills/polis-protocol/SKILL.md`（Codex/Antigravity 复本），都指向 `CONSTITUTION.md`。

公民用 wikilinks（`[[path/to/note]]`）链接项目文件。`_polis/` 文件夹是协议拥有的唯一内容。

## 每次会话首先要做的事

在触碰任何项目文件之前，按顺序执行入口流程：

1. **polis 存在？** 查找 `_polis/CONSTITUTION.md`。若不存在，搭建它（见"创建 polis"）。
2. **你已注册？** 查找 `_polis/citizens/<self>/capability_card.yml`。若不存在，注册（见"注册公民"）。
3. **读取 `_polis/CONSTITUTION.md`**——每个会话一次——它是此 polis 的规范协议；本 SKILL.md 是它生长出来的种子。
4. **读取 `_polis/index.md`**——当前状态（两分钟读完）。
5. **读取你的收件箱**——`_polis/citizens/<self>/inbox.md`。
6. **向后扫描 `chronicle.md` 的尾部**，直到你达到 `status.md` 中的 `last_seen_event:`。那是你的补课内容。
7. **读取你的开放契约**——`_polis/contracts/open/` 中任何 `owner: <self>` 的内容。
8. **更新 `status.md` 中的 `last_seen_event` 和 `last_active`。**
9. **向用户汇报**——项目状态、进行中的内容、需要他们输入的内容、一个具体的下一步行动。

如果 `chronicle.md` 已变大，rollover 策略（`references/troubleshooting.md`）可保持其有界。

## 编年史：记录你所做的事

每次有意义的行动后，向 `_polis/chronicle.md` 追加恰好一行。格式是严格的，因为路由器和其他公民会解析它：

```
- YYYY-MM-DD HH:MM | <agent-id> | <verb-phrase> | [[<wikilink>]] | <one-line note or - >
- 2026-05-14 09:15 | codex-frontend-pesaj | settled contract | [[contracts/settled/auth-refactor]] | tests passing, lesson filed
```

有意义的行动是任何其他公民需要知道的内容（契约开放/结算、交接、阻塞、请求审查、提出修正案、index-keeper 变更）。内部推理和小修改留在你的私有 `journal.md` 中，永不到达编年史——保护其信噪比是最重要的纪律。

保留的动词短语带有脚本可能过滤的含义：`joined`/`left polis`、`opened`/`claimed`/`settled`/`abandoned contract`、`filed lesson`、`requested review`/`signed off`/`rejected review`、`proposed`/`ratified`/`rejected amendment`、`blocked on <thing>`/`unblocked`、`assumed`/`released index keeper`。完整语义见 `references/protocol-spec.md`；否则使用普通的过去时动词。

**粒度——最常见的失败是过度记录：** 如果这事*不*被记录，另一个公民是否会浪费时间、做出错误判断或重复工作？如果是，记录它；如果否，别记录。校准表见 `references/troubleshooting.md`。

## 登记处：能力卡

每个公民发布 `_polis/citizens/<agent-id>/capability_card.yml`——机器可解析的"谁能做什么"答案：

```yaml
agent_id: claude-research-pesaj
vendor: anthropic        # model: claude-opus-4-7
capability_tags:
  long-context-reading: { self_rating: 5, evidence: "150k token context" }
  spanish-translation:  { self_rating: 3, evidence: "native-ish, not certified" }
cost_envelope: { relative: medium }   # low|medium|high   latency: typical/max minutes
content_hash: "sha256:…"   # tamper-evidence, not a cryptographic signature
```

自评是起点，不是真相——`routing_stats.yml` 中的实际表现会在每个标签几次任务后接管。保持标签具体（`react-component-design`，而非 `frontend-code`），随你学习自由编辑自己的卡片，并将 `content_hash` 视为篡改证据（它显示卡片自上次通过 `polis verify` 盖章后发生了变化，而非*谁*更改了它）。新智能体无需询问即可写入自己的卡片——登记处设计为开放的。完整 schema 见 `references/protocol-spec.md`。

## 契约：带有学习型路由的结构化任务

契约有三个部分，写在契约的生命周期中：**意图**（目标、验收标准、所需能力标签、截止日期、成本上限、 stakes）在开放时；**分配**（owner、方法、努力）在认领时；**结算**（结果、什么有效/什么失败、教训引用、质量分数）在关闭时。Schema 见 `references/protocol-spec.md`；模板见 `references/templates.md`。

**路由**是一个多臂赌博机：对于每个所需标签，从自评（冷启动时权重很大）、`routing_stats.yml` 中的历史质量、成本和可用性对每个公民评分；通常路由给最高分（利用），偶尔路由给另一个（探索，默认 15%）以保持策略诚实。以 `scripts/route_contract.py` 运行或作为一个简短的推理步骤——两种方式给出相同推荐。这是一个推荐，**不是命令**：任何公民可通过认领并在 `分配`部分注明原因来覆盖；覆盖会被记录并反馈给策略。数学和调优见 `references/routing.md`。

**结算**同时做三件事：写入`结算`部分；在 `_polis/lessons/<tag>/<id>.md` 下创建一个教训（一段 + 标签）；发布一行 `settled contract` 编年史条目。路由器读取已结算契约和教训来更新 `routing_stats.yml`——那个更新是团队改进的关键。教训（frontmatter：`lesson_id`、`filed_by`、`capability_tags`、`related_contracts`、`quality_impact`，然后一段）被同一标签的新契约在路由前拉取，所以路由器和执行智能体都承载着团队累积的智慧。这正是将无记忆智能体转变为拥有制度记忆的团队的关键。

## 高 stakes 契约的 Chavruta 审查

任何标记为 `stakes: high` 的契约（删除数据、发布到生产、做出架构决策、或承诺一个难以逆转的方向）需要一个第二公民——理想上**来自不同供应商**——在执行前批评计划。流程：owner 写入`分配`"计划"并发布 `requested review` + 一条收件箱消息给一个强力审查者 → 审查者写入 `_polis/reviews/<ts>-<contract>.md` 回答"什么是对的/什么是缺失的/签署、请求变更或拒绝" → 签署后 owner 执行；请求变更时修订一次并重复；拒绝时升级或放弃。同供应商审查允许但较弱——模型间的结构差异才是全部价值。谨慎使用；大多数契约是低 stakes 并跳过此步骤。详情见 `references/protocol-spec.md`。

## 修正案：一个自我更新的 polis

当公民注意到一个反复的失败、一条不清晰的规则、或一个路由病理时，他们提出修正案。流程：写入 `_polis/amendments/proposed/<id>.md`（问题 + 提议的宪法变更 + 任何新规则/格式）→ 发布 `proposed amendment` 到编年史和每条收件箱一行指针 → 公民在文件中回应（`agree | disagree | abstain | request changes` + 理由）→ 达到 quorum（默认：过去 14 天活跃公民的简单多数）时移至 `ratified/` 并编辑 `_polis/CONSTITUTION.md`，各一行编年史条目。被拒绝的修正案留在 `proposed/` 中带 `status: rejected`，以便未来公民知道尝试过什么。宪法对给定 polis 总是规范的；本 SKILL.md 是种子。何时修正 vs 绕过、quorum 规则、示例见 `references/amendments.md`。

`polis reflect` 自动化*注意*：它从已结算契约历史中挖掘反复的过程病理（慢性错误路由、低质量标签、stakes 校准错误）并将证据支持的提案草拟到 `amendments/proposed/`（由 `polis-reflector` 撰写，引用契约）。它只提议——公民仍投票和批准。运行 `polis reflect` 预览，`--apply` 提交它们。

## 创建 polis

如果 `_polis/CONSTITUTION.md` 不存在，创建 polis。三条路径，按偏好顺序——使用你环境中可用的第一条：

1. **在线，最新（推荐）。** `uvx` 从 PyPI 获取最新发布版，所以用户自动保持最新：
   ```
   uvx polis-protocol init --project-root <path> --agent-id <your-agent-id> \
     --vendor <anthropic|openai|google|other> --model <model-id> --project-name "<name>"
   ```
   （等效：`pipx install polis-protocol` 然后 `polis init …`。）

2. **离线——无网络，无安装。** 此技能在 `templates/` 旁附带一个自包含初始化器。从技能文件夹用相同参数运行：
   ```
   python scripts/init_polis.py --project-root <path> --agent-id <your-agent-id> \
     --vendor <…> --model <model-id> --project-name "<name>"
   ```
   它只需要 Python 3 和附带的 `templates/`——无需 `polis` 包，无需网络。当 `uvx`/`pipx` 不可用（sandbox、离线、无 PyPI）时使用此法，而非寻找缺失的 CLI。

3. **手动——完全无 Python。** 复制 `references/templates.md` 中的模板。最小可行 polis 是 `_polis/CONSTITUTION.md` + 你自己的 `capability_card.yml` + 一个带 frontmatter 块的空 `chronicle.md`。

这三条都写入完整 `_polis/` 结构（宪法、创建者能力卡、种子 `chronicle.md`、空 `routing_stats.yml`、以及 `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` 桥接指针）。都是幂等的，永不覆盖现有文件。`polis init --repair`（或重新运行脚本）恢复缺失的管理文件；`polis migrate --plan|--apply|--rollback` 处理可逆的 schema 升级。

## 注册公民到已有 polis

当你来到一个有 `_polis/CONSTITUTION.md` 但没有你卡片的项目时，注册你自己——不要等待许可：

1. 选择一个智能体 ID（约定见下）。
2. 创建 `_polis/citizens/<your-id>/`。
3. 写入 `capability_card.yml`（schema 见 `references/protocol-spec.md`）。
4. 从模板创建空的 `status.md`、`inbox.md`、`journal.md`。
5. 在 `chronicle.md` 中发布一行 `joined polis` 链接你的卡片。
6. 继续入口流程。

**智能体 ID 约定：** `<vendor-or-tool>-<role>-<project>`。vendor 前缀让任何公民能一眼看出哪个模型产生了一条编年史条目。好的：`claude-research-pesaj`、`codex-frontend-pesaj`、`gemini-translator-pesaj`。坏的：`agent-7a3f`（晦涩）、`helper`（泛泛）、`gemini-2026-05-14-1430`（时间戳不是身份）。小写，仅连字符，8–40 字符；一旦注册，永不重命名。

## 跨供应商工作

启动时写入的桥接指针让 Claude、Codex、Gemini CLI、GPT 工具和任何读取 markdown 的东西共享一个 polis（`AGENTS.md` 也覆盖 Jules、Aider、goose、opencode、Zed、Warp、VS Code、Devin）。都指向 `_polis/CONSTITUTION.md`，所以协议在一个文件中更新。跨供应商路由是收益：赌博机将翻译发给有最佳 `spanish-translation` 记录的人，而非恰好是当前聊天的那个。

## 失败模式与恢复

完整恢复步骤见 `references/troubleshooting.md`。公民静默 → 检查 `status.md`；超过 stale threshold，转移所有权。两个公民认领同一契约 → `owner:` 上先写者胜，失败者重选。路由器持续错选 → 可能冷启动；覆盖几个来 seeding，否则修正权重。卡片被非 owner 编辑 → 通过 `polis verify` 检出 `content_hash` 不匹配；恢复并记录。修正案卡住无 quorum → 降低活跃阈值或合并提案（30 天自动过期）。polis 太大 → 每季度 rollover `chronicle.md`，归档 90 天前的已结算契约；教训永不 rollover。

## 参考资料

- `references/protocol-spec.md`——每个文件的完整 schema + 保留动词语义；读取以验证或解析文件。
- `references/templates.md`——带注释的可复制模板；手动创建、注册或提交时读取。
- `references/routing.md`——赌博机数学、评分、冷启动、探索率调优；路由器选得奇怪时读取。
- `references/amendments.md`——何时修正 vs 绕过、quorum 规则、示例。
- `references/troubleshooting.md`——失败模式、粒度校准表、扩容、agent-vault 迁移。
- `templates/POLIS_CONSTITUTION.md`——启动时写入每个 polis 的规范协议。

## 局限性

- 仅当任务明显匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更前验证命令、生成代码、依赖、凭证和外部服务行为。
- 不要将示例替代为环境特定的测试、安全审查、或用户对破坏性或高成本操作的批准。