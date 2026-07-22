# 方法论 — 营销计划如何制定

三阶段工作流，用于产出一份全面的营销计划。SKILL.md 是编排层；本文档是操作细节。

## 阶段 1 — INIT（研究 + 信息采集）

**目标：** 带着足够的上下文进入阶段 2，可以在不猜测的情况下起草每一节。

### 步骤 1.1 — 建立计划文件夹

每个计划的标准文件布局：

```
~/marketing-plans/{client-slug}/
├── materials/         # 客户提供的文件（演示文稿、审计输出、品牌语调文档等）
├── research.md        # 在阶段 1（INIT）中编写
├── progress.md        # 状态机 — 参见步骤 1.1.1 的 schema
├── sections/
│   ├── 01.md          # 执行摘要（最后编写，排序第一）
│   ├── 02.md          # 战略框架
│   ├── ...
│   └── 13.md          # 度量、RACI、待定决策、附录
└── final_plan.md      # 编译交付物（阶段 3 输出）
```

### 步骤 1.1.1 — `progress.md` 状态 schema

每个计划在计划根目录跟踪一个 `progress.md` 文件。它是恢复的真相来源。Schema：

```markdown
# {Client} — Marketing Plan Progress

phase: init | review | finalize | finalized
current_section: <number, only meaningful during review phase>
plan_version: v1
last_updated: YYYY-MM-DD HH:MM

## Sections completed
- [ ] 2. Strategic frame
- [ ] 3. Current state
- [ ] 4. Acquisition
- [ ] 5. Activation
- [ ] 6. Retention
- [ ] 7. Referral
- [ ] 8. Revenue
- [ ] 9. 90-day roadmap
- [ ] 10. 12-month outlook
- [ ] 11. Marketing operations stack
- [ ] 12. Tactical idea bank
- [ ] 13. Measurement, RACI, open decisions, appendix
- [ ] 1. Executive summary (synthesized last)

## Approved artifacts
sections/02.md, sections/03.md, ... (list as they're written)

## Notes
<any open decisions, blockers, or out-of-band context that aren't in research.md>
```

### 步骤 1.1.2 — 恢复决策树

每次调用时，按以下顺序检查状态：

1. **无 `{client-slug}/` 文件夹** → 新计划。创建文件夹 + `materials/` + 空 `sections/`。开始 INIT（步骤 1.2）。
2. **文件夹存在，无 `research.md`** → INIT 被中断。从步骤 1.2 恢复。
3. **`research.md` 存在，无 `progress.md`** → INIT 完成，REVIEW 未开始。创建 `progress.md`，从第 2 节开始 REVIEW。
4. **`progress.md` 存在，`phase: review`** → REVIEW 进行中。从 `current_section` 恢复（或第一个未勾选的复选框）。
5. **`progress.md` 存在，`phase: finalize`** → FINALIZE 被中断。重新运行阶段 3。
6. **`progress.md` 存在，`phase: finalized`** → 计划已完成。**不要静默覆盖。** 询问用户：*"此计划已定稿（v{N}）。要 (a) 作为 v{N+1} 修订，(b) 在新文件夹中开始新计划，还是 (c) 重新打开某个特定节？"*

每当状态变化时更新 `phase` 和 `last_updated`。

### 步骤 1.2 — 读取现有材料

如果 `materials/` 有文件，读取所有文件。常见的材料包括：
- 融资演示文稿 / 投资人演示文稿
- 定位文档 / 品牌语调文档
- 客户研究 / ICP 文档
- App Store 指标 / 分析快照
- 生命周期邮件清单
- 之前的审计输出（团队运行过的任何评分当前状态评估）
- SEO 研究（`seo/plan.md`、`seo/keyword-shortlist.md`）
- 启动会通话记录
- 创始人 Slack / 异步笔记

读取所有内容。边读边将关键事实记录到 `research.md`。

### 步骤 1.3 — 拉取已对接的实时数据

如果此客户已对接 MCP/API，拉取：

