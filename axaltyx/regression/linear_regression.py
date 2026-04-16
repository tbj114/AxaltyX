
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.linear_model import LinearRegression as SKLinearRegression
from sklearn.linear_model import Lasso, Ridge, ElasticNet


class LinearRegression:
    @staticmethod
    def simple_linear(data, x_col, y_col):
        data_clean = data[[x_col, y_col]].dropna()
        X = sm.add_constant(data_clean[x_col])
        y = data_clean[y_col]
        
        model = sm.OLS(y, X).fit()
        return {
            'model': model,
            'summary': model.summary()
        }
    
    @staticmethod
    def multiple_linear(data, formula):
        model = ols(formula, data=data).fit()
        return {
            'model': model,
            'summary': model.summary()
        }
    
    @staticmethod
    def lasso(data, X_cols, y_col, alpha=1.0):
        data_clean = data[X_cols + [y_col]].dropna()
        X = data_clean[X_cols]
        y = data_clean[y_col]
        
        model = Lasso(alpha=alpha)
        model.fit(X, y)
        
        return {
            'model': model,
            'coefficients': dict(zip(X_cols, model.coef_)),
            'intercept': model.intercept_,
            'r_squared': model.score(X, y)
        }
    
    @staticmethod
    def ridge(data, X_cols, y_col, alpha=1.0):
        data_clean = data[X_cols + [y_col]].dropna()
        X = data_clean[X_cols]
        y = data_clean[y_col]
        
        model = Ridge(alpha=alpha)
        model.fit(X, y)
        
        return {
            'model': model,
            'coefficients': dict(zip(X_cols, model.coef_)),
            'intercept': model.intercept_,
            'r_squared': model.score(X, y)
        }
    
    @staticmethod
    def elastic_net(data, X_cols, y_col, alpha=1.0, l1_ratio=0.5):
        data_clean = data[X_cols + [y_col]].dropna()
        X = data_clean[X_cols]
        y = data_clean[y_col]
        
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
        model.fit(X, y)
        
        return {
            'model': model,
            'coefficients': dict(zip(X_cols, model.coef_)),
            'intercept': model.intercept_,
            'r_squared': model.score(X, y)
        }
