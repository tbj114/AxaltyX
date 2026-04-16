
import pandas as pd
import numpy as np
from scipy import stats


class DescriptiveStats:
    @staticmethod
    def mean(data, column=None):
        if column:
            return data[column].mean()
        return data.mean()
    
    @staticmethod
    def median(data, column=None):
        if column:
            return data[column].median()
        return data.median()
    
    @staticmethod
    def mode(data, column=None):
        if column:
            return data[column].mode()
        return data.mode()
    
    @staticmethod
    def variance(data, column=None, ddof=1):
        if column:
            return data[column].var(ddof=ddof)
        return data.var(ddof=ddof)
    
    @staticmethod
    def std(data, column=None, ddof=1):
        if column:
            return data[column].std(ddof=ddof)
        return data.std(ddof=ddof)
    
    @staticmethod
    def min_max(data, column=None):
        if column:
            return (data[column].min(), data[column].max())
        return (data.min(), data.max())
    
    @staticmethod
    def percentile(data, column, q):
        return data[column].quantile(q)
    
    @staticmethod
    def iqr(data, column=None):
        if column:
            return data[column].quantile(0.75) - data[column].quantile(0.25)
        return data.quantile(0.75) - data.quantile(0.25)
    
    @staticmethod
    def skewness(data, column=None):
        if column:
            return stats.skew(data[column].dropna())
        return data.apply(lambda x: stats.skew(x.dropna()))
    
    @staticmethod
    def kurtosis(data, column=None):
        if column:
            return stats.kurtosis(data[column].dropna())
        return data.apply(lambda x: stats.kurtosis(x.dropna()))
    
    @staticmethod
    def summary(data, columns=None):
        cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        summary_data = []
        for col in cols:
            col_data = data[col].dropna()
            summary_data.append({
                'Variable': col,
                'N': len(col_data),
                'Mean': col_data.mean(),
                'Median': col_data.median(),
                'Std': col_data.std(),
                'Variance': col_data.var(),
                'Min': col_data.min(),
                'Max': col_data.max(),
                '25%': col_data.quantile(0.25),
                '50%': col_data.quantile(0.5),
                '75%': col_data.quantile(0.75),
                'Skewness': stats.skew(col_data),
                'Kurtosis': stats.kurtosis(col_data)
            })
        return pd.DataFrame(summary_data).set_index('Variable')
