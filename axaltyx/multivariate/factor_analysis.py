
import pandas as pd
import numpy as np
from sklearn.decomposition import FactorAnalysis as SKFactorAnalysis
from sklearn.preprocessing import StandardScaler


class FactorAnalysis:
    @staticmethod
    def fit(data, columns, n_factors, rotation=None):
        data_clean = data[columns].dropna()
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_clean)
        
        fa = SKFactorAnalysis(n_components=n_factors, rotation=rotation)
        fa.fit(data_scaled)
        
        loadings = pd.DataFrame(
            fa.components_.T,
            index=columns,
            columns=[f'Factor{i+1}' for i in range(n_factors)]
        )
        
        variance = pd.DataFrame({
            'Variance': fa.noise_variance_,
            'Communality': 1 - fa.noise_variance_
        }, index=columns)
        
        return {
            'model': fa,
            'loadings': loadings,
            'variance': variance,
            'factor_variance': fa.get_covariance()
        }
