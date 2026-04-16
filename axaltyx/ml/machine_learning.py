
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score


class MachineLearning:
    @staticmethod
    def random_forest(data, X_cols, y_col, task='classification', test_size=0.2, random_state=42, **kwargs):
        X = data[X_cols].dropna()
        y = data.loc[X.index, y_col]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        if task == 'classification':
            model = RandomForestClassifier(random_state=random_state, **kwargs)
        else:
            model = RandomForestRegressor(random_state=random_state, **kwargs)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        if task == 'classification':
            score = accuracy_score(y_test, y_pred)
            score_name = 'Accuracy'
        else:
            score = r2_score(y_test, y_pred)
            score_name = 'R2 Score'
        
        return {
            'model': model,
            'predictions': y_pred,
            f'{score_name}': score,
            'feature_importances': pd.DataFrame({
                'feature': X_cols,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
        }
    
    @staticmethod
    def svm(data, X_cols, y_col, task='classification', test_size=0.2, random_state=42, **kwargs):
        X = data[X_cols].dropna()
        y = data.loc[X.index, y_col]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        if task == 'classification':
            model = SVC(random_state=random_state, **kwargs)
        else:
            model = SVR(**kwargs)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        if task == 'classification':
            score = accuracy_score(y_test, y_pred)
            score_name = 'Accuracy'
        else:
            score = r2_score(y_test, y_pred)
            score_name = 'R2 Score'
        
        return {
            'model': model,
            'predictions': y_pred,
            f'{score_name}': score
        }
    
    @staticmethod
    def neural_network(data, X_cols, y_col, task='classification', test_size=0.2, random_state=42, **kwargs):
        X = data[X_cols].dropna()
        y = data.loc[X.index, y_col]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        if task == 'classification':
            model = MLPClassifier(random_state=random_state, **kwargs)
        else:
            model = MLPRegressor(random_state=random_state, **kwargs)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        if task == 'classification':
            score = accuracy_score(y_test, y_pred)
            score_name = 'Accuracy'
        else:
            score = r2_score(y_test, y_pred)
            score_name = 'R2 Score'
        
        return {
            'model': model,
            'predictions': y_pred,
            f'{score_name}': score
        }
