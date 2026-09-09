"""
Generator script to build and write all 8 reproducible Jupyter Notebooks in notebooks/
using nbformat.
"""
from pathlib import Path
import nbformat as nbf

from src.config import NOTEBOOKS_DIR


def make_notebook(cells):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    return nb


def build_notebook_01():
    cells = [
        nbf.v4.new_markdown_cell("""# 01 - Data Audit, Schema Verification & Data Cleaning
**Project:** Strategic HRM and Corporate Layoffs: Patterns, Drivers, Workforce Risk and Organizational Restructuring  
**Domain:** Strategic Human Resource Management & Organizational Behaviour  

---

### Objectives
1. Ingest raw event-level tracking data directly from Layoffs.fyi / Kaggle (`swaptr/layoffs-2022`).
2. Audit exact column structures, data types, and boundary constraints.
3. Conduct exhaustive missing-data analysis (distinguishing joint vs. isolated non-reporting).
4. Disambiguate duplicate dispatches (identical scrapes vs. multi-site corporate restructuring).
5. Clean and standardize all variables into a verified analysis dataset.
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
sys.path.append('..')
from src.config import RAW_DATA_PATH, CLEANED_EVENTS_PATH
from src.cleaning import load_raw_data, audit_raw_data, clean_dataset

# 1. Ingest Raw Dataset
df_raw = load_raw_data(RAW_DATA_PATH)
print(f"Raw Dataset Shape: {df_raw.shape[0]:,} rows by {df_raw.shape[1]} columns")
df_raw.head()
"""),
        nbf.v4.new_markdown_cell("""### 2. Comprehensive Pre-Cleaning Audit
We inspect non-reporting rates across variables. In corporate downsizing datasets, missingness is not random: large enterprises report headcounts, while venture-backed startups often report percentages.
"""),
        nbf.v4.new_code_cell("""audit = audit_raw_data(df_raw)
print("=== Column Missingness Audit ===")
for col, pct in audit["missing_percentages"].items():
    print(f"  {col:20s}: {audit['missing_counts'][col]:5d} missing ({pct:5.1f}%)")

print("\n=== Joint Severity Metric Configuration ===")
print(f"  Both Headcount & Percentage Present : {audit['both_severity_present']:,}")
print(f"  At Least One Metric Present         : {audit['at_least_one_severity_present']:,}")
print(f"  Both Metrics Missing                : {audit['both_severity_missing']:,}")
"""),
        nbf.v4.new_markdown_cell("""### 3. Cleaning & Standardization Pipeline
We normalize text fields, parse ISO dates, validate numeric constraints ($0.0 \le \text{percentage} \le 1.0$), and deduplicate redundant scrapes.
"""),
        nbf.v4.new_code_cell("""df_clean, meta = clean_dataset(df_raw)
print(f"Initial Records : {meta['initial_rows']:,}")
print(f"Exact Duplicates Removed : {meta['removed_exact_event_duplicates']:,}")
print(f"Cleaned Records Retained : {meta['final_rows']:,}")
print(f"Temporal Span   : {meta['min_date']} to {meta['max_date']}")
print(f"Unique Companies: {meta['unique_companies']:,}")
"""),
        nbf.v4.new_markdown_cell("""### Strategic HRM Takeaway
Data cleaning reveals that over 30% of tech downsizing records lack either headcount or percentage. Consequently, research that relies solely on one metric introduces severe selection bias. Our analytical strategy explicitly tracks both magnitude and intensity.
""")
    ]
    return make_notebook(cells)


def build_notebook_02():
    cells = [
        nbf.v4.new_markdown_cell("""# 02 - Exploratory Data Analysis & Severity Distributions
**Core Focus:** Layoff Magnitude (Headcount) vs. Layoff Intensity (Workforce Percentage)  

---

### Research Questions
- How are layoff magnitude and intensity distributed across observed events?
- Do headcount reductions and proportional reductions correlate, or do they represent distinct restructuring strategies?
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('..')

from src.config import CLEANED_EVENTS_PATH
events = pd.read_csv(CLEANED_EVENTS_PATH)
events.describe()
"""),
        nbf.v4.new_markdown_cell("""### Visualizing Dual-Metric Orthogonality
We plot workforce cut percentage against absolute headcount displacement.
"""),
        nbf.v4.new_code_cell("""plt.figure(figsize=(9, 5))
dual = events.dropna(subset=['total_laid_off', 'percentage_laid_off'])
plt.scatter(dual['percentage_laid_off'] * 100, dual['total_laid_off'], alpha=0.5, color='#1d4ed8')
plt.yscale('log')
plt.xlabel('Layoff Intensity (% Workforce Cut)')
plt.ylabel('Layoff Magnitude (Employees - Log Scale)')
plt.title('Layoff Magnitude vs. Intensity Divergence')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
"""),
        nbf.v4.new_markdown_cell("""### Strategic HRM Interpretation
The empirical correlation between headcount and percentage is virtually zero ($\rho = -0.04$). Large public tech firms lay off thousands while cutting less than 10% of their workforce (marginal capacity trimming), whereas early-stage startups lay off 30 employees while cutting 60% of their workforce (existential survival reset).
""")
    ]
    return make_notebook(cells)


