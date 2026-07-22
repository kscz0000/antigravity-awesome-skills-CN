---
name: color-blocking
description: Color Blocking 的 Web 与 App 实现指南。当用户需要大面积色块、醒目的版面分割或蒙德里安风格网格时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Color Blocking

> "网格可视化。大面积、对比鲜明的纯色块定义版式。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **几何分割**：视口被分割为大型矩形或正方形，每块填充纯色。
2. **色块之间无间距**：色块直接相邻，通常仅由 1px 或 2px 的纯黑线分隔（或无线条，颜色直接碰撞）。
3. **文字作为纹理**：文字被精确放置在这些色块中，平衡色彩的视觉重量。

## 视觉 DNA
- **颜色**：高对比度、大胆的搭配。使用 3 到 4 种强烈的颜色，如 **Industrial Chic**（红、黑、灰、白）或自定义大胆配色（黄、海军蓝、粉）。
- **排版**：非常干净、粗壮的无衬线字体，能在大面积色块中保持存在感。
- **边框**：经常使用粗黑色边框（`2px solid #000`）强调网格，让人联想到蒙德里安绘画。

## Web 实现
- CSS Grid 是有效构建此风格的唯一方法。
- **CSS 示例**：
```css
body {
  margin: 0;
  font-family: 'Space Grotesk', sans-serif;
  color: #000;
}

.color-block-grid {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  grid-template-rows: 60vh 40vh;
  /* 色块之间的粗黑线 */
  gap: 4px;
  background-color: #000; 
  border: 4px solid #000;
  min-height: 100vh;
}

.block {
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.block-yellow { background-color: #FACC15; }
.block-white  { background-color: #FFFFFF; }
.block-blue   { background-color: #2563EB; color: #FFF; }
.block-red    { background-color: #EF4444; }

.block-title {
  font-size: 3rem;
  font-weight: 900;
  text-transform: uppercase;
  margin: 0;
}
```

## App 实现

### SwiftUI
```swift
struct ColorBlockingView: View {
    let gridSpacing: CGFloat = 4 // 黑色线条的厚度
    
    var body: some View {
        // 黑色背景充当色块之间的网格线
        VStack(spacing: gridSpacing) {
            // 顶部行
            HStack(spacing: gridSpacing) {
                ColorBlock(color: .yellow, text: "CREATE", textColor: .black)
                ColorBlock(color: .blue, text: "VISION", textColor: .white)
            }
            .frame(height: 300)
            
            // 底部行
            HStack(spacing: gridSpacing) {
                ColorBlock(color: .red, text: "BOLD", textColor: .white)
                    .frame(width: 120) // 固定窄块
                ColorBlock(color: .white, text: "MINIMAL", textColor: .black)
            }
        }
        .background(Color.black) // 网格线
        .border(Color.black, width: gridSpacing) // 外边框
        .ignoresSafeArea()
    }
}

struct ColorBlock: View {
    let color: Color
    let text: String
    let textColor: Color
    var body: some View {
        color
            .overlay(
                Text(text)
                    .font(.system(size: 32, weight: .black))
                    .foregroundColor(textColor)
                    .padding(),
                alignment: .bottomLeading
            )
    }
}
```
- 在 SwiftUI 中，创建蒙德里安式粗黑网格线的最简单方法是在父级 stack 上设置 `.background(Color.black)` 并使用 `spacing: 4`。背景会从间隙中透出。
- `.ignoresSafeArea()` 允许色块延伸到物理设备的边缘。

