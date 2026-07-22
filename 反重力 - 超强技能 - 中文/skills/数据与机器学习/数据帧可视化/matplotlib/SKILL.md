---
name: matplotlib
description: "Matplotlib 是 Python 的基础可视化库，用于创建静态、动画和交互式图表。触发词：matplotlib、Python可视化、绘图、图表、数据可视化、plot、figure、axes、pyplot"
license: https://github.com/matplotlib/matplotlib/tree/main/LICENSE
metadata:
    skill-author: K-Dense Inc.
    risk: unknown
    source: community
---

# Matplotlib

## 概述

Matplotlib 是 Python 的基础可视化库，用于创建静态、动画和交互式图表。本技能提供有效使用 matplotlib 的指导，涵盖 pyplot 接口（MATLAB 风格）和面向对象 API（Figure/Axes），以及创建出版级可视化的最佳实践。

## 何时使用本技能

以下情况应使用本技能：
- 创建任何类型的图表（折线图、散点图、柱状图、直方图、热力图、等高线图等）
- 生成科学或统计可视化
- 自定义图表外观（颜色、样式、标签、图例）
- 创建包含多个子图的多面板图形
- 将可视化导出为各种格式（PNG、PDF、SVG 等）
- 构建交互式图表或动画
- 处理 3D 可视化
- 将图表集成到 Jupyter notebook 或 GUI 应用程序中

## 核心概念

### Matplotlib 层级结构

Matplotlib 使用对象的层级结构：

1. **Figure** - 所有图表元素的顶级容器
2. **Axes** - 实际显示数据的绘图区域（一个 Figure 可以包含多个 Axes）
3. **Artist** - 图形上所有可见的内容（线条、文本、刻度等）
4. **Axis** - 处理刻度和标签的数轴对象（x 轴、y 轴）

### 两种接口

**1. pyplot 接口（隐式，MATLAB 风格）**
```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
```
- 适合快速、简单的图表
- 自动维护状态
- 适合交互式工作和简单脚本

**2. 面向对象接口（显式）**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4])
ax.set_ylabel('some numbers')
plt.show()
```
- **推荐用于大多数场景**
- 对图形和坐标轴有更明确的控制
- 更适合包含多个子图的复杂图形
- 更易于维护和调试

## 常用工作流程

### 1. 基本图表创建

**单图工作流程：**
```python
import matplotlib.pyplot as plt
import numpy as np

# 创建图形和坐标轴（OO 接口 - 推荐）
fig, ax = plt.subplots(figsize=(10, 6))

# 生成并绘制数据
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# 自定义
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Trigonometric Functions')
ax.legend()
ax.grid(True, alpha=0.3)

# 保存和/或显示
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### 2. 多个子图

**创建子图布局：**
```python
# 方法 1：规则网格
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, y1)
axes[0, 1].scatter(x, y2)
axes[1, 0].bar(categories, values)
axes[1, 1].hist(data, bins=30)

# 方法 2：马赛克布局（更灵活）
fig, axes = plt.subplot_mosaic([['left', 'right_top'],
                                 ['left', 'right_bottom']],
                                figsize=(10, 8))
axes['left'].plot(x, y)
axes['right_top'].scatter(x, y)
axes['right_bottom'].hist(data)

# 方法 3：GridSpec（最大控制）
from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, :])  # 顶行，所有列
ax2 = fig.add_subplot(gs[1:, 0])  # 底部两行，第一列
ax3 = fig.add_subplot(gs[1:, 1:])  # 底部两行，后两列
```

### 3. 图表类型与使用场景

**折线图** - 时间序列、连续数据、趋势
```python
ax.plot(x, y, linewidth=2, linestyle='--', marker='o', color='blue')
```

**散点图** - 变量间关系、相关性
```python
ax.scatter(x, y, s=sizes, c=colors, alpha=0.6, cmap='viridis')
```

**柱状图** - 分类比较
```python
ax.bar(categories, values, color='steelblue', edgecolor='black')
# 水平柱状图：
ax.barh(categories, values)
```

**直方图** - 分布
```python
ax.hist(data, bins=30, edgecolor='black', alpha=0.7)
```

**热力图** - 矩阵数据、相关性
```python
im = ax.imshow(matrix, cmap='coolwarm', aspect='auto')
plt.colorbar(im, ax=ax)
```

**等高线图** - 2D 平面上的 3D 数据
```python
contour = ax.contour(X, Y, Z, levels=10)
ax.clabel(contour, inline=True, fontsize=8)
```

**箱线图** - 统计分布
```python
ax.boxplot([data1, data2, data3], labels=['A', 'B', 'C'])
```

**小提琴图** - 分布密度
```python
ax.violinplot([data1, data2, data3], positions=[1, 2, 3])
```

更多图表类型示例和变体，请参阅 `references/plot_types.md`。

### 4. 样式与自定义

**颜色指定方法：**
- 命名颜色：`'red'`、`'blue'`、`'steelblue'`
- 十六进制代码：`'#FF5733'`
- RGB 元组：`(0.1, 0.2, 0.3)`
- 色彩映射：`cmap='viridis'`、`cmap='plasma'`、`cmap='coolwarm'`

**使用样式表：**
```python
plt.style.use('seaborn-v0_8-darkgrid')  # 应用预定义样式
# 可用样式：'ggplot'、'bmh'、'fivethirtyeight' 等
print(plt.style.available)  # 列出所有可用样式
```

**使用 rcParams 自定义：**
```python
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 18
```

