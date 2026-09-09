"""
Interactive Plotly / Dash Web Application for Strategic HRM and Corporate Layoffs Research.
Contains 6 Dedicated Analytical Pages:
1. Layoff Landscape
2. Workforce Severity (Magnitude vs. Intensity)
3. Strategic Firm Characteristics
4. Repeated Restructuring
5. Statistical & Regression Findings
6. Strategic HRM Interpretation & Decision Matrix
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
from src.config import CLEANED_EVENTS_PATH, COMPANY_PROFILES_PATH, REPORTS_DIR

# Load Cleaned Datasets
events_df = pd.read_csv(CLEANED_EVENTS_PATH)
profiles_df = pd.read_csv(COMPANY_PROFILES_PATH)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    title="Strategic HRM & Corporate Layoffs Research Portal"
)

# Shared UI Navigation Bar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("Strategic HRM & Corporate Layoffs", className="ms-2 fw-bold text-primary fs-4"),
        dbc.Nav([
            dbc.NavLink("1. Landscape", href="/", active="exact", className="fw-semibold"),
            dbc.NavLink("2. Severity", href="/severity", active="exact", className="fw-semibold"),
            dbc.NavLink("3. Firm Characteristics", href="/characteristics", active="exact", className="fw-semibold"),
            dbc.NavLink("4. Repeated Restructuring", href="/recurrence", active="exact", className="fw-semibold"),
            dbc.NavLink("5. Statistical Evidence", href="/statistics", active="exact", className="fw-semibold"),
            dbc.NavLink("6. Strategic HRM", href="/strategic-hrm", active="exact", className="fw-semibold text-danger"),
        ], className="ms-auto", navbar=True)
    ], fluid=True),
    color="light",
    className="mb-4 shadow-sm border-bottom"
)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    dbc.Container(id="page-content", fluid=True, className="px-4 pb-5")
])


# -------------------------------------------------------------
# PAGE 1: LAYOFF LANDSCAPE
# -------------------------------------------------------------
def build_page_1():
    total_events = len(events_df)
    total_displaced = events_df["total_laid_off"].sum()
    median_displaced = events_df["total_laid_off"].median()
    median_intensity = events_df["percentage_laid_off"].median() * 100
    total_companies = events_df["company"].nunique()
    
    # Monthly trend chart
    monthly = events_df.groupby("year_month").agg(
        events=("company", "count"),
        displaced=("total_laid_off", "sum")
    ).reset_index()
    monthly["roll3"] = monthly["displaced"].rolling(3, min_periods=1).mean()
    
    fig_time = go.Figure()
    fig_time.add_trace(go.Bar(
        x=monthly["year_month"],
        y=monthly["displaced"],
        name="Displaced Workers",
        marker_color="#93c5fd",
        opacity=0.7
    ))
    fig_time.add_trace(go.Scatter(
        x=monthly["year_month"],
        y=monthly["roll3"],
        name="3-Mo Rolling Avg",
        line=dict(color="#1d4ed8", width=3)
    ))
    fig_time.add_trace(go.Scatter(
        x=monthly["year_month"],
        y=monthly["events"] * 100,
        name="Event Count (Scaled x100)",
        line=dict(color="#dc2626", width=2, dash="dot"),
        yaxis="y2"
    ))
    fig_time.update_layout(
        title="Monthly Technology Layoffs & Restructuring Waves (2020 - 2026)",
        xaxis_title="Year-Month",
        yaxis_title="Total Displaced Employees",
        yaxis2=dict(title="Layoff Events (Scaled)", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.1, x=0.2),
        template="plotly_white",
        height=420
    )
    
    # Regional Breakdown
    region_agg = events_df.groupby("region")["total_laid_off"].sum().reset_index()
    fig_region = px.pie(
        region_agg,
        values="total_laid_off",
        names="region",
        title="Global Geographic Distribution of Displaced Workers",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    fig_region.update_layout(template="plotly_white", height=420)
    
    return html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("TOTAL EVENTS", className="text-muted text-uppercase mb-1"),
                html.H3(f"{total_events:,}", className="fw-bold text-primary"),
                html.Small("Verified tech restructuring events", className="text-muted")
            ]), className="shadow-sm border-0 bg-light"), width=12, md=2),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("TOTAL DISPLACED", className="text-muted text-uppercase mb-1"),
                html.H3(f"{total_displaced:,.0f}", className="fw-bold text-danger"),
                html.Small("Cumulative workforce reduction", className="text-muted")
            ]), className="shadow-sm border-0 bg-light"), width=12, md=3),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("MEDIAN PER EVENT", className="text-muted text-uppercase mb-1"),
                html.H3(f"{median_displaced:.0f} workers", className="fw-bold text-dark"),
                html.Small("Mean is 310.7 (severe right skew)", className="text-muted")
            ]), className="shadow-sm border-0 bg-light"), width=12, md=2),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("MEDIAN CUT %", className="text-muted text-uppercase mb-1"),
                html.H3(f"{median_intensity:.1f}%", className="fw-bold text-warning"),
                html.Small("Proportional workforce cut", className="text-muted")
            ]), className="shadow-sm border-0 bg-light"), width=12, md=2),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H6("AFFECTED FIRMS", className="text-muted text-uppercase mb-1"),
                html.H3(f"{total_companies:,}", className="fw-bold text-info"),
                html.Small("30.2% conducted multi-wave cuts", className="text-muted")
            ]), className="shadow-sm border-0 bg-light"), width=12, md=3),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_time)), className="shadow-sm border-0"), width=12, lg=8),
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_region)), className="shadow-sm border-0"), width=12, lg=4),
        ])
    ])


# -------------------------------------------------------------
# PAGE 2: WORKFORCE SEVERITY (Magnitude vs. Intensity)
# -------------------------------------------------------------
def build_page_2():
    dual = events_df.dropna(subset=["total_laid_off", "percentage_laid_off"]).copy()
    dual["percentage_display"] = dual["percentage_laid_off"] * 100
    dual["funds_display"] = dual["funds_raised"].fillna(dual["funds_raised"].median())
    
    fig_scatter = px.scatter(
        dual,
        x="percentage_display",
        y="total_laid_off",
        color="stage_group",
        size="funds_display",
        hover_name="company",
        hover_data=["date", "industry", "country"],
        log_y=True,
        labels={"percentage_display": "Layoff Intensity (% Workforce Eliminated)", "total_laid_off": "Layoff Magnitude (Headcount - Log Scale)"},
        title="Figure 2 (Interactive): Layoff Magnitude vs. Layoff Intensity (N = 2,031)",
        template="plotly_white"
    )
    fig_scatter.update_layout(height=520)
    
    top_events = events_df.sort_values(by="total_laid_off", ascending=False).head(10)[[
        "company", "date", "total_laid_off", "percentage_laid_off", "stage", "industry", "country"
    ]].copy()
    top_events["percentage_laid_off"] = (top_events["percentage_laid_off"] * 100).round(1).astype(str) + "%"
    top_events["total_laid_off"] = top_events["total_laid_off"].map("{:,.0f}".format)
    
    table_top = dash_table.DataTable(
        columns=[{"name": c, "id": c} for c in top_events.columns],
        data=top_events.to_dict("records"),
        style_header={"backgroundColor": "#1e293b", "color": "white", "fontWeight": "bold"},
        style_cell={"padding": "8px", "fontSize": "13px"},
        style_as_list_view=True
    )
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4("Layoff Severity: Magnitude vs. Intensity Divergence", className="fw-bold"),
                html.P("In Strategic HRM, evaluating restructuring solely by raw headcounts ignores organizational vulnerability. A 50-person cut represents an existential shock to a 75-person startup, while a 1,000-person cut may represent marginal trimming (<5%) for an enterprise.", className="text-muted")
            ])
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_scatter)), className="shadow-sm border-0 mb-4"), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5("Top 10 Largest Recorded Restructuring Events", className="fw-bold mb-3"),
                dbc.Card(dbc.CardBody(table_top), className="shadow-sm border-0")
            ], width=12)
        ])
    ])


# -------------------------------------------------------------
# PAGE 3: STRATEGIC FIRM CHARACTERISTICS
# -------------------------------------------------------------
def build_page_3():
    stage_agg = events_df.groupby("stage_group").agg(
        median_laid_off=("total_laid_off", "median"),
        median_pct=("percentage_laid_off", lambda x: x.median() * 100),
        event_count=("company", "count")
    ).reset_index()
    
    fig_stage = go.Figure()
    fig_stage.add_trace(go.Bar(
        x=stage_agg["stage_group"],
        y=stage_agg["median_laid_off"],
        name="Median Headcount Laid Off",
        marker_color="#2563eb"
    ))
    fig_stage.add_trace(go.Bar(
        x=stage_agg["stage_group"],
        y=stage_agg["median_pct"],
        name="Median Workforce Cut %",
        marker_color="#f87171"
    ))
    fig_stage.update_layout(
        title="Asymmetry Across Organizational Maturity Stages",
        barmode="group",
        template="plotly_white",
        height=400,
        xaxis_tickangle=-30
    )
    
    ind_agg = events_df.groupby("industry_group")["total_laid_off"].sum().sort_values(ascending=True).reset_index()
    fig_ind = px.bar(
        ind_agg,
        x="total_laid_off",
        y="industry_group",
        orientation="h",
        title="Total Displaced Workers by Industry Cohort",
        labels={"total_laid_off": "Displaced Workers", "industry_group": "Industry"},
        color="total_laid_off",
        color_continuous_scale="Blues",
        template="plotly_white"
    )
    fig_ind.update_layout(height=400)
    
    return html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_stage)), className="shadow-sm border-0"), width=12, lg=6),
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_ind)), className="shadow-sm border-0"), width=12, lg=6)
        ])
    ])


# -------------------------------------------------------------
# PAGE 4: REPEATED RESTRUCTURING & RECURRENCE
# -------------------------------------------------------------
def build_page_4():
    multi_wave = profiles_df[profiles_df["event_count"] > 1].copy()
    rec_dist = profiles_df["event_count"].value_counts().reset_index()
    rec_dist.columns = ["Rounds", "Companies"]
    
    fig_rec = px.bar(
        rec_dist.head(6),
        x="Rounds",
        y="Companies",
        title="Restructuring Recurrence: Single vs. Multi-Wave Restructurers",
        color="Companies",
        color_continuous_scale="Reds",
        template="plotly_white"
    )
    fig_rec.update_layout(height=380)
    
    fig_hist = px.histogram(
        multi_wave,
        x="mean_inter_event_days",
        nbins=30,
        title="Temporal Latency Between Successive Downsizing Waves (Days)",
        labels={"mean_inter_event_days": "Mean Days Between Events"},
        color_discrete_sequence=["#8b5cf6"],
        template="plotly_white"
    )
    fig_hist.update_layout(height=380)
    
    chronic = profiles_df.sort_values(by="event_count", ascending=False).head(10)[[
        "company", "event_count", "total_laid_off", "mean_inter_event_days", "industry", "stage"
    ]].copy()
    chronic["total_laid_off"] = chronic["total_laid_off"].map("{:,.0f}".format)
    chronic["mean_inter_event_days"] = chronic["mean_inter_event_days"].map("{:.0f} days".format)
    
    table_chronic = dash_table.DataTable(
        columns=[{"name": c, "id": c} for c in chronic.columns],
        data=chronic.to_dict("records"),
        style_header={"backgroundColor": "#334155", "color": "white", "fontWeight": "bold"},
        style_cell={"padding": "8px", "fontSize": "13px"},
        style_as_list_view=True
    )
    
    return html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_rec)), className="shadow-sm border-0"), width=12, lg=6),
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_hist)), className="shadow-sm border-0"), width=12, lg=6)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.H5("Top 10 Organizations with Highest Restructuring Recurrence", className="fw-bold mb-3"),
                dbc.Card(dbc.CardBody(table_chronic), className="shadow-sm border-0")
            ], width=12)
        ])
    ])


# -------------------------------------------------------------
# PAGE 5: STATISTICAL EVIDENCE & REGRESSION COEFFICIENTS
# -------------------------------------------------------------
def build_page_5():
    # Load statistical tables
    spearman_data = [
        {"Comparison": "Capital Raised vs. Layoff Magnitude", "Spearman Rho": "+0.4081", "p-value": "< 1e-100", "Significance": "*** (Strong Positive)"},
        {"Comparison": "Capital Raised vs. Layoff Intensity (%)", "Spearman Rho": "-0.3901", "p-value": "< 1e-90", "Significance": "*** (Strong Negative)"},
        {"Comparison": "Layoff Magnitude vs. Layoff Intensity", "Spearman Rho": "-0.0422", "p-value": "0.0573", "Significance": "ns (Orthogonal / Uncorrelated)"}
    ]
    
    kw_data = [
        {"Predictor": "Funding Stage Cohort", "Dependent Metric": "Workforce Cut %", "Kruskal H": "633.85", "p-value": "< 1e-130", "Epsilon²": "0.2182 (Large Effect)"},
        {"Predictor": "Funding Stage Cohort", "Dependent Metric": "Headcount Displaced", "Kruskal H": "626.89", "p-value": "< 1e-130", "Epsilon²": "0.2072 (Large Effect)"},
        {"Predictor": "Industry Group", "Dependent Metric": "Workforce Cut %", "Kruskal H": "93.14", "p-value": "1.27e-15", "Epsilon²": "0.0290 (Moderate Effect)"},
        {"Predictor": "Macroeconomic Regime", "Dependent Metric": "Workforce Cut %", "Kruskal H": "33.09", "p-value": "3.08e-07", "Epsilon²": "0.0105 (Small Effect)"}
    ]
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4("Inferential Evidence & Econometric Modeling", className="fw-bold"),
                html.P("Hypothesis tests demonstrate that corporate restructuring follows systematic organizational parameters rather than random cost-cutting shocks.", className="text-muted")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H5("1. Spearman Rank Correlations (Robust to Heavy Right-Skew)", className="fw-bold mb-2"),
                dbc.Card(dbc.CardBody(
                    dash_table.DataTable(
                        columns=[{"name": k, "id": k} for k in spearman_data[0].keys()],
                        data=spearman_data,
                        style_header={"backgroundColor": "#0f172a", "color": "white", "fontWeight": "bold"},
                        style_cell={"padding": "8px", "fontSize": "13px"},
                        style_as_list_view=True
                    )
                ), className="shadow-sm border-0 mb-4")
            ], width=12, lg=6),
            dbc.Col([
                html.H5("2. Kruskal-Wallis Non-Parametric ANOVAs & Effect Sizes", className="fw-bold mb-2"),
                dbc.Card(dbc.CardBody(
                    dash_table.DataTable(
                        columns=[{"name": k, "id": k} for k in kw_data[0].keys()],
                        data=kw_data,
                        style_header={"backgroundColor": "#0f172a", "color": "white", "fontWeight": "bold"},
                        style_cell={"padding": "8px", "fontSize": "13px"},
                        style_as_list_view=True
                    )
                ), className="shadow-sm border-0 mb-4")
            ], width=12, lg=6)
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("3. Econometric Summary: The Capitalization & Maturity Paradox", className="fw-bold"),
                html.P("In OLS models with MacKinnon-White HC3 robust standard errors:"),
                html.Ul([
                    html.Li("Capital Elasticity (Magnitude): Log funding exhibits a positive elasticity of +0.1415 (p < 0.001) with absolute headcounts."),
                    html.Li("Maturity Elasticity (Intensity): Post-IPO public firms downsize an estimated 51.0 percentage points less of their workforce than Seed startups (p < 0.001, t = -14.68)."),
                    html.Li("Interaction Stability: Venture capitalization buffered firms against workforce cuts during easy-money periods (2020-2021) but acted as an amplifier of headcount reductions following 2022-2023 interest rate hikes.")
                ])
            ]), className="shadow-sm border-0 bg-light"), width=12)
        ])
    ])


# -------------------------------------------------------------
# PAGE 6: STRATEGIC HRM INTERPRETATION & DECISION MATRIX
# -------------------------------------------------------------
def build_page_6():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4("Strategic HRM Translation & Organizational Intervention Matrix", className="fw-bold text-danger"),
                html.P("Translating empirical restructuring metrics into organizational behavior implications and actionable HR intervention playbooks.", className="text-muted")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Interactive Workforce Restructuring Risk Simulator", className="mb-0 fw-bold")),
                    dbc.CardBody([
                        html.Label("Anticipated Workforce Cut Percentage:", className="fw-semibold"),
                        dcc.Slider(id="slider-pct", min=5, max=75, step=5, value=20, marks={5: "5%", 25: "25%", 50: "50%", 75: "75%"}),
                        html.Br(),
                        html.Label("Downsizing History (Prior Waves Conducted):", className="fw-semibold"),
                        dcc.RadioItems(
                            id="radio-rec",
                            options=[
                                {"label": " First Restructuring Round (Single Wave)", "value": 1},
                                {"label": " Second Restructuring Round (Two Waves)", "value": 2},
                                {"label": " Chronic Restructuring (3+ Waves)", "value": 3}
                            ],
                            value=1,
                            className="mb-3"
                        ),
                        html.Label("Days Elapsed Since Prior Restructuring:", className="fw-semibold"),
                        dcc.Slider(id="slider-days", min=30, max=500, step=30, value=180, marks={30: "30d", 90: "90d", 180: "180d", 365: "1yr"}),
                    ])
                ], className="shadow-sm border-0 mb-4")
            ], width=12, lg=5),
            dbc.Col([
                html.Div(id="risk-output-card")
            ], width=12, lg=7)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card(dbc.CardBody([
                    html.H5("Four-Stage Strategic HRM Restructuring Playbook", className="fw-bold text-primary mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.H6("Stage 1: Pre-Downsizing Audit", className="fw-bold"),
                            html.P("Conduct critical skill dependency audits; map tacit architectural knowledge; verify non-labor cost cutting measures first; assess severance financial liability.", className="small text-muted")
                        ], md=4),
                        dbc.Col([
                            html.H6("Stage 2: Implementation & Justice", className="fw-bold"),
                            html.P("Ensure procedural fairness with objective, skill-based retention criteria; transparent senior leadership communication; manager training on empathetic termination; comprehensive outplacement support.", className="small text-muted")
                        ], md=4),
                        dbc.Col([
                            html.H6("Stage 3: Post-Downsizing Retention", className="fw-bold"),
                            html.P("Actively counteract 'survivor syndrome'; redistribute workloads to prevent burnout; offer retention bonuses to critical core talent; establish psychological safety forums.", className="small text-muted")
                        ], md=4),
                    ])
                ]), className="shadow-sm border-0 bg-light")
            ], width=12)
        ])
    ])


# Routing Callback
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return build_page_1()
    elif pathname == "/severity":
        return build_page_2()
    elif pathname == "/characteristics":
        return build_page_3()
    elif pathname == "/recurrence":
        return build_page_4()
    elif pathname == "/statistics":
        return build_page_5()
    elif pathname == "/strategic-hrm":
        return build_page_6()
    return build_page_1()


# Interactive WRRI Risk Simulator Callback
@app.callback(
    Output("risk-output-card", "children"),
    [Input("slider-pct", "value"), Input("radio-rec", "value"), Input("slider-days", "value")]
)
def update_risk_score(pct_val, rec_val, days_val):
    # Component 1: Intensity
    comp_i = min(25.0, (pct_val / 100.0) * 50.0)
    # Component 2: Magnitude proxy
    comp_m = 12.5  # Baseline median
    # Component 3: Recurrence
    comp_r = 5.0 if rec_val == 1 else (15.0 if rec_val == 2 else 25.0)
    # Component 4: Velocity
    if rec_val == 1:
        comp_v = 5.0
    else:
        comp_v = 25.0 if days_val < 90 else (20.0 if days_val < 180 else (12.0 if days_val < 365 else 7.0))
        
    score = comp_i + comp_m + comp_r + comp_v
    
    if score < 35:
        badge = "badge bg-success"
        category = "Lower Restructuring Exposure"
        ob_implication = "Minimal survivor syndrome expected. Standard organizational communication and severance outplacement are sufficient."
    elif score < 55:
        badge = "badge bg-warning text-dark"
        category = "Moderate Restructuring Exposure"
        ob_implication = "Moderate risk of psychological contract breach. Workload redistribution and team realignments required to prevent survivor fatigue."
    elif score < 75:
        badge = "badge bg-danger"
        category = "Elevated Restructuring Exposure"
        ob_implication = "Acute risk of survivor syndrome: top performer voluntary flight, elevated anxiety, institutional knowledge loss. High change management urgency."
    else:
        badge = "badge bg-dark"
        category = "Critical / Chronic Restructuring Exposure"
        ob_implication = "Severe existential organizational disruption. Prolonged restructuring has broken psychological contracts. Immediate leadership intervention required."

    return dbc.Card([
        dbc.CardHeader(html.H5("Calculated Workforce Restructuring Risk Indicator (WRRI)", className="mb-0 fw-bold")),
        dbc.CardBody([
            html.Div([
                html.H1(f"{score:.1f} / 100", className="fw-bold d-inline me-3 text-danger"),
                html.Span(category, className=f"{badge} fs-6 align-middle p-2")
            ]),
            html.Hr(),
            html.H6("Organizational Behaviour (OB) Implications:", className="fw-bold mt-3"),
            html.P(ob_implication, className="text-dark"),
            html.H6("Strategic HR Recommended Action:", className="fw-bold mt-3"),
            html.Ul([
                html.Li(f"Intensity Exposure Score: {comp_i:.1f} / 25.0"),
                html.Li(f"Recurrence Exposure Score: {comp_r:.1f} / 25.0 ({'Single event' if rec_val == 1 else ('Two waves' if rec_val == 2 else 'Chronic waves')})"),
                html.Li(f"Velocity Compression Score: {comp_v:.1f} / 25.0 ({days_val} days spacing)")
            ], className="small text-muted")
        ])
    ], className="shadow-sm border-0")


if __name__ == "__main__":
    print("Starting Strategic HRM & Corporate Layoffs Interactive Portal...")
    app.run(debug=True, port=8050)
