---
name: frontend-optimistic-mutations
description: 一个可移植、与框架无关的规范，适用于任何使用 query/cache 层的 React 或 React Native 应用的写入路径。固化乐观更新生命周期（取消进行中的查询 → 快照每个受影响的缓存 → 即时打补丁 → 出错时逐字回滚 → 完成后失效）。当用户提及乐观更新、乐观突变、回滚、idempotency key、useMutation onMutate、TanStack Query 写入路径、RTK Query updateQueryData、SWR mutate rollbackOnError、缓存一致性、列表与详情同步、或 React/React Native 写入路径规范时使用。
risk: unknown
source: https://github.com/stareezy-1/frontend-architecture-skill/tree/main/skills/frontend-optimistic-mutations
source_repo: stareezy-1/frontend-architecture-skill
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/stareezy-1/frontend-architecture-skill/blob/main/LICENSE
---

# 前端乐观突变（写入路径）
## 使用场景

当你需要一套可移植、与框架无关的写入路径规范，用于任何使用 query/cache 层的 React 或 React Native 应用时，使用本技能。它固化了乐观更新生命周期（取消进行中的查询 → 快照每个受影响的缓存 → 即时打补丁 → 出错时逐字回滚 → 完成后失效……）。


> 可移植技能——Claude Code、OpenCode、Codex、Cursor、Windsurf 等均可阅读。
> 本技能描述的是**写入路径的规范**——乐观更新、回滚、幂等性、缓存一致性——而非某个 UI 库或样式系统。它直接建立在 **frontend-data-contracts** 技能（写入通过类型化客户端进行）和 **frontend-architecture** 技能（突变位于 `modules/{feature}/hooks/`，由工厂函数生成键）之上。

目标：写入操作**感觉即时**（UI 在服务器确认前就反映出变化），**安全可靠**（失败时恢复精确的先前状态，重试绝不会重复扣款），并使缓存保持**一致**（详情视图与每个列表页一致）。三者同时做到——这就是技艺所在。

---

## 0. 五大核心思想

1. **乐观生命周期是固定的。** 取消 → 快照 → 打补丁 →（出错：回滚）→（完成：失效）。每个乐观突变都遵循同样的五个节拍。
2. **逐字回滚。** 失败时，恢复打补丁前所取的精确快照——而不是靠"最佳猜测"重新推导。将快照保留在突变上下文中。
3. **幂等键只生成一次，而不是每次尝试都生成。** 键在表单初始化时（或首次意图时）创建，以便网络重放重试时返回原始服务器响应，而非重复执行动作。
4. **缓存同步推进。** 状态变更同时打补丁到详情缓存**和**包含该实体的每个列表页，使不同视图上的徽标永不冲突。
5. **服务器状态永不进入客户端 store。** 乐观状态存于 query 缓存中，而非 Zustand/Redux。缓存是服务器数据的唯一真相源（参见 frontend-architecture §4）。

---

## 1. 何时使用乐观更新（以及何时不用）

| 场景                                                                              | 策略                                                                                                                          |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 高置信、低冲突的写入（切换状态、点赞、标记已付、排序）                            | **乐观** —— 立即打补丁，出错时回滚。                                                                                          |
| 需要服务器生成 id/编号/总计的创建操作                                             | **待定状态**，随后通过服务器响应 `setQueryData`。可选地临时插入乐观行；成功时协调一致。                                       |
| 破坏性或难以撤销的写入（级联删除、转账）                                          | **先确认**，再乐观**或**待定——绝不静默乐观。                                                                                  |
| 用户暂时看不到结果的写入（后台任务）                                              | **待定 + Toast**，完成时失效。不打乐观补丁。                                                                                  |

乐观是一种针对你确信会成功的写入的 UX 工具。如果失败常见或撤销代价高昂，请优先使用待定状态。

---

## 2. 乐观生命周期（TanStack Query）

规范的形态。每个节拍都有其职责；跳过任何一个都会破坏正确性。

