---
name: brutalist-typography
description: Brutalist Typography 的 Web 与 App 实现指南。当用户需要巨型字体、粗犷呈现和激进布局决策时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Brutalist Typography

> "激进、未经修饰、不卑不亢。文字通过打破规则来博取关注。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **打破规则**：文字会重叠、忽略边距，或故意被屏幕边缘裁切。
2. **反设计**：刻意使用系统字体或"丑陋"字体（Times New Roman、Courier），尺寸巨大。
3. **生硬的对比度**：相互冲突的颜色或刺眼的单色。

## 视觉 DNA
- **颜色**：**Industrial Chic**（黑、白、红）或激进的霓虹冲突色（例如纯蓝配纯红）。
- **排版**：系统默认字体（`Times New Roman`、`Arial`、`Courier New`），放大到 150px。
- **样式**：跑马灯、闪烁文字、穿过下伸部的下划线。

## Web 实现
- 打破网格。使用绝对定位或负 margin。
- **CSS 示例**：
```css
body {
  background-color: #fff;
  color: #000;
  font-family: 'Times New Roman', serif;
}

.brutalist-headline {
  font-size: 15vw;
  line-height: 0.7;
  letter-spacing: -5px;
  margin-left: -10px; /* 故意溢出屏幕 */
  word-wrap: break-word; /* 让单词尴尬地换行 */
}

.brutalist-highlight {
  background-color: #ff0000;
  color: #fff;
  padding: 0 10px;
}

.marquee-container {
  border-top: 5px solid #000;
  border-bottom: 5px solid #000;
  overflow: hidden;
  white-space: nowrap;
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  font-weight: bold;
  padding: 10px 0;
}

/* 致敬 90 年代早期 Web */
.brutalist-link {
  color: #0000ee;
  text-decoration: underline;
  text-transform: uppercase;
}
.brutalist-link:hover {
  background-color: #0000ee;
  color: #fff;
}
```

## App 实现

### SwiftUI
```swift
struct BrutalistTypeView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: -20) {
                // 故意溢出边缘
                Text("BREAK")
                    .font(.custom("Times New Roman", size: 120))
                    .padding(.leading, -20) 
                
                Text("THE")
                    .font(.custom("Arial", size: 140))
                    .fontWeight(.black)
                    .foregroundColor(.clear)
                    .overlay(
                        Text("THE").stroke(Color.red, lineWidth: 3)
                    )
                    .offset(x: 40)
                
                Text("GRID.")
                    .font(.custom("Courier New", size: 100))
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .rotationEffect(.degrees(-5))
                    .offset(y: -40)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.top, 50)
        }
        .ignoresSafeArea() // 粗犷字体所必需
        .background(Color.white)
    }
}
```
- `.ignoresSafeArea()` 是必需的。文字必须允许侵入刘海和状态栏区域。
- 在 `VStack` 中使用负 `spacing` 或显式的负 `.offset()` 来强制文字元素相互激进重叠。
- 通过将 `.foregroundColor(.clear)` 与 `.stroke()` 叠加实现描边文字。

### Flutter
```dart
class BrutalistTypeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // 不使用 SafeArea 的 Scaffold
    return Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [
          Positioned(
            top: -20,
            left: -20,
            child: const Text(
              'BREAK',
              style: TextStyle(
                fontFamily: 'Times New Roman',
                fontSize: 150,
                height: 0.8, // 负的行间距
                color: Colors.black,
              ),
            ),
          ),
          Positioned(
            top: 100,
            left: 40,
            child: Text(
              'THE',
              style: TextStyle(
                fontFamily: 'Arial',
                fontSize: 140,
                fontWeight: FontWeight.w900,
                foreground: Paint()
                  ..style = PaintingStyle.stroke
                  ..strokeWidth = 3
                  ..color = Colors.red,
              ),
            ),
          ),
          Positioned(
            top: 220,
            left: 10,
            child: Transform.rotate(
              angle: -0.1,
              child: Container(
                color: Colors.blue,
                child: const Text(
                  'GRID.',
                  style: TextStyle(
                    fontFamily: 'Courier',
                    fontSize: 120,
                    color: Colors.white,
                  ),
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
- 不要使用 `SafeArea`。
- 通过 `Stack` 和 `Positioned` 进行绝对定位是打破网格、强制重叠最简单的方法。
- 在 `TextStyle` 中使用 `height: 0.8`（或小于 1.0 的值）来挤压文字行。

### React Native
```jsx
const BrutalistTypeScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#FFF' }}>
      {/* 
        注意：React Native 文字裁剪在 Android 上可能出问题。
        确保父级 View 没有 overflow: 'hidden'。
      */}
      <Text style={{
        fontFamily: 'Times New Roman',
        fontSize: 130,
        lineHeight: 110,
        color: '#000',
        marginLeft: -15, // 溢出边缘
        marginTop: 40
      }}>
        BREAK
      </Text>
      
      <Text style={{
        fontFamily: 'Arial',
        fontSize: 140,
        fontWeight: '900',
        color: 'transparent',
        textShadowColor: '#FF0000',
        textShadowRadius: 1, // 模拟描边效果
        marginLeft: 40,
        marginTop: -30 // 与上一段文字重叠
      }}>
        THE
      </Text>
      
      <Text style={{
        fontFamily: 'monospace',
        fontSize: 100,
        backgroundColor: '#0000FF',
        color: '#FFF',
        transform: [{ rotate: '-5deg' }],
        marginTop: -20,
        alignSelf: 'flex-start'
      }}>
        GRID.
      </Text>
    </View>
  );
};
```
- React Native 没有原生文字描边属性，可以模拟文字阴影来近似，或使用 `@shopify/react-native-skia` 实现真正的描边文字。
- 使用负 `marginTop` 和 `marginLeft` 来强制布局混乱。

### Jetpack Compose
```kotlin
@Composable
fun BrutalistTypeScreen() {
    // 使用 Box 进行绝对重叠布局
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
    ) {
        Text(
            text = "BREAK",
            fontFamily = FontFamily.Serif, // Times New Roman 等效
            fontSize = 130.sp,
            color = Color.Black,
            lineHeight = 100.sp,
            modifier = Modifier.offset(x = (-15).dp, y = (-20).dp)
        )
        
        Text(
            text = "THE",
            fontFamily = FontFamily.SansSerif,
            fontSize = 140.sp,
            fontWeight = FontWeight.Black,
            style = TextStyle(
                drawStyle = Stroke(width = 5f)
            ),
            color = Color.Red,
            modifier = Modifier.offset(x = 40.dp, y = 100.dp)
        )
        
        Text(
            text = "GRID.",
            fontFamily = FontFamily.Monospace,
            fontSize = 100.sp,
            color = Color.White,
            modifier = Modifier
                .offset(x = 10.dp, y = 220.dp)
                .rotate(-5f)
                .background(Color.Blue)
        )
    }
}
```
- `Box` 与显式 `Modifier.offset(x, y)` 配合，可实现自由重叠排版，摆脱标准的 `Column`/`Row` 网格。
- Compose 的 `TextStyle` 支持 `drawStyle = Stroke(width = 5f)`，让描边排版变得异常简单。

## 推荐与避免
- **推荐**：大胆混用衬线字体和等宽字体。
- **避免**：添加投影、渐变或圆角。设计必须看起来原始、未经修饰。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。