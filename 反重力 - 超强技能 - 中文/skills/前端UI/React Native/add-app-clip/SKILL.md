---
name: add-app-clip
description: 向 Expo 应用添加 iOS App Clip 目标。适用于用户提及 App Clip、AASA、apple-app-site-association、appclips、smart app banner，或希望发布一个可通过 URL 与主应用一同启动的轻量级 iOS Clip 的场景。触发词：App Clip、AASA、apple-app-site-association、appclips、smart app banner、轻量级 iOS Clip、关联域、TestFlight
risk: unknown
source: https://github.com/expo/skills/tree/main/plugins/expo/skills/add-app-clip
source_repo: expo/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/expo/skills/blob/main/LICENSE
---

# 向 Expo 应用添加 App Clip
## 适用场景

当你需要向 Expo 应用添加 iOS App Clip 目标时使用本技能。适用于用户提及 App Clip、AASA、apple-app-site-association、appclips、smart app banner，或希望发布一个可通过 URL 与主应用一同启动的轻量级 iOS Clip 的场景。


为 Expo 项目添加一个 iOS App Clip 目标。Clip 位于 `targets/clip/`，与主应用一同发布，并通过 Apple App Site Association（AASA）文件由应用域名下的一个 URL 触发启动。

主应用的 Bundle ID 变为 `com.<username>.<app-name>`，Clip 的 Bundle ID 会自动派生为 `<parent>.clip`（例如 `com.bacon.may20.clip`）。

## 1. 设置 `bundleIdentifier` 与 `appleTeamId`

如果缺失这两项，`bun create target` 会发出警告。请将其加入 `app.json`：

```json
{
  "expo": {
    "ios": {
      "bundleIdentifier": "com.<username>.<app-name>",
      "appleTeamId": "XX57RJ5UTD"
    }
  }
}
```

## 2. 添加 App Clip 目标

```sh
bun create target clip
```

