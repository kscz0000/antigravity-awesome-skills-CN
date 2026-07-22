---
name: floating-ui
description: Floating UI 的 Web 与 App 实现指南。当用户希望脱离式卡片、悬浮组件和轻盈通透感时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Floating UI

> "反抗重力。在表面之上轻盈漂浮的元素。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **脱离感**：UI 元素（如导航栏、侧边栏或主要内容卡片）不接触屏幕边缘。它们在所有边上都带有边距悬浮。
2. **柔和、弥散的阴影**：元素下方有大面积、高度模糊的阴影。
3. **胶囊形状与圆角**：完全圆润的角（胶囊形状）增强漂浮、气泡般的美感。

## 视觉 DNA
- **颜色**：**Earth-Grounded Elegance** 或 **Minimalist Slate**。使用略带色调的背景（近白或极浅灰色），让漂浮的白色元素凸显。
- **排版**：干净、通透的无衬线字体，行高宽松。
- **布局**：用于导航的"漂浮岛屿"模式（屏幕底部或顶部居中的胶囊形导航栏）。

## Web 实现
- 注重大边距和特定的阴影样式。
- **CSS 示例**：
```css
body {
  background-color: var(--bg-primary); /* 例如 #F4F4F9 */
  padding: 24px; /* 确保没有元素接触边缘 */
}

.floating-nav {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border-radius: 50px; /* 胶囊形状 */
  padding: 12px 32px;
  
  /* 大而柔和的阴影 */
  box-shadow: 0 16px 40px rgba(0,0,0,0.08);
  
  display: flex;
  gap: 24px;
}

.floating-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
```

## App 实现

### SwiftUI
```swift
struct FloatingUIView: View {
    var body: some View {
        ZStack {
            // 极浅的背景
            Color(red: 0.95, green: 0.95, blue: 0.97).ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 24) {
                    // 漂浮内容卡片
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Floating Card")
                            .font(.title2).fontWeight(.bold)
                        Text("This card hovers above the background, with massive soft shadows and completely rounded corners.")
                            .foregroundColor(.secondary)
                    }
                    .padding(32)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color.white)
                    .cornerRadius(32) // 超大圆角
                    // 大而高模糊的阴影
                    .shadow(color: Color.black.opacity(0.05), radius: 30, x: 0, y: 15)
                    .padding(.horizontal, 24) // 与边缘保持脱离
                }
                .padding(.top, 40)
            }
            
            // 漂浮胶囊导航
            VStack {
                Spacer()
                HStack(spacing: 40) {
                    Image(systemName: "house.fill").foregroundColor(.blue)
                    Image(systemName: "magnifyingglass").foregroundColor(.gray)
                    Image(systemName: "bell.fill").foregroundColor(.gray)
                    Image(systemName: "person.fill").foregroundColor(.gray)
                }
                .padding(.vertical, 16)
                .padding(.horizontal, 32)
                .background(Color.white)
                .clipShape(Capsule()) // 胶囊形状
                .shadow(color: Color.black.opacity(0.1), radius: 25, x: 0, y: 10)
                .padding(.bottom, 32) // 与底部边缘脱离
            }
        }
    }
}
```
- `.clipShape(Capsule())` 搭配大尺寸 `.shadow()` 创建完美的漂浮胶囊导航栏。
- 将 `.shadow(radius: ...)` 推高到 25 或 30，配置非常低的不透明度（0.05），以获得柔和、弥散的悬浮效果。

### Flutter
```dart
class FloatingUIScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F4F9),
      body: Stack(
        children: [
          ListView(
            padding: const EdgeInsets.all(24),
            children: [
              // 漂浮内容卡片
              Container(
                margin: const EdgeInsets.only(bottom: 24),
                padding: const EdgeInsets.all(32),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(32), // 大圆角
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.05),
                      blurRadius: 30,
                      offset: const Offset(0, 15),
                    )
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Floating Card', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                    SizedBox(height: 12),
                    Text('This card hovers above the background.', style: TextStyle(color: Colors.grey)),
                  ],
                ),
              ),
            ],
          ),
          
          // 漂浮底部导航
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              margin: const EdgeInsets.only(bottom: 32),
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(50), // 胶囊形状
                boxShadow: [
                  BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 25, offset: const Offset(0, 10))
                ],
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min, // 包裹内容
                children: const [
                  Icon(Icons.home, color: Colors.blue),
                  SizedBox(width: 40),
                  Icon(Icons.search, color: Colors.grey),
                  SizedBox(width: 40),
                  Icon(Icons.person, color: Colors.grey),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```
