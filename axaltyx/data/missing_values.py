
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer


class MissingValues:
    @staticmethod
    def count_missing(data):
        return data.isnull().sum()
    
    @staticmethod
    def proportion_missing(data):
        return data.isnull().mean() * 100
    
    @staticmethod
    def drop_missing(data, axis=0, threshold=None):
        if threshold:
            return data.dropna(axis=axis, thresh=threshold)
        return data.dropna(axis=axis)
    
    @staticmethod
    def impute_mean(data, columns=None):
        data_copy = data.copy()
        cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        imputer = SimpleImputer(strategy='mean')
        data_copy[cols] = imputer.fit_transform(data_copy[cols])
        return data_copy
    
    @staticmethod
    def impute_median(data, columns=None):
        data_copy = data.copy()
        cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        imputer = SimpleImputer(strategy='median')
        data_copy[cols] = imputer.fit_transform(data_copy[cols])
        return data_copy
    
    @staticmethod
    def impute_mode(data, columns=None):
        data_copy = data.copy()
        cols = columns if columns else data.columns
        for col in cols:
            data_copy[col] = data_copy[col].fillna(data_copy[col].mode()[0])
        return data_copy
    
    @staticmethod
    def impute_knn(data, n_neighbors=5):
        imputer = KNNImputer(n_neighbors=n_neighbors)
        return pd.DataFrame(imputer.fit_transform(data), columns=data.columns, index=data.index)
