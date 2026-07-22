---
name: spatial-design
description: Spatial Design 的 Web 与 App 实现指南。当用户希望环境感知布局、Apple Vision Pro 启发或混合现实美学时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Spatial Design

> "属于房间中的 UI。透明、玻璃般的面板，对物理空间的光照做出反应。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **环境透明性**：UI 表现得像玻璃窗。重度依赖背景模糊，但特别旨在让环境（或模拟的环境图像）决定氛围。
2. **动态光照**：元素响应光标位置，仿佛有一束光照在上面。
3. **微妙的体积**：不是扁平的，但也不是极度的 3D。元素边缘有非常薄的光环（镜面高光）。

## 视觉 DNA
- **颜色**：几乎只使用 `rgba()` 白色或黑色。实际颜色完全来自背景环境。
- **排版**：极其清晰，高可读性。经常使用变化的字重建立层级而不依赖颜色。Apple 的 `SF Pro` 是这里的标准。
- **图标**：描边、高可读性的字形。

## Web 实现
- **CSS 示例**：
```css
body {
  /* 需要复杂的背景才能达到效果 */
  background: url('room-environment.jpg') cover;
}

.spatial-panel {
  /* 核心材质 */
  background: rgba(255, 255, 255, 0.2); /* 非常透明 */
  backdrop-filter: blur(40px) saturate(150%);
  -webkit-backdrop-filter: blur(40px) saturate(150%);
  
  border-radius: 32px;
  padding: 40px;
  
  /* 镜面边缘光 */
  box-shadow: 
    inset 0 1px 1px rgba(255,255,255,0.6),
    inset 0 0 1px 1px rgba(255,255,255,0.2),
    0 24px 48px rgba(0,0,0,0.1);
}

.spatial-btn {
  background: rgba(0,0,0,0.1);
  color: white;
  border-radius: 20px;
  padding: 12px 24px;
  backdrop-filter: blur(10px);
  transition: all 0.2s;
}

.spatial-btn:hover {
  background: rgba(255,255,255,0.2);
  /* 高亮效果 */
  box-shadow: inset 0 0 20px rgba(255,255,255,0.4);
}
```

## App 实现

### SwiftUI
```swift
struct SpatialDesignView: View {
    var body: some View {
        ZStack {
            // 环境背景
            Image("room-environment")
                .resizable()
                .aspectRatio(contentMode: .fill)
                .ignoresSafeArea()
            
            // 空间面板
            VStack(spacing: 24) {
                Text("Environmental UI")
                    .font(.title).fontWeight(.bold)
                    .foregroundColor(.white)
                
                Button(action: {}) {
                    Text("Interact")
                        .foregroundColor(.white)
                        .padding(.horizontal, 32)
                        .padding(.vertical, 16)
                }
                .background(.ultraThinMaterial)
                .clipShape(Capsule())
                .overlay(Capsule().stroke(Color.white.opacity(0.3), lineWidth: 1))
            }
            .padding(40)
            .background(.ultraThinMaterial) // 核心空间材质
            .cornerRadius(32)
            // 镜面边缘光
            .overlay(
                RoundedRectangle(cornerRadius: 32)
                    .stroke(
                        LinearGradient(
                            colors: [.white.opacity(0.6), .white.opacity(0.1)],
                            startPoint: .topLeading, endPoint: .bottomTrailing
                        ), 
                        lineWidth: 1
                    )
            )
            // 非常柔和、弥散的投影
            .shadow(color: .black.opacity(0.1), radius: 40, y: 20)
        }
    }
}
```
- `.background(.ultraThinMaterial)` 正是 Apple 用于这种美学的材质。
- 镜面高光至关重要。使用 `.overlay` 配合 `LinearGradient` 描边模拟光源击中玻璃面板的左上边缘。

