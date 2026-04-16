
import pandas as pd
import numpy as np
import pymc3 as pm


class BayesianStats:
    @staticmethod
    def linear_regression(data, X_cols, y_col):
        with pm.Model() as model:
            alpha = pm.Normal('alpha', mu=0, sd=10)
            betas = pm.Normal('betas', mu=0, sd=10, shape=len(X_cols))
            sigma = pm.HalfNormal('sigma', sd=10)
            
            mu = alpha + pm.math.dot(data[X_cols], betas)
            likelihood = pm.Normal('y', mu=mu, sd=sigma, observed=data[y_col])
            
            trace = pm.sample(2000, tune=1000, return_inferencedata=True)
        
        return {
            'model': model,
            'trace': trace
        }
    
    @staticmethod
    def logistic_regression(data, X_cols, y_col):
        with pm.Model() as model:
            alpha = pm.Normal('alpha', mu=0, sd=10)
            betas = pm.Normal('betas', mu=0, sd=10, shape=len(X_cols))
            
            mu = alpha + pm.math.dot(data[X_cols], betas)
            p = pm.invlogit(mu)
            likelihood = pm.Bernoulli('y', p=p, observed=data[y_col])
            
            trace = pm.sample(2000, tune=1000, return_inferencedata=True)
        
        return {
            'model': model,
            'trace': trace
        }
