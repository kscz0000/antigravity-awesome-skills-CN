---
name: isometric-design
description: Isometric Design 的 Web 与 App 实现指南。当用户希望无消失点的角度 3D 视觉时触发，常用于技术插图。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Isometric Design

> "建筑师的视角。平行投影中深度恒定且平行线永不汇聚。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **平行线**：与真正的 3D 不同，等距投影没有消失点。一切都从精确的 30 度角观察。
2. **自顶向下、倾斜视角**：经典的"模拟城市"视角。
3. **块状建筑**：UI 元素通常看起来像城市街区或堆叠的瓦片。

## 视觉 DNA
- **颜色**：**Warm Tech** 或 **Earth-Grounded Elegance**。等距设计常看起来像实物模型，因此柔和、真实的颜色效果很好。
- **排版**：保持文字与屏幕齐平，或完美映射到等距平面（顶部、左侧、右侧）。
- **阴影**：生硬、长的投影以精确角度（通常是 -45 或 45 度）投射。

## Web 实现
- CSS 变换非常适合此场景。结合 `rotateX(60deg)` 和 `rotateZ(-45deg)`。
- **CSS 示例**：
```css
.isometric-grid {
  /* 基础 */
  transform-style: preserve-3d;
  transform: rotateX(60deg) rotateZ(-45deg);
}

.iso-block {
  width: 100px;
  height: 100px;
  background-color: var(--secondary-base);
  position: relative;
  transition: transform 0.3s;
}

/* 使用伪元素创建 3D 块 */
.iso-block::before {
  content: '';
  position: absolute;
  width: 20px; /* 深度 */
  height: 100%;
  background-color: var(--primary-text); /* 较深色调作为侧面 */
  right: 100%;
  transform-origin: right;
  transform: skewY(-45deg);
}

.iso-block::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 20px; /* 深度 */
  background-color: var(--cta-highlight); /* 最浅色调作为顶/底 */
  top: 100%;
  transform-origin: top;
  transform: skewX(-45deg);
}

.iso-block:hover {
  transform: translateZ(20px) translate(-10px, -10px);
}
```

## App 实现

### SwiftUI
```swift
struct IsometricView: View {
    var body: some View {
        ZStack {
            Color.white.ignoresSafeArea()
            
            // 等距堆叠
            VStack(spacing: 0) {
                // 顶层
                Rectangle()
                    .fill(Color.blue)
                    .frame(width: 150, height: 150)
                    .overlay(Text("TOP").foregroundColor(.white))
                
                // 阴影模拟
                Rectangle()
                    .fill(Color.black.opacity(0.2))
                    .frame(width: 150, height: 20)
            }
            // 等距投影的精确 3D 变换
            .rotationEffect(.degrees(-45))
            .rotation3DEffect(.degrees(60), axis: (x: 1, y: 0, z: 0))
        }
    }
}
```
- SwiftUI 的 `.rotation3DEffect` 让这一切变得出奇简单。先通过 `.rotationEffect` 将 Z 轴旋转 -45 度，再将 X 轴旋转 60 度。
- 可以沿 Z 轴堆叠多个视图（或在 3D 旋转之前用 Y 偏移模拟），创建高耸的等距城市街区。

### Flutter
```dart
import 'dart:math';

class IsometricScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Transform(
          // 等距矩阵
          alignment: FractionalOffset.center,
          transform: Matrix4.identity()
            ..setEntry(3, 2, 0.001) // 透视
            ..rotateX(pi / 3) // 60 度
            ..rotateZ(-pi / 4), // -45 度
          child: Container(
            width: 150,
            height: 150,
            decoration: BoxDecoration(
              color: Colors.blue,
              boxShadow: [
                // 生硬的等距投影
                BoxShadow(
                  color: Colors.black.withOpacity(0.3),
                  offset: const Offset(20, 20),
                  blurRadius: 0, // 等距无模糊
                ),
              ],
            ),
            child: const Center(child: Text('ISO BLOCK', style: TextStyle(color: Colors.white))),
          ),
        ),
      ),
    );
  }
}
```
- Flutter 需要带 `Matrix4` 的 `Transform`。应用 `rotateX` 和 `rotateZ` 即可生成经典的等距网格。
- 等距阴影通常完全生硬（`blurRadius: 0`），并沿网格轴完美偏移。

### React Native
```jsx
const IsometricScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#FFF', justifyContent: 'center', alignItems: 'center' }}>
      
      <View style={{
        width: 150,
        height: 150,
        backgroundColor: '#2196F3',
        justifyContent: 'center',
        alignItems: 'center',
        
        // 等距变换
        transform: [
          { rotateX: '60deg' },
          { rotateZ: '-45deg' }
        ],
        
        // 生硬的等距阴影
        shadowColor: '#000',
        shadowOffset: { width: 20, height: 20 },
        shadowOpacity: 0.3,
        shadowRadius: 0, // 生硬边缘
        elevation: 10,
      }}>
        <Text style={{ color: '#FFF', fontWeight: 'bold' }}>ISO BLOCK</Text>
      </View>
      
    </View>
  );
};
```
- `transform` 数组按顺序处理。先应用 `rotateX`，再应用 `rotateZ`。
- 生硬阴影（`shadowRadius: 0`）带来插图感。

### Jetpack Compose
```kotlin
@Composable
fun IsometricScreen() {
    Box(
        modifier = Modifier.fillMaxSize().background(Color.White),
        contentAlignment = Alignment.Center
    ) {
        Box(
            modifier = Modifier
                .graphicsLayer {
                    // 等距变换
                    rotationX = 60f
                    rotationZ = -45f
                    // 如果被裁剪，添加细微的缩放
                    scaleX = 0.8f
                    scaleY = 0.8f
                }
                .size(150.dp)
                // 在盒子后面绘制生硬阴影
                .drawBehind {
                    drawRect(
                        color = Color.Black.copy(alpha = 0.3f),
                        topLeft = Offset(40f, 40f), // 等距偏移
                        size = size
                    )
                }
                .background(Color(0xFF2196F3)),
            contentAlignment = Alignment.Center
        ) {
            Text("ISO BLOCK", color = Color.White, fontWeight = FontWeight.Bold)
        }
    }
}
```
- 使用 `Modifier.graphicsLayer` 应用 `rotationX` 和 `rotationZ`。
- 要在 Compose 中获得真正的生硬等距投影而不被凸起模糊，使用 `Modifier.drawBehind` 手动绘制一个从主内容偏移的深色矩形。

## 推荐与避免
- **推荐**：将其用于信息图表、功能图或主视觉区块。
- **避免**：将整个应用的功能性 UI 都建成等距投影。交互起来太难。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。