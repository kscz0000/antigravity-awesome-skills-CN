---
name: networkx
description: "NetworkX 是一个用于创建、操作和分析复杂网络与图的 Python 包。当用户需要处理网络或图数据结构、社交网络分析、生物网络、交通系统、引用网络、知识图谱，或任何涉及实体间关系的系统时使用此技能。"
license: 3-clause BSD license
metadata:
    skill-author: K-Dense Inc.
risk: unknown
source: "https://github.com/networkx/networkx"
---

# NetworkX

## 概述

NetworkX 是一个用于创建、操作和分析复杂网络与图的 Python 包。当处理网络或图数据结构时使用此技能，包括社交网络、生物网络、交通系统、引用网络、知识图谱，或任何涉及实体间关系的系统。

## 何时使用此技能

当任务涉及以下内容时调用此技能：

- **创建图**：从数据构建网络结构，添加带有属性的节点和边
- **图分析**：计算中心性度量、寻找最短路径、检测社区、测量聚类
- **图算法**：运行标准算法，如 Dijkstra、PageRank、最小生成树、最大流
- **网络生成**：创建合成网络（随机、无标度、小世界模型）用于测试或模拟
- **图 I/O**：读取或写入各种格式（边列表、GraphML、JSON、CSV、邻接矩阵）
- **可视化**：使用 matplotlib 或交互式库绘制和自定义网络可视化
- **网络比较**：检查同构、计算图度量、分析结构属性

## 核心能力

### 1. 图创建与操作

NetworkX 支持四种主要图类型：
- **Graph**：具有单条边的无向图
- **DiGraph**：具有单向连接的有向图
- **MultiGraph**：允许节点间多条边的无向图
- **MultiDiGraph**：具有多条边的有向图

创建图的方式：
```python
import networkx as nx

# 创建空图
G = nx.Graph()

# 添加节点（可以是任何可哈希类型）
G.add_node(1)
G.add_nodes_from([2, 3, 4])
G.add_node("protein_A", type='enzyme', weight=1.5)

# 添加边
G.add_edge(1, 2)
G.add_edges_from([(1, 3), (2, 4)])
G.add_edge(1, 4, weight=0.8, relation='interacts')
```

**参考**：参见 `references/graph-basics.md` 获取关于创建、修改、检查和管理图结构的全面指南，包括使用属性和子图。

### 2. 图算法

NetworkX 提供丰富的网络分析算法：

**最短路径**：
```python
# 查找最短路径
path = nx.shortest_path(G, source=1, target=5)
length = nx.shortest_path_length(G, source=1, target=5, weight='weight')
```

**中心性度量**：
```python
# 度中心性
degree_cent = nx.degree_centrality(G)

# 介数中心性
betweenness = nx.betweenness_centrality(G)

# PageRank
pagerank = nx.pagerank(G)
```

**社区检测**：
```python
from networkx.algorithms import community

# 检测社区
communities = community.greedy_modularity_communities(G)
```

**连通性**：
```python
# 检查连通性
is_connected = nx.is_connected(G)

# 查找连通分量
components = list(nx.connected_components(G))
```

**参考**：参见 `references/algorithms.md` 获取所有可用算法的详细文档，包括最短路径、中心性度量、聚类、社区检测、流、匹配、树算法和图遍历。

### 3. 图生成器

创建用于测试、模拟或建模的合成网络：

**经典图**：
```python
# 完全图
G = nx.complete_graph(n=10)

# 环图
G = nx.cycle_graph(n=20)

# 知名图
G = nx.karate_club_graph()
G = nx.petersen_graph()
```

**随机网络**：
```python
# Erdős-Rényi 随机图
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)

# Barabási-Albert 无标度网络
G = nx.barabasi_albert_graph(n=100, m=3, seed=42)

# Watts-Strogatz 小世界网络
G = nx.watts_strogatz_graph(n=100, k=6, p=0.1, seed=42)
```

**结构化网络**：
```python
# 网格图
G = nx.grid_2d_graph(m=5, n=7)

# 随机树
G = nx.random_tree(n=100, seed=42)
```

**参考**：参见 `references/generators.md` 获取所有图生成器的全面覆盖，包括经典图、随机图、格子图、二部图和专用网络模型及其详细参数和用例。

