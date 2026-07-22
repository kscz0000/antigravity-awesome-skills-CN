---
name: performance-optimization
description: 应用性能优化技能。当存在性能需求、怀疑性能回归、或 Core Web Vitals 与加载时间需要改进时使用。当性能分析揭示需要修复的瓶颈时使用。触发词：性能优化、性能调优、页面加载优化、Core Web Vitals、Lighthouse、前端性能、后端性能、bundle 优化、N+1 查询、图片优化、缓存策略、性能预算、性能监控、LCP、INP、CLS、TTFB、代码分割、懒加载、React.memo、useMemo、性能瓶颈、性能回归检测、RUM、APM
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/performance-optimization
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# 性能优化

## 概述

优化前先测量。没有测量依据的性能工作就是在猜测——而猜测会导致过早优化，增加复杂性却不能改善关键问题。先分析性能，找出真正的瓶颈，修复它，再次测量。只优化经测量证明确实重要的部分。

## 使用时机

- 规格中存在性能要求（加载时间预算、响应时间 SLA）
- 用户或监控系统报告运行缓慢
- Core Web Vitals 分数低于阈值
- 你怀疑某次变更引入了回归问题
- 正在构建处理大数据集或高流量的功能

**何时不使用：** 在没有问题证据之前不要进行优化。过早优化会增加复杂性，其成本往往超过获得的性能收益。

## Core Web Vitals 目标值

| 指标 | 良好 | 需要改善 | 较差 |
|--------|------|-------------------|------|
| **LCP**（最大内容绘制） | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| **INP**（交互到下次绘制） | ≤ 200ms | ≤ 500ms | > 500ms |
| **CLS**（累积布局偏移） | ≤ 0.1 | ≤ 0.25 | > 0.25 |

## 优化工作流

```
1. 测量    → 用真实数据建立基线
2. 识别    → 找出真正的瓶颈（而非假设）
3. 修复    → 针对性解决具体瓶颈
4. 验证    → 再次测量，确认改善
5. 守卫    → 添加监控或测试防止回归
```

### 步骤 1：测量

两种互补的方法——结合使用：

- **合成监测（Lighthouse、DevTools Performance 标签页）：** 受控条件，可复现。最适合 CI 回归检测和隔离特定问题。
- **真实用户监控 RUM（web-vitals 库、CrUX）：** 真实条件下的真实用户数据。用于验证修复是否真正改善了用户体验。

**前端：**
```bash
# 合成监测：Chrome DevTools 中的 Lighthouse（或 CI）
# Chrome DevTools → Performance 标签页 → Record
# Chrome DevTools MCP → Performance trace

# 真实用户监控：代码中的 Web Vitals 库
import { onLCP, onINP, onCLS } from 'web-vitals';

onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

**后端：**
```bash
# 响应时间日志记录
# 应用性能监控（APM）
# 带计时功能的数据库查询日志记录

# 简单计时
console.time('db-query');
const result = await db.query(...);
console.timeEnd('db-query');
```

### 从哪里开始测量

根据症状决定首先测量什么：

```
什么慢了？
├── 首页加载
│   ├── 包体积过大？ --> 测量包大小，检查代码分割
│   ├── 服务端响应慢？ --> 在 DevTools Network 瀑布图中测量 TTFB
│   │   ├── DNS 慢？ --> 为已知来源添加 dns-prefetch / preconnect
│   │   ├── TCP/TLS 慢？ --> 启用 HTTP/2，检查边缘部署，keep-alive
│   │   └── 等待（服务端）时间长？ --> 分析后端性能，检查查询和缓存
│   └── 渲染阻塞资源？ --> 在网络瀑布图中检查 CSS/JS 阻塞情况
├── 交互感觉卡顿
│   ├── 点击时 UI 冻结？ --> 分析主线程，查找长任务（>50ms）
│   ├── 表单输入延迟？ --> 检查重复渲染，受控组件开销
│   └── 动画掉帧？ --> 检查布局抖动，强制回流
├── 导航后的页面
│   ├── 数据加载？ --> 测量 API 响应时间，检查瀑布请求
│   └── 客户端渲染？ --> 分析组件渲染时间，检查 N+1 请求
└── 后端 / API
    ├── 单个接口慢？ --> 分析数据库查询，检查索引
    ├── 所有接口都慢？ --> 检查连接池、内存、CPU
    └── 间歇性缓慢？ --> 检查锁竞争、GC 暂停、外部依赖
