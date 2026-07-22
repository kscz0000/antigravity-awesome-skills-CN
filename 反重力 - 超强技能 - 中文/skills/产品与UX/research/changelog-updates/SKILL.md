---
name: changelog-updates
description: '撰写开发者真正愿意阅读并关心的发布说明与产品更新。本技能涵盖更新日志格式、版本号沟通、重大变更公告、弃用通知，以及为新功能造势。触发词：更新日志、changelog、发布说明、release notes、产品更新、product updates、版本号、versioning、重大变更、breaking change、弃用、deprecation、发布动态、发布节奏、release cadence。'
risk: unknown
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates
source_repo: jonathimer/devmarketing-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/jonathimer/devmarketing-skills/blob/main/LICENSE
---

# 开发者真正关心的更新日志与产品动态
## 适用场景

当你需要撰写开发者真正愿意阅读并关心的发布说明与产品更新时使用本技能。本技能涵盖更新日志格式、版本号沟通、重大变更公告、弃用通知，以及为新功能造势。触发词：更新日志、changelog、发布说明、release notes、产品更新、product updates、版本号、versioning、重大变更、breaking change、弃用、deprecation、发布动态、发布节奏、release cadence。


发布说明是面向开发者的沟通，而非文档。写得好时，它们能建立信任、展示产品节奏，并将每次更新转化为营销契机。

## 概述

更新日志服务于多种受众并承担不同目的：
- **活跃开发者**："有哪些变更会影响我的集成？"
- **评估期的开发者**："这个产品还在积极维护吗？"
- **开发者布道者**："哪些内容值得分享给我的受众？"
- **你的团队**：历史上线内容与上线时间的记录

本技能帮助你撰写能够传递信息、建立信任，并偶尔让人眼前一亮的更新日志。

## 开始之前

请先查阅 **developer-audience-context** 技能以了解：
- 你的开发者更倾向通过什么渠道接收更新？
- 他们最关心哪些类型的变更？
- 他们需要多详细的说明？
- 他们对破坏性变更的容忍度如何？

你的更新日志语气与详略程度应与受众匹配。

## 更新日志格式

### 标准结构

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]
### Added
- New feature in development

## [2.3.0] - 2024-01-15
### Added
- New `analyze()` method for sentiment analysis
- Support for batch processing up to 100 items

### Changed
- Improved error messages with troubleshooting links
- Default timeout increased from 30s to 60s

### Deprecated
- `old_analyze()` will be removed in v3.0.0

