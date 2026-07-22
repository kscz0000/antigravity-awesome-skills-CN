---
name: neumorphism
description: Neumorphism（柔和 UI）的 Web 与 App 实现指南。当用户希望柔和阴影、挤压外观和单一光源模拟时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Neumorphism（柔和 UI）

> "元素从背景材料本身被挤压出来，由一个持续存在的单一光源塑形。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **统一的表面色**：背景和元素必须共享完全相同的基础色。
2. **双重阴影**：元素由两个阴影塑形：光源侧的浅色阴影（高光）和对面的深色阴影。
3. **没有边框**：形状完全由阴影定义。

## 视觉 DNA
- **颜色**：最适合中等调性的中性色。**Desert Mirage**、**Earth-Grounded Elegance** 或 **Sophisticated Neutral** 都是完美的。避免纯白或纯黑（阴影/高光不会显现）。
- **排版**：柔和、圆润的无衬线字体（如 `Nunito`、`Quicksand`）。
- **形状**：胶囊形、圆角矩形。锐角会破坏挤压材质的错觉。

## Web 实现
- 魔法完全在于 `box-shadow` 操控基础色的明暗变化。
- **CSS 示例**：
```css
:root {
  --base-color: #E6E2DD; /* 来自 Sophisticated Neutral */
  --highlight: #ffffff;
  --shadow: #c4c0bc;
}

body {
  background-color: var(--base-color);
}

.neu-element {
  background-color: var(--base-color);
  border-radius: 20px;
  /* 左上高光，右下阴影 */
  box-shadow:  9px 9px 18px var(--shadow),
              -9px -9px 18px var(--highlight);
  padding: 32px;
}

.neu-pressed {
  /* 按下/激活状态的内阴影 */
  border-radius: 20px;
  background: var(--base-color);
  box-shadow: inset 9px 9px 18px var(--shadow),
              inset -9px -9px 18px var(--highlight);
}
```

## App 实现

### SwiftUI
```swift
struct NeuCard: View {
    let baseColor = Color(red: 0.90, green: 0.89, blue: 0.87) // #E6E2DD
    
    var body: some View {
        VStack(spacing: 24) {
            Text("Neumorphic Card")
                .font(.system(size: 20, weight: .semibold, design: .rounded))
            
            Text("Extruded from the surface itself.")
                .font(.system(size: 15, design: .rounded))
                .foregroundColor(.secondary)
        }
        .padding(32)
        .background(baseColor)
        .cornerRadius(20)
        // 浅色阴影（左上）
        .shadow(color: Color.white.opacity(0.7), radius: 10, x: -8, y: -8)
        // 深色阴影（右下）
        .shadow(color: Color.black.opacity(0.15), radius: 10, x: 8, y: 8)
    }
}

// 按下 / 内嵌柔和按钮
struct NeuButton: View {
    @State private var isPressed = false
    let baseColor = Color(red: 0.90, green: 0.89, blue: 0.87)
    
    var body: some View {
        Button(action: {}) {
            Text("Press Me")
                .font(.system(size: 16, weight: .semibold, design: .rounded))
                .foregroundColor(.primary)
                .padding(.horizontal, 32)
                .padding(.vertical, 16)
        }
        .background(
            Group {
                if isPressed {
                    // 使用 ZStack/overlay 技巧实现内阴影效果
                    RoundedRectangle(cornerRadius: 16)
                        .fill(baseColor)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(baseColor, lineWidth: 4)
                                .shadow(color: Color.black.opacity(0.2), radius: 4, x: 4, y: 4)
                                .clipShape(RoundedRectangle(cornerRadius: 16))
                        )
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(baseColor, lineWidth: 4)
                                .shadow(color: Color.white.opacity(0.7), radius: 4, x: -4, y: -4)
                                .clipShape(RoundedRectangle(cornerRadius: 16))
                        )
                } else {
                    RoundedRectangle(cornerRadius: 16)
                        .fill(baseColor)
                        .shadow(color: Color.white.opacity(0.7), radius: 10, x: -8, y: -8)
                        .shadow(color: Color.black.opacity(0.15), radius: 10, x: 8, y: 8)
                }
            }
        )
        .buttonStyle(.plain)
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
    }
}
```
- 关键技巧：两个 `.shadow()` modifier —— 一个白色（左上），一个深色（右下）。
- 内阴影（按下状态）需要 ZStack/overlay 技巧，因为 SwiftUI 没有原生 `inset` 阴影。裁剪描边形状以模拟。
- 视图的背景色必须与父级背景完全一致。

