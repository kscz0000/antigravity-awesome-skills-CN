---
name: fp-data-transforms
description: 使用函数式模式进行日常数据转换——数组、对象、分组、聚合和空值安全访问。当用户要求'数据转换'、'数组操作'、'对象转换'、'分组聚合'或'空值安全访问'时使用。
risk: unknown
source: community
version: 1.0.0
author: Claude
tags:
  - functional-programming
  - typescript
  - data-transformation
  - fp-ts
  - arrays
  - objects
  - grouping
  - aggregation
  - null-safety
---

# 实用数据转换

本技能涵盖日常数据转换：数组操作、对象重塑、API 响应规范化、数据分组和嵌套值安全访问。每节先展示命令式写法，再展示函数式等价写法，并诚实评估各自的适用场景。

## 使用场景

- 需要在 TypeScript 中转换数组、对象、分组数据或嵌套值
- 任务涉及重塑 API 响应、空值安全访问、聚合或规范化
- 需要实用的函数式模式处理日常数据工作，而非底层循环

---

## 目录

1. [数组操作](#1-array-operations)
2. [对象转换](#2-object-transformations)
3. [数据规范化](#3-data-normalization)
4. [分组与聚合](#4-grouping-and-aggregation)
5. [空值安全访问](#5-null-safe-access)
6. [实战示例](#6-real-world-examples)
7. [如何选择](#7-when-to-use-what)

---

## 1. 数组操作

数组操作是数据转换的基础。让我们用表达性强、可链式调用的操作替代冗长的循环。

### Map：转换每个元素

**任务**：将价格数组从分转换为美元。

#### 命令式写法

```typescript
const pricesInCents = [999, 1499, 2999, 4999];

function convertToDollars(prices: number[]): number[] {
  const result: number[] = [];
  for (let i = 0; i < prices.length; i++) {
    result.push(prices[i] / 100);
  }
  return result;
}

const dollars = convertToDollars(pricesInCents);
// [9.99, 14.99, 29.99, 49.99]
```

#### 函数式写法

```typescript
const pricesInCents = [999, 1499, 2999, 4999];

const toDollars = (cents: number): number => cents / 100;

const dollars = pricesInCents.map(toDollars);
// [9.99, 14.99, 29.99, 49.99]
```

**函数式更好的原因**：意图一目了然。`map` 表示"转换每个元素"。转换逻辑（`toDollars`）被命名且可复用。无需管理索引，无需手动构建数组。

### Filter：保留匹配项

**任务**：从列表中获取所有活跃用户。

#### 命令式写法

```typescript
interface User {
  id: string;
  name: string;
  isActive: boolean;
}

function getActiveUsers(users: User[]): User[] {
  const result: User[] = [];
  for (const user of users) {
    if (user.isActive) {
      result.push(user);
    }
  }
  return result;
}
```

#### 函数式写法

```typescript
const isActive = (user: User): boolean => user.isActive;

const activeUsers = users.filter(isActive);

// 简单谓词也可以内联
const activeUsers = users.filter(user => user.isActive);
```

**函数式更好的原因**：谓词（`isActive`）与迭代逻辑分离。你可以独立地复用、测试和组合谓词。

### Reduce：累积为新值

**任务**：计算购物车中商品的总价。

#### 命令式写法

```typescript
interface CartItem {
  name: string;
  price: number;
  quantity: number;
}

function calculateTotal(items: CartItem[]): number {
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }
  return total;
}
```

#### 函数式写法

```typescript
const calculateTotal = (items: CartItem[]): number =>
  items.reduce(
    (total, item) => total + item.price * item.quantity,
    0
  );

// 或提取行小计计算
const lineTotal = (item: CartItem): number => item.price * item.quantity;

const calculateTotal = (items: CartItem[]): number =>
  items.map(lineTotal).reduce((a, b) => a + b, 0);
```

**诚实评估**：对于简单求和，命令式循环其实很易读。函数式版本在需要将累积与其他转换组合，或归约逻辑足够复杂、值得命名时才更有优势。

### 链式调用：组合操作

**任务**：获取所有活跃高级用户的姓名，按字母排序。

#### 命令式写法

```typescript
interface User {
  id: string;
  name: string;
  isActive: boolean;
  tier: 'free' | 'premium';
}

function getActivePremiumNames(users: User[]): string[] {
  const result: string[] = [];
  for (const user of users) {
    if (user.isActive && user.tier === 'premium') {
      result.push(user.name);
    }
  }
  result.sort((a, b) => a.localeCompare(b));
  return result;
}
```

#### 函数式写法

```typescript
const getActivePremiumNames = (users: User[]): string[] =>
  users
    .filter(user => user.isActive)
    .filter(user => user.tier === 'premium')
    .map(user => user.name)
    .sort((a, b) => a.localeCompare(b));

// 或使用命名谓词以便复用
const isActive = (user: User): boolean => user.isActive;
const isPremium = (user: User): boolean => user.tier === 'premium';
const getName = (user: User): string => user.name;
const alphabetically = (a: string, b: string): number => a.localeCompare(b);

const getActivePremiumNames = (users: User[]): string[] =>
  users
    .filter(isActive)
    .filter(isPremium)
    .map(getName)
    .sort(alphabetically);
```

**函数式更好的原因**：链中每一步职责单一。你可以将转换读作一系列步骤："筛选活跃、筛选高级、获取姓名、排序"。添加或删除步骤很简单。

### 使用 fp-ts Array 模块

fp-ts 提供额外的数组工具函数，支持更好的组合：

```typescript
import * as A from 'fp-ts/Array';
import * as O from 'fp-ts/Option';
import { pipe } from 'fp-ts/function';

// 安全获取首元素
const first = pipe(
  [1, 2, 3],
  A.head
); // Some(1)

const firstOfEmpty = pipe(
  [] as number[],
  A.head
); // None

// 按索引安全查找
const third = pipe(
  ['a', 'b', 'c', 'd'],
  A.lookup(2)
); // Some('c')

// 按条件查找
const found = pipe(
  users,
  A.findFirst(user => user.id === 'abc123')
); // Option<User>

// 分区为两组
const [inactive, active] = pipe(
  users,
  A.partition(user => user.isActive)
);

// 取前 N 个元素
const topThree = pipe(
  sortedScores,
  A.takeLeft(3)
);

// 去重
const uniqueTags = pipe(
  allTags,
  A.uniq({ equals: (a, b) => a === b })
);
```

---

## 2. 对象转换

对象经常需要重塑：选取字段、移除敏感数据、合并设置、更新嵌套值。

### Pick：选取特定字段

**任务**：从用户对象中仅提取公开字段。

#### 命令式写法

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  passwordHash: string;
  internalNotes: string;
}

function getPublicUser(user: User): { id: string; name: string; email: string } {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
  };
}
```

#### 函数式写法

```typescript
// 通用 pick 工具函数
const pick = <T extends object, K extends keyof T>(
  keys: K[]
) => (obj: T): Pick<T, K> =>
  keys.reduce(
    (result, key) => {
      result[key] = obj[key];
      return result;
    },
    {} as Pick<T, K>
  );

const getPublicUser = pick<User, 'id' | 'name' | 'email'>(['id', 'name', 'email']);

const publicUser = getPublicUser(user);
```

**函数式更好的原因**：`pick` 工具函数可在整个代码库复用。类型安全确保只能选取存在的键。

### Omit：移除特定字段

**任务**：日志前移除敏感字段。

#### 命令式写法

```typescript
function sanitizeForLogging(user: User): Omit<User, 'passwordHash' | 'internalNotes'> {
  const { passwordHash, internalNotes, ...safe } = user;
  return safe;
}
```

#### 函数式写法

```typescript
// 通用 omit 工具函数
const omit = <T extends object, K extends keyof T>(
  keys: K[]
) => (obj: T): Omit<T, K> => {
  const result = { ...obj };
  for (const key of keys) {
    delete result[key];
  }
  return result as Omit<T, K>;
};

const sanitizeForLogging = omit<User, 'passwordHash' | 'internalNotes'>([
  'passwordHash',
  'internalNotes',
]);
```

**诚实评估**：对于一次性移除，解构（命令式写法）完全没问题且很易读。函数式 `omit` 工具函数在有大量此类转换或需要组合时才值得。

### Merge：合并对象

**任务**：将用户设置与默认值合并。

#### 命令式写法

```typescript
interface Settings {
  theme: 'light' | 'dark';
  fontSize: number;
  notifications: boolean;
  language: string;
}

function mergeSettings(
  defaults: Settings,
  userSettings: Partial<Settings>
): Settings {
  return {
    theme: userSettings.theme !== undefined ? userSettings.theme : defaults.theme,
    fontSize: userSettings.fontSize !== undefined ? userSettings.fontSize : defaults.fontSize,
    notifications: userSettings.notifications !== undefined
      ? userSettings.notifications
      : defaults.notifications,
    language: userSettings.language !== undefined ? userSettings.language : defaults.language,
  };
}
```

#### 函数式写法

```typescript
const mergeSettings = (
  defaults: Settings,
  userSettings: Partial<Settings>
): Settings => ({
  ...defaults,
  ...userSettings,
});

// 使用示例
const defaults: Settings = {
  theme: 'light',
  fontSize: 14,
  notifications: true,
  language: 'en',
};

const userPrefs: Partial<Settings> = {
  theme: 'dark',
  fontSize: 16,
};

const finalSettings = mergeSettings(defaults, userPrefs);
// { theme: 'dark', fontSize: 16, notifications: true, language: 'en' }
```

**函数式更好的原因**：展开语法简洁，可处理任意数量的键。后面的展开覆盖前面的，自然实现"默认值加覆盖"的行为。

### 深度合并：嵌套对象组合

**任务**：合并嵌套的配置对象。

#### 命令式写法

```typescript
interface Config {
  api: {
    baseUrl: string;
    timeout: number;
    retries: number;
  };
  ui: {
    theme: string;
    animations: boolean;
  };
}

function deepMerge(
  target: Config,
  source: Partial<Config>
): Config {
  const result = { ...target };

  if (source.api) {
    result.api = { ...target.api, ...source.api };
  }
  if (source.ui) {
    result.ui = { ...target.ui, ...source.ui };
  }

  return result;
}
```

#### 函数式写法

```typescript
// 单层嵌套的通用深度合并
const deepMerge = <T extends Record<string, object>>(
  target: T,
  source: { [K in keyof T]?: Partial<T[K]> }
): T => {
  const result = { ...target };

  for (const key of Object.keys(source) as Array<keyof T>) {
    if (source[key] !== undefined) {
      result[key] = { ...target[key], ...source[key] };
    }
  }

  return result;
};

// 使用示例
const defaultConfig: Config = {
  api: { baseUrl: 'https://api.example.com', timeout: 5000, retries: 3 },
  ui: { theme: 'light', animations: true },
};

const customConfig = deepMerge(defaultConfig, {
  api: { timeout: 10000 },
  ui: { theme: 'dark' },
});
// api.baseUrl 保留，api.timeout 被覆盖
// ui.theme 被覆盖，ui.animations 保留
```

### 不可变更新：修改嵌套值

**任务**：不使用变异更新深层嵌套值。

#### 命令式（变异）写法

```typescript
interface State {
  user: {
    profile: {
      settings: {
        theme: string;
      };
    };
  };
}

function updateTheme(state: State, newTheme: string): void {
  state.user.profile.settings.theme = newTheme; // 变异！
}
```

#### 函数式（不可变）写法

```typescript
// 手动嵌套展开
const updateTheme = (state: State, newTheme: string): State => ({
  ...state,
  user: {
    ...state.user,
    profile: {
      ...state.user.profile,
      settings: {
        ...state.user.profile.settings,
        theme: newTheme,
      },
    },
  },
});

// 使用类 lens 辅助函数
const updatePath = <T, V>(
  obj: T,
  path: string[],
  value: V
): T => {
  if (path.length === 0) return value as unknown as T;

  const [head, ...rest] = path;
  return {
    ...obj,
    [head]: updatePath((obj as Record<string, unknown>)[head], rest, value),
  } as T;
};

const newState = updatePath(state, ['user', 'profile', 'settings', 'theme'], 'dark');
```

**诚实评估**：嵌套展开冗长但明确。对于深层嵌套更新，考虑使用 `immer` 或 fp-ts lenses 等库。函数式写法的冗长是不可变性的代价。

---

## 3. 数据规范化

API 响应很少与应用所需的结构匹配。规范化将嵌套的、非规范化数据转换为扁平的、索引化结构。

### API 响应转应用状态

**任务**：将嵌套的 API 响应转换为规范化状态。

#### API 响应（你得到的）

```typescript
interface ApiResponse {
  orders: Array<{
    id: string;
    customerId: string;
    customerName: string;
    customerEmail: string;
    items: Array<{
      productId: string;
      productName: string;
      quantity: number;
      price: number;
    }>;
    total: number;
    status: string;
  }>;
}
```

#### 应用状态（你需要的）

```typescript
interface NormalizedState {
  orders: {
    byId: Record<string, Order>;
    allIds: string[];
  };
  customers: {
    byId: Record<string, Customer>;
    allIds: string[];
  };
  products: {
    byId: Record<string, Product>;
    allIds: string[];
  };
}

interface Order {
  id: string;
  customerId: string;
  itemIds: string[];
  total: number;
  status: string;
}

interface Customer {
  id: string;
  name: string;
  email: string;
}

interface Product {
  id: string;
  name: string;
  price: number;
}
```

#### 命令式写法

```typescript
function normalizeApiResponse(response: ApiResponse): NormalizedState {
  const state: NormalizedState = {
    orders: { byId: {}, allIds: [] },
    customers: { byId: {}, allIds: [] },
    products: { byId: {}, allIds: [] },
  };

  for (const order of response.orders) {
    // 提取客户
    if (!state.customers.byId[order.customerId]) {
      state.customers.byId[order.customerId] = {
        id: order.customerId,
        name: order.customerName,
        email: order.customerEmail,
      };
      state.customers.allIds.push(order.customerId);
    }

    // 提取产品并构建商品 ID
    const itemIds: string[] = [];
    for (const item of order.items) {
      if (!state.products.byId[item.productId]) {
        state.products.byId[item.productId] = {
          id: item.productId,
          name: item.productName,
          price: item.price,
        };
        state.products.allIds.push(item.productId);
      }
      itemIds.push(item.productId);
    }

    // 添加规范化订单
    state.orders.byId[order.id] = {
      id: order.id,
      customerId: order.customerId,
      itemIds,
      total: order.total,
      status: order.status,
    };
    state.orders.allIds.push(order.id);
  }

  return state;
}
```

#### 函数式写法

```typescript
import { pipe } from 'fp-ts/function';
import * as A from 'fp-ts/Array';
import * as R from 'fp-ts/Record';

// 创建规范化集合的辅助函数
interface NormalizedCollection<T extends { id: string }> {
  byId: Record<string, T>;
  allIds: string[];
}

const createNormalizedCollection = <T extends { id: string }>(
  items: T[]
): NormalizedCollection<T> => ({
  byId: pipe(
    items,
    A.reduce({} as Record<string, T>, (acc, item) => ({
      ...acc,
      [item.id]: item,
    }))
  ),
  allIds: items.map(item => item.id),
});

// 提取实体
const extractCustomers = (orders: ApiResponse['orders']): Customer[] =>
  pipe(
    orders,
    A.map(order => ({
      id: order.customerId,
      name: order.customerName,
      email: order.customerEmail,
    })),
    A.uniq({ equals: (a, b) => a.id === b.id })
  );

const extractProducts = (orders: ApiResponse['orders']): Product[] =>
  pipe(
    orders,
    A.flatMap(order => order.items),
    A.map(item => ({
      id: item.productId,
      name: item.productName,
      price: item.price,
    })),
    A.uniq({ equals: (a, b) => a.id === b.id })
  );

const extractOrders = (orders: ApiResponse['orders']): Order[] =>
  orders.map(order => ({
    id: order.id,
    customerId: order.customerId,
    itemIds: order.items.map(item => item.productId),
    total: order.total,
    status: order.status,
  }));

// 组合成最终规范化结果
const normalizeApiResponse = (response: ApiResponse): NormalizedState => ({
  orders: createNormalizedCollection(extractOrders(response.orders)),
  customers: createNormalizedCollection(extractCustomers(response.orders)),
  products: createNormalizedCollection(extractProducts(response.orders)),
});
```

**函数式更好的原因**：每个提取函数独立且可测试。`createNormalizedCollection` 辅助函数可复用。添加新实体类型只需添加一个新提取函数。

### API 响应转 UI 就绪数据

**任务**：将 API 数据转换为组件所需格式。

```typescript
// API 返回的数据
interface ApiUser {
  user_id: string;
  first_name: string;
  last_name: string;
  email_address: string;
  created_at: string; // ISO 字符串
  avatar_url: string | null;
}

// 组件需要的数据
interface DisplayUser {
  id: string;
  fullName: string;
  email: string;
  memberSince: string; // "Jan 2024"
  avatarUrl: string; // 带回退值
}
```

#### 函数式写法

```typescript
const formatDate = (isoString: string): string => {
  const date = new Date(isoString);
  return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
};

const DEFAULT_AVATAR = 'https://example.com/default-avatar.png';

const toDisplayUser = (apiUser: ApiUser): DisplayUser => ({
  id: apiUser.user_id,
  fullName: `${apiUser.first_name} ${apiUser.last_name}`,
  email: apiUser.email_address,
  memberSince: formatDate(apiUser.created_at),
  avatarUrl: apiUser.avatar_url ?? DEFAULT_AVATAR,
});

// 转换用户数组
const toDisplayUsers = (apiUsers: ApiUser[]): DisplayUser[] =>
  apiUsers.map(toDisplayUser);
```

---

## 4. 分组与聚合

分组和聚合数据对于报表、仪表盘和分析至关重要。

### GroupBy：按键组织

**任务**：按客户分组订单。

#### 命令式写法

```typescript
interface Order {
  id: string;
  customerId: string;
  total: number;
  date: string;
}

function groupByCustomer(orders: Order[]): Record<string, Order[]> {
  const result: Record<string, Order[]> = {};

  for (const order of orders) {
    if (!result[order.customerId]) {
      result[order.customerId] = [];
    }
    result[order.customerId].push(order);
  }

  return result;
}
```

#### 函数式写法

```typescript
// 通用 groupBy 工具函数
const groupBy = <T, K extends string | number>(
  getKey: (item: T) => K
) => (items: T[]): Record<K, T[]> =>
  items.reduce(
    (groups, item) => {
      const key = getKey(item);
      return {
        ...groups,
        [key]: [...(groups[key] || []), item],
      };
    },
    {} as Record<K, T[]>
  );

// 使用示例
const groupByCustomer = groupBy<Order, string>(order => order.customerId);
const ordersByCustomer = groupByCustomer(orders);

// 或内联
const ordersByStatus = groupBy((order: Order) => order.status)(orders);
```

**使用 fp-ts NonEmptyArray.groupBy**：

```typescript
import * as NEA from 'fp-ts/NonEmptyArray';
import { pipe } from 'fp-ts/function';

// NEA.groupBy 保证结果中的数组非空
const ordersByCustomer = pipe(
  orders as NEA.NonEmptyArray<Order>, // 必须非空
  NEA.groupBy(order => order.customerId)
); // Record<string, NonEmptyArray<Order>>
```

### CountBy：计数统计

**任务**：按状态统计订单。

#### 命令式写法

```typescript
function countByStatus(orders: Order[]): Record<string, number> {
  const counts: Record<string, number> = {};

  for (const order of orders) {
    counts[order.status] = (counts[order.status] || 0) + 1;
  }

  return counts;
}
```

#### 函数式写法

```typescript
// 通用 countBy 工具函数
const countBy = <T, K extends string>(
  getKey: (item: T) => K
) => (items: T[]): Record<K, number> =>
  items.reduce(
    (counts, item) => {
      const key = getKey(item);
      return {
        ...counts,
        [key]: (counts[key] || 0) + 1,
      };
    },
    {} as Record<K, number>
  );

// 使用示例
const orderCountByStatus = countBy((order: Order) => order.status)(orders);
// { pending: 5, shipped: 12, delivered: 8 }
```

### SumBy：聚合数值

**任务**：按产品类别计算总收入。

#### 命令式写法

```typescript
interface Sale {
  productId: string;
  category: string;
  amount: number;
}

function sumByCategory(sales: Sale[]): Record<string, number> {
  const totals: Record<string, number> = {};

  for (const sale of sales) {
    totals[sale.category] = (totals[sale.category] || 0) + sale.amount;
  }

  return totals;
}
```

#### 函数式写法

```typescript
// 通用 sumBy 工具函数
const sumBy = <T, K extends string>(
  getKey: (item: T) => K,
  getValue: (item: T) => number
) => (items: T[]): Record<K, number> =>
  items.reduce(
    (totals, item) => {
      const key = getKey(item);
      return {
        ...totals,
        [key]: (totals[key] || 0) + getValue(item),
      };
    },
    {} as Record<K, number>
  );

// 使用示例
const revenueByCategory = sumBy(
  (sale: Sale) => sale.category,
  (sale: Sale) => sale.amount
)(sales);
// { electronics: 15000, clothing: 8500, books: 3200 }
```

### 复杂聚合示例

**任务**：从包含数量和单价的行项目计算总计。

```typescript
interface LineItem {
  productId: string;
  productName: string;
  quantity: number;
  unitPrice: number;
}

interface Invoice {
  id: string;
  lineItems: LineItem[];
  taxRate: number;
}
```

#### 函数式写法

```typescript
const lineTotal = (item: LineItem): number =>
  item.quantity * item.unitPrice;

const subtotal = (items: LineItem[]): number =>
  items.reduce((sum, item) => sum + lineTotal(item), 0);

const calculateTax = (amount: number, rate: number): number =>
  amount * rate;

const calculateInvoiceTotal = (invoice: Invoice): {
  subtotal: number;
  tax: number;
  total: number;
} => {
  const sub = subtotal(invoice.lineItems);
  const tax = calculateTax(sub, invoice.taxRate);

  return {
    subtotal: sub,
    tax,
    total: sub + tax,
  };
};

// 使用 fp-ts pipe 更清晰
import { pipe } from 'fp-ts/function';

const calculateInvoiceTotal = (invoice: Invoice) => {
  const sub = pipe(
    invoice.lineItems,
    A.map(lineTotal),
    A.reduce(0, (a, b) => a + b)
  );

  return {
    subtotal: sub,
    tax: sub * invoice.taxRate,
    total: sub * (1 + invoice.taxRate),
  };
};
```

---

## 5. 空值安全访问

别再写 `if (x && x.y && x.y.z)`。安全地导航嵌套结构，避免运行时错误。

### 问题所在

```typescript
interface Config {
  database?: {
    connection?: {
      host?: string;
      port?: number;
    };
    pool?: {
      max?: number;
    };
  };
  features?: {
    experimental?: {
      enabled?: boolean;
    };
  };
}
```

#### 命令式（冗长）写法

```typescript
function getDatabaseHost(config: Config): string {
  if (
    config.database &&
    config.database.connection &&
    config.database.connection.host
  ) {
    return config.database.connection.host;
  }
  return 'localhost';
}
```

#### 可选链（现代 TypeScript）

```typescript
const getDatabaseHost = (config: Config): string =>
  config.database?.connection?.host ?? 'localhost';
```

**诚实评估**：对于简单访问模式，可选链（`?.`）很完美。它是语言内置的，非常易读。当需要对可能缺失的值进行操作组合时，使用 fp-ts Option。

### 何时使用 Option

以下情况使用 fp-ts Option：
- 需要对可能缺失的值链式调用多个操作
- 想区分"缺失"与其他假值
- 正在构建转换管道

```typescript
import * as O from 'fp-ts/Option';
import { pipe } from 'fp-ts/function';

// 返回 Option 的安全属性访问
const prop = <T, K extends keyof T>(key: K) =>
  (obj: T | null | undefined): O.Option<T[K]> =>
    obj != null && key in obj
      ? O.some(obj[key] as T[K])
      : O.none;

// 使用 flatMap 链式访问
const getDatabaseHost = (config: Config): O.Option<string> =>
  pipe(
    O.some(config),
    O.flatMap(prop('database')),
    O.flatMap(prop('connection')),
    O.flatMap(prop('host'))
  );

// 提取并提供默认值
const host = pipe(
  getDatabaseHost(config),
  O.getOrElse(() => 'localhost')
);
```

### 安全数组访问

```typescript
import * as A from 'fp-ts/Array';
import * as O from 'fp-ts/Option';
import { pipe } from 'fp-ts/function';

// 命令式：数组为空时抛出异常
const first = items[0]; // 可能是 undefined！

// 安全：返回 Option
const first = A.head(items); // Option<Item>

// 获取首元素的名称，或默认值
const firstName = pipe(
  items,
  A.head,
  O.map(item => item.name),
  O.getOrElse(() => 'No items')
);

// 按索引安全查找
const third = pipe(
  items,
  A.lookup(2),
  O.map(item => item.name),
  O.getOrElse(() => 'Not found')
);
```

### 安全 Record/字典访问

```typescript
import * as R from 'fp-ts/Record';
import * as O from 'fp-ts/Option';
import { pipe } from 'fp-ts/function';

const users: Record<string, User> = {
  'user-1': { name: 'Alice', email: 'alice@example.com' },
  'user-2': { name: 'Bob', email: 'bob@example.com' },
};

// 命令式：可能是 undefined
const user = users['user-3']; // User | undefined

// 安全：返回 Option
const user = R.lookup('user-3')(users); // Option<User>

// 获取用户邮箱或默认值
const email = pipe(
  users,
  R.lookup('user-3'),
  O.map(u => u.email),
  O.getOrElse(() => 'unknown@example.com')
);
```

### 组合多个可选值

**任务**：获取用户的显示名称，需要同时有姓和名。

```typescript
interface Profile {
  firstName?: string;
  lastName?: string;
  nickname?: string;
}

// 命令式
function getDisplayName(profile: Profile): string {
  if (profile.firstName && profile.lastName) {
    return `${profile.firstName} ${profile.lastName}`;
  }
  if (profile.nickname) {
    return profile.nickname;
  }
  return 'Anonymous';
}

// 使用 Option 的函数式写法
import * as O from 'fp-ts/Option';
import { pipe } from 'fp-ts/function';

const getDisplayName = (profile: Profile): string =>
  pipe(
    // 先尝试全名
    O.Do,
    O.bind('first', () => O.fromNullable(profile.firstName)),
    O.bind('last', () => O.fromNullable(profile.lastName)),
    O.map(({ first, last }) => `${first} ${last}`),
    // 回退到昵称
    O.alt(() => O.fromNullable(profile.nickname)),
    // 最后默认为 Anonymous
    O.getOrElse(() => 'Anonymous')
  );
```

---

## 6. 实战示例

### 示例 1：API 响应转 UI 就绪数据

```typescript
// API 响应
interface ApiOrder {
  order_id: string;
  customer: {
    id: string;
    full_name: string;
  };
  line_items: Array<{
    product_id: string;
    product_name: string;
    qty: number;
    unit_price: number;
  }>;
  order_date: string;
  status: 'pending' | 'processing' | 'shipped' | 'delivered';
}

// UI 需要的数据
interface OrderSummary {
  id: string;
  customerName: string;
  itemCount: number;
  total: number;
  formattedTotal: string;
  date: string;
  statusLabel: string;
  statusColor: string;
}

// 转换
const STATUS_CONFIG: Record<string, { label: string; color: string }> = {
  pending: { label: 'Pending', color: 'yellow' },
  processing: { label: 'Processing', color: 'blue' },
  shipped: { label: 'Shipped', color: 'purple' },
  delivered: { label: 'Delivered', color: 'green' },
};

const formatCurrency = (cents: number): string =>
  `$${(cents / 100).toFixed(2)}`;

const formatDate = (iso: string): string =>
  new Date(iso).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

const toOrderSummary = (order: ApiOrder): OrderSummary => {
  const total = order.line_items.reduce(
    (sum, item) => sum + item.qty * item.unit_price,
    0
  );

  const status = STATUS_CONFIG[order.status] ?? STATUS_CONFIG.pending;

  return {
    id: order.order_id,
    customerName: order.customer.full_name,
    itemCount: order.line_items.reduce((sum, item) => sum + item.qty, 0),
    total,
    formattedTotal: formatCurrency(total),
    date: formatDate(order.order_date),
    statusLabel: status.label,
    statusColor: status.color,
  };
};

// 转换所有订单
const toOrderSummaries = (orders: ApiOrder[]): OrderSummary[] =>
  orders.map(toOrderSummary);
```

### 示例 2：合并用户设置与默认值

```typescript
interface AppSettings {
  theme: {
    mode: 'light' | 'dark' | 'system';
    primaryColor: string;
    fontSize: 'small' | 'medium' | 'large';
  };
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
    frequency: 'immediate' | 'daily' | 'weekly';
  };
  privacy: {
    showProfile: boolean;
    showActivity: boolean;
    allowAnalytics: boolean;
  };
}

type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

const DEFAULT_SETTINGS: AppSettings = {
  theme: {
    mode: 'system',
    primaryColor: '#007bff',
    fontSize: 'medium',
  },
  notifications: {
    email: true,
    push: true,
    sms: false,
    frequency: 'immediate',
  },
  privacy: {
    showProfile: true,
    showActivity: true,
    allowAnalytics: true,
  },
};

const deepMergeSettings = (
  defaults: AppSettings,
  user: DeepPartial<AppSettings>
): AppSettings => ({
  theme: { ...defaults.theme, ...user.theme },
  notifications: { ...defaults.notifications, ...user.notifications },
  privacy: { ...defaults.privacy, ...user.privacy },
});

// 使用示例
const userPreferences: DeepPartial<AppSettings> = {
  theme: { mode: 'dark' },
  notifications: { sms: true, frequency: 'daily' },
};

const finalSettings = deepMergeSettings(DEFAULT_SETTINGS, userPreferences);
```

### 示例 3：按客户分组订单并计算总计

```typescript
interface Order {
  id: string;
  customerId: string;
  customerName: string;
  items: Array<{ name: string; price: number; quantity: number }>;
  date: string;
}

interface CustomerOrderSummary {
  customerId: string;
  customerName: string;
  orderCount: number;
  totalSpent: number;
  orders: Order[];
}

const calculateOrderTotal = (order: Order): number =>
  order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);

const groupOrdersByCustomer = (orders: Order[]): CustomerOrderSummary[] => {
  const grouped = groupBy((order: Order) => order.customerId)(orders);

  return Object.entries(grouped).map(([customerId, customerOrders]) => ({
    customerId,
    customerName: customerOrders[0].customerName,
    orderCount: customerOrders.length,
    totalSpent: customerOrders.reduce(
      (sum, order) => sum + calculateOrderTotal(order),
      0
    ),
    orders: customerOrders,
  }));
};
```

### 示例 4：安全访问深层嵌套配置

```typescript
interface AppConfig {
  services?: {
    api?: {
      endpoints?: {
        users?: string;
        orders?: string;
        products?: string;
      };
      auth?: {
        type?: 'bearer' | 'basic' | 'oauth';
        token?: string;
      };
    };
    database?: {
      primary?: {
        host?: string;
        port?: number;
        name?: string;
      };
    };
  };
}

import * as O from 'fp-ts/Option';
import { pipe } from 'fp-ts/function';

// 创建类型安全的配置访问器
const getConfigValue = <T>(
  config: AppConfig,
  path: (config: AppConfig) => T | undefined,
  defaultValue: T
): T => path(config) ?? defaultValue;

// 使用可选链（最简单）
const apiUsersEndpoint = getConfigValue(
  config,
  c => c.services?.api?.endpoints?.users,
  '/api/users'
);

// 复杂场景使用 Option
const getEndpoint = (config: AppConfig, name: 'users' | 'orders' | 'products'): string =>
  pipe(
    O.fromNullable(config.services),
    O.flatMap(s => O.fromNullable(s.api)),
    O.flatMap(a => O.fromNullable(a.endpoints)),
    O.flatMap(e => O.fromNullable(e[name])),
    O.getOrElse(() => `/api/${name}`)
  );

// 多值复用模式
const getDbConfig = (config: AppConfig) => ({
  host: config.services?.database?.primary?.host ?? 'localhost',
  port: config.services?.database?.primary?.port ?? 5432,
  name: config.services?.database?.primary?.name ?? 'app',
});
```

---

## 7. 如何选择

### 使用原生方法的场景

- **简单转换**：`.map()`、`.filter()`、`.reduce()` 完全够用
- **无需组合**：一次性转换
- **团队熟悉度**：人人都懂原生方法
- **可选链足够**：`obj?.prop?.value ?? default` 能满足空值安全需求

```typescript
// 原生方法就够了
const activeUserNames = users
  .filter(u => u.isActive)
  .map(u => u.name);
```

### 使用 fp-ts 的场景

- **链式调用可能失败的操作**：多个步骤，每步都可能返回空值
- **组合转换**：构建可复用的转换管道
- **类型安全的错误处理**：让编译器追踪潜在失败
- **复杂数据管道**：多步骤，显式组合更清晰

```typescript
// fp-ts 在这里更有优势
const result = pipe(
  users,
  A.findFirst(u => u.id === userId),
  O.flatMap(u => O.fromNullable(u.profile)),
  O.flatMap(p => O.fromNullable(p.settings)),
  O.map(s => s.theme),
  O.getOrElse(() => 'default')
);
```

### 使用自定义工具函数的场景

- **领域特定操作**：`groupBy`、`countBy`、`sumBy` 针对你的数据
- **重复模式**：发现自己在写相同的转换很多次
- **团队约定**：在代码库中建立一致的模式

```typescript
// 自定义工具函数在多次使用时值得
const revenueByRegion = sumBy(
  (sale: Sale) => sale.region,
  (sale: Sale) => sale.amount
)(sales);
```

### 性能考量

- **链式调用创建中间数组**：`arr.filter().map()` 先创建一个数组，再创建另一个
- **热点路径考虑 `reduce`**：一次遍历数据
- **优化前先测量**：优化的可读性代价通常不值得

```typescript
// 如果性能重要（且已测量！）
const result = items.reduce((acc, item) => {
  if (item.isActive) {
    acc.push(item.name.toUpperCase());
  }
  return acc;
}, [] as string[]);

// vs 更易读（但两次遍历）的版本
const result = items
  .filter(item => item.isActive)
  .map(item => item.name.toUpperCase());
```

---

## 总结

| 任务 | 命令式 | 函数式 | 推荐 |
|------|--------|--------|------|
| 转换数组元素 | for 循环加 push | `.map()` | 使用 map |
| 过滤数组 | for 循环加条件 | `.filter()` | 使用 filter |
| 累积值 | for 循环加累加器 | `.reduce()` | 复杂用 reduce，简单用循环 |
| 按键分组 | for 循环加对象 | `groupBy` 工具函数 | 创建可复用工具函数 |
| 选取对象字段 | 手动复制属性 | `pick` 工具函数 | 一次性用展开，多次用工具函数 |
| 合并对象 | 逐属性复制 | 展开语法 | 使用展开 |
| 深度合并 | 嵌套条件判断 | 递归工具函数 | 使用工具函数或库 |
| 空值安全访问 | `if (x && x.y)` | `?.` 或 Option | 简单用 `?.`，组合用 Option |
| 规范化 API 数据 | 嵌套循环 | 提取函数 | 拆分为可组合函数 |

**函数式更好的情况：**
- 需要组合操作
- 想要可复用的转换
- 重视显式数据流胜过隐式状态
- 缺失值的类型安全很重要

**命令式可接受的情况：**
- 转换是一次性的
- 逻辑简单且线性
- 性能关键且已测量
- 团队更习惯这种方式

## 局限性
- 仅当任务明确匹配上述范围时使用本技能
- 输出不能替代特定环境的验证、测试或专家审查
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清
