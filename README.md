# Strategic HRM and Corporate Layoffs: Patterns, Drivers, Workforce Risk and Organizational Restructuring

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Econometrics: Statsmodels HC3](https://img.shields.io/badge/Econometrics-Statsmodels%20HC3-green.svg)](https://www.statsmodels.org/)
[![Dashboard: Plotly / Dash](https://img.shields.io/badge/Dashboard-Plotly%20%2F%20Dash-orange.svg)](https://dash.plotly.com/)
[![Tests: Pytest Passing](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://pytest.org/)

An undergraduate research project in **Strategic Human Resource Management**, **Organizational Behaviour**, and **Quantitative Social Research**.

---

## Executive Summary & Research Positioning

This project investigates global corporate downsizing across the technology sector from the COVID-19 pandemic through the post-2023 high-interest-rate and artificial intelligence realignment era (**March 11, 2020 – September 3, 2026**). 

Rather than framing layoffs as a generic machine learning prediction contest, this study models workforce reductions as an **event-level organizational restructuring phenomenon**. We analyze **4,589 verified layoff events** across **2,975 organizations** from the Layoffs.fyi / Kaggle dataset (`swaptr/layoffs-2022`, Version 478).

### The Strategic HRM Bridge
```
Empirical Restructuring Event
  (Layoffs.fyi 2020 - 2026, N = 4,589)
               │
               ▼
Strategic Firm Conditions
  (Capitalization, Funding Stage, Industry, Macro Timing)
               │
               ▼
Human-Capital Risk & Structural Disruption
  (Magnitude vs. Intensity Divergence, Recurrence Latency)
               │
               ▼
SHRM & Organizational Behaviour Theories
  (Workforce Planning, Organizational Justice, Survivor Syndrome)
               │
               ▼
Evidence-Informed HR Restructuring Playbook
  (Pre-downsizing capability audits, procedural fairness, survivor retention)
```

---

## Key Research Findings

1. **The Magnitude vs. Intensity Orthogonality:**
   - Absolute headcount reduction (**Magnitude**) and proportional workforce cut (**Intensity**) are statistically uncorrelated ($\rho = -0.0422, p = 0.0573$).
   - Evaluating downsizing solely by public headcount headlines obscures organizational vulnerability. A 40-person cut can threaten startup viability (e.g., 60% of staff), whereas a 2,000-person cut may represent marginal operational trimming (<3%) for an enterprise.
2. **The Capitalization & Maturity Paradox:**
   - Financial capitalization correlates positively with absolute layoffs ($\rho = +0.4081, p < 10^{-100}$) but negatively with layoff intensity ($\rho = -0.3901, p < 10^{-90}$).
   - In econometric regressions with MacKinnon-White HC3 robust standard errors, mature public (Post-IPO) firms downsized an estimated **51.0 percentage points less** of their workforce than Seed startups ($p < 0.001$), while shedding significantly higher absolute headcounts ($\hat{\beta} = +1.603, p < 0.001$).
3. **Chronic Multi-Wave Restructuring:**
   - **899 firms (30.2%)** engaged in repeated restructuring rounds.
   - The median temporal latency between successive downsizing waves was **220 days** (~7.3 months), with over 25% occurring within 90 days. Iterative downsizing severely damages survivor psychological contracts and accelerates voluntary turnover among top performers.
4. **Empirical Restructuring Archetypes ($k = 4$):**
   - **Cluster 0 (High-Intensity Resets, 82% median cut):** Early-stage venture firms facing runway exhaustion.
   - **Cluster 1 (Single-Wave Growth Resets, 17% median cut):** Expansion-stage startups executing a disciplined one-time capacity realignment.
   - **Cluster 2 (Multi-Wave Enterprise Downsizers, 12% median cut, 3 rounds):** Mature corporations continuously rationalizing operating margins.
   - **Cluster 3 (Chronic Mega-Tech Downscalers, 5% median cut, 12 rounds):** Large technology conglomerates (Amazon, Meta, Google, Microsoft) reallocating capital from legacy bets toward artificial intelligence infrastructure.

---

## Visual Research Findings & Matplotlib Figure Gallery

Each figure below answers a core research question, paired with a plain-English explanation of the visual components, key statistical takeaways, and strategic implications for human resource leaders.

---

### Figure 1: Macroeconomic Waves of Technology Layoffs (2020–2026)
![Figure 1: Macroeconomic Waves of Technology Layoffs](figures/fig1_temporal_layoff_waves.png)

- **How to Read This Chart:**
  - The **light blue bars** represent the total number of tech workers laid off each month (in thousands).
  - The **solid dark blue line** shows the 3-month rolling average trend, smoothing out short-term reporting noise.
  - The **dashed red line** (right axis) tracks the monthly count of distinct layoff announcement events.
- **Key Findings (What the Data Shows):**
  - **Phase 1 (2020):** A sharp initial shock at the onset of COVID-19 (~81,000 workers displaced), followed by rapid stabilization.
  - **Phase 2 (2021):** An "easy-money" lull with almost zero layoffs (only 44 events all year), during which tech companies hired aggressively.
  - **Phase 3 (Late 2022 – 2023):** The **massive contraction peak**, driven by rising interest rates and overhiring corrections. 2023 alone saw **264,660 displaced workers** across 1,389 events.
  - **Phase 4 (2024 – 2026):** Event frequency dropped, but average event size grew substantially (mean 540 workers in 2025, 620 in 2026), indicating large structural enterprise realignments toward AI and capital efficiency.
- **Strategic HRM Takeaway:**
  - Corporate downsizing occurs in macroeconomic waves. When organizations engage in speculative talent acquisition during booms without rigorous workforce planning, they inevitably face collective, painful restructuring when capital costs normalize.

---

### Figure 2: Layoff Magnitude vs. Layoff Intensity (Dual-Metric Divergence)
![Figure 2: Layoff Magnitude vs. Layoff Intensity](figures/fig2_magnitude_vs_intensity.png)

- **How to Read This Chart:**
  - The **horizontal axis** represents **Layoff Intensity** (% of the company's total workforce eliminated).
  - The **vertical axis** represents **Layoff Magnitude** (total headcount laid off, plotted on a logarithmic scale).
  - Each dot represents a single layoff event ($N = 2,031$ dual-reported events), colored by total funding raised ($M USD).
- **Key Findings (What the Data Shows):**
  - Magnitude and intensity are **completely uncorrelated** ($\rho = -0.0422, p = 0.0573$).
  - **Top-Left Quadrant (Enterprise Scale):** Mature, public corporations shed large headcounts (1,000 to 10,000+ employees) but cut only **5% to 15%** of their total workforce.
  - **Bottom-Right Quadrant (Startup Vulnerability):** Early-stage firms shed modest headcounts (20 to 150 employees), but eliminate **40% to 100%** of their entire staff.
- **Strategic HRM Takeaway:**
  - **Headcount alone is a misleading indicator of organizational harm.** Eliminating 40 people at an AI startup can destroy critical institutional memory and project velocity, whereas eliminating 2,000 people at a global conglomerate may represent marginal operational trimming. HR leaders must evaluate proportional workforce depletion.

---

### Figure 3: Cumulative Workforce Reductions Across Industry Sectors
![Figure 3: Cumulative Workforce Reductions Across Industry Sectors](figures/fig3_industry_hhi_concentration.png)

- **How to Read This Chart:**
  - A horizontal ranking of total tech workers displaced across major industry sectors from 2020 through 2026.
  - Bar widths display cumulative headcounts in thousands of employees.
- **Key Findings (What the Data Shows):**
  - **Consumer & Retail** led all sectors with **259,200 displaced workers**, reflecting the post-pandemic e-commerce normalization.
  - **Hardware & Manufacturing** followed with **118,600 displaced workers**, driven by semiconductor and device cyclicality.
  - **Travel & Transportation** (~102,700) and **Fintech & Financial Services** (~81,200) also experienced heavy downsizing.
  - Annual **Herfindahl-Hirschman Index (HHI)** concentration scores remained between **1,225 and 1,797**, confirming that restructuring was **broadly dispersed across the tech economy**, rather than confined to a single distressed niche.
- **Strategic HRM Takeaway:**
  - Because layoffs were systemic and economy-wide, displaced tech talent faced a contracted labor market with fewer outside job offers. For surviving employees, awareness of widespread industry cuts intensified job insecurity and reduced voluntary mobility.

---

### Figure 4: Organizational Maturity & Workforce Restructuring Asymmetry
![Figure 4: Organizational Maturity & Workforce Restructuring Asymmetry](figures/fig4_funding_stage_severity.png)

- **How to Read This Chart:**
  - **Panel A (Left, Blue):** Boxplot of absolute headcount laid off per event across maturity stages (from Seed through Post-IPO).
  - **Panel B (Right, Red):** Boxplot of workforce percentage cut per event across the exact same maturity stages.
- **Key Findings (What the Data Shows):**
  - **The Maturity Paradox:** As organizations mature, **Panel A rises sharply** (median headcounts jump from 25 at Seed to 180+ at Post-IPO), while **Panel B falls dramatically** (median cut drops from 60%+ at Seed to ~12%–15% at Post-IPO).
  - Kruskal-Wallis non-parametric tests confirm a **large effect size** ($\epsilon^2 = 0.2182, p < 10^{-130}$), proving that organizational maturity explains over 21% of all rank variation in downsizing intensity.
- **Strategic HRM Takeaway:**
  - Startups downsize to avoid corporate death (liquidation risk), necessitating emergency knowledge-retention triage. Mature corporations downsize to optimize quarterly margins and return on invested capital (ROIC), requiring robust outplacement and employer-brand protection.

---

### Figure 5: Restructuring Recurrence & Multi-Wave Timing
![Figure 5: Restructuring Recurrence & Multi-Wave Timing](figures/fig5_recurrence_and_inter_event_days.png)

- **How to Read This Chart:**
  - **Panel A (Left):** Distribution of companies by number of layoff rounds conducted (1, 2, 3, or 4+ rounds).
  - **Panel B (Right):** Histogram showing the temporal spacing (mean days) between successive layoff rounds for multi-wave firms.
- **Key Findings (What the Data Shows):**
  - **30.2% of all affected companies (899 firms)** executed multiple layoff waves. Over 10% conducted 3 or more separate rounds.
  - Among multi-wave downsizers, the median gap between rounds was **220 days** (~7.3 months), with over 25% of repeat rounds occurring within **90 days** of the prior announcement.
- **Strategic HRM Takeaway:**
  - **The Chronic Restructuring Trap:** Repeated mini-layoffs are toxic to organizational climate. In Organizational Justice theory, survivors can tolerate a single deep cut if leadership communicates finality and strategic necessity. Recurring rounds break psychological contracts, breed cynicism, and provoke proactive voluntary exits among the organization's highest-performing talent.

---

### Figure 6: Multivariate Regression Coefficient Forest Plot
![Figure 6: Regression Coefficient Forest Plot](figures/fig6_regression_forest_plot.png)

- **How to Read This Chart:**
  - A forest plot showing the econometric coefficients and 95% confidence intervals from our OLS model with HC3 robust standard errors ($N = 2,676, R^2 = 0.3172$).
  - Points to the **right of the dashed red line (0.0)** indicate a positive association with layoff headcount; points to the **left** indicate a negative association.
- **Key Findings (What the Data Shows):**
  - **Funding Raised ($\hat{\beta} = +0.1415, p < 0.001$):** Holding stage, industry, and year constant, higher capitalization is a statistically significant positive predictor of layoff headcount.
  - **Post-IPO Status ($\hat{\beta} = +1.6028, p < 0.001$):** The single largest positive predictor of headcount magnitude relative to Seed stage firms.
  - **Marketing & Media ($\hat{\beta} = -0.5306, p < 0.001$):** Experienced significantly smaller average headcount cuts than the Consumer & Retail reference group.
- **Strategic HRM Takeaway:**
  - Confirms statistically that firm capitalization and organizational maturity dictate restructuring scale, even when controlling for macroeconomic timing and industry sector.

---

### Figure 7: Discovered Organizational Restructuring Archetypes
![Figure 7: Discovered Restructuring Archetypes](figures/fig7_cluster_restructuring_archetypes.png)

- **How to Read This Chart:**
  - **Panel A (Left):** Scatter plot of all 1,554 fully profiled companies, colored by their unsupervised machine learning cluster ($k = 4$).
  - **Panel B (Right):** Bar chart comparing the median cut percentage (red bars) and median number of downsizing waves (blue bars) for each cluster.
- **Key Findings (What the Data Shows):**
  - **Cluster 0 (High-Intensity Resets, 82.3% cut, 1 wave):** Early venture firms facing sudden cash exhaustion.
  - **Cluster 1 (Single-Wave Growth Cuts, 17.0% cut, 1 wave):** The standard corporate reset: a one-time structural realignment.
  - **Cluster 2 (Multi-Wave Enterprise Downsizers, 12.0% cut, 3 waves):** Public firms conducting prolonged, iterative capacity adjustments.
  - **Cluster 3 (Chronic Mega-Tech Downscalers, 5.3% cut, 12 waves):** Global conglomerates (Amazon, Meta, Google) executing dozens of divisional cuts across multiple years.
- **Strategic HRM Takeaway:**
  - Restructuring is not one-size-fits-all. Managing survivors in a Cluster 0 company requires crisis triage and retention bonuses, while managing survivors in Cluster 2 and Cluster 3 requires rebuilding trust, re-scoping expanded workloads, and halting the cycle of chronic anxiety.

---

### Figure 8: Workforce Restructuring Risk Indicator (WRRI) Profile
![Figure 8: Workforce Restructuring Risk Indicator Profile](figures/fig8_workforce_risk_matrix.png)

- **How to Read This Chart:**
  - **Panel A (Left):** Histogram of composite WRRI scores ($0–100$), combining intensity, scale, recurrence, and suddenness.
  - **Panel B (Right):** Donut chart categorizing all 4,589 events into four risk tiers.
- **Key Findings (What the Data Shows):**
  - The distribution centers around a median score of **47.5 / 100**.
  - **41.2%** of events presented **Moderate Risk**, **28.5%** presented **Elevated Risk**, and **14.1%** presented **Critical / Chronic Risk**.
  - Only **16.2%** qualified as **Lower Risk Exposure**.
- **Strategic HRM Takeaway:**
  - Over 83% of tech layoffs carried moderate-to-critical human capital disruption risk. HR executives can utilize the WRRI scorecard prior to restructuring to evaluate whether an impending cut risks catastrophic survivor disengagement.

---

## Theoretical Framework

- **Strategic HRM & Workforce Planning (Delery & Shaw, 2001; Cascio, 2002):** Explaining why multi-wave layoffs reflect reactive capacity adjustments and forecasting breakdowns rather than strategic human capital design.
- **Organizational Justice Theory (Colquitt, 2001; Greenberg, 1990):** Examining how procedural and interactional justice condition survivor perceptions and post-restructuring organizational performance.
- **Survivor Syndrome & Psychological Contract Theory (Rousseau, 1995; Brockner et al., 1987, 2004; Datta et al., 2010):** Analyzing why downsizing induces risk aversion, institutional knowledge drain, and burnout among surviving employees.

---

## Repository Architecture

```
corporate-layoffs/
│
├── README.md                                 <- Project overview, theory, and execution instructions
├── requirements.txt                          <- Pinned library dependencies
│
├── data/
│   ├── raw/
│   │   └── layoffs_raw.csv                   <- Pristine Layoffs.fyi version 478 CSV
│   └── processed/
│       ├── layoffs_cleaned_events.csv        <- Standardized event dataset with engineered features
│       ├── layoffs_company_profiles.csv      <- Organizational-level aggregation dataset
│       ├── clustered_company_profiles.csv    <- Firm-level restructuring cluster assignments
│       └── data_dictionary.md                <- Field specifications, types, and ranges
│
├── src/                                      <- Modular Python research engine
│   ├── __init__.py
│   ├── config.py                             <- Paths, constants, palettes, and mappings
│   ├── cleaning.py                           <- Ingestion, audit, deduplication, and bounds checking
│   ├── features.py                           <- Derived variables, macro regimes, and aggregations
│   ├── statistics.py                         <- Spearman correlations, Kruskal-Wallis, HHI index
│   ├── regression.py                         <- OLS models with HC3 robust standard errors & interactions
│   ├── clustering.py                         <- K-Means, silhouette evaluation, and profile discovery
│   ├── risk_index.py                         <- Workforce Restructuring Risk Indicator (WRRI)
│   ├── visualization.py                      <- Publication-grade Matplotlib static figure engine
│   ├── run_pipeline.py                       <- Master end-to-end execution runner
│   ├── generate_descriptive_stats.py         <- Descriptive statistics generator
│   ├── generate_notebooks.py                 <- Automated Jupyter notebook generator
│   └── robustness.py                         <- Sensitivity checks & model stability suite
│
├── notebooks/                                <- 8 Reproducible Research Notebooks
│   ├── 01_data_audit.ipynb                   <- Raw data audit, data dictionary, missingness
│   ├── 02_eda.ipynb                          <- Bivariate distributions & magnitude/intensity scatter
│   ├── 03_temporal_analysis.ipynb            <- Monthly trends, rolling averages, macro regimes
│   ├── 04_statistical_analysis.ipynb         <- Spearman tests, Kruskal-Wallis ANOVAs, effect sizes
│   ├── 05_multivariate_analysis.ipynb        <- OLS regressions, HC3 standard errors, interactions
│   ├── 06_company_patterns.ipynb             <- Recurrence, multi-wave downsizers, inter-event spacing
│   ├── 07_clustering.ipynb                   <- Unsupervised profile clustering (k=4 archetypes)
│   └── 08_robustness.ipynb                   <- Outlier trimming, raw vs. log, era split stability
│
├── dashboard/                                <- Plotly Research Applications
│   ├── app.py                                <- Live interactive 6-page Dash web application
│   ├── generate_standalone_dashboard.py      <- Standalone HTML compiler
│   └── index.html                            <- Self-contained interactive dashboard (opens in browser)
│
├── figures/                                  <- High-Resolution (300 DPI) Publication Figures
│   ├── fig1_temporal_layoff_waves.png        <- Monthly volumes, rolling averages, regime waves
│   ├── fig2_magnitude_vs_intensity.png       <- Dual-metric scatter with funding color gradient
│   ├── fig3_industry_hhi_concentration.png   <- Displaced workers by sector
│   ├── fig4_funding_stage_severity.png       <- Stage vs. magnitude & intensity dual boxplot
│   ├── fig5_recurrence_and_inter_event_days.png <- Recurrence counts & inter-event days histogram
│   ├── fig6_regression_forest_plot.png       <- Econometric coefficient forest plot (95% CIs)
│   ├── fig7_cluster_restructuring_archetypes.png <- Restructuring profile comparison
│   └── fig8_workforce_risk_matrix.png        <- WRRI composite risk distribution
│
├── reports/                                  <- Academic Research Reports
│   ├── data_dictionary.md                    <- Variable definitions and types
│   ├── missing_data_report.md                <- Systematic non-reporting analysis
│   ├── duplicate_report.md                   <- Disambiguation of identical vs. multi-site dispatches
│   ├── data_quality_report.md                <- Empirical data integrity verification
│   ├── descriptive_statistics.md             <- Full statistical summary tables
│   ├── statistical_results_table.md          <- Hypothesis tests, p-values, and effect sizes
│   ├── regression_diagnostics_report.md      <- Econometric model summaries and diagnostics
│   ├── clustering_analysis_report.md         <- Cluster validation metrics & profile summaries
│   ├── robustness_analysis_report.md         <- Sensitivity analysis results
│   └── strategic_hrm_research_report.md      <- Complete 16-section academic research paper
│
└── tests/                                    <- Automated Test Suite
    └── test_pipeline.py                      <- Pytest verification for cleaning, features, models
```

---

## Installation & Quickstart

### 1. Environment Setup
```bash
# Clone or navigate to the repository
cd corporate-layoffs

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Full Research Pipeline
To re-run data cleaning, feature engineering, statistical modeling, clustering, and figure generation:
```bash
python -m src.run_pipeline
```

### 3. Run Automated Tests
```bash
python -m pytest tests/
```

### 4. Explore the Interactive Plotly Dashboard
You can view the interactive dashboard in two ways:
- **Option A (Instant in Browser):** Simply double-click or open `dashboard/index.html` in any modern web browser.
- **Option B (Live Dash Server):**
  ```bash
  python dashboard/app.py
  # Open http://127.0.0.1:8050 in your browser
  ```

---

## Strategic HRM Four-Stage Translation Framework

Every statistical finding in this project is translated through our four-part analytical bridge:

| Empirical Data Finding | Strategic Business Meaning | Theoretical HR/OB Implication | Recommended HR Intervention |
| :--- | :--- | :--- | :--- |
| **Orthogonality of Magnitude & Intensity** ($\rho = -0.04$) | Headcount volume and percentage cut represent distinct decisions. | Survivor threat is governed by proportional depletion, not raw headcount. | Evaluate relative organizational disruption; de-scope unstaffed projects. |
| **Capitalization & Maturity Paradox** (Stage: $-51\%$ cut, $+1.6$ log headcount) | Mature enterprises cut marginal capacity; startups face existential resets. | Enterprise cuts risk employer brand; startup cuts trigger panic flight. | Enterprise: prioritize severance & outplacement. Startups: protect core IP & tacit knowledge. |
| **Recurrence Rate** (30.2% repeated, 220d median spacing) | Downsizing is often an iterative, multi-wave cost-containment trap. | Chronic restructuring shatters psychological contracts and elevates turnover. | Execute a single definitive restructuring; communicate credible finality. |
| **Industry Diffusion** (HHI 1225–1797, broad dispersion) | Tech restructuring was systemic across all sectors, not isolated to niches. | External market contractions constrain outside employment opportunities. | Reassure survivors that restructuring is macro-driven; retain high performers. |

---

## Citation & Academic References

- Cascio, W. F. (2002). *Responsible Restructuring: Creative and Profitable Alternatives to Layoffs*. Berrett-Koehler Publishers.
- Colquitt, J. A. (2001). On the dimensionality of organizational justice: A construct validation of a measure. *Journal of Applied Psychology*, 86(3), 386-400.
- Datta, D. K., Guthrie, J. P., Basuil, D., & Pandey, A. (2010). Causes and effects of employee downsizing: A review and synthesis. *Journal of Management*, 36(1), 281-348.
- Delery, J. E., & Shaw, J. D. (2001). The strategic management of people in work organizations: Review, synthesis, and extension. *Research in Personnel and Human Resources Management*, 20, 165-197.
- Greenberg, J. (1990). Organizational justice: Yesterday, today, and tomorrow. *Journal of Management*, 16(2), 399-432.
- Rousseau, D. M. (1995). *Psychological Contracts in Organizations: Understanding Written and Unwritten Agreements*. SAGE Publications.
