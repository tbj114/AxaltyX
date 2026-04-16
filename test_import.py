
"""
AxaltyX 库导入测试
"""
print("测试 AxaltyX 库导入...")

try:
    import axaltyx
    print(f"✓ AxaltyX 版本: {axaltyx.__version__}")
except Exception as e:
    print(f"✗ 导入失败: {e}")

print("\n测试各模块导入...")

modules_to_test = [
    ('数据管理', 'axaltyx.data'),
    ('描述性统计', 'axaltyx.descriptive'),
    ('推断统计', 'axaltyx.inference'),
    ('回归分析', 'axaltyx.regression'),
    ('多元统计', 'axaltyx.multivariate'),
    ('可视化', 'axaltyx.visualization'),
    ('生存分析', 'axaltyx.survival'),
    ('时间序列', 'axaltyx.timeseries'),
    ('机器学习', 'axaltyx.ml'),
    ('贝叶斯统计', 'axaltyx.bayesian'),
    ('因果推断', 'axaltyx.causal'),
]

for name, module_path in modules_to_test:
    try:
        __import__(module_path)
        print(f"✓ {name} 模块导入成功")
    except Exception as e:
        print(f"✗ {name} 模块导入失败: {e}")

print("\n测试主要类导入...")

classes_to_test = [
    ('axaltyx.data', 'DataManager'),
    ('axaltyx.data', 'MissingValues'),
    ('axaltyx.data', 'DataTransform'),
    ('axaltyx.descriptive', 'DescriptiveStats'),
    ('axaltyx.descriptive', 'FrequencyAnalysis'),
    ('axaltyx.descriptive', 'CrossTab'),
    ('axaltyx.inference', 'TTests'),
    ('axaltyx.inference', 'ANOVA'),
    ('axaltyx.inference', 'NonParametric'),
    ('axaltyx.inference', 'NormalityTests'),
    ('axaltyx.regression', 'Correlation'),
    ('axaltyx.regression', 'LinearRegression'),
    ('axaltyx.regression', 'LogisticRegression'),
    ('axaltyx.multivariate', 'FactorAnalysis'),
    ('axaltyx.multivariate', 'Clustering'),
    ('axaltyx.multivariate', 'PCA'),
    ('axaltyx.visualization', 'BasicPlots'),
    ('axaltyx.visualization', 'StatisticalPlots'),
    ('axaltyx.visualization', 'InteractivePlots'),
    ('axaltyx.visualization', 'AdvancedPlots'),
    ('axaltyx.survival', 'SurvivalAnalysis'),
    ('axaltyx.timeseries', 'TimeSeriesAnalysis'),
    ('axaltyx.ml', 'MachineLearning'),
    ('axaltyx.bayesian', 'BayesianStats'),
    ('axaltyx.causal', 'CausalInference'),
]

for module_path, class_name in classes_to_test:
    try:
        module = __import__(module_path, fromlist=[class_name])
        cls = getattr(module, class_name)
        print(f"✓ {class_name} 导入成功")
    except Exception as e:
        print(f"✗ {class_name} 导入失败: {e}")

print("\n" + "=" * 60)
print("导入测试完成！")
print("=" * 60)
