# D3.js 比例尺参考

所有 d3 比例尺类型的完整指南，包含示例和用例。

## 连续比例尺

### 线性比例尺

使用线性插值将连续输入域映射到连续输出范围。

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

scale(50);  // 返回 250
scale(0);   // 返回 0
scale(100); // 返回 500

// 反转比例尺（从输出获取输入）
scale.invert(250); // 返回 50
```

**用例：**
- 定量数据最常用的比例尺
- 坐标轴、柱长、位置编码
- 温度、价格、计数、测量值

**方法：**
- `.domain([min, max])` - 设置输入域
- `.range([min, max])` - 设置输出范围
- `.invert(value)` - 从范围值获取域值
- `.clamp(true)` - 将输出限制在范围边界内
- `.nice()` - 将域扩展到整齐的整数值

### 幂比例尺

使用指数变换将连续输入映射到连续输出。

```javascript
const sqrtScale = d3.scalePow()
  .exponent(0.5)  // 平方根
  .domain([0, 100])
  .range([0, 500]);

const squareScale = d3.scalePow()
  .exponent(2)  // 平方
  .domain([0, 100])
  .range([0, 500]);

// 平方根的简写
const sqrtScale2 = d3.scaleSqrt()
  .domain([0, 100])
  .range([0, 500]);
```

**用例：**
- 感知缩放（人类感知是非线性的）
- 面积编码（使用平方根将值映射到圆半径）
- 强调小值或大值的差异

### 对数比例尺

使用对数变换将连续输入映射到连续输出。

```javascript
const logScale = d3.scaleLog()
  .domain([1, 1000])  // 必须为正数
  .range([0, 500]);

logScale(1);    // 返回 0
logScale(10);   // 返回 ~167
logScale(100);  // 返回 ~333
logScale(1000); // 返回 500
```

**用例：**
- 跨越多个数量级的数据
- 人口、GDP、财富分布
- 对数坐标轴
- 指数增长可视化

**重要：** 域值必须严格为正（>0）。

### 时间比例尺

专门用于时间数据的线性比例尺。

```javascript
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)])
  .range([0, 800]);

timeScale(new Date(2022, 0, 1)); // 返回 400

// 反转以获取日期
timeScale.invert(400); // 返回 2022 年中旬的 Date 对象
```

**用例：**
- 时间序列可视化
- 时间轴坐标轴
- 时间动画
- 基于日期的交互

**方法：**
- `.nice()` - 将域扩展到整齐的时间间隔
- `.ticks(count)` - 生成均匀间隔的刻度值
- 所有线性比例尺方法都适用

### 量化比例尺

将连续输入映射到离散输出桶。

```javascript
const quantizeScale = d3.scaleQuantize()
  .domain([0, 100])
  .range(['低', '中', '高']);

quantizeScale(25);  // 返回 '低'
quantizeScale(50);  // 返回 '中'
quantizeScale(75);  // 返回 '高'

// 获取阈值
quantizeScale.thresholds(); // 返回 [33.33, 66.67]
```

**用例：**
- 连续数据分箱
- 热力图颜色
- 风险类别（低/中/高）
- 年龄组、收入档次

### 分位数比例尺

基于分位数将连续输入映射到离散输出。

```javascript
const quantileScale = d3.scaleQuantile()
  .domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20, 24]) // 样本数据
  .range(['低', '中', '高']);

quantileScale(8);  // 根据分位数位置返回
quantileScale.quantiles(); // 返回分位数阈值
```

**用例：**
- 不论分布如何，创建等大小的组
- 基于百分位的分类
- 处理偏态分布

### 阈值比例尺

使用自定义阈值将连续输入映射到离散输出。

```javascript
const thresholdScale = d3.scaleThreshold()
  .domain([0, 10, 20])
  .range(['冰冻', '冷', '暖', '热']);

thresholdScale(-5);  // 返回 '冰冻'
thresholdScale(5);   // 返回 '冷'
thresholdScale(15);  // 返回 '暖'
thresholdScale(25);  // 返回 '热'
```

**用例：**
- 自定义断点
- 成绩等级（A、B、C、D、F）
- 温度类别
- 空气质量指数

## 序列比例尺

### 序列颜色比例尺

将连续输入映射到连续颜色渐变。

```javascript
const colourScale = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, 100]);