```ts
// modules/invoice/hooks/useInvoiceMutations.ts
interface MarkPaidContext {
  previousInvoice: Invoice | undefined; // detail snapshot
  previousLists: Array<[readonly unknown[], InvoiceListResponse]>; // every list page snapshot
}

export function useMarkInvoicePaid() {
  const queryClient = useQueryClient();
  const notifyError = useApiErrorToast();

  return useMutation<Invoice, ApiError, { id: InvoiceId }, MarkPaidContext>({
    mutationFn: ({ id }) => apiClient.post<Invoice>(INVOICE_API.markPaid(id)),

    // 1 + 2 + 3: cancel in-flight reads, snapshot, patch
    onMutate: async ({ id }) => {
      await queryClient.cancelQueries({ queryKey: invoiceKeys.all }); // (1) no late refetch clobber

      const detailKey = invoiceKeys.detail(id);
      const previousInvoice = queryClient.getQueryData<Invoice>(detailKey); // (2) snapshot detail
      if (previousInvoice) {
        queryClient.setQueryData<Invoice>(detailKey, {
          // (3) patch detail
          ...previousInvoice,
          status: InvoiceStatus.Paid,
        });
      }

      const previousLists: MarkPaidContext["previousLists"] = [];
      for (const [key, list] of queryClient.getQueriesData<InvoiceListResponse>(
        {
          queryKey: invoiceKeys.lists(),
        },
      )) {
        if (!list) continue;
        previousLists.push([key, list]); // (2) snapshot each page
        if (!list.invoices.some((i) => i.id === id)) continue;
        queryClient.setQueryData<InvoiceListResponse>(key, {
          // (3) patch matching row
          ...list,
          invoices: list.invoices.map((i) =>
            i.id === id ? { ...i, status: InvoiceStatus.Paid } : i,
          ),
        });
      }
      return { previousInvoice, previousLists };
    },

    // 4: roll back verbatim
    onError: (error, { id }, ctx) => {
      if (ctx?.previousInvoice)
        queryClient.setQueryData(invoiceKeys.detail(id), ctx.previousInvoice);
      for (const [key, list] of ctx?.previousLists ?? [])
        queryClient.setQueryData(key, list);
      notifyError(error);
    },

    // 5: invalidate so authoritative server state (paidAt, aggregates) refetches
    onSettled: (_d, _e, { id }) => {
      void queryClient.invalidateQueries({ queryKey: invoiceKeys.detail(id) });
      void queryClient.invalidateQueries({ queryKey: invoiceKeys.lists() });
    },
  });
}
```

**每个节拍的作用：**

- **取消** —— 没有它，已经在飞的查询可能在你的补丁之后解析并覆盖乐观状态。
- **快照** —— 唯一安全的回滚来源；绝不要手工重建先前状态。
- **打补丁** —— 即时 UX；同时变更详情**和**列表（§4）。
- **回滚** —— 逐字恢复快照，然后展示类型化的 `ApiError`。
- **完成时失效** —— 无论成功失败，都重新拉取，使服务器计算字段（时间戳、汇总）成为权威。是在"完成"时而非仅在"成功"时：失败的写入也可能改变了服务器状态。

---

## 3. 非乐观写入：创建带服务器自有字段的记录

返回 id/编号/总计的创建操作无法完全乐观。作为待定突变运行，并用响应数据填充缓存。

```ts
export function useCreateInvoice() {
  const queryClient = useQueryClient();
  return useMutation<Invoice, ApiError, CreateInvoiceInput>({
    mutationFn: ({ document, idempotencyKey }) =>
      apiClient.post<Invoice>("/invoices", document, { idempotencyKey }),
    onSuccess: (invoice) => {
      queryClient.setQueryData(invoiceKeys.detail(invoice.id), invoice); // seed detail
      void queryClient.invalidateQueries({ queryKey: invoiceKeys.lists() }); // refresh lists
    },
    onError: (error) => notifyError(error),
  });
}
```

---

## 4. 缓存一致性（详情 + 列表同步推进）

单一实体出现在多个缓存中：它的详情，以及每个经过筛选/分页的列表页。一次乐观补丁必须触及**所有这些缓存**，否则各视图会不一致。使用**分层键工厂**（参见 frontend-architecture §4.3），以便精确命中目标。

```ts
export const invoiceKeys = {
  all: ["invoices"] as const,
  lists: () => [...invoiceKeys.all, "list"] as const,
  list: (p: IListParams) => [...invoiceKeys.lists(), p] as const,
  detail: (id: InvoiceId) => [...invoiceKeys.all, "detail", id] as const,
} as const;
```

- `getQueriesData({ queryKey: invoiceKeys.lists() })` 枚举**每个**已缓存的列表页，以便逐一打补丁。
- `invalidateQueries({ queryKey: invoiceKeys.lists() })` 在完成时刷新它们。
- `detail(id)` 精确命中单个实体。

为你触及的**每一页**做快照（以其精确的 query 键为键），以便回滚时逐字恢复每一页，而不仅仅是当前屏幕上的那一页。

---

## 5. 幂等性（在涉及金钱的写入上安全重试）

重试的 POST 不得重复执行动作。在**表单初始化时（或用户首次意图时）一次性**生成键，将其贯穿所有重试，并让客户端将其作为请求头发送。服务器在其窗口期内对重复的键重放原始响应。

