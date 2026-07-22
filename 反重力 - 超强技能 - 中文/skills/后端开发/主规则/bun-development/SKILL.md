---
name: bun-development
description: "使用 Bun 运行时进行快速、现代的 JavaScript/TypeScript 开发，灵感来自 [oven-sh/bun](https://github.com/oven-sh/bun)。当用户要求使用 Bun 开发项目、从 Node.js 迁移到 Bun、优化开发速度、使用 Bun 内置工具或排查 Bun 问题时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

<!-- security-allowlist: curl-pipe-bash, irm-pipe-iex -->

# ⚡ Bun 开发

> 使用 Bun 运行时进行快速、现代的 JavaScript/TypeScript 开发，灵感来自 [oven-sh/bun](https://github.com/oven-sh/bun)。

## 何时使用此技能

在以下场景使用此技能：

- 使用 Bun 启动新的 JS/TS 项目
- 从 Node.js 迁移到 Bun
- 优化开发速度
- 使用 Bun 内置工具（打包器、测试运行器）
- 排查 Bun 特有的问题

---

## 1. 快速入门

### 1.1 安装

```bash
# macOS / Linux
curl -fsSL https://bun.sh/install | bash

# Windows
powershell -c "irm bun.sh/install.ps1 | iex"

# Homebrew
brew tap oven-sh/bun
brew install bun

# npm（如需）
npm install -g bun

# 升级
bun upgrade
```

### 1.2 为什么选择 Bun？

| 特性           | Bun            | Node.js                     |
| :------------- | :------------- | :-------------------------- |
| 启动时间       | ~25ms          | ~100ms+                     |
| 包安装速度     | 快 10-100 倍   | 基准                        |
| TypeScript     | 原生支持       | 需要转译器                  |
| JSX            | 原生支持       | 需要转译器                  |
| 测试运行器     | 内置           | 外部（Jest、Vitest）        |
| 打包器         | 内置           | 外部（Webpack、esbuild）    |

---

## 2. 项目设置

### 2.1 创建新项目

```bash
# 初始化项目
bun init

# 生成文件：
# ├── package.json
# ├── tsconfig.json
# ├── index.ts
# └── README.md

# 使用指定模板
bun create <template> <project-name>

# 示例
bun create react my-app        # React 应用
bun create next my-app         # Next.js 应用
bun create vite my-app         # Vite 应用
bun create elysia my-api       # Elysia API
```

### 2.2 package.json

```json
{
  "name": "my-bun-project",
  "version": "1.0.0",
  "module": "index.ts",
  "type": "module",
  "scripts": {
    "dev": "bun run --watch index.ts",
    "start": "bun run index.ts",
    "test": "bun test",
    "build": "bun build ./index.ts --outdir ./dist",
    "lint": "bunx eslint ."
  },
  "devDependencies": {
    "@types/bun": "latest"
  },
  "peerDependencies": {
    "typescript": "^5.0.0"
  }
}
```

### 2.3 tsconfig.json（Bun 优化版）

```json
{
  "compilerOptions": {
    "lib": ["ESNext"],
    "module": "esnext",
    "target": "esnext",
    "moduleResolution": "bundler",
    "moduleDetection": "force",
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "composite": true,
    "strict": true,
    "downlevelIteration": true,
    "skipLibCheck": true,
    "jsx": "react-jsx",
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "allowJs": true,
    "types": ["bun-types"]
  }
}
```

---

## 3. 包管理

### 3.1 安装包

```bash
# 从 package.json 安装
bun install              # 或 'bun i'

# 添加依赖
bun add express          # 生产依赖
bun add -d typescript    # 开发依赖
bun add -D @types/node   # 开发依赖（别名）
bun add --optional pkg   # 可选依赖

# 从指定注册源安装
bun add lodash --registry https://registry.npmmirror.com

# 安装指定版本
bun add react@18.2.0
bun add react@latest
bun add react@next

# 从 Git 仓库安装
bun add github:user/repo
bun add git+https://github.com/user/repo.git
```

### 3.2 删除与更新

```bash
# 删除包
bun remove lodash

# 更新包
bun update              # 更新全部
bun update lodash       # 更新指定包
bun update --latest     # 更新到最新版（忽略版本范围）

# 检查过时包
bun outdated
```

### 3.3 bunx（等同于 npx）

```bash
# 执行包的二进制文件
bunx prettier --write .
bunx tsc --init
bunx create-react-app my-app

# 使用指定版本
bunx -p typescript@4.9 tsc --version

# 无需安装直接运行
bunx cowsay "Hello from Bun!"
```

### 3.4 锁文件

```bash
# bun.lockb 是二进制锁文件（解析更快）
# 生成文本锁文件用于调试：
bun install --yarn    # 创建 yarn.lock

# 信任已有锁文件
bun install --frozen-lockfile
```

---

## 4. 运行代码

### 4.1 基本执行

```bash
# 直接运行 TypeScript（无需构建步骤！）
bun run index.ts

# 运行 JavaScript
bun run index.js

# 带参数运行
bun run server.ts --port 3000

# 运行 package.json 脚本
bun run dev
bun run build

# 简写形式（仅限脚本）
bun dev
bun build
```

### 4.2 监听模式

```bash
# 文件变更时自动重启
bun --watch run index.ts

# 热重载
bun --hot run server.ts
```

### 4.3 环境变量

```typescript
// .env 文件会自动加载！

// 访问环境变量
const apiKey = Bun.env.API_KEY;
const port = Bun.env.PORT ?? "3000";

// 或使用 process.env（兼容 Node.js）
const dbUrl = process.env.DATABASE_URL;
```

```bash
# 使用指定 env 文件运行
bun --env-file=.env.production run index.ts
```

---

## 5. 内置 API

### 5.1 文件系统（Bun.file）

```typescript
// 读取文件
const file = Bun.file("./data.json");
const text = await file.text();
const json = await file.json();
const buffer = await file.arrayBuffer();

// 文件信息
console.log(file.size); // 字节数
console.log(file.type); // MIME 类型

// 写入文件
await Bun.write("./output.txt", "Hello, Bun!");
await Bun.write("./data.json", JSON.stringify({ foo: "bar" }));

// 流式读取大文件
const reader = file.stream();
for await (const chunk of reader) {
  console.log(chunk);
}
```

### 5.2 HTTP 服务器（Bun.serve）

```typescript
const server = Bun.serve({
  port: 3000,

  fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/") {
      return new Response("Hello World!");
    }

    if (url.pathname === "/api/users") {
      return Response.json([
        { id: 1, name: "Alice" },
        { id: 2, name: "Bob" },
      ]);
    }

    return new Response("Not Found", { status: 404 });
  },

  error(error) {
    return new Response(`Error: ${error.message}`, { status: 500 });
  },
});

console.log(`Server running at http://localhost:${server.port}`);
```

### 5.3 WebSocket 服务器

```typescript
const server = Bun.serve({
  port: 3000,

  fetch(req, server) {
    // 升级为 WebSocket
    if (server.upgrade(req)) {
      return; // 已升级
    }
    return new Response("Upgrade failed", { status: 500 });
  },

  websocket: {
    open(ws) {
      console.log("Client connected");
      ws.send("Welcome!");
    },

    message(ws, message) {
      console.log(`Received: ${message}`);
      ws.send(`Echo: ${message}`);
    },

    close(ws) {
      console.log("Client disconnected");
    },
  },
});
```

### 5.4 SQLite（Bun.sql）

```typescript
import { Database } from "bun:sqlite";

const db = new Database("mydb.sqlite");

// 创建表
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
  )
