---
name: salesforce-development
description: Salesforce 平台开发专家模式，涵盖 Lightning Web Components (LWC)、Apex 触发器和类、REST/Bulk API、Connected Apps，以及 Salesforce DX 的 Scratch Org 和第二代包（2GP）。触发词：salesforce、sfdc、apex、lwc、lightning web components、sfdx、scratch org、visualforce、soql、governor limits、connected app
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Salesforce 开发

Salesforce 平台开发专家模式，涵盖 Lightning Web Components (LWC)、Apex 触发器和类、REST/Bulk API、Connected Apps，以及 Salesforce DX 的 Scratch Org 和第二代包（2GP）。

## 模式

### 使用 Wire Service 的 Lightning Web Component

使用 @wire 装饰器与 Lightning Data Service 或 Apex 方法进行响应式数据绑定。@wire 契合 LWC 的响应式架构，可利用 Salesforce 的性能优化能力。

// myComponent.js
import { LightningElement, wire, api } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import getRelatedRecords from '@salesforce/apex/MyController.getRelatedRecords';
import ACCOUNT_NAME from '@salesforce/schema/Account.Name';
import ACCOUNT_INDUSTRY from '@salesforce/schema/Account.Industry';

const FIELDS = [ACCOUNT_NAME, ACCOUNT_INDUSTRY];

export default class MyComponent extends LightningElement {
  @api recordId;  // 从父组件或记录页面传入

  // 绑定到 Lightning Data Service（单条记录首选方案）
  @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
  account;

  // 绑定到 Apex 方法（复杂查询场景）
  @wire(getRelatedRecords, { accountId: '$recordId' })
  wiredRecords({ error, data }) {
    if (data) {
      this.relatedRecords = data;
      this.error = undefined;
    } else if (error) {
      this.error = error;
      this.relatedRecords = undefined;
    }
  }

  get accountName() {
    return getFieldValue(this.account.data, ACCOUNT_NAME);
  }

  get isLoading() {
    return !this.account.data && !this.account.error;
  }

  // 响应式：修改 recordId 会自动重新获取数据
}

// myComponent.html
<template>
  <lightning-card title={accountName}>
    <template if:true={isLoading}>
      <lightning-spinner alternative-text="Loading"></lightning-spinner>
    </template>

    <template if:true={account.data}>
      <p>Industry: {industry}</p>
    </template>

    <template if:true={error}>
      <p class="slds-text-color_error">{error.body.message}</p>
    </template>
  </lightning-card>
</template>

// MyController.cls
public with sharing class MyController {
  @AuraEnabled(cacheable=true)
  public static List<Contact> getRelatedRecords(Id accountId) {
    return [
      SELECT Id, Name, Email, Phone
      FROM Contact
      WHERE AccountId = :accountId
      WITH SECURITY_ENFORCED
      LIMIT 100
    ];
  }
}

### 上下文

- 构建 LWC 组件
- 获取 Salesforce 数据
- 响应式 UI

### 批量化 Apex 触发器与 Handler 模式

Apex 触发器必须支持批量化处理，单次事务可处理 200+ 条记录。使用 handler 模式实现关注点分离、可测试性和递归防护。

// AccountTrigger.trigger
trigger AccountTrigger on Account (
  before insert, before update, before delete,
  after insert, after update, after delete, after undelete
) {
  new AccountTriggerHandler().run();
}

// TriggerHandler.cls（基类）
public virtual class TriggerHandler {
  // 递归防护
  private static Set<String> executedHandlers = new Set<String>();

  public void run() {
    String handlerName = String.valueOf(this).split(':')[0];

    // 防止递归
    String contextKey = handlerName + '_' + Trigger.operationType;
    if (executedHandlers.contains(contextKey)) {
      return;
    }
    executedHandlers.add(contextKey);

    switch on Trigger.operationType {
      when BEFORE_INSERT { this.beforeInsert(); }
      when BEFORE_UPDATE { this.beforeUpdate(); }
      when BEFORE_DELETE { this.beforeDelete(); }
      when AFTER_INSERT { this.afterInsert(); }
      when AFTER_UPDATE { this.afterUpdate(); }
      when AFTER_DELETE { this.afterDelete(); }
      when AFTER_UNDELETE { this.afterUndelete(); }
    }
  }

  // 子类中重写
  protected virtual void beforeInsert() {}
  protected virtual void beforeUpdate() {}
  protected virtual void beforeDelete() {}
  protected virtual void afterInsert() {}
  protected virtual void afterUpdate() {}
  protected virtual void afterDelete() {}
  protected virtual void afterUndelete() {}
}

