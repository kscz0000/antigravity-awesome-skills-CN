---
name: algolia-search
description: Algolia 搜索实现、索引策略、React InstantSearch 和相关性调优的专家模式。触发词：Algolia搜索、InstantSearch、搜索实现、索引策略、相关性调优、React搜索、全文搜索、搜索API、自动补全搜索、分面搜索
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Algolia 搜索集成

Algolia 搜索实现、索引策略、React InstantSearch 和相关性调优的专家模式

## 模式

### React InstantSearch 与 Hooks

使用 hooks 的现代 React InstantSearch 配置，实现即时搜索。

使用 react-instantsearch-hooks-web 包和 algoliasearch 客户端。
Widgets 是可以用 classnames 自定义的组件。

核心 hooks：
- useSearchBox: 搜索输入处理
- useHits: 访问搜索结果
- useRefinementList: 分面过滤
- usePagination: 结果分页
- useInstantSearch: 完整状态访问

### 代码示例

// lib/algolia.ts
import algoliasearch from 'algoliasearch/lite';

export const searchClient = algoliasearch(
  process.env.NEXT_PUBLIC_ALGOLIA_APP_ID!,
  process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY!  // Search-only key!
);

export const INDEX_NAME = 'products';

// components/Search.tsx
'use client';
import { InstantSearch, SearchBox, Hits, Configure } from 'react-instantsearch';
import { searchClient, INDEX_NAME } from '@/lib/algolia';

function Hit({ hit }: { hit: ProductHit }) {
  return (
    <article>
      <h3>{hit.name}</h3>
      <p>{hit.description}</p>
      <span>${hit.price}</span>
    </article>
  );
}

export function ProductSearch() {
  return (
    <InstantSearch searchClient={searchClient} indexName={INDEX_NAME}>
      <Configure hitsPerPage={20} />
      <SearchBox
        placeholder="Search products..."
        classNames={{
          root: 'relative',
          input: 'w-full px-4 py-2 border rounded',
        }}
      />
      <Hits hitComponent={Hit} />
    </InstantSearch>
  );
}

// Custom hook usage
import { useSearchBox, useHits, useInstantSearch } from 'react-instantsearch';

function CustomSearch() {
  const { query, refine } = useSearchBox();
  const { hits } = useHits<ProductHit>();
  const { status } = useInstantSearch();

  return (
    <div>
      <input
        value={query}
        onChange={(e) => refine(e.target.value)}
        placeholder="Search..."
      />
      {status === 'loading' && <p>Loading...</p>}
      <ul>
        {hits.map((hit) => (
          <li key={hit.objectID}>{hit.name}</li>
        ))}
      </ul>
    </div>
  );
}

### 反模式

- 模式：在前端代码中使用 Admin API key | 原因：Admin key 暴露完整的索引控制权限，包括删除 | 修复：使用带限制的 search-only API key
- 模式：前端未使用 /lite 客户端 | 原因：完整客户端包含搜索不需要的冗余代码 | 修复：从 algoliasearch/lite 导入以减小包体积

### 参考资料

- https://www.algolia.com/doc/api-reference/widgets/react
- https://www.algolia.com/doc/libraries/javascript/v5/methods/search/

### Next.js 服务端渲染

使用 react-instantsearch-nextjs 包实现 Next.js SSR 集成。

SSR 场景下使用 <InstantSearchNext> 替代 <InstantSearch>。
支持 Pages Router 和 App Router（实验性）。

关键注意事项：
- 设置 dynamic = 'force-dynamic' 以获取最新结果
- 使用 routing prop 处理 URL 同步
- 使用 getServerState 获取初始状态

### 代码示例

// app/search/page.tsx
import { InstantSearchNext } from 'react-instantsearch-nextjs';
import { searchClient, INDEX_NAME } from '@/lib/algolia';
import { SearchBox, Hits, RefinementList } from 'react-instantsearch';

// Force dynamic rendering for fresh search results
export const dynamic = 'force-dynamic';

