---
name: kaizen
description: "持续改进、防错设计和标准化指南。当用户想要改进代码质量、重构或讨论流程改进时使用此技能。触发词：持续改进、Kaizen、防错设计、Poka-Yoke、标准化工作、代码质量改进、渐进式改进、重构方法论。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Kaizen: 持续改进

## 概述

持续进行小的改进。设计时防错。遵循有效的方法。只构建需要的内容。

**核心原则：** 许多小的改进胜过一次大的改变。在设计时预防错误，而不是事后修复。

## 何时使用
**始终应用于：**

- 代码实现和重构
- 架构和设计决策
- 流程和工作流改进
- 错误处理和验证

**理念：** 通过渐进式进步和预防实现质量，而非通过大规模努力追求完美。

## 四大支柱

### 1. 持续改进 (Kaizen)

小的、频繁的改进会累积成巨大的收益。

#### 原则

**渐进式优于革命式：**

- 做出能改善质量的最小可行变更
- 一次只改进一项
- 在进行下一次之前验证每次变更
- 通过小的胜利建立动力

**始终让代码变得更好：**

- 遇到小问题时就修复它们
- 工作时进行重构（在范围内）
- 更新过时的注释
- 看到死代码就删除

**迭代式精炼：**

- 第一版：让它能工作
- 第二遍：让它清晰
- 第三遍：让它高效
- 不要试图同时做到这三点

<Good>
```typescript
// 迭代 1：让它能工作
const calculateTotal = (items: Item[]) => {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
};

// 迭代 2：让它清晰（重构）
const calculateTotal = (items: Item[]): number => {
return items.reduce((total, item) => {
return total + (item.price * item.quantity);
}, 0);
};

// 迭代 3：让它健壮（添加验证）
const calculateTotal = (items: Item[]): number => {
if (!items?.length) return 0;

return items.reduce((total, item) => {
if (item.price < 0 || item.quantity < 0) {
throw new Error('Price and quantity must be non-negative');
}
return total + (item.price * item.quantity);
}, 0);
};

````
每一步都是完整、经过测试且可工作的
</Good>

<Bad>
```typescript
// 试图一次完成所有事情
const calculateTotal = (items: Item[]): number => {
  // 同时验证、优化、添加功能、处理边界情况
  if (!items?.length) return 0;
  const validItems = items.filter(item => {
    if (item.price < 0) throw new Error('Negative price');
    if (item.quantity < 0) throw new Error('Negative quantity');
    return item.quantity > 0; // 还在过滤零数量
  });
  // 加上缓存、日志、货币转换...
  return validItems.reduce(...); // 一次处理太多关注点
};
````

令人不知所措、容易出错、难以验证
</Bad>

#### 实践中

**实现功能时：**

1. 从能工作的最简单版本开始
2. 添加一项改进（错误处理、验证等）
3. 测试并验证
4. 如果时间允许则重复
5. 不要试图立即做到完美

**重构时：**

- 一次修复一个代码异味
- 每次改进后提交
- 始终保持测试通过
- 当"足够好"时停止（收益递减）

**代码审查时：**

- 建议渐进式改进（而非重写）
- 优先级排序：关键 → 重要 → 锦上添花
- 首先关注影响最大的变更
- 接受"比之前更好"即使不完美

### 2. 防错设计 (Poka-Yoke)

设计能在编译/设计时预防错误的系统，而非运行时。

#### 原则

**让错误不可能发生：**

- 类型系统捕获错误
- 编译器强制执行契约
- 无效状态无法表示
- 尽早捕获错误（生产之前）

**为安全而设计：**

- 快速且大声地失败
- 提供有帮助的错误消息
- 让正确路径显而易见
- 让错误路径难以执行

**分层防御：**

1. 类型系统（编译时）
2. 验证（运行时，早期）
3. 守卫（前置条件）
4. 错误边界（优雅降级）

#### 类型系统防错

