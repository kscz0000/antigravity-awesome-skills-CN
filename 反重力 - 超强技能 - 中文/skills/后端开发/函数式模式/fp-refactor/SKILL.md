---
name: fp-refactor
description: 将命令式 TypeScript 代码重构为 fp-ts 函数式模式的综合指南。触发词：fp-ts重构、函数式重构、Either转换、Option转换、TaskEither迁移、Reader模式、命令式转函数式、try-catch重构、null检查重构、回调转Task、DI重构、循环转函数式
risk: unknown
source: community
version: 1.0.0
author: fp-ts-skills
tags:
  - fp-ts
  - refactoring
  - functional-programming
  - typescript
  - migration
  - either
  - option
  - task
  - reader
---

# 将命令式代码重构为 fp-ts

本技能提供将现有命令式 TypeScript 代码迁移到 fp-ts 函数式编程模式的综合模式和策略。

## 何时使用
- 你正在将现有命令式 TypeScript 代码库重构为 fp-ts 模式。
- 任务涉及将 `try/catch`、null 检查、回调、依赖注入或循环转换为函数式等价物。
- 你需要迁移指导和权衡分析，而不仅仅是孤立的 fp-ts 示例。

## 目录

1. [将 try-catch 转换为 Either/TaskEither](#1-converting-try-catch-to-eithertaskeither)
2. [将 null 检查转换为 Option](#2-converting-null-checks-to-option)
3. [将回调转换为 Task](#3-converting-callbacks-to-task)
4. [将基于类的依赖注入转换为 Reader](#4-converting-class-based-di-to-reader)
5. [将命令式循环转换为函数式操作](#5-converting-imperative-loops-to-functional-operations)
6. [将 Promise 链迁移到 TaskEither](#6-migrating-promise-chains-to-taskeither)
7. [常见陷阱](#7-common-pitfalls)
8. [渐进式采用策略](#8-gradual-adoption-strategies)
9. [何时不应重构](#9-when-not-to-refactor)

---

## 1. 将 try-catch 转换为 Either/TaskEither

### try-catch 的问题

传统 try-catch 块有几个问题：
- 错误处理是隐式的，容易被遗忘
- 类型系统无法追踪哪些函数可能抛出异常
- 控制流是非线性的，难以推理
- 组合多个可能失败的操作很繁琐

### 模式：同步 try-catch 转 Either

#### 重构前（命令式）

```typescript
function parseJSON(input: string): unknown {
  try {
    return JSON.parse(input);
  } catch (error) {
    throw new Error(`Invalid JSON: ${error}`);
  }
}

function validateUser(data: unknown): User {
  try {
    if (!data || typeof data !== 'object') {
      throw new Error('Data must be an object');
    }
    const obj = data as Record<string, unknown>;
    if (typeof obj.name !== 'string') {
      throw new Error('Name is required');
    }
    if (typeof obj.age !== 'number') {
      throw new Error('Age must be a number');
    }
    return { name: obj.name, age: obj.age };
  } catch (error) {
    throw error;
  }
}

// 嵌套 try-catch 的使用方式
function processUserInput(input: string): User | null {
  try {
    const data = parseJSON(input);
    const user = validateUser(data);
    return user;
  } catch (error) {
    console.error('Failed to process user:', error);
    return null;
  }
}
```

#### 重构后（fp-ts Either）

```typescript
import * as E from 'fp-ts/Either';
import * as J from 'fp-ts/Json';
import { pipe } from 'fp-ts/function';

interface User {
  name: string;
  age: number;
}

// 使用 Json.parse，它返回 Either<Error, Json>
const parseJSON = (input: string): E.Either<Error, unknown> =>
  pipe(
    J.parse(input),
    E.mapLeft((e) => new Error(`Invalid JSON: ${e}`))
  );

// 验证返回 Either，使错误在类型中显式可见
const validateUser = (data: unknown): E.Either<Error, User> => {
  if (!data || typeof data !== 'object') {
    return E.left(new Error('Data must be an object'));
  }
  const obj = data as Record<string, unknown>;
  if (typeof obj.name !== 'string') {
    return E.left(new Error('Name is required'));
  }
  if (typeof obj.age !== 'number') {
    return E.left(new Error('Age must be a number'));
  }
  return E.right({ name: obj.name, age: obj.age });
};

// 使用 pipe 和 flatMap 组合 - 错误自动传播
const processUserInput = (input: string): E.Either<Error, User> =>
  pipe(
    parseJSON(input),
    E.flatMap(validateUser)
  );

// 显式处理两种情况
pipe(
  processUserInput('{"name": "Alice", "age": 30}'),
  E.match(
    (error) => console.error('Failed to process user:', error.message),
    (user) => console.log('User:', user)
  )
);
```

### 分步重构指南

1. **识别错误类型**：确定可能发生哪些错误并创建适当的错误类型
2. **更改返回类型**：从 `T` 改为 `Either<E, T>`，其中 `E` 是你的错误类型
3. **替换 throw 语句**：将 `throw new Error(...)` 转换为 `E.left(new Error(...))`
4. **替换 return 语句**：将 `return value` 转换为 `E.right(value)`
5. **移除 try-catch 块**：不再需要它们
6. **更新调用方**：使用 `pipe` 配合 `E.flatMap` 来链式操作

### 模式：异步 try-catch 转 TaskEither

#### 重构前（命令式）

```typescript
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    const data = await response.json();
    return validateUser(data);
  } catch (error) {
    throw new Error(`Failed to fetch user: ${error}`);
  }
}

async function fetchUserPosts(userId: string): Promise<Post[]> {
  try {
    const response = await fetch(`/api/users/${userId}/posts`);
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    throw new Error(`Failed to fetch posts: ${error}`);
  }
}

// 使用 try-catch 的复杂编排
async function getUserWithPosts(id: string): Promise<{ user: User; posts: Post[] } | null> {
  try {
    const user = await fetchUser(id);
    const posts = await fetchUserPosts(id);
    return { user, posts };
  } catch (error) {
    console.error(error);
    return null;
  }
}
```

#### 重构后（fp-ts TaskEither）

```typescript
import * as TE from 'fp-ts/TaskEither';
import * as E from 'fp-ts/Either';
import { pipe } from 'fp-ts/function';

// 将 fetch 包装在 TaskEither 中
const fetchUser = (id: string): TE.TaskEither<Error, User> =>
  pipe(
    TE.tryCatch(
      () => fetch(`/api/users/${id}`),
      (reason) => new Error(`Network error: ${reason}`)
    ),
    TE.flatMap((response) =>
      response.ok
        ? TE.right(response)
        : TE.left(new Error(`HTTP error: ${response.status}`))
    ),
    TE.flatMap((response) =>
      TE.tryCatch(
        () => response.json(),
        (reason) => new Error(`JSON parse error: ${reason}`)
      )
    ),
    TE.flatMap((data) => TE.fromEither(validateUser(data)))
  );

const fetchUserPosts = (userId: string): TE.TaskEither<Error, Post[]> =>
  pipe(
    TE.tryCatch(
      () => fetch(`/api/users/${userId}/posts`),
      (reason) => new Error(`Network error: ${reason}`)
    ),
    TE.flatMap((response) =>
      response.ok
        ? TE.right(response)
        : TE.left(new Error(`HTTP error: ${response.status}`))
    ),
    TE.flatMap((response) =>
      TE.tryCatch(
        () => response.json(),
        (reason) => new Error(`JSON parse error: ${reason}`)
      )
    )
  );

// 清晰的组合，错误自动传播
const getUserWithPosts = (
  id: string
): TE.TaskEither<Error, { user: User; posts: Post[] }> =>
  pipe(
    TE.Do,
    TE.bind('user', () => fetchUser(id)),
    TE.bind('posts', () => fetchUserPosts(id))
  );

// 执行并处理结果
const main = async () => {
  const result = await getUserWithPosts('123')();
  pipe(
    result,
    E.match(
      (error) => console.error('Failed:', error.message),
      ({ user, posts }) => console.log('Success:', user, posts)
    )
  );
};
```

### 辅助工具：tryCatch 工具函数

为可能抛出异常的函数创建可复用的包装器：

```typescript
import * as E from 'fp-ts/Either';
import * as TE from 'fp-ts/TaskEither';

// 用于同步函数
const tryCatchSync = <A>(f: () => A): E.Either<Error, A> =>
  E.tryCatch(f, (e) => (e instanceof Error ? e : new Error(String(e))));

// 用于异步函数
const tryCatchAsync = <A>(f: () => Promise<A>): TE.TaskEither<Error, A> =>
  TE.tryCatch(f, (e) => (e instanceof Error ? e : new Error(String(e))));
```

---

## 2. 将 null 检查转换为 Option

### null/undefined 的问题

- TypeScript 的严格 null 检查有帮助，但 null 仍然会在代码中传播
- 链式属性访问需要冗长的 null 守卫
- "缺失"和"存在但为 null"之间的区别不清晰
- 容易忘记 null 检查导致运行时错误

### 模式：简单 null 检查转 Option

#### 重构前（命令式）

```typescript
interface Config {
  database?: {
    host?: string;
    port?: number;
    credentials?: {
      username?: string;
      password?: string;
    };
  };
}

function getDatabaseUrl(config: Config): string | null {
  if (!config.database) {
    return null;
  }
  if (!config.database.host) {
    return null;
  }
  const port = config.database.port ?? 5432;

  let auth = '';
  if (config.database.credentials) {
    if (config.database.credentials.username && config.database.credentials.password) {
      auth = `${config.database.credentials.username}:${config.database.credentials.password}@`;
    }
  }

  return `postgres://${auth}${config.database.host}:${port}`;
}

// 使用时需要 null 检查
const url = getDatabaseUrl(config);
if (url !== null) {
  connectToDatabase(url);
} else {
  console.error('Database URL not configured');
}
```

#### 重构后（fp-ts Option）

```typescript
import * as O from 'fp-ts/Option';
import { pipe } from 'fp-ts/function';

const getDatabaseUrl = (config: Config): O.Option<string> =>
  pipe(
    O.fromNullable(config.database),
    O.flatMap((db) =>
      pipe(
        O.fromNullable(db.host),
        O.map((host) => {
          const port = db.port ?? 5432;
          const auth = pipe(
            O.fromNullable(db.credentials),
            O.flatMap((creds) =>
              pipe(
                O.Do,
                O.bind('username', () => O.fromNullable(creds.username)),
                O.bind('password', () => O.fromNullable(creds.password)),
                O.map(({ username, password }) => `${username}:${password}@`)
              )
            ),
            O.getOrElse(() => '')
          );
          return `postgres://${auth}${host}:${port}`;
        })
      )
    )
  );

// 使用时明确表示可选性质
pipe(
  getDatabaseUrl(config),
  O.match(
    () => console.error('Database URL not configured'),
    (url) => connectToDatabase(url)
  )
);
```

### 模式：数组 find 操作

#### 重构前（命令式）

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

function findUserById(users: User[], id: string): User | undefined {
  return users.find((u) => u.id === id);
}

function getUserEmail(users: User[], id: string): string | null {
  const user = findUserById(users, id);
  if (!user) {
    return null;
  }
  return user.email;
}

// 链式查找变得混乱
function getManagerEmail(users: User[], employee: { managerId?: string }): string | null {
  if (!employee.managerId) {
    return null;
  }
  const manager = findUserById(users, employee.managerId);
  if (!manager) {
    return null;
  }
  return manager.email;
}
```

#### 重构后（fp-ts Option）

```typescript
import * as O from 'fp-ts/Option';
import * as A from 'fp-ts/Array';
import { pipe } from 'fp-ts/function';

const findUserById = (users: User[], id: string): O.Option<User> =>
  A.findFirst<User>((u) => u.id === id)(users);

const getUserEmail = (users: User[], id: string): O.Option<string> =>
  pipe(
    findUserById(users, id),
    O.map((user) => user.email)
  );

const getManagerEmail = (
  users: User[],
  employee: { managerId?: string }
): O.Option<string> =>
  pipe(
    O.fromNullable(employee.managerId),
    O.flatMap((managerId) => findUserById(users, managerId)),
    O.map((manager) => manager.email)
  );
```

### 分步重构指南

1. **识别可空值**：找出所有 `T | null`、`T | undefined` 或可选属性
2. **用 fromNullable 包装**：在系统边界将可空值转换为 Option
3. **更改返回类型**：从 `T | null` 改为 `Option<T>`
4. **替换 null 检查**：使用 `O.map`、`O.flatMap`、`O.filter` 代替 if 语句
5. **在边界处理**：与非 fp 代码交互时使用 `O.getOrElse`、`O.match` 或 `O.toNullable`

### Option 和 Either 之间的转换

```typescript
import * as O from 'fp-ts/Option';
import * as E from 'fp-ts/Either';
import { pipe } from 'fp-ts/function';

// Option 转 Either：为 None 情况提供错误
const optionToEither = <E, A>(onNone: () => E) => (
  option: O.Option<A>
): E.Either<E, A> =>
  pipe(
    option,
    E.fromOption(onNone)
  );

// 示例
const findUser = (id: string): O.Option<User> => /* ... */;

const getUser = (id: string): E.Either<Error, User> =>
  pipe(
    findUser(id),
    E.fromOption(() => new Error(`User ${id} not found`))
  );
```

---

## 3. 将回调转换为 Task

### 回调的问题

- 回调地狱使代码难以阅读
- 错误处理不一致
- 难以组合和排序
- 没有处理异步操作的标准方式

### 模式：Node 风格回调转 Task

#### 重构前（命令式）

```typescript
import * as fs from 'fs';

function readFileCallback(
  path: string,
  callback: (error: Error | null, data: string | null) => void
): void {
  fs.readFile(path, 'utf-8', (err, data) => {
    if (err) {
      callback(err, null);
    } else {
      callback(null, data);
    }
  });
}

function processFile(
  inputPath: string,
  outputPath: string,
  callback: (error: Error | null) => void
): void {
  readFileCallback(inputPath, (err, data) => {
    if (err) {
      callback(err);
      return;
    }
    const processed = data!.toUpperCase();
    fs.writeFile(outputPath, processed, (writeErr) => {
      if (writeErr) {
        callback(writeErr);
      } else {
        callback(null);
      }
    });
  });
}

// 回调地狱
function processMultipleFiles(
  files: Array<{ input: string; output: string }>,
  callback: (error: Error | null) => void
): void {
  let completed = 0;
  let hasError = false;

  files.forEach(({ input, output }) => {
    if (hasError) return;
    processFile(input, output, (err) => {
      if (hasError) return;
      if (err) {
        hasError = true;
        callback(err);
        return;
      }
      completed++;
      if (completed === files.length) {
        callback(null);
      }
    });
  });
}
```

#### 重构后（fp-ts Task/TaskEither）

```typescript
import * as fs from 'fs/promises';
import * as TE from 'fp-ts/TaskEither';
import * as A from 'fp-ts/Array';
import { pipe } from 'fp-ts/function';

// 将 fs.promises 包装在 TaskEither 中
const readFile = (path: string): TE.TaskEither<Error, string> =>
  TE.tryCatch(
    () => fs.readFile(path, 'utf-8'),
    (e) => (e instanceof Error ? e : new Error(String(e)))
  );

const writeFile = (path: string, data: string): TE.TaskEither<Error, void> =>
  TE.tryCatch(
    () => fs.writeFile(path, data),
    (e) => (e instanceof Error ? e : new Error(String(e)))
  );

// 清晰的组合
const processFile = (
  inputPath: string,
  outputPath: string
): TE.TaskEither<Error, void> =>
  pipe(
    readFile(inputPath),
    TE.map((data) => data.toUpperCase()),
    TE.flatMap((processed) => writeFile(outputPath, processed))
  );

// 并行或顺序处理多个文件
const processMultipleFilesParallel = (
  files: Array<{ input: string; output: string }>
): TE.TaskEither<Error, void[]> =>
  pipe(
    files,
    A.traverse(TE.ApplicativePar)(({ input, output }) =>
      processFile(input, output)
    )
  );

const processMultipleFilesSequential = (
  files: Array<{ input: string; output: string }>
): TE.TaskEither<Error, void[]> =>
  pipe(
    files,
    A.traverse(TE.ApplicativeSeq)(({ input, output }) =>
      processFile(input, output)
    )
  );
```

### 模式：转换基于回调的 API

```typescript
import * as TE from 'fp-ts/TaskEither';

// 通用的回调转 TaskEither 转换器
const fromCallback = <A>(
  f: (callback: (error: Error | null, result: A | null) => void) => void
): TE.TaskEither<Error, A> =>
  () =>
    new Promise((resolve) => {
      f((error, result) => {
        if (error) {
          resolve({ _tag: 'Left', left: error });
        } else {
          resolve({ _tag: 'Right', right: result as A });
        }
      });
    });

// 使用示例
const readFileLegacy = (path: string): TE.TaskEither<Error, string> =>
  fromCallback((cb) => fs.readFile(path, 'utf-8', cb));
```

---

## 4. 将基于类的依赖注入转换为 Reader

### 基于类的依赖注入的问题

- 类与其依赖项之间紧密耦合
- 测试需要模拟整个类层次结构
- 依赖注入容器增加了运行时复杂性
- 难以追踪应用程序中的数据流

### 模式：服务类转 Reader

#### 重构前（使用类的命令式）

```typescript
// 传统的基于类的方法
interface Logger {
  log(message: string): void;
  error(message: string): void;
}

interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

interface EmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

class UserService {
  constructor(
    private readonly logger: Logger,
    private readonly userRepo: UserRepository,
    private readonly emailService: EmailService
  ) {}

  async updateEmail(userId: string, newEmail: string): Promise<void> {
    this.logger.log(`Updating email for user ${userId}`);

    const user = await this.userRepo.findById(userId);
    if (!user) {
      this.logger.error(`User ${userId} not found`);
      throw new Error(`User ${userId} not found`);
    }

    const oldEmail = user.email;
    user.email = newEmail;

    await this.userRepo.save(user);

    await this.emailService.send(
      oldEmail,
      'Email Changed',
      `Your email has been changed to ${newEmail}`
    );

    this.logger.log(`Email updated for user ${userId}`);
  }
}

// 手动 DI 设置
const logger = new ConsoleLogger();
const userRepo = new PostgresUserRepository(dbConnection);
const emailService = new SmtpEmailService(smtpConfig);
const userService = new UserService(logger, userRepo, emailService);
```

#### 重构后（fp-ts Reader）

```typescript
import * as R from 'fp-ts/Reader';
import * as RTE from 'fp-ts/ReaderTaskEither';
import * as TE from 'fp-ts/TaskEither';
import { pipe } from 'fp-ts/function';

// 将环境/依赖项定义为接口
interface AppEnv {
  logger: {
    log: (message: string) => void;
    error: (message: string) => void;
  };
  userRepo: {
    findById: (id: string) => TE.TaskEither<Error, User | null>;
    save: (user: User) => TE.TaskEither<Error, void>;
  };
  emailService: {
    send: (to: string, subject: string, body: string) => TE.TaskEither<Error, void>;
  };
}

// 访问环境的辅助函数
const ask = RTE.ask<AppEnv, Error>();

// 使用 ReaderTaskEither 的服务函数
const logInfo = (message: string): RTE.ReaderTaskEither<AppEnv, Error, void> =>
  pipe(
    ask,
    RTE.map((env) => env.logger.log(message))
  );

const logError = (message: string): RTE.ReaderTaskEither<AppEnv, Error, void> =>
  pipe(
    ask,
    RTE.map((env) => env.logger.error(message))
  );

const findUser = (id: string): RTE.ReaderTaskEither<AppEnv, Error, User | null> =>
  pipe(
    ask,
    RTE.flatMapTaskEither((env) => env.userRepo.findById(id))
  );

const saveUser = (user: User): RTE.ReaderTaskEither<AppEnv, Error, void> =>
  pipe(
    ask,
    RTE.flatMapTaskEither((env) => env.userRepo.save(user))
  );

const sendEmail = (
  to: string,
  subject: string,
  body: string
): RTE.ReaderTaskEither<AppEnv, Error, void> =>
  pipe(
    ask,
    RTE.flatMapTaskEither((env) => env.emailService.send(to, subject, body))
  );

// 使用 Reader 组合的 updateEmail 函数
const updateEmail = (
  userId: string,
  newEmail: string
): RTE.ReaderTaskEither<AppEnv, Error, void> =>
  pipe(
    logInfo(`Updating email for user ${userId}`),
    RTE.flatMap(() => findUser(userId)),
    RTE.flatMap((user) => {
      if (!user) {
        return pipe(
          logError(`User ${userId} not found`),
          RTE.flatMap(() => RTE.left(new Error(`User ${userId} not found`)))
        );
      }
      const oldEmail = user.email;
      const updatedUser = { ...user, email: newEmail };

      return pipe(
        saveUser(updatedUser),
        RTE.flatMap(() =>
          sendEmail(
            oldEmail,
            'Email Changed',
            `Your email has been changed to ${newEmail}`
          )
        ),
        RTE.flatMap(() => logInfo(`Email updated for user ${userId}`))
      );
    })
  );

// 构建环境
const createAppEnv = (): AppEnv => ({
  logger: {
    log: (msg) => console.log(`[INFO] ${msg}`),
    error: (msg) => console.error(`[ERROR] ${msg}`),
  },
  userRepo: {
    findById: (id) => TE.tryCatch(
      () => postgresClient.query('SELECT * FROM users WHERE id = $1', [id]),
      (e) => new Error(String(e))
    ),
    save: (user) => TE.tryCatch(
      () => postgresClient.query('UPDATE users SET email = $1 WHERE id = $2', [user.email, user.id]),
      (e) => new Error(String(e))
    ),
  },
  emailService: {
    send: (to, subject, body) => TE.tryCatch(
      () => smtpClient.send({ to, subject, body }),
      (e) => new Error(String(e))
    ),
  },
});

// 运行程序
const main = async () => {
  const env = createAppEnv();
  const result = await updateEmail('user-123', 'new@email.com')(env)();

  pipe(
    result,
    E.match(
      (error) => console.error('Failed:', error),
      () => console.log('Success!')
    )
  );
};
```

### 使用 Reader 进行测试

```typescript
// 使用模拟环境轻松测试
const createTestEnv = (): AppEnv => {
  const logs: string[] = [];
  const savedUsers: User[] = [];
  const sentEmails: Array<{ to: string; subject: string; body: string }> = [];

  return {
    logger: {
      log: (msg) => logs.push(`[INFO] ${msg}`),
      error: (msg) => logs.push(`[ERROR] ${msg}`),
    },
    userRepo: {
      findById: (id) =>
        TE.right(id === 'existing-user' ? { id, email: 'old@email.com', name: 'Test' } : null),
      save: (user) => {
        savedUsers.push(user);
        return TE.right(undefined);
      },
    },
    emailService: {
      send: (to, subject, body) => {
        sentEmails.push({ to, subject, body });
        return TE.right(undefined);
      },
    },
  };
};

// 测试
describe('updateEmail', () => {
  it('should update email and send notification', async () => {
    const env = createTestEnv();
    const result = await updateEmail('existing-user', 'new@email.com')(env)();

    expect(E.isRight(result)).toBe(true);
    // 对捕获的副作用进行断言
  });
});
```

---

## 5. 将命令式循环转换为函数式操作

### 模式：for 循环转 map/filter/reduce

#### 重构前（命令式）

```typescript
interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}

function processProducts(products: Product[]): {
  totalValue: number;
  categoryCounts: Record<string, number>;
  expensiveProducts: string[];
} {
  let totalValue = 0;
  const categoryCounts: Record<string, number> = {};
  const expensiveProducts: string[] = [];

  for (let i = 0; i < products.length; i++) {
    const product = products[i];

    // 跳过缺货商品
    if (!product.inStock) {
      continue;
    }

    // 累加总价值
    totalValue += product.price;

    // 统计分类
    if (categoryCounts[product.category] === undefined) {
      categoryCounts[product.category] = 0;
    }
    categoryCounts[product.category]++;

    // 收集昂贵商品
    if (product.price > 100) {
      expensiveProducts.push(product.name);
    }
  }

  return { totalValue, categoryCounts, expensiveProducts };
}
```

#### 重构后（fp-ts 函数式操作）

```typescript
import * as A from 'fp-ts/Array';
import * as R from 'fp-ts/Record';
import { pipe } from 'fp-ts/function';
import * as N from 'fp-ts/number';
import * as Monoid from 'fp-ts/Monoid';

const processProducts = (products: Product[]) => {
  const inStockProducts = pipe(
    products,
    A.filter((p) => p.inStock)
  );

  const totalValue = pipe(
    inStockProducts,
    A.map((p) => p.price),
    A.reduce(0, (acc, price) => acc + price)
  );

  const categoryCounts = pipe(
    inStockProducts,
    A.reduce({} as Record<string, number>, (acc, product) => ({
      ...acc,
      [product.category]: (acc[product.category] ?? 0) + 1,
    }))
  );

  const expensiveProducts = pipe(
    inStockProducts,
    A.filter((p) => p.price > 100),
    A.map((p) => p.name)
  );

  return { totalValue, categoryCounts, expensiveProducts };
};

// 或使用 foldMap 进行单次遍历以提高效率
import { Monoid as M } from 'fp-ts/Monoid';

interface ProductStats {
  totalValue: number;
  categoryCounts: Record<string, number>;
  expensiveProducts: string[];
}

const productStatsMonoid: M<ProductStats> = {
  empty: { totalValue: 0, categoryCounts: {}, expensiveProducts: [] },
  concat: (a, b) => ({
    totalValue: a.totalValue + b.totalValue,
    categoryCounts: pipe(
      a.categoryCounts,
      R.union({ concat: (x, y) => x + y })(b.categoryCounts)
    ),
    expensiveProducts: [...a.expensiveProducts, ...b.expensiveProducts],
  }),
};

const processProductsSinglePass = (products: Product[]): ProductStats =>
  pipe(
    products,
    A.filter((p) => p.inStock),
    A.foldMap(productStatsMonoid)((product) => ({
      totalValue: product.price,
      categoryCounts: { [product.category]: 1 },
      expensiveProducts: product.price > 100 ? [product.name] : [],
    }))
  );
```

### 模式：嵌套循环转 flatMap

#### 重构前（命令式）

```typescript
interface Order {
  id: string;
  items: OrderItem[];
}

interface OrderItem {
  productId: string;
  quantity: number;
}

function getAllProductIds(orders: Order[]): string[] {
  const productIds: string[] = [];

  for (const order of orders) {
    for (const item of order.items) {
      if (!productIds.includes(item.productId)) {
        productIds.push(item.productId);
      }
    }
  }

  return productIds;
}
```

#### 重构后（fp-ts）

```typescript
import * as A from 'fp-ts/Array';
import { pipe } from 'fp-ts/function';
import * as S from 'fp-ts/Set';
import * as Str from 'fp-ts/string';

const getAllProductIds = (orders: Order[]): string[] =>
  pipe(
    orders,
    A.flatMap((order) => order.items),
    A.map((item) => item.productId),
    A.uniq(Str.Eq)
  );

// 或使用 Set 以提高大数据集的性能
const getAllProductIdsSet = (orders: Order[]): Set<string> =>
  pipe(
    orders,
    A.flatMap((order) => order.items),
    A.map((item) => item.productId),
    (ids) => new Set(ids)
  );
```

### 模式：while 循环转递归/unfold

#### 重构前（命令式）

```typescript
function paginate<T>(
  fetchPage: (cursor: string | null) => Promise<{ items: T[]; nextCursor: string | null }>
): Promise<T[]> {
  const allItems: T[] = [];
  let cursor: string | null = null;

  while (true) {
    const { items, nextCursor } = await fetchPage(cursor);
    allItems.push(...items);

    if (nextCursor === null) {
      break;
    }
    cursor = nextCursor;
  }

  return allItems;
}
```

#### 重构后（fp-ts）

```typescript
import * as TE from 'fp-ts/TaskEither';
import * as A from 'fp-ts/Array';
import { pipe } from 'fp-ts/function';

interface Page<T> {
  items: T[];
  nextCursor: string | null;
}

const paginate = <T>(
  fetchPage: (cursor: string | null) => TE.TaskEither<Error, Page<T>>
): TE.TaskEither<Error, T[]> => {
  const go = (
    cursor: string | null,
    accumulated: T[]
  ): TE.TaskEither<Error, T[]> =>
    pipe(
      fetchPage(cursor),
      TE.flatMap(({ items, nextCursor }) => {
        const newAccumulated = [...accumulated, ...items];
        return nextCursor === null
          ? TE.right(newAccumulated)
          : go(nextCursor, newAccumulated);
      })
    );

  return go(null, []);
};

// 使用 unfold 生成序列
import * as RA from 'fp-ts/ReadonlyArray';

const range = (start: number, end: number): readonly number[] =>
  RA.unfold(start, (n) => (n <= end ? O.some([n, n + 1]) : O.none));
```

---

## 6. 将 Promise 链迁移到 TaskEither

### 模式：Promise.then 链转 pipe

#### 重构前（命令式）

```typescript
function fetchUserData(userId: string): Promise<UserProfile> {
  return fetch(`/api/users/${userId}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return response.json();
    })
    .then((data) => validateUserData(data))
    .then((validData) => enrichUserProfile(validData))
    .catch((error) => {
      console.error('Failed to fetch user data:', error);
      throw error;
    });
}

// 带条件判断的链式 Promise
function processOrder(orderId: string): Promise<OrderResult> {
  return getOrder(orderId)
    .then((order) => {
      if (order.status === 'cancelled') {
        throw new Error('Order is cancelled');
      }
      return order;
    })
    .then((order) => validateInventory(order))
    .then((validOrder) => processPayment(validOrder))
    .then((paidOrder) => shipOrder(paidOrder))
    .catch((error) => {
      logError(error);
      return { success: false, error: error.message };
    });
}
```

#### 重构后（fp-ts TaskEither）

```typescript
import * as TE from 'fp-ts/TaskEither';
import * as E from 'fp-ts/Either';
import { pipe } from 'fp-ts/function';

const fetchUserData = (userId: string): TE.TaskEither<Error, UserProfile> =>
  pipe(
    TE.tryCatch(
      () => fetch(`/api/users/${userId}`),
      (e) => new Error(`Network error: ${e}`)
    ),
    TE.flatMap((response) =>
      response.ok
        ? TE.tryCatch(
            () => response.json(),
            (e) => new Error(`Parse error: ${e}`)
          )
        : TE.left(new Error(`HTTP ${response.status}`))
    ),
    TE.flatMap((data) => TE.fromEither(validateUserData(data))),
    TE.flatMap((validData) => enrichUserProfile(validData))
  );

// 条件判断变得显式
const processOrder = (orderId: string): TE.TaskEither<Error, OrderResult> =>
  pipe(
    getOrder(orderId),
    TE.filterOrElse(
      (order) => order.status !== 'cancelled',
      () => new Error('Order is cancelled')
    ),
    TE.flatMap(validateInventory),
    TE.flatMap(processPayment),
    TE.flatMap(shipOrder),
    TE.map((shipped) => ({ success: true, order: shipped })),
    TE.orElse((error) =>
      pipe(
        TE.fromIO(() => logError(error)),
        TE.map(() => ({ success: false, error: error.message }))
      )
    )
  );
```

### 模式：Promise.all 转 traverse

#### 重构前（命令式）

```typescript
async function fetchAllUsers(ids: string[]): Promise<User[]> {
  const promises = ids.map((id) => fetchUser(id));
  return Promise.all(promises);
}

// 带单项错误处理的版本
async function fetchUsersWithFallback(ids: string[]): Promise<Array<User | null>> {
  const promises = ids.map(async (id) => {
    try {
      return await fetchUser(id);
    } catch {
      return null;
    }
  });
  return Promise.all(promises);
}
```

#### 重构后（fp-ts）

```typescript
import * as TE from 'fp-ts/TaskEither';
import * as A from 'fp-ts/Array';
import * as T from 'fp-ts/Task';
import { pipe } from 'fp-ts/function';

// 并行执行 - 遇到第一个错误即失败
const fetchAllUsers = (ids: string[]): TE.TaskEither<Error, User[]> =>
  pipe(
    ids,
    A.traverse(TE.ApplicativePar)(fetchUser)
  );

// 顺序执行
const fetchAllUsersSequential = (ids: string[]): TE.TaskEither<Error, User[]> =>
  pipe(
    ids,
    A.traverse(TE.ApplicativeSeq)(fetchUser)
  );

// 收集成功项，忽略失败（使用 Task 而非 TaskEither）
const fetchUsersWithFallback = (ids: string[]): T.Task<Array<User | null>> =>
  pipe(
    ids,
    A.traverse(T.ApplicativePar)((id) =>
      pipe(
        fetchUser(id),
        TE.match(
          () => null,
          (user) => user
        )
      )
    )
  );

// 或追踪哪些失败了
const fetchUsersPartitioned = (
  ids: string[]
): T.Task<{ successes: User[]; failures: Array<{ id: string; error: Error }> }> =>
  pipe(
    ids,
    A.traverse(T.ApplicativePar)((id) =>
      pipe(
        fetchUser(id),
        TE.bimap(
          (error) => ({ id, error }),
          (user) => user
        ),
        (te) => te
      )
    ),
    T.map(A.separate),
    T.map(({ left: failures, right: successes }) => ({ successes, failures }))
  );
```

### 模式：Promise.race 转 alternative

```typescript
import * as TE from 'fp-ts/TaskEither';
import * as T from 'fp-ts/Task';
import { pipe } from 'fp-ts/function';

// 竞速 - 第一个完成的获胜
const raceTaskEithers = <E, A>(
  tasks: Array<TE.TaskEither<E, A>>
): TE.TaskEither<E, A> =>
  () => Promise.race(tasks.map((te) => te()));

// 失败时尝试备选方案（类似 Promise.any 但有类型）
const tryAlternatives = <E, A>(
  primary: TE.TaskEither<E, A>,
  fallback: TE.TaskEither<E, A>
): TE.TaskEither<E, A> =>
  pipe(
    primary,
    TE.orElse(() => fallback)
  );

// 备选链
const withFallbacks = <E, A>(
  tasks: Array<TE.TaskEither<E, A>>
): TE.TaskEither<E, A> =>
  tasks.reduce((acc, task) => pipe(acc, TE.orElse(() => task)));
```

---

## 7. 常见陷阱

### 陷阱 1：忘记执行 Task

```typescript
// 错误：Task 未执行
const fetchData = (): TE.TaskEither<Error, Data> => /* ... */;
const result = fetchData(); // 这仍然是 Task，不是结果！

// 正确：执行 Task
const result = await fetchData()(); // 注意双重调用
```

### 陷阱 2：错误地混用 async/await 和 fp-ts

```typescript
// 错误：脱离 fp-ts 生态系统
const processData = async (input: string): Promise<Result> => {
  const parsed = parseInput(input); // 返回 Either
  if (E.isLeft(parsed)) {
    throw new Error(parsed.left.message); // 不要这样做！
  }
  return await fetchData(parsed.right)();
};

// 正确：保持在生态系统中
const processData = (input: string): TE.TaskEither<Error, Result> =>
  pipe(
    parseInput(input),
    TE.fromEither,
    TE.flatMap(fetchData)
  );
```

### 陷阱 3：需要 flatMap 时使用了 map

```typescript
// 错误：导致嵌套 Either
const result: E.Either<Error, E.Either<Error, User>> = pipe(
  parseUserId(input), // E.Either<Error, string>
  E.map(fetchUser) // 返回 E.Either<Error, User>，所以得到嵌套 Either
);

// 正确：使用 flatMap 展平
const result: E.Either<Error, User> = pipe(
  parseUserId(input),
  E.flatMap(fetchUser)
);
```

### 陷阱 4：丢失错误信息

```typescript
// 错误：原始错误上下文丢失
const fetchData = (): TE.TaskEither<Error, Data> =>
  pipe(
    TE.tryCatch(
      () => fetch('/api/data'),
      () => new Error('Failed') // 丢失了原始错误！
    )
  );

// 正确：保留错误上下文
const fetchData = (): TE.TaskEither<Error, Data> =>
  pipe(
    TE.tryCatch(
      () => fetch('/api/data'),
      (reason) => new Error(`Network request failed: ${reason}`)
    )
  );

// 更好：使用类型化错误
type FetchError =
  | { _tag: 'NetworkError'; cause: unknown }
  | { _tag: 'ParseError'; cause: unknown }
  | { _tag: 'ValidationError'; message: string };

const fetchData = (): TE.TaskEither<FetchError, Data> =>
  pipe(
    TE.tryCatch(
      () => fetch('/api/data'),
      (cause): FetchError => ({ _tag: 'NetworkError', cause })
    ),
    TE.flatMap((response) =>
      TE.tryCatch(
        () => response.json(),
        (cause): FetchError => ({ _tag: 'ParseError', cause })
      )
    )
  );
```

### 陷阱 5：过度使用 fromNullable

```typescript
// 错误：不必要的包装和解包
const getName = (user: User | null): string => {
  const optUser = O.fromNullable(user);
  const name = pipe(optUser, O.map(u => u.name), O.toNullable);
  return name ?? 'Unknown';
};

// 正确：只在需要组合优势时使用 Option
const getName = (user: User | null): string => user?.name ?? 'Unknown';

// 更好：链式操作多个步骤时使用 Option
const getManagerName = (user: User | null): O.Option<string> =>
  pipe(
    O.fromNullable(user),
    O.flatMap(u => O.fromNullable(u.manager)),
    O.map(m => m.name)
  );
```

### 陷阱 6：不处理 left 情况

```typescript
// 错误：忽略潜在错误
const processUser = (input: string): User => {
  const result = parseUser(input); // E.Either<Error, User>
  return (result as E.Right<User>).right; // 不安全的类型断言！
};

// 正确：始终处理两种情况
const processUser = (input: string): User =>
  pipe(
    parseUser(input),
    E.getOrElse((error) => {
      console.error('Parse failed:', error);
      return defaultUser;
    })
  );
```

---

## 8. 渐进式采用策略

### 策略 1：从边界开始

从系统边缘的函数开始转换：
- API 响应处理器
- 数据库查询结果
- 文件系统操作
- 用户输入验证

```typescript
// 首先包装外部 API 调用
const fetchUserApi = (id: string): TE.TaskEither<ApiError, UserDto> =>
  pipe(
    TE.tryCatch(
      () => externalApiClient.getUser(id),
      (e) => ({ type: 'api_error' as const, cause: e })
    )
  );

// 内部代码最初可以保持命令式
async function handleUserRequest(userId: string) {
  const result = await fetchUserApi(userId)();
  if (E.isRight(result)) {
    // 使用现有代码处理用户
    return processUser(result.right);
  } else {
    throw new Error(`API error: ${result.left.type}`);
  }
}
```

### 策略 2：创建桥接函数

构建在 fp-ts 和命令式代码之间转换的辅助函数：

```typescript
// 从 Either 到抛出错误的桥接
const unsafeUnwrap = <E, A>(either: E.Either<E, A>): A =>
  pipe(
    either,
    E.getOrElseW((e) => {
      throw e instanceof Error ? e : new Error(String(e));
    })
  );

// 从抛出错误到 Either 的桥接
const catchSync = <A>(f: () => A): E.Either<Error, A> =>
  E.tryCatch(f, (e) => (e instanceof Error ? e : new Error(String(e))));

// 从 Promise 到 TaskEither 的桥接
const fromPromise = <A>(p: Promise<A>): TE.TaskEither<Error, A> =>
  TE.tryCatch(() => p, (e) => (e instanceof Error ? e : new Error(String(e))));

// 从 TaskEither 到 Promise 的桥接（Left 时抛出）
const toPromise = <E, A>(te: TE.TaskEither<E, A>): Promise<A> =>
  te().then(E.getOrElseW((e) => { throw e; }));
```

### 策略 3：逐模块迁移

1. **选择一个边界清晰的模块**
2. **为内部函数添加 fp-ts 类型**
3. **最初保持外部 API 不变**
4. **充分测试后再继续**
5. **内部稳定后更新外部 API**

```typescript
// 阶段 1：内部函数使用 fp-ts
// 文件：user-service.internal.ts
export const validateUser = (data: unknown): E.Either<ValidationError, User> => /* ... */;
export const enrichUser = (user: User): TE.TaskEither<Error, EnrichedUser> => /* ... */;

// 文件：user-service.ts（公共 API 不变）
export async function getUser(id: string): Promise<User> {
  const result = await pipe(
    fetchUser(id),
    TE.flatMap(validateUser >>> TE.fromEither),
    TE.flatMap(enrichUser)
  )();

  if (E.isLeft(result)) {
    throw result.left;
  }
  return result.right;
}

// 阶段 2：更新公共 API
// 文件：user-service.ts
export const getUser = (id: string): TE.TaskEither<UserError, User> =>
  pipe(
    fetchUser(id),
    TE.flatMap(validateUser >>> TE.fromEither),
    TE.flatMap(enrichUser)
  );
```

### 策略 4：类型驱动开发

使用 TypeScript 的类型系统指导迁移：

```typescript
// 步骤 1：先更改类型签名
type OldGetUser = (id: string) => Promise<User | null>;
type NewGetUser = (id: string) => TE.TaskEither<UserError, User>;

// 步骤 2：编译器会显示所有需要更新的调用点
const getUser: NewGetUser = (id) => /* 实现 */;

// 步骤 3：逐一更新调用点
// 编译器确保你处理所有情况
```

### 策略 5：测试即文档

编写演示预期行为的测试：

```typescript
describe('UserService', () => {
  describe('getUser (fp-ts)', () => {
    it('returns Right with user on success', async () => {
      const result = await getUser('valid-id')();
      expect(E.isRight(result)).toBe(true);
      if (E.isRight(result)) {
        expect(result.right.id).toBe('valid-id');
      }
    });

    it('returns Left with NotFound error for unknown id', async () => {
      const result = await getUser('unknown')();
      expect(E.isLeft(result)).toBe(true);
      if (E.isLeft(result)) {
        expect(result.left._tag).toBe('NotFound');
      }
    });
  });
});
```

---

## 9. 何时不应重构

### 简单的同步代码

不要重构那些无法从 fp-ts 受益的简单代码：

```typescript
// 这样就很好
function formatName(first: string, last: string): string {
  return `${first} ${last}`;
}

// 不要这样做 - 增加了复杂性却没有好处
const formatName = (first: string, last: string): string =>
  pipe(
    first,
    (f) => `${f} ${last}`
  );
```

### 性能关键的循环

fp-ts 操作会创建中间数组。对于热路径，保持命令式代码：

```typescript
// 对于处理数百万项的性能关键代码，保持这样
function sumLargeArray(numbers: number[]): number {
  let sum = 0;
  for (let i = 0; i < numbers.length; i++) {
    sum += numbers[i];
  }
  return sum;
}

// 这会创建中间数组
const sumWithFpts = (numbers: number[]): number =>
  pipe(numbers, A.reduce(0, (acc, n) => acc + n));
```

### 第三方库接口

当使用期望特定模式的库时：

```typescript
// Express 中间件必须匹配 Express 的接口
app.get('/users/:id', async (req, res) => {
  // 这里保持命令式，在边界处转换
  const result = await getUser(req.params.id)();

  if (E.isLeft(result)) {
    res.status(404).json({ error: result.left.message });
  } else {
    res.json(result.right);
  }
});
```

### 非函数式团队成员维护的代码

如果你的团队不熟悉 fp-ts，强制采用会损害生产力：

```typescript
// 如果团队不懂 fp-ts，这更难维护
const processOrder = (order: Order): TE.TaskEither<Error, Result> =>
  pipe(
    validateOrder(order),
    TE.fromEither,
    TE.flatMap(enrichOrder),
    TE.flatMap(submitOrder)
  );

// 所有 TypeScript 开发者都熟悉这个
async function processOrder(order: Order): Promise<Result> {
  const validated = validateOrder(order);
  if (!validated.success) {
    throw new Error(validated.error);
  }
  const enriched = await enrichOrder(validated.data);
  return await submitOrder(enriched);
}
```

### 简单的一次性 null 检查

不要为简单的一次性 null 检查使用 Option：

```typescript
// 这样就很好
const name = user?.name ?? 'Anonymous';

// 对于简单情况来说过度了
const name = pipe(
  O.fromNullable(user),
  O.map((u) => u.name),
  O.getOrElse(() => 'Anonymous')
);
```

### 当错误类型不重要时

如果你反正要抛出/记录日志，不需要错误组合：

```typescript
// 如果这就是你的错误处理方式...
try {
  await doSomething();
} catch (e) {
  logger.error(e);
  throw e;
}

// ...那么 Either 没有增加多少价值
const result = await doSomethingTE()();
if (E.isLeft(result)) {
  logger.error(result.left);
  throw result.left;
}
```

### 测试代码

测试代码应该易读，不必是函数式的：

```typescript
// 清晰的测试代码
describe('UserService', () => {
  it('creates a user', async () => {
    const user = await createUser({ name: 'Alice' });
    expect(user.name).toBe('Alice');
  });
});

// 不必要的复杂
describe('UserService', () => {
  it('creates a user', async () => {
    await pipe(
      createUser({ name: 'Alice' }),
      TE.map((user) => expect(user.name).toBe('Alice')),
      TE.getOrElse(() => T.of(fail('Should not fail')))
    )();
  });
});
```

---

## 快速参考：命令式到 fp-ts 映射表

| 命令式模式 | fp-ts 等价物 |
|-------------------|------------------|
| `try { } catch { }` | `E.tryCatch()`, `TE.tryCatch()` |
| `throw new Error()` | `E.left()`, `TE.left()` |
| `return value` | `E.right()`, `TE.right()` |
| `if (x === null)` | `O.fromNullable()`, `O.isNone()` |
| `x ?? defaultValue` | `O.getOrElse()` |
| `x?.property` | `O.map()`, `O.flatMap()` |
| `array.map()` | `A.map()` |
| `array.filter()` | `A.filter()` |
| `array.reduce()` | `A.reduce()`, `A.foldMap()` |
| `array.find()` | `A.findFirst()` |
| `array.flatMap()` | `A.flatMap()` |
| `Promise.then()` | `TE.map()`, `TE.flatMap()` |
| `Promise.catch()` | `TE.orElse()`, `TE.mapLeft()` |
| `Promise.all()` | `A.traverse(TE.ApplicativePar)` |
| `async/await` | `TE.flatMap()` 链 |
| `new Class(deps)` | `R.asks()`, `RTE.ask()` |
| `for...of` | `A.map()`, `A.reduce()` |
| `while` | 递归, `unfold()` |

---

## 总结

迁移到 fp-ts 是一段旅程，而非终点。关键原则：

1. **从小处着手**：转换单个函数，而非整个代码库
2. **务实**：并非所有东西都需要是函数式的
3. **类型驱动**：让编译器指导你的重构
4. **充分测试**：每次转换都应验证
5. **记录模式**：为你的代码库创建团队特定的指南
6. **审视收益**：确保增加的复杂性提供了价值

目标是更可维护、类型安全的代码——而不是为了函数式编程而函数式编程。

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
