---
name: holographic-ui
description: Holographic UI 的 Web 与 App 实现指南。当用户希望基于光的视觉、投影界面和透明漂浮元素时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Holographic UI

> "由光构成。被投影到稀薄空气中的界面，可见但完全透明。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **零透明度背景**：元素永远不是完全实心的。一切都是半透明的，让背景透出。
2. **扫描线和干涉**：通过水平扫描线、轻度色差或闪烁来营造投影的错觉。
3. **发光的边缘**：元素的边框比中心更亮，模仿激光或光投影聚焦在边缘的方式。

## 视觉 DNA
- **颜色**：几乎只使用单色的青、蓝或绿，配以白色核心高光。
- **排版**：纤细、技术性的无衬线字体。必须有发光的 `text-shadow`。
- **样式**：大量使用 `rgba()`、`mix-blend-mode: screen` 或 `add`，以及 CSS 滤镜。

## Web 实现
- **CSS 示例**：
```css
body {
  background-color: #020202; /* 必须深色才能看到全息图 */
  background-image: url('dark-lab-background.jpg');
  background-size: cover;
  color: #88ffff;
}

.hologram-panel {
  background: rgba(0, 200, 255, 0.05); /* 极度透明 */
  border: 1px solid rgba(136, 255, 255, 0.5);
  border-radius: 4px;
  padding: 30px;
  
  /* 发光边缘 */
  box-shadow: 
    inset 0 0 20px rgba(0, 200, 255, 0.2),
    0 0 15px rgba(0, 200, 255, 0.3);
    
  /* 扫描线效果 */
  background-image: linear-gradient(
    rgba(136, 255, 255, 0.1) 1px, 
    transparent 1px
  );
  background-size: 100% 4px;
}

.holo-text {
  font-family: 'Rajdhani', sans-serif;
  text-transform: uppercase;
  text-shadow: 0 0 8px rgba(136, 255, 255, 0.8);
  mix-blend-mode: screen;
}

/* 微妙的闪烁 */
.holo-flicker {
  animation: hologramFlicker 4s infinite;
}

@keyframes hologramFlicker {
  0%, 100% { opacity: 1; }
  92% { opacity: 1; }
  93% { opacity: 0.4; }
  94% { opacity: 0.9; }
  96% { opacity: 0.2; }
  98% { opacity: 1; }
}
```

## App 实现

### SwiftUI
```swift
struct HolographicUIView: View {
    @State private var isFlickering = false
    
    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            
            VStack {
                Text("HOLOGRAM ACTIVE")
                    .font(.custom("Courier", size: 24))
                    .foregroundColor(Color(hex: "88FFFF"))
                    .shadow(color: Color(hex: "88FFFF"), radius: 10)
                    .blendMode(.screen) // 光 UI 绝对必需
                
                Spacer().frame(height: 40)
                
                VStack {
                    Text("SYSTEM DIAGNOSTICS")
                        .foregroundColor(Color(hex: "88FFFF"))
                }
                .padding(30)
                .frame(maxWidth: .infinity)
                .background(Color(hex: "88FFFF").opacity(0.05))
                .border(Color(hex: "88FFFF").opacity(0.5), width: 1)
                // 发光边缘效果
                .shadow(color: Color(hex: "88FFFF").opacity(0.5), radius: 15)
                .blendMode(.screen)
                .opacity(isFlickering ? 0.4 : 1.0)
            }
            .padding()
            
            // 扫描线叠加
            LinearGradient(
                stops: [
                    .init(color: Color(hex: "88FFFF").opacity(0.1), location: 0),
                    .init(color: .clear, location: 0.5)
                ],
                startPoint: .top, endPoint: .bottom
            )
            .frame(height: 4)
            .background(Color.clear)
            // 在真实应用中，你需要使用 Image 或自定义形状平铺
            .blendMode(.screen)
        }
        .onAppear {
            // 模拟闪烁
            Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
                if Int.random(in: 1...100) > 95 {
                    isFlickering.toggle()
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                        isFlickering = false
                    }
                }
            }
        }
    }
}
```
- `.blendMode(.screen)` 绝对至关重要。它使元素表现得像投影的光。
- 堆叠多个 `.shadow()` modifier 围绕文字和边框创建发光效果。

