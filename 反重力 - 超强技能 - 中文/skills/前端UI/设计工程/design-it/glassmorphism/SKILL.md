---
name: glassmorphism
description: Glassmorphism 的 Web 与 App 实现指南。当用户需要毛玻璃效果、模糊背景、透明度或类似 macOS 的精致质感时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Glassmorphism

> "透过磨砂窗户窥视。界面与鲜艳背景无缝融合。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **背景模糊（Backdrop Filter）**：最核心的特征。元素模糊其下方的所有内容。
2. **半透明白色/深色背景**：面板使用 rgba() 颜色，让背景穿透。
3. **细微的亮色边框**：1px 半透明白色（或浅色）边框，模拟玻璃边缘捕捉光线。

## 视觉 DNA
- **颜色**：需要鲜艳或带纹理的背景（如渐变、抽象网格或照片）。在有底层视觉纹理的情况下，搭配 **Yacht Club** 或 **Earth-Grounded Elegance** 效果极佳。
- **排版**：干净的几何无衬线字体。高对比度文字（纯白或纯黑）以保证在玻璃上的可读性。
- **阴影**：柔和、细微的投影，使玻璃面板从背景中脱离出来。

## Web 实现
- 大量依赖 `backdrop-filter: blur()`。
- **CSS 示例**：
```css
body {
  /* 需要复杂的背景才能看到玻璃效果 */
  background: url('abstract-mesh.jpg') cover; 
}

.glass-panel {
  background: rgba(255, 255, 255, 0.15); /* 浅色玻璃 */
  /* 或者 background: rgba(0, 0, 0, 0.25); 用于深色玻璃 */
  
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  
  border: 1px solid rgba(255, 255, 255, 0.3); /* 玻璃边缘 */
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  
  padding: 32px;
}
```

## App 实现

### SwiftUI
```swift
struct GlassCard: View {
    var body: some View {
        ZStack {
            // 需要鲜艳的背景才能展示玻璃效果
            LinearGradient(
                colors: [.purple, .blue, .cyan],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            // 玻璃面板
            VStack(alignment: .leading, spacing: 16) {
                Text("Glass Panel")
                    .font(.system(size: 22, weight: .semibold))
                    .foregroundColor(.white)
                Text("Content floating on frosted glass.")
                    .font(.system(size: 15))
                    .foregroundColor(.white.opacity(0.8))
                
                Button(action: {}) {
                    Text("Continue")
                        .font(.system(size: 15, weight: .semibold))
                        .foregroundColor(.white)
                        .padding(.horizontal, 24)
                        .padding(.vertical, 12)
                        .background(.ultraThinMaterial)
                        .cornerRadius(8)
                }
            }
            .padding(24)
            .background(.ultraThinMaterial)  // 内置的毛玻璃
            .cornerRadius(16)
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(.white.opacity(0.3), lineWidth: 1) // 玻璃边缘高光
            )
            .shadow(color: .black.opacity(0.1), radius: 20, x: 0, y: 10)
            .padding(24)
        }
    }
}
```
- 使用 `.ultraThinMaterial`、`.thinMaterial`、`.regularMaterial`、`.thickMaterial`——Apple 原生支持玻璃态效果。
- 添加 `.overlay(RoundedRectangle().stroke(.white.opacity(0.3)))` 以呈现玻璃边缘高光。
- 只有在玻璃后方有鲜艳背景可见时，玻璃效果才会显现。

### Flutter
```dart
class GlassCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // 鲜艳背景
        Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Colors.purple, Colors.blue, Colors.cyan],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
        ),
        // 玻璃面板
        Center(
          child: ClipRRect(
            borderRadius: BorderRadius.circular(16),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 16, sigmaY: 16),
              child: Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: Colors.white.withOpacity(0.3),
                    width: 1,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 20,
                      offset: const Offset(0, 10),
                    ),
                  ],
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Glass Panel',
                      style: TextStyle(fontSize: 22, fontWeight: FontWeight.w600,
                        color: Colors.white)),
                    const SizedBox(height: 16),
                    Text('Content floating on frosted glass.',
                      style: TextStyle(fontSize: 15,
                        color: Colors.white.withOpacity(0.8))),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
```
- **关键**：`BackdropFilter` 必须包裹在 `ClipRRect` 中——没有裁剪，模糊会应用到整个屏幕。
- 使用 `ImageFilter.blur(sigmaX: 10...20, sigmaY: 10...20)` 实现磨砂效果。
- 将容器颜色设置为 `Colors.white.withOpacity(0.1...0.2)`——过高的不透明度会破坏玻璃质感。

