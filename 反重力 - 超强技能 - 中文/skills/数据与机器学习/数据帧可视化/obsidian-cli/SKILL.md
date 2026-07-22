---
name: obsidian-cli
description: "使用 Obsidian CLI 读取、创建、搜索和管理 vault 内容，或从命令行开发和调试 Obsidian 插件和主题。当用户要求'使用 Obsidian CLI 管理 vault 内容'或'从命令行开发 Obsidian 插件'时使用。"
risk: unknown
source: "https://github.com/kepano/obsidian-skills"
date_added: "2026-03-21"
---

# Obsidian CLI

使用 `obsidian` CLI 与正在运行的 Obsidian 实例进行交互。需要 Obsidian 处于打开状态。

## 使用场景
- 通过 Obsidian CLI 管理 vault 内容时使用。
- 从命令行开发或调试 Obsidian 插件和主题时使用。
- 当用户需要与正在运行的 Obsidian 应用进行 shell 驱动的交互时使用。

## 命令参考

运行 `obsidian help` 查看所有可用命令。此信息始终是最新的。完整文档：https://help.obsidian.md/cli

## 语法

**参数** 使用 `=` 赋值。包含空格的值需要引号：

```bash
obsidian create name="My Note" content="Hello world"
```

**标志** 是布尔开关，无需赋值：

```bash
obsidian create name="My Note" silent overwrite
```

多行内容使用 `\n` 表示换行，`\t` 表示制表符。

## 文件定位

许多命令接受 `file` 或 `path` 来定位文件。如果都不指定，则使用当前活动文件。

- `file=<name>` — 类似 wikilink 解析（仅需名称，无需路径或扩展名）
- `path=<path>` — 从 vault 根目录开始的精确路径，例如 `folder/note.md`

## Vault 定位

命令默认定位最近聚焦的 vault。使用 `vault=<name>` 作为第一个参数来定位特定 vault：

```bash
obsidian vault="My Vault" search query="test"
```

## 常用模式

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

在任何命令上使用 `--copy` 可将输出复制到剪贴板。使用 `silent` 防止文件打开。在列表命令上使用 `total` 获取计数。

## 插件开发

### 开发/测试周期

对插件或主题进行代码更改后，遵循以下工作流程：

1. **重新加载** 插件以获取更改：
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **检查错误** — 如果出现错误，修复后从步骤 1 重复：
   ```bash
   obsidian dev:errors
   ```
3. **视觉验证** 通过截图或 DOM 检查：
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **检查控制台输出** 查看警告或意外日志：
   ```bash
   obsidian dev:console level=error
   ```

### 其他开发者命令

在应用上下文中运行 JavaScript：

```bash
obsidian eval code="app.vault.getFiles().length"
```

检查 CSS 值：

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

切换移动设备模拟：

```bash
obsidian dev:mobile on
```

运行 `obsidian help` 查看其他开发者命令，包括 CDP 和调试器控制。

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。