// AccountTriggerHandler.cls
public class AccountTriggerHandler extends TriggerHandler {
  private List<Account> newAccounts;
  private List<Account> oldAccounts;
  private Map<Id, Account> newMap;
  private Map<Id, Account> oldMap;

  public AccountTriggerHandler() {
    this.newAccounts = (List<Account>) Trigger.new;
    this.oldAccounts = (List<Account>) Trigger.old;
    this.newMap = (Map<Id, Account>) Trigger.newMap;
    this.oldMap = (Map<Id, Account>) Trigger.oldMap;
  }

  protected override void afterInsert() {
    createDefaultContacts();
    notifySlack();
  }

  protected override void afterUpdate() {
    handleIndustryChange();
  }

  // 批量化：一次查询，一次更新
  private void createDefaultContacts() {
    List<Contact> contactsToInsert = new List<Contact>();

    for (Account acc : newAccounts) {
      if (acc.Type == 'Prospect') {
        contactsToInsert.add(new Contact(
          AccountId = acc.Id,
          LastName = 'Primary Contact',
          Email = 'contact@' + acc.Website
        ));
      }
    }

    if (!contactsToInsert.isEmpty()) {
      insert contactsToInsert;  // 单次 DML 处理所有记录
    }
  }

  private void handleIndustryChange() {
    Set<Id> changedAccountIds = new Set<Id>();

    for (Account acc : newAccounts) {
      Account oldAcc = oldMap.get(acc.Id);
      if (acc.Industry != oldAcc.Industry) {
        changedAccountIds.add(acc.Id);
      }
    }

    if (!changedAccountIds.isEmpty()) {
      // 将重量级操作排入异步队列
      System.enqueueJob(new IndustryChangeQueueable(changedAccountIds));
    }
  }

  private void notifySlack() {
    // 将 callout 卸载到异步
    List<Id> accountIds = new List<Id>(newMap.keySet());
    System.enqueueJob(new SlackNotificationQueueable(accountIds));
  }
}

### 上下文

- Apex 触发器
- 数据操作
- 自动化

### Queueable Apex 异步处理

使用 Queueable Apex 进行异步处理，支持非原始类型、通过 AsyncApexJob 监控，以及作业链式调用。限制：单次事务最多 50 个作业，链式调用时仅限 1 个子作业。

// IndustryChangeQueueable.cls
public class IndustryChangeQueueable implements Queueable, Database.AllowsCallouts {
  private Set<Id> accountIds;
  private Integer retryCount;

  public IndustryChangeQueueable(Set<Id> accountIds) {
    this(accountIds, 0);
  }

  public IndustryChangeQueueable(Set<Id> accountIds, Integer retryCount) {
    this.accountIds = accountIds;
    this.retryCount = retryCount;
  }

  public void execute(QueueableContext context) {
    try {
      // 使用最新数据查询
      List<Account> accounts = [
        SELECT Id, Name, Industry, OwnerId
        FROM Account
        WHERE Id IN :accountIds
        WITH SECURITY_ENFORCED
      ];

      // 处理并发起 callout
      for (Account acc : accounts) {
        syncToExternalSystem(acc);
      }

      // 更新记录
      updateRelatedOpportunities(accountIds);

    } catch (Exception e) {
      handleError(e);
    }
  }

  private void syncToExternalSystem(Account acc) {
    HttpRequest req = new HttpRequest();
    req.setEndpoint('callout:ExternalCRM/accounts');
    req.setMethod('POST');
    req.setHeader('Content-Type', 'application/json');
    req.setBody(JSON.serialize(new Map<String, Object>{
      'salesforceId' => acc.Id,
      'name' => acc.Name,
      'industry' => acc.Industry
    }));

    Http http = new Http();
    HttpResponse res = http.send(req);

    if (res.getStatusCode() != 200 && res.getStatusCode() != 201) {
      throw new CalloutException('Sync failed: ' + res.getBody());
    }
  }

