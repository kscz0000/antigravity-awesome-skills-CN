---
name: android-cli
description: 使用 `android` 命令行工具编排 Android 开发任务，包括项目创建、部署、SDK 管理以及环境诊断。
category: tools
risk: critical
source: self
source_type: self
date_added: "2026-06-15"
author: Owais
tags: [android, cli, adb, mobile, build, emulator]
tools: [claude, cursor, gemini, antigravity]
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "安装引导会执行远程 Android CLI 安装脚本；应避免放入插件安全包。"
    docs: SKILL.md
---

# Android CLI 专家

本技能提供使用 `android` CLI 工具的说明。该工具包含用于创建项目、运行应用、与设备交互以及管理 CLI 环境的各类命令。

## 使用场景

- 需要通过命令行创建、配置或分析 Android 项目时。
- 需要与运行中的 Android 设备交互、向其部署应用或截取屏幕时。
- 需要管理 Android SDK 组件、版本或虚拟设备（模拟器）时。
- 需要检查 UI 布局或运行 XML 指定的 journey 测试时。

## 安装

如果 `android` 工具不在 PATH 中，请将平台安装程序下载到私有临时目录，检查其内容，并在用户确认来源与内容后再执行：

```bash
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/android-cli.XXXXXX")" || exit 1
curl -fsSL https://dl.google.com/android/cli/latest/linux_x86_64/install.sh -o "$tmpdir/install.sh"
sed -n '1,160p' "$tmpdir/install.sh"
# 检查并经用户明确确认后：
bash "$tmpdir/install.sh"
```

macOS 与 Windows 请分别使用对应的 `darwin_arm64/install.sh` 或 `windows_x86_64/install.cmd` 链接。请勿将可变网络安装脚本直接通过管道传入 shell 执行。

## SDK 管理

使用 `sdk` 命令管理 Android SDK 与工具的安装。例如：

- `android sdk install <package>[@<version>]...`：安装指定包，可一次指定多个，以空格分隔。`<version>` 默认为最新版。例如：`android sdk install platforms/android-30@2 platforms/android-34`
- `android sdk update [<pkg-name>]`：将指定包或全部包更新到最新版。
- `android sdk remove <pkg-name>`：从本地 SDK 中移除某个包。
- `android sdk list --all`：列出已安装和可用的 SDK 包。

## 项目创建

使用 `create` 命令从模板创建项目。

例如：
```bash
android create empty-activity --name="My App" --output=./my-app
```

## 与设备交互

有关与运行中设备交互的更多信息，请参阅 [此处](references/interact.md)。

## 运行 Journey 测试

有关运行 journey 的更多信息，请参阅 [此处](references/journeys.md)。

## 文档检索

`docs` 命令可在 Android 知识库中检索权威且高质量的 Android 开发者文档。
只需提供若干关键词，该工具就会返回包含 Android API 或库使用示例与指导的高质量文章。
当需要获取完成 Android 特定任务的方法或了解 Android API、Surface、库、设备的相关信息时，请使用此工具。

请始终使用此工具获取关于 Android 概念的最新信息。典型的使用场景包括：
  - 查找 API 的迁移指南。
  - 查找 API 的使用示例。
  - 查找 Android API 的最新信息。
  - 查找 Android 概念的最佳实践。

## 运行 APK

使用 `run` 命令运行 Android 应用。

## 管理模拟器

使用 `android emulator` 命令管理 Android 虚拟设备（AVD）。

## 截取屏幕

使用 `android screen capture -o <file path>` 命令截取已连接 Android 设备当前屏幕的图像，并输出到指定文件。

## 管理 Skills

使用 `android skills` 命令管理用于 Android 的 antigravity 智能体技能。

## 检查 UI 布局

使用 `android layout` 命令检查 Android 应用的 UI 布局。它会以 JSON 格式返回应用的布局树。在调试 UI 错误时，这通常比截图快得多。

## 更新 CLI

使用 `android update` 命令更新 Android CLI。

## 限制

- `android` CLI 必须已安装并在 `PATH` 中可用；否则请先安装或参考上文平台特定的设置指引。
- 设备、模拟器、SDK 与文档命令依赖本地 Android SDK 状态、网络访问以及接入的硬件。
- 将生成的命令视为对环境敏感：执行前请检查路径、包名、设备序列号以及安装/更新目标。

## Android 帮助输出

