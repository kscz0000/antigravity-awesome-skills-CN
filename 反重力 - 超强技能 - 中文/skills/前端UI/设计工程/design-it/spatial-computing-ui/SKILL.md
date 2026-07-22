---
name: spatial-computing-ui
description: Spatial Computing UI 的 Web 与 App 实现指南。当用户希望漂浮元素、环境感知和 Apple Vision Pro 风格时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Spatial Computing UI

> "超越 Spatial Design 的一步。在增强现实中完全 3D 漂浮的窗口。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **Z 空间层级**：不仅是投影，而是真正的 3D 距离。模态框在主窗口前方 10px 漂浮。
2. **基于凝视的交互提示**：元素在被悬停时生动地高亮，预示眼动追踪或精确指针控制。
3. **玻璃与光**：窗口是厚厚的磨砂玻璃薄片，能弯曲光线并在物理环境上投射柔和阴影。

## 视觉 DNA
- **颜色**：完全依赖背景环境。使用纯粹的半透明白色（`rgba(255,255,255,0.x)`）和黑色。
- **排版**：`SF Pro`。重度使用变化的字重（Regular、Semibold、Bold）建立层级。
- **形状**：高圆角（`24px`-`32px`）。所有元素都是圆角矩形或完美圆形。

## Web 实现
- 最好通过 CSS 3D 变换模拟用户视角来仿真。
- **CSS 示例**：
```css
body {
  /* 模拟物理房间 */
  background: url('living-room.jpg') center/cover;
  perspective: 1200px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.spatial-window {
  width: 800px;
  height: 600px;
  border-radius: 32px;
  
  /* 玻璃材质 */
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(50px) saturate(200%);
  -webkit-backdrop-filter: blur(50px) saturate(200%);
  
  /* 镜面高光 */
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 
    inset 0 1px 2px rgba(255, 255, 255, 0.8),
    0 30px 60px rgba(0, 0, 0, 0.3);
    
  /* 3D 定位 */
  transform: translateZ(-100px);
  transform-style: preserve-3d;
}

.spatial-modal {
  /* 漂浮在主窗口前方 */
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%) translateZ(50px);
  
  background: rgba(255, 255, 255, 0.6); /* 更不透明 */
  backdrop-filter: blur(30px);
  border-radius: 24px;
  padding: 30px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.spatial-btn {
  /* 凝视/悬停交互 */
  background: rgba(0,0,0,0.05);
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.spatial-btn:hover {
  background: rgba(255,255,255,0.4);
  transform: translateZ(10px) scale(1.05);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
```

## App 实现

### SwiftUI (visionOS Native / iOS emulation)
```swift
struct SpatialComputingView: View {
    var body: some View {
        ZStack {
            // 模拟房间环境
            Image("living-room")
                .resizable()
                .aspectRatio(contentMode: .fill)
                .ignoresSafeArea()
            
            // 空间窗口
            VStack(spacing: 24) {
                Text("Spatial Window")
                    .font(.title).fontWeight(.bold)
                    .foregroundColor(.white)
                
                // 凝视响应按钮
                Button(action: {}) {
                    Text("Focus Me")
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .padding(.horizontal, 32)
                        .padding(.vertical, 16)
                        // .hoverEffect() 在 visionOS/iPadOS 上很神奇
                        // .hoverEffect(.highlight)
                }
                .background(Color.black.opacity(0.2))
                .clipShape(Capsule())
            }
            .padding(60)
            // 神奇玻璃材质
            .background(.ultraThinMaterial)
            .cornerRadius(32)
            // 镜面边缘高光
            .overlay(
                RoundedRectangle(cornerRadius: 32)
                    .stroke(Color.white.opacity(0.4), lineWidth: 1)
            )
            // 环境阴影
            .shadow(color: .black.opacity(0.3), radius: 40, y: 30)
            
            // Z 空间模态框模拟（在 iOS 上）
            // 在 visionOS 上，这会是独立的窗口卷
            Text("Floating Modal")
                .foregroundColor(.white)
                .padding(30)
                .background(.thinMaterial)
                .cornerRadius(24)
                .shadow(color: .black.opacity(0.4), radius: 30, y: 20)
                .offset(x: 100, y: 100)
        }
    }
}
```
- 对基础窗口使用 `.ultraThinMaterial`，对漂浮弹出框使用 `.thinMaterial`，让它们越靠近眼睛越显得不透明。
- 如果目标平台是 iPadOS 或 visionOS，大量使用 `.hoverEffect()`。

