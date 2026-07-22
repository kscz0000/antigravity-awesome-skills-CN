---
name: aurora-ui
description: Aurora UI 的 Web 与 App 实现指南。当用户需要渐变光晕、色块和氛围光效果时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Aurora UI

> "空灵、流光溢彩。如同被困在磨砂玻璃下的极光。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **模糊的彩色光球**：大尺寸、失焦、高饱和度的色块在背景中漂浮。
2. **玻璃态叠加**：前景元素通常是半透明的（玻璃态），让极光效果能够穿透出来。
3. **流动的运动**：背景色块应当缓慢地漂浮、扩张和收缩。

## 视觉 DNA
- **颜色**：需要深邃的背景搭配鲜艳、发光的强调色。**Midnight Luxury** 或改为暗色模式的 **Yacht Club** 都效果很好，注入亮青色、品红或酸橙绿作为发光光球。
- **排版**：纤细、优雅的无衬线字体或精致的衬线字体。高对比度白色文字。
- **布局**：保持前景 UI 元素极简，让背景成为主角。

## Web 实现
- 最佳实现方式是在主内容背后使用绝对定位、严重模糊的 `div`。
- **CSS 示例**：
```css
body {
  background-color: #0A0A0A;
  overflow-x: hidden;
  position: relative;
}

/* 发光光球 */
.aurora-blob {
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(181,154,95,0.8) 0%, rgba(181,154,95,0) 70%);
  border-radius: 50%;
  filter: blur(80px);
  z-index: -1;
  animation: float 20s infinite ease-in-out alternate;
}

.aurora-blob.blue {
  background: radial-gradient(circle, rgba(92,107,115,0.8) 0%, rgba(0,0,0,0) 70%);
  top: 20%;
  left: 60%;
  animation-delay: -5s;
}

@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-50px, 100px) scale(1.2); }
  100% { transform: translate(100px, -50px) scale(0.9); }
}

/* 前景内容应采用玻璃态 */
.aurora-card {
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 24px;
}
```

## App 实现

### SwiftUI
```swift
struct AuroraView: View {
    @State private var animate = false
    
    var body: some View {
        ZStack {
            // 深色背景
            Color.black.ignoresSafeArea()
            
            // 动画光球
            Circle()
                .fill(Color(red: 0.71, green: 0.60, blue: 0.37)) // #B59A5F
                .blur(radius: 80)
                .frame(width: 300, height: 300)
                .offset(x: animate ? -50 : 50, y: animate ? -100 : 0)
            
            Circle()
                .fill(Color(red: 0.36, green: 0.42, blue: 0.45)) // #5C6B73
                .blur(radius: 80)
                .frame(width: 300, height: 300)
                .offset(x: animate ? 100 : -50, y: animate ? 100 : -50)
            
            // 玻璃态前景内容
            VStack {
                Text("Aurora Interface")
                    .font(.largeTitle.bold())
                    .foregroundColor(.white)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(.ultraThinMaterial)
        }
        .onAppear {
            withAnimation(.easeInOut(duration: 10).repeatForever(autoreverses: true)) {
                animate = true
            }
        }
    }
}
```
- 在主内容下方的 `ZStack` 中使用 `Circle().blur(radius: 80...120)`。
- 用非常长的动画时长（10-20 秒）对 `.offset()` 进行动画。
- 在前景容器上使用 `.background(.ultraThinMaterial)`，让彩色光线漂亮地透过。