### 4. 图的读取与写入

NetworkX 支持多种文件格式和数据源：

**文件格式**：
```python
# 边列表
G = nx.read_edgelist('graph.edgelist')
nx.write_edgelist(G, 'graph.edgelist')

# GraphML（保留属性）
G = nx.read_graphml('graph.graphml')
nx.write_graphml(G, 'graph.graphml')

# GML
G = nx.read_gml('graph.gml')
nx.write_gml(G, 'graph.gml')

# JSON
data = nx.node_link_data(G)
G = nx.node_link_graph(data)
```

**Pandas 集成**：
```python
import pandas as pd

# 从 DataFrame 创建
df = pd.DataFrame({'source': [1, 2, 3], 'target': [2, 3, 4], 'weight': [0.5, 1.0, 0.75]})
G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight')

# 转换为 DataFrame
df = nx.to_pandas_edgelist(G)
```

**矩阵格式**：
```python
import numpy as np

# 邻接矩阵
A = nx.to_numpy_array(G)
G = nx.from_numpy_array(A)

# 稀疏矩阵
A = nx.to_scipy_sparse_array(G)
G = nx.from_scipy_sparse_array(A)
```

**参考**：参见 `references/io.md` 获取所有 I/O 格式的完整文档，包括 CSV、SQL 数据库、Cytoscape、DOT，以及不同用例的格式选择指南。

### 5. 可视化

创建清晰且信息丰富的网络可视化：

**基础可视化**：
```python
import matplotlib.pyplot as plt

# 简单绘制
nx.draw(G, with_labels=True)
plt.show()

# 带布局
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', node_size=500)
plt.show()
```

**自定义**：
```python
# 按度数着色
node_colors = [G.degree(n) for n in G.nodes()]
nx.draw(G, node_color=node_colors, cmap=plt.cm.viridis)

# 按中心性调整大小
centrality = nx.betweenness_centrality(G)
node_sizes = [3000 * centrality[n] for n in G.nodes()]
nx.draw(G, node_size=node_sizes)

# 边权重
edge_widths = [3 * G[u][v].get('weight', 1) for u, v in G.edges()]
nx.draw(G, width=edge_widths)
```

**布局算法**：
```python
# 弹簧布局（力导向）
pos = nx.spring_layout(G, seed=42)

# 环形布局
pos = nx.circular_layout(G)

# Kamada-Kawai 布局
pos = nx.kamada_kawai_layout(G)

# 谱布局
pos = nx.spectral_layout(G)
```

**出版质量**：
```python
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, node_color='lightblue', node_size=500,
        edge_color='gray', with_labels=True, font_size=10)
plt.title('Network Visualization', fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.savefig('network.png', dpi=300, bbox_inches='tight')
plt.savefig('network.pdf', bbox_inches='tight')  # 矢量格式
```

**参考**：参见 `references/visualization.md` 获取可视化技术的详尽文档，包括布局算法、自定义选项、使用 Plotly 和 PyVis 的交互式可视化、3D 网络，以及出版质量图表的创建。

## 使用 NetworkX

### 安装

确保已安装 NetworkX：
```python
# 检查是否已安装
import networkx as nx
print(nx.__version__)

# 如需安装（通过 bash）
# uv pip install networkx
# uv pip install networkx[default]  # 包含可选依赖
```

### 常见工作流模式

大多数 NetworkX 任务遵循此模式：

1. **创建或加载图**：
   ```python
   # 从头创建
   G = nx.Graph()
   G.add_edges_from([(1, 2), (2, 3), (3, 4)])

   # 或从文件/数据加载
   G = nx.read_edgelist('data.txt')
   ```

2. **检查结构**：
   ```python
   print(f"Nodes: {G.number_of_nodes()}")
   print(f"Edges: {G.number_of_edges()}")
   print(f"Density: {nx.density(G)}")
   print(f"Connected: {nx.is_connected(G)}")
   ```

3. **分析**：
   ```python
   # 计算度量
   degree_cent = nx.degree_centrality(G)
   avg_clustering = nx.average_clustering(G)

   # 查找路径
   path = nx.shortest_path(G, source=1, target=4)

   # 检测社区
   communities = community.greedy_modularity_communities(G)
   ```

