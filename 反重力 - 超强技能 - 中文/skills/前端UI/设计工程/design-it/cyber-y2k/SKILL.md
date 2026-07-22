---
name: cyber-y2k
description: Cyber Y2K 的 Web 与 App 实现指南。当用户需要现代 Y2K、全息视觉和故障美学时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Cyber Y2K

> "Y2K，但通过扭曲的现代视角呈现。更暗、更故障、更具全息感。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **全息渐变**：虹彩、油膜般的色彩调色板，会随着观察角度变化。
2. **故障艺术**：文字或图像看似损坏、分离成 RGB 通道、或出现抖动。
3. **部落与部落科技矢量**：尖锐、激进的矢量图形（想想 2000 年代早期的部落纹身与电路板的结合）。

## 视觉 DNA
- **颜色**：深黑色背景。高光部分是全息的（紫色、青色、酸橙绿、热粉色混合成流动的渐变）。
- **排版**：极度粗壮、拉伸的字体，或高度技术性的等宽字体。
- **视觉**：CD-ROM 反射、铁丝网图案和强烈的色差。

## Web 实现
- 使用 CSS 动画实现故障效果和动画背景渐变。
- **CSS 示例**：
```css
body {
  background-color: #050505;
  color: #fff;
}

/* 全息按钮 */
.cyber-y2k-btn {
  background: linear-gradient(124deg, #ff2400, #e81d1d, #e8b71d, #e3e81d, #1de840, #1ddde8, #2b1de8, #dd00f3, #dd00f3);
  background-size: 1800% 1800%;
  animation: rainbow 18s ease infinite;
  
  color: #fff;
  font-weight: 900;
  text-transform: uppercase;
  border: 1px solid rgba(255,255,255,0.5);
  border-radius: 30px;
  padding: 16px 32px;
  mix-blend-mode: screen; /* 让它与背景交互 */
}

@keyframes rainbow { 
  0%{background-position:0% 82%}
  50%{background-position:100% 19%}
  100%{background-position:0% 82%}
}

/* RGB 分离文字效果 */
.glitch-text {
  position: relative;
  font-family: 'Courier New', monospace;
  font-size: 3rem;
  font-weight: bold;
}
.glitch-text::before, .glitch-text::after {
  content: attr(data-text);
  position: absolute;
  top: 0; left: 0;
  opacity: 0.8;
}
.glitch-text::before {
  color: #0ff;
  z-index: -1;
  transform: translate(-3px, 2px);
}
.glitch-text::after {
  color: #f0f;
  z-index: -2;
  transform: translate(3px, -2px);
}
```

## App 实现

### SwiftUI
```swift
struct CyberY2KView: View {
    @State private var rotation: Double = 0
    
    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            
            VStack(spacing: 40) {
                // 故障文字
                ZStack {
                    Text("SYSTEM.ERROR")
                        .font(.custom("Courier New", size: 40).bold())
                        .foregroundColor(.cyan)
                        .offset(x: -3, y: 2) // RGB 分离通道 1
                    
                    Text("SYSTEM.ERROR")
                        .font(.custom("Courier New", size: 40).bold())
                        .foregroundColor(.pink)
                        .offset(x: 3, y: -2) // RGB 分离通道 2
                    
                    Text("SYSTEM.ERROR")
                        .font(.custom("Courier New", size: 40).bold())
                        .foregroundColor(.white)
                }
                
                // 全息按钮
                Button(action: {}) {
                    Text("ENTER MATRIX")
                        .font(.headline.weight(.black))
                        .foregroundColor(.white)
                        .padding(.horizontal, 32)
                        .padding(.vertical, 16)
                        .background(
                            AngularGradient(
                                gradient: Gradient(colors: [.red, .yellow, .green, .cyan, .blue, .purple, .red]),
                                center: .center,
                                angle: .degrees(rotation)
                            )
                        )
                        .cornerRadius(30)
                        .overlay(RoundedRectangle(cornerRadius: 30).stroke(Color.white.opacity(0.5), lineWidth: 1))
                }
                .onAppear {
                    withAnimation(.linear(duration: 5).repeatForever(autoreverses: false)) {
                        rotation = 360
                    }
                }
            }
        }
    }
}
```
- SwiftUI 中的 RGB 故障效果非常简单：在 `ZStack` 中堆叠三个相同的 `Text` 视图。给底部的设置 `.cyan` 和 `.pink` 颜色，并轻微 `.offset()` 它们。
- 使用绑定到旋转 `@State` 变量的 `AngularGradient` 实现虹彩 CD-ROM 全息效果。

