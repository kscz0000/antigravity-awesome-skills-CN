---
name: azure-security-keyvault-keys-dotnet
description: Azure Key Vault 密钥 .NET SDK。用于管理 Azure Key Vault 和 Managed HSM 中密钥的客户端库。支持密钥创建、轮换、加密、解密、签名和验证。当用户要求'管理 Azure Key Vault 密钥'、'Key Vault 加密解密'、'密钥轮换策略'、'Key Vault 签名验证'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.Security.KeyVault.Keys (.NET)

用于管理 Azure Key Vault 和 Managed HSM 中密钥的客户端库。

## 安装

```bash
dotnet add package Azure.Security.KeyVault.Keys
dotnet add package Azure.Identity
```

**当前版本**：4.7.0（稳定版）

## 环境变量

```bash
KEY_VAULT_NAME=<your-key-vault-name>
# 或完整 URI
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net
```

## 客户端层级

```
KeyClient (密钥管理)
├── CreateKey / CreateRsaKey / CreateEcKey
├── GetKey / GetKeys
├── UpdateKeyProperties
├── DeleteKey / PurgeDeletedKey
├── BackupKey / RestoreKey
└── GetCryptographyClient() → CryptographyClient

CryptographyClient (加密操作)
├── Encrypt / Decrypt
├── WrapKey / UnwrapKey
├── Sign / Verify
└── SignData / VerifyData

KeyResolver (密钥解析)
└── Resolve(keyId) → CryptographyClient
```

## 身份验证

### DefaultAzureCredential（推荐）

```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Keys;

var keyVaultName = Environment.GetEnvironmentVariable("KEY_VAULT_NAME");
var kvUri = $"https://{keyVaultName}.vault.azure.net";

var client = new KeyClient(new Uri(kvUri), new DefaultAzureCredential());
```

### 服务主体

```csharp
var credential = new ClientSecretCredential(
    tenantId: "<tenant-id>",
    clientId: "<client-id>",
    clientSecret: "<client-secret>");

var client = new KeyClient(new Uri(kvUri), credential);
```

## 密钥管理

### 创建密钥

```csharp
// 创建 RSA 密钥
KeyVaultKey rsaKey = await client.CreateKeyAsync("my-rsa-key", KeyType.Rsa);
Console.WriteLine($"Created key: {rsaKey.Name}, Type: {rsaKey.KeyType}");

// 创建带选项的 RSA 密钥
var rsaOptions = new CreateRsaKeyOptions("my-rsa-key-2048")
{
    KeySize = 2048,
    HardwareProtected = false, // true 表示 HSM 保护
    ExpiresOn = DateTimeOffset.UtcNow.AddYears(1),
    NotBefore = DateTimeOffset.UtcNow,
    Enabled = true
};
rsaOptions.KeyOperations.Add(KeyOperation.Encrypt);
rsaOptions.KeyOperations.Add(KeyOperation.Decrypt);

KeyVaultKey rsaKey2 = await client.CreateRsaKeyAsync(rsaOptions);

// 创建 EC 密钥
var ecOptions = new CreateEcKeyOptions("my-ec-key")
{
    CurveName = KeyCurveName.P256,
    HardwareProtected = true // HSM 保护
};
KeyVaultKey ecKey = await client.CreateEcKeyAsync(ecOptions);

// 创建 Oct（对称）密钥用于包装/解包
var octOptions = new CreateOctKeyOptions("my-oct-key")
{
    KeySize = 256,
    HardwareProtected = true
};
KeyVaultKey octKey = await client.CreateOctKeyAsync(octOptions);
```

### 检索密钥

```csharp
// 获取特定密钥（最新版本）
KeyVaultKey key = await client.GetKeyAsync("my-rsa-key");
Console.WriteLine($"Key ID: {key.Id}");
Console.WriteLine($"Key Type: {key.KeyType}");
Console.WriteLine($"Version: {key.Properties.Version}");

// 获取特定版本
KeyVaultKey keyVersion = await client.GetKeyAsync("my-rsa-key", "version-id");

// 列出所有密钥
await foreach (KeyProperties keyProps in client.GetPropertiesOfKeysAsync())
{
    Console.WriteLine($"Key: {keyProps.Name}, Enabled: {keyProps.Enabled}");
}

// 列出密钥版本
await foreach (KeyProperties version in client.GetPropertiesOfKeyVersionsAsync("my-rsa-key"))
{
    Console.WriteLine($"Version: {version.Version}, Created: {version.CreatedOn}");
}
```

### 更新密钥属性

