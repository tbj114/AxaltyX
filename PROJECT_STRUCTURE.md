
# AxaltyX 统计库项目结构

## 项目概述
AxaltyX 是一个功能全面的专业统计分析与数据可视化 Python 库。

## 目录结构

```
/workspace/
├── setup.py              # 项目配置文件
├── requirements.txt      # 依赖包列表
├── README.md            # 项目说明
├── examples.py          # 使用示例
├── PROJECT_STRUCTURE.md # 项目结构文档
├── test_import.py       # 导入测试
├── simple_test.py       # 简单功能测试
└── axaltyx/            # 主包目录
    ├── __init__.py
    ├── data/            # 数据管理模块
    │   ├── __init__.py
    │   ├── data_manager.py
    │   ├── missing_values.py
    │   └── data_transform.py
    ├── descriptive/     # 描述性统计模块
    │   ├── __init__.py
    │   ├── descriptive_stats.py
    │   ├── frequency.py
    │   └── crosstab.py
    ├── inference/       # 推断统计模块
    │   ├── __init__.py
    │   ├── ttests.py
    │   ├── anova.py
    │   ├── nonparametric.py
    │   └── normality.py
    ├── regression/      # 回归分析模块
    │   ├── __init__.py
    │   ├── correlation.py
    │   ├── linear_regression.py
    │   └── logistic_regression.py
    ├── multivariate/    # 多元统计模块
    │   ├── __init__.py
    │   ├── factor_analysis.py
    │   ├── clustering.py
    │   └── pca.py
    ├── visualization/   # 可视化模块
    │   ├── __init__.py
    │   ├── basic_plots.py
    │   ├── statistical_plots.py
    │   ├── interactive_plots.py
    │   └── advanced_plots.py
    ├── survival/        # 生存分析模块
    │   ├── __init__.py
    │   └── survival_analysis.py
    ├── timeseries/      # 时间序列分析模块
    │   ├── __init__.py
    │   └── time_series.py
    ├── ml/              # 机器学习模块
    │   ├── __init__.py
    │   └── machine_learning.py
    ├── bayesian/        # 贝叶斯统计模块
    │   ├── __init__.py
    │   └── bayesian_stats.py
    └── causal/          # 因果推断模块
        ├── __init__.py
        └── causal_inference.py
```

## 主要功能模块

### 1. 数据管理 (axaltyx.data)
- DataManager: 数据加载、保存、选择、过滤
- MissingValues: 缺失值计数、删除、插补
- DataTransform: 标准化、归一化、编码、数据重构

### 2. 描述性统计 (axaltyx.descriptive)
- DescriptiveStats: 均值、中位数、方差、分位数、偏度、峰度
- FrequencyAnalysis: 频数表、直方图、多重响应分析
- CrossTab: 交叉表、卡方检验、Cramer's V、Phi系数

### 3. 推断统计 (axaltyx.inference)
- TTests: 单样本t检验、独立样本t检验、配对样本t检验
- ANOVA: 单因素方差分析、双因素方差分析、重复测量、协方差分析
- NonParametric: Mann-Whitney、Wilcoxon、Kruskal-Wallis、Friedman、符号检验
- NormalityTests: Shapiro-Wilk、Kolmogorov-Smirnov、Anderson-Darling

### 4. 回归分析 (axaltyx.regression)
- Correlation: Pearson、Spearman、Kendall相关、偏相关
- LinearRegression: 简单线性回归、多元线性回归、Lasso、Ridge、ElasticNet
- LogisticRegression: 二元Logistic回归、有序Logistic回归

### 5. 多元统计 (axaltyx.multivariate)
- FactorAnalysis: 因子分析
- Clustering: K-Means聚类、层次聚类、肘部法则
- PCA: 主成分分析

### 6. 可视化 (axaltyx.visualization)
- BasicPlots: 条形图、直方图、散点图、饼图、热力图、词云
- StatisticalPlots: Q-Q图、P-P图、小提琴图、山脊图、ACF图
- InteractivePlots: Plotly交互式图表、3D散点图、旭日图、桑基图
- AdvancedPlots: 树状图、ROC曲线、混淆矩阵、人口金字塔

### 7. 其他高级模块
- 生存分析 (survival): Kaplan-Meier、Cox回归、Weibull模型
- 时间序列 (timeseries): 分解、ARIMA、指数平滑
- 机器学习 (ml): 随机森林、SVM、神经网络
- 贝叶斯统计 (bayesian): 贝叶斯线性回归、贝叶斯Logistic回归
- 因果推断 (causal): 倾向得分匹配

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
import pandas as pd
import numpy as np
from axaltyx.data import DataManager
from axaltyx.descriptive import DescriptiveStats
from axaltyx.visualization import BasicPlots

# 创建数据
data = pd.DataFrame({
    'age': np.random.randint(18, 80, 100),
    'income': np.random.normal(50000, 15000, 100),
    'score': np.random.normal(75, 10, 100)
})

# 描述性统计
descr = DescriptiveStats()
print(descr.summary(data))

# 可视化
plots = BasicPlots()
fig = plots.histogram(data, 'income', kde=True)
fig.savefig('income_hist.png')
```
