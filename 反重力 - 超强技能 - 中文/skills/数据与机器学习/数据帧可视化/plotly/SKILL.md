---
name: plotly
description: 交互式可视化库。当需要悬停信息、缩放、平移或可嵌入网页的图表时使用。最适合仪表盘、探索性分析和演示。静态出版级图表请使用 matplotlib 或 scientific-visualization。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
risk: unknown
source: community
---

# Plotly

Python 图形库，用于创建交互式、出版级可视化，支持 40+ 种图表类型。

## 何时使用

- 需要带有悬停、缩放、平移或网页嵌入功能的交互式图表。
- 正在构建仪表盘、探索性分析笔记本或受益于丰富交互的演示文稿。
- 想要在 Plotly Express 和 Graph Objects 之间选择合适的可视化方案。

## 快速开始

安装 Plotly：
```bash
uv pip install plotly
```

使用 Plotly Express（高级 API）的基本用法：
```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13]
})

fig = px.scatter(df, x='x', y='y', title='My First Plot')
fig.show()
```

## API 选择指南

### 使用 Plotly Express (px)

快速创建标准可视化，具有合理的默认设置：
- 处理 pandas DataFrame
- 创建常见图表类型（散点图、折线图、柱状图、直方图等）
- 需要自动颜色编码和图例
- 希望代码简洁（1-5 行）

完整指南见 reference/plotly-express.md。

### 使用 Graph Objects (go)

精细控制和自定义可视化：
- Plotly Express 不支持的图表类型（3D 网格、等值面、复杂金融图表）
- 从零构建复杂的多轨迹图形
- 需要精确控制各个组件
- 创建带有自定义形状和标注的专业可视化

完整指南见 reference/graph-objects.md。

**注意：** Plotly Express 返回 graph objects Figure，因此可以组合使用：
```python
fig = px.scatter(df, x='x', y='y')
fig.update_layout(title='Custom Title')  # 在 px 图形上使用 go 方法
fig.add_hline(y=10)                     # 添加形状
```

## 核心能力

### 1. 图表类型

Plotly 支持 40+ 种图表类型，按类别组织：

**基础图表：** 散点图、折线图、柱状图、饼图、面积图、气泡图

**统计图表：** 直方图、箱线图、小提琴图、分布图、误差条

**科学图表：** 热力图、等高线图、三元图、图像显示

**金融图表：** K线图、OHLC图、瀑布图、漏斗图、时间序列

**地图：** 散点地图、分级统计地图、密度地图（地理可视化）

**3D 图表：** scatter3d、曲面图、网格图、锥形图、体积图

**专业图表：** 旭日图、树图、桑基图、平行坐标图、仪表盘

所有图表类型的详细示例和用法见 reference/chart-types.md。

### 2. 布局与样式

**子图：** 创建共享坐标轴的多图布局：
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=2, cols=2, subplot_titles=('A', 'B', 'C', 'D'))
fig.add_trace(go.Scatter(x=[1, 2], y=[3, 4]), row=1, col=1)
```

**模板：** 应用协调的样式：
```python
fig = px.scatter(df, x='x', y='y', template='plotly_dark')
# 内置模板：plotly_white, plotly_dark, ggplot2, seaborn, simple_white
```

**自定义：** 控制外观的各个方面：
- 颜色（离散序列、连续色阶）
- 字体和文本
- 坐标轴（范围、刻度、网格）
- 图例
- 边距和尺寸
- 标注和形状

完整的布局和样式选项见 reference/layouts-styling.md。

### 3. 交互性

内置交互功能：
- 可自定义数据的悬停工具提示
- 平移和缩放
- 图例切换
- 框选/套索选择
- 时间序列的范围滑块
- 按钮和下拉菜单
- 动画

```python
# 自定义悬停模板
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
)

# 添加范围滑块
fig.update_xaxes(rangeslider_visible=True)

# 动画
fig = px.scatter(df, x='x', y='y', animation_frame='year')
```

完整的交互指南见 reference/export-interactivity.md。

### 4. 导出选项

**交互式 HTML：**
```python
fig.write_html('chart.html')                       # 完整独立文件
fig.write_html('chart.html', include_plotlyjs='cdn')  # 更小的文件
```

**静态图像（需要 kaleido）：**
```bash
uv pip install kaleido
```

```python
fig.write_image('chart.png')   # PNG
fig.write_image('chart.pdf')   # PDF
fig.write_image('chart.svg')   # SVG
```

完整的导出选项见 reference/export-interactivity.md。

## 常见工作流

### 科学数据可视化

```python
import plotly.express as px

# 带趋势线的散点图
fig = px.scatter(df, x='temperature', y='yield', trendline='ols')

# 矩阵热力图
fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='RdBu')

# 3D 曲面图
import plotly.graph_objects as go
fig = go.Figure(data=[go.Surface(z=z_data, x=x_data, y=y_data)])
```

### 统计分析

```python
# 分布比较
fig = px.histogram(df, x='values', color='group', marginal='box', nbins=30)

# 显示所有点的箱线图
fig = px.box(df, x='category', y='value', points='all')

# 小提琴图
fig = px.violin(df, x='group', y='measurement', box=True)
```

### 时间序列与金融

```python
# 带范围滑块的时间序列
fig = px.line(df, x='date', y='price')
fig.update_xaxes(rangeslider_visible=True)

# K线图
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
```

### 多图仪表盘

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('散点图', '柱状图', '直方图', '箱线图'),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'histogram'}, {'type': 'box'}]]
)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=['A', 'B'], y=[1, 2]), row=1, col=2)
fig.add_trace(go.Histogram(x=data), row=2, col=1)
fig.add_trace(go.Box(y=data), row=2, col=2)

fig.update_layout(height=800, showlegend=False)
```

## 与 Dash 集成

对于交互式 Web 应用，使用 Dash（Plotly 的 Web 应用框架）：

```bash
uv pip install dash
```

```python
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

fig = px.scatter(df, x='x', y='y')

app.layout = html.Div([
    html.H1('Dashboard'),
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)
```

## 参考文件

- **plotly-express.md** - 快速可视化高级 API
- **graph-objects.md** - 精细控制低级 API
- **chart-types.md** - 40+ 种图表类型完整目录及示例
- **layouts-styling.md** - 子图、模板、颜色、自定义
- **export-interactivity.md** - 导出选项和交互功能

## 其他资源

- 官方文档：https://plotly.com/python/
- API 参考：https://plotly.com/python-api-reference/
- 社区论坛：https://community.plotly.com/

## 限制

- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
