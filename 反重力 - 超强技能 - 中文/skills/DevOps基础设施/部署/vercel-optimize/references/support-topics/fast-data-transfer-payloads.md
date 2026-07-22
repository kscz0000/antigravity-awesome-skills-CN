---
id: fast-data-transfer-payloads
title: Fast Data Transfer payloads
status: active
candidateKinds: ["uncached_route"]
frameworks: ["*"]
priority: 65
citations: ["https://vercel.com/docs/manage-cdn-usage", "https://vercel.com/docs/caching/cdn-cache"]
maxBriefChars: 900
---

## 调查简报
当未缓存的路由承载高带宽时，在仅推荐缓存头之前检查有效负载形状。Fast Data Transfer 包括请求和响应传输的字节；将压缩后响应大小与信号进行比较，而不是原始 JSON。

## 需要检查的证据
使用 `bandwidthByCache`、响应大小和源序列化。查找无界 JSON、大型嵌入对象、通过函数的静态文件、缺少分页。

## 何时不建议
不要在未识别该路由响应不需要的字段或资产的情况下缩小有效负载。

## 验证
将发现与观察到的字节、缓存结果混合以及确切响应行相关联。"大型有效负载"声明必须反映压缩后的字节——FDT 计量的单位。