---
name: mailtrap-managing-contacts
description: 管理 Mailtrap 联系人、列表、细分、自定义字段、导入、CRM 同步和营销活动受众，通过 UI 或 API 操作。触发词：Mailtrap联系人、联系人管理、联系人导入、联系人列表、联系人细分、CRM同步、营销受众
risk: critical
source: community
date_added: "2026-06-19"
---

# 管理 Mailtrap 联系人

## 概述

**在生成 API 请求体之前：** 查阅 [Contacts OpenAPI 规范](https://github.com/mailtrap/mailtrap-openapi/blob/main/specs/contacts.openapi.yml) 以获取当前字段名称、必需参数和嵌套结构。

**联系人**是营销数据库：列表、细分、自定义字段和导入，服务于**营销活动受众**及相关工作流。**Contacts API** 可自动化创建/更新联系人，并可对接 **CRM 或 CDP 同步**（由你的代码或 Zapier、Make、n8n 等工具实现——参见[导入联系人](https://docs.mailtrap.io/email-marketing/contacts/import-contacts.md)）。

**抑制列表**（硬退信、垃圾邮件投诉、**发送**端的退订）位于发送产品中，会**阻止**这些地址在你的流上的投递。这与决定谁有资格接收营销活动的**营销**过滤器（细分、列表成员资格、同意标记）是分开应用的。关于发送端的阻止，参见[抑制列表](https://docs.mailtrap.io/developers/email-sending/suppressions.md)和 `mailtrap-sending-emails`。

**相关技能：** `mailtrap-sending-emails`（实时发送路径）。

## 何时使用

- 编程式联系人管理（创建、更新、[批量导入](https://docs.mailtrap.io/developers/promotional/contacts/bulk-import.md)）
- 与 CRM 或数据仓库同步
- 联系人列表清理和 CSV 导入
- 使用**自定义字段**更新联系人或为[自动化](https://docs.mailtrap.io/email-marketing/automations.md)触发**自定义事件**
- 细分和[自定义字段](https://docs.mailtrap.io/email-marketing/contacts/custom-fields.md)用于受众构建

## 授权

以下所有端点需要 `Authorization: Bearer $MAILTRAP_API_TOKEN` 以及路径中的 `$MAILTRAP_ACCOUNT_ID`。通过 `GET https://mailtrap.io/api/accounts` 解析 `$MAILTRAP_ACCOUNT_ID`，并将令牌存储在环境变量或密钥管理器中。

## 端点（替换占位符）

| 操作                                   | 方法    | URL                                                                                       | 参考                                                                                            |
| -------------------------------------- | ------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| 创建 / 获取 / 更新 / 删除联系人         | various | `https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/contacts`                          | [Contacts](https://docs.mailtrap.io/developers/promotional/contacts/contacts.md)               |
| 批量导入（异步任务）                     | `POST`  | `https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/contacts/imports`                  | [Bulk import](https://docs.mailtrap.io/developers/promotional/contacts/bulk-import.md)         |
| 联系人列表                              | various | `https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/contacts/lists`                    | [Contact lists](https://docs.mailtrap.io/developers/promotional/contacts/contact-lists.md)     |
| 自定义字段                              | various | `https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/contacts/fields`                   | [Contact fields](https://docs.mailtrap.io/developers/promotional/contacts/contact-fields.md)   |
| 自定义事件                              | `POST`  | `https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/contacts/{contact_identifier}/events` | [Contact events](https://docs.mailtrap.io/developers/promotional/contacts/contact-events.md)   |
| 导出联系人                              | various | `https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/contacts/exports`                  | [Export contacts](https://docs.mailtrap.io/developers/promotional/contacts/export-contacts.md) |

- 速率限制（典型值）：每个账户每 60 秒 **200 个请求**——大量负载时请使用批量导入。
- **批量导入限制：** 每次导入请求最多 **50,000** 个联系人（异步任务）；使用 `GET .../contacts/imports/{import_id}` 轮询导入状态。参见[批量导入](https://docs.mailtrap.io/developers/promotional/contacts/bulk-import.md)。

## 示例（`curl`）

### 创建单个联系人（含自定义字段）

```bash
curl -X POST "https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/contacts" \
  -H "Authorization: Bearer $MAILTRAP_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "contact": {
      "email": "john.smith@example.com",
      "fields": {"first_name": "John", "last_name": "Smith", "company": "Example Inc"},
      "list_ids": [1, 2, 3]
    }
  }'
```

### 批量导入（联系人数组）

```bash
curl -X POST "https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/contacts/imports" \
  -H "Authorization: Bearer $MAILTRAP_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "contacts": [
      {"email": "user1@example.com", "fields": {"first_name": "John"}, "list_ids_included": [1, 2]},
      {"email": "user2@example.com", "fields": {"first_name": "Jane"}, "list_ids_included": [1]}
    ]
  }'
```

### 自定义事件（事件名称 + 载荷）

```bash
curl -X POST "https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/contacts/{contact_identifier}/events" \
  -H "Authorization: Bearer $MAILTRAP_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name": "UserLogin", "params": {"user_id": 101, "is_active": true}}'
```

## 概念

- **列表** — 显式定义的联系人列表。
- **细分** — 动态分组；参见[细分](https://docs.mailtrap.io/email-marketing/contacts/segments.md)。
- **自定义字段** — 如名字、姓氏或会员等级等属性；参见[自定义字段](https://docs.mailtrap.io/email-marketing/contacts/custom-fields.md)。
- **自定义事件** — 通过 `POST .../events` 发送事件 `name` 和 `params` 对象，用于[自动化](https://docs.mailtrap.io/email-marketing/automations.md)。

## CRM 与同步

- **API：** 适用于从 CRM 或数据库进行实时或定时同步。
- **无代码：** Zapier、Make.com、n8n，参见[导入联系人 – 第三方工具](https://docs.mailtrap.io/email-marketing/contacts/import-contacts.md)。

## 营销活动用例

联系人驱动**营销活动**：你在此维护干净的列表、同意状态和属性；营销活动创作和排期是产品功能，文档参见[营销活动](https://docs.mailtrap.io/email-marketing/campaigns.md)。

## 常见错误

| 错误                                     | 修正                                                              |
| ---------------------------------------- | ----------------------------------------------------------------- |
| 逐条创建联系人触发速率限制                | 对大批量使用 `/contacts/imports`（遵守每次请求 50k 限制）并退避   |
| 将营销联系人当作发送抑制列表处理          | 对发送流上的被阻止收件人使用**抑制列表**                          |

## 限制

- 联系人 API 结构可能变更；生成请求体前请查阅 Mailtrap 当前的 OpenAPI 规范。