### Fixed
- Race condition in concurrent requests (#234)
- Memory leak when processing large files (#256)

## [2.2.1] - 2024-01-08
### Fixed
- Critical security patch for authentication bypass

## [2.2.0] - 2024-01-01
...
```

### 变更分类

| 分类 | 用途 |
|----------|---------|
| **Added（新增）** | 新功能、新接口、新参数 |
| **Changed（变更）** | 行为变更、性能改进 |
| **Deprecated（弃用）** | 即将下线的功能（暂时仍可用） |
| **Removed（移除）** | 已不再存在的功能 |
| **Fixed（修复）** | Bug 修复 |
| **Security（安全）** | 与安全相关的变更 |

### 好条目 vs 坏条目

**优秀的更新日志条目：**
```markdown
### Added
- New `batch_analyze()` method processes up to 100 items in a single
  request, reducing API calls by 90% for bulk operations.
  [See docs](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link) (#198)

### Fixed
- Fixed timeout errors when processing files larger than 10MB.
  Uploads now stream in chunks, eliminating memory issues. (#234)

### Deprecated
- `legacy_auth()` will be removed in v3.0.0 (scheduled for March 2024).
  Migrate to `oauth_auth()` using our [migration guide](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link).
```

**糟糕的更新日志条目：**
```markdown
### Added
- New feature

### Fixed
- Fixed bug
- Fixed another bug
- Various improvements

### Changed
- Updated dependencies
```

### 写作风格

**写得具体：**
```
❌ "Improved performance"
✅ "Reduced API response time by 40% for list operations"
```

**提供上下文：**
```
❌ "Fixed issue #234"
✅ "Fixed timeout errors when uploading large files (#234)"
```

**附带资源链接：**
```
✅ "New batch API - [documentation](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link) | [migration guide](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)"
```

**说明影响：**
```
✅ "Breaking: `user_id` parameter renamed to `id`.
    Update your code before upgrading."
```

## 应当包含的内容

### 必须包含

**API 变更：**
- 新接口
- 新参数
- 响应格式变更
- 错误码变更

**SDK 变更：**
- 新方法
- 方法签名变更
- 新增配置项

**破坏性变更：**
- 任何需要修改代码的事项
- 已移除的功能
- 默认值变更

**安全修复：**
- 即使细节模糊，也应公开承认安全更新
- 遵循负责任披露的时间表

### 建议包含

**性能改进：**
```markdown
### Changed
- List operations now 3x faster through pagination optimization
```

**开发者体验：**
```markdown
### Added
- Error messages now include troubleshooting links
- SDK now validates API keys at initialization
```

**基础设施：**
```markdown
### Changed
- New data center in EU (eu-west.api.example.com)
- Increased rate limits from 100 to 500 requests/minute
```

### 可以省略或淡化

**内部重构：**
```markdown
❌ "Refactored authentication module"
（除非确实影响开发者）
```

**琐碎的依赖升级：**
```markdown
❌ "Updated lodash from 4.17.20 to 4.17.21"
（除非与安全相关）
```

**拼写修正：**
```markdown
❌ "Fixed typo in error message"
（合并为"Various documentation improvements"即可）
```

## 版本号沟通

### 向用户解释语义化版本

帮助开发者理解版本号的含义：

```markdown
# Versioning

We follow [Semantic Versioning](https://semver.org/):

- **Major versions (3.0.0)**: May include breaking changes.
  Check the migration guide before upgrading.

- **Minor versions (2.3.0)**: New features, backward compatible.
  Safe to upgrade.

- **Patch versions (2.3.1)**: Bug fixes only.
  Always safe to upgrade.
```

### 版本固定建议

帮助开发者做出合理选择：

```markdown
# Recommended Version Constraints

For stability, we recommend:
- `"myapi": "^2.3.0"` - Get patches and minor updates
- `"myapi": "~2.3.0"` - Get patches only

For production systems:
- Pin exact versions: `"myapi": "2.3.0"`
- Review changelogs before upgrading
- Test in staging first
```

### API 版本号沟通

```markdown
# API Versions

## Current Versions
- **v2** (current): Full support, recommended for new integrations
- **v1** (legacy): Security fixes only, sunset March 2025

## Version Lifecycle
| Status | Duration | What It Means |
|--------|----------|---------------|
| Current | Ongoing | Full support, new features |
| Legacy | 12 months | Security fixes only |
| Deprecated | 6 months | No updates, migration required |
| Sunset | - | No longer available |

## Specifying Version
```bash
curl https://api.example.com/v2/users
# or
curl -H "API-Version: 2024-01-15" https://api.example.com/users
```
```

## 破坏性变更

### 破坏性变更公告模板

```markdown
# Breaking Change: [Brief Description]

**Affects**: SDK v3.0.0, API version 2024-03
**Timeline**: Changes take effect March 15, 2024

## What's Changing
[Clear description of the change]

## Why We're Making This Change
[Honest explanation - better performance, security, consistency]

## Who's Affected
- ✅ Users of SDK v2.x - no action required
- ⚠️ Users of SDK v3.0.0+ - update required
- ⚠️ Direct API users on v1 - update required

## Required Actions

### If you use our SDK:
```python
# Before (v2.x)
client.old_method(user_id="123")

# After (v3.x)
client.new_method(id="123")
```

### If you call the API directly:
```bash
# Before
POST /v1/users/123/analyze

# After
POST /v2/users/123/analyze
```

## Migration Guide
[Link to detailed migration documentation]

## Timeline
- **Now**: v3.0.0 beta available for testing
- **Feb 1**: v3.0.0 stable released
- **Mar 1**: v2.x enters legacy support
- **Mar 15**: Breaking changes take effect in API
- **Sep 15**: v2.x sunset (no longer supported)

## Need Help?
- [Migration guide](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
- [Office hours signup](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
- [Support channel](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
```

### 破坏性变更沟通时间表

```
6 months before:  Announce upcoming change
3 months before:  Release new version with migration path
1 month before:   Send direct emails to affected users
2 weeks before:   Final reminder
Day of:           Change takes effect
1 week after:     Follow-up for stragglers
```

## 弃用通知

### 代码内弃用标记

```python
import warnings

def old_method(self, user_id):
    """
    .. deprecated:: 2.3.0
       Use :meth:`new_method` instead. Will be removed in v3.0.0.
    """
    warnings.warn(
        "old_method() is deprecated and will be removed in v3.0.0. "
        "Use new_method() instead. "
        "Migration guide: https://docs.example.com/migrate-v3",
        DeprecationWarning,
        stacklevel=2
    )
    return self.new_method(id=user_id)
```

### API 弃用响应头

```http
HTTP/1.1 200 OK
Deprecation: Sun, 15 Sep 2024 00:00:00 GMT
Sunset: Sun, 15 Mar 2025 00:00:00 GMT
Link: <https://docs.example.com/migrate-v3>; rel="deprecation"

{
  "data": {...},
  "_deprecation": {
    "message": "This endpoint is deprecated",
    "sunset": "2025-03-15",
    "migration": "https://docs.example.com/migrate-v3"
  }
}
```

### 弃用类更新日志条目

```markdown
### Deprecated
- **`/v1/analyze` endpoint**: Use `/v2/analyze` instead.
  - Migration guide: [link]
  - Sunset date: March 15, 2025
  - After sunset: Requests will return 410 Gone
```

## 制造期待感

### "即将上线" 预告

为即将到来的功能制造期待：

```markdown
# Coming in Q2 2024

## Batch Processing API (Beta available now)
Process up to 1,000 items in a single request.
[Join the beta](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)

## Python SDK v3.0
Complete rewrite with async support, type hints, and 50% faster.
[Preview documentation](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)

## EU Data Residency
For customers with European data requirements.
[Join waitlist](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
```

### 发布节奏沟通

明确预期：

```markdown
# Release Schedule

**SDK Releases**: First Monday of each month
**API Updates**: Continuous (backward compatible)
**Breaking Changes**: Twice per year (March, September)

Subscribe to updates:
- [GitHub releases](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
- [Email newsletter](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
- [Discord announcements](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
- [Twitter/X](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
```

### 把功能上线做成事件

把重要版本发布变成高光时刻：

```markdown
# 🚀 SDK v3.0 Launch

We're excited to announce the biggest SDK update in 2 years!

## Highlights
- **50% faster** request processing
- **Full async support** for high-throughput applications
- **Type hints** throughout for better IDE support
- **Simplified auth** - configure once, use everywhere

## Launch Week
- **Monday**: SDK v3.0 stable release
- **Tuesday**: Live coding session (YouTube)
- **Wednesday**: Migration office hours
- **Thursday**: Community showcase
- **Friday**: AMA with the SDK team

## Resources
- [Documentation](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
- [Migration guide](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)
- [Video walkthrough](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/changelog-updates/link)

## Thank You
Special thanks to our 47 beta testers who found 23 bugs
and suggested 12 improvements that made it into this release!
```

## 分发渠道

### 发布到哪里

| 渠道 | 受众 | 内容详略 |
|---------|----------|---------------|
| GitHub Releases | 关注仓库的开发者 | 完整更新日志 |
| 文档站更新日志 | 所有开发者 | 完整更新日志 |
| 博客 | 更广泛的受众 | 亮点 + 背景 |
| 邮件 | 活跃用户 | 摘要 + 行动项 |
| Twitter/X | 社区 | 仅亮点 |
| Discord/Slack | 高参与度社区 | 讨论 + 亮点 |

### 邮件模板

**常规发布：**
```
Subject: [Product] v2.3.0 Released - Batch Processing + Bug Fixes

Hey [name],

We just released v2.3.0 with some improvements you'll like:

✨ New batch processing API - handle 100 items at once
🐛 Fixed timeout issues with large files
⚡ 40% faster list operations

Full changelog: [link]
Upgrade guide: [link]

Happy building,
The [Product] Team
```

**破坏性变更：**
```
Subject: ⚠️ Action Required: [Product] Breaking Change on March 15

Hey [name],

We're making changes to improve [X], and you'll need to
update your integration before March 15.

What's changing: [one sentence]
What you need to do: [one sentence]
Full details: [link]

Need help? Reply to this email or join our office hours: [link]

Best,
The [Product] Team
```

## 工具

### 更新日志生成
- **Conventional Commits**：结构化的提交信息
- **semantic-release**：基于 commit 自动生成更新日志
- **changesets**：Monorepo 更新日志管理
- **Keep a Changelog**：格式规范

### 分发
- **GitHub Releases**：贴近大多数开发者工作流
- **Beehiiv/Buttondown**：面向开发者的 Newsletter 平台
- **Twitter/X**：向社区快速同步
- **Discord/Slack**：社区讨论

### 监控
- **GitHub Stars/Watchers**：互动指标
- **npm 下载量**：采用度追踪
- **邮件打开率**：沟通效果

## 相关技能

- **sdk-dx**：SDK 版本管理与迁移
- **docs-as-marketing**：作为文档的更新日志
- **developer-community**：社区沟通渠道
- **developer-metrics**：衡量更新日志互动度
- **technical-content-strategy**：作为内容的更新日志

## 局限

- 仅当任务明确匹配其上游来源与本地项目上下文时使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要把示例当作环境专属测试、安全审查或用户对破坏性 / 高成本操作的审批的替代品。