### Flutter
```dart
import 'dart:ui';

class SpatialComputingScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: [
          // 模拟环境
          Image.asset('assets/living-room.jpg', fit: BoxFit.cover),
          
          Center(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(32),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 40.0, sigmaY: 40.0), // 大模糊
                child: Container(
                  width: 600, height: 400,
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.15), // 玻璃色调
                    borderRadius: BorderRadius.circular(32),
                    border: Border.all(color: Colors.white.withOpacity(0.4), width: 1), // 镜面高光
                    // 注意：BoxShadow 在 BackdropFilter 下不能很好渲染，除非包裹在单独的 PhysicalModel 中
                  ),
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text('Spatial Window', style: TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 32),
                        // 模拟凝视按钮
                        InkWell(
                          onTap: () {},
                          borderRadius: BorderRadius.circular(50),
                          hoverColor: Colors.white.withOpacity(0.4), // 响应鼠标/凝视
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                            decoration: BoxDecoration(color: Colors.black.withOpacity(0.2), borderRadius: BorderRadius.circular(50)),
                            child: const Text('Focus Me', style: TextStyle(color: Colors.white, fontSize: 18)),
                          ),
                        )
                      ],
                    ),
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
- 必须将 `BackdropFilter` 包裹在 `ClipRRect` 中，以给模糊的玻璃加上圆角。
- `InkWell` 上的 `hoverColor` 模拟凝视高亮。

### React Native
```jsx
// REQUIRES: @react-native-community/blur
import { BlurView } from '@react-native-community/blur';

const SpatialComputingScreen = () => {
  return (
    <ImageBackground source={{uri: 'room_bg'}} style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      
      {/* 空间窗口 */}
      <View style={{
        width: '90%', height: 400,
        shadowColor: '#000', shadowOffset: { width: 0, height: 30 },
        shadowOpacity: 0.3, shadowRadius: 40, elevation: 20
      }}>
        <BlurView
          style={{ flex: 1, borderRadius: 32, borderWidth: 1, borderColor: 'rgba(255,255,255,0.4)', padding: 40, justifyContent: 'center', alignItems: 'center' }}
          blurType="light"
          blurAmount={30}
          reducedTransparencyFallbackColor="gray"
        >
          <Text style={{ color: '#FFF', fontSize: 32, fontWeight: 'bold', marginBottom: 32 }}>
            Spatial Window
          </Text>

          {/* 模拟凝视的可点击 */}
          <TouchableOpacity style={{
            backgroundColor: 'rgba(0,0,0,0.2)', paddingVertical: 16, paddingHorizontal: 32, borderRadius: 50
          }}>
            <Text style={{ color: '#FFF', fontSize: 18, fontWeight: '600' }}>Focus Me</Text>
          </TouchableOpacity>
        </BlurView>
      </View>

    </ImageBackground>
  );
};
```
- React Native 核心无法实现背景模糊。必须安装 `@react-native-community/blur`。
- 将阴影应用到包装的 `View`，并将 `BlurView` 放在其中，配合 `borderRadius` 和 `borderWidth`。

### Jetpack Compose
```kotlin
@Composable
fun SpatialComputingScreen() {
    Box(modifier = Modifier.fillMaxSize()) {
        // 环境
        Image(painterResource(R.drawable.living_room), contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
        
        // 空间窗口
        Box(
            modifier = Modifier
                .align(Alignment.Center)
                .size(600.dp, 400.dp)
                // 注意：原生 Android 背景模糊需要 Android 12+（RenderEffect）
                .graphicsLayer {
                    renderEffect = RenderEffect.createBlurEffect(40f, 40f, Shader.TileMode.DECAL).asComposeRenderEffect()
                    clip = true
                    shape = RoundedCornerShape(32.dp)
                }
                .background(Color.White.copy(alpha = 0.15f))
                .border(1.dp, Color.White.copy(alpha = 0.4f), RoundedCornerShape(32.dp))
                .padding(40.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Spatial Window", color = Color.White, fontSize = 32.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(32.dp))
                
                // 按钮
                Box(
                    modifier = Modifier
                        .background(Color.Black.copy(alpha = 0.2f), CircleShape)
                        .clickable { }
                        .padding(horizontal = 32.dp, vertical = 16.dp)
                ) {
                    Text("Focus Me", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
    }
}
```
- 在 Android 12+ 上，使用 `RenderEffect.createBlurEffect` 应用于 `graphicsLayer` 来模糊控件*后面*的 UI。
- `border` modifier 应用亮镜面边缘，对玻璃效果至关重要。

## 推荐与避免
- **推荐**：在悬停/聚焦时营造明显的视觉冲击（尺寸增大、阴影加深）以模拟空间计算的凝视追踪交互。
- **避免**：为主窗口使用扁平、不透明的颜色。它们必须是玻璃。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。