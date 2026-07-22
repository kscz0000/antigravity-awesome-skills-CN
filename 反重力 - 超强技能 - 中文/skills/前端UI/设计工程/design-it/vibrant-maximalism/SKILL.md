---
name: vibrant-maximalism
description: Vibrant Maximalism 的 Web 与 App 实现指南。当用户希望丰富色彩、密集布局、极端感官输入和"越多越好"时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Vibrant Maximalism

> "越多越好。色彩、图案和排版的爆炸。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **感官过载**：每个像素都在做某事。图案叠加在渐变上，渐变叠加在照片上。
2. **冲突的颜色**：忘掉标准的色彩和谐规则。把霓虹绿配热粉，或亮橙配电蓝。
3. **多种字体**：在同一布局中混合 3 或 4 种完全不同的字体。

## 视觉 DNA
- **颜色**：所有颜色。高度饱和、未调淡的色调。不允许冷静的中性色。
- **排版**：混乱的搭配。巨型衬线标题、泡泡字母副标题、等宽正文字。
- **视觉**：贴纸、重复图案、emoji、3D 渲染、跑马灯滚动文字。

## Web 实现
- **CSS 示例**：
```css
body {
  /* 复杂的冲突背景 */
  background: 
    radial-gradient(circle at 20% 30%, #FF00FF 0%, transparent 40%),
    radial-gradient(circle at 80% 70%, #00FFFF 0%, transparent 40%),
    url('checkerboard-pattern.png') repeat;
  background-color: #FFFF00;
  color: #000;
  overflow-x: hidden;
}

.max-headline {
  font-family: 'Anton', sans-serif;
  font-size: 8rem;
  text-transform: uppercase;
  line-height: 0.8;
  color: #FF0000;
  /* 疯狂阴影效果 */
  text-shadow: 
    4px 4px 0px #000,
    8px 8px 0px #00FFFF,
    12px 12px 0px #FF00FF;
  transform: rotate(-3deg);
}

.max-sticker {
  position: absolute;
  background: #000;
  color: #00FF00;
  font-family: monospace;
  padding: 10px;
  border-radius: 50%;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  border: 4px dashed #FF00FF;
  animation: spin 10s linear infinite;
}

@keyframes spin { 100% { transform: rotate(360deg); } }

.max-card {
  background: rgba(255, 255, 255, 0.9);
  border: 5px solid #000;
  box-shadow: 10px 10px 0px #0000FF;
  padding: 40px;
  border-radius: 0 40px 0 40px; /* 奇怪的不对称圆角 */
}
```

## App 实现

### SwiftUI
```swift
struct VibrantMaximalismView: View {
    var body: some View {
        ScrollView {
            ZStack {
                // 混乱的分层背景
                Color(hex: "FFFF00").ignoresSafeArea() // 纯黄
                
                Circle()
                    .fill(RadialGradient(colors: [Color(hex: "FF00FF"), .clear], center: .center, startRadius: 0, endRadius: 200))
                    .frame(width: 400, height: 400)
                    .offset(x: -100, y: -200)
                
                Circle()
                    .fill(RadialGradient(colors: [Color(hex: "00FFFF"), .clear], center: .center, startRadius: 0, endRadius: 200))
                    .frame(width: 400, height: 400)
                    .offset(x: 150, y: 200)
                
                // 内容
                VStack(spacing: 40) {
                    Text("OVERLOAD")
                        .font(.custom("Anton", size: 80))
                        .foregroundColor(Color(hex: "FF0000"))
                        .shadow(color: .black, radius: 0, x: 4, y: 4)
                        .shadow(color: Color(hex: "00FFFF"), radius: 0, x: 8, y: 8)
                        .rotationEffect(.degrees(-3))
                    
                    // 奇怪形状的卡片
                    VStack {
                        Text("More is more.")
                            .font(.system(size: 24, weight: .black, design: .monospaced))
                    }
                    .padding(40)
                    .background(Color.white.opacity(0.9))
                    .border(.black, width: 5)
                    .cornerRadius(40, corners: [.topRight, .bottomLeft]) // 自定义圆角扩展需要
                    .shadow(color: Color(hex: "0000FF"), radius: 0, x: 10, y: 10)
                }
            }
        }
    }
}
```
- 在 `ZStack` 中将多个 `RadialGradient` 分层在内容后面，创造复杂的、冲突的色彩色块。
- 使用多个硬投影（`radius: 0`，但 X/Y 偏移大）和冲突色来构建响亮的文字效果。

