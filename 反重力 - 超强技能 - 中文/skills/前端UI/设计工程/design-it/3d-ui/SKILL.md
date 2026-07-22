---
name: 3d-ui
description: 3D UI 的 Web 与 App 实现指南。当用户需要真正的 3D 对象、透视效果和空间纵深时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# 3D UI

> "打破平面。存在于三维、可旋转空间中的界面。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **真实深度（Z 轴平移）**：元素不仅有阴影，还会在物理上靠近或远离镜头。
2. **透视**：使用 CSS perspective 或 WebGL 创建真实的消失点。
3. **交互式旋转**：元素应当响应鼠标移动或设备陀螺仪，在三维空间中倾斜或旋转。

## 视觉 DNA
- **颜色**：大胆、引人注目的调色板，如 **Midnight Luxury** 或 **Industrial Chic**。3D 元素需要高对比度才能展现其几何形态。
- **排版**：粗体、块状或拉伸的文字。
- **图形**：放弃扁平图标，使用渲染好的 3D 资产（.glb、.gltf，或 3D 对象的高分辨率 PNG）。

## Web 实现
- 大量依赖 `perspective`、`transform-style: preserve-3d` 和 `rotateX`/`rotateY`。
- **CSS 示例**：
```css
.perspective-container {
  perspective: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-3d {
  width: 300px;
  height: 400px;
  transform-style: preserve-3d;
  transition: transform 0.5s ease;
  
  /* 初始轻微旋转 */
  transform: rotateX(15deg) rotateY(-15deg);
}

.card-3d:hover {
  /* 悬停时归正 */
  transform: rotateX(0) rotateY(0) translateZ(50px);
}

/* 内部元素凸出 */
.card-content {
  transform: translateZ(30px); /* 将内容向观察者推近 30px */
}
```

## App 实现

### SwiftUI
```swift
struct Card3D: View {
    @State private var dragOffset = CGSize.zero
    
    var body: some View {
        VStack {
            Text("3D Card")
                .font(.largeTitle.bold())
                .foregroundColor(.white)
        }
        .frame(width: 300, height: 400)
        .background(
            LinearGradient(colors: [.blue, .purple], startPoint: .topLeading, endPoint: .bottomTrailing)
        )
        .cornerRadius(24)
        .shadow(radius: 20)
        // 基于拖动手势的魔幻 3D 效果
        .rotation3DEffect(
            .degrees(Double(dragOffset.width / 10)),
            axis: (x: 0, y: 1, z: 0),
            perspective: 0.5
        )
        .rotation3DEffect(
            .degrees(Double(-dragOffset.height / 10)),
            axis: (x: 1, y: 0, z: 0),
            perspective: 0.5
        )
        .gesture(
            DragGesture()
                .onChanged { value in
                    withAnimation(.interactiveSpring()) {
                        dragOffset = value.translation
                    }
                }
                .onEnded { _ in
                    withAnimation(.spring()) {
                        dragOffset = .zero
                    }
                }
        )
    }
}
```
- SwiftUI 通过 `.rotation3DEffect()` 让这一切变得极其简单。
- 使用 `perspective` 参数（默认 1/6，数值越大越扭曲）控制镜头距离。
- 将旋转轴（`x`、`y`）链接到拖动手势或 CoreMotion（陀螺仪），实现交互式 3D UI。

### Flutter
```dart
class Card3D extends StatefulWidget {
  @override
  State<Card3D> createState() => _Card3DState();
}

class _Card3DState extends State<Card3D> {
  Offset _offset = Offset.zero;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onPanUpdate: (details) {
        setState(() => _offset += details.delta);
      },
      onPanEnd: (_) {
        setState(() => _offset = Offset.zero); // 归位
      },
      child: TweenAnimationBuilder(
        tween: Tween<Offset>(begin: Offset.zero, end: _offset),
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeOut,
        builder: (context, Offset offset, child) {
          // 透视矩阵
          final transform = Matrix4.identity()
            ..setEntry(3, 2, 0.001) // 透视
            ..rotateX(-offset.dy * 0.01)
            ..rotateY(offset.dx * 0.01);

          return Transform(
            transform: transform,
            alignment: FractionalOffset.center,
            child: Container(
              width: 300,
              height: 400,
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [Colors.blue, Colors.purple]),
                borderRadius: BorderRadius.circular(24),
                boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 20)],
              ),
              alignment: Alignment.center,
              child: const Text('3D Card', 
                style: TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold)),
            ),
          );
        },
      ),
    );
  }
}
```
- Flutter 实现透视的关键是 `Matrix4.identity()..setEntry(3, 2, 0.001)`。
- 用 `Transform` 包裹目标容器，并对 X 轴和 Y 轴应用旋转。
- 使用 `TweenAnimationBuilder` 平滑处理归位物理动画。

