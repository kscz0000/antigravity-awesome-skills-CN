---
name: odoo-project-timesheet
description: "Odoo 项目和工时表专家指南：任务阶段、计费时间跟踪、工时表审批、预算警报和工时表开票。当用户要求'配置Odoo项目工时表'或'设置工时审批流程'时使用。"
risk: safe
source: "self"
---

# Odoo 项目与工时表

## 概述

本技能帮助服务型企业、代理商和咨询公司配置 Odoo 项目和工时表。涵盖带预算的项目设置、任务阶段管理、员工工时记录、审批流程以及将已审批工时转换为客户发票。

## 使用场景

- 设置包含任务、截止日期和团队分配的新项目
- 按项目配置可计费与非计费时间跟踪
- 创建面向经理的工时表审批工作流
- 基于记录工时向客户开票（时间和材料计费）

## 工作原理

1. **激活**：提及 `@odoo-project-timesheet` 并描述您的项目或计费场景
2. **配置**：获取分步设置指南
3. **自动化**：获取从已审批工时表自动生成发票的指导

## 示例

### 示例 1：创建可计费项目

```text
Menu: Project → New Project (or the "+" button in Project view)

Name:     Website Redesign — Acme Corp
Customer: Acme Corporation
Billable: YES  (toggle ON)

Settings tab:
  Billing Type: Based on Timesheets (Time & Materials)
  Service Product: Consulting Hours ($150/hr)
  ☑ Timesheets
  ☑ Task Dependencies
  ☑ Subtasks

Budget:
  Planned Hours: 120 hours
  Budget Alert: at 80% (96 hrs) → notify project manager
```

### 示例 2：在任务中记录时间

```text
Method A — Directly inside the Task (recommended for accuracy):
  Open Task → Timesheets tab → Add a Line
  Employee:    John Doe
  Date:        Today
  Description: "Initial wireframes and site map" (required for clear invoices)
  Duration:    3:30  (3 hours 30 minutes)

Method B — Timesheets app (for end-of-day bulk entry):
  Menu: Timesheets → My Timesheets → New
  Project:  Website Redesign
  Task:     Wireframe Design
  Duration: 3:30
```

### 示例 3：启用开票前的工时表审批

```text
Menu: Timesheets → Configuration → Settings
  ☑ Timesheet Approval  (employees submit; managers approve)

Approval flow:
  1. Employee submits timesheet at week/month end
  2. Manager reviews: Timesheets → Managers → Timesheets to Approve
  3. Manager clicks "Approve" → entries are locked and billable
  4. Only approved entries flow into the invoice

If Approval is disabled, all logged hours are immediately billable.
```

### 示例 4：从工时表生成发票

```text
Step 1: Verify approved hours
  Menu: Timesheets → Managers → All Timesheets
  Filter: Billable = YES, Timesheet Invoice State = "To Invoice"

Step 2: Generate Invoice
  Menu: Sales → Orders → To Invoice → Timesheets  (v15/v16)
  or:   Accounting → Customers → Invoiceable Time  (v17)
  Filter by Customer: Acme Corporation
  Select entries → Create Invoices

Step 3: Invoice pre-populates with:
  Product: Consulting Hours
  Quantity: Sum of approved hours
  Unit Price: $150.00
  Total: Calculated automatically
```

## 最佳实践

- ✅ **推荐：** 启用**工时表审批**，确保只有经理审批的工时才会出现在客户发票上
- ✅ **推荐：** 设置**预算警报**为计划工时的 80%，以便项目经理在超支前及时介入
- ✅ **推荐：** 要求填写**工时描述**——发票上出现"完成工作"等模糊记录会破坏客户信任
- ✅ **推荐：** 使用**子任务**将工作拆分为细粒度单元，同时保持父任务在看板上可见
- ❌ **禁止：** 混合计费项目和内部项目而不加标签——这会破坏盈利能力和利用率报告
- ❌ **禁止：** 在项目本身（而非任务）上记录时间——无法按任务级别生成报告

## 限制

- **工时表审批**在某些 Odoo 版本中仅限企业版——请确认您的套餐包含此功能
- 不涵盖**项目预测**（资源容量规划）——需要企业版预测应用
- **时间和材料**计费适用于按小时计费，但不适合**固定价格项目**——此类项目请使用里程碑或手动发票行
- 在活跃项目-任务对之外记录的工时条目（如内部项目）无法直接分配给客户发票，需要自定义配置