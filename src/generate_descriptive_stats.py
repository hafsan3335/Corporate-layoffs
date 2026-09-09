"""
Generate comprehensive descriptive statistics markdown report.
"""
from pathlib import Path
import numpy as np
import pandas as pd

from src.config import CLEANED_EVENTS_PATH, COMPANY_PROFILES_PATH, REPORTS_DIR


def generate_descriptive_statistics_report():
    events = pd.read_csv(CLEANED_EVENTS_PATH)
    profiles = pd.read_csv(COMPANY_PROFILES_PATH)

    def format_pct(val):
        if pd.isna(val):
            return "N/A"
        return f"{val * 100:.1f}%"

    lines = []
    lines.append("# Descriptive Statistics: Corporate Layoffs Research Dataset\n")
    lines.append("## 1. Overall System Metrics")
    lines.append("| Metric | Value |")
    lines.append("| :--- | :--- |")
    lines.append(f"| Total Layoff Events Recorded | **{len(events):,}** |")
    lines.append(f"| Total Displaced Employees Reported | **{events['total_laid_off'].sum():,.0f}** |")
    lines.append(f"| Mean Employees Laid Off per Event | **{events['total_laid_off'].mean():.1f}** |")
    lines.append(f"| Median Employees Laid Off per Event | **{events['total_laid_off'].median():.1f}** |")
    lines.append(f"| Mean Percentage Workforce Laid Off | **{events['percentage_laid_off'].mean() * 100:.1f}%** |")
    lines.append(f"| Median Percentage Workforce Laid Off | **{events['percentage_laid_off'].median() * 100:.1f}%** |")
    lines.append(f"| Unique Affected Companies | **{events['company'].nunique():,}** |")
    lines.append(f"| Unique Countries Represented | **{events['country'].nunique()}** |")
    lines.append(
        f"| Multi-Wave / Repeated Restructuring Firms | **{(profiles['event_count'] > 1).sum():,} ({(profiles['event_count'] > 1).mean() * 100:.1f}%)** |"
    )

    # 2. By Year
    lines.append("\n## 2. Temporal Dynamics by Calendar Year")
    lines.append("| Year | Events | Displaced Workers | Mean Layoffs | Median Layoffs | Mean Intensity | Median Intensity |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for yr, g in events.groupby("year"):
        tot_laid = g["total_laid_off"].sum()
        mean_laid = g["total_laid_off"].mean()
        med_laid = g["total_laid_off"].median()
        mean_pct = g["percentage_laid_off"].mean()
        med_pct = g["percentage_laid_off"].median()
        lines.append(
            f"| **{yr}** | {len(g):,} | {tot_laid:,.0f} | {mean_laid:.1f} | {med_laid:.1f} | {format_pct(mean_pct)} | {format_pct(med_pct)} |"
        )

    # 3. By Macro Regime
    lines.append("\n## 3. Layoff Patterns Across Macroeconomic Regimes")
    lines.append("| Macroeconomic Regime | Events | Displaced Workers | Median Layoffs | Median Intensity |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for reg, g in events.groupby("macro_regime"):
        lines.append(
            f"| **{reg}** | {len(g):,} | {g['total_laid_off'].sum():,.0f} | {g['total_laid_off'].median():.1f} | {format_pct(g['percentage_laid_off'].median())} |"
        )

    # 4. By Industry Group
    lines.append("\n## 4. Restructuring by Industry Group")
    lines.append("| Industry Group | Events | Displaced Workers | Mean Layoffs | Median Layoffs | Median Intensity |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    by_ind = events.groupby("industry_group").agg(
        events=("company", "count"),
        displaced=("total_laid_off", "sum"),
        mean_laid=("total_laid_off", "mean"),
        med_laid=("total_laid_off", "median"),
        med_pct=("percentage_laid_off", "median")
    ).sort_values(by="displaced", ascending=False)
    for ind, r in by_ind.iterrows():
        lines.append(
            f"| **{ind}** | {r['events']:,} | {r['displaced']:,.0f} | {r['mean_laid']:.1f} | {r['med_laid']:.1f} | {format_pct(r['med_pct'])} |"
        )

    # 5. By Geography
    lines.append("\n## 5. Regional Distribution of Restructuring")
    lines.append("| Global Region | Events | Displaced Workers | Median Layoffs | Median Intensity |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    by_reg = events.groupby("region").agg(
        events=("company", "count"),
        displaced=("total_laid_off", "sum"),
        med_laid=("total_laid_off", "median"),
        med_pct=("percentage_laid_off", "median")
    ).sort_values(by="displaced", ascending=False)
    for reg, r in by_reg.iterrows():
        lines.append(
            f"| **{reg}** | {r['events']:,} | {r['displaced']:,.0f} | {r['med_laid']:.1f} | {format_pct(r['med_pct'])} |"
        )

    # 6. By Funding Stage Group
    lines.append("\n## 6. Organizational Maturity & Funding Stage")
    lines.append("| Funding Stage Cohort | Events | Displaced Workers | Median Layoffs | Median Intensity |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    by_stg = events.groupby("stage_group").agg(
        events=("company", "count"),
        displaced=("total_laid_off", "sum"),
        med_laid=("total_laid_off", "median"),
        med_pct=("percentage_laid_off", "median")
    ).sort_values(by="displaced", ascending=False)
    for stg, r in by_stg.iterrows():
        lines.append(
            f"| **{stg}** | {r['events']:,} | {r['displaced']:,.0f} | {r['med_laid']:.1f} | {format_pct(r['med_pct'])} |"
        )

    # 7. Top 10 Largest Events
    lines.append("\n## 7. Top 10 Largest Single Layoff Events")
    lines.append("| Company | Date | Headcount Laid Off | Percentage | Stage | Country | Industry |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    top_events = events.sort_values(by="total_laid_off", ascending=False).head(10)
    for _, r in top_events.iterrows():
        lines.append(
            f"| **{r['company']}** | {r['date']} | {r['total_laid_off']:,.0f} | {format_pct(r['percentage_laid_off'])} | {r['stage']} | {r['country']} | {r['industry']} |"
        )

    # 8. Top 10 Cumulative Layoffs by Company
    lines.append("\n## 8. Top 10 Companies by Cumulative Displaced Workers")
    lines.append("| Company | Total Displaced | Layoff Events | Mean Days Between Waves | Industry | Stage |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    top_firms = profiles.sort_values(by="total_laid_off", ascending=False).head(10)
    for _, r in top_firms.iterrows():
        days_str = f"{r['mean_inter_event_days']:.0f} days" if pd.notna(r["mean_inter_event_days"]) else "N/A (Single event)"
        lines.append(
            f"| **{r['company']}** | {r['total_laid_off']:,.0f} | {r['event_count']} | {days_str} | {r['industry']} | {r['stage']} |"
        )

    out_file = REPORTS_DIR / "descriptive_statistics.md"
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out_file}")


if __name__ == "__main__":
    generate_descriptive_statistics_report()
