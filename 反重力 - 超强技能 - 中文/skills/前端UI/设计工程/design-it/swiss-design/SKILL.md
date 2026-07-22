---
name: swiss-design
description: Swiss Design（国际主义印刷风格）的 Web 与 App 实现指南。当用户希望严格的网格系统、强烈的排版和干净的不对称对齐时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Swiss Design（国际主义印刷风格）

> "形式追随功能。网格是绝对的。排版是主要的视觉元素。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **数学网格**：一切对齐到严格的底层网格。优先采用不对称而非居中文本。
2. **无衬线排版**：Helvetica 是王者，但任何干净、中性的无衬线字体都行。文本左对齐，右边不对齐。
3. **客观摄影**：如果使用图片，应当是客观的纪实风格照片，而非风格化插图。

## 视觉 DNA
- **颜色**：非常有限。通常只有黑、白和**一种**高饱和度的强调色（通常是原色红、蓝或黄）。**Industrial Chic** 完美适用。
- **排版**：`Helvetica Neue`、`Inter` 或 `Roboto`。字号差距巨大（例如 6rem 标题搭配 1rem 正文）。
- **布局**：**绝不**居中文本。永远。

## Web 实现
- 大量使用 CSS Grid。让列定义布局。
- **CSS 示例**：
```css
body {
  background-color: #f4f4f4;
  color: #111;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  line-height: 1.4;
}

.swiss-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
  padding: 40px;
}

.swiss-header {
  grid-column: 1 / 11; /* 横跨多列，右侧留空 */
  font-size: 6vw;
  font-weight: 700;
  text-transform: lowercase; /* 可选，但在粗野/瑞士风格中常见 */
  margin-bottom: 2rem;
  line-height: 0.9;
  letter-spacing: -0.04em;
}

.swiss-content {
  grid-column: 4 / 9; /* 缩进对齐 */
  font-size: 1.25rem;
  text-align: left; /* 左对齐，右边不对齐 */
}

.swiss-accent {
  color: #E2001A; /* 经典瑞士红 */
}
```

## App 实现

### SwiftUI
```swift
struct SwissDesignView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 0) {
                // 标题块
                VStack(alignment: .leading, spacing: 8) {
                    Text("the grid")
                        .font(.custom("Helvetica Neue", size: 60))
                        .fontWeight(.heavy)
                        .tracking(-2) // 紧字距
                    Text("is absolute.")
                        .font(.custom("Helvetica Neue", size: 60))
                        .fontWeight(.heavy)
                        .tracking(-2)
                        .foregroundColor(Color(hex: "E2001A")) // 瑞士红
                }
                .padding(.horizontal, 24)
                .padding(.top, 60)
                .padding(.bottom, 40)
                
                Divider().background(Color.black)
                
                // 不对称内容块
                HStack(alignment: .top, spacing: 20) {
                    // 左侧空列（负空间就是结构性元素）
                    Spacer().frame(width: 40)
                    
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Form follows function.")
                            .font(.custom("Helvetica Neue", size: 24))
                            .fontWeight(.bold)
                        
                        Text("Typography is the primary visual element. Everything aligns to a strict underlying grid. Asymmetry is preferred over centered text.")
                            .font(.custom("Helvetica Neue", size: 16))
                            .lineSpacing(6)
                    }
                    .padding(.vertical, 40)
                    .padding(.trailing, 24)
                }
                
                Divider().background(Color.black)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .background(Color(white: 0.96))
        .foregroundColor(.black)
    }
}
```
- 严格使用 `alignment: .leading`。永远不要使用 `.center`。
- 在 `HStack` 中使用 `Spacer().frame(width: X)` 故意将内容推出左边距，营造经典的瑞士缩进不对称网格。

### Flutter
```dart
class SwissDesignScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F4F4),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 80),
            // 标题
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text('the grid', style: TextStyle(fontFamily: 'Helvetica', fontSize: 60, fontWeight: FontWeight.w900, height: 0.9, letterSpacing: -2)),
                  Text('is absolute.', style: TextStyle(fontFamily: 'Helvetica', fontSize: 60, fontWeight: FontWeight.w900, height: 0.9, letterSpacing: -2, color: Color(0xFFE2001A))),
                ],
              ),
            ),
            const SizedBox(height: 40),
            const Divider(color: Colors.black, thickness: 1, height: 1),
            
            // 不对称内容
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // 结构性空列
                const SizedBox(width: 64),
                // 内容列
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.only(top: 40.0, bottom: 40.0, right: 24.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text('Form follows function.', style: TextStyle(fontFamily: 'Helvetica', fontSize: 24, fontWeight: FontWeight.bold)),
                        SizedBox(height: 16),
                        Text('Typography is the primary visual element. Everything aligns to a strict underlying grid.', style: TextStyle(fontFamily: 'Helvetica', fontSize: 16, height: 1.4)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const Divider(color: Colors.black, thickness: 1, height: 1),
          ],
        ),
      ),
    );
  }
}
```
- 在所有 `Column` 上强制 `CrossAxisAlignment.start`。
- 使用带固定 `SizedBox` 宽度的 `Row` 在左侧，右侧使用 `Expanded` 组件强制执行不对称网格列。

