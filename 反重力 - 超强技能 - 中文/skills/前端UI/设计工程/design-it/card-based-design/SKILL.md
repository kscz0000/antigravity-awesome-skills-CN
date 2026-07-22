---
name: card-based-design
description: Card-Based Design 的 Web 与 App 实现指南。当用户需要信息卡片、Pinterest 风格布局或小巧的内容容器时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Card-Based Design

> "小口消化。将离散的信息封装进独立的视觉容器中。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **封装性**：每个卡片自成一格。它包含一张图片、一个标题、一段简短描述，通常还有一个操作（如按钮或"点赞"图标）。
2. **响应式流**：卡片能在不同屏幕尺寸下轻松重排（桌面端 4 列网格，手机端单列）。
3. **清晰的边界**：卡片必须在视觉上从背景中凸显出来。

## 视觉 DNA
- **颜色**：非常灵活。背景应与卡片颜色略有区别或色调不同。**Sophisticated Neutral** 适合营造高级感。
- **排版**：卡片内有清晰的层级（标题、副标题、正文）。
- **样式**：标准的 `border-radius: 8px` 和中等强度的投影。

## Web 实现
- CSS Grid 配合 `auto-fit` 或瀑布流布局。
- **CSS 示例**：
```css
body {
  background-color: #f0f2f5; /* 标准应用背景 */
  padding: 40px;
}

.card-grid {
  display: grid;
  /* 自动响应式布局 */
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.card {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden; /* 保持图片在圆角内 */
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-bottom: 1px solid #eee;
}

.card-content {
  padding: 20px;
  flex-grow: 1; /* 将底部推至卡片末尾 */
}

.card-footer {
  padding: 16px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
}
```

## App 实现

### SwiftUI
```swift
struct ContentCard: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // 图片区域
            Rectangle()
                .fill(Color.gray.opacity(0.2))
                .frame(height: 160)
            
            // 内容区域
            VStack(alignment: .leading, spacing: 8) {
                Text("Card Title")
                    .font(.headline)
                Text("A brief description of the content inside this discrete card container.")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            .padding(16)
        }
        .background(Color.white)
        .cornerRadius(12)
        // 干净、细微的投影
        .shadow(color: Color.black.opacity(0.08), radius: 12, x: 0, y: 4)
    }
}

// 在你的视图中：
// LazyVGrid(columns: [GridItem(.adaptive(minimum: 160), spacing: 16)]) { ... }
```
- 内部使用 `VStack` 配合 `.cornerRadius` 和 `.shadow` 是标准做法。
- 使用 `LazyVGrid` 与 `.adaptive(minimum: 160)` 自动创建一个多列卡片网格，在 iPad 或 iPhone 上都能完美排列。

### Flutter
```dart
class ContentCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4, // 原生处理阴影
      shadowColor: Colors.black.withOpacity(0.4),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      clipBehavior: Clip.antiAlias, // 关键：防止图片溢出圆角
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          // 图片区域
          Container(
            height: 160,
            color: Colors.grey[300],
            width: double.infinity,
          ),
          // 内容区域
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                Text('Card Title', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                SizedBox(height: 8),
                Text(
                  'A brief description of the content inside this discrete card container.',
                  style: TextStyle(color: Colors.black54),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
// 在你的视图中：使用 GridView.builder 进行布局
```
- 原生 `Card` 组件完成了几乎所有繁重工作。
- **关键修复**：必须在 `Card` 上设置 `clipBehavior: Clip.antiAlias`，否则图片的顶角会露出圆角边框之外。

### React Native
```jsx
const ContentCard = () => {
  return (
    <View style={styles.card}>
      <View style={styles.imageArea} />
      <View style={styles.contentArea}>
        <Text style={styles.title}>Card Title</Text>
        <Text style={styles.description} numberOfLines={2}>
          A brief description of the content inside this discrete card container.
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFF',
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 12,
    elevation: 4,
    margin: 8,
    overflow: 'hidden', // 将图片限制在边框内
  },
  imageArea: {
    height: 160,
    backgroundColor: '#E0E0E0',
  },
  contentArea: {
    padding: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 8,
  },
  description: {
    color: '#666',
  }
});
// 在你的视图中：<FlatList numColumns={2} data={data} renderItem={...} />
```
- 用带 `borderRadius` 和 `overflow: 'hidden'` 的 View 包裹所有内容。
- `elevation: 4` 在 Android 上提供投影，而 `shadow*` 属性处理 iOS。
- 对于 Pinterest/瀑布流风格（不同高度的列），必须使用 `react-native-masonry-list` 等第三方库，因为 `FlatList` 无法实现列内不同行高。

### Jetpack Compose
```kotlin
@Composable
fun ContentCard() {
    // ElevatedCard 原生提供阴影和形状
    ElevatedCard(
        elevation = CardDefaults.elevatedCardElevation(defaultElevation = 4.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.elevatedCardColors(containerColor = Color.White),
        modifier = Modifier.fillMaxWidth().padding(8.dp)
    ) {
        Column {
            // 图片区域
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(160.dp)
                    .background(Color.LightGray)
            )
            
            // 内容区域
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "Card Title",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Spacer(Modifier.height(8.dp))
                Text(
                    text = "A brief description of the content inside this discrete card container.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = Color.Gray,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}
// 在你的视图中：LazyVerticalGrid(columns = GridCells.Adaptive(minSize = 160.dp)) { ... }
```
- `ElevatedCard` 是 Material 3 中完美的组件，自动处理裁剪和阴影。
- 在 `LazyVerticalGrid` 中使用 `GridCells.Adaptive(minSize = 160.dp)`，实现与 CSS Grid `auto-fit` 完全一致的自动流网格。

## 推荐与避免
- **推荐**：让整张卡片都可点击，而不仅仅是标题或图片。
- **避免**：在卡片中塞入过多文字。如果用户需要*在卡片内*滚动，说明卡片太大了。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。