---
id: sveltekit-isr-prerender-safety
title: SvelteKit ISR and prerender safety
status: active
candidateKinds: ["uncached_route", "isr_overrevalidation"]
frameworks: ["sveltekit@*"]
priority: 90
citations: ["https://vercel.com/docs/frameworks/full-stack/sveltekit", "https://svelte.dev/docs/kit/adapter-vercel", "https://svelte.dev/docs/kit/page-options"]
maxBriefChars: 850
---

## 调查简报
对于 SvelteKit，正确的杠杆通常是公共消费者页面上的 `prerender` 或 adapter ISR。首先证明每个访问者可以安全地在配置的时间间隔内看到相同的响应。

## 需要检查的证据
检查 `+page`、`+page.server`、`+server`、布局、`prerender`、`ssr` 和 adapter `isr` 配置。比较路由缓存结果、ISR 写入以及路由是否读取 cookies、鉴权或每用户本地变量。

## 何时不建议
不要对仪表板、购物车、结账、账户数据、草稿或任何输出因访问者而异的路由使用 ISR。当 `prerender = true` 已经使其无关紧要时，不要添加 ISR。

## 验证
命名路由、当前 SvelteKit 页面选项或 adapter 配置、观察到的缓存或 ISR 信号以及要更改的确切文件行。