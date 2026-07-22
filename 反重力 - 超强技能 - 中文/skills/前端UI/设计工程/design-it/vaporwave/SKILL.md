---
name: vaporwave
description: Vaporwave 的 Web 与 App 实现指南。当用户希望霓虹色、复古数字美学、90 年代 OS 元素和罗马雕像时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Vaporwave

> "对 90 年代计算和柔和霓虹的超现实、怀旧之梦。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **Windows 95 / Mac OS 9 主题**：UI 元素设计明确模仿 1990 年代的操作系统（灰框、硬倒角、蓝色标题栏）。
2. **超现实柔和色与霓虹**：柔和粉色、青色与生硬霓虹叠加的混合。
3. **拼贴美学**：古典艺术（罗马半身像）、早期 3D 渲染（棋盘地板）和日文（汉字/片假名）的混搭。

## 视觉 DNA
- **颜色**：青色（`#00FFFF`）、品红（`#FF00FF`）、薰衣草（`#E6E6FA`）和经典 Windows 灰（`#C0C0C0`）。
- **排版**：`MS Sans Serif`、`Tahoma` 或像素字体。强烈鼓励使用全角字符（ＡＥＳＴＨＥＴＩＣ）作为标题。
- **样式**：硬、1px 外凸和内凹边框，模拟 90 年代的 3D 按钮。

## Web 实现
- 使用标准 CSS 边框创建经典的 90 年代按钮外观。
- **CSS 示例**：
```css
body {
  background: linear-gradient(180deg, #ff99cc 0%, #99ccff 100%);
  color: #000;
  font-family: 'Tahoma', sans-serif;
  min-height: 100vh;
}

/* Windows 95 风格窗口 */
.vapor-window {
  background-color: #C0C0C0;
  border: 2px outset #fff;
  border-right-color: #808080;
  border-bottom-color: #808080;
  width: 400px;
  padding: 2px;
}

.vapor-titlebar {
  background: linear-gradient(90deg, #000080, #1084d0);
  color: white;
  font-weight: bold;
  padding: 4px 8px;
  display: flex;
  justify-content: space-between;
}

.vapor-button {
  background-color: #C0C0C0;
  border: 2px outset #fff;
  border-right-color: #808080;
  border-bottom-color: #808080;
  padding: 4px 12px;
}
.vapor-button:active {
  border-style: inset;
}

/* 标志性的蒸汽波太阳/网格 */
.vapor-sun {
  width: 200px; height: 200px;
  background: linear-gradient(to bottom, #ff00ff, #ffff00);
  border-radius: 50%;
  box-shadow: 0 0 20px #ff00ff;
}
```

## App 实现

### SwiftUI
```swift
struct VaporwaveView: View {
    var body: some View {
        ZStack {
            // 霓虹渐变背景
            LinearGradient(colors: [Color(hex: "ff99cc"), Color(hex: "99ccff")], startPoint: .top, endPoint: .bottom)
                .ignoresSafeArea()
            
            // Win95 窗口
            VStack(spacing: 0) {
                // 标题栏
                HStack {
                    Text("ＡＥＳＴＨＥＴＩＣ.exe")
                        .font(.system(size: 14, weight: .bold, design: .monospaced))
                        .foregroundColor(.white)
                    Spacer()
                    Text("X")
                        .font(.system(size: 12, weight: .bold))
                        .padding(.horizontal, 6)
                        .background(Color(hex: "C0C0C0"))
                        .border(.white, width: 1) // 伪造 3D
                }
                .padding(4)
                .background(LinearGradient(colors: [Color(hex: "000080"), Color(hex: "1084d0")], startPoint: .leading, endPoint: .trailing))
                
                // 内容
                VStack {
                    Text("It's all in your head.")
                        .font(.custom("Tahoma", size: 16))
                        .padding()
                    
                    // Win95 按钮
                    Button(action: {}) {
                        Text("ＯＫ")
                            .foregroundColor(.black)
                            .padding(.horizontal, 24)
                            .padding(.vertical, 8)
                    }
                    .background(Color(hex: "C0C0C0"))
                    // 复杂边框模拟 Outset
                    .overlay(
                        Rectangle().stroke(Color.black, lineWidth: 1) // 外底部/右侧
                    )
                    .overlay(
                        Rectangle().stroke(Color.white, lineWidth: 1).padding(1) // 内顶部/左侧
                    )
                }
                .frame(maxWidth: .infinity)
                .padding(16)
                .background(Color(hex: "C0C0C0"))
            }
            .frame(width: 300)
            // 窗口的外凸边框
            .border(Color(hex: "808080"), width: 2)
            .padding()
        }
    }
}
```
- 你不能在 Vaporwave 设计中使用任何 `.cornerRadius()`。
- Win95 的 3D 倒角通过堆叠 `.border()` 和 `.overlay(Rectangle().stroke())` 实现，颜色不同（白色用于顶部/左侧，深灰色用于底部/右侧）。

