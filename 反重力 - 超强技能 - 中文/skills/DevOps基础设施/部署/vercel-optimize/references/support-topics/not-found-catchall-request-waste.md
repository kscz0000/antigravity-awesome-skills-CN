---
id: not-found-catchall-request-waste
title: Not-found and catch-all request waste
status: active
candidateKinds: ["uncached_route"]
frameworks: ["*"]
routePatterns: ["(^|/)404$", "not-found", "\\[\\.\\.\\.]"]
priority: 92
citations: ["https://vercel.com/docs/routing/", "https://vercel.com/docs/redirects/bulk-redirects/", "https://vercel.com/docs/vercel-firewall/vercel-waf/custom-rules", "https://vercel.com/docs/vercel-firewall/vercel-waf/managed-rulesets"]
maxBriefChars: 850
---

## 调查简报
大量的 404 或 catch-all 流量通常是请求浪费。首先确定流量是旧 URL、bot、损坏链接还是真实的产品路由。

## 需要检查的证据
使用路由量、方法份额、缓存结果、bot 份额和热门请求路径。检查重写、catch-all 路由、sitemap/robots 输出以及任何已记录或阻止该模式的 WAF 规则。

## 何时不建议
不要在没有 log 模式验证路径的情况下阻止或重定向合法的产品路由、搜索爬虫或未知流量。不要用包罗万象的重写替换有用的 404 页面。

## 验证
命名主要的错误路径模式、观察到的请求或 bot 量以及将停止浪费函数路径的重定向、路由或 WAF 规则。