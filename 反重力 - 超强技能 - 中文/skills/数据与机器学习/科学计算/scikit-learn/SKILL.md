---
name: scikit-learn
description: 使用 scikit-learn 进行 Python 机器学习。适用于分类、回归、聚类、模型评估和 ML 流水线。触发词：scikit-learn、sklearn、机器学习、分类、回归、聚类、模型评估、ML流水线
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
risk: unknown
source: community
---

# Scikit-learn

## 概述

本技能提供使用 scikit-learn 进行机器学习任务的全面指南。scikit-learn 是经典机器学习领域的行业标准 Python 库。当需要进行分类、回归、聚类、降维、数据预处理、模型评估以及构建生产级 ML 流水线时，请使用本技能。

## 安装

```bash
# 使用 uv 安装 scikit-learn
uv uv pip install scikit-learn

# 可选：安装可视化依赖
uv uv pip install matplotlib seaborn

# 常用搭配
uv uv pip install pandas numpy
```

## 适用场景

在以下情况下使用 scikit-learn 技能：

- 构建分类或回归模型
- 执行聚类或降维
- 为机器学习预处理和转换数据
- 使用交叉验证评估模型性能
- 使用网格搜索或随机搜索调优超参数
- 为生产工作流创建 ML 流水线
- 比较不同算法在同一任务上的表现
- 处理结构化（表格）数据和文本数据
- 需要可解释的经典机器学习方法

## 快速上手

