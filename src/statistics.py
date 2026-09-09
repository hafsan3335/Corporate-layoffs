"""
Inferential statistics, nonparametric hypothesis testing, effect sizes,
and concentration metrics for Strategic HRM Layoffs research.
"""
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def calculate_hhi(series: pd.Series) -> float:
    """
    Calculate Herfindahl-Hirschman Index (HHI) for market/industry concentration.
    Formula: sum of squared market shares (ranging from 0 to 10,000).
    """
    counts = series.value_counts(dropna=True)
    if len(counts) == 0:
        return 0.0
    shares = (counts / counts.sum()) * 100
    hhi = float(np.sum(shares ** 2))
    return hhi


def run_spearman_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Spearman rank correlations, p-values, and 95% confidence intervals
    between continuous variables (robust to severe right-skewness).
    """
    vars_to_test = ["total_laid_off", "percentage_laid_off", "funds_raised"]
    results = []
    
    pairs = [
        ("funds_raised", "total_laid_off", "Capitalization vs. Layoff Magnitude"),
        ("funds_raised", "percentage_laid_off", "Capitalization vs. Layoff Intensity"),
        ("total_laid_off", "percentage_laid_off", "Layoff Magnitude vs. Layoff Intensity")
    ]
    
    for v1, v2, desc in pairs:
        subset = df[[v1, v2]].dropna()
        n = len(subset)
        if n > 2:
            rho, pval = stats.spearmanr(subset[v1], subset[v2])
            # Fisher z-transformation for 95% CI on Spearman rank
            z = np.arctanh(rho)
            se = 1.0 / np.sqrt(n - 3)
            ci_lower = np.tanh(z - 1.96 * se)
            ci_upper = np.tanh(z + 1.96 * se)
            
            results.append({
                "Variable 1": v1,
                "Variable 2": v2,
                "Relationship": desc,
                "Sample Size (N)": n,
                "Spearman Rho": round(rho, 4),
                "p-value": pval,
                "95% CI Lower": round(ci_lower, 4),
                "95% CI Upper": round(ci_upper, 4),
                "Significance": "***" if pval < 0.001 else ("**" if pval < 0.01 else ("*" if pval < 0.05 else "ns"))
            })
            
    return pd.DataFrame(results)


def run_kruskal_wallis_group(df: pd.DataFrame, group_col: str, metric_col: str) -> Dict[str, Any]:
    """
    Run Kruskal-Wallis non-parametric ANOVA test and compute Epsilon-Squared (epsilon^2) effect size.
    Epsilon-Squared: (H - k + 1) / (N - k), representing proportion of variance explained by rank.
    """
    clean_sub = df[[group_col, metric_col]].dropna()
    groups = [group[metric_col].values for name, group in clean_sub.groupby(group_col) if len(group) >= 5]
    group_names = [name for name, group in clean_sub.groupby(group_col) if len(group) >= 5]
    
    k = len(groups)
    n = len(clean_sub[clean_sub[group_col].isin(group_names)])
    
    if k < 2 or n <= k:
        return {"error": "Insufficient groups or sample size"}
        
    stat, pval = stats.kruskal(*groups)
    
    # Epsilon squared effect size
    epsilon_sq = (stat - k + 1) / (n - k) if (n - k) > 0 else 0.0
    epsilon_sq = max(0.0, min(1.0, epsilon_sq))
    
    # Also calculate standard one-way parametric ANOVA for comparison
    f_stat, f_pval = stats.f_oneway(*groups)
    # Eta squared
    ss_between = sum(len(g) * (np.mean(g) - clean_sub[metric_col].mean())**2 for g in groups)
    ss_total = np.sum((clean_sub[metric_col] - clean_sub[metric_col].mean())**2)
    eta_sq = ss_between / ss_total if ss_total > 0 else 0.0

    return {
        "group_col": group_col,
        "metric_col": metric_col,
        "n_groups": k,
        "total_n": n,
        "kruskal_stat_H": round(float(stat), 3),
        "kruskal_pval": float(pval),
        "epsilon_squared": round(float(epsilon_sq), 4),
        "anova_F": round(float(f_stat), 3),
        "anova_pval": float(f_pval),
        "eta_squared": round(float(eta_sq), 4)
    }


def run_chi_square_contingency(df: pd.DataFrame, col1: str, col2: str) -> Dict[str, Any]:
    """
    Calculate Pearson Chi-Square test of independence and Cramér's V effect size.
    """
    subset = df[[col1, col2]].dropna()
    # Filter out categories with extremely small counts
    crosstab = pd.crosstab(subset[col1], subset[col2])
    chi2, pval, dof, expected = stats.chi2_contingency(crosstab)
    
    n = crosstab.sum().sum()
    min_dim = min(crosstab.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim)) if (n * min_dim) > 0 else 0.0
    
    return {
        "col1": col1,
        "col2": col2,
        "n": int(n),
        "chi2_stat": round(float(chi2), 3),
        "p_value": float(pval),
        "dof": int(dof),
        "cramers_v": round(float(cramers_v), 4)
    }


def run_comprehensive_statistical_battery(events_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Execute all core inferential statistical tests:
    1. Spearman rank correlations (Capital vs. Magnitude, Capital vs. Intensity)
    2. Kruskal-Wallis across Industry on percentage_laid_off
    3. Kruskal-Wallis across Funding Stage on percentage_laid_off and total_laid_off
    4. Kruskal-Wallis across Macroeconomic Regime
    5. Chi-square on Region vs Severity Tier
    6. HHI Industry concentration by year
    """
    results = {}
    
    # 1. Spearman Correlations
    results["spearman"] = run_spearman_correlations(events_df)
    
    # 2. Non-parametric ANOVAs
    results["kw_industry_pct"] = run_kruskal_wallis_group(events_df, "industry_group", "percentage_laid_off")
    results["kw_stage_pct"] = run_kruskal_wallis_group(events_df, "stage_group", "percentage_laid_off")
    results["kw_stage_count"] = run_kruskal_wallis_group(events_df, "stage_group", "total_laid_off")
    results["kw_regime_pct"] = run_kruskal_wallis_group(events_df, "macro_regime", "percentage_laid_off")
    results["kw_regime_count"] = run_kruskal_wallis_group(events_df, "macro_regime", "total_laid_off")
    
    # 3. Chi-Square
    results["chi2_region_severity"] = run_chi_square_contingency(events_df, "region", "severity_magnitude")
    
    # 4. HHI Concentration across years
    hhi_by_year = {}
    for yr, g in events_df.groupby("year"):
        hhi_by_year[int(yr)] = round(calculate_hhi(g["industry_group"]), 2)
    results["hhi_by_year"] = hhi_by_year
    
    return results
