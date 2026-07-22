---
id: auth-preserving-parallelization
title: Authorization-preserving parallelization
status: active
candidateKinds: ["slow_route"]
frameworks: ["*"]
priority: 90
citations: ["vercel-react-best-practices:async-parallel", "vercel-react-best-practices:server-parallel-fetching"]
maxBriefChars: 900
---

## 调查简报
仅当并行化不会将私有数据访问移到保护该数据的鉴权、所有权、租户或权限检查之前时，才是安全的。

## 需要检查的证据
列出每个被重新排序的 await 操作。如果私有查找当前在 `getSession()`、所有权查询、租户检查或重定向保护之后运行，证明查找本身在推荐 `Promise.all` 之前强制执行相同谓词。

## 何时不建议
不要将私有记录获取与授权该获取的所有权检查并行化。而是推荐将保护和查找组合成一个由已认证用户、租户或所有权键约束的查询。

## 验证
修复必须保留顺序保护或将其替换为单个已授权查询。除非已测量该辅助函数的时长，否则不要承诺等于辅助函数大小的延迟下降。