### Flutter
```dart
class VaporwaveScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Color(0xFFFF99CC), Color(0xFF99CCFF)]),
        ),
        child: Center(
          child: Container(
            width: 300,
            decoration: const BoxDecoration(
              color: Color(0xFFC0C0C0),
              // 经典 Win95 外凸边框
              border: Border(
                top: BorderSide(color: Colors.white, width: 2),
                left: BorderSide(color: Colors.white, width: 2),
                bottom: BorderSide(color: Color(0xFF808080), width: 2),
                right: BorderSide(color: Color(0xFF808080), width: 2),
              ),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // 标题栏
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
                  margin: const EdgeInsets.all(2),
                  decoration: const BoxDecoration(gradient: LinearGradient(colors: [Color(0xFF000080), Color(0xFF1084D0)])),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('ＡＥＳＴＨＥＴＩＣ.exe', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      Container(color: const Color(0xFFC0C0C0), padding: const EdgeInsets.symmetric(horizontal: 4), child: const Text('X', style: TextStyle(fontWeight: FontWeight.bold))),
                    ],
                  ),
                ),
                // 内容
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      const Text('nostalgia.sys loaded.', style: TextStyle(fontFamily: 'Tahoma')),
                      const SizedBox(height: 16),
                      // 外凸按钮
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
                        decoration: const BoxDecoration(
                          color: Color(0xFFC0C0C0),
                          border: Border(
                            top: BorderSide(color: Colors.white, width: 2), left: BorderSide(color: Colors.white, width: 2),
                            bottom: BorderSide(color: Color(0xFF808080), width: 2), right: BorderSide(color: Color(0xFF808080), width: 2),
                          ),
                        ),
                        child: const Text('ＯＫ'),
                      )
                    ],
                  ),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```
- Flutter 的 `BoxDecoration` 支持复杂的 `Border` 定义，可以独立设置 `BorderSide` 颜色。这完美复刻了 CSS 的 `outset` / `inset`。

