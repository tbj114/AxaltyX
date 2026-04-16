
import pandas as pd
import numpy as np
from scipy import stats


class Correlation:
    @staticmethod
    def pearson(data, col1, col2):
        data_clean = data[[col1, col2]].dropna()
        corr, p_value = stats.pearsonr(data_clean[col1], data_clean[col2])
        return {
            'correlation': corr,
            'p_value': p_value,
            'n': len(data_clean),
            'method': 'Pearson'
        }
    
    @staticmethod
    def spearman(data, col1, col2):
        data_clean = data[[col1, col2]].dropna()
        corr, p_value = stats.spearmanr(data_clean[col1], data_clean[col2])
        return {
            'correlation': corr,
            'p_value': p_value,
            'n': len(data_clean),
            'method': 'Spearman'
        }
    
    @staticmethod
    def kendall(data, col1, col2):
        data_clean = data[[col1, col2]].dropna()
        corr, p_value = stats.kendalltau(data_clean[col1], data_clean[col2])
        return {
            'correlation': corr,
            'p_value': p_value,
            'n': len(data_clean),
            'method': 'Kendall'
        }
    
    @staticmethod
    def partial_correlation(data, x, y, controls):
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        import statsmodels.api as sm
        
        data_clean = data[[x, y] + controls].dropna()
        
        model_x = sm.OLS(data_clean[x], sm.add_constant(data_clean[controls])).fit()
        resid_x = model_x.resid
        
        model_y = sm.OLS(data_clean[y], sm.add_constant(data_clean[controls])).fit()
        resid_y = model_y.resid
        
        partial_corr, p_value = stats.pearsonr(resid_x, resid_y)
        
        return {
            'partial_correlation': partial_corr,
            'p_value': p_value,
            'n': len(data_clean),
            'controls': controls,
            'method': 'Partial correlation'
        }
    
    @staticmethod
    def correlation_matrix(data, columns=None, method='pearson'):
        cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        return data[cols].corr(method=method)