### 分类示例

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 预处理
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 训练模型
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# 评估
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
```

### 混合数据的完整流水线

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier

# 定义特征类型
numeric_features = ['age', 'income']
categorical_features = ['gender', 'occupation']

# 创建预处理流水线
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# 组合转换器
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# 完整流水线
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier(random_state=42))
])

# 拟合和预测
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

## 核心能力

### 1. 监督学习

涵盖分类和回归任务的全面算法。

**核心算法：**
- **线性模型**：逻辑回归、线性回归、Ridge、Lasso、ElasticNet
- **树模型**：决策树、随机森林、梯度提升
- **支持向量机**：SVC、SVR，支持多种核函数
- **集成方法**：AdaBoost、Voting、Stacking
- **神经网络**：MLPClassifier、MLPRegressor
- **其他**：朴素贝叶斯、K 近邻

**适用场景：**
- 分类：预测离散类别（垃圾邮件检测、图像分类、欺诈检测）
- 回归：预测连续值（价格预测、需求预测）

**详见：** `references/supervised_learning.md`，包含详细的算法文档、参数说明和使用示例。

### 2. 无监督学习

通过聚类和降维发现无标签数据中的模式。

**聚类算法：**
- **基于划分**：K-Means、MiniBatchKMeans
- **基于密度**：DBSCAN、HDBSCAN、OPTICS
- **层次聚类**：AgglomerativeClustering
- **概率模型**：高斯混合模型
- **其他**：MeanShift、SpectralClustering、BIRCH

**降维方法：**
- **线性方法**：PCA、TruncatedSVD、NMF
- **流形学习**：t-SNE、UMAP、Isomap、LLE
- **特征提取**：FastICA、LatentDirichletAllocation

**适用场景：**
- 客户分群、异常检测、数据可视化
- 降低特征维度、探索性数据分析
- 主题建模、图像压缩

**详见：** `references/unsupervised_learning.md`，包含详细文档。

### 3. 模型评估与选择

提供稳健的模型评估、交叉验证和超参数调优工具。

**交叉验证策略：**
- KFold、StratifiedKFold（分类任务）
- TimeSeriesSplit（时间序列数据）
- GroupKFold（分组样本）

**超参数调优：**
- GridSearchCV（穷举搜索）
- RandomizedSearchCV（随机采样）
- HalvingGridSearchCV（逐次减半）

**评估指标：**
- **分类**：准确率、精确率、召回率、F1 分数、ROC AUC、混淆矩阵
- **回归**：MSE、RMSE、MAE、R²、MAPE
- **聚类**：轮廓系数、Calinski-Harabasz 指数、Davies-Bouldin 指数

**适用场景：**
- 客观比较模型性能
- 寻找最优超参数
- 通过交叉验证防止过拟合
- 通过学习曲线理解模型行为

**详见：** `references/model_evaluation.md`，包含全面的指标和调优策略。

### 4. 数据预处理

将原始数据转换为适合机器学习的格式。

**缩放和归一化：**
- StandardScaler（零均值、单位方差）
- MinMaxScaler（限定范围）
- RobustScaler（对异常值鲁棒）
- Normalizer（按样本归一化）

**分类变量编码：**
- OneHotEncoder（无序分类）
- OrdinalEncoder（有序分类）
- LabelEncoder（标签编码）

**缺失值处理：**
- SimpleImputer（均值、中位数、众数填充）
- KNNImputer（K 近邻填充）
- IterativeImputer（多元迭代填充）

**特征工程：**
- PolynomialFeatures（交互项）
- KBinsDiscretizer（分箱）
- 特征选择（RFE、SelectKBest、SelectFromModel）

**适用场景：**
- 训练需要特征缩放的算法之前（SVM、KNN、神经网络）
- 将分类变量转换为数值格式
- 系统性处理缺失数据
- 为线性模型创建非线性特征

**详见：** `references/preprocessing.md`，包含详细的预处理技术。

### 5. 流水线与组合

构建可复现的生产级 ML 工作流。

**核心组件：**
- **Pipeline**：将转换器和估计器串联
- **ColumnTransformer**：对不同列应用不同预处理
- **FeatureUnion**：并行组合多个转换器
- **TransformedTargetRegressor**：转换目标变量

**优势：**
- 防止交叉验证中的数据泄漏
- 简化代码、提高可维护性
- 支持联合超参数调优
- 确保训练和预测的一致性

**适用场景：**
- 生产工作流中始终使用 Pipeline
- 混合数值和分类特征时（使用 ColumnTransformer）
- 在包含预处理步骤的交叉验证中
- 超参数调优包含预处理参数时

**详见：** `references/pipelines_and_composition.md`，包含全面的流水线模式。

## 示例脚本

### 分类流水线

运行完整的分类工作流，包含预处理、模型比较、超参数调优和评估：

```bash
python scripts/classification_pipeline.py
```

此脚本演示：
- 处理混合数据类型（数值和分类）
- 使用交叉验证进行模型比较
- 使用 GridSearchCV 进行超参数调优
- 使用多种指标进行全面评估
- 特征重要性分析

### 聚类分析

执行聚类分析，包含算法比较和可视化：

```bash
python scripts/clustering_analysis.py
```

此脚本演示：
- 确定最优聚类数（肘部法、轮廓系数分析）
- 比较多种聚类算法（K-Means、DBSCAN、层次聚类、高斯混合模型）
- 在没有真实标签的情况下评估聚类质量
- 使用 PCA 投影可视化结果

## 参考文档

本技能包含全面的参考文件，用于深入研究特定主题：

### 快速参考
**文件：** `references/quick_reference.md`
- 常见导入模式和安装说明
- 常见任务的快速工作流模板
- 算法选择速查表
- 常见模式和注意事项
- 性能优化技巧

### 监督学习
**文件：** `references/supervised_learning.md`
- 线性模型（回归和分类）
- 支持向量机
- 决策树和集成方法
- K 近邻、朴素贝叶斯、神经网络
- 算法选择指南

### 无监督学习
**文件：** `references/unsupervised_learning.md`
- 所有聚类算法的参数和使用场景
- 降维技术
- 异常值和新颖性检测
- 高斯混合模型
- 方法选择指南

### 模型评估
**文件：** `references/model_evaluation.md`
- 交叉验证策略
- 超参数调优方法
- 分类、回归和聚类指标
- 学习曲线和验证曲线
- 模型选择最佳实践

### 预处理
**文件：** `references/preprocessing.md`
- 特征缩放和归一化
- 分类变量编码
- 缺失值填充
- 特征工程技术
- 自定义转换器

### 流水线与组合
**文件：** `references/pipelines_and_composition.md`
- 流水线构建和使用
- 用于混合数据类型的 ColumnTransformer
- 用于并行转换的 FeatureUnion
- 完整的端到端示例
- 最佳实践

## 常见工作流

### 构建分类模型

1. **加载和探索数据**
   ```python
   import pandas as pd
   df = pd.read_csv('data.csv')
   X = df.drop('target', axis=1)
   y = df['target']
   ```

2. **分层划分数据**
   ```python
   from sklearn.model_selection import train_test_split
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, stratify=y, random_state=42
   )
   ```

3. **创建预处理流水线**
   ```python
   from sklearn.pipeline import Pipeline
   from sklearn.preprocessing import StandardScaler
   from sklearn.compose import ColumnTransformer

   # 分别处理数值和分类特征
   preprocessor = ColumnTransformer([
       ('num', StandardScaler(), numeric_features),
       ('cat', OneHotEncoder(), categorical_features)
   ])
   ```

4. **构建完整流水线**
   ```python
   model = Pipeline([
       ('preprocessor', preprocessor),
       ('classifier', RandomForestClassifier(random_state=42))
   ])
   ```

5. **调优超参数**
   ```python
   from sklearn.model_selection import GridSearchCV

   param_grid = {
       'classifier__n_estimators': [100, 200],
       'classifier__max_depth': [10, 20, None]
   }

   grid_search = GridSearchCV(model, param_grid, cv=5)
   grid_search.fit(X_train, y_train)
   ```

6. **在测试集上评估**
   ```python
   from sklearn.metrics import classification_report

   best_model = grid_search.best_estimator_
   y_pred = best_model.predict(X_test)
   print(classification_report(y_test, y_pred))
   ```

### 执行聚类分析

1. **预处理数据**
   ```python
   from sklearn.preprocessing import StandardScaler

   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(X)
   ```

2. **确定最优聚类数**
   ```python
   from sklearn.cluster import KMeans
   from sklearn.metrics import silhouette_score

   scores = []
   for k in range(2, 11):
       kmeans = KMeans(n_clusters=k, random_state=42)
       labels = kmeans.fit_predict(X_scaled)
       scores.append(silhouette_score(X_scaled, labels))

   optimal_k = range(2, 11)[np.argmax(scores)]
   ```

3. **应用聚类**
   ```python
   model = KMeans(n_clusters=optimal_k, random_state=42)
   labels = model.fit_predict(X_scaled)
   ```

4. **使用降维可视化**
   ```python
   from sklearn.decomposition import PCA

   pca = PCA(n_components=2)
   X_2d = pca.fit_transform(X_scaled)

   plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap='viridis')
   ```

## 最佳实践

### 始终使用流水线
流水线可防止数据泄漏并确保一致性：
```python
# 正确：预处理在流水线中
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])

