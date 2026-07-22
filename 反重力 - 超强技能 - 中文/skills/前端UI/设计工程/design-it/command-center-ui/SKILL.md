---
name: command-center-ui
description: Command Center UI 的 Web 与 App 实现指南。当用户需要监控系统、企业仪表板、NOC（网络运营中心）和全球地图时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Command Center UI

> "任务控制中心。全球监控、实时告警和高赌注的数据可视化。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **深色/黑色背景**：对于充满发光屏幕的房间（NOC）至关重要。它让数据跃然屏上，减少眩光。
2. **地图与拓扑图**：UI 的中心几乎总是一个暗色模式的地理地图或基于节点的网络拓扑。
3. **告警层级**：90% 的屏幕平静而呈蓝灰色。一旦出现警告，会闪烁亮黄色或红色，立刻吸引眼球。

## 视觉 DNA
- **颜色**：纯黑（`#000000`）或深海军蓝（`#0B132B`）。强调色为电青色（`#00FFFF`）、琥珀色（`#FFBF00`）和警示红色（`#FF0000`）。
- **排版**：干净、技术导向的无衬线字体（`Orbitron`、`Roboto`、`Share Tech`）。
- **样式**：发光边框、雷达扫描、生硬的数据驱动图表。

## Web 实现
- **CSS 示例**：
```css
body {
  background-color: #030a16;
  color: #8ab4f8;
  font-family: 'Roboto', sans-serif;
  margin: 0;
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  height: 100vh;
}

.panel {
  background-color: rgba(13, 27, 42, 0.8);
  border: 1px solid #1c355e;
  box-shadow: inset 0 0 20px rgba(0, 255, 255, 0.05);
  margin: 10px;
  display: flex;
  flex-direction: column;
}

.panel-header {
  background: linear-gradient(90deg, #1c355e, transparent);
  color: #00ffff;
  padding: 8px 16px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  border-bottom: 1px solid #00ffff;
}

/* 地图/主视图 */
.main-view {
  /* 占位巨大的地球或地图 */
  background: radial-gradient(circle, #0d1b2a 0%, #030a16 100%);
  position: relative;
}

/* 关键告警 */
.alert-critical {
  background-color: rgba(255, 0, 0, 0.1);
  border: 1px solid #ff0000;
  color: #ff0000;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  animation: pulse-red 2s infinite;
}

@keyframes pulse-red {
  0% { box-shadow: 0 0 5px rgba(255, 0, 0, 0.2); }
  50% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.8); }
  100% { box-shadow: 0 0 5px rgba(255, 0, 0, 0.2); }
}
```

## App 实现

### SwiftUI
```swift
struct CommandCenterView: View {
    @State private var isAlerting = false
    
    var body: some View {
        VStack(spacing: 16) {
            // 标题
            HStack {
                Text("GLOBAL_OPS // ALPHA")
                    .font(.custom("Orbitron", size: 20))
                    .foregroundColor(Color(red: 0.0, green: 1.0, blue: 1.0)) // 青色
                Spacer()
                Text(Date(), style: .time).foregroundColor(.gray)
            }
            .padding()
            .border(Color(red: 0.0, green: 1.0, blue: 1.0), width: 1)
            
            // 地图或主视觉占位
            Circle()
                .strokeBorder(
                    LinearGradient(colors: [.cyan, .blue], startPoint: .top, endPoint: .bottom),
                    lineWidth: 2
                )
                .frame(height: 250)
                .overlay(Text("TOPOLOGY SCAN").foregroundColor(.cyan.opacity(0.5)))
            
            // 关键告警面板
            VStack(alignment: .leading) {
                Text("WARNING: SECTOR 7G")
                    .font(.headline)
                    .foregroundColor(.red)
                Text("Anomalous activity detected.")
                    .font(.subheadline)
                    .foregroundColor(.white)
            }
            .padding()
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(Color.red.opacity(0.1))
            .border(Color.red, width: 2)
            .shadow(color: isAlerting ? .red : .clear, radius: 10)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color(red: 0.01, green: 0.04, blue: 0.09)) // 极深的海军蓝
        .onAppear {
            withAnimation(.easeInOut(duration: 1.0).repeatForever()) {
                isAlerting.toggle()
            }
        }
    }
}
```
- 大量依赖 `.border()` 和 `.strokeBorder()` 配合渐变来创建技术性发光线框。
- 持续对 `.shadow()` 进行动画以实现脉冲告警。

### Flutter
```dart
class CommandCenterScreen extends StatefulWidget {
  @override
  State<CommandCenterScreen> createState() => _CommandCenterScreenState();
}

class _CommandCenterScreenState extends State<CommandCenterScreen> with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(vsync: this, duration: const Duration(seconds: 1))..repeat(reverse: true);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF030A16), // 深色 NOC 背景
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // 面板标题
              Container(
                padding: const EdgeInsets.all(12),
                decoration: const BoxDecoration(
                  border: Border(bottom: BorderSide(color: Colors.cyan)),
                  gradient: LinearGradient(colors: [Color(0xFF1C355E), Colors.transparent]),
                ),
                child: const Text('GLOBAL_OPS // ALPHA', 
                  style: TextStyle(color: Colors.cyan, fontFamily: 'Orbitron', letterSpacing: 2)),
              ),
              const SizedBox(height: 24),
              // 地图占位
              Expanded(
                child: Container(
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.cyan.withOpacity(0.5), width: 2),
                  ),
                  child: const Center(child: Text('RADAR ACTIVE', style: TextStyle(color: Colors.cyan))),
                ),
              ),
              const SizedBox(height: 24),
              // 动画关键告警
              AnimatedBuilder(
                animation: _pulseController,
                builder: (context, child) {
                  return Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.red.withOpacity(0.1),
                      border: Border.all(color: Colors.red),
                      boxShadow: [
                        BoxShadow(color: Colors.red.withOpacity(_pulseController.value * 0.8), blurRadius: 20)
                      ],
                    ),
                    child: const Text('WARNING: SECTOR 7G', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```
