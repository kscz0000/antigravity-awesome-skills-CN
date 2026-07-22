---
name: sci-fi-interface
description: Sci-Fi Interface Design（HUD）的 Web 与 App 实现指南。当用户希望 HUD、航天器仪表板或战术军用读数器时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Sci-Fi Interface Design（HUD）

> "抬头显示。战术性、精确、高度分析性。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **线框与轮廓**：界面几乎完全由细描边而非实心填充框构建。
2. **圆形阵列与雷达**：大量使用同心圆、雷达扫描和弧形进度条。
3. **单色 + 警示**：通常完全单色（仅蓝或仅绿），辅色（红色）仅用于警报。

## 视觉 DNA
- **颜色**：午夜背景。UI 是纯青色、翠绿色或琥珀色（如同经典单色显示器）。**Minimalist Slate** 改为深色也能胜任。
- **排版**：严格、技术性的等宽字体（`Share Tech Mono`、`VT323`、`Space Mono`）。全大写。
- **样式**：极小的 UI 装饰细节（目标括号 `[ ]`、框线、精确的像素坐标）。

## Web 实现
- 大量使用 SVG 绘制圆形表盘，CSS 边框处理布局。
- **CSS 示例**：
```css
body {
  background-color: #000b18; /* 深空海军蓝 */
  color: #4df; /* 全息青色 */
  font-family: 'Share Tech Mono', monospace;
  text-transform: uppercase;
}

/* HUD 框架 */
.hud-container {
  border: 1px solid rgba(68, 221, 255, 0.3);
  position: relative;
  padding: 30px;
}

/* 角部括号 */
.hud-container::before {
  content: '';
  position: absolute;
  top: -2px; left: -2px;
  width: 20px; height: 20px;
  border-top: 2px solid #4df;
  border-left: 2px solid #4df;
}
.hud-container::after {
  content: '';
  position: absolute;
  bottom: -2px; right: -2px;
  width: 20px; height: 20px;
  border-bottom: 2px solid #4df;
  border-right: 2px solid #4df;
}

.hud-value {
  font-size: 3rem;
  text-shadow: 0 0 10px rgba(68, 221, 255, 0.8);
}

.hud-warning {
  color: #ff3333;
  text-shadow: 0 0 10px rgba(255, 51, 51, 0.8);
  animation: blink 1s step-end infinite;
}

@keyframes blink { 50% { opacity: 0; } }
```

## App 实现

### SwiftUI
```swift
struct SciFiHUDView: View {
    @State private var bootUp = false
    
    var body: some View {
        ZStack {
            Color(hex: "000b18").ignoresSafeArea() // 深空海军蓝
            
            VStack {
                // 圆形雷达/表盘
                ZStack {
                    Circle()
                        .stroke(Color(hex: "4df").opacity(0.3), lineWidth: 1)
                    
                    Circle()
                        .trim(from: 0.0, to: bootUp ? 0.75 : 0.0)
                        .stroke(Color(hex: "4df"), style: StrokeStyle(lineWidth: 4, lineCap: .round))
                        .rotationEffect(.degrees(-90))
                    
                    Text("SYS.OK")
                        .font(.custom("Space Mono", size: 24))
                        .foregroundColor(Color(hex: "4df"))
                        .shadow(color: Color(hex: "4df"), radius: 5)
                }
                .frame(width: 200, height: 200)
                .padding(.bottom, 40)
                
                // HUD 数据框
                HStack {
                    Text("COORD: 45.22, 12.8")
                    Spacer()
                    Text("[ LOCK ]")
                }
                .font(.custom("Space Mono", size: 16))
                .foregroundColor(Color(hex: "4df"))
                .padding()
                .border(Color(hex: "4df").opacity(0.5), width: 1)
                .overlay(
                    // 角部括号装饰
                    Path { path in
                        path.move(to: CGPoint(x: 0, y: 15)); path.addLine(to: CGPoint(x: 0, y: 0)); path.addLine(to: CGPoint(x: 15, y: 0))
                        path.move(to: CGPoint(x: 300, y: 15)); path.addLine(to: CGPoint(x: 300, y: 0)); path.addLine(to: CGPoint(x: 285, y: 0))
                    }
                    .stroke(Color(hex: "4df"), lineWidth: 2)
                )
            }
            .padding()
        }
        .onAppear {
            withAnimation(.easeInOut(duration: 2.0)) { bootUp = true }
        }
    }
}
```
- SwiftUI 在 Sci-Fi HUD 上表现卓越。`Circle().trim(from: to:)` 让你构建复杂的扫掠圆形进度环。
- 使用 `Path` 叠加绘制精确的 90 度角括号（`[ ]`），这是 HUD 视觉的标志。

### Flutter
```dart
class SciFiHUDScreen extends StatefulWidget {
  @override
  State<SciFiHUDScreen> createState() => _SciFiHUDScreenState();
}

class _SciFiHUDScreenState extends State<SciFiHUDScreen> with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 2))..forward();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF000B18),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // 圆形雷达
            SizedBox(
              width: 200, height: 200,
              child: Stack(
                fit: StackFit.expand,
                children: [
                  CircularProgressIndicator(value: 1.0, strokeWidth: 1, color: const Color(0xFF44DDFF).withOpacity(0.3)),
                  AnimatedBuilder(
                    animation: _ctrl,
                    builder: (context, _) => CircularProgressIndicator(
                      value: _ctrl.value * 0.75, // 75% 填充
                      strokeWidth: 4,
                      color: const Color(0xFF44DDFF),
                    ),
                  ),
                  const Center(
                    child: Text('SYS.OK', style: TextStyle(fontFamily: 'SpaceMono', color: Color(0xFF44DDFF), fontSize: 24, shadows: [Shadow(color: Color(0xFF44DDFF), blurRadius: 5)])),
                  )
                ],
              ),
            ),
            const SizedBox(height: 40),
            
            // HUD 数据框（真正的角括号需要 CustomPaint）
            Container(
              width: 300,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(border: Border.all(color: const Color(0xFF44DDFF).withOpacity(0.5))),
              child: const Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('COORD: 45.22, 12.8', style: TextStyle(fontFamily: 'SpaceMono', color: Color(0xFF44DDFF))),
                  Text('[ LOCK ]', style: TextStyle(fontFamily: 'SpaceMono', color: Color(0xFF44DDFF))),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
```
- `CircularProgressIndicator` 是圆形 HUD 圆环的简易替代方案，但对于真正的 Sci-Fi 界面，你应该构建 `CustomPainter` 来绘制同心描边圆和弧线。
- 大量使用等宽字体和纯青色（`#44DDFF`）。

