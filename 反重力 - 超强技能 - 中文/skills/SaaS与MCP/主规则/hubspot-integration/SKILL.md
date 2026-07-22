---
name: hubspot-integration
description: HubSpot CRM 集成专家模式，涵盖 OAuth 认证、CRM 对象、关联关系、批量操作、Webhook 和自定义对象。适用于 Node.js 和 Python SDK。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# HubSpot 集成

HubSpot CRM 集成专家模式，涵盖 OAuth 认证、CRM 对象、关联关系、批量操作、Webhook 和自定义对象。适用于 Node.js 和 Python SDK。

## 模式

### OAuth 2.0 认证

公共应用的安全认证

**适用于**：构建公共应用或多账户集成

### 模板

// OAuth 2.0 flow for HubSpot
import { Client } from "@hubspot/api-client";

// Environment variables
const CLIENT_ID = process.env.HUBSPOT_CLIENT_ID;
const CLIENT_SECRET = process.env.HUBSPOT_CLIENT_SECRET;
const REDIRECT_URI = process.env.HUBSPOT_REDIRECT_URI;
const SCOPES = "crm.objects.contacts.read crm.objects.contacts.write";

// Step 1: Generate authorization URL
function getAuthUrl(): string {
  const authUrl = new URL("https://app.hubspot.com/oauth/authorize");
  authUrl.searchParams.set("client_id", CLIENT_ID);
  authUrl.searchParams.set("redirect_uri", REDIRECT_URI);
  authUrl.searchParams.set("scope", SCOPES);
  return authUrl.toString();
}

// Step 2: Handle OAuth callback
async function handleOAuthCallback(code: string) {
  const response = await fetch("https://api.hubapi.com/oauth/v1/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      redirect_uri: REDIRECT_URI,
      code: code,
    }),
  });

  const tokens = await response.json();
  // {
  //   access_token: "xxx",
  //   refresh_token: "xxx",
  //   expires_in: 1800  // 30 minutes
  // }

  // Store tokens securely
  await storeTokens(tokens);

  return tokens;
}

// Step 3: Refresh access token (before expiry)
async function refreshAccessToken(refreshToken: string) {
  const response = await fetch("https://api.hubapi.com/oauth/v1/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      refresh_token: refreshToken,
    }),
  });

  return response.json();
}

// Step 4: Create authenticated client
function createClient(accessToken: string): Client {
  const hubspotClient = new Client({ accessToken });
  return hubspotClient;
}

### 注意事项

- 访问令牌 30 分钟后过期
- 在过期前刷新令牌
- 安全存储刷新令牌
- 每 6 个月轮换令牌

### 私有应用令牌

单账户集成的认证方式

**适用于**：为单个 HubSpot 账户构建内部集成

### 模板

// Private App Token - simpler for single account
import { Client } from "@hubspot/api-client";

// Create client with private app token
const hubspotClient = new Client({
  accessToken: process.env.HUBSPOT_PRIVATE_APP_TOKEN,
});

// Private app tokens don't expire
// But should be rotated every 6 months for security

// Example: Get contacts
async function getContacts() {
  try {
    const response = await hubspotClient.crm.contacts.basicApi.getPage(
      100,  // limit
      undefined,  // after cursor
      ["firstname", "lastname", "email", "phone"],  // properties
    );

    return response.results;
  } catch (error) {
    if (error.code === 429) {
      // Rate limited - implement backoff
      const retryAfter = error.headers?.["retry-after"] || 10;
      await sleep(retryAfter * 1000);
      return getContacts();
    }
    throw error;
  }
}

// Python equivalent
// from hubspot import HubSpot
//
// client = HubSpot(access_token=os.environ["HUBSPOT_PRIVATE_APP_TOKEN"])
//
// contacts = client.crm.contacts.basic_api.get_page(
//     limit=100,
//     properties=["firstname", "lastname", "email"]
// )

### 注意事项

