---
name: azure-appconfiguration-java
description: Azure App Configuration Java SDK — 集中化应用配置管理，支持键值设置、功能标志和快照。触发词：Azure配置、App Configuration、Java配置管理、配置中心、功能开关、配置快照、Key Vault引用
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure App Configuration SDK for Java

Azure App Configuration 的客户端库，这是一个用于集中管理应用配置的托管服务。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-data-appconfiguration</artifactId>
    <version>1.8.0</version>
</dependency>
```

或使用 Azure SDK BOM：

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-sdk-bom</artifactId>
            <version>{bom_version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-data-appconfiguration</artifactId>
    </dependency>
</dependencies>
```

## 前置条件

- Azure App Configuration 存储实例
- 连接字符串或 Entra ID 凭证

## 环境变量

```bash
AZURE_APPCONFIG_CONNECTION_STRING=Endpoint=https://<store>.azconfig.io;Id=<id>;Secret=<secret>
AZURE_APPCONFIG_ENDPOINT=https://<store>.azconfig.io
```

## 创建客户端

### 使用连接字符串

```java
import com.azure.data.appconfiguration.ConfigurationClient;
import com.azure.data.appconfiguration.ConfigurationClientBuilder;

ConfigurationClient configClient = new ConfigurationClientBuilder()
    .connectionString(System.getenv("AZURE_APPCONFIG_CONNECTION_STRING"))
    .buildClient();
```

### 异步客户端

```java
import com.azure.data.appconfiguration.ConfigurationAsyncClient;

ConfigurationAsyncClient asyncClient = new ConfigurationClientBuilder()
    .connectionString(connectionString)
    .buildAsyncClient();
```

### 使用 Entra ID（推荐）

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

ConfigurationClient configClient = new ConfigurationClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(System.getenv("AZURE_APPCONFIG_ENDPOINT"))
    .buildClient();
```

## 核心概念

| 概念 | 描述 |
|---------|-------------|
| Configuration Setting | 带可选标签的键值对 |
| Label | 用于分隔设置的维度（如环境） |
| Feature Flag | 用于功能管理的特殊设置 |
| Secret Reference | 指向 Key Vault 密钥的设置 |
| Snapshot | 设置的时间点不可变视图 |

## 配置设置操作

### 创建设置（Add）

仅当设置不存在时创建：

```java
import com.azure.data.appconfiguration.models.ConfigurationSetting;

ConfigurationSetting setting = configClient.addConfigurationSetting(
    "app/database/connection", 
    "Production", 
    "Server=prod.db.com;Database=myapp"
);
```

### 创建或更新设置（Set）

创建或覆盖：

```java
ConfigurationSetting setting = configClient.setConfigurationSetting(
    "app/cache/enabled", 
    "Production", 
    "true"
);
```

### 获取设置

```java
ConfigurationSetting setting = configClient.getConfigurationSetting(
    "app/database/connection", 
    "Production"
);
System.out.println("Value: " + setting.getValue());
System.out.println("Content-Type: " + setting.getContentType());
System.out.println("Last Modified: " + setting.getLastModified());
```

### 条件获取（If Changed）

```java
import com.azure.core.http.rest.Response;
import com.azure.core.util.Context;

Response<ConfigurationSetting> response = configClient.getConfigurationSettingWithResponse(
    setting,      // 带有 ETag 的设置
    null,         // Accept datetime
    true,         // ifChanged - 仅在修改时获取
    Context.NONE
);

if (response.getStatusCode() == 304) {
    System.out.println("Setting not modified");
} else {
    ConfigurationSetting updated = response.getValue();
}
```

### 更新设置

```java
ConfigurationSetting updated = configClient.setConfigurationSetting(
    "app/cache/enabled", 
    "Production", 
    "false"
);
```

### 条件更新（If Unchanged）

```java
// 仅当 ETag 匹配时更新（无并发修改）
Response<ConfigurationSetting> response = configClient.setConfigurationSettingWithResponse(
    setting,     // 带有当前 ETag 的设置
    true,        // ifUnchanged
    Context.NONE
);
```

### 删除设置

```java
ConfigurationSetting deleted = configClient.deleteConfigurationSetting(
    "app/cache/enabled", 
    "Production"
);
```

### 条件删除

```java
Response<ConfigurationSetting> response = configClient.deleteConfigurationSettingWithResponse(
    setting,     // 带有 ETag 的设置
    true,        // ifUnchanged
    Context.NONE
);
```

## 列出和筛选设置

### 按键模式列出

```java
import com.azure.data.appconfiguration.models.SettingSelector;
import com.azure.core.http.rest.PagedIterable;

