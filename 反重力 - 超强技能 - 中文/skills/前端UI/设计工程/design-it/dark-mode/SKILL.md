---
name: dark-mode
description: Dark Mode Design 的 Web 与 App 实现指南。当用户需要暗色界面、减轻眼疲劳和高级精致美学时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Dark Mode Design

> "不仅仅是反色。而是在深色之上精心构建的光的层级。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **绝不纯黑**：真正的 `#000000` 在 OLED 屏幕上会导致涂抹感，搭配白字也会极度刺眼。使用深灰色（如 `#121212` 或 `#0A0A0A`）。
2. **通过明度表达层级**：在浅色模式中，阴影表现层级。在暗色模式中阴影不可见，因此凸起的表面必须比背景更浅。
3. **降低饱和度的强调色**：饱和色在深色背景上会刺眼地闪烁。需要降低品牌色的饱和度。

## 视觉 DNA
- **颜色**：**Midnight Luxury** 或 **Minimalist Slate**（反色）。背景 `#121212`。凸起的卡片 `#1E1E1E`、`#252525`。主文字 `#E1E1E1`（而非 `#FFFFFF`）。
- **排版**：标准的高可读性无衬线字体，但通常比浅色模式降低一个字重，因为在深色背景上浅色文字在视觉上显得更粗。
- **阴影**：纯黑阴影，但使用更低的不透明度，主要用于分隔略有差异的灰色。

## Web 实现
- **CSS 示例**：
```css
:root {
  --bg-base: #121212;
  --bg-elevated-1: #1E1E1E;
  --bg-elevated-2: #242424;
  --text-high-emphasis: rgba(255, 255, 255, 0.87);
  --text-medium-emphasis: rgba(255, 255, 255, 0.60);
  
  /* 强调色：降低饱和度的紫色，而非亮紫色 */
  --accent-color: #BB86FC; 
}

body {
  background-color: var(--bg-base);
  color: var(--text-high-emphasis);
  font-weight: 300; /* 暗色模式使用更细的字重 */
}

.dark-card {
  background-color: var(--bg-elevated-1);
  border-radius: 8px;
  padding: 24px;
  
  /* 极细微的边框有助于分隔暗色表面 */
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.dark-card:hover {
  /* 悬停时元素靠近用户，因此变得更浅 */
  background-color: var(--bg-elevated-2);
}

.dark-btn {
  background-color: var(--accent-color);
  color: #000; /* 暗色文字配浅色强调色，高可读 */
  font-weight: 600;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
}
```

## App 实现

### SwiftUI
```swift
struct DarkModeView: View {
    // 强制此视图进入 Dark Mode（或使用系统设置）
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // 主凸起卡片
                VStack(alignment: .leading, spacing: 12) {
                    Text("Elevation via Lightness")
                        .font(.headline)
                        .foregroundColor(.primary) // 自动适配
                    Text("In dark mode, elevated surfaces are lighter grey, not shadowed.")
                        .font(.subheadline)
                        .foregroundColor(.secondary) // 自动适配
                }
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                // 使用原生语义色。.secondarySystemBackground 浅于 .systemBackground
                .background(Color(UIColor.secondarySystemBackground))
                .cornerRadius(12)
                
                // 降低饱和度的强调按钮
                Button(action: {}) {
                    Text("Desaturated Accent")
                        .fontWeight(.semibold)
                        .foregroundColor(.black) // 暗色文字配浅色强调色
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color(red: 0.73, green: 0.52, blue: 0.98)) // #BB86FC（降低饱和度的紫色）
                        .cornerRadius(8)
                }
            }
            .padding()
        }
        // #121212 是标准暗色模式背景，systemBackground 与之接近
        .background(Color(UIColor.systemBackground))
    }
}
// .preferredColorScheme(.dark) 来强制
```
- **依赖语义色**：SwiftUI 的 `Color.primary`、`Color.secondary`、`Color(UIColor.systemBackground)` 和 `Color(UIColor.secondarySystemBackground)` 自动处理完美的暗色模式过渡。
- 除非你构建自定义主题的应用，否则避免为背景强制使用明确的十六进制色。