`);

// 插入数据
const insert = db.prepare("INSERT INTO users (name, email) VALUES (?, ?)");
insert.run("Alice", "alice@example.com");

// 查询
const query = db.prepare("SELECT * FROM users WHERE name = ?");
const user = query.get("Alice");
console.log(user); // { id: 1, name: "Alice", email: "alice@example.com" }

// 查询全部
const allUsers = db.query("SELECT * FROM users").all();
```

### 5.5 密码哈希

```typescript
// 哈希密码
const password = "super-secret";
const hash = await Bun.password.hash(password);

// 验证密码
const isValid = await Bun.password.verify(password, hash);
console.log(isValid); // true

// 指定算法选项
const bcryptHash = await Bun.password.hash(password, {
  algorithm: "bcrypt",
  cost: 12,
});
```

---

## 6. 测试

### 6.1 基本测试

```typescript
// math.test.ts
import { describe, it, expect, beforeAll, afterAll } from "bun:test";

describe("Math operations", () => {
  it("adds two numbers", () => {
    expect(1 + 1).toBe(2);
  });

  it("subtracts two numbers", () => {
    expect(5 - 3).toBe(2);
  });
});
```

### 6.2 运行测试

```bash
# 运行全部测试
bun test

# 运行指定文件
bun test math.test.ts

# 运行匹配模式
bun test --grep "adds"

# 监听模式
bun test --watch

# 带覆盖率
bun test --coverage

# 设置超时
bun test --timeout 5000
```

### 6.3 匹配器

```typescript
import { expect, test } from "bun:test";

test("matchers", () => {
  // 相等性
  expect(1).toBe(1);
  expect({ a: 1 }).toEqual({ a: 1 });
  expect([1, 2]).toContain(1);

  // 比较
  expect(10).toBeGreaterThan(5);
  expect(5).toBeLessThanOrEqual(5);

  // 真值判断
  expect(true).toBeTruthy();
  expect(null).toBeNull();
  expect(undefined).toBeUndefined();

  // 字符串
  expect("hello").toMatch(/ell/);
  expect("hello").toContain("ell");

  // 数组
  expect([1, 2, 3]).toHaveLength(3);

  // 异常
  expect(() => {
    throw new Error("fail");
  }).toThrow("fail");

  // 异步
  await expect(Promise.resolve(1)).resolves.toBe(1);
  await expect(Promise.reject("err")).rejects.toBe("err");
});
```

### 6.4 模拟

