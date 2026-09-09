"""
Workforce Restructuring Risk Indicator (WRRI) conceptual framework.
Standardized composite index (0-100) quantifying organizational human-capital disruption risk.
NOTE: This is an analytical research index designed for this study, not an established statutory HR standard.
"""
from typing import Tuple
import numpy as np
import pandas as pd


def compute_event_risk_index(df_events: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Workforce Restructuring Risk Indicator (WRRI) at the event level.
    Components:
    1. Intensity Score (0-25): workforce percentage cut
    2. Magnitude Score (0-25): log-scaled headcount displacement
    3. Recurrence Score (0-25): single vs. repeated organizational restructuring
    4. Velocity Score (0-25): temporal compression between successive rounds
    """
    df = df_events.copy()

    # 1. Intensity Component (0 - 25)
    # 50% cut = 25 pts; 10% = 5 pts; median default if missing
    pct = df["percentage_laid_off"].fillna(df["percentage_laid_off"].median())
    comp_intensity = np.clip(pct * 50.0, 0, 25)

    # 2. Magnitude Component (0 - 25)
    # Log-scaled: 10,000 workers = 25 pts; 100 workers = 12.5 pts
    laid_off = df["total_laid_off"].fillna(df["total_laid_off"].median())
    log_headcount = np.log1p(laid_off)
    max_log_ref = np.log1p(10000)
    comp_magnitude = np.clip((log_headcount / max_log_ref) * 25.0, 0, 25)

    # 3. Recurrence Component (0 - 25)
    # Events per company
    def score_recurrence(cnt):
        if cnt == 1:
            return 5.0
        elif cnt == 2:
            return 15.0
        else:
            return 25.0

    comp_recurrence = df["company_total_events"].apply(score_recurrence)

    # 4. Velocity Component (0 - 25)
    # Days since prior layoff (temporal compression)
    def score_velocity(days, cnt):
        if cnt == 1 or pd.isna(days):
            return 5.0  # Baseline for single event
        if days < 90:
            return 25.0  # Acute, hyper-frequent shock (< 3 months)
        elif days < 180:
            return 20.0  # Frequent shock (< 6 months)
        elif days < 365:
            return 12.0  # Annual rhythm
        else:
            return 7.0   # Well-spaced multi-year adjustment

    comp_velocity = [
        score_velocity(d, c)
        for d, c in zip(df["days_since_prior_layoff"], df["company_total_events"])
    ]
    comp_velocity = np.array(comp_velocity)

    # Composite WRRI
    wrri = comp_intensity + comp_magnitude + comp_recurrence + comp_velocity
    df["wrri_intensity_comp"] = comp_intensity.round(1)
    df["wrri_magnitude_comp"] = comp_magnitude.round(1)
    df["wrri_recurrence_comp"] = comp_recurrence.round(1)
    df["wrri_velocity_comp"] = comp_velocity.round(1)
    df["wrri_score"] = wrri.round(1)

    # Categorize Risk Exposure
    def categorize_risk(score):
        if score < 35:
            return "Lower Risk Exposure"
        elif score < 55:
            return "Moderate Risk Exposure"
        elif score < 75:
            return "Elevated Risk Exposure"
        else:
            return "Critical / Chronic Risk Exposure"

    df["wrri_category"] = df["wrri_score"].apply(categorize_risk)
    return df
