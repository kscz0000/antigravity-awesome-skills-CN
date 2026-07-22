---
name: defuddle
description: 使用 Defuddle CLI 从网页提取干净的 Markdown 内容，去除杂乱元素和导航以节省 token。当用户提供 URL 需要阅读或分析时使用，适用于在线文档、文章、博客文章或任何标准网页。触发词：defuddle、网页提取、网页内容提取、Markdown 提取、干净内容、去除杂乱、网页转 Markdown、网页解析。
risk: unknown
source: "https://github.com/kepano/obsidian-skills"
date_added: "2026-03-21"
---

# Defuddle

使用 Defuddle CLI 从网页提取干净的可读内容。相比 WebFetch，它更适合标准网页——能去除导航、广告和杂乱元素，减少 token 使用量。

## 何时使用
- 当用户提供普通网页 URL 需要阅读、总结或分析时使用。
- 当需要节省 token 时，优先选择此方案而非嘈杂的页面抓取方法。
- 适用于文档、文章、博客文章和类似的公开网页内容。

如未安装：`npm install -g defuddle`

## 使用方法

始终使用 `--md` 输出 Markdown 格式：

```bash
defuddle parse <url> --md
```

保存到文件：

```bash
defuddle parse <url> --md -o content.md
```

提取特定元数据：

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## 输出格式

| 标志 | 格式 |
|------|------|
| `--md` | Markdown（默认选择） |
| `--json` | JSON（包含 HTML 和 Markdown） |
| （无） | HTML |
| `-p <name>` | 特定元数据属性 |

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