- **Ahrefs** → 域名评分、有机关键词、反向链接、热门页面、引用域名（按 `/seo-audit` 技能）
- **GA4 MCP** → 按渠道的流量、转化事件、留存曲线
- **Stripe MCP** → MRR、ARR、流失、计划分布、按群组的综合 LTV
- **App Store Connect**（手动或 `dev-browser`）→ 安装 → 试用 → 付费漏斗；群组留存
- **Customer.io MCP** → 流程清单、发送 / 打开 / 点击 / 退订率
- **Shopify** → 产品页转化率、AOV、复购率
- **GitHub MCP** → 仓库清单、最后提交日期、哪些已过时
- **Notion** → 内部知识目录（如已暴露）

不要让用户复制/粘贴可以直接拉取的数据。

### 步骤 1.4 — 进行结构化信息采集

对于材料中的每个缺口，询问用户。最小信息采集覆盖十个主题：

#### 采集 1 — 客户概览
- 公司做什么，一句话（创始人的话）？
- 主要产品是什么？
- 还有哪些其他产品 / SKU / 层级？
- 产品处于上线、测试还是预发布阶段？
- 如果测试中：是否限流？GA 时间线？

#### 采集 2 — ICP
- 你们面向谁，一句话？
- 他们说他们想要什么？
- 他们实际想要什么？
- 他们表述的问题是什么？真正的问题是什么？
- 人口统计 / 企业画像：谁完全符合 ICP？

#### 采集 3 — 当前漏斗状态
- 当前漏斗数据是什么？（注册、激活、付费、留存）
- 漏斗*形状*是什么 — 在顶部、中部还是底部是瓶颈？
- 最大的流失点在哪里？

#### 采集 4 — 融资状态
- 当前轮次（pre-seed / seed / Series A / 等）？
- 迄今总融资额？
- 当前烧钱率 / 现金跑道？
- 正在融资？预计何时关账？
- 重要投资人？
- 是否允许在融资路演中提及 fCMO 合作？

#### 采集 5 — 团队
- 创始人及各自负责领域（产品、营销、销售等）？
- 团队中其他角色及其营销接触面？
- 参与营销的顾问？
- 机构 / 承包商 / 兼职人员？
- 明显的缺口在哪里？
- 对于团队当前的营销负责人（如果有）：是 π 型（两个深度技能）、T 型（一个深度加广度），还是仅战术型？参见 `team-and-agency-model.md` 中影响第 11 节 RACI 和第 9 节首批招聘建议的框架。

#### 采集 6 — 预算
- 当前月度营销支出，按付费获客、工具、外包、人力拆分？
- 对应的预算层级（参见 `funding-stage-unlocks.md`）？
- 下一轮关账后预算解锁什么？
- 综合加本 CAC（如已知，包括工资、内容成本、工具、外包 — 不只是付费广告支出）。如未知，标记为第 13 节最高优先待定决策 — 每个收入预测都依赖它。
- ARPC、年留存率（或流失率），以便 `budget-planning.md` 中的预算数学可以应用于第 8 节（Revenue）和第 10 节（12 个月展望）。

#### 采集 7 — 当前活跃渠道
- 获客：有机 SEO、付费搜索、付费社交、内容、社交、合作伙伴、活动、PR、大使等 — 各渠道状态（活跃 / 暂停 / 未尝试）
- 激活：引导状态、注册流程、付费墙、首次体验、App Store 列表
- 留存：生命周期邮件状态、应用内追加销售、流失群组
- 推荐：项目是否存在、归因、入站兴趣
- 变现：定价结构、计划分布、近期实验

#### 采集 8 — 已完成的工作
本计划应承认哪些过往工作？
- 重大发布及日期
- PR 时刻及报道媒体
- 内容支柱 / 中心 / 基石内容
- 合作伙伴关系
- 奖项 / 认证
- 重要客户 / 用户（如为消费者命名用户）
- 过往顾问 / 兼职人员

#### 采集 9 — 进行中且卡住的工作
- 什么已起草但未发布？为什么？
- 什么已经"快好了"好几个月了？
- 各自的阻碍是什么？
- 什么已损坏或有负面影响？

#### 采集 10 — 战略姿态
- 本季度最需要修复的事（创始人的判断）
- 本季度最需要忽略的事（创始人的判断）
- 投资人 / 董事会最关心什么
- 任何其他地方看不到的约束（法律、合作伙伴相关、品牌相关）

### 步骤 1.5 — 按评分标准对当前状态打分

使用 `references/current-state-rubric.md` 中的 17 节评分标准作为评分透镜。两种模式：

