---
name: neo-brutalism
description: Neo-Brutalism 的 Web 与 App 实现指南。当用户希望粗边框、硬阴影、鲜艳颜色和俏皮又有条理的外观时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Neo-Brutalism

> "粗犷主义，但让它更具表现力。生硬的线条、刺眼的阴影，以及鲜艳、不加掩饰的色彩。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **硬投影**：纯黑阴影，无模糊。通常向下、向右偏移几个像素。
2. **粗描边**：所有元素都有厚实的纯黑边框（通常 2px-4px）。
3. **扁平、高对比度颜色**：明亮、饱和的柔和色或原色，与纯白或纯黑形成对比。

## 视觉 DNA
- **颜色**：从偏白背景（如 `#FDF8F5`）开始，加入刺眼的黑色边框 `#000000`，并使用饱和的强调色如柠檬黄、亮青或珊瑚色。
- **排版**：非常粗壮、几何无衬线字体（如 `Space Grotesk`、`Archivo Black`、`Inter Black`）。
- **形状**：锐利矩形或完全圆润的胶囊形，但都带有厚重的描边。

## Web 实现
- 定义性特征是 `box-shadow` 配合 `0` 模糊。
- **CSS 示例**：
```css
:root {
  --neo-border: 3px solid #000000;
  --neo-shadow: 6px 6px 0px #000000;
  --neo-bg: #F4F4F0;
  --neo-accent: #FF3366;
}

body {
  background-color: var(--neo-bg);
  font-family: 'Space Grotesk', sans-serif;
}

.neo-card {
  background-color: #ffffff;
  border: var(--neo-border);
  box-shadow: var(--neo-shadow);
  border-radius: 8px; /* 可选，锐利也行 */
  padding: 32px;
  transition: transform 0.1s, box-shadow 0.1s;
}

.neo-btn {
  background-color: var(--neo-accent);
  color: #000;
  font-weight: 800;
  text-transform: uppercase;
  border: var(--neo-border);
  box-shadow: 4px 4px 0px #000000;
  padding: 16px 32px;
  cursor: pointer;
  transition: all 0.1s ease;
}

.neo-btn:active {
  /* "按下"效果是移除阴影并向下移动它 */
  transform: translate(4px, 4px);
  box-shadow: 0px 0px 0px #000000;
}
```

## App 实现

### SwiftUI
```swift
struct NeoCard: View {
    @State private var isPressed = false
    let neoBorder: CGFloat = 3
    let neoShadow: CGFloat = 6
    
    var body: some View {
        Button(action: {}) {
            VStack(alignment: .leading, spacing: 16) {
                Text("NEO-BRUTALISM")
                    .font(.system(size: 24, weight: .black, design: .default))
                    .foregroundColor(.black)
                Text("Stark shadows, bright colors.")
                    .font(.system(size: 16, weight: .bold))
                    .foregroundColor(.black)
            }
            .padding(24)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(Color(red: 1.0, green: 0.2, blue: 0.4)) // 亮珊瑚
            // 新粗野主义实心描边
            .overlay(
                Rectangle()
                    .stroke(Color.black, lineWidth: neoBorder)
            )
        }
        .buttonStyle(.plain)
        // 硬投影（0 模糊）
        .shadow(color: .black, radius: 0, x: isPressed ? 0 : neoShadow, y: isPressed ? 0 : neoShadow)
        // 按下时物理位移以遮盖阴影
        .offset(x: isPressed ? neoShadow : 0, y: isPressed ? neoShadow : 0)
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
        // 瞬间切换，无平滑动画
        .animation(.none, value: isPressed)
    }
}
```
- `.shadow(radius: 0)` 是秘诀。设置偏移（例如 `x: 6, y: 6`）。
- 对于交互，移除阴影并使用 `.offset()` 将元素平移相同的偏移量。
- 确保 `.animation(.none)` — Neo-brutalism 交互应该瞬间切换，像物理开关。