colourScale(0);   // 返回最浅的蓝色
colourScale(50);  // 返回中等蓝色
colourScale(100); // 返回最深的蓝色
```

**可用的插值器：**

**单色相：**
- `d3.interpolateBlues`, `d3.interpolateGreens`, `d3.interpolateReds`
- `d3.interpolateOranges`, `d3.interpolatePurples`, `d3.interpolateGreys`

**多色相：**
- `d3.interpolateViridis`, `d3.interpolateInferno`, `d3.interpolateMagma`
- `d3.interpolatePlasma`, `d3.interpolateWarm`, `d3.interpolateCool`
- `d3.interpolateCubehelixDefault`, `d3.interpolateTurbo`

**用例：**
- 热力图、分级统计地图
- 连续数据可视化
- 温度、海拔、密度

### 发散颜色比例尺

将连续输入映射到具有中点的发散颜色渐变。

```javascript
const divergingScale = d3.scaleDiverging(d3.interpolateRdBu)
  .domain([-10, 0, 10]);

divergingScale(-10); // 返回红色
divergingScale(0);   // 返回白色/中性色
divergingScale(10);  // 返回蓝色
```

**可用的插值器：**
- `d3.interpolateRdBu` - 红到蓝
- `d3.interpolateRdYlBu` - 红、黄、蓝
- `d3.interpolateRdYlGn` - 红、黄、绿
- `d3.interpolatePiYG` - 粉、黄、绿
- `d3.interpolateBrBG` - 棕、蓝绿
- `d3.interpolatePRGn` - 紫、绿
- `d3.interpolatePuOr` - 紫、橙
- `d3.interpolateRdGy` - 红、灰
- `d3.interpolateSpectral` - 彩虹光谱

**用例：**
- 具有有意义中点（零、平均值、中性）的数据
- 正/负值
- 高于/低于比较
- 相关矩阵

### 序列分位数比例尺

结合序列颜色与分位数映射。

```javascript
const sequentialQuantileScale = d3.scaleSequentialQuantile(d3.interpolateBlues)
  .domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20, 24]);

// 基于分位数位置映射
```

**用例：**
- 感知均匀的分箱
- 处理异常值
- 偏态分布

## 序数比例尺

### 带状比例尺

将离散输入映射到连续带（矩形），可选填充。

```javascript
const bandScale = d3.scaleBand()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.1);

bandScale('A');           // 返回起始位置（如 0）
bandScale('B');           // 返回起始位置（如 110）
bandScale.bandwidth();    // 返回每个带的宽度（如 95）
bandScale.step();         // 返回包含填充的总步长
bandScale.paddingInner(); // 返回内部填充（带之间）
bandScale.paddingOuter(); // 返回外部填充（边缘处）
```

**用例：**
- 柱状图（最常用例）
- 分组元素
- 分类坐标轴
- 热力图单元格

**填充选项：**
- `.padding(value)` - 同时设置内部和外部填充（0-1）
- `.paddingInner(value)` - 带之间的填充（0-1）
- `.paddingOuter(value)` - 边缘处的填充（0-1）
- `.align(value)` - 带的对齐方式（0-1，默认 0.5）

### 点比例尺

将离散输入映射到连续点（无宽度）。

```javascript
const pointScale = d3.scalePoint()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.5);

pointScale('A'); // 返回位置（如 50）
pointScale('B'); // 返回位置（如 150）
pointScale('C'); // 返回位置（如 250）
pointScale('D'); // 返回位置（如 350）
pointScale.step(); // 返回点之间的距离
```

**用例：**
- 折线图分类 x 轴
- 带分类轴的散点图
- 网络图中的节点位置
- 分类的任何点定位

### 序数颜色比例尺

将离散输入映射到离散输出（颜色、形状等）。

```javascript
const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

colourScale('苹果');  // 返回第一种颜色
colourScale('橙子'); // 返回第二种颜色
colourScale('苹果');  // 返回相同的第一种颜色（一致）