### Flutter
```dart
import 'dart:ui';

class AuroraView extends StatefulWidget {
  @override
  State<AuroraView> createState() => _AuroraViewState();
}

class _AuroraViewState extends State<AuroraView> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(seconds: 10))..repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // 动画光球
          AnimatedBuilder(
            animation: _controller,
            builder: (context, child) {
              return Positioned(
                top: 100 + (_controller.value * 100),
                left: -50 + (_controller.value * 100),
                child: Container(
                  width: 300,
                  height: 300,
                  decoration: const BoxDecoration(
                    shape: BoxShape.circle,
                    color: Color(0xFFB59A5F),
                  ),
                ),
              );
            },
          ),
          // 大面积模糊层覆盖在光球上
          Positioned.fill(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 80, sigmaY: 80),
              child: Container(color: Colors.transparent),
            ),
          ),
          // 玻璃态前景
          Center(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(24),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 16, sigmaY: 16),
                child: Container(
                  padding: const EdgeInsets.all(32),
                  color: Colors.white.withOpacity(0.05),
                  child: const Text('Aurora Interface',
                    style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
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
- 在移动的实心圆上方叠加一个全屏的 `BackdropFilter`，比单独模糊每个圆更具性能优势。
- 再叠加一层较弱的 `BackdropFilter` 来实现真正的玻璃态前景面板。

### React Native
```jsx
// 需要 @react-native-community/blur
import { BlurView } from '@react-native-community/blur';

const AuroraView = () => {
  const anim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(anim, { toValue: 1, duration: 10000, useNativeDriver: true }),
        Animated.timing(anim, { toValue: 0, duration: 10000, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  const translateY = anim.interpolate({ inputRange: [0, 1], outputRange: [0, 100] });

  return (
    <View style={{ flex: 1, backgroundColor: '#000' }}>
      {/* 光球 — 注意：React Native 对大面积实时模糊支持不佳，
          因此在生产环境中强烈推荐使用预先渲染好的模糊 PNG */}
      <Animated.Image 
        source={require('./blurred_orb_cyan.png')} 
        style={{
          position: 'absolute',
          top: -50, left: -50,
          width: 400, height: 400,
          opacity: 0.8,
          transform: [{ translateY }]
        }}
      />

      {/* 玻璃前景 */}
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <BlurView blurType="dark" blurAmount={20} style={{ padding: 32, borderRadius: 24 }}>
          <Text style={{ color: '#FFF', fontSize: 24, fontWeight: '700' }}>
            Aurora Interface
          </Text>
        </BlurView>
      </View>
    </View>
  );
};
```
- **性能警告**：不要在 React Native 上将 `BlurView` 用于移动背景光球——尤其在 Android 上，会严重卡顿。
- **最佳实践**：在 Figma/Photoshop 中创建大尺寸、已模糊的 PNG 图像，然后用 `Animated.Image` 对其进行动画处理。

### Jetpack Compose
```kotlin
@Composable
fun AuroraView() {
    val infiniteTransition = rememberInfiniteTransition()
    val offsetY by infiniteTransition.animateFloat(
        initialValue = -50f,
        targetValue = 100f,
        animationSpec = infiniteRepeatable(
            animation = tween(10000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        )
    )

    Box(modifier = Modifier
        .fillMaxSize()
        .background(Color.Black)) {
        
        // 模糊光球
        Box(
            modifier = Modifier
                .offset(x = (-50).dp, y = offsetY.dp)
                .size(300.dp)
                .blur(80.dp) // 仅支持 API 31+！
                .background(Color(0xFFB59A5F), CircleShape)
        )
        
        // API 31 以下的回退方案：使用径向渐变代替模糊
        Box(
            modifier = Modifier
                .offset(x = 150.dp, y = (offsetY * -1).dp)
                .size(300.dp)
                .background(
                    Brush.radialGradient(
                        colors = listOf(Color(0xFF5C6B73).copy(alpha = 0.8f), Color.Transparent)
                    )
                )
        )

        // 玻璃面板
        Card(
            modifier = Modifier.align(Alignment.Center).padding(32.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.05f)),
            shape = RoundedCornerShape(24.dp),
        ) {
            Text("Aurora Interface",
                color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(32.dp))
        }
    }
}
```
- `Modifier.blur()` 仅在 Android 12（API 31+）上完全受支持。
- **关键回退方案**：对于旧设备，使用 `Brush.radialGradient` 从颜色渐变到 `Color.Transparent`，模拟发光光球效果，无需昂贵的模糊计算。

## 推荐与避免
- **推荐**：确保前景文字保持可读。如果一个明亮的光球漂浮在白色文字背后，文字会消失。使用玻璃面板来保证对比度。
- **避免**：使用尖锐的渐变。背景中所有元素都必须严重模糊并弥散。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。