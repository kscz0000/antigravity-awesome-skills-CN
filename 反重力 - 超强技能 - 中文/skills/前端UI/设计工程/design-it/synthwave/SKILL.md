---
name: synthwave
description: Synthwave（Outrun）的 Web 与 App 实现指南。当用户希望 80 年代霓虹、暗黑背景、Outrun 网格和迈阿密风云美学时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Synthwave（Outrun）

> "午夜驾驶法拉第穿过霓虹灯点缀的数字网格。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **默认暗色模式**：绝对纯黑或深紫色背景。
2. **霓虹发光矢量**：亮品红、青色和黄色的线框、文字和网格。大量使用 `box-shadow` 和 `text-shadow` 实现发光效果。
3. **透视网格**：标志性的视觉是发光的网格，向地平线上的消失点渐隐。

## 视觉 DNA
- **颜色**：深空背景（`#0B0C10`、`#110022`）。发光的霓虹强调色：青色（`#00FFFF`）、热粉（`#FF00FF`）、电黄（`#FFFF00`）。
- **排版**：80 年代铬合金文字、毛笔风格（像霓虹招牌）和粗体斜体无衬线字体。
- **阴影**：投影不是黑色；它们与元素本身颜色相同，模糊度极高，营造光发射的感觉。

## Web 实现
- 依赖 `text-shadow` 实现霓虹灯，`3D` 变换实现地板网格。
- **CSS 示例**：
```css
body {
  background-color: #090014;
  color: #fff;
  font-family: 'Montserrat', sans-serif;
  overflow-x: hidden;
}

/* 霓虹文字发光 */
.synth-neon-text {
  font-family: 'Mr Dafoe', cursive; /* 经典 80 年代手写体 */
  font-size: 4rem;
  color: #fff;
  text-shadow: 
    0 0 5px #fff,
    0 0 10px #fff,
    0 0 20px #FF00FF,
    0 0 40px #FF00FF,
    0 0 80px #FF00FF;
}

/* 透视网格地板 */
.synth-grid {
  position: absolute;
  bottom: 0; left: -50%;
  width: 200%; height: 50vh;
  background-image: 
    linear-gradient(rgba(0, 255, 255, 0.8) 2px, transparent 2px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.8) 2px, transparent 2px);
  background-size: 50px 50px;
  
  /* 创建 3D 地平线效果 */
  transform: perspective(500px) rotateX(60deg);
  transform-origin: top center;
  
  /* 渐隐至地平线 */
  mask-image: linear-gradient(to bottom, transparent 0%, black 100%);
  -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 100%);
}
```

## App 实现

### SwiftUI
```swift
struct NeonText: View {
    let text: String
    
    var body: some View {
        Text(text)
            .font(.custom("Mr Dafoe", size: 64))
            .foregroundColor(.white)
            // 分层阴影创建发光晕染
            .shadow(color: .white, radius: 2)
            .shadow(color: .pink, radius: 5)
            .shadow(color: .pink, radius: 10)
            .shadow(color: .pink, radius: 20)
    }
}

struct SynthwaveScreen: View {
    var body: some View {
        ZStack {
            Color(red: 0.03, green: 0.0, blue: 0.08).ignoresSafeArea() // #090014
            
            VStack {
                NeonText(text: "Outrun")
                Spacer()
            }
            
            // 注意：3D 透视网格需要 SceneKit 或预渲染图像
            // 原生 SwiftUI 3D 变换作用于视图，但无法轻松绘制无限地板网格。
            Image("synth_grid")
                .resizable()
                .scaledToFill()
                .frame(height: 300)
                .offset(y: 200)
        }
    }
}
```
- 在文字上直接堆叠多个 `.shadow(color:radius:)` modifier 来创建鲜艳的霓虹晕染效果。
- 3D 线框地平线网格最好通过预渲染的背景图像来实现。