- **从丰富材料打分。** 当团队分享了演示文稿、之前的内容审计、已有品牌语调文档、近期的定位工作、或启动会通话记录 — 从这些材料打分。在节标题中标记"基于材料打分"。
- **从独立评分的审计打分。** 如果团队已有评分的当前状态评估（任何格式），直接导入那些数字。不要重做工作。

无论哪种方式，输出是评分后的 17 行表格，成为计划的第 3 节，后跟 2–4 句"形状解读"，指出优势和缺口的聚集区域。

### 步骤 1.6 — 编写 research.md

将所有内容编译到 `research.md`，使用以下结构：

```markdown
# {Client} — Marketing Plan Research Record

**Date:** YYYY-MM-DD
**Author:** (fCMO / planner name)

## Company snapshot
- One-sentence description
- Stage (pre-seed / seed / Series A / etc.)
- Product status (beta / GA)

## ICP
- Primary ICP
- Stated vs. actual problem
- Demographics / firmographics

## Funnel state today
- Current numbers
- Funnel shape
- Biggest leak

## Funding
- Total raised
- Current round status
- Runway

## Team
- Founders and ownership
- Marketing surface area by person
- Gaps

## Current marketing budget
- $/mo total
- Breakdown
- Tier mapping

## Channels currently active
[By AARRR stage]

## Already done (acknowledge in plan)
[List]

## In-flight and stuck
[List with blockers]

## Strategic posture
- Founder's top priority
- Founder's top de-prioritization
- Investor pressure points
- Constraints

## Current-state rubric scores
[17 section scores using `references/current-state-rubric.md`. If a prior scored audit exists, paste those scores. Otherwise mark "scored from materials."]

## Materials read
[List of files in materials/ + when read]
```

保存。进入阶段 2。

---

## 阶段 2 — REVIEW（逐节起草）

**目标：** 逐一审阅计划模板（`references/plan-template.md`）的全部 13 节，起草每一节，获得用户确认，逐节保存。

### 步骤 2.1 — 初始化 progress.md

使用上方步骤 1.1.1 中定义的 schema。设置 `phase: review`、`current_section: 2`、`plan_version: v1`，并标记 `last_updated`。

### 步骤 2.2 — 按此顺序审阅每一节：2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13，然后 1

第 1 节（执行摘要）**最后**起草，因为它依赖于其他每节的结论。按数字顺序审阅第 2 → 13 节，然后从其他节综合第 1 节。最终编译的 `final_plan.md` 始终按标准顺序 1 → 13 呈现。

对于每一节，使用 `references/plan-template.md` 的模板起草。然后在对话中：

1. 呈现草稿（或关键要点 — 短节内联展示，长节先展示要点大纲）
2. 询问：*"批准、调整还是展开？"*
3. 迭代直到用户确认
4. 将确认文本保存到 `sections/01.md` ... `sections/13.md`（每节一个文件，零填充以便排序）。这是标准的持久化产物 — 恢复依赖于它。
5. 在 `progress.md` 中勾选对应复选框
6. 进入下一节

### 步骤 2.3 — 各节特定指导

**第 1 节（执行摘要）** 在第 2–13 节全部批准后综合。最后起草；在输出文档中最先呈现。

**第 3 节（当前状态）** 使用 `references/current-state-rubric.md` 中嵌入的 17 节评分标准。如已有评分审计，直接粘贴那些分数。如无，从可用材料打分。

**第 4–8 节（AARRR）** 各自遵循相同的内部结构：当前状态、计划（编号行动项）、90 天行动、12 个月展望、技能 + 工具。不要跳过技能 + 工具子节 — 它使计划在操作上诚实。

**第 11 节（营销运营栈）** 可从 `references/ops-stack-mapping.md` 加第 4–8 节中指定的具体行动自动生成。

**第 12 节（想法库）** 可从 `references/idea-cross-reference.md` 加客户端特定过滤自动生成（跳过与品牌语调冲突的想法；根据融资阶段时间调整行动状态）。

**第 13 节** 位于末尾。待定决策应按影响排序。附录应仅引用团队可访问的文件（对机器本地路径发出警告）。

### 步骤 2.4 — 品牌语调一致性

如果客户有记录的品牌语调规则（在 research.md / 第 2 节中捕获），每一节必须遵守。常见的语调约束：
- 词汇规则（YES / NO 列表）
- CTA 规则（例如"绝不施压"）
- 启动性 vs 解释性框架
- 语调（例如权威且平易近人、亲切且专业）

