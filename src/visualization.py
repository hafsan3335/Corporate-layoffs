"""
Visualization module for publication-grade Matplotlib static figures
and Plotly interactive dashboard components.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import plotly.graph_objects as go

from src.config import FIGURES_DIR, COLORS


# Apply consistent Matplotlib publication theme
def set_publication_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "axes.edgecolor": "#334155",
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "grid.color": "#e2e8f0",
        "grid.linestyle": "--",
        "grid.alpha": 0.7,
        "xtick.color": "#334155",
        "ytick.color": "#334155",
        "figure.titlesize": 13,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.dpi": 300
    })


def generate_all_publication_figures(events_df: pd.DataFrame, profiles_df: pd.DataFrame, reg_summary: pd.DataFrame, clusters_df: pd.DataFrame = None):
    """Generate all 8 publication-quality Matplotlib static research figures."""
    set_publication_style()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------
    # Figure 1: Temporal Restructuring Waves & Monthly Volume
    # -------------------------------------------------------------
    monthly = events_df.groupby("year_month").agg(
        events=("company", "count"),
        displaced=("total_laid_off", "sum")
    ).reset_index()
    monthly["displaced_roll3"] = monthly["displaced"].rolling(3, min_periods=1).mean()
    
    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    ax2 = ax1.twinx()
    
    x = np.arange(len(monthly))
    ax1.bar(x, monthly["displaced"] / 1e3, color="#93c5fd", alpha=0.6, width=0.7, label="Monthly Displaced Workers (Thousands)")
    ax1.plot(x, monthly["displaced_roll3"] / 1e3, color="#1d4ed8", linewidth=2.2, label="3-Month Rolling Average")
    ax2.plot(x, monthly["events"], color="#dc2626", linewidth=1.8, linestyle="-", label="Layoff Announcement Events")
    
    # Format axes
    ax1.set_xlabel("Time Horizon (Year-Month: 2020 - 2026)", labelpad=10)
    ax1.set_ylabel("Displaced Tech Workers (Thousands)", color="#1d4ed8")
    ax2.set_ylabel("Number of Layoff Events", color="#dc2626")
    ax1.set_xticks(x[::4])
    ax1.set_xticklabels(monthly["year_month"].iloc[::4], rotation=45, ha="right")
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True, facecolor="white", framealpha=0.9)
    ax1.set_title("Figure 1: Macroeconomic Waves of Technology Layoffs (2020–2026)", weight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig1_temporal_layoff_waves.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Figure 2: Magnitude vs. Intensity Dual-Metric Scatter
    # -------------------------------------------------------------
    dual = events_df.dropna(subset=["total_laid_off", "percentage_laid_off"]).copy()
    fig, ax = plt.subplots(figsize=(9, 6))
    
    scatter = ax.scatter(
        dual["percentage_laid_off"] * 100,
        dual["total_laid_off"],
        c=dual["funding_log"].fillna(0),
        cmap="viridis",
        alpha=0.6,
        s=30,
        edgecolors="none"
    )
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Log(1 + Total Funding Raised in $M)", rotation=270, labelpad=15)
    
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{int(y):,}"))
    ax.set_xlabel("Layoff Intensity: Percentage of Workforce Cut (%)", labelpad=8)
    ax.set_ylabel("Layoff Magnitude: Total Displaced Employees (Log Scale)", labelpad=8)
    ax.set_title("Figure 2: Layoff Magnitude vs. Layoff Intensity (N = 2,031)", weight="bold", pad=12)
    
    # Annotate quadrants
    ax.axvline(x=20, color="#64748b", linestyle=":", alpha=0.7)
    ax.axhline(y=500, color="#64748b", linestyle=":", alpha=0.7)
    ax.text(5, 5000, "High Headcount / Low % (Enterprise Scale)", fontsize=8, color="#334155", bbox=dict(boxstyle='round,pad=0.2', facecolor='#f1f5f9', alpha=0.8))
    ax.text(60, 20, "Low Headcount / High % (Startup Vulnerability)", fontsize=8, color="#334155", bbox=dict(boxstyle='round,pad=0.2', facecolor='#f1f5f9', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig2_magnitude_vs_intensity.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Figure 3: Industry Restructuring Volume & HHI Concentration
    # -------------------------------------------------------------
    ind_agg = events_df.groupby("industry_group")["total_laid_off"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    y_pos = np.arange(len(ind_agg))
    bars = ax.barh(y_pos, ind_agg.values / 1e3, color="#3b82f6", alpha=0.85, edgecolor="#1d4ed8")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(ind_agg.index)
    ax.set_xlabel("Total Reported Displaced Workers (Thousands)", labelpad=8)
    ax.set_title("Figure 3: Cumulative Workforce Reductions Across Industry Sectors", weight="bold", pad=12)
    
    # Add data labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2, f"{width:.1f}k", va="center", fontsize=8, color="#1e293b")
    
    ax.set_xlim(0, max(ind_agg.values / 1e3) * 1.15)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig3_industry_hhi_concentration.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Figure 4: Funding Stage vs. Layoff Severity (Magnitude & Intensity)
    # -------------------------------------------------------------
    stage_order = [
        "Early Stage (Seed)", "Early Venture (Series A)", "Expansion Stage (Series B)",
        "Late Stage (Series C-D)", "Growth Stage (Series E+)", "Public (Post-IPO)", "Acquired / Subsidiary"
    ]
    stage_sub = events_df[events_df["stage_group"].isin(stage_order)].copy()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    
    # Left: Headcount by stage (log)
    headcount_data = [stage_sub[stage_sub["stage_group"] == s]["total_laid_off"].dropna() for s in stage_order]
    bp1 = ax1.boxplot(headcount_data, tick_labels=[s.replace(" ", "\n") for s in stage_order], patch_artist=True, showfliers=False)
    for patch in bp1['boxes']:
        patch.set_facecolor('#93c5fd')
    ax1.set_ylabel("Headcount Laid Off per Event (Employees)")
    ax1.set_title("Panel A: Layoff Magnitude across Maturity Stages", weight="bold", fontsize=10)
    ax1.tick_params(axis="x", rotation=45)
    
    # Right: Percentage by stage
    pct_data = [stage_sub[stage_sub["stage_group"] == s]["percentage_laid_off"].dropna() * 100 for s in stage_order]
    bp2 = ax2.boxplot(pct_data, tick_labels=[s.replace(" ", "\n") for s in stage_order], patch_artist=True, showfliers=False)
    for patch in bp2['boxes']:
        patch.set_facecolor('#fca5a5')
    ax2.set_ylabel("Workforce Percentage Eliminated (%)")
    ax2.set_title("Panel B: Layoff Intensity across Maturity Stages", weight="bold", fontsize=10)
    ax2.tick_params(axis="x", rotation=45)
    
    fig.suptitle("Figure 4: Organizational Maturity & Workforce Restructuring Asymmetry", weight="bold", fontsize=12, y=1.02)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig4_funding_stage_severity.png", dpi=300, bbox_inches="tight")
    plt.close()

    # -------------------------------------------------------------
    # Figure 5: Recurrence & Temporal Spacing Between Layoff Waves
    # -------------------------------------------------------------
    multi_wave = profiles_df[profiles_df["event_count"] > 1].copy()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Recurrence counts
    rec_counts = profiles_df["event_count"].value_counts().sort_index()
    rec_cats = ["1 Event\n(Single)", "2 Events\n(Two Waves)", "3 Events\n(Three Waves)", "4+ Events\n(Chronic)"]
    vals = [
        rec_counts.get(1, 0),
        rec_counts.get(2, 0),
        rec_counts.get(3, 0),
        sum(v for k, v in rec_counts.items() if k >= 4)
    ]
    ax1.bar(rec_cats, vals, color=["#60a5fa", "#f59e0b", "#f97316", "#ef4444"], edgecolor="#334155")
    ax1.set_ylabel("Number of Companies")
    ax1.set_title("Panel A: Distribution of Restructuring Recurrence", weight="bold", fontsize=10)
    for i, v in enumerate(vals):
        ax1.text(i, v + 20, f"{v:,}\n({v/sum(vals)*100:.1f}%)", ha="center", fontsize=8)
    
    # Inter-event days
    ax2.hist(multi_wave["mean_inter_event_days"].dropna(), bins=25, color="#8b5cf6", alpha=0.75, edgecolor="#4c1d95")
    ax2.axvline(multi_wave["mean_inter_event_days"].median(), color="#dc2626", linestyle="--", label=f"Median: {multi_wave['mean_inter_event_days'].median():.0f} Days")
    ax2.set_xlabel("Mean Days Between Successive Layoff Rounds")
    ax2.set_ylabel("Company Count")
    ax2.set_title("Panel B: Temporal Latency Between Downsizing Waves", weight="bold", fontsize=10)
    ax2.legend()
    
    fig.suptitle("Figure 5: Restructuring Recurrence & Multi-Wave Timing", weight="bold", fontsize=12, y=1.02)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig5_recurrence_and_inter_event_days.png", dpi=300, bbox_inches="tight")
    plt.close()

    # -------------------------------------------------------------
    # Figure 6: Multivariate Regression Coefficient Forest Plot
    # -------------------------------------------------------------
    if reg_summary is not None and len(reg_summary) > 0:
        fig, ax = plt.subplots(figsize=(10, 7))
        # Exclude constant / intercept for clean display
        plot_df = reg_summary.loc[~reg_summary.index.str.contains("Intercept")].copy()
        y_pos = np.arange(len(plot_df))
        
        # Clean up index labels
        clean_labels = [
            lbl.replace("C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.", "Stage: ")
               .replace("C(industry_group, Treatment(reference='Consumer & Retail'))[T.", "Ind: ")
               .replace("C(year, Treatment(reference='2022'))[T.", "Year: ")
               .replace("C(region, Treatment(reference='North America'))[T.", "Region: ")
               .replace("]", "")
               .replace("funding_log", "Log(1 + Funding Raised)")
            for lbl in plot_df.index
        ]
        
        ax.errorbar(
            plot_df["Coefficient"],
            y_pos,
            xerr=[plot_df["Coefficient"] - plot_df["CI_Lower_95"], plot_df["CI_Upper_95"] - plot_df["Coefficient"]],
            fmt="o",
            color="#1d4ed8",
            ecolor="#93c5fd",
            elinewidth=2,
            capsize=3
        )
        ax.axvline(0, color="#dc2626", linestyle="--", alpha=0.7)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(clean_labels, fontsize=8)
        ax.set_xlabel("Regression Coefficient (HC3 Robust 95% CI)", labelpad=8)
        ax.set_title("Figure 6: Predictors of Layoff Magnitude (Log Headcount Model)", weight="bold", pad=12)
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "fig6_regression_forest_plot.png", dpi=300)
        plt.close()

    # -------------------------------------------------------------
    # Figure 8: Workforce Restructuring Risk Indicator (WRRI) Distribution
    # -------------------------------------------------------------
    if "wrri_score" in events_df.columns:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1.hist(events_df["wrri_score"].dropna(), bins=30, color="#0ea5e9", alpha=0.8, edgecolor="#0369a1")
        ax1.set_xlabel("WRRI Composite Score (0 - 100)")
        ax1.set_ylabel("Layoff Event Count")
        ax1.set_title("Panel A: Distribution of Restructuring Risk Scores", weight="bold", fontsize=10)
        
        cat_counts = events_df["wrri_category"].value_counts()
        ax2.pie(
            cat_counts.values,
            labels=cat_counts.index,
            autopct="%1.1f%%",
            colors=["#22c55e", "#f59e0b", "#f97316", "#ef4444"][:len(cat_counts)],
            startangle=140
        )
        ax2.set_title("Panel B: Restructuring Exposure Tiers", weight="bold", fontsize=10)
        
        fig.suptitle("Figure 8: Workforce Restructuring Risk Indicator (WRRI) Profile", weight="bold", fontsize=12, y=1.02)
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "fig8_workforce_risk_matrix.png", dpi=300, bbox_inches="tight")
        plt.close()

    print(f"All publication figures saved successfully to {FIGURES_DIR}")
