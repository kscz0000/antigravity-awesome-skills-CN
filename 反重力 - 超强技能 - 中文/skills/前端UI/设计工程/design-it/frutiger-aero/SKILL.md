---
name: frutiger-aero
description: Frutiger Aero 的 Web 与 App 实现指南。当用户希望光泽渐变、2000 年代初的自然主题科技、玻璃与水主题时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Frutiger Aero

> "2000 年代中期的乐观美学。光泽塑料、清澈的水、蓝天和环保科技。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **超光泽质感**：按钮看起来像抛光的玻璃或湿润的塑料。大量使用凸形渐变和高光。
2. **拟物自然**：绿草、蓝天、水滴、气泡等自然主题，与光滑玻璃科技相融合（想想 Windows Aero 或早期 iOS）。
3. **半透明**：磨砂玻璃效果，但比现代玻璃态更饱和、更具反射感。

## 视觉 DNA
- **颜色**：青色、天蓝、酸橙绿和纯白。完全避免深色主题。
- **排版**：干净、高度可读的人文无衬线字体（如 Frutiger、`Segoe UI` 或 `Myriad Pro`）。
- **样式**：投影很深。高光是按钮顶部明亮、锐利的白色线条。

## Web 实现
- 使用多重 box-shadow（inset 实现光泽，outset 实现深度）和 linear-gradient。
- **CSS 示例**：
```css
body {
  /* 经典蓝天 / 绿草渐变 */
  background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 60%, #98FB98 100%);
  font-family: 'Segoe UI', Tahoma, sans-serif;
}

.aero-btn {
  background: linear-gradient(to bottom, #73c8f8 0%, #1583d7 50%, #0361a3 50%, #299eef 100%);
  color: white;
  border: 1px solid #024b7f;
  border-radius: 20px;
  padding: 12px 32px;
  font-weight: 600;
  text-shadow: 0 -1px 1px rgba(0,0,0,0.5);
  
  /* 光泽高光与深度 */
  box-shadow: 
    inset 0 1px 1px rgba(255,255,255,0.8), /* 顶部边缘高光 */
    inset 0 15px 15px rgba(255,255,255,0.3), /* 凸形塑料光泽 */
    0 4px 6px rgba(0,0,0,0.2); /* 投影 */
}

.aero-panel {
  /* Windows Vista/7 Aero 玻璃 */
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-top-color: #ffffff; /* 顶部边缘更亮 */
  border-radius: 8px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
```

## App 实现

### SwiftUI
```swift
struct FrutigerAeroView: View {
    var body: some View {
        ZStack {
            // 经典蓝天到绿草渐变
            LinearGradient(
                colors: [Color(hex: "87CEEB"), Color(hex: "E0F6FF"), Color(hex: "98FB98")],
                startPoint: .top, endPoint: .bottom
            ).ignoresSafeArea()
            
            // 光泽按钮
            Button(action: {}) {
                Text("Windows Vista")
                    .font(.headline)
                    .foregroundColor(.white)
                    .shadow(color: .black.opacity(0.5), radius: 1, y: -1) // 内嵌文字阴影效果
                    .padding(.horizontal, 40)
                    .padding(.vertical, 16)
                    .background(
                        // 基础渐变
                        LinearGradient(
                            stops: [
                                .init(color: Color(hex: "73c8f8"), location: 0.0),
                                .init(color: Color(hex: "1583d7"), location: 0.5),
                                .init(color: Color(hex: "0361a3"), location: 0.5), // 锐利的色彩断点
                                .init(color: Color(hex: "299eef"), location: 1.0)
                            ],
                            startPoint: .top, endPoint: .bottom
                        )
                    )
                    .cornerRadius(25)
                    .overlay(
                        // 顶部白色镜面高光
                        RoundedRectangle(cornerRadius: 25)
                            .stroke(
                                LinearGradient(colors: [.white, .clear], startPoint: .top, endPoint: .bottom),
                                lineWidth: 1.5
                            )
                    )
                    .shadow(color: .black.opacity(0.3), radius: 5, y: 4)
            }
        }
    }
}
// 注意：Color(hex:) 需要在 SwiftUI 中自定义扩展
```
- 标志性的 Frutiger Aero"果冻"外观需要正中间有一个锐利的色彩过渡。将两个 `Gradient stops` 设置为 `0.5` 但颜色不同。
- 使用 `.overlay` 配合自上而下的白色到透明渐变描边，创建玻璃高光边缘。

