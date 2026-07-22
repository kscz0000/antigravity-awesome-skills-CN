---
name: statsmodels
description: "Statsmodels 是 Python 首要的统计建模库，提供广泛的统计方法用于估计、推断和诊断。当用户需要线性回归、逻辑回归、时间序列分析、ARIMA、统计检验、计量经济学分析、假设检验、模型诊断时使用此技能。"
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
risk: unknown
source: community
---

# Statsmodels：统计建模与计量经济学

## 概述

Statsmodels 是 Python 首要的统计建模库，提供广泛的统计方法用于估计、推断和诊断。从简单的线性回归到复杂的时间序列模型和计量经济学分析，使用此技能进行严谨的统计分析。

## 何时使用此技能

此技能应在以下情况下使用：
- 拟合回归模型（OLS、WLS、GLS、分位数回归）
- 执行广义线性建模（逻辑回归、泊松回归、Gamma回归等）
- 分析离散结果（二元、多项、计数、有序）
- 进行时间序列分析（ARIMA、SARIMAX、VAR、预测）
- 运行统计检验和诊断
- 检验模型假设（异方差性、自相关、正态性）
- 检测异常值和有影响力的观测值
- 比较模型（AIC/BIC、似然比检验）
- 估计因果效应
- 生成可发表的统计表格和推断结果

## 快速入门指南

### 线性回归（OLS）

```python
import statsmodels.api as sm
import numpy as np
import pandas as pd

# 准备数据 - 始终添加常数项作为截距
X = sm.add_constant(X_data)

# 拟合 OLS 模型
model = sm.OLS(y, X)
results = model.fit()

# 查看完整结果
print(results.summary())

# 关键结果
print(f"R-squared: {results.rsquared:.4f}")
print(f"Coefficients:\\n{results.params}")
print(f"P-values:\\n{results.pvalues}")

# 带置信区间的预测
predictions = results.get_prediction(X_new)
pred_summary = predictions.summary_frame()
print(pred_summary)  # 包含均值、置信区间、预测区间

# 诊断检验
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(results.resid, X)
print(f"Breusch-Pagan p-value: {bp_test[1]:.4f}")

# 可视化残差
import matplotlib.pyplot as plt
plt.scatter(results.fittedvalues, results.resid)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.show()
```

### 逻辑回归（二元结果）

```python
from statsmodels.discrete.discrete_model import Logit

# 添加常数项
X = sm.add_constant(X_data)

# 拟合 logit 模型
model = Logit(y_binary, X)
results = model.fit()

print(results.summary())

# 优势比
odds_ratios = np.exp(results.params)
print("Odds ratios:\\n", odds_ratios)

# 预测概率
probs = results.predict(X)

# 二元预测（0.5 阈值）
predictions = (probs > 0.5).astype(int)

# 模型评估
from sklearn.metrics import classification_report, roc_auc_score

print(classification_report(y_binary, predictions))
print(f"AUC: {roc_auc_score(y_binary, probs):.4f}")

# 边际效应
marginal = results.get_margeff()
print(marginal.summary())
```

### 时间序列（ARIMA）

```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 检验平稳性
from statsmodels.tsa.stattools import adfuller

adf_result = adfuller(y_series)
print(f"ADF p-value: {adf_result[1]:.4f}")

if adf_result[1] > 0.05:
    # 序列非平稳，进行差分
    y_diff = y_series.diff().dropna()

# 绘制 ACF/PACF 以识别 p, q
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(y_diff, lags=40, ax=ax1)
plot_pacf(y_diff, lags=40, ax=ax2)
plt.show()

# 拟合 ARIMA(p,d,q)
model = ARIMA(y_series, order=(1, 1, 1))
results = model.fit()

print(results.summary())

# 预测
forecast = results.forecast(steps=10)
forecast_obj = results.get_forecast(steps=10)
forecast_df = forecast_obj.summary_frame()

print(forecast_df)  # 包含均值和置信区间

# 残差诊断
results.plot_diagnostics(figsize=(12, 8))
plt.show()
```

### 广义线性模型（GLM）

```python
import statsmodels.api as sm

# 用于计数数据的泊松回归
X = sm.add_constant(X_data)
model = sm.GLM(y_counts, X, family=sm.families.Poisson())
results = model.fit()

print(results.summary())

# 发生率比（对数链接函数的泊松回归）
rate_ratios = np.exp(results.params)
print("Rate ratios:\\n", rate_ratios)

# 检查过度离散
overdispersion = results.pearson_chi2 / results.df_resid
print(f"Overdispersion: {overdispersion:.2f}")

if overdispersion > 1.5:
    # 改用负二项回归
    from statsmodels.discrete.count_model import NegativeBinomial
    nb_model = NegativeBinomial(y_counts, X)
    nb_results = nb_model.fit()
    print(nb_results.summary())
```

