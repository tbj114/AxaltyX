
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder


class DataTransform:
    @staticmethod
    def standardize(data, columns=None):
        data_copy = data.copy()
        cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        scaler = StandardScaler()
        data_copy[cols] = scaler.fit_transform(data_copy[cols])
        return data_copy
    
    @staticmethod
    def normalize(data, columns=None):
        data_copy = data.copy()
        cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        scaler = MinMaxScaler()
        data_copy[cols] = scaler.fit_transform(data_copy[cols])
        return data_copy
    
    @staticmethod
    def log_transform(data, columns=None):
        data_copy = data.copy()
        cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        for col in cols:
            data_copy[col] = np.log1p(data_copy[col])
        return data_copy
    
    @staticmethod
    def label_encode(data, columns):
        data_copy = data.copy()
        encoders = {}
        for col in columns:
            encoder = LabelEncoder()
            data_copy[col] = encoder.fit_transform(data_copy[col].astype(str))
            encoders[col] = encoder
        return data_copy, encoders
    
    @staticmethod
    def one_hot_encode(data, columns, drop_first=False):
        return pd.get_dummies(data, columns=columns, drop_first=drop_first)
    
    @staticmethod
    def reshape_wide_to_long(data, id_vars, var_name, value_name):
        return pd.melt(data, id_vars=id_vars, var_name=var_name, value_name=value_name)
    
    @staticmethod
    def reshape_long_to_wide(data, index, columns, values):
        return data.pivot(index=index, columns=columns, values=values)
    
    @staticmethod
    def aggregate(data, groupby, agg_dict):
        return data.groupby(groupby).agg(agg_dict)