4. **可视化**：
   ```python
   pos = nx.spring_layout(G, seed=42)
   nx.draw(G, pos=pos, with_labels=True)
   plt.show()
   ```

5. **导出结果**：
   ```python
   # 保存图
   nx.write_graphml(G, 'analyzed_network.graphml')

   # 保存度量
   df = pd.DataFrame({
       'node': list(degree_cent.keys()),
       'centrality': list(degree_cent.values())
   })
   df.to_csv('centrality_results.csv', index=False)
   ```

### 重要注意事项

**浮点精度**：当图包含浮点数时，由于精度限制，所有结果本质上都是近似的。这可能影响算法结果，特别是在最小/最大计算中。

**内存与性能**：每次脚本运行时，图数据必须加载到内存中。对于大型网络：
- 使用适当的数据结构（大型稀疏图使用稀疏矩阵）
- 考虑仅加载必要的子图
- 使用高效的文件格式（Python 对象使用 pickle，压缩格式）
- 对超大型网络使用近似算法（例如中心性计算中的 `k` 参数）

**节点和边类型**：
- 节点可以是任何可哈希的 Python 对象（数字、字符串、元组、自定义对象）
- 使用有意义的标识符以保持清晰
- 删除节点时，所有关联边会自动删除

**随机种子**：在随机图生成和力导向布局中始终设置随机种子以确保可重现性：
```python
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)
pos = nx.spring_layout(G, seed=42)
```

## 快速参考

### 基本操作
```python
# 创建
G = nx.Graph()
G.add_edge(1, 2)

# 查询
G.number_of_nodes()
G.number_of_edges()
G.degree(1)
list(G.neighbors(1))

# 检查
G.has_node(1)
G.has_edge(1, 2)
nx.is_connected(G)

# 修改
G.remove_node(1)
G.remove_edge(1, 2)
G.clear()
```

### 核心算法
```python
# 路径
nx.shortest_path(G, source, target)
nx.all_pairs_shortest_path(G)

# 中心性
nx.degree_centrality(G)
nx.betweenness_centrality(G)
nx.closeness_centrality(G)
nx.pagerank(G)

# 聚类
nx.clustering(G)
nx.average_clustering(G)

# 分量
nx.connected_components(G)
nx.strongly_connected_components(G)  # 有向图

# 社区
community.greedy_modularity_communities(G)
```

### 文件 I/O 快速参考
```python
# 读取
nx.read_edgelist('file.txt')
nx.read_graphml('file.graphml')
nx.read_gml('file.gml')

# 写入
nx.write_edgelist(G, 'file.txt')
nx.write_graphml(G, 'file.graphml')
nx.write_gml(G, 'file.gml')

# Pandas
nx.from_pandas_edgelist(df, 'source', 'target')
nx.to_pandas_edgelist(G)
```

## 资源

此技能包含全面的参考文档：

### references/graph-basics.md
关于图类型、创建和修改图、添加节点和边、管理属性、检查结构以及使用子图的详细指南。

### references/algorithms.md
NetworkX 算法的完整覆盖，包括最短路径、中心性度量、连通性、聚类、社区检测、流算法、树算法、匹配、着色、同构和图遍历。

### references/generators.md
图生成器的全面文档，包括经典图、随机模型（Erdős-Rényi、Barabási-Albert、Watts-Strogatz）、格子图、树、社交网络模型和专用生成器。

### references/io.md
读取和写入各种格式图的完整指南：边列表、邻接列表、GraphML、GML、JSON、CSV、Pandas DataFrame、NumPy 数组、SciPy 稀疏矩阵、数据库集成，以及格式选择指南。

### references/visualization.md
可视化技术的详尽文档，包括布局算法、自定义节点和边外观、标签、使用 Plotly 和 PyVis 的交互式可视化、3D 网络、二部图布局，以及创建出版质量图表。

## 其他资源

- **官方文档**：https://networkx.org/documentation/latest/
- **教程**：https://networkx.org/documentation/latest/tutorial.html
- **示例库**：https://networkx.org/documentation/latest/auto_examples/index.html
- **GitHub**：https://github.com/networkx/networkx

## 限制
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
