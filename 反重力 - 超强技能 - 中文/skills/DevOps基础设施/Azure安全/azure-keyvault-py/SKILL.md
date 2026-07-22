---
name: azure-keyvault-py
description: Azure Key Vault Python SDK，用于机密、密钥和证书的安全存储与管理。当用户要求'管理 Azure Key Vault 机密/密钥/证书'、'使用 Python 操作 Key Vault'、'安全存储机密和证书'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Key Vault SDK for Python

密钥、加密密钥和证书的安全存储与管理。

## 安装

```bash
# Secrets
pip install azure-keyvault-secrets azure-identity

# Keys (cryptographic operations)
pip install azure-keyvault-keys azure-identity

# Certificates
pip install azure-keyvault-certificates azure-identity

# All
pip install azure-keyvault-secrets azure-keyvault-keys azure-keyvault-certificates azure-identity
```

## 环境变量

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net/
```

## Secrets

### SecretClient 初始化

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
vault_url = "https://<vault-name>.vault.azure.net/"

client = SecretClient(vault_url=vault_url, credential=credential)
```

### Secret 操作

```python
# Set secret
secret = client.set_secret("database-password", "super-secret-value")
print(f"Created: {secret.name}, version: {secret.properties.version}")

# Get secret
secret = client.get_secret("database-password")
print(f"Value: {secret.value}")

# Get specific version
secret = client.get_secret("database-password", version="abc123")

# List secrets (names only, not values)
for secret_properties in client.list_properties_of_secrets():
    print(f"Secret: {secret_properties.name}")

# List versions
for version in client.list_properties_of_secret_versions("database-password"):
    print(f"Version: {version.version}, Created: {version.created_on}")

# Delete secret (soft delete)
poller = client.begin_delete_secret("database-password")
deleted_secret = poller.result()

# Purge (permanent delete, if soft-delete enabled)
client.purge_deleted_secret("database-password")

# Recover deleted secret
client.begin_recover_deleted_secret("database-password").result()
```

## Keys

### KeyClient 初始化

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient

credential = DefaultAzureCredential()
vault_url = "https://<vault-name>.vault.azure.net/"

client = KeyClient(vault_url=vault_url, credential=credential)
```

### Key 操作

```python
from azure.keyvault.keys import KeyType

# Create RSA key
rsa_key = client.create_rsa_key("rsa-key", size=2048)

# Create EC key
ec_key = client.create_ec_key("ec-key", curve="P-256")

# Get key
key = client.get_key("rsa-key")
print(f"Key type: {key.key_type}")

# List keys
for key_properties in client.list_properties_of_keys():
    print(f"Key: {key_properties.name}")

# Delete key
poller = client.begin_delete_key("rsa-key")
deleted_key = poller.result()
```

### 加密操作

```python
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

# Get crypto client for a specific key
crypto_client = CryptographyClient(key, credential=credential)
# Or from key ID
crypto_client = CryptographyClient(
    "https://<vault>.vault.azure.net/keys/<key-name>/<version>",
    credential=credential
)

# Encrypt
plaintext = b"Hello, Key Vault!"
result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, plaintext)
ciphertext = result.ciphertext

# Decrypt
result = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, ciphertext)
decrypted = result.plaintext

# Sign
from azure.keyvault.keys.crypto import SignatureAlgorithm
import hashlib

digest = hashlib.sha256(b"data to sign").digest()
result = crypto_client.sign(SignatureAlgorithm.rs256, digest)
signature = result.signature

# Verify
result = crypto_client.verify(SignatureAlgorithm.rs256, digest, signature)
print(f"Valid: {result.is_valid}")
```

## Certificates

### CertificateClient 初始化

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.certificates import CertificateClient, CertificatePolicy

credential = DefaultAzureCredential()
vault_url = "https://<vault-name>.vault.azure.net/"

client = CertificateClient(vault_url=vault_url, credential=credential)
```

### Certificate 操作

```python
# Create self-signed certificate
policy = CertificatePolicy.get_default()
poller = client.begin_create_certificate("my-cert", policy=policy)
certificate = poller.result()

# Get certificate
certificate = client.get_certificate("my-cert")
print(f"Thumbprint: {certificate.properties.x509_thumbprint.hex()}")

# Get certificate with private key (as secret)
from azure.keyvault.secrets import SecretClient
secret_client = SecretClient(vault_url=vault_url, credential=credential)
cert_secret = secret_client.get_secret("my-cert")
# cert_secret.value contains PEM or PKCS12

# List certificates
for cert in client.list_properties_of_certificates():
    print(f"Certificate: {cert.name}")

# Delete certificate
poller = client.begin_delete_certificate("my-cert")
deleted = poller.result()
```

## 客户端类型表

| 客户端 | 包 | 用途 |
|--------|---------|---------|
| `SecretClient` | `azure-keyvault-secrets` | 存储/检索密钥 |
| `KeyClient` | `azure-keyvault-keys` | 管理加密密钥 |
| `CryptographyClient` | `azure-keyvault-keys` | 加密/解密/签名/验证 |
| `CertificateClient` | `azure-keyvault-certificates` | 管理证书 |

## 异步客户端

```python
from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient

async def get_secret():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    async with client:
        secret = await client.get_secret("my-secret")
        print(secret.value)

import asyncio
asyncio.run(get_secret())
```

## 错误处理

```python
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

try:
    secret = client.get_secret("nonexistent")
except ResourceNotFoundError:
    print("Secret not found")
except HttpResponseError as e:
    if e.status_code == 403:
        print("Access denied - check RBAC permissions")
    raise
```

## 最佳实践

1. **使用 DefaultAzureCredential** 进行身份验证
2. **使用托管标识** 在 Azure 托管应用中
3. **启用软删除** 以便恢复（默认已启用）
4. **使用 RBAC** 而非访问策略，实现细粒度控制
5. **定期轮换密钥**，利用版本管理
6. **使用 Key Vault 引用** 在 App Service/Functions 配置中
7. **适当缓存密钥** 以减少 API 调用
8. **使用异步客户端** 处理高吞吐量场景

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