### React Native
```jsx
const VaporwaveScreen = () => {
  return (
    <LinearGradient colors={['#ff99cc', '#99ccff']} style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      
      {/* 窗口 */}
      <View style={{
        backgroundColor: '#C0C0C0', width: 300,
        borderTopWidth: 2, borderLeftWidth: 2, borderTopColor: '#FFF', borderLeftColor: '#FFF',
        borderBottomWidth: 2, borderRightWidth: 2, borderBottomColor: '#808080', borderRightColor: '#808080',
        padding: 2
      }}>
        
        {/* 标题栏 */}
        <LinearGradient colors={['#000080', '#1084d0']} start={{x: 0, y: 0}} end={{x: 1, y: 0}} style={{ flexDirection: 'row', justifyContent: 'space-between', padding: 4 }}>
          <Text style={{ color: '#FFF', fontWeight: 'bold' }}>ＡＥＳＴＨＥＴＩＣ.exe</Text>
          <View style={{ backgroundColor: '#C0C0C0', paddingHorizontal: 4 }}><Text style={{ fontWeight: 'bold' }}>X</Text></View>
        </LinearGradient>

        <View style={{ padding: 16, alignItems: 'center' }}>
          <Text style={{ fontFamily: 'monospace', marginBottom: 16 }}>nostalgia.sys</Text>
          
          {/* 外凸按钮 */}
          <TouchableOpacity style={{
            backgroundColor: '#C0C0C0', paddingHorizontal: 24, paddingVertical: 8,
            borderTopWidth: 2, borderLeftWidth: 2, borderTopColor: '#FFF', borderLeftColor: '#FFF',
            borderBottomWidth: 2, borderRightWidth: 2, borderBottomColor: '#808080', borderRightColor: '#808080',
          }}>
            <Text style={{ fontWeight: 'bold' }}>ＯＫ</Text>
          </TouchableOpacity>
        </View>

      </View>

    </LinearGradient>
  );
};
```
- 使用独立的边框颜色样式（`borderTopColor: '#FFF'`、`borderBottomColor: '#808080'`）构建 90 年代 OS 装饰。
- 确保对文字使用日文全角字符以获得最佳的蒸汽波美学。

### Jetpack Compose
```kotlin
@Composable
fun VaporwaveScreen() {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(Color(0xFFFF99CC), Color(0xFF99CCFF)))),
        contentAlignment = Alignment.Center
    ) {
        // 窗口
        Column(
            modifier = Modifier
                .width(300.dp)
                // 自定义绘制的外凸边框
                .drawBehind {
                    val stroke = 4f
                    // 底部/右侧（深色）
                    drawLine(Color(0xFF808080), Offset(0f, size.height), Offset(size.width, size.height), stroke)
                    drawLine(Color(0xFF808080), Offset(size.width, 0f), Offset(size.width, size.height), stroke)
                    // 顶部/左侧（浅色）
                    drawLine(Color.White, Offset(0f, 0f), Offset(size.width, 0f), stroke)
                    drawLine(Color.White, Offset(0f, 0f), Offset(0f, size.height), stroke)
                }
                .background(Color(0xFFC0C0C0))
                .padding(2.dp)
        ) {
            // 标题栏
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Brush.horizontalGradient(listOf(Color(0xFF000080), Color(0xFF1084D0))))
                    .padding(4.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("ＡＥＳＴＨＥＴＩＣ.exe", color = Color.White, fontWeight = FontWeight.Bold)
                Box(modifier = Modifier.background(Color(0xFFC0C0C0)).padding(horizontal = 4.dp)) {
                    Text("X", fontWeight = FontWeight.Bold)
                }
            }
            
            // 内容
            Column(modifier = Modifier.fillMaxWidth().padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Welcome to the 90s.", fontFamily = FontFamily.Monospace)
                Spacer(Modifier.height(16.dp))
                
                // Win95 按钮
                Box(
                    modifier = Modifier
                        .clickable { }
                        .drawBehind {
                            val stroke = 4f
                            drawLine(Color(0xFF808080), Offset(0f, size.height), Offset(size.width, size.height), stroke)
                            drawLine(Color(0xFF808080), Offset(size.width, 0f), Offset(size.width, size.height), stroke)
                            drawLine(Color.White, Offset(0f, 0f), Offset(size.width, 0f), stroke)
                            drawLine(Color.White, Offset(0f, 0f), Offset(0f, size.height), stroke)
                        }
                        .padding(horizontal = 24.dp, vertical = 8.dp)
                ) {
                    Text("ＯＫ", fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}
```
- Compose 的 `Modifier.border` 在所有边上绘制均匀。要获得 90 年代的外凸外观，必须使用 `Modifier.drawBehind` 并手动绘制顶部/左侧的白色线条和底部/右侧的深灰色线条。

## 推荐与避免
- **推荐**：使用正宗的 90 年代图标（像素化沙漏、文件夹、错误对话框）。
- **避免**：使用现代投影或圆角。90 年代的 UI 是锐利而粗犷的。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。