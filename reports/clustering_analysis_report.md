# Unsupervised Clustering & Organizational Restructuring Profiles

## 1. Cluster Validation Metrics across k
|   k |   Silhouette_Score |   Davies_Bouldin_Index |   Calinski_Harabasz_Index |   Inertia |
|----:|-------------------:|-----------------------:|--------------------------:|----------:|
|   2 |             0.3844 |                 1.1393 |                    732.48 |   7085.25 |
|   3 |             0.3794 |                 1.0209 |                    670.13 |   5594.69 |
|   4 |             0.3789 |                 0.9081 |                    714.18 |   4377.85 |
|   5 |             0.2715 |                 1.0573 |                    702.32 |   3706.73 |

## 2. Discovered Restructuring Archetype Profiles (k = 4)
|   cluster |   firm_count |   median_events |   mean_events |   median_total_laid_off |   mean_total_laid_off |   median_intensity |   mean_intensity |   median_funding_m |   median_timespan_days | top_stage               | top_industry                 | Theoretical_Archetype                                                |
|----------:|-------------:|----------------:|--------------:|------------------------:|----------------------:|-------------------:|-----------------:|-------------------:|-----------------------:|:------------------------|:-----------------------------|:---------------------------------------------------------------------|
|         0 |          180 |               1 |       1.28889 |                    81.5 |               158.483 |             0.8225 |         0.804833 |               45   |                      0 | Unspecified / Private   | Consumer & Retail            | Targeted Multi-Wave Downscalers (Iterative Restructuring)            |
|         1 |          949 |               1 |       1.28767 |                    63   |               116.275 |             0.17   |         0.18555  |              131.5 |                      0 | Late Stage (Series C-D) | Fintech & Financial Services | Severe Single-Wave Resets (Deep Structural Cuts)                     |
|         2 |          415 |               3 |       3.23373 |                   400   |              1119.81  |             0.12   |         0.146361 |              460   |                   1034 | Public (Post-IPO)       | Consumer & Retail            | Enterprise Mega-Downscalers (High Capitalization, Scaled Magnitude)  |
|         3 |           10 |              12 |      14.1     |                 19519   |             24091.2   |             0.0525 |         0.0685   |             3300   |                   1413 | Public (Post-IPO)       | Consumer & Retail            | Early-Stage Capital-Constrained Exits (High Percentage, Small Scale) |

## 3. Strategic HRM Interpretation of Archetypes
- **Targeted Multi-Wave Downscalers:** Conduct repeated rounds with moderate percentage cuts. Presents acute survivor anxiety and repeated psychological contract violation.
- **Severe Single-Wave Resets:** Conduct a single, deep restructuring (25-40% cut). Clear 'rip the band-aid' approach; requires intensive procedural justice and immediate survivor stabilization.
- **Enterprise Mega-Downscalers:** Large public firms releasing thousands of employees with small percentage impact (<15%). Massive external media attention, high public visibility, risk of brand erosion.
- **Early-Stage Capital-Constrained Exits:** Seed/Series A firms with >40% cuts driven by cash runway exhaustion. Risk of critical technical brain drain and loss of core architectural knowledge.