- 私有应用令牌不会过期
- 所有私有应用共享每日速率限制
- 每个私有应用有独立的突发限制
- 建议：每 6 个月轮换一次

### CRM 对象 CRUD 操作

创建、读取、更新、删除 CRM 记录

**适用于**：处理联系人、公司、交易、工单

### 模板

import { Client } from "@hubspot/api-client";

const hubspotClient = new Client({
  accessToken: process.env.HUBSPOT_TOKEN,
});

// CREATE contact
async function createContact(data: {
  email: string;
  firstname: string;
  lastname: string;
}) {
  const response = await hubspotClient.crm.contacts.basicApi.create({
    properties: {
      email: data.email,
      firstname: data.firstname,
      lastname: data.lastname,
    },
  });

  return response;
}

// READ contact by ID
async function getContact(contactId: string) {
  const response = await hubspotClient.crm.contacts.basicApi.getById(
    contactId,
    ["firstname", "lastname", "email", "phone", "company"],
  );

  return response;
}

// UPDATE contact
async function updateContact(contactId: string, properties: object) {
  const response = await hubspotClient.crm.contacts.basicApi.update(
    contactId,
    { properties },
  );

  return response;
}

// DELETE contact
async function deleteContact(contactId: string) {
  await hubspotClient.crm.contacts.basicApi.archive(contactId);
}

// SEARCH contacts
async function searchContacts(query: string) {
  const response = await hubspotClient.crm.contacts.searchApi.doSearch({
    query,
    limit: 100,
    properties: ["firstname", "lastname", "email"],
    sorts: [{ propertyName: "createdate", direction: "DESCENDING" }],
  });

  return response.results;
}

// LIST with pagination
async function getAllContacts() {
  const allContacts = [];
  let after = undefined;

  do {
    const response = await hubspotClient.crm.contacts.basicApi.getPage(
      100,
      after,
      ["firstname", "lastname", "email"],
    );

    allContacts.push(...response.results);
    after = response.paging?.next?.after;
  } while (after);

  return allContacts;
}

### 注意事项

- 使用 properties 参数仅获取所需字段
- 搜索 API 有 1 万条结果限制
- 列表查询务必实现分页
- 支持归档（软删除）和 GDPR 删除

### 批量操作

高效创建、更新或读取多条记录

**适用于**：处理多条记录（减少速率限制消耗）

### 模板

import { Client } from "@hubspot/api-client";

const hubspotClient = new Client({
  accessToken: process.env.HUBSPOT_TOKEN,
});

// BATCH CREATE contacts (up to 100 per batch)
async function batchCreateContacts(contacts: Array<{
  email: string;
  firstname: string;
  lastname: string;
}>) {
  const inputs = contacts.map((contact) => ({
    properties: {
      email: contact.email,
      firstname: contact.firstname,
      lastname: contact.lastname,
    },
  }));

  const response = await hubspotClient.crm.contacts.batchApi.create({
    inputs,
  });

  return response.results;
}

// BATCH UPDATE contacts
async function batchUpdateContacts(
  updates: Array<{ id: string; properties: object }>
) {
  const inputs = updates.map(({ id, properties }) => ({
    id,
    properties,
  }));

  const response = await hubspotClient.crm.contacts.batchApi.update({
    inputs,
  });

  return response.results;
}

// BATCH READ contacts by ID
async function batchReadContacts(
  ids: string[],
  properties: string[] = ["firstname", "lastname", "email"]
) {
  const response = await hubspotClient.crm.contacts.batchApi.read({
    inputs: ids.map((id) => ({ id })),
    properties,
  });

  return response.results;
}

// BATCH ARCHIVE contacts
async function batchDeleteContacts(ids: string[]) {
  await hubspotClient.crm.contacts.batchApi.archive({
    inputs: ids.map((id) => ({ id })),
  });
}

