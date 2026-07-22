---
name: odoo-security-rules
description: "Odoo 访问控制专家：ir.model.access.csv、记录规则（ir.rule）、用户组和多公司安全模式。当用户要求'Odoo权限配置'、'访问控制'、'ir.model.access'、'记录规则'或'多公司安全'时使用。"
risk: safe
source: "self"
---

# Odoo 安全规则

## 概述

Odoo 的安全管理分为两个层级：**模型级访问**（谁能读/写哪些模型）和**记录级规则**（用户能看到哪些记录）。本技能帮助你编写正确的 `ir.model.access.csv` 条目和基于 `ir.rule` 域的记录规则。

## 使用场景

- 为新自定义模块设置访问权限。
- 限制记录，使用户只能看到自己的数据或其公司的数据。
- 调试"Access Denied"或"You are not allowed to access"错误。
- 实现多公司记录可见性规则。

## 使用方法

1. **激活**：提及 `@odoo-security-rules` 并描述访问场景。
2. **生成**：获取正确的 CSV 访问行和 XML 记录规则。
3. **调试**：粘贴访问错误，获取诊断和修复方案。

## 示例

### 示例 1：ir.model.access.csv

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_hospital_patient_user,hospital.patient.user,model_hospital_patient,base.group_user,1,0,0,0
access_hospital_patient_manager,hospital.patient.manager,model_hospital_patient,base.group_erp_manager,1,1,1,1
```

> **注意：** 对 ERP 管理员使用 `base.group_erp_manager`，而非 `base.group_system` —— 该组保留给 Odoo 的技术超级用户。始终为模块特定的管理员角色创建自定义组：
>
> ```xml
> <record id="group_hospital_manager" model="res.groups">
>     <field name="name">Hospital Manager</field>
>     <field name="category_id" ref="base.module_category_hidden"/>
> </record>
> ```

### 示例 2：记录规则 — 用户只能看到自己的记录

```xml
<record id="rule_hospital_patient_own" model="ir.rule">
    <field name="name">Hospital Patient: Own Records Only</field>
    <field name="model_id" ref="model_hospital_patient"/>
    <field name="domain_force">[('create_uid', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="False"/>
</record>
```

> **重要：** 如果省略 `<field name="groups">`，规则将变为**全局**规则，适用于所有用户（包括管理员）。除非你明确需要全局限制，否则始终要指定用户组。

### 示例 3：多公司记录规则

```xml
<record id="rule_hospital_patient_company" model="ir.rule">
    <field name="name">Hospital Patient: Multi-Company</field>
    <field name="model_id" ref="model_hospital_patient"/>
    <field name="domain_force">
        ['|', ('company_id', '=', False),
               ('company_id', 'in', company_ids)]
    </field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>
```

## 最佳实践

- ✅ **推荐：** 从最严格的访问权限开始，按需逐步开放。
- ✅ **推荐：** 在多公司规则中使用 `company_ids`（复数形式）—— 它包含用户所属的所有公司。
- ✅ **推荐：** 使用非管理员用户在调试模式下测试规则 —— `sudo()` 会完全绕过所有记录规则。
- ✅ **推荐：** 为每个模块创建专用安全组，而不是复用 Odoo 核心组。
- ❌ **不要：** 给普通用户 `perm_unlink = 1` 权限，除非业务流程明确要求删除操作。
- ❌ **不要：** 在 `ir.model.access.csv` 中留空 `group_id`，除非你打算授予公共（未认证）访问权限。
- ❌ **不要：** 对模块管理员使用 `base.group_system` —— 这会授予包括服务器配置在内的完整技术访问权限。

## 局限性

- 不涵盖**字段级访问控制**（`ir.model.fields` 读/写限制）—— 这些需要自定义 OWL 或 Python 覆盖。
- **门户和公共用户**的访问规则有额外细节，此处未完全涵盖；使用 `base.group_portal` 时请仔细测试。
- 记录规则会被 `sudo()` **绕过** —— 在超级用户上下文中运行的代码会忽略所有 `ir.rule` 条目。
- 不涵盖**通过 PostgreSQL 的行级安全**（RLS）—— Odoo 在 ORM 层管理所有安全性。