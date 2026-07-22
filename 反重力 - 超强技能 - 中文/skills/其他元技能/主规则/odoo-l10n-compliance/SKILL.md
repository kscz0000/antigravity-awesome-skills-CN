---
name: odoo-l10n-compliance
description: "各国 Odoo 本地化配置：税务设置、电子发票（CFDI、FatturaPA、SAF-T）、财务报告及国家会计科目表配置。当用户要求配置特定国家的 Odoo 本地化、电子发票或税务合规时使用。"
risk: unknown
source: community
---

# Odoo 本地化与合规 (l10n)

## 概述

Odoo 为 80 多个国家/地区提供本地化模块（`l10n_*`），可配置正确的会计科目表、税种和财务报告。本技能帮助您安装和配置适合的本地化模块，设置国家级电子发票功能（墨西哥 CFDI、意大利 FatturaPA、波兰 SAF-T），并确保财务合规性。

## 使用场景

- 为特定国家/地区的公司设置 Odoo（墨西哥、意大利、西班牙、美国等）。
- 配置国家级电子发票（向税务机关提交电子发票）。
- 设置 VAT/GST/IVA 税务规则和正确的财务位置。
- 生成所需的财务报告（增值税申报、SAF-T、DIAN 报告）。

## 使用方式

1. **激活**：提及 `@odoo-l10n-compliance` 并指定您的国家和 Odoo 版本。
2. **安装**：获取精确的本地化模块和配置步骤。
3. **配置**：接收税务代码设置、财务位置规则和报告指导。

## 国家/地区本地化模块

| 国家/地区 | 模块 | 主要功能 |
|---|---|---|
| 🇺🇸 美国 | `l10n_us` | GAAP 会计科目表、薪资（ADP 集成）、1099 报告 |
| 🇲🇽 墨西哥 | `l10n_mx_edi` | CFDI 4.0 电子发票、SAT 集成、IEPS 税 |
| 🇪🇸 西班牙 | `l10n_es` | SII 实时增值税、Modelo 303/390、AEAT |
| 🇮🇹 意大利 | `l10n_it_edi` | FatturaPA XML、SDI 提交、反向征收 |
| 🇵🇱 波兰 | `l10n_pl` | SAF-T JPK_FA、VAT-7 申报 |
| 🇧🇷 巴西 | `l10n_br` | NF-e、NFS-e、SPED、ICMS/PIS/COFINS |
| 🇩🇪 德国 | `l10n_de` | SKR03/SKR04 会计科目表、DATEV 导出、UStVA |
| 🇨🇴 哥伦比亚 | `l10n_co_edi` | DIAN 电子发票、UBL 2.1 |

## 示例

### 示例 1：配置墨西哥 CFDI 4.0

```
Step 1: Install module
  Apps → Search "Mexico" → Install "Mexico - Accounting"
  Also install: "Mexico - Electronic Invoicing" (l10n_mx_edi)

Step 2: Configure Company
  Settings → Company → [Your Company]
  Country: Mexico
  RFC: Your RFC number (tax ID)
  Company Type: Moral Person or Physical Person

Step 3: Upload SAT Certificates
  Accounting → Configuration → Certificates → New
  CSD Certificate (.cer file from SAT)
  Private Key (.key file from SAT)
  Password: Your FIEL password

Step 4: Issue a CFDI Invoice
  Create invoice → Confirm → CFDI XML generated automatically
  Sent to SAT → Receive UUID (folio fiscal)
  PDF includes QR code + UUID for buyer verification
```

### 示例 2：欧盟内部增值税设置（适用于任何欧盟国家）

```
Menu: Accounting → Configuration → Taxes → New

Tax Name: EU Intra-Community Sales (0%)
Tax Type: Sales
Tax Scope: Services or Goods
Tax Computation: Fixed
Amount: 0%
Tax Group: Intra-Community

Label on Invoice: "Intra-Community Supply - VAT Exempt per Art. 138 VAT Directive"

Fiscal Position (created separately):
  Name: EU B2B Intra-Community
  Auto-detect: Country Group = Europe + VAT Required = YES
  Tax Mapping: Standard VAT Rate → 0% Intra-Community
```

### 示例 3：安装和验证本地化模块

```bash
# Install via CLI (if module not in Apps)
./odoo-bin -d mydb --stop-after-init -i l10n_mx_edi

# Verify in Odoo:
# Apps → Installed → Search "l10n_mx" → Should show as Installed
```

## 最佳实践

- ✅ **推荐：**在创建任何会计分录**之前**安装本地化模块——它会设置正确的账户。
- ✅ **推荐：**使用**财务位置**自动切换国际客户的税务规则（B2B 对 B2C、国内对出口）。
- ✅ **推荐：**在 **SAT/税务机关测试环境**中测试电子发票，然后再上线。
- ❌ **避免：**如果您的国家有本地化模块，不要手动创建会计科目表。
- ❌ **避免：**不要将本地化税务账户与自定义账户混合——这会破坏财务报告。

## 限制条件

- 仅在任务明确符合上述范围时使用本技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