## 核心统计建模能力

### 1. 线性回归模型

适用于连续结果变量的完整线性模型套件，支持多种误差结构。

**可用模型：**
- **OLS**：具有独立同分布误差的标准线性回归
- **WLS**：加权最小二乘法，适用于异方差误差
- **GLS**：广义最小二乘法，适用于任意协方差结构
- **GLSAR**：具有自回归误差的 GLS，适用于时间序列
- **分位数回归**：条件分位数（对异常值稳健）
- **混合效应模型**：具有随机效应的层次/多层模型
- **递归/滚动回归**：时变参数估计

**关键特性：**
- 完整的诊断检验
- 稳健标准误（HC、HAC、聚类稳健）
- 影响统计量（Cook距离、杠杆值、DFFITS）
- 假设检验（F检验、Wald检验）
- 模型比较（AIC、BIC、似然比检验）
- 带置信区间和预测区间的预测

**何时使用：** 连续结果变量，需要对系数进行推断，需要诊断检验

**参考文档：** 详见 `references/linear_models.md` 获取模型选择、诊断和最佳实践的详细指导。

### 2. 广义线性模型（GLM）

将线性模型扩展到非正态分布的灵活框架。

**分布族：**
- **Binomial**：二元结果或比例（逻辑回归）
- **Poisson**：计数数据
- **Negative Binomial**：过度离散计数
- **Gamma**：正连续、右偏数据
- **Inverse Gaussian**：具有特定方差结构的正连续数据
- **Gaussian**：等同于 OLS
- **Tweedie**：适用于半连续数据的灵活族

**链接函数：**
- Logit、Probit、Log、Identity、Inverse、Sqrt、CLogLog、Power
- 根据解释需求和模型拟合选择

**关键特性：**
- 通过 IRLS 进行最大似然估计
- 偏差和 Pearson 残差
- 拟合优度统计量
- 伪 R方度量
- 稳健标准误

**何时使用：** 非正态结果，需要灵活的方差和链接函数设定

**参考文档：** 详见 `references/glm.md` 获取分布族选择、链接函数、解释和诊断的指导。

### 3. 离散选择模型

用于分类和计数结果的模型。

**二元模型：**
- **Logit**：逻辑回归（优势比）
- **Probit**：Probit回归（正态分布）

**多项模型：**
- **MNLogit**：无序类别（3个及以上水平）
- **Conditional Logit**：具有备选特定变量的选择模型
- **Ordered Model**：有序结果（有序类别）

**计数模型：**
- **Poisson**：标准计数模型
- **Negative Binomial**：过度离散计数
- **Zero-Inflated**：零膨胀模型（ZIP、ZINB）
- **Hurdle Models**：零值较多数据的两阶段模型

**关键特性：**
- 最大似然估计
- 均值处边际效应或平均边际效应
- 通过 AIC/BIC 进行模型比较
- 预测概率和分类
- 拟合优度检验

**何时使用：** 二元、分类或计数结果

**参考文档：** 详见 `references/discrete_choice.md` 获取模型选择、解释和评估的指导。

### 4. 时间序列分析

完整的时间序列建模和预测能力。

**单变量模型：**
- **AutoReg (AR)**：自回归模型
- **ARIMA**：自回归积分滑动平均模型
- **SARIMAX**：带外生变量的季节性 ARIMA
- **Exponential Smoothing**：简单指数平滑、Holt、Holt-Winters
- **ETS**：创新状态空间模型

**多变量模型：**
- **VAR**：向量自回归
- **VARMAX**：带 MA 和外生变量的 VAR
- **Dynamic Factor Models**：提取公共因子
- **VECM**：向量误差修正模型（协整）

**高级模型：**
- **State Space**：卡尔曼滤波、自定义设定
- **Regime Switching**：马尔可夫转换模型
- **ARDL**：自回归分布滞后

**关键特性：**
- ACF/PACF 分析用于模型识别
- 平稳性检验（ADF、KPSS）
- 带预测区间的预测
- 残差诊断（Ljung-Box、异方差性）
- Granger因果检验
- 脉冲响应函数（IRF）
- 预测误差方差分解（FEVD）

**何时使用：** 时间序列数据、预测、理解时间动态

**参考文档：** 详见 `references/time_series.md` 获取模型选择、诊断和预测方法的指导。

### 5. 统计检验与诊断

用于模型验证的广泛检验和诊断能力。

**残差诊断：**
- 自相关检验（Ljung-Box、Durbin-Watson、Breusch-Godfrey）
- 异方差性检验（Breusch-Pagan、White、ARCH）
- 正态性检验（Jarque-Bera、Omnibus、Anderson-Darling、Lilliefors）
- 设定检验（RESET、Harvey-Collier）