SettingSelector selector = new SettingSelector()
    .setKeyFilter("app/*");

PagedIterable<ConfigurationSetting> settings = configClient.listConfigurationSettings(selector);
for (ConfigurationSetting s : settings) {
    System.out.println(s.getKey() + " = " + s.getValue());
}
```

### 按标签列出

```java
SettingSelector selector = new SettingSelector()
    .setKeyFilter("*")
    .setLabelFilter("Production");

PagedIterable<ConfigurationSetting> settings = configClient.listConfigurationSettings(selector);
```

### 按多个键列出

```java
SettingSelector selector = new SettingSelector()
    .setKeyFilter("app/database/*,app/cache/*");

PagedIterable<ConfigurationSetting> settings = configClient.listConfigurationSettings(selector);
```

### 列出修订版本

```java
SettingSelector selector = new SettingSelector()
    .setKeyFilter("app/database/connection");

PagedIterable<ConfigurationSetting> revisions = configClient.listRevisions(selector);
for (ConfigurationSetting revision : revisions) {
    System.out.println("Value: " + revision.getValue() + ", Modified: " + revision.getLastModified());
}
```

## 功能标志

### 创建功能标志

```java
import com.azure.data.appconfiguration.models.FeatureFlagConfigurationSetting;
import com.azure.data.appconfiguration.models.FeatureFlagFilter;
import java.util.Arrays;

FeatureFlagFilter percentageFilter = new FeatureFlagFilter("Microsoft.Percentage")
    .addParameter("Value", 50);

FeatureFlagConfigurationSetting featureFlag = new FeatureFlagConfigurationSetting("beta-feature", true)
    .setDescription("Beta feature rollout")
    .setClientFilters(Arrays.asList(percentageFilter));

FeatureFlagConfigurationSetting created = (FeatureFlagConfigurationSetting)
    configClient.addConfigurationSetting(featureFlag);
```

### 获取功能标志

```java
FeatureFlagConfigurationSetting flag = (FeatureFlagConfigurationSetting)
    configClient.getConfigurationSetting(featureFlag);

System.out.println("Feature: " + flag.getFeatureId());
System.out.println("Enabled: " + flag.isEnabled());
System.out.println("Filters: " + flag.getClientFilters());
```

### 更新功能标志

```java
featureFlag.setEnabled(false);
FeatureFlagConfigurationSetting updated = (FeatureFlagConfigurationSetting)
    configClient.setConfigurationSetting(featureFlag);
```

## 密钥引用

### 创建密钥引用

```java
import com.azure.data.appconfiguration.models.SecretReferenceConfigurationSetting;

SecretReferenceConfigurationSetting secretRef = new SecretReferenceConfigurationSetting(
    "app/secrets/api-key",
    "https://myvault.vault.azure.net/secrets/api-key"
);

SecretReferenceConfigurationSetting created = (SecretReferenceConfigurationSetting)
    configClient.addConfigurationSetting(secretRef);
```

### 获取密钥引用

```java
SecretReferenceConfigurationSetting ref = (SecretReferenceConfigurationSetting)
    configClient.getConfigurationSetting(secretRef);

System.out.println("Secret URI: " + ref.getSecretId());
```

## 只读设置

### 设置为只读

```java
ConfigurationSetting readOnly = configClient.setReadOnly(
    "app/critical/setting", 
    "Production", 
    true
);
```

### 清除只读

```java
ConfigurationSetting writable = configClient.setReadOnly(
    "app/critical/setting", 
    "Production", 
    false
);
```

## 快照

### 创建快照

```java
import com.azure.data.appconfiguration.models.ConfigurationSnapshot;
import com.azure.data.appconfiguration.models.ConfigurationSettingsFilter;
import com.azure.core.util.polling.SyncPoller;
import com.azure.core.util.polling.PollOperationDetails;

