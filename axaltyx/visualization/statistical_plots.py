
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm


class StatisticalPlots:
    @staticmethod
    def qq_plot(data, column, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        col_data = data[column].dropna()
        stats.probplot(col_data, plot=ax)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def pp_plot(data, column, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        col_data = data[column].dropna()
        sorted_data = np.sort(col_data)
        ecdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        theorical = stats.norm.cdf(sorted_data, loc=np.mean(col_data), scale=np.std(col_data))
        
        ax.plot(theorical, ecdf, 'o')
        ax.plot([0, 1], [0, 1], 'r--')
        ax.set_xlabel('Theoretical Probability')
        ax.set_ylabel('Empirical Probability')
        
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def violin_plot(data, x=None, y=None, hue=None, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.violinplot(data=data, x=x, y=y, hue=hue, ax=ax)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def ridgeline_plot(data, column, group_column, title=None):
        g = sns.FacetGrid(data, row=group_column, aspect=15, height=0.75)
        g.map(sns.kdeplot, column, fill=True, alpha=0.8)
        g.set_titles('{row_name}')
        if title:
            g.fig.suptitle(title, y=1.02)
        return g.fig
    
    @staticmethod
    def scatter_matrix(data, columns=None, hue=None, title=None):
        cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        fig = sns.pairplot(data[cols], hue=hue)
        if title:
            fig.fig.suptitle(title, y=1.02)
        return fig.fig
    
    @staticmethod
    def residual_plot(model, data, x_col, y_col, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        residuals = model.resid
        fitted = model.fittedvalues
        
        ax.scatter(fitted, residuals)
        ax.axhline(y=0, color='r', linestyle='--')
        ax.set_xlabel('Fitted Values')
        ax.set_ylabel('Residuals')
        
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def acf_plot(data, column, lags=20, title=None):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        col_data = data[column].dropna()
        
        sm.graphics.tsa.plot_acf(col_data, lags=lags, ax=ax1)
        sm.graphics.tsa.plot_pacf(col_data, lags=lags, ax=ax2)
        
        if title:
            ax1.set_title(title)
        plt.tight_layout()
        return fig
