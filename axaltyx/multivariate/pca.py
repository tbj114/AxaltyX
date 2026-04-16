
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA as SKPCA
from sklearn.preprocessing import StandardScaler


class PCA:
    @staticmethod
    def fit(data, columns, n_components=None):
        data_clean = data[columns].dropna()
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_clean)
        
        pca = SKPCA(n_components=n_components)
        pca_result = pca.fit_transform(data_scaled)
        
        components = pd.DataFrame(
            pca.components_,
            index=[f'PC{i+1}' for i in range(pca.n_components_)],
            columns=columns
        )
        
        explained_variance = pd.DataFrame({
            'Eigenvalue': pca.explained_variance_,
            'Proportion': pca.explained_variance_ratio_,
            'Cumulative': np.cumsum(pca.explained_variance_ratio_)
        }, index=[f'PC{i+1}' for i in range(pca.n_components_)])
        
        transformed_data = pd.DataFrame(
            pca_result,
            index=data_clean.index,
            columns=[f'PC{i+1}' for i in range(pca.n_components_)]
        )
        
        return {
            'model': pca,
            'components': components,
            'explained_variance': explained_variance,
            'transformed_data': transformed_data
        }
