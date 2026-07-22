# D3.js 配色方案与调色板推荐

使用 d3.js 进行数据可视化时的配色综合指南。

## 内置分类配色方案

### Category10（默认）

```javascript
d3.schemeCategory10
// ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
//  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
```

**特点：**
- 10 种不同的颜色
- 良好的色盲可访问性
- 大多数分类数据的默认选择
- 饱和度和亮度均衡

**使用场景：** 通用分类编码、图例项、多个数据系列

### Tableau10

```javascript
d3.schemeTableau10
```

**特点：**
- 10 种专为数据可视化优化的颜色
- 专业外观
- 出色的可区分性

**使用场景：** 商业仪表板、专业报告、演示文稿

### Accent

```javascript
d3.schemeAccent
// 8 种高饱和度颜色
```

**特点：**
- 明亮、鲜艳的颜色
- 高对比度
- 现代美学

**使用场景：** 突出重要类别、现代 Web 应用

### Dark2

```javascript
d3.schemeDark2
// 8 种较暗、柔和的颜色
```

**特点：**
- 柔和的调色板
- 专业外观
- 适合深色背景

**使用场景：** 深色模式可视化、专业场景

### Paired

```javascript
d3.schemePaired
// 12 种相似色相的颜色对
```

**特点：**
- 浅色和深色变体对
- 适用于嵌套类别
- 12 种不同的颜色

**使用场景：** 分组柱状图、层级类别、前后对比

### Pastel1 和 Pastel2

```javascript
d3.schemePastel1 // 9 种颜色
d3.schemePastel2 // 8 种颜色
```

**特点：**
- 柔和、低饱和度的颜色
- 温和的外观
- 适合大面积使用

**使用场景：** 背景色、细微分类、平静的可视化

### Set1、Set2、Set3

```javascript
d3.schemeSet1 // 9 种颜色 - 鲜艳
d3.schemeSet2 // 8 种颜色 - 柔和
d3.schemeSet3 // 12 种颜色 - 粉彩
```

**特点：**
- Set1：高饱和度，最大区分度
- Set2：专业、均衡
- Set3：细腻，多类别

**使用场景：** 根据视觉层级需求选择

## 顺序配色方案

顺序方案使用单一色相或渐变将连续数据从低值映射到高值。

### 单色相顺序

**蓝色：**
```javascript
d3.interpolateBlues
d3.schemeBlues[9] // 9 级离散版本
```

**其他单色相选项：**
- `d3.interpolateGreens` / `d3.schemeGreens`
- `d3.interpolateOranges` / `d3.schemeOranges`
- `d3.interpolatePurples` / `d3.schemePurples`
- `d3.interpolateReds` / `d3.schemeReds`
- `d3.interpolateGreys` / `d3.schemeGreys`

**使用场景：**
- 简单热力图
- 等值区域图
- 密度图
- 单指标可视化

### 多色相顺序

**Viridis（推荐）：**
```javascript
d3.interpolateViridis
```

**特点：**
- 感知均匀
- 色盲友好
- 打印安全
- 无视觉死角
- 感知亮度单调递增

**其他感知均匀选项：**
- `d3.interpolatePlasma` - 紫色到黄色
- `d3.interpolateInferno` - 黑色经红色/橙色到白色
- `d3.interpolateMagma` - 黑色经紫色到白色
- `d3.interpolateCividis` - 色盲优化

**色盲可访问：**
```javascript
d3.interpolateTurbo // 彩虹状但感知均匀
d3.interpolateCool  // 青色到品红色
d3.interpolateWarm  // 橙色到黄色
```

**使用场景：**
- 科学可视化
- 医学成像
- 任何高精度数据可视化
- 可访问性可视化

### 传统顺序

**黄-橙-红：**
```javascript
d3.interpolateYlOrRd
d3.schemeYlOrRd[9]
```

**黄-绿-蓝：**
```javascript
d3.interpolateYlGnBu
d3.schemeYlGnBu[9]
```

**其他多色相：**
- `d3.interpolateBuGn` - 蓝色到绿色
- `d3.interpolateBuPu` - 蓝色到紫色
- `d3.interpolateGnBu` - 绿色到蓝色
- `d3.interpolateOrRd` - 橙色到红色
- `d3.interpolatePuBu` - 紫色到蓝色
- `d3.interpolatePuBuGn` - 紫色到蓝绿色
- `d3.interpolatePuRd` - 紫色到红色
- `d3.interpolateRdPu` - 红色到紫色
- `d3.interpolateYlGn` - 黄色到绿色
- `d3.interpolateYlOrBr` - 黄色到橙棕色

**使用场景：** 传统数据可视化、熟悉的颜色关联（温度、植被、水体）