- 使用渐变到 `Colors.transparent` 的 `LinearGradient` 容器，非常适合高科技标题。
- 使用 `AnimatedBuilder` 操控 `BoxShadow` 的 `blurRadius` 和不透明度，创建闪烁告警面板。

### React Native
```jsx
const CommandCenterScreen = () => {
  const pulseAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1, duration: 1000, useNativeDriver: false }),
        Animated.timing(pulseAnim, { toValue: 0, duration: 1000, useNativeDriver: false })
      ])
    ).start();
  }, []);

  const shadowOpacity = pulseAnim.interpolate({ inputRange: [0, 1], outputRange: [0.2, 1] });

  return (
    <View style={{ flex: 1, backgroundColor: '#030A16', padding: 16 }}>
      {/* 标题面板 */}
      <View style={{
        borderBottomWidth: 1, borderColor: '#00FFFF', padding: 12, backgroundColor: '#1C355E'
      }}>
        <Text style={{ color: '#00FFFF', fontFamily: 'monospace', letterSpacing: 2 }}>
          GLOBAL_OPS // ALPHA
        </Text>
      </View>

      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <View style={{
          width: 250, height: 250, borderRadius: 125, borderWidth: 2, borderColor: '#00FFFF',
          justifyContent: 'center', alignItems: 'center'
        }}>
          <Text style={{ color: '#00FFFF', opacity: 0.5 }}>SCANNING...</Text>
        </View>
      </View>

      {/* 关键告警 */}
      <Animated.View style={{
        backgroundColor: 'rgba(255,0,0,0.1)',
        borderWidth: 2, borderColor: '#FF0000', padding: 16,
        shadowColor: '#FF0000', shadowRadius: 15, shadowOpacity, elevation: 10
      }}>
        <Text style={{ color: '#FF0000', fontWeight: 'bold', fontSize: 18 }}>WARNING: SECTOR 7G</Text>
        <Text style={{ color: '#FFF' }}>Anomalous activity detected.</Text>
      </Animated.View>
    </View>
  );
};
```
- 依赖锐利的 1px 或 2px 边框配合明亮的十六进制色值（`#00FFFF`、`#FF0000`），而非圆角。
- 保持背景是极深的海军蓝（`#030A16`）而非纯黑，以避免 OLED 涂抹感，同时保留 NOC 质感。

### Jetpack Compose
```kotlin
@Composable
fun CommandCenterScreen() {
    val infiniteTransition = rememberInfiniteTransition()
    val pulseAlpha by infiniteTransition.animateFloat(
        initialValue = 0.2f,
        targetValue = 1.0f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF030A16))
            .padding(16.dp)
    ) {
        // 标题
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(Brush.horizontalGradient(listOf(Color(0xFF1C355E), Color.Transparent)))
                .border(width = 1.dp, color = Color.Cyan) // 简化边框
                .padding(12.dp)
        ) {
            Text("GLOBAL_OPS // ALPHA", color = Color.Cyan, fontFamily = FontFamily.Monospace, letterSpacing = 2.sp)
        }
        
        Spacer(Modifier.height(32.dp))
        
        // 主视觉
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(250.dp)
                    .border(2.dp, Color.Cyan.copy(alpha = 0.5f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Text("SCANNING...", color = Color.Cyan.copy(alpha = 0.5f))
            }
        }
        
        Spacer(Modifier.height(32.dp))
        
        // 关键告警
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .shadow(20.dp, spotColor = Color.Red.copy(alpha = pulseAlpha), ambientColor = Color.Red.copy(alpha = pulseAlpha))
                .background(Color.Red.copy(alpha = 0.1f))
                .border(2.dp, Color.Red)
                .padding(16.dp)
        ) {
            Text("WARNING: SECTOR 7G", color = Color.Red, fontWeight = FontWeight.Bold, fontSize = 18.sp)
            Text("Anomalous activity detected.", color = Color.White)
        }
    }
}
```
- Compose 很好地处理霓虹界面。使用 `Modifier.border(..., CircleShape)` 创建雷达圈。
- 在 Compose 中让容器发光，必须使用 `Modifier.shadow`，并将 `spotColor` 和 `ambientColor` 设置为霓虹色，绕过默认的黑色阴影。

## 推荐与避免
- **推荐**：营造明确的视觉节奏。在特定告警需要关注之前，屏幕应保持平静。
- **避免**：用明亮的纯白色面板填满屏幕。指挥中心应柔和发光，而不是让用户眼花。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。