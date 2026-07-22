---
id: isr-revalidation-static-generation
title: ISR revalidation and static generation
status: active
candidateKinds: ["isr_overrevalidation"]
frameworks: ["next@>=13.4.0"]
priority: 95
citations: ["https://vercel.com/docs/incremental-static-regeneration", "https://nextjs.org/docs/app/api-reference/functions/revalidateTag", "https://nextjs.org/docs/app/api-reference/functions/revalidatePath"]
maxBriefChars: 1000
---

## 调查简报
对于 ISR 过度重新验证，目标是减少不必要的重新生成工作，而不会使内容过时超出产品的容忍度。

## 需要检查的证据
比较 ISR 写与读，然后检查路由的 `revalidate`、`cacheLife()`、标签失效和内容更新路径。在更新由事件驱动的路由上查找非常短的计时器重新验证。如果推荐对标记内容使用 `cacheLife()` 或 `cacheTag()`，证明确切的标签由 `revalidateTag()` 或 `updateTag()` 失效；近似匹配不算。

## 何时不建议
除非源证明陈旧读取是可接受的，否则不要为库存、定价、鉴权或其他用户关键的新鲜度延长重新验证。除非匹配的失效调用或配置在允许的文件中，否则不要声明现有的 CMS 或 webhook 失效。

## 验证
将修复与观察到的 ISR 每次读取的写入数以及控制重新验证或按需失效的行相关联。