  private void updateRelatedOpportunities(Set<Id> accIds) {
    List<Opportunity> oppsToUpdate = [
      SELECT Id, Industry__c, AccountId
      FROM Opportunity
      WHERE AccountId IN :accIds
      WITH SECURITY_ENFORCED
    ];

    Map<Id, Account> accountMap = new Map<Id, Account>([
      SELECT Id, Industry FROM Account WHERE Id IN :accIds
    ]);

    for (Opportunity opp : oppsToUpdate) {
      opp.Industry__c = accountMap.get(opp.AccountId).Industry;
    }

    if (!oppsToUpdate.isEmpty()) {
      update oppsToUpdate;
    }
  }

  private void handleError(Exception e) {
    // 记录错误日志
    System.debug(LoggingLevel.ERROR, 'Queueable failed: ' + e.getMessage());

    // 指数退避重试（最多 3 次）
    if (retryCount < 3) {
      // 链式调度新作业进行重试
      System.enqueueJob(new IndustryChangeQueueable(accountIds, retryCount + 1));
    } else {
      // 创建错误记录用于监控
      insert new Integration_Error__c(
        Type__c = 'Industry Sync',
        Message__c = e.getMessage(),
        Stack_Trace__c = e.getStackTraceString(),
        Record_Ids__c = String.join(new List<Id>(accountIds), ',')
      );
    }
  }
}

### 上下文

- 异步处理
- 长时间运行操作
- 触发器中的 callout

### 使用 Connected App 的 REST API 集成

外部集成使用 Connected App 配合 OAuth 2.0。JWT Bearer 流程用于服务端到服务端通信，Web Server 流程用于面向用户的应用。始终使用 Named Credentials 进行安全的 callout 配置。

// Node.js - JWT Bearer 流程（服务端到服务端）
import jwt from 'jsonwebtoken';
import fs from 'fs';

class SalesforceClient {
  private accessToken: string | null = null;
  private instanceUrl: string | null = null;
  private tokenExpiry: number = 0;

  constructor(
    private clientId: string,
    private username: string,
    private privateKeyPath: string,
    private loginUrl: string = 'https://login.salesforce.com'
  ) {}

  async authenticate(): Promise<void> {
    // 检查 token 是否仍有效（预留 5 分钟缓冲）
    if (this.accessToken && Date.now() < this.tokenExpiry - 300000) {
      return;
    }

    const privateKey = fs.readFileSync(this.privateKeyPath, 'utf8');

    // 创建 JWT 断言
    const claim = {
      iss: this.clientId,
      sub: this.username,
      aud: this.loginUrl,
      exp: Math.floor(Date.now() / 1000) + 300  // 5 分钟
    };

    const assertion = jwt.sign(claim, privateKey, { algorithm: 'RS256' });

    // 用 JWT 换取访问令牌
    const response = await fetch(`${this.loginUrl}/services/oauth2/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        assertion
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Auth failed: ${error.error_description}`);
    }

    const data = await response.json();
    this.accessToken = data.access_token;
    this.instanceUrl = data.instance_url;
    this.tokenExpiry = Date.now() + 7200000;  // 2 小时
  }

  async query(soql: string): Promise<any> {
    await this.authenticate();

    const response = await fetch(
      `${this.instanceUrl}/services/data/v59.0/query?q=${encodeURIComponent(soql)}`,
      {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        }
      }
    );

    if (!response.ok) {
      await this.handleError(response);
    }

    return response.json();
  }

  async createRecord(sobject: string, data: object): Promise<any> {
    await this.authenticate();

    const response = await fetch(
      `${this.instanceUrl}/services/data/v59.0/sobjects/${sobject}`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      }
    );

    if (!response.ok) {
      await this.handleError(response);
    }

    return response.json();
  }

  private async handleError(response: Response): Promise<never> {
    const error = await response.json();

    if (response.status === 401) {
      // 令牌已过期，清除并重试
      this.accessToken = null;
      throw new Error('Session expired, retry required');
    }

    throw new Error(`API Error: ${JSON.stringify(error)}`);
  }
}

