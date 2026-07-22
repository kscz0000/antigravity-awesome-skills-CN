---
name: editorial-design
description: Editorial Design 的 Web 与 App 实现指南。当用户需要杂志风格布局、大标题和优雅的字体搭配时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Editorial Design

> "数字杂志。精致的字体搭配和刻意而优雅的节奏。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **衬线 & 无衬线搭配**：编辑设计的标志。一款漂亮、高对比度的衬线字体用于标题，搭配一款干净的无衬线字体用于正文。
2. **大写首字母下沉 & 拉引语**：引导读者视线、打破长段文字的排版装饰。
3. **分栏布局**：内容在不同的栏中流动，常用细线（栏规）分隔。

## 视觉 DNA
- **颜色**：**Modern Editorial** 或 **Yacht Club**。温暖、纸感背景搭配深沉的墨色黑或海军蓝。
- **排版**：
  - 标题：`Playfair Display`、`Merriweather`、`Bodoni`。
  - 正文：`Lato`、`Open Sans`、`Source Sans Pro`。
- **边框**：细而优雅的水平细线（发丝线）用于分隔区块。

## Web 实现
- **CSS 示例**：
```css
body {
  background-color: #F9F9F9; /* 纸张白 */
  color: #121212; /* 墨色黑 */
}

/* 字体搭配 */
.editorial-headline {
  font-family: 'Playfair Display', serif;
  font-size: 4rem;
  font-weight: 700;
  font-style: italic;
  margin-bottom: 24px;
  border-bottom: 1px solid #121212;
  padding-bottom: 24px;
}

.editorial-body {
  font-family: 'Lato', sans-serif;
  font-size: 1.1rem;
  line-height: 1.8;
  column-count: 2; /* 杂志栏 */
  column-gap: 40px;
}

/* 首字母下沉 */
.editorial-body::first-letter {
  font-family: 'Playfair Display', serif;
  font-size: 4rem;
  float: left;
  line-height: 0.8;
  padding-right: 12px;
  color: var(--cta-highlight);
}

.pull-quote {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  text-align: center;
  margin: 48px 0;
  padding: 24px 0;
  border-top: 2px solid #121212;
  border-bottom: 2px solid #121212;
}
```

## App 实现

### SwiftUI
```swift
struct EditorialView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                // 编辑式标题
                Text("The Digital\nMagazine")
                    .font(.custom("Playfair Display", size: 48))
                    .fontWeight(.bold)
                    .italic()
                    .foregroundColor(Color(white: 0.05))
                    .padding(.bottom, 16)
                
                Divider().background(Color.black)
                
                // 首字母下沉与正文
                HStack(alignment: .top, spacing: 8) {
                    Text("I")
                        .font(.custom("Playfair Display", size: 64))
                        .foregroundColor(Color(red: 0.7, green: 0.2, blue: 0.2))
                        // 负内边距将正文拉近首字母
                        .padding(.top, -10) 
                    
                    Text("n an era of sterile, flat interfaces, the return to elegant typography feels like a breath of fresh air. The interplay of serif and sans-serif...")
                        .font(.custom("Lato", size: 16))
                        .lineSpacing(6)
                        .foregroundColor(Color(white: 0.1))
                }
                
                // 拉引语
                VStack {
                    Divider().background(Color.black)
                    Text("“Sophistication is in the spacing.”")
                        .font(.custom("Playfair Display", size: 28))
                        .italic()
                        .multilineTextAlignment(.center)
                        .padding(.vertical, 24)
                    Divider().background(Color.black)
                }
                .padding(.vertical, 24)
            }
            .padding(24)
        }
        .background(Color(red: 0.98, green: 0.98, blue: 0.96)) // 温暖纸张白
    }
}
```
- 必须大量使用 `.font(.custom())`。系统字体看起来太像普通应用。
- 使用 `Divider()` 创建印刷设计中常见的细发线。
- 可以通过 `HStack` 顶部对齐伪造"首字母下沉"。

### Flutter
```dart
class EditorialScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9F9F8), // 纸张背景
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 40),
            const Text(
              'The Digital\nMagazine',
              style: TextStyle(fontFamily: 'PlayfairDisplay', fontSize: 48, fontWeight: FontWeight.bold, fontStyle: FontStyle.italic, height: 1.1),
            ),
            const SizedBox(height: 24),
            const Divider(color: Colors.black, thickness: 1),
            const SizedBox(height: 24),
            // 使用 RichText 模拟首字母下沉比较复杂，
            // 移动端使用简单的 Row 方式已经足够
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'I',
                  style: TextStyle(fontFamily: 'PlayfairDisplay', fontSize: 72, height: 1.0, color: Color(0xFF8B0000)),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: const Text(
                    'n an era of sterile, flat interfaces, the return to elegant typography feels like a breath of fresh air. The interplay of serif and sans-serif brings humanity back to the screen.',
                    style: TextStyle(fontFamily: 'Lato', fontSize: 16, height: 1.6, color: Colors.black87),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 48),
            // 拉引语
            const Divider(color: Colors.black, thickness: 2),
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 32.0),
              child: Center(
                child: Text(
                  '“Sophistication is in the spacing.”',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontFamily: 'PlayfairDisplay', fontSize: 28, fontStyle: FontStyle.italic),
                ),
              ),
            ),
            const Divider(color: Colors.black, thickness: 2),
          ],
        ),
      ),
    );
  }
}
```
- 在 `TextStyle` 中设置 `height` 参数（行高）。`1.6` 是良好的编辑式正文字体行高。
- 使用 `thickness: 2` 的 `Divider` 来表现拉引语周围的粗栏规。

