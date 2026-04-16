
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import logit
from sklearn.linear_model import LogisticRegression as SKLogisticRegression


class LogisticRegression:
    @staticmethod
    def binary_logistic(data, formula):
        model = logit(formula, data=data).fit()
        return {
            'model': model,
            'summary': model.summary(),
            'odds_ratios': np.exp(model.params)
        }
    
    @staticmethod
    def sklearn_logistic(data, X_cols, y_col, C=1.0, penalty='l2'):
        data_clean = data[X_cols + [y_col]].dropna()
        X = data_clean[X_cols]
        y = data_clean[y_col]
        
        model = SKLogisticRegression(C=C, penalty=penalty, solver='liblinear')
        model.fit(X, y)
        
        return {
            'model': model,
            'coefficients': dict(zip(X_cols, model.coef_[0])),
            'intercept': model.intercept_[0],
            'odds_ratios': dict(zip(X_cols, np.exp(model.coef_[0]))),
            'score': model.score(X, y)
        }
    
    @staticmethod
    def ordinal_logistic(data, formula):
        from statsmodels.miscmodels.ordinal_model import OrderedModel
        model = OrderedModel.from_formula(formula, data=data).fit()
        return {
            'model': model,
            'summary': model.summary()
        }
    
    @staticmethod
    def predict_probability(model, new_data):
        return model.predict(new_data)