如果某一节的草稿违反了品牌语调，在展示给用户之前重做。

---

## 阶段 3 — FINALIZE（编译 + 验证 + 发布）

**目标：** 产出 `final_plan.md` 并可选发布到共享仓库。

### 步骤 3.1 — 编译

开始前在 `progress.md` 中设置 `phase: finalize`。将 `sections/01.md` 到 `sections/13.md` 拼接为 `final_plan.md`（标准顺序 1 → 13，无论起草顺序）。添加：
- 带有日期和 "v1" 版本标记的标题头
- "编制人 / 为 / 日期 / 状态" 前置信息
- 在 Notion 粘贴时可用的节锚点

### 步骤 3.2 — 验证检查

在输出前：

- **交叉引用检查** — 每个营销想法编号（例如"idea #17"）与 `references/idea-cross-reference.md` 中的实际想法匹配。每个相关技能提及要么存在于 `marketingskills` 仓库中，要么作为外部依赖被记录（参见 ops-stack-mapping 中关于跨市场技能的说明）。
- **MCP/API 检查** — 第 11 节中提到的每个工具确实存在于用户的技术栈中（根据 research.md 采集）或被标记为"未来 / 尚未对接"。
- **路径检查** — 输出中没有机器特定路径（`/Users/...`、`/home/...`）。替换为描述性引用。
- **语调检查** — 对照品牌语调规则最终审阅。标记并修复违规。
- **待定决策检查** — 采集中的每个 "TBD" 或未回答问题都列在第 13 节的待定决策中，而不是隐藏在正文中。
- **确认检查** — research.md 中"已完成的工作"的每一项都在计划中的某处被确认。

### 步骤 3.3 — 输出

将 `final_plan.md` 输出到计划文件夹。在对话中打印摘要：

> *"Marketing Plan v1 已保存至 `~/marketing-plans/{client-slug}/final_plan.md`。约 X,XXX 字，13 节。可粘贴到 Notion 或与团队分享。"*

### 步骤 3.4 — 发布（可选）

询问用户：
> *"要我发布到共享 GitHub 仓库以便团队访问吗？如果是，目标仓库和路径是什么（例如 `{client-org}/{client-context}/marketing/plan.md`）？"*

如果是：
- 克隆（或假定已克隆）目标仓库
- 根据用户偏好检出功能分支或直接推送到 main
- 将 `final_plan.md` 复制到目标路径
- 调整附录使用仓库相对路径（而非机器路径）
- 提交 + 推送
- 用提交 URL 确认

如果否：保留在本地。完成。

### 步骤 3.5 — 标记为已定稿

在 `progress.md` 中设置 `phase: finalized` 并标记 `last_updated`。这是终态，防止未来的 `/marketing-plan` 调用静默覆盖计划（参见步骤 1.1.2 情况 6）。

---

## 恢复计划

恢复完全由上方步骤 1.1.2 中的决策树管理 — 每次调用时始终按该顺序检查状态。

如果用户说 *"重新开始"* → 询问他们是要删除现有文件夹还是先移到 `archive/`；不要静默覆盖。
如果用户说 *"重做第 X 节"* → 在 `progress.md` 中取消勾选该复选框，删除 `sections/0X.md`，重新起草。

## 需要注意的失败模式

- **跳过信息采集。** 没有适当采集信息写出的计划是泛泛的，经不起创始人的审视。始终完成完整的十个主题采集，除非用户明确放弃。
- **假装数据存在。** 如果你无法确认某个数字（当前 MRR、留存率等），不要猜测。在计划中标记为 `[TBD — 需与团队确认]` 并添加到待定决策。
- **忽视品牌语调。** 如果客户有强烈的语调（大多数都有），每一节都必须遵守。在起草任何文案相关文本之前阅读语调规则。
- **填充想法库。** 第 12 节只有在包含跳过列表及原因时才是全面的。不要为了凑 139 个而塞入明显不适用的想法。
- **回避不舒服的指标。** 如果流失率高或激活率低，在当前状态中指出。创始人会看穿粉饰。
- **遗忘融资阶段逻辑。** 如果客户正在融资中，计划必须解释轮次关账后会发生什么变化。跳过这一点会让计划变成愿望清单。
