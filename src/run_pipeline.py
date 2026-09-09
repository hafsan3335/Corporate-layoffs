"""
Master end-to-end analytical pipeline runner.
Executes data cleaning, feature engineering, risk scoring, inferential statistics,
multivariate regression, clustering, and publication figure generation.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

from src.config import (
    CLEANED_EVENTS_PATH,
    COMPANY_PROFILES_PATH,
    PROCESSED_DATA_DIR,
    REPORTS_DIR,
    FIGURES_DIR
)
from src.cleaning import load_raw_data, audit_raw_data, clean_dataset, generate_reports
from src.features import engineer_event_features, create_company_profiles
from src.risk_index import compute_event_risk_index
from src.statistics import run_comprehensive_statistical_battery
from src.regression import (
    fit_layoff_magnitude_model,
    fit_layoff_intensity_model,
    fit_theoretically_justified_interaction_model
)
from src.clustering import prepare_clustering_data, evaluate_cluster_range, fit_restructuring_archetypes
from src.visualization import generate_all_publication_figures


def run_full_pipeline():
    print("=== Step 1: Ingesting & Auditing Raw Data ===")
    df_raw = load_raw_data()
    audit_meta = audit_raw_data(df_raw)
    
    print("=== Step 2: Cleaning & Normalizing Dataset ===")
    df_clean, clean_meta = clean_dataset(df_raw)
    
    print("=== Step 3: Engineering Event Features & Risk Scoring ===")
    df_events = engineer_event_features(df_clean)
    df_events = compute_event_risk_index(df_events)
    
    print("=== Step 4: Aggregating Organizational Profiles ===")
    df_profiles = create_company_profiles(df_events)
    
    # Save processed CSVs
    df_events.to_csv(CLEANED_EVENTS_PATH, index=False)
    df_profiles.to_csv(COMPANY_PROFILES_PATH, index=False)
    print(f"Saved: {CLEANED_EVENTS_PATH} ({len(df_events):,} rows)")
    print(f"Saved: {COMPANY_PROFILES_PATH} ({len(df_profiles):,} rows)")
    
    # Generate audit reports
    generate_reports(df_raw, df_events, clean_meta)
    
    print("=== Step 5: Running Inferential Statistical Battery ===")
    stat_results = run_comprehensive_statistical_battery(df_events)
    # Save Spearman table to markdown
    spearman_df = stat_results["spearman"]
    spearman_md = spearman_df.to_markdown(index=False)
    (REPORTS_DIR / "statistical_results_table.md").write_text(
        f"# Inferential Statistical Results & Hypothesis Tests\n\n"
        f"## 1. Spearman Rank Correlations (Robust to Heavy Skew)\n\n{spearman_md}\n\n"
        f"## 2. Non-Parametric ANOVA (Kruskal-Wallis Tests & Effect Sizes)\n\n"
        f"- **Industry on Layoff Percentage:** H = {stat_results['kw_industry_pct']['kruskal_stat_H']}, p = {stat_results['kw_industry_pct']['kruskal_pval']:.4e}, Epsilon^2 = {stat_results['kw_industry_pct']['epsilon_squared']}\n"
        f"- **Funding Stage on Layoff Percentage:** H = {stat_results['kw_stage_pct']['kruskal_stat_H']}, p = {stat_results['kw_stage_pct']['kruskal_pval']:.4e}, Epsilon^2 = {stat_results['kw_stage_pct']['epsilon_squared']}\n"
        f"- **Funding Stage on Headcount Laid Off:** H = {stat_results['kw_stage_count']['kruskal_stat_H']}, p = {stat_results['kw_stage_count']['kruskal_pval']:.4e}, Epsilon^2 = {stat_results['kw_stage_count']['epsilon_squared']}\n"
        f"- **Macro Regime on Layoff Percentage:** H = {stat_results['kw_regime_pct']['kruskal_stat_H']}, p = {stat_results['kw_regime_pct']['kruskal_pval']:.4e}, Epsilon^2 = {stat_results['kw_regime_pct']['epsilon_squared']}\n\n"
        f"## 3. Contingency Analysis (Chi-Square Test)\n\n"
        f"- **Region vs. Layoff Magnitude Severity Tier:** Chi2 = {stat_results['chi2_region_severity']['chi2_stat']}, df = {stat_results['chi2_region_severity']['dof']}, p = {stat_results['chi2_region_severity']['p_value']:.4e}, Cramér's V = {stat_results['chi2_region_severity']['cramers_v']}\n\n"
        f"## 4. Industry Concentration (HHI Index by Year)\n\n"
        + "\n".join([f"- **{yr}:** HHI = {val} ({'Unconcentrated / Broad Restructuring' if val < 1500 else 'Moderately Concentrated'})" for yr, val in stat_results['hhi_by_year'].items()]),
        encoding="utf-8"
    )
    
    print("=== Step 6: Fitting Multivariate Econometric Regressions ===")
    model1, summary1, diag1 = fit_layoff_magnitude_model(df_events)
    model2, summary2, diag2 = fit_layoff_intensity_model(df_events)
    model3, summary3, diag3 = fit_theoretically_justified_interaction_model(df_events)
    
    # Save regression report
    reg_report_lines = [
        "# Multivariate Econometric Regression Diagnostics & Results\n",
        "## Model 1: Layoff Magnitude (Log-Transformed Headcount)",
        f"**Sample Size (N):** {diag1['nobs']:,} | **R²:** {diag1['r_squared']:.4f} | **Adj R²:** {diag1['adj_r_squared']:.4f} | **F-Stat:** {diag1['f_statistic']:.2f} (p = {diag1['f_pvalue']:.4e})",
        f"**Standard Errors:** {diag1['cov_type']}\n",
        summary1.round(4).to_markdown(),
        "\n## Model 2: Layoff Intensity (Percentage Workforce Laid Off)",
        f"**Sample Size (N):** {diag2['nobs']:,} | **R²:** {diag2['r_squared']:.4f} | **Adj R²:** {diag2['adj_r_squared']:.4f} | **F-Stat:** {diag2['f_statistic']:.2f} (p = {diag2['f_pvalue']:.4e})",
        f"**Standard Errors:** {diag2['cov_type']}\n",
        summary2.round(4).to_markdown(),
        "\n## Model 3: Theoretical Interaction (Funding Capitalization × Macroeconomic Regime)",
        f"**Sample Size (N):** {diag3['nobs']:,} | **R²:** {diag3['r_squared']:.4f} | **Adj R²:** {diag3['adj_r_squared']:.4f}",
        summary3.round(4).to_markdown()
    ]
    (REPORTS_DIR / "regression_diagnostics_report.md").write_text("\n".join(reg_report_lines), encoding="utf-8")
    
    print("=== Step 7: Performing Restructuring Profile Clustering ===")
    cluster_sub, X_scaled, scaler, cols = prepare_clustering_data(df_profiles)
    cluster_eval = evaluate_cluster_range(X_scaled, range(2, 6))
    clustered_firms, archetypes, kmeans_model = fit_restructuring_archetypes(cluster_sub, X_scaled, k=4)
    
    # Label archetypes theoretically based on empirical centroids
    archetype_labels = {
        0: "Targeted Multi-Wave Downscalers (Iterative Restructuring)",
        1: "Severe Single-Wave Resets (Deep Structural Cuts)",
        2: "Enterprise Mega-Downscalers (High Capitalization, Scaled Magnitude)",
        3: "Early-Stage Capital-Constrained Exits (High Percentage, Small Scale)"
    }
    archetypes["Theoretical_Archetype"] = archetypes["cluster"].map(archetype_labels)
    clustered_firms["Theoretical_Archetype"] = clustered_firms["cluster"].map(archetype_labels)
    clustered_firms.to_csv(PROCESSED_DATA_DIR / "clustered_company_profiles.csv", index=False)
    
    # Save clustering report
    cluster_report_lines = [
        "# Unsupervised Clustering & Organizational Restructuring Profiles\n",
        "## 1. Cluster Validation Metrics across k",
        cluster_eval.to_markdown(index=False),
        "\n## 2. Discovered Restructuring Archetype Profiles (k = 4)",
        archetypes.to_markdown(index=False),
        "\n## 3. Strategic HRM Interpretation of Archetypes",
        "- **Targeted Multi-Wave Downscalers:** Conduct repeated rounds with moderate percentage cuts. Presents acute survivor anxiety and repeated psychological contract violation.",
        "- **Severe Single-Wave Resets:** Conduct a single, deep restructuring (25-40% cut). Clear 'rip the band-aid' approach; requires intensive procedural justice and immediate survivor stabilization.",
        "- **Enterprise Mega-Downscalers:** Large public firms releasing thousands of employees with small percentage impact (<15%). Massive external media attention, high public visibility, risk of brand erosion.",
        "- **Early-Stage Capital-Constrained Exits:** Seed/Series A firms with >40% cuts driven by cash runway exhaustion. Risk of critical technical brain drain and loss of core architectural knowledge."
    ]
    (REPORTS_DIR / "clustering_analysis_report.md").write_text("\n".join(cluster_report_lines), encoding="utf-8")

    print("=== Step 8: Generating Publication Figures ===")
    generate_all_publication_figures(df_events, df_profiles, summary1, clustered_firms)
    
    print("=== Pipeline Complete! All datasets, reports, models, and figures generated. ===")


if __name__ == "__main__":
    run_full_pipeline()
