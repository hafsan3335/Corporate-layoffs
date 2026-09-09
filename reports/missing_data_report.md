# Missing Data Audit & Methodological Treatment

## 1. Executive Summary
In corporate downsizing datasets, non-reporting is systematically structured by media coverage incentives: large enterprise layoffs frequently report exact headcounts, whereas early-stage startups often report percentage reductions to avoid disclosing absolute staff sizes.

## 2. Severity Metric Missingness Breakdown
Total Cleaned Events Analyzed: **4,589**

| Empirical Configuration | Count | Percentage | Research Method Treatment |
| :--- | :--- | :--- | :--- |
| **Both Metrics Observed** (`total_laid_off` AND `percentage_laid_off`) | **2,027** | **44.17%** | Core analytical benchmark for bivariate comparisons, dual modeling, and elasticity estimation. |
| **Only Headcount Observed** | **969** | **21.12%** | Retained for absolute volume models, temporal trends, and industry aggregate analysis. |
| **Only Percentage Observed** | **850** | **18.52%** | Retained for restructuring intensity models and proportional vulnerability analysis. |
| **Both Severity Metrics Missing** | **743** | **16.19%** | Retained strictly for event-frequency and timing analysis; excluded from continuous regression. |

## 3. Missingness by Column
| Variable | Missing Count | % of Records | Handling Strategy |
| :--- | :--- | :--- | :--- |
| `company` | 0 | 0.00% | Complete. Used as primary key for firm aggregation. |
| `date` | 0 | 0.00% | Complete. Used for all time-series and rolling trends. |
| `total_laid_off` | 1,593 | 34.71% | Log-transformed in regression (`log1p`); analyzed in non-missing subset. |
| `percentage_laid_off` | 1,712 | 37.31% | Modeled separately in intensity regression; robustness checks applied. |
| `funds_raised` | 544 | 11.85% | Log-transformed; dummy variable indicator for unstated funding tested in robustness. |
| `industry` | 0 | 0.00% | Categorized; nulls harmonized into 'Unknown'. |
| `stage` | 0 | 0.00% | Categorized; nulls harmonized into 'Unknown'. |
| `country` | 0 | 0.00% | Categorized; nulls harmonized into 'Unknown'. |

## 4. Methodological Safeguard
Under no circumstances are missing values imputed using mean/median substitution for dependent variables, as this would artificially compress variance and distort standard errors. Listwise deletion is applied explicitly within model specifications and reported with exact sample sizes ($N$).
