# 打包说明

## 构建输出路径
SwiftPM 将二进制文件放在以下位置：
- `.build/<arch>-apple-macosx/<config>/<AppName>`：特定架构构建
- `.build/<config>/<AppName>`：部分产品（框架/工具）

使用 `ARCHES="arm64 x86_64"` 配合 `swift build` 可生成通用二进制文件。

## 常用环境变量（模板使用）
- `APP_NAME`：应用/二进制文件名称（例如 `MyApp`）。
- `BUNDLE_ID`：包标识符（例如 `com.example.myapp`）。
- `ARCHES`：以空格分隔的架构列表（默认：宿主架构）。
- `SIGNING_MODE`：设为 `adhoc` 可在开发时避免钥匙串提示。
- `APP_IDENTITY`：发布构建的代码签名身份名称。
- `MACOS_MIN_VERSION`：Info.plist 中的最低 macOS 版本。
- `MENU_BAR_APP`：设为 `1` 可在 Info.plist 中添加 `LSUIElement`。
