"""
Feature engineering and company-level aggregation module for Strategic HRM Layoffs analysis.
"""
from datetime import datetime
from typing import Tuple
import numpy as np
import pandas as pd

from src.config import MACRO_REGIMES


# Geographic mapping from Country to Global Macro-Region
COUNTRY_TO_REGION = {
    "United States": "North America",
    "Canada": "North America",
    "United Kingdom": "Europe",
    "Germany": "Europe",
    "Netherlands": "Europe",
    "France": "Europe",
    "Sweden": "Europe",
    "Ireland": "Europe",
    "Spain": "Europe",
    "Switzerland": "Europe",
    "Norway": "Europe",
    "Denmark": "Europe",
    "Finland": "Europe",
    "Estonia": "Europe",
    "Portugal": "Europe",
    "Austria": "Europe",
    "Belgium": "Europe",
    "India": "Asia-Pacific",
    "Singapore": "Asia-Pacific",
    "Australia": "Asia-Pacific",
    "Indonesia": "Asia-Pacific",
    "China": "Asia-Pacific",
    "Japan": "Asia-Pacific",
    "South Korea": "Asia-Pacific",
    "Hong Kong": "Asia-Pacific",
    "Malaysia": "Asia-Pacific",
    "New Zealand": "Asia-Pacific",
    "Vietnam": "Asia-Pacific",
    "Thailand": "Asia-Pacific",
    "Israel": "Middle East",
    "United Arab Emirates": "Middle East",
    "Saudi Arabia": "Middle East",
    "Brazil": "Latin America",
    "Mexico": "Latin America",
    "Colombia": "Latin America",
    "Argentina": "Latin America",
    "Chile": "Latin America",
    "Nigeria": "Africa",
    "Kenya": "Africa",
    "South Africa": "Africa",
    "Egypt": "Africa",
    "Ghana": "Africa"
}


def assign_macro_regime(date_val: pd.Timestamp) -> str:
    """Assign an event to an economic/macro regime period."""
    if pd.isna(date_val):
        return "Unknown"
    date_str = date_val.strftime("%Y-%m-%d")
    for regime_key, (start, end, label) in MACRO_REGIMES.items():
        if start <= date_str <= end:
            return label
    return "Phase 4: AI Pivot & Structural Realignment"


