
"""
直接测试各个模块，不通过主包导入
"""
import pandas as pd
import numpy as np

print("=" * 60)
print("AxaltyX 模块功能测试")
print("=" * 60)

# 生成测试数据
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

print("\n1. 测试数据管理模块...")
try:
    import sys
    sys.path.insert(0, '/workspace')
    
    from axaltyx.data.data_manager import DataManager
    from axaltyx.data.missing_values import MissingValues
    from axaltyx.data.data_transform import DataTransform
    
    print("✓ 数据管理模块导入成功")
    
    dm = DataManager(data)
    print("  - DataManager: 创建成功")
    print("  - 数据前5行:")
    print(dm.head())
    
    mv = MissingValues()
    missing_count = mv.count_missing(data)
    print("  - MissingValues: 缺失值计数完成")
    
    dt = DataTransform()
    standardized = dt.standardize(data, columns=['age', 'income'])
    print("  - DataTransform: 标准化完成")
    
    print("✓ 数据管理模块测试通过")
except Exception as e:
    print(f"✗ 数据管理模块测试失败: {e}")

print("\n2. 测试描述性统计模块...")
try:
    from axaltyx.descriptive.descriptive_stats import DescriptiveStats
    from axaltyx.descriptive.frequency import FrequencyAnalysis
    from axaltyx.descriptive.crosstab import CrossTab
    
    print("✓ 描述性统计模块导入成功")
    
    descr = DescriptiveStats()
    summary = descr.summary(data, columns=['age', 'income', 'score'])
    print("  - 描述性统计摘要:")
    print(summary)
    
    freq = FrequencyAnalysis()
    freq_table = freq.frequency_table(data, 'education')
    print("  - 频数分析:")
    print(freq_table)
    
    crosstab = CrossTab()
    cross_table = crosstab.crosstab(data, 'gender', 'education')
    print("  - 交叉表:")
    print(cross_table)
    
    print("✓ 描述性统计模块测试通过")
except Exception as e:
    print(f"✗ 描述性统计模块测试失败: {e}")

print("\n3. 测试推断统计模块...")
try:
    from axaltyx.inference.ttests import TTests
    from axaltyx.inference.anova import ANOVA
    from axaltyx.inference.nonparametric import NonParametric
    from axaltyx.inference.normality import NormalityTests
    
    print("✓ 推断统计模块导入成功")
    
    ttests = TTests()
    one_sample = ttests.one_sample(data, 'income', 50000)
    print("  - 单样本t检验:")
    print(f"    t={one_sample['t_statistic']:.4f}, p={one_sample['p_value']:.4f}")
    
    normality = NormalityTests()
    shapiro = normality.shapiro_wilk(data, 'income')
    print("  - Shapiro-Wilk:")
    print(f"    statistic={shapiro['statistic']:.4f}, p={shapiro['p_value']:.4f}")
    
    print("✓ 推断统计模块测试通过")
except Exception as e:
    print(f"✗ 推断统计模块测试失败: {e}")

print("\n4. 测试相关与回归模块...")
try:
    from axaltyx.regression.correlation import Correlation
    from axaltyx.regression.linear_regression import LinearRegression
    from axaltyx.regression.logistic_regression import LogisticRegression
    
    print("✓ 相关与回归模块导入成功")
    
    corr = Correlation()
    pearson = corr.pearson(data, 'age', 'income')
    print("  - Pearson相关:")
    print(f"    r={pearson['correlation']:.4f}, p={pearson['p_value']:.4f}")
    
    corr_matrix = corr.correlation_matrix(data, columns=['age', 'income', 'score'])
    print("  - 相关矩阵:")
    print(corr_matrix)
    
    lr = LinearRegression()
    simple_lr = lr.simple_linear(data, 'income', 'score')
    print("  - 简单线性回归: 完成")
    
    print("✓ 相关与回归模块测试通过")
except Exception as e:
    print(f"✗ 相关与回归模块测试失败: {e}")

print("\n5. 测试多元统计模块...")
try:
    from axaltyx.multivariate.factor_analysis import FactorAnalysis
    from axaltyx.multivariate.clustering import Clustering
    from axaltyx.multivariate.pca import PCA
    
    print("✓ 多元统计模块导入成功")
    
    pca = PCA()
    pca_result = pca.fit(data, columns=['age', 'income', 'score'], n_components=2)
    print("  - PCA解释方差:")
    print(pca_result['explained_variance'])
    
    clustering = Clustering()
    elbow = clustering.elbow_method(data, columns=['age', 'income', 'score'], max_clusters=5)
    print("  - 肘部法则: 完成")
    
    print("✓ 多元统计模块测试通过")
except Exception as e:
    print(f"✗ 多元统计模块测试失败: {e}")

print("\n6. 测试可视化模块...")
try:
    import matplotlib
    matplotlib.use('Agg')
    
    from axaltyx.visualization.basic_plots import BasicPlots
    from axaltyx.visualization.statistical_plots import StatisticalPlots
    
    print("✓ 可视化模块导入成功")
    
    plots = BasicPlots()
    
    fig1 = plots.histogram(data, 'income', kde=True, title='收入分布')
    fig1.savefig('/workspace/test_income_hist.png')
    print("  - 直方图: 已保存")
    
    fig2 = plots.scatter_plot(data, x='age', y='income', hue='gender', title='年龄与收入')
    fig2.savefig('/workspace/test_scatter.png')
    print("  - 散点图: 已保存")
    
    fig3 = plots.heatmap(data, columns=['age', 'income', 'score', 'satisfaction'])
    fig3.savefig('/workspace/test_heatmap.png')
    print("  - 热力图: 已保存")
    
    print("✓ 可视化模块测试通过")
except Exception as e:
    print(f"✗ 可视化模块测试失败: {e}")

print("\n7. 测试其他高级模块...")
try:
    from axaltyx.survival.survival_analysis import SurvivalAnalysis
    from axaltyx.timeseries.time_series import TimeSeriesAnalysis
    from axaltyx.ml.machine_learning import MachineLearning
    from axaltyx.causal.causal_inference import CausalInference
    
    print("✓ 高级模块导入成功")
    
    print("  - 生存分析模块: 可访问")
    print("  - 时间序列模块: 可访问")
    print("  - 机器学习模块: 可访问")
    print("  - 因果推断模块: 可访问")
    
    print("✓ 高级模块测试通过")
except Exception as e:
    print(f"✗ 高级模块测试失败: {e}")

print("\n" + "=" * 60)
print("模块功能测试完成！")
print("=" * 60)
