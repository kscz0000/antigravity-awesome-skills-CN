---
name: ai-native-ui
description: AI Native UI 的 Web 与 App 实现指南。当用户需要对话式界面、自适应布局和生成式 AI 美学时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# AI Native UI

> "流动、自适应、对话式。界面随内容而变。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **对话优先**：聊天输入框或语音提示是主要的导航方式，而非侧边栏链接。
2. **生成式状态**：加载状态不是转圈动画，而是闪烁文字、渐变变形或骨架布局，最后平滑地解析为内容。
3. **自适应组件**：卡片和区块会根据生成内容的长度动态调整自身大小。

## 视觉 DNA
- **颜色**：将 **Minimalist Slate** 与 **Electric Indigo** 或 **Neon Pulse** 渐变结合，用于 AI 元素。背景干净（白色或深灰色），而 AI 的"在场感"则由一个不断变幻的彩虹渐变表示。
- **排版**：高可读性的系统字体（`Inter`、`SF Pro`）。
- **样式**：细微的发光边框，用于指示 AI 正在生成。

## Web 实现
- **CSS 示例**：
```css
body {
  background-color: #FAFAFA;
  color: #1A1A1A;
  font-family: 'Inter', sans-serif;
}

/* AI 聊天输入框 */
.ai-prompt-box {
  background: #ffffff;
  border-radius: 24px;
  padding: 16px 24px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.05);
  border: 1px solid transparent;
  
  /* AI 发光边框 */
  background-clip: padding-box, border-box;
  background-origin: padding-box, border-box;
  background-image: 
    linear-gradient(#ffffff, #ffffff), 
    linear-gradient(90deg, #8A2387, #E94057, #F27121);
    
  transition: all 0.3s ease;
}

.ai-prompt-box:focus-within {
  box-shadow: 0 12px 40px rgba(233, 64, 87, 0.15);
}

/* 生成式闪烁文字 */
.ai-generating-text {
  background: linear-gradient(90deg, #aaa 0%, #333 50%, #aaa 100%);
  background-size: 200% auto;
  color: transparent;
  -webkit-background-clip: text;
  animation: shine 1.5s linear infinite;
}

@keyframes shine {
  to { background-position: 200% center; }
}
```

## App 实现

### SwiftUI
```swift
struct AINativeInput: View {
    @State private var isGenerating = true
    @State private var gradientOffset = 0.0
    
    var body: some View {
        VStack {
            // 生成式闪烁文字
            if isGenerating {
                Text("Synthesizing response...")
                    .font(.headline)
                    .foregroundStyle(
                        LinearGradient(
                            colors: [.gray.opacity(0.3), .gray, .gray.opacity(0.3)],
                            startPoint: UnitPoint(x: gradientOffset - 1, y: 0),
                            endPoint: UnitPoint(x: gradientOffset + 1, y: 0)
                        )
                    )
                    .onAppear {
                        withAnimation(.linear(duration: 1.5).repeatForever(autoreverses: false)) {
                            gradientOffset = 1.0
                        }
                    }
            }
            
            // AI 输入框
            HStack {
                TextField("Ask anything...", text: .constant(""))
                Image(systemName: "sparkles")
                    .foregroundColor(.purple)
            }
            .padding()
            .background(Color.white)
            .cornerRadius(24)
            .overlay(
                RoundedRectangle(cornerRadius: 24)
                    .stroke(
                        LinearGradient(colors: [.purple, .pink, .orange], startPoint: .topLeading, endPoint: .bottomTrailing),
                        lineWidth: 2
                    )
            )
            .shadow(color: .pink.opacity(0.15), radius: 20)
        }
        .padding()
    }
}
```
- 在文字上叠加一个平移的 `LinearGradient` 蒙版，可以创造出美观的"思考中"状态。
- 在 `RoundedRectangle` 叠加层上使用渐变 `.stroke`，就能在输入框周围创建标志性的 AI 发光边框。

