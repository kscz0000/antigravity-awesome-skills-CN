---
name: gradient-design
description: Gradient Design 的 Web 与 App 实现指南。当用户希望大量使用渐变、活力十足的过渡和现代能量感时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Gradient Design

> "运动中的色彩。为扁平表面增添能量和深度的流动过渡。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **渐变是主要的视觉元素**：背景、按钮、文字和边框都使用渐变而非纯色。
2. **相似或互补的混合**：必须仔细选择渐变，使过渡颜色不会变浑浊（例如，红到绿的混合在中间会产生浑浊的棕色。应该红到黄再到绿）。
3. **微妙的动画**：背景渐变应缓慢移动和旋转。

## 视觉 DNA
- **颜色**：**Warm Tech**（蓝色到橙色）或创建自定义活力搭配（如紫到珊瑚、深蓝到青）。
- **排版**：干净、粗壮的无衬线字体，可以轻松使用渐变填充蒙版。
- **布局**：保持 UI 结构极简（玻璃面板或白色/黑色卡片），让渐变得以呼吸。

## Web 实现
- **CSS 示例**：
```css
body {
  /* 复杂的网状动画渐变 */
  background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
  color: #fff;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.gradient-text {
  background: linear-gradient(90deg, #F9D423 0%, #FF4E50 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 4rem;
  font-weight: 900;
}

.gradient-border-card {
  background: #ffffff;
  color: #333;
  padding: 32px;
  border-radius: 12px;
  position: relative;
  /* 使用伪元素实现渐变边框 */
}
.gradient-border-card::before {
  content: '';
  position: absolute;
  top: -3px; left: -3px; right: -3px; bottom: -3px;
  background: linear-gradient(90deg, #8A2387, #E94057, #F27121);
  z-index: -1;
  border-radius: 15px;
}
```

## App 实现

### SwiftUI
```swift
struct GradientDesignView: View {
    @State private var animateGradient = false
    
    var body: some View {
        ZStack {
            // 动画背景渐变
            LinearGradient(
                colors: [Color(hex: "ee7752"), Color(hex: "e73c7e"), Color(hex: "23a6d5"), Color(hex: "23d5ab")],
                startPoint: animateGradient ? .topLeading : .bottomLeading,
                endPoint: animateGradient ? .bottomTrailing : .topTrailing
            )
            .ignoresSafeArea()
            .onAppear {
                withAnimation(.linear(duration: 5.0).repeatForever(autoreverses: true)) {
                    animateGradient.toggle()
                }
            }
            
            VStack(spacing: 40) {
                // 渐变文字
                Text("VIBRANT")
                    .font(.system(size: 60, weight: .black))
                    .foregroundStyle(
                        LinearGradient(
                            colors: [Color(hex: "F9D423"), Color(hex: "FF4E50")],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                
                // 渐变边框卡片
                Text("Gradient Border")
                    .padding()
                    .frame(width: 250, height: 150)
                    .background(Color.white)
                    .cornerRadius(12)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(
                                LinearGradient(
                                    colors: [Color(hex: "8A2387"), Color(hex: "E94057"), Color(hex: "F27121")],
                                    startPoint: .leading, endPoint: .trailing
                                ),
                                lineWidth: 3
                            )
                    )
            }
        }
    }
}
```
- `.foregroundStyle(LinearGradient(...))` 让现代 SwiftUI 中的渐变文字变得非常简单。
- 使用 `.stroke(LinearGradient(...))` 配合 `.overlay` 创建渐变边框。

### Flutter
```dart
class GradientDesignScreen extends StatefulWidget {
  @override
  State<GradientDesignScreen> createState() => _GradientDesignScreenState();
}

class _GradientDesignScreenState extends State<GradientDesignScreen> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<Alignment> _topAlignment;
  late Animation<Alignment> _bottomAlignment;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(seconds: 5))..repeat(reverse: true);
    _topAlignment = TweenSequence<Alignment>([
      TweenSequenceItem(tween: AlignmentTween(begin: Alignment.topLeft, end: Alignment.topRight), weight: 1),
    ]).animate(_controller);
    _bottomAlignment = TweenSequence<Alignment>([
      TweenSequenceItem(tween: AlignmentTween(begin: Alignment.bottomRight, end: Alignment.bottomLeft), weight: 1),
    ]).animate(_controller);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AnimatedBuilder(
        animation: _controller,
        builder: (context, _) {
          return Container(
            width: double.infinity,
            decoration: BoxDecoration(
              // 动画背景渐变
              gradient: LinearGradient(
                begin: _topAlignment.value,
                end: _bottomAlignment.value,
                colors: const [Color(0xFFee7752), Color(0xFFe73c7e), Color(0xFF23a6d5), Color(0xFF23d5ab)],
              ),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // 渐变文字
                ShaderMask(
                  blendMode: BlendMode.srcIn,
                  shaderCallback: (bounds) => const LinearGradient(
                    colors: [Color(0xFFF9D423), Color(0xFFFF4E50)],
                  ).createShader(Rect.fromLTWH(0, 0, bounds.width, bounds.height)),
                  child: const Text('VIBRANT', style: TextStyle(fontSize: 60, fontWeight: FontWeight.w900, color: Colors.white)),
                ),
                const SizedBox(height: 40),
                // 渐变边框卡片
                Container(
                  width: 250, height: 150,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15),
                    gradient: const LinearGradient(colors: [Color(0xFF8A2387), Color(0xFFE94057), Color(0xFFF27121)]),
                  ),
                  padding: const EdgeInsets.all(3), // 边框宽度
                  child: Container(
                    decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
                    alignment: Alignment.center,
                    child: const Text('Gradient Border'),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
```
- Flutter 文字渐变需要 `ShaderMask` 配合 `BlendMode.srcIn`。
- 要动画渐变背景，可以对 `LinearGradient` 的 `Alignment` 值进行动画。