### Flutter
```dart
class CyberY2KScreen extends StatefulWidget {
  @override
  State<CyberY2KScreen> createState() => _CyberY2KScreenState();
}

class _CyberY2KScreenState extends State<CyberY2KScreen> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(seconds: 5))..repeat();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // 故障文字
            Stack(
              children: [
                Transform.translate(offset: const Offset(-3, 2), child: const Text('SYSTEM.ERROR', style: TextStyle(color: Colors.cyan, fontSize: 40, fontFamily: 'Courier', fontWeight: FontWeight.bold))),
                Transform.translate(offset: const Offset(3, -2), child: const Text('SYSTEM.ERROR', style: TextStyle(color: Colors.pinkAccent, fontSize: 40, fontFamily: 'Courier', fontWeight: FontWeight.bold))),
                const Text('SYSTEM.ERROR', style: TextStyle(color: Colors.white, fontSize: 40, fontFamily: 'Courier', fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 60),
            // 通过 ShaderMask 实现全息按钮
            AnimatedBuilder(
              animation: _controller,
              builder: (context, child) {
                return ShaderMask(
                  shaderCallback: (Rect bounds) {
                    return SweepGradient(
                      colors: const [Colors.red, Colors.yellow, Colors.green, Colors.cyan, Colors.blue, Colors.purple, Colors.red],
                      transform: GradientRotation(_controller.value * 2 * 3.14159), // 旋转 360 度
                    ).createShader(bounds);
                  },
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.white, // 被 shader 遮罩的颜色
                      borderRadius: BorderRadius.circular(30),
                      border: Border.all(color: Colors.white.withOpacity(0.5)),
                    ),
                    padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                    child: const Text('ENTER MATRIX', style: TextStyle(color: Colors.black, fontWeight: FontWeight.w900)),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
```
- 在 Flutter 中，将 `ShaderMask` 与 `SweepGradient` 结合 `AnimationController`，可在任何控件上创建完美、高性能的油膜全息效果。
- 使用 `Stack` 和 `Transform.translate` 构建 RGB 故障文字。

### React Native
```jsx
// 需要 react-native-linear-gradient 来实现复杂渐变
import LinearGradient from 'react-native-linear-gradient';

const GlitchText = ({ text }) => {
  const baseStyle = { fontSize: 40, fontFamily: 'Courier', fontWeight: 'bold', position: 'absolute' };
  return (
    <View style={{ alignItems: 'center', height: 50, justifyContent: 'center' }}>
      <Text style={[baseStyle, { color: '#00FFFF', transform: [{ translateX: -3 }, { translateY: 2 }] }]}>{text}</Text>
      <Text style={[baseStyle, { color: '#FF00FF', transform: [{ translateX: 3 }, { translateY: -2 }] }]}>{text}</Text>
      <Text style={[baseStyle, { color: '#FFF' }]}>{text}</Text>
    </View>
  );
};

const CyberY2KScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#050505', justifyContent: 'center', alignItems: 'center' }}>
      <GlitchText text="SYSTEM.ERROR" />
      
      <View style={{ marginTop: 60 }}>
        {/* React Native 无法原生动画渐变角度。
            使用复杂 LinearGradient 模拟虹彩光泽。 */}
        <LinearGradient
          colors={['#ff2400', '#e8b71d', '#1de840', '#1ddde8', '#dd00f3']}
          start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }}
          style={{
            borderRadius: 30, padding: 16, paddingHorizontal: 32,
            borderWidth: 1, borderColor: 'rgba(255,255,255,0.5)'
          }}
        >
          <Text style={{ color: '#FFF', fontWeight: '900' }}>ENTER MATRIX</Text>
        </LinearGradient>
      </View>
    </View>
  );
};
```
- 堆叠的绝对定位 `<Text>` 节点能很好地处理 RGB 分离故障。
- 真正的动画全息渐变（如 Sweep/Angular）需要 `@shopify/react-native-skia`。如果没有 Skia，可使用静态多停顿 `LinearGradient` 作为回退。

### Jetpack Compose
```kotlin
@Composable
fun GlitchText(text: String) {
    Box(contentAlignment = Alignment.Center) {
        Text(text, color = Color.Cyan, fontSize = 40.sp, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold,
            modifier = Modifier.offset(x = (-3).dp, y = 2.dp))
        Text(text, color = Color.Magenta, fontSize = 40.sp, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold,
            modifier = Modifier.offset(x = 3.dp, y = (-2).dp))
        Text(text, color = Color.White, fontSize = 40.sp, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun CyberY2KScreen() {
    val infiniteTransition = rememberInfiniteTransition()
    val rotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(5000, easing = LinearEasing)
        )
    )

    Column(
        modifier = Modifier.fillMaxSize().background(Color.Black),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        GlitchText("SYSTEM.ERROR")
        
        Spacer(Modifier.height(60.dp))
        
        // 全息按钮
        Box(
            modifier = Modifier
                .background(
                    brush = Brush.sweepGradient(
                        colors = listOf(Color.Red, Color.Yellow, Color.Green, Color.Cyan, Color.Blue, Color.Magenta, Color.Red),
                        center = Offset.Unspecified
                    ),
                    shape = RoundedCornerShape(30.dp)
                )
                .graphicsLayer { rotationZ = rotation } // 注意：这会旋转整个按钮。 
                // 仅旋转渐变画笔本身需要在 drawBehind 中通过自定义 ShaderBrush 或绘制矩形进行 Matrix 操作
                .border(1.dp, Color.White.copy(alpha = 0.5f), RoundedCornerShape(30.dp))
                .padding(horizontal = 32.dp, vertical = 16.dp)
        ) {
            Text("ENTER MATRIX", color = Color.White, fontWeight = FontWeight.Black)
        }
    }
}
```
- 与其他框架一样，使用 `Box` 堆叠带 `Modifier.offset()` 的文字以实现故障。
- `Brush.sweepGradient` 创建全息 CD-ROM 色彩，尽管在 Compose 中旋转*画笔本身*（而非整个控件）需要一些高级 `Matrix` 操作配合 `ShaderBrush`。

## 推荐与避免
- **推荐**：融入看起来像原始 HTML/CSS 的 UI 元素（如可见的表格或 marquee 标签），作为对早期 Web 的反讽致敬。
- **避免**：使用干净、现代的几何布局。Cyber Y2K 是混乱和叛逆的。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。