---
name: typography-first
description: Typography First Design 的 Web 与 App 实现指南。当用户希望文字成为绝对主要视觉元素、最小化 UI chroming 时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Typography First Design

> "文字就是界面。没有干扰，只有美丽的文字。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **超尺寸排版**：主标题大到成为抽象的图形元素。
2. **极简 UI 装饰**：按钮就是文字。导航就是文字。没有盒子，没有背景。
3. **动态排版**：文字移动、滚动或响应光标。

## 视觉 DNA
- **颜色**：极致高对比度。纯黑与白，或非常深的背景搭配单一的霓虹强调色。**Midnight Luxury** 效果很好。
- **排版**：极具个性的展示字体。使用 `Oswald`、`Anton` 或 `Bebas Neue` 营造冲击力，或巨型衬线。
- **布局**：经常将巨型文字完美居中放置在视口中，在边缘处裁切。

## Web 实现
- 依赖 `vw` 和 `vh` 单位进行字号缩放，让文字完美填满屏幕。
- **CSS 示例**：
```css
body {
  background-color: #0A0A0A;
  color: #F5F5F0;
  overflow-x: hidden;
  margin: 0;
}

.hero-type {
  font-family: 'Anton', sans-serif;
  font-size: 25vw; /* 填满屏幕宽度 */
  text-transform: uppercase;
  line-height: 0.8;
  white-space: nowrap;
  
  /* 描边效果 */
  color: transparent;
  -webkit-text-stroke: 2px #F5F5F0;
  transition: color 0.3s;
}

.hero-type:hover {
  color: var(--cta-highlight);
  -webkit-text-stroke: 0;
}

.nav-text-btn {
  background: none;
  border: none;
  color: #F5F5F0;
  font-size: 2rem;
  font-family: 'Helvetica Neue', sans-serif;
  text-decoration: underline;
  text-underline-offset: 8px;
  cursor: pointer;
}
```

## App 实现

### SwiftUI
```swift
struct TypographyFirstView: View {
    var body: some View {
        ZStack {
            Color(hex: "0A0A0A").ignoresSafeArea()
            
            VStack {
                // 溢出边缘的巨型排版
                Text("THE WORDS ARE THE INTERFACE")
                    .font(.custom("Anton", size: 200)) // 荒谬地大
                    .foregroundColor(Color(hex: "F5F5F0"))
                    .lineLimit(1)
                    .fixedSize(horizontal: true, vertical: false) // 强制不换行
                    .minimumScaleFactor(1.0) // 防止自动缩小
                
                // 描边变体
                Text("NO CHROMING")
                    .font(.custom("Anton", size: 150))
                    .foregroundColor(.clear)
                    .overlay(
                        Text("NO CHROMING")
                            .font(.custom("Anton", size: 150))
                            .foregroundColor(Color(hex: "0A0A0A"))
                            // SwiftUI 中文字描边的技巧
                            .shadow(color: Color(hex: "F5F5F0"), radius: 1)
                    )
                    .lineLimit(1)
                    .fixedSize()
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.leading, -20) // 故意裁切
        }
    }
}
```
- 使用 `.fixedSize(horizontal: true, vertical: false)` 和 `.lineLimit(1)` 强制巨型字体溢出屏幕边缘而不是换行成段落。
- 原生文字描边在 SwiftUI 中很困难；重叠遮罩文字或使用细阴影是常见的变通方法。

### Flutter
```dart
class TypographyFirstScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0A0A0A),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 自动缩放英雄文字
            FittedBox(
              fit: BoxFit.cover,
              child: Text(
                'THE WORDS ARE',
                style: TextStyle(fontFamily: 'Anton', color: const Color(0xFFF5F5F0), height: 0.8),
              ),
            ),
            
            // 描边文字
            FittedBox(
              fit: BoxFit.cover,
              child: Stack(
                children: [
                  // 描边
                  Text(
                    'THE INTERFACE',
                    style: TextStyle(
                      fontFamily: 'Anton', height: 0.8,
                      foreground: Paint()..style = PaintingStyle.stroke..strokeWidth = 2..color = const Color(0xFFF5F5F0),
                    ),
                  ),
                  // 实色填充（透明）
                  const Text('THE INTERFACE', style: TextStyle(fontFamily: 'Anton', height: 0.8, color: Colors.transparent)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```
- `FittedBox` 配合 `BoxFit.cover` 是你最好的朋友。它确保文字在任何设备屏幕上都能占据最大可能的宽度/高度。
- Flutter 通过 `foreground: Paint()..style = PaintingStyle.stroke` 在 `TextStyle` 中轻松实现文字描边。

### React Native
```jsx
const { width } = Dimensions.get('window');

const TypographyFirstScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#0A0A0A', justifyContent: 'center' }}>
      
      {/* 巨型文字 */}
      <Text 
        numberOfLines={1} 
        style={{ fontFamily: 'Anton-Regular', fontSize: width * 0.4, color: '#F5F5F0', lineHeight: width * 0.35, marginLeft: -20 }}
      >
        WORDS ARE
      </Text>

      {/* 描边文字（React Native 标准 Text 原生不支持；需要 SVG 或阴影） */}
      <Text 
        numberOfLines={1} 
        style={{ 
          fontFamily: 'Anton-Regular', fontSize: width * 0.35, color: '#0A0A0A', lineHeight: width * 0.3,
          textShadowColor: '#F5F5F0', textShadowOffset: {width: -1, height: 1}, textShadowRadius: 1
        }}
      >
        INTERFACE
      </Text>

      {/* 排版按钮 */}
      <TouchableOpacity style={{ marginTop: 40, alignSelf: 'center' }}>
        <Text style={{ color: '#F5F5F0', fontSize: 24, textDecorationLine: 'underline' }}>
          Explore Now
        </Text>
      </TouchableOpacity>

    </View>
  );
};
```
- 依赖 `Dimensions.get('window').width` 动态计算极端字号（例如 `fontSize: width * 0.4`）。
- 使用 `numberOfLines={1}` 和负 margin 让文字表现得像溢出的图形元素。

### Jetpack Compose
```kotlin
@Composable
fun TypographyFirstScreen() {
    Column(
        modifier = Modifier.fillMaxSize().background(Color(0xFF0A0A0A)),
        verticalArrangement = Arrangement.Center
    ) {
        // 巨型文字
        Text(
            text = "THE WORDS ARE",
            color = Color(0xFFF5F5F0),
            fontSize = 120.sp, // 荒谬的大小
            fontFamily = FontFamily.SansSerif, // 替换为 Anton
            lineHeight = 100.sp,
            softWrap = false, // 强制溢出边缘
            modifier = Modifier.offset(x = (-20).dp)
        )
        
        // 描边文字
        Text(
            text = "THE INTERFACE",
            fontSize = 100.sp,
            fontFamily = FontFamily.SansSerif,
            lineHeight = 90.sp,
            softWrap = false,
            style = TextStyle(
                drawStyle = Stroke(
                    miter = 10f,
                    width = 2f,
                    join = StrokeJoin.Round
                )
            ),
            color = Color(0xFFF5F5F0) // 描边颜色
        )
    }
}
```
- 在 `Text` 上设置 `softWrap = false`，防止其换行并破坏巨型标题的美感。
- Compose 通过 `style = TextStyle(drawStyle = Stroke(...))` 原生支持文字描边。

## 推荐与避免
- **推荐**：混用实色文字和描边文字（使用 `-webkit-text-stroke`）来增加视觉趣味。
- **避免**：将文字包裹在卡片或容器中。让它出血到背景中。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。