# 沟通模板 — 质量与不合格品管理

> **参考类型:** 第三层 — 在编写或审查质量沟通文档时按需加载。
>
> **使用说明:** 每个模板都包含 `{{双花括号}}` 形式的变量占位符，可直接替换使用。模板按受众和场景组织。请选择与场景匹配的模板，替换变量，参考语气指导，然后发送。

---

## 目录

1. [不合格品报告通知（内部）](#1-不合格品报告通知内部)
2. [MRB 处置记录](#2-mrb-处置记录)
3. [供应商纠正措施请求（CAR）](#3-供应商纠正措施请求car)
4. [CAPA 启动记录](#4-capa-启动记录)
5. [CAPA 有效性评审](#5-capa-有效性评审)
6. [审核发现项响应](#6-审核发现项响应)
7. [客户质量通知](#7-客户质量通知)
8. [供应商审核报告摘要](#8-供应商审核报告摘要)
9. [质量警报（内部）](#9-质量警报内部)
10. [管理评审质量摘要](#10-管理评审质量摘要)
11. [监管机构响应（FDA 483 表格）](#11-监管机构响应fda-483-表格)

---

## 变量参考

跨模板使用的常用变量：

| 变量 | 描述 | 示例 |
|---|---|---|
| `{{ncr_number}}` | 不合格品报告编号 | `NCR-2025-0412` |
| `{{capa_number}}` | CAPA 记录编号 | `CAPA-2025-0023` |
| `{{scar_number}}` | 供应商纠正措施请求编号 | `SCAR-2025-0089` |
| `{{part_number}}` | 零件号与版本 | `7832-A Rev D` |
| `{{part_description}}` | 零件描述 | `Shaft, Output — Titanium` |
| `{{lot_number}}` | 批次或批号 | `LOT-2025-4471` |
| `{{po_number}}` | 采购订单号 | `PO-2025-08832` |
| `{{wo_number}}` | 工单号 | `WO-2025-1104` |
| `{{serial_numbers}}` | 受影响的序列号（如适用） | `SN-10042 through SN-10089` |
| `{{supplier_name}}` | 供应商公司名称 | `Precision Castings Corp.` |
| `{{supplier_contact}}` | 供应商质量联系人姓名 | `Maria Gonzalez, Quality Manager` |
| `{{customer_name}}` | 客户公司名称 | `MedTech Instruments Inc.` |
| `{{customer_contact}}` | 客户质量联系人姓名 | `David Chen, Supplier Quality Engineer` |
| `{{spec_requirement}}` | 违反的规范和要求 | `Drawing 7832-A Rev D, Dim A: 12.45 ±0.05mm` |
| `{{actual_values}}` | 不合格品的测量值 | `12.52mm, 12.54mm, 12.51mm (3 of 50 sample)` |
| `{{quantity_affected}}` | 受影响零件数量 | `18 of 500 pieces inspected` |
| `{{quantity_total}}` | 批次总数量 | `2,000 pieces` |
| `{{defect_description}}` | 不合格品描述 | `OD exceeds USL by 0.02-0.04mm` |
| `{{containment_status}}` | 当前遏制措施 | `Material quarantined in MRB cage, Bay 3` |
| `{{our_quality_contact}}` | 内部质量联系人 | `Sarah Thompson, Quality Engineer` |
| `{{our_quality_email}}` | 内部质量邮箱 | `sthompson@company.com` |
| `{{our_quality_phone}}` | 内部质量联系电话 | `(555) 234-5678` |
| `{{our_company}}` | 我方公司名称 | `Advanced Manufacturing Solutions` |
| `{{date_discovered}}` | 发现不合格品的日期 | `2025-03-15` |
| `{{response_deadline}}` | 响应截止日期 | `2025-03-25 (10 business days)` |
| `{{severity_level}}` | NCR 严重程度分类 | `Major — Dimensional non-conformance on key characteristic` |

---

## 1. 不合格品报告通知（内部）

### 何时使用
- 在来料检验、过程检验或最终检验中发现不合格品
- 向受影响部门（制造、工程、采购、计划）发出初步通知
- 物料已被隔离；待处置

### 语气指导
客观、直接。内部团队需要了解发生了什么、范围多大、当前直接影响是什么。不归咎、不猜测——只列数据。提供足够的细节供工程部门开始评估，并供计划部门评估生产影响。

### 模板

**主题:** `{{ncr_number}}: {{part_number}} — {{defect_description}}`

**收件人:** 制造工程、生产计划、采购（如涉及供应商）、质量经理
**抄送:** 质量文件

---

**不合格品报告：{{ncr_number}}**

**发现日期:** {{date_discovered}}
**发现人:** {{inspector_name}}，{{inspection_stage}}（来料 / 过程 / 最终）
**零件号:** {{part_number}} — {{part_description}}
**批次/批号:** {{lot_number}} | 工单: {{wo_number}} | 采购订单: {{po_number}}（如为来料）

**不合格品描述：**
{{defect_description}}

**规范要求:** {{spec_requirement}}
**实际测量值:** {{actual_values}}
**受影响数量:** {{quantity_affected}} / {{quantity_total}} 总批次

**遏制状态：**
{{containment_status}}

**初始范围评估：**
- [ ] 已检查同一供应商/生产批次中的其他批次：{{scope_check_result}}
- [ ] 已识别含此物料的在制品：{{wip_status}}
- [ ] 已识别含此物料的成品：{{fg_status}}
- [ ] 已发运的下游客户货物中含此物料：{{shipped_status}}

**生产影响：**
{{production_impact_summary}}（例如："3 号产线正在等待 WO-2025-1104 的此物料；如在星期四前未完成处置，将影响 2 天"）

**请求行动：**
请工程部门在 {{disposition_deadline}} 前完成功能影响评审。
MRB 会议已安排：{{mrb_date_time}}。

**质量联系人:** {{our_quality_contact}} | {{our_quality_email}} | {{our_quality_phone}}

---

## 2. MRB 处置记录

### 何时使用
- 记录物料评审委员会的处置决定
- 所有非简单报废的 NCR 处置均需填写
- 审计追溯文件；审核员将审查此文档

### 语气指导
正式、精确、完整。这是一份受控文件。每个字段都必须填写。工程依据必须技术合理且具体——不能写"经工程评审合格"，而要给出引用功能要求的详细原理。

### 模板

**MRB 处置记录**

| 字段 | 值 |
|---|---|
| NCR 编号 | {{ncr_number}} |
| MRB 日期 | {{mrb_date}} |
| 零件号/版本 | {{part_number}} |
| 零件描述 | {{part_description}} |
| 批次/批号 | {{lot_number}} |
| 受影响数量 | {{quantity_affected}} |
| 不合格情况 | {{defect_description}} |
| 违反的规范 | {{spec_requirement}} |
| 实际测量值 | {{actual_values}} |

**处置决定：** ☐ 照用 ☐ 返工 ☐ 返修 ☐ 退回供应商 ☐ 报废

**工程依据（照用和返修必填）：**
{{engineering_justification}}

示例："12.52mm 的 OD 测量值（USL 12.50mm）超出图纸公差 0.02mm。根据工程分析 EA-2025-0034，该尺寸与配对零件 7833-B 上的孔径 12.60 +0.05/-0.00mm 配合。最差情况叠加公差下的最小间隙（轴 12.52mm，孔 12.60mm）为 0.08mm。装配要求 DWG 100-ASSY-Rev C 规定最小间隙 0.05mm。0.08mm 的间隙满足功能要求。对形式、装配或功能无影响。"

**风险评估（安全关键零件必填）：**
{{risk_assessment_reference}}（例如："根据 ISO 14971 风险评估 RA-2025-0012，风险等级可接受——严重度[轻微]、概率[极低]"）

**客户批准（航空航关照用/返修必填）：**
☐ 无需（标准/非受控） ☐ 已申请 — 参考：{{customer_approval_ref}} ☐ 已批准 — 日期：{{approval_date}} ☐ 已拒绝

**成本影响：**
| 项目 | 金额 |
|---|---|
| 报废成本 | {{scrap_cost}} |
| 返工人工 | {{rework_cost}} |
| 复检 | {{reinspect_cost}} |
| 紧急/替换 | {{expedite_cost}} |
| **NCR 总成本** | **{{total_cost}}** |

**是否需要 CAPA：** ☐ 是 — {{capa_number}} ☐ 否 — 理由：{{no_capa_rationale}}

**MRB 参会人员与签名：**

| 姓名 | 部门 | 签名 | 日期 |
|---|---|---|---|
| {{quality_rep}} | 质量工程 | | {{date}} |
| {{engineering_rep}} | 设计/产品工程 | | {{date}} |
| {{manufacturing_rep}} | 制造工程 | | {{date}} |
| {{other_rep}} | {{other_dept}} | | {{date}} |

---

## 3. 供应商纠正措施请求（CAR）

### 何时使用
- 来料物料上发现的重大不合格品，可追溯至供应商
- 同一供应商反复出现轻微不合格品（90 天内 3 次及以上）
- 供应商升级一级（SCAR 签发）

### 语气指导
专业、具体、结构化。提供供应商调查所需的全部数据。明确响应格式和时间表的预期。不要指责——陈述事实并要求调查。供应商的响应意愿和响应质量将告诉您这是可修复的问题还是系统性问题。

### 不可使用的措辞
- 在首次 CAR 中不要威胁从 ASL 中移除（升级措辞留给二级及以上）
- 不要猜测根本原因——那是供应商的工作
- 不要包含内部财务影响数字（此阶段供应商无需了解您的下游成本）

### 模板

**主题:** `SCAR-{{scar_number}}: 采购订单# {{po_number}} 上的不合格品 — 请于 {{response_deadline}} 前回复`

**收件人:** {{supplier_contact}}，{{supplier_name}}
**抄送:** {{our_quality_contact}}，采购员

---

**供应商纠正措施请求**

**SCAR 编号:** {{scar_number}}
**签发日期:** {{date_issued}}
**响应截止:** {{response_deadline}}（含遏制措施 + 初步根本原因的初始响应）
**完整纠正措施计划截止:** {{full_response_deadline}}（30 个日历日）

**供应商信息：**
- 供应商: {{supplier_name}}
- 供应商代码: {{supplier_code}}
- 联系人: {{supplier_contact}}

**不合格品详情：**
- 零件号: {{part_number}} — {{part_description}}
- 采购订单号: {{po_number}}
- 批次/批号: {{lot_number}}
- 收货数量: {{quantity_total}}
- 不合格数量: {{quantity_affected}}
- 收货日期: {{date_received}}
- 不合格品发现日期: {{date_discovered}}

**规范要求：**
{{spec_requirement}}

**实际结果：**
{{actual_values}}

**随附的支持文件：**
- [ ] 含测量数据的检验报告
- [ ] 不合格物料的照片
- [ ] 标注受影响尺寸/要求的图纸摘录
- [ ] 本批次的合格证明书副本

**对我方运营的影响：**
{{impact_summary}}（例如："生产线已暂停，等待处置。预计影响客户交付进度 3 天。"）

**要求的响应（使用 8D 格式或同等格式）：**
1. **遏制措施** — 立即采取行动保护我方库存及可能收到同批次物料的其他客户。确认同一生产批次的其他批次是否可能受到影响。
2. **根本原因分析** — 我们要求严格的根本原因调查，而非表面解释。"操作员失误"或"检验漏检"不是可接受的根本原因。识别导致此不合格品的系统性流程或系统故障。
3. **纠正措施** — 针对已验证的根本原因采取具体、可衡量的行动。包括实施日期和责任人。
4. **有效性验证计划** — 您将如何以及何时验证纠正措施的有效性？

**不合格物料的处置：**
☐ 退回供应商 — 请提供 RMA 编号和运输说明
☐ 在我方处分选 — 分选人工费的贷项通知单将随后开具
☐ 在我方处报废 — 物料价值的贷项通知单将随后开具

**问题联系人：**
{{our_quality_contact}} | {{our_quality_email}} | {{our_quality_phone}}

---

## 4. CAPA 启动记录

### 何时使用
- 基于既定触发标准正式启动 CAPA
- 记录触发事件、范围、团队分配和初始时间表

### 语气指导
结构化且客观。启动记录为整个 CAPA 设定范围和预期。此处的模糊性会导致后续范围蔓延或调查不完整。请具体说明触发 CAPA 的原因及预期结果。

### 模板

**纠正与预防措施记录**

| 字段 | 值 |
|---|---|
| CAPA 编号 | {{capa_number}} |
| 启动日期 | {{date_initiated}} |
| 类型 | ☐ 纠正 ☐ 预防 |
| 来源 | ☐ NCR ☐ 客户投诉 ☐ 审核发现 ☐ 趋势分析 ☐ 现场失效 ☐ 其他：{{other_source}} |
| 来源参考 | {{source_references}}（例如：NCR-2025-0412, NCR-2025-0398, NCR-2025-0456） |
| 优先级 | ☐ 关键（安全/法规） ☐ 高（客户影响） ☐ 中（内部） ☐ 低（改进） |

**问题陈述：**
{{problem_statement}}

示例："零件 7832-A Rev D 上反复出现尺寸不合格——孔径超出公差（>USL 12.50mm）。过去 60 天内发生三次 NCR（NCR-2025-0398、-0412、-0456），涉及三个不同生产批次。迄今总报废成本：14,200 美元。尚未确认对客户的影响，但根据检验抽样率存在漏检风险。"

**范围：**
- 受影响产品：{{products_affected}}
- 受影响工序：{{processes_affected}}
- 地点：{{locations_affected}}
- 期间：{{time_period}}

**团队分配：**

| 角色 | 姓名 | 部门 |
|---|---|---|
| CAPA 负责人 | {{capa_owner}} | {{owner_dept}} |
| 首席调查员 | {{investigator}} | {{investigator_dept}} |
| 团队成员 | {{team_members}} | {{team_depts}} |
| 管理发起人 | {{sponsor}} | {{sponsor_dept}} |

**时间表：**

| 阶段 | 目标日期 |
|---|---|
| 根本原因调查完成 | {{rca_target}} |
| 纠正措施计划批准 | {{plan_target}} |
| 实施完成 | {{implementation_target}} |
| 有效性验证开始 | {{verification_start}} |
| 有效性验证完成 | {{verification_end}} |
| CAPA 关闭目标 | {{closure_target}} |

**初步遏制措施（如适用）：**
{{containment_actions}}

---

## 5. CAPA 有效性评审

### 何时使用
- 在有效性监测期结束时（通常为实施后 90 天）
- 记录有效性证据及关闭/延期决定

### 语气指导
数据驱动且结论性。有效性评审是 CAPA 通过成功证据关闭或通过失败证据重新开启的关键节点。审核员会专门审查有效性证据——必须量化，并与原始问题陈述相关联。

### 模板

**CAPA 有效性评审**

| 字段 | 值 |
|---|---|
| CAPA 编号 | {{capa_number}} |
| 原始问题 | {{problem_statement}} |
| 根本原因 | {{verified_root_cause}} |
| 已实施的纠正措施 | {{corrective_actions}} |
| 实施日期 | {{implementation_date}} |
| 监测期 | {{monitoring_start}} 至 {{monitoring_end}} |

**实施验证：**
- [ ] 作业指导/程序已更新：版本 {{rev}} 生效日期 {{date}}
- [ ] 人员已培训：{{training_records_ref}}
- [ ] 设备/工装已安装并验证：{{validation_ref}}
- [ ] FMEA / 控制计划已更新：{{fmea_ref}}
- [ ] 供应商纠正措施已验证：{{scar_ref}}

**有效性数据：**

| 指标 | 基线（CAPA 前） | 目标 | 实际（监测期） | 结果 |
|---|---|---|---|---|
| {{metric_1}} | {{baseline_1}} | {{target_1}} | {{actual_1}} | ☐ 通过 ☐ 失败 |
| {{metric_2}} | {{baseline_2}} | {{target_2}} | {{actual_2}} | ☐ 通过 ☐ 失败 |
| 复发次数 | {{baseline_recurrence}} | 零 | {{actual_recurrence}} | ☐ 通过 ☐ 失败 |

**结论：**
☐ **CAPA 有效 — 关闭。** 所有有效性标准已达成。监测期内零复发。过程能力达到目标。
☐ **CAPA 部分有效 — 延长监测。** 已显示改进但监测期不足以得出明确结论。延长 {{extension_days}} 天。
☐ **CAPA 无效 — 重新开启。** 监测期内观察到复发。需重新调查根本原因。参见 {{reopened_investigation_ref}}。

**评审人：**

| 姓名 | 角色 | 签名 | 日期 |
|---|---|---|---|
| {{reviewer_1}} | CAPA 负责人 | | |
| {{reviewer_2}} | 质量经理 | | |

---

## 6. 审核发现项响应

### 何时使用
- 响应外部审核发现（注册机构、客户、监管机构）
- 结构适用于 ISO 审核 NCR、客户审核 CAR 和 FDA 483 响应（按模板 11 进行修改）

### 语气指导
客观、负责、面向解决方案。接受发现项（即使您不同意解读——单独讨论解读，不要在纠正措施响应中讨论）。展示您理解要求的目的，而不仅仅是字面意思。审核员看重自我意识和系统性思维。

### 模板

**审核发现项纠正措施响应**

**审核:** {{audit_type}}（例如：ISO 9001 监督审核、客户审核、IATF 16949 再认证）
**审核员/机构:** {{auditor_name}}，{{audit_organization}}
**审核日期:** {{audit_dates}}
**发现编号:** {{finding_number}}
**发现分类:** ☐ 重大不符合 ☐ 轻微不符合 ☐ 观察项/OFI

**发现陈述：**
{{finding_statement}}

**引用的标准条款:** {{standard_clause}}（例如：ISO 9001:2015 §8.5.2, IATF 16949 §10.2.3）

**我方响应：**

**1. 确认：**
我们确认此发现项。{{brief_acknowledgment}}

**2. 根本原因分析：**
{{root_cause_analysis}}

**3. 遏制（即时采取的行动）：**
{{containment_actions}}

**4. 纠正措施：**
| 行动 | 负责人 | 目标日期 | 完成证据 |
|---|---|---|---|
| {{action_1}} | {{responsible_1}} | {{date_1}} | {{evidence_1}} |
| {{action_2}} | {{responsible_2}} | {{date_2}} | {{evidence_2}} |

**5. 范围扩展（我们是否检查了其他地方的类似差距？）：**
{{scope_extension}}

**6. 有效性验证计划：**
{{effectiveness_plan}}

**提交人:** {{responder_name}}，{{responder_title}}
**日期:** {{submission_date}}

---

## 7. 客户质量通知

### 何时使用
- 在已发运给客户的产品上发现不合格品
- 主动通知——客户应先从您处听到此事，而不是自行发现

### 语气指导
透明、行动导向、结构化。开头就说明您已知和已做的事情（遏制），而不是找借口。提供客户识别和隔离库存中受影响产品所需的具体可追溯性数据。客户将根据您处理此通知的方式评判您的质量体系——透明和速度建立信任；拖延和模糊则摧毁信任。

### 不可使用的措辞
- 不要淡化：在您尚不知范围时不要写"发现了一个小问题"
- 不要猜测根本原因：未经核实数据不要写"我们认为这是由...引起的"
- 不要过度承诺时间表：除非您确定，不要写"这将在星期五前解决"

### 模板

**主题:** `质量通知：{{part_number}} — {{defect_description}} — 需要采取行动`

**收件人:** {{customer_contact}}，{{customer_name}}
**抄送:** {{our_quality_contact}}，客户经理

---

**客户质量通知**

**日期:** {{date}}
**我方参考:** {{ncr_number}}
**优先级:** {{priority_level}}（关键/高/标准）

尊敬的 {{customer_contact}}：

我们联系您是为了通知您我们所供物料中的一个质量问题。

**受影响产品：**
- 零件号: {{part_number}} — {{part_description}}
- 批次号: {{lot_numbers}}
- 序列号: {{serial_numbers}}（如适用）
- 发运日期: {{ship_dates}}
- 采购订单/订单参考: {{po_numbers}}
- 已发运数量: {{quantity_shipped}}

**不合格性质：**
{{defect_description_for_customer}}

**已采取的遏制措施：**
1. 我方设施的所有库存已被隔离并暂停使用
2. 已尽可能拦截运输途中的货物：{{transit_status}}
3. 我们请求您在库存中隔离以下批次：{{lots_to_quarantine}}

**建议的客户行动：**
{{recommended_customer_action}}（例如："请隔离并保留上述受影响的批次号。在我们提供处置指导之前，请勿使用此物料。"）

**调查状态：**
我们已启动调查（{{ncr_number}}），正在进行[根本原因分析/遏制分选/物料验证]。我们将在 {{next_update_date}} 前提供最新状态。

**您的直接联系人：**
{{our_quality_contact}}
{{our_quality_email}}
{{our_quality_phone}}

我们认真对待此事，并承诺在调查过程中保持完全透明。我们将至少每 {{update_frequency}} 提供一次更新，直至问题解决。

此致

{{our_quality_contact}}，{{our_quality_title}}
{{our_company}}

---

## 8. 供应商审核报告摘要

### 何时使用
- 供应商质量审核的摘要（过程、体系或产品审核）
- 分发给采购、工程和供应商质量管理
- 审核后续行动的依据

### 语气指导
客观且平衡。报告观察到的情况，包括优点和不足。如果审核报告全是否定的，则暗示审核员是在找问题而非评估能力。如果审核报告全是肯定的，则暗示审核员不够深入。摘要应让管理层对供应商的质量成熟度有清晰的了解。

### 模板

**供应商审核报告摘要**

| 字段 | 值 |
|---|---|
| 供应商 | {{supplier_name}} |
| 供应商代码 | {{supplier_code}} |
| 审核类型 | ☐ 体系 ☐ 过程 ☐ 产品 ☐ 综合 |
| 审核日期 | {{audit_dates}} |
| 审核员 | {{auditor_names}} |
| 审核依据标准 | {{standards}}（例如：ISO 9001:2015, IATF 16949, AS9100D） |
| 范围 | {{audit_scope}} |

**总体评估:** ☐ 批准 ☐ 有条件批准 ☐ 不批准

**观察到的优点：**
1. {{strength_1}}
2. {{strength_2}}
3. {{strength_3}}

**发现项：**

| # | 条款 | 发现 | 分类 |
|---|---|---|---|
| 1 | {{clause_1}} | {{finding_1}} | 重大/轻微/OFI |
| 2 | {{clause_2}} | {{finding_2}} | 重大/轻微/OFI |

**纠正措施要求：**
- 响应截止: {{car_deadline}}
- 格式: 8D 或同等格式，含根本原因分析和实施计划
- 提交至: {{submit_to}}

**建议：**
{{recommendations}}（例如："批准用于生产，但需在 6 个月内进行强制性后续审核以验证纠正措施。在验证纠正措施前，将来料检验等级提升至加严检验。"）

---

## 9. 质量警报（内部）

### 何时使用
- 紧急通知生产现场、检验和发运部门有关需要立即采取行动的质量问题
- 不合格品可能影响当前在产或待发运的产品
- 临时加强检验或遏制措施

### 语气指导
紧急、清晰、可操作。这将发给生产现场——操作员、主管、检验员。使用通俗语言。尽可能附上照片。明确具体要做什么以及要查找什么。这不是要求分析；这是立即行动的指令。

### 模板

**⚠ 质量警报 ⚠**

**警报编号:** QA-{{alert_number}}
**签发日期:** {{date_issued}}
**立即生效 — 直至撤销**

**受影响零件:** {{part_number}} — {{part_description}}
**受影响区域:** {{production_areas}}（例如："3 号产线 — CNC 车削、来料检验、最终检验、发运"）

**问题：**
{{issue_description_plain_language}}

**查找内容：**
{{what_to_look_for}}（具体、可衡量的标准，如有照片请附上）

**要求行动：**
1. {{action_1}}（例如："在放行至下一道工序前，对该零件号的所有在制品按受影响尺寸进行 100% 检验"）
2. {{action_2}}（例如："隔离并标记发现的任何不合格零件——未经质量工程授权不得报废"）
3. {{action_3}}（例如："如发现任何其他不合格零件，请立即通知质量工程：{{contact_info}}"）

**本警报生效至：** {{rescind_condition}}（例如："质量工程书面通知根本原因已得到解决并已验证"）

**签发人:** {{issuer_name}}，{{issuer_title}}

---

## 10. 管理评审质量摘要

### 何时使用
- 月度或季度管理评审的质量绩效输入
- 总结关键指标、重大质量事件、CAPA 状态和质量成本

### 语气指导
高管层面。开头就给出一句话——质量绩效是在改善、稳定还是恶化？然后提供支持数据。管理者需要了解趋势方向和业务影响，而不是个别 NCR 细节。使用图表和表格；减少叙述。

### 模板

**质量管理评审 — {{review_period}}**

**编制人:** {{quality_manager}}
**日期:** {{date}}

**执行摘要：**
{{executive_summary}}（2-3 句话：整体质量趋势、最重大事件、需要的关键行动）

**关键绩效指标：**

| 指标 | 目标 | 上期 | 本期 | 趋势 |
|---|---|---|---|---|
| 内部缺陷率（PPM） | < 1,000 | {{prior_ppm}} | {{current_ppm}} | ↑ ↓ → |
| 客户投诉率 | < 50/百万件 | {{prior_complaints}} | {{current_complaints}} | ↑ ↓ → |
| 供应商 PPM（来料） | < 500 | {{prior_supplier_ppm}} | {{current_supplier_ppm}} | ↑ ↓ → |
| NCR 关闭时间（中位天数） | < 15 | {{prior_ncr_cycle}} | {{current_ncr_cycle}} | ↑ ↓ → |
| CAPA 按时关闭率 | > 90% | {{prior_capa_otc}} | {{current_capa_otc}} | ↑ ↓ → |
| 质量成本（占收入百分比） | < 3% | {{prior_coq}} | {{current_coq}} | ↑ ↓ → |

**重大质量事件：**
1. {{event_1}}
2. {{event_2}}

**CAPA 状态：**

| 状态 | 数量 |
|---|---|
| 开放 — 进展正常 | {{on_track}} |
| 开放 — 已逾期 | {{overdue}} |
| 本期已关闭 | {{closed}} |
| 有效性已验证 | {{verified}} |

**按 PPM 排名的顶级供应商（最差的 5 个）：**

| 供应商 | PPM | 趋势 | 当前升级等级 |
|---|---|---|---|
| {{supplier_1}} | {{ppm_1}} | ↑ ↓ → | {{level_1}} |
| {{supplier_2}} | {{ppm_2}} | ↑ ↓ → | {{level_2}} |

**质量成本明细：**

| 类别 | 金额 | 占收入百分比 |
|---|---|---|
| 预防 | {{prevention_cost}} | {{prevention_pct}} |
| 鉴定 | {{appraisal_cost}} | {{appraisal_pct}} |
| 内部失效 | {{internal_failure_cost}} | {{internal_pct}} |
| 外部失效 | {{external_failure_cost}} | {{external_pct}} |
| **总质量成本** | **{{total_coq}}** | **{{total_coq_pct}}** |

**管理层需采取的行动：**
1. {{action_request_1}}（例如："批准自动化检验系统的资本支出 — 已附 ROI 分析"）
2. {{action_request_2}}（例如："需要决定是否将供应商 X 升级至三级/备选来源资格认证"）

---

## 11. 监管机构响应（FDA 483 表格）

### 何时使用
- 正式响应 FDA 483 表格观察项
- 收到 483 后 15 个工作日内提交
- 这是一份关键文件——它将成为 FDA 公开检查记录的一部分

### 语气指导
尊重、彻底、负责。确认每项观察。不要争辩、淡化或归咎个人。展示您理解法规的目的，而不仅仅是字面意思。FDA 评审员会专门评估您的响应是否针对系统性问题，而不仅仅是具体观察项。

### 不可使用的措辞
- "我们不同意此观察项"——即使您不同意也要处理
- "这是一个孤立事件"——FDA 明确寻找系统性问题
- "员工已被解雇"——这是惩罚性的，不是纠正性的；FDA 想要系统性的修复
- 写"我们将处理此事"而不附具体行动、日期和责任人

### 模板

**[公司抬头]**

{{date}}

{{fda_district_director_name}}
Director, {{fda_district_office}}
Food and Drug Administration
{{fda_address}}

**关于: 对 FDA 483 表格检查观察项的响应**
**生产场所:** {{facility_name_address}}
**FEI 编号:** {{fei_number}}
**检查日期:** {{inspection_dates}}
**检查员:** {{investigator_name}}

尊敬的 {{fda_district_director_name}}：

{{our_company}} 感谢有机会对 FDA 在 {{inspection_dates}} 对我方 {{facility_name}} 设施的检查中识别的观察项作出响应。我们认真对待这些观察项，并已启动如下所述的纠正措施。

---

**观察项 {{obs_number}}：**
"{{verbatim_483_observation}}"

**响应：**

**确认：**
{{acknowledgment}}（例如："我们确认我方程序 QP-4401 未充分涉及..."）

**调查：**
{{investigation_summary}}（我们调查了什么、发现了什么、根本原因）

**纠正措施：**

| 行动 | 描述 | 负责人 | 目标日期 | 状态 |
|---|---|---|---|---|
| 1 | {{action_1_description}} | {{responsible_1}} | {{date_1}} | {{status_1}} |
| 2 | {{action_2_description}} | {{responsible_2}} | {{date_2}} | {{status_2}} |

**范围扩展：**
{{scope_extension}}（例如："我们审查了我方设施中所有类似程序，并识别出另外两个存在相同差距的领域。这些已作为上述行动 3 和 4 的一部分得到纠正。"）

**有效性验证：**
{{effectiveness_plan}}（例如："我们将在 90 天内通过跟踪[具体指标]来监测这些纠正措施的有效性。有效性证据将应要求提供审查。"）

**随附证据:** {{list_of_evidence}}

---

[对每项观察项重复]

---

我们承诺完全遵守 21 CFR Part 820 并持续改进我们的质量管理体系。我们欢迎您有机会讨论这些响应或提供更多信息。

此致

{{signatory_name}}
{{signatory_title}}
{{our_company}}
{{contact_information}}

附件: {{list_of_enclosures}}