// 使用示例
const sf = new SalesforceClient(
  process.env.SF_CLIENT_ID!,
  process.env.SF_USERNAME!,
  './certificates/server.key'
);

const accounts = await sf.query(
  "SELECT Id, Name FROM Account WHERE CreatedDate = TODAY"
);

### 上下文

- 外部集成
- REST API 访问
- Connected Apps

### Bulk API 2.0 大规模数据操作

对 10K+ 条记录的操作使用 Bulk API 2.0。基于作业的异步处理工作流。属于 REST API 的一部分，相比原版 Bulk API 接口更精简。

// Node.js - Bulk API 2.0 批量插入
class SalesforceBulkClient extends SalesforceClient {

  async bulkInsert(sobject: string, records: object[]): Promise<any> {
    await this.authenticate();

    // 步骤 1：创建作业
    const job = await this.createBulkJob(sobject, 'insert');

    try {
      // 步骤 2：上传数据（CSV 格式）
      await this.uploadJobData(job.id, records);

      // 步骤 3：关闭作业以启动处理
      await this.closeJob(job.id);

      // 步骤 4：轮询等待完成
      return await this.waitForJobCompletion(job.id);

    } catch (error) {
      // 出错时中止作业
      await this.abortJob(job.id);
      throw error;
    }
  }

  private async createBulkJob(sobject: string, operation: string): Promise<any> {
    const response = await fetch(
      `${this.instanceUrl}/services/data/v59.0/jobs/ingest`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          object: sobject,
          operation,
          contentType: 'CSV',
          lineEnding: 'LF'
        })
      }
    );

    return response.json();
  }

  private async uploadJobData(jobId: string, records: object[]): Promise<void> {
    // 转换为 CSV
    const csv = this.recordsToCSV(records);

    await fetch(
      `${this.instanceUrl}/services/data/v59.0/jobs/ingest/${jobId}/batches`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'text/csv'
        },
        body: csv
      }
    );
  }

  private async closeJob(jobId: string): Promise<void> {
    await fetch(
      `${this.instanceUrl}/services/data/v59.0/jobs/ingest/${jobId}`,
      {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ state: 'UploadComplete' })
      }
    );
  }

  private async waitForJobCompletion(jobId: string): Promise<any> {
    const maxWaitTime = 10 * 60 * 1000;  // 10 分钟
    const pollInterval = 5000;  // 5 秒
    const startTime = Date.now();

    while (Date.now() - startTime < maxWaitTime) {
      const response = await fetch(
        `${this.instanceUrl}/services/data/v59.0/jobs/ingest/${jobId}`,
        {
          headers: { 'Authorization': `Bearer ${this.accessToken}` }
        }
      );

      const job = await response.json();

      if (job.state === 'JobComplete') {
        // 获取结果
        return {
          success: job.numberRecordsProcessed - job.numberRecordsFailed,
          failed: job.numberRecordsFailed,
          failedResults: job.numberRecordsFailed > 0
            ? await this.getFailedResults(jobId)
            : []
        };
      }

      if (job.state === 'Failed' || job.state === 'Aborted') {
        throw new Error(`Bulk job failed: ${job.state}`);
      }

      await new Promise(r => setTimeout(r, pollInterval));
    }

    throw new Error('Bulk job timeout');
  }

  private async getFailedResults(jobId: string): Promise<any[]> {
    const response = await fetch(
      `${this.instanceUrl}/services/data/v59.0/jobs/ingest/${jobId}/failedResults`,
      {
        headers: { 'Authorization': `Bearer ${this.accessToken}` }
      }
    );

    const csv = await response.text();
    return this.parseCSV(csv);
  }

  private recordsToCSV(records: object[]): string {
    if (records.length === 0) return '';

    const headers = Object.keys(records[0]);
    const rows = records.map(r =>
      headers.map(h => this.escapeCSV(r[h])).join(',')
    );

    return [headers.join(','), ...rows].join('\n');
  }

  private escapeCSV(value: any): string {
    if (value === null || value === undefined) return '';
    const str = String(value);
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
  }
}

### 上下文

- 大数据量
- 数据迁移
- 批量操作