### React Native
```jsx
import { BlurView } from '@react-native-community/blur';

const GlassCard = () => (
  <View style={{ flex: 1 }}>
    {/* 鲜艳背景 */}
    <LinearGradient
      colors={['#9B59B6', '#3498DB', '#1ABC9C']}
      style={StyleSheet.absoluteFill}
    />
    
    {/* 玻璃面板 */}
    <View style={{
      margin: 24,
      borderRadius: 16,
      overflow: 'hidden', // 模糊裁剪所必需
    }}>
      <BlurView
        blurType="light"
        blurAmount={16}
        style={{ padding: 24 }}
      >
        <View style={{
          // 玻璃边框叠加
          borderRadius: 16,
          borderWidth: 1,
          borderColor: 'rgba(255,255,255,0.3)',
        }}>
          <Text style={{
            fontSize: 22, fontWeight: '600', color: '#FFF',
            marginBottom: 16,
          }}>
            Glass Panel
          </Text>
          <Text style={{
            fontSize: 15, color: 'rgba(255,255,255,0.8)',
          }}>
            Content floating on frosted glass.
          </Text>
        </View>
      </BlurView>
    </View>
  </View>
);
```
- 安装 `@react-native-community/blur`——React Native 本身不支持原生模糊。
- 用一个带有 `overflow: 'hidden'` 和 `borderRadius` 的 `View` 包裹 `BlurView` 的父容器，以裁剪模糊。
- 使用 `blurType: 'light'` 表示浅色玻璃，`'dark'` 表示深色玻璃，`'chromeMaterial'` 表示 iOS Chrome 效果。
- **Android 限制**：`BlurView` 在 Android 上的性能表现不一，需要充分测试。

### Jetpack Compose
```kotlin
@Composable
fun GlassCard() {
    Box(modifier = Modifier.fillMaxSize()) {
        // 鲜艳背景
        Box(modifier = Modifier
            .fillMaxSize()
            .background(Brush.linearGradient(
                colors = listOf(Color(0xFF9B59B6), Color(0xFF3498DB), Color(0xFF1ABC9C)),
                start = Offset.Zero,
                end = Offset.Infinite,
            ))
        )
        
        // 玻璃面板 — Compose 没有原生 backdrop-filter，
        // 因此使用半透明 surface 并通过 Modifier.blur() 模糊
        Card(
            modifier = Modifier
                .padding(24.dp)
                .align(Alignment.Center),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = Color.White.copy(alpha = 0.15f),
            ),
            border = BorderStroke(1.dp, Color.White.copy(alpha = 0.3f)),
            elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
        ) {
            Column(modifier = Modifier.padding(24.dp)) {
                Text("Glass Panel",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = Color.White)
                Spacer(Modifier.height(16.dp))
                Text("Content floating on frosted glass.",
                    fontSize = 15.sp,
                    color = Color.White.copy(alpha = 0.8f))
            }
        }
    }
}
```
- **Compose 限制**：真正的 `backdrop-filter` 模糊在 Compose 中不存在。可以使用 `Modifier.blur()`（API 31+）对背景进行模糊，或使用 `RenderEffect.createBlurEffect()` 兼容更低 API。
- 使用 `haze` 库（`dev.chrisbanes.haze`）在 Compose 中实现真正的玻璃态——它提供 `Modifier.haze()` 和 `Modifier.hazeChild()`。
- 没有原生模糊时，可回退到 `Color.White.copy(alpha = 0.15f)` 配合粗边框来模拟玻璃边缘。

## 推荐与避免
- **推荐**：确保文字与模糊背景之间有足够的对比度。可访问性是这种风格的常见挑战。
- **避免**：在纯白或纯黑背景上使用 Glassmorphism——效果将完全不可见。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。