---
title: Load fonts natively at build time
impact: LOW
impactDescription: 启动时字体即可用，无需异步加载
tags: fonts, expo, performance, config-plugin
---

## 使用 Expo Config Plugin 加载字体

使用 `expo-font` config plugin 在构建时嵌入字体，而非使用
`useFonts` 或 `Font.loadAsync` 进行异步加载。嵌入字体更高效，应用启动时字体即可用，无需等待加载或显示加载状态。异步加载需要额外的加载状态管理，可能导致文本闪烁或布局跳动，而构建时嵌入则完全消除了这些问题。

**错误示例（异步字体加载）：**

```tsx
import { useFonts } from 'expo-font'
import { Text, View } from 'react-native'

function App() {
  const [fontsLoaded] = useFonts({
    'Geist-Bold': require('./assets/fonts/Geist-Bold.otf'),
  })

  if (!fontsLoaded) {
    return null
  }

  return (
    <View>
      <Text style={{ fontFamily: 'Geist-Bold' }}>Hello</Text>
    </View>
  )
}
```

**正确示例（config plugin，构建时嵌入字体）：**

```json
// app.json
{
  "expo": {
    "plugins": [
      [
        "expo-font",
        {
          "fonts": ["./assets/fonts/Geist-Bold.otf"]
        }
      ]
    ]
  }
}
```

```tsx
import { Text, View } from 'react-native'

function App() {
  // No loading state needed—font is already available
  return (
    <View>
      <Text style={{ fontFamily: 'Geist-Bold' }}>Hello</Text>
    </View>
  )
}
```

将字体添加到 config plugin 后，运行 `npx expo prebuild` 并重新构建原生应用。构建完成后，字体将直接嵌入应用包中，无需任何运行时加载逻辑。

参考:
[Expo Font Documentation](https://docs.expo.dev/versions/latest/sdk/font/)
