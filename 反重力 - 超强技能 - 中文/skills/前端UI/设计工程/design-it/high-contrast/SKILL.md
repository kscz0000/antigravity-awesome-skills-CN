---
name: high-contrast
description: High Contrast Design 的 Web 与 App 实现指南。当用户需要无障碍优先设计、极致可读性或强烈视觉冲击时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# High Contrast Design

> "极致可读性。强烈、有力且普适可访问。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **WCAG AAA 合规**：每一种颜色搭配都必须超过 7:1 的对比度。
2. **清晰的边界**：可交互元素具有高度可见的边框和焦点状态。
3. **不模糊**：避免细微的灰色、低透明度文字或纯粹分散核心内容注意力的装饰元素。

## 视觉 DNA
- **颜色**：**Industrial Chic**（黑和白）或 **Modern Editorial**。经常使用一种高亮度的单一强调色（如纯黄 `#FFFF00` 或青 `#00FFFF`）与黑色对比。
- **排版**：高可读性、健壮的无衬线字体（`Atkinson Hyperlegible`、`Inter`、`Roboto`）。大号基础字号（18px+）。
- **样式**：卡片和按钮周围使用 2px 实心边框。避免投影，因为它们会降低边缘清晰度。

## Web 实现
- 重点关注焦点状态（`:focus-visible`）和清晰的激活状态。
- **CSS 示例**：
```css
:root {
  --hc-bg: #ffffff;
  --hc-text: #000000;
  --hc-accent: #0000FF; /* 纯蓝 */
  --hc-focus: #FF00FF; /* 高可见度焦点环 */
}

body {
  background-color: var(--hc-bg);
  color: var(--hc-text);
  font-family: 'Atkinson Hyperlegible', sans-serif;
  font-size: 18px; /* 更大的默认 */
}

.hc-card {
  background-color: #ffffff;
  border: 3px solid #000000; /* 不容错过的边界 */
  padding: 32px;
  border-radius: 8px;
}

.hc-btn {
  background-color: var(--hc-accent);
  color: #ffffff;
  border: 3px solid transparent; /* 为焦点预留空间 */
  border-radius: 4px;
  padding: 16px 32px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
}

/* 对高对比度 / 可访问性至关重要 */
.hc-btn:focus-visible, a:focus-visible {
  outline: 4px solid var(--hc-focus);
  outline-offset: 4px;
}

a {
  color: var(--hc-accent);
  text-decoration: underline;
  text-decoration-thickness: 2px;
}
```

## App 实现

### SwiftUI
```swift
struct HighContrastView: View {
    var body: some View {
        VStack(spacing: 32) {
            // 高对比度卡片
            VStack(alignment: .leading, spacing: 16) {
                Text("Maximum Legibility")
                    .font(.custom("Atkinson Hyperlegible", size: 24))
                    .fontWeight(.bold)
                    .foregroundColor(.black)
                
                Text("Content is king. Borders are stark. Contrast ratios exceed 7:1.")
                    .font(.custom("Atkinson Hyperlegible", size: 18))
                    .foregroundColor(.black)
            }
            .padding(32)
            .background(Color.white)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.black, lineWidth: 3)
            )
            
            // 高对比度操作按钮
            Button(action: {}) {
                Text("CONFIRM ACTION")
                    .font(.custom("Atkinson Hyperlegible", size: 18))
                    .fontWeight(.black)
                    .foregroundColor(.white)
                    .padding(.vertical, 16)
                    .padding(.horizontal, 32)
                    .background(Color.blue) // 必须是高对比度的蓝色，例如 #0000FF
                    .cornerRadius(4)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color.white)
    }
}
```
- 依赖 `.stroke(Color.black, lineWidth: 3)` 叠加。
- 确保文字是纯 `.black` 配纯 `.white`。如果使用 `.secondary` 颜色使对比度低于 7:1，请避免。
- 使用专为可读性设计的字体，如 Atkinson Hyperlegible。

