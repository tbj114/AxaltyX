
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt


class Clustering:
    @staticmethod
    def kmeans(data, columns, n_clusters, random_state=42):
        data_clean = data[columns].dropna()
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_clean)
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        labels = kmeans.fit_predict(data_scaled)
        result = data_clean.copy()
        result['Cluster'] = labels
        centroids = pd.DataFrame(
            scaler.inverse_transform(kmeans.cluster_centers_),
            columns=columns,
            index=[f'Cluster{i}' for i in range(n_clusters)]
        )
        return {
            'model': kmeans,
            'clustered_data': result,
            'centroids': centroids,
            'inertia': kmeans.inertia_
        }
    
    @staticmethod
    def hierarchical(data, columns, method='ward', metric='euclidean'):
        data_clean = data[columns].dropna()
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_clean)
        Z = linkage(data_scaled, method=method, metric=metric)
        return {
            'linkage_matrix': Z,
            'data': data_clean
        }
    
    @staticmethod
    def elbow_method(data, columns, max_clusters=10):
        data_clean = data[columns].dropna()
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_clean)
        inertias = []
        for k in range(1, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(data_scaled)
            inertias.append(kmeans.inertia_)
        return {
            'clusters': list(range(1, max_clusters + 1)),
            'inertias': inertias
        }