### React Native
```jsx
const Card3D = () => {
  const pan = useRef(new Animated.ValueXY()).current;

  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onPanResponderMove: Animated.event([null, { dx: pan.x, dy: pan.y }], { useNativeDriver: false }),
      onPanResponderRelease: () => {
        Animated.spring(pan, { toValue: { x: 0, y: 0 }, useNativeDriver: false }).start();
      },
    })
  ).current;

  // 将拖动距离映射为度数
  const rotateX = pan.y.interpolate({ inputRange: [-200, 200], outputRange: ['20deg', '-20deg'] });
  const rotateY = pan.x.interpolate({ inputRange: [-200, 200], outputRange: ['-20deg', '20deg'] });

  return (
    <Animated.View
      {...panResponder.panHandlers}
      style={{
        width: 300, height: 400,
        backgroundColor: '#6b21a8',
        borderRadius: 24,
        justifyContent: 'center', alignItems: 'center',
        // 伪 3D 变换
        transform: [
          { perspective: 1000 },
          { rotateX },
          { rotateY }
        ]
      }}
    >
      <Text style={{ color: '#fff', fontSize: 32, fontWeight: '700' }}>3D Card</Text>
    </Animated.View>
  );
};
```
- 真正的 3D 模型需要 `react-three-fiber`。
- 对于 UI 透视变换，使用 `transform` 数组：`[{ perspective: 1000 }, { rotateX: '...' }, { rotateY: '...' }]`。
- `perspective` 必须是 `transform` 数组中的第一项，否则效果无法正确渲染。

### Jetpack Compose
```kotlin
@Composable
fun Card3D() {
    var offset by remember { mutableStateOf(Offset.Zero) }
    val animatedOffset by animateOffsetAsState(
        targetValue = offset,
        animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy)
    )

    Box(
        modifier = Modifier
            .size(300.dp, 400.dp)
            .pointerInput(Unit) {
                detectDragGestures(
                    onDrag = { change, dragAmount ->
                        change.consume()
                        offset += dragAmount
                    },
                    onDragEnd = { offset = Offset.Zero },
                    onDragCancel = { offset = Offset.Zero }
                )
            }
            .graphicsLayer {
                // 根据拖动偏移应用 3D 旋转
                rotationX = -animatedOffset.y * 0.1f
                rotationY = animatedOffset.x * 0.1f
                cameraDistance = 8f * density // 设置透视
            }
            .shadow(20.dp, RoundedCornerShape(24.dp))
            .clip(RoundedCornerShape(24.dp))
            .background(Brush.linearGradient(listOf(Color.Blue, Color.Magenta)))
    ) {
        Text("3D Card",
            color = Color.White, fontSize = 32.sp, fontWeight = FontWeight.Bold,
            modifier = Modifier.align(Alignment.Center))
    }
}
```
- 在 `Modifier.graphicsLayer { }` 中应用 3D 变换。
- 设置 `rotationX` 和 `rotationY` 来控制倾斜。
- **关键**：设置 `cameraDistance` 来建立 Z 轴透视消失点。通常 `8f * density` 是一个不错的起点。

## 推荐与避免
- **推荐**：将 3D 旋转与用户输入绑定（Web 端用鼠标移动，移动端用设备倾斜），以获得最佳效果。
- **避免**：除非是巨型标题，否则不要让文字本身变成 3D。3D 文字在小尺寸下通常难以辨认。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。