def engineer_event_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construct temporal, logarithmic, geographic, and quantile severity features
    at the individual layoff event level.
    """
    data = df.copy()

    # 1. Temporal dimensions
    data["year"] = data["date"].dt.year
    data["quarter"] = data["date"].dt.quarter
    data["month"] = data["date"].dt.month
    data["month_name"] = data["date"].dt.month_name()
    data["year_month"] = data["date"].dt.to_period("M").astype(str)
    data["day_of_week"] = data["date"].dt.day_name()
    data["macro_regime"] = data["date"].apply(assign_macro_regime)

    # 2. Geographic Region
    data["region"] = data["country"].map(COUNTRY_TO_REGION).fillna("Other / International")

    # 3. Logarithmic transformations (handling skewness)
    data["laid_off_log"] = np.log1p(data["total_laid_off"])
    data["funding_log"] = np.log1p(data["funds_raised"])

    # 4. Layoff Severity Tiers (Empirical Quantiles on observed values)
    # Headcount Severity Tiers
    headcount_q = data["total_laid_off"].dropna()
    q25, q50, q75, q90 = headcount_q.quantile([0.25, 0.50, 0.75, 0.90])
    
    def classify_magnitude(val):
        if pd.isna(val):
            return "Unreported"
        if val <= q25:
            return f"Low (<= {int(q25)})"
        elif val <= q75:
            return f"Moderate ({int(q25)+1} - {int(q75)})"
        elif val <= q90:
            return f"High ({int(q75)+1} - {int(q90)})"
        else:
            return f"Mega-Event (> {int(q90)})"

    data["severity_magnitude"] = data["total_laid_off"].apply(classify_magnitude)

    # Percentage Intensity Tiers (Substantive theoretical thresholds)
    def classify_intensity(val):
        if pd.isna(val):
            return "Unreported"
        if val < 0.10:
            return "Targeted (< 10%)"
        elif val <= 0.20:
            return "Substantial (10% - 20%)"
        elif val <= 0.40:
            return "Severe (20% - 40%)"
        else:
            return "Existential / Drastic (> 40%)"

    data["severity_intensity"] = data["percentage_laid_off"].apply(classify_intensity)

    # 5. Inter-event spacing and recurrence flags within the event table
    # Sort by company and date
    data = data.sort_values(by=["company", "date"]).reset_index(drop=True)
    data["prev_event_date"] = data.groupby("company")["date"].shift(1)
    data["days_since_prior_layoff"] = (data["date"] - data["prev_event_date"]).dt.days
    data["event_sequence_number"] = data.groupby("company").cumcount() + 1
    
    # Total events per company mapped back
    company_event_counts = data.groupby("company")["date"].transform("count")
    data["company_total_events"] = company_event_counts
    data["is_repeated_restructurer"] = data["company_total_events"] > 1

    return data


def create_company_profiles(df_events: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate event-level records into an organizational unit-of-analysis dataset.
    Crucial for analyzing organizational recurrence, chronic downsizing, and clustering.
    """
    records = []
    grouped = df_events.groupby("company")

    for company, group in grouped:
        event_count = len(group)
        dates = group["date"].sort_values().tolist()
        first_date = dates[0]
        last_date = dates[-1]
        timespan_days = (last_date - first_date).days

        # Inter-event spacing
        if event_count > 1:
            diffs = [(dates[i] - dates[i - 1]).days for i in range(1, event_count)]
            mean_inter_event_days = float(np.mean(diffs))
            min_inter_event_days = float(np.min(diffs))
        else:
            mean_inter_event_days = np.nan
            min_inter_event_days = np.nan

        # Layoff magnitude aggregates
        laid_off_vals = group["total_laid_off"].dropna()
        total_laid_off = float(laid_off_vals.sum()) if len(laid_off_vals) > 0 else np.nan
        mean_laid_off = float(laid_off_vals.mean()) if len(laid_off_vals) > 0 else np.nan
        max_laid_off = float(laid_off_vals.max()) if len(laid_off_vals) > 0 else np.nan

        # Layoff intensity aggregates
        pct_vals = group["percentage_laid_off"].dropna()
        mean_percentage = float(pct_vals.mean()) if len(pct_vals) > 0 else np.nan
        median_percentage = float(pct_vals.median()) if len(pct_vals) > 0 else np.nan
        max_percentage = float(pct_vals.max()) if len(pct_vals) > 0 else np.nan

        # Firm descriptors (mode or last observed)
        industry = group["industry"].iloc[-1]
        industry_group = group["industry_group"].iloc[-1]
        stage = group["stage"].iloc[-1]
        stage_group = group["stage_group"].iloc[-1]
        country = group["country"].iloc[-1]
        region = group["region"].iloc[-1]
        funds_raised = group["funds_raised"].max()  # Peak reported funding

        records.append({
            "company": company,
            "event_count": event_count,
            "is_repeated": event_count > 1,
            "first_layoff_date": first_date,
            "last_layoff_date": last_date,
            "timespan_days": timespan_days,
            "mean_inter_event_days": mean_inter_event_days,
            "min_inter_event_days": min_inter_event_days,
            "total_laid_off": total_laid_off,
            "mean_laid_off": mean_laid_off,
            "max_laid_off": max_laid_off,
            "mean_percentage": mean_percentage,
            "median_percentage": median_percentage,
            "max_percentage": max_percentage,
            "industry": industry,
            "industry_group": industry_group,
            "stage": stage,
            "stage_group": stage_group,
            "country": country,
            "region": region,
            "funds_raised": funds_raised,
            "funds_raised_log": np.log1p(funds_raised) if pd.notna(funds_raised) else np.nan,
            "total_laid_off_log": np.log1p(total_laid_off) if pd.notna(total_laid_off) else np.nan
        })

    profiles_df = pd.DataFrame(records)
    return profiles_df