```csharp
KeyVaultKey key = await client.GetKeyAsync("my-rsa-key");

key.Properties.ExpiresOn = DateTimeOffset.UtcNow.AddYears(2);
key.Properties.Tags["environment"] = "production";

KeyVaultKey updatedKey = await client.UpdateKeyPropertiesAsync(key.Properties);
```

### 删除和清除密钥

```csharp
// 启动删除操作
DeleteKeyOperation operation = await client.StartDeleteKeyAsync("my-rsa-key");

// 等待删除完成（清除前必须等待）
await operation.WaitForCompletionAsync();
Console.WriteLine($"Deleted key scheduled purge date: {operation.Value.ScheduledPurgeDate}");

// 立即清除（如果启用了软删除）
await client.PurgeDeletedKeyAsync("my-rsa-key");

// 或恢复已删除的密钥
KeyVaultKey recoveredKey = await client.StartRecoverDeletedKeyAsync("my-rsa-key");
```

### 备份和恢复

```csharp
// 备份密钥
byte[] backup = await client.BackupKeyAsync("my-rsa-key");
await File.WriteAllBytesAsync("key-backup.bin", backup);

// 恢复密钥
byte[] backupData = await File.ReadAllBytesAsync("key-backup.bin");
KeyVaultKey restoredKey = await client.RestoreKeyBackupAsync(backupData);
```

## 加密操作

### 获取 CryptographyClient

```csharp
// 从 KeyClient 获取
KeyVaultKey key = await client.GetKeyAsync("my-rsa-key");
CryptographyClient cryptoClient = client.GetCryptographyClient(
    key.Name, 
    key.Properties.Version);

// 或使用密钥 ID 直接创建
CryptographyClient cryptoClient = new CryptographyClient(
    new Uri("https://myvault.vault.azure.net/keys/my-rsa-key/version"),
    new DefaultAzureCredential());
```

### 加密和解密

```csharp
byte[] plaintext = Encoding.UTF8.GetBytes("Secret message to encrypt");

// 加密
EncryptResult encryptResult = await cryptoClient.EncryptAsync(
    EncryptionAlgorithm.RsaOaep256, 
    plaintext);
Console.WriteLine($"Encrypted: {Convert.ToBase64String(encryptResult.Ciphertext)}");

// 解密
DecryptResult decryptResult = await cryptoClient.DecryptAsync(
    EncryptionAlgorithm.RsaOaep256, 
    encryptResult.Ciphertext);
string decrypted = Encoding.UTF8.GetString(decryptResult.Plaintext);
Console.WriteLine($"Decrypted: {decrypted}");
```

### 密钥包装和解包

```csharp
// 要包装的密钥（例如 AES 密钥）
byte[] keyToWrap = new byte[32]; // 256 位密钥
RandomNumberGenerator.Fill(keyToWrap);

// 包装密钥
WrapResult wrapResult = await cryptoClient.WrapKeyAsync(
    KeyWrapAlgorithm.RsaOaep256, 
    keyToWrap);

// 解包密钥
UnwrapResult unwrapResult = await cryptoClient.UnwrapKeyAsync(
    KeyWrapAlgorithm.RsaOaep256, 
    wrapResult.EncryptedKey);
```

### 签名和验证

```csharp
// 要签名的数据
byte[] data = Encoding.UTF8.GetBytes("Data to sign");

// 签名数据（内部计算哈希）
SignResult signResult = await cryptoClient.SignDataAsync(
    SignatureAlgorithm.RS256, 
    data);

// 验证签名
VerifyResult verifyResult = await cryptoClient.VerifyDataAsync(
    SignatureAlgorithm.RS256, 
    data, 
    signResult.Signature);
Console.WriteLine($"Signature valid: {verifyResult.IsValid}");

// 或对预计算的哈希签名
using var sha256 = SHA256.Create();
byte[] hash = sha256.ComputeHash(data);

SignResult signHashResult = await cryptoClient.SignAsync(
    SignatureAlgorithm.RS256, 
    hash);
```

## 密钥解析器

```csharp
using Azure.Security.KeyVault.Keys.Cryptography;

var resolver = new KeyResolver(new DefaultAzureCredential());

// 通过密钥 ID 解析获取 CryptographyClient
CryptographyClient cryptoClient = await resolver.ResolveAsync(
    new Uri("https://myvault.vault.azure.net/keys/my-key/version"));

// 用于加密
EncryptResult result = await cryptoClient.EncryptAsync(
    EncryptionAlgorithm.RsaOaep256, 
    plaintext);
```

## 密钥轮换

