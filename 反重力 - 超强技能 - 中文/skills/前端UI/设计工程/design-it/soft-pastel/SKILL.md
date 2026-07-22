---
name: soft-pastel
description: Soft Pastel Design 的 Web 与 App 实现指南。当用户希望柔和的颜色、平静的 UI、婴儿/生活方式品牌或低对比度美学时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Soft Pastel Design

> "平静、通透、温柔。在洗淡、明快的色调上构建的低压力界面。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **降低饱和度、高亮度的颜色**：每种颜色都与大量白色混合。
2. **柔和、圆润的边缘**：圆角较大且友好。
3. **通透的间距**：慷慨的留白防止柔和颜色显得浑浊或拥挤。

## 视觉 DNA
- **颜色**：薄荷绿、婴儿蓝、腮红粉、薰衣草黄油。背景使用温暖、略偏白的色调（例如 `#FFFBF7`），而非临床感的纯 `#FFFFFF`。
- **排版**：柔和、圆润的无衬线字体（如 `Quicksand`、`Nunito`）或优雅、低对比度的衬线字体。避免激进、超粗的字体。
- **阴影**：非常柔和、面积大的阴影，通常带有柔和色调而非黑色。

## Web 实现
- **CSS 示例**：
```css
:root {
  --pastel-bg: #FFFBF7;
  --pastel-pink: #FFD1DC;
  --pastel-blue: #AEC6CF;
  --pastel-green: #B7E4C7;
  --pastel-text: #4A4A4A; /* 柔和的深灰色，而非纯黑 */
}

body {
  background-color: var(--pastel-bg);
  color: var(--pastel-text);
  font-family: 'Nunito', sans-serif;
  line-height: 1.6;
}

.pastel-card {
  background-color: #ffffff;
  border-radius: 24px;
  padding: 40px;
  /* 带色调的、非常柔和的阴影 */
  box-shadow: 0 20px 40px rgba(174, 198, 207, 0.15); 
}

.pastel-pill {
  background-color: var(--pastel-pink);
  color: #a05a6c; /* 较深版本的粉色以保证对比度 */
  border-radius: 50px;
  padding: 8px 24px;
  font-weight: 700;
  display: inline-block;
}

.pastel-btn {
  background-color: var(--pastel-blue);
  color: #2b5563; /* 较深文字 */
  border: none;
  border-radius: 12px;
  padding: 16px 32px;
  transition: transform 0.2s;
}
.pastel-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(174, 198, 207, 0.4);
}
```

## App 实现

### SwiftUI
```swift
struct SoftPastelView: View {
    // 柔和色调色板
    let bg = Color(hex: "FFFBF7")
    let pink = Color(hex: "FFD1DC")
    let blue = Color(hex: "AEC6CF")
    let textDark = Color(hex: "4A4A4A")
    
    var body: some View {
        ScrollView {
            VStack(spacing: 32) {
                // 柔和卡片
                VStack(alignment: .leading, spacing: 16) {
                    Text("Calm & Airy")
                        .font(.custom("Nunito-Bold", size: 28))
                        .foregroundColor(textDark)
                    
                    Text("Generous whitespace and soft corners prevent the desaturated colors from feeling muddy.")
                        .font(.custom("Nunito-Regular", size: 16))
                        .foregroundColor(textDark.opacity(0.8))
                        .lineSpacing(6)
                }
                .padding(40)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color.white)
                .cornerRadius(32) // 柔和的大圆角
                // 带柔和色调的阴影，而非黑色或灰色
                .shadow(color: blue.opacity(0.2), radius: 30, y: 15)
                
                // 柔和按钮
                Button(action: {}) {
                    Text("Gentle Action")
                        .font(.custom("Nunito-Bold", size: 18))
                        .foregroundColor(Color(hex: "2B5563")) // 较深对比色
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 20)
                        .background(blue)
                        .cornerRadius(20)
                }
            }
            .padding(24)
        }
        .background(bg.ignoresSafeArea())
    }
}
```
- 像 Nunito 或 Quicksand 这样的自定义字体几乎是必需的。系统字体通常过于生硬。
- `shadow(color:)` 必须带有柔和色调之一，绝不能是黑色或灰色。
- 圆角应该非常大（20-32）。