### Flutter
```dart
class NeonText extends StatelessWidget {
  final String text;
  const NeonText(this.text);

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: const TextStyle(
        fontFamily: 'Mr Dafoe', // 或任何花体 80 年代字体
        fontSize: 64,
        color: Colors.white,
        shadows: [
          Shadow(color: Colors.white, blurRadius: 2),
          Shadow(color: Colors.pinkAccent, blurRadius: 5),
          Shadow(color: Colors.pinkAccent, blurRadius: 15),
          Shadow(color: Colors.pinkAccent, blurRadius: 30),
        ],
      ),
    );
  }
}

class SynthwaveScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF090014),
      body: Stack(
        children: [
          // 背景网格资产
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            height: 300,
            child: Image.asset('assets/synth_grid.png', fit: BoxFit.cover),
          ),
          // 前景 UI
          const Center(child: NeonText('Outrun')),
        ],
      ),
    );
  }
}
```
- `TextStyle` 接受 `Shadow` 对象列表。堆叠它们，模糊半径呈指数增长（例如 2, 5, 15, 30），模拟光的散射。
- 除非你想手动做 3D 数学，否则避免使用 `CustomPaint` 程序化渲染透视网格。使用资产。

### React Native
```jsx
// React Native 原生仅支持每个 Text 元素一个 textShadow。
// 要创建真正的霓虹光晕，必须堆叠相同的 Text 组件。

const NeonText = ({ text }) => {
  const baseStyle = {
    fontSize: 64,
    fontFamily: 'MrDafoe',
    fontWeight: 'bold',
    color: '#FFF',
    position: 'absolute',
  };

  return (
    <View style={{ alignItems: 'center', height: 80 }}>
      {/* 外层光晕 */}
      <Text style={[baseStyle, { textShadowColor: '#FF00FF', textShadowRadius: 30 }]}>{text}</Text>
      {/* 中层光晕 */}
      <Text style={[baseStyle, { textShadowColor: '#FF00FF', textShadowRadius: 15 }]}>{text}</Text>
      {/* 核心光晕 */}
      <Text style={[baseStyle, { textShadowColor: '#FFF', textShadowRadius: 5 }]}>{text}</Text>
      {/* 锐利白色核心 */}
      <Text style={baseStyle}>{text}</Text>
    </View>
  );
};

const SynthwaveScreen = () => (
  <View style={{ flex: 1, backgroundColor: '#090014', justifyContent: 'center' }}>
    <NeonText text="Outrun" />
    
    <Image 
      source={require('./synth_grid.png')}
      style={{ position: 'absolute', bottom: 0, width: '100%', height: 300, resizeMode: 'cover' }}
    />
  </View>
);
```
- **React Native 限制**：无法将阴影数组传递给 `textShadow`。
- **变通方案**：使用 `position: 'absolute'` 渲染相同 `<Text>` 组件 3-4 次，每次使用不同的 `textShadowRadius` 来构建晕染。

### Jetpack Compose
```kotlin
@Composable
fun NeonText(text: String) {
    Text(
        text = text,
        fontSize = 64.sp,
        color = Color.White,
        fontFamily = FontFamily.Cursive,
        // Compose 原生仅在 TextStyle 上支持单个 Shadow
        style = TextStyle(
            shadow = Shadow(
                color = Color(0xFFFF00FF),
                offset = Offset.Zero,
                blurRadius = 30f // 单个大幅模糊作为回退
            )
        ),
        // 要获取堆叠模糊，使用 Modifier.drawBehind 重复绘制文字
    )
}

// 高级堆叠发光方法
@Composable
fun AdvancedNeonText(text: String) {
    Box(contentAlignment = Alignment.Center) {
        // 渲染文字图层来构建光晕
        val blurs = listOf(30f, 15f, 5f)
        blurs.forEach { blur ->
            Text(
                text = text,
                color = Color.Transparent,
                style = TextStyle(
                    shadow = Shadow(Color(0xFFFF00FF), Offset.Zero, blur)
                )
            )
        }
        // 顶部实色图层
        Text(text = text, color = Color.White)
    }
}
```
- **Compose 限制**：与 React Native 一样，`TextStyle` 仅接受单个 `Shadow`。
- **变通方案**：在 `Box` 中堆叠多个透明的 `Text` 组合，每个投射不同大小的阴影，顶部覆盖实色白色核心文字。

## 推荐与避免
- **推荐**：将字体斜体化，传达速度感和前进的动力。
- **避免**：使用标准、微妙的 box shadow。如果元素投射阴影，它必须投射霓虹光晕。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。