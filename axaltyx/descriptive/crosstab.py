
import pandas as pd
import numpy as np
from scipy import stats


class CrossTab:
    @staticmethod
    def crosstab(data, row, col, margins=True, normalize=False):
        return pd.crosstab(data[row], data[col], margins=margins, normalize=normalize)
    
    @staticmethod
    def chi_square(data, row, col):
        contingency = pd.crosstab(data[row], data[col])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
        return {
            'chi2': chi2,
            'p_value': p_value,
            'dof': dof,
            'expected': expected
        }
    
    @staticmethod
    def cramers_v(data, row, col):
        contingency = pd.crosstab(data[row], data[col])
        chi2, _, _, _ = stats.chi2_contingency(contingency)
        n = contingency.sum().sum()
        min_dim = min(contingency.shape) - 1
        return np.sqrt(chi2 / (n * min_dim))
    
    @staticmethod
    def phi_coefficient(data, row, col):
        contingency = pd.crosstab(data[row], data[col])
        if contingency.shape != (2, 2):
            raise ValueError("Phi coefficient is only for 2x2 tables")
        chi2, _, _, _ = stats.chi2_contingency(contingency)
        n = contingency.sum().sum()
        return np.sqrt(chi2 / n)
    
    @staticmethod
    def lambda_coefficient(data, row, col, direction='symmetric'):
        contingency = pd.crosstab(data[row], data[col])
        n = contingency.sum().sum()
        
        if direction == 'row':
            mode_row = contingency.max(axis=1).sum()
            mode_total = contingency.sum().max()
            return (mode_row - mode_total) / (n - mode_total)
        elif direction == 'column':
            mode_col = contingency.max(axis=0).sum()
            mode_total = contingency.sum(axis=1).max()
            return (mode_col - mode_total) / (n - mode_total)
        else:
            mode_row = contingency.max(axis=1).sum()
            mode_col = contingency.max(axis=0).sum()
            mode_total_row = contingency.sum().max()
            mode_total_col = contingency.sum(axis=1).max()
            lambda_row = (mode_row - mode_total_row) / (n - mode_total_row)
            lambda_col = (mode_col - mode_total_col) / (n - mode_total_col)
            return (lambda_row + lambda_col) / 2
