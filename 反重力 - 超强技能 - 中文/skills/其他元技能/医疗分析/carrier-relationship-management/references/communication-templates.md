# 沟通模板 — 承运商关系管理

> **参考类型：** 第 3 层 — 在撰写或审查承运商沟通时按需加载。
>
> **用法：** 每个模板包含 `{{双大括号}}` 中的变量占位符，用于直接替换。模板按沟通类型和业务场景组织。选择匹配您场景的模板，替换变量，审查语气指导，然后发送。

---

## 目录

1. [RFP 邀请函](#1-rfp-邀请函)
2. [运价谈判开场](#2-运价谈判开场)
3. [运价还价](#3-运价还价)
4. [承运商绩效审查 — 正面](#4-承运商绩效审查--正面)
5. [承运商绩效审查 — 整改](#5-承运商绩效审查--整改)
6. [承运商入驻欢迎](#6-承运商入驻欢迎)
7. [承运商警告信](#7-承运商警告信)
8. [承运商退出通知](#8-承运商退出通知)
9. [市场运价讨论](#9-市场运价讨论)
10. [合作伙伴提案](#10-合作伙伴提案)
11. [滞留争议沟通](#11-滞留争议沟通)
12. [附加费质疑](#12-附加费质疑)

---

## 变量参考

模板中使用的通用变量：

| 变量 | 描述 | 示例 |
|---|---|---|
| `{{carrier_name}}` | 承运商法定名称或 DBA 名称 | `Ridgeline Transport, Inc.` |
| `{{carrier_contact}}` | 承运商联系人姓名 | `Mike Patterson` |
| `{{carrier_contact_title}}` | 承运商联系人职位 | `VP of Sales` |
| `{{carrier_mc}}` | 承运商 MC 号 | `MC-498132` |
| `{{our_company}}` | 我方公司名称 | `Consolidated Manufacturing LLC` |
| `{{our_contact_name}}` | 我方代表姓名 | `Sarah Chen` |
| `{{our_contact_title}}` | 我方代表职位 | `Director of Transportation` |
| `{{our_contact_email}}` | 我方代表邮箱 | `schen@company.com` |
| `{{our_contact_phone}}` | 我方代表电话 | `(312) 555-0189` |
| `{{lane_origin}}` | 航线起点城市/州 | `Chicago, IL` |
| `{{lane_destination}}` | 航线终点城市/州 | `Dallas, TX` |
| `{{current_rate}}` | 当前合同每英里运价 | `$2.45/mile` |
| `{{proposed_rate}}` | 提议新运价 | `$2.28/mile` |
| `{{market_rate}}` | DAT/基准市场运价 | `$2.18/mile` |
| `{{volume_loads_week}}` | 每周货量 | `8 loads/week` |
| `{{annual_spend}}` | 与承运商的年度运费支出 | `$2.4M` |
| `{{contract_start}}` | 合同生效日期 | `2026-04-01` |
| `{{contract_end}}` | 合同到期日期 | `2027-03-31` |
| `{{rfp_deadline}}` | RFP 响应截止日期 | `2026-03-15` |
| `{{otd_percentage}}` | 承运商准时交付率 | `96.2%` |
| `{{tender_acceptance}}` | 承运商派车接受率 | `91.4%` |
| `{{claims_ratio}}` | 承运商索赔率 | `0.3%` |
| `{{invoice_accuracy}}` | 承运商发票准确率 | `97.8%` |
| `{{review_period}}` | 绩效审查时间段 | `Q3 2025 (Jul-Sep)` |
| `{{detention_amount}}` | 争议滞留费金额 | `$4,275` |
| `{{accessorial_type}}` | 具体附加费类型 | `升降尾板配送` |

---

## 1. RFP 邀请函

**渠道：** 邮件
**受众：** 承运商销售/定价领导层
**语气：** 专业、机会导向。您在邀请他们竞争业务，而非强求让步。

---

**主题：** `投标邀请 — {{our_company}} 货运 RFP — {{contract_start}} 授予`

{{carrier_contact}}，

{{our_company}} 正在进行年度货运 RFP 流程，我们邀请 {{carrier_name}} 作为投标承运商参与。基于我们对市场能力的分析及您的运营概况，我们认为您的网络与我们的运输需求之间存在良好的契合度。

**RFP 概览：**
- **范围：** {{lane_count}} 条航线，涵盖整车、零担和多式联运模式
- **年度总运费支出：** 约 {{total_annual_spend}}
- **合同期：** {{contract_start}} 至 {{contract_end}}
- **投标截止：** {{rfp_deadline}} 下午 5:00 CT

**我们寻找的承运商：**
我们按加权评分卡评估投标：运价竞争力（40%）、服务历史与可靠性（25%）、运力承诺（20%）以及运营匹配度含技术集成（15%）。我们重视提供稳定服务并致力于伙伴关系的承运商，而非最低运价。

**随函附上：**
1. 航线级投标包，含货量范围、设备要求和运输时效预期
2. 附加费表，含标准运价和可协商项目
3. 保险和合规要求
4. 服务级别预期（OTD、派车接受率、索赔阈值）
5. 合同条款摘要

**下一步：**
请在 {{rfp_confirm_date}} 前确认您的投标意向。所有参与承运商的问答网络研讨会定于 {{qa_date}} {{qa_time}} CT 举行。所有问题必须通过 RFP 门户书面提交；回复将与所有投标者共享。

期待您的参与。

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 2. 运价谈判开场

**渠道：** 邮件后接电话
**受众：** 承运商客户经理或销售副总裁
**语气：** 数据驱动、协作。以市场数据引领，而非要求。定位为对齐运价与市场现实，而非压榨承运商。

---

**主题：** `运价审查讨论 — {{lane_origin}} 至 {{lane_destination}} | {{our_company}}`

{{carrier_contact}}，

我想安排一个电话，讨论我们 {{lane_origin}} 至 {{lane_destination}} 航线的运价对齐。作为我们季度运价基准流程的一部分，我们发现有机会确保该航线的定价反映当前市场状况。

**我们当前情况：**
- **当前合同运价：** {{current_rate}}（自 {{contract_start}} 生效）
- **该航线 DAT 90 天合同平均：** {{market_rate}}
- **您在该航线的当前货量：** {{volume_loads_week}}
- **您的绩效：** {{otd_percentage}} OTD，{{tender_acceptance}} 派车接受率

我们认可 {{carrier_name}} 在该航线上提供了优质服务，我们的目标是找到一个对双方都有吸引力的运价。我们不想将运价压到损害您的服务或司机报酬的水平——我们寻求的是与市场变化的对齐。

您本周能安排 30 分钟通话吗？我想一起过一遍数据并探讨选项。

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 3. 运价还价

**渠道：** 邮件
**受众：** 承运商客户经理或定价团队
**语气：** 坚定但尊重。承认承运商立场的同时推进己方立场。始终以数据为依据。

---

**主题：** `回复：运价提案 — {{lane_origin}} 至 {{lane_destination}}`

{{carrier_contact}}，

感谢您对我们 {{lane_origin}} 至 {{lane_destination}} 航线的运价提案。我感谢您团队投入的细节和时间。

在根据我们的市场数据和总成本模型审查您的提案后，我想分享我们的还价立场：

**您方提案：** {{carrier_proposed_rate}}
**我方还价：** {{our_counter_rate}}

**理由：**
- 该航线 DAT 90 天合同平均为 {{market_rate}}，这意味着您的提案比当前市场基准高出 {{percentage_above_market}}%。
- 我们在柴油价格 $3.25、$3.85 和 $4.50/加仑下建模了包含您提议燃油附加费表的总成本。在当前柴油价格（{{current_diesel}}）下，您的每英里总成本为 {{total_cost_per_mile}}，比我们的基准总成本高出 {{total_cost_vs_market}}%。
- 我们 {{our_counter_rate}} 的还价运价反映市场基准加上 {{premium_percentage}}% 的服务质量溢价——我们真心重视这一点。您的 {{otd_percentage}} OTD 是我们组合中最好的之一。

**我们提供的回报：**
- 货量承诺：保证每周 {{volume_commitment}} 车（vs 您当前 {{current_volume}} 车/周）
- 付款条款：Net {{payment_days}}（vs 我们标准 Net 30）
- 我们 {{facility_name}} 设施的甩挂项目（平均每车消除 {{detention_hours}} 小时滞留）

我相信我们能找到对齐点。{{proposed_call_date}} 通话讨论可行吗？

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 4. 承运商绩效审查 — 正面

**渠道：** 邮件 + 正式季度业务审查会议
**受众：** 承运商客户经理、销售副总裁和运营领导层
**语气：** 庆祝性且具体。点名指标、量化影响，并以具体行动奖励（更多货量、更长合同、公开认可）。泛泛的表扬不如不表扬。

---

**主题：** `Q{{quarter}} 绩效审查 — {{carrier_name}} | 卓越成果`

{{carrier_contact}}，

我想正式认可 {{carrier_name}} 在 {{review_period}} 期间的表现。您的团队在我们追踪的每个指标上都表现卓越，我们要确保您知道这一点——并以行动支持这一认可。

**绩效摘要 — {{review_period}}：**

| 指标 | 目标 | 您的表现 | 组合平均 |
|--------|--------|-----------------|-------------------|
| 准时交付率 | ≥95% | {{otd_percentage}} | {{portfolio_avg_otd}} |
| 派车接受率 | ≥90% | {{tender_acceptance}} | {{portfolio_avg_tender}} |
| 索赔率 | <0.5% | {{claims_ratio}} | {{portfolio_avg_claims}} |
| 发票准确率 | ≥97% | {{invoice_accuracy}} | {{portfolio_avg_invoice}} |

**具体亮点：**
- 您的团队在 {{highlight_lane}} 航线上的表现尤为突出——{{highlight_detail}}。
- 司机 {{driver_name}} 因持续的专业精神和高效的月台操作收到我们 {{facility_name}} 收货团队的表扬。
- 您的运营团队在 {{event}} 期间的主动沟通避免了一次可能严重的服务中断。

**这对我们的伙伴关系意味着什么：**
基于此表现，我们将在 {{effective_date}} 起进行以下分配调整：
- **{{lane_1}}：** 将您的分配从 {{old_allocation_1}}% 增加到 {{new_allocation_1}}%
- **{{lane_2}}：** 新增您为主要承运商（新航线授予 — {{volume_2}} 车/周）
- **合同延长：** 我们想讨论将协议延长至 {{extended_end_date}}，条款不变

感谢让我们的运营更好。我们重视这段伙伴关系，期待继续共同成长。

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 5. 承运商绩效审查 — 整改

**渠道：** 邮件后接当面或视频会议
**受众：** 承运商客户经理和运营领导层
**语气：** 专业、直接、数据驱动。非惩罚性——整改性。呈现数据、陈述影响、设定明确期望和时间线、定义后果。避免情绪化语言。

---

**主题：** `绩效审查 — {{carrier_name}} | 需要整改行动`

{{carrier_contact}}，

我联系您是关于 {{carrier_name}} 在 {{review_period}} 期间为 {{our_company}} 服务的航线表现。多项指标已低于我们的最低标准，我想直接解决这个问题，以便我们共同找到解决方案。

**绩效摘要 — {{review_period}}：**

| 指标 | 我方标准 | 您的表现 | 差距 |
|--------|-------------|-----------------|-----|
| 准时交付率 | ≥95% | {{otd_percentage}} | {{otd_gap}} 低于标准 |
| 派车接受率 | ≥90% | {{tender_acceptance}} | {{tender_gap}} 低于标准 |
| 索赔率 | <0.5% | {{claims_ratio}} | {{claims_gap}} 高于标准 |
| 发票准确率 | ≥97% | {{invoice_accuracy}} | {{invoice_gap}} 低于标准 |

**业务影响：**
- {{problem_lane}} 航线上的派车拒绝迫使 {{spot_loads}} 车货物进入现货市场，平均溢价 {{spot_premium}}%，造成约 ${{incremental_cost}} 增量运费支出。
- 延迟交付导致 {{penalty_count}} 次客户罚款事件，总计 ${{penalty_total}}。

**我们需要什么：**
我们重视与 {{carrier_name}} 的关系并希望找到前进道路。我们要求一份整改行动计划，在以下时间线内解决：

| 指标 | 目标 | 30 天检查点 | 60 天检查点 |
|--------|--------|-------------------|-------------------|
| OTD | ≥{{otd_target}}% | ≥{{otd_30day}}% | ≥{{otd_60day}}% |
| 派车接受率 | ≥{{tender_target}}% | ≥{{tender_30day}}% | ≥{{tender_60day}}% |

请在 {{cap_due_date}} 前发送您的 CAP 文件，概述您识别的根本原因及具体运营变更。

**如果未达标：**
如果 60 天检查点目标未达成，我们将需要把您在受影响航线上的分配减少 50%，并将货量重新分配给替代承运商。这不是我们期望的结果——我们更希望看到改进并继续建立这段伙伴关系。

我想在 {{proposed_call_date}} 安排一个电话讨论您的初步评估。请告知您的可用时间。

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 6. 承运商入驻欢迎

**渠道：** 邮件
**受众：** 承运商指定客户经理和运营联系人
**语气：** 欢迎、有序、明确期望。第一印象决定关系轨迹。

---

**主题：** `欢迎加入 {{our_company}} 承运商网络 — 入驻信息`

{{carrier_contact}}，

欢迎加入 {{our_company}} 承运商网络。我们很高兴 {{carrier_name}} 成为运输合作伙伴，期待富有成效的关系。

本邮件包含您开始所需的一切。请仔细审查，如有问题请告知。

**您被授予的航线：**

| 航线 | 货量 | 设备 | 运输时效要求 |
|------|--------|-----------|-------------------|
| {{lane_1_origin}} → {{lane_1_dest}} | {{lane_1_volume}}/周 | {{lane_1_equip}} | {{lane_1_transit}} |
| {{lane_2_origin}} → {{lane_2_dest}} | {{lane_2_volume}}/周 | {{lane_2_equip}} | {{lane_2_transit}} |

**入驻清单（请在 {{onboarding_deadline}} 前完成）：**

- [ ] 返还签署的承运商运输协议（附件）
- [ ] 提供符合我们最低要求的当前保险证明（$1M 汽车责任险，$100K 货物险）
- [ ] 完成 W-9 表格（附件）
- [ ] 提供系统集成设置的 EDI/API 联系人（如适用）
- [ ] 确认日常派车运营联系人（姓名、电话、邮箱）
- [ ] 确认下班后紧急联系人（姓名、电话）

**预期内容：**
- **前 30 天：** 我们将在您被授予的航线上运行试运货物。我们在试运期间的最低标准：≥93% OTD，≥85% 派车接受率，≥95% 发票准确率。
- **第 30 天审查：** 我们将一起审查试运绩效。如果达标，您将获得全额分配。如果未达标，我们将讨论需要哪些调整。
- **持续：** 季度绩效审查，与我们的 RFP 周期对齐的年度运价审查。

**我们的设施 — 关键运营说明：**

| 设施 | 月台时间 | 需预约？ | 平均装卸时间 | 滞留政策 |
|----------|-----------|----------------------|---------------------|-----------------|
| {{facility_1}} | {{hours_1}} | {{appt_1}} | {{avg_time_1}} | {{detention_1}} |
| {{facility_2}} | {{hours_2}} | {{appt_2}} | {{avg_time_2}} | {{detention_2}} |

**您在 {{our_company}} 的主要联系人：**
- **关系管理：** {{our_contact_name}}，{{our_contact_title}}（{{our_contact_email}}，{{our_contact_phone}}）
- **日常运营/派车：** {{ops_contact_name}}，{{ops_contact_title}}（{{ops_contact_email}}，{{ops_contact_phone}}）
- **应付账款/发票：** {{ap_contact_name}}（{{ap_contact_email}}）

欢迎加入。我们相信奖励绩效——提供稳定、优质服务的承运商将获得更多货量、更长合同和新航线的优先考虑。

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}

---

## 7. 承运商警告信

**渠道：** 正式邮件，请求已读回执；抄送承运商销售副总裁
**受众：** 承运商客户经理 + 承运商高级领导层
**语气：** 正式且严肃。这是记录事件，也是沟通——它为潜在退出决策建立书面记录。事实性，非情绪化。引用具体合同条款。

---

**主题：** `正式通知：绩效缺陷 — {{carrier_name}} / {{our_company}} 账户`

{{carrier_contact}}，

本函作为正式通知，{{carrier_name}} 在 {{our_company}} 账户上的表现已持续低于合同标准，持续不合规将导致货量减少及可能从我们的路由指南中移除。

**缺陷摘要：**
根据我们 {{agreement_date}} 运输协议第 {{contract_section}} 条，以下最低标准适用：

| 指标 | 合同最低 | {{carrier_name}} 表现（{{deficiency_period}}） |
|--------|--------------------|----------------------------------------------------|
| {{metric_1}} | {{standard_1}} | {{actual_1}} |
| {{metric_2}} | {{standard_2}} | {{actual_2}} |

**先前沟通：**
- {{prior_comm_date_1}}：{{prior_comm_description_1}}
- {{prior_comm_date_2}}：{{prior_comm_description_2}}
- {{cap_date}}：提交整改行动计划，目标在 {{cap_target_date}} 前改进
- 截至 {{current_date}}，目标未达成。

**后果：**
自 {{consequence_date}} 起，我们将把 {{carrier_name}} 在以下航线的分配减少 {{reduction_percentage}}%：
{{affected_lanes_list}}

如果绩效在 {{final_deadline}} 前未达到合同最低标准，{{carrier_name}} 将从所有受影响航线的活跃路由指南中移除。

**解决路径：**
我们更愿意合作解决此问题。如果 {{carrier_name}} 能提供更新的补救计划，解决具体根本原因并承诺可衡量的改进目标，我们愿意将审查期延长 30 天。

请在 {{response_deadline}} 前书面回复。

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

抄送：{{carrier_vp_name}}，{{carrier_vp_title}}，{{carrier_name}}
抄送：{{our_director_name}}，{{our_director_title}}，{{our_company}}

---

## 8. 承运商退出通知

**渠道：** 正式邮件后接电话
**受众：** 承运商客户经理和承运商高级领导层
**语气：** 尊重且最终。这是商业决策，非惩罚。为未来考虑留有余地。避免断桥——承运商圈子比你想象的要小。

---

**主题：** `路由指南移除通知 — {{carrier_name}} / {{our_company}}`

{{carrier_contact}}，

经过仔细考虑和审查 {{carrier_name}} 在过去 {{review_months}} 个月的表现，我们决定自 {{exit_date}} 起将 {{carrier_name}} 从 {{our_company}} 活跃路由指南中移除。

**决策原因：**
{{exit_reason_summary}}

**过渡计划：**
- **{{exit_date}} 至 {{transition_end_date}}：** 我们将在过渡期内每周减少约 {{reduction_percent}}% 的派车货量，以便双方组织调整。
- **未结发票：** 所有未结发票将按标准付款条款处理。请确保所有发票在 {{invoice_deadline}} 前提交。
- **未结索赔：** 任何待处理索赔将继续其正常解决流程。此决定不影响未结索赔的裁决。

**对未来的意义：**
这不一定是永久决定。我们在年度 RFP 流程期间审查承运商组合。如果 {{carrier_name}} 解决上述问题并希望重新合作，我们欢迎您参与未来的 RFP 周期。

如果您想直接沟通，我可以讨论此决定。我尊重您团队为我们账户所做的工作，并希望确保此过渡专业处理。

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 9. 市场运价讨论

**渠道：** 邮件或电话，取决于关系深度
**受众：** 承运商客户经理
**语气：** 友善且透明。这是市场讨论，非谈判——您在分享数据并邀请对话。当市场条件发生变化且您想在成为正式重新谈判之前主动讨论对齐时使用。

---

**主题：** `市场情况沟通 — {{lane_origin}} 至 {{lane_destination}} 走廊`

{{carrier_contact}}，

我想主动联系您，讨论我们在 {{lane_origin}} 至 {{lane_destination}} 市场看到的情况。如您所知，我们按季度追踪航线级基准，最新数据显示一些值得讨论的变化。

**我们看到的情况：**
- 该航线 DAT 合同平均在过去 {{timeframe}} 从 {{old_benchmark}} 变动至 {{new_benchmark}}——{{percentage_change}} {{direction}} 变化。
- 我们在该走廊溢出货物上的现货采购在过去 30 天平均为 {{spot_average}}。
- {{region}} 地区的货车比目前为 {{ltt_ratio}}，而上季度为 {{ltt_previous}}。

**我们的观点：**
我们发送此邮件不是作为正式运价请求——这是市场对话。我们想了解您如何看待同样的数据，以及是否有机会主动对齐，而非等待合同续签。

如果市场变化影响了我们航线的经济性，我宁愿现在讨论并找到双方可行的解决方案，也不愿在年度审查时才发现问题。

您本周有 20 分钟讨论吗？

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 10. 合作伙伴提案

**渠道：** 正式信函或会议演示
**受众：** 承运商 CEO、总裁或销售高级副总裁
**语气：** 战略性且前瞻性。这是商业伙伴提案，非采购交易。强调互利、增长潜力和承诺。

---

**主题：** `战略合作伙伴提案 — {{our_company}} 与 {{carrier_name}}`

{{carrier_contact}}，

我想提议将 {{our_company}} 与 {{carrier_name}} 的关系从标准承运商-托运商安排提升为战略伙伴关系。我们的分析表明，更深层次、更一体化的合作将带来显著互利。

**为何选择 {{carrier_name}}：**
在过去 {{relationship_years}} 年中，{{carrier_name}} 在我们承运商组合中持续表现顶级。具体而言：
- {{otd_percentage}} OTD（vs 组合平均 {{portfolio_avg}}%）
- {{tender_acceptance}} 派车接受率（vs 平均 {{portfolio_avg_tender}}%）
- 卓越的沟通和问题解决响应能力

**我们提议的内容：**
1. **货量承诺：** 将 {{carrier_name}} 在我们总货运中的份额从 {{current_share}}% 增加到 {{proposed_share}}%，代表约 {{proposed_spend}} 年度运费支出。
2. **多年协议：** 24 个月合同，预设年度调价与 {{escalator_index}} 挂钩，替代您航线的年度 RFP 周期。
3. **运营整合：** 实施实时追踪集成（API）、共享 KPI 仪表盘和季度高管业务审查。
4. **增长协作：** 当 {{our_company}} 扩展至 {{growth_markets}} 时，{{carrier_name}} 将成为您网络中新航线的首选承运商。

**我们需要您提供的：**
1. 运价对齐：反映货量承诺和多年确定性的竞争性定价（我们的目标是 DAT 合同基准 {{target_range}}% 范围内的运价）。
2. 服务保证：{{otd_target}}% OTD 和 {{tender_target}}% 派车接受率，季度审查。
3. 专属客户管理：一位了解我们运营、客户和季节性模式的指定联系人。
4. 运力优先：在旺季或中断事件期间，{{our_company}} 货物获得您运营团队的优先派车。

我欢迎有机会与您领导团队会面讨论此事。{{proposed_meeting_date}} 在 {{proposed_location}} 进行当面会议可行吗？

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 11. 滞留争议沟通

**渠道：** 邮件，附支持文档
**受众：** 承运商计费/应收账款团队，抄送承运商客户经理
**语气：** 事实性且合作。滞留争议很快变得对抗——以数据引领，愿意支付合理部分，同时争议不合理部分。

---

**主题：** `滞留发票争议 — PRO# {{pro_number}} / {{dispute_date}}`

{{carrier_contact}}，

我们已审查 PRO# {{pro_number}}（{{lane_origin}} 至 {{lane_destination}}，{{delivery_date}} 交付）的滞留发票，发现发票滞留与我们设施记录之间存在差异。

**您方发票：**
- 司机到达：{{carrier_arrival_time}}
- 离开：{{carrier_departure_time}}
- 计费滞留总计：{{billed_detention_hours}} 小时，单价 ${{detention_rate}}/小时 = {{detention_amount}}

**我方记录：**
- 司机在门卫处签到：{{our_checkin_time}}
- 分配月台门：{{dock_assign_time}}
- 装卸完成（BOL 签字）：{{bol_sign_time}}
- 免费时间：按合同第 {{contract_section}} 条 {{free_time_hours}} 小时

**差异分析：**
- 司机在预约时间 {{appointment_time}} 前 {{early_minutes}} 分钟到达。按我们合同，滞留从预约时间或到达时间中较晚者开始计算——而非提前到达时间。
- 我们的记录显示实际月台停留时间（从签到到 BOL 签字）为 {{actual_dwell}} 小时，其中 {{free_time_hours}} 小时为免费时间。按我们记录计费滞留：{{adjusted_detention}} 小时。

**我方提议解决方案：**
我们将支付此发票 {{adjusted_amount}}（{{adjusted_detention}} 小时 × ${{detention_rate}}/小时）。如果您认为我们的记录不准确，请提供司机 GPS 或 ELD 数据显示月台到达和离开时间，我们将核对。

我们希望为双方正确处理此事。如果该航线的滞留是持续问题，我欢迎讨论调整预约调度或实施甩挂项目以解决根本原因。

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 12. 附加费质疑

**渠道：** 邮件
**受众：** 承运商计费/定价团队，抄送承运商客户经理
**语气：** 适度且基于证据。附加费争议是高频低额事件，如果处理激进会损害关系。关注准确性，非指责。

---

**主题：** `附加费审查 — {{accessorial_type}} | PRO# {{pro_number}}`

{{carrier_contact}}，

我们正在审查 PRO# {{pro_number}}（{{lane_origin}} 至 {{lane_destination}}，{{delivery_date}}）的附加费，在处理付款前需要澄清。

**争议费用：**
- 附加费类型：{{accessorial_type}}
- 金额：${{accessorial_amount}}
- 发票参考：{{invoice_number}}

**我方关切：**
{{concern_detail}}

按我们运输协议（第 {{contract_section}} 条，附加费表项目 {{schedule_item}}），{{accessorial_type}} 费用适用于 {{contract_condition}}。基于此货物的 BOL 和交付收据，{{evidence_detail}}。

**支持文档（附件）：**
- BOL 显示 {{bol_detail}}
- 交付收据显示 {{pod_detail}}
- 含附加费表参考的运价确认

**请求行动：**
请根据附件文档审查该费用，并 (a) 提供我们可能未有的额外支持证据确认收费，或 (b) 对发票 {{invoice_number}} 开具 ${{accessorial_amount}} 的贷项通知单。

如果此附加费类别在该航线上成为持续问题，我想讨论是否有运营调整（任一端）可防止这些费用累积。

感谢您的及时审查。

此致，

{{our_contact_name}}
{{our_contact_title}} | {{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 使用指南

### 按关系状态校准语气

| 关系状态 | 适用模板 | 语气调整 |
|--------------------|----------------------|-----------------|
| 新承运商（< 6 个月） | 入驻欢迎、运价谈判开场、市场运价讨论 | 更正式，设定明确期望，具体说明标准 |
| 成熟承运商（6-24 个月） | 所有模板 | 标准专业语气，数据驱动，协作 |
| 战略伙伴（2+ 年，顶级） | 绩效审查正面、合作伙伴提案、市场运价讨论 | 更友善，强调增长机会，分享更多运营背景 |
| 表现不佳承运商 | 绩效审查整改、警告信、退出通知 | 严格专业，记录一切，关注事实和数据 |
| 争议中承运商 | 滞留争议、附加费质疑、警告信 | 事实性且中立，避免情绪化语言，始终提议解决路径 |

### 沟通渠道选择

| 情况 | 主要渠道 | 何时升级渠道 |
|-----------|----------------|------------------------|
| 运价讨论（常规） | 邮件 → 电话跟进 | 如果邮件往来超过 3 轮未解决 |
| 绩效审查（正面） | 邮件 + QBR 会议 | 不适用 — 始终广泛分享好消息 |
| 绩效审查（整改） | 邮件优先（文档记录），然后电话/会议 | 如果承运商 5 个工作日内未回复 |
| 警告信 | 正式邮件带已读回执 | 如果承运商 3 个工作日内未回复，通过承运商副总裁电话跟进 |
| 退出通知 | 正式邮件 + 当天电话 | 不适用 — 始终通过两个渠道传达退出决定 |
| 滞留/附加费争议 | 邮件附带文档 | 如果 15 个工作日内未解决，升级至承运商客户经理 |
| 合作伙伴提案 | 正式信函/邮件 → 当面会议 | 不适用 — 合作伙伴提案需要当面讨论 |