**影响力和异常值：**
- 杠杆值（帽子值）
- Cook距离
- DFFITS 和 DFBETAs
- 学生化残差
- 影响力图

**假设检验：**
- t检验（单样本、双样本、配对）
- 比例检验
- 卡方检验
- 非参数检验（Mann-Whitney、Wilcoxon、Kruskal-Wallis）
- ANOVA（单因素、双因素、重复测量）

**多重比较：**
- Tukey's HSD
- Bonferroni校正
- 错误发现率（FDR）

**效应量和功效：**
- Cohen's d、eta-squared
- t检验和比例检验的功效分析
- 样本量计算

**稳健推断：**
- 异方差一致性标准误（HC0-HC3）
- HAC标准误（Newey-West）
- 聚类稳健标准误

**何时使用：** 验证假设、检测问题、确保稳健推断

**参考文档：** 详见 `references/stats_diagnostics.md` 获取完整的检验和诊断流程。

## 公式 API（R风格）

Statsmodels 支持 R 风格的公式进行直观的模型设定：

```python
import statsmodels.formula.api as smf

# 使用公式的 OLS
results = smf.ols('y ~ x1 + x2 + x1:x2', data=df).fit()

# 分类变量（自动虚拟编码）
results = smf.ols('y ~ x1 + C(category)', data=df).fit()

# 交互项
results = smf.ols('y ~ x1 * x2', data=df).fit()  # x1 + x2 + x1:x2

# 多项式项
results = smf.ols('y ~ x + I(x**2)', data=df).fit()

# Logit
results = smf.logit('y ~ x1 + x2 + C(group)', data=df).fit()

# Poisson
results = smf.poisson('count ~ x1 + x2', data=df).fit()

# ARIMA（不通过公式提供，使用常规 API）
```

## 模型选择与比较

### 信息准则

```python
# 使用 AIC/BIC 比较模型
models = {
    'Model 1': model1_results,
    'Model 2': model2_results,
    'Model 3': model3_results
}

comparison = pd.DataFrame({
    'AIC': {name: res.aic for name, res in models.items()},
    'BIC': {name: res.bic for name, res in models.items()},
    'Log-Likelihood': {name: res.llf for name, res in models.items()}
})

print(comparison.sort_values('AIC'))
# 较低的 AIC/BIC 表示更好的模型
```

### 似然比检验（嵌套模型）

```python
# 对于嵌套模型（一个是另一个的子集）
from scipy import stats

lr_stat = 2 * (full_model.llf - reduced_model.llf)
df = full_model.df_model - reduced_model.df_model
p_value = 1 - stats.chi2.cdf(lr_stat, df)

print(f"LR statistic: {lr_stat:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("完整模型显著更好")
else:
    print("简化模型更优（简约性原则）")
```

### 交叉验证

```python
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []

for train_idx, val_idx in kf.split(X):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

    # 拟合模型
    model = sm.OLS(y_train, X_train).fit()

    # 预测
    y_pred = model.predict(X_val)

    # 评分
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    cv_scores.append(rmse)

print(f"CV RMSE: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
```

## 最佳实践

### 数据准备

1. **始终添加常数项**：使用 `sm.add_constant()`，除非明确排除截距
2. **检查缺失值**：拟合前处理或填补
3. **必要时标准化**：改善收敛性和解释（但树模型不需要）
4. **编码分类变量**：使用公式 API 或手动虚拟编码

### 模型构建

1. **从简单开始**：从基础模型开始，根据需要增加复杂性
2. **检查假设**：检验残差、异方差性、自相关
3. **使用适当的模型**：匹配模型与结果类型（二元→Logit，计数→Poisson）
4. **考虑替代方案**：如果违反假设，使用稳健方法或不同模型

### 推断

1. **报告效应量**：不只是 p 值
2. **使用稳健标准误**：当存在异方差性或聚类时
3. **多重比较**：检验多个假设时进行校正
4. **置信区间**：始终与点估计一起报告

### 模型评估

1. **检查残差**：绘制残差与拟合值、Q-Q图
2. **影响力诊断**：识别并调查有影响力的观测值
3. **样本外验证**：在保留集上测试或交叉验证
4. **比较模型**：非嵌套模型使用 AIC/BIC，嵌套模型使用 LR 检验

### 报告

1. **完整摘要**：使用 `.summary()` 获取详细输出
2. **记录决策**：注明变换、排除的观测值
3. **谨慎解释**：考虑链接函数（如对数链接的 exp(β)）
4. **可视化**：绘制预测、置信区间、诊断图

## 常见工作流

### 工作流 1：线性回归分析

