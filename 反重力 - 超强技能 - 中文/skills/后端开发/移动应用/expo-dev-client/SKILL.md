---
name: expo-dev-client
description: 在本地或通过 TestFlight 构建和分发 Expo 开发客户端
risk: unknown
source: community
version: 1.0.0
license: MIT
---

使用 EAS Build 创建开发客户端，用于在物理设备上测试原生代码更改。适用于为应用的测试分支创建自定义 Expo Go 客户端。

## 何时使用
- 需要 Expo 开发客户端，因为应用依赖自定义原生代码或 Expo Go 不支持的目标平台。
- 任务涉及在物理设备上构建、分发或测试 EAS 开发构建。
- 需要指导何时选择开发客户端而非继续使用普通 Expo Go。

## 重要提示：何时需要开发客户端

**仅在应用需要自定义原生代码时创建开发客户端。** 大多数应用在 Expo Go 中运行良好。

仅在以下情况需要开发客户端：
- 本地 Expo 模块（自定义原生代码）
- Apple 目标（小组件、App Clips、扩展）
- Expo Go 中未包含的第三方原生模块

**首先尝试 Expo Go**，使用 `npx expo start`。如果一切正常，则不需要开发客户端。

## EAS 配置

确保 `eas.json` 包含开发配置文件：

```json
{
  "cli": {
    "version": ">= 16.0.1",
    "appVersionSource": "remote"
  },
  "build": {
    "production": {
      "autoIncrement": true
    },
    "development": {
      "autoIncrement": true,
      "developmentClient": true
    }
  },
  "submit": {
    "production": {},
    "development": {}
  }
}
```

关键设置：
- `developmentClient: true` - 为开发构建打包 expo-dev-client
- `autoIncrement: true` - 自动递增构建号
- `appVersionSource: "remote"` - 使用 EAS 作为版本号的权威来源

## 为 TestFlight 构建

使用一条命令构建 iOS 开发客户端并提交到 TestFlight：

```bash
eas build -p ios --profile development --submit
```

这将：
1. 在云端构建开发客户端
2. 自动提交到 App Store Connect
3. 当构建在 TestFlight 中就绪时发送邮件通知

收到 TestFlight 邮件后：
1. 在设备上从 TestFlight 下载构建
2. 启动应用查看 expo-dev-client UI
3. 连接到本地 Metro 打包器或扫描二维码

## 本地构建

在本地机器上构建开发客户端：

```bash
# iOS（需要 Xcode）
eas build -p ios --profile development --local

# Android
eas build -p android --profile development --local
```

本地构建输出：
- iOS：`.ipa` 文件
- Android：`.apk` 或 `.aab` 文件

## 安装本地构建

在模拟器上安装 iOS 构建：

```bash
# 在 .tar.gz 输出中找到 .app
tar -xzf build-*.tar.gz
xcrun simctl install booted ./path/to/App.app
```

在设备上安装 iOS 构建（需要签名）：

```bash
# 使用 Xcode Devices 窗口或 ideviceinstaller
ideviceinstaller -i build.ipa
```

安装 Android 构建：

```bash
adb install build.apk
```

## 为特定平台构建

```bash
# 仅 iOS
eas build -p ios --profile development

# 仅 Android
eas build -p android --profile development

# 两个平台
eas build --profile development
```

## 检查构建状态

```bash
# 列出最近的构建
eas build:list

# 查看构建详情
eas build:view
```

## 使用开发客户端

安装完成后，开发客户端提供：
- **开发服务器连接** - 输入 Metro 打包器 URL 或扫描二维码
- **构建信息** - 查看原生构建详情
- **启动器 UI** - 在开发服务器之间切换

连接到本地开发环境：

```bash
# 启动 Metro 打包器
npx expo start --dev-client

# 使用开发客户端扫描二维码或手动输入 URL
```

## 故障排除

**构建因签名错误失败：**
```bash
eas credentials
```

**清除构建缓存：**
```bash
eas build -p ios --profile development --clear-cache
```

**检查 EAS CLI 版本：**
```bash
eas --version
eas update
```

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
