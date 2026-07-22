---
name: cyberpunk-ui
description: Cyberpunk UI 的 Web 与 App 实现指南。当用户需要霓虹色、暗黑背景、高科技反乌托邦美学和黑客界面时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Cyberpunk UI

> "高科技，低生活。霓虹灯招牌划破反乌托邦巨型城市的烟雾。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **黑底霓虹**：基础是绝对黑色（`#000000`）或深炭灰，被刺眼的霓虹强调色切穿。
2. **斜角几何**：斜切角（倒角）而非圆角。UI 元素通常看起来像从金属板上切割下来。
3. **故障与数据**：十六进制数据流、条形码强调色和故意的视觉撕裂。

## 视觉 DNA
- **颜色**：酸性黄（`#FCE205`）、青色（`#00FFFF`）、热粉色（`#FF003C`），对比黑色。
- **排版**：工业化、方正的无衬线字体（如 `Rajdhani`、`Blender Pro` 或 `Teko`），搭配用于数据的小号等宽字体。
- **样式**：对角条纹、警戒胶带图案和厚重的外发光。

## Web 实现
- 依赖 `clip-path` 实现斜角切割。
- **CSS 示例**：
```css
body {
  background-color: #050505;
  color: #00FFFF;
  font-family: 'Rajdhani', sans-serif;
  background-image: repeating-linear-gradient(
    45deg,
    #050505,
    #050505 10px,
    #0a0a0a 10px,
    #0a0a0a 20px
  );
}

.cyberpunk-button {
  background-color: #FF003C; /* 赛博朋克红/粉 */
  color: #FFF;
  font-size: 1.5rem;
  font-weight: bold;
  text-transform: uppercase;
  border: none;
  padding: 16px 32px;
  
  /* 标志性的斜切角 */
  clip-path: polygon(
    0 0, 
    calc(100% - 15px) 0, 
    100% 15px, 
    100% 100%, 
    15px 100%, 
    0 calc(100% - 15px)
  );
  
  position: relative;
  transition: all 0.2s ease;
}

/* 故障/阴影效果 */
.cyberpunk-button:hover {
  background-color: #FCE205; /* 酸性黄 */
  color: #000;
  box-shadow: 
    -4px 0 0 #00FFFF,
    4px 0 0 #FF003C;
}

.data-stream {
  font-family: monospace;
  font-size: 0.8rem;
  color: rgba(0, 255, 255, 0.5);
}
```

## App 实现

### SwiftUI
```swift
struct CyberpunkShape: Shape {
    let cutSize: CGFloat = 15
    func path(in rect: CGRect) -> Path {
        var path = Path()
        // 左上
        path.move(to: CGPoint(x: 0, y: 0))
        // 右上（切割）
        path.addLine(to: CGPoint(x: rect.maxX - cutSize, y: 0))
        path.addLine(to: CGPoint(x: rect.maxX, y: cutSize))
        // 右下
        path.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
        // 左下（切割）
        path.addLine(to: CGPoint(x: cutSize, y: rect.maxY))
        path.addLine(to: CGPoint(x: 0, y: rect.maxY - cutSize))
        path.closeSubpath()
        return path
    }
}

struct CyberButton: View {
    var body: some View {
        Button(action: {}) {
            Text("SYS.OVERRIDE")
                .font(.custom("Rajdhani", size: 24))
                .fontWeight(.bold)
                .foregroundColor(.white)
                .padding(.horizontal, 32)
                .padding(.vertical, 16)
        }
        .background(Color(red: 1.0, green: 0.0, blue: 0.24)) // 赛博朋克红
        .clipShape(CyberpunkShape())
        .overlay(
            CyberpunkShape()
                .stroke(Color(red: 0.0, green: 1.0, blue: 1.0), lineWidth: 2) // 青色边框
        )
    }
}
```
- 定义自定义 `Shape` 物理切割角部，绕过标准 `cornerRadius`。
- 使用 `.clipShape()` 处理背景，`.overlay()` 配合 `.stroke()` 处理高科技边框。