List<ConfigurationSettingsFilter> filters = new ArrayList<>();
filters.add(new ConfigurationSettingsFilter("app/*"));

SyncPoller<PollOperationDetails, ConfigurationSnapshot> poller = configClient.beginCreateSnapshot(
    "release-v1.0",
    new ConfigurationSnapshot(filters),
    Context.NONE
);
poller.setPollInterval(Duration.ofSeconds(10));
poller.waitForCompletion();

ConfigurationSnapshot snapshot = poller.getFinalResult();
System.out.println("Snapshot: " + snapshot.getName() + ", Status: " + snapshot.getStatus());
```

### 获取快照

```java
ConfigurationSnapshot snapshot = configClient.getSnapshot("release-v1.0");
System.out.println("Created: " + snapshot.getCreatedAt());
System.out.println("Items: " + snapshot.getItemCount());
```

### 列出快照中的设置

```java
PagedIterable<ConfigurationSetting> settings = 
    configClient.listConfigurationSettingsForSnapshot("release-v1.0");

for (ConfigurationSetting setting : settings) {
    System.out.println(setting.getKey() + " = " + setting.getValue());
}
```

### 归档快照

```java
ConfigurationSnapshot archived = configClient.archiveSnapshot("release-v1.0");
System.out.println("Status: " + archived.getStatus()); // archived
```

### 恢复快照

```java
ConfigurationSnapshot recovered = configClient.recoverSnapshot("release-v1.0");
System.out.println("Status: " + recovered.getStatus()); // ready
```

### 列出所有快照

```java
import com.azure.data.appconfiguration.models.SnapshotSelector;

SnapshotSelector selector = new SnapshotSelector().setNameFilter("release-*");
PagedIterable<ConfigurationSnapshot> snapshots = configClient.listSnapshots(selector);

for (ConfigurationSnapshot snap : snapshots) {
    System.out.println(snap.getName() + " - " + snap.getStatus());
}
```

## 标签

### 列出标签

```java
import com.azure.data.appconfiguration.models.SettingLabelSelector;

configClient.listLabels(new SettingLabelSelector().setNameFilter("*"))
    .forEach(label -> System.out.println("Label: " + label.getName()));
```

## 异步操作

```java
ConfigurationAsyncClient asyncClient = new ConfigurationClientBuilder()
    .connectionString(connectionString)
    .buildAsyncClient();

// 使用响应式流异步列出
asyncClient.listConfigurationSettings(new SettingSelector().setLabelFilter("Production"))
    .subscribe(
        setting -> System.out.println(setting.getKey() + " = " + setting.getValue()),
        error -> System.err.println("Error: " + error.getMessage()),
        () -> System.out.println("Completed")
    );
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    configClient.getConfigurationSetting("nonexistent", null);
} catch (HttpResponseException e) {
    if (e.getResponse().getStatusCode() == 404) {
        System.err.println("Setting not found");
    } else {
        System.err.println("Error: " + e.getMessage());
    }
}
```

## 最佳实践

1. **使用标签** — 按环境分隔配置（Dev、Staging、Production）
2. **使用快照** — 为发布创建不可变快照
3. **功能标志** — 用于渐进式发布和 A/B 测试
4. **密钥引用** — 将敏感值存储在 Key Vault 中
5. **条件请求** — 使用 ETag 实现乐观并发控制
6. **只读保护** — 锁定关键生产设置
7. **使用 Entra ID** — 优先于连接字符串
8. **异步客户端** — 用于高吞吐量场景

## 参考链接

| 资源 | URL |
|----------|-----|
| Maven Package | https://central.sonatype.com/artifact/com.azure/azure-data-appconfiguration |
| GitHub | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/appconfiguration/azure-data-appconfiguration |
| API Documentation | https://aka.ms/java-docs |
| Product Docs | https://learn.microsoft.com/azure/azure-app-configuration |
| Samples | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/appconfiguration/azure-data-appconfiguration/src/samples |
| Troubleshooting | https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/appconfiguration/azure-data-appconfiguration/TROUBLESHOOTING.md |

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
