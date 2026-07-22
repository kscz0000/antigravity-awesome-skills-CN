# 沟通模板 — 物流异常管理

> **参考类型：** 第三层 — 在撰写或审查异常沟通时按需加载。
>
> **使用方法：** 每个模板包含 `{{双花括号}}` 中的变量占位符，用于直接替换。模板按受众和升级阶段组织。选择匹配你场景的模板，替换变量，审查语气指导，然后发送。

---

## 目录

1. [初始异常通知 — 承运商（标准）](#1-初始异常通知--承运商标准)
2. [初始异常通知 — 承运商（紧急）](#2-初始异常通知--承运商紧急)
3. [客户主动更新 — 延误](#3-客户主动更新--延误)
4. [客户主动更新 — 损坏](#4-客户主动更新--损坏)
5. [客户主动更新 — 丢失](#5-客户主动更新--丢失)
6. [升级至承运商客户经理](#6-升级至承运商客户经理)
7. [升级至承运商 VP/总监](#7-升级至承运商-vp总监)
8. [内部升级至供应链 VP](#8-内部升级至供应链-vp)
9. [索赔提交附函](#9-索赔提交附函)
10. [和解谈判回复（接受）](#10-和解谈判回复接受)
11. [和解谈判回复（拒绝）](#11-和解谈判回复拒绝)
12. [解决后总结](#12-解决后总结)
13. [承运商绩效警告](#13-承运商绩效警告)
14. [客户致歉及解决方案](#14-客户致歉及解决方案)

---

## 变量参考

模板中使用的通用变量：

| 变量 | 描述 | 示例 |
|---|---|---|
| `{{pro_number}}` | 承运商 PRO / 追踪号 | `PRO 1234-5678-90` |
| `{{bol_number}}` | 提单号 | `BOL-2025-04872` |
| `{{po_number}}` | 客户采购订单号 | `PO-88431` |
| `{{shipment_id}}` | 内部货物参考号 | `SHP-2025-11049` |
| `{{carrier_name}}` | 承运商法定名称或 DBA 名称 | `Acme Freight, Inc.` |
| `{{carrier_mc}}` | 承运商 MC/DOT 号 | `MC-345678` |
| `{{carrier_scac}}` | 承运商 SCAC 代码 | `ACMF` |
| `{{origin_city_state}}` | 始发城市和州 | `Dallas, TX` |
| `{{dest_city_state}}` | 目的城市和州 | `Columbus, OH` |
| `{{ship_date}}` | 原始发货日期 | `2025-09-14` |
| `{{original_eta}}` | 原始预计交付时间 | `2025-09-17` |
| `{{revised_eta}}` | 修订预计交付时间 | `2025-09-19` |
| `{{customer_name}}` | 客户公司名称 | `Midwest Distribution Co.` |
| `{{customer_contact}}` | 客户联系人姓名 | `Sarah Chen` |
| `{{our_contact_name}}` | 我方代表姓名 | `James Petrovic` |
| `{{our_contact_title}}` | 我方代表职务 | `Transportation Manager` |
| `{{our_contact_email}}` | 我方代表邮箱 | `jpetrovic@company.com` |
| `{{our_contact_phone}}` | 我方代表电话 | `(312) 555-0147` |
| `{{our_company}}` | 我方公司名称 | `Consolidated Shippers LLC` |
| `{{exception_date}}` | 异常发现日期 | `2025-09-16` |
| `{{commodity}}` | 货物商品描述 | `Automotive brake assemblies` |
| `{{weight}}` | 货物重量 | `12,400 lbs` |
| `{{piece_count}}` | 件数/托盘数 | `14 pallets` |
| `{{freight_charge}}` | 运费金额 | `$3,840.00` |
| `{{cargo_value}}` | 申报货物价值 | `$47,200.00` |
| `{{claim_amount}}` | 索赔金额 | `$47,200.00` |
| `{{claim_number}}` | 承运商分配的索赔编号 | `CLM-2025-0398` |
| `{{our_claim_ref}}` | 内部索赔参考号 | `EXC-2025-1104` |
| `{{deadline_date}}` | 回复或行动截止日期 | `2025-09-18 by 14:00 CT` |
| `{{days_in_transit}}` | 货物在途天数 | `5` |
| `{{last_known_location}}` | 最后扫描或电话确认位置 | `Indianapolis, IN terminal` |

---

## 1. 初始异常通知 — 承运商（标准）

### 何时使用
- 通过追踪、电话确认未果或 OS&D 报告发现异常。
- 严重程度为中等——货物延误或有差异，但没有立即危险。
- 首次就特定问题联系承运商运营或调度部门。

### 语气指导
保持客观和协作。你是以专业身份通知合作伙伴存在差异，而非指责任何人失职。假设善意——目标是获取信息和纠正方案，而非在此阶段归责。

### 不要说的话
- 不要在首次联系中威胁索赔或合同后果。
- 不要猜测异常原因。
- 不要使用"你们未能"或"你们的司机造成"之类的措辞——你尚未确认根因。
- 不要在承运商运营沟通中抄送客户。

### 主题行

```
Exception Notice — PRO {{pro_number}} | {{origin_city_state}} to {{dest_city_state}} | BOL {{bol_number}}
```

### 正文

```
Team,

We are writing regarding a shipment exception on the following load:

  PRO:            {{pro_number}}
  BOL:            {{bol_number}}
  PO:             {{po_number}}
  Origin:         {{origin_city_state}}
  Destination:    {{dest_city_state}}
  Ship Date:      {{ship_date}}
  Original ETA:   {{original_eta}}
  Commodity:      {{commodity}}
  Weight/Count:   {{weight}} / {{piece_count}}

EXCEPTION DETAILS:
{{exception_description}}

We identified this exception on {{exception_date}} at approximately {{exception_time}}.
The last confirmed status was {{last_known_status}} at {{last_known_location}} on
{{last_scan_date}}.

We need the following from your team:

  1. Current physical location of the freight
  2. Updated ETA to the consignee
  3. Root cause of the delay or discrepancy
  4. Corrective action being taken

Please respond by {{deadline_date}} so we can update our customer accordingly.

If you have questions or need additional shipment details, contact me directly at
{{our_contact_phone}} or {{our_contact_email}}.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}}
```

---

## 2. 初始异常通知 — 承运商（紧急）

### 何时使用
- 货物属于关键类型：生产线停工、门店开业、易腐品或高价值货物。
- 异常造成即时财务暴露（如生产线停工、合同罚款窗口）。
- 客户已升级或 SLA 违约迫在眉睫（24小时内）。

### 语气指导
直接且有时间约束。这不是敌意，而是传达情况需要立即行动，而非明天回电。每句话都应推动具体下一步。使用具体截止时间，而非"尽快"。

### 不要说的话
- 不要弱化紧迫性——"方便的时候"会削弱整条信息。
- 不要在这个阶段发出你无法执行的最后通牒。
- 不要提及其他货物或无关绩效问题——聚焦本票货物。
- 不要省略财务暴露数字；它证明了紧迫性的合理性。

### 主题行

```
URGENT — Immediate Response Required | PRO {{pro_number}} | {{dest_city_state}} | ETA Miss
```

### 正文

```
URGENT — IMMEDIATE RESPONSE REQUIRED

This shipment requires your immediate attention. We need a substantive response
by {{deadline_date}} — not an acknowledgment, but confirmed status and a recovery plan.

SHIPMENT DETAILS:
  PRO:            {{pro_number}}
  BOL:            {{bol_number}}
  PO:             {{po_number}}
  Origin:         {{origin_city_state}}
  Destination:    {{dest_city_state}}
  Ship Date:      {{ship_date}}
  Original ETA:   {{original_eta}}
  Commodity:      {{commodity}}
  Weight/Count:   {{weight}} / {{piece_count}}
  Declared Value: {{cargo_value}}

EXCEPTION:
{{exception_description}}

BUSINESS IMPACT:
{{business_impact_description}}

Estimated financial exposure if not resolved by {{resolution_deadline}}: {{financial_exposure}}.

REQUIRED BY {{deadline_date}}:
  1. Confirmed physical location of the freight — verified, not last-scan
  2. Firm revised delivery date and time
  3. Name and direct phone number of the person managing recovery
  4. Written recovery plan

If I do not have a response by the deadline above, I will escalate to your account
management team and begin contingency planning, which may include diversion or
re-tender.

Contact me directly:
{{our_contact_name}} | {{our_contact_phone}} | {{our_contact_email}}

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
```

---

## 3. 客户主动更新 — 延误

### 何时使用
- 运输延误已确认或极有可能（修订 ETA 超出承诺窗口）。
- 在客户自行发现延误之前发送。主动沟通维护信任；被动沟通侵蚀信任。
- 你有修订的 ETA——即使是近似的。如果完全没有 ETA，如实说明并承诺跟进时间。

### 语气指导
诚实且以解决方案为导向。直接承认延误——不要用修饰语掩盖。先给出修订时间线，再简要说明原因。客户想知道"我什么时候能收到货"，然后才是"发生了什么"。不要点名承运商或将责任归咎于任何特定方。

### 不要说的话
- 不要点名指责承运商——说"我们的承运商合作伙伴"，而非"XYZ 卡车公司搞砸了"。
- 不要说"不可预见的情况"——具体说明原因类别（天气、设备、路线）。
- 不要承诺你无法支撑的修订 ETA。如果不确定，给出范围。
- 不要使用"对造成的不便深表歉意"——这读起来像套话。具体说明你理解的影响。

### 主题行

```
Shipment Update — PO {{po_number}} | Revised ETA {{revised_eta}}
```

### 正文

```
{{customer_contact}},

I want to update you on PO {{po_number}} (our reference {{shipment_id}}) shipping
from {{origin_city_state}} to {{dest_city_state}}.

This shipment is experiencing a transit delay. The original estimated delivery was
{{original_eta}}. Based on current status, the revised delivery estimate is
{{revised_eta}}.

CAUSE: {{delay_cause_customer_facing}}

HERE IS WHAT WE ARE DOING:
  - {{action_item_1}}
  - {{action_item_2}}
  - {{action_item_3}}

I will send you another update by {{next_update_time}} with confirmed delivery
details. If the timeline shifts further in either direction, you will hear from me
immediately.

If this delay impacts your operations and you need us to evaluate expedited
alternatives, please let me know and I will have options to you within
{{expedite_response_window}}.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}} | {{our_contact_email}}
```

### 变体 — 延误但尚无 ETA

当你无法提供修订 ETA 时，替换 ETA 部分：

```
This shipment is experiencing a transit delay. The original estimated delivery was
{{original_eta}}. We do not yet have a confirmed revised delivery time, but I am
working to get one and will update you by {{next_update_time}} today.
```

---

## 4. 客户主动更新 — 损坏

### 何时使用
- 承运商或收货人报告交付时或运输中有可见损坏。
- 损坏已确认或强烈怀疑（如司机照片、收货人在 POD 上的标注）。
- 在客户打电话给你之前发送。如果他们是收货人，在他们不得不追着你问下一步之前发送。

### 语气指导
先说解决方案，再说问题。客户的第一个问题是"你们打算怎么办"——在描述损坏之前先回答。具体说明补救路径（替换、贷记、重新发货）和时间线。对业务影响表达真诚关切，但不要夸张。

### 不要说的话
- 不要以损坏描述开头。开头段落应该是关于解决方案路径。
- 不要说"运输中这种事难免"——这弱化了客户的损失。
- 在调查完成前不要猜测原因（包装、搬运、天气）。
- 不要让客户自己提索赔——那是你的工作。

### 主题行

```
PO {{po_number}} — Delivery Update and Resolution Plan
```

### 正文

```
{{customer_contact}},

I am reaching out regarding PO {{po_number}} (our reference {{shipment_id}})
delivered to {{dest_city_state}} on {{delivery_date}}.

We have identified damage to a portion of this shipment and I want to walk you
through the resolution we are putting in place.

RESOLUTION:
  {{resolution_description}}

  Timeline: {{resolution_timeline}}

DAMAGE DETAILS:
  Items Affected:   {{damaged_items_description}}
  Extent:           {{damage_extent}}
  Pieces Affected:  {{damaged_piece_count}} of {{piece_count}} total

We are handling the carrier claim and investigation on our end — no action is
needed from your team on that front.

What we do need from you:
  - Confirmation of the affected quantities once your receiving team completes
    inspection
  - Direction on whether you want us to {{resolution_option_a}} or
    {{resolution_option_b}}

I understand this impacts your {{customer_impact_area}} and I take that seriously.
I will stay on this personally until it is fully resolved.

Next update from me: {{next_update_time}}.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}} | {{our_contact_email}}
```

---

## 5. 客户主动更新 — 丢失

### 何时使用
- 货物已确认丢失——不仅是延误或无法定位。当承运商在彻底追踪后确认无法找到货物，或已过 {{days_without_scan}} 天且承运商未回应追踪请求时，货物即为"丢失"。
- 这是最敏感的异常沟通。客户正在得知他们的货物已经没了。不要对仅仅是迟到或暂时无法定位的货物使用此模板。

### 语气指导
同理心、直接、行动导向。不要含糊其辞或使用被动语态——"您的货物已丢失"比"似乎存在涉及您订单未交付的情况"更清晰。立即建立行动计划。客户需要知道三件事：(1) 发生了什么，(2) 你现在在做什么，(3) 何时会有解决方案。传达你理解严重性。

### 不要说的话
- 如果货物已确认丢失，不要说"放错了位置"或"配错了路线"——听起来像你在淡化。
- 不要在没有具体下一步和截止时间的情况下说"我们还在调查"。
- 不要点名指责承运商。
- 不要以索赔流程开头——以替换或补救方案开头。客户需要的是货物，不是索赔教育。
- 不要使用"不幸的是"超过一次。

### 主题行

```
PO {{po_number}} — Shipment Status and Immediate Action Plan
```

### 正文

```
{{customer_contact}},

I need to share a difficult update on PO {{po_number}} (our reference
{{shipment_id}}), originally shipping {{origin_city_state}} to
{{dest_city_state}} on {{ship_date}}.

After an extensive trace with our carrier partner, we have confirmed that this
shipment — {{piece_count}} of {{commodity}}, valued at {{cargo_value}} — has
been lost in transit. I know this creates a real problem for your team and I want
to lay out exactly what we are doing about it.

IMMEDIATE ACTION PLAN:

  1. REPLACEMENT / RE-SHIP:
     {{replacement_plan}}
     Expected availability: {{replacement_date}}

  2. FINANCIAL REMEDIATION:
     {{financial_remediation_plan}}
     Timeline: {{financial_remediation_timeline}}

  3. CARRIER CLAIM:
     We have filed a formal cargo claim against the carrier. This is our
     responsibility to manage — you do not need to take any action on the
     claim.
     Claim reference: {{our_claim_ref}}

  4. PREVENTION:
     {{prevention_steps}}

I will call you at {{follow_up_call_time}} to discuss this directly and answer
any questions. If you need to reach me before then, my cell is
{{our_contact_phone}}.

I take full ownership of making this right.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}} | {{our_contact_email}}
```

---

## 6. 升级至承运商客户经理

### 何时使用
- 对承运商调度或运营的首次联系在标准异常上4小时以上未获回复，或在紧急异常上2小时以上未获回复。
- 你已记录至少两次对一线联系人的联系尝试（邮件、电话或两者）。
- 客户经理是承运商组织中可以在内部施加压力的下一层级。

### 语气指导
专业但坚定。你不是在生气——你是一个合理请求被忽视的商业伙伴，你需要客户经理介入。如实陈述你尝试的时间线。让请求具体化。客户经理需要确切知道你需要什么以及何时需要，这样他们才能推动自己的运营团队。

### 不要说的话
- 不要点名贬低一线联系人——说"你们的运营团队"或"你们的调度"。
- 除非你确实有此意图和权限，否则不要在此阶段威胁撤走货物。
- 不要堆叠无关问题——聚焦本票货物。

### 主题行

```
Escalation — No Response on PRO {{pro_number}} | Requires Your Intervention
```

### 正文

```
{{carrier_account_manager_name}},

I am escalating to you because I have been unable to get a substantive response
from your operations team on a shipment exception that requires immediate
attention.

SHIPMENT:
  PRO:          {{pro_number}}
  BOL:          {{bol_number}}
  PO:           {{po_number}}
  Route:        {{origin_city_state}} → {{dest_city_state}}
  Ship Date:    {{ship_date}}
  Original ETA: {{original_eta}}

EXCEPTION:
{{exception_description}}

OUTREACH TIMELINE:
  {{attempt_1_date_time}} — {{attempt_1_method}}: {{attempt_1_summary}}
  {{attempt_2_date_time}} — {{attempt_2_method}}: {{attempt_2_summary}}
  {{attempt_3_date_time}} — {{attempt_3_method}}: {{attempt_3_summary}}

It has been {{hours_since_first_contact}} hours since our first outreach with no
confirmed status or recovery plan.

I need the following by {{deadline_date}}:
  1. Confirmed current location of the freight
  2. Firm revised ETA
  3. A direct contact managing the recovery who I can reach by phone

My customer is waiting on this update and I cannot continue to respond with "we
are working on it" without specifics.

Please call me at {{our_contact_phone}} or reply to this email by the deadline
above.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}} | {{our_contact_email}}
```

---

## 7. 升级至承运商 VP/总监

### 何时使用
- 客户经理未能在合理窗口内解决或回复（通常为客户经理升级后12-24小时）。
- 异常有重大财务暴露，或存在类似故障的模式。
- 你准备好引用合同条款、运量承诺或有记录的绩效历史。
- 这是正式升级——发送时要知道它可能被分享给承运商高管层。

### 语气指导
正式且数据驱动。这是资深专业人士之间的商务沟通。不带情绪、不带讽刺、不带威胁——但清晰陈述作为商业现实的后果。引用具体合同条款、金额和事件历史。VP 需要理解这不是一次性的投诉；这是他们需要管理的商业风险。

### 不要说的话
- 不要讽刺或居高临下——"我确定您很忙"会削弱你的可信度。
- 不要做出你无法兑现的威胁（如"我们再也不会用你们了"，而他们是你某条线路的唯一选择）。
- 不要引用口头承诺或非正式协议——只引用有记录的内容。
- 不要抄送你的客户。这是承运商管理对话。

### 主题行

```
Executive Escalation — Unresolved Exception PRO {{pro_number}} | {{our_company}} Account
```

### 正文

```
{{carrier_vp_name}},
{{carrier_vp_title}}
{{carrier_name}}

I am writing to escalate a shipment exception that has not been resolved despite
repeated engagement with your operations and account management teams.

SHIPMENT DETAILS:
  PRO:            {{pro_number}}
  BOL:            {{bol_number}}
  Route:          {{origin_city_state}} → {{dest_city_state}}
  Ship Date:      {{ship_date}}
  Commodity:      {{commodity}}
  Shipment Value: {{cargo_value}}

EXCEPTION SUMMARY:
{{exception_description}}

ESCALATION HISTORY:
  {{escalation_timeline_summary}}

  Total time without resolution: {{total_hours_unresolved}} hours.

FINANCIAL EXPOSURE:
  Direct cargo exposure:    {{cargo_value}}
  Customer penalty risk:    {{customer_penalty_amount}}
  Expedite/recovery costs:  {{recovery_cost_estimate}}
  Total potential exposure:  {{total_financial_exposure}}

CONTRACT REFERENCE:
Per Section {{contract_section}} of our transportation agreement dated
{{contract_date}}, {{relevant_contract_provision}}.

{{#if pattern_exists}}
PERFORMANCE PATTERN:
This is not an isolated incident. Over the past {{pattern_period}}, we have
logged {{incident_count}} exceptions on your loads, resulting in
{{total_pattern_cost}} in direct costs. Specific incidents:
  {{pattern_incident_list}}
{{/if}}

I need the following from your team by {{deadline_date}}:
  1. Full resolution of this specific shipment
  2. Written root cause analysis
  3. Corrective action plan to prevent recurrence

I value the partnership between {{our_company}} and {{carrier_name}}, and I want
to resolve this collaboratively. However, continued non-responsiveness will
require us to reassess our routing and volume commitments on the
{{origin_city_state}}–{{dest_city_state}} lane.

I am available to discuss at {{our_contact_phone}}.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}} | {{our_contact_email}}
```

---

## 8. 内部升级至供应链 VP

### 何时使用
- 财务暴露超过你的权限阈值（通常$25,000以上或客户特定触发条件）。
- 客户关系面临风险，可能需要高管对高管的沟通。
- 需要超出你权限的决策：重新招标、以溢价成本加急、授权生产线停工恢复或放弃合同条款。
- 即使不需要 VP 行动，也需要 VP 知悉——重大异常不应成为意外。

### 语气指导
简短且结构化。你的 VP 不需要叙事——他们需要数字、暴露、你已经做了什么以及你需要他们做什么。先说决策或知悉事项。使用要点。这是内部运营简报，不是客户沟通。

### 不要说的话
- 不要评论——"承运商太差了"毫无价值。陈述事实。
- 不要埋没财务数字。它应该在前三行。
- 不要只提问题不给建议方案。
- 不要在未穷尽你权限内升级步骤的情况下发送此邮件。

### 主题行

```
[ACTION REQUIRED] Exception — {{customer_name}} PO {{po_number}} | ${{financial_exposure}} Exposure
```

### 正文

```
{{vp_name}},

Flagging an active exception that requires {{your_awareness / your_decision}}.

BOTTOM LINE:
  Customer:          {{customer_name}}
  Shipment:          PO {{po_number}} / PRO {{pro_number}}
  Exception Type:    {{exception_type}}
  Financial Exposure: ${{financial_exposure}}
  Customer Risk:     {{customer_risk_level}} — {{customer_risk_description}}

SITUATION:
  {{two_to_three_sentence_summary}}

WHAT I HAVE DONE:
  - {{action_taken_1}}
  - {{action_taken_2}}
  - {{action_taken_3}}

WHAT I NEED FROM YOU:
  {{decision_or_action_needed}}

  Options:
    A. {{option_a}} — Cost: ${{option_a_cost}} | Timeline: {{option_a_timeline}}
    B. {{option_b}} — Cost: ${{option_b_cost}} | Timeline: {{option_b_timeline}}

  My recommendation: Option {{recommended_option}} because {{rationale}}.

I need a decision by {{decision_deadline}} to execute the recovery plan.

—{{our_contact_name}}
```

---

## 9. 索赔提交附函

### 何时使用
- 已决定向承运商提交正式货运索赔。
- 所有支持文件已收集（BOL、POD、检验报告、照片、发票、装箱单）。
- 索赔在提交窗口内发送（Carmack Amendment 下州际运输为9个月；州内或经纪货运请查阅州法或合同）。

### 语气指导
正式且精确。这是一份法律文件。不带情绪、不带叙述、不带关系语言。陈述事实，引用适用法律，列出随附文件，要求付款。每项陈述都应有证据支撑。使用承运商的法定名称和 MC 号码，而非其 DBA 或销售联系人姓名。

### 不要说的话
- 不要评论承运商的服务或你的不满。
- 不要包含超出可证明损失金额的诉求——后果性损害需要单独分析和法律审查。
- 不要遗漏提交日期或索赔金额——这些是管辖权要求。
- 不要引用和解讨论或口头认错。

### 主题行

```
Formal Freight Claim — PRO {{pro_number}} | Claim Amount: ${{claim_amount}}
```

### 正文

```
                                              {{current_date}}

VIA EMAIL AND CERTIFIED MAIL

{{carrier_legal_name}}
{{carrier_claims_address}}
MC-{{carrier_mc}} / DOT-{{carrier_dot}}

Attn: Claims Department

RE:   Formal Freight Claim
      PRO Number:       {{pro_number}}
      BOL Number:       {{bol_number}}
      Ship Date:        {{ship_date}}
      Origin:           {{origin_city_state}}
      Destination:      {{dest_city_state}}
      Our Reference:    {{our_claim_ref}}
      Claim Amount:     ${{claim_amount}}

Dear Claims Department:

{{our_company}} hereby files this formal claim for {{claim_type}} against
{{carrier_legal_name}} pursuant to the Carmack Amendment, 49 U.S.C. § 14706,
and applicable regulations at 49 C.F.R. Part 370.

FACTS:

On {{ship_date}}, {{our_company}} tendered {{piece_count}} of {{commodity}},
weighing {{weight}}, to {{carrier_legal_name}} at {{origin_facility}},
{{origin_city_state}}, for transportation to {{dest_facility}},
{{dest_city_state}}, under BOL {{bol_number}}.

{{claim_facts_paragraph}}

CLAIMED AMOUNT:

The total claimed amount is ${{claim_amount}}, computed as follows:

  {{claim_calculation_line_items}}

  Total: ${{claim_amount}}

This amount represents the {{value_basis}} of the goods at the time and place
of shipment, supported by the enclosed invoice documentation.

ENCLOSED DOCUMENTATION:

  1. Bill of Lading (BOL {{bol_number}})
  2. Delivery receipt / Proof of Delivery with consignee notations
  3. {{inspection_report_description}}
  4. Photographs of {{photo_description}}
  5. Commercial invoice(s) — Invoice No. {{invoice_numbers}}
  6. Packing list
  7. Shipper's certificate of value / weight
  {{#if additional_documents}}
  8. {{additional_documents}}
  {{/if}}

DEMAND:

{{our_company}} demands payment of ${{claim_amount}} within thirty (30) days
of receipt of this claim, per 49 C.F.R. § 370.9. In the alternative, we
request written acknowledgment within thirty (30) days and final disposition
within one hundred twenty (120) days, as required by regulation.

Please direct all claim correspondence to:

  {{our_contact_name}}
  {{our_contact_title}}
  {{our_company}}
  {{our_claims_address}}
  {{our_contact_email}}
  {{our_contact_phone}}

  Claim Reference: {{our_claim_ref}}

{{our_company}} reserves all rights and remedies available under applicable
law, including the right to pursue this claim in a court of competent
jurisdiction if not resolved within the regulatory timeframe.

Respectfully,


{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
```

---

## 10. 和解谈判回复（接受）

### 何时使用
- 承运商已提出和解金额，你已决定接受。
- 和解金额已获内部批准（检查你的权限级别——部分和解通常需要管理层签字）。
- 你准备结案并释放承运商在此货物上的进一步责任。

### 语气指导
专业且结论性。你在了结一项商业事务，不是在帮承运商的忙。清晰确认确切条款——金额、付款方式、时间线和释放范围。不要对和解表示感谢或暗示金额慷慨。这是商业解决方案。

### 不要说的话
- 不要说"感谢您慷慨的提议"——你是在接受公平赔偿，不是接受馈赠。
- 不要对释放范围留下任何模糊——指定 PRO、BOL 和索赔参考号。
- 未经法律审查，不要同意保密条款或宽泛的释放。
- 不要口头接受——始终书面确认。

### 主题行

```
Claim Settlement Acceptance — PRO {{pro_number}} | Claim {{our_claim_ref}}
```

### 正文

```
{{carrier_claims_contact}},

This letter confirms {{our_company}}'s acceptance of the settlement offer
received on {{offer_date}} regarding the following claim:

  PRO Number:     {{pro_number}}
  BOL Number:     {{bol_number}}
  Our Reference:  {{our_claim_ref}}
  Your Reference: {{claim_number}}

SETTLEMENT TERMS:

  Settlement Amount: ${{settlement_amount}}
  Payment Method:    {{payment_method}}
  Payment Due:       Within {{payment_days}} business days of this acceptance
  Scope of Release:  Full and final settlement of all claims arising from PRO
                     {{pro_number}} / BOL {{bol_number}} for the shipment of
                     {{commodity}} from {{origin_city_state}} to
                     {{dest_city_state}} on {{ship_date}}

Upon receipt of ${{settlement_amount}}, {{our_company}} releases
{{carrier_legal_name}} (MC-{{carrier_mc}}) from any further liability related
to the above-referenced shipment.

This release does not extend to any other shipments, claims, or obligations
between the parties.

Please remit payment to:

  {{our_company}}
  {{our_remittance_address}}
  {{our_payment_details}}

  Reference: {{our_claim_ref}}

Please confirm receipt of this acceptance and expected payment date.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}} | {{our_contact_email}}
```

---

## 11. 和解谈判回复（拒绝）

### 何时使用
- 承运商的和解报价低于你有记录的损失金额，你有证据支持更高的索赔。
- 你准备以有文件支撑的具体金额提出反报价。
- 你已审查了承运商降低报价的陈述理由，可以回应其异议。

### 语气指导
坚定且基于证据。你不是被低价冒犯了——你在纠正不准确的估值。逐步审视他们的理由，指出错误之处，将你的反报价锚定在具体证据上。为解决留门，但明确说明有记录的损失支持你的立场。

### 不要说的话
- 不要说"这是侮辱"或对报价金额表达情绪。
- 不要在提出反报价的同一句话中威胁诉讼——这与和解姿态矛盾。
- 如果他们的框架不正确，不要接受他们的框架（如他们对新货折旧或排除了有记录的项目）。
- 不要在没有支撑文件的情况下提出反报价——附上证据。

### 主题行

```
Claim {{our_claim_ref}} — Settlement Offer Declined | Counter-Offer Enclosed
```

### 正文

```
{{carrier_claims_contact}},

We have reviewed your settlement offer of ${{offered_amount}} dated
{{offer_date}} for the following claim:

  PRO Number:     {{pro_number}}
  BOL Number:     {{bol_number}}
  Our Reference:  {{our_claim_ref}}
  Your Reference: {{claim_number}}
  Original Claim: ${{claim_amount}}

We are unable to accept this offer. Our original claim of ${{claim_amount}} is
supported by documented evidence, and the offered amount does not adequately
compensate for the loss.

RESPONSE TO YOUR STATED BASIS FOR REDUCTION:

{{carrier_reduction_reason_1}}:
  Our response: {{our_response_1}}
  Supporting documentation: {{supporting_doc_1}}

{{carrier_reduction_reason_2}}:
  Our response: {{our_response_2}}
  Supporting documentation: {{supporting_doc_2}}

{{#if carrier_reduction_reason_3}}
{{carrier_reduction_reason_3}}:
  Our response: {{our_response_3}}
  Supporting documentation: {{supporting_doc_3}}
{{/if}}

COUNTER-OFFER:

{{our_company}} is willing to settle this claim for ${{counter_offer_amount}},
which reflects {{counter_offer_basis}}.

This counter-offer is supported by the following enclosed documentation:
  {{counter_offer_documentation_list}}

We request your response within {{response_days}} business days. We remain open
to resolving this matter directly and would welcome a call to discuss if that
would be productive.

If we are unable to reach a fair resolution, we will need to evaluate our
options under 49 U.S.C. § 14706, which provides a two-year statute of
limitations from the date of claim denial.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}} | {{our_contact_email}}
```

---

## 12. 解决后总结

### 何时使用
- 异常已完全解决——货物已交付、索赔已和解或损失已补救。
- 分发给内部利益相关方：运营、客户管理、财务和承运商采购。
- 这成为异常的永久记录，并用于承运商评分卡审查。

### 语气指导
中立且分析性。这是事后复盘，不是投诉。陈述发生了什么、花了多少、做了什么以及应该改变什么。对经验教训要具体——"我们需要更好地沟通"这种模糊说法毫无价值。推荐具体的流程变更。

### 不要说的话
- 不要对个人归咎——聚焦流程和系统失误。
- 即使索赔有利解决，也不要省略财务影响——真实成本包括员工时间、加急费用和客户商誉。
- 不要跳过"预防"部分。如果你无法推荐预防步骤，说明原因。

### 主题行

```
[CLOSED] Exception Summary — {{customer_name}} / PRO {{pro_number}} | {{exception_type}}
```

### 正文

```
EXCEPTION POST-RESOLUTION SUMMARY
====================================

Exception Reference:  {{our_claim_ref}}
Status:               CLOSED — {{closure_date}}
Prepared by:          {{our_contact_name}}
Distribution:         {{distribution_list}}

1. SHIPMENT DETAILS
   Customer:       {{customer_name}}
   PO:             {{po_number}}
   PRO:            {{pro_number}}
   BOL:            {{bol_number}}
   Carrier:        {{carrier_name}} (MC-{{carrier_mc}} / SCAC: {{carrier_scac}})
   Route:          {{origin_city_state}} → {{dest_city_state}}
   Ship Date:      {{ship_date}}
   Commodity:      {{commodity}}
   Weight/Pieces:  {{weight}} / {{piece_count}}

2. EXCEPTION SUMMARY
   Type:            {{exception_type}}
   Discovered:      {{exception_date}}
   Root Cause:      {{confirmed_root_cause}}
   Description:     {{exception_narrative}}

3. TIMELINE
   {{exception_timeline}}

4. FINANCIAL IMPACT
   Cargo Loss/Damage:              ${{cargo_loss_amount}}
   Freight Charges (original):     ${{freight_charge}}
   Expedite / Recovery Costs:      ${{recovery_costs}}
   Customer Penalties / Credits:   ${{customer_penalties}}
   Internal Labor (est.):          ${{internal_labor_cost}}
   ─────────────────────────────────
   Total Cost of Exception:        ${{total_exception_cost}}

   Claim Filed:                    ${{claim_amount}}
   Settlement Received:            ${{settlement_amount}}
   Net Unrecovered Loss:           ${{net_loss}}

5. CUSTOMER IMPACT
   {{customer_impact_summary}}
   Customer Satisfaction Status:   {{csat_status}}
   Relationship Risk:              {{relationship_risk_level}}

6. CARRIER SCORECARD IMPACT
   Carrier:                {{carrier_name}}
   Incidents (trailing 12 months): {{trailing_12_incident_count}}
   On-Time Rate Impact:            {{ot_rate_impact}}
   Claims Ratio Impact:            {{claims_ratio_impact}}
   Recommended Action:             {{carrier_recommended_action}}

7. LESSONS LEARNED
   {{lesson_1}}
   {{lesson_2}}
   {{lesson_3}}

8. PROCESS IMPROVEMENTS
   {{improvement_1}} — Owner: {{owner_1}} — Due: {{due_date_1}}
   {{improvement_2}} — Owner: {{owner_2}} — Due: {{due_date_2}}
   {{improvement_3}} — Owner: {{owner_3}} — Due: {{due_date_3}}

====================================
Filed in: {{document_management_location}}
```

---

## 13. 承运商绩效警告

### 何时使用
- 承运商有记录的异常模式超过可接受阈值（如准时率低于90%、索赔率高于2%、一个季度内多起 OS&D 事件）。
- 你有 TMS 或评分卡数据支持此警告。
- 这是正式通知——不是电话上的随口提醒。它创建书面记录，支持未来的路线决策或合同重新谈判。
- 在模式建立后发送（通常3起以上事件或一个季度低于阈值绩效），而非一次糟糕的货物之后。

### 语气指导
数据先行且不带情绪。让数字说话。你不是在生气——你是在管理供应商绩效的供应链专业人士。陈述期望，展示差距，清晰定义后果。为纠正行动留出空间——你希望他们改进，而非仅仅感到被惩罚。

### 不要说的话
- 不要人身攻击——"你们的司机不在乎"不专业。
- 不要发出你未准备好执行的最终通牒。
- 不要在活跃异常期间发送——等当前问题解决后再处理模式。
- 不要将此与新货物招标或正面反馈混合——这会稀释信息。

### 主题行

```
Carrier Performance Notice — {{carrier_name}} (MC-{{carrier_mc}}) | {{performance_period}}
```

### 正文

```
{{carrier_contact_name}},
{{carrier_contact_title}}
{{carrier_name}}

This letter serves as a formal performance notice regarding {{carrier_name}}'s
service on {{our_company}} freight during the period {{performance_period}}.

PERFORMANCE SUMMARY:

  Metric                  Target     Actual     Variance
  ─────────────────────   ────────   ────────   ────────
  On-Time Delivery        {{ot_target}}   {{ot_actual}}   {{ot_variance}}
  Claims Ratio            {{claims_target}}   {{claims_actual}}   {{claims_variance}}
  Tender Acceptance       {{ta_target}}   {{ta_actual}}   {{ta_variance}}
  Check-Call Compliance   {{cc_target}}   {{cc_actual}}   {{cc_variance}}
  OS&D Incidents          {{osd_target}}   {{osd_actual}}   {{osd_variance}}

SPECIFIC INCIDENTS:

  {{incident_date_1}} | PRO {{incident_pro_1}} | {{incident_type_1}} | ${{incident_cost_1}}
  {{incident_date_2}} | PRO {{incident_pro_2}} | {{incident_type_2}} | ${{incident_cost_2}}
  {{incident_date_3}} | PRO {{incident_pro_3}} | {{incident_type_3}} | ${{incident_cost_3}}
  {{#if more_incidents}}
  ({{additional_incident_count}} additional incidents detailed in attachment)
  {{/if}}

  Total Exception Cost ({{performance_period}}): ${{total_period_exception_cost}}

VOLUME CONTEXT:

During this period, {{carrier_name}} handled {{total_loads}} loads for
{{our_company}} representing ${{total_freight_spend}} in freight spend. You are
currently ranked {{carrier_rank}} of {{total_carriers}} carriers in our network
for the lanes you serve.

EXPECTATIONS:

To maintain current volume and lane assignments, we require:
  1. {{expectation_1}}
  2. {{expectation_2}}
  3. {{expectation_3}}

We require a written corrective action plan within {{corrective_plan_days}}
business days of this notice.

CONSEQUENCES:

If performance does not improve to target levels within {{improvement_period}}:
  - {{consequence_1}}
  - {{consequence_2}}
  - {{consequence_3}}

We are committed to working with carrier partners who meet our service
standards. I welcome a call to discuss this notice and develop a corrective plan
together.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}} | {{our_contact_email}}

CC: {{internal_cc_list}}
```

---

## 14. 客户致歉及解决方案

### 何时使用
- 重大异常已完全解决，客户已收到货物、替换品或贷记。
- 异常严重到需要正式确认，超出已发送的运营更新。
- 你想巩固关系并展示正在实施系统性改进——而非一次性修补。

### 语气指导
真诚且具体。好的致歉点明具体影响、描述已做的工作、承诺具体预防步骤。它不卑躬屈膝或过度道歉——客户是商业伙伴，不是受害者。它应该让人感觉是由理解其业务的高级专业人士撰写，而非客服脚本。以前瞻性基调结尾。

### 不要说的话
- 不要使用"对造成的不便深表歉意"——点明实际影响。"我知道两天的延误迫使你们团队重新安排零售陈列"效果好十倍。
- 不要指责承运商或任何第三方。你拥有客户关系。
- 不要做出你无法兑现的承诺。"这绝不会再发生"不可信。"以下是我们正在实施的三项具体步骤"才可信。
- 不要把这变成销售推销或过渡到新服务。聚焦解决方案。
- 不要在解决当天发送——等1-2个工作日，让客户确认解决方案令人满意。

### 主题行

```
PO {{po_number}} — Resolution Confirmed and Path Forward
```

### 正文

```
{{customer_contact}},

Now that PO {{po_number}} has been fully resolved, I want to close the loop
personally.

WHAT HAPPENED:
On {{exception_date}}, {{exception_summary_one_sentence}}. This resulted in
{{specific_customer_impact}}.

WHAT WE DID:
  - {{resolution_action_1}}
  - {{resolution_action_2}}
  - {{resolution_action_3}}
  - Final resolution: {{final_resolution_summary}}

WHAT WE ARE CHANGING:
I do not want to repeat what you experienced. Here are the specific steps we
are putting in place:

  1. {{prevention_step_1}}
  2. {{prevention_step_2}}
  3. {{prevention_step_3}}

{{#if financial_goodwill}}
GOODWILL:
{{financial_goodwill_description}}
{{/if}}

I value your business and I value the trust your team places in us. I take it
personally when we fall short of the standard you expect.

If you have any remaining concerns about this shipment or anything else, I am
always available at {{our_contact_phone}}.

Regards,
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_phone}} | {{our_contact_email}}
```

---

## AI 智能体使用说明

**模板选择：** 将模板匹配到受众（承运商运营、承运商高管、客户、内部）和异常生命周期阶段（发现、升级、索赔、解决、事后复盘）。不确定时，从适合已过时间和严重程度的最低升级模板开始。

**变量替换：** 所有 `{{变量}}` 必须在发送前替换。如果值未知，不要保留占位符——要么获取信息，要么删除该部分并注明后续补充。

**条件段落：** 包裹在 `{{#if}}...{{/if}}` 中的段落是可选的，仅在条件适用时包含（如 VP 升级模板中的 `{{#if pattern_exists}}`）。

**语气校准：** 每个模板的语气指导反映了该受众和场景的适当语域。不要为了"更友好"而弱化升级模板，也不要为了"更强硬"而硬化客户模板——校准是经过深思熟虑的。

**法律免责声明：** 索赔提交附函引用了 Carmack Amendment（49 U.S.C. § 14706），适用于州际汽车承运商运输。对于经纪货运、国际运输或州内运输，发送前请验证适用的法律框架。不确定时，转交法律审查。

**时间要求：**
- 初始承运商通知：异常发现后1小时内。
- 客户主动更新：确认影响后2小时内，或客户下一个工作日开始前——以先到者为准。
- 升级至客户经理：4小时无回复后（紧急为2小时）。
- 升级至 VP/总监：客户经理12-24小时未解决后。
- 索赔提交：文件整理完毕后尽快，在9个月法定窗口内。
- 解决后总结：结案后5个工作日内。
- 绩效警告：模式记录后，不在活跃异常期间。
- 客户致歉：解决方案确认后1-2个工作日。