### 使用 Scratch Org 的 Salesforce DX

基于源码驱动的开发模式，使用可丢弃的 Scratch Org 进行隔离测试。Scratch Org 有效期 7-30 天，可全天候创建，不受沙箱刷新频率限制。

// project-scratch-def.json - Scratch Org 定义
{
  "orgName": "MyApp Dev Org",
  "edition": "Developer",
  "features": ["EnableSetPasswordInApi", "Communities"],
  "settings": {
    "lightningExperienceSettings": {
      "enableS1DesktopEnabled": true
    },
    "mobileSettings": {
      "enableS1EncryptedStoragePref2": false
    },
    "securitySettings": {
      "passwordPolicies": {
        "enableSetPasswordInApi": true
      }
    }
  }
}

// sfdx-project.json - 项目配置
{
  "packageDirectories": [
    {
      "path": "force-app",
      "default": true,
      "package": "MyPackage",
      "versionName": "ver 1.0",
      "versionNumber": "1.0.0.NEXT",
      "dependencies": [
        {
          "package": "SomePackage@2.0.0"
        }
      ]
    }
  ],
  "namespace": "myns",
  "sfdcLoginUrl": "https://login.salesforce.com",
  "sourceApiVersion": "59.0"
}

# 开发工作流命令
# 1. 创建 Scratch Org
sf org create scratch \
  --definition-file config/project-scratch-def.json \
  --alias myapp-dev \
  --duration-days 7 \
  --set-default

# 2. 推送源码到 Scratch Org
sf project deploy start --target-org myapp-dev

# 3. 分配权限集
sf org assign permset --name MyApp_Admin --target-org myapp-dev

# 4. 导入示例数据
sf data import tree --plan data/sample-data-plan.json --target-org myapp-dev

# 5. 打开 Org
sf org open --target-org myapp-dev

# 6. 运行测试
sf apex run test \
  --code-coverage \
  --result-format human \
  --wait 10 \
  --target-org myapp-dev

# 7. 拉取变更回本地
sf project retrieve start --target-org myapp-dev

### 上下文

- 开发工作流
- CI/CD
- 测试

### 第二代包（2GP）开发

2GP 以源码驱动、模块化打包取代 1GP。需要启用 2GP 的 Dev Hub、关联命名空间，提升发布的包需要 75% 代码覆盖率。

# 在 Setup 中启用 Dev Hub 和 2GP：
# Setup > Dev Hub > Enable Dev Hub
# Setup > Dev Hub > Enable Unlocked Packages and 2GP

# 关联命名空间（托管包必须）
sf package create \
  --name "MyManagedPackage" \
  --package-type Managed \
  --path force-app \
  --target-dev-hub DevHub

# 创建包版本（beta）
sf package version create \
  --package "MyManagedPackage" \
  --installation-key-bypass \
  --wait 30 \
  --code-coverage \
  --target-dev-hub DevHub

# 查看版本状态
sf package version list --packages "MyManagedPackage" --target-dev-hub DevHub

# 提升为正式版（需 75% 覆盖率）
sf package version promote \
  --package "MyManagedPackage@1.0.0-1" \
  --target-dev-hub DevHub

# 安装到沙箱进行测试
sf package install \
  --package "MyManagedPackage@1.0.0-1" \
  --target-org MySandbox \
  --wait 20

# CI/CD 流水线（GitHub Actions）
# .github/workflows/salesforce-ci.yml
name: Salesforce CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Salesforce CLI
        run: npm install -g @salesforce/cli

      - name: Authenticate Dev Hub
        run: |
          echo "${{ secrets.SFDX_AUTH_URL }}" > auth.txt
          sf org login sfdx-url --sfdx-url-file auth.txt --alias DevHub --set-default-dev-hub

      - name: Create Scratch Org
        run: |
          sf org create scratch \
            --definition-file config/project-scratch-def.json \
            --alias ci-scratch \
            --duration-days 1 \
            --set-default

      - name: Deploy Source
        run: sf project deploy start --target-org ci-scratch

      - name: Run Tests
        run: |
          sf apex run test \
            --code-coverage \
            --result-format human \
            --wait 20 \
            --target-org ci-scratch

      - name: Delete Scratch Org
        if: always()
        run: sf org delete scratch --target-org ci-scratch --no-prompt

