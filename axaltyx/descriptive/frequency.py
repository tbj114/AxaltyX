
import pandas as pd
import numpy as np


class FrequencyAnalysis:
    @staticmethod
    def frequency_table(data, column, sort=True, ascending=False):
        freq = data[column].value_counts(sort=sort, ascending=ascending)
        percent = data[column].value_counts(normalize=True, sort=sort, ascending=ascending) * 100
        cumulative = percent.cumsum()
        
        table = pd.DataFrame({
            'Frequency': freq,
            'Percent': percent,
            'Cumulative Percent': cumulative
        })
        return table
    
    @staticmethod
    def histogram(data, column, bins='auto'):
        return np.histogram(data[column].dropna(), bins=bins)
    
    @staticmethod
    def grouped_frequency(data, column, groupby_column):
        return pd.crosstab(data[groupby_column], data[column])
    
    @staticmethod
    def multiple_response(data, columns, delimiter=None):
        if delimiter:
            all_responses = []
            for col in columns:
                responses = data[col].dropna().str.split(delimiter).explode()
                all_responses.extend(responses.tolist())
            return pd.Series(all_responses).value_counts()
        else:
            freq_data = {}
            for col in columns:
                freq_data[col] = data[col].sum()
            return pd.Series(freq_data)
