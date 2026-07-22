---
name: azure-security-keyvault-secrets-java
description: "Azure Key Vault 机密 Java SDK，用于机密管理。当用户要求'管理密码、密钥、连接字符串或其他敏感配置数据'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Key Vault 机密 (Java)

安全地存储和管理机密，如密码、密钥和连接字符串。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-security-keyvault-secrets</artifactId>
    <version>4.9.0</version>
</dependency>
```

## 创建客户端

```java
import com.azure.security.keyvault.secrets.SecretClient;
import com.azure.security.keyvault.secrets.SecretClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

// Sync client
SecretClient secretClient = new SecretClientBuilder()
    .vaultUrl("https://<vault-name>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();

// Async client
SecretAsyncClient secretAsyncClient = new SecretClientBuilder()
    .vaultUrl("https://<vault-name>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

## 创建/设置机密

```java
import com.azure.security.keyvault.secrets.models.KeyVaultSecret;

// Simple secret
KeyVaultSecret secret = secretClient.setSecret("database-password", "P@ssw0rd123!");
System.out.println("Secret name: " + secret.getName());
System.out.println("Secret ID: " + secret.getId());

// Secret with options
KeyVaultSecret secretWithOptions = secretClient.setSecret(
    new KeyVaultSecret("api-key", "sk_live_abc123xyz")
        .setProperties(new SecretProperties()
            .setContentType("application/json")
            .setExpiresOn(OffsetDateTime.now().plusYears(1))
            .setNotBefore(OffsetDateTime.now())
            .setEnabled(true)
            .setTags(Map.of(
                "environment", "production",
                "service", "payment-api"
            ))
        )
);
```

## 获取机密

```java
// Get latest version
KeyVaultSecret secret = secretClient.getSecret("database-password");
String value = secret.getValue();
System.out.println("Secret value: " + value);

// Get specific version
KeyVaultSecret specificVersion = secretClient.getSecret("database-password", "<version-id>");

// Get only properties (no value)
SecretProperties props = secretClient.getSecret("database-password").getProperties();
System.out.println("Enabled: " + props.isEnabled());
System.out.println("Created: " + props.getCreatedOn());
```

## 更新机密属性

```java
// Get secret
KeyVaultSecret secret = secretClient.getSecret("api-key");

// Update properties (cannot update value - create new version instead)
secret.getProperties()
    .setEnabled(false)
    .setExpiresOn(OffsetDateTime.now().plusMonths(6))
    .setTags(Map.of("status", "rotating"));

SecretProperties updated = secretClient.updateSecretProperties(secret.getProperties());
System.out.println("Updated: " + updated.getUpdatedOn());
```

## 列出机密

```java
import com.azure.core.util.paging.PagedIterable;
import com.azure.security.keyvault.secrets.models.SecretProperties;

// List all secrets (properties only, no values)
for (SecretProperties secretProps : secretClient.listPropertiesOfSecrets()) {
    System.out.println("Secret: " + secretProps.getName());
    System.out.println("  Enabled: " + secretProps.isEnabled());
    System.out.println("  Created: " + secretProps.getCreatedOn());
    System.out.println("  Content-Type: " + secretProps.getContentType());
    
    // Get value if needed
    if (secretProps.isEnabled()) {
        KeyVaultSecret fullSecret = secretClient.getSecret(secretProps.getName());
        System.out.println("  Value: " + fullSecret.getValue().substring(0, 5) + "...");
    }
}

// List versions of a secret
for (SecretProperties version : secretClient.listPropertiesOfSecretVersions("database-password")) {
    System.out.println("Version: " + version.getVersion());
    System.out.println("Created: " + version.getCreatedOn());
    System.out.println("Enabled: " + version.isEnabled());
}
```

## 删除机密

```java
import com.azure.core.util.polling.SyncPoller;
import com.azure.security.keyvault.secrets.models.DeletedSecret;

// Begin delete (returns poller for soft-delete enabled vaults)
SyncPoller<DeletedSecret, Void> deletePoller = secretClient.beginDeleteSecret("old-secret");

// Wait for deletion
DeletedSecret deletedSecret = deletePoller.poll().getValue();
System.out.println("Deleted on: " + deletedSecret.getDeletedOn());
System.out.println("Scheduled purge: " + deletedSecret.getScheduledPurgeDate());

deletePoller.waitForCompletion();
```

## 恢复已删除的机密

```java
// List deleted secrets
for (DeletedSecret deleted : secretClient.listDeletedSecrets()) {
    System.out.println("Deleted: " + deleted.getName());
    System.out.println("Deletion date: " + deleted.getDeletedOn());
}

// Recover deleted secret
SyncPoller<KeyVaultSecret, Void> recoverPoller = secretClient.beginRecoverDeletedSecret("old-secret");
recoverPoller.waitForCompletion();

KeyVaultSecret recovered = recoverPoller.getFinalResult();
System.out.println("Recovered: " + recovered.getName());
```

## 永久清除已删除的机密

```java
// Permanently delete (cannot be recovered)
secretClient.purgeDeletedSecret("old-secret");

// Get deleted secret info first
DeletedSecret deleted = secretClient.getDeletedSecret("old-secret");
System.out.println("Will purge: " + deleted.getName());
secretClient.purgeDeletedSecret("old-secret");
```

## 备份与恢复

```java
// Backup secret (all versions)
byte[] backup = secretClient.backupSecret("important-secret");

// Save to file
Files.write(Paths.get("secret-backup.blob"), backup);

// Restore from backup
byte[] backupData = Files.readAllBytes(Paths.get("secret-backup.blob"));
KeyVaultSecret restored = secretClient.restoreSecretBackup(backupData);
System.out.println("Restored: " + restored.getName());
```

## 异步操作

```java
SecretAsyncClient asyncClient = new SecretClientBuilder()
    .vaultUrl("https://<vault>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();

// Set secret async
asyncClient.setSecret("async-secret", "async-value")
    .subscribe(
        secret -> System.out.println("Created: " + secret.getName()),
        error -> System.out.println("Error: " + error.getMessage())
    );

// Get secret async
asyncClient.getSecret("async-secret")
    .subscribe(secret -> System.out.println("Value: " + secret.getValue()));

// List secrets async
asyncClient.listPropertiesOfSecrets()
    .doOnNext(props -> System.out.println("Found: " + props.getName()))
    .subscribe();
```

## 配置模式

### 加载多个机密

```java
public class ConfigLoader {
    private final SecretClient client;
    
    public ConfigLoader(String vaultUrl) {
        this.client = new SecretClientBuilder()
            .vaultUrl(vaultUrl)
            .credential(new DefaultAzureCredentialBuilder().build())
            .buildClient();
    }
    
    public Map<String, String> loadSecrets(List<String> secretNames) {
        Map<String, String> secrets = new HashMap<>();
        for (String name : secretNames) {
            try {
                KeyVaultSecret secret = client.getSecret(name);
                secrets.put(name, secret.getValue());
            } catch (ResourceNotFoundException e) {
                System.out.println("Secret not found: " + name);
            }
        }
        return secrets;
    }
}

// Usage
ConfigLoader loader = new ConfigLoader("https://my-vault.vault.azure.net");
Map<String, String> config = loader.loadSecrets(
    Arrays.asList("db-connection-string", "api-key", "jwt-secret")
);
```

### 机密轮换模式

```java
public void rotateSecret(String secretName, String newValue) {
    // Get current secret
    KeyVaultSecret current = secretClient.getSecret(secretName);
    
    // Disable old version
    current.getProperties().setEnabled(false);
    secretClient.updateSecretProperties(current.getProperties());
    
    // Create new version with new value
    KeyVaultSecret newSecret = secretClient.setSecret(secretName, newValue);
    System.out.println("Rotated to version: " + newSecret.getProperties().getVersion());
}
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;
import com.azure.core.exception.ResourceNotFoundException;

try {
    KeyVaultSecret secret = secretClient.getSecret("my-secret");
    System.out.println("Value: " + secret.getValue());
} catch (ResourceNotFoundException e) {
    System.out.println("Secret not found");
} catch (HttpResponseException e) {
    int status = e.getResponse().getStatusCode();
    if (status == 403) {
        System.out.println("Access denied - check permissions");
    } else if (status == 429) {
        System.out.println("Rate limited - retry later");
    } else {
        System.out.println("HTTP error: " + status);
    }
}
```

## 机密属性

| 属性 | 说明 |
|------|------|
| `name` | 机密名称 |
| `value` | 机密值（字符串） |
| `id` | 完整标识符 URL |
| `contentType` | MIME 类型提示 |
| `enabled` | 机密是否可被检索 |
| `notBefore` | 激活时间 |
| `expiresOn` | 过期时间 |
| `createdOn` | 创建时间戳 |
| `updatedOn` | 最后更新时间戳 |
| `recoveryLevel` | 软删除恢复级别 |
| `tags` | 用户定义的元数据 |

## 环境变量

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net
```

## 最佳实践

1. **启用软删除** - 防止意外删除
2. **使用标签** - 为机密标记环境、服务、所有者
3. **设置过期时间** - 对需要轮换的凭证使用 `setExpiresOn()`
4. **内容类型** - 设置 `contentType` 以指示格式（如 `application/json`）
5. **版本管理** - 轮换时不要立即删除旧版本
6. **访问日志** - 在 Key Vault 上启用诊断日志
7. **最小权限** - 不同环境使用独立的保管库

## 常见机密类型

```java
// Database connection string
secretClient.setSecret(new KeyVaultSecret("db-connection", 
    "Server=myserver.database.windows.net;Database=mydb;...")
    .setProperties(new SecretProperties()
        .setContentType("text/plain")
        .setTags(Map.of("type", "connection-string"))));

// API key
secretClient.setSecret(new KeyVaultSecret("stripe-api-key", "sk_live_...")
    .setProperties(new SecretProperties()
        .setContentType("text/plain")
        .setExpiresOn(OffsetDateTime.now().plusYears(1))));

// JSON configuration
secretClient.setSecret(new KeyVaultSecret("app-config", 
    "{\"endpoint\":\"https://...\",\"key\":\"...\"}")
    .setProperties(new SecretProperties()
        .setContentType("application/json")));

// Certificate password
secretClient.setSecret(new KeyVaultSecret("cert-password", "CertP@ss!")
    .setProperties(new SecretProperties()
        .setContentType("text/plain")
        .setTags(Map.of("certificate", "my-cert"))));
```

## 触发词

- "Key Vault 机密 Java"、"机密管理 Java"
- "存储密码"、"存储密钥"、"连接字符串"
- "检索机密"、"轮换机密"
- "Azure 机密"、"保管库机密"

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
