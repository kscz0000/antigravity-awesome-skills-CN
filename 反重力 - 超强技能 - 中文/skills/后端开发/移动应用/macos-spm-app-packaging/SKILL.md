---
name: macos-spm-app-packaging
description: 无需 Xcode 项目，即可搭建、构建、签名和打包 SwiftPM macOS 应用。当用户要求"SwiftPM 打包""macOS 应用打包""无需 Xcode 构建""SwiftPM 签名""macOS 公证"时使用。
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# macOS SwiftPM 应用打包（无需 Xcode）

## 概述
引导创建一个完整的 SwiftPM macOS 应用目录，然后在无需 Xcode 的情况下完成构建、打包和运行。使用 `assets/templates/bootstrap/` 获取初始布局，使用 `references/packaging.md` + `references/release.md` 了解打包和发布详情。

## 适用场景
- 用户需要一个基于 SwiftPM 的 macOS 应用，且不依赖 Xcode 项目。
- 需要为 SwiftPM 应用提供打包、签名、公证或 appcast 相关指导。

## 两步工作流
1) 引导项目目录
   - 将 `assets/templates/bootstrap/` 复制到新仓库中。
   - 在 `Package.swift`、`Sources/MyApp/` 和 `version.env` 中重命名 `MyApp`。
   - 自定义 `APP_NAME`、`BUNDLE_ID` 和版本号。

2) 构建、打包和运行引导后的应用
   - 将 `assets/templates/` 中的脚本复制到你的仓库（例如 `Scripts/`）。
   - 构建/测试：`swift build` 和 `swift test`。
   - 打包：`Scripts/package_app.sh`。
   - 运行：`Scripts/compile_and_run.sh`（推荐）或 `Scripts/launch.sh`。
   - 发布（可选）：`Scripts/sign-and-notarize.sh` 和 `Scripts/make_appcast.sh`。
   - 打标签 + GitHub 发布（可选）：创建 git 标签，将 zip/appcast 上传到 GitHub release，然后发布。

## 最小端到端示例
从引导到运行应用的最短路径：
```bash
# 1. 复制并重命名骨架
cp -R assets/templates/bootstrap/ ~/Projects/MyApp
cd ~/Projects/MyApp
sed -i '' 's/MyApp/HelloApp/g' Package.swift version.env

# 2. 复制脚本
cp assets/templates/package_app.sh Scripts/
cp assets/templates/compile_and_run.sh Scripts/
chmod +x Scripts/*.sh

# 3. 构建并启动
swift build
Scripts/compile_and_run.sh
```

## 验证检查点
在关键步骤之后运行以下检查，以便在进入下一阶段之前尽早发现故障。

**打包后（`Scripts/package_app.sh`）：**
```bash
# 确认 .app 包结构完整
ls -R build/HelloApp.app/Contents

# 检查二进制文件存在且可执行
file build/HelloApp.app/Contents/MacOS/HelloApp
```

**签名后（`Scripts/sign-and-notarize.sh` 或临时开发签名）：**
```bash
# 检查签名和权限
codesign -dv --verbose=4 build/HelloApp.app

# 验证包能否通过本地 Gatekeeper 检查
spctl --assess --type execute --verbose build/HelloApp.app
```

**公证和装订后：**
```bash
# 确认装订票据已附加
stapler validate build/HelloApp.app

# 重新运行 Gatekeeper 以确认公证已被识别
spctl --assess --type execute --verbose build/HelloApp.app
```

## 常见公证失败
| 症状 | 可能原因 | 恢复方法 |
|---|---|---|
| `The software asset has already been uploaded` | 同一版本重复提交 | 在 `version.env` 中递增 `BUILD_NUMBER` 并重新打包。 |
| `Package Invalid: Invalid Code Signing Entitlements` | `.entitlements` 文件中的权限与配置文件不匹配 | 对照 Apple 允许的权限集审核；移除不支持的键。 |
| `The executable does not have the hardened runtime enabled` | `codesign` 调用中缺少 `--options runtime` 标志 | 编辑 `sign-and-notarize.sh`，在所有 `codesign` 调用中添加 `--options runtime`。 |
| 公证挂起 / 未收到状态邮件 | `xcrun notarytool` 网络或凭证问题 | 运行 `xcrun notarytool history` 检查状态；如密钥过期则重新导出 App Store Connect API 密钥。 |
| `stapler validate` 在公证成功后失败 | 票据尚未传播 | 等待约 60 秒，然后重新运行 `xcrun stapler staple`。 |

## 模板
- `assets/templates/package_app.sh`：构建二进制文件，创建 .app 包，复制资源，签名。
- `assets/templates/compile_and_run.sh`：开发循环，终止运行中的应用、打包、启动。
- `assets/templates/build_icon.sh`：从 Icon Composer 文件生成 .icns（需安装 Xcode）。
- `assets/templates/sign-and-notarize.sh`：公证、装订并压缩发布构建。
- `assets/templates/make_appcast.sh`：为更新生成 Sparkle appcast 条目。
- `assets/templates/setup_dev_signing.sh`：创建稳定的开发代码签名身份。
- `assets/templates/launch.sh`：已打包 .app 的简易启动器。
- `assets/templates/version.env`：打包脚本使用的示例版本文件。
- `assets/templates/bootstrap/`：最小 SwiftPM macOS 应用骨架（Package.swift、Sources/、version.env）。

## 注意事项
- 权限和签名配置应显式声明；编辑模板脚本而非重新实现。
- 如果不使用 Sparkle 进行更新，请移除 Sparkle 相关步骤。
- Sparkle 依赖于包的构建号（`CFBundleVersion`），因此每次更新时 `version.env` 中的 `BUILD_NUMBER` 必须递增。
- 对于菜单栏应用，打包时设置 `MENU_BAR_APP=1` 以在 Info.plist 中生成 `LSUIElement`。

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
