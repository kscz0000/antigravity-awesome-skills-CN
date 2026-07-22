---
name: app-store-changelog
description: 从上次标签以来的 git 历史生成面向用户的 App Store 发布说明。当用户要求'App Store 更新日志'、'发布说明'、'What's New 文本'时使用。
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# App Store 更新日志

## 概述
从上次标签以来的 git 历史生成全面的、面向用户的更新日志，然后将提交记录转化为清晰的 App Store 发布说明。

## 使用场景
- 当用户要求从 git 历史生成 App Store "What's New" 文本或发布说明时。
- 当你需要将原始提交记录转化为简洁的、面向用户的发布要点时。

## 工作流程

### 1) 收集变更
- 从仓库根目录运行 `scripts/collect_release_changes.sh` 来收集提交和涉及的文件。
- 如需指定标签或引用：`scripts/collect_release_changes.sh v1.2.3 HEAD`。
- 如果不存在标签，脚本将回退到完整历史。

### 2) 筛选用户影响
- 扫描提交和文件，识别用户可见的变更。
- 按主题分组变更（新增、改进、修复），并去除重叠项。
- 丢弃仅内部的工作（构建脚本、重构、依赖升级、CI）。

### 3) 起草 App Store 说明
- 为每个面向用户的变更编写简短的、以收益为导向的要点。
- 使用清晰的动词和通俗语言；避免内部术语。
- 优先 5 到 10 条要点，除非用户要求不同长度。

### 4) 验证
- 确保每条要点都能映射回范围内的真实变更。
- 检查重复和过于技术化的措辞。
- 如果任何变更含糊不清或可能仅限内部，请求澄清。

## 提交到要点示例

以下展示了原始提交如何转化为 App Store 要点：

| 原始提交消息 | App Store 要点 |
|---|---|
| `fix(auth): resolve token refresh race condition on iOS 17` | • 修复了可能导致部分用户意外退出登录的问题。 |
| `feat(search): add voice input to search bar` | • 使用新的语音输入选项，解放双手搜索你的内容库。 |
| `perf(timeline): lazy-load images to reduce scroll jank` | • 浏览时间线现在更流畅、更快速。 |

仅内部的提交将被**丢弃**（无用户影响）：
- `chore: upgrade fastlane to 2.219`
- `refactor(network): extract URLSession wrapper into module`
- `ci: add nightly build job`

## 输出示例

```
What's New in Version 3.4

• Search your library hands-free with the new voice input option.
• Scrolling through your timeline is now smoother and faster.
• Fixed a login issue that could leave some users unexpectedly signed out.
• Added dark-mode support to the settings screen.
• Improved load times when opening large photo albums.
```

## 输出格式
- 标题（可选）："What's New" 或产品名 + 版本号。
- 仅要点列表；每条一句话。
- 如果用户提供了字数限制，遵守商店限制。

## 资源
- `scripts/collect_release_changes.sh`：收集上次标签以来的提交和涉及的文件。
- `references/release-notes-guidelines.md`：App Store 说明的语言、过滤和 QA 规则。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，停下来请求澄清。
