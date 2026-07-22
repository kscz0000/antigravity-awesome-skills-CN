---
name: claymorphism
description: Claymorphism 的 Web 与 App 实现指南。当用户需要柔和的 3D 元素、圆滑的形状，以及俏皮、有质感的视觉表现时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Claymorphism

> "如同与一套全新的数字黏土动画互动。柔软、圆润且非常平易近人。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **蓬松的 3D 体积**：元素看起来像被吹胀的气球或柔软的黏土块。
2. **双重内阴影**：Claymorphism 的标志是左上的内亮阴影和右下的内暗阴影，为实心形状赋予 3D 体积感。
3. **连续的曲线**：圆角拉满。在这个世界里不存在尖锐的边角。

## 视觉 DNA
- **颜色**：在柔和色和明亮友好的色调中茁壮成长。**Desert Mirage**、**Earth-Grounded Elegance** 或自定义柔和色调效果最佳。
- **排版**：俏皮、粗壮、圆润的字体（如 `Sniglet`、`Fredoka One`、`Nunito`）。
- **形状**：'Squircle'（边角高度圆润的方形）和完美圆形。

## Web 实现
- 区别于 Neumorphism：Claymorphism 元素从背景中"脱离"（有投影）并使用内阴影来创造体积，颜色通常与背景形成对比。
- **CSS 示例**：
```css
.clay-card {
  background-color: #F8B4A6; /* 柔和珊瑚色 */
  border-radius: 32px;
  padding: 40px;
  
  /* 
    1. 外投影（从背景脱离）
    2. 内左上方高光（体积）
    3. 内右下方阴影（体积）
  */
  box-shadow: 
    8px 8px 24px rgba(0, 0, 0, 0.15),           /* 外 */
    inset -8px -8px 16px rgba(0, 0, 0, 0.1),    /* 内暗 */
    inset 8px 8px 16px rgba(255, 255, 255, 0.4); /* 内亮 */
    
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1); /* 弹性 */
}

.clay-card:hover {
  transform: translateY(-5px) scale(1.02);
}
```

## App 实现

### SwiftUI
```swift
struct ClayCard: View {
    @State private var isPressed = false
    
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "cloud.sun.fill")
                .font(.system(size: 48))
                .foregroundColor(.white)
            Text("Claymorphic Card")
                .font(.system(size: 20, weight: .bold, design: .rounded))
                .foregroundColor(.white)
        }
        .padding(40)
        .background(Color(red: 0.97, green: 0.71, blue: 0.65)) // 柔和珊瑚色
        .cornerRadius(32)
        // 外阴影 — 从背景脱离
        .shadow(color: .black.opacity(0.15), radius: 12, x: 8, y: 8)
        // 内高光（左上）— 通过叠加模拟
        .overlay(
            RoundedRectangle(cornerRadius: 32)
                .stroke(
                    LinearGradient(
                        colors: [.white.opacity(0.5), .clear, .black.opacity(0.1)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: 3
                )
        )
        // 点击时的弹性动画
        .scaleEffect(isPressed ? 0.95 : 1.0)
        .animation(.interpolatingSpring(stiffness: 300, damping: 10), value: isPressed)
        .onTapGesture { }
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
    }
}
```
- "黏土"体积来自渐变描边叠加：左上为白色，右下为黑色。
- 使用 `.interpolatingSpring(stiffness: 300, damping: 10)` 营造弹性手感 — 对黏土美学至关重要。
- 背景色应为柔和色/亮色，但与父级*不同*（与 Neumorphism 不同）。

### Flutter
```dart
class ClayCard extends StatefulWidget {
  @override
  State<ClayCard> createState() => _ClayCardState();
}

class _ClayCardState extends State<ClayCard> with SingleTickerProviderStateMixin {
  double _scale = 1.0;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => setState(() => _scale = 0.95),
      onTapUp: (_) => setState(() => _scale = 1.0),
      onTapCancel: () => setState(() => _scale = 1.0),
      child: AnimatedScale(
        scale: _scale,
        duration: const Duration(milliseconds: 200),
        curve: Curves.elasticOut,  // 弹性黏土手感
        child: Container(
          padding: const EdgeInsets.all(40),
          decoration: BoxDecoration(
            color: const Color(0xFFF8B4A6), // 柔和珊瑚色
            borderRadius: BorderRadius.circular(32),
            boxShadow: [
              // 外阴影
              BoxShadow(
                color: Colors.black.withOpacity(0.15),
                offset: const Offset(8, 8),
                blurRadius: 24,
              ),
            ],
            // 黏土体积效果的渐变边框
            border: GradientBorder(
              gradient: LinearGradient(
                colors: [
                  Colors.white.withOpacity(0.5),
                  Colors.transparent,
                  Colors.black.withOpacity(0.1),
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              width: 3,
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.wb_sunny, size: 48, color: Colors.white),
              const SizedBox(height: 16),
              const Text('Claymorphic Card',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold,
                  color: Colors.white)),
            ],
          ),
        ),
      ),
    );
  }
}
```
- 使用 `Curves.elasticOut` 或 `Curves.bounceOut` 实现弹性动画 — 对黏土手感至关重要。
- 渐变边框需要自定义 `ShapeDecoration` 或在主容器后放置一个渐变容器的 `Stack`。
- 内阴影的替代方案：使用 `flutter_inset_box_shadow` 包，左上亮、右下暗。

