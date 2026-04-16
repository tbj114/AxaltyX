
import sys
import json
import traceback
import pandas as pd
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from axaltyx.data.data_manager import DataManager
from axaltyx.data.missing_values import MissingValues
from axaltyx.descriptive.descriptive_stats import DescriptiveStats
from axaltyx.inference.ttests import TTests
from axaltyx.inference.anova import ANOVA
from axaltyx.regression.correlation import Correlation
from axaltyx.regression.linear_regression import LinearRegression
from axaltyx.visualization.basic_plots import BasicPlots

class AxaltyXBridge:
    def __init__(self):
        self.data_manager = DataManager()
        self.df = None
        self.plots = BasicPlots()
    
    def load_data(self, file_path):
        try:
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(file_path)
            return {
                'success': True,
                'data': self.df.to_dict('records'),
                'columns': list(self.df.columns),
                'shape': self.df.shape
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def save_data(self, file_path, data):
        try:
            df = pd.DataFrame(data)
            if file_path.endswith('.csv'):
                df.to_csv(file_path, index=False)
            elif file_path.endswith(('.xlsx', '.xls')):
                df.to_excel(file_path, index=False)
            return {'success': True}
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def descriptive_stats(self, data, columns):
        try:
            df = pd.DataFrame(data)
            stats = DescriptiveStats(df)
            result = stats.summary(columns)
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def t_test(self, data, options):
        try:
            df = pd.DataFrame(data)
            t_tests = TTests(df)
            test_type = options.get('type', 'independent')
            
            if test_type == 'one_sample':
                result = t_tests.one_sample(
                    column=options['column'],
                    popmean=options.get('popmean', 0)
                )
            elif test_type == 'independent':
                result = t_tests.independent_samples(
                    column=options['column'],
                    group_column=options['group_column']
                )
            elif test_type == 'paired':
                result = t_tests.paired_samples(
                    column1=options['column1'],
                    column2=options['column2']
                )
            else:
                raise ValueError(f'Unknown test type: {test_type}')
            
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def anova(self, data, options):
        try:
            df = pd.DataFrame(data)
            anova = ANOVA(df)
            result = anova.one_way(
                dependent=options['dependent'],
                independent=options['independent']
            )
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def correlation(self, data, columns, method='pearson'):
        try:
            df = pd.DataFrame(data)
            corr = Correlation(df)
            if method == 'pearson':
                result = corr.pearson(columns)
            elif method == 'spearman':
                result = corr.spearman(columns)
            else:
                raise ValueError(f'Unknown method: {method}')
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def regression(self, data, options):
        try:
            df = pd.DataFrame(data)
            reg = LinearRegression(df)
            result = reg.fit(
                dependent=options['dependent'],
                independents=options['independents']
            )
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def plot(self, plot_type, data, options):
        try:
            df = pd.DataFrame(data)
            plots = BasicPlots(df)
            
            if plot_type == 'bar':
                fig = plots.bar_plot(
                    x=options.get('x'),
                    y=options.get('y'),
                    title=options.get('title', 'Bar Plot')
                )
            elif plot_type == 'histogram':
                fig = plots.histogram(
                    column=options.get('column'),
                    title=options.get('title', 'Histogram')
                )
            elif plot_type == 'scatter':
                fig = plots.scatter_plot(
                    x=options.get('x'),
                    y=options.get('y'),
                    title=options.get('title', 'Scatter Plot')
                )
            elif plot_type == 'heatmap':
                fig = plots.heatmap(
                    columns=options.get('columns'),
                    title=options.get('title', 'Heatmap')
                )
            else:
                raise ValueError(f'Unknown plot type: {plot_type}')
            
            import io
            import base64
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            
            return {
                'success': True,
                'image': img_base64
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def execute(self, command, args):
        try:
            method = getattr(self, command)
            return method(*args)
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }

def main():
    bridge = AxaltyXBridge()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            request = json.loads(line)
            command = request.get('command')
            args = request.get('args', [])
            
            result = bridge.execute(command, args)
            print(json.dumps(result))
            sys.stdout.flush()
        except Exception as e:
            error_response = {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == '__main__':
    main()
