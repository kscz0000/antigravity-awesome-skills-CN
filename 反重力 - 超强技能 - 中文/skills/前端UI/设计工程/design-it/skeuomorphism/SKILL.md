---
name: skeuomorphism
description: Skeuomorphism 的 Web 与 App 实现指南。当用户希望 UI 模仿真实物体、写实纹理或物理隐喻时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Skeuomorphism

> "数字界面看起来、表现得像它们的物理对应物。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **写实纹理**：皮革、拉丝金属、木纹、纸张。UI 应该感觉像可以触摸的真实物体。
2. **物理光照与深度**：密切关注镜面高光、投影、内阴影、倒角和环境光遮蔽。
3. **真实世界隐喻**：看起来像硬件开关的开关、有刻度的拨盘、有装订环的记事本。

## 视觉 DNA
- **颜色**：高度依赖于被模拟的材料。对于经典的拟物风格，使用 **Industrial Chic**（金属/硬件）或 **Monochromatic Brown**（木材/皮革）调色板。
- **排版**：与物理对象匹配的字体（例如，打字机字体用于纸张、LCD 字体用于数字屏幕、浮雕无衬线用于硬件按钮）。
- **细节**：螺钉、缝线、眩光和渐变是你主要的工具。

## Web 实现
- 大量使用分层背景图像（纹理）、复杂渐变和多重 box-shadow。
- **CSS 示例**：
```css
.skeuo-button {
  /* 拉丝金属效果 */
  background: linear-gradient(180deg, #e0e0e0 0%, #a0a0a0 100%),
              url('brushed-metal-texture.png');
  background-blend-mode: overlay;
  
  border: 1px solid #7a7a7a;
  border-radius: 50%;
  width: 80px;
  height: 80px;
  
  /* 倒角、内高光和投影 */
  box-shadow: 
    inset 0 2px 4px rgba(255,255,255,0.8), /* 顶部高光 */
    inset 0 -2px 4px rgba(0,0,0,0.4),      /* 底部阴影 */
    0 4px 6px rgba(0,0,0,0.5),             /* 投影 */
    0 1px 1px rgba(0,0,0,0.2);
}

.skeuo-button:active {
  /* 按下物理按钮 */
  box-shadow: 
    inset 0 4px 8px rgba(0,0,0,0.6),
    inset 0 -1px 2px rgba(255,255,255,0.4),
    0 1px 1px rgba(0,0,0,0.2);
  transform: translateY(2px);
}
```

## App 实现

### SwiftUI
```swift
struct SkeuoButton: View {
    @State private var isPressed = false
    
    var body: some View {
        Button(action: {}) {
            Text("POWER")
                .font(.system(size: 14, weight: .bold))
                .foregroundColor(.white)
                .textCase(.uppercase)
        }
        .frame(width: 80, height: 80)
        .background(
            ZStack {
                // 拉丝金属基础
                Circle()
                    .fill(
                        LinearGradient(
                            colors: [Color(white: 0.88), Color(white: 0.63)],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
                // 内高光（顶部倒角）
                Circle()
                    .stroke(
                        LinearGradient(
                            colors: [.white.opacity(0.8), .clear],
                            startPoint: .top,
                            endPoint: .center
                        ),
                        lineWidth: 2
                    )
                    .padding(1)
            }
        )
        .clipShape(Circle())
        // 外圈边框
        .overlay(Circle().stroke(Color(white: 0.5), lineWidth: 1))
        // 物理投影
        .shadow(color: .black.opacity(isPressed ? 0.2 : 0.5), radius: isPressed ? 2 : 6,
                x: 0, y: isPressed ? 1 : 4)
        .scaleEffect(isPressed ? 0.96 : 1.0)
        .animation(.easeOut(duration: 0.1), value: isPressed)
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
    }
}
```
- 堆叠多个形状（`Circle`、`RoundedRectangle`）配合不同的渐变来构建有真实感的深度。
- 使用 `.overlay()` 与描边形状作为边缘高光。
- 按下状态应同时减少阴影并缩放——模拟物理按压。

