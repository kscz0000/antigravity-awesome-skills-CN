# 无头 CMS 指南

为营销内容选择、建模和实施无头 CMS 的参考资料。

## 何时使用本参考

在为新项目选择 CMS、设计营销站点的内容模型、设置编辑工作流，或将 CMS 内容连接到程序化页面时使用。

---

## 无头 CMS 与传统 CMS

无头 CMS 将内容管理与展示分离。内容存储在结构化后端，通过 API 投递给任何前端。

### 何时适合采用无头 CMS

- 多个前端消费相同内容（Web、移动端、邮件）
- 开发者希望完全控制前端技术栈
- 内容需要在不同渠道复用
- 正在使用现代框架构建（Next.js、Remix、Astro）
- 营销团队需要结构化、可复用的内容块

### 何时传统 CMS 更合适

- 小团队，没有专职开发者
- 简单的博客或宣传站
- WYSIWYG 编辑是硬性要求
- 预算紧张，WordPress/Webflow 就能胜任

### 决策清单

| 因素 | 无头 | 传统 |
|--------|----------|-------------|
| 多渠道投递 | 是 | 有限 |
| 开发者控制 | 完全 | 受限 |
| 非技术编辑 | 需要配置 | 内置 |
| 上线时间 | 更长 | 更快 |
| 内容复用 | 原生 | 手动 |
| 托管灵活性 | 任意前端 | 平台依赖 |

---

## 营销内容建模

### 核心原则

1. **按类型思考，而非按页面。** "落地页" 是一个带字段的内容类型——而非 HTML 文件。这让你能在页面间复用组件。
2. **内容与展示分离。** 存储标题文本，而非带样式的标题。展示属于前端的职责。
3. **为复用而设计。** 如果证言出现在 5 个页面上，创建一个 Testimonial 类型并引用它——不要复制。
4. **保持模型扁平。** 深层嵌套结构难以查询和维护。优先使用引用而非嵌套。

### 常见的营销内容类型

| 类型 | 关键字段 | 说明 |
|------|-----------|-------|
| **落地页（Landing Page）** | title, slug, hero, sections[], seo | 模块化 sections 以提高灵活性 |
| **博客文章（Blog Post）** | title, slug, body, author, category, tags, publishedAt, seo | 富文本或 Portable Text 正文 |
| **案例研究（Case Study）** | title, customer, challenge, solution, results, metrics[], logo | 关联到相关产品/功能 |
| **证言（Testimonial）** | quote, author, role, company, avatar, rating | 从落地页引用 |
| **FAQ** | question, answer, category | 按 category 分组以支持程序化页面 |
| **作者（Author）** | name, bio, avatar, social links | 从博客文章引用 |
| **CTA 块（CTA Block）** | heading, body, buttonText, buttonUrl, variant | 跨页面复用 |

### SEO 字段清单

每个页面级内容类型都需要：

- `metaTitle` — 50-60 字符
- `metaDescription` — 150-160 字符
- `ogImage` — 1200x630 像素的社交预览图
- `slug` — URL 路径段
- `canonicalUrl` — 可选覆盖
- `noIndex` — 布尔值，用于从搜索中排除
- `structuredData` — 可选 JSON-LD 覆盖

---

## 编辑工作流

### 草稿 → 审阅 → 发布 循环

1. **草稿（Draft）** — 作者创建或编辑内容
2. **审阅（Review）** — 编辑检查准确性、品牌语调、SEO
3. **批准（Approve）** — 利益相关者签字
4. **排期（Schedule）** — 设置发布日期/时间
5. **发布（Publish）** — 内容通过 API 上线

### 预览 API

所有主流无头 CMS 平台都支持草稿预览：

- **Sanity**：使用 `useLiveQuery` 或 Presentation 工具的实时预览
- **Contentful**：预览 API（`preview.contentful.com`），使用单独的访问令牌
- **Strapi**：Draft & Publish 系统，使用 `status=draft` 查询参数（v5；取代 v4 的 `publicationState`）

在前端设置一个预览路由（例如 `/api/preview`），用于鉴权并渲染草稿内容。

### 角色与权限

| 角色 | 可创建 | 可编辑 | 可发布 | 可删除 |
|------|:----------:|:--------:|:-----------:|:----------:|
| 作者（Author） | 是 | 自己的 | 否 | 自己的草稿 |
| 编辑（Editor） | 是 | 全部 | 是 | 草稿 |
| 管理员（Admin） | 是 | 全部 | 是 | 全部 |