### Flutter
```dart
class SoftPastelScreen extends StatelessWidget {
  final Color bg = const Color(0xFFFFFBF7);
  final Color pink = const Color(0xFFFFD1DC);
  final Color blue = const Color(0xFFAEC6CF);
  final Color textDark = const Color(0xFF4A4A4A);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: bg,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            // 柔和卡片
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(40),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(32), // 柔和边角
                boxShadow: [
                  // 带色调的阴影
                  BoxShadow(color: blue.withOpacity(0.2), blurRadius: 30, offset: const Offset(0, 15))
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Calm & Airy', style: TextStyle(fontFamily: 'Nunito', fontSize: 28, fontWeight: FontWeight.bold, color: textDark)),
                  const SizedBox(height: 16),
                  Text('Generous whitespace and soft corners.', style: TextStyle(fontFamily: 'Nunito', fontSize: 16, height: 1.6, color: textDark.withOpacity(0.8))),
                ],
              ),
            ),
            const SizedBox(height: 32),
            
            // 柔和按钮
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                backgroundColor: blue,
                foregroundColor: const Color(0xFF2B5563), // 较深文字以保证对比度
                minimumSize: const Size(double.infinity, 60),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                elevation: 0, // 移除默认生硬阴影
              ),
              child: const Text('Gentle Action', style: TextStyle(fontFamily: 'Nunito', fontSize: 18, fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }
}
```
- 如果要应用自定义色调投影，禁用 Flutter 按钮和卡片的 `elevation`。默认凸起会投射黑色阴影。

### React Native
```jsx
const SoftPastelScreen = () => {
  const colors = {
    bg: '#FFFBF7',
    blue: '#AEC6CF',
    textDark: '#4A4A4A'
  };

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg, padding: 24 }}>
      
      {/* 柔和卡片 */}
      <View style={{
        backgroundColor: '#FFFFFF',
        borderRadius: 32,
        padding: 40,
        marginBottom: 32,
        // iOS 带色调阴影
        shadowColor: colors.blue, shadowOffset: { width: 0, height: 15 },
        shadowOpacity: 0.2, shadowRadius: 30,
        // Android 带色调阴影（需要 Android 9+）
        elevation: 10, shadowColor: colors.blue,
      }}>
        <Text style={{ fontFamily: 'Nunito-Bold', fontSize: 28, color: colors.textDark, marginBottom: 16 }}>
          Calm & Airy
        </Text>
        <Text style={{ fontFamily: 'Nunito-Regular', fontSize: 16, lineHeight: 26, color: colors.textDark, opacity: 0.8 }}>
          Generous whitespace and soft corners prevent the desaturated colors from feeling muddy.
        </Text>
      </View>

      {/* 柔和按钮 */}
      <TouchableOpacity style={{
        backgroundColor: colors.blue,
        borderRadius: 20,
        paddingVertical: 20,
        alignItems: 'center'
      }}>
        <Text style={{ fontFamily: 'Nunito-Bold', fontSize: 18, color: '#2B5563' }}>
          Gentle Action
        </Text>
      </TouchableOpacity>
      
    </ScrollView>
  );
};
```
- 确保使用柔和的、非纯白的背景（`#FFFBF7`），让纯白 `#FFFFFF` 卡片与之形成柔和对比。
- 在 Android 9+ 上，带色调的阴影通过 `shadowColor` 配合 `elevation` 起效。

### Jetpack Compose
```kotlin
@Composable
fun SoftPastelScreen() {
    val bg = Color(0xFFFFFBF7)
    val blue = Color(0xFFAEC6CF)
    val textDark = Color(0xFF4A4A4A)

    Column(
        modifier = Modifier.fillMaxSize().background(bg).verticalScroll(rememberScrollState()).padding(24.dp)
    ) {
        // 柔和卡片
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .shadow(
                    elevation = 20.dp, 
                    shape = RoundedCornerShape(32.dp), 
                    ambientColor = blue, // 带色调阴影
                    spotColor = blue
                )
                .background(Color.White, RoundedCornerShape(32.dp))
                .padding(40.dp)
        ) {
            Column {
                Text(
                    text = "Calm & Airy",
                    fontSize = 28.sp,
                    fontWeight = FontWeight.Bold,
                    color = textDark,
                    fontFamily = FontFamily.SansSerif // 替换为 Nunito
                )
                Spacer(Modifier.height(16.dp))
                Text(
                    text = "Generous whitespace and soft corners.",
                    fontSize = 16.sp,
                    lineHeight = 26.sp,
                    color = textDark.copy(alpha = 0.8f),
                    fontFamily = FontFamily.SansSerif
                )
            }
        }
        
        Spacer(Modifier.height(32.dp))
        
        // 柔和按钮
        Button(
            onClick = { },
            colors = ButtonDefaults.buttonColors(containerColor = blue, contentColor = Color(0xFF2B5563)),
            shape = RoundedCornerShape(20.dp),
            modifier = Modifier.fillMaxWidth().height(60.dp),
            elevation = null
        ) {
            Text("Gentle Action", fontSize = 18.sp, fontWeight = FontWeight.Bold)
        }
    }
}
```
- Compose 的 `shadow` modifier 接受 `ambientColor` 和 `spotColor`。将两者都设为你的柔和色调强调色，以获得柔和的色调光晕。

## 推荐与避免
- **推荐**：使用与柔和氛围匹配的插画素材（扁平矢量、柔和渐变）。
- **避免**：使用刺眼的黑色边框、锐利的角或高饱和度的原色。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。