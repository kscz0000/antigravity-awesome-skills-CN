---
id: next-route-handler-get-cache-defaults
title: Next.js Route Handler GET cache defaults
status: active
candidateKinds: ["uncached_route", "cache_header_gap"]
frameworks: ["next@>=15.0.0"]
priority: 91
citations: ["https://nextjs.org/docs/app/api-reference/file-conventions/route", "https://vercel.com/docs/caching/cdn-cache"]
maxBriefChars: 850
---

## 调查简报
在 Next.js 15+ 上，GET 路由处理器默认是动态的。对于热门的公共 GET 处理器，在推荐缓存头或路由配置之前验证未缓存行为是否是有意的。

## 需要检查的证据
使用方法份额、缓存结果和源。检查 `GET`、`revalidate`、`dynamic`、请求头、cookies、鉴权、查询参数以及响应 `Cache-Control`。

## 何时不建议
不要缓存 POST 风格的处理器、webhook、每用户 API、流式响应、具有用户特定参数的搜索请求或读取鉴权/cookies 的处理器。

## 验证
命名 Next.js 版本、GET 份额、缓存结果混合以及使公共缓存安全的确切处理器或头行。