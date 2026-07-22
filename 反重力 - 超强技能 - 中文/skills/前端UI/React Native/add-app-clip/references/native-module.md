# 原生 App Clip 检测

创建一个本地 Expo 模块，使 JS 能够检测当前是否运行在 App Clip 内，并展示完整应用的安装提示。

```sh
bunx create-expo-module --local
```

## Swift 模块

```swift
import ExpoModulesCore
import StoreKit

internal class MissingCurrentWindowSceneException: Exception {
  override var reason: String {
    "Cannot determine the current window scene in which to present the modal for requesting a review."
  }
}

internal class MissingContainerURLException: Exception {
  override var reason: String {
    "Cannot determine the container URL."
  }
}

public class AppClipModule: Module {
  private static let isAppClip: Bool = {
    if let infoPlist = Bundle.main.infoDictionary, let _ = infoPlist["NSAppClip"] as? [String: Any] {
      return true
    }
    return false
  }()

  public func definition() -> ModuleDefinition {
    Name("AppClip")

    Constant("isAppClip") {
      AppClipModule.isAppClip
    }

    // Display overlay to advertise full app.
    // https://developer.apple.com/documentation/app_clips/recommending_your_app_to_app_clip_users
    AsyncFunction("prompt") {
      if #available(iOS 16, *) {
        guard let currentScene = UIApplication.shared.connectedScenes.first as? UIWindowScene else {
          throw MissingCurrentWindowSceneException()
        }

        let config = SKOverlay.AppClipConfiguration(position: .bottom)
        let overlay = SKOverlay(configuration: config)
        overlay.present(in: currentScene)
      }
    }.runOnQueue(DispatchQueue.main)
  }
}
```

## TypeScript 接口

```ts
import { NativeModule, requireOptionalNativeModule } from "expo";

declare class AppClipModule extends NativeModule<{}> {
  prompt(): void;
  isAppClip?: boolean;
}

const AppClipNative = requireOptionalNativeModule<AppClipModule>("AppClip");

if (AppClipNative?.isAppClip) {
  navigator.appClip = {
    prompt: AppClipNative.prompt,
  };
}

declare global {
  interface Navigator {
    /**
     * Only available in an App Clip context.
     * @expo
     */
    appClip?: {
      /** Open the SKOverlay */
      prompt: () => void;
    };
  }
}

export {};
```

## 使用方式

- 检测 App Clip 上下文：`if (navigator.appClip) { ... }`
- 提示安装完整应用：`navigator.appClip?.prompt()`