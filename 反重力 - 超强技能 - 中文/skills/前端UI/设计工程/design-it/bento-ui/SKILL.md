---
name: bento-ui
description: Bento UI 的 Web 与 App 实现指南。当用户需要模块化网格卡片、Apple 风格的仪表板，或像便当盒一样分区排列的界面时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Bento UI

> "万物各得其所。由独立分隔组成的、结构化、高度模块化的网格。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **严格网格结构**：整个 UI 构建在响应式、多列网格之上（通常是 3x3、4x4，或不规则的瀑布流）。
2. **圆角分隔**：每个独立的内容块都包裹在卡片（分隔）中，圆角一致且通常较大。
3. **等距间距**：分隔之间的间隙必须处处完全一致。

## 视觉 DNA
- **颜色**：适应性极强，但搭配 **Minimalist Slate** 或 **Yacht Club** 显得非常高级。通常使用略微偏白或浅灰的背景，让白色分隔更加突出。
- **排版**：苹果风格（如 `SF Pro`、`Inter`）。标题通常加粗，置于每个分隔的左上角或左下角。
- **视觉**：经常依赖高质量的边到边图片，或在特定网格单元中放置单个大型 3D 图标，以打破文字密集型卡片。

## Web 实现
- CSS Grid 是必需的。Flexbox 难以维持严格的二维结构。
- **CSS 示例**：
```css
.bento-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 200px;
  gap: 24px;
  padding: 24px;
  background-color: var(--bg-primary); /* 比卡片稍深的颜色 */
}

.bento-card {
  background-color: #fff;
  border-radius: 32px; /* 非常大的圆角 */
  padding: 32px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.04);
  /* 可选：细微的 1px 边框增加清晰度 */
  border: 1px solid rgba(0,0,0,0.05);
  
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* 创建不同便当尺寸的跨格 */
.bento-span-2 { grid-column: span 2; }
.bento-span-2-row { grid-row: span 2; }
.bento-large { grid-column: span 2; grid-row: span 2; }
```

## App 实现

### SwiftUI
```swift
struct BentoGrid: View {
    let columns = [
        GridItem(.flexible(), spacing: 16),
        GridItem(.flexible(), spacing: 16)
    ]
    
    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 16) {
                // 2x1 跨格（满宽）
                BentoCard(title: "Hero", color: .blue)
                    .frame(height: 180)
                
                // 1x1 跨格
                BentoCard(title: "Stats", color: .green)
                    .frame(height: 180)
                BentoCard(title: "Graph", color: .purple)
                    .frame(height: 180)
                
                // 1x2 跨格（高）
                BentoCard(title: "Activity", color: .orange)
                    .frame(height: 376) // (180 * 2) + 16 间距
                
                // 高卡片旁边的 1x1 跨格
                VStack(spacing: 16) {
                    BentoCard(title: "A", color: .pink).frame(height: 180)
                    BentoCard(title: "B", color: .cyan).frame(height: 180)
                }
            }
            .padding(16)
        }
        .background(Color(.systemGroupedBackground))
    }
}

struct BentoCard: View {
    let title: String
    let color: Color
    var body: some View {
        RoundedRectangle(cornerRadius: 24)
            .fill(Color(.secondarySystemGroupedBackground))
            .overlay(
                Text(title).font(.headline).foregroundColor(color),
                alignment: .topLeading
            )
            .padding(16)
            // 柔和的便当阴影
            .shadow(color: .black.opacity(0.04), radius: 12, x: 0, y: 4)
    }
}
```
- 使用 `LazyVGrid` 处理均匀网格。
- 对于复杂的不规则便当布局（如 1x2 跨格），通常需要在网格单元格内混合使用 `VStack` 和 `HStack` 来模拟跨格。
- 严格保持 `cornerRadius`（通常 24-32pt）和 `spacing`（通常 16pt）的绝对一致性。