```csharp
// 轮换密钥（创建新版本）
KeyVaultKey rotatedKey = await client.RotateKeyAsync("my-rsa-key");
Console.WriteLine($"New version: {rotatedKey.Properties.Version}");

// 获取轮换策略
KeyRotationPolicy policy = await client.GetKeyRotationPolicyAsync("my-rsa-key");

// 更新轮换策略
policy.ExpiresIn = "P90D"; // 90 天
policy.LifetimeActions.Add(new KeyRotationLifetimeAction
{
    Action = KeyRotationPolicyAction.Rotate,
    TimeBeforeExpiry = "P30D" // 到期前 30 天轮换
});

await client.UpdateKeyRotationPolicyAsync("my-rsa-key", policy);
```

## 密钥类型参考

| 类型 | 用途 |
|------|------|
| `KeyClient` | 密钥管理操作 |
| `CryptographyClient` | 加密操作 |
| `KeyResolver` | 将密钥 ID 解析为 CryptographyClient |
| `KeyVaultKey` | 包含加密材料的密钥 |
| `KeyProperties` | 密钥元数据（不含加密材料） |
| `CreateRsaKeyOptions` | RSA 密钥创建选项 |
| `CreateEcKeyOptions` | EC 密钥创建选项 |
| `CreateOctKeyOptions` | 对称密钥选项 |
| `EncryptResult` | 加密结果 |
| `DecryptResult` | 解密结果 |
| `SignResult` | 签名结果 |
| `VerifyResult` | 验证结果 |
| `WrapResult` | 密钥包装结果 |
| `UnwrapResult` | 密钥解包结果 |

## 算法参考

### 加密算法
| 算法 | 密钥类型 | 说明 |
|------|----------|------|
| `RsaOaep` | RSA | RSA-OAEP |
| `RsaOaep256` | RSA | RSA-OAEP-256 |
| `Rsa15` | RSA | RSA 1.5（旧版） |
| `A128Gcm` | Oct | AES-128-GCM |
| `A256Gcm` | Oct | AES-256-GCM |

### 签名算法
| 算法 | 密钥类型 | 说明 |
|------|----------|------|
| `RS256` | RSA | RSASSA-PKCS1-v1_5 SHA-256 |
| `RS384` | RSA | RSASSA-PKCS1-v1_5 SHA-384 |
| `RS512` | RSA | RSASSA-PKCS1-v1_5 SHA-512 |
| `PS256` | RSA | RSASSA-PSS SHA-256 |
| `ES256` | EC | ECDSA P-256 SHA-256 |
| `ES384` | EC | ECDSA P-384 SHA-384 |
| `ES512` | EC | ECDSA P-521 SHA-512 |

### 密钥包装算法
| 算法 | 密钥类型 | 说明 |
|------|----------|------|
| `RsaOaep` | RSA | RSA-OAEP |
| `RsaOaep256` | RSA | RSA-OAEP-256 |
| `A128KW` | Oct | AES-128 密钥包装 |
| `A256KW` | Oct | AES-256 密钥包装 |

## 最佳实践

1. **使用托管标识** — 优先使用 `DefaultAzureCredential` 而非机密
2. **启用软删除** — 防止意外删除
3. **使用 HSM 保护的密钥** — 对敏感密钥设置 `HardwareProtected = true`
4. **实施密钥轮换** — 使用自动轮换策略
5. **限制密钥操作** — 仅启用所需的 `KeyOperations`
6. **设置过期日期** — 始终为密钥设置 `ExpiresOn`
7. **使用特定版本** — 在生产环境中固定版本
8. **缓存 CryptographyClient** — 多次操作时复用

## 错误处理

```csharp
using Azure;

try
{
    KeyVaultKey key = await client.GetKeyAsync("my-key");
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Key not found");
}
catch (RequestFailedException ex) when (ex.Status == 403)
{
    Console.WriteLine("Access denied - check RBAC permissions");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Key Vault error: {ex.Status} - {ex.Message}");
}
```

## 所需 RBAC 角色

| 角色 | 权限 |
|------|------|
| Key Vault Crypto Officer | 完整密钥管理 |
| Key Vault Crypto User | 使用密钥进行加密操作 |
| Key Vault Reader | 读取密钥元数据 |

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.Security.KeyVault.Keys` | 密钥（本 SDK） | `dotnet add package Azure.Security.KeyVault.Keys` |
| `Azure.Security.KeyVault.Secrets` | 机密 | `dotnet add package Azure.Security.KeyVault.Secrets` |
| `Azure.Security.KeyVault.Certificates` | 证书 | `dotnet add package Azure.Security.KeyVault.Certificates` |
| `Azure.Identity` | 身份验证 | `dotnet add package Azure.Identity` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.Security.KeyVault.Keys |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.security.keyvault.keys |
| 快速入门 | https://learn.microsoft.com/azure/key-vault/keys/quick-create-net |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/keyvault/Azure.Security.KeyVault.Keys |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
