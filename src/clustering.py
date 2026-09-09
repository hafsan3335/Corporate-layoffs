"""
Unsupervised clustering and organizational restructuring profile discovery module.
Discovers empirical restructuring profiles across technology firms.
"""
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


def prepare_clustering_data(profiles_df: pd.DataFrame) -> Tuple[pd.DataFrame, np.ndarray, RobustScaler, pd.Index]:
    """
    Select and normalize organizational restructuring features.
    Filters for firms with sufficient metric completeness to avoid synthetic distortion.
    """
    # Features capturing frequency, scale, intensity, capitalization, and temporal spread
    features = [
        "event_count",
        "total_laid_off_log",
        "median_percentage",
        "max_laid_off",
        "funds_raised_log",
        "timespan_days"
    ]
    
    # Work with firms that reported at least one headcount and one percentage metric
    subset = profiles_df.dropna(subset=["total_laid_off_log", "median_percentage"]).copy()
    
    # Funds raised and timespan: if funding missing, impute with median of stage group or global median
    subset["funds_raised_log"] = subset["funds_raised_log"].fillna(subset["funds_raised_log"].median())
    subset["max_laid_off_log"] = np.log1p(subset["max_laid_off"].fillna(0))
    subset["timespan_days"] = subset["timespan_days"].fillna(0)
    
    clustering_cols = [
        "event_count",
        "total_laid_off_log",
        "median_percentage",
        "max_laid_off_log",
        "funds_raised_log",
        "timespan_days"
    ]
    
    X = subset[clustering_cols].values
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)
    
    return subset, X_scaled, scaler, clustering_cols


def evaluate_cluster_range(X_scaled: np.ndarray, k_range=range(2, 7)) -> pd.DataFrame:
    """
    Compute Silhouette Score, Davies-Bouldin Index, and Inertia across k
    to empirically determine the optimal number of restructuring archetypes.
    """
    eval_records = []
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        
        sil = silhouette_score(X_scaled, labels)
        db = davies_bouldin_score(X_scaled, labels)
        ch = calinski_harabasz_score(X_scaled, labels)
        inertia = kmeans.inertia_
        
        eval_records.append({
            "k": k,
            "Silhouette_Score": round(float(sil), 4),
            "Davies_Bouldin_Index": round(float(db), 4),
            "Calinski_Harabasz_Index": round(float(ch), 2),
            "Inertia": round(float(inertia), 2)
        })
        
    return pd.DataFrame(eval_records)


def fit_restructuring_archetypes(
    subset_df: pd.DataFrame,
    X_scaled: np.ndarray,
    k: int = 4
) -> Tuple[pd.DataFrame, pd.DataFrame, KMeans]:
    """
    Fit K-Means clustering and profile each restructuring archetype.
    """
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
    labels = kmeans.fit_predict(X_scaled)
    
    clustered_df = subset_df.copy()
    clustered_df["cluster"] = labels
    
    # Calculate profile medians and means for each cluster
    profile_summary = clustered_df.groupby("cluster").agg(
        firm_count=("company", "count"),
        median_events=("event_count", "median"),
        mean_events=("event_count", "mean"),
        median_total_laid_off=("total_laid_off", "median"),
        mean_total_laid_off=("total_laid_off", "mean"),
        median_intensity=("median_percentage", "median"),
        mean_intensity=("median_percentage", "mean"),
        median_funding_m=("funds_raised", "median"),
        median_timespan_days=("timespan_days", "median"),
        top_stage=("stage_group", lambda s: s.mode().iloc[0] if len(s) > 0 else "Unknown"),
        top_industry=("industry_group", lambda s: s.mode().iloc[0] if len(s) > 0 else "Unknown")
    ).reset_index()
    
    return clustered_df, profile_summary, kmeans
