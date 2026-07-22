---
name: duotone-design
description: Duotone Design 的 Web 与 App 实现指南。当用户需要双色配色方案、醒目图像和 Spotify 风格播放列表美学时触发。
date_added: "2026-06-17"
risk: safe
source: self
source_type: self
---

# Duotone Design

> "醒目的对比。摄影和 UI 被剥离为恰好两种冲突或互补的颜色。"


## 使用时机

当用户的请求匹配上述美学风格时使用此子风格。这是 `design-it` 技能的子参考，不应被直接触发。

## 核心原则
1. **仅两种颜色**：整个设计映射到一种深色（替代黑色/阴影）和一种浅色（替代白色/高光）。
2. **图像处理**：所有照片必须被处理为双色配色。
3. **粗体、扁平排版**：文字通常体积庞大、填充实心，使用两种颜色之一。

## 视觉 DNA
- **颜色**：高对比度配色。海军蓝配桃色、深紫配霓虹绿、深红配米白。可以参考 **Industrial Chic**。
- **排版**：粗体、压缩的无衬线字体（如 `League Gothic`、`Oswald`）。
- **图像**：高对比度、颗粒感强的摄影作品在映射为双色时效果最佳。

## Web 实现
- 现代 CSS 无需 Photoshop 即可实现图像双色效果，可使用 `mix-blend-mode` 和滤镜。
- **CSS 示例**：
```css
:root {
  --duo-dark: #1E0045; /* 深紫色 */
  --duo-light: #CCFF00; /* 霓虹酸橙色 */
}

body {
  background-color: var(--duo-dark);
  color: var(--duo-light);
}

/* CSS 双色图像效果 */
.duotone-container {
  position: relative;
  width: 100%;
  height: 400px;
  background-color: var(--duo-light); /* 基础色 */
}

.duotone-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* 转为灰度，提高对比度 */
  filter: grayscale(100%) contrast(1.5); 
  /* 将灰度图像与浅色背景相乘 */
  mix-blend-mode: multiply;
}

.duotone-container::after {
  /* 使用 screen/lighten 叠加深色 */
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: var(--duo-dark);
  mix-blend-mode: screen;
}

.duotone-btn {
  background: var(--duo-light);
  color: var(--duo-dark);
  border: none;
  font-weight: 900;
  text-transform: uppercase;
  padding: 16px 32px;
}
```

## App 实现

### SwiftUI
```swift
struct DuotoneImage: View {
    let duoDark = Color(red: 0.12, green: 0.0, blue: 0.27)  // #1E0045
    let duoLight = Color(red: 0.8, green: 1.0, blue: 0.0)   // #CCFF00
    
    var body: some View {
        ZStack {
            // 基础背景色
            duoLight.ignoresSafeArea()
            
            // 图像处理
            Image("sample_photo")
                .resizable()
                .scaledToFill()
                .grayscale(1.0)
                .contrast(1.5)
                .colorMultiply(duoLight) // 将浅色乘到灰度中
            
            // 深色叠加
            duoDark
                .blendMode(.screen) // 等价于 CSS screen 混合模式
                .allowsHitTesting(false)
        }
        .frame(height: 400)
        .clipped()
    }
}
```
- 在 SwiftUI 中实时图像处理非常简单。
- 转为 `.grayscale()`，提升 `.contrast()`，然后使用 `.colorMultiply()` 和 `.blendMode(.screen)` 图层，精确映射两种颜色，与 CSS `mix-blend-mode` 一致。

