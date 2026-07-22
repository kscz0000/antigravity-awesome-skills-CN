# changelog-updates

撰写开发者真正愿意阅读并关心的发布说明与产品更新。

## 本技能涵盖的内容

- **更新日志格式**：行之有效的结构与写作风格
- **应当包含的内容**：判断哪些内容值得记录
- **版本号沟通**：向用户解释语义化版本
- **破坏性变更**：降低阻力的公告方式
- **弃用通知**：优雅地下线功能
- **制造期待感**：把发布变成高光时刻

## 何时使用本技能

- 为新项目搭建更新日志
- 改进现有的发布沟通
- 规划破坏性变更的公告
- 优雅地弃用某个功能
- 为即将到来的发布制造期待

## 核心原则

发布说明是面向开发者的沟通，而非文档。写得好时，它们能建立信任、展示产品节奏，并将每次更新转化为营销契机。

## 好条目 vs 坏条目

**优秀：**
```markdown
### Fixed
- Fixed timeout errors when uploading files larger than 10MB.
  Uploads now stream in chunks, eliminating memory issues. (#234)
```

**糟糕：**
```markdown
### Fixed
- Fixed bug
```

## 速赢建议

1. 遵循 Keep a Changelog 格式
2. 每一条目都附上 Issue / PR 链接
3. 为破坏性变更解释"为什么"
4. 为弃用提供迁移指南
5. 对重要版本发送邮件摘要

## 相关技能

- `sdk-dx` - SDK 版本策略
- `docs-as-marketing` - 作为文档的更新日志
- `developer-community` - 在哪里分享更新