export default function SearchPage() {
  return (
    <InstantSearchNext
      searchClient={searchClient}
      indexName={INDEX_NAME}
      routing={{
        router: {
          cleanUrlOnDispose: false,
        },
      }}
    >
      <div className="flex gap-8">
        <aside className="w-64">
          <h3>Categories</h3>
          <RefinementList attribute="category" />
          <h3>Brand</h3>
          <RefinementList attribute="brand" />
        </aside>
        <main className="flex-1">
          <SearchBox placeholder="Search products..." />
          <Hits hitComponent={ProductHit} />
        </main>
      </div>
    </InstantSearchNext>
  );
}

// For custom routing (URL synchronization)
import { history } from 'instantsearch.js/es/lib/routers';
import { simple } from 'instantsearch.js/es/lib/stateMappings';

<InstantSearchNext
  searchClient={searchClient}
  indexName={INDEX_NAME}
  routing={{
    router: history({
      getLocation: () =>
        typeof window === 'undefined'
          ? new URL(url) as unknown as Location
          : window.location,
    }),
    stateMapping: simple(),
  }}
>
  {/* widgets */}
</InstantSearchNext>

### 反模式

- 模式：在 Next.js SSR 中使用 InstantSearch 组件 | 原因：普通组件不支持服务端渲染 | 修复：使用 react-instantsearch-nextjs 的 InstantSearchNext
- 模式：搜索页面使用静态渲染 | 原因：搜索结果必须每次请求都是最新的 | 修复：设置 export const dynamic = 'force-dynamic'

### 参考资料

- https://www.npmjs.com/package/react-instantsearch-nextjs
- https://www.algolia.com/developers/code-exchange/instantsearch-and-next-js-starter

### 数据同步与索引

保持 Algolia 与数据同步的索引策略。

三种主要方式：
1. 全量重建索引 - 替换整个索引（开销大）
2. 全量记录更新 - 替换单条记录
3. 部分更新 - 仅更新特定属性

最佳实践：
- 批量处理记录（理想：10MB，每批 1K-10K 条记录）
- 尽可能使用增量更新
- 属性级变更使用 partialUpdateObjects
- 避免使用 deleteBy（计算开销大）

### 代码示例

// lib/algolia-admin.ts (SERVER ONLY)
import algoliasearch from 'algoliasearch';

// Admin client - NEVER expose to frontend
const adminClient = algoliasearch(
  process.env.ALGOLIA_APP_ID!,
  process.env.ALGOLIA_ADMIN_KEY!  // Admin key for indexing
);

const index = adminClient.initIndex('products');

// Batch indexing (recommended approach)
export async function indexProducts(products: Product[]) {
  const records = products.map((p) => ({
    objectID: p.id,  // Required unique identifier
    name: p.name,
    description: p.description,
    price: p.price,
    category: p.category,
    inStock: p.inventory > 0,
    createdAt: p.createdAt.getTime(),  // Use timestamps for sorting
  }));

  // Batch in chunks of ~1000-5000 records
  const BATCH_SIZE = 1000;
  for (let i = 0; i < records.length; i += BATCH_SIZE) {
    const batch = records.slice(i, i + BATCH_SIZE);
    await index.saveObjects(batch);
  }
}

// Partial update - update only specific fields
export async function updateProductPrice(productId: string, price: number) {
  await index.partialUpdateObject({
    objectID: productId,
    price,
    updatedAt: Date.now(),
  });
}

// Partial update with operations
export async function incrementViewCount(productId: string) {
  await index.partialUpdateObject({
    objectID: productId,
    viewCount: {
      _operation: 'Increment',
      value: 1,
    },
  });
}

// Delete records (prefer this over deleteBy)
export async function deleteProducts(productIds: string[]) {
  await index.deleteObjects(productIds);
}

// Full reindex with zero-downtime (atomic swap)
export async function fullReindex(products: Product[]) {
  const tempIndex = adminClient.initIndex('products_temp');

  // Index to temp index
  await tempIndex.saveObjects(
    products.map((p) => ({
      objectID: p.id,
      ...p,
    }))
  );

  // Copy settings from main index
  await adminClient.copyIndex('products', 'products_temp', {
    scope: ['settings', 'synonyms', 'rules'],
  });

  // Atomic swap
  await adminClient.moveIndex('products_temp', 'products');
}

### 反模式

- 模式：使用 deleteBy 批量删除 | 原因：deleteBy 计算开销大且有速率限制 | 修复：使用 deleteObjects 配合 objectID 数组
- 模式：逐条索引记录 | 原因：产生索引队列，拖慢处理速度 | 修复：以 1K-10K 为单位批量处理
- 模式：小改动也做全量重建 | 原因：浪费操作次数，比增量更新慢 | 修复：属性变更使用 partialUpdateObject

