
import pandas as pd
import numpy as np
from scipy import stats


class NonParametric:
    @staticmethod
    def mann_whitney(data, group_col, value_col):
        groups = list(data.groupby(group_col)[value_col])
        if len(groups) != 2:
            raise ValueError("Mann-Whitney U test requires exactly 2 groups")
        group1 = groups[0][1].dropna()
        group2 = groups[1][1].dropna()
        u_stat, p_value = stats.mannwhitneyu(group1, group2)
        return {
            'u_statistic': u_stat,
            'p_value': p_value,
            'n1': len(group1),
            'n2': len(group2)
        }
    
    @staticmethod
    def wilcoxon(data, col1, col2):
        data_clean = data[[col1, col2]].dropna()
        z_stat, p_value = stats.wilcoxon(data_clean[col1], data_clean[col2])
        return {
            'z_statistic': z_stat,
            'p_value': p_value,
            'n': len(data_clean)
        }
    
    @staticmethod
    def kruskal_wallis(data, group_col, value_col):
        groups = [group.dropna() for _, group in data.groupby(group_col)[value_col]]
        h_stat, p_value = stats.kruskal(*groups)
        return {
            'h_statistic': h_stat,
            'p_value': p_value,
            'n_groups': len(groups)
        }
    
    @staticmethod
    def friedman(data, block_col, treatment_col, value_col):
        pivot = data.pivot(index=block_col, columns=treatment_col, values=value_col)
        chi2_stat, p_value = stats.friedmanchisquare(*[pivot[col] for col in pivot.columns])
        return {
            'chi2_statistic': chi2_stat,
            'p_value': p_value,
            'n_blocks': len(pivot),
            'n_treatments': len(pivot.columns)
        }
    
    @staticmethod
    def sign_test(data, col1, col2):
        data_clean = data[[col1, col2]].dropna()
        diff = data_clean[col1] - data_clean[col2]
        n_pos = (diff > 0).sum()
        n_neg = (diff < 0).sum()
        n = n_pos + n_neg
        k = min(n_pos, n_neg)
        p_value = 2 * stats.binom.cdf(k, n, 0.5)
        return {
            'p_value': p_value,
            'n_positive': n_pos,
            'n_negative': n_neg,
            'n_ties': len(diff) - n
        }