1. 探索数据（图表、描述统计）
2. 拟合初始 OLS 模型
3. 检查残差诊断
4. 检验异方差性、自相关
5. 检查多重共线性（VIF）
6. 识别有影响力的观测值
7. 必要时使用稳健标准误重新拟合
8. 解释系数和推断
9. 在保留集上验证或通过 CV 验证

### 工作流 2：二元分类

1. 拟合逻辑回归（Logit）
2. 检查收敛问题
3. 解释优势比
4. 计算边际效应
5. 评估分类性能（AUC、混淆矩阵）
6. 检查有影响力的观测值
7. 与替代模型比较（Probit）
8. 在测试集上验证预测

### 工作流 3：计数数据分析

1. 拟合泊松回归
2. 检查过度离散
3. 如果过度离散，拟合负二项回归
4. 检查零膨胀（考虑 ZIP/ZINB）
5. 解释发生率比
6. 评估拟合优度
7. 通过 AIC 比较模型
8. 验证预测

### 工作流 4：时间序列预测

1. 绘制序列，检查趋势/季节性
2. 检验平稳性（ADF、KPSS）
3. 如果非平稳则差分
4. 从 ACF/PACF 识别 p, q
5. 拟合 ARIMA 或 SARIMAX
6. 检查残差诊断（Ljung-Box）
7. 生成带置信区间的预测
8. 在测试集上评估预测精度

## 参考文档

此技能包含详细的参考文件以供深入指导：

### references/linear_models.md
线性回归模型的详细覆盖，包括：
- OLS、WLS、GLS、GLSAR、分位数回归
- 混合效应模型
- 递归和滚动回归
- 完整诊断（异方差性、自相关、多重共线性）
- 影响统计量和异常值检测
- 稳健标准误（HC、HAC、聚类）
- 假设检验和模型比较

### references/glm.md
广义线性模型完整指南：
- 所有分布族（Binomial、Poisson、Gamma等）
- 链接函数及其使用场景
- 模型拟合和解释
- 伪 R方和拟合优度
- 诊断和残差分析
- 应用（逻辑回归、泊松回归、Gamma回归）

### references/discrete_choice.md
离散结果模型综合指南：
- 二元模型（Logit、Probit）
- 多项模型（MNLogit、条件 Logit）
- 计数模型（Poisson、负二项、零膨胀、Hurdle）
- 有序模型
- 边际效应和解释
- 模型诊断和比较

### references/time_series.md
深入的时间序列分析指导：
- 单变量模型（AR、ARIMA、SARIMAX、指数平滑）
- 多变量模型（VAR、VARMAX、动态因子）
- 状态空间模型
- 平稳性检验和诊断
- 预测方法和评估
- Granger因果、IRF、FEVD

### references/stats_diagnostics.md
完整的统计检验和诊断：
- 残差诊断（自相关、异方差性、正态性）
- 影响力和异常值检测
- 假设检验（参数和非参数）
- ANOVA 和事后检验
- 多重比较校正
- 稳健协方差矩阵
- 功效分析和效应量

**何时参考：**
- 需要详细的参数解释
- 在相似模型间选择
- 排除收敛或诊断问题
- 理解特定检验统计量
- 查找高级功能的代码示例

**搜索模式：**
```bash
# 查找特定模型的信息
grep -r "Quantile Regression" references/

# 查找诊断检验
grep -r "Breusch-Pagan" references/stats_diagnostics.md

# 查找时间序列指导
grep -r "SARIMAX" references/time_series.md
```

## 常见陷阱及避免方法

1. **忘记常数项**：始终使用 `sm.add_constant()`，除非不需要截距
2. **忽略假设**：检查残差、异方差性、自相关
3. **结果类型与模型不匹配**：二元→Logit/Probit，计数→Poisson/NB，不是 OLS
4. **不检查收敛**：注意优化警告
5. **错误解释系数**：记住链接函数（log、logit等）
6. **过度离散时使用泊松**：检查离散度，必要时使用负二项
7. **不使用稳健标准误**：当存在异方差性或聚类时
8. **过拟合**：参数过多相对于样本量
9. **数据泄露**：在测试数据上拟合或使用未来信息
10. **不验证预测**：始终检查样本外性能
11. **比较非嵌套模型**：使用 AIC/BIC，不是 LR 检验
12. **忽略有影响力的观测值**：检查 Cook 距离和杠杆值
13. **多重检验**：检验多个假设时校正 p 值
14. **不对时间序列差分**：在非平稳数据上拟合 ARIMA
15. **混淆预测区间与置信区间**：预测区间更宽

## 获取帮助

详细文档和示例：
- 官方文档：https://www.statsmodels.org/stable/
- 用户指南：https://www.statsmodels.org/stable/user-guide.html
- 示例：https://www.statsmodels.org/stable/examples/index.html
- API 参考：https://www.statsmodels.org/stable/api.html

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来询问澄清。