### Flutter
```dart
class FrutigerAeroScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        // 天空/草地背景
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter, end: Alignment.bottomCenter,
            colors: [Color(0xFF87CEEB), Color(0xFFE0F6FF), Color(0xFF98FB98)],
          ),
        ),
        child: Center(
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(25),
              boxShadow: const [BoxShadow(color: Colors.black38, blurRadius: 6, offset: Offset(0, 4))],
              // 光泽果冻按钮
              gradient: const LinearGradient(
                begin: Alignment.topCenter, end: Alignment.bottomCenter,
                stops: [0.0, 0.5, 0.5, 1.0], // 50% 处锐利过渡
                colors: [
                  Color(0xFF73C8F8), // 浅色顶部
                  Color(0xFF1583D7), // 中上部
                  Color(0xFF0361A3), // 深色中部（形成玻璃地平线）
                  Color(0xFF299EEF), // 鲜亮底部反射
                ],
              ),
              border: Border.all(color: Colors.white.withOpacity(0.5), width: 1),
            ),
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                borderRadius: BorderRadius.circular(25),
                onTap: () {},
                child: const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 40, vertical: 16),
                  child: Text(
                    'Media Player',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      shadows: [Shadow(color: Colors.black54, offset: Offset(0, -1))],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
```
- Flutter 的 `LinearGradient` `stops` 数组对此非常合适。在 `0.5` 提供两次会创建一条硬线，模仿弯曲玻璃的反射。
- 使用 `Text` 阴影配合负 `offset: Offset(0, -1)` 重现 2000 年代的经典蚀刻文字外观。

### React Native
```jsx
import LinearGradient from 'react-native-linear-gradient';

const FrutigerAeroScreen = () => {
  return (
    <LinearGradient
      colors={['#87CEEB', '#E0F6FF', '#98FB98']}
      style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}
    >
      <View style={{
        shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, 
        shadowOpacity: 0.3, shadowRadius: 5, elevation: 8
      }}>
        <LinearGradient
          colors={['#73C8F8', '#1583D7', '#0361A3', '#299EEF']}
          locations={[0, 0.5, 0.5, 1]} // 锐利的玻璃地平线
          style={{
            borderRadius: 25,
            paddingVertical: 16,
            paddingHorizontal: 40,
            borderWidth: 1,
            borderColor: 'rgba(255,255,255,0.6)',
            borderTopWidth: 2 // 顶部更强的镜面高光
          }}
        >
          <Text style={{ 
            color: '#FFF', 
            fontWeight: 'bold', 
            textShadowColor: 'rgba(0,0,0,0.5)', 
            textShadowOffset: { width: 0, height: -1 }, 
            textShadowRadius: 1 
          }}>
            Glossy Button
          </Text>
        </LinearGradient>
      </View>
    </LinearGradient>
  );
};
```
- `react-native-linear-gradient` 支持 `locations`。将它们设置为 `[0, 0.5, 0.5, 1]` 来创建双色凸形反射。
- 将 `borderTopWidth: 2` 配合白色边框颜色能有效模拟明亮塑料物体顶部边缘的高光。

### Jetpack Compose
```kotlin
@Composable
fun FrutigerAeroScreen() {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(listOf(Color(0xFF87CEEB), Color(0xFFE0F6FF), Color(0xFF98FB98)))
            ),
        contentAlignment = Alignment.Center
    ) {
        // 光泽按钮
        val glassBrush = Brush.verticalGradient(
            0.0f to Color(0xFF73C8F8),
            0.49f to Color(0xFF1583D7),
            0.5f to Color(0xFF0361A3), // 锐利的反射线
            1.0f to Color(0xFF299EEF)
        )

        Box(
            modifier = Modifier
                .shadow(8.dp, RoundedCornerShape(25.dp))
                .background(glassBrush, RoundedCornerShape(25.dp))
                .border(
                    width = 1.dp,
                    brush = Brush.verticalGradient(listOf(Color.White, Color.Transparent)), // 顶部高光
                    shape = RoundedCornerShape(25.dp)
                )
                .clickable { }
                .padding(horizontal = 40.dp, vertical = 16.dp)
        ) {
            Text(
                text = "Eco Tech",
                color = Color.White,
                fontWeight = FontWeight.Bold,
                style = TextStyle(
                    shadow = Shadow(color = Color.Black.copy(alpha = 0.5f), offset = Offset(0f, -2f), blurRadius = 2f)
                )
            )
        }
    }
}
```
- Compose 的 `Brush.verticalGradient` 接受 `vararg colorStops: Pair<Float, Color>`。使用 `0.49f` 和 `0.5f` 来创建硬反射线。
- 从白色渐变到透明的渐变边框 `Modifier.border(brush = ...)` 完美再现自上而下的镜面高光。

## 推荐与避免
- **推荐**：在适当场合加入镜头眩光、极光或水泡的图像。
- **避免**：做成扁平风格。Frutiger Aero 是 Flat Design 的终极对立面。一切都必须闪耀。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。