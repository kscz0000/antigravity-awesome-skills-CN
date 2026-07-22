---
title: 为 DBOS 使用正确的测试设置
impact: LOW-MEDIUM
impactDescription: 通过正确的 DBOS 生命周期管理确保一致的测试结果
tags: testing, jest, setup, integration, mock
---

## 为 DBOS 使用正确的测试设置

DBOS 应用可通过单元测试（模拟 DBOS）或集成测试（真实 Postgres 数据库）进行测试。

**错误（测试之间无生命周期管理）：**

```typescript
// 测试共享状态 - 结果不一致！
describe("tests", () => {
  it("test one", async () => {
    await myWorkflow("input");
  });
  it("test two", async () => {
    // 上一个测试的状态泄漏到本测试
    await myWorkflow("input");
  });
});
```

**正确（使用 mock 进行单元测试）：**

```typescript
// 模拟 DBOS - 无需 Postgres
jest.mock("@dbos-inc/dbos-sdk", () => ({
  DBOS: {
    registerWorkflow: jest.fn((fn) => fn),
    runStep: jest.fn((fn) => fn()),
    setEvent: jest.fn(),
    recv: jest.fn(),
    startWorkflow: jest.fn(),
    workflowID: "test-workflow-id",
  },
}));

describe("workflow unit tests", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should process data", async () => {
    jest.mocked(DBOS.recv).mockResolvedValue("success");
    await myWorkflow("input");
    expect(DBOS.setEvent).toHaveBeenCalledWith("status", "done");
  });
});
```

模拟 `registerWorkflow` 直接返回函数本身（不用持久化工作流代码包装）。

**正确（使用 Postgres 进行集成测试）：**

```typescript
import { DBOS, DBOSConfig } from "@dbos-inc/dbos-sdk";
import { Client } from "pg";

async function resetDatabase(databaseUrl: string) {
  const dbName = new URL(databaseUrl).pathname.slice(1);
  const postgresDatabaseUrl = new URL(databaseUrl);
  postgresDatabaseUrl.pathname = "/postgres";
  const client = new Client({ connectionString: postgresDatabaseUrl.toString() });
  await client.connect();
  try {
    await client.query(`DROP DATABASE IF EXISTS ${dbName} WITH (FORCE)`);
    await client.query(`CREATE DATABASE ${dbName}`);
  } finally {
    await client.end();
  }
}

describe("integration tests", () => {
  beforeEach(async () => {
    const databaseUrl = process.env.DBOS_TEST_DATABASE_URL;
    if (!databaseUrl) throw Error("DBOS_TEST_DATABASE_URL must be set");
    await DBOS.shutdown();
    await resetDatabase(databaseUrl);
    DBOS.setConfig({ name: "my-integration-test", systemDatabaseUrl: databaseUrl });
    await DBOS.launch();
  }, 10000);

  afterEach(async () => {
    await DBOS.shutdown();
  });

  it("should complete workflow", async () => {
    const result = await myWorkflow("test-input");
    expect(result).toBe("expected-output");
  });
});
```

要点：
- 在重置和重新配置前调用 `DBOS.shutdown()`
- 在测试之间重置数据库以保持隔离
- 设置较宽的 `beforeEach` 超时（10s）用于数据库设置
- 若要重新注册函数，使用 `DBOS.shutdown({ deregister: true })`

参考：[Testing & Mocking](https://docs.dbos.dev/typescript/tutorials/testing)
