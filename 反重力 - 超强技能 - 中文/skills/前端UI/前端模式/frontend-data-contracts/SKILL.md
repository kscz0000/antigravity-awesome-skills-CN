---
name: frontend-data-contracts
description: 为任意 React 或 React Native 应用的网络边界提供一套可移植、与框架无关的类型安全规范。它只用一个类型化 API 客户端作为唯一的 fetch 边界；用 parse-don't-validate 原则在数据进入应用之前把线上 JSON 转化为可信的领域类型；统一一种…
risk: unknown
source: https://github.com/stareezy-1/frontend-architecture-skill/tree/main/skills/frontend-data-contracts
source_repo: stareezy-1/frontend-architecture-skill
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/stareezy-1/frontend-architecture-skill/blob/main/LICENSE
---

# Frontend Data Contracts（类型化的网络边界）
## 何时使用

当你在任意 React 或 React Native 应用的网络边界需要一套可移植、与框架无关的类型安全规范时，使用本技能。它只用一个类型化 API 客户端作为唯一的 fetch 边界；用 parse-don't-validate 原则在数据进入应用之前把线上 JSON 转化为可信的领域类型；统一一种…

> 可移植技能 — 可被 Claude Code、OpenCode、Codex、Cursor、Windsurf 等阅读。
> 本技能描述的是**网络边界上的一套规范** —— 一个客户端、一个信封、一个错误类型，
> 加经过验证的类型 —— 它不是状态库，也不是样式系统。它与 **frontend-architecture**
> 技能配套使用（客户端位于 `shared/api-client/`），也是 **frontend-optimistic-mutations**
> 技能的基础。

目标：数据一旦从网络跨入应用，它就立刻不再是 `any` 形态的线上 JSON，
而是变成一个**可信的、类型化的领域值** —— 或者变成**一个统一的类型化错误**。
整个转换只发生在一个地方，没有未类型化的东西能逃逸出去。

---

## 0. 五个核心思想

1. **唯一客户端即唯一的 fetch 边界。** 一个类型化的 `apiClient` 包装了 `fetch`。组件和 hooks 绝不直接调用 `fetch`/`axios` —— 这个边界在代码评审和 lint 中是可强制执行的。
2. **Parse，而非 validate。** 线上 JSON 在边界处被解析为领域类型。客户端返回之后，值在所有下游都被信任 —— 不要再写防御性的 `?.` 链，也不要在组件里反复检查 shape。
3. **统一信封。** 每个成功响应都是 `{ data }`，每个失败响应都是 `{ error }`。客户端负责解包 `data` 并在 `error` 时抛出，调用方直接拿到 payload 或收到一个类型化的 throw。
4. **统一规范化的错误类型。** 服务端错误信封、非 2xx 状态码、格式错误的响应体、网络失败以及中止，都会归一成单个 `ApiError`，包含一个机器可读 code、status，以及可选的逐字段错误。调用方只需处理一种 shape。
5. **标识符带品牌。** 领域 ID 是 nominal 类型（`InvoiceId`、`CustomerId`），编译器会拒绝把一个 ID 传到另一个 ID 的位置 —— 这是数据密集型 UI 中最常见的隐性 bug。

---

## 1. 目录结构

边界就是 `shared/` 下的一个目录（依据 frontend-architecture 技能）。

```
src/shared/api-client/
├── index.ts        ← barrel: apiClient, ApiError, types
├── client.ts       ← the fetch wrapper: buildUrl, headers, parse, verbs
├── config.ts       ← base URL resolution, default headers
├── error.ts        ← the ApiError class + code→message-key mapping
├── types.ts        ← envelope types, HttpMethod, RequestOptions, field errors
└── client.test.ts  ← boundary behavior tests (envelope, errors, network)
```

领域实体类型及其 **schema** 放在特性模块内部
（`modules/{feature}/types/`）或一个共享的 contract 包里；客户端是 `T` 上的泛型。

---

## 2. 唯一客户端，即唯一的 fetch 边界

每个动词都返回由调用方类型化的、**已解包**的 `data` payload，并在任何失败时**抛出**一个
`ApiError`。组件永远看不到信封，也看不到裸响应。

```ts
// shared/api-client/client.ts (essence)
export const apiClient = {
  get<T>(path: string, options?: RequestOptions): Promise<T> {
    return request<T>("GET", path, undefined, options);
  },
  post<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return request<T>("POST", path, body, options);
  },
  patch<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T> {
    /* … */
  },
  put<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T> {
    /* … */
  },
  delete<T>(path: string, options?: RequestOptions): Promise<T> {
    /* … */
  },
} as const;

export type ApiClient = typeof apiClient;
```

```ts
// CORRECT — a feature hook wraps the client, typed by the caller
const invoice = await apiClient.get<Invoice>(`/invoices/${id}`, { signal });

// WRONG — a raw fetch in a component bypasses the boundary entirely
const res = await fetch(`/api/invoices/${id}`); // untyped, unhandled errors, no envelope
```

**硬性规则：**

