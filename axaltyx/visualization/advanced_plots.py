
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import dendrogram
from sklearn.metrics import roc_curve, auc, confusion_matrix


class AdvancedPlots:
    @staticmethod
    def dendrogram_plot(linkage_matrix, labels=None, title=None):
        fig, ax = plt.subplots(figsize=(12, 6))
        dendrogram(linkage_matrix, labels=labels, leaf_rotation=90, ax=ax)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def roc_curve_plot(y_true, y_score, title=None):
        fpr, tpr, _ = roc_curve(y_true, y_score)
        roc_auc = auc(fpr, tpr)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (area = {roc_auc:.3f})')
        ax.plot([0, 1], [0, 1], 'k--', lw=2)
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.legend(loc="lower right")
        
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def confusion_matrix_plot(y_true, y_pred, labels=None, normalize=False, title=None):
        cm = confusion_matrix(y_true, y_pred)
        
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='.2f' if normalize else 'd', 
                    cmap='Blues', xticklabels=labels, yticklabels=labels, ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('True')
        
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def surface_plot(x, y, z, title=None):
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(x, y, z, cmap='viridis', linewidth=0, antialiased=True)
        fig.colorbar(surf, ax=ax)
        
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def population_pyramid(data, age_col, gender_col, value_col=None, title=None):
        if value_col is None:
            data = data.groupby([age_col, gender_col]).size().reset_index(name='count')
            value_col = 'count'
        
        males = data[data[gender_col] == 'Male'].copy()
        females = data[data[gender_col] == 'Female'].copy()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        ax1.barh(males[age_col], males[value_col], color='skyblue', label='Male')
        ax1.invert_xaxis()
        ax1.set_xlabel('Male')
        
        ax2.barh(females[age_col], females[value_col], color='pink', label='Female')
        ax2.set_xlabel('Female')
        
        if title:
            fig.suptitle(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def pareto_plot(data, column, title=None):
        count_data = data[column].value_counts().sort_values(ascending=False)
        cumulative = count_data.cumsum() / count_data.sum() * 100
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        
        ax1.bar(count_data.index, count_data.values, color='skyblue')
        ax2.plot(count_data.index, cumulative.values, color='red', marker='o')
        
        ax1.set_xlabel(column)
        ax1.set_ylabel('Frequency', color='skyblue')
        ax2.set_ylabel('Cumulative %', color='red')
        
        if title:
            ax1.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def interaction_plot(data, x_col, trace_col, y_col, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        means = data.groupby([x_col, trace_col])[y_col].mean().reset_index()
        
        for level in means[trace_col].unique():
            subset = means[means[trace_col] == level]
            ax.plot(subset[x_col], subset[y_col], marker='o', label=f'{trace_col} = {level}')
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(f'Mean of {y_col}')
        ax.legend()
        
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