### Flutter
```dart
import 'package:flutter_staggered_grid_view/flutter_staggered_grid_view.dart';

class BentoScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: StaggeredGrid.count(
          crossAxisCount: 4, // 共 4 列
          mainAxisSpacing: 16,
          crossAxisSpacing: 16,
          children: const [
            // 2x1（在 2 列布局中占满宽度，跨 4）
            StaggeredGridTile.count(
              crossAxisCellCount: 4,
              mainAxisCellCount: 2,
              child: BentoCard(title: 'Hero'),
            ),
            // 1x1
            StaggeredGridTile.count(
              crossAxisCellCount: 2,
              mainAxisCellCount: 2,
              child: BentoCard(title: 'Stats'),
            ),
            // 1x1
            StaggeredGridTile.count(
              crossAxisCellCount: 2,
              mainAxisCellCount: 2,
              child: BentoCard(title: 'Graph'),
            ),
            // 1x2（高）
            StaggeredGridTile.count(
              crossAxisCellCount: 2,
              mainAxisCellCount: 4,
              child: BentoCard(title: 'Activity'),
            ),
          ],
        ),
      ),
    );
  }
}

class BentoCard extends StatelessWidget {
  final String title;
  const BentoCard({required this.title});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      alignment: Alignment.topLeft,
      child: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
    );
  }
}
```
- `flutter_staggered_grid_view` 包对于 Flutter 中复杂的便当网格几乎是必需的。
- 使用 `StaggeredGridTile.count` 显式声明每个分隔的 `crossAxis` 和 `mainAxis` 跨格。

### React Native
```jsx
const BentoScreen = () => {
  return (
    <ScrollView 
      style={{ flex: 1, backgroundColor: '#F2F2F7' }}
      contentContainerStyle={{ padding: 16 }}
    >
      {/* 2x1 跨格 */}
      <View style={[styles.bentoCard, { height: 180, marginBottom: 16 }]}>
        <Text style={styles.title}>Hero</Text>
      </View>

      <View style={{ flexDirection: 'row', gap: 16, marginBottom: 16 }}>
        {/* 1x1 跨格 */}
        <View style={[styles.bentoCard, { flex: 1, height: 180 }]}>
          <Text style={styles.title}>Stats</Text>
        </View>
        <View style={[styles.bentoCard, { flex: 1, height: 180 }]}>
          <Text style={styles.title}>Graph</Text>
        </View>
      </View>

      <View style={{ flexDirection: 'row', gap: 16 }}>
        {/* 1x2 跨格（高） */}
        <View style={[styles.bentoCard, { flex: 1, height: 376 }]}>
          <Text style={styles.title}>Activity</Text>
        </View>
        
        <View style={{ flex: 1, gap: 16 }}>
          {/* 堆叠的 1x1 */}
          <View style={[styles.bentoCard, { height: 180 }]}>
            <Text style={styles.title}>A</Text>
          </View>
          <View style={[styles.bentoCard, { height: 180 }]}>
            <Text style={styles.title}>B</Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  bentoCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 24,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.04,
    shadowRadius: 12,
    elevation: 2,
  },
  title: {
    fontWeight: '700',
    fontSize: 18,
  }
});
```
- React Native 没有 CSS Grid。必须使用 `flexDirection: 'row'` 和垂直堆叠手动组合网格。
- React Native flexbox 中的 `gap` 属性使这比使用 margin 简单得多。

### Jetpack Compose
```kotlin
@Composable
fun BentoGrid() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF2F2F7))
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // 满宽
        BentoCard(title = "Hero", modifier = Modifier.fillMaxWidth().height(180.dp))
        
        // 两列
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            BentoCard(title = "Stats", modifier = Modifier.weight(1f).height(180.dp))
            BentoCard(title = "Graph", modifier = Modifier.weight(1f).height(180.dp))
        }
        
        // 复杂跨格：左 1x2，右两个 1x1
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            BentoCard(title = "Activity", modifier = Modifier.weight(1f).height(376.dp))
            
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                BentoCard(title = "A", modifier = Modifier.fillMaxWidth().height(180.dp))
                BentoCard(title = "B", modifier = Modifier.fillMaxWidth().height(180.dp))
            }
        }
    }
}

@Composable
fun BentoCard(title: String, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Text(title, fontWeight = FontWeight.Bold, modifier = Modifier.padding(24.dp))
    }
}
```
- 虽然有 `LazyVerticalGrid`，但对于高度特定的不规则便当布局，使用 `weight(1f)` 手动构建行和列通常更可靠。
- 在 Column 和 Row 上都使用 `Arrangement.spacedBy(16.dp)`，确保间距数学上完全一致。

## 推荐与避免
- **推荐**：混合尺寸！如果每个单元格都是 1x1，便当盒会很乏味。使用 2x1、1x2 和 2x2 单元格来创造视觉趣味。
- **避免**：在便当卡内部塞满元素。如果需要很多元素，应拆分成多个卡片。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。