### React Native
```jsx
// 需要 react-native-svg
import Svg, { Circle, Path } from 'react-native-svg';

const SciFiHUDScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#000B18', justifyContent: 'center', alignItems: 'center' }}>
      
      {/* 圆形雷达 */}
      <View style={{ width: 200, height: 200, justifyContent: 'center', alignItems: 'center', marginBottom: 40 }}>
        <Svg height="200" width="200" style={{ position: 'absolute' }}>
          <Circle cx="100" cy="100" r="90" stroke="rgba(68, 221, 255, 0.3)" strokeWidth="1" fill="none" />
          <Circle cx="100" cy="100" r="90" stroke="#4df" strokeWidth="4" strokeDasharray="565" strokeDashoffset="140" fill="none" />
        </Svg>
        <Text style={{ fontFamily: 'monospace', color: '#4df', fontSize: 24, textShadowColor: '#4df', textShadowRadius: 5 }}>
          SYS.OK
        </Text>
      </View>

      {/* HUD 框 */}
      <View style={{ 
        width: 300, padding: 16, flexDirection: 'row', justifyContent: 'space-between',
        borderColor: 'rgba(68, 221, 255, 0.5)', borderWidth: 1 
      }}>
        <Text style={{ fontFamily: 'monospace', color: '#4df' }}>COORD: 45.22, 12.8</Text>
        <Text style={{ fontFamily: 'monospace', color: '#4df' }}>[ LOCK ]</Text>

        {/* 使用绝对定位 View 伪造角括号 */}
        <View style={{ position: 'absolute', top: -2, left: -2, width: 15, height: 15, borderTopWidth: 2, borderLeftWidth: 2, borderColor: '#4df' }} />
        <View style={{ position: 'absolute', bottom: -2, right: -2, width: 15, height: 15, borderBottomWidth: 2, borderRightWidth: 2, borderColor: '#4df' }} />
      </View>

    </View>
  );
};
```
- 必须使用 `react-native-svg` 绘制圆形 HUD 表盘。使用 `<Circle>` 的 `strokeDasharray` 和 `strokeDashoffset` 绘制弧线。
- 角括号通过绝对定位小 `View` 构建，每个 `View` 在容器角上启用 2 条边。

### Jetpack Compose
```kotlin
@Composable
fun SciFiHUDScreen() {
    // 启动动画
    val transition = rememberInfiniteTransition()
    val sweep by transition.animateFloat(initialValue = 0f, targetValue = 270f, animationSpec = infiniteRepeatable(tween(2000), RepeatMode.Restart))

    Column(
        modifier = Modifier.fillMaxSize().background(Color(0xFF000B18)),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        // 圆形雷达
        Box(contentAlignment = Alignment.Center, modifier = Modifier.size(200.dp)) {
            Canvas(modifier = Modifier.fillMaxSize()) {
                drawCircle(color = Color(0xFF44DDFF).copy(alpha = 0.3f), style = Stroke(width = 2f))
                drawArc(
                    color = Color(0xFF44DDFF),
                    startAngle = -90f,
                    sweepAngle = sweep,
                    useCenter = false,
                    style = Stroke(width = 8f, cap = StrokeCap.Round)
                )
            }
            Text("SYS.OK", color = Color(0xFF44DDFF), fontFamily = FontFamily.Monospace, fontSize = 24.sp)
        }
        
        Spacer(Modifier.height(40.dp))
        
        // HUD 框
        Box(modifier = Modifier.width(300.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth().border(1.dp, Color(0xFF44DDFF).copy(alpha = 0.5f)).padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("COORD: 45.22, 12.8", color = Color(0xFF44DDFF), fontFamily = FontFamily.Monospace)
                Text("[ LOCK ]", color = Color(0xFF44DDFF), fontFamily = FontFamily.Monospace)
            }
            
            // 通过 Canvas 绘制角括号
            Canvas(modifier = Modifier.fillMaxSize()) {
                val path = Path().apply {
                    moveTo(0f, 40f); lineTo(0f, 0f); lineTo(40f, 0f) // 左上
                    moveTo(size.width, size.height - 40f); lineTo(size.width, size.height); lineTo(size.width - 40f, size.height) // 右下
                }
                drawPath(path, color = Color(0xFF44DDFF), style = Stroke(width = 4f))
            }
        }
    }
}
```
- Jetpack Compose 的 `Canvas` 在此非常强大。使用 `drawArc` 绘制圆形 HUD 圆环。
- 使用覆盖在 Box 上的 `Canvas`，通过 `Path().apply { moveTo... lineTo... }` 绘制角括号。

## 推荐与避免
- **推荐**：让元素以"启动"或"校准"的方式动画进入屏幕（线条从 0 绘制到 100%）。
- **避免**：使用投影。HUD 中的光是发射的，不是被阻挡的。使用 `text-shadow` 制造发光。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。