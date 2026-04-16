
"""
AxaltyX 统计库使用示例
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("AxaltyX 统计库 - 快速入门示例")
print("=" * 60)

# 生成示例数据
np.random.seed(42)
data = pd.DataFrame({
    'id': range(100),
    'age': np.random.randint(18, 80, 100),
    'income': np.random.normal(50000, 15000, 100),
    'score': np.random.normal(75, 10, 100),
    'gender': np.random.choice(['Male', 'Female'], 100),
    'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], 100),
    'satisfaction': np.random.randint(1, 6, 100),
    'treatment': np.random.choice([0, 1], 100)
})

print("\n1. 数据管理示例")
print("-" * 60)
from axaltyx.data import DataManager, MissingValues, DataTransform

dm = DataManager(data)
print("数据前5行:")
print(dm.head())

print("\n2. 描述性统计示例")
print("-" * 60)
from axaltyx.descriptive import DescriptiveStats, FrequencyAnalysis, CrossTab

descr = DescriptiveStats()
print("\n描述性统计摘要:")
print(descr.summary(data, columns=['age', 'income', 'score']))

freq = FrequencyAnalysis()
print("\n频数分析 - 教育水平:")
print(freq.frequency_table(data, 'education'))

crosstab = CrossTab()
print("\n交叉表 - 性别 vs 教育水平:")
print(crosstab.crosstab(data, 'gender', 'education'))

print("\n3. 统计检验示例")
print("-" * 60)
from axaltyx.inference import TTests, NormalityTests

ttests = TTests()
print("\n单样本t检验 - 检验收入均值是否为50000:")
result = ttests.one_sample(data, 'income', 50000)
print(f"t统计量: {result['t_statistic']:.4f}, p值: {result['p_value']:.4f}")

print("\n独立样本t检验 - 性别间收入差异:")
result = ttests.independent_samples(data, 'gender', 'income')
print(f"t统计量: {result['t_statistic']:.4f}, p值: {result['p_value']:.4f}")

normality = NormalityTests()
print("\n正态性检验 (Shapiro-Wilk) - 收入:")
result = normality.shapiro_wilk(data, 'income')
print(f"统计量: {result['statistic']:.4f}, p值: {result['p_value']:.4f}")

print("\n4. 相关与回归示例")
print("-" * 60)
from axaltyx.regression import Correlation, LinearRegression

corr = Correlation()
print("\n年龄与收入的Pearson相关:")
result = corr.pearson(data, 'age', 'income')
print(f"相关系数: {result['correlation']:.4f}, p值: {result['p_value']:.4f}")

print("\n相关矩阵:")
print(corr.correlation_matrix(data, columns=['age', 'income', 'score']))

lr = LinearRegression()
print("\n简单线性回归 (收入 -> 分数):")
result = lr.simple_linear(data, 'income', 'score')
print(result['summary'])

print("\n5. 多元统计示例")
print("-" * 60)
from axaltyx.multivariate import PCA, Clustering

print("\n主成分分析 (PCA):")
pca = PCA()
result = pca.fit(data, columns=['age', 'income', 'score'], n_components=2)
print("\n解释方差:")
print(result['explained_variance'])

print("\n6. 可视化示例")
print("-" * 60)
from axaltyx.visualization import BasicPlots, StatisticalPlots

plots = BasicPlots()

print("生成直方图...")
fig = plots.histogram(data, 'income', kde=True, title='收入分布')
fig.savefig('/workspace/income_histogram.png')
print("直方图已保存为 income_histogram.png")

print("生成箱线图...")
fig = plots.box_plot(data, x='education', y='income', title='不同教育水平的收入分布')
fig.savefig('/workspace/income_boxplot.png')
print("箱线图已保存为 income_boxplot.png")

print("生成散点图...")
fig = plots.scatter_plot(data, x='age', y='income', hue='gender', title='年龄与收入关系')
fig.savefig('/workspace/age_income_scatter.png')
print("散点图已保存为 age_income_scatter.png")

print("生成热力图...")
fig = plots.heatmap(data, columns=['age', 'income', 'score', 'satisfaction'], title='相关性热力图')
fig.savefig('/workspace/correlation_heatmap.png')
print("热力图已保存为 correlation_heatmap.png")

stat_plots = StatisticalPlots()
print("生成Q-Q图...")
fig = stat_plots.qq_plot(data, 'income', title='收入Q-Q图')
fig.savefig('/workspace/income_qqplot.png')
print("Q-Q图已保存为 income_qqplot.png")

print("\n" + "=" * 60)
print("示例运行完成！")
print("=" * 60)
