
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols


class ANOVA:
    @staticmethod
    def one_way(data, group_col, value_col):
        groups = [group.dropna() for _, group in data.groupby(group_col)[value_col]]
        f_stat, p_value = stats.f_oneway(*groups)
        
        k = len(groups)
        n = sum(len(g) for g in groups)
        
        grand_mean = np.mean(np.concatenate(groups))
        ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
        ss_within = sum(sum((g - np.mean(g))**2) for g in groups)
        ss_total = ss_between + ss_within
        
        ms_between = ss_between / (k - 1)
        ms_within = ss_within / (n - k)
        
        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'df_between': k - 1,
            'df_within': n - k,
            'df_total': n - 1,
            'ss_between': ss_between,
            'ss_within': ss_within,
            'ss_total': ss_total,
            'ms_between': ms_between,
            'ms_within': ms_within
        }
    
    @staticmethod
    def two_way(data, formula):
        model = ols(formula, data=data).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        return {
            'anova_table': anova_table,
            'model': model
        }
    
    @staticmethod
    def repeated_measures(data, formula):
        model = ols(formula, data=data).fit()
        return {
            'model': model
        }
    
    @staticmethod
    def ancova(data, formula):
        model = ols(formula, data=data).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        return {
            'anova_table': anova_table,
            'model': model
        }
