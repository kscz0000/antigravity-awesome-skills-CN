---
name: material-design
description: Material Design 的 Web 与 App 实现指南。当用户希望 Google 美学、层次、运动和一致组件时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Material Design

> "数字纸张与墨水。基于堆叠材料的物理属性构建的界面。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **Z 轴层次**：一切都存在于特定的层上。阴影传达层级和状态。
2. **有意义的运动**：动画是连续的，引导用户的焦点从一个状态到下一个（例如涟漪效果、共享元素转场）。
3. **结构化布局**：严格遵守 8dp 基线网格和特定组件解剖（卡片、FAB、应用栏）。

## 视觉 DNA
- **颜色**：与 **Desert Mirage** 或 **Minimalist Slate** 搭配出色。利用主色、次色、表面和错误语义的映射。
- **排版**：`Roboto` 或 `Google Sans`（或等效的干净几何无衬线）。严格遵守 Material 类型等级（H1-H6、副标题、正文、说明、标签）。
- **形状**：中等圆角（4px 到 16px）。

## Web 实现
- 不要重新发明轮子：模仿标准 Material 层次。
- **CSS 示例**：
```css
.material-card {
  background: var(--bg-surface);
  border-radius: 8px;
  padding: 16px;
  /* Material Elevation 2 */
  box-shadow: 0 3px 1px -2px rgba(0,0,0,0.2), 
              0 2px 2px 0 rgba(0,0,0,0.14), 
              0 1px 5px 0 rgba(0,0,0,0.12);
  transition: box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1);
}

.material-btn {
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 1.25px;
  padding: 0 16px;
  height: 36px;
  border-radius: 4px;
  background: var(--cta-highlight);
  color: #fff;
  border: none;
  /* 涟漪效果通常由 JS 处理，但结构是关键 */
}
```

## App 实现

### SwiftUI
```swift
struct MaterialCard: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Material Card")
                .font(.system(size: 20, weight: .medium))
            Text("Digital paper and ink. Shadows communicate where this surface sits.")
                .font(.system(size: 14))
                .foregroundColor(.secondary)
            HStack {
                Spacer()
                Button("ACTION") {}
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(.accentColor)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
            }
        }
        .padding(16)
        .background(Color(.systemBackground))
        .cornerRadius(8)
        // Material Elevation 2 等效
        .shadow(color: Color.black.opacity(0.12), radius: 3, x: 0, y: 1)
        .shadow(color: Color.black.opacity(0.08), radius: 2, x: 0, y: 2)
    }
}

// Material FAB
struct MaterialFAB: View {
    var body: some View {
        Button(action: {}) {
            Image(systemName: "plus")
                .font(.system(size: 24))
                .foregroundColor(.white)
                .frame(width: 56, height: 56)
                .background(Color.accentColor)
                .cornerRadius(16)
                .shadow(color: Color.black.opacity(0.2), radius: 6, x: 0, y: 3)
                .shadow(color: Color.black.opacity(0.14), radius: 4, x: 0, y: 2)
        }
    }
}
```
- 通过堆叠不同模糊/偏移值的多个 `.shadow()` modifier 来模拟 Material 层次。
- 使用 `.cornerRadius(8...16)` — Material Design 3 的形状比 M2 更圆润。
- 使用 `.animation(.easeInOut(duration: 0.28))` 对阴影变化进行动画 — Material 使用 280ms 过渡。

### Flutter
```dart
// Flutter 本身就是 Material Design — 直接原生使用
class MaterialScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: const Color(0xFF6750A4), // Material You 种子色
        // 在此映射你的通用调色板
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Material Design'),
          // M3 appbar elevation 默认 0，滚动时为 3
        ),
        body: Padding(
          padding: const EdgeInsets.all(16),
          child: Card(
            elevation: 2,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('Material Card',
                    style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 8),
                  Text('Digital paper and ink.',
                    style: Theme.of(context).textTheme.bodyMedium),
                  const SizedBox(height: 16),
                  Align(
                    alignment: Alignment.centerRight,
                    child: TextButton(
                      onPressed: () {},
                      child: const Text('ACTION'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () {},
          child: const Icon(Icons.add),
          // M3 FAB 自动获得正确的 elevation 和 shape
        ),
      ),
    );
  }
}
```
- **Flutter 是 Material Design 的原生栖息地。** 使用 `MaterialApp`、`ThemeData(useMaterial3: true)` 和标准组件。
- 通过 `colorSchemeSeed` 映射通用调色板，或手动构建 `ColorScheme`。
- 通过 `Theme.of(context).textTheme` 使用 Material 类型等级。
- 涟漪效果由 `InkWell` 和 `ElevatedButton` 免费提供。

