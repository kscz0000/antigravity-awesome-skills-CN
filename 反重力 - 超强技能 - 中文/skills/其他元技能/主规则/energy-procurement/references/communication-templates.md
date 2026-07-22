# 沟通模板 — 能源采购

> **参考类型：** Tier 3 — 在撰写或审查能源采购沟通文档时按需加载。
>
> **使用方式：** 每个模板都包含 `{{双花括号}}` 形式的变量占位符，可直接替换。模板按沟通类型和业务场景组织。选择匹配你场景的模板，替换变量，参照语气指引，发送。

---

## 目录

1. [向能源供应商发送的 RFP](#1-向能源供应商发送的-rfp)
2. [PPA 条款书回应](#2-ppa-条款书回应)
3. [公用事业费率案例干预意见](#3-公用事业费率案例干预意见)
4. [需求响应项目入网申请](#4-需求响应项目入网申请)
5. [预算预测汇报](#5-预算预测汇报)
6. [可持续发展报告 — 能源部分](#6-可持续发展报告--能源部分)
7. [内部能源成本差异分析](#7-内部能源成本差异分析)
8. [供应商合同续签谈判](#8-供应商合同续签谈判)
9. [监管备案意见](#9-监管备案意见)
10. [董事会级能源战略摘要](#10-董事会级能源战略摘要)

---

## 变量参考表

各模板通用的公共变量：

| 变量 | 说明 | 示例 |
|---|---|---|
| `{{our_company}}` | 贵公司法定名称 | `Meridian Manufacturing Corp.` |
| `{{our_contact_name}}` | 贵方代表姓名 | `Jennifer Walsh` |
| `{{our_contact_title}}` | 贵方代表职务 | `Director of Energy Procurement` |
| `{{our_contact_email}}` | 贵方代表邮箱 | `jwalsh@meridian.com` |
| `{{our_contact_phone}}` | 贵方代表电话 | `(614) 555-0247` |
| `{{supplier_name}}` | 能源供应商名称 | `NorthStar Energy Solutions` |
| `{{supplier_contact}}` | 供应商联系人姓名 | `David Chen` |
| `{{supplier_contact_title}}` | 供应商联系人职务 | `VP, Commercial Sales` |
| `{{utility_name}}` | 公用事业公司名称 | `AEP Ohio` |
| `{{iso_name}}` | ISO/RTO 名称 | `PJM Interconnection` |
| `{{facility_name}}` | 设施名称 | `Columbus Manufacturing Plant` |
| `{{facility_address}}` | 设施地址 | `4500 Industrial Parkway, Columbus, OH 43228` |
| `{{account_number}}` | 公用事业账号 | `110-485-7723` |
| `{{annual_consumption_mwh}}` | 年用电量 | `42,000 MWh` |
| `{{peak_demand_kw}}` | 峰值需量（kW） | `6,200 kW` |
| `{{current_rate}}` | 当前合同电价 | `$0.058/kWh` |
| `{{proposed_rate}}` | 拟议新电价 | `$0.054/kWh` |
| `{{market_rate}}` | 市场基准电价 | `$0.062/kWh` |
| `{{contract_start}}` | 合同起始日 | `2027-01-01` |
| `{{contract_end}}` | 合同结束日 | `2029-12-31` |
| `{{rfp_deadline}}` | RFP 投标截止日 | `2026-05-15` |
| `{{ppa_project_name}}` | 可再生能源项目名称 | `Prairie Wind Farm II` |
| `{{ppa_capacity_mw}}` | PPA 项目容量 | `150 MW` |
| `{{ppa_strike_price}}` | PPA 执行价格 | `$34/MWh` |
| `{{ppa_term_years}}` | PPA 合同期限 | `15 years` |
| `{{re_percentage}}` | 当前可再生能源占比 | `38%` |
| `{{re_target}}` | RE100 目标年 | `2030` |
| `{{docket_number}}` | 监管案卷编号 | `Case No. 26-1234-EL-AIR` |
| `{{budget_year}}` | 预算预测年度 | `2027` |
| `{{total_energy_spend}}` | 年能源支出总额 | `$14.2M` |
| `{{num_facilities}}` | 设施数量 | `18` |

---

## 1. 向能源供应商发送的 RFP

**渠道：** 邮件附 RFP 文档
**受众：** 零售能源供应商的销售/定价团队
**语气：** 专业、数据翔实、具竞争性。你提供的是重要的商业机会——要把它呈现为这样的机会。

---

**主题：** `招标邀请 — {{our_company}} 电力供应 RFP — {{contract_start}} 启动`

{{supplier_contact}}，

{{our_company}} 正在 {{iso_name}} 辖区内的 {{num_facilities}} 个设施开展竞争性电力供应采购。基于贵方在我方服务区域的市场地位与能力，特此邀请 {{supplier_name}} 参与本次投标。

**RFP 概要：**
- **范围：** {{num_facilities}} 个商业和工业设施
- **年总用电量：** {{annual_consumption_mwh}}
- **合计峰值需量：** {{peak_demand_kw}}
- **合同期：** {{contract_start}} 至 {{contract_end}}
- **请求的产品结构：** 固定价格全需求、分块指数和带价格上限的指数
- **投标截止时间：** {{rfp_deadline}}，下午 5:00（美东时间）

**随函附上：**
1. RFP 响应模板（Excel），含站点级明细
2. 各设施 36 个月的 15 分钟间隔数据（CSV）
3. 当前费率信息与公用事业账号
4. 评标标准与权重

**评标标准：**
- 三种价格情景下的总成本（40%）
- 供应商信用质量与财务稳健性（20%）
- 合同灵活性，包括数量容差与提前终止条款（15%）
- 可持续服务 — REC 采购、碳报告、PPA 咨询（15%）
- 市场情报与咨询能力（10%）

**关键要求：**
- 所有投标须至少包含 ±10% 的数量容差
- 三种产品结构须独立报价
- 供应商须达到 BBB 及以上或同等级别的信用评级
- REC 须来自 {{iso_name}} 辖区内的项目

请于 {{rfp_confirmation_date}} 前确认参与意向。澄清问题请于 {{rfp_questions_deadline}} 前发送至 {{our_contact_email}}。

期待 {{supplier_name}} 的参与。

{{our_contact_name}}
{{our_contact_title}}
{{our_company}}
{{our_contact_email}} | {{our_contact_phone}}

---

**语气指引：**
- 不要向投标人透露当前报价。"当前合同细节属保密信息"是标准答复。
- 不要披露投标家数。"我们邀请了具有竞争力的候选"已足够。
- 所有澄清问题须以合并 Q&A 形式同时发送给所有投标人，确保公平。

---

## 2. PPA 条款书回应

**渠道：** 邮件发送至开发商商务团队
**受众：** 可再生能源项目开发商
**语气：** 协作但商业严谨。PPA 是 10-25 年的承诺——每个条款都至关重要。

---

**主题：** `{{our_company}} 对 {{ppa_project_name}} 条款书的回应 — 商务反馈`

{{developer_contact}}，

感谢贵方就 {{ppa_project_name}}（{{ppa_capacity_mw}}）提供的条款书。我们已完成初步审查，以下为按商务、财务和运营条款组织的反馈。

**商务条款：**
- **执行价格：** 拟议的 {{ppa_strike_price}} 在我们基于当前远期曲线的目标范围内。我们希望讨论价格递增结构——前 1-5 年 0% 递增，第 6 年起按 [CPI 联动 / 固定 1.5%] 递增。
- **结算点：** 我们请求以 {{iso_name}} [负荷区/枢纽] 而非项目节点结算，以降低我方基差风险敞口。我们理解这可能需要价格调整，并愿就此进行讨论。
- **合同电量：** 我们希望讨论部分承购（{{our_offtake_mw}} MW 来自 {{ppa_capacity_mw}} 项目），并保留对额外容量的优先购买权。

**风险分摊：**
- **削减：** 我们请求开发商承担前 5% 的年度削减风险，5%-10% 区间双方各承担 50%，10% 以上由开发商承担。当前条款书将全部削减风险分配给承购方，对于 {{ppa_term_years}} 年期的承诺而言不可接受。
- **负电价：** 我们要求设置负电价下限条款：当结算点 LMP 为负的时段，不发生结算（双方均不付款）。这能保护双方免受负电价波动时段的影响。
- **法律变更：** 条款书中的法律变更条款是单方面的。我们提议：若法规变更实质性地影响任一方的经济利益，则双方均享有终止权，并设置 {{materiality_threshold}} 的重大性阈值。

**财务与信用：**
- **信用支持：** 我们可提供 [母公司担保 / 信用证]，金额为 {{credit_support_amount}}，规模相当于我方压力情景下两年潜在负向盯市敞口。
- **会计处理：** 我们需要确认 PPA 结构符合 ASC 815 下的常规购销（NPNS）豁免条件，或可适用套期会计。我方财务团队将与我方审计师一起审查最终合同。

**REC 条款：**
- **时效交付：** REC 须在发电后 12 个月内交付，以保持 RE100 合规。
- **替代 REC：** 若项目任何年度的 REC 交付低于合同量 10% 以上，开发商须从同等级设施无偿提供替代 REC。

我们欢迎本周内就此召开电话会议讨论以上要点，请告知贵方可用时间。

{{our_contact_name}}
{{our_contact_title}}

---

**语气指引：**
- PPA 谈判是多轮博弈。首次回应应确立关键立场，避免使用最后通牒式语言。
- 始终将风险分摊表述为"对双方公平"，而非"我们不接受贵方的风险"。
- 开发商每周收到大量条款书回应——具体、有条理才能脱颖而出，成为被认真对待的承购方。

---

## 3. 公用事业费率案例干预意见

**渠道：** 向州公用事业委员会正式提交
**受众：** PUC 委员、行政法官、公用事业监管人员
**语气：** 正式、数据驱动、法律上精确。这是监管程序——意见必须有证据支持。

---

**关于：** {{docket_number}} — {{utility_name}} 提请调增电费

**提交至 {{state}} 公用事业委员会**

**{{our_company}} 的意见**

{{our_company}} 谨就 {{utility_name}} 于 {{filing_date}} 提交的通用费率上调申请提交以下意见。

**一、{{our_company}} 的利益**

{{our_company}} 在 {{utility_name}} 服务区域内运营 {{num_facilities}} 个设施，按 {{rate_schedule}} 费率表年消耗约 {{annual_consumption_mwh}}。拟议的费率上调将给 {{our_company}} 的运营带来约每年 ${{annual_impact}} 的额外成本。

**二、关切摘要**

{{our_company}} 不反对 {{utility_name}} 收回审慎发生成本并获得合理回报的权利。然而，我们对所提交申请提出以下关切：

1. **请求的股权回报率（ROE）：** {{utility_name}} 请求 {{requested_roe}}% 的 ROE。{{comparable_states}} 的同类程序中，委员会最近授权的 ROE 为 {{comparable_roe_range}}%。我们谨此指出，所请求的 ROE 超出当前资本市场条件支持的范围。

2. **费率设计：** 拟议费率设计将按量电量电费上调 {{energy_increase_pct}}%，而仅将需量电费下调 {{demand_decrease_pct}}%。该成本分摊方法对高负荷率的工业客户不利——按每 kWh 计算，他们对系统峰值的贡献较低。我们建议基于实证成本成因进行分摊，对需量相关成本采用同时峰值方法。

3. **附加费传导时点：** 拟议的基础设施改善附加费允许按季度调整费率，无需委员会审查。我们请求任何附加费机制都应包含年度清算并经委员会审查，以及 {{rider_cap_pct}}% 的累计上限，以避免费率冲击。

**三、请求的救济**

{{our_company}} 请求委员会：
- 将 ROE 设定在可比授权回报率的中点（约 {{recommended_roe}}%）
- 对 {{rate_schedule}} 费率类别采用同时峰值成本分摊方法
- 对拟议基础设施附加费设置年度委员会审查与累计上限

{{our_contact_name}}
{{our_contact_title}}，{{our_company}}

---

## 4. 需求响应项目入网申请

**渠道：** 正式入网申请
**受众：** 公用事业或 ISO 的需求响应项目管理员
**语气：** 技术性、精确。DR 入网文件具合同性质——准确性至关重要。

---

**主题：** `需求响应项目入网申请 — {{facility_name}}`

收件人：{{dr_program_administrator}}

{{our_company}} 借此申请将 {{facility_name}} 入网到 {{delivery_year}} 交付年的 {{dr_program_name}}。

**设施信息：**
- **设施：** {{facility_name}}
- **地址：** {{facility_address}}
- **公用事业账号：** {{account_number}}
- **电表 ID：** {{meter_id}}
- **供电电压：** {{service_voltage}}
- **当前峰值需量：** {{peak_demand_kw}}

**削减能力：**
- **承诺削减容量：** {{dr_commitment_kw}} kW
- **所需最短通知时间：** {{notification_minutes}} 分钟
- **最长削减持续时间：** {{max_duration_hours}} 小时
- **削减方式：** [通过楼宇自控系统 BAS 卸载负荷 / 备用发电 / 电池放电 / 组合方式]
- **可削减负荷：** {{curtailable_loads}}
- **不可削减负荷（关键工艺）：** {{non_curtailable_loads}}

**基线方法：**
我们请求采用 {{baseline_method}} 基线计算方法。附件为 12 个月的间隔数据文件，展示我方在 DR 事件窗口（{{event_window}}）的典型负荷曲线。

**测试：**
我方可在 {{test_week}} 这周进行入网验证测试。我方能够在收到通知后 {{notification_minutes}} 分钟内展示完整的 {{dr_commitment_kw}} kW 削减。

{{our_contact_name}}
{{our_contact_title}}

---

## 5. 预算预测汇报

**渠道：** 内部演示（PowerPoint / 备忘录）
**受众：** CFO、财务副总裁、预算委员会
**语气：** 精确、情景导向、聚焦行动。财务需要的是数字、区间和决策点——而非能源市场教程。

---

### {{budget_year}} 能源成本预测 — {{our_company}}

**编制人：** {{our_contact_name}}，{{our_contact_title}}
**日期：** {{forecast_date}}
**范围：** {{num_facilities}} 个设施，覆盖全部电力与天然气

**执行摘要：**
按基准假设，{{budget_year}} 年能源支出总额预测为 **${{base_case_total}}**，较 {{prior_year}} 实际 ${{prior_year_total}} 变动 {{yoy_change_pct}}% [上升/下降]。压力情景下预测区间为 **${{low_case_total}}** 至 **${{high_case_total}}**。

| 组成部分 | {{prior_year}} 实际 | {{budget_year}} 基准情景 | 变动 |
|-----------|---------------------|--------------------------|--------|
| 电力 — 供应 | ${{elec_supply_prior}} | ${{elec_supply_forecast}} | {{elec_supply_change}} |
| 电力 — 输送（T&D） | ${{elec_delivery_prior}} | ${{elec_delivery_forecast}} | {{elec_delivery_change}} |
| 电力 — 需量电费 | ${{demand_charges_prior}} | ${{demand_charges_forecast}} | {{demand_change}} |
| 电力 — 容量电费 | ${{capacity_prior}} | ${{capacity_forecast}} | {{capacity_change}} |
| 天然气 | ${{gas_prior}} | ${{gas_forecast}} | {{gas_change}} |
| REC / 可持续 | ${{rec_prior}} | ${{rec_forecast}} | {{rec_change}} |
| **合计** | **${{prior_year_total}}** | **${{base_case_total}}** | **{{total_change}}** |

**关键假设：**
- 电力远期曲线：截至 {{curve_date}}，{{forward_curve_source}}
- 天然气：Henry Hub {{gas_assumption}} + 基差 {{basis_assumption}}
- 天气：10 年正常 HDD/CDD
- 生产量：较上年 [持平 / 变动 {{production_change}}%]
- 对冲头寸：{{hedge_pct}}% 的电量锁定在 ${{hedged_rate}}/MWh

**情景分析：**

| 情景 | 电力成本 | 天然气成本 | 合计 | 较基准 |
|----------|-----------------|----------|-------|---------------|
| 基准 | ${{elec_base}} | ${{gas_base}} | ${{base_case_total}} | — |
| 暖冬/凉夏 | ${{elec_low}} | ${{gas_low}} | ${{low_case_total}} | {{low_delta}} |
| 寒冬/热夏 | ${{elec_high}} | ${{gas_high}} | ${{high_case_total}} | {{high_delta}} |
| 市场压力（2× 远期） | ${{elec_stress}} | ${{gas_stress}} | ${{stress_total}} | {{stress_delta}} |

**请求的决策：**
1. 批准 ${{base_case_total}} 的基准预算
2. 授权额外对冲 {{additional_hedge_pct}}%，使总对冲头寸达到 {{target_hedge_pct}}%
3. 批准 ${{capex_amount}} 资本预算，用于 {{capex_facilities}} 的需量电费缓解项目

---

## 6. 可持续发展报告 — 能源部分

**渠道：** 年度可持续发展 / ESG 报告
**受众：** 投资者、客户、ESG 评级机构、RE100、CDP
**语气：** 透明、有数据支撑、面向未来。避免"漂绿"——ESG 受众很专业。

---

### 能源与气候 — {{report_year}}

**范围 2 排放：**

| 指标 | {{prior_year}} | {{report_year}} | 变动 |
|--------|---------------|-----------------|--------|
| 总用电量（MWh） | {{elec_prior_mwh}} | {{elec_current_mwh}} | {{elec_change_pct}} |
| 范围 2 — 基于位置（吨 CO₂e） | {{scope2_loc_prior}} | {{scope2_loc_current}} | {{scope2_loc_change}} |
| 范围 2 — 基于市场（吨 CO₂e） | {{scope2_mkt_prior}} | {{scope2_mkt_current}} | {{scope2_mkt_change}} |
| 可再生电力占比 | {{re_pct_prior}} | {{re_pct_current}} | {{re_change}} |

**可再生能源采购：**

| 工具 | 电量（MWh） | 来源 | 额外性 |
|-----------|-------------|--------|---------------|
| 实物 PPA | {{phys_ppa_mwh}} | {{phys_ppa_project}} | 新项目，{{ppa_cod}} 投运 |
| 虚拟 PPA（REC） | {{vppa_rec_mwh}} | {{vppa_project}} | 新项目，{{vppa_location}} |
| 公用事业绿色费率 | {{green_tariff_mwh}} | {{green_tariff_utility}} | 视项目设计而定 |
| 非捆绑 REC | {{unbundled_rec_mwh}} | National wind | 市场 REC |
| 现场光伏 | {{onsite_mwh}} | {{onsite_locations}} | 自发自用 |

**RE100 进展：** {{our_company}} 在 {{report_year}} 实现 {{re_pct_current}}% 的可再生电力，达成我们 {{re_target}} 年 100% 可再生电力承诺的目标。

**未来目标：**
- {{next_year}} 年底前达到 {{re_target_next_year}}% 可再生电力
- {{next_year}} 年 Q2 前完成额外 {{next_ppa_mw}} MW 的可再生能源采购
- 以 {{baseline_year}} 为基准，{{target_year}} 年前基于市场的范围 2 排放减少 {{scope2_reduction_target}}%

---

## 7. 内部能源成本差异分析

**渠道：** 月度内部备忘录
**受众：** 财务总监、工厂经理、运营副总裁
**语气：** 分析性、行动导向。解释差异背后的"为什么"以及正在采取的措施。

---

**主题：** `能源成本差异报告 — {{year}} 年 {{month}}`

**摘要：** 能源成本实际 ${{actual_total}}，预算 ${{budget_total}}——差异 ${{variance}}（{{variance_pct}}）。

**差异分解：**

| 驱动因素 | 影响 | 说明 |
|--------|--------|-------------|
| 天气（HDD/CDD 与正常对比） | ${{weather_impact}} | {{month}} 较 {{weather_description}} —— 实际 HDD/CDD {{hdd_cdd_actual}}，预算 {{hdd_cdd_budget}} |
| 市场价格（指数敞口） | ${{market_impact}} | 日前 LMP 平均 ${{actual_lmp}}/MWh，预算假设 ${{budget_lmp}}/MWh |
| 需量电费 | ${{demand_impact}} | {{facility_name}} 峰值 {{actual_peak_kw}} kW，预算 {{budget_peak_kw}} kW |
| 产量 | ${{volume_impact}} | 生产工时 {{production_description}} 较计划 |
| 费率/电价变更 | ${{tariff_impact}} | {{tariff_description}} |

**已采取的行动：**
1. {{action_1}}
2. {{action_2}}
3. {{action_3}}

**预测修正：** 基于年初至今实际，全年能源成本预测修正为 ${{revised_forecast}}（此前 ${{prior_forecast}}）。主要原因：{{revision_driver}}。

---

## 8. 供应商合同续签谈判

**渠道：** 邮件
**受众：** 在位能源供应商的商务团队
**语气：** 关系优先、数据支撑。希望在条款公平的前提下续签——在建立竞争压力的同时明确表达这一意愿。

---

**主题：** `合同续签讨论 — {{our_company}} / {{supplier_name}} — {{contract_end}} 到期`

{{supplier_contact}}，

我方当前供应协议将于 {{contract_end}} 到期，我们希望就续签条款展开讨论。在过去 {{contract_duration}}，{{supplier_name}} 是值得信赖的合作伙伴，我们希望以具备商业竞争力的条款延续这一合作关系。

为搭建讨论框架，以下是我方对续签的看法：

**效果良好的方面：**
- 计费准确性与运营执行出色
- 市场情报更新对我方采购规划很有价值
- 客户管理团队响应迅速、积极主动

**希望改进的方面：**
- 我方当前 {{current_rate}} 的电价在签约时具备竞争力，但续签期（{{contract_start}} 至 {{new_contract_end}}）的远期曲线目前为 {{market_rate}} ——我们需要反映当前市场状况的续签定价
- 我们希望就 [分块指数结构 / 扩大的数量容差 / REC 捆绑] 展开讨论

**我方流程：**
我方正就此续签开展竞争性评估。我们已邀请 {{num_bidders}} 家供应商提供指示性报价。决策时间表：
- 指示性报价审查：{{pricing_review_date}}
- 短名单与最终谈判：{{negotiation_date}}
- 合同签署：{{execution_date}}

我们欢迎于 {{proposed_call_date}} 就 {{supplier_name}} 的续签方案进行电话沟通。请于 {{pricing_deadline}} 前按上述结构提交指示性报价。

{{our_contact_name}}
{{our_contact_title}}

---

**语气指引：**
- 提及竞争流程但不要虚张投标家数。
- 首先要肯定效果良好的方面——在位关系有其价值，应予承认。
- 保持时间表透明，以便供应商分配报价资源。

---

## 9. 监管备案意见

**渠道：** 向监管机构（FERC、州 PUC、ISO 利益相关方程序）提交书面意见
**受众：** 监管委员、ISO 市场设计团队
**语气：** 政策导向、基于证据。监管者尊重理解市场机制的评论者。

---

**关于：** {{docket_number}} — 拟议修订 {{program_or_rule}}

{{our_company}} 感谢有机会就 {{program_or_rule}} 的拟议修订发表意见。

作为 {{iso_name}} 辖区内年用电 {{annual_consumption_mwh}} 的大型商业和工业电力用户，{{our_company}} 对促进高效价格形成、可靠容量采购和公平成本分摊的市场设计有直接利益。

**支持/关切：**
{{our_company}} [支持 / 对] 拟议修订[存在关切]，具体如下：

1. **{{provision_1}}：** [立场与理由，特别说明该修订对工商业用户的影响]
2. **{{provision_2}}：** [立场与定量影响评估（如可获得）]
3. **{{provision_3}}：** [立场与替代方案（如反对）]

**建议：**
{{our_company}} 建议委员会 [附带条件批准 / 拒绝 / 暂缓待进一步分析] 拟议的 {{program_or_rule}} 修订，具体纳入以下修改：
- {{recommendation_1}}
- {{recommendation_2}}

此致，

{{our_contact_name}}
{{our_contact_title}}，{{our_company}}

---

## 10. 董事会级能源战略摘要

**渠道：** 董事会备忘录 / 演示文稿
**受众：** 董事会、CEO、CFO
**语气：** 战略导向、简洁、聚焦决策。董事会关心的是风险、成本轨迹、可持续承诺和资本配置——而非市场机制。

---

### 能源战略更新 — {{year}} 年第 {{quarter}} 季度

**呈 {{our_company}} 董事会**

**关键指标：**

| 指标 | 当前 | 目标 | 状态 |
|--------|---------|--------|--------|
| 年度能源支出 | ${{current_spend}} | ${{target_spend}} | {{spend_status}} |
| 能源成本占收入比 | {{energy_pct_revenue}}% | {{target_pct}}% | {{pct_status}} |
| 可再生电力（RE100） | {{re_pct_current}}% | {{re_target}} 年达 100% | {{re_status}} |
| 范围 2 排放（基于市场） | {{current_emissions}} 吨 CO₂e | {{target_emissions}} 吨 | {{emissions_status}} |

**战略优先级：**
1. **成本管理：** [1-2 句话总结采购策略与成果]
2. **可持续性：** [1-2 句话总结 RE100 进展与下一里程碑]
3. **风险管理：** [1-2 句话总结对冲头寸与市场展望]

**请求的决策：**
1. 批准与 {{ppa_project_name}} 签订 {{ppa_term_years}} 年期虚拟 PPA，执行价 {{ppa_strike_price}}，容量 {{ppa_capacity_mw}} MW —— 合同期内预计 NPV ${{ppa_npv}}，每年交付 {{ppa_annual_recs}} REC，支撑我方 RE100 承诺。
2. 授权 ${{capex_amount}} 资本支出，用于 {{capex_facilities}} 的电池储能 —— 预计 {{payback_years}} 年回本，叠加价值 ${{annual_savings}}/年（来自需量电费与容量成本削减）。

**风险摘要：**
- 市场风险：已对冲 {{hedge_pct}}%，对冲期至 {{hedge_end}}。未对冲敞口：按当前远期计 ${{unhedged_exposure}}。
- 监管风险：{{regulatory_summary}}
- 供应商风险：所有供应合同对手方均为投资级。无信用担忧。

**下次更新：** {{next_update_date}}

---

**语气指引：**
- 董事会沟通须控制在 2 页以内。详细材料以附件形式提供。
- 首先要列出"诉求"——如需董事会批准 PPA 或资本项目，应放在执行摘要。
- 一切都要量化。"可持续进展良好"毫无意义。"可再生占比 38%，按计划年底达 50%"才有意义。
- 明确承认风险。董事会若发现未被提及的风险，会失去对管理层的信任。