<Good>
```typescript
// 错误：字符串状态可以是任何值
type OrderBad = {
  status: string; // 可以是 "pending"、"PENDING"、"pnding"，任何值！
  total: number;
};

// 好：只有有效状态可能
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered';
type Order = {
status: OrderStatus;
total: number;
};

// 更好：状态与关联数据
type Order =
| { status: 'pending'; createdAt: Date }
| { status: 'processing'; startedAt: Date; estimatedCompletion: Date }
| { status: 'shipped'; trackingNumber: string; shippedAt: Date }
| { status: 'delivered'; deliveredAt: Date; signature: string };

// 现在不可能有已发货但没有 trackingNumber 的情况

````
类型系统预防了整类错误
</Good>

<Good>
```typescript
// 让无效状态无法表示
type NonEmptyArray<T> = [T, ...T[]];

const firstItem = <T>(items: NonEmptyArray<T>): T => {
  return items[0]; // 总是安全，永远不会是 undefined！
};

// 调用者必须证明数组非空
const items: number[] = [1, 2, 3];
if (items.length > 0) {
  firstItem(items as NonEmptyArray<number>); // 安全
}
````

函数签名保证了安全性
</Good>

#### 验证防错

<Good>
```typescript
// 错误：使用后验证
const processPayment = (amount: number) => {
  const fee = amount * 0.03; // 验证前就使用了！
  if (amount <= 0) throw new Error('Invalid amount');
  // ...
};

// 好：立即验证
const processPayment = (amount: number) => {
if (amount <= 0) {
throw new Error('Payment amount must be positive');
}
if (amount > 10000) {
throw new Error('Payment exceeds maximum allowed');
}

const fee = amount * 0.03;
// ... 现在可以安全使用
};

// 更好：在边界处用品牌类型验证
type PositiveNumber = number & { readonly __brand: 'PositiveNumber' };

const validatePositive = (n: number): PositiveNumber => {
if (n <= 0) throw new Error('Must be positive');
return n as PositiveNumber;
};

const processPayment = (amount: PositiveNumber) => {
// amount 保证是正数，无需检查
const fee = amount * 0.03;
};

// 在系统边界验证
const handlePaymentRequest = (req: Request) => {
const amount = validatePositive(req.body.amount); // 验证一次
processPayment(amount); // 到处安全使用
};

````
在边界处验证一次，其他地方都安全
</Good>

#### 守卫和前置条件

<Good>
```typescript
// 早期返回防止深层嵌套代码
const processUser = (user: User | null) => {
  if (!user) {
    logger.error('User not found');
    return;
  }

  if (!user.email) {
    logger.error('User email missing');
    return;
  }

  if (!user.isActive) {
    logger.info('User inactive, skipping');
    return;
  }

  // 主逻辑在这里，保证用户有效且活跃
  sendEmail(user.email, 'Welcome!');
};
````

守卫让假设变得明确且强制执行
</Good>

#### 配置防错

<Good>
```typescript
// 错误：可选配置带不安全默认值
type ConfigBad = {
  apiKey?: string;
  timeout?: number;
};

const client = new APIClient({ timeout: 5000 }); // apiKey 缺失！

// 好：必需配置，早期失败
type Config = {
apiKey: string;
timeout: number;
};

const loadConfig = (): Config => {
const apiKey = process.env.API_KEY;
if (!apiKey) {
throw new Error('API_KEY environment variable required');
}

return {
apiKey,
timeout: 5000,
};
};

// 应用在启动时失败如果配置无效，而非请求期间
const config = loadConfig();
const client = new APIClient(config);

````
在启动时失败，而非生产环境
</Good>

#### 实践中

**设计 API 时：**
- 使用类型约束输入
- 让无效状态无法表示
- 返回 Result<T, E> 而非抛出异常
- 在类型中记录前置条件

**处理错误时：**
- 在系统边界验证

- 使用守卫检查前置条件
- 快速失败并提供清晰消息
- 记录调试上下文

**配置时：**
- 必需优于带默认值的可选
- 启动时验证所有配置
- 配置无效则部署失败
- 不允许部分配置

### 3. 标准化工作
遵循既定模式。记录有效的方法。让良好实践易于遵循。

#### 原则

**一致性优于聪明：**
- 遵循现有代码库模式
- 不要重复解决已解决的问题
- 只有显著更好时才引入新模式
- 团队同意新模式

**文档与代码共存：**
- README 用于设置和架构
- CLAUDE.md 用于 AI 编码约定
- 注释解释"为什么"，而非"是什么"
- 为复杂模式提供示例

**自动化标准：**
- Linter 强制执行风格
- 类型检查强制执行契约
- 测试验证行为
- CI/CD 强制执行质量门

#### 遵循模式

<Good>
```typescript
// 现有代码库中 API 客户端的模式
class UserAPIClient {
  async getUser(id: string): Promise<User> {
    return this.fetch(`/users/${id}`);
  }
}