### 参考资料

- https://www.algolia.com/doc/guides/sending-and-managing-data/send-and-update-your-data/in-depth/the-different-synchronization-strategies
- https://www.algolia.com/blog/engineering/search-indexing-best-practices-for-top-performance-with-code-samples

### API Key 安全与限制

Algolia 的安全 API key 配置。

密钥类型：
- Admin API Key: 完全控制（索引、设置、删除）
- Search-Only API Key: 前端安全使用
- Secured API Keys: 从基础密钥生成，带限制条件

可用限制：
- Indices: 限制可访问的索引
- Rate limit: 限制每 IP 每小时的 API 调用次数
- Validity: 设置过期时间
- HTTP referrers: 限制特定 URL
- Query parameters: 强制搜索参数

### 代码示例

// NEVER do this - admin key in frontend
// const client = algoliasearch(appId, ADMIN_KEY);  // WRONG!

// Correct: Use search-only key in frontend
const searchClient = algoliasearch(
  process.env.NEXT_PUBLIC_ALGOLIA_APP_ID!,
  process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY!
);

// Server-side: Generate secured API key
// lib/algolia-secured-key.ts
import algoliasearch from 'algoliasearch';

const adminClient = algoliasearch(
  process.env.ALGOLIA_APP_ID!,
  process.env.ALGOLIA_ADMIN_KEY!
);

// Generate user-specific secured key
export function generateSecuredKey(userId: string) {
  const searchKey = process.env.ALGOLIA_SEARCH_KEY!;

  return adminClient.generateSecuredApiKey(searchKey, {
    // User can only see their own data
    filters: `userId:${userId}`,
    // Key expires in 1 hour
    validUntil: Math.floor(Date.now() / 1000) + 3600,
    // Restrict to specific index
    restrictIndices: ['user_documents'],
  });
}

// Rate-limited key for public APIs
export async function createRateLimitedKey() {
  const { key } = await adminClient.addApiKey({
    acl: ['search'],
    indexes: ['products'],
    description: 'Public search with rate limit',
    maxQueriesPerIPPerHour: 1000,
    referers: ['https://mysite.com/*'],
    validity: 0,  // Never expires
  });

  return key;
}

// API endpoint to get user's secured key
// app/api/search-key/route.ts
import { auth } from '@/lib/auth';
import { generateSecuredKey } from '@/lib/algolia-secured-key';

export async function GET() {
  const session = await auth();
  if (!session?.user) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const securedKey = generateSecuredKey(session.user.id);

  return Response.json({ key: securedKey });
}

### 反模式

- 模式：在客户端代码中硬编码 Admin API key | 原因：向攻击者暴露完整索引控制权限 | 修复：使用带限制的 search-only key
- 模式：所有用户使用同一密钥 | 原因：无法按用户限制数据访问 | 修复：生成带用户过滤器的 secured API keys
- 模式：公开搜索无速率限制 | 原因：机器人可能耗尽搜索配额 | 修复：在 API key 上设置 maxQueriesPerIPPerHour

### 参考资料

- https://www.algolia.com/doc/guides/security/api-keys
- https://support.algolia.com/hc/en-us/articles/14339249272977-What-are-the-best-practices-to-manage-Algolia-API-keys-in-my-code-and-protect-them

### 自定义排序与相关性调优

配置可搜索属性和自定义排序以提升相关性。

可搜索属性（顺序重要）：
1. 最重要的字段在前（title, name）
2. 其次是次要字段（description, tags）
3. 排除非搜索字段（image_url, id）

自定义排序：
- 添加业务指标（popularity, rating, date）
- 使用 desc() 降序，asc() 升序

### 代码示例

// scripts/configure-index.ts
import algoliasearch from 'algoliasearch';

const adminClient = algoliasearch(
  process.env.ALGOLIA_APP_ID!,
  process.env.ALGOLIA_ADMIN_KEY!
);

const index = adminClient.initIndex('products');

