---
name: flat-design
description: Flat Design（扁平设计）风格的 Web 与 App 实现指南。当用户希望无阴影、简洁形状和大胆配色时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Flat Design

> "数字界面就应该看起来是数字的。拥抱二维平面。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **零深度**：完全没有投影、斜面、渐变或 3D 效果。一切都位于同一 Z 轴上。
2. **锐利简单的几何**：完美圆形、锐利矩形。无复杂有机形状。
3. **高对比纯色块**：依靠纯色块之间的强烈对比来划分空间。

## 视觉 DNA
- **颜色**：与 **Industrial Chic** 或 **Modern Editorial** 搭配良好。完全避免渐变。
- **排版**：强而高度可读的无衬线字体（如 `Roboto`、`Open Sans`）。保持中等至粗体字重。
- **图标**：单色、字形风格的图标，无复杂细节。

## Web 实现
- 完全依靠背景色和边框来构建结构。
- **CSS 示例**：
```css
.flat-card {
  background-color: var(--secondary-base);
  border: 2px solid var(--primary-text);
  border-radius: 0; /* 优先使用锐角 */
  padding: 32px;
  /* 没有 box-shadow */
}
.flat-btn {
  background-color: var(--cta-highlight);
  color: #fff;
  border: none;
  padding: 16px 32px;
  font-weight: 700;
  text-transform: uppercase;
  transition: opacity 0.2s;
}
.flat-btn:hover {
  opacity: 0.8; /* 悬停时仅改变不透明度或纯色背景，没有"抬起"效果 */
}
```

## App 实现

### SwiftUI
```swift
struct FlatCard: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Card Title")
                .font(.system(size: 18, weight: .bold))
            
            Text("Content without any depth effects.")
                .font(.system(size: 15))
                .foregroundColor(.secondary)
            
            Button(action: {}) {
                Text("ACTION")
                    .font(.system(size: 14, weight: .bold))
                    .foregroundColor(.white)
                    .padding(.horizontal, 24)
                    .padding(.vertical, 12)
                    .background(Color.blue)
                    // 没有圆角 — 锐利边缘
            }
        }
        .padding(24)
        .background(Color(.secondarySystemBackground))
        // 没有 .shadow() — 永远
        // 没有 .cornerRadius() — 锐利矩形
        .overlay(
            Rectangle().stroke(Color.primary.opacity(0.2), lineWidth: 1)
        )
    }
}
```
- 永远不要使用 `.shadow()` 或 `.cornerRadius()`。元素都是扁平矩形。
- 使用 `.overlay(Rectangle().stroke(...))` 作为可见边框，而非阴影来划分空间。
- 悬停/点击状态只能改变 `opacity` 或切换纯色背景。

### Flutter
```dart
class FlatCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        border: Border.all(color: Colors.black26, width: 1),
        // borderRadius: 无 — 锐利角
        // boxShadow: 无 — 零深度
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Card Title',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          const Text('Content without any depth effects.',
            style: TextStyle(fontSize: 15, color: Colors.black54)),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () {},
            style: ElevatedButton.styleFrom(
              elevation: 0,           // 关键：无阴影
              backgroundColor: Colors.blue,
              foregroundColor: Colors.white,
              shape: const RoundedRectangleBorder(
                borderRadius: BorderRadius.zero, // 锐利角
              ),
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            ),
            child: const Text('ACTION',
              style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1)),
          ),
        ],
      ),
    );
  }
}
```
- 全局覆盖 `ThemeData` 来消除所有凸起：
  ```dart
  ThemeData(
    cardTheme: const CardTheme(elevation: 0, shape: RoundedRectangleBorder()),
    appBarTheme: const AppBarTheme(elevation: 0),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(elevation: 0),
  )
  ```
- 使用 `Container` 配合 `BoxDecoration` 而不是 `Card` 组件，避免默认凸起。

### React Native
```jsx
const FlatCard = () => (
  <View style={{
    padding: 24,
    backgroundColor: '#F0F0F0',
    borderWidth: 1,
    borderColor: '#CCCCCC',
    // 没有 borderRadius
    // 没有 elevation 或 shadow 属性
  }}>
    <Text style={{ fontSize: 18, fontWeight: '700', marginBottom: 16 }}>
      Card Title
    </Text>
    <Text style={{ fontSize: 15, color: '#666', marginBottom: 16 }}>
      Content without any depth effects.
    </Text>
    <TouchableOpacity
      style={{
        backgroundColor: '#2196F3',
        paddingHorizontal: 24,
        paddingVertical: 12,
        alignSelf: 'flex-start',
        // 没有 borderRadius，没有 elevation
      }}
      activeOpacity={0.7}
    >
      <Text style={{ color: '#FFF', fontWeight: '700', letterSpacing: 1 }}>
        ACTION
      </Text>
    </TouchableOpacity>
  </View>
);
```
- 显式设置 `elevation: 0` 并删除所有阴影属性（`shadowColor`、`shadowOffset` 等）。
- 如果使用 React Native Paper，覆盖主题：`const theme = { ...DefaultTheme, roundness: 0, }`。
- 点击反馈应直接改变 `backgroundColor`，而不是添加光晕或抬起。

### Jetpack Compose
```kotlin
@Composable
fun FlatCard() {
    Column(
        modifier = Modifier
            .background(Color(0xFFF0F0F0))
            .border(1.dp, Color(0xFFCCCCCC))
            .padding(24.dp)
    ) {
        Text("Card Title", fontSize = 18.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(16.dp))
        Text("Content without any depth effects.",
            fontSize = 15.sp, color = Color(0xFF666666))
        Spacer(Modifier.height(16.dp))
        Button(
            onClick = {},
            shape = RectangleShape,  // 锐利角
            elevation = ButtonDefaults.buttonElevation(
                defaultElevation = 0.dp,  // 无阴影
                pressedElevation = 0.dp,
            ),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2196F3)),
            contentPadding = PaddingValues(horizontal = 24.dp, vertical = 12.dp),
        ) {
            Text("ACTION", fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
        }
    }
}
```
- 覆盖 `MaterialTheme` 形状：`shapes = Shapes(small = RectangleShape, medium = RectangleShape, large = RectangleShape)`。
- 将所有 `Card`、`TopAppBar` 和 `FloatingActionButton` 的 elevation 设为 `0.dp`。
- 使用 `Modifier.border()` 替代 elevation 来分隔 UI 区域。

## 推荐与避免
- **推荐**：使用纯色、对比鲜明的边框来分隔重叠元素。
- **避免**：使用任何透明度（rgba）或模糊效果。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。