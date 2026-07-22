---
name: monochromatic-ui
description: Monochromatic UI 的 Web 与 App 实现指南。当用户希望单色调色板、高雅和严格的色彩纪律时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Monochromatic UI

> "通过克制实现优雅。单一色调，通过其所有色阶、色调和阴影来探索。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **单一色调**：选择一种基础色（例如深蓝）。整个 UI 都使用该色调的较浅（色阶）和较深（阴影）版本构建。
2. **高对比度以保证可读性**：最深阴影和最浅色阶必须具备足够的对比度，以通过无障碍标准。
3. **纹理替代颜色**：由于颜色受限，使用微妙的纹理、图案或变化的不透明度来区分区块。

## 视觉 DNA
- **颜色**：**Monochromatic Brown** 或从 **Earth-Grounded Elegance** 中选取一种主导色调并演绎。
- **排版**：干净、不抢眼。由于不能用颜色区分，布局重度依赖字重来建立层级。
- **阴影**：阴影必须带有基础色调，绝不能是纯黑色。

## Web 实现
- 在 CSS 中大量使用 HSL（色相、饱和度、亮度），让构建调色板变得简单。
- **CSS 示例**：
```css
:root {
  /* 基础色：深蓝 (210) */
  --mono-900: hsl(210, 80%, 10%); /* 极深 */
  --mono-700: hsl(210, 70%, 30%); /* 深 */
  --mono-500: hsl(210, 60%, 50%); /* 基础 */
  --mono-300: hsl(210, 50%, 80%); /* 浅 */
  --mono-100: hsl(210, 40%, 95%); /* 极浅背景 */
}

body {
  background-color: var(--mono-100);
  color: var(--mono-900);
  font-family: 'Inter', sans-serif;
}

.mono-card {
  background-color: #ffffff; /* 或 mono-100 */
  border: 1px solid var(--mono-300);
  border-radius: 8px;
  padding: 32px;
  /* 带色调的阴影 */
  box-shadow: 0 10px 25px hsla(210, 80%, 10%, 0.05);
}

.mono-btn {
  background-color: var(--mono-500);
  color: #ffffff;
  border: none;
  border-radius: 4px;
  padding: 12px 24px;
  transition: background-color 0.2s;
}

.mono-btn:hover {
  background-color: var(--mono-700);
}

.mono-subtext {
  color: var(--mono-500); /* 使用中间色调作为次要文字 */
  font-weight: 500;
}
```

## App 实现

### SwiftUI
```swift
struct MonochromaticView: View {
    // 基础色：深蓝 (HSB/HSL 中 210)
    // SwiftUI 中 hue 是 0.0 到 1.0（210/360 = 0.58）
    let mono900 = Color(hue: 0.58, saturation: 0.80, brightness: 0.10)
    let mono700 = Color(hue: 0.58, saturation: 0.70, brightness: 0.30)
    let mono500 = Color(hue: 0.58, saturation: 0.60, brightness: 0.50)
    let mono300 = Color(hue: 0.58, saturation: 0.50, brightness: 0.80)
    let mono100 = Color(hue: 0.58, saturation: 0.40, brightness: 0.95)
    
    var body: some View {
        VStack(spacing: 24) {
            // 卡片
            VStack(alignment: .leading, spacing: 12) {
                Text("Monochromatic Elegance")
                    .font(.title2).fontWeight(.semibold)
                    .foregroundColor(mono900)
                
                Text("Using only variations in saturation and brightness of a single hue.")
                    .foregroundColor(mono500)
            }
            .padding(32)
            .background(Color.white)
            .border(mono300, width: 1)
            .shadow(color: mono900.opacity(0.1), radius: 15, y: 5) // 带色调的阴影
            
            // 按钮
            Button(action: {}) {
                Text("Primary Action")
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(mono500)
                    .cornerRadius(8)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(mono100)
    }
}
```
- 使用 `Color(hue: saturation: brightness:)` 定义颜色。这能确保数学上完美的单色和谐。
- *始终*使用 `mono900` 为你的投影着色。纯黑阴影在严格的单色 UI 中看起来脏。