```

### 步骤 2：识别瓶颈

按类别划分的常见瓶颈：

**前端：**

| 症状 | 可能原因 | 排查方向 |
|---------|-------------|---------------|
| LCP 慢 | 图片过大、渲染阻塞资源、服务器响应慢 | 检查网络瀑布图、图片尺寸 |
| CLS 高 | 缺少尺寸属性的图片、延迟加载的内容、字体偏移 | 检查布局偏移归因 |
| INP 差 | 主线程上的重度 JavaScript、大量 DOM 更新 | 在 Performance trace 中检查长任务 |
| 初始加载慢 | 包过大、过多网络请求 | 检查包大小、代码分割 |

**后端：**

| 症状 | 可能原因 | 排查方向 |
|---------|-------------|---------------|
| API 响应慢 | N+1 查询、缺少索引、未优化的查询 | 检查数据库查询日志 |
| 内存增长 | 引用泄漏、无界缓存、大负载 | 堆快照分析 |
| CPU 飙高 | 同步重计算、正则回溯 | CPU 性能分析 |
| 延迟高 | 缺少缓存、冗余计算、网络跳转 | 全链路追踪请求 |

### 步骤 3：修复常见反模式

#### N+1 查询（后端）

```typescript
// 不好：N+1 — 为每个任务的 owner 各执行一次查询
const tasks = await db.tasks.findMany();
for (const task of tasks) {
  task.owner = await db.users.findUnique({ where: { id: task.ownerId } });
}

// 好：使用 join/include 的单次查询
const tasks = await db.tasks.findMany({
  include: { owner: true },
});
```

#### 无界数据获取

```typescript
// 不好：获取所有记录
const allTasks = await db.tasks.findMany();

// 好：带限制的分页查询
const tasks = await db.tasks.findMany({
  take: 20,
  skip: (page - 1) * 20,
  orderBy: { createdAt: 'desc' },
});
```

#### 图片未优化（前端）

```html
<!-- 不好：没有尺寸属性，没有格式优化 -->
<img src="/hero.jpg" />

<!-- 好：首屏/LCP 图片 — 自适应方向 + 分辨率切换，高优先级 -->
<!--
  两种技术组合：
  - 自适应方向（media）：按断点提供不同裁剪/构图
  - 分辨率切换（srcset + sizes）：按屏幕密度提供合适文件大小
-->
<picture>
  <!-- 移动端：竖版裁剪（8:10） -->
  <source
    media="(max-width: 767px)"
    srcset="/hero-mobile-400.avif 400w, /hero-mobile-800.avif 800w"
    sizes="100vw"
    width="800"
    height="1000"
    type="image/avif"
  />
  <source
    media="(max-width: 767px)"
    srcset="/hero-mobile-400.webp 400w, /hero-mobile-800.webp 800w"
    sizes="100vw"
    width="800"
    height="1000"
    type="image/webp"
  />
  <!-- 桌面端：横版裁剪（2:1） -->
  <source
    srcset="/hero-800.avif 800w, /hero-1200.avif 1200w, /hero-1600.avif 1600w"
    sizes="(max-width: 1200px) 100vw, 1200px"
    width="1200"
    height="600"
    type="image/avif"
  />
  <source
    srcset="/hero-800.webp 800w, /hero-1200.webp 1200w, /hero-1600.webp 1600w"
    sizes="(max-width: 1200px) 100vw, 1200px"
    width="1200"
    height="600"
    type="image/webp"
  />
  <img
    src="/hero-desktop.jpg"
    width="1200"
    height="600"
    fetchpriority="high"
    alt="Hero image description"
  />
</picture>

<!-- 好：折叠屏以下图片 — 懒加载 + 异步解码 -->
<img
  src="/content.webp"
  width="800"
  height="400"
  loading="lazy"
  decoding="async"
  alt="Content image description"
/>
```

#### 不必要的重复渲染（React）

```tsx
// 不好：每次渲染创建新对象，导致子组件重复渲染
function TaskList() {
  return <TaskFilters options={{ sortBy: 'date', order: 'desc' }} />;
}

// 好：稳定引用
const DEFAULT_OPTIONS = { sortBy: 'date', order: 'desc' } as const;
function TaskList() {
  return <TaskFilters options={DEFAULT_OPTIONS} />;
}

