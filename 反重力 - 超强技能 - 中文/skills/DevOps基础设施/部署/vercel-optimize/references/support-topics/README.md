# 支持主题

支持主题是注入子代理简报中的小型、候选范围的调查护栏。

它们不是建议、闸门、扫描器或广泛的文档。主题告诉调查员为某一类候选检查哪些证据、要避免哪些误报，以及何时弃权。

## 添加主题

添加一个文件：`references/support-topics/<id>.md`。

文件名必须匹配 `id`。Frontmatter 使用 YAML 的严格子集：每行一个 `key: value`，数组为 JSON 数组。

```md
---
id: cdn-cache-auth-safety
title: CDN cache auth safety
status: active
candidateKinds: ["uncached_route", "cache_header_gap"]
frameworks: ["*"]
priority: 90
citations: ["https://vercel.com/docs/caching/cdn-cache"]
maxBriefChars: 900
---

## Investigation Brief
...

## Evidence To Check
...

## Do Not Recommend When
...

## Verification
...
```

## 规则

- 每个活动主题必须仅引用已存在于 `references/docs-library.json` 中的 URL 或技能规则引用。
- 使用 `candidateKinds` 保持主题范围窄。仅当工作流/协议主题真正适用于每个候选时才使用 `"*"`。
- 仅当主题适用于特定候选指标时使用可选 `metrics`，例如 `["LCP"]`、`["INP"]` 或 `["CLS"]` 用于 Core Web Vitals。
- 当主题应仅对特定候选路由出现时，使用可选 `routePatterns` 作为 JavaScript 正则源字符串，例如 `["(^|/)404$"]`。
- 保持正文低于 `maxBriefChars`；简报渲染器会在选定的主题到达子代理之前进行截断。
- 仅在 frontmatter 中放置 URL。主题正文应描述检查和护栏，而不是引用新来源。
- 不要包含内部仓库路径、服务名称、定价表、精确节省声明或没有版本门控的框架 API。