
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing


class TimeSeriesAnalysis:
    @staticmethod
    def decompose(data, column, model='additive', period=None):
        ts = data[column].dropna()
        decomposition = sm.tsa.seasonal_decompose(ts, model=model, period=period)
        return {
            'decomposition': decomposition,
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid
        }
    
    @staticmethod
    def arima(data, column, order=(1, 0, 0)):
        ts = data[column].dropna()
        model = ARIMA(ts, order=order)
        result = model.fit()
        return {
            'model': result,
            'summary': result.summary(),
            'forecast': result.forecast
        }
    
    @staticmethod
    def exponential_smoothing(data, column, trend=None, seasonal=None, seasonal_periods=None):
        ts = data[column].dropna()
        model = ExponentialSmoothing(ts, trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)
        result = model.fit()
        return {
            'model': result,
            'forecast': result.forecast
        }
