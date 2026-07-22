---
name: retro-design
description: Retro Design（60-80 年代）的 Web 与 App 实现指南。当用户希望复古美学、温暖柔和的颜色和怀旧布局时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Retro Design

> "温暖、模拟的感觉。通过柔和的色调、颗粒感和经典排版表达怀旧。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **温暖、模拟的调色板**：颜色看起来被阳光晒褪或印在旧纸上。
2. **纹理和噪点**：轻度的颗粒叠加层模拟胶片或旧印刷介质。
3. **经典排版搭配**：粗壮、有律动的展示字体搭配打字机或经典衬线正文。

## 视觉 DNA
- **颜色**：**Monochromatic Brown** 或温暖、柔和的调色板（芥末黄、焦橙、鼠尾草绿、米白）。
- **排版**：展示字体如 `Cooper Black`、`Garamond` 或 `Courier`。
- **样式**：徽章、印章、波浪边框和半色调图案。

## Web 实现
- 使用 CSS 滤镜和背景噪点图像创建纹理。
- **CSS 示例**：
```css
body {
  background-color: #F4E8D1; /* 旧纸 */
  color: #3E2723; /* 深褐墨水 */
  font-family: 'Georgia', serif;
  
  /* 使用伪元素或背景图像应用微妙的噪点叠加 */
  background-image: url('noise-texture.png');
  background-blend-mode: multiply;
}

.retro-header {
  font-family: 'Cooper Black', serif;
  font-size: 4rem;
  color: #D35400; /* 焦橙 */
  text-shadow: 2px 2px 0px #F1C40F; /* 芥末黄投影 */
  letter-spacing: -1px;
}

.retro-card {
  background-color: #FFF3E0;
  border: 2px solid #3E2723;
  border-radius: 12px;
  padding: 24px;
  
  /* 复古偏移投影 */
  box-shadow: 8px 8px 0px #795548;
}

.retro-badge {
  display: inline-block;
  background-color: #E74C3C;
  color: #F4E8D1;
  font-family: monospace;
  font-weight: bold;
  padding: 8px 16px;
  border-radius: 50%; /* 看起来像贴纸 */
  transform: rotate(-10deg);
}
```

## App 实现

### SwiftUI
```swift
struct RetroCard: View {
    let paperColor = Color(red: 0.96, green: 0.91, blue: 0.82) // #F4E8D1
    let inkColor = Color(red: 0.24, green: 0.15, blue: 0.14) // #3E2723
    
    var body: some View {
        ZStack {
            paperColor.ignoresSafeArea()
            
            // 可选：噪点纹理
            Image("film_grain")
                .resizable()
                .blendMode(.multiply)
                .opacity(0.3)
                .ignoresSafeArea()
            
            VStack(alignment: .leading, spacing: 24) {
                Text("RETRO DESIGN")
                    .font(.custom("Cooper Black", size: 36))
                    .foregroundColor(Color(red: 0.83, green: 0.33, blue: 0.0)) // #D35400
                    .shadow(color: Color(red: 0.95, green: 0.77, blue: 0.06), radius: 0, x: 2, y: 2)
                
                Text("Analog warmth and classic typography.")
                    .font(.custom("Georgia", size: 18))
                    .foregroundColor(inkColor)
            }
            .padding(32)
            .background(Color(red: 1.0, green: 0.95, blue: 0.88))
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(inkColor, lineWidth: 2)
            )
            // 复古实心偏移投影
            .shadow(color: Color(red: 0.47, green: 0.33, blue: 0.28), radius: 0, x: 8, y: 8)
        }
    }
}
```
- 颗粒纹理图像可以使用 `.blendMode(.multiply)` 叠加。注意全屏纹理的内存使用。
- 使用 `.shadow(radius: 0)` 创建 70 年代印刷媒体的硬偏移投影。
- Cooper Black 等自定义字体是绝对必需的。