// Process large dataset in chunks
async function processLargeDataset(allContacts: any[]) {
  const BATCH_SIZE = 100;
  const results = [];

  for (let i = 0; i < allContacts.length; i += BATCH_SIZE) {
    const batch = allContacts.slice(i, i + BATCH_SIZE);
    const batchResults = await batchCreateContacts(batch);
    results.push(...batchResults);

    // Respect rate limits - wait between batches
    if (i + BATCH_SIZE < allContacts.length) {
      await sleep(100);  // 100ms between batches
    }
  }

  return results;
}

### 注意事项

- 每批次最多 100 条记录
- 可节省高达 80% 的速率限制配额
- 批量操作按记录原子执行（可能部分成功）
- 检查 response.errors 获取失败记录

### 关联关系 v4 API

在 CRM 记录之间创建关系

**适用于**：将联系人关联到公司、交易等

### 模板

import { Client, AssociationTypes } from "@hubspot/api-client";

const hubspotClient = new Client({
  accessToken: process.env.HUBSPOT_TOKEN,
});

// CREATE association (Contact to Company)
async function associateContactToCompany(
  contactId: string,
  companyId: string
) {
  await hubspotClient.crm.associations.v4.basicApi.create(
    "contacts",
    contactId,
    "companies",
    companyId,
    [
      {
        associationCategory: "HUBSPOT_DEFINED",
        associationTypeId: AssociationTypes.contactToCompany,
      },
    ]
  );
}

// CREATE association (Deal to Contact)
async function associateDealToContact(dealId: string, contactId: string) {
  await hubspotClient.crm.associations.v4.basicApi.create(
    "deals",
    dealId,
    "contacts",
    contactId,
    [
      {
        associationCategory: "HUBSPOT_DEFINED",
        associationTypeId: 3,  // deal_to_contact
      },
    ]
  );
}

// GET associations for a record
async function getContactCompanies(contactId: string) {
  const response = await hubspotClient.crm.associations.v4.basicApi.getPage(
    "contacts",
    contactId,
    "companies",
    undefined,
    500
  );

  return response.results;
}

// CREATE association with custom label
async function createLabeledAssociation(
  contactId: string,
  companyId: string,
  labelId: number  // Custom association label ID
) {
  await hubspotClient.crm.associations.v4.basicApi.create(
    "contacts",
    contactId,
    "companies",
    companyId,
    [
      {
        associationCategory: "USER_DEFINED",
        associationTypeId: labelId,
      },
    ]
  );
}

// BATCH create associations
async function batchAssociateContactsToCompany(
  contactIds: string[],
  companyId: string
) {
  const inputs = contactIds.map((contactId) => ({
    _from: { id: contactId },
    to: { id: companyId },
    types: [
      {
        associationCategory: "HUBSPOT_DEFINED",
        associationTypeId: AssociationTypes.contactToCompany,
      },
    ],
  }));

  await hubspotClient.crm.associations.v4.batchApi.create(
    "contacts",
    "companies",
    { inputs }
  );
}

// Common association type IDs
// Contact to Company: 1
// Company to Contact: 2
// Deal to Contact: 3
// Contact to Deal: 4
// Deal to Company: 5
// Company to Deal: 6

### 注意事项

- 需要 SDK 9.0.0+ 版本支持 v4 API
- 关联标签支持自定义关系
- 多个关联使用批量 API
- HUBSPOT_DEFINED 用于标准关联，USER_DEFINED 用于自定义标签

### Webhook 处理

接收 HubSpot 实时通知

**适用于**：需要 CRM 变更的即时更新

### 模板

import crypto from "crypto";
import { Client } from "@hubspot/api-client";

// Webhook signature validation
function validateWebhookSignature(
  requestBody: string,
  signature: string,
  clientSecret: string
): boolean {
  // For v2 signature (most common)
  const expectedSignature = crypto
    .createHmac("sha256", clientSecret)
    .update(requestBody)
    .digest("hex");

  return signature === expectedSignature;
}