### Flutter
```dart
import 'package:flutter/material.dart';

class DarkModeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // 配置暗色主题
      themeMode: ThemeMode.dark,
      darkTheme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF121212), // 标准暗色背景
        cardColor: const Color(0xFF1E1E1E), // 凸起表面
        colorScheme: const ColorScheme.dark().copyWith(
          primary: const Color(0xFFBB86FC), // 降低饱和度的强调色
          onPrimary: Colors.black, // 暗色文字配浅色强调色
          surface: const Color(0xFF1E1E1E),
        ),
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Dark Mode', style: TextStyle(color: Colors.white70))),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Card(
              elevation: 0, // 阴影在暗色下效果不佳
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(color: Colors.white.withOpacity(0.05)), // 细微边框
              ),
              child: const Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Elevation via Lightness', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    SizedBox(height: 8),
                    Text('Elevated surfaces use lighter greys.', style: TextStyle(color: Colors.white60)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {},
              child: const Text('Desaturated Accent'),
            ),
          ],
        ),
      ),
    );
  }
}
```
- 使用 `ThemeData.dark()` 时，主动覆盖 `scaffoldBackgroundColor` 为 `#121212`，`cardColor` 为 `#1E1E1E`。
- 确保 `colorScheme.onPrimary` 为黑色，以便在降低饱和度的浅色强调按钮上放置文字时清晰可读。

### React Native
```jsx
import { useColorScheme } from 'react-native';

const DarkModeScreen = () => {
  const isDark = useColorScheme() === 'dark';
  
  // 自定义暗色主题字典
  const theme = {
    bgBase: isDark ? '#121212' : '#FFFFFF',
    bgElevated: isDark ? '#1E1E1E' : '#F5F5F5',
    textHigh: isDark ? 'rgba(255, 255, 255, 0.87)' : 'rgba(0, 0, 0, 0.87)',
    textMedium: isDark ? 'rgba(255, 255, 255, 0.60)' : 'rgba(0, 0, 0, 0.60)',
    accent: isDark ? '#BB86FC' : '#6200EE', // 暗色降低饱和度，亮色更鲜艳
    onAccent: isDark ? '#000' : '#FFF',
  };

  return (
    <View style={{ flex: 1, backgroundColor: theme.bgBase, padding: 16 }}>
      <View style={{
        backgroundColor: theme.bgElevated,
        padding: 24,
        borderRadius: 12,
        borderWidth: isDark ? 1 : 0,
        borderColor: 'rgba(255,255,255,0.05)',
        marginBottom: 20
      }}>
        <Text style={{ color: theme.textHigh, fontSize: 18, fontWeight: 'bold', marginBottom: 8 }}>
          Elevation via Lightness
        </Text>
        <Text style={{ color: theme.textMedium }}>
          Elevated surfaces use lighter greys.
        </Text>
      </View>

      <TouchableOpacity style={{
        backgroundColor: theme.accent,
        padding: 16,
        borderRadius: 8,
        alignItems: 'center'
      }}>
        <Text style={{ color: theme.onAccent, fontWeight: 'bold' }}>Desaturated Accent</Text>
      </TouchableOpacity>
    </View>
  );
};
```
- 依赖 React Native 的 `useColorScheme()` 钩子。
- 定义严格的颜色 token 字典。注意 `theme.accent` 从亮色模式的鲜艳紫色（`#6200EE`）过渡到暗色模式的柔和淡紫色（`#BB86FC`）。

### Jetpack Compose
```kotlin
@Composable
fun DarkModeScreen() {
    // 通常此逻辑写在你的 Theme.kt 中
    val darkColors = darkColorScheme(
        background = Color(0xFF121212),
        surface = Color(0xFF1E1E1E),
        primary = Color(0xFFBB86FC),
        onPrimary = Color.Black,
        onBackground = Color.White.copy(alpha = 0.87f),
        onSurface = Color.White.copy(alpha = 0.87f)
    )

    MaterialTheme(colorScheme = darkColors) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(16.dp)
        ) {
            Card(
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                shape = RoundedCornerShape(12.dp),
                border = BorderStroke(1.dp, Color.White.copy(alpha = 0.05f))
            ) {
                Column(modifier = Modifier.padding(24.dp)) {
                    Text(
                        text = "Elevation via Lightness", 
                        style = MaterialTheme.typography.titleMedium, 
                        color = MaterialTheme.colorScheme.onSurface)
                    Spacer(Modifier.height(8.dp))
                    Text(
                        text = "Elevated surfaces use lighter greys.", 
                        style = MaterialTheme.typography.bodyMedium, 
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                }
            }
            
            Spacer(Modifier.height(20.dp))
            
            Button(
                onClick = {},
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary
                ),
                modifier = Modifier.fillMaxWidth().height(50.dp)
            ) {
                Text("Desaturated Accent", fontWeight = FontWeight.Bold)
            }
        }
    }
}
```
- Material 3 完美处理暗色模式语义。定义你的 `darkColorScheme`。
- 对 `surface` 使用 `Color(0xFF1E1E1E)`，对 `background` 使用 `Color(0xFF121212)`。Compose 会自动将这些映射到 `Card` 和 Scaffold。

## 推荐与避免
- **推荐**：满足 WCAG 对比度标准。仅因为是暗色，不代表文字可以暗到看不清。
- **避免**：使用鲜艳、高饱和度的原色。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。