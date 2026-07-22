---
name: update-swiftui-apis
description: 扫描 Apple SwiftUI 文档以查找已废弃 API，并用现代替代方案更新 SwiftUI Expert Skill。适用于"更新最新 API"、"刷新已废弃的 SwiftUI API"、"检查新的 SwiftUI 废弃项"、"扫描 API 变更"，或在新版 iOS/Xcode 发布后。涉及 SwiftUI 废弃、API 迁移、Sosumi MCP、iOS 版本适配、latest-apis 时使用。
risk: unknown
source: https://github.com/AvdLee/SwiftUI-Agent-Skill/tree/main/.agents/skills/update-swiftui-apis
source_repo: AvdLee/SwiftUI-Agent-Skill
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/AvdLee/SwiftUI-Agent-Skill/blob/main/LICENSE
---

# 更新 SwiftUI API
## 适用场景

需要扫描 Apple SwiftUI 文档以查找已废弃 API，并用现代替代方案更新 SwiftUI Expert Skill 时，使用本技能。适用于"更新最新 API"、"刷新已废弃的 SwiftUI API"、"检查新的 SwiftUI 废弃项"、"扫描 API 变更"，或在新版 iOS/Xcode 发布后。


通过 Sosumi MCP 系统性扫描 Apple 开发者文档，识别已废弃的 SwiftUI API 及其现代替代方案，并更新 `swiftui-expert-skill/references/latest-apis.md`。

## 前置条件

- **Sosumi MCP** 必须启用并可用（提供 `searchAppleDocumentation`、`fetchAppleDocumentation`、`fetchAppleVideoTranscript`、`fetchExternalDocumentation`）
- 对本仓库（或其 fork）拥有写入权限

## 工作流程

### 1. 了解当前覆盖范围

阅读 `swiftui-expert-skill/references/latest-apis.md`，了解：
- 已记录了哪些从废弃到现代的迁移项
- 当前使用的版本分段（iOS 15+、16+、17+、18+、26+）
- 底部的快速查找表

### 2. 加载扫描清单

阅读 `references/scan-manifest.md`（相对于本技能）。其中包含分类好的 API 区域、文档路径、搜索查询和 WWDC 视频路径。

### 3. 扫描 Apple 文档

针对清单中的每个分类：

1. 使用列出的查询调用 `searchAppleDocumentation` 以发现相关页面。
2. 对特定文档路径调用 `fetchAppleDocumentation` 以获取完整 API 详情。
3. 查找废弃通知、"Deprecated" 标签，以及 "Use ... instead" 说明。
4. 记下现代替代方案可用的 iOS 版本。
5. 可选地调用 `fetchAppleVideoTranscript` 获取宣布 API 变更的 WWDC 会议内容。

批量执行相关搜索以提升效率。重点关注尚未在 `latest-apis.md` 中出现的**新**废弃项。

### 4. 对比并识别变更

将发现与现有条目进行对比。结果分类：
- **新废弃项**：尚未记录在 `latest-apis.md` 中的 API
- **修正项**：需要更新的现有条目（版本错误、有更好的替代方案）
- **新版本分段**：如果新的 iOS 版本引入了废弃项，则添加新章节

### 5. 更新 latest-apis.md

严格遵循既定格式。每个条目必须包含：

**章节归位**——放在正确的版本分段下：
- "Always Use (iOS 15+)" 用于长期废弃的 API
- "When Targeting iOS 16+" / "17+" / "18+" / "26+" 用于按版本门控的变更

**条目格式：**

```markdown
**Always use `modernAPI()` instead of `deprecatedAPI()`.**

\```swift
// Modern
View()
    .modernAPI()

// Deprecated
View()
    .deprecatedAPI()
\```
```

**Quick Lookup Table**——在文件底部添加一行：

```markdown
| `deprecatedAPI()` | `modernAPI()` | iOS XX+ |
```

在文件顶部保留署名行：
> Based on a comparison of Apple's documentation using the Sosumi MCP, we found the latest recommended APIs to use.

### 6. 提交 Pull Request

1. 从 `main` 创建分支，分支名为 `update/latest-apis-YYYY-MM`（使用当前年月）。
2. 提交对 `swiftui-expert-skill/references/latest-apis.md` 的修改。
3. 通过 `gh pr create` 提交 PR：
   - **标题**："Update latest SwiftUI APIs (Month Year)"
   - **正文**：新增/变更条目摘要，署名 Sosumi MCP

## Sosumi MCP 工具参考

| Tool | Parameters | Returns |
|------|-----------|---------|
| `searchAppleDocumentation` | `query` (string) | JSON with `results[]` containing `title`, `url`, `description`, `breadcrumbs`, `tags`, `type` |
| `fetchAppleDocumentation` | `path` (string, e.g. `/documentation/swiftui/view/foregroundstyle(_:)`) | Markdown documentation content |
| `fetchAppleVideoTranscript` | `path` (string, e.g. `/videos/play/wwdc2025/10133`) | Markdown transcript |
| `fetchExternalDocumentation` | `url` (string, full https URL) | Markdown documentation content |

## 提示

- 先用 `searchAppleDocumentation` 查询做大范围检索，再用 `fetchAppleDocumentation` 针对特定路径深挖。
- Apple 的废弃文档通常包含 "Deprecated" 字样，并链接到替代方案。
- WWDC 的 "What's new in SwiftUI" 专题是寻找新引入替代方案的最佳来源。
- 对废弃 API 的具体 iOS 版本不确定时，查阅抓取文档中的 "Availability" 部分加以确认。
- 如果某 API 已废弃但没有直接替代方案，应如实注明，不要建议错误的备选。

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性/高成本操作的审批的替代品。