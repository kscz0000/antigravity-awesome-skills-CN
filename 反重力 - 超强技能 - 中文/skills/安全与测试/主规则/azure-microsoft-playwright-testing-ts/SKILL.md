---
name: azure-microsoft-playwright-testing-ts
description: "使用云端托管浏览器大规模运行 Playwright 测试，并集成 Azure 门户报告。当用户要求'Azure Playwright 测试'、'云端 Playwright'、'Playwright 大规模测试'、'Azure 浏览器测试'、'Playwright 云端执行'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Playwright Workspaces SDK for TypeScript

使用云端托管浏览器大规模运行 Playwright 测试，并集成 Azure 门户报告。

> **迁移通知：** `@azure/microsoft-playwright-testing` 已于 **2026 年 3 月 8 日**退役。请改用 `@azure/playwright`。参见[迁移指南](https://aka.ms/mpt/migration-guidance)。

## 安装

```bash
# Recommended: Auto-generates config
npm init @azure/playwright@latest

# Manual installation
npm install @azure/playwright --save-dev
npm install @playwright/test@^1.47 --save-dev
npm install @azure/identity --save-dev
```

**要求：**
- Playwright 版本 1.47+（基本用法）
- Playwright 版本 1.57+（Azure 报告器功能）

## 环境变量

```bash
PLAYWRIGHT_SERVICE_URL=wss://eastus.api.playwright.microsoft.com/playwrightworkspaces/{workspace-id}/browsers
```

## 身份认证

### Microsoft Entra ID（推荐）

```bash
# Sign in with Azure CLI
az login
```

```typescript
// playwright.service.config.ts
import { defineConfig } from "@playwright/test";
import { createAzurePlaywrightConfig, ServiceOS } from "@azure/playwright";
import { DefaultAzureCredential } from "@azure/identity";
import config from "./playwright.config";

export default defineConfig(
  config,
  createAzurePlaywrightConfig(config, {
    os: ServiceOS.LINUX,
    credential: new DefaultAzureCredential(),
  })
);
```

### 自定义凭据

```typescript
import { ManagedIdentityCredential } from "@azure/identity";
import { createAzurePlaywrightConfig } from "@azure/playwright";

export default defineConfig(
  config,
  createAzurePlaywrightConfig(config, {
    credential: new ManagedIdentityCredential(),
  })
);
```

## 核心工作流

### 服务配置

```typescript
// playwright.service.config.ts
import { defineConfig } from "@playwright/test";
import { createAzurePlaywrightConfig, ServiceOS } from "@azure/playwright";
import { DefaultAzureCredential } from "@azure/identity";
import config from "./playwright.config";

export default defineConfig(
  config,
  createAzurePlaywrightConfig(config, {
    os: ServiceOS.LINUX,
    connectTimeout: 30000,
    exposeNetwork: "<loopback>",
    credential: new DefaultAzureCredential(),
  })
);
```

### 运行测试

```bash
npx playwright test --config=playwright.service.config.ts --workers=20
```

### 使用 Azure 报告器

```typescript
import { defineConfig } from "@playwright/test";
import { createAzurePlaywrightConfig, ServiceOS } from "@azure/playwright";
import { DefaultAzureCredential } from "@azure/identity";
import config from "./playwright.config";

export default defineConfig(
  config,
  createAzurePlaywrightConfig(config, {
    os: ServiceOS.LINUX,
    credential: new DefaultAzureCredential(),
  }),
  {
    reporter: [
      ["html", { open: "never" }],
      ["@azure/playwright/reporter"],
    ],
  }
);
```

### 手动浏览器连接

```typescript
import playwright, { test, expect, BrowserType } from "@playwright/test";
import { getConnectOptions } from "@azure/playwright";

test("manual connection", async ({ browserName }) => {
  const { wsEndpoint, options } = await getConnectOptions();
  const browser = await (playwright[browserName] as BrowserType).connect(wsEndpoint, options);
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto("https://example.com");
  await expect(page).toHaveTitle(/Example/);

  await browser.close();
});
```

## 配置选项

```typescript
type PlaywrightServiceAdditionalOptions = {
  serviceAuthType?: "ENTRA_ID" | "ACCESS_TOKEN";  // Default: ENTRA_ID
  os?: "linux" | "windows";                        // Default: linux
  runName?: string;                                // Custom run name for portal
  connectTimeout?: number;                         // Default: 30000ms
  exposeNetwork?: string;                          // Default: <loopback>
  credential?: TokenCredential;                    // REQUIRED for Entra ID
};
```

### ServiceOS 枚举

```typescript
import { ServiceOS } from "@azure/playwright";

// Available values
ServiceOS.LINUX   // "linux" - default
ServiceOS.WINDOWS // "windows"
```

### ServiceAuth 枚举

```typescript
import { ServiceAuth } from "@azure/playwright";

// Available values
ServiceAuth.ENTRA_ID      // Recommended - uses credential
ServiceAuth.ACCESS_TOKEN  // Use PLAYWRIGHT_SERVICE_ACCESS_TOKEN env var
```

## CI/CD 集成

### GitHub Actions

```yaml
name: playwright-ts
on: [push, pull_request]

permissions:
  id-token: write
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - run: npm ci
      
      - name: Run Tests
        env:
          PLAYWRIGHT_SERVICE_URL: ${{ secrets.PLAYWRIGHT_SERVICE_URL }}
        run: npx playwright test -c playwright.service.config.ts --workers=20
```

### Azure Pipelines

```yaml
- task: AzureCLI@2
  displayName: Run Playwright Tests
  env:
    PLAYWRIGHT_SERVICE_URL: $(PLAYWRIGHT_SERVICE_URL)
  inputs:
    azureSubscription: My_Service_Connection
    scriptType: pscore
    inlineScript: |
      npx playwright test -c playwright.service.config.ts --workers=20
    addSpnToEnvironment: true
```

## 核心类型

```typescript
import {
  createAzurePlaywrightConfig,
  getConnectOptions,
  ServiceOS,
  ServiceAuth,
  ServiceEnvironmentVariable,
} from "@azure/playwright";

import type {
  OsType,
  AuthenticationType,
  BrowserConnectOptions,
  PlaywrightServiceAdditionalOptions,
} from "@azure/playwright";
```

## 从旧包迁移

| 旧版（`@azure/microsoft-playwright-testing`） | 新版（`@azure/playwright`） |
|---------------------------------------------|---------------------------|
| `getServiceConfig()` | `createAzurePlaywrightConfig()` |
| `timeout` 选项 | `connectTimeout` 选项 |
| `runId` 选项 | `runName` 选项 |
| `useCloudHostedBrowsers` 选项 | 已移除（始终启用） |
| `@azure/microsoft-playwright-testing/reporter` | `@azure/playwright/reporter` |
| 隐式凭据 | 显式 `credential` 参数 |

### 迁移前（旧版）

```typescript
import { getServiceConfig, ServiceOS } from "@azure/microsoft-playwright-testing";

export default defineConfig(
  config,
  getServiceConfig(config, {
    os: ServiceOS.LINUX,
    timeout: 30000,
    useCloudHostedBrowsers: true,
  }),
  {
    reporter: [["@azure/microsoft-playwright-testing/reporter"]],
  }
);
```

### 迁移后（新版）

```typescript
import { createAzurePlaywrightConfig, ServiceOS } from "@azure/playwright";
import { DefaultAzureCredential } from "@azure/identity";

export default defineConfig(
  config,
  createAzurePlaywrightConfig(config, {
    os: ServiceOS.LINUX,
    connectTimeout: 30000,
    credential: new DefaultAzureCredential(),
  }),
  {
    reporter: [
      ["html", { open: "never" }],
      ["@azure/playwright/reporter"],
    ],
  }
);
```

## 最佳实践

1. **使用 Entra ID 认证** — 比访问令牌更安全
2. **提供显式凭据** — 始终传入 `credential: new DefaultAzureCredential()`
3. **启用产物** — 在配置中设置 `trace: "on-first-retry"`、`video: "retain-on-failure"`
4. **扩展 Worker 数量** — 使用 `--workers=20` 或更高实现并行执行
5. **区域选择** — 选择最接近测试目标的区域
6. **HTML 报告器优先** — 使用 Azure 报告器时，将 HTML 报告器列在 Azure 报告器之前

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
