---
name: retro-futurism
description: Retro Futurism 的 Web 与 App 实现指南。当用户希望复古未来概念、1950 年代太空时代美学或原子朋克氛围时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Retro Futurism

> "1950、60 年代想象中的未来。火箭、原子，以及流线型的铬合金。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **空气动力学形状**：大量流线型曲线、水滴形状和扫掠线条。没有完美的正方形。
2. **太空时代主题**：星星、原子、轨道和鳍状物（像 1950 年代的凯迪拉克）。
3. **中世纪配色搭配铬合金**：经典 50 年代柔和色搭配光亮、反光的金属。

## 视觉 DNA
- **颜色**：绿松石（`#40E0D0`）、原子橙（`#FF9966`）、薄荷绿（`#98FF98`），搭配银/铬和深空黑。
- **排版**：Googie 建筑字体、粗体花体字或干净的中世纪几何无衬线字体（如 `Futura`）。
- **样式**：流线型边框、戏剧化投影和偏移重叠的形状。

## Web 实现
- **CSS 示例**：
```css
body {
  background-color: #FDF5E6; /* 旧纸 / 奶油色 */
  color: #2F4F4F;
  font-family: 'Futura', 'Trebuchet MS', sans-serif;
  overflow-x: hidden;
}

/* Googie 风格扫掠背景元素 */
.retro-future-swoop {
  position: absolute;
  top: 0; right: -10%;
  width: 120%; height: 300px;
  background-color: #40E0D0; /* 绿松石 */
  border-radius: 0 0 50% 50%;
  transform: rotate(-5deg);
  z-index: -1;
  border-bottom: 8px solid #FF9966; /* 原子橙条纹 */
}

.atompunk-card {
  background-color: #fff;
  border: 4px solid #Silver;
  border-radius: 40px 10px 40px 10px; /* 扫掠的空气动力学角 */
  padding: 32px;
  box-shadow: 15px 15px 0px rgba(0,0,0,0.1);
  position: relative;
}

/* 经典星爆图案 */
.starburst {
  position: absolute;
  top: -20px; left: -20px;
  width: 40px; height: 40px;
  background-color: #FF9966;
  clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}
```

## App 实现

### SwiftUI
```swift
struct AtompunkShape: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        // 扫掠的空气动力学曲线（左上大圆角，右下小圆角）
        path.addRoundedRect(
            in: rect,
            cornerSize: CGSize(width: 40, height: 40),
            style: .continuous
        )
        // 为了完美的真实感，使用 Path 绘制水滴曲线
        return path
    }
}

struct RetroFutureCard: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("ATOMPUNK")
                .font(.custom("Futura", size: 28))
                .fontWeight(.bold)
                .foregroundColor(Color(red: 0.18, green: 0.31, blue: 0.31))
            
            Text("Sleek chrome and sweeping curves.")
                .font(.custom("Futura", size: 16))
        }
        .padding(32)
        .background(Color.white)
        // 不对称的角：左上大、右下小
        .cornerRadius(40, corners: [.topLeft, .bottomRight])
        .cornerRadius(10, corners: [.topRight, .bottomLeft])
        .overlay(
            // 铬合金般的边框
            RoundedRectangle(cornerRadius: 10) // 为演示简化的叠加层
                .stroke(
                    LinearGradient(colors: [.gray, .white, .gray], startPoint: .top, endPoint: .bottom),
                    lineWidth: 4
                )
        )
        .shadow(color: .black.opacity(0.1), radius: 0, x: 15, y: 15)
    }
}
// 注意：不对称角需要在 SwiftUI 中使用自定义 ViewModifier。
```
- 依赖不对称的圆角半径来营造空气动力学、水滴般的美感。
- 金属/铬合金边框通过使用 `.gray` 和 `.white` 灰度值的 `LinearGradient` 伪造。

