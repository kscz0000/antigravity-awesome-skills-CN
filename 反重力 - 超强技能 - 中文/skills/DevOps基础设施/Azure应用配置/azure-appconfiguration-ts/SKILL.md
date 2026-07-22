---
name: azure-appconfiguration-ts
description: "Azure App Configuration TypeScript SDK — 集中式配置管理，支持功能开关和动态刷新。触发词：Azure App Configuration、应用配置、配置中心、功能开关、feature flags、动态配置、配置管理、TypeScript 配置 SDK"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure App Configuration SDK for TypeScript

集中式配置管理，支持功能开关和动态刷新。

## 安装

```bash
# 底层 CRUD SDK
npm install @azure/app-configuration @azure/identity

# 高级 Provider（推荐用于应用）
npm install @azure/app-configuration-provider @azure/identity

# 功能开关管理
npm install @microsoft/feature-management
```

## 环境变量

```bash
AZURE_APPCONFIG_ENDPOINT=https://<your-resource>.azconfig.io
# 或
AZURE_APPCONFIG_CONNECTION_STRING=Endpoint=https://...;Id=...;Secret=...
```

## 认证

```typescript
import { AppConfigurationClient } from "@azure/app-configuration";
import { DefaultAzureCredential } from "@azure/identity";

// DefaultAzureCredential（推荐）
const client = new AppConfigurationClient(
  process.env.AZURE_APPCONFIG_ENDPOINT!,
  new DefaultAzureCredential()
);

// 连接字符串
const client2 = new AppConfigurationClient(
  process.env.AZURE_APPCONFIG_CONNECTION_STRING!
);
```

## CRUD 操作

### 创建/更新配置项

```typescript
// 新增（已存在则失败）
await client.addConfigurationSetting({
  key: "app:settings:message",
  value: "Hello World",
  label: "production",
  contentType: "text/plain",
  tags: { environment: "prod" },
});

// 设置（创建或更新）
await client.setConfigurationSetting({
  key: "app:settings:message",
  value: "Updated value",
  label: "production",
});

// 带乐观并发的更新
const existing = await client.getConfigurationSetting({ key: "myKey" });
existing.value = "new value";
await client.setConfigurationSetting(existing, { onlyIfUnchanged: true });
```

### 读取配置项

```typescript
// 获取单个配置
const setting = await client.getConfigurationSetting({
  key: "app:settings:message",
  label: "production",  // 可选
});
console.log(setting.value);

// 带过滤条件列出
const settings = client.listConfigurationSettings({
  keyFilter: "app:*",
  labelFilter: "production",
});

for await (const setting of settings) {
  console.log(`${setting.key}: ${setting.value}`);
}
```

### 删除配置项

```typescript
await client.deleteConfigurationSetting({
  key: "app:settings:message",
  label: "production",
});
```

### 锁定/解锁（只读）

```typescript
// 锁定
await client.setReadOnly({ key: "myKey", label: "prod" }, true);

// 解锁
await client.setReadOnly({ key: "myKey", label: "prod" }, false);
```

## App Configuration Provider

### 加载配置

```typescript
import { load } from "@azure/app-configuration-provider";
import { DefaultAzureCredential } from "@azure/identity";

const appConfig = await load(
  process.env.AZURE_APPCONFIG_ENDPOINT!,
  new DefaultAzureCredential(),
  {
    selectors: [
      { keyFilter: "app:*", labelFilter: "production" },
    ],
    trimKeyPrefixes: ["app:"],
  }
);

// Map 风格访问
const value = appConfig.get("settings:message");

// 对象风格访问
const config = appConfig.constructConfigurationObject({ separator: ":" });
console.log(config.settings.message);
```

### 动态刷新

```typescript
const appConfig = await load(endpoint, credential, {
  selectors: [{ keyFilter: "app:*" }],
  refreshOptions: {
    enabled: true,
    refreshIntervalInMs: 30_000,  // 30 秒
  },
});

// 触发刷新（非阻塞）
appConfig.refresh();

// 监听刷新事件
const disposer = appConfig.onRefresh(() => {
  console.log("Configuration refreshed!");
});

// Express 中间件模式
app.use((req, res, next) => {
  appConfig.refresh();
  next();
});
```

### Key Vault 引用

