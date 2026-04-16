
import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter, CoxPHFitter, WeibullFitter


class SurvivalAnalysis:
    @staticmethod
    def kaplan_meier(data, duration_col, event_col):
        kmf = KaplanMeierFitter()
        kmf.fit(data[duration_col], data[event_col])
        return {
            'model': kmf,
            'survival_function': kmf.survival_function_
        }
    
    @staticmethod
    def cox_ph(data, duration_col, event_col, covariates):
        cph = CoxPHFitter()
        cols = [duration_col, event_col] + covariates
        cph.fit(data[cols], duration_col=duration_col, event_col=event_col)
        return {
            'model': cph,
            'summary': cph.summary()
        }
    
    @staticmethod
    def weibull(data, duration_col, event_col):
        wf = WeibullFitter()
        wf.fit(data[duration_col], data[event_col])
        return {
            'model': wf,
            'parameters': {
                'lambda_': wf.lambda_,
                'rho_': wf.rho_
            }
        }
