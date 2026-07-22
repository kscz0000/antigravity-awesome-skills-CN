---
id: build-minutes-monorepo-fanout
title: Build Minutes monorepo fanout
status: active
candidateKinds: ["build_minutes_fanout"]
frameworks: ["*"]
scannerPatterns: ["turbo-force-bypass"]
priority: 90
citations: ["https://vercel.com/docs/monorepos", "https://vercel.com/docs/builds", "https://turborepo.dev/docs/crafting-your-repository/caching"]
maxBriefChars: 900
---

## 调查简报
当提交重建未变化的工作时，Build Minutes 攀升。常见原因：`TURBO_FORCE`、`cache: false`、缺少 outputs 或禁用的 build-skip 设置。

## 需要检查的证据
确认 Build Minutes 份额和扫描器子类型。检查 `package.json`、`turbo.json`、outputs、`.gitignore`、`vercel.json` 和项目设置。如果 `build` 运行迁移，请在推荐 Turbo 构建缓存之前将它们拆分为未缓存的步骤。

## 何时不建议
在没有扫描器发现的情况下，账单份额低于 5% 时跳过。跳过单项目仓库和有意的 CI 强制标志。不要仅根据仓库 grep 推荐 `ignoreCommand`；仅仪表板的 skip-unaffected 可能更好。

## 验证
命名违规的文件和模式。仅推荐经过验证的修复：缓存纯构建任务、添加生成的 `outputs`、启用 skip-unaffected 构建，或仅在需要时添加 `ignoreCommand`。