### Flutter
```dart
class DuotoneImage extends StatelessWidget {
  final Color duoDark = const Color(0xFF1E0045);
  final Color duoLight = const Color(0xFFCCFF00);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 400,
      width: double.infinity,
      color: duoLight,
      child: Stack(
        fit: StackFit.expand,
        children: [
          // 1. 灰度与对比（使用 ColorFilter 矩阵）
          // 2. 浅色相乘
          ColorFiltered(
            colorFilter: ColorFilter.mode(duoLight, BlendMode.multiply),
            child: ColorFiltered(
              // 简单灰度矩阵
              colorFilter: const ColorFilter.matrix([
                0.2126, 0.7152, 0.0722, 0, 0,
                0.2126, 0.7152, 0.0722, 0, 0,
                0.2126, 0.7152, 0.0722, 0, 0,
                0,      0,      0,      1, 0,
              ]),
              child: Image.asset('assets/sample_photo.jpg', fit: BoxFit.cover),
            ),
          ),
          // 3. 深色屏幕叠加
          ColorFiltered(
            colorFilter: ColorFilter.mode(duoDark, BlendMode.screen),
            child: Container(color: Colors.transparent), // 对下方栈应用滤镜
          ),
        ],
      ),
    );
  }
}
```
- Flutter 需要堆叠 `ColorFiltered` 控件。
- 使用 `ColorFilter.matrix` 将图像转为灰度。
- 使用浅色应用 `BlendMode.multiply`，然后使用深色叠加 `BlendMode.screen`。

### React Native
```jsx
// 实时 CSS-like 混合模式在 React Native 中原生不存在。
// 必须使用 react-native-skia 或预先处理图像。

import { Canvas, Image, useImage, ColorMatrix } from "@shopify/react-native-skia";

const DuotoneImage = () => {
  const image = useImage(require('./sample_photo.jpg'));
  
  if (!image) return null;

  // Skia 允许自定义 SVG/CSS 风格的颜色矩阵。
  // 构建真正的双色矩阵需要数学映射黑色到 duoDark、白色到 duoLight。
  
  return (
    <View style={{ height: 400, backgroundColor: '#CCFF00' }}>
      <Canvas style={{ flex: 1 }}>
        <Image image={image} x={0} y={0} width={400} height={400} fit="cover">
          {/* 在生产环境中，你需要构建特定的 
              ColorMatrix 将亮度映射到两种十六进制颜色。 */}
          <ColorMatrix
            matrix={[
              -1, 0, 0, 0, 255,
              0, -1, 0, 0, 255,
              0, 0, -1, 0, 255,
              0, 0, 0, 1, 0,
            ]}
          />
        </Image>
      </Canvas>
    </View>
  );
};
```
- **关键限制**：标准 React Native `<Image>` 无法进行双色混合。
- **方案一**：使用 `@shopify/react-native-skia` 应用底层颜色矩阵和混合模式。
- **方案二**：在 Photoshop/Figma 中预处理所有图像再导入应用。这是最安全、性能最高的方案。

### Jetpack Compose
```kotlin
@Composable
fun DuotoneImage() {
    val duoDark = Color(0xFF1E0045)
    val duoLight = Color(0xFFCCFF00)

    // 真正的双色需要 ColorMatrix 将亮度映射到两种颜色。
    // 为简便起见，这里使用 BlendMode 近似 CSS multiply/screen 效果。
    Box(modifier = Modifier
        .fillMaxWidth()
        .height(400.dp)
        .background(duoLight)
    ) {
        Image(
            painter = painterResource(id = R.drawable.sample_photo),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.matchParentSize(),
            colorFilter = ColorFilter.colorMatrix(ColorMatrix().apply { 
                setToSaturation(0f) // 灰度
            })
        )
        
        // 浅色相乘
        Spacer(modifier = Modifier
            .matchParentSize()
            .background(duoLight)
            .graphicsLayer { blendMode = BlendMode.Multiply }
        )
        
        // 深色屏幕
        Spacer(modifier = Modifier
            .matchParentSize()
            .background(duoDark)
            .graphicsLayer { blendMode = BlendMode.Screen }
        )
    }
}
```
- 使用 `ColorFilter.colorMatrix` 配合 `setToSaturation(0f)` 将图像转为灰度。
- 使用 `Spacer` 叠加配合 `Modifier.graphicsLayer { blendMode = BlendMode... }` 应用双重颜色映射。
- 与 Flutter 类似，叠加 `Multiply`（浅色）和 `Screen`（深色）来达到效果。

## 推荐与避免
- **推荐**：确保深色足够深，作为浅色背景下的文字使用时足够清晰。
- **避免**：添加第三种颜色。它会瞬间破坏美学。

## 限制
- 这是一个样式参考，不能替代特定环境的验证、可访问性测试或专家评审。
- 适当的对比度和响应式行为需要单独验证。