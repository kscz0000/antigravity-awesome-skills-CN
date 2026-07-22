---
name: tile-design
description: Tile Design（Metro UI）的 Web 与 App 实现指南。当用户希望微软 Metro 风格、锐利方形信息单元和水平滚动网格时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Tile Design（Metro UI）

> "原生数字化。干净、锐利的方块，完全依靠排版和纯色构建。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **锐利的角**：绝对没有圆角。一切都是完美的正方形或锐利矩形。
2. **实时数据**：瓦片在内部翻转、滚动或淡入以显示实时更新，无需用户交互。
3. **水平平移**：网格经常向右无限扩展，鼓励水平滚动。

## 视觉 DNA
- **颜色**：高饱和度、纯色。暗色背景（纯黑）配以亮青色、品红、橙色和绿色瓦片。
- **排版**：极其干净、浅色无衬线字体（如 `Segoe UI Light`）。文字几乎总是纯白色。
- **图标**：简单、线框、单色字形，居中或置于角落。

## Web 实现
- **CSS 示例**：
```css
body {
  background-color: #111;
  color: #fff;
  font-family: 'Segoe UI', sans-serif;
  overflow-x: auto; /* 水平滚动 */
}

.tile-group {
  display: grid;
  grid-template-columns: repeat(4, 150px);
  grid-auto-rows: 150px;
  gap: 8px;
  padding: 40px;
}

.tile {
  background-color: #0078D7; /* 经典 Windows 蓝 */
  padding: 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  
  /* "倾斜"点击效果 */
  transition: transform 0.1s;
  transform-origin: center;
}

.tile:active {
  transform: scale(0.95);
}

.tile-wide { grid-column: span 2; }
.tile-large { grid-column: span 2; grid-row: span 2; }

/* 实时瓦片动画 */
.tile-live-content {
  animation: slideUp 5s infinite;
}

@keyframes slideUp {
  0%, 45% { transform: translateY(0); }
  50%, 95% { transform: translateY(-100%); } /* 向上滑动以揭示下一项 */
  100% { transform: translateY(0); }
}
```

## App 实现

### SwiftUI
```swift
struct TileDesignView: View {
    let rows = [GridItem(.fixed(150), spacing: 8), GridItem(.fixed(150), spacing: 8)]
    
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            LazyHGrid(rows: rows, spacing: 8) {
                TileView(title: "Mail", color: Color(hex: "0078D7"), icon: "envelope")
                TileView(title: "Photos", color: Color(hex: "00CC6A"), icon: "photo", isLarge: true)
                TileView(title: "Weather", color: Color(hex: "2D7D9A"), icon: "cloud.sun")
                TileView(title: "Calendar", color: Color(hex: "D13438"), icon: "calendar")
            }
            .padding(40)
        }
        .background(Color(hex: "111111").ignoresSafeArea())
    }
}

struct TileView: View {
    let title: String
    let color: Color
    let icon: String
    var isLarge: Bool = false
    
    @State private var isPressed = false
    
    var body: some View {
        VStack(alignment: .leading) {
            Image(systemName: icon)
                .font(.system(size: 32, weight: .light))
                .foregroundColor(.white)
            Spacer()
            Text(title)
                .font(.custom("Segoe UI", size: 16))
                .foregroundColor(.white)
        }
        .padding(16)
        // 锐利的角是必需的
        .frame(width: isLarge ? 308 : 150, height: isLarge ? 308 : 150, alignment: .leading)
        .background(color)
        .scaleEffect(isPressed ? 0.95 : 1.0)
        .animation(.spring(response: 0.2, dampingFraction: 0.5), value: isPressed)
        .onLongPressGesture(minimumDuration: .infinity, maximumDistance: .infinity, pressing: { pressing in
            isPressed = pressing
        }, perform: {})
    }
}
```
- 水平 `ScrollView` 内的 `LazyHGrid` 完美复刻了 Windows Phone / Windows 8 开始屏幕。
- 绝对不要圆角。
- `isPressed` 状态触发 `.scaleEffect(0.95)` 复刻 Metro 瓦片的物理"倾斜"交互。

### Flutter
```dart
class TileDesignScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF111111),
      body: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.all(40),
        child: SizedBox(
          height: 308, // 两行 150px + 8px 间距
          child: Wrap(
            direction: Axis.vertical,
            spacing: 8,
            runSpacing: 8,
            children: [
              _buildTile('Mail', const Color(0xFF0078D7), Icons.mail_outline),
              _buildTile('Weather', const Color(0xFF2D7D9A), Icons.cloud_outlined),
              _buildTile('Photos', const Color(0xFF00CC6A), Icons.photo_outlined, isLarge: true),
              _buildTile('Calendar', const Color(0xFFD13438), Icons.calendar_today),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTile(String title, Color color, IconData icon, {bool isLarge = false}) {
    return StatefulBuilder(
      builder: (context, setState) {
        bool isPressed = false;
        return GestureDetector(
          onTapDown: (_) => setState(() => isPressed = true),
          onTapUp: (_) => setState(() => isPressed = false),
          onTapCancel: () => setState(() => isPressed = false),
          child: AnimatedScale(
            scale: isPressed ? 0.95 : 1.0,
            duration: const Duration(milliseconds: 100),
            child: Container(
              width: isLarge ? 308 : 150,
              height: isLarge ? 308 : 150,
              color: color, // 锐利的角
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Icon(icon, color: Colors.white, size: 32),
                  Text(title, style: const TextStyle(color: Colors.white, fontFamily: 'Segoe UI', fontSize: 16)),
                ],
              ),
            ),
          ),
        );
      }
    );
  }
}
```
- 水平滚动 `SizedBox` 中的 `Wrap` 配合 `direction: Axis.vertical` 是构建从左到右流动的 Metro 网格的最简单方法。
- 将瓦片包裹在 `GestureDetector` 和 `AnimatedScale` 中处理按下动画。