### React Native
```jsx
const ClayCard = () => {
  const scale = useRef(new Animated.Value(1)).current;
  
  const pressIn = () => {
    Animated.spring(scale, {
      toValue: 0.95,
      friction: 3,      // 低摩擦力 = 弹性
      tension: 100,
      useNativeDriver: true,
    }).start();
  };
  
  const pressOut = () => {
    Animated.spring(scale, {
      toValue: 1,
      friction: 3,
      tension: 100,
      useNativeDriver: true,
    }).start();
  };

  return (
    <Pressable onPressIn={pressIn} onPressOut={pressOut}>
      <Animated.View style={{
        transform: [{ scale }],
        padding: 40,
        backgroundColor: '#F8B4A6',
        borderRadius: 32,
        alignItems: 'center',
        // 外阴影
        shadowColor: '#000',
        shadowOffset: { width: 8, height: 8 },
        shadowOpacity: 0.15,
        shadowRadius: 12,
        elevation: 8,
        // 渐变边框必须用包装器或 SVG 模拟
        borderWidth: 3,
        borderColor: 'rgba(255,255,255,0.3)', // 简化版 — 顶部高光
      }}>
        <Text style={{ fontSize: 48 }}>☀️</Text>
        <Text style={{
          fontSize: 20, fontWeight: '700', color: '#FFF', marginTop: 16,
        }}>
          Claymorphic Card
        </Text>
      </Animated.View>
    </Pressable>
  );
};
```
- 使用 `Animated.spring` 配合低 `friction`（3-5）实现标志性的弹性黏土行为。
- 原生不支持渐变边框——可使用带白色调的纯色边框作为简化近似，或包裹在 `expo-linear-gradient` View 中。

### Jetpack Compose
```kotlin
@Composable
fun ClayCard() {
    var isPressed by remember { mutableStateOf(false) }
    val scale by animateFloatAsState(
        targetValue = if (isPressed) 0.95f else 1f,
        animationSpec = spring(dampingRatio = 0.3f, stiffness = 300f),
    )
    
    Box(
        modifier = Modifier
            .graphicsLayer { scaleX = scale; scaleY = scale }
            .shadow(8.dp, RoundedCornerShape(32.dp))
            .clip(RoundedCornerShape(32.dp))
            .background(Color(0xFFF8B4A6))
            .border(
                3.dp,
                Brush.linearGradient(
                    colors = listOf(
                        Color.White.copy(alpha = 0.5f),
                        Color.Transparent,
                        Color.Black.copy(alpha = 0.1f),
                    ),
                    start = Offset.Zero,
                    end = Offset.Infinite,
                ),
                RoundedCornerShape(32.dp),
            )
            .padding(40.dp)
            .pointerInput(Unit) {
                detectTapGestures(
                    onPress = {
                        isPressed = true
                        tryAwaitRelease()
                        isPressed = false
                    },
                )
            },
        contentAlignment = Alignment.Center,
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(Icons.Default.WbSunny, tint = Color.White,
                modifier = Modifier.size(48.dp))
            Spacer(Modifier.height(16.dp))
            Text("Claymorphic Card",
                fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color.White)
        }
    }
}
```
- 使用 `spring(dampingRatio = 0.3f)` — 低阻尼 = 弹性。这是黏土手感的核心。
- Compose 中渐变边框通过 `Modifier.border(width, Brush.linearGradient(...), shape)` 原生支持。
- 在 `.background()` 之前使用 `Modifier.clip()`，确保圆角正确裁剪内容。

## 推荐与避免
- **推荐**：使用高度弹性的弹簧动画，强化"黏土"的柔软物理感。
- **避免**：使用纤细、娇柔的字体。它们会在厚重、富有体积感的 UI 元素中消失。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。