### React Native
```jsx
const EditorialScreen = () => {
  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#F9F9F8', padding: 24 }}>
      <Text style={{ 
        fontFamily: 'PlayfairDisplay-BoldItalic', 
        fontSize: 48, 
        color: '#121212', 
        lineHeight: 52,
        marginTop: 40,
        marginBottom: 24 
      }}>
        The Digital{'\n'}Magazine
      </Text>
      
      <View style={{ height: 1, backgroundColor: '#121212', marginBottom: 24 }} />
      
      <View style={{ flexDirection: 'row' }}>
        <Text style={{ 
          fontFamily: 'PlayfairDisplay-Bold', 
          fontSize: 72, 
          color: '#8B0000',
          lineHeight: 80,
          marginTop: -10, // 调整对齐
          marginRight: 8
        }}>
          I
        </Text>
        <Text style={{ 
          flex: 1, 
          fontFamily: 'Lato-Regular', 
          fontSize: 16, 
          lineHeight: 26, 
          color: '#333' 
        }}>
          n an era of sterile, flat interfaces, the return to elegant typography feels like a breath of fresh air. The interplay of serif and sans-serif brings humanity.
        </Text>
      </View>
      
      {/* 拉引语 */}
      <View style={{ 
        borderTopWidth: 2, borderBottomWidth: 2, borderColor: '#121212', 
        marginTop: 48, paddingVertical: 32 
      }}>
        <Text style={{ 
          fontFamily: 'PlayfairDisplay-Italic', 
          fontSize: 28, 
          textAlign: 'center', 
          color: '#121212' 
        }}>
          “Sophistication is in the spacing.”
        </Text>
      </View>
    </ScrollView>
  );
};
```
- 行高和字体就是一切。你必须在 React Native 项目中链接自定义字体，这种风格才能正常工作。
- 在容器 `View` 上使用 `borderTopWidth` 和 `borderBottomWidth` 来创建拉引语样式。

### Jetpack Compose
```kotlin
@Composable
fun EditorialScreen() {
    // 假设 Playfair 和 Lato 已定义在 FontFamily 中
    val playfair = FontFamily.Serif 
    val lato = FontFamily.SansSerif

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF9F9F8))
            .verticalScroll(rememberScrollState())
            .padding(24.dp)
    ) {
        Spacer(Modifier.height(40.dp))
        
        Text(
            text = "The Digital\nMagazine",
            fontFamily = playfair,
            fontSize = 48.sp,
            fontWeight = FontWeight.Bold,
            fontStyle = FontStyle.Italic,
            lineHeight = 52.sp,
            color = Color(0xFF121212)
        )
        
        Spacer(Modifier.height(24.dp))
        Divider(color = Color(0xFF121212), thickness = 1.dp)
        Spacer(Modifier.height(24.dp))
        
        Row(verticalAlignment = Alignment.Top) {
            Text(
                text = "I",
                fontFamily = playfair,
                fontSize = 72.sp,
                color = Color(0xFF8B0000),
                modifier = Modifier.offset(y = (-10).dp).padding(end = 8.dp)
            )
            Text(
                text = "n an era of sterile, flat interfaces, the return to elegant typography feels like a breath of fresh air. The interplay of serif and sans-serif.",
                fontFamily = lato,
                fontSize = 16.sp,
                lineHeight = 26.sp,
                color = Color(0xFF333333)
            )
        }
        
        Spacer(Modifier.height(48.dp))
        
        // 拉引语
        Divider(color = Color(0xFF121212), thickness = 2.dp)
        Text(
            text = "“Sophistication is in the spacing.”",
            fontFamily = playfair,
            fontSize = 28.sp,
            fontStyle = FontStyle.Italic,
            textAlign = TextAlign.Center,
            modifier = Modifier.fillMaxWidth().padding(vertical = 32.dp)
        )
        Divider(color = Color(0xFF121212), thickness = 2.dp)
    }
}
```
- Compose 非常优雅地处理自定义字体和行高（`26.sp`）。
- 使用 `Divider()` 创建细发线。根据标题与拉引语的需要调整粗细。

## 推荐与避免
- **推荐**：像对待印刷页面一样对待界面。边距应慷慨。
- **避免**：用典型的应用组件（如浮动操作按钮或厚重的导航栏）堆砌 UI。保持简洁。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。