该命令会安装 [`@bacons/apple-targets`](https://github.com/EvanBacon/expo-apple-targets)，将其加入 `app.json` 的 `plugins` 数组，并写入以下文件：

- `targets/clip/expo-target.config.js` — 目标的配置插件
- `targets/clip/Info.plist` — Clip 的 Info.plist
- `targets/clip/AppDelegate.swift`、`Assets.xcassets` 等

挑选一个合适的图标，或复用主应用中已定义的图标——可通过 `bunx expo config` 检查 `icon` 或 `ios.icon` 字段。

## 3. 配置关联域

主应用与 Clip 各自都需要一份指向托管 AASA 文件域名的关联域（Associated Domains）授权。

在 `app.json` 中，同时添加 `applinks:`（主应用）与 `appclips:`（用于触发 Clip）条目：

```json
{
  "expo": {
    "ios": {
      "associatedDomains": [
        "applinks:may20.expo.app",
        "appclips:may20.expo.app"
      ]
    }
  }
}
```

在 `targets/clip/expo-target.config.js` 中声明 Clip 的授权：

```js
/** @type {import('@bacons/apple-targets/app.plugin').ConfigFunction} */
module.exports = (config) => ({
  type: "clip",
  icon: "https://github.com/expo.png",
  entitlements: {
    "com.apple.developer.associated-domains": ["appclips:may20.expo.app"],
  },
});
```

> 若跳过此步骤，`expo prebuild` 会打印：`Apple App Clip may require the associated domains entitlement but none were found`。

## 4. 注册 Bundle ID 并创建 App Store 条目

```sh
bunx setup-safari
```

该命令会登录 Apple Developer 账号，注册 `com.bacon.may20`，创建 App Store Connect 条目，并输出：

- 一段起步用的 `apple-app-site-association` JSON
- 一个带有 iTunes app id 的 `<meta name="apple-itunes-app">` 标签
- Team ID、iTunes ID 和 Bundle ID

## 5. 托管 AASA 文件

当 iOS 访问 `https://<your-domain>/.well-known/apple-app-site-association` 并找到匹配的 `appclips` 条目时，便会触发 App Clip。

```sh
mkdir -p public/.well-known
touch public/.well-known/apple-app-site-association
```

将 `setup-safari` 输出的 JSON 粘贴进去，并**为 Clip 的完整 App ID（`<TeamID>.<ClipBundleID>`）补充一个 `appclips` 块**。`setup-safari` 的输出只覆盖主应用：

```json
{
  "applinks": {
    "details": [
      {
        "appIDs": ["XX57RJ5UTD.com.bacon.may20"],
        "components": [{ "/": "*", "comment": "Matches all routes" }]
      }
    ]
  },
  "appclips": {
    "apps": ["XX57RJ5UTD.com.bacon.may20.clip"]
  },
  "activitycontinuation": {
    "apps": ["XX57RJ5UTD.com.bacon.may20"]
  },
  "webcredentials": {
    "apps": ["XX57RJ5UTD.com.bacon.may20"]
  }
}
```

注意事项：

- 文件**没有扩展名**，对 `Content-Type` 也**没有特殊要求**，原样提供即可。Expo Router 的静态导出会按原样提供 `public/` 下的文件。
- `appclips` 块是该域上某个 URL 能够启动 Clip 的关键。
- `webcredentials` 用于在网站、主应用与 App Clip 之间共享凭据。
- `activitycontinuation` 为可选项，用于在移动端与桌面端之间共享链接。必须配合 expo-router 的 `Head` 使用——详见 https://docs.expo.dev/router/advanced/apple-handoff/
- 标记与路由禁用细节：https://sosumi.ai/documentation/xcode/supporting-associated-domains

## 6. 添加 Smart App Banner meta 标签

创建 `src/app/+html.tsx`（Expo Router 的 HTML 外壳），并添加 `setup-safari` 输出的标签。如果尚未创建该版本化模板，请先创建：

```sh
bunx expo customize src/app/+html.tsx
```

将 meta 标签添加到 `<head>` 中：

```tsx
import { ScrollViewStyleReset } from "expo-router/html";

export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="apple-itunes-app" content="app-id=6771566491" />
        <ScrollViewStyleReset />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

若希望网站显示 App Clip 卡片而非安装卡片，可使用：

```html
<meta
  name="apple-itunes-app"
  content="app-id=6771566491, app-clip-bundle-id=com.bacon.may20.clip, app-clip-display=card"
/>
```

## 7. 部署网站

iOS 必须先能访问到 AASA 文件，才会信任该关联。可使用 [EAS Hosting](https://docs.expo.dev/eas/hosting/)：

```sh
bunx expo export -p web
eas deploy --prod
```

这会将网站发布到 `https://<slug>.expo.app`（包括 `/.well-known/apple-app-site-association`）。可通过下述命令验证：

```sh
curl https://may20.expo.app/.well-known/apple-app-site-association
```

## 8. 镜像权限

在 prebuild 之后，检查主应用的权限：

```sh
npx expo config --type introspect
```

查看 `infoPlist` 对象——在 App Clip 的 `Info.plist` 中镜像相应的权限键，以便 Clip 内也能调用对应的 API。

在 Clip 的目标配置中设置 `deploymentTarget: "17.6"`——iOS 17.6 中 App Clip 的最小体积上限更高。

如果应用使用推送通知或定位服务，请在 App Clip 的 `Info.plist` 中添加以下内容以申请相应权限：

```xml
<key>NSAppClip</key>
<dict>
  <key>NSAppClipRequestEphemeralUserNotification</key>
  <false/>
  <key>NSAppClipRequestLocationConfirmation</key>
  <true/>
</dict>
```

## 9. 构建并提交至 TestFlight

```sh
bunx testflight
```

此命令将执行：

1. 如缺失 `eas.json`，则生成一份。
2. 为**两个**目标（主应用 + Clip）分别配置凭证。两者各自拥有独立的 Provisioning Profile，但可以共用同一份发布证书。
3. 同步能力配置——请留意 Clip 目标中的 `Enabled: Associated Domains`。
4. 构建、上传并安排一次 TestFlight 提交。

## 10. 配置 App Clip 元数据

将现有的 App Store 元数据拉取到本地：

```sh
eas metadata:pull
```

在 `store.config.json` 中添加 `apple.appClip`。最多可以配置 3 个调用 URL，从网页端启动 Clip：

```json
{
  "configVersion": 0,
  "apple": {
    "appClip": {
      "defaultExperience": {
        "action": "PLAY",
        "releaseWithAppStoreVersion": true,
        "reviewDetail": {
          "invocationUrls": ["https://may20.expo.app/", null, null]
        },
        "info": {
          "en-US": {
            "subtitle": "Instantly native with Expo",
            "headerImage": "store/apple/app-clip/en-US/asc-app-clip.png"
          }
        }
      }
    }
  }
}
```

`headerImage` 必须为不透明、1800x1200 的 PNG。

再将其推回商店：

```sh
eas metadata:push
```

Apple 推荐的 App Clip 元数据指南：https://sosumi.ai/documentation/appclip/configuring-the-launch-experience-of-your-app-clip

## 交付物

- 主应用目标：`com.bacon.may20`
- App Clip 目标：`com.bacon.may20.clip`，位于 `targets/clip/`
- AASA 托管于 `https://may20.expo.app/.well-known/apple-app-site-association`
- 每个 Web 路由上的 Smart App Banner meta 标签
- 每个路由都关联到对应的原生页面
- 主应用的 TestFlight 构建，其中已嵌入 Clip

一旦 Apple 从该域上的某个 URL 触发 Clip，iOS 便会打开 `targets/clip/` 的入口，进而加载 React Native 应用。

## 原生检测（可选）

若希望 JS 能检测到当前运行在 App Clip 内，并展示完整应用的安装提示，可创建一个本地 Expo 模块（`bunx create-expo-module --local`），对外暴露 `navigator.appClip.prompt()`。

Swift 模块、TypeScript 接口与使用方式详见 [./references/native-module.md](./references/native-module.md)。

## 参考资料

- ./references/native-module.md — 用于检测 App Clip 上下文并展示 SKOverlay 安装提示的本地 Expo 模块

## 局限性

- 仅当任务明确匹配其上游产品或 API 范围时才使用本技能。
- 在执行任何变更之前，请依据最新的官方文档核实命令、API 行为、价格、配额、凭证以及部署影响。
- 不要把生成的示例当作特定环境的测试、安全审查或对破坏性、高代价操作的用户授权的替代品。