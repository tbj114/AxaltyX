
"""
简单测试 - 只测试基础模块
"""
import pandas as pd
import numpy as np

print("生成测试数据...")
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
    from axaltyx.data import DataManager, MissingValues, DataTransform
    print("✓ 数据管理模块导入成功")
    
    dm = DataManager(data)
    print("  - DataManager 创建成功")
    print("  - 数据前5行:")
    print(dm.head())
    
    descr_result = dm.describe()
    print("  - 描述统计成功")
    
    print("✓ 数据管理模块测试通过")
except Exception as e:
    print(f"✗ 数据管理模块测试失败: {e}")

print("\n2. 测试描述性统计模块...")
try:
    from axaltyx.descriptive import DescriptiveStats, FrequencyAnalysis, CrossTab
    print("✓ 描述性统计模块导入成功")
    
    descr = DescriptiveStats()
    summary = descr.summary(data, columns=['age', 'income', 'score'])
    print("  - 描述统计摘要:")
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
    from axaltyx.inference import TTests, ANOVA, NonParametric, NormalityTests
    print("✓ 推断统计模块导入成功")
    
    ttests = TTests()
    one_sample_result = ttests.one_sample(data, 'income', 50000)
    print("  - 单样本t检验:")
    print(f"    t统计量: {one_sample_result['t_statistic']:.4f}, p值: {one_sample_result['p_value']:.4f}")
    
    normality = NormalityTests()
    shapiro_result = normality.shapiro_wilk(data, 'income')
    print("  - Shapiro-Wilk正态性检验:")
    print(f"    统计量: {shapiro_result['statistic']:.4f}, p值: {shapiro_result['p_value']:.4f}")
    
    print("✓ 推断统计模块测试通过")
except Exception as e:
    print(f"✗ 推断统计模块测试失败: {e}")

print("\n4. 测试相关与回归模块...")
try:
    from axaltyx.regression import Correlation, LinearRegression
    print("✓ 相关与回归模块导入成功")
    
    corr = Correlation()
    pearson_result = corr.pearson(data, 'age', 'income')
    print("  - Pearson相关:")
    print(f"    相关系数: {pearson_result['correlation']:.4f}, p值: {pearson_result['p_value']:.4f}")
    
    corr_matrix = corr.correlation_matrix(data, columns=['age', 'income', 'score'])
    print("  - 相关矩阵:")
    print(corr_matrix)
    
    lr = LinearRegression()
    lr_result = lr.simple_linear(data, 'income', 'score')
    print("  - 简单线性回归完成")
    
    print("✓ 相关与回归模块测试通过")
except Exception as e:
    print(f"✗ 相关与回归模块测试失败: {e}")

print("\n" + "=" * 60)
print("简单测试完成！")
print("=" * 60)