```ts
// at form initialisation — stable for the lifetime of this attempt
const idempotencyKey = useMemo(() => crypto.randomUUID(), []);

// mutation forwards it; the typed client puts it on the header
apiClient.post<Invoice>("/invoices", document, { idempotencyKey });
```

**硬性规则：**

- 在**意图时刻**生成键，而不是在 `mutationFn` 内部（后者每次重试都会重新运行 → 失去意义）。
- 数据客户端自动检测金融类路由并注入该请求头；显式键总是优先生效，使重试能够重放。
- 将幂等性与**待定时禁用**的 UI 配对，以防用户发起第二次不同的写入。

---

## 6. 重试策略

- **读取：** 带退避策略重试几次（大多数 query 库的默认行为）——安全且幂等。
- **写入：** 对非幂等突变**不要**自动重试。仅当幂等键保证重放时、或仅在网络错误（状态码 0）时重试，绝不在 4xx 时重试。
- **冲突（409）：** 不重试——展示类型化错误，失效，让用户在新鲜数据上重新决策。

```ts
useMutation({
  retry: (count, error: ApiError) => error.isNetworkError && count < 2, // network-only, bounded
});
```

---

## 7. 库适配器

五个节拍的生命周期是相同的；区别在于 hook。

| 库                | 乐观机制                                                                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TanStack Query** | `onMutate`（取消 + 快照 + 打补丁）→ `onError`（回滚）→ `onSettled`（失效）。上面的参考形态。                                                              |
| **RTK Query**      | `onQueryStarted`：`updateQueryData` 返回一个 `patchResult`；`await queryFulfilled` 并在 `catch` 中调用 `patchResult.undo()`。完成时使用 `invalidatesTags`。 |
| **SWR**            | `mutate(key, optimisticData, { rollbackOnError: true, populateCache, revalidate: true })` —— 乐观数据 + 自动回滚 + 重新校验。                            |

对于 **React Native**，上述三个库都不需要改动即可使用；缓存同样在原生侧是真相源。保持突变 hook 不依赖 DOM，以便在 Web 和原生之间共享。

---

## 8. 规范清单（在评审中强制执行）

- [ ] 乐观突变遵循 取消 → 快照 → 打补丁 → 回滚 → 失效 的顺序。
- [ ] `onMutate` 在打补丁前取消进行中的查询。
- [ ] 回滚从上下文中恢复**精确**的快照，而不是重新推导。
- [ ] 详情**和**每个受影响的列表页一并被打补丁和快照。
- [ ] `onSettled` 失效，使服务器计算的字段被重新拉取（成功**和**出错时均如此）。
- [ ] 幂等键在意图时生成并在重试间重放，而不是每次尝试重新生成。
- [ ] 涉及金钱/破坏性的写入先确认，并在待定期间禁用触发按钮。
- [ ] 非幂等写入不自动重试；409 错误展示而非重试。
- [ ] 服务器状态保留在 query 缓存中——绝不复制到客户端 store。
- [ ] Query 键来自分层工厂；失效是精确范围的，而非全局一刀切。

---

## 9. 如何应用本技能

**新增乐观突变：** 决定它适合乐观（§1）。编写五个节拍（§2）。识别实体所在的每个缓存并对它们一并打补丁/快照（§4）。

**让写入可安全重试：** 在表单初始化时生成幂等键，将其贯穿整个突变，确认客户端会发送它（§5），并设置仅限网络错误的有限重试（§6）。

**调试闪烁/写入后状态错误：** 检查 `onMutate` 是否取消了查询（晚到的 refetch 覆盖）以及 `onSettled` 是否失效（陈旧的服务器计算字段）。检查**所有**列表页是否都打了补丁，而不仅仅是可见的那一页。

**评审写入路径：** 运行 §8 的清单。最有价值的捕获项是缺失的 `cancelQueries`（竞争覆盖）、部分缓存补丁（详情/列表不一致）以及在 `mutationFn` 内生成的幂等键（不再保护重试）。

---

## 发布 / 安装本技能

本技能遵循 Anthropic 的 `SKILL.md` 格式，可跨智能体移植。

1. 将其放在公共 GitHub 仓库的 `skills/frontend-optimistic-mutations/SKILL.md` 下。
2. 保留 frontmatter 的 `name` 和高信号的 `description`——发现索引据此匹配。
3. 通过以下方式安装：`npx skills add <org>/<repo> --skill "frontend-optimistic-mutations"`。
4. 非 `SKILL.md` 的智能体可从 `AGENTS.md` / `CLAUDE.md` 指向此处；Kiro 可将其作为 steering 文件镜像。

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用更改之前，请验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要将示例视为针对特定环境的测试、安全审查或用户对破坏性/高成本操作的批准的替代品。