### Flutter
```dart
import 'dart:ui';

class SpatialDesignScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: [
          Image.asset('assets/room-environment.jpg', fit: BoxFit.cover),
          
          Center(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(32),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 30.0, sigmaY: 30.0),
                child: Container(
                  width: 350,
                  padding: const EdgeInsets.all(40),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(32),
                    // 镜面边缘光
                    border: Border.all(color: Colors.white.withOpacity(0.4), width: 1),
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text('Environmental UI', style: TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 32),
                      
                      // 空间按钮
                      ClipRRect(
                        borderRadius: BorderRadius.circular(50),
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 10.0, sigmaY: 10.0),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.1),
                              border: Border.all(color: Colors.white.withOpacity(0.2)),
                              borderRadius: BorderRadius.circular(50),
                            ),
                            child: const Text('Interact', style: TextStyle(color: Colors.white)),
                          ),
                        ),
                      )
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```
- `BackdropFilter` 是模糊背景所必需的。
- 注意面板*内*的按钮也有 `BackdropFilter`。这创造了嵌套玻璃，是 Spatial Design 的标志。

### React Native
```jsx
// 需要 @react-native-community/blur
import { BlurView } from '@react-native-community/blur';

const SpatialDesignScreen = () => {
  return (
    <ImageBackground source={{uri: 'room_bg'}} style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      
      <View style={{ width: '85%', shadowColor: '#000', shadowOffset: { width: 0, height: 20 }, shadowOpacity: 0.1, shadowRadius: 40, elevation: 10 }}>
        <BlurView
          style={{ borderRadius: 32, borderWidth: 1, borderColor: 'rgba(255,255,255,0.4)', padding: 40, alignItems: 'center' }}
          blurType="light"
          blurAmount={20}
        >
          <Text style={{ color: '#FFF', fontSize: 28, fontWeight: 'bold', marginBottom: 32 }}>
            Environmental UI
          </Text>

          <View style={{ borderRadius: 50, overflow: 'hidden' }}>
            <BlurView blurType="dark" blurAmount={10} style={{ paddingVertical: 16, paddingHorizontal: 32, borderWidth: 1, borderColor: 'rgba(255,255,255,0.2)' }}>
              <Text style={{ color: '#FFF', fontSize: 16 }}>Interact</Text>
            </BlurView>
          </View>
        </BlurView>
      </View>

    </ImageBackground>
  );
};
```
- `@react-native-community/blur` 的 `BlurView` 是唯一的方法。
- 主面板使用 `blurType="light"`，按钮使用 `blurType="dark"`，在玻璃层之间形成对比。

### Jetpack Compose
```kotlin
@Composable
fun SpatialDesignScreen() {
    Box(modifier = Modifier.fillMaxSize()) {
        Image(painterResource(R.drawable.room_environment), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
        
        Box(
            modifier = Modifier
                .align(Alignment.Center)
                .width(350.dp)
                // 阴影放在外面
                .shadow(20.dp, RoundedCornerShape(32.dp), spotColor = Color.Black.copy(alpha = 0.1f))
                // Android 12+ 模糊
                .graphicsLayer {
                    renderEffect = RenderEffect.createBlurEffect(30f, 30f, Shader.TileMode.DECAL).asComposeRenderEffect()
                    clip = true
                    shape = RoundedCornerShape(32.dp)
                }
                .background(Color.White.copy(alpha = 0.1f))
                .border(1.dp, Brush.linearGradient(listOf(Color.White.copy(alpha = 0.6f), Color.Transparent)), RoundedCornerShape(32.dp))
                .padding(40.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Environmental UI", color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(32.dp))
                
                // 按钮
                Box(
                    modifier = Modifier
                        .background(Color.Black.copy(alpha = 0.1f), CircleShape)
                        .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                        .padding(horizontal = 32.dp, vertical = 16.dp)
                ) {
                    Text("Interact", color = Color.White)
                }
            }
        }
    }
}
```
- 应用于 `Modifier.border` 的 `Brush.linearGradient` 完美地模拟了从顶部击中厚玻璃板的光线。

## 推荐与避免
- **推荐**：拉满 `backdrop-filter` 的 `saturate()`，让背景颜色透过玻璃更鲜艳。
- **避免**：使用深色、不透明的投影。UI 应该看起来像玻璃，不会投射生硬的阴影。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。