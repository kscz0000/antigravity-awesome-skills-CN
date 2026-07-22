---
name: widget-based-design
description: Widget-Based Design 的 Web 与 App 实现指南。当用户希望模块化块、iOS 主屏幕美学和可定制的小型应用时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Widget-Based Design

> "微型应用。小巧、高度功能化的 UI 块，设计为可重新排列。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **严格的宽高比**：小部件通常遵循严格的尺寸（1x1 正方形、2x1 矩形、2x2 大正方形）。
2. **一眼概览**：小部件即时显示最重要的数据。深度交互通常需要打开完整应用。
3. **圆角匹配**：内部内容的圆角应完美嵌套在小部件的外圆角内。

## 视觉 DNA
- **颜色**：小部件经常使用明亮、纯色的背景或全幅照片来区分彼此。
- **排版**：大而粗的数字（如时钟或天气温度）搭配极小的子标签。
- **布局**：与 Bento UI 类似，但专门聚焦于功能性小程序而非仅是内容布局。

## Web 实现
- **CSS 示例**：
```css
.widget-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  grid-auto-rows: 160px; /* 强制方形 */
  gap: 16px;
  padding: 32px;
}

.widget {
  background-color: #ffffff;
  border-radius: 24px; /* 经典 iOS 小部件圆角 */
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  position: relative;
}

/* 特定尺寸 */
.widget-small { grid-column: span 1; grid-row: span 1; }
.widget-medium { grid-column: span 2; grid-row: span 1; }
.widget-large { grid-column: span 2; grid-row: span 2; }

/* 天气小部件示例 */
.widget.weather {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}
.weather-temp { font-size: 3rem; font-weight: 300; }
.weather-icon { position: absolute; top: 16px; right: 16px; font-size: 2rem; }
```

## App 实现

### SwiftUI
```swift
struct WidgetDesignView: View {
    let columns = [GridItem(.flexible(), spacing: 16), GridItem(.flexible(), spacing: 16)]
    
    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 16) {
                // 2x1 小部件
                WeatherWidget()
                    .frame(height: 160) // 基础单位高度
                
                // 1x1 小部件
                FitnessWidget()
                    .frame(height: 160)
                
                // 1x1 小部件
                MusicWidget()
                    .frame(height: 160)
            }
            .padding(24)
        }
        .background(Color(white: 0.95))
    }
}

struct WeatherWidget: View {
    var body: some View {
        ZStack(alignment: .topTrailing) {
            LinearGradient(colors: [Color(hex: "4facfe"), Color(hex: "00f2fe")], startPoint: .topLeading, endPoint: .bottomTrailing)
            
            Image(systemName: "cloud.sun.fill")
                .foregroundColor(.white)
                .font(.system(size: 40))
                .padding()
            
            VStack(alignment: .leading) {
                Spacer()
                Text("72°")
                    .font(.system(size: 48, weight: .thin))
                    .foregroundColor(.white)
                Text("San Francisco")
                    .font(.subheadline)
                    .foregroundColor(.white.opacity(0.8))
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding()
        }
        .cornerRadius(24) // 经典 iOS 小部件圆角
        .shadow(color: .black.opacity(0.1), radius: 10, y: 5)
    }
}
```
- SwiftUI 在这方面很完美。`LazyVGrid` 处理布局，`.cornerRadius(24)` 完美匹配 Apple 默认的小部件样式。
- 使用 `ZStack` 作为小部件的根，方便地将内容叠加在复杂渐变或图像之上。

### Flutter
```dart
class WidgetDesignScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF2F2F2),
      body: GridView.count(
        crossAxisCount: 2, // 2 列适用于典型手机
        padding: const EdgeInsets.all(24),
        mainAxisSpacing: 16,
        crossAxisSpacing: 16,
        childAspectRatio: 1.0, // 1x1 正方形
        children: [
          // 注意：Flutter 的 GridView 不容易跨行/列。
          // 生产应用中强烈推荐使用 flutter_staggered_grid_view 包。
          _buildWeatherWidget(),
          _buildFitnessWidget(),
          _buildMusicWidget(),
        ],
      ),
    );
  }

  Widget _buildWeatherWidget() {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(24),
        gradient: const LinearGradient(colors: [Color(0xFF4FACFE), Color(0xFF00F2FE)]),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 10, offset: const Offset(0, 5))],
      ),
      padding: const EdgeInsets.all(16),
      child: Stack(
        children: [
          const Align(
            alignment: Alignment.topRight,
            child: Icon(Icons.cloud, color: Colors.white, size: 40),
          ),
          Align(
            alignment: Alignment.bottomLeft,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('72°', style: TextStyle(color: Colors.white, fontSize: 48, fontWeight: FontWeight.w300)),
                Text('San Francisco', style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 14)),
              ],
            ),
          )
        ],
      ),
    );
  }
}
```
- `Stack` 内放 `Container`，配合 `BorderRadius.circular(24)` 是每个小部件的蓝图。
- 标准 `GridView` 对混合的 2x1 和 1x1 小部件过于死板。在生产应用中使用 `flutter_staggered_grid_view` 包。