## 发散配色方案

发散方案使用两种不同的色相突出偏离中心值的情况。

### 红-蓝（温度）

```javascript
d3.interpolateRdBu
d3.schemeRdBu[11]
```

**特点：**
- 直觉的温度隐喻
- 强对比度
- 清晰的正/负区分

**使用场景：** 温度、盈利/亏损、高于/低于平均值、相关性

### 红-黄-蓝

```javascript
d3.interpolateRdYlBu
d3.schemeRdYlBu[11]
```

**特点：**
- 三色渐变
- 经黄色的柔和过渡
- 更多视觉层次

**使用场景：** 需要强调极值且中间值需要可见性时

### 其他发散方案

**交通信号灯：**
```javascript
d3.interpolateRdYlGn // 红色（差）到绿色（好）
```

**光谱（彩虹）：**
```javascript
d3.interpolateSpectral // 全光谱
```

**其他选项：**
- `d3.interpolateBrBG` - 棕色到蓝绿色
- `d3.interpolatePiYG` - 粉色到黄绿色
- `d3.interpolatePRGn` - 紫色到绿色
- `d3.interpolatePuOr` - 紫色到橙色
- `d3.interpolateRdGy` - 红色到灰色

**使用场景：** 根据语义含义和可访问性需求选择

## 色盲友好调色板

### 通用指南

1. **避免红绿组合**（最常见的色盲类型）
2. **使用蓝橙发散**代替红绿
3. **添加纹理或图案**作为冗余编码
4. **使用模拟工具测试**

### 推荐的色盲安全方案

**分类：**
```javascript
// Okabe-Ito 调色板（色盲安全）
const okabePalette = [
  '#E69F00', // Orange
  '#56B4E9', // Sky blue
  '#009E73', // Bluish green
  '#F0E442', // Yellow
  '#0072B2', // Blue
  '#D55E00', // Vermillion
  '#CC79A7', // Reddish purple
  '#000000'  // Black
];

const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(okabePalette);
```

**顺序：**
```javascript
// 使用 Viridis、Cividis 或 Blues
d3.interpolateViridis  // 整体最佳
d3.interpolateCividis  // 针对 CVD 优化
d3.interpolateBlues    // 简单、安全
```

**发散：**
```javascript
// 使用蓝橙代替红绿
d3.interpolateBrBG
d3.interpolatePuOr
```

## 自定义调色板

### 创建自定义顺序

```javascript
const customSequential = d3.scaleLinear()
  .domain([0, 100])
  .range(['#e8f4f8', '#006d9c']) // Light to dark blue
  .interpolate(d3.interpolateLab); // Perceptually uniform
```

### 创建自定义发散

```javascript
const customDiverging = d3.scaleLinear()
  .domain([0, 50, 100])
  .range(['#ca0020', '#f7f7f7', '#0571b0']) // Red, grey, blue
  .interpolate(d3.interpolateLab);
```

### 创建自定义分类

```javascript
// Brand colours
const brandPalette = [
  '#FF6B6B', // Primary red
  '#4ECDC4', // Secondary teal
  '#45B7D1', // Tertiary blue
  '#FFA07A', // Accent coral
  '#98D8C8'  // Accent mint
];

const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(brandPalette);
```

## 语义颜色关联

### 通用颜色含义

**红色：**
- 危险、错误、负面
- 高温
- 负债、亏损

**绿色：**
- 成功、正面
- 增长、植被
- 利润、收益

**蓝色：**
- 信任、平静
- 水、寒冷
- 信息、中性

**黄色/橙色：**
- 警告、注意
- 能量、温暖
- 关注

**灰色：**
- 中性、非活动
- 缺失数据
- 背景

### 特定场景调色板

**金融：**
```javascript
const financialColours = {
  profit: '#27ae60',
  loss: '#e74c3c',
  neutral: '#95a5a6',
  highlight: '#3498db'
};
```

**温度：**
```javascript
const temperatureScale = d3.scaleSequential(d3.interpolateRdYlBu)
  .domain([40, -10]); // Hot to cold (reversed)
```

**交通/状态：**
```javascript
const statusColours = {
  success: '#27ae60',
  warning: '#f39c12',
  error: '#e74c3c',
  info: '#3498db',
  neutral: '#95a5a6'
};
```

## 可访问性最佳实践

### 对比度比率

确保颜色与背景之间有足够的对比度：

```javascript
// Good contrast example
const highContrast = {
  background: '#ffffff',
  text: '#2c3e50',
  primary: '#3498db',
  secondary: '#e74c3c'
};
```