### Flutter
```dart
class RetroCard extends StatelessWidget {
  final Color paperColor = const Color(0xFFF4E8D1);
  final Color inkColor = const Color(0xFF3E2723);

  @override
  Widget build(BuildContext context) {
    return Container(
      color: paperColor,
      child: Stack(
        fit: StackFit.expand,
        children: [
          // 噪点纹理
          Opacity(
            opacity: 0.3,
            child: Image.asset('assets/film_grain.png', 
              fit: BoxFit.cover, 
              colorBlendMode: BlendMode.multiply),
          ),
          Center(
            child: Container(
              padding: const EdgeInsets.all(32),
              decoration: BoxDecoration(
                color: const Color(0xFFFFF3E0),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: inkColor, width: 2),
                boxShadow: const [
                  BoxShadow(
                    color: Color(0xFF795548),
                    blurRadius: 0, // 硬偏移投影
                    offset: Offset(8, 8),
                  ),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('RETRO DESIGN',
                    style: TextStyle(
                      fontFamily: 'Cooper',
                      fontSize: 36,
                      color: Color(0xFFD35400),
                      shadows: [Shadow(color: Color(0xFFF1C40F), offset: Offset(2, 2))],
                    )),
                  const SizedBox(height: 24),
                  Text('Analog warmth and classic typography.',
                    style: TextStyle(fontFamily: 'Georgia', fontSize: 18, color: inkColor)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```
- 在 `Stack` 中包裹背景，将半透明胶片颗粒资源叠加在纯色之上。
- 文字和容器的投影必须使用 `blurRadius: 0` 来模拟偏移错位的油墨印刷。

### React Native
```jsx
const RetroCard = () => {
  return (
    <ImageBackground 
      source={require('./film_grain.png')}
      style={{ flex: 1, backgroundColor: '#F4E8D1', padding: 24, justifyContent: 'center' }}
      imageStyle={{ opacity: 0.3, tintColor: '#3E2723' }}
    >
      <View style={{
        backgroundColor: '#FFF3E0',
        padding: 32,
        borderRadius: 12,
        borderWidth: 2,
        borderColor: '#3E2723',
        // 硬投影
        shadowColor: '#795548',
        shadowOffset: { width: 8, height: 8 },
        shadowOpacity: 1,
        shadowRadius: 0,
        elevation: 8, // Android 后备，会带模糊
      }}>
        <Text style={{
          fontFamily: 'CooperBlack',
          fontSize: 36,
          color: '#D35400',
          textShadowColor: '#F1C40F',
          textShadowOffset: { width: 2, height: 2 },
          textShadowRadius: 0,
          marginBottom: 24
        }}>
          RETRO DESIGN
        </Text>
        <Text style={{ fontFamily: 'Georgia', fontSize: 18, color: '#3E2723' }}>
          Analog warmth and classic typography.
        </Text>
      </View>
    </ImageBackground>
  );
};
```
- 在根 View 上使用 `ImageBackground` 作为颗粒。
- Android 的 `elevation` 无法原生实现无模糊偏移阴影。使用 `react-native-drop-shadow` 在 Android 上获得完美的复古投影。

### Jetpack Compose
```kotlin
@Composable
fun RetroCard() {
    val inkColor = Color(0xFF3E2723)
    
    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF4E8D1))) {
        // 噪点纹理叠加
        Image(
            painter = painterResource(id = R.drawable.film_grain),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.matchParentSize().alpha(0.3f),
            colorFilter = ColorFilter.tint(Color.Black, BlendMode.Multiply)
        )
        
        Box(
            modifier = Modifier
                .align(Alignment.Center)
                .padding(24.dp)
                // 在 Compose 中通过 drawBehind 伪造硬投影
                .drawBehind {
                    drawRoundRect(
                        color = Color(0xFF795548),
                        topLeft = Offset(8.dp.toPx(), 8.dp.toPx()),
                        size = size,
                        cornerRadius = CornerRadius(12.dp.toPx())
                    )
                }
                .background(Color(0xFFFFF3E0), RoundedCornerShape(12.dp))
                .border(2.dp, inkColor, RoundedCornerShape(12.dp))
                .padding(32.dp)
        ) {
            Column {
                Text("RETRO DESIGN",
                    fontFamily = FontFamily(Font(R.font.cooper_black)),
                    fontSize = 36.sp,
                    color = Color(0xFFD35400),
                    style = TextStyle(shadow = Shadow(Color(0xFFF1C40F), Offset(4f, 4f), 0f))
                )
                Spacer(Modifier.height(24.dp))
                Text("Analog warmth and classic typography.",
                    fontFamily = FontFamily.Serif,
                    fontSize = 18.sp,
                    color = inkColor)
            }
        }
    }
}
```
- 原生 `Modifier.shadow` 创建柔和模糊。使用 `Modifier.drawBehind` 绘制偏移的 `drawRoundRect` 来获得硬复古投影。
- 文字阴影完美支持硬偏移，通过 `Shadow(color, offset, blurRadius = 0f)`。

## 推荐与避免
- **推荐**：使用略偏白的背景（奶油色、米色）而非纯 `#FFFFFF`，以模拟旧纸张。
- **避免**：使用时尚的现代几何无衬线字体或科技感霓虹色。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。