"""
Automated unit tests for data cleaning, features, statistics, regression, and clustering.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.config import RAW_DATA_PATH, CLEANED_EVENTS_PATH, COMPANY_PROFILES_PATH
from src.cleaning import load_raw_data, audit_raw_data, clean_dataset
from src.features import engineer_event_features, create_company_profiles, assign_macro_regime
from src.risk_index import compute_event_risk_index
from src.statistics import calculate_hhi, run_spearman_correlations, run_kruskal_wallis_group
from src.regression import fit_layoff_magnitude_model, fit_layoff_intensity_model
from src.clustering import prepare_clustering_data, evaluate_cluster_range, fit_restructuring_archetypes


def test_raw_data_loading():
    df = load_raw_data(RAW_DATA_PATH)
    assert not df.empty
    assert "company" in df.columns
    assert "total_laid_off" in df.columns
    assert "percentage_laid_off" in df.columns
    assert len(df) >= 4000


def test_cleaning_and_bounds():
    df_raw = load_raw_data(RAW_DATA_PATH)
    df_clean, meta = clean_dataset(df_raw)
    
    assert len(df_clean) <= len(df_raw)
    assert meta["removed_exact_event_duplicates"] >= 0
    # Check percentage bounds
    valid_pct = df_clean["percentage_laid_off"].dropna()
    assert (valid_pct >= 0.0).all()
    assert (valid_pct <= 1.0).all()
    # Check total laid off bounds
    valid_laid = df_clean["total_laid_off"].dropna()
    assert (valid_laid > 0).all()


def test_feature_engineering():
    df_raw = load_raw_data(RAW_DATA_PATH)
    df_clean, _ = clean_dataset(df_raw)
    df_events = engineer_event_features(df_clean)
    
    assert "laid_off_log" in df_events.columns
    assert "funding_log" in df_events.columns
    assert "macro_regime" in df_events.columns
    assert "region" in df_events.columns
    assert "is_repeated_restructurer" in df_events.columns
    
    # Check company aggregation
    profiles = create_company_profiles(df_events)
    assert not profiles.empty
    assert "event_count" in profiles.columns
    assert "total_laid_off" in profiles.columns


def test_risk_index_bounds():
    df_raw = load_raw_data(RAW_DATA_PATH)
    df_clean, _ = clean_dataset(df_raw)
    df_events = engineer_event_features(df_clean)
    df_scored = compute_event_risk_index(df_events)
    
    assert "wrri_score" in df_scored.columns
    assert (df_scored["wrri_score"] >= 0).all()
    assert (df_scored["wrri_score"] <= 100).all()
    assert "wrri_category" in df_scored.columns


def test_inferential_statistics():
    events = pd.read_csv(CLEANED_EVENTS_PATH)
    # Spearman
    spearman_df = run_spearman_correlations(events)
    assert len(spearman_df) == 3
    # HHI
    hhi = calculate_hhi(events["industry_group"])
    assert 0 < hhi <= 10000
    # Kruskal Wallis
    kw = run_kruskal_wallis_group(events, "stage_group", "percentage_laid_off")
    assert "kruskal_stat_H" in kw
    assert kw["kruskal_pval"] < 0.05


def test_regression_models():
    events = pd.read_csv(CLEANED_EVENTS_PATH)
    m1, s1, d1 = fit_layoff_magnitude_model(events)
    assert d1["r_squared"] > 0.15
    assert d1["nobs"] > 1000
    
    m2, s2, d2 = fit_layoff_intensity_model(events)
    assert d2["r_squared"] > 0.15
    assert d2["nobs"] > 1000


def test_clustering_archetypes():
    profiles = pd.read_csv(COMPANY_PROFILES_PATH)
    sub, X_scaled, scaler, cols = prepare_clustering_data(profiles)
    eval_df = evaluate_cluster_range(X_scaled, range(2, 5))
    assert len(eval_df) == 3
    
    clustered, summary, kmeans = fit_restructuring_archetypes(sub, X_scaled, k=4)
    assert len(summary) == 4
    assert "cluster" in clustered.columns
