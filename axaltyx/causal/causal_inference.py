
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors


class CausalInference:
    @staticmethod
    def propensity_score_matching(data, treatment_col, outcome_col, covariates, k=1):
        X = data[covariates]
        treatment = data[treatment_col]
        
        ps_model = LogisticRegression()
        ps_model.fit(X, treatment)
        propensity_scores = ps_model.predict_proba(X)[:, 1]
        
        treated = data[treatment == 1].copy()
        control = data[treatment == 0].copy()
        
        treated_ps = propensity_scores[treatment == 1]
        control_ps = propensity_scores[treatment == 0]
        
        nn = NearestNeighbors(n_neighbors=k)
        nn.fit(control_ps.reshape(-1, 1))
        distances, indices = nn.kneighbors(treated_ps.reshape(-1, 1))
        
        matched_data = []
        for i, treated_idx in enumerate(treated.index):
            matched_data.append(data.loc[treated_idx])
            for match_idx in indices[i]:
                matched_data.append(control.iloc[match_idx])
        
        matched_df = pd.DataFrame(matched_data)
        
        ate = (matched_df[matched_df[treatment_col] == 1][outcome_col].mean() -
               matched_df[matched_df[treatment_col] == 0][outcome_col].mean())
        
        return {
            'matched_data': matched_df,
            'propensity_scores': propensity_scores,
            'ate': ate
        }