// 新代码遵循相同模式
class OrderAPIClient {
  async getOrder(id: string): Promise<Order> {
    return this.fetch(`/orders/${id}`);
  }
}
````

一致性让代码库可预测
</Good>

<Bad>
```typescript
// 现有模式使用类
class UserAPIClient { /* ... */ }

// 新代码未经讨论引入不同模式
const getOrder = async (id: string): Promise<Order> => {
// "因为我更喜欢函数"而破坏一致性
};

````
不一致造成困惑
</Bad>

#### 错误处理模式

<Good>
```typescript
// 项目标准：可恢复错误使用 Result 类型
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

// 所有服务遵循此模式
const fetchUser = async (id: string): Promise<Result<User, Error>> => {
  try {
    const user = await db.users.findById(id);
    if (!user) {
      return { ok: false, error: new Error('User not found') };
    }
    return { ok: true, value: user };
  } catch (err) {
    return { ok: false, error: err as Error };
  }
};

// 调用者使用一致的模式
const result = await fetchUser('123');
if (!result.ok) {
  logger.error('Failed to fetch user', result.error);
  return;
}
const user = result.value; // 类型安全！
````

代码库中的标准模式
</Good>

#### 文档标准

<Good>
```typescript
/**
 * 使用指数退避重试异步操作。
 *
 * 为什么：网络请求会临时失败；重试提高可靠性
 * 何时使用：外部 API 调用、数据库操作
 * 何时不使用：用户输入验证、内部函数调用
 *
 * @example
 * const result = await retry(
 *   () => fetch('https://api.example.com/data'),
 *   { maxAttempts: 3, baseDelay: 1000 }
 * );
 */
const retry = async <T>(
  operation: () => Promise<T>,
  options: RetryOptions
): Promise<T> => {
  // 实现...
};
```
记录为什么、何时以及如何
</Good>

#### 实践中

**添加新模式前：**

- 搜索代码库中已解决的类似问题
- 检查 CLAUDE.md 中的项目约定
- 如果要打破模式则与团队讨论
- 引入新模式时更新文档

**编写代码时：**

- 匹配现有文件结构
- 使用相同的命名约定
- 遵循相同的错误处理方法
- 从相同位置导入

**审查时：**

- 检查与现有代码的一致性
- 指向代码库中的示例
- 建议与标准对齐
- 如果出现新标准则更新 CLAUDE.md

### 4. 准时化 (JIT)

只构建现在需要的。不多不少。避免过早优化和过度工程。

#### 原则

**YAGNI (You Aren't Gonna Need It)：**

- 只实现当前需求
- 不要"以防万一"的功能
- 不要"我们以后可能需要"的代码
- 删除投机性代码

**能工作的最简单方案：**

- 从直接的解决方案开始
- 只在需要时增加复杂性
- 需求变化时重构
- 不要预测未来需求

**测量后优化：**

- 不要过早优化
- 优化前先分析
- 测量变更的影响
- 接受"足够好"的性能

#### YAGNI 实战

<Good>
```typescript
// 当前需求：将错误记录到控制台
const logError = (error: Error) => {
  console.error(error.message);
};
```
简单，满足当前需求
</Good>

<Bad>
```typescript
// 为"未来需求"过度工程
interface LogTransport {
  write(level: LogLevel, message: string, meta?: LogMetadata): Promise<void>;
}

class ConsoleTransport implements LogTransport { /*...*/ }
class FileTransport implements LogTransport { /* ...*/ }
class RemoteTransport implements LogTransport { /* ...*/ }

class Logger {
private transports: LogTransport[] = [];
private queue: LogEntry[] = [];
private rateLimiter: RateLimiter;
private formatter: LogFormatter;

// 200 行代码用于"也许我们需要"
}

const logError = (error: Error) => {
Logger.getInstance().log('error', error.message);
};

````
为想象中的未来需求构建
</Bad>

**何时添加复杂性：**
- 当前需求要求
- 使用中发现痛点
- 测量到的性能问题
- 出现多个用例

<Good>
```typescript
// 从简单开始
const formatCurrency = (amount: number): string => {
  return `$${amount.toFixed(2)}`;
};

// 需求演进：支持多种货币
const formatCurrency = (amount: number, currency: string): string => {
  const symbols = { USD: '$', EUR: '€', GBP: '£' };
  return `${symbols[currency]}${amount.toFixed(2)}`;
};

// 需求演进：支持本地化
const formatCurrency = (amount: number, locale: string): string => {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: locale === 'en-US' ? 'USD' : 'EUR',
  }).format(amount);
};
````

