---
name: makepad-deployment
description: |
  关键技能：用于 Makepad 打包与部署。触发词：
  deploy, package, APK, IPA, 打包, 部署,
  cargo-packager, cargo-makepad, WASM, Android, iOS,
  distribution, installer, .deb, .dmg, .nsis,
  GitHub Actions, CI, action, marketplace
  当用户要求"打包"、"部署"、"发布 Makepad 应用"时使用。
risk: critical
source: community
---

# Makepad 打包与部署

本技能涵盖 Makepad 应用在所有支持平台上的打包流程。

## 适用场景

- 需要打包、分发或自动化部署 Makepad 应用
- 涉及桌面安装程序、APK/IPA 构建、WebAssembly 输出或基于 CI 的发布产物
- 需要 `cargo-packager`、`cargo-makepad` 或 GitHub Actions 打包流程指导

## 快速导航

| 平台 | 工具 | 产物 |
|------|------|------|
| [桌面](#desktop-packaging) | `cargo-packager` | .deb, .nsis, .dmg |
| [Android](#android) | `cargo-makepad` | .apk |
| [iOS](#ios) | `cargo-makepad` | .app, .ipa |
| [Web](#wasm-packaging) | `cargo-makepad` | Wasm + HTML/JS |
| [CI/CD](#github-actions-packaging) | `makepad-packaging-action` | GitHub Release 产物 |

---

## GitHub Actions 打包

在 CI 中使用 `makepad-packaging-action` 打包 Makepad 应用。它封装了 `cargo-packager`（桌面端）和 `cargo-makepad`（移动端），并可将产物上传至 GitHub Releases。

```yaml
jobs:
  package:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - uses: Project-Robius-China/makepad-packaging-action@v1
        with:
          args: --target x86_64-unknown-linux-gnu --release
```

注意事项：
- 桌面打包必须在匹配操作系统的 Runner 上运行（Linux/Windows/macOS）
- iOS 构建需要 macOS Runner
- Android 构建可在任意操作系统的 Runner 上运行

完整的 inputs/env/outputs 及发布工作流详见 `references/makepad-packaging-action.md`。

## 桌面打包

桌面打包使用 `cargo-packager`，配合 `robius-packaging-commands` 处理资源。

### 安装工具

```bash
# Install cargo-packager
cargo install cargo-packager --locked

# Install robius-packaging-commands (v0.2.1)
cargo install --version 0.2.1 --locked \
    --git https://github.com/project-robius/robius-packaging-commands.git \
    robius-packaging-commands
```

### 配置 Cargo.toml

在 `Cargo.toml` 中添加打包配置：

```toml
[package.metadata.packager]
product_name = "YourAppName"
identifier = "com.yourcompany.yourapp"
authors = ["Your Name or Team"]
description = "A brief description of your Makepad application"
# Note: long_description has 80 character max per line
long_description = """
Your detailed description here.
Keep each line under 80 characters.
"""
icons = ["./assets/icon.png"]
out_dir = "./dist"

# Pre-packaging command to collect resources
before-packaging-command = """
robius-packaging-commands before-packaging \
    --force-makepad \
    --binary-name your-app \
    --path-to-binary ./target/release/your-app
"""

# Resources to include in package
resources = [
    # Makepad built-in resources (required)
    { src = "./dist/resources/makepad_widgets", target = "makepad_widgets" },
    { src = "./dist/resources/makepad_fonts_chinese_bold", target = "makepad_fonts_chinese_bold" },
    { src = "./dist/resources/makepad_fonts_chinese_bold_2", target = "makepad_fonts_chinese_bold_2" },
    { src = "./dist/resources/makepad_fonts_chinese_regular", target = "makepad_fonts_chinese_regular" },
    { src = "./dist/resources/makepad_fonts_chinese_regular_2", target = "makepad_fonts_chinese_regular_2" },
    { src = "./dist/resources/makepad_fonts_emoji", target = "makepad_fonts_emoji" },

    # Your app resources
    { src = "./dist/resources/your_app_resource", target = "your_app_resource" },
]

before-each-package-command = """
robius-packaging-commands before-each-package \
    --force-makepad \
    --binary-name your-app \
    --path-to-binary ./target/release/your-app
"""
```

### Linux（Debian/Ubuntu）

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install libssl-dev libsqlite3-dev pkg-config \
    binfmt-support libxcursor-dev libx11-dev libasound2-dev libpulse-dev

# Build package
cargo packager --release
```

产物：`./dist/` 目录下的 `.deb` 文件

### Windows

```bash
# Build NSIS installer
cargo packager --release --formats nsis
```

产物：`./dist/` 目录下的 `.exe` 安装程序

### macOS

```bash
# Build package
cargo packager --release
```

产物：`./dist/` 目录下的 `.dmg` 文件

### 平台专属配置

```toml
# Linux (Debian)
[package.metadata.packager.deb]
depends = "./dist/depends_deb.txt"
desktop_template = "./packaging/your-app.desktop"
section = "utils"

# macOS
[package.metadata.packager.macos]
minimum_system_version = "11.0"
frameworks = []
info_plist_path = "./packaging/Info.plist"
entitlements = "./packaging/Entitlements.plist"
# Optional: signing identity for distribution
signing_identity = "Developer ID Application: Your Name (XXXXXXXXXX)"

# macOS DMG
[package.metadata.packager.dmg]
background = "./packaging/dmg_background.png"
window_size = { width = 960, height = 540 }
app_position = { x = 200, y = 250 }
application_folder_position = { x = 760, y = 250 }

# Windows NSIS
[package.metadata.packager.nsis]
appdata_paths = [
    "$APPDATA/$PUBLISHER/$PRODUCTNAME",
    "$LOCALAPPDATA/$PRODUCTNAME",
]
```

---

## 移动端打包

移动平台使用 `cargo-makepad` 进行构建和打包。

### 安装 cargo-makepad

```bash
cargo install --force --git https://github.com/makepad/makepad.git \
    --branch dev cargo-makepad
```

### Android

```bash
# Install Android toolchain
cargo makepad android install-toolchain

# Full NDK (recommended for complete support)
cargo makepad android install-toolchain --full-ndk

# Build APK
cargo makepad android build -p your-app --release
```

产物：`./target/makepad-android-app/` 目录下的 `.apk`

**在设备/模拟器上运行：**
```bash
cargo makepad android run -p your-app --release
```

### iOS

```bash
# Install iOS toolchain
cargo makepad apple ios install-toolchain
```

**iOS 模拟器：**
```bash
cargo makepad apple ios \
    --org=com.yourcompany \
    --app=YourApp \
    run-sim -p your-app --release
```

产物：`./target/makepad-apple-app/aarch64-apple-ios-sim/release/` 目录下的 `.app`

**iOS 真机（需要签名配置）：**

首先在 Xcode 中创建一个同 org/app 名称的空应用，以生成签名配置文件。

```bash
cargo makepad apple ios \
    --org=com.yourcompany \
    --app=YourApp \
    --profile=$YOUR_PROFILE_PATH \
    --cert=$YOUR_CERT_FINGERPRINT \
    --device=iPhone \
    run-device -p your-app --release
```

产物：`./target/makepad-apple-app/aarch64-apple-ios/release/` 目录下的 `.app`

**生成 IPA 用于分发：**
```bash
cd ./target/makepad-apple-app/aarch64-apple-ios/release
mkdir Payload
cp -r your-app.app Payload/
zip -r your-app-ios.ipa Payload
```

---

## Wasm 打包

将 Makepad 应用构建为浏览器可用的 Web 版本。

```bash
# Install Wasm toolchain
cargo makepad wasm install-toolchain

# Build and run
cargo makepad wasm run -p your-app --release
```

产物位于 `./target/makepad-wasm-app/release/your-app/`：
- `index.html` — 入口页面
- `*.wasm` — WebAssembly 模块
- `*.js` — JavaScript 桥接层
- `resources/` — 静态资源

**本地预览：**
```bash
cd ./target/makepad-wasm-app/release/your-app
python3 -m http.server 8080
# Open http://localhost:8080
```

---

## 完整示例 Cargo.toml

```toml
[package]
name = "my-makepad-app"
version = "1.0.0"
edition = "2024"

[dependencies]
makepad-widgets = { git = "https://github.com/makepad/makepad", branch = "dev" }

[profile.release]
opt-level = 3

[profile.release-lto]
inherits = "release"
lto = "thin"

[profile.distribution]
inherits = "release"
codegen-units = 1
lto = "fat"

[package.metadata.packager]
product_name = "My Makepad App"
identifier = "com.example.mymakepadapp"
authors = ["Your Name <you@example.com>"]
description = "A cross-platform Makepad application"
long_description = """
My Makepad App is a cross-platform application
built with the Makepad UI framework in Rust.
It runs on desktop, mobile, and web platforms.
"""
icons = ["./packaging/icon.png"]
out_dir = "./dist"

before-packaging-command = """
robius-packaging-commands before-packaging \
    --force-makepad \
    --binary-name my-makepad-app \
    --path-to-binary ./target/release/my-makepad-app
"""

resources = [
    { src = "./dist/resources/makepad_widgets", target = "makepad_widgets" },
    { src = "./dist/resources/makepad_fonts_chinese_bold", target = "makepad_fonts_chinese_bold" },
    { src = "./dist/resources/makepad_fonts_chinese_bold_2", target = "makepad_fonts_chinese_bold_2" },
    { src = "./dist/resources/makepad_fonts_chinese_regular", target = "makepad_fonts_chinese_regular" },
    { src = "./dist/resources/makepad_fonts_chinese_regular_2", target = "makepad_fonts_chinese_regular_2" },
    { src = "./dist/resources/makepad_fonts_emoji", target = "makepad_fonts_emoji" },
    { src = "./dist/resources/my-makepad-app", target = "my-makepad-app" },
]

before-each-package-command = """
robius-packaging-commands before-each-package \
    --force-makepad \
    --binary-name my-makepad-app \
    --path-to-binary ./target/release/my-makepad-app
"""

[package.metadata.packager.deb]
depends = "./dist/depends_deb.txt"
section = "utils"

[package.metadata.packager.macos]
minimum_system_version = "11.0"

[package.metadata.packager.nsis]
appdata_paths = ["$LOCALAPPDATA/$PRODUCTNAME"]
```

---

## 速查表

| 任务 | 命令 |
|------|------|
| 安装桌面打包工具 | `cargo install cargo-packager --locked` |
| 安装资源处理工具 | `cargo install --version 0.2.1 --locked --git https://github.com/project-robius/robius-packaging-commands.git robius-packaging-commands` |
| 安装移动端打包工具 | `cargo install --force --git https://github.com/makepad/makepad.git --branch dev cargo-makepad` |
| GitHub Actions 打包 | `uses: Project-Robius-China/makepad-packaging-action@v1` |
| Linux 打包 | `cargo packager --release` |
| Windows 打包 | `cargo packager --release --formats nsis` |
| macOS 打包 | `cargo packager --release` |
| 构建 Android APK | `cargo makepad android build -p app --release` |
| 构建 iOS（模拟器） | `cargo makepad apple ios --org=x --app=y run-sim -p app --release` |
| 构建 iOS（真机） | `cargo makepad apple ios --org=x --app=y --profile=... --cert=... run-device -p app --release` |
| 构建 Wasm | `cargo makepad wasm run -p app --release` |

---

## 故障排查

### 资源缺失

应用因资源缺失崩溃时：
1. 检查 Cargo.toml 中的 `resources` 数组是否包含所有 Makepad 资源
2. 确认 `before-packaging-command` 已成功执行
3. 检查 `./dist/resources/` 下是否包含预期文件

### iOS 签名配置

iOS 真机部署：
1. 在 Xcode 中创建同 org/app 标识符的空应用
2. 在真机上运行一次以生成签名配置文件
3. 记录配置文件路径和证书指纹
4. 使用 `--profile`、`--cert`、`--device` 参数

### Android SDK 问题

```bash
# Reinstall toolchain with full NDK
cargo makepad android install-toolchain --full-ndk
```

## 参考文件

- `references/platform-troubleshooting.md` — 平台专属部署问题
- `references/makepad-packaging-action.md` — GitHub Actions 打包参考
- `community/dora-studio-package-workflow.md` — Dora Studio CI 打包示例

## 外部参考

- [cargo-packager 文档](https://docs.crabnebula.dev/packager/)
- [robius-packaging-commands](https://github.com/project-robius/robius-packaging-commands)
- [cargo-makepad](https://github.com/makepad/makepad)
- [makepad-packaging-action](https://github.com/marketplace/actions/makepad-packaging-action)

## 限制

- 仅在任务明确匹配上述范围时使用本技能
- 输出内容不能替代针对具体环境的验证、测试或专家评审
- 缺少必要输入、权限、安全边界或成功标准时，应停下来请求澄清