```typescript
import { mock, spyOn } from "bun:test";

// 模拟函数
const mockFn = mock((x: number) => x * 2);
mockFn(5);
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledWith(5);
expect(mockFn.mock.results[0].value).toBe(10);

// 监视方法
const obj = {
  method: () => "original",
};
const spy = spyOn(obj, "method").mockReturnValue("mocked");
expect(obj.method()).toBe("mocked");
expect(spy).toHaveBeenCalled();
```

---

## 7. 打包

### 7.1 基本构建

```bash
# 生产环境打包
bun build ./src/index.ts --outdir ./dist

# 带选项
bun build ./src/index.ts \
  --outdir ./dist \
  --target browser \
  --minify \
  --sourcemap
```

### 7.2 构建 API

```typescript
const result = await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  target: "browser", // 或 "bun"、"node"
  minify: true,
  sourcemap: "external",
  splitting: true,
  format: "esm",

  // 外部包（不打包）
  external: ["react", "react-dom"],

  // 定义全局变量
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
  },

  // 命名规则
  naming: {
    entry: "[name].[hash].js",
    chunk: "chunks/[name].[hash].js",
    asset: "assets/[name].[hash][ext]",
  },
});

if (!result.success) {
  console.error(result.logs);
}
```

### 7.3 编译为可执行文件

```bash
# 创建独立可执行文件
bun build ./src/cli.ts --compile --outfile myapp

# 交叉编译
bun build ./src/cli.ts --compile --target=bun-linux-x64 --outfile myapp-linux
bun build ./src/cli.ts --compile --target=bun-darwin-arm64 --outfile myapp-mac

# 嵌入资源文件
bun build ./src/cli.ts --compile --outfile myapp --embed ./assets
```

---

## 8. 从 Node.js 迁移

### 8.1 兼容性

```typescript
// 大多数 Node.js API 开箱即用
import fs from "fs";
import path from "path";
import crypto from "crypto";

// process 是全局变量
console.log(process.cwd());
console.log(process.env.HOME);

// Buffer 是全局变量
const buf = Buffer.from("hello");

// __dirname 和 __filename 可用
console.log(__dirname);
console.log(__filename);
```

### 8.2 常见迁移步骤

```bash
# 1. 安装 Bun
curl -fsSL https://bun.sh/install | bash

# 2. 替换包管理器
rm -rf node_modules package-lock.json
bun install

# 3. 更新 package.json 中的脚本
# "start": "node index.js" → "start": "bun run index.ts"
# "test": "jest" → "test": "bun test"

# 4. 添加 Bun 类型
bun add -d @types/bun
```

### 8.3 与 Node.js 的差异

```typescript
// ❌ Node.js 特有（可能不工作）
require("module")             // 改用 import
require.resolve("pkg")        // 改用 import.meta.resolve
__non_webpack_require__       // 不支持

// ✅ Bun 等效写法
import pkg from "pkg";
const resolved = import.meta.resolve("pkg");
Bun.resolveSync("pkg", process.cwd());

// ❌ 以下全局变量有差异
process.hrtime()              // 改用 Bun.nanoseconds()
setImmediate()                // 改用 queueMicrotask()

// ✅ Bun 特有功能
const file = Bun.file("./data.txt");  // 快速文件 API
Bun.serve({ port: 3000, fetch: ... }); // 快速 HTTP 服务器
Bun.password.hash(password);           // 内置哈希
```

---

## 9. 性能技巧

### 9.1 使用 Bun 原生 API

```typescript
// 慢（Node.js 兼容模式）
import fs from "fs/promises";
const content = await fs.readFile("./data.txt", "utf-8");

// 快（Bun 原生）
const file = Bun.file("./data.txt");
const content = await file.text();
```

### 9.2 使用 Bun.serve 处理 HTTP

```typescript
// 不推荐：Express/Fastify（有额外开销）
import express from "express";
const app = express();

// 推荐：Bun.serve（原生，快 4-10 倍）
Bun.serve({
  fetch(req) {
    return new Response("Hello!");
  },
});

// 或使用 Elysia（Bun 优化框架）
import { Elysia } from "elysia";
new Elysia().get("/", () => "Hello!").listen(3000);
```

### 9.3 生产环境打包

```bash
# 生产环境务必打包并压缩
bun build ./src/index.ts --outdir ./dist --minify --target node

# 然后运行打包产物
bun run ./dist/index.js
```

---

## 快速参考

| 任务         | 命令                                       |
| :----------- | :----------------------------------------- |
| 初始化项目   | `bun init`                                 |
| 安装依赖     | `bun install`                              |
| 添加包       | `bun add <pkg>`                            |
| 运行脚本     | `bun run <script>`                         |
| 运行文件     | `bun run file.ts`                          |
| 监听模式     | `bun --watch run file.ts`                  |
| 运行测试     | `bun test`                                 |
| 构建         | `bun build ./src/index.ts --outdir ./dist` |
| 执行包       | `bunx <pkg>`                               |

---

## 资源

- [Bun 文档](https://bun.sh/docs)
- [Bun GitHub](https://github.com/oven-sh/bun)
- [Elysia 框架](https://elysiajs.com/)
- [Bun Discord](https://bun.sh/discord)

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