- `shared/api-client/` 之外不允许 `fetch`/`axios`/`XMLHttpRequest` —— 用 ESLint 的 `no-restricted-imports`/`no-restricted-globals` 规则强制执行。
- 客户端是**与框架无关的**：不带 toast、不带 router、不带 React。副作用（toast、重定向）放在 query 层的 `onError` 里（见 §6）。
- 通过 `RequestOptions` 透传 `AbortSignal`，让 query 层可以取消（由 TanStack Query 串联）。

---

## 3. Parse，而非 validate（边界转换）

"Validate" 留给你的是一个无类型的值加上一个布尔值。"Parse" 返回的是**一个新的、类型化的值** —— 所以下游代码由类型系统保证正确。在边界处跑一次 schema 解析；之后，这个值就是可信的。

```ts
// modules/invoice/types/invoice.schema.ts
import { z } from "zod";

export const invoiceSchema = z.object({
  id: z.string().transform(toInvoiceId), // brand it (see §5)
  number: z.string(),
  status: z.nativeEnum(InvoiceStatus),
  total: z.number().int(), // minor units — never float money
  issuedAt: z.string().datetime(),
});
export type Invoice = z.infer<typeof invoiceSchema>;
```

```ts
// the client (or a thin per-entity wrapper) parses at the edge
const raw = await apiClient.get<unknown>(`/invoices/${id}`, { signal });
return invoiceSchema.parse(raw); // throws on contract drift → surfaces as a typed failure
```

**为什么这很重要：** 后端一旦给字段改名，或在不该出现 `null` 的地方发了 `null`，**在边界处**就能被捕获，并给出清晰的错误，而不是等到三层组件深处才冒出 `undefined`，那时堆栈已经毫无用处。下游组件再也不必写防御性的 `invoice?.total ?? 0`。

> 校验库可以自由选择 —— **Zod**、**Valibot**、**ArkType**、**io-ts**。规则不变：在边界处有一个 parse 步骤把 `unknown` 的线上数据转换为类型化的领域值。

---

## 4. 唯一的响应信封

在客户端里镜像后端的统一信封，并在客户端里只解包一次。

```ts
// shared/api-client/types.ts
export interface ApiSuccessEnvelope<T> {
  data: T;
}
export interface ApiErrorEnvelope {
  error: ApiErrorBody;
}
export type ApiEnvelope<T> = ApiSuccessEnvelope<T> | ApiErrorEnvelope;

export function isApiErrorEnvelope<T>(
  e: ApiEnvelope<T>,
): e is ApiErrorEnvelope {
  return typeof e === "object" && e !== null && "error" in e;
}

export interface ApiErrorBody {
  code: ServerErrorCode; // machine-readable, stable
  message: string; // server message (NOT shown to users directly)
  fields?: Record<string, string[]>; // per-field validation errors
}
```

parse 步骤覆盖每一种情况：`204 No Content` → `undefined`；`{ error }` → throw；非 2xx 但没有格式良好的信封 → 合成一个 error；`{ data }` → 返回 `data`。调用方只会看到一个类型化的 payload 或一次 throw。

---

## 5. 品牌化（nominal）标识符

字符串可以互换，领域 ID 不行。给它们打上品牌，编译器就会阻止你把 `CustomerId` 传到需要 `InvoiceId` 的地方。

```ts
// shared/types/id.ts
declare const brand: unique symbol;
export type Brand<T, B extends string> = T & { readonly [brand]: B };

export type InvoiceId = Brand<string, "InvoiceId">;
export type CustomerId = Brand<string, "CustomerId">;

export const toInvoiceId = (s: string): InvoiceId => s as InvoiceId;
export const toCustomerId = (s: string): CustomerId => s as CustomerId;
```

```ts
function loadInvoice(id: InvoiceId) {
  /* … */
}
loadInvoice(customerId); // ❌ compile error — exactly the bug you want caught
loadInvoice(invoiceId); // ✅
```

在 parse 边界（§3）处给 ID 打品牌，这样应用内每个 ID 就已经是 nominal 的。运行时成本为零 —— brand 在编译期被擦除。

---

## 6. 统一规范化的错误类型

把所有失败模式都归一到单个 `ApiError`，让调用方只处理一种 shape。它带有一个机器可读 `code`、HTTP `status`、可选的逐字段错误，以及一个用于本地化消息的稳定 key（它本身**不做**本地化 —— 那是 UI 的事）。

```ts
// shared/api-client/error.ts (essence)
export class ApiError extends Error {
  readonly code: ServerErrorCode;
  readonly status: number; // 0 when no response (network/abort)
  readonly fields?: Record<string, string[]>;

  get isNetworkError() {
    return this.status === 0;
  }
  get hasFieldErrors() {
    return !!this.fields && Object.keys(this.fields).length > 0;
  }
  /** Stable key under an `errors` i18n namespace — never a raw server string. */
  get messageKey() {
    if (this.isNetworkError) return "network";
    return ERROR_CODE_MESSAGE_KEYS[this.code] ?? "generic";
  }

  static fromEnvelope(body: ApiErrorBody, status: number) {
    /* server { error } */
  }
  static fromNetwork(cause: unknown) {
    /* offline / CORS / abort → status 0 */
  }
}
```

