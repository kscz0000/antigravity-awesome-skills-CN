# 退货与逆向物流沟通模板

> **参考类型：** 第三层 — 在撰写或审查退货相关沟通时按需加载。
>
> **用法：** 每个模板包含 `{{双大括号}}` 格式的变量占位符，可直接替换。模板按受众和阶段组织。选择与您场景匹配的模板，替换变量，审查语气指引后发送。

---

## 目录

1. [RMA 批准通知](#1-rma-批准通知)
2. [RMA 拒绝通知](#2-rma-拒绝通知)
3. [欺诈调查暂停通知](#3-欺诈调查暂停通知)
4. [供应商 RTV 索赔提交](#4-供应商-rtv-索赔提交)
5. [客户退款确认](#5-客户退款确认)
6. [重新入库费说明](#6-重新入库费说明)
7. [向制造商提交保修索赔](#7-向制造商提交保修索赔)
8. [处置报告（内部）](#8-处置报告内部)
9. [退货政策例外批准](#9-退货政策例外批准)

---

## 变量参考

模板中使用的通用变量：

| 变量 | 说明 | 示例 |
|---|---|---|
| `{{customer_name}}` | 客户全名 | `Sarah Chen` |
| `{{customer_email}}` | 客户邮箱 | `schen@email.com` |
| `{{order_number}}` | 原始订单号 | `ORD-2025-88431` |
| `{{rma_number}}` | 退货授权编号 | `RMA-2025-04872` |
| `{{product_name}}` | 产品名称/描述 | `Sony WH-1000XM5 Wireless Headphones` |
| `{{product_sku}}` | 产品 SKU | `SNY-WH1000XM5-BLK` |
| `{{serial_number}}` | 产品序列号 | `SN-8834201` |
| `{{purchase_date}}` | 原始购买日期 | `2025-09-14` |
| `{{purchase_price}}` | 原始购买价格 | `$349.99` |
| `{{refund_amount}}` | 待发放退款金额 | `$349.99` |
| `{{restocking_fee}}` | 重新入库费金额 | `$52.50` |
| `{{payment_method}}` | 原始支付方式（脱敏） | `Visa ending in 4821` |
| `{{return_reason}}` | 客户声明的退货原因 | `Product not as described` |
| `{{return_window_end}}` | 标准退货截止日 | `2025-10-14` |
| `{{rma_expiry}}` | RMA 标签/授权过期日期 | `2025-10-28` |
| `{{our_company}}` | 我方公司名称 | `Apex Commerce Inc.` |
| `{{our_contact_name}}` | 退货团队联系人姓名 | `Maria Gonzalez` |
| `{{our_contact_title}}` | 职位头衔 | `Returns Operations Supervisor` |
| `{{our_contact_email}}` | 联系邮箱 | `returns@apexcommerce.com` |
| `{{our_contact_phone}}` | 联系电话 | `(800) 555-0199` |
| `{{vendor_name}}` | 供应商/制造商名称 | `Bose Corporation` |
| `{{vendor_contact}}` | 供应商退货联系人 | `James Park, RTV Coordinator` |
| `{{vendor_account}}` | 供应商账户编号 | `APEX-VND-00342` |
| `{{defect_description}}` | 缺陷描述 | `Left ear cup intermittent audio dropout` |
| `{{inspection_grade}}` | 分配的状况等级 | `Grade B` |
| `{{disposition_route}}` | 处置决策 | `Open box resale` |
| `{{business_days}}` | 处理时间（工作日） | `5-7` |
| `{{carrier_name}}` | 退货运输承运商 | `UPS Ground` |
| `{{tracking_number}}` | 退货物流追踪号 | `1Z999AA10123456784` |
| `{{warranty_end_date}}` | 保修到期日期 | `2027-09-14` |
| `{{claim_number}}` | 保修或供应商索赔参考编号 | `WC-2025-11294` |

---

## 1. RMA 批准通知

### 使用场景
- 客户已发起退货请求，且该请求已根据标准政策或授权例外获得批准。
- 在 RMA 批准后立即发送，以最大限度减少客户持有产品的时间。

### 语气指引
温暖且高效。客户已做出退货决定 — 让过程尽可能简单。以可操作信息（RMA 编号、运输说明）开头，而非政策。

### 不可说的内容
- 不要在此阶段询问"您确定吗？"或试图劝阻退货。
- 不要使用暗示客户做错了什么的语言。
- 不要将运输说明埋在营销内容下方。

### 模板

**主题：** 您的退货已获批准 — RMA# {{rma_number}}

---

Hi {{customer_name}}，

您对 **{{product_name}}**（订单 {{order_number}}）的退货已获批准。

**您的 RMA 编号：** {{rma_number}}

**如何退回商品：**

1. 将产品连同所有配件一起放入原始包装中。
2. 打印本邮件附带的预付退货标签。
3. 将标签贴在包裹外部。
4. 将包裹送至任意 {{carrier_name}} 网点。

**重要详情：**
- 请在 **{{rma_expiry}}** 之前寄出退货商品 — RMA 在此日期后过期。
- 我们收到并检查您的退货后，**{{refund_amount}}** 的退款将在 {{business_days}} 个工作日内处理至您的 {{payment_method}}。

如有任何疑问，请回复此邮件或致电 {{our_contact_phone}} 联系我们。

此致，
{{our_company}} 退货团队

---

## 2. RMA 拒绝通知

### 使用场景
- 退货请求不符合政策要求（超出退货窗口期、排除品类、状况不符）。
- 始终提供具体原因和替代方案。

### 语气指引
有同理心但清晰。客户会感到失望。承认其处境，说明具体原因（不要笼统地说"根据我们的政策"），并始终至少提供一种替代解决途径。

### 不可说的内容
- "unfortunately"（遗憾地）不要使用超过一次。
- 不要引用政策条款编号或使用法律用语。
- 不要完全关闭大门 — 始终提供替代方案或升级路径。
- 绝不说"我们无能为力"。

### 模板

**主题：** 关于您的退货请求 — 订单 {{order_number}}

---

Hi {{customer_name}}，

感谢您联系我们咨询关于 **{{product_name}}**（订单 {{order_number}}，购买日期 {{purchase_date}}）的退货事宜。

在审查您的请求后，我们无法处理标准退货，原因是 **{{denial_reason}}**。

**我们理解这令人沮丧，我们希望为您提供帮助。以下是您的选择：**

{{#if warranty_eligible}}
- **保修索赔：** 您的产品仍在制造商保修范围内，保修期至 {{warranty_end_date}}。我们可以帮助您提交保修索赔以进行维修或更换。只需回复此邮件，我们将为您启动流程。
{{/if}}

{{#if exchange_eligible}}
- **换货：** 虽然我们无法提供退款，但我们可以安排更换相同产品或类似商品。将收取 {{restocking_fee_pct}}% 的重新入库费。
{{/if}}

- **商店余额：** 我们可能根据具体情况提供商店余额。如果您希望我们审查此选项，请回复邮件并提供有关您情况的额外详情。

- **与主管沟通：** 如果您认为您的情况需要例外处理，我们很乐意安排主管审查您的案件。请致电 {{our_contact_phone}} 并要求与退货主管通话。

我们珍视您的业务，并希望找到适合您的解决方案。

诚挚地，
{{our_contact_name}}
{{our_company}} 退货团队
{{our_contact_email}} | {{our_contact_phone}}

---

## 3. 欺诈调查暂停通知

### 使用场景
- 退货已被欺诈评分系统标记（评分 ≥ 65），需要在退款处理前进行审查。
- 必须通知客户延迟，但不得透露欺诈调查。

### 语气指引
中立且专业。这是一份"处理延迟"通知。**绝不**使用"欺诈"、"可疑"、"调查"或"已标记"等词语。客户可能完全合法 — 暂停是预防性的。

### 不可说的内容
- 绝不说"您的退货已被标记"。
- 绝不提及欺诈、盗窃或滥用。
- 绝不暗示客户做了错事。
- 不要给出不确定的时间表 — 始终承诺具体的审查窗口。

### 模板

**主题：** 您的退货正在处理中 — 订单 {{order_number}}

---

Hi {{customer_name}}，

感谢您退回 **{{product_name}}**（RMA# {{rma_number}}）。

我们已收到您退回的商品，目前正在进行质量审查流程。此审查确保我们准确评估产品状况并正确处理您的退款。

**我们预计将在 {{review_days}} 个工作日内完成此审查。**

您目前无需采取任何行动。退款处理完成后，我们将向您发送确认邮件。

如有疑问，请致电 {{our_contact_phone}} 或回复此邮件联系我们。

感谢您的耐心，
{{our_company}} 退货团队

---

### 内部附注（不发送给客户）

**欺诈审查 — RMA# {{rma_number}}**

| 字段 | 详情 |
|---|---|
| 客户 | {{customer_name}} ({{customer_email}}) |
| 欺诈评分 | {{fraud_score}} |
| 主要信号 | {{fraud_signals}} |
| 产品 | {{product_name}} ({{product_sku}}) |
| 退货价值 | {{purchase_price}} |
| 客户 LTV | {{customer_ltv}}) |
| 所需操作 | {{review_action}} |
| 审查截止日期 | {{review_deadline}} |
| 负责人 | {{reviewer_name}} |

**审查说明：** 完成检查并拍照记录。核实序列号与订单记录是否一致。检查产品重量与预期重量是否相符。将实物产品与产品列表进行对比。将结果记录在欺诈案件管理系统中。建议：处理退款 / 部分退款 / 拒绝并升级。

---

## 4. 供应商 RTV 索赔提交

### 使用场景
- 因缺陷产品、供应商导致的质量问题或供应商合规违规提交退货至供应商索赔。
- 附上所有支持文件（照片、检查报告、客户投诉数据）。

### 语气指引
专业且基于证据。供应商响应数据而非投诉。以事实开头：SKU、数量、缺陷描述、退货率数据。引用供应商协议中涵盖缺陷索赔的条款。

### 模板

**主题：** RTV 索赔 — {{vendor_account}} — {{claim_number}}

---

{{vendor_contact}}，

请查阅以下我们在账户 {{vendor_account}} 下就收到的缺陷商品提交的退货至供应商索赔。

**索赔参考：** {{claim_number}}
**提交日期：** {{claim_date}}
**RTV 授权编号：** {{rtv_auth_number}}（如适用）

**索赔详情：**

| SKU | 产品名称 | 缺陷数量 | 缺陷描述 | 单位成本 | 合计 |
|---|---|---|---|---|---|
| {{sku_1}} | {{product_1}} | {{qty_1}} | {{defect_1}} | {{cost_1}} | {{ext_1}} |
| {{sku_2}} | {{product_2}} | {{qty_2}} | {{defect_2}} | {{cost_2}} | {{ext_2}} |

**索赔总金额：** {{total_claim_amount}}

**支持文件（附件）：**
- 缺陷照片（{{photo_count}} 张图片）
- 各 SKU 的检查报告
- 按 SKU 统计的客户退货数据（退货率、投诉摘要）
- 原始采购订单：{{po_numbers}}

**缺陷率分析：**
- SKU {{sku_1}}：{{defect_rate_1}}% 退货率（{{period}}），品类基线为 {{baseline_rate}}%
- 超出基线的多余退货：{{excess_units}} 件

根据我们签订日期为 {{agreement_date}} 的供应商协议第 {{agreement_section}} 条，缺陷率超过 {{defect_threshold}}% 阈值的缺陷商品有资格获得全额信用额度，包括入站运费和退货处理费用。

**请求解决方案：** {{total_claim_amount}} 的全额商品信用额度，加上 {{processing_costs}} 的退货处理费用和 {{freight_costs}} 的入站运费，索赔总额为 {{grand_total}}。

请确认收到并提供预计信用额度到账时间。根据我们的协议，供应商信用额度应在索赔提交后 {{credit_days}} 天内到账。

此致，
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 5. 客户退款确认

### 使用场景
- 退款已处理。这是标准退货的最终沟通。
- 在退款发起时立即发送（而非在客户银行到账时）。

### 语气指引
温暖且简洁。以退款金额和时间线开头。客户想知道的是：多少钱、什么时候到账。

### 模板

**主题：** 您的退款已处理 — {{refund_amount}}

---

Hi {{customer_name}}，

您对 **{{product_name}}**（订单 {{order_number}}）的退款已处理。

**退款详情：**
- **金额：** {{refund_amount}}
- **退款至：** {{payment_method}}
- **预计到账：** {{refund_timeline}}

{{#if restocking_fee_applied}}
根据我们的退货政策，已拆封的 {{product_category}} 商品将收取 {{restocking_fee}} 的重新入库费。您的原始购买价格为 {{purchase_price}}。
{{/if}}

{{#if store_credit}}
您的 {{store_credit_amount}} 商店余额已添加到您的账户，可立即使用。
{{/if}}

感谢您的惠顾。如有其他需要帮助的地方，我们随时为您服务。

此致，
{{our_company}} 客户关怀

---

## 6. 重新入库费说明

### 使用场景
- 当收取重新入库费且客户提出疑问时（在退货时主动告知或回应投诉时）。

### 语气指引
透明且实事求是。说明费用涵盖的内容。不要对政策表示歉意，但要明确说明具体金额。

### 模板

**主题：** 回复：您的退货 — 重新入库费详情

---

Hi {{customer_name}}，

我了解到您对退回 **{{product_name}}** 时收取的重新入库费有疑问。

以下是明细：

| 项目 | 金额 |
|---|---|
| 原始购买价格 | {{purchase_price}} |
| 重新入库费（{{restocking_fee_pct}}%） | -{{restocking_fee}} |
| **您的退款** | **{{refund_amount}}** |

**收取重新入库费的原因：**

我们的退货政策对已拆封的 {{product_category}} 产品收取 {{restocking_fee_pct}}% 的重新入库费。此费用涵盖检查、测试和重新包装产品的成本，以便以降低的"开箱"价格提供给下一位客户。商品一旦拆封使用，就不能再作为全新品出售，重新入库费有助于弥补这一价值差异。

**请注意：** 缺陷产品和配送错误免收重新入库费。如果您认为您的产品存在缺陷，请告知我们，我们将进行审查 — 如果确认存在缺陷，我们将退还重新入库费。

如需进一步讨论，请致电 {{our_contact_phone}} 或回复此邮件。

此致，
{{our_contact_name}}
{{our_company}} 退货团队

---

## 7. 向制造商提交保修索赔

### 使用场景
- 代表客户或针对零售商持有的缺陷库存向制造商提交保修索赔。

### 语气指引
正式且详尽。制造商根据文件质量处理保修索赔。一次性提供所有信息以避免反复沟通。

### 模板

**主题：** 保修索赔 — {{claim_number}} — {{product_name}}

---

致：{{manufacturer_warranty_dept}}

**保修索赔提交**

| 字段 | 详情 |
|---|---|
| 索赔参考 | {{claim_number}} |
| 零售商账户 | {{retailer_account_number}} |
| 产品 | {{product_name}} ({{product_sku}}) |
| 序列号 | {{serial_number}} |
| 购买日期 | {{purchase_date}} |
| 保修到期日 | {{warranty_end_date}} |
| 缺陷描述 | {{defect_description}} |
| 缺陷报告日期 | {{defect_report_date}} |

**客户信息：**
- 姓名：{{customer_name}}
- 原始订单：{{order_number}}
- 已为客户提供临时解决方案：{{interim_resolution}}

**缺陷文件：**
- 缺陷照片：已附（{{photo_count}} 张图片）
- 功能测试结果：{{test_results}}
- 客户缺陷描述："{{customer_defect_statement}}"

**产品状况：**
- 外观状况：{{physical_condition}}
- 改装情况：{{modifications_noted}}
- 配件状况：{{accessories_status}}

**请求解决方案：** {{requested_resolution}}（维修 / 更换 / 信用额度）

请确认收到并提供索赔处理时间线。客户正在等待解决方案。

此致，
{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

## 8. 处置报告（内部）

### 使用场景
- 退货处置结果的每周或每月汇总，供管理层审查。
- 用于追踪回收率、识别处置效率机会和监控欺诈趋势。

### 语气指引
数据优先、简洁。管理层阅读这些报告是为了了解趋势和例外情况，而非长篇叙述。

### 模板

**主题：** 退货处置报告 — {{report_period}}

---

## 摘要

| 指标 | 本期 | 上期 | 趋势 |
|---|---|---|---|
| 收到退货总数 | {{total_returns}} | {{prior_total}} | {{trend_total}} |
| 退货总价值 | {{total_value}} | {{prior_value}} | {{trend_value}} |
| 平均退货价值 | {{avg_value}} | {{prior_avg}} | {{trend_avg}} |
| 重新上架率（A 级） | {{restock_pct}}% | {{prior_restock}}% | {{trend_restock}} |
| 开箱/翻新率（B 级） | {{open_box_pct}}% | {{prior_open_box}}% | {{trend_ob}} |
| 清仓率（C 级） | {{liquidation_pct}}% | {{prior_liq}}% | {{trend_liq}} |
| 销毁/回收率（D 级） | {{destroy_pct}}% | {{prior_destroy}}% | {{trend_destroy}} |
| 净回收率 | {{recovery_pct}}% | {{prior_recovery}}% | {{trend_recovery}} |
| 触发欺诈标记数 | {{fraud_flags}} | {{prior_fraud}} | {{trend_fraud}} |
| 已确认欺诈案件 | {{confirmed_fraud}} | {{prior_confirmed}} | {{trend_confirmed}} |
| 提交的供应商 RTV 索赔 | {{rtv_count}} ({{rtv_value}}) | {{prior_rtv}} | {{trend_rtv}} |

## 退货原因排名

| 原因 | 数量 | 占比 | 平均价值 |
|---|---|---|---|
| {{reason_1}} | {{count_1}} | {{pct_1}}% | {{avg_1}} |
| {{reason_2}} | {{count_2}} | {{pct_2}}% | {{avg_2}} |
| {{reason_3}} | {{count_3}} | {{pct_3}}% | {{avg_3}} |
| {{reason_4}} | {{count_4}} | {{pct_4}}% | {{avg_4}} |
| {{reason_5}} | {{count_5}} | {{pct_5}}% | {{avg_5}} |

## 退货量排名前 SKU

| SKU | 产品 | 退货数 | 退货率 | 主要原因 | 操作 |
|---|---|---|---|---|---|
| {{sku_1}} | {{prod_1}} | {{ret_1}} | {{rate_1}}% | {{reason_sku_1}} | {{action_1}} |
| {{sku_2}} | {{prod_2}} | {{ret_2}} | {{rate_2}}% | {{reason_sku_2}} | {{action_2}} |
| {{sku_3}} | {{prod_3}} | {{ret_3}} | {{rate_3}}% | {{reason_sku_3}} | {{action_3}} |

## 例外与升级

- {{exception_summary_1}}
- {{exception_summary_2}}
- {{exception_summary_3}}

## 建议

- {{recommendation_1}}
- {{recommendation_2}}
- {{recommendation_3}}

---

编制人：{{our_contact_name}}，{{our_contact_title}}
分发范围：{{distribution_list}}

---

## 9. 退货政策例外批准

### 使用场景
- 当标准退货政策的例外已获批准时（超出退货窗口期、缺少收据、状况超出标准验收标准）。
- 记录例外情况以备审计，并将决定告知客户。

### 语气指引
面向客户的版本：温暖，传达您为客户额外争取了。内部版本：实事求是，记录商业理由。

### 面向客户的模板

**主题：** 好消息 — 您的退货已获批准

---

Hi {{customer_name}}，

我们已审查您对 **{{product_name}}**（订单 {{order_number}}）的退货请求，很高兴通知您，我们已将其作为一次性例外予以批准。

**以下是您需要了解的信息：**

- **退款金额：** {{refund_amount}}，以 {{refund_type}} 形式
- **如何退货：** {{return_instructions}}
- **RMA 编号：** {{rma_number}}（有效期至 {{rma_expiry}}）

{{#if conditions}}
**请注意：** {{exception_conditions}}
{{/if}}

感谢您的忠诚，希望这能帮到您。如有其他需要，我们随时为您服务。

此致，
{{our_contact_name}}
{{our_company}} 客户关怀

---

### 内部审批记录

**政策例外批准**

| 字段 | 详情 |
|---|---|
| RMA | {{rma_number}} |
| 客户 | {{customer_name}} ({{customer_email}}) |
| 订单 | {{order_number}} |
| 产品 | {{product_name}} ({{product_sku}}) |
| 购买价格 | {{purchase_price}} |
| 退款金额 | {{refund_amount}} |
| 退款类型 | {{refund_type}} |
| 违反的标准政策 | {{policy_violation}} |
| 例外评分 | {{exception_score}}（根据例外矩阵） |
| 客户 LTV | {{customer_ltv}} |
| 客户退货率 | {{customer_return_rate}}% |
| 商业理由 | {{business_justification}} |
| 审批人 | {{approver_name}} ({{approver_title}}) |
| 审批日期 | {{approval_date}} |
| 先例风险 | {{precedent_risk}} |
| 备注 | {{approval_notes}} |
