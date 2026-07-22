---
name: brutalism
description: Brutalism 的 Web 与 App 实现指南。当用户需要粗犷外观、故意未完成的感觉，以及对标准设计惯例的反叛时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Brutalism

> "原始材料裸露在外。刻意拒绝润色、渐变和柔和阴影。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **未经修饰的组件**：浏览器对按钮、输入框和链接的默认样式被加以彰显。
2. **裸露的结构**：使用网格线、带可见边框的表格和生硬的边界来代替空白分隔内容。
3. **反美学**：刻意的笨拙感。元素可能以一种"坏掉"的方式轻微重叠，或使用系统默认字体。

## 视觉 DNA
- **颜色**：高对比度，经常相互冲突。链接使用纯 `#0000FF` 蓝色、强调使用 `#FF0000` 红色，背景为刺眼的白色或 `#C0C0C0` 灰色。**Industrial Chic** 调色板最为契合。
- **排版**：Courier New、Times New Roman、Comic Sans 或默认无衬线字体。不使用 Web 字体。
- **视觉**：抖动图像、像素化图形或重度压缩的 jpeg。

## Web 实现
- 尽可能使用标准 HTML 标签，不覆盖其默认外观。
- **CSS 示例**：
```css
body {
  background-color: #ffffff;
  color: #000000;
  font-family: monospace;
}

/* 暴露结构 */
.brutalist-container {
  border: 1px solid #000;
  padding: 10px;
}

.brutalist-section {
  border-bottom: 2px dashed #000;
  margin-bottom: 20px;
  padding-bottom: 20px;
}

/* 默认外观但超大的按钮 */
.brutalist-btn {
  background-color: #c0c0c0;
  border: 2px outset #ffffff;
  border-right-color: #000000;
  border-bottom-color: #000000;
  color: #000000;
  font-family: sans-serif;
  font-size: 24px;
  padding: 10px 20px;
  cursor: pointer;
}

.brutalist-btn:active {
  border-style: inset;
}

/* 系统链接蓝色 */
a {
  color: #0000FF;
  text-decoration: underline;
}
```

## App 实现

### SwiftUI
```swift
struct BrutalistView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text("BRUTALISM")
                .font(.custom("Courier New", size: 32))
                .foregroundColor(.black)
                .padding(10)
                .border(Color.black, width: 2)
            
            Divider().background(Color.black).padding(.vertical, 20)
            
            Button(action: {}) {
                Text("CLICK_HERE")
                    .font(.custom("Courier New", size: 24))
                    .foregroundColor(.blue)
                    .underline()
            }
            .padding(10)
            
            // 原始结构容器
            VStack(alignment: .leading) {
                Text("System Status: RAW").font(.custom("Courier New", size: 14))
            }
            .padding()
            .border(Color.black, width: 1)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        .background(Color.white)
    }
}
```
- 避免使用任何原生 `ButtonStyle` 组件。使用带 `.underline()` 映射系统蓝色的 `Text`。
- 使用 `.border(Color.black, width: 1)` 代替背景或阴影。
- 强制使用 Courier New 或 Menlo 等等宽字体。

### Flutter
```dart
class BrutalistScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // 尽量不要使用 MaterialApp theme 或 Scaffold，
    // 或将其彻底剥离
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.black, width: 2),
                ),
                child: const Text(
                  'BRUTALISM',
                  style: TextStyle(
                    fontFamily: 'Courier',
                    fontSize: 32,
                    color: Colors.black,
                  ),
                ),
              ),
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 20),
                child: Divider(color: Colors.black, thickness: 2),
              ),
              GestureDetector(
                onTap: () {},
                child: const Text(
                  'CLICK_HERE',
                  style: TextStyle(
                    fontFamily: 'Courier',
                    fontSize: 24,
                    color: Colors.blue,
                    decoration: TextDecoration.underline,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```
- 避免使用 `ElevatedButton`、`Card` 或 `AppBar`。
- 使用带 `Border.all(color: Colors.black)` 的原始 `Container` 和 `Text` 组件构建 UI。
- 使用 `TextDecoration.underline` 表示可交互。

### React Native
```jsx
const BrutalistScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#FFFFFF', padding: 16 }}>
      <View style={{
        borderWidth: 2,
        borderColor: '#000000',
        padding: 10,
        alignSelf: 'flex-start'
      }}>
        <Text style={{ fontFamily: 'monospace', fontSize: 32, color: '#000' }}>
          BRUTALISM
        </Text>
      </View>
      
      <View style={{ height: 2, backgroundColor: '#000', marginVertical: 20 }} />
      
      <TouchableOpacity activeOpacity={1}>
        <Text style={{
          fontFamily: 'monospace',
          fontSize: 24,
          color: '#0000FF',
          textDecorationLine: 'underline'
        }}>
          CLICK_HERE
        </Text>
      </TouchableOpacity>

      <View style={{
        borderWidth: 1,
        borderColor: '#000',
        padding: 16,
        marginTop: 40
      }}>
        <Text style={{ fontFamily: 'monospace', color: '#000' }}>
          System Status: RAW
        </Text>
      </View>
    </View>
  );
};
```
- 剥离所有原生触感。不要使用 `react-native-elements` 或 `react-native-paper`。
- 在 `TouchableOpacity` 上设置 `activeOpacity={1}`，使点击时没有平滑的淡出效果——瞬间切换。
- 使用纯十六进制颜色：`#FFFFFF`、`#000000`、`#0000FF`。

### Jetpack Compose
```kotlin
@Composable
fun BrutalistScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
            .padding(16.dp)
    ) {
        Box(
            modifier = Modifier
                .border(2.dp, Color.Black)
                .padding(10.dp)
        ) {
            BasicText(
                text = "BRUTALISM",
                style = TextStyle(
                    fontFamily = FontFamily.Monospace,
                    fontSize = 32.sp,
                    color = Color.Black
                )
            )
        }
        
        Spacer(Modifier.height(20.dp))
        Box(modifier = Modifier.fillMaxWidth().height(2.dp).background(Color.Black))
        Spacer(Modifier.height(20.dp))
        
        BasicText(
            text = "CLICK_HERE",
            modifier = Modifier.clickable { },
            style = TextStyle(
                fontFamily = FontFamily.Monospace,
                fontSize = 24.sp,
                color = Color.Blue,
                textDecoration = TextDecoration.Underline
            )
        )
    }
}
```
- 使用 `BasicText` 替代 `Text`，绕过 Material 主题默认值。
- 使用带 `.background(Color.Black)` 的 `Box` 构建结构线。
- **不要**使用 `Button`、`Card` 或任何 Material 组合函数。仅使用原始布局。

## 推荐与避免
- **推荐**：在所有元素周围使用生硬的高对比度边框（1px 纯黑色实线）。
- **避免**：使用圆角、投影或平滑过渡。如果有动画，应该瞬间切换（0 秒过渡）。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。