# 错误：预处理在外部（可能泄漏信息）
X_scaled = StandardScaler().fit_transform(X)
```

### 仅在训练数据上拟合
切勿在测试数据上拟合：
```python
# 正确
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 仅转换

# 错误
scaler = StandardScaler()
X_all_scaled = scaler.fit_transform(np.vstack([X_train, X_test]))
```

### 分类任务使用分层划分
保持类别分布：
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

### 设置随机种子以确保可复现性
```python
model = RandomForestClassifier(n_estimators=100, random_state=42)
```

### 选择合适的评估指标
- 平衡数据：准确率、F1 分数
- 不平衡数据：精确率、召回率、ROC AUC、平衡准确率
- 成本敏感：自定义评分器

### 需要时进行特征缩放
需要特征缩放的算法：
- SVM、KNN、神经网络
- PCA、带正则化的线性/逻辑回归
- K-Means 聚类

不需要缩放的算法：
- 树模型（决策树、随机森林、梯度提升）
- 朴素贝叶斯

## 常见问题排查

### ConvergenceWarning（收敛警告）
**问题：** 模型未收敛
**解决方案：** 增加 `max_iter` 或对特征进行缩放
```python
model = LogisticRegression(max_iter=1000)
```

### 测试集表现差
**问题：** 过拟合
**解决方案：** 使用正则化、交叉验证或更简单的模型
```python
# 添加正则化
model = Ridge(alpha=1.0)

# 使用交叉验证
scores = cross_val_score(model, X, y, cv=5)
```

### 大数据集内存不足
**解决方案：** 使用专为大数据设计的算法
```python
# 大数据集使用 SGD
from sklearn.linear_model import SGDClassifier
model = SGDClassifier()

# 聚类使用 MiniBatchKMeans
from sklearn.cluster import MiniBatchKMeans
model = MiniBatchKMeans(n_clusters=8, batch_size=100)
```

## 更多资源

- 官方文档：https://scikit-learn.org/stable/
- 用户指南：https://scikit-learn.org/stable/user_guide.html
- API 参考：https://scikit-learn.org/stable/api/index.html
- 示例库：https://scikit-learn.org/stable/auto_examples/index.html

## 使用限制

- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来寻求澄清。