- 避免使用原生 `BottomNavigationBar`。改用 `Stack` 和 `Align(alignment: Alignment.bottomCenter)` 配合 `Container` 来构建漂浮胶囊菜单。
- 在 `BoxShadow` 中使用 `blurRadius: 30` 实现弥散效果。

### React Native
```jsx
const FloatingUIScreen = () => {
  return (
    <View style={{ flex: 1, backgroundColor: '#F4F4F9' }}>
      <ScrollView contentContainerStyle={{ padding: 24 }}>
        {/* 漂浮卡片 */}
        <View style={styles.floatingCard}>
          <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 12 }}>Floating Card</Text>
          <Text style={{ color: '#666' }}>This card hovers above the background, detached from all edges.</Text>
        </View>
      </ScrollView>

      {/* 漂浮胶囊导航 */}
      <View style={styles.floatingNav}>
        <Text style={{ fontSize: 20 }}>🏠</Text>
        <Text style={{ fontSize: 20, opacity: 0.5 }}>🔍</Text>
        <Text style={{ fontSize: 20, opacity: 0.5 }}>👤</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  floatingCard: {
    backgroundColor: '#FFF',
    borderRadius: 32,
    padding: 32,
    marginBottom: 24,
    // iOS 阴影
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 15 },
    shadowOpacity: 0.05,
    shadowRadius: 30,
    // Android 阴影
    elevation: 8,
  },
  floatingNav: {
    position: 'absolute',
    bottom: 40,
    alignSelf: 'center',
    flexDirection: 'row',
    backgroundColor: '#FFF',
    borderRadius: 50,
    paddingVertical: 16,
    paddingHorizontal: 32,
    gap: 40, // 需要 RN 0.71+
    
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.1,
    shadowRadius: 25,
    elevation: 10,
  }
});
```
- `position: 'absolute'` 配合 `alignSelf: 'center'` 是 React Native 中放置胶囊导航的最简单方法。
- Android 的 `elevation` 不支持大模糊半径，因此效果在 iOS 上更强烈、更柔和。

### Jetpack Compose
```kotlin
@Composable
fun FloatingUIScreen() {
    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF4F4F9))) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp)
        ) {
            // 漂浮卡片
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .shadow(15.dp, RoundedCornerShape(32.dp), spotColor = Color.Black.copy(alpha = 0.05f))
                    .background(Color.White, RoundedCornerShape(32.dp))
                    .padding(32.dp)
            ) {
                Column {
                    Text("Floating Card", fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(12.dp))
                    Text("This card hovers above the background.", color = Color.Gray)
                }
            }
        }
        
        // 漂浮胶囊导航
        Row(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 32.dp)
                .shadow(20.dp, CircleShape, spotColor = Color.Black.copy(alpha = 0.1f))
                .background(Color.White, CircleShape)
                .padding(horizontal = 32.dp, vertical = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(40.dp)
        ) {
            Icon(Icons.Default.Home, contentDescription = null, tint = Color.Blue)
            Icon(Icons.Default.Search, contentDescription = null, tint = Color.Gray)
            Icon(Icons.Default.Person, contentDescription = null, tint = Color.Gray)
        }
    }
}
```
- 对胶囊导航背景使用 `CircleShape`。
- 关键是降低 `Modifier.shadow` 中 `spotColor` 的 `alpha`，以获得柔和、弥散的阴影效果，否则 Compose 默认会使用生硬的暗阴影。

## 推荐与避免
- **推荐**：为漂浮元素添加动画！一个缓慢持续的 2px 上/下 translateY 动画能让人感到真正轻盈。
- **避免**：将元素钉在屏幕边缘（背景图像除外）。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。