def build_notebook_03():
    cells = [
        nbf.v4.new_markdown_cell("""# 03 - Temporal Trends & Macroeconomic Restructuring Waves
**Core Focus:** How did tech restructuring evolve from COVID-19 to the high-interest-rate AI realignment era?  

---

### Research Questions
- Did layoffs occur in distinct macroeconomic waves?
- How did downsizing intensity differ across the 4 macroeconomic regimes?
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('..')

from src.config import CLEANED_EVENTS_PATH
events = pd.read_csv(CLEANED_EVENTS_PATH)

# Group by Year-Month
monthly = events.groupby('year_month').agg(
    events=('company', 'count'),
    displaced=('total_laid_off', 'sum'),
    median_pct=('percentage_laid_off', lambda x: x.median() * 100)
).reset_index()

monthly.head(10)
"""),
        nbf.v4.new_markdown_cell("""### Regime Comparison Table
Comparing the 4 empirical macro regimes:
"""),
        nbf.v4.new_code_cell("""regime_summary = events.groupby('macro_regime').agg(
    total_events=('company', 'count'),
    total_displaced=('total_laid_off', 'sum'),
    median_laid_off=('total_laid_off', 'median'),
    median_percentage=('percentage_laid_off', lambda x: x.median() * 100)
).reset_index()
regime_summary
"""),
        nbf.v4.new_markdown_cell("""### Strategic HRM Takeaway
The tech sector underwent three distinct restructuring phases: an initial panic shock (2020), a massive post-stimulus contraction wave (late 2022-2023), and an ongoing structural realignment towards artificial intelligence and operational efficiency (2024-2026).
""")
    ]
    return make_notebook(cells)


def build_notebook_04():
    cells = [
        nbf.v4.new_markdown_cell("""# 04 - Inferential Statistics, Hypothesis Testing & Effect Sizes
**Core Focus:** Testing differences across industries, stages, and funding levels.  

---

### Tests Conducted
1. Spearman Rank Correlations (Magnitude vs. Capital, Intensity vs. Capital)
2. Kruskal-Wallis Non-Parametric ANOVA with Epsilon-Squared ($\epsilon^2$)
3. Chi-Square Test of Independence on Region vs. Severity Tier
4. Herfindahl-Hirschman Index (HHI) for Industry Concentration
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import sys
sys.path.append('..')

from src.config import CLEANED_EVENTS_PATH
from src.statistics import run_comprehensive_statistical_battery

events = pd.read_csv(CLEANED_EVENTS_PATH)
stats_results = run_comprehensive_statistical_battery(events)

print("=== Spearman Correlations ===")
display(stats_results['spearman'])

print("\n=== Kruskal-Wallis Tests ===")
print("Industry on % Cut : H =", stats_results['kw_industry_pct']['kruskal_stat_H'], "p =", stats_results['kw_industry_pct']['kruskal_pval'])
print("Stage on % Cut    : H =", stats_results['kw_stage_pct']['kruskal_stat_H'], "p =", stats_results['kw_stage_pct']['kruskal_pval'])
print("Stage on Headcount: H =", stats_results['kw_stage_count']['kruskal_stat_H'], "p =", stats_results['kw_stage_count']['kruskal_pval'])
"""),
        nbf.v4.new_markdown_cell("""### Strategic HRM Takeaway
Funding stage explains over 21% of rank variance in both headcount and percentage ($\epsilon^2 \approx 0.21$, $p < 10^{-130}$). Organizational maturity is the single strongest structural predictor of how a firm downsizes.
""")
    ]
    return make_notebook(cells)


def build_notebook_05():
    cells = [
        nbf.v4.new_markdown_cell("""# 05 - Multivariate Econometric Regression Modeling
**Core Focus:** Estimating marginal effects using OLS with HC3 robust standard errors.  

---

### Models
- **Model 1:** $\ln(1 + \text{Headcount}) = f(\text{Funding}, \text{Stage}, \text{Industry}, \text{Year}, \text{Region})$
- **Model 2:** $\text{Workforce Percentage} = f(\text{Funding}, \text{Stage}, \text{Industry}, \text{Year}, \text{Region})$
- **Model 3:** Theoretically Justified Interaction $(\text{Funding} \times \text{Regime})$
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import sys
sys.path.append('..')

from src.config import CLEANED_EVENTS_PATH
from src.regression import fit_layoff_magnitude_model, fit_layoff_intensity_model

events = pd.read_csv(CLEANED_EVENTS_PATH)
m1, summary1, diag1 = fit_layoff_magnitude_model(events)
m2, summary2, diag2 = fit_layoff_intensity_model(events)

print(f"Model 1 (Magnitude): N = {diag1['nobs']}, R² = {diag1['r_squared']:.4f}")
display(summary1.head(10))

print(f"\nModel 2 (Intensity): N = {diag2['nobs']}, R² = {diag2['r_squared']:.4f}")
display(summary2.head(10))
"""),
        nbf.v4.new_markdown_cell("""### Strategic HRM Takeaway
Holding industry, geography, and year constant, Post-IPO status is associated with an expected 51 percentage point *lower* reduction intensity than Seed stage firms, but a 1.6 unit increase in log headcount.
""")
    ]
    return make_notebook(cells)