async function configureIndex() {
  await index.setSettings({
    // Searchable attributes in order of importance
    searchableAttributes: [
      'name',              // Most important
      'brand',
      'category',
      'description',       // Least important
    ],

    // Attributes for faceting/filtering
    attributesForFaceting: [
      'category',
      'brand',
      'filterOnly(inStock)',  // Filter only, not displayed
      'searchable(tags)',     // Searchable facet
    ],

    // Custom ranking (after text relevance)
    customRanking: [
      'desc(popularity)',     // Most popular first
      'desc(rating)',         // Then by rating
      'desc(createdAt)',      // Then by recency
    ],

    // Typo tolerance
    typoTolerance: true,
    minWordSizefor1Typo: 4,
    minWordSizefor2Typos: 8,

    // Query settings
    queryLanguages: ['en'],
    removeStopWords: ['en'],

    // Highlighting
    attributesToHighlight: ['name', 'description'],
    highlightPreTag: '<mark>',
    highlightPostTag: '</mark>',

    // Pagination
    hitsPerPage: 20,
    paginationLimitedTo: 1000,

    // Distinct (deduplication)
    attributeForDistinct: 'productFamily',
    distinct: true,
  });

  // Add synonyms
  await index.saveSynonyms([
    {
      objectID: 'phone-mobile',
      type: 'synonym',
      synonyms: ['phone', 'mobile', 'cell', 'smartphone'],
    },
    {
      objectID: 'laptop-notebook',
      type: 'oneWaySynonym',
      input: 'laptop',
      synonyms: ['notebook', 'portable computer'],
    },
  ]);

  // Add rules (query-based customization)
  await index.saveRules([
    {
      objectID: 'boost-sale-items',
      condition: {
        anchoring: 'contains',
        pattern: 'sale',
      },
      consequence: {
        params: {
          filters: 'onSale:true',
          optionalFilters: ['featured:true'],
        },
      },
    },
  ]);

  console.log('Index configured successfully');
}

configureIndex();

### 反模式

- 模式：所有属性同等搜索 | 原因：降低相关性，描述中的匹配与标题同等排名 | 修复：按重要性排序 searchableAttributes
- 模式：无自定义排序 | 原因：仅依赖文本匹配，忽略业务价值 | 修复：在 customRanking 中添加 popularity、rating 或 recency
- 模式：将原始日期字符串索引 | 原因：无法正确按日期排序 | 修复：使用时间戳（getTime()）进行日期排序

### 参考资料

- https://www.algolia.com/doc/guides/managing-results/relevance-overview
- https://www.algolia.com/doc/guides/managing-results/must-do/custom-ranking

### 分面搜索与过滤

使用 refinement lists、range sliders 和 hierarchical menus 实现分面导航。

Widget 类型：
- RefinementList: 多选复选框
- Menu: 单选列表
- HierarchicalMenu: 嵌套分类
- RangeInput/RangeSlider: 数值范围
- ToggleRefinement: 布尔过滤器

### 代码示例

'use client';
import {
  InstantSearch,
  SearchBox,
  Hits,
  RefinementList,
  HierarchicalMenu,
  RangeInput,
  ToggleRefinement,
  ClearRefinements,
  CurrentRefinements,
  Stats,
  SortBy,
} from 'react-instantsearch';
import { searchClient, INDEX_NAME } from '@/lib/algolia';