### Flutter
```dart
class SkeuoButton extends StatefulWidget {
  @override
  State<SkeuoButton> createState() => _SkeuoButtonState();
}

class _SkeuoButtonState extends State<SkeuoButton> {
  bool _isPressed = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => setState(() => _isPressed = true),
      onTapUp: (_) => setState(() => _isPressed = false),
      onTapCancel: () => setState(() => _isPressed = false),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 100),
        width: 80,
        height: 80,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          // 拉丝金属渐变
          gradient: LinearGradient(
            colors: [Colors.grey[300]!, Colors.grey[600]!],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
          border: Border.all(color: Colors.grey[500]!, width: 1),
          boxShadow: [
            // 外投影
            BoxShadow(
              color: Colors.black.withOpacity(_isPressed ? 0.2 : 0.5),
              blurRadius: _isPressed ? 4 : 12,
              offset: Offset(0, _isPressed ? 2 : 6),
            ),
            // 顶部内高光（通过光内阴影伪造）
            BoxShadow(
              color: Colors.white.withOpacity(0.6),
              blurRadius: 1,
              offset: const Offset(0, -1),
              spreadRadius: -1,
            ),
          ],
        ),
        transform: Matrix4.identity()..scale(_isPressed ? 0.96 : 1.0),
        alignment: Alignment.center,
        child: const Text('POWER',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold,
            fontSize: 14, shadows: [
              Shadow(color: Colors.black54, offset: Offset(0, 1), blurRadius: 2),
            ])),
      ),
    );
  }
}
```
- 使用 `AnimatedContainer` 实现平滑的按下过渡。在点击时调整 `boxShadow`、`transform` 和渐变。
- 分层 `BoxShadow` 条目：一个用于外投影，一个用于顶部边缘高光。
- 对于复杂纹理（皮革、木纹），在 `BoxDecoration` 中使用 `DecorationImage` 配合资源文件。

### React Native
```jsx
const SkeuoButton = () => {
  const [pressed, setPressed] = useState(false);
  
  return (
    <Pressable
      onPressIn={() => setPressed(true)}
      onPressOut={() => setPressed(false)}
      style={{
        width: 80,
        height: 80,
        borderRadius: 40,
        alignItems: 'center',
        justifyContent: 'center',
        // 金属渐变必须通过图像或 LinearGradient 组件实现
        backgroundColor: '#A0A0A0',
        borderWidth: 1,
        borderColor: '#7A7A7A',
        // 投影在按下时变化
        shadowColor: '#000',
        shadowOffset: { width: 0, height: pressed ? 1 : 4 },
        shadowOpacity: pressed ? 0.2 : 0.5,
        shadowRadius: pressed ? 2 : 6,
        elevation: pressed ? 2 : 8,
        transform: [{ scale: pressed ? 0.96 : 1 }],
      }}
    >
      <Text style={{
        color: '#FFF',
        fontWeight: '700',
        fontSize: 14,
        textShadowColor: 'rgba(0,0,0,0.5)',
        textShadowOffset: { width: 0, height: 1 },
        textShadowRadius: 2,
      }}>
        POWER
      </Text>
    </Pressable>
  );
};
```
- 为了逼真的纹理，使用 `ImageBackground` 配合导出的纹理资源（leather.png、brushed-metal.png）。
- 使用 `Pressable` 与 `onPressIn`/`onPressOut` 来动画阴影深度、缩放和不透明度变化。
- 复杂的渐变倒角需要 `react-native-linear-gradient` 或 `expo-linear-gradient`。

### Jetpack Compose
```kotlin
@Composable
fun SkeuoButton() {
    var isPressed by remember { mutableStateOf(false) }
    val scale by animateFloatAsState(if (isPressed) 0.96f else 1f)
    val elevation by animateDpAsState(if (isPressed) 2.dp else 8.dp)
    
    Box(
        modifier = Modifier
            .size(80.dp)
            .graphicsLayer { scaleX = scale; scaleY = scale }
            .shadow(elevation, CircleShape)
            .clip(CircleShape)
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xFFE0E0E0), Color(0xFFA0A0A0))
                )
            )
            .border(1.dp, Color(0xFF7A7A7A), CircleShape)
            .pointerInput(Unit) {
                detectTapGestures(
                    onPress = {
                        isPressed = true
                        tryAwaitRelease()
                        isPressed = false
                    }
                )
            },
        contentAlignment = Alignment.Center,
    ) {
        Text("POWER",
            color = Color.White,
            fontWeight = FontWeight.Bold,
            fontSize = 14.sp,
            style = TextStyle(shadow = Shadow(
                color = Color.Black.copy(alpha = 0.5f),
                offset = Offset(0f, 2f),
                blurRadius = 4f,
            )))
    }
}
```
- 使用 `Brush.verticalGradient()` 处理金属表面，使用 `Modifier.border()` 与 `CircleShape` 处理边框。
- 在按下时动画 `shadow` 凸起和 `graphicsLayer { scaleX/scaleY }`，获得真实的物理按压感。
- 对于纹理，使用 `Modifier.paint(painterResource(R.drawable.brushed_metal))` 作为背景。

## 推荐与避免
- **推荐**：确保隐喻对用户任务有意义。
- **避免**：过度使用导致杂乱。让交互元素高度逼真，但让结构布局保持简洁。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。