### Flutter
```dart
class NeoCard extends StatefulWidget {
  @override
  State<NeoCard> createState() => _NeoCardState();
}

class _NeoCardState extends State<NeoCard> {
  bool _isPressed = false;
  final double neoOffset = 6.0;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => setState(() => _isPressed = true),
      onTapUp: (_) => setState(() => _isPressed = false),
      onTapCancel: () => setState(() => _isPressed = false),
      child: Transform.translate(
        // 按下时移动容器
        offset: Offset(_isPressed ? neoOffset : 0, _isPressed ? neoOffset : 0),
        child: Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: const Color(0xFFFF3366), // 亮珊瑚
            border: Border.all(color: Colors.black, width: 3),
            // 锐利阴影在按下时消失
            boxShadow: _isPressed ? [] : [
              BoxShadow(
                color: Colors.black,
                blurRadius: 0,     // 关键：0 模糊
                spreadRadius: 0,
                offset: Offset(neoOffset, neoOffset),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: const [
              Text('NEO-BRUTALISM',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: Colors.black)),
              SizedBox(height: 16),
              Text('Stark shadows, bright colors.',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black)),
            ],
          ),
        ),
      ),
    );
  }
}
```
- `BoxShadow` 内 `blurRadius: 0` 创建实心色块。
- 当 `_isPressed` 为 true 时完全移除阴影数组，并同时使用 `Transform.translate` 将控件向右下方移动。

### React Native
```jsx
const NeoCard = () => {
  const [pressed, setPressed] = useState(false);
  const offset = 6;

  return (
    <Pressable
      onPressIn={() => setPressed(true)}
      onPressOut={() => setPressed(false)}
      style={{
        backgroundColor: '#FF3366',
        padding: 24,
        borderWidth: 3,
        borderColor: '#000',
        transform: [
          { translateX: pressed ? offset : 0 },
          { translateY: pressed ? offset : 0 }
        ],
        // iOS 硬阴影
        shadowColor: '#000',
        shadowOffset: { width: pressed ? 0 : offset, height: pressed ? 0 : offset },
        shadowOpacity: pressed ? 0 : 1,
        shadowRadius: 0,
        // Android elevation 无法原生实现 0 模糊的偏移阴影
        // elevation: 0
      }}
    >
      <Text style={{ fontSize: 24, fontWeight: '900', color: '#000' }}>
        NEO-BRUTALISM
      </Text>
    </Pressable>
  );
};
```
- **Android 限制**：标准 `elevation` 无法创建无模糊的偏移投影。
- **解决方案**：要在 Android 上实现这一点，必须使用 `react-native-drop-shadow` 库，或者在卡片后面绝对定位渲染一个相同的黑色 `<View>` 来模拟。

### Jetpack Compose
```kotlin
@Composable
fun NeoCard() {
    var isPressed by remember { mutableStateOf(false) }
    val neoOffset = 6.dp
    
    // Compose 的 Modifier.shadow() 总是带模糊。
    // 要获得实心硬阴影，使用 Modifier.drawBehind。
    Box(
        modifier = Modifier
            .padding(16.dp)
            .offset(
                x = if (isPressed) neoOffset else 0.dp,
                y = if (isPressed) neoOffset else 0.dp
            )
            .drawBehind {
                if (!isPressed) {
                    drawRect(
                        color = Color.Black,
                        topLeft = Offset(neoOffset.toPx(), neoOffset.toPx()),
                        size = size
                    )
                }
            }
            .background(Color(0xFFFF3366))
            .border(3.dp, Color.Black)
            .pointerInput(Unit) {
                detectTapGestures(
                    onPress = {
                        isPressed = true
                        tryAwaitRelease()
                        isPressed = false
                    }
                )
            }
            .padding(24.dp)
    ) {
        Column {
            Text("NEO-BRUTALISM",
                fontSize = 24.sp, fontWeight = FontWeight.Black, color = Color.Black)
            Spacer(Modifier.height(16.dp))
            Text("Stark shadows, bright colors.",
                fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)
        }
    }
}
```
- **Compose 限制**：原生 `Modifier.shadow()` 应用环境模糊，会破坏新粗野主义美学。
- 使用 `Modifier.drawBehind { drawRect(...) }` 在偏移处绘制实心阴影块。
- 在按下时使用 `Modifier.offset` 平移容器，同时隐藏阴影层。

## 推荐与避免
- **推荐**：让激活/按下状态在视觉上将按钮平移以遮盖阴影，营造物理"咔哒"感。
- **避免**：使用渐变或模糊阴影。这种美学完全依赖扁平、锐利的矢量。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。