export function ProductSearch() {
  return (
    <InstantSearch searchClient={searchClient} indexName={INDEX_NAME}>
      <div className="flex gap-8">
        {/* Filters Sidebar */}
        <aside className="w-64 space-y-6">
          <ClearRefinements />
          <CurrentRefinements />

          {/* Category hierarchy */}
          <div>
            <h3 className="font-semibold mb-2">Categories</h3>
            <HierarchicalMenu
              attributes={[
                'categories.lvl0',
                'categories.lvl1',
                'categories.lvl2',
              ]}
              limit={10}
              showMore
            />
          </div>

          {/* Brand filter */}
          <div>
            <h3 className="font-semibold mb-2">Brand</h3>
            <RefinementList
              attribute="brand"
              searchable
              searchablePlaceholder="Search brands..."
              showMore
              limit={5}
              showMoreLimit={20}
            />
          </div>

          {/* Price range */}
          <div>
            <h3 className="font-semibold mb-2">Price</h3>
            <RangeInput
              attribute="price"
              precision={0}
              classNames={{
                input: 'w-20 px-2 py-1 border rounded',
              }}
            />
          </div>

          {/* In stock toggle */}
          <ToggleRefinement
            attribute="inStock"
            label="In Stock Only"
            on={true}
          />

          {/* Rating filter */}
          <div>
            <h3 className="font-semibold mb-2">Rating</h3>
            <RefinementList
              attribute="rating"
              transformItems={(items) =>
                items.map((item) => ({
                  ...item,
                  label: '★'.repeat(Number(item.label)),
                }))
              }
            />
          </div>
        </aside>

        {/* Results */}
        <main className="flex-1">
          <div className="flex justify-between items-center mb-4">
            <SearchBox placeholder="Search products..." />
            <SortBy
              items={[
                { label: 'Relevance', value: 'products' },
                { label: 'Price (Low to High)', value: 'products_price_asc' },
                { label: 'Price (High to Low)', value: 'products_price_desc' },
                { label: 'Rating', value: 'products_rating_desc' },
              ]}
            />
          </div>
          <Stats />
          <Hits hitComponent={ProductHit} />
        </main>
      </div>
    </InstantSearch>
  );
}

// For sorting, create replica indices
// products_price_asc: customRanking: ['asc(price)']
// products_price_desc: customRanking: ['desc(price)']
// products_rating_desc: customRanking: ['desc(rating)']

### 反模式

- 模式：对非分面属性进行分面 | 原因：必须在设置中声明 attributesForFaceting | 修复：将属性添加到 attributesForFaceting 数组
- 模式：隐藏过滤器未使用 filterOnly() | 原因：在不展示的属性上浪费分面计算 | 修复：对不展示的过滤器使用 filterOnly(attribute)

### 参考资料

- https://www.algolia.com/doc/guides/managing-results/refine-results/faceting
- https://www.algolia.com/doc/api-reference/widgets/refinement-list/react

### 查询建议与自动补全

实现带查询建议和即时结果的自动补全。

使用 @algolia/autocomplete-js 实现独立自动补全，或
与 InstantSearch 的 SearchBox 集成。

查询建议需要 Algolia 生成的独立索引。

### 代码示例

// Standalone Autocomplete
// components/Autocomplete.tsx
'use client';
import { autocomplete, getAlgoliaResults } from '@algolia/autocomplete-js';
import algoliasearch from 'algoliasearch/lite';
import { useEffect, useRef } from 'react';
import '@algolia/autocomplete-theme-classic';

const searchClient = algoliasearch(
  process.env.NEXT_PUBLIC_ALGOLIA_APP_ID!,
  process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY!
);

export function Autocomplete() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const search = autocomplete({
      container: containerRef.current,
      placeholder: 'Search for products',
      openOnFocus: true,
      getSources({ query }) {
        if (!query) return [];

        return [
          // Query suggestions
          {
            sourceId: 'suggestions',
            getItems() {
              return getAlgoliaResults({
                searchClient,
                queries: [
                  {
                    indexName: 'products_query_suggestions',
                    query,
                    params: { hitsPerPage: 5 },
                  },
                ],
              });
            },
            templates: {
              header() {
                return 'Suggestions';
              },
              item({ item, html }) {
                return html`<span>${item.query}</span>`;
              },
            },
          },
          // Instant results
          {
            sourceId: 'products',
            getItems() {
              return getAlgoliaResults({
                searchClient,
                queries: [
                  {
                    indexName: 'products',
                    query,
                    params: { hitsPerPage: 8 },
                  },
                ],
              });
            },
            templates: {
              header() {
                return 'Products';
              },
              item({ item, html }) {
                return html`
                  <a href="/products/${item.objectID}">
                    <img src="${item.image}" alt="${item.name}" />
                    <span>${item.name}</span>
                    <span>$${item.price}</span>
                  </a>
                `;
              },
            },
            onSelect({ item, setQuery, refresh }) {
              // Navigate on selection
              window.location.href = `/products/${item.objectID}`;
            },
          },
        ];
      },
    });

    return () => search.destroy();
  }, []);

  return <div ref={containerRef} />;
}

// Combined with InstantSearch
import { connectSearchBox } from 'react-instantsearch';
import { autocomplete } from '@algolia/autocomplete-js';

// Or use built-in Autocomplete widget
import { Autocomplete as AlgoliaAutocomplete } from 'react-instantsearch';