```text
Usage: android [-hV] [--sdk=PARAM] [COMMAND]
  -h, --help        Show this help message and exit.
      --sdk=PARAM   Path to the Android SDK
  -V, --version     Print version information and exit.
Commands:
  create    Create a new Android project
  describe  Analyzes an Android project to generate descriptive metadata.
  docs      Android documentation commands
  emulator  Emulator commands
  help      Shows the help of all commands
  info      Print environment information (SDK Location, etc.)
  init      Initializes the environment (eg. skills) for Android CLI.
  layout    Returns the layout tree of an application
  run       Deploy an Android Application
  screen    Commands to view the device
  sdk       Download and list SDK packages
  skills    Manage skills
  update    Update the Android CLI

create
          Usage: android create [-h] [--verbose] [--list] [--minSdk=api]
                                --name=applicationName [-o=dest-path] [template-name]
          Create a new Android project
                [template-name]      The template name
            -h, --help               Show this help message and exit.
                --minSdk=api         The 'minSdk' supported by the application (default
                                       is defined in the template)
                --name=applicationName
                                      The name of the application (e.g. 'My Application')
            -o, --output=dest-path   The destination project directory path (default is
                                       '.')
                --verbose            Enables verbose output
                --list               List all available templates

describe
          Usage: android describe [-hV] [--project_dir=PARAM]
          Analyzes an Android project to generate descriptive metadata.
          This command identifies and outputs the paths to JSON files that detail the
          project's structure, including build targets and their corresponding output
          artifact locations (e.g., APKs). This information enables other tools and
          commands to locate build artifacts efficiently.
            -h, --help                Show this help message and exit.
                --project_dir=PARAM   The project directory to describe
            -V, --version             Print version information and exit.

docs
          Usage: android docs [-h] [COMMAND]
          Android documentation commands
            -h, --help   Show this help message and exit.
          Commands:
            search  Search Android documentation
            fetch   Fetch Android documentation

emulator
          Usage: android emulator [-h] [COMMAND]
          Emulator commands
            -h, --help   Show this help message and exit.
          Commands:
            create  Creates a virtual device
            start   Launches the specified virtual device. This command will return when
                      the emulator is fully started and ready to use.
            stop    Stops the specified virtual device
            list    Lists available virtual devices
            remove  Delete a virtual device

help
          Usage: android help [COMMAND]
          Shows the help of all commands
                [COMMAND]   The command to show help for

info
          Usage: android info <field>
          Print environment information (SDK Location, etc.)
                <field>   The specific field to print the value of. If omitted print all.

init
          Usage: android init
          Initializes the environment (eg. skills) for Android CLI.

layout
          Usage: android layout [-dhp] [--device=PARAM] [-o=PARAM]
          Returns the layout tree of an application
            -d, --diff           Returns a flat list of the layout elements that have
                                   changed since the last invocation of ui-dump
                --device=PARAM   The device serial number
            -h, --help           Show this help message and exit.
            -o, --output=PARAM   Writes the layout tree to the specified file or
                                   directory. If omitted, prints the tree to standard
                                   output
            -p, --pretty         Pretty-prints the returned JSON

run
          Usage: android run [-h] [--debug] [--activity=PARAM] [--device=PARAM]
                             [--type=PARAM] [--apks=PARAM[,PARAM...]]...
          Deploy an Android Application
                --activity=PARAM   The activity name
                --apks=PARAM[,PARAM...]
                                   The paths to the APKs
                --debug            Run in debug mode
                --device=PARAM     The device serial number
            -h, --help             Show this help message and exit.
                --type=PARAM       The component type (ACTIVITY, SERVICE, etc.)

screen
          Usage: android screen [-h] [COMMAND]
          Commands to view the device
            -h, --help   Show this help message and exit.
          Commands:
            capture  Outputs the device screen to a PNG
            resolve  Target UI elements visually

sdk
          Usage: android sdk [COMMAND]
          Download and list SDK packages
          Commands:
            install  Install SDK packages
            update   Update one or all packages to the latest version
            remove   Remove a package from the SDK
            list     List installed and available SDK packages

skills
          Usage: android skills [COMMAND]
          Manage skills
          Commands:
            add     Install a skill
            remove  Remove a skill
            list    List available skills
            find    Find skills by keyword

update
          Usage: android update [--url=PARAM]
          Update the Android CLI
                --url=PARAM   The URL to download the update from
```