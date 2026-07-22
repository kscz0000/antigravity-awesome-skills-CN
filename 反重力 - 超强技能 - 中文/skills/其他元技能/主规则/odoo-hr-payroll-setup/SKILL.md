---
name: odoo-hr-payroll-setup
description: "Odoo HR 与薪资管理专家指南：工资结构、工资单规则、休假政策、员工合同及薪资记账凭证。当用户要求'配置Odoo薪资结构'、'设置工资单规则'、'排查工资计算错误'或'对接薪资与会计'时使用。"
risk: safe
source: "self"
---

# Odoo HR 与薪资管理配置

## 概述

本技能指导 HR 经理和薪资会计正确配置 Odoo HR 与薪资模块。涵盖工资结构创建（含 Python 计算规则）、休假政策、员工合同类型，以及薪资 → 会计的凭证过账流程。

## 适用场景

- 创建包含基本工资、扣款项和实发工资的薪资结构
- 配置年假、病假和法定假日政策
- 排查工资单金额错误或规则计算项缺失问题
- 设置薪资日记账以正确对接会计模块

## 使用方式

1. **激活**：输入 `@odoo-hr-payroll-setup` 并描述你的薪资场景
2. **配置**：获取工资规则和假期分配的分步配置指导
3. **调试**：粘贴工资规则或工资单问题，获取根因分析

## 示例

### 示例 1：带扣款的薪资结构

```text
Menu: Payroll → Configuration → Salary Structures → New

Name: US Employee Monthly
Payslip Code: MONTHLY

Rules (executed top-to-bottom — order matters):
  Code  | Name                   | Formula                        | Category
  ----- | ---------------------- | ------------------------------ | ---------
  BASIC | Basic Wage             | contract.wage                  | Basic
  GROSS | Gross                  | BASIC                          | Gross
  SS    | Social Security (6.2%) | -GROSS * 0.062                 | Deduction
  MED   | Medicare (1.45%)       | -GROSS * 0.0145                | Deduction
  FIT   | Federal Income Tax     | -GROSS * inputs.FIT_RATE.amount| Deduction
  NET   | Net Salary             | GROSS + SS + MED + FIT         | Net
```

> **联邦所得税：** Odoo 标准的美国本地化模块并未暴露单独的 `l10n_us_w4_rate` 字段。请使用 **输入项**（salary input type）为每位员工传入预扣税率，或安装社区版美国薪资模块（OCA `l10n_us_hr_payroll`），该模块能正确处理 W4 申报状态。

### 示例 2：配置休假类型

```text
Menu: Time Off → Configuration → Time Off Types → New

Name: Annual Leave / PTO
Approval: Time Off Officer
Leave Validation: Time Off Officer  (single approver)
  or: "Both" for HR + Manager double approval

Allocation:
  ☑ Employees can allocate time off themselves
  Requires approval: No

Negative Balance: Not allowed (employees cannot go negative)

Then create initial allocations:
Menu: Time Off → Managers → Allocations → New
  Employee: [Each employee]
  Time Off Type: Annual Leave / PTO
  Allocation: 15 days
  Validity: Jan 1 – Dec 31 [current year]
```

### 示例 3：薪资凭证过账结果

```text
After validating a payroll batch, Odoo generates:

Debit   Salary Expense Account     $5,000.00
  Credit  Social Security Payable     $310.00
  Credit  Medicare Payable             $72.50
  Credit  Federal Tax Payable         (varies)
  Credit  Salary Payable           $4,617.50+

When net salary is paid:
Debit   Salary Payable            $4,617.50
  Credit  Bank Account              $4,617.50

Employer taxes (e.g., FUTA, SUTA) post as separate journal entries.
```

## 最佳实践

- ✅ **推荐：** 在自定义规则前先安装对应国家的 **薪资本地化模块**（`l10n_us_hr_payroll`、`l10n_mx_hr_payroll` 等）——它提供预配置的税务结构
- ✅ **推荐：** 使用 **工资规则输入项**（`inputs.ALLOWANCE.amount`）传递变量值（奖金、津贴、预扣税率），而非在规则公式中硬编码
- ✅ **推荐：** 归档旧薪资结构而非删除——已生效的工资单会引用其结构，删除会导致工资单异常
- ✅ **推荐：** 生成工资单前，确保员工已关联有效的 **劳动合同**，且日期和薪资正确
- ❌ **禁止：** 手动编辑已过账的工资单——如需更正，请取消并重新生成工资单批次
- ❌ **禁止：** 在扣款规则中使用 `contract.wage` 却不核实结构是按月还是按年——务必检查合同工资周期

## 限制说明

- **Odoo 薪资模块仅限企业版**——社区版不包含薪资模块（`hr_payroll`）
- 美国合规功能（W2、941、州 SUI/SDI 申报）需要在基础本地化之外安装额外模块；Odoo 不直接生成税务申报表
- 不支持 **多国薪资**（不同国家的员工需要独立的薪资结构和本地化配置）
- 通过工资单处理 **费用报销**（如里程费、家庭办公补贴）需要自定义工资规则输入项，标准 HR 薪资文档中未涉及