### Flutter
```dart
class ColorBlockingScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 黑色背景创建网格线
      backgroundColor: Colors.black,
      body: SafeArea(
        bottom: false,
        child: Column(
          children: [
            // 顶部行
            Expanded(
              flex: 3, // 占 3/5 垂直空间
              child: Row(
                children: [
                  Expanded(flex: 1, child: ColorBlock(color: const Color(0xFFFACC15), text: 'CREATE', textColor: Colors.black)),
                  const SizedBox(width: 4), // 网格线
                  Expanded(flex: 2, child: ColorBlock(color: const Color(0xFF2563EB), text: 'VISION', textColor: Colors.white)),
                ],
              ),
            ),
            const SizedBox(height: 4), // 水平网格线
            // 底部行
            Expanded(
              flex: 2, // 占 2/5 垂直空间
              child: Row(
                children: [
                  Expanded(flex: 1, child: ColorBlock(color: const Color(0xFFEF4444), text: 'BOLD', textColor: Colors.white)),
                  const SizedBox(width: 4),
                  Expanded(flex: 2, child: ColorBlock(color: Colors.white, text: 'MINIMAL', textColor: Colors.black)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class ColorBlock extends StatelessWidget {
  final Color color;
  final String text;
  final Color textColor;
  const ColorBlock({required this.color, required this.text, required this.textColor});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: color,
      padding: const EdgeInsets.all(24),
      alignment: Alignment.bottomLeft,
      child: Text(text, style: TextStyle(fontSize: 32, fontWeight: FontWeight.w900, color: textColor)),
    );
  }
}
```
- 使用不同 `flex` 比例的 `Expanded` 以几何方式划分屏幕。
- 在行和列之间插入 `SizedBox(width: 4)` 或 `height: 4`，露出黑色 `Scaffold` 背景，从而形成网格线。

### React Native
```jsx
const ColorBlockingScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#000', gap: 4 }}>
      {/* 顶部行 */}
      <View style={{ flex: 3, flexDirection: 'row', gap: 4 }}>
        <View style={[styles.block, { flex: 1, backgroundColor: '#FACC15' }]}>
          <Text style={[styles.text, { color: '#000' }]}>CREATE</Text>
        </View>
        <View style={[styles.block, { flex: 2, backgroundColor: '#2563EB' }]}>
          <Text style={[styles.text, { color: '#FFF' }]}>VISION</Text>
        </View>
      </View>
      
      {/* 底部行 */}
      <View style={{ flex: 2, flexDirection: 'row', gap: 4 }}>
        <View style={[styles.block, { flex: 1, backgroundColor: '#EF4444' }]}>
          <Text style={[styles.text, { color: '#FFF' }]}>BOLD</Text>
        </View>
        <View style={[styles.block, { flex: 2, backgroundColor: '#FFF' }]}>
          <Text style={[styles.text, { color: '#000' }]}>MINIMAL</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  block: {
    justifyContent: 'flex-end',
    padding: 24,
  },
  text: {
    fontSize: 32,
    fontWeight: '900',
    fontFamily: 'SpaceGrotesk-Bold',
  }
});
```
- React Native flexbox 中的 `gap` 属性让这变得简单。在父级设置黑色背景、`gap: 4`，子元素自动留出间距，露出粗黑线。
- 使用 `flex: 1`、`flex: 2` 等决定色块的比例。

### Jetpack Compose
```kotlin
@Composable
fun ColorBlockingScreen() {
    val gridSpacing = 4.dp
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black) // 网格线
    ) {
        // 顶部行
        Row(
            modifier = Modifier.weight(3f),
            horizontalArrangement = Arrangement.spacedBy(gridSpacing)
        ) {
            ColorBlock(Color(0xFFFACC15), "CREATE", Color.Black, Modifier.weight(1f))
            ColorBlock(Color(0xFF2563EB), "VISION", Color.White, Modifier.weight(2f))
        }
        
        Spacer(Modifier.height(gridSpacing))
        
        // 底部行
        Row(
            modifier = Modifier.weight(2f),
            horizontalArrangement = Arrangement.spacedBy(gridSpacing)
        ) {
            ColorBlock(Color(0xFFEF4444), "BOLD", Color.White, Modifier.weight(1f))
            ColorBlock(Color.White, "MINIMAL", Color.Black, Modifier.weight(2f))
        }
    }
}

@Composable
fun ColorBlock(color: Color, text: String, textColor: Color, modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .fillMaxHeight()
            .background(color)
            .padding(24.dp),
        contentAlignment = Alignment.BottomStart
    ) {
        Text(text, fontSize = 32.sp, fontWeight = FontWeight.Black, color = textColor)
    }
}
```
- 与其他移动框架一样，`Modifier.background(Color.Black)` 与 `Arrangement.spacedBy(4.dp)` 完美地创建蒙德里安网格。
- 使用 `Modifier.weight(Xf)` 以数学方式划分屏幕空间。

## 推荐与避免
- **推荐**：确保极致的对比度。黄色块上的文字应为黑色。深蓝色块上的文字应为白色。
- **避免**：使用投影、圆角或渐变。保持完全扁平、锐利。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。