### Flutter
```dart
class CyberpunkClipper extends CustomClipper<Path> {
  final double cutSize = 15.0;

  @override
  Path getClip(Size size) {
    Path path = Path();
    path.lineTo(size.width - cutSize, 0); // 右上切割起点
    path.lineTo(size.width, cutSize);     // 右上切割终点
    path.lineTo(size.width, size.height);
    path.lineTo(cutSize, size.height);    // 左下切割起点
    path.lineTo(0, size.height - cutSize);// 左下切割终点
    path.close();
    return path;
  }

  @override
  bool shouldReclip(CustomClipper<Path> oldClipper) => false;
}

class CyberButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ClipPath(
      clipper: CyberpunkClipper(),
      child: Container(
        color: const Color(0xFFFF003C), // 赛博朋克红
        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
        child: const Text(
          'SYS.OVERRIDE',
          style: TextStyle(
            color: Colors.white,
            fontSize: 24,
            fontWeight: FontWeight.bold,
            fontFamily: 'Rajdhani',
          ),
        ),
      ),
    );
  }
}
```
- 继承 `CustomClipper<Path>` 计算精确的斜角切割。
- 用 `ClipPath` 包裹你的容器。
- 对于边框，必须使用 `CustomPaint` 与 `CustomPainter` 描绘完全相同的路径。

### React Native
```jsx
import Svg, { Polygon } from 'react-native-svg';

const CyberButton = () => {
  return (
    <View style={{ alignItems: 'center', justifyContent: 'center', width: 200, height: 60 }}>
      {/* 背景 SVG 实现斜切角效果 */}
      <View style={{ position: 'absolute', top: 0, bottom: 0, left: 0, right: 0 }}>
        <Svg height="100%" width="100%" viewBox="0 0 200 60" preserveAspectRatio="none">
          <Polygon 
            points="0,0 185,0 200,15 200,60 15,60 0,45"
            fill="#FF003C" 
            stroke="#00FFFF"
            strokeWidth="2"
          />
        </Svg>
      </View>
      
      <Text style={{ 
        color: '#FFF', 
        fontSize: 20, 
        fontWeight: 'bold',
        fontFamily: 'Rajdhani-Bold' 
      }}>
        SYS.OVERRIDE
      </Text>
    </View>
  );
};
```
- React Native 本身不能轻松在 View 上支持裁剪路径。
- **解决方案**：使用 `react-native-svg` 绘制一个 `<Polygon>`，作为绝对定位的背景放在透明文字后面。

### Jetpack Compose
```kotlin
class CyberpunkShape(private val cutSize: Dp) : Shape {
    override fun createOutline(
        size: Size,
        layoutDirection: LayoutDirection,
        density: Density
    ): Outline {
        val cutPx = with(density) { cutSize.toPx() }
        val path = Path().apply {
            moveTo(0f, 0f)
            lineTo(size.width - cutPx, 0f)
            lineTo(size.width, cutPx)
            lineTo(size.width, size.height)
            lineTo(cutPx, size.height)
            lineTo(0f, size.height - cutPx)
            close()
        }
        return Outline.Generic(path)
    }
}

@Composable
fun CyberButton() {
    Box(
        modifier = Modifier
            .clip(CyberpunkShape(15.dp))
            .background(Color(0xFFFF003C))
            .border(2.dp, Color(0xFF00FFFF), CyberpunkShape(15.dp))
            .clickable { }
            .padding(horizontal = 32.dp, vertical = 16.dp)
    ) {
        Text(
            text = "SYS.OVERRIDE",
            color = Color.White,
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            // 假设已加载自定义字体
        )
    }
}
```
- 通过重写 `createOutline` 并描绘 `Path` 创建自定义 `Shape`。
- 直接将此形状传入 `Modifier.clip()` 和 `Modifier.background()`。
- 你可以使用 `Modifier.border()` 直接给自定义形状描边。

## 推荐与避免
- **推荐**：包含微小的、看似无意义的技术细节（十字准线、序列号、"SYS.OVERRIDE" 文字）。
- **避免**：使用柔和、有机的曲线或渐变。必须保持锐利和激进。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。