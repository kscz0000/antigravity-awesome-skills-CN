---
name: minimalism
description: Minimalism（极简）风格的 Web 与 App 实现指南。当用户希望简洁布局、丰富留白、少量颜色和清晰层级时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Minimalism

> "少即是多。去除一切，只留下本质。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **极致留白**：边距和内边距应该是你最初认为合适的两倍。
2. **严格的排版**：依赖字重和字号建立层级，而不是颜色或边框。
3. **没有装饰**：没有边框，没有投影，没有背景纹理。

## 视觉 DNA
- **颜色**：与 **Minimalist Slate** 或 **Modern Editorial** 调色板搭配最佳。背景必须纯粹（纯白/黑或近白/黑）。
- **排版**：无衬线、几何字体（如 `Inter`、`Helvetica Neue`、`SF Pro`）。使用极致的字重对比（细体 vs 粗体）。
- **间距**：使用慷慨的基线网格（例如 8px 的倍数，强烈倾向于 48px 至 120px 的内边距）。

## Web 实现
- 使用 Flexbox/Grid 搭配大 `gap` 属性。
- **CSS 示例**：
```css
.minimal-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 120px 24px;
  background-color: var(--bg-primary);
}
.minimal-title {
  font-size: 3rem;
  font-weight: 300;
  letter-spacing: -0.02em;
  margin-bottom: 48px;
}
.minimal-btn {
  background: transparent;
  border: 1px solid var(--text-primary);
  padding: 16px 32px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  transition: all 0.3s ease;
}
```

## App 实现

### SwiftUI
```swift
struct MinimalView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 48) {
                Text("Headline")
                    .font(.system(size: 34, weight: .light))
                    .tracking(-0.5)
                
                Text("Body text sits quietly with generous space around it. Let the content breathe.")
                    .font(.system(size: 17, weight: .regular))
                    .foregroundColor(.secondary)
                    .lineSpacing(6)
                
                // 极简按钮 — 只有细边框，无填充
                Button(action: {}) {
                    Text("Continue")
                        .font(.system(size: 14, weight: .medium))
                        .tracking(1.5)
                        .textCase(.uppercase)
                        .padding(.horizontal, 32)
                        .padding(.vertical, 16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 0)
                                .stroke(Color.primary, lineWidth: 1)
                        )
                }
            }
            .padding(.horizontal, 24)
            .padding(.vertical, 80)
        }
        .background(Color(.systemBackground))
    }
}
```
- 使用 `VStack(spacing: 40...64)` 在元素间进行慷慨的分隔。
- 永远不要使用 `.shadow()` 或类似 `Card` 的容器。让留白定义分组。
- 谨慎使用 `Divider()` — 仅当两个相邻的区块需要分隔时才用。

### Flutter
```dart
class MinimalScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 80),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Headline',
              style: TextStyle(
                fontSize: 34,
                fontWeight: FontWeight.w300,
                letterSpacing: -0.5,
                color: Colors.black87,
              ),
            ),
            const SizedBox(height: 48),
            Text(
              'Body text sits quietly with generous space around it.',
              style: TextStyle(
                fontSize: 17,
                fontWeight: FontWeight.w400,
                height: 1.6,
                color: Colors.black54,
              ),
            ),
            const SizedBox(height: 48),
            // 极简按钮 — 仅描边，无凸起
            OutlinedButton(
              onPressed: () {},
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: Colors.black87, width: 1),
                shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              ),
              child: Text(
                'CONTINUE',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                  letterSpacing: 1.5,
                  color: Colors.black87,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```
- 在所有 Material 组件（`AppBar`、`Card`、`FloatingActionButton`）上设置 `elevation: 0`。
- 使用 `SizedBox(height: 48)` 或更大的垂直间距。避免紧凑布局。
- 覆盖 `ThemeData` 以删除所有默认阴影：`cardTheme: CardTheme(elevation: 0)`。

### React Native
```jsx
const MinimalScreen = () => (
  <ScrollView
    style={{ flex: 1, backgroundColor: '#FFFFFF' }}
    contentContainerStyle={{ paddingHorizontal: 24, paddingVertical: 80 }}
  >
    <Text style={{
      fontSize: 34,
      fontWeight: '300',
      letterSpacing: -0.5,
      color: '#1A1A1A',
      marginBottom: 48,
    }}>
      Headline
    </Text>

    <Text style={{
      fontSize: 17,
      fontWeight: '400',
      lineHeight: 28,
      color: '#666666',
      marginBottom: 48,
    }}>
      Body text sits quietly with generous space around it.
    </Text>

    <TouchableOpacity
      style={{
        borderWidth: 1,
        borderColor: '#1A1A1A',
        paddingHorizontal: 32,
        paddingVertical: 16,
        alignSelf: 'flex-start',
      }}
      activeOpacity={0.6}
    >
      <Text style={{
        fontSize: 14,
        fontWeight: '500',
        letterSpacing: 1.5,
        color: '#1A1A1A',
        textTransform: 'uppercase',
      }}>
        Continue
      </Text>
    </TouchableOpacity>
  </ScrollView>
);
```
- 使用 `paddingVertical: 80` 作为屏幕级别的间距。翻倍于本能感受。
- 避免所有 `elevation` 和 `shadowColor` 属性。卡片不要 `borderRadius`。
- 如果使用 UI 库（如 React Native Paper），剥离默认凸起。

### Jetpack Compose
```kotlin
@Composable
fun MinimalScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 24.dp, vertical = 80.dp)
    ) {
        Text(
            text = "Headline",
            fontSize = 34.sp,
            fontWeight = FontWeight.Light,
            letterSpacing = (-0.5).sp,
            color = Color(0xFF1A1A1A),
        )
        Spacer(modifier = Modifier.height(48.dp))
        Text(
            text = "Body text sits quietly with generous space around it.",
            fontSize = 17.sp,
            fontWeight = FontWeight.Normal,
            lineHeight = 28.sp,
            color = Color(0xFF666666),
        )
        Spacer(modifier = Modifier.height(48.dp))
        // 极简描边按钮
        OutlinedButton(
            onClick = {},
            shape = RectangleShape,
            border = BorderStroke(1.dp, Color(0xFF1A1A1A)),
            colors = ButtonDefaults.outlinedButtonColors(containerColor = Color.Transparent),
            contentPadding = PaddingValues(horizontal = 32.dp, vertical = 16.dp),
        ) {
            Text(
                text = "CONTINUE",
                fontSize = 14.sp,
                fontWeight = FontWeight.Medium,
                letterSpacing = 1.5.sp,
                color = Color(0xFF1A1A1A),
            )
        }
    }
}
```
- 将所有 `Card`、`TopAppBar` 和 `FloatingActionButton` 组合的 `elevation` 设为 `0.dp`。
- 一致地使用 `Spacer(modifier = Modifier.height(48.dp))` 来获得慷慨的垂直间距。
- 覆盖 `MaterialTheme` 形状和阴影默认值以删除所有深度提示。

## 推荐与避免
- **推荐**：极度专注于对齐。1px 的错位会破坏极简的错觉。
- **避免**：为内容使用"卡片"包装器。让留白定义分组。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。