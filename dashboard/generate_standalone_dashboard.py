"""
Generate a standalone, self-contained HTML dashboard (dashboard/index.html)
using Plotly so that the user can open and interact with the 6 dashboard pages
instantly in any browser without needing a running server.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.config import CLEANED_EVENTS_PATH, COMPANY_PROFILES_PATH, DASHBOARD_DIR


def generate_standalone_html_dashboard():
    events = pd.read_csv(CLEANED_EVENTS_PATH)
    profiles = pd.read_csv(COMPANY_PROFILES_PATH)

    # 1. Timeline
    monthly = events.groupby("year_month").agg(
        events=("company", "count"),
        displaced=("total_laid_off", "sum")
    ).reset_index()
    monthly["roll3"] = monthly["displaced"].rolling(3, min_periods=1).mean()
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=monthly["year_month"], y=monthly["displaced"], name="Monthly Displaced Workers", marker_color="#60a5fa", opacity=0.7))
    fig1.add_trace(go.Scatter(x=monthly["year_month"], y=monthly["roll3"], name="3-Mo Rolling Avg", line=dict(color="#1d4ed8", width=3)))
    fig1.update_layout(title="Monthly Displaced Workers Across Global Technology Sector (2020-2026)", template="plotly_white", height=400)
    html_chart1 = fig1.to_html(full_html=False, include_plotlyjs="cdn")

    # 2. Magnitude vs Intensity Dual
    dual = events.dropna(subset=["total_laid_off", "percentage_laid_off"]).copy()
    dual["pct_display"] = dual["percentage_laid_off"] * 100
    dual["funds_display"] = dual["funds_raised"].fillna(dual["funds_raised"].median())
    fig2 = px.scatter(
        dual,
        x="pct_display",
        y="total_laid_off",
        color="stage_group",
        size="funds_display",
        hover_name="company",
        log_y=True,
        labels={"pct_display": "Layoff Intensity (% Cut)", "total_laid_off": "Headcount Displaced (Log)"},
        title="Layoff Magnitude vs. Layoff Intensity (N = 2,031)",
        template="plotly_white"
    )
    fig2.update_layout(height=450)
    html_chart2 = fig2.to_html(full_html=False, include_plotlyjs=False)

    # 3. Industry Breakdown
    ind_agg = events.groupby("industry_group")["total_laid_off"].sum().sort_values(ascending=True).reset_index()
    fig3 = px.bar(
        ind_agg,
        x="total_laid_off",
        y="industry_group",
        orientation="h",
        title="Total Displaced Workers by Industry Sector",
        color="total_laid_off",
        color_continuous_scale="Blues",
        template="plotly_white"
    )
    fig3.update_layout(height=400)
    html_chart3 = fig3.to_html(full_html=False, include_plotlyjs=False)

    # 4. Repeated Restructuring
    multi_wave = profiles[profiles["event_count"] > 1]
    fig4 = px.histogram(
        multi_wave,
        x="mean_inter_event_days",
        nbins=25,
        title="Temporal Spacing Between Successive Layoff Rounds (Days)",
        color_discrete_sequence=["#8b5cf6"],
        template="plotly_white"
    )
    fig4.update_layout(height=400)
    html_chart4 = fig4.to_html(full_html=False, include_plotlyjs=False)

    # HTML Shell with Bootstrap 5 and tabbed layout
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Strategic HRM & Corporate Layoffs Research Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        .kpi-card {{ border: none; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .nav-tabs .nav-link.active {{ font-weight: bold; border-bottom: 3px solid #2563eb; }}
    </style>
</head>
<body class="p-4">
    <div class="container-fluid max-w-7xl">
        <header class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom">
            <div>
                <h2 class="fw-bold text-primary mb-1">Strategic HRM & Corporate Layoffs: Research Portal</h2>
                <p class="text-muted mb-0">Patterns, Drivers, Workforce Risk and Organizational Restructuring (2020 - 2026)</p>
            </div>
            <span class="badge bg-primary fs-6 p-2">Layoffs.fyi Verified Tracker</span>
        </header>

        <!-- KPI Row -->
        <div class="row g-3 mb-4">
            <div class="col-md-2">
                <div class="card kpi-card bg-white p-3">
                    <span class="text-muted small fw-semibold">TOTAL EVENTS</span>
                    <h3 class="fw-bold text-dark mt-1">{len(events):,}</h3>
                    <small class="text-muted">Recorded actions</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card kpi-card bg-white p-3">
                    <span class="text-muted small fw-semibold">TOTAL DISPLACED</span>
                    <h3 class="fw-bold text-danger mt-1">{events['total_laid_off'].sum():,.0f}</h3>
                    <small class="text-muted">Tech employees affected</small>
                </div>
            </div>
            <div class="col-md-2">
                <div class="card kpi-card bg-white p-3">
                    <span class="text-muted small fw-semibold">MEDIAN LAID OFF</span>
                    <h3 class="fw-bold text-primary mt-1">{events['total_laid_off'].median():.0f}</h3>
                    <small class="text-muted">Per event (Mean: 310.7)</small>
                </div>
            </div>
            <div class="col-md-2">
                <div class="card kpi-card bg-white p-3">
                    <span class="text-muted small fw-semibold">MEDIAN CUT %</span>
                    <h3 class="fw-bold text-warning mt-1">{events['percentage_laid_off'].median()*100:.1f}%</h3>
                    <small class="text-muted">Workforce intensity</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card kpi-card bg-white p-3">
                    <span class="text-muted small fw-semibold">REPEATED RESTRUCTURERS</span>
                    <h3 class="fw-bold text-info mt-1">{(profiles['event_count']>1).sum():,} firms</h3>
                    <small class="text-muted">30.2% conducted 2+ waves</small>
                </div>
            </div>
        </div>

        <!-- Tabbed Navigation -->
        <ul class="nav nav-tabs mb-4" id="researchTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="tab1-btn" data-bs-toggle="tab" data-bs-target="#tab1" type="button">1. Layoff Landscape</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="tab2-btn" data-bs-toggle="tab" data-bs-target="#tab2" type="button">2. Workforce Severity</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="tab3-btn" data-bs-toggle="tab" data-bs-target="#tab3" type="button">3. Industry & Capitalization</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="tab4-btn" data-bs-toggle="tab" data-bs-target="#tab4" type="button">4. Repeated Restructuring</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="tab5-btn" data-bs-toggle="tab" data-bs-target="#tab5" type="button">5. Statistical Results</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link text-danger" id="tab6-btn" data-bs-toggle="tab" data-bs-target="#tab6" type="button">6. Strategic HRM Framework</button>
            </li>
        </ul>

        <div class="tab-content" id="researchTabsContent">
            <!-- TAB 1 -->
            <div class="tab-pane fade show active" id="tab1" role="tabpanel">
                <div class="card border-0 shadow-sm p-3 mb-3">
                    {html_chart1}
                </div>
            </div>

            <!-- TAB 2 -->
            <div class="tab-pane fade" id="tab2" role="tabpanel">
                <div class="card border-0 shadow-sm p-3 mb-3">
                    {html_chart2}
                </div>
            </div>

            <!-- TAB 3 -->
            <div class="tab-pane fade" id="tab3" role="tabpanel">
                <div class="card border-0 shadow-sm p-3 mb-3">
                    {html_chart3}
                </div>
            </div>

            <!-- TAB 4 -->
            <div class="tab-pane fade" id="tab4" role="tabpanel">
                <div class="card border-0 shadow-sm p-3 mb-3">
                    {html_chart4}
                </div>
            </div>

            <!-- TAB 5 -->
            <div class="tab-pane fade" id="tab5" role="tabpanel">
                <div class="card border-0 shadow-sm p-4">
                    <h4 class="fw-bold">Econometric & Non-Parametric Hypothesis Results</h4>
                    <table class="table table-hover mt-3">
                        <thead class="table-dark">
                            <tr><th>Research Relationship</th><th>Statistical Test</th><th>Test Statistic</th><th>p-value</th><th>Effect Size</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Capitalization vs. Layoff Magnitude</td><td>Spearman Rank Correlation</td><td>Rho = +0.4081</td><td>p < 1e-100</td><td>Moderate-Strong Positive</td></tr>
                            <tr><td>Capitalization vs. Layoff Intensity (%)</td><td>Spearman Rank Correlation</td><td>Rho = -0.3901</td><td>p < 1e-90</td><td>Moderate-Strong Negative</td></tr>
                            <tr><td>Funding Stage on Layoff Percentage</td><td>Kruskal-Wallis ANOVA</td><td>H = 633.85</td><td>p < 1e-130</td><td>Epsilon² = 0.2182 (Large)</td></tr>
                            <tr><td>Industry on Layoff Percentage</td><td>Kruskal-Wallis ANOVA</td><td>H = 93.14</td><td>p = 1.27e-15</td><td>Epsilon² = 0.0290 (Moderate)</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- TAB 6 -->
            <div class="tab-pane fade" id="tab6" role="tabpanel">
                <div class="card border-0 shadow-sm p-4">
                    <h4 class="fw-bold text-danger">Strategic HRM Translation & Managerial Restructuring Playbook</h4>
                    <div class="row g-4 mt-2">
                        <div class="col-md-4">
                            <div class="p-3 border rounded bg-light h-100">
                                <h5 class="fw-bold text-primary">Stage 1: Pre-Downsizing</h5>
                                <p class="small text-muted">Conduct critical capability and succession audits. Identify tacit technical knowledge holders. Exhaust non-labor cost cuts before headcount reductions.</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="p-3 border rounded bg-light h-100">
                                <h5 class="fw-bold text-primary">Stage 2: Implementation</h5>
                                <p class="small text-muted">Uphold procedural and interactional justice. Use objective skill-based retention criteria. Provide transparent executive rationale and comprehensive outplacement.</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="p-3 border rounded bg-light h-100">
                                <h5 class="fw-bold text-primary">Stage 3: Post-Downsizing</h5>
                                <p class="small text-muted">Directly mitigate 'survivor syndrome' (burnout, risk aversion, voluntary turnover). Rebalance workloads, re-establish psychological safety, and re-engage remaining talent.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    out_file = DASHBOARD_DIR / "index.html"
    out_file.write_text(html_content, encoding="utf-8")
    print(f"Standalone HTML dashboard written to: {out_file}")


if __name__ == "__main__":
    generate_standalone_html_dashboard()
