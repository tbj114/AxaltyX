
import pandas as pd
import numpy as np
from scipy import stats


class TTests:
    @staticmethod
    def one_sample(data, column, popmean):
        col_data = data[column].dropna()
        t_stat, p_value = stats.ttest_1samp(col_data, popmean)
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'df': len(col_data) - 1,
            'mean': col_data.mean(),
            'popmean': popmean
        }
    
    @staticmethod
    def independent_samples(data, group_col, value_col, equal_var=True):
        groups = [group for _, group in data.groupby(group_col)[value_col]]
        t_stat, p_value = stats.ttest_ind(*groups, equal_var=equal_var)
        
        means = data.groupby(group_col)[value_col].mean()
        stds = data.groupby(group_col)[value_col].std()
        ns = data.groupby(group_col)[value_col].count()
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'equal_variance': equal_var,
            'group_means': means.to_dict(),
            'group_stds': stds.to_dict(),
            'group_ns': ns.to_dict()
        }
    
    @staticmethod
    def paired_samples(data, col1, col2):
        data_clean = data[[col1, col2]].dropna()
        t_stat, p_value = stats.ttest_rel(data_clean[col1], data_clean[col2])
        
        diff = data_clean[col1] - data_clean[col2]
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'df': len(data_clean) - 1,
            'mean_diff': diff.mean(),
            'std_diff': diff.std(),
            'mean_col1': data_clean[col1].mean(),
            'mean_col2': data_clean[col2].mean()
        }
    
    @staticmethod
    def welch_anova(data, group_col, value_col):
        from scipy.stats import f_oneway
        groups = [group.dropna() for _, group in data.groupby(group_col)[value_col]]
        
        k = len(groups)
        n = sum(len(g) for g in groups)
        
        grand_mean = np.mean(np.concatenate(groups))
        ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
        ss_within = sum(sum((g - np.mean(g))**2) for g in groups)
        
        ms_between = ss_between / (k - 1)
        ms_within = ss_within / (n - k)
        
        f_stat = ms_between / ms_within
        p_value = 1 - stats.f.cdf(f_stat, k - 1, n - k)
        
        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'df_between': k - 1,
            'df_within': n - k,
            'ss_between': ss_between,
            'ss_within': ss_within,
            'ms_between': ms_between,
            'ms_within': ms_within
        }