只在需要时添加复杂性
</Good>

#### 过早抽象

<Bad>
```typescript
// 一个用例，却构建通用框架
abstract class BaseCRUDService<T> {
  abstract getAll(): Promise<T[]>;
  abstract getById(id: string): Promise<T>;
  abstract create(data: Partial<T>): Promise<T>;
  abstract update(id: string, data: Partial<T>): Promise<T>;
  abstract delete(id: string): Promise<void>;
}

class GenericRepository<T> { /*300 行*/ }
class QueryBuilder<T> { /* 200 行*/ }
// ... 为单表构建整个 ORM

````
为不确定的未来做大规模抽象
</Bad>

<Good>
```typescript
// 为当前需求的简单函数
const getUsers = async (): Promise<User[]> => {
  return db.query('SELECT * FROM users');
};

const getUserById = async (id: string): Promise<User | null> => {
  return db.query('SELECT * FROM users WHERE id = $1', [id]);
};

// 当模式在多个实体间出现时，再抽象
````

只在模式在 3+ 个案例中验证后才抽象
</Good>

#### 性能优化

<Good>
```typescript
// 当前：简单方法
const filterActiveUsers = (users: User[]): User[] => {
  return users.filter(user => user.isActive);
};

// 基准测试显示：1000 个用户 50ms（可接受）
// ✓ 发布它，不需要优化

// 之后：分析显示这是瓶颈
// 然后用索引查找或缓存优化

````
基于测量优化，而非假设
</Good>

<Bad>
```typescript
// 过早优化
const filterActiveUsers = (users: User[]): User[] => {
  // "这可能很慢，所以让我们缓存和索引"
  const cache = new WeakMap();
  const indexed = buildBTreeIndex(users, 'isActive');
  // 100 行优化代码
  // 增加复杂性，更难维护
  // 没有证据表明需要
};\
````

为未测量的问题提供复杂解决方案
</Bad>

#### 实践中

**实现时：**

- 解决眼前的问题
- 使用直接的方法
- 抵制"万一"思维
- 删除投机性代码

**优化时：**

- 先分析，后优化
- 测量前后
- 记录为什么需要优化
- 在测试中保留简单版本

**抽象时：**

- 等待 3+ 个相似案例（三法则）
- 让抽象尽可能简单
- 宁愿重复也不要错误的抽象
- 模式清晰时重构

## 与命令集成

Kaizen 技能指导你如何工作。命令提供结构化分析：

- **`/why`**：根因分析（5 个为什么）
- **`/cause-and-effect`**：多因素分析（鱼骨图）
- **`/plan-do-check-act`**：迭代改进循环
- **`/analyse-problem`**：全面文档（A3）
- **`/analyse`**：智能方法选择（现场/价值流/浪费）

使用命令进行结构化问题解决。应用技能进行日常开发。

## 危险信号

**违反持续改进：**

- "我以后再重构"（永远不会发生）
- 让代码比你发现时更糟
- 大爆炸式重写而非渐进式

**违反防错设计：**

- "用户应该小心点"
- 使用后验证而非使用前
- 可选配置无验证

**违反标准化工作：**

- "我更喜欢我的方式"
- 不检查现有模式
- 忽略项目约定

**违反准时化：**

- "我们有一天可能需要这个"
- 在使用前构建框架
- 没有测量就优化

## 记住

**Kaizen 关乎：**

- 持续进行小的改进
- 设计预防错误
- 遵循已验证的模式
- 只构建需要的

**不关乎：**

- 第一次就完美
- 大规模重构项目
- 聪明的抽象
- 过早优化

**心态：** 今天足够好，明天更好。重复。

## 限制
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并请求澄清。
