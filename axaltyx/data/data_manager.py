
import pandas as pd
import numpy as np


class DataManager:
    def __init__(self, data=None):
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
    
    def load_csv(self, filepath, **kwargs):
        self.data = pd.read_csv(filepath, **kwargs)
        return self
    
    def load_excel(self, filepath, **kwargs):
        self.data = pd.read_excel(filepath, **kwargs)
        return self
    
    def save_csv(self, filepath, **kwargs):
        self.data.to_csv(filepath, **kwargs)
        return self
    
    def save_excel(self, filepath, **kwargs):
        self.data.to_excel(filepath, **kwargs)
        return self
    
    def select_columns(self, columns):
        return DataManager(self.data[columns])
    
    def filter_rows(self, condition):
        return DataManager(self.data[condition])
    
    def add_column(self, name, values):
        self.data[name] = values
        return self
    
    def drop_columns(self, columns):
        return DataManager(self.data.drop(columns=columns))
    
    def drop_na(self, axis=0, how='any'):
        return DataManager(self.data.dropna(axis=axis, how=how))
    
    def get_data(self):
        return self.data.copy()
    
    def head(self, n=5):
        return self.data.head(n)
    
    def info(self):
        return self.data.info()
    
    def describe(self):
        return self.data.describe()
