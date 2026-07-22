# 混合 Android 参考（Capacitor + Ionic / React）

## 何时使用混合方案

✅ 适用场景：
- Web 团队要构建配套 Android 应用
- 内容密集型应用（新闻、文档、表单）
- 将 PWA 升级为可安装应用
- 快速原型开发

❌ 避免场景：
- 实时游戏 / 重型动画
- 深度访问原生传感器 / 硬件
- 需要 60fps 自定义动画的应用
- 蓝牙/NFC 密集型应用（可使用插件，但较复杂）

## 技术栈选项

| 方案 | UI 框架 | 适用场景 |
|--------|------------|---------|
| Capacitor + Ionic | Ionic 组件 | 完整移动端优化 UI |
| Capacitor + React | React + Tailwind | Web 团队复用 |
| Capacitor + Vue | Vue + Ionic | Vue 团队 |
| Capacitor + Angular | Angular + Ionic | 企业级 Angular 团队 |

## 项目结构（Capacitor + React）

```
src/
├── App.tsx
├── pages/                # 页面组件
├── components/           # 共享 UI 组件
├── hooks/                # 业务逻辑 Hook
├── services/             # API、存储服务
└── store/                # 状态管理
android/                  # 原生 Android 项目（自动生成）
├── app/src/main/
│   ├── AndroidManifest.xml
│   └── java/.../MainActivity.kt
capacitor.config.ts       # Capacitor 配置
```

## Capacitor 配置

```typescript
// capacitor.config.ts
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.example.app',
  appName: 'My App',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
  },
  android: {
    buildOptions: {
      releaseType: 'APK', // 或 Play Store 使用的 AAB
    },
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 0,
      backgroundColor: '#FFFFFF',
    },
    PushNotifications: {
      presentationOptions: ['badge', 'sound', 'alert'],
    },
  },
};
```

## 原生插件使用

```typescript
import { Camera, CameraResultType } from '@capacitor/camera';
import { SecureStorage } from '@aparajita/capacitor-secure-storage';
import { PushNotifications } from '@capacitor/push-notifications';
import { Geolocation } from '@capacitor/geolocation';

// 相机
const takePhoto = async () => {
  const photo = await Camera.getPhoto({
    quality: 90,
    allowEditing: false,
    resultType: CameraResultType.Uri,
  });
  return photo.webPath;
};

// 安全存储：不要将鉴权令牌存储在 Capacitor Preferences 中。
// 请使用平台级的安全存储插件，例如
// @aparajita/capacitor-secure-storage、Ionic Identity Vault
// 或等价的 Android Keystore 插件。
const saveToken = async (token: string) => {
  await SecureStorage.set({ key: 'auth_token', value: token });
};

const getToken = async (): Promise<string | null> => {
  const { value } = await SecureStorage.get({ key: 'auth_token' });
  return value;
};

// 推送通知
const initPush = async () => {
  const permission = await PushNotifications.requestPermissions();
  if (permission.receive === 'granted') {
    await PushNotifications.register();
  }
  PushNotifications.addListener('registration', () => {
    console.log('Push registration succeeded');
  });
};
```

## 性能最佳实践

- 确保在 AndroidManifest.xml 中为应用启用硬件加速（Capacitor 默认启用）
- 在 Android WebView 设置中启用 HTTP 缓存
- 使用 React.lazy / 动态导入懒加载路由
- 动画避免使用 `setTimeout`/`setInterval`；改用 CSS 过渡
- 使用 `@ionic/react` 组件——它们已处理移动端特有的触摸行为
- 长列表使用 Ionic 虚拟滚动

## 构建与部署

```bash
# 构建 Web 资源
npm run build

# 同步到原生项目
npx cap sync android

# 在 Android Studio 中打开
npx cap open android

# 通过 Android Studio 构建 release APK/AAB，或：
cd android && ./gradlew bundleRelease
```

## 自定义原生插件（内置插件无法覆盖时）

```
// android/app/src/main/java/.../MyPlugin.kt
@CapacitorPlugin(name = "MyPlugin")
class MyPlugin : Plugin() {
    @PluginMethod
    fun doNativeWork(call: PluginCall) {
        val value = call.getString("input") ?: return call.reject("No input")
        // 执行原生工作
        val result = JSObject()
        result.put("output", "processed: $value")
        call.resolve(result)
    }
}

// TypeScript usage
import { registerPlugin } from '@capacitor/core';
const MyPlugin = registerPlugin<{ doNativeWork: (opts: { input: string }) => Promise<{ output: string }> }>('MyPlugin');
const result = await MyPlugin.doNativeWork({ input: 'hello' });
```