### React Native
```jsx
const WidgetDesignScreen = () => {
  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#F2F2F2' }} contentContainerStyle={{ padding: 24 }}>
      <View style={{ flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', gap: 16 }}>
        
        {/* 2x1 小部件（满宽减去内边距） */}
        <View style={[styles.widget, { width: '100%' }]}>
          <LinearGradient colors={['#4facfe', '#00f2fe']} style={styles.widgetBg} />
          <Text style={styles.temp}>72°</Text>
          <Text style={styles.sub}>San Francisco</Text>
        </View>

        {/* 1x1 小部件（一半宽减去一半间隙） */}
        <View style={[styles.widget, { width: '47%' }]}><Text>Fitness</Text></View>
        <View style={[styles.widget, { width: '47%' }]}><Text>Music</Text></View>

      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  widget: {
    height: 160, // 固定高度强制方形/矩形宽高比
    borderRadius: 24,
    backgroundColor: '#FFF',
    padding: 16,
    justifyContent: 'flex-end',
    shadowColor: '#000', shadowOffset: { width: 0, height: 5 }, shadowOpacity: 0.1, shadowRadius: 10, elevation: 5,
    overflow: 'hidden'
  },
  widgetBg: {
    ...StyleSheet.absoluteFillObject,
    borderRadius: 24,
  },
  temp: { fontSize: 48, fontWeight: '300', color: '#FFF' },
  sub: { fontSize: 14, color: 'rgba(255,255,255,0.8)' }
});
```
- 在 React Native 中，`flexWrap: 'wrap'` 配合百分比宽度（例如 `47%` 用于 2 列 + 间隙）是构建响应式小部件布局最干净的方法。
- 如果使用 `expo-linear-gradient` 或 `react-native-linear-gradient`，对其应用 `StyleSheet.absoluteFillObject` 使其位于文字后面。

### Jetpack Compose
```kotlin
@Composable
fun WidgetDesignScreen() {
    LazyVerticalGrid(
        columns = GridCells.Fixed(2),
        modifier = Modifier.fillMaxSize().background(Color(0xFFF2F2F2)).padding(24.dp),
        horizontalArrangement = Arrangement.spacedBy(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // 2x1 小部件（横跨两列）
        item(span = { GridItemSpan(2) }) {
            WeatherWidget(Modifier.height(160.dp))
        }
        // 1x1 小部件
        item { Box(Modifier.height(160.dp).background(Color.White, RoundedCornerShape(24.dp))) }
        item { Box(Modifier.height(160.dp).background(Color.White, RoundedCornerShape(24.dp))) }
    }
}

@Composable
fun WeatherWidget(modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .shadow(10.dp, RoundedCornerShape(24.dp))
            .background(Brush.linearGradient(listOf(Color(0xFF4FACFE), Color(0xFF00F2FE))), RoundedCornerShape(24.dp))
            .padding(16.dp)
    ) {
        // 图标
        Icon(Icons.Filled.Cloud, contentDescription = null, tint = Color.White, modifier = Modifier.align(Alignment.TopEnd).size(40.dp))
        
        // 数据
        Column(modifier = Modifier.align(Alignment.BottomStart)) {
            Text("72°", fontSize = 48.sp, fontWeight = FontWeight.Light, color = Color.White)
            Text("San Francisco", fontSize = 14.sp, color = Color.White.copy(alpha = 0.8f))
        }
    }
}
```
- `LazyVerticalGrid` 配合 `GridCells.Fixed(2)` 和 `GridItemSpan` 完美复刻 iOS 小部件网格。
- `RoundedCornerShape(24.dp)` 对于营造外观至关重要。

## 推荐与避免
- **推荐**：使用全幅背景颜色让不同的小部件脱颖而出。
- **避免**：在 1x1 小部件内放置复杂的表单或可滚动列表。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。