### Flutter
```dart
import 'package:shimmer/shimmer.dart';

class AINativeInput extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // 生成式闪烁
          Shimmer.fromColors(
            baseColor: Colors.grey[300]!,
            highlightColor: Colors.grey[600]!,
            child: const Text('Synthesizing response...',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ),
          const SizedBox(height: 16),
          // AI 输入框
          Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(24),
              boxShadow: [
                BoxShadow(color: Colors.pink.withOpacity(0.15), blurRadius: 20),
              ],
            ),
            child: Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(24),
                // 渐变边框模拟
                gradient: const LinearGradient(
                  colors: [Colors.purple, Colors.pink, Colors.orange],
                ),
              ),
              padding: const EdgeInsets.all(2), // 边框宽度
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(22),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                child: Row(
                  children: const [
                    Expanded(
                      child: TextField(
                        decoration: InputDecoration(
                          hintText: 'Ask anything...',
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                    Icon(Icons.auto_awesome, color: Colors.purple),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```
- `shimmer` 包是 Flutter 中 AI 加载状态的绝对标准。
- `BoxDecoration` 本身不支持渐变边框；通过嵌套容器（外层带渐变背景，内层带纯白填充）来模拟。

### React Native
```jsx
// 需要 react-native-linear-gradient 和 react-native-shimmer-placeholder
import LinearGradient from 'react-native-linear-gradient';
import { createShimmerPlaceholder } from 'react-native-shimmer-placeholder';

const ShimmerPlaceHolder = createShimmerPlaceholder(LinearGradient);

const AINativeInput = () => {
  return (
    <View style={{ padding: 16 }}>
      {/* 生成式闪烁 */}
      <ShimmerPlaceHolder 
        style={{ width: 200, height: 20, borderRadius: 10, marginBottom: 16 }}
        shimmerColors={['#ebebeb', '#c5c5c5', '#ebebeb']}
      />
      
      {/* 带渐变边框的 AI 输入框 */}
      <LinearGradient
        colors={['#8A2387', '#E94057', '#F27121']}
        style={{ borderRadius: 24, padding: 2, shadowColor: '#E94057', shadowRadius: 20, shadowOpacity: 0.2 }}
      >
        <View style={{ 
          backgroundColor: '#FFF', 
          borderRadius: 22, 
          flexDirection: 'row', 
          alignItems: 'center',
          paddingHorizontal: 16,
          height: 50
        }}>
          <TextInput 
            placeholder="Ask anything..." 
            style={{ flex: 1, fontSize: 16 }} 
          />
          <Text style={{ fontSize: 20 }}>✨</Text>
        </View>
      </LinearGradient>
    </View>
  );
};
```
- `react-native-shimmer-placeholder` 是处理变形骨架状态的最佳方式。
- 与 Flutter 一样，React Native 没有原生渐变边框。用 `padding: 2` 的 `LinearGradient` 包裹输入框以模拟描边。

### Jetpack Compose
```kotlin
@Composable
fun AINativeInput() {
    val infiniteTransition = rememberInfiniteTransition()
    val gradientOffset by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1000f,
        animationSpec = infiniteRepeatable(
            animation = tween(1500, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        )
    )

    Column(modifier = Modifier.padding(16.dp)) {
        // 生成式闪烁文字
        val shimmerBrush = Brush.linearGradient(
            colors = listOf(Color.LightGray, Color.Gray, Color.LightGray),
            start = Offset(gradientOffset - 500f, 0f),
            end = Offset(gradientOffset, 0f)
        )
        Text("Synthesizing response...", style = TextStyle(brush = shimmerBrush, fontWeight = FontWeight.Bold))
        
        Spacer(Modifier.height(16.dp))
        
        // AI 输入框
        val borderBrush = Brush.linearGradient(listOf(Color(0xFF8A2387), Color(0xFFE94057), Color(0xFFF27121)))
        
        Row(
            modifier = Modifier
                .shadow(20.dp, RoundedCornerShape(24.dp), ambientColor = Color(0xFFE94057), spotColor = Color(0xFFE94057))
                .background(Color.White, RoundedCornerShape(24.dp))
                .border(2.dp, borderBrush, RoundedCornerShape(24.dp))
                .padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            BasicTextField(
                value = "",
                onValueChange = {},
                modifier = Modifier.weight(1f),
                decorationBox = { innerTextField -> Text("Ask anything...", color = Color.Gray) }
            )
            Icon(Icons.Default.Star, contentDescription = null, tint = Color(0xFF8A2387))
        }
    }
}
```
- Compose 允许直接将 `Brush` 传入 `TextStyle`，让闪烁文字无需第三方库即可轻松实现。
- Compose 的 `Modifier.border()` 原生接受 `Brush`，让渐变边框成为一行代码。

## 推荐与避免
- **推荐**：用一种独特、鲜艳的渐变来代表 AI"代理"，与非常简洁、干净的背景形成对比。
- **避免**：使用复杂的导航标题栏。用户应当通过向 AI 提问来导航，而不是点击层层菜单。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。