### Flutter
```dart
class MonochromaticScreen extends StatelessWidget {
  // 基础色：深蓝 (210)
  // Flutter HSVColor 使用 Hue 0-360，Saturation 0.0-1.0，Value 0.0-1.0
  final Color mono900 = const HSVColor.fromAHSV(1.0, 210, 0.80, 0.10).toColor();
  final Color mono500 = const HSVColor.fromAHSV(1.0, 210, 0.60, 0.50).toColor();
  final Color mono300 = const HSVColor.fromAHSV(1.0, 210, 0.50, 0.80).toColor();
  final Color mono100 = const HSVColor.fromAHSV(1.0, 210, 0.40, 0.95).toColor();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: mono100,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // 卡片
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(32),
                decoration: BoxDecoration(
                  color: Colors.white,
                  border: Border.all(color: mono300),
                  borderRadius: BorderRadius.circular(8),
                  boxShadow: [
                    BoxShadow(color: mono900.withOpacity(0.1), blurRadius: 15, offset: const Offset(0, 5))
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Monochromatic', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w600, color: mono900)),
                    const SizedBox(height: 12),
                    Text('Variations of a single hue.', style: TextStyle(fontSize: 16, color: mono500)),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              // 按钮
              ElevatedButton(
                onPressed: () {},
                style: ElevatedButton.styleFrom(
                  backgroundColor: mono500,
                  foregroundColor: Colors.white,
                  minimumSize: const Size(double.infinity, 56),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  elevation: 0,
                ),
                child: const Text('Primary Action', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```
- Flutter 的 `HSVColor.fromAHSV()` 是在没有猜测十六进制代码的情况下明确编码单色调色板的最佳方法。

### React Native
```jsx
// 基础色：深蓝 (210)
const theme = {
  mono900: 'hsl(210, 80%, 10%)',
  mono700: 'hsl(210, 70%, 30%)',
  mono500: 'hsl(210, 60%, 50%)',
  mono300: 'hsl(210, 50%, 80%)',
  mono100: 'hsl(210, 40%, 95%)',
};

const MonochromaticScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: theme.mono100, padding: 24, justifyContent: 'center' }}>
      
      <View style={{
        backgroundColor: '#FFFFFF',
        borderColor: theme.mono300,
        borderWidth: 1,
        borderRadius: 8,
        padding: 32,
        marginBottom: 24,
        // 带色调的阴影（iOS）
        shadowColor: theme.mono900, shadowOffset: { width: 0, height: 5 },
        shadowOpacity: 0.1, shadowRadius: 15,
      }}>
        <Text style={{ fontSize: 24, fontWeight: '600', color: theme.mono900, marginBottom: 12 }}>
          Monochromatic
        </Text>
        <Text style={{ fontSize: 16, color: theme.mono500 }}>
          Using HSL strings in React Native makes palette generation trivial.
        </Text>
      </View>

      <TouchableOpacity style={{
        backgroundColor: theme.mono500,
        padding: 16,
        borderRadius: 8,
        alignItems: 'center'
      }}>
        <Text style={{ fontWeight: 'bold', color: '#FFFFFF', fontSize: 16 }}>
          Primary Action
        </Text>
      </TouchableOpacity>
      
    </View>
  );
};
```
- React Native 的 StyleSheet 原生接受 CSS `hsl()` 字符串。使用它们！比起十六进制代码，让单色调色板的调试和调整容易一百万倍。

### Jetpack Compose
```kotlin
@Composable
fun MonochromaticScreen() {
    // 基础色：深蓝 (210)
    // Compose Color.hsv 需要 Hue 0-360f，Saturation 0-1f，Value 0-1f
    val mono900 = Color.hsv(210f, 0.80f, 0.10f)
    val mono500 = Color.hsv(210f, 0.60f, 0.50f)
    val mono300 = Color.hsv(210f, 0.50f, 0.80f)
    val mono100 = Color.hsv(210f, 0.40f, 0.95f)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(mono100)
            .padding(24.dp),
        verticalArrangement = Arrangement.Center
    ) {
        // 卡片
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .shadow(15.dp, RoundedCornerShape(8.dp), spotColor = mono900.copy(alpha = 0.2f))
                .background(Color.White, RoundedCornerShape(8.dp))
                .border(1.dp, mono300, RoundedCornerShape(8.dp))
                .padding(32.dp)
        ) {
            Column {
                Text("Monochromatic", fontSize = 24.sp, fontWeight = FontWeight.SemiBold, color = mono900)
                Spacer(Modifier.height(12.dp))
                Text("Strictly enforced hue discipline.", color = mono500)
            }
        }
        
        Spacer(Modifier.height(24.dp))
        
        // 按钮
        Button(
            onClick = { },
            colors = ButtonDefaults.buttonColors(containerColor = mono500, contentColor = Color.White),
            shape = RoundedCornerShape(8.dp),
            modifier = Modifier.fillMaxWidth().height(56.dp)
        ) {
            Text("Primary Action", fontWeight = FontWeight.Bold)
        }
    }
}
```
- 使用 `Color.hsv()` 定义调色板。
- 将 `Modifier.shadow` 中的 `spotColor` 设为 `mono900`，让阴影不会显得浑浊或脱离设计系统。

## 推荐与避免
- **推荐**：必要时使用纯白或纯黑作为绝对极值以保证文字可读性。
- **避免**：偷偷加入强调色。如果你在蓝色单色 UI 上加了红色错误按钮，它会立刻破坏美学并变成"双色"或标准 UI。设法用粗体文字或基础色调的暗色来表达错误。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。