### Flutter
```dart
class VibrantMaximalismScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // 背景颜色
          Container(color: const Color(0xFFFFFF00)),
          // 渐变色块 1
          Positioned(
            top: -100, left: -100,
            child: Container(
              width: 400, height: 400,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                gradient: RadialGradient(colors: [Color(0xFFFF00FF), Colors.transparent]),
              ),
            ),
          ),
          
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Transform.rotate(
                  angle: -0.05, // 轻微倾斜
                  child: const Text(
                    'OVERLOAD',
                    style: TextStyle(
                      fontFamily: 'Anton', fontSize: 80, color: Color(0xFFFF0000),
                      shadows: [
                        Shadow(color: Colors.black, offset: Offset(4, 4)),
                        Shadow(color: Color(0xFF00FFFF), offset: Offset(8, 8)),
                      ]
                    ),
                  ),
                ),
                const SizedBox(height: 40),
                
                // 奇怪的不对称卡片
                Container(
                  padding: const EdgeInsets.all(40),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.9),
                    border: Border.all(color: Colors.black, width: 5),
                    borderRadius: const BorderRadius.only(topRight: Radius.circular(40), bottomLeft: Radius.circular(40)),
                    boxShadow: const [BoxShadow(color: Color(0xFF0000FF), offset: Offset(10, 10))],
                  ),
                  child: const Text('More is more.', style: TextStyle(fontFamily: 'Courier', fontSize: 24, fontWeight: FontWeight.bold)),
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```
- Flutter 的 `Stack` 与 `Positioned` 控件让你能在屏幕任何位置随意投放冲突的径向渐变。
- 应用 `BorderRadius.only` 创建怪异的、不对称的容器，打破典型的 UI 规范。

### React Native
```jsx
const VibrantMaximalismScreen = () => {
  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#FFFF00' }}>
      
      {/* 在 React Native 中模拟径向色块通常需要 SVG 或 ImageBackground。这里我们使用绝对定位的 View */}
      <View style={{ position: 'absolute', top: -50, left: -50, width: 300, height: 300, borderRadius: 150, backgroundColor: '#FF00FF', opacity: 0.5, filter: 'blur(50px)' }} />

      <View style={{ padding: 40, alignItems: 'center', marginTop: 100 }}>
        
        {/* 响亮文字 */}
        <Text style={{
          fontFamily: 'Anton-Regular', fontSize: 64, color: '#FF0000',
          transform: [{ rotate: '-3deg' }],
          textShadowColor: '#00FFFF', textShadowOffset: { width: 8, height: 8 }, textShadowRadius: 0
        }}>
          OVERLOAD
        </Text>

        {/* 不对称卡片 */}
        <View style={{
          marginTop: 60, padding: 40, backgroundColor: 'rgba(255,255,255,0.9)',
          borderWidth: 5, borderColor: '#000',
          borderTopRightRadius: 40, borderBottomLeftRadius: 40,
          shadowColor: '#0000FF', shadowOffset: { width: 10, height: 10 }, shadowOpacity: 1, shadowRadius: 0, elevation: 10
        }}>
          <Text style={{ fontFamily: 'monospace', fontSize: 24, fontWeight: '900' }}>More is more.</Text>
        </View>

      </View>
    </ScrollView>
  );
};
```
- 使用 `textShadowRadius: 0` 创建硬、偏移、粗野风格的文字阴影，使用冲突色（例如红色文字配青色硬阴影）。
- 应用 `transform: [{ rotate: '-3deg' }]` 故意打破对齐。

### Jetpack Compose
```kotlin
@Composable
fun VibrantMaximalismScreen() {
    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFFFFF00))) {
        
        // 模拟径向渐变
        Box(modifier = Modifier.offset(x = (-100).dp, y = (-100).dp).size(400.dp).background(Brush.radialGradient(listOf(Color(0xFFFF00FF), Color.Transparent))))
        Box(modifier = Modifier.offset(x = 100.dp, y = 300.dp).size(400.dp).background(Brush.radialGradient(listOf(Color(0xFF00FFFF), Color.Transparent))))
        
        Column(
            modifier = Modifier.fillMaxSize().padding(40.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            // 旋转标题
            Text(
                text = "OVERLOAD",
                fontSize = 80.sp,
                fontFamily = FontFamily.SansSerif, // 替换为 Anton
                color = Color(0xFFFF0000),
                modifier = Modifier.rotate(-3f),
                style = TextStyle(
                    shadow = Shadow(color = Color(0xFF00FFFF), offset = Offset(16f, 16f), blurRadius = 0f)
                )
            )
            
            Spacer(Modifier.height(60.dp))
            
            // 不对称卡片
            Box(
                modifier = Modifier
                    .shadow(elevation = 0.dp) // 重置默认阴影
                    // 自定义硬阴影技巧：先绘制阴影形状
                    .offset(10.dp, 10.dp)
                    .background(Color(0xFF0000FF), RoundedCornerShape(topEnd = 40.dp, bottomStart = 40.dp))
                    .offset((-10).dp, (-10).dp)
                    .background(Color.White.copy(alpha = 0.9f), RoundedCornerShape(topEnd = 40.dp, bottomStart = 40.dp))
                    .border(5.dp, Color.Black, RoundedCornerShape(topEnd = 40.dp, bottomStart = 40.dp))
                    .padding(40.dp)
            ) {
                Text("More is more.", fontFamily = FontFamily.Monospace, fontSize = 24.sp, fontWeight = FontWeight.Black)
            }
        }
    }
}
```
- `Brush.radialGradient` 非常适合在背景中投入色彩色块。
- Compose 的默认 `shadow` modifier 会模糊边缘。要在 Compose 中获得硬、粗野风格的阴影，在主形状后面以偏移渲染一个相同形状的纯色。

## 推荐与避免
- **推荐**：打破网格。让元素尴尬地重叠。
- **避免**：使用留白。如果有空区域，就用图案、跑马灯或巨型 emoji 填满它。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。