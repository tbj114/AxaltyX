
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud


class BasicPlots:
    @staticmethod
    def bar_plot(data, x, y=None, hue=None, title=None, stacked=False, horizontal=False):
        fig, ax = plt.subplots(figsize=(10, 6))
        if y is None:
            if horizontal:
                data[x].value_counts().plot(kind='barh', ax=ax)
            else:
                data[x].value_counts().plot(kind='bar', ax=ax)
        else:
            if stacked:
                pivot_data = data.pivot_table(index=x, columns=hue, values=y, aggfunc='sum')
                pivot_data.plot(kind='bar', stacked=True, ax=ax)
            else:
                sns.barplot(data=data, x=x, y=y, hue=hue, ax=ax)
        
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def histogram(data, column, bins='auto', kde=False, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=data, x=column, bins=bins, kde=kde, ax=ax)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def density_plot(data, columns=None, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        if columns:
            for col in columns:
                sns.kdeplot(data=data, x=col, label=col, ax=ax)
            ax.legend()
        else:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                sns.kdeplot(data=data, x=col, label=col, ax=ax)
            ax.legend()
        
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def scatter_plot(data, x, y, hue=None, size=None, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=data, x=x, y=y, hue=hue, size=size, ax=ax)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def line_plot(data, x, y, hue=None, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=data, x=x, y=y, hue=hue, ax=ax)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def box_plot(data, x=None, y=None, hue=None, title=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=data, x=x, y=y, hue=hue, ax=ax)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def pie_chart(data, column, title=None):
        fig, ax = plt.subplots(figsize=(10, 10))
        data[column].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def heatmap(data, columns=None, annot=True, cmap='coolwarm', title=None):
        corr_data = data[columns].corr() if columns else data.corr()
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr_data, annot=annot, cmap=cmap, ax=ax, center=0)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def word_cloud(text, max_words=100, background_color='white'):
        wordcloud = WordCloud(
            max_words=max_words,
            background_color=background_color
        ).generate(text)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout()
        return fig