// Express webhook handler
app.post("/webhooks/hubspot", async (req, res) => {
  const signature = req.headers["x-hubspot-signature-v3"] as string;
  const timestamp = req.headers["x-hubspot-request-timestamp"] as string;
  const requestBody = JSON.stringify(req.body);

  // Validate signature
  const isValid = validateWebhookSignature(
    requestBody,
    signature,
    process.env.HUBSPOT_CLIENT_SECRET
  );

  if (!isValid) {
    console.error("Invalid webhook signature");
    return res.status(401).send("Unauthorized");
  }

  // Check timestamp (prevent replay attacks)
  const timestampAge = Date.now() - parseInt(timestamp);
  if (timestampAge > 300000) {  // 5 minutes
    console.error("Webhook timestamp too old");
    return res.status(401).send("Timestamp expired");
  }

  // Process events - respond quickly!
  const events = req.body;

  // Queue for async processing
  for (const event of events) {
    await queue.add("hubspot-webhook", event);
  }

  // Respond immediately
  res.status(200).send("OK");
});

// Async processor
async function processWebhookEvent(event: any) {
  const { subscriptionType, objectId, propertyName, propertyValue } = event;

  switch (subscriptionType) {
    case "contact.creation":
      await handleContactCreated(objectId);
      break;

    case "contact.propertyChange":
      await handleContactPropertyChange(objectId, propertyName, propertyValue);
      break;

    case "deal.creation":
      await handleDealCreated(objectId);
      break;

    case "contact.deletion":
      await handleContactDeleted(objectId);
      break;

    default:
      console.log(`Unhandled event: ${subscriptionType}`);
  }
}

// Webhook subscription types:
// contact.creation, contact.deletion, contact.propertyChange
// company.creation, company.deletion, company.propertyChange
// deal.creation, deal.deletion, deal.propertyChange

### 注意事项

- 处理前验证签名
- 5 秒内响应
- 耗时操作放入队列异步处理
- 每个应用最多 1000 个 Webhook 订阅

### 自定义对象

创建和管理自定义对象类型

**适用于**：标准对象不满足数据模型需求

### 模板

import { Client } from "@hubspot/api-client";

const hubspotClient = new Client({
  accessToken: process.env.HUBSPOT_TOKEN,
});

// CREATE custom object schema
async function createCustomObjectSchema() {
  const schema = {
    name: "projects",
    labels: {
      singular: "Project",
      plural: "Projects",
    },
    primaryDisplayProperty: "project_name",
    requiredProperties: ["project_name"],
    properties: [
      {
        name: "project_name",
        label: "Project Name",
        type: "string",
        fieldType: "text",
      },
      {
        name: "status",
        label: "Status",
        type: "enumeration",
        fieldType: "select",
        options: [
          { label: "Active", value: "active" },
          { label: "Completed", value: "completed" },
          { label: "On Hold", value: "on_hold" },
        ],
      },
      {
        name: "budget",
        label: "Budget",
        type: "number",
        fieldType: "number",
      },
      {
        name: "start_date",
        label: "Start Date",
        type: "date",
        fieldType: "date",
      },
    ],
    associatedObjects: ["CONTACT", "COMPANY"],
  };

  const response = await hubspotClient.crm.schemas.coreApi.create(schema);
  return response;
}

// CREATE custom object record
async function createProject(data: {
  project_name: string;
  status: string;
  budget: number;
}) {
  const response = await hubspotClient.crm.objects.basicApi.create(
    "projects",  // Custom object name
    { properties: data }
  );

  return response;
}

// READ custom object by ID
async function getProject(projectId: string) {
  const response = await hubspotClient.crm.objects.basicApi.getById(
    "projects",
    projectId,
    ["project_name", "status", "budget", "start_date"]
  );

  return response;
}

// UPDATE custom object
async function updateProject(projectId: string, properties: object) {
  const response = await hubspotClient.crm.objects.basicApi.update(
    "projects",
    projectId,
    { properties }
  );

  return response;
}