### 6.1 副作用放在哪里

客户端只负责抛出；**query 层**决定用户看到什么。把 toast/重定向留在客户端之外。

```ts
// a TanStack Query mutation maps the typed error to a localized toast
useMutation({
  mutationFn: (input) => apiClient.post<Invoice>("/invoices", input),
  onError: (error: ApiError) => notifyError(error), // looks up error.messageKey in i18n
});
```

### 6.2 逐字段错误 → 表单字段

服务端校验（`fields`）直接映射到表单字段错误 —— 一个地方，类型化。

```ts
if (error.hasFieldErrors) {
  for (const [field, messages] of Object.entries(error.fields!)) {
    form.setError(field as Path<FormValues>, { message: messages[0] });
  }
}
```

**硬性规则：**

- 数据层禁止 `throw new Error(string)` —— 一律用带 `code` 的 `ApiError`。
- 禁止把 `error.message`（一段服务端/开发字符串）直接展示给用户 —— 通过 i18n 解析 `messageKey`。
- 一个 2xx 但响应体无法解析是**契约违规** → 抛 `INVALID_RESPONSE`，不要悄悄返回 `undefined`。

---

## 7. 库适配器

规范本身是固定的；数据获取库只改变 `onError`/解析挂在哪一层。

| Library                    | Where the client is called                                                | Where `ApiError` is handled                                                      |
| -------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **TanStack Query**         | `queryFn`/`mutationFn` call `apiClient.*`                                 | `onError` per query/mutation, or a global `QueryCache`/`MutationCache` `onError` |
| **RTK Query**              | `baseQuery` wraps `apiClient`, parses + returns `{ data }` or `{ error }` | `transformErrorResponse` → `ApiError`; handle in component or middleware         |
| **SWR**                    | `fetcher = (key) => apiClient.get(key)`                                   | `onError` in `SWRConfig` or per-hook                                             |
| **Plain fetch hooks (RN)** | a `useAsync` wrapper calls `apiClient.*`                                  | try/catch sets a typed error state                                               |

对于 **React Native**，客户端无需改动 —— RN 里也有 `fetch` 和 `AbortController`。
只有 `credentials: "include"`（cookie 鉴权）可能需要根据你的鉴权方式换成 token header。

---

## 8. 约定清单（在评审中强制）

- [ ] `shared/api-client/` 下恰好只有一个 `apiClient`；其他地方没有 `fetch`/`axios`（lint 强制）。
- [ ] 客户端与框架无关 —— 内部不带 toast、router 或 React。
- [ ] 响应在边界处被解析为类型化的领域值（parse，而非 validate）。
- [ ] 唯一的 `{ data } / { error }` 信封，在客户端里只解包一次。
- [ ] 每个失败都归一成一个 `ApiError`（code + status + 可选 fields）；不允许裸 `throw new Error`。
- [ ] 领域 ID 是品牌化的；ID 在 parse 边界处被打上品牌。
- [ ] `error.messageKey` 通过 i18n 解析 —— 服务端的 `message` 绝不直接展示给用户。
- [ ] 服务端逐字段错误通过类型化的 `fields` map 映射到表单字段。
- [ ] `AbortSignal` 通过 `RequestOptions` 流转以支持取消。
- [ ] 一个 2xx 但响应体格式错误时，抛出契约违规错误，而不是 `undefined`。

---

## 9. 如何应用本技能

**给项目加上边界：** 在 `shared/api-client/` 下创建 `client.ts`、`error.ts`、
`types.ts`、`config.ts`。加上禁止其他地方用 `fetch`/`axios` 的 lint 规则。
按后端的契约定义你的信封和 `ApiError` codes。

**新增一个实体：** 在特性模块里定义它的 schema（Zod/Valibot）和 `z.infer` 类型，
在 parse 时给它的 ID 打品牌，并把 `apiClient` 包到类型化的 query/mutation hooks 里 —— 永远不要在组件里直接调用客户端。

**调试"三层组件深处的 undefined"：** 补/修边界处的 parse，让契约漂移在边缘处用类型化错误大声失败，而不是把 `undefined` 泄漏到下游。

**评审数据层：** 跑一遍 §8 的清单。最值得抓的是组件里的裸 `fetch`（绕过了边界）和数据层里的 `throw new Error(string)`（未类型化的失败）。

---

## 发布 / 安装本技能

本技能遵循 Anthropic 的 `SKILL.md` 格式，可在多个智能体间移植。

1. 把它放在公开 GitHub 仓库下的 `skills/frontend-data-contracts/SKILL.md`。
2. 保留 frontmatter 中的 `name` 和高信号的 `description` —— 发现索引依赖它们匹配。
3. 通过 `npx skills add <org>/<repo> --skill "frontend-data-contracts"` 安装。
4. 非 `SKILL.md` 的智能体可以从 `AGENTS.md` / `CLAUDE.md` 指向这里；Kiro 可以把它镜像成 steering file。

## 局限性

- 只有在任务明确匹配其上游来源和本地项目上下文时，才使用本技能。
- 在应用变更前，校验命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要把示例当成环境专属测试、安全审查或对破坏性/高代价操作的授权的替代。