### React Native
```jsx
import { Provider as PaperProvider, Card, Button, Title, Paragraph } from 'react-native-paper';

const materialTheme = {
  ...DefaultTheme,
  roundness: 8,
  colors: {
    ...DefaultTheme.colors,
    primary: '#6750A4',    // Material You 紫色
    surface: '#FFFBFE',
    background: '#FFFBFE',
  },
};

const MaterialScreen = () => (
  <PaperProvider theme={materialTheme}>
    <ScrollView style={{ flex: 1, padding: 16 }}>
      <Card style={{ marginBottom: 16 }} elevation={2}>
        <Card.Content>
          <Title>Material Card</Title>
          <Paragraph>Digital paper and ink. Shadows communicate hierarchy.</Paragraph>
        </Card.Content>
        <Card.Actions>
          <Button mode="text" onPress={() => {}}>ACTION</Button>
        </Card.Actions>
      </Card>

      {/* Filled button — Material M3 风格 */}
      <Button
        mode="contained"
        onPress={() => {}}
        style={{ alignSelf: 'flex-start', borderRadius: 20 }}
        labelStyle={{ fontWeight: '500', letterSpacing: 1.25 }}
      >
        Filled Button
      </Button>
    </ScrollView>
  </PaperProvider>
);
```
- 使用 `react-native-paper` — 它为 React Native 原生实现了 Material Design 3。
- 配置主题以将你的通用调色板映射到 Material 语义色。
- 使用 `Card`（配合 `elevation` prop）、`Button`（配合 `mode` prop）和 `TextInput` 以获得正确的 Material 行为。
- Android 上的涟漪效果通过 `Pressable` 免费提供；在 iOS 上，使用 `react-native-paper` 的 `TouchableRipple`。

### Jetpack Compose
```kotlin
// Jetpack Compose 本身就是 Material Design — 直接原生使用
@Composable
fun MaterialScreen() {
    MaterialTheme(
        colorScheme = lightColorScheme(
            primary = Color(0xFF6750A4),
            onPrimary = Color.White,
            surface = Color(0xFFFFFBFE),
        ),
        typography = Typography(
            titleLarge = TextStyle(fontSize = 22.sp, fontWeight = FontWeight.Medium),
            bodyMedium = TextStyle(fontSize = 14.sp, lineHeight = 20.sp),
        ),
    ) {
        Scaffold(
            topBar = {
                TopAppBar(title = { Text("Material Design") })
            },
            floatingActionButton = {
                FloatingActionButton(onClick = {}) {
                    Icon(Icons.Default.Add, contentDescription = "Add")
                }
            },
        ) { padding ->
            Column(modifier = Modifier.padding(padding).padding(16.dp)) {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                    shape = RoundedCornerShape(12.dp),
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Material Card",
                            style = MaterialTheme.typography.titleLarge)
                        Spacer(Modifier.height(8.dp))
                        Text("Digital paper and ink.",
                            style = MaterialTheme.typography.bodyMedium)
                        Spacer(Modifier.height(16.dp))
                        TextButton(
                            onClick = {},
                            modifier = Modifier.align(Alignment.End),
                        ) { Text("ACTION") }
                    }
                }
            }
        }
    }
}
```
- **Jetpack Compose 就是 Material Design。** 直接使用 `MaterialTheme`、`Card`、`Scaffold`、`TopAppBar` 和 `FloatingActionButton`。
- 将通用调色板映射到 `lightColorScheme()` 或 `darkColorScheme()`。
- 使用 `MaterialTheme.typography` 获取完整类型等级。
- 动画使用 `animateFloatAsState` 配合 Material 缓动：`FastOutSlowInEasing`（等价于 `cubic-bezier(0.4, 0.0, 0.2, 1)`）。

## 推荐与避免
- **推荐**：使用标准 Material 缓动曲线（`cubic-bezier(0.4, 0.0, 0.2, 1)`）进行动画。
- **避免**：随意混用重叠的阴影。元素应该清晰地"位于"其他元素之上或之下。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。