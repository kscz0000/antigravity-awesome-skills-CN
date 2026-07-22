# 配置管理 — UnifiedConfig 模式

后端微服务配置管理完整指南。

## 目录

- [UnifiedConfig 概述](#unifiedconfig-overview)
- [绝不直接使用 process.env](#never-use-processenv-directly)
- [配置结构](#configuration-structure)
- [环境专属配置](#environment-specific-configs)
- [密钥管理](#secrets-management)
- [迁移指南](#migration-guide)

---

## UnifiedConfig 概述

### 为什么选择 UnifiedConfig？

**process.env 的问题：**
- ❌ 无类型安全
- ❌ 无校验机制
- ❌ 难以测试
- ❌ 散落在代码各处
- ❌ 无默认值
- ❌ 拼写错误导致运行时才报错

**UnifiedConfig 的优势：**
- ✅ 类型安全的配置
- ✅ 单一数据源
- ✅ 启动时即完成校验
- ✅ 可用 mock 轻松测试
- ✅ 结构清晰
- ✅ 回退到环境变量

---

## 绝不直接使用 process.env

### 规则

```typescript
// ❌ NEVER DO THIS
const timeout = parseInt(process.env.TIMEOUT_MS || '5000');
const dbHost = process.env.DB_HOST || 'localhost';

// ✅ ALWAYS DO THIS
import { config } from './config/unifiedConfig';
const timeout = config.timeouts.default;
const dbHost = config.database.host;
```

### 为什么重要

**典型问题示例：**
```typescript
// Typo in environment variable name
const host = process.env.DB_HSOT; // undefined! No error!

// Type safety
const port = process.env.PORT; // string! Need parseInt
const timeout = parseInt(process.env.TIMEOUT); // NaN if not set!
```

**使用 UnifiedConfig 后：**
```typescript
const port = config.server.port; // number, guaranteed
const timeout = config.timeouts.default; // number, with fallback
```

---

## 配置结构

### UnifiedConfig 接口

```typescript
export interface UnifiedConfig {
    database: {
        host: string;
        port: number;
        username: string;
        password: string;
        database: string;
    };
    server: {
        port: number;
        sessionSecret: string;
    };
    tokens: {
        jwt: string;
        inactivity: string;
        internal: string;
    };
    keycloak: {
        realm: string;
        client: string;
        baseUrl: string;
        secret: string;
    };
    aws: {
        region: string;
        emailQueueUrl: string;
        accessKeyId: string;
        secretAccessKey: string;
    };
    sentry: {
        dsn: string;
        environment: string;
        tracesSampleRate: number;
    };
    // ... more sections
}
```

### 实现模式

**文件：** `/blog-api/src/config/unifiedConfig.ts`

```typescript
import * as fs from 'fs';
import * as path from 'path';
import * as ini from 'ini';

const configPath = path.join(__dirname, '../../config.ini');
const iniConfig = ini.parse(fs.readFileSync(configPath, 'utf-8'));

export const config: UnifiedConfig = {
    database: {
        host: iniConfig.database?.host || process.env.DB_HOST || 'localhost',
        port: parseInt(iniConfig.database?.port || process.env.DB_PORT || '3306'),
        username: iniConfig.database?.username || process.env.DB_USER || 'root',
        password: iniConfig.database?.password || process.env.DB_PASSWORD || '',
        database: iniConfig.database?.database || process.env.DB_NAME || 'blog_dev',
    },
    server: {
        port: parseInt(iniConfig.server?.port || process.env.PORT || '3002'),
        sessionSecret: iniConfig.server?.sessionSecret || process.env.SESSION_SECRET || 'dev-secret',
    },
    // ... more configuration
};

// Validate critical config
if (!config.tokens.jwt) {
    throw new Error('JWT secret not configured!');
}
```

**关键要点：**
- 优先从 config.ini 读取
- 回退到 process.env
- 开发环境提供默认值
- 启动时即完成校验
- 类型安全访问

---

## 环境专属配置

### config.ini 结构

```ini
[database]
host = localhost
port = 3306
username = root
password = password1
database = blog_dev

[server]
port = 3002
sessionSecret = your-secret-here

[tokens]
jwt = your-jwt-secret
inactivity = 30m
internal = internal-api-token

[keycloak]
realm = myapp
client = myapp-client
baseUrl = http://localhost:8080
secret = keycloak-client-secret

[sentry]
dsn = https://your-sentry-dsn
environment = development
tracesSampleRate = 0.1
```

### 环境变量覆盖

```bash
# .env file (optional overrides)
DB_HOST=production-db.example.com
DB_PASSWORD=secure-password
PORT=80
```

**优先级（从高到低）：**
1. config.ini（最高优先级）
2. process.env 环境变量
3. 硬编码默认值（最低优先级）

---

## 密钥管理

### 切勿提交密钥

```gitignore
# .gitignore
config.ini
.env
sentry.ini
*.pem
*.key
```

### 生产环境使用环境变量

```typescript
// Development: config.ini
// Production: Environment variables

export const config: UnifiedConfig = {
    database: {
        password: process.env.DB_PASSWORD || iniConfig.database?.password || '',
    },
    tokens: {
        jwt: process.env.JWT_SECRET || iniConfig.tokens?.jwt || '',
    },
};
```

---

## 迁移指南

### 查找所有 process.env 用法

```bash
grep -r "process.env" blog-api/src/ --include="*.ts" | wc -l
```

### 迁移示例

**迁移前：**
```typescript
// Scattered throughout code
const timeout = parseInt(process.env.OPENID_HTTP_TIMEOUT_MS || '15000');
const keycloakUrl = process.env.KEYCLOAK_BASE_URL;
const jwtSecret = process.env.JWT_SECRET;
```

**迁移后：**
```typescript
import { config } from './config/unifiedConfig';

const timeout = config.keycloak.timeout;
const keycloakUrl = config.keycloak.baseUrl;
const jwtSecret = config.tokens.jwt;
```

**收益：**
- 类型安全
- 集中管理
- 易于测试
- 启动时即完成校验

---

**相关文件：**
- SKILL.md
- [testing-guide.md](testing-guide.md)
