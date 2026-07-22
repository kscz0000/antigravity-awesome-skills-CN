---
name: fixing-metadata
description: >
  审计并修复 HTML 元数据，包括页面标题、meta 描述、canonical URL、Open Graph 标签、Twitter 卡片、favicon、JSON-LD 结构化数据以及 robots 指令。当添加或审查 SEO 与社交元数据时使用。触发词：元数据、SEO、Open Graph、Twitter 卡片、canonical、favicon、JSON-LD、robots。
risk: safe
source: community
version: 1.0.1
license: MIT
---

## 工作流

1. 识别元数据缺失或不正确的页面（标题、描述、canonical、OG 标签）
2. 按下方优先级规则审计——先修复严重问题（重复、索引）
3. 确保 title、description、canonical 和 og:url 彼此一致
4. 在真实 URL（而非 localhost）上验证社交卡片渲染正确
5. 保持 diff 最小且范围限于元数据——不要重构无关代码

## 何时使用

在以下情况参考这些指南：
- 添加或修改页面标题、描述、canonical、robots
- 实现 Open Graph 或 Twitter 卡片元数据
- 设置 favicon、应用图标、manifest、theme-color
- 构建共享 SEO 组件或布局元数据默认值
- 添加结构化数据（JSON-LD）
- 更改语言区域、备用语言或 canonical 路由
- 发布新页面、营销页面或可分享链接

## 规则类别（按优先级）

| 优先级 | 类别 | 影响 |
|:------:|------|:----:|
| 1 | 正确性与重复 | 严重 |
| 2 | 标题与描述 | 高 |
| 3 | canonical 与索引 | 高 |
| 4 | 社交卡片 | 高 |
| 5 | 图标与 manifest | 中 |
| 6 | 结构化数据 | 中 |
| 7 | 语言区域与备用 | 低-中 |
| 8 | 工具边界 | 严重 |

## 速查

### 1. 正确性与重复（严重）

- 每页在一处定义元数据，避免竞争系统
- 不输出重复的 title、description、canonical 或 robots 标签
- 元数据必须确定，无随机或不稳定值
- 对任何用户生成或动态字符串进行转义和清理
- 每页必须有 title 和 description 的安全默认值

### 2. 标题与描述（高）

- 每页必须有标题
- 跨站点使用一致的标题格式
- 标题保持简短可读，避免堆砌
- 可分享或可搜索的页面应具有 meta description
- 描述必须为纯文本，无 markdown 或引用刷屏

### 3. canonical 与索引（高）

- canonical 必须指向页面的首选 URL
- 仅对私有、重复或非公开页面使用 noindex
- robots meta 必须与实际访问意图匹配
- 预览或暂存页面在可能时应默认 noindex
- 分页页面必须具有正确的 canonical 行为

### 4. 社交卡片（高）

- 可分享页面必须设置 Open Graph 标题、描述和图片
- Open Graph 和 Twitter 图片必须使用绝对 URL
- 偏好正确的图片尺寸和稳定的长宽比
- og:url 必须匹配 canonical URL
- 使用合理的 og:type，通常是 website 或 article
- 适当设置 twitter:card，默认 summary_large_image

### 5. 图标与 manifest（中）

- 至少包含一个跨浏览器可用的 favicon
- 适当时包含 apple-touch-icon
- manifest 在使用时必须有效且被引用
- 有意设置 theme-color 避免 UI chrome 不匹配
- 图标路径应稳定且可缓存

### 6. 结构化数据（中）

- 除非清晰映射到真实页面内容，否则不要添加 JSON-LD
- JSON-LD 必须有效并反映实际渲染内容
- 不要编造评分、评论、价格或组织详情
- 每页优选一个结构化数据块，除非必需

### 7. 语言区域与备用（低-中）

- 正确设置 html lang 属性
- 存在本地化时设置 og:locale
- 仅在页面真实存在时添加 hreflang 备用
- 本地化页面必须按语言区域正确 canonicalize

### 8. 工具边界（严重）

- 偏好最小改动，不要重构无关代码
- 除非被请求，否则不要迁移框架或 SEO 库
- 遵循项目现有元数据模式（Next.js metadata API、react-helmet、手动 head 等）

## 审查指导

- 优先修复严重问题（重复、canonical、索引）
- 确保 title、description、canonical 和 og:url 一致
- 在真实 URL（而非 localhost）上验证社交卡片
- 偏好稳定、朴实的元数据，而非聪明或动态的
- 保持 diff 最小且范围限于元数据

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
