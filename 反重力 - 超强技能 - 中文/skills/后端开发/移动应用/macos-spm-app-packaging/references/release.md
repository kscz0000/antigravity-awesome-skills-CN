# 发布和公证说明

## 公证要求
- 安装 Xcode 命令行工具（提供 `xcrun` 和 `notarytool`）。
- 提供 App Store Connect API 凭证：
  - `APP_STORE_CONNECT_API_KEY_P8`
  - `APP_STORE_CONNECT_KEY_ID`
  - `APP_STORE_CONNECT_ISSUER_ID`
- 在 `APP_IDENTITY` 中提供 Developer ID Application 身份。

## Sparkle appcast（可选）
- 安装 Sparkle 工具，使 `generate_appcast` 可在 PATH 中访问。
- 提供 `SPARKLE_PRIVATE_KEY_FILE`（ed25519 密钥）。
- appcast 脚本使用你的 zip 产物创建更新的 `appcast.xml`。
- Sparkle 比较 `sparkle:version`（派生自 `CFBundleVersion`），因此每次发布都需递增 `BUILD_NUMBER`。

## 打标签和 GitHub 发布（可选）
使用带版本号的 git 标签，并在 GitHub release 中发布已公证的 zip（如果在 GitHub Releases 上托管 appcast，也一并上传）。

示例流程：
```
git tag v<version>
git push origin v<version>

gh release create v<version> CodexBar-<version>.zip appcast.xml \
  --title "AppName <version>" \
  --notes-file CHANGELOG.md
```

注意事项：
- 如果从 GitHub Releases 或原始 URL 提供 appcast，请确保 release 已发布且资源可访问（无 404 错误）。
- 建议使用精心编写的发布说明文件，而非直接输出完整变更日志。
