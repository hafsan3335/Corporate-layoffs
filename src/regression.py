"""
Econometric and multivariate regression modeling module for Strategic HRM Layoffs analysis.
Utilizes statsmodels for rigorous statistical inference, HC3 robust standard errors,
interaction effects, and regression diagnostics.
"""
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor


def fit_layoff_magnitude_model(df: pd.DataFrame) -> Tuple[Any, pd.DataFrame, Dict[str, Any]]:
    """
    Model 1: Layoff Magnitude (Log-Transformed Headcount)
    Formula: laid_off_log ~ funding_log + C(stage_group) + C(industry_group) + C(year) + C(region)
    Fitted using OLS with Heteroscedasticity-Consistent (HC3) robust standard errors.
    """
    # Filter dataset for valid complete cases on modeled variables
    cols = ["laid_off_log", "funding_log", "stage_group", "industry_group", "year", "region"]
    model_data = df[cols].dropna().copy()
    model_data["year"] = model_data["year"].astype(str)
    
    # Establish explicit theoretically sound reference categories
    # Reference: Early Stage (Seed), Consumer & Retail, Year 2022, North America
    formula = (
        "laid_off_log ~ funding_log + "
        "C(stage_group, Treatment(reference='Early Stage (Seed)')) + "
        "C(industry_group, Treatment(reference='Consumer & Retail')) + "
        "C(year, Treatment(reference='2022')) + "
        "C(region, Treatment(reference='North America'))"
    )
    
    ols_model = smf.ols(formula=formula, data=model_data).fit(cov_type="HC3")
    
    # Format comprehensive results table
    summary_df = pd.DataFrame({
        "Coefficient": ols_model.params,
        "Robust_SE": ols_model.bse,
        "t_statistic": ols_model.tvalues,
        "p_value": ols_model.pvalues,
        "CI_Lower_95": ols_model.conf_int()[0],
        "CI_Upper_95": ols_model.conf_int()[1]
    })
    
    diagnostics = {
        "nobs": int(ols_model.nobs),
        "r_squared": round(float(ols_model.rsquared), 4),
        "adj_r_squared": round(float(ols_model.rsquared_adj), 4),
        "f_statistic": round(float(ols_model.fvalue), 2) if ols_model.fvalue is not None else np.nan,
        "f_pvalue": float(ols_model.f_pvalue) if ols_model.f_pvalue is not None else np.nan,
        "aic": round(float(ols_model.aic), 2),
        "bic": round(float(ols_model.bic), 2),
        "cov_type": "HC3 (MacKinnon and White heteroscedasticity-consistent)"
    }
    
    return ols_model, summary_df, diagnostics


def fit_layoff_intensity_model(df: pd.DataFrame) -> Tuple[Any, pd.DataFrame, Dict[str, Any]]:
    """
    Model 2: Layoff Intensity (Percentage Laid Off)
    Formula: percentage_laid_off ~ funding_log + C(stage_group) + C(industry_group) + C(year) + C(region)
    Fitted using OLS with HC3 robust standard errors on observed percentage events.
    """
    cols = ["percentage_laid_off", "funding_log", "stage_group", "industry_group", "year", "region"]
    model_data = df[cols].dropna().copy()
    model_data["year"] = model_data["year"].astype(str)
    
    formula = (
        "percentage_laid_off ~ funding_log + "
        "C(stage_group, Treatment(reference='Early Stage (Seed)')) + "
        "C(industry_group, Treatment(reference='Consumer & Retail')) + "
        "C(year, Treatment(reference='2022')) + "
        "C(region, Treatment(reference='North America'))"
    )
    
    ols_model = smf.ols(formula=formula, data=model_data).fit(cov_type="HC3")
    
    summary_df = pd.DataFrame({
        "Coefficient": ols_model.params,
        "Robust_SE": ols_model.bse,
        "t_statistic": ols_model.tvalues,
        "p_value": ols_model.pvalues,
        "CI_Lower_95": ols_model.conf_int()[0],
        "CI_Upper_95": ols_model.conf_int()[1]
    })
    
    diagnostics = {
        "nobs": int(ols_model.nobs),
        "r_squared": round(float(ols_model.rsquared), 4),
        "adj_r_squared": round(float(ols_model.rsquared_adj), 4),
        "f_statistic": round(float(ols_model.fvalue), 2) if ols_model.fvalue is not None else np.nan,
        "f_pvalue": float(ols_model.f_pvalue) if ols_model.f_pvalue is not None else np.nan,
        "aic": round(float(ols_model.aic), 2),
        "bic": round(float(ols_model.bic), 2),
        "cov_type": "HC3 (MacKinnon and White heteroscedasticity-consistent)"
    }
    
    return ols_model, summary_df, diagnostics


def fit_theoretically_justified_interaction_model(df: pd.DataFrame) -> Tuple[Any, pd.DataFrame, Dict[str, Any]]:
    """
    Model 3: Interaction Effects
    Tests whether the relationship between capitalization (funding_log) and restructuring intensity
    differed across macroeconomic regimes (e.g. Zero-Interest-Rate era vs. High-Interest-Rate era).
    Formula: percentage_laid_off ~ funding_log * C(macro_regime) + C(stage_group) + C(industry_group)
    """
    cols = ["percentage_laid_off", "funding_log", "macro_regime", "stage_group", "industry_group"]
    model_data = df[cols].dropna().copy()
    
    formula = (
        "percentage_laid_off ~ funding_log * C(macro_regime, Treatment(reference='Phase 1: COVID Shock & Virtualization')) + "
        "C(stage_group, Treatment(reference='Early Stage (Seed)')) + "
        "C(industry_group, Treatment(reference='Consumer & Retail'))"
    )
    
    ols_model = smf.ols(formula=formula, data=model_data).fit(cov_type="HC3")
    
    summary_df = pd.DataFrame({
        "Coefficient": ols_model.params,
        "Robust_SE": ols_model.bse,
        "t_statistic": ols_model.tvalues,
        "p_value": ols_model.pvalues,
        "CI_Lower_95": ols_model.conf_int()[0],
        "CI_Upper_95": ols_model.conf_int()[1]
    })
    
    diagnostics = {
        "nobs": int(ols_model.nobs),
        "r_squared": round(float(ols_model.rsquared), 4),
        "adj_r_squared": round(float(ols_model.rsquared_adj), 4),
        "f_statistic": round(float(ols_model.fvalue), 2) if ols_model.fvalue is not None else np.nan,
        "f_pvalue": float(ols_model.f_pvalue) if ols_model.f_pvalue is not None else np.nan,
        "cov_type": "HC3"
    }
    
    return ols_model, summary_df, diagnostics