### Flutter
```dart
class HolographicScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black, // 深色实验室背景
      body: Stack(
        children: [
          Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // 发光文字
                const Text(
                  'HOLOGRAM ACTIVE',
                  style: TextStyle(
                    fontFamily: 'Courier',
                    fontSize: 24,
                    color: Color(0xFF88FFFF),
                    shadows: [Shadow(color: Color(0xFF88FFFF), blurRadius: 10)],
                  ),
                ),
                const SizedBox(height: 40),
                
                // 全息面板
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(30),
                  decoration: BoxDecoration(
                    color: const Color(0xFF88FFFF).withOpacity(0.05),
                    border: Border.all(color: const Color(0xFF88FFFF).withOpacity(0.5)),
                    boxShadow: [
                      BoxShadow(color: const Color(0xFF88FFFF).withOpacity(0.2), blurRadius: 15, spreadRadius: 5),
                    ],
                  ),
                  child: const Text(
                    'SYSTEM DIAGNOSTICS',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Color(0xFF88FFFF)),
                  ),
                ),
              ],
            ),
          ),
          // 扫描线（IgnorePointer 防止阻挡点击）
          IgnorePointer(
            child: ShaderMask(
              blendMode: BlendMode.screen, // 表现得像光
              shaderCallback: (bounds) => const LinearGradient(
                begin: Alignment.topCenter, end: Alignment.bottomCenter,
                stops: [0.0, 0.5, 0.5, 1.0],
                colors: [Colors.black12, Colors.black12, Colors.transparent, Colors.transparent],
              ).createShader(bounds),
              // 要在 Flutter 中真正平铺，通常需要 CustomPainter。
              // 这里我们模拟混合模式。
              child: Container(color: const Color(0xFF88FFFF).withOpacity(0.1)),
            ),
          ),
        ],
      ),
    );
  }
}
```
- `TextStyle` 内的 `Shadow` 数组创建发光文字。
- 带 `spreadRadius` 的 `BoxShadow` 创建发光面板边框。
- 叠加在 UI 上方的 `ShaderMask` 配合 `BlendMode.screen` 赋予它光投影的质感。

### React Native
```jsx
const HolographicScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#020202', padding: 24, justifyContent: 'center' }}>
      
      <Text style={{
        fontFamily: 'monospace', fontSize: 24, textAlign: 'center', color: '#88FFFF',
        textShadowColor: '#88FFFF', textShadowRadius: 10, marginBottom: 40
      }}>
        HOLOGRAM ACTIVE
      </Text>

      <View style={{
        backgroundColor: 'rgba(0, 200, 255, 0.05)',
        borderWidth: 1, borderColor: 'rgba(136, 255, 255, 0.5)',
        padding: 30, borderRadius: 4,
        // 发光边缘
        shadowColor: '#88FFFF', shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.5, shadowRadius: 15, elevation: 10
      }}>
        <Text style={{ color: '#88FFFF', textAlign: 'center', fontFamily: 'monospace' }}>
          SYSTEM DIAGNOSTICS
        </Text>
      </View>

      {/* 伪扫描线叠加。在真实应用中，使用平铺的 Image 背景。 */}
      <View pointerEvents="none" style={{
        position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
        backgroundColor: 'rgba(136, 255, 255, 0.03)',
      }} />

    </View>
  );
};
```
- React Native 默认不支持 `mix-blend-mode`，因此必须重度依赖低透明度背景和强烈的 `textShadow` / `shadowRadius`。
- 在扫描线叠加层上使用 `pointerEvents="none"`，使其不阻挡用户交互。

### Jetpack Compose
```kotlin
@Composable
fun HolographicScreen() {
    Box(modifier = Modifier.fillMaxSize().background(Color(0xFF020202))) {
        Column(
            modifier = Modifier.fillMaxSize().padding(24.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // 发光文字
            Text(
                text = "HOLOGRAM ACTIVE",
                fontFamily = FontFamily.Monospace,
                fontSize = 24.sp,
                color = Color(0xFF88FFFF),
                style = TextStyle(
                    shadow = Shadow(color = Color(0xFF88FFFF), blurRadius = 10f)
                ),
                modifier = Modifier.graphicsLayer { blendMode = BlendMode.Screen }
            )
            
            Spacer(Modifier.height(40.dp))
            
            // 发光面板
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .graphicsLayer { blendMode = BlendMode.Screen }
                    .shadow(15.dp, ambientColor = Color(0xFF88FFFF), spotColor = Color(0xFF88FFFF))
                    .background(Color(0xFF88FFFF).copy(alpha = 0.05f))
                    .border(1.dp, Color(0xFF88FFFF).copy(alpha = 0.5f))
                    .padding(30.dp),
                contentAlignment = Alignment.Center
            ) {
                Text("SYSTEM DIAGNOSTICS", color = Color(0xFF88FFFF), fontFamily = FontFamily.Monospace)
            }
        }
        
        // 模拟扫描线叠加
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0xFF88FFFF).copy(alpha = 0.03f))
        )
    }
}
```
- `Modifier.graphicsLayer { blendMode = BlendMode.Screen }` 正是在 Compose 中让元素表现得像投影光的关键。
- 对 Compose 的 `shadow` modifier 使用 `ambientColor` 和 `spotColor` 设为青色，使面板发光。

## 推荐与避免
- **推荐**：使用 `mix-blend-mode: screen`（Web）或附加混合，让重叠的全息面板在交叉处变得更亮。
- **避免**：对 UI 元素使用任何深色或投影。阴影在光投影中不存在。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。