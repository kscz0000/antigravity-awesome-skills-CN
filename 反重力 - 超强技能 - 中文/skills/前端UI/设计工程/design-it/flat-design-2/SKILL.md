---
name: flat-design-2
description: Flat Design 2.0（半扁平）的 Web 与 App 实现指南。当用户希望扁平设计带有微妙阴影和改进的可用性时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Flat Design 2.0（半扁平）

> "扁平美学，但带有微妙的物理暗示来传达可交互性。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **大体扁平**：主要美学保持 2D 和纯色。
2. **微妙凸起**：仅使用极柔和、弥散的阴影来指示可交互元素（按钮、浮动操作按钮）或分层（模态框）。
3. **微渐变**：偶尔使用几乎察觉不到的线性渐变，防止大表面感觉死板。

## 视觉 DNA
- **颜色**：与 **Warm Tech** 或 **Earth-Grounded Elegance** 搭配良好。
- **排版**：干净、可读的无衬线字体。
- **阴影**：阴影必须低不透明度、高模糊度，并通常带背景色调而非纯黑色。

## Web 实现
- **CSS 示例**：
```css
:root {
  --shadow-color: rgba(43, 48, 58, 0.08); /* 带色调的阴影 */
}

.flat2-card {
  background-color: var(--bg-primary);
  border-radius: 8px;
  padding: 32px;
  /* 极柔和、弥散的阴影 */
  box-shadow: 0 10px 30px var(--shadow-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.flat2-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(43, 48, 58, 0.12);
}

.flat2-btn {
  background: var(--cta-highlight);
  border-radius: 4px;
  padding: 12px 24px;
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
```

## App 实现

### SwiftUI
```swift
struct SemiFlatCard: View {
    @State private var isPressed = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Semi-Flat Card")
                .font(.system(size: 18, weight: .semibold))
            Text("Flat aesthetic with just enough depth to hint at interactivity.")
                .font(.system(size: 15))
                .foregroundColor(.secondary)
        }
        .padding(24)
        .background(Color(.systemBackground))
        .cornerRadius(8)
        // 关键：非常柔和、带色调的阴影 — 不是生硬的黑色
        .shadow(color: Color.black.opacity(0.06), radius: 12, x: 0, y: 4)
        .scaleEffect(isPressed ? 0.98 : 1.0)
        .animation(.easeOut(duration: 0.2), value: isPressed)
        .onLongPressGesture(minimumDuration: .infinity, pressing: { pressing in
            isPressed = pressing
        }, perform: {})
    }
}

struct SemiFlatButton: View {
    var body: some View {
        Button(action: {}) {
            Text("Continue")
                .font(.system(size: 15, weight: .semibold))
                .foregroundColor(.white)
                .padding(.horizontal, 24)
                .padding(.vertical, 12)
                .background(Color.accentColor)
                .cornerRadius(4)
                // 微妙的按钮阴影
                .shadow(color: Color.accentColor.opacity(0.25), radius: 8, x: 0, y: 4)
        }
        .buttonStyle(.plain)
    }
}
```
- 阴影颜色应当带有色调（例如 `Color.accentColor.opacity(0.15)`），而非纯黑色。
- 使用 `radius: 10...16` 配合 `opacity: 0.05...0.08` — 如果你立刻就能看见阴影，那它就太重了。
- 在按下时添加微妙的 `scaleEffect`，以暗示物理反馈。

### Flutter
```dart
class SemiFlatCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        // 极柔和、带色调的阴影
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF2B303A).withOpacity(0.08),
            blurRadius: 24,
            offset: const Offset(0, 8),
            spreadRadius: 0,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Semi-Flat Card',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          const Text('Flat aesthetic with just enough depth to hint at interactivity.',
            style: TextStyle(fontSize: 15, color: Colors.black54)),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () {},
            style: ElevatedButton.styleFrom(
              elevation: 2,  // 非常低 — 刚好足以感觉可点击
              shadowColor: Theme.of(context).primaryColor.withOpacity(0.3),
              backgroundColor: Theme.of(context).primaryColor,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            ),
            child: const Text('Continue', style: TextStyle(fontWeight: FontWeight.w600)),
          ),
        ],
      ),
    );
  }
}
```
- 使用 `elevation: 1` 到 `elevation: 4`，最高不要超过 `elevation: 6`。
- 将 `shadowColor` 着色，与卡片背景或品牌色一致。
- 使用 `InkWell` 实现水波纹效果，并对按下添加微妙的 `Transform.translate` 动画。

### React Native
```jsx
const SemiFlatCard = () => (
  <View style={{
    padding: 24,
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
    // 极柔和、弥散的阴影
    shadowColor: '#2B303A',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.08,
    shadowRadius: 24,
    // Android
    elevation: 3,
  }}>
    <Text style={{ fontSize: 18, fontWeight: '600', marginBottom: 16 }}>
      Semi-Flat Card
    </Text>
    <Text style={{ fontSize: 15, color: '#666', marginBottom: 20 }}>
      Flat aesthetic with just enough depth to hint at interactivity.
    </Text>
    <Pressable
      style={({ pressed }) => ({
        backgroundColor: '#4A90D9',
        paddingHorizontal: 24,
        paddingVertical: 12,
        borderRadius: 4,
        alignSelf: 'flex-start',
        transform: [{ scale: pressed ? 0.97 : 1 }],
        shadowColor: '#4A90D9',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.25,
        shadowRadius: 8,
      })}
    >
      <Text style={{ color: '#FFF', fontWeight: '600' }}>Continue</Text>
    </Pressable>
  </View>
);
```
- 在 iOS 上使用 `shadowOpacity: 0.05...0.10` 配合 `shadowRadius: 16...24` 获得弥散效果。
- 在 Android 上，`elevation: 2...4` 等效。避免超过 `elevation: 6`。
- 使用 `Pressable` 与 `({ pressed })` 样式回调实现动画的按下状态。

### Jetpack Compose
```kotlin
@Composable
fun SemiFlatCard() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
    ) {
        Column(modifier = Modifier.padding(24.dp)) {
            Text("Semi-Flat Card", fontSize = 18.sp, fontWeight = FontWeight.SemiBold)
            Spacer(Modifier.height(16.dp))
            Text("Flat aesthetic with just enough depth to hint at interactivity.",
                fontSize = 15.sp, color = Color(0xFF666666))
            Spacer(Modifier.height(20.dp))
            Button(
                onClick = {},
                shape = RoundedCornerShape(4.dp),
                elevation = ButtonDefaults.buttonElevation(defaultElevation = 2.dp),
                contentPadding = PaddingValues(horizontal = 24.dp, vertical = 12.dp),
            ) {
                Text("Continue", fontWeight = FontWeight.SemiBold)
            }
        }
    }
}
```
- 使用 `CardDefaults.cardElevation(defaultElevation = 2.dp)` — 保持在 4dp 以下。
- 悬停/按下时：`hoveredElevation = 4.dp, pressedElevation = 1.dp` 以提供微妙的物理感。
- 通过 `Modifier.shadow(elevation, shape, ambientColor, spotColor)` 使用自定义着色阴影。

## 推荐与避免
- **推荐**：保持阴影极其微妙。如果你立刻就能注意到阴影，那它就太暗了。
- **避免**：使用内阴影、重渐变或拟物纹理。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。