// 自定义范围
const customScale = d3.scaleOrdinal()
  .domain(['类别1', '类别2', '类别3'])
  .range(['#FF6B6B', '#4ECDC4', '#45B7D1']);
```

**内置颜色方案：**

**分类：**
- `d3.schemeCategory10` - 10 种颜色
- `d3.schemeAccent` - 8 种颜色
- `d3.schemeDark2` - 8 种颜色
- `d3.schemePaired` - 12 种颜色
- `d3.schemePastel1` - 9 种颜色
- `d3.schemePastel2` - 8 种颜色
- `d3.schemeSet1` - 9 种颜色
- `d3.schemeSet2` - 8 种颜色
- `d3.schemeSet3` - 12 种颜色
- `d3.schemeTableau10` - 10 种颜色

**用例：**
- 类别颜色
- 图例项
- 多系列图表
- 网络节点类型

## 比例尺工具

### 整齐域

将域扩展到整齐的整数值。

```javascript
const scale = d3.scaleLinear()
  .domain([0.201, 0.996])
  .nice();

scale.domain(); // 返回 [0.2, 1.0]

// 带数量（近似刻度数量）
const scale2 = d3.scaleLinear()
  .domain([0.201, 0.996])
  .nice(5);
```

### 钳制

将输出限制在范围边界内。

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500])
  .clamp(true);

scale(-10); // 返回 0（被钳制）
scale(150); // 返回 500（被钳制）
```

### 复制比例尺

创建独立副本。

```javascript
const scale1 = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

const scale2 = scale1.copy();
// scale2 独立于 scale1
```

### 刻度生成

为坐标轴生成整齐的刻度值。

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

scale.ticks(10);        // 生成约 10 个刻度
scale.tickFormat(10);   // 获取刻度的格式化函数
scale.tickFormat(10, ".2f"); // 自定义格式（2 位小数）

// 时间比例尺刻度
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)]);

timeScale.ticks(d3.timeYear);      // 年度刻度
timeScale.ticks(d3.timeMonth, 3);  // 每 3 个月
timeScale.tickFormat(5, "%Y-%m");  // 格式化为年-月
```

## 颜色空间和插值

### RGB 插值

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"]);
// 默认：RGB 插值
```

### HSL 插值

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"])
  .interpolate(d3.interpolateHsl);
// 更平滑的颜色过渡
```

### Lab 插值

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"])
  .interpolate(d3.interpolateLab);
// 感知均匀
```

### HCL 插值

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"])
  .interpolate(d3.interpolateHcl);
// 带色调的感知均匀
```

## 常见模式

### 带自定义中点的发散比例尺

```javascript
const scale = d3.scaleLinear()
  .domain([min, midpoint, max])
  .range(["red", "white", "blue"])
  .interpolate(d3.interpolateHcl);
```

### 多停止点渐变比例尺

```javascript
const scale = d3.scaleLinear()
  .domain([0, 25, 50, 75, 100])
  .range(["#d53e4f", "#fc8d59", "#fee08b", "#e6f598", "#66c2a5"]);
```

### 圆形半径比例尺（感知）

```javascript
const radiusScale = d3.scaleSqrt()
  .domain([0, d3.max(data, d => d.value)])
  .range([0, 50]);

// 用于圆形
circle.attr("r", d => radiusScale(d.value));
```

### 基于数据范围的自适应比例尺

```javascript
function createAdaptiveScale(data) {
  const extent = d3.extent(data);
  const range = extent[1] - extent[0];
  
  // 如果数据跨越 >2 个数量级则使用对数比例尺
  if (extent[1] / extent[0] > 100) {
    return d3.scaleLog()
      .domain(extent)
      .range([0, width]);
  }
  
  // 否则使用线性
  return d3.scaleLinear()
    .domain(extent)
    .range([0, width]);
}
```

### 带显式类别的颜色比例尺

```javascript
const colourScale = d3.scaleOrdinal()
  .domain(['低风险', '中风险', '高风险'])
  .range(['#2ecc71', '#f39c12', '#e74c3c'])
  .unknown('#95a5a6'); // 未知值的回退颜色
```