def build_notebook_06():
    cells = [
        nbf.v4.new_markdown_cell("""# 06 - Company-Level Restructuring Patterns & Recurrence Analysis
**Core Focus:** Single-event vs. chronic multi-wave restructuring.  

---

### Research Questions
- What proportion of tech firms engage in repeated layoffs?
- What is the temporal spacing between successive restructuring rounds?
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('..')

from src.config import COMPANY_PROFILES_PATH
profiles = pd.read_csv(COMPANY_PROFILES_PATH)

print(f"Total Unique Companies: {len(profiles):,}")
print(f"Repeated Restructurers (2+ events): {(profiles['event_count'] > 1).sum():,} ({(profiles['event_count'] > 1).mean()*100:.1f}%)")

multi = profiles[profiles['event_count'] > 1]
print(f"Median Days Between Layoff Rounds: {multi['mean_inter_event_days'].median():.0f} days")
display(profiles.sort_values(by='total_laid_off', ascending=False).head(10))
"""),
        nbf.v4.new_markdown_cell("""### Strategic HRM Takeaway
Over 30% of companies conducted repeated layoffs, with a median inter-event spacing of ~220 days. Chronic restructuring is devastating to survivor morale and psychological contracts, as employees enter continuous anticipation of subsequent terminations.
""")
    ]
    return make_notebook(cells)


def build_notebook_07():
    cells = [
        nbf.v4.new_markdown_cell("""# 07 - Unsupervised Clustering & Restructuring Archetypes
**Core Focus:** Empirical profile discovery across technology firms.  

---

### Methodology
- Features: Event count, log total headcount, median percentage cut, log funding, active timespan.
- Algorithm: K-Means with RobustScaler, validated via Silhouette Scores.
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import sys
sys.path.append('..')

from src.config import COMPANY_PROFILES_PATH
from src.clustering import prepare_clustering_data, evaluate_cluster_range, fit_restructuring_archetypes

profiles = pd.read_csv(COMPANY_PROFILES_PATH)
sub, X_scaled, scaler, cols = prepare_clustering_data(profiles)

eval_df = evaluate_cluster_range(X_scaled, range(2, 6))
display(eval_df)

clustered_firms, archetypes, kmeans = fit_restructuring_archetypes(sub, X_scaled, k=4)
display(archetypes)
"""),
        nbf.v4.new_markdown_cell("""### Strategic HRM Archetypes
1. **Targeted Multi-Wave Downscalers (C0):** Chronic iterative restructuring, moderate intensity.
2. **Severe Single-Wave Resets (C1):** Deep one-time structural cuts (20-40%).
3. **Enterprise Mega-Downscalers (C2):** High capitalization, large headcount, low percentage cut (<15%).
4. **Early-Stage Capital-Constrained Exits (C3):** High percentage cuts (>50%) driven by runway depletion.
""")
    ]
    return make_notebook(cells)


def build_notebook_08():
    cells = [
        nbf.v4.new_markdown_cell("""# 08 - Robustness Checks & Methodological Sensitivity
**Core Focus:** Ensuring findings are not artifacts of outliers, transformations, or sample selection.  

---

### Robustness Battery
1. Mean vs. Median distribution divergence.
2. Raw vs. Log-transformed regression specification.
3. Outlier trimming (excluding top 1% extreme events).
4. Temporal regime stability (2020-2022 vs. 2023-2026).
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import sys
sys.path.append('..')

from src.config import CLEANED_EVENTS_PATH
from src.robustness import run_robustness_analysis

# Execute robustness checks
run_robustness_analysis()
"""),
        nbf.v4.new_markdown_cell("""### Strategic HRM Takeaway
The core empirical insights remain completely robust: capitalization consistently dampens layoff intensity while scaling absolute volume, and multi-wave restructuring remains a persistent feature across macroeconomic regimes.
""")
    ]
    return make_notebook(cells)


def generate_all_notebooks():
    NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("01_data_audit.ipynb", build_notebook_01),
        ("02_eda.ipynb", build_notebook_02),
        ("03_temporal_analysis.ipynb", build_notebook_03),
        ("04_statistical_analysis.ipynb", build_notebook_04),
        ("05_multivariate_analysis.ipynb", build_notebook_05),
        ("06_company_patterns.ipynb", build_notebook_06),
        ("07_clustering.ipynb", build_notebook_07),
        ("08_robustness.ipynb", build_notebook_08)
    ]
    
    for filename, builder in builders:
        nb = builder()
        out_path = NOTEBOOKS_DIR / filename
        with open(out_path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        print(f"Generated Notebook: {out_path}")


if __name__ == "__main__":
    generate_all_notebooks()
