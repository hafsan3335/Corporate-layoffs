# Inferential Statistical Results & Hypothesis Tests

## 1. Spearman Rank Correlations (Robust to Heavy Skew)

| Variable 1     | Variable 2          | Relationship                          |   Sample Size (N) |   Spearman Rho |      p-value |   95% CI Lower |   95% CI Upper | Significance   |
|:---------------|:--------------------|:--------------------------------------|------------------:|---------------:|-------------:|---------------:|---------------:|:---------------|
| funds_raised   | total_laid_off      | Capitalization vs. Layoff Magnitude   |              2676 |         0.4081 | 5.87517e-108 |         0.3761 |         0.4392 | ***            |
| funds_raised   | percentage_laid_off | Capitalization vs. Layoff Intensity   |              2556 |        -0.3901 | 1.14317e-93  |        -0.4225 |        -0.3567 | ***            |
| total_laid_off | percentage_laid_off | Layoff Magnitude vs. Layoff Intensity |              2027 |        -0.0422 | 0.0573427    |        -0.0856 |         0.0013 | ns             |

## 2. Non-Parametric ANOVA (Kruskal-Wallis Tests & Effect Sizes)

- **Industry on Layoff Percentage:** H = 93.144, p = 1.2717e-15, Epsilon^2 = 0.029
- **Funding Stage on Layoff Percentage:** H = 633.846, p = 1.2329e-131, Epsilon^2 = 0.2182
- **Funding Stage on Headcount Laid Off:** H = 626.885, p = 3.8745e-130, Epsilon^2 = 0.2072
- **Macro Regime on Layoff Percentage:** H = 33.089, p = 3.0839e-07, Epsilon^2 = 0.0105

## 3. Contingency Analysis (Chi-Square Test)

- **Region vs. Layoff Magnitude Severity Tier:** Chi2 = 118.8, df = 24, p = 1.5863e-14, Cramér's V = 0.0804

## 4. Industry Concentration (HHI Index by Year)

- **2020:** HHI = 1297.76 (Unconcentrated / Broad Restructuring)
- **2021:** HHI = 1797.52 (Moderately Concentrated)
- **2022:** HHI = 1254.9 (Unconcentrated / Broad Restructuring)
- **2023:** HHI = 1225.33 (Unconcentrated / Broad Restructuring)
- **2024:** HHI = 1302.38 (Unconcentrated / Broad Restructuring)
- **2025:** HHI = 1564.36 (Moderately Concentrated)
- **2026:** HHI = 1470.6 (Unconcentrated / Broad Restructuring)