// SEARCH custom objects
async function searchProjects(status: string) {
  const response = await hubspotClient.crm.objects.searchApi.doSearch(
    "projects",
    {
      filterGroups: [
        {
          filters: [
            {
              propertyName: "status",
              operator: "EQ",
              value: status,
            },
          ],
        },
      ],
      properties: ["project_name", "status", "budget"],
      limit: 100,
    }
  );

  return response.results;
}

### 注意事项

- 自定义对象需要企业版
- 每个账户最多 10 个自定义对象
- 使用 crm.objects API，对象名称作为参数
- 可与标准对象和其他自定义对象关联

## 陷阱

### 速率限制因应用类型和 Hub 版本而异

严重程度：高

### 市场应用 5% 错误率阈值

严重程度：高

### API 密钥已弃用 - 使用 OAuth 或私有应用令牌

严重程度：严重

### OAuth 访问令牌 30 分钟后过期

严重程度：高

### Webhook 请求必须验证

严重程度：严重

### 所有列表端点需要分页

严重程度：中

### 关联关系 v4 API 有破坏性变更

严重程度：高

### 轮询限制为每日 10 万次请求

严重程度：中

## 验证检查

### 硬编码 HubSpot API 密钥

严重程度：错误

API 密钥绝不能硬编码

消息：检测到硬编码的 HubSpot API 密钥。请使用环境变量。注意：API 密钥已弃用，请使用私有应用令牌。

### 硬编码 HubSpot 访问令牌

严重程度：错误

访问令牌必须使用环境变量

消息：硬编码的 HubSpot 访问令牌。请使用环境变量。

### 硬编码客户端密钥

严重程度：错误

OAuth 客户端密钥必须安全存储

消息：硬编码的客户端密钥。请使用环境变量。

### 缺少 Webhook 签名验证

严重程度：错误

Webhook 端点必须验证 HubSpot 签名

消息：Webhook 端点缺少签名验证。请验证 X-HubSpot-Signature-v3。

### 缺少速率限制处理

严重程度：警告

API 调用应处理 429 响应

消息：HubSpot API 调用缺少速率限制处理。请实现带退避的重试逻辑。

### 未限流的并行 API 调用

严重程度：警告

并行调用可能超出速率限制

消息：并行 HubSpot API 调用未限流。请使用速率限制器。

### 列表调用缺少分页

严重程度：警告

列表端点返回分页结果

消息：API 调用缺少分页处理。请实现基于游标的分页。

### 循环中的单个操作

严重程度：信息

多条记录应使用批量操作

消息：循环中的单个 API 调用。建议使用批量操作以提升性能。

### 令牌存储未记录过期时间

严重程度：警告

OAuth 令牌会过期，需要刷新逻辑

消息：令牌存储未记录过期时间。请存储 expiresAt 用于刷新逻辑。

### 使用已弃用的 API 密钥

严重程度：错误

API 密钥已弃用

消息：正在使用已弃用的 API 密钥。请迁移到私有应用令牌或 OAuth 2.0。

## 协作

### 委托触发条件

- 用户需要邮件营销自动化 → email-marketing（超出 HubSpot 内置邮件工具范围）
- 用户需要自定义 CRM UI → frontend（构建门户或仪表盘）
- 用户需要数据管道 → data-engineer（从 HubSpot 到数仓的 ETL）
- 用户需要 Salesforce 集成 → salesforce-development（HubSpot + Salesforce 同步）
- 用户需要支付处理 → stripe-integration（超出 HubSpot 报价单的支付功能）
- 用户需要分析仪表盘 → analytics-specialist（超出 HubSpot 的自定义报表）

## 适用场景
- 用户提及或暗示：hubspot
- 用户提及或暗示：hubspot api
- 用户提及或暗示：hubspot crm
- 用户提及或暗示：hubspot integration
- 用户提及或暗示：contacts api

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 输出内容不能替代环境特定的验证、测试或专家评审。
- 若缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清。