### 上下文

- 打包
- ISV 开发
- AppExchange

## 陷阱

### Governor Limits 按事务而非按记录计算

严重程度：CRITICAL

### @wire 结果有缓存，可能过期

严重程度：HIGH

### LWC 属性区分大小写

严重程度：MEDIUM

### Apex 集合中的空指针异常

严重程度：HIGH

### 触发器递归导致无限循环

严重程度：CRITICAL

### 同步触发器中无法发起 callout

严重程度：HIGH

### 不能混合 Setup 和 Non-Setup DML

严重程度：HIGH

### 动态 SOQL 存在注入风险

严重程度：CRITICAL

### Scratch Org 到期后所有数据丢失

严重程度：MEDIUM

### API 版本不匹配导致静默失败

严重程度：MEDIUM

## 验证检查

### SOQL 查询在循环内

严重程度：ERROR

循环中的 SOQL 在批量数据场景下会触发 Governor Limit 异常

提示信息：SOQL 查询在循环内。在循环外查询一次，使用 Map。

### DML 操作在循环内

严重程度：ERROR

循环中的 DML 会触发 150 条语句限制

提示信息：DML 操作在循环内。收集记录后在循环外执行单次 DML。

### 触发器中发起 HTTP Callout

严重程度：ERROR

同步触发器无法发起 callout

提示信息：触发器中有 callout。使用 @future(callout=true) 或带 Database.AllowsCallouts 的 Queueable。

### 潜在的 SOQL 注入

严重程度：ERROR

使用字符串拼接的动态 SOQL 存在漏洞

提示信息：动态 SOQL 使用了拼接。使用绑定变量或 String.escapeSingleQuotes()。

### 缺少 WITH SECURITY_ENFORCED

严重程度：WARNING

SOQL 应强制执行 FLS/CRUD 权限

提示信息：SOQL 未启用安全强制。添加 WITH SECURITY_ENFORCED。

### 硬编码 Salesforce ID

严重程度：WARNING

记录 ID 在不同 Org 间不通用

提示信息：硬编码了 Salesforce ID。改用 DeveloperName 或 ExternalId 查询。

### 硬编码凭证

严重程度：ERROR

凭证必须使用 Named Credentials 或 Custom Metadata

提示信息：硬编码了凭证。使用 Named Credentials 或 Custom Metadata。

### LWC 中直接操作 DOM

严重程度：WARNING

LWC 使用 Shadow DOM，直接操作会破坏封装

提示信息：LWC 中直接访问了 DOM。使用 this.template.querySelector() 或数据绑定。

### 未使用 @track 的响应式属性

严重程度：INFO

复杂对象属性需要 @track 才能实现响应式

提示信息：对象赋值可能需要 @track 才能响应式更新（Spring '20 之后对象自动追踪）。

### DML 后未刷新 Wire

严重程度：WARNING

更新后 Wire 缓存数据会过期

提示信息：@wire 之后执行了 DML 但未调用 refreshApex。数据可能已过期。

## 协作

### 委托触发条件

- 用户需要外部 API 集成 -> backend（REST API 设计、外部系统同步）
- 用户需要 LWC 无法满足的复杂 UI -> frontend（使用 React/Next.js 的自定义门户）
- 用户需要 HubSpot 集成 -> hubspot-integration（Salesforce-HubSpot 同步模式）
- 用户需要数据仓库同步 -> data-engineer（从 Salesforce 到数据仓库的 ETL）
- 用户需要支付处理 -> stripe-integration（超越 Salesforce Billing）
- 用户需要高级认证 -> auth-specialist（SSO、SAML、自定义门户）

## 何时使用
- 用户提及或暗示：salesforce
- 用户提及或暗示：sfdc
- 用户提及或暗示：apex
- 用户提及或暗示：lwc
- 用户提及或暗示：lightning web components
- 用户提及或暗示：sfdx
- 用户提及或暗示：scratch org
- 用户提及或暗示：visualforce
- 用户提及或暗示：soql
- 用户提及或暗示：governor limits
- 用户提及或暗示：connected app

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。