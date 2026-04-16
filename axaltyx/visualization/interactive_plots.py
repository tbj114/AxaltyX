
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots


class InteractivePlots:
    @staticmethod
    def interactive_scatter(data, x, y, color=None, size=None, title=None):
        fig = px.scatter(data, x=x, y=y, color=color, size=size, title=title)
        fig.update_layout(height=600)
        return fig
    
    @staticmethod
    def interactive_line(data, x, y, color=None, title=None):
        fig = px.line(data, x=x, y=y, color=color, title=title)
        fig.update_layout(height=600)
        return fig
    
    @staticmethod
    def interactive_bar(data, x, y=None, color=None, barmode='group', title=None):
        if y is None:
            count_data = data[x].value_counts().reset_index()
            count_data.columns = [x, 'count']
            fig = px.bar(count_data, x=x, y='count', color=color, barmode=barmode, title=title)
        else:
            fig = px.bar(data, x=x, y=y, color=color, barmode=barmode, title=title)
        
        fig.update_layout(height=600)
        return fig
    
    @staticmethod
    def interactive_heatmap(data, columns=None, title=None):
        corr_data = data[columns].corr() if columns else data.corr()
        fig = px.imshow(corr_data, text_auto=True, aspect='auto', title=title)
        fig.update_layout(height=700)
        return fig
    
    @staticmethod
    def interactive_3d_scatter(data, x, y, z, color=None, title=None):
        fig = px.scatter_3d(data, x=x, y=y, z=z, color=color, title=title)
        fig.update_layout(height=700)
        return fig
    
    @staticmethod
    def interactive_pie(data, column, title=None):
        count_data = data[column].value_counts().reset_index()
        count_data.columns = [column, 'count']
        fig = px.pie(count_data, values='count', names=column, title=title)
        fig.update_layout(height=600)
        return fig
    
    @staticmethod
    def interactive_sunburst(data, path, values=None, title=None):
        fig = px.sunburst(data, path=path, values=values, title=title)
        fig.update_layout(height=700)
        return fig
    
    @staticmethod
    def interactive_treemap(data, path, values=None, title=None):
        fig = px.treemap(data, path=path, values=values, title=title)
        fig.update_layout(height=700)
        return fig
    
    @staticmethod
    def interactive_sankey(data, source, target, value, title=None):
        fig = px.sankey(data, source=source, target=target, value=value, title=title)
        fig.update_layout(height=700)
        return fig
    
    @staticmethod
    def interactive_radar(data, r, theta, color=None, title=None):
        fig = px.line_polar(data, r=r, theta=theta, color=color, line_close=True, title=title)
        fig.update_layout(height=700)
        return fig