### Flutter
```dart
class RetroFutureCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: Colors.white,
        // 不对称的"空气动力学"形状
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(40),
          bottomRight: Radius.circular(40),
          topRight: Radius.circular(10),
          bottomLeft: Radius.circular(10),
        ),
        // 铬合金边框模拟
        border: Border.all(
          width: 4,
          color: Colors.transparent, // 需要自定义 painter 实现渐变边框
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            offset: const Offset(15, 15),
            blurRadius: 0, // 硬投影
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: const [
          Text('ATOMPUNK',
            style: TextStyle(fontFamily: 'Futura', fontSize: 28, fontWeight: FontWeight.bold, color: Color(0xFF2F4F4F))),
          SizedBox(height: 16),
          Text('Sleek chrome and sweeping curves.',
            style: TextStyle(fontFamily: 'Futura', fontSize: 16)),
        ],
      ),
    );
  }
}
```
- Flutter 通过 `BorderRadius.only()` 原生支持不对称圆角。
- 渐变边框（铬合金）需要 `CustomPaint` 或将容器包裹在带渐变背景和内边距的另一个容器中。

### React Native
```jsx
const RetroFutureCard = () => {
  return (
    <View style={{
      backgroundColor: '#FFF',
      padding: 32,
      // 不对称空气动力学圆角
      borderTopLeftRadius: 40,
      borderBottomRightRadius: 40,
      borderTopRightRadius: 10,
      borderBottomLeftRadius: 10,
      
      borderWidth: 4,
      borderColor: '#C0C0C0', // 纯银色回退
      
      // 偏移硬投影
      shadowColor: '#000',
      shadowOffset: { width: 15, height: 15 },
      shadowOpacity: 0.1,
      shadowRadius: 0,
      elevation: 5,
    }}>
      <Text style={{ fontFamily: 'Futura', fontSize: 28, fontWeight: 'bold', color: '#2F4F4F' }}>
        ATOMPUNK
      </Text>
      <Text style={{ fontFamily: 'Futura', fontSize: 16, marginTop: 16 }}>
        Sleek chrome and sweeping curves.
      </Text>
    </View>
  );
};
```
- React Native 原生支持独立的 `borderTopLeftRadius` 等样式属性，让空气动力学形状变得简单。
- 复杂几何背景（如星爆）应通过 `react-native-svg` 导入为 SVG 组件。

### Jetpack Compose
```kotlin
@Composable
fun RetroFutureCard() {
    Box(
        modifier = Modifier
            .padding(24.dp)
            // 伪造硬投影
            .drawBehind {
                drawRoundRect(
                    color = Color.Black.copy(alpha = 0.1f),
                    topLeft = Offset(15.dp.toPx(), 15.dp.toPx()),
                    size = size,
                    cornerRadius = CornerRadius(40.dp.toPx(), 10.dp.toPx()) // 简化
                )
            }
            .background(
                color = Color.White,
                // 空气动力学不对称圆角
                shape = RoundedCornerShape(
                    topStart = 40.dp,
                    topEnd = 10.dp,
                    bottomEnd = 40.dp,
                    bottomStart = 10.dp
                )
            )
            .border(
                width = 4.dp,
                brush = Brush.verticalGradient(listOf(Color.LightGray, Color.White, Color.LightGray)),
                shape = RoundedCornerShape(
                    topStart = 40.dp,
                    topEnd = 10.dp,
                    bottomEnd = 40.dp,
                    bottomStart = 10.dp
                )
            )
            .padding(32.dp)
    ) {
        Column {
            Text("ATOMPUNK",
                fontFamily = FontFamily.SansSerif, // 替换为 Futura
                fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Color(0xFF2F4F4F))
            Spacer(Modifier.height(16.dp))
            Text("Sleek chrome and sweeping curves.", fontSize = 16.sp)
        }
    }
}
```
- 使用 `RoundedCornerShape(topStart, topEnd, bottomEnd, bottomStart)` 创建原子朋克美学。
- `Modifier.border` 原生接受 `Brush`，让金属铬合金渐变比其它框架更容易实现。

## 推荐与避免
- **推荐**：严格使用 `Futura` 或 `Century Gothic` 以获得真实的中世纪感。
- **避免**：让 UI 显得脏污或做旧（那是普通复古或蒸汽朋克风格）。Retro-futurism 是干净、乐观且闪亮的。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。