具体权限模型因平台而异。Sanity 使用基于角色的访问控制。Contentful 拥有空间级角色。Strapi 提供细粒度 RBAC。

---

## 平台对比

| 特性 | Sanity | Contentful | Strapi |
|---------|--------|------------|--------|
| 托管 | 云（托管） | 云（托管） | 自托管或云 |
| 查询语言 | GROQ | REST / GraphQL | REST / GraphQL |
| 免费层 | 慷慨 | 有限 | 开源（免费） |
| 实时协作 | 是（内置） | 有限 | 否 |
| 最适合 | 开发者灵活性 | 企业多语言区域 | 预算/自托管 |
| 内容建模 | Schema-as-code | Web UI | Web UI 或代码 |
| 媒体处理 | 内置 DAM | 内置 | 插件化 |

### Sanity

**优势**：GROQ 查询语言强大而灵活。Schema 以代码定义（可版本控制）。实时协作编辑。Portable Text 用于富内容。慷慨的免费层。

**注意事项**：对非开发者学习曲线较陡。Studio 定制需要 React 知识。GROQ 查询存在供应商锁定。

**营销适配度**：最适合开发者和营销人员紧密协作。非常适合内容密集型站点和复杂模型。

### Contentful

**优势**：成熟的企业级平台。出色的多语言区域支持。强大的集成生态。通过 Studio 实现可组合内容。文档完善的 API。

**注意事项**：定价随内容类型和语言区域扩展。两套独立的 API（Delivery 和 Management）。低阶套餐的速率限制可能较紧。

**营销适配度**：最适合具有多市场内容需求的企业。当需要可靠的成熟供应商时表现良好。

### Strapi

**优势**：开源、可自托管。完全的数据控制。无按席位计费。可定制的管理面板。插件生态。默认 REST，通过插件支持 GraphQL。

**注意事项**：自托管意味着需要自行处理基础设施。生态规模小于 Sanity/Contentful。从 V4 迁移到 V5 可能改动较大。

**营销适配度**：最适合具备 DevOps 能力、希望完全控制且无供应商锁定的团队。适合预算敏感的项目。

### 其他值得关注

- **Hygraph** — 原生 GraphQL，在联邦和多源内容方面表现强劲
- **Keystatic** — 基于 Git，适合开发者与内容编辑混合工作流
- **Payload** — TypeScript 优先，自托管，配置方式类似 Sanity
- **Builder.io** — 可视化编辑器搭配无头后端，适合非技术营销人员
- **Prismic** — 基于 Slice 的内容建模，Next.js 集成强劲

---

## 与营销技能的集成

### 程序化 SEO

将 CMS 用作程序化页面的数据源。将结构化数据（FAQ、对比、城市页面）存储为内容类型，并通过查询生成页面。参见 **programmatic-seo** 技能。

### 文案撰写

CMS 内容模型强制一致的结构。定义的字段应匹配你的文案框架（标题、副标题、社会证明、CTA）。参见 **copywriting** 技能。

### 站点架构

URL 结构、导航层级和内链都取决于内容在 CMS 中的组织方式。内容模型和站点架构应一起规划。参见 **site-architecture** 技能。

### 邮件序列

将 CMS 内容拉入邮件模板，在 Web 和邮件之间保持统一信息。案例研究、证言和博客文章可为邮件培育序列提供素材。参见 **email-sequence** 技能。

---

## 实施清单

- [ ] 基于页面类型和可复用块定义内容类型
- [ ] 为每个页面级内容类型添加 SEO 字段
- [ ] 在前端设置预览/草稿模式
- [ ] 为团队配置角色与权限
- [ ] 在构建前端前为每种类型创建示例内容
- [ ] 设置 webhook 通知以响应内容变更（触发重建）
- [ ] 为编辑撰写内容指南文档（字段说明、字符限制）
- [ ] 测试内容投递性能（CDN、缓存、ISR）
- [ ] 如果从现有 CMS 迁移，规划迁移策略

---

## 相关集成指南

- [Sanity](../../../tools/integrations/sanity.md) — GROQ 查询、变更、CLI
- [Contentful](../../../tools/integrations/contentful.md) — Delivery/Management API、发布
- [Strapi](../../../tools/integrations/strapi.md) — REST CRUD、过滤器、Document API