**文本和注释：**
```python
ax.text(x, y, 'annotation', fontsize=12, ha='center')
ax.annotate('important point', xy=(x, y), xytext=(x+1, y+1),
            arrowprops=dict(arrowstyle='->', color='red'))
```

详细的样式选项和色彩映射指南，请参阅 `references/styling_guide.md`。

### 5. 保存图形

**导出为各种格式：**
```python
# 用于演示/论文的高分辨率 PNG
plt.savefig('figure.png', dpi=300, bbox_inches='tight', facecolor='white')

# 用于出版的矢量格式（可缩放）
plt.savefig('figure.pdf', bbox_inches='tight')
plt.savefig('figure.svg', bbox_inches='tight')

# 透明背景
plt.savefig('figure.png', dpi=300, bbox_inches='tight', transparent=True)
```

**重要参数：**
- `dpi`：分辨率（出版物用 300，网页用 150，屏幕用 72）
- `bbox_inches='tight'`：移除多余空白
- `facecolor='white'`：确保白色背景（对透明主题有用）
- `transparent=True`：透明背景

### 6. 处理 3D 图表

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 曲面图
ax.plot_surface(X, Y, Z, cmap='viridis')

# 3D 散点图
ax.scatter(x, y, z, c=colors, marker='o')

# 3D 折线图
ax.plot(x, y, z, linewidth=2)

# 标签
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
```

## 最佳实践

### 1. 接口选择
- **使用面向对象接口**（fig, ax = plt.subplots()）用于生产代码
- 仅将 pyplot 接口用于快速交互式探索
- 始终显式创建图形，而非依赖隐式状态

### 2. 图形大小和 DPI
- 创建时设置 figsize：`fig, ax = plt.subplots(figsize=(10, 6))`
- 根据输出媒介使用适当的 DPI：
  - 屏幕/notebook：72-100 dpi
  - 网页：150 dpi
  - 打印/出版物：300 dpi

### 3. 布局管理
- 使用 `constrained_layout=True` 或 `tight_layout()` 防止元素重叠
- 推荐使用 `fig, ax = plt.subplots(constrained_layout=True)` 实现自动间距

### 4. 色彩映射选择
- **顺序型**（viridis、plasma、inferno）：具有一致递进的有序数据
- **发散型**（coolwarm、RdBu）：具有有意义中心点（如零）的数据
- **定性型**（tab10、Set3）：分类/名义数据
- 避免使用彩虹色彩映射（jet）- 它们在感知上不均匀

### 5. 无障碍性
- 使用色盲友好的色彩映射（viridis、cividis）
- 为柱状图添加图案/阴影，除颜色外增加区分度
- 确保元素之间有足够的对比度
- 包含描述性标签和图例

### 6. 性能
- 对于大数据集，在绘图调用中使用 `rasterized=True` 减小文件大小
- 绘图前使用适当的数据缩减（如对密集时间序列降采样）
- 对于动画，使用 blitting 提高性能

### 7. 代码组织
```python
# 良好实践：清晰的结构
def create_analysis_plot(data, title):
    """创建标准化分析图表。"""
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    # 绘制数据
    ax.plot(data['x'], data['y'], linewidth=2)

    # 自定义
    ax.set_xlabel('X Axis Label', fontsize=12)
    ax.set_ylabel('Y Axis Label', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    return fig, ax

# 使用函数
fig, ax = create_analysis_plot(my_data, 'My Analysis')
plt.savefig('analysis.png', dpi=300, bbox_inches='tight')
```

## 快速参考脚本

本技能在 `scripts/` 目录中包含辅助脚本：

### `plot_template.py`
演示各种图表类型和最佳实践的模板脚本。用作创建新可视化的起点。

**用法：**
```bash
python scripts/plot_template.py
```

### `style_configurator.py`
配置 matplotlib 样式偏好并生成自定义样式表的交互式工具。

**用法：**
```bash
python scripts/style_configurator.py
```

## 详细参考

如需全面信息，请查阅参考文档：

- **`references/plot_types.md`** - 图表类型完整目录，包含代码示例和使用场景
- **`references/styling_guide.md`** - 详细样式选项、色彩映射和自定义
- **`references/api_reference.md`** - 核心类和方法参考
- **`references/common_issues.md`** - 常见问题故障排除指南

## 与其他工具的集成

Matplotlib 与以下工具良好集成：
- **NumPy/Pandas** - 直接从数组和 DataFrame 绘图
- **Seaborn** - 基于 matplotlib 构建的高级统计可视化
- **Jupyter** - 使用 `%matplotlib inline` 或 `%matplotlib widget` 进行交互式绘图
- **GUI 框架** - 嵌入到 Tkinter、Qt、wxPython 应用程序中

## 常见陷阱

1. **元素重叠**：使用 `constrained_layout=True` 或 `tight_layout()`
2. **状态混乱**：使用 OO 接口避免 pyplot 状态机问题
3. **多个图形导致内存问题**：使用 `plt.close(fig)` 显式关闭图形
4. **字体警告**：安装字体或使用 `plt.rcParams['font.sans-serif']` 抑制警告
5. **DPI 困惑**：记住 figsize 单位是英寸，不是像素：`pixels = dpi * inches`

## 其他资源

- 官方文档：https://matplotlib.org/
- 画廊：https://matplotlib.org/stable/gallery/index.html
- 速查表：https://matplotlib.org/cheatsheets/
- 教程：https://matplotlib.org/stable/tutorials/index.html

## 限制
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