// 对昂贵组件使用 React.memo
const TaskItem = React.memo(function TaskItem({ task }: Props) {
  return <div>{/* expensive render */}</div>;
});

// 对昂贵计算使用 useMemo
function TaskStats({ tasks }: Props) {
  const stats = useMemo(() => calculateStats(tasks), [tasks]);
  return <div>{stats.completed} / {stats.total}</div>;
}
```

#### 包体积过大

```typescript
// 现代打包工具（Vite、webpack 5+）自动处理具名导入的 tree-shaking，
// 前提是依赖项发布 ESM 并在 package.json 中标记 `sideEffects: false`。
// 修改导入方式前先分析——真正的收益来自分割和懒加载。

// 好：对重量级、少用的功能使用动态导入
const ChartLibrary = lazy(() => import('./ChartLibrary'));

// 好：路由级代码分割，配合 Suspense
const SettingsPage = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <SettingsPage />
    </Suspense>
  );
}
```

#### 缺少缓存（后端）

```typescript
// 缓存频繁读取、很少变化的数据
const CACHE_TTL = 5 * 60 * 1000; // 5 分钟
let cachedConfig: AppConfig | null = null;
let cacheExpiry = 0;

async function getAppConfig(): Promise<AppConfig> {
  if (cachedConfig && Date.now() < cacheExpiry) {
    return cachedConfig;
  }
  cachedConfig = await db.config.findFirst();
  cacheExpiry = Date.now() + CACHE_TTL;
  return cachedConfig;
}

// 静态资源的 HTTP 缓存头
app.use('/static', express.static('public', {
  maxAge: '1y',           // 缓存 1 年
  immutable: true,        // 永不重新验证（文件名中使用内容哈希）
}));

// API 响应的 Cache-Control
res.set('Cache-Control', 'public, max-age=300'); // 5 分钟
```

## 性能预算

设定预算并执行落地：

```
JavaScript 包大小：< 200KB gzipped（初始加载）
CSS：< 50KB gzipped
图片：每张 < 200KB（首屏区域）
字体：总计 < 100KB
API 响应时间：< 200ms（p95）
可交互时间：< 3.5s（4G 网络）
Lighthouse 性能分：≥ 90
```

**在 CI 中强制执行：**
```bash
# 包大小检查
npx bundlesize --config bundlesize.config.json

# Lighthouse CI
npx lhci autorun
```

## 参考资源

详细的性能检查清单、优化命令和反模式参考，参见 `references/performance-checklist.md`。

## 常见借口 vs 现实

| 借口 | 现实 |
|---|---|
| "以后再优化" | 性能债务会不断累积。现在就修复明显的反模式，微优化可以延后。 |
| "在我机器上挺快的" | 你的机器不是用户的机器。在具有代表性的硬件和网络环境下分析。 |
| "这个优化很明显" | 如果没测量过，你并不了解。先分析再动手。 |
| "用户不会注意到 100ms" | 研究表明 100ms 的延迟会影响转化率。用户的感知比你想象的更敏锐。 |
| "框架会处理性能" | 框架能预防部分问题，但无法解决 N+1 查询或包体积过大的问题。 |

## 危险信号

- 没有分析数据支撑的优化行为
- 数据获取中存在 N+1 查询模式
- 列表接口缺少分页
- 图片缺少尺寸属性、懒加载或响应式尺寸
- 包体积未经审查地持续增长
- 生产环境没有任何性能监控
- 到处使用 `React.memo` 和 `useMemo`（过度使用和不用一样有害）

## 验证清单

任何与性能相关的变更后：

- [ ] 存在变更前后的测量数据（具体数值）
- [ ] 已识别并解决了具体的瓶颈
- [ ] Core Web Vitals 处于"良好"阈值范围内
- [ ] 包大小没有显著增加
- [ ] 新的数据获取代码中没有 N+1 查询
- [ ] 性能预算在 CI 中通过（如已配置）
- [ ] 现有测试仍然通过（优化未破坏已有行为）

## 局限性

- 仅当任务明确匹配上游来源和本地项目上下文时才使用此技能。
- 应用变更前，请验证命令、生成的代码、依赖项、凭证以及外部服务的行为。
- 不要将示例替代为针对特定环境的测试、安全审查，或对破坏性或高成本操作的用户审批。