### React Native
```jsx
// 需要：expo-linear-gradient 或 react-native-linear-gradient
import { LinearGradient } from 'expo-linear-gradient';
import MaskedView from '@react-native-masked-view/masked-view';

const GradientDesignScreen = () => {
  return (
    <LinearGradient
      colors={['#ee7752', '#e73c7e', '#23a6d5', '#23d5ab']}
      start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }}
      style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}
    >
      {/* 渐变文字 */}
      <MaskedView
        style={{ height: 80, width: '100%', flexDirection: 'row' }}
        maskElement={
          <View style={{ backgroundColor: 'transparent', flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Text style={{ fontSize: 60, fontWeight: '900', color: 'black' }}>VIBRANT</Text>
          </View>
        }
      >
        <LinearGradient
          colors={['#F9D423', '#FF4E50']}
          start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
          style={{ flex: 1 }}
        />
      </MaskedView>

      <View style={{ marginTop: 40 }}>
        {/* 渐变边框卡片 */}
        <LinearGradient
          colors={['#8A2387', '#E94057', '#F27121']}
          start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
          style={{ padding: 3, borderRadius: 15 }}
        >
          <View style={{ backgroundColor: '#FFF', width: 250, height: 150, borderRadius: 12, justifyContent: 'center', alignItems: 'center' }}>
            <Text>Gradient Border</Text>
          </View>
        </LinearGradient>
      </View>
    </LinearGradient>
  );
};
```
- React Native 中的渐变文字非常麻烦。必须使用 `@react-native-masked-view/masked-view` 将 `LinearGradient` 与 `<Text>` 节点蒙版。
- 渐变边框通过在小内边距（例如 `padding: 3`）的 `LinearGradient` 内嵌套纯色 View 来实现。

### Jetpack Compose
```kotlin
@Composable
fun GradientDesignScreen() {
    // 动画背景
    val infiniteTransition = rememberInfiniteTransition()
    val offset by infiniteTransition.animateFloat(
        initialValue = 0f, targetValue = 1000f,
        animationSpec = infiniteRepeatable(tween(5000, easing = LinearEasing), RepeatMode.Reverse)
    )

    val bgBrush = Brush.linearGradient(
        colors = listOf(Color(0xFFee7752), Color(0xFFe73c7e), Color(0xFF23a6d5), Color(0xFF23d5ab)),
        start = Offset(offset, 0f), end = Offset(offset + 500f, 1000f)
    )

    Box(
        modifier = Modifier.fillMaxSize().background(bgBrush),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            // 渐变文字
            val textBrush = Brush.horizontalGradient(listOf(Color(0xFFF9D423), Color(0xFFFF4E50)))
            Text(
                text = "VIBRANT",
                style = TextStyle(brush = textBrush, fontSize = 60.sp, fontWeight = FontWeight.Black)
            )

            Spacer(Modifier.height(40.dp))

            // 渐变边框卡片
            val borderBrush = Brush.horizontalGradient(listOf(Color(0xFF8A2387), Color(0xFFE94057), Color(0xFFF27121)))
            Box(
                modifier = Modifier
                    .size(250.dp, 150.dp)
                    .border(3.dp, borderBrush, RoundedCornerShape(12.dp))
                    .background(Color.White, RoundedCornerShape(12.dp)),
                contentAlignment = Alignment.Center
            ) {
                Text("Gradient Border")
            }
        }
    }
}
```
- Compose 通过 `Brush` 完美处理渐变。
- 你可以将 `Brush` 直接传入 `TextStyle` 实现渐变文字，或传入 `Modifier.border()` 实现渐变边框。

## 推荐与避免
- **推荐**：使用多停顿渐变（3 或 4 种颜色），而不仅仅是简单的 A 到 B 渐变，以获得更现代、丰富的外观。
- **避免**：将渐变应用在小文字或细图标上，它们会立刻失去可读性。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。