### React Native
```jsx
const SwissDesignScreen = () => {
  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#F4F4F4' }}>
      
      {/* 标题 */}
      <View style={{ paddingHorizontal: 24, paddingTop: 80, paddingBottom: 40 }}>
        <Text style={{ fontFamily: 'HelveticaNeue-CondensedBlack', fontSize: 60, lineHeight: 60, letterSpacing: -2, color: '#111' }}>
          the grid
        </Text>
        <Text style={{ fontFamily: 'HelveticaNeue-CondensedBlack', fontSize: 60, lineHeight: 60, letterSpacing: -2, color: '#E2001A' }}>
          is absolute.
        </Text>
      </View>

      <View style={{ height: 1, backgroundColor: '#111' }} />

      {/* 不对称布局 */}
      <View style={{ flexDirection: 'row', paddingVertical: 40 }}>
        {/* 空左侧列 */}
        <View style={{ width: 64 }} />
        
        {/* 内容 */}
        <View style={{ flex: 1, paddingRight: 24 }}>
          <Text style={{ fontFamily: 'HelveticaNeue-Bold', fontSize: 24, color: '#111', marginBottom: 16 }}>
            Form follows function.
          </Text>
          <Text style={{ fontFamily: 'HelveticaNeue-Regular', fontSize: 16, lineHeight: 24, color: '#111' }}>
            Typography is the primary visual element. Everything aligns to a strict underlying grid.
          </Text>
        </View>
      </View>

      <View style={{ height: 1, backgroundColor: '#111' }} />

    </ScrollView>
  );
};
```
- 链接 Helvetica Neue 字体家族。`HelveticaNeue-CondensedBlack` 标题与 `HelveticaNeue-Regular` 正文之间的对比定义了这种风格。
- 使用 `flexDirection: 'row'` 构建严格的列结构。

### Jetpack Compose
```kotlin
@Composable
fun SwissDesignScreen() {
    Column(
        modifier = Modifier.fillMaxSize().background(Color(0xFFF4F4F4)).verticalScroll(rememberScrollState())
    ) {
        Spacer(Modifier.height(80.dp))
        
        // 标题
        Column(modifier = Modifier.padding(horizontal = 24.dp, vertical = 40.dp)) {
            Text(
                text = "the grid",
                fontFamily = FontFamily.SansSerif, // 替换为 Helvetica
                fontSize = 60.sp,
                fontWeight = FontWeight.Black,
                letterSpacing = (-2).sp,
                lineHeight = 60.sp,
                color = Color.Black
            )
            Text(
                text = "is absolute.",
                fontFamily = FontFamily.SansSerif,
                fontSize = 60.sp,
                fontWeight = FontWeight.Black,
                letterSpacing = (-2).sp,
                lineHeight = 60.sp,
                color = Color(0xFFE2001A)
            )
        }
        
        Divider(color = Color.Black, thickness = 1.dp)
        
        // 不对称网格行
        Row(modifier = Modifier.fillMaxWidth().padding(vertical = 40.dp)) {
            // 空网格列
            Spacer(modifier = Modifier.width(64.dp))
            
            // 内容
            Column(modifier = Modifier.weight(1f).padding(right = 24.dp)) {
                Text(
                    text = "Form follows function.",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )
                Spacer(Modifier.height(16.dp))
                Text(
                    text = "Typography is the primary visual element. Everything aligns to a strict underlying grid.",
                    fontSize = 16.sp,
                    color = Color.Black
                )
            }
        }
        
        Divider(color = Color.Black, thickness = 1.dp)
    }
}
```
- 使用 `Divider(color = Color.Black, thickness = 1.dp)` 创建生硬的水平结构线。
- 结合 `Row`、固定 `Spacer` 宽度和带 `Modifier.weight(1f)` 的 `Column` 强制执行不对称设计。

## 推荐与避免
- **推荐**：将负空间作为结构性元素。空列与填充列同样重要。
- **避免**：居中文本。不要使用衬线字体。不要使用投影。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。