### Flutter
```dart
class HighContrastScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // 高对比度卡片
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(32),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.black, width: 3), // 不容错过的边界
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Maximum Legibility', 
                      style: TextStyle(fontFamily: 'Atkinson', fontSize: 24, fontWeight: FontWeight.bold, color: Colors.black)),
                    SizedBox(height: 16),
                    Text('Content is king. Borders are stark. Contrast ratios exceed 7:1.', 
                      style: TextStyle(fontFamily: 'Atkinson', fontSize: 18, color: Colors.black)),
                  ],
                ),
              ),
              const SizedBox(height: 32),
              
              // 高对比度按钮
              ElevatedButton(
                onPressed: () {},
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF0000FF), // 纯蓝
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
                  elevation: 0, // 无阴影
                ),
                child: const Text('CONFIRM ACTION', 
                  style: TextStyle(fontFamily: 'Atkinson', fontSize: 18, fontWeight: FontWeight.w900)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```
- 在按钮上禁用 `elevation`；阴影会模糊边缘，降低对比度。
- 在容器上使用 `Border.all(color: Colors.black, width: 3)` 明确为低视力用户定义空间边界。

### React Native
```jsx
const HighContrastScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#FFFFFF', padding: 24, justifyContent: 'center' }}>
      
      {/* 高对比度卡片 */}
      <View style={{
        backgroundColor: '#FFFFFF',
        borderColor: '#000000',
        borderWidth: 3,
        borderRadius: 8,
        padding: 32,
        marginBottom: 32
      }}>
        <Text style={{ fontFamily: 'Atkinson-Bold', fontSize: 24, color: '#000000', marginBottom: 16 }}>
          Maximum Legibility
        </Text>
        <Text style={{ fontFamily: 'Atkinson-Regular', fontSize: 18, color: '#000000' }}>
          Content is king. Borders are stark. Contrast ratios exceed 7:1.
        </Text>
      </View>

      {/* 高对比度按钮 */}
      <TouchableOpacity style={{
        backgroundColor: '#0000FF',
        paddingVertical: 16,
        paddingHorizontal: 32,
        borderRadius: 4,
        alignItems: 'center'
      }}>
        <Text style={{ fontFamily: 'Atkinson-Bold', fontSize: 18, color: '#FFFFFF', fontWeight: '900' }}>
          CONFIRM ACTION
        </Text>
      </TouchableOpacity>
      
    </View>
  );
};
```
- 在 React Native 中，可访问性在很大程度上依赖高对比度。确保 `borderWidth: 3` 和明确的纯 `#000000` 文字颜色。
- 确保使用可访问的 `<TouchableOpacity>` 区域（最小 48x48 内边距用于命中区域）。

### Jetpack Compose
```kotlin
@Composable
fun HighContrastScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
            .padding(24.dp),
        verticalArrangement = Arrangement.Center
    ) {
        // 高对比度卡片
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color.White, RoundedCornerShape(8.dp))
                .border(3.dp, Color.Black, RoundedCornerShape(8.dp))
                .padding(32.dp)
        ) {
            Column {
                Text(
                    text = "Maximum Legibility",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )
                Spacer(Modifier.height(16.dp))
                Text(
                    text = "Content is king. Borders are stark. Contrast ratios exceed 7:1.",
                    fontSize = 18.sp,
                    color = Color.Black
                )
            }
        }
        
        Spacer(Modifier.height(32.dp))
        
        // 高对比度按钮
        Button(
            onClick = { },
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(0xFF0000FF),
                contentColor = Color.White
            ),
            shape = RoundedCornerShape(4.dp),
            elevation = null, // 禁用阴影以保持锐利
            modifier = Modifier.fillMaxWidth().height(56.dp)
        ) {
            Text("CONFIRM ACTION", fontSize = 18.sp, fontWeight = FontWeight.Black)
        }
    }
}
```
- 在容器周围使用 `Modifier.border(3.dp, Color.Black)`。
- 禁用按钮凸起（`elevation = null`），保持设计完全扁平锐利。

## 推荐与避免
- **推荐**：将颜色导入对比度检查器。如果低于 7:1，请调整。
- **避免**：仅依靠颜色传达含义（例如，不要仅将错误状态设为红色；要设为红色并添加错误图标并加粗文字）。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。