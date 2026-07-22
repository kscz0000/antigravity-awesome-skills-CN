---
name: azure-security-keyvault-keys-java
description: "Azure Key Vault Keys Java SDK，用于加密密钥管理。当用户要求'创建、管理或使用 RSA/EC 密钥，执行加密/解密/签名/验证操作，或使用 HSM 支持的密钥'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Key Vault Keys (Java)

在 Azure Key Vault 和 Managed HSM 中管理加密密钥并执行加密操作。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-security-keyvault-keys</artifactId>
    <version>4.9.0</version>
</dependency>
```

## 客户端创建

```java
import com.azure.security.keyvault.keys.KeyClient;
import com.azure.security.keyvault.keys.KeyClientBuilder;
import com.azure.security.keyvault.keys.cryptography.CryptographyClient;
import com.azure.security.keyvault.keys.cryptography.CryptographyClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

// Key management client
KeyClient keyClient = new KeyClientBuilder()
    .vaultUrl("https://<vault-name>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();

// Async client
KeyAsyncClient keyAsyncClient = new KeyClientBuilder()
    .vaultUrl("https://<vault-name>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();

// Cryptography client (for encrypt/decrypt/sign/verify)
CryptographyClient cryptoClient = new CryptographyClientBuilder()
    .keyIdentifier("https://<vault-name>.vault.azure.net/keys/<key-name>/<key-version>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

## 密钥类型

| 类型 | 说明 |
|------|------|
| `RSA` | RSA 密钥（2048、3072、4096 位） |
| `RSA_HSM` | HSM 中的 RSA 密钥 |
| `EC` | 椭圆曲线密钥 |
| `EC_HSM` | HSM 中的椭圆曲线密钥 |
| `OCT` | 对称密钥（仅限 Managed HSM） |
| `OCT_HSM` | HSM 中的对称密钥 |

## 创建密钥

### 创建 RSA 密钥

```java
import com.azure.security.keyvault.keys.models.*;

// Simple RSA key
KeyVaultKey rsaKey = keyClient.createRsaKey(new CreateRsaKeyOptions("my-rsa-key")
    .setKeySize(2048));

System.out.println("Key name: " + rsaKey.getName());
System.out.println("Key ID: " + rsaKey.getId());
System.out.println("Key type: " + rsaKey.getKeyType());

// RSA key with options
KeyVaultKey rsaKeyWithOptions = keyClient.createRsaKey(new CreateRsaKeyOptions("my-rsa-key-2")
    .setKeySize(4096)
    .setExpiresOn(OffsetDateTime.now().plusYears(1))
    .setNotBefore(OffsetDateTime.now())
    .setEnabled(true)
    .setKeyOperations(KeyOperation.ENCRYPT, KeyOperation.DECRYPT, 
                       KeyOperation.WRAP_KEY, KeyOperation.UNWRAP_KEY)
    .setTags(Map.of("environment", "production")));

// HSM-backed RSA key
KeyVaultKey hsmKey = keyClient.createRsaKey(new CreateRsaKeyOptions("my-hsm-key")
    .setKeySize(2048)
    .setHardwareProtected(true));
```

### 创建 EC 密钥

```java
// EC key with P-256 curve
KeyVaultKey ecKey = keyClient.createEcKey(new CreateEcKeyOptions("my-ec-key")
    .setCurveName(KeyCurveName.P_256));

// EC key with other curves
KeyVaultKey ecKey384 = keyClient.createEcKey(new CreateEcKeyOptions("my-ec-key-384")
    .setCurveName(KeyCurveName.P_384));

KeyVaultKey ecKey521 = keyClient.createEcKey(new CreateEcKeyOptions("my-ec-key-521")
    .setCurveName(KeyCurveName.P_521));

// HSM-backed EC key
KeyVaultKey ecHsmKey = keyClient.createEcKey(new CreateEcKeyOptions("my-ec-hsm-key")
    .setCurveName(KeyCurveName.P_256)
    .setHardwareProtected(true));
```

### 创建对称密钥（仅限 Managed HSM）

```java
KeyVaultKey octKey = keyClient.createOctKey(new CreateOctKeyOptions("my-symmetric-key")
    .setKeySize(256)
    .setHardwareProtected(true));
```

## 获取密钥

```java
// Get latest version
KeyVaultKey key = keyClient.getKey("my-key");

// Get specific version
KeyVaultKey keyVersion = keyClient.getKey("my-key", "<version-id>");

// Get only key properties (no key material)
KeyProperties keyProps = keyClient.getKey("my-key").getProperties();
```

## 更新密钥属性

```java
KeyVaultKey key = keyClient.getKey("my-key");

// Update properties
key.getProperties()
    .setEnabled(false)
    .setExpiresOn(OffsetDateTime.now().plusMonths(6))
    .setTags(Map.of("status", "archived"));

KeyVaultKey updatedKey = keyClient.updateKeyProperties(key.getProperties(),
    KeyOperation.ENCRYPT, KeyOperation.DECRYPT);
```

## 列出密钥

```java
import com.azure.core.util.paging.PagedIterable;

// List all keys
for (KeyProperties keyProps : keyClient.listPropertiesOfKeys()) {
    System.out.println("Key: " + keyProps.getName());
    System.out.println("  Enabled: " + keyProps.isEnabled());
    System.out.println("  Created: " + keyProps.getCreatedOn());
}

// List key versions
for (KeyProperties version : keyClient.listPropertiesOfKeyVersions("my-key")) {
    System.out.println("Version: " + version.getVersion());
    System.out.println("Created: " + version.getCreatedOn());
}
```

## 删除密钥

```java
import com.azure.core.util.polling.SyncPoller;

// Begin delete (soft-delete enabled vaults)
SyncPoller<DeletedKey, Void> deletePoller = keyClient.beginDeleteKey("my-key");

// Wait for deletion
DeletedKey deletedKey = deletePoller.poll().getValue();
System.out.println("Deleted: " + deletedKey.getDeletedOn());

deletePoller.waitForCompletion();

// Purge deleted key (permanent deletion)
keyClient.purgeDeletedKey("my-key");

// Recover deleted key
SyncPoller<KeyVaultKey, Void> recoverPoller = keyClient.beginRecoverDeletedKey("my-key");
recoverPoller.waitForCompletion();
```

## 加密操作

### 加密/解密

```java
import com.azure.security.keyvault.keys.cryptography.models.*;

CryptographyClient cryptoClient = new CryptographyClientBuilder()
    .keyIdentifier("https://<vault>.vault.azure.net/keys/<key-name>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();

byte[] plaintext = "Hello, World!".getBytes(StandardCharsets.UTF_8);

// Encrypt
EncryptResult encryptResult = cryptoClient.encrypt(EncryptionAlgorithm.RSA_OAEP, plaintext);
byte[] ciphertext = encryptResult.getCipherText();
System.out.println("Ciphertext length: " + ciphertext.length);

// Decrypt
DecryptResult decryptResult = cryptoClient.decrypt(EncryptionAlgorithm.RSA_OAEP, ciphertext);
String decrypted = new String(decryptResult.getPlainText(), StandardCharsets.UTF_8);
System.out.println("Decrypted: " + decrypted);
```

### 签名/验证

```java
import java.security.MessageDigest;

// Create digest of data
byte[] data = "Data to sign".getBytes(StandardCharsets.UTF_8);
MessageDigest md = MessageDigest.getInstance("SHA-256");
byte[] digest = md.digest(data);

// Sign
SignResult signResult = cryptoClient.sign(SignatureAlgorithm.RS256, digest);
byte[] signature = signResult.getSignature();

// Verify
VerifyResult verifyResult = cryptoClient.verify(SignatureAlgorithm.RS256, digest, signature);
System.out.println("Valid signature: " + verifyResult.isValid());
```

### 包装/解包密钥

```java
// Key to wrap (e.g., AES key)
byte[] keyToWrap = new byte[32];  // 256-bit key
new SecureRandom().nextBytes(keyToWrap);

// Wrap
WrapResult wrapResult = cryptoClient.wrapKey(KeyWrapAlgorithm.RSA_OAEP, keyToWrap);
byte[] wrappedKey = wrapResult.getEncryptedKey();

// Unwrap
UnwrapResult unwrapResult = cryptoClient.unwrapKey(KeyWrapAlgorithm.RSA_OAEP, wrappedKey);
byte[] unwrappedKey = unwrapResult.getKey();
```

## 备份与恢复

```java
// Backup
byte[] backup = keyClient.backupKey("my-key");

// Save backup to file
Files.write(Paths.get("key-backup.blob"), backup);

// Restore
byte[] backupData = Files.readAllBytes(Paths.get("key-backup.blob"));
KeyVaultKey restoredKey = keyClient.restoreKeyBackup(backupData);
```

## 密钥轮换

```java
// Rotate to new version
KeyVaultKey rotatedKey = keyClient.rotateKey("my-key");
System.out.println("New version: " + rotatedKey.getProperties().getVersion());

// Set rotation policy
KeyRotationPolicy policy = new KeyRotationPolicy()
    .setExpiresIn("P90D")  // Expire after 90 days
    .setLifetimeActions(Arrays.asList(
        new KeyRotationLifetimeAction(KeyRotationPolicyAction.ROTATE)
            .setTimeBeforeExpiry("P30D")));  // Rotate 30 days before expiry

keyClient.updateKeyRotationPolicy("my-key", policy);

// Get rotation policy
KeyRotationPolicy currentPolicy = keyClient.getKeyRotationPolicy("my-key");
```

## 导入密钥

```java
import com.azure.security.keyvault.keys.models.ImportKeyOptions;
import com.azure.security.keyvault.keys.models.JsonWebKey;

// Import existing key material
JsonWebKey jsonWebKey = new JsonWebKey()
    .setKeyType(KeyType.RSA)
    .setN(modulus)
    .setE(exponent)
    .setD(privateExponent)
    // ... other RSA components
    ;

ImportKeyOptions importOptions = new ImportKeyOptions("imported-key", jsonWebKey)
    .setHardwareProtected(false);

KeyVaultKey importedKey = keyClient.importKey(importOptions);
```

## 加密算法

| 算法 | 密钥类型 | 说明 |
|-----------|----------|------|
| `RSA1_5` | RSA | RSAES-PKCS1-v1_5 |
| `RSA_OAEP` | RSA | RSAES with OAEP（推荐） |
| `RSA_OAEP_256` | RSA | RSAES with OAEP using SHA-256 |
| `A128GCM` | OCT | AES-GCM 128 位 |
| `A256GCM` | OCT | AES-GCM 256 位 |
| `A128CBC` | OCT | AES-CBC 128 位 |
| `A256CBC` | OCT | AES-CBC 256 位 |

## 签名算法

| 算法 | 密钥类型 | 哈希 |
|-----------|----------|------|
| `RS256` | RSA | SHA-256 |
| `RS384` | RSA | SHA-384 |
| `RS512` | RSA | SHA-512 |
| `PS256` | RSA | SHA-256 (PSS) |
| `ES256` | EC P-256 | SHA-256 |
| `ES384` | EC P-384 | SHA-384 |
| `ES512` | EC P-521 | SHA-512 |

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;
import com.azure.core.exception.ResourceNotFoundException;

try {
    KeyVaultKey key = keyClient.getKey("non-existent-key");
} catch (ResourceNotFoundException e) {
    System.out.println("Key not found: " + e.getMessage());
} catch (HttpResponseException e) {
    System.out.println("HTTP error " + e.getResponse().getStatusCode());
    System.out.println("Message: " + e.getMessage());
}
```

## 环境变量

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net
```

## 最佳实践

1. **生产环境使用 HSM 密钥** — 对敏感密钥设置 `setHardwareProtected(true)`
2. **启用软删除** — 防止意外删除
3. **密钥轮换** — 设置自动轮换策略
4. **最小权限** — 为不同操作使用单独的密钥
5. **尽可能本地加密** — 使用带有本地密钥材料的 `CryptographyClient` 以减少网络往返

## 触发词

- "Key Vault keys Java"、"加密密钥 Java"
- "加密解密 Java"、"签名验证 Java"
- "RSA 密钥"、"EC 密钥"、"HSM 密钥"
- "密钥轮换"、"包装解包密钥"

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