### React Native
```jsx
const TileDesignScreen = () => {
  return (
    <ScrollView horizontal style={{ flex: 1, backgroundColor: '#111' }} contentContainerStyle={{ padding: 40 }}>
      <View style={{ flexDirection: 'column', flexWrap: 'wrap', height: 308, gap: 8 }}>
        
        <Tile title="Mail" color="#0078D7" />
        <Tile title="Weather" color="#2D7D9A" />
        <Tile title="Photos" color="#00CC6A" isLarge />
        <Tile title="Calendar" color="#D13438" />

      </View>
    </ScrollView>
  );
};

const Tile = ({ title, color, isLarge }) => {
  const scale = useRef(new Animated.Value(1)).current;

  const handlePressIn = () => Animated.spring(scale, { toValue: 0.95, useNativeDriver: true }).start();
  const handlePressOut = () => Animated.spring(scale, { toValue: 1, useNativeDriver: true }).start();

  return (
    <TouchableWithoutFeedback onPressIn={handlePressIn} onPressOut={handlePressOut}>
      <Animated.View style={{
        width: isLarge ? 308 : 150, height: isLarge ? 308 : 150,
        backgroundColor: color, padding: 16, justifyContent: 'space-between',
        transform: [{ scale }] // Metro 倾斜效果
      }}>
        <View style={{ width: 32, height: 32, backgroundColor: '#FFF', opacity: 0.5 }} />
        <Text style={{ color: '#FFF', fontFamily: 'Segoe UI', fontSize: 16 }}>{title}</Text>
      </Animated.View>
    </TouchableWithoutFeedback>
  );
};
```
- 使用 `<ScrollView horizontal>` 配合一个带固定 `height` 和 `flexWrap: 'wrap', flexDirection: 'column'` 的子 `<View>`。这强制子元素形成列并水平流动。
- 使用 `Animated.View` 和 `TouchableWithoutFeedback` 创建缩放动画。

### Jetpack Compose
```kotlin
@Composable
fun TileDesignScreen() {
    LazyHorizontalGrid(
        rows = GridCells.Fixed(2),
        modifier = Modifier.fillMaxSize().background(Color(0xFF111111)),
        contentPadding = PaddingValues(40.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item(span = { GridItemSpan(1) }) { Tile("Mail", Color(0xFF0078D7)) }
        // 注意：LazyHorizontalGrid 不容易支持跨多行（2x2 瓦片）。
        // 对于真正的 Metro 布局，通常必须构建自定义 Layout 或使用瀑布流网格。
        item(span = { GridItemSpan(2) }) { Tile("Photos Wide", Color(0xFF00CC6A)) } 
        item(span = { GridItemSpan(1) }) { Tile("Weather", Color(0xFF2D7D9A)) }
    }
}

@Composable
fun Tile(title: String, color: Color) {
    var isPressed by remember { mutableStateOf(false) }
    val scale by animateFloatAsState(if (isPressed) 0.95f else 1.0f)

    Box(
        modifier = Modifier
            .size(150.dp) // 或根据参数宽/大
            .scale(scale)
            .background(color) // 锐利的角！没有 RoundedCornerShape
            .pointerInput(Unit) {
                detectTapGestures(
                    onPress = {
                        isPressed = true
                        tryAwaitRelease()
                        isPressed = false
                    }
                )
            }
            .padding(16.dp)
    ) {
        // 图标
        Box(modifier = Modifier.size(32.dp).background(Color.White.copy(alpha = 0.5f)).align(Alignment.TopStart))
        // 文字
        Text(
            text = title,
            color = Color.White,
            fontFamily = FontFamily.SansSerif,
            modifier = Modifier.align(Alignment.BottomStart)
        )
    }
}
```
- `LazyHorizontalGrid` 是正确的工具，尽管构建真正的 2x2"大"瓦片需要自定义布局数学（如果与 1x1 瓦片混合）。
- `Modifier.scale()` 配合 `pointerInput` 的 `detectTapGestures` 处理 Metro 交互。

## 推荐与避免
- **推荐**：将瓦片标签文字严格放在瓦片的左下角。
- **避免**：为瓦片添加投影或渐变。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。