```typescript
const appConfig = await load(endpoint, credential, {
  selectors: [{ keyFilter: "app:*" }],
  keyVaultOptions: {
    credential: new DefaultAzureCredential(),
    secretRefreshIntervalInMs: 7200_000,  // 2 小时
  },
});

// 密钥自动解析
const dbPassword = appConfig.get("database:password");
```

## 功能开关

### 创建功能开关（底层 API）

```typescript
import {
  featureFlagPrefix,
  featureFlagContentType,
  FeatureFlagValue,
  ConfigurationSetting,
} from "@azure/app-configuration";

const flag: ConfigurationSetting<FeatureFlagValue> = {
  key: `${featureFlagPrefix}Beta`,
  contentType: featureFlagContentType,
  value: {
    id: "Beta",
    enabled: true,
    description: "Beta feature",
    conditions: {
      clientFilters: [
        {
          name: "Microsoft.Targeting",
          parameters: {
            Audience: {
              Users: ["user@example.com"],
              Groups: [{ Name: "beta-testers", RolloutPercentage: 50 }],
              DefaultRolloutPercentage: 0,
            },
          },
        },
      ],
    },
  },
};

await client.addConfigurationSetting(flag);
```

### 加载并评估功能开关

```typescript
import { load } from "@azure/app-configuration-provider";
import {
  ConfigurationMapFeatureFlagProvider,
  FeatureManager,
} from "@microsoft/feature-management";

const appConfig = await load(endpoint, credential, {
  featureFlagOptions: {
    enabled: true,
    selectors: [{ keyFilter: "*" }],
    refresh: {
      enabled: true,
      refreshIntervalInMs: 30_000,
    },
  },
});

const featureProvider = new ConfigurationMapFeatureFlagProvider(appConfig);
const featureManager = new FeatureManager(featureProvider);

// 简单检查
const isEnabled = await featureManager.isEnabled("Beta");

// 带目标上下文检查
const isEnabledForUser = await featureManager.isEnabled("Beta", {
  userId: "user@example.com",
  groups: ["beta-testers"],
});
```

## 快照

```typescript
// 创建快照
const snapshot = await client.beginCreateSnapshotAndWait({
  name: "release-v1.0",
  retentionPeriod: 2592000,  // 30 天
  filters: [{ keyFilter: "app:*", labelFilter: "production" }],
});

// 获取快照
const snap = await client.getSnapshot("release-v1.0");

// 列出快照中的配置
const settings = client.listConfigurationSettingsForSnapshot("release-v1.0");
for await (const setting of settings) {
  console.log(`${setting.key}: ${setting.value}`);
}

// 归档/恢复
await client.archiveSnapshot("release-v1.0");
await client.recoverSnapshot("release-v1.0");

// 从快照加载（Provider）
const config = await load(endpoint, credential, {
  selectors: [{ snapshotName: "release-v1.0" }],
});
```

## 标签

```typescript
// 创建带标签的配置
await client.setConfigurationSetting({
  key: "database:host",
  value: "dev-db.example.com",
  label: "development",
});

await client.setConfigurationSetting({
  key: "database:host",
  value: "prod-db.example.com",
  label: "production",
});

// 按标签过滤
const prodSettings = client.listConfigurationSettings({
  keyFilter: "*",
  labelFilter: "production",
});

// 无标签（null 标签）
const noLabelSettings = client.listConfigurationSettings({
  labelFilter: "\0",
});

// 列出可用标签
for await (const label of client.listLabels()) {
  console.log(label.name);
}
```

## 类型导入

```typescript
import {
  AppConfigurationClient,
  ConfigurationSetting,
  FeatureFlagValue,
  SecretReferenceValue,
  featureFlagPrefix,
  featureFlagContentType,
  secretReferenceContentType,
  ListConfigurationSettingsOptions,
} from "@azure/app-configuration";

import { load } from "@azure/app-configuration-provider";

import {
  FeatureManager,
  ConfigurationMapFeatureFlagProvider,
} from "@microsoft/feature-management";
```

## 最佳实践

1. **应用使用 Provider** — 运行时配置使用 `@azure/app-configuration-provider`
2. **管理使用底层 SDK** — CRUD 操作使用 `@azure/app-configuration`
3. **启用刷新** — 实现动态配置更新
4. **使用标签** — 按环境隔离配置
5. **使用快照** — 实现不可变的发布配置
6. **哨兵模式** — 使用哨兵键触发完整刷新
7. **RBAC 角色** — 只读访问使用 `App Configuration Data Reader`

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确符合上述范围时使用本技能。
- 输出内容不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