export function SearchWithAutocomplete() {
  return (
    <InstantSearch searchClient={searchClient} indexName="products">
      <AlgoliaAutocomplete
        placeholder="Search products..."
        detachedMediaQuery="(max-width: 768px)"
      />
      <Hits hitComponent={ProductHit} />
    </InstantSearch>
  );
}

### 反模式

- 模式：创建自动补全时未做防抖 | 原因：每次按键都触发搜索，浪费操作次数 | 修复：Algolia autocomplete 自动处理防抖
- 模式：未使用查询建议索引 | 原因：缺失热门查询的搜索分析数据 | 修复：在 Algolia 控制台启用查询建议

### 参考资料

- https://www.algolia.com/doc/ui-libraries/autocomplete/introduction/what-is-autocomplete
- https://www.algolia.com/doc/guides/building-search-ui/ui-and-ux-patterns/query-suggestions/how-to/optimizing-query-suggestions-relevance/js

## 风险提示

### 前端代码中的 Admin API Key

严重程度：严重

### 索引速率限制与节流

严重程度：高

### 记录大小与索引限制

严重程度：中

### 索引名称中的 PII 在网络中可见

严重程度：中

### 可搜索属性顺序影响相关性

严重程度：中

### 全量重建消耗所有操作次数

严重程度：中

### 每次按键都计入搜索操作

严重程度：中

### InstantSearch SSR 水合不匹配

严重程度：中

### 排序副本索引成倍增加存储

严重程度：低

### 分面需要声明 attributesForFaceting

严重程度：中

## 验证检查

### 客户端代码中的 Admin API Key

严重程度：错误

Admin API key 绝不能暴露给客户端代码

消息：Admin API key 暴露给客户端。请使用 search-only key。

### 硬编码的 Algolia API Key

严重程度：错误

API key 应使用环境变量

消息：硬编码的 Algolia 凭证。请使用环境变量。

### 使用 Search Key 进行索引操作

严重程度：错误

索引操作需要 admin key，而非 search key

消息：使用 search key 进行索引。写入操作请使用 admin key。

### 循环中逐条索引记录

严重程度：警告

应批量处理记录以提高索引效率

消息：循环中逐条索引记录。请使用 saveObjects 批量索引。

### 使用 deleteBy 删除

严重程度：警告

deleteBy 开销大且有速率限制

消息：deleteBy 开销大。建议使用 deleteObjects 配合具体 ID。

### 频繁全量重建索引

严重程度：警告

全量重建对未变更数据浪费操作次数

消息：频繁全量重建。对未变更数据请考虑增量同步。

### 使用完整客户端而非 Lite

严重程度：提示

前端使用 lite 客户端可减小包体积

消息：导入了完整 Algolia 客户端。前端请使用 algoliasearch/lite。

### Next.js 中使用普通 InstantSearch

严重程度：警告

使用 react-instantsearch-nextjs 以支持 SSR

消息：使用普通 InstantSearch。Next.js SSR 请使用 InstantSearchNext。

### 缺少可搜索属性配置

严重程度：警告

配置 searchableAttributes 以提升相关性

消息：未配置 searchableAttributes。请设置属性优先级以提升相关性。

### 缺少自定义排序

严重程度：提示

自定义排序可提升业务相关性

消息：未配置 customRanking。请添加业务指标（popularity, rating）。

## 协作

### 委派触发条件

- 用户需要电商结账 -> stripe-integration（产品搜索后购买）
- 用户需要搜索分析 -> segment-cdp（追踪搜索查询和结果）
- 用户需要用户认证 -> clerk-auth（按用户生成安全 API key）
- 用户需要数据库设置 -> postgres-wizard（索引用源数据）
- 用户需要无服务器部署 -> aws-serverless（索引用 Lambda 任务）

## 使用时机
- 用户提及或暗示：添加搜索到
- 用户提及或暗示：algolia
- 用户提及或暗示：instantsearch
- 用户提及或暗示：search api
- 用户提及或暗示：search functionality
- 用户提及或暗示：typeahead
- 用户提及或暗示：autocomplete search
- 用户提及或暗示：faceted search
- 用户提及或暗示：search index
- 用户提及或暗示：search as you type

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 输出不能替代特定环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