**WCAG 指南：**
- 普通文本：最低 4.5:1
- 大号文本：最低 3:1
- UI 组件：最低 3:1

### 冗余编码

切勿仅依赖颜色传达信息：

```javascript
// Add patterns or shapes
const symbols = ['circle', 'square', 'triangle', 'diamond'];

// Add text labels
// Use line styles (solid, dashed, dotted)
// Use size encoding
```

### 测试

测试可视化效果的色盲可访问性：
- Chrome DevTools（Rendering > Emulate vision deficiencies）
- Colour Oracle（免费桌面应用）
- Coblis（在线模拟器）

## 专业配色推荐

### 数据新闻

```javascript
// Guardian style
const guardianPalette = [
  '#005689', // Guardian blue
  '#c70000', // Guardian red
  '#7d0068', // Guardian pink
  '#951c75', // Guardian purple
];

// FT style
const ftPalette = [
  '#0f5499', // FT blue
  '#990f3d', // FT red
  '#593380', // FT purple
  '#262a33', // FT black
];
```

### 学术/科学

```javascript
// Nature journal style
const naturePalette = [
  '#0071b2', // Blue
  '#d55e00', // Vermillion
  '#009e73', // Green
  '#f0e442', // Yellow
];

// Use Viridis for continuous data
const scientificScale = d3.scaleSequential(d3.interpolateViridis);
```

### 企业/商业

```javascript
// Professional, conservative
const corporatePalette = [
  '#003f5c', // Dark blue
  '#58508d', // Purple
  '#bc5090', // Magenta
  '#ff6361', // Coral
  '#ffa600'  // Orange
];
```

## 动态颜色选择

### 基于数据范围

```javascript
function selectColourScheme(data) {
  const extent = d3.extent(data);
  const hasNegative = extent[0] < 0;
  const hasPositive = extent[1] > 0;
  
  if (hasNegative && hasPositive) {
    // Diverging: data crosses zero
    return d3.scaleSequentialSymlog(d3.interpolateRdBu)
      .domain([extent[0], 0, extent[1]]);
  } else {
    // Sequential: all positive or all negative
    return d3.scaleSequential(d3.interpolateViridis)
      .domain(extent);
  }
}
```

### 基于类别数量

```javascript
function selectCategoricalScheme(categories) {
  const n = categories.length;
  
  if (n <= 10) {
    return d3.scaleOrdinal(d3.schemeTableau10);
  } else if (n <= 12) {
    return d3.scaleOrdinal(d3.schemePaired);
  } else {
    // For many categories, use sequential with quantize
    return d3.scaleQuantize()
      .domain([0, n - 1])
      .range(d3.quantize(d3.interpolateRainbow, n));
  }
}
```

## 常见配色错误

1. **顺序数据使用彩虹渐变**
   - 问题：非感知均匀，难以阅读
   - 解决方案：使用 Viridis、Blues 或其他均匀方案

2. **发散数据使用红绿色（色盲问题）**
   - 问题：8% 的男性无法区分
   - 解决方案：使用蓝橙或紫绿

3. **分类颜色过多**
   - 问题：难以区分和记忆
   - 解决方案：限制在 5-8 个类别，使用分组

4. **对比度不足**
   - 问题：可读性差
   - 解决方案：测试对比度比率，浅色背景使用深色

5. **文化不一致的颜色**
   - 问题：语义含义混淆
   - 解决方案：研究目标受众的颜色关联

6. **温度刻度反转**
   - 问题：违反直觉（红色 = 冷）
   - 解决方案：红/橙 = 热，蓝色 = 冷

## 快速参考指南

**需要展示...**

- **类别（≤10）：** `d3.schemeCategory10` 或 `d3.schemeTableau10`
- **类别（>10）：** `d3.schemePaired` 或分组类别
- **顺序（通用）：** `d3.interpolateViridis`
- **顺序（科学）：** `d3.interpolateViridis` 或 `d3.interpolatePlasma`
- **顺序（温度）：** `d3.interpolateRdYlBu`（反转）
- **发散（零点）：** `d3.interpolateRdBu` 或 `d3.interpolateBrBG`
- **发散（好/坏）：** `d3.interpolateRdYlGn`（反转）
- **色盲安全（分类）：** Okabe-Ito 调色板（见上文）
- **色盲安全（顺序）：** `d3.interpolateCividis` 或 `d3.interpolateBlues`
- **色盲安全（发散）：** `d3.interpolatePuOr` 或 `d3.interpolateBrBG`

**始终记住：**
1. 测试色盲可访问性
2. 确保足够的对比度
3. 适当使用语义颜色
4. 添加冗余编码（图案、标签）
5. 保持简洁（颜色越少 = 可视化越清晰）
