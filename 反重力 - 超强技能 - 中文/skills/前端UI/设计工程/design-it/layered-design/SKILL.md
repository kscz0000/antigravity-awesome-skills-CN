---
name: layered-design
description: Layered Design 的 Web 与 App 实现指南。当用户希望多层深度、漂浮面板和重叠内容时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Layered Design

> "堆叠上下文。由重叠、独立的层构建的界面。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **显式重叠**：元素故意相互重叠，打破网格，展示深度。
2. **清晰分层**：每一层必须通过阴影、边框或对比色加以视觉区分。
3. **视差滚动**：背景层在交互/滚动时移动得比前景层慢。

## 视觉 DNA
- **颜色**：**Monochromatic Brown** 或 **Sophisticated Neutral**。分层在背景与漂浮元素明显不同时效果最佳。
- **排版**：经常是大型、跨图像和背景层的重叠文字。
- **间距**：重叠元素周围需要留白，避免显得杂乱。

## Web 实现
- 大量使用 `position: absolute`、负 margin 和 `z-index`。
- **CSS 示例**：
```css
.layer-container {
  position: relative;
  padding: 100px;
}

.layer-bg-image {
  position: absolute;
  top: 0; right: 0;
  width: 60%;
  height: 400px;
  object-fit: cover;
  z-index: 1;
}

.layer-text-box {
  position: relative;
  z-index: 2; /* 位于图像之上 */
  background: white;
  padding: 40px;
  width: 50%;
  margin-top: 200px; /* 向下拉过图像 */
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  /* 可选：边框定义边缘 */
  border-left: 4px solid var(--cta-highlight);
}
```

## App 实现

### SwiftUI
```swift
struct LayeredDesignView: View {
    var body: some View {
        ScrollView {
            ZStack(alignment: .top) {
                // 背景图片层（后方）
                Image("architectural-bg")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(height: 400)
                    .offset(x: 40, y: 0) // 向右偏移
                    .zIndex(1)
                
                // 内容卡片层（前方）
                VStack(alignment: .leading, spacing: 16) {
                    Text("Stacking Context")
                        .font(.largeTitle).bold()
                    Text("This card intentionally overlaps the background image to create depth without relying on a grid.")
                        .foregroundColor(.secondary)
                }
                .padding(40)
                .background(Color.white)
                .shadow(color: Color.black.opacity(0.1), radius: 30, y: 20)
                .offset(x: -40, y: 200) // 向左偏移并向下拉
                .zIndex(2)
            }
            .padding(.bottom, 200) // 为偏移预留空间
        }
    }
}
```
- `ZStack` 是 SwiftUI 中分层设计的基础。
- 使用 `.offset()` 故意打破对齐，创建重叠组合。
- 如果偏移可能导致意外的绘制顺序，显式设置 `.zIndex()`。

### Flutter
```dart
class LayeredDesignScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: SizedBox(
          height: 600, // 固定高度栈或使用约束
          child: Stack(
            children: [
              // 背景图片层
              Positioned(
                top: 0,
                right: -40, // 偏出屏幕右侧
                width: MediaQuery.of(context).size.width * 0.8,
                height: 400,
                child: Image.asset('assets/architectural-bg.jpg', fit: BoxFit.cover),
              ),
              
              // 内容卡片层
              Positioned(
                top: 250, // 与图像底部重叠
                left: 20, // 与图像左侧重叠
                width: MediaQuery.of(context).size.width * 0.7,
                child: Container(
                  padding: const EdgeInsets.all(40),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    boxShadow: [
                      BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 30, offset: const Offset(0, 20))
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text('Stacking Context', style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
                      SizedBox(height: 16),
                      Text('This card intentionally overlaps the background image.', style: TextStyle(color: Colors.grey)),
                    ],
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
- `Stack` 配合 `Positioned` 子项是必需的。
- 可以在 `Positioned` 中使用负值（如 `right: -40`），让图层出血到屏幕边缘外，这是分层设计中的常见手法。

### React Native
```jsx
const LayeredDesignScreen = () => {
  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#F8F8F8' }}>
      <View style={{ height: 600 }}>
        
        {/* 背景图片层 */}
        <Image 
          source={{ uri: 'https://example.com/architectural-bg.jpg' }}
          style={{
            position: 'absolute',
            top: 0,
            right: -40,
            width: '80%',
            height: 400,
            zIndex: 1,
          }}
        />

        {/* 内容卡片层 */}
        <View style={{
          position: 'absolute',
          top: 250,
          left: 20,
          width: '70%',
          backgroundColor: '#FFF',
          padding: 40,
          zIndex: 2,
          // 深阴影以分隔图层
          shadowColor: '#000', shadowOffset: { width: 0, height: 20 },
          shadowOpacity: 0.1, shadowRadius: 30, elevation: 15,
        }}>
          <Text style={{ fontSize: 32, fontWeight: 'bold', marginBottom: 16 }}>Stacking Context</Text>
          <Text style={{ color: '#666' }}>This card intentionally overlaps the background image.</Text>
        </View>

      </View>
    </ScrollView>
  );
};
```
- 在相对容器内大量使用 `position: 'absolute'`。
- 显式管理 `zIndex`。注意在 Android 上，`elevation` 也控制 Z 索引，因此卡片必须有比图像更高的 `elevation`。

### Jetpack Compose
```kotlin
@Composable
fun LayeredDesignScreen() {
    Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
        Box(modifier = Modifier.height(600.dp).fillMaxWidth()) {
            
            // 背景图片层
            Image(
                painter = painterResource(id = R.drawable.architectural_bg),
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .offset(x = 40.dp) // 出血到右侧
                    .width(300.dp)
                    .height(400.dp)
                    .zIndex(1f)
            )
            
            // 内容卡片层
            Box(
                modifier = Modifier
                    .align(Alignment.TopStart)
                    .offset(x = 20.dp, y = 250.dp) // 与图像重叠
                    .width(280.dp)
                    .zIndex(2f)
                    .shadow(30.dp)
                    .background(Color.White)
                    .padding(40.dp)
            ) {
                Column {
                    Text("Stacking Context", fontSize = 32.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(16.dp))
                    Text("This card intentionally overlaps the background image.", color = Color.Gray)
                }
            }
        }
    }
}
```
- `Box` 作为你的栈。
- 使用 `Modifier.align()` 设置基准位置，再使用 `Modifier.offset()` 推出网格对齐。
- `Modifier.zIndex()` 确保内容卡片始终渲染在图像之上。

## 推荐与避免
- **推荐**：在层交叉处使用对比色或投影，让边界清晰。
- **避免**：将可交互元素（如按钮）藏在其他无法点击的层下。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。