### Flutter
```dart
class NeuCard extends StatelessWidget {
  final Color baseColor = const Color(0xFFE6E2DD);
  
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: baseColor,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          // 深色阴影（右下）
          BoxShadow(
            color: Colors.black.withOpacity(0.15),
            offset: const Offset(8, 8),
            blurRadius: 16,
          ),
          // 浅色阴影（左上）
          BoxShadow(
            color: Colors.white.withOpacity(0.7),
            offset: const Offset(-8, -8),
            blurRadius: 16,
          ),
        ],
      ),
      child: Column(
        children: [
          const Text('Neumorphic Card',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          Text('Extruded from the surface itself.',
            style: TextStyle(fontSize: 15, color: Colors.black54)),
        ],
      ),
    );
  }
}
```
- Flutter 的 `BoxShadow` **原生不支持**内阴影。
- 使用 `flutter_inset_box_shadow` 包，或用分层 `Stack` 伪造：在顶层放一个深色渐变 `Container`，下方放一个浅色渐变。
- 将 `Scaffold` 背景设置为**相同**的 `baseColor`，让元素看起来像被挤压出来。

### React Native
```jsx
const NeuCard = () => (
  <View style={{
    padding: 32,
    backgroundColor: '#E6E2DD',
    borderRadius: 20,
    // 浅色阴影（左上）— iOS 仅支持一个阴影
    shadowColor: '#FFFFFF',
    shadowOffset: { width: -8, height: -8 },
    shadowOpacity: 0.7,
    shadowRadius: 10,
    // Android — 使用 elevation 实现基础阴影
    elevation: 8,
  }}>
    <Text style={{ fontSize: 20, fontWeight: '600' }}>Neumorphic Card</Text>
    <Text style={{ fontSize: 15, color: '#888', marginTop: 16 }}>
      Extruded from the surface itself.
    </Text>
  </View>
);
```
- **重大限制**：React Native 每个 View 只支持一个阴影。真正的 Neumorphism 需要两个对立的阴影。
- **变通方案**：使用 `react-native-shadow-2` 或 `react-native-neomorph-shadows` 提供多阴影支持。
- 替代方案：包装两个嵌套的 `View`——外层有深色阴影，内层有浅色阴影。
- 按下状态的内阴影需要基于 SVG 的解决方案或预渲染图像。

### Jetpack Compose
```kotlin
@Composable
fun NeuCard() {
    val baseColor = Color(0xFFE6E2DD)
    
    Box(
        modifier = Modifier
            .padding(24.dp)
            .shadow(
                elevation = 8.dp,
                shape = RoundedCornerShape(20.dp),
                ambientColor = Color.Black.copy(alpha = 0.15f),
                spotColor = Color.Black.copy(alpha = 0.15f),
            )
            .background(baseColor, RoundedCornerShape(20.dp))
            .padding(32.dp)
    ) {
        Column {
            Text("Neumorphic Card",
                fontSize = 20.sp, fontWeight = FontWeight.SemiBold)
            Spacer(Modifier.height(16.dp))
            Text("Extruded from the surface itself.",
                fontSize = 15.sp, color = Color(0xFF888888))
        }
    }
}
```
- **Compose 限制**：与 React Native 一样，`Modifier.shadow()` 仅支持单一方向的阴影。
- 要实现真正的双重阴影 Neumorphism，使用自定义 `Modifier.drawBehind { }` 与 `drawIntoCanvas` 绘制两个独立的阴影路径（一浅一深）。
- `neumorphic-compose` 库提供预构建的 `Modifier.neumorphic()`，处理两种阴影。
- 将 `Scaffold` 背景设为相同 `baseColor` —— 这是不可妥协的。

## 推荐与避免
- **推荐**：对"激活"状态（如按下按钮或填写的表单字段）使用内阴影。
- **避免**：在没有辅助指示的情况下依赖 Neumorphism 表达关键元素。其固有的低对比度，如果使用不当，对可访问性是一场噩梦。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。