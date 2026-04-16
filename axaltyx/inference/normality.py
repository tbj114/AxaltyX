
import pandas as pd
import numpy as np
from scipy import stats


class NormalityTests:
    @staticmethod
    def shapiro_wilk(data, column=None):
        if column:
            col_data = data[column].dropna()
            statistic, p_value = stats.shapiro(col_data)
            return {
                'test': 'Shapiro-Wilk',
                'statistic': statistic,
                'p_value': p_value
            }
        else:
            results = {}
            for col in data.select_dtypes(include=[np.number]).columns:
                col_data = data[col].dropna()
                if len(col_data) >= 3:
                    statistic, p_value = stats.shapiro(col_data)
                    results[col] = {
                        'statistic': statistic,
                        'p_value': p_value
                    }
            return results
    
    @staticmethod
    def kolmogorov_smirnov(data, column, dist='norm'):
        col_data = data[column].dropna()
        statistic, p_value = stats.kstest(col_data, dist)
        return {
            'test': 'Kolmogorov-Smirnov',
            'distribution': dist,
            'statistic': statistic,
            'p_value': p_value
        }
    
    @staticmethod
    def anderson_darling(data, column=None):
        if column:
            col_data = data[column].dropna()
            result = stats.anderson(col_data, dist='norm')
            return {
                'test': 'Anderson-Darling',
                'statistic': result.statistic,
                'critical_values': result.critical_values.tolist(),
                'significance_levels': result.significance_level.tolist()
            }
        else:
            results = {}
            for col in data.select_dtypes(include=[np.number]).columns:
                col_data = data[col].dropna()
                if len(col_data) >= 3:
                    result = stats.anderson(col_data, dist='norm')
                    results[col] = {
                        'statistic': result.statistic,
                        'critical_values': result.critical_values.tolist(),
                        'significance_levels': result.significance_level.tolist()
                    }
            return results
    
    @staticmethod
    def dagostino_pearson(data, column=None):
        if column:
            col_data = data[column].dropna()
            statistic, p_value = stats.normaltest(col_data)
            return {
                'test': "D'Agostino-Pearson",
                'statistic': statistic,
                'p_value': p_value
            }
        else:
            results = {}
            for col in data.select_dtypes(include=[np.number]).columns:
                col_data = data[col].dropna()
                if len(col_data) >= 20:
                    statistic, p_value = stats.normaltest(col_data)
                    results[col] = {
                        'statistic': statistic,
                        'p_value': p_value
                    }
            return results
