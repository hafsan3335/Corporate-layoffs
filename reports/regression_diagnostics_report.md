# Multivariate Econometric Regression Diagnostics & Results

## Model 1: Layoff Magnitude (Log-Transformed Headcount)
**Sample Size (N):** 2,676 | **R²:** 0.3172 | **Adj R²:** 0.3092 | **F-Stat:** 38.10 (p = 2.3263e-186)
**Standard Errors:** HC3 (MacKinnon and White heteroscedasticity-consistent)

|                                                                                             |   Coefficient |   Robust_SE |   t_statistic |   p_value |   CI_Lower_95 |   CI_Upper_95 |
|:--------------------------------------------------------------------------------------------|--------------:|------------:|--------------:|----------:|--------------:|--------------:|
| Intercept                                                                                   |        2.9697 |      0.1895 |       15.6734 |    0      |        2.5983 |        3.341  |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Acquired / Subsidiary]          |        1.2661 |      0.2024 |        6.2569 |    0      |        0.8695 |        1.6627 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Early Venture (Series A)]       |        0.1262 |      0.191  |        0.6606 |    0.5089 |       -0.2482 |        0.5006 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Expansion Stage (Series B)]     |        0.3916 |      0.1883 |        2.079  |    0.0376 |        0.0224 |        0.7607 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Growth Stage (Series E+)]       |        0.8575 |      0.2049 |        4.1858 |    0      |        0.456  |        1.259  |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Late Stage (Series C-D)]        |        0.5485 |      0.1937 |        2.8317 |    0.0046 |        0.1689 |        0.9282 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Private Equity Owned]           |        0.9318 |      0.2574 |        3.6203 |    0.0003 |        0.4273 |        1.4362 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Public (Post-IPO)]              |        1.6028 |      0.2063 |        7.7709 |    0      |        1.1985 |        2.007  |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Unspecified / Private]          |        0.6325 |      0.1954 |        3.2377 |    0.0012 |        0.2496 |        1.0154 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.EdTech & Learning]            |        0.0897 |      0.1013 |        0.8858 |    0.3757 |       -0.1088 |        0.2882 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Enterprise & Infrastructure]  |       -0.2575 |      0.0804 |       -3.2037 |    0.0014 |       -0.4151 |       -0.1    |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Fintech & Financial Services] |       -0.2533 |      0.0688 |       -3.6829 |    0.0002 |       -0.3881 |       -0.1185 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Hardware & Manufacturing]     |        0.1743 |      0.1876 |        0.9292 |    0.3528 |       -0.1933 |        0.542  |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Healthcare & BioTech]         |       -0.183  |      0.0842 |       -2.1739 |    0.0297 |       -0.3479 |       -0.018  |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Marketing & Media]            |       -0.5306 |      0.0808 |       -6.5668 |    0      |       -0.6889 |       -0.3722 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Other / Diversified]          |       -0.0024 |      0.0797 |       -0.0301 |    0.976  |       -0.1587 |        0.1539 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Professional Services]        |       -0.1592 |      0.1144 |       -1.3923 |    0.1638 |       -0.3834 |        0.0649 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Real Estate & PropTech]       |        0.1086 |      0.1035 |        1.0499 |    0.2938 |       -0.0942 |        0.3114 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Travel & Transportation]      |       -0.0196 |      0.0781 |       -0.2515 |    0.8014 |       -0.1727 |        0.1334 |
| C(year, Treatment(reference='2022'))[T.2020]                                                |       -0.0169 |      0.0597 |       -0.2838 |    0.7766 |       -0.134  |        0.1001 |
| C(year, Treatment(reference='2022'))[T.2021]                                                |        0.4785 |      0.2377 |        2.013  |    0.0441 |        0.0126 |        0.9445 |
| C(year, Treatment(reference='2022'))[T.2023]                                                |       -0.0084 |      0.0515 |       -0.1631 |    0.8704 |       -0.1093 |        0.0925 |
| C(year, Treatment(reference='2022'))[T.2024]                                                |        0.0179 |      0.0716 |        0.25   |    0.8026 |       -0.1225 |        0.1583 |
| C(year, Treatment(reference='2022'))[T.2025]                                                |        0.1921 |      0.0914 |        2.102  |    0.0356 |        0.013  |        0.3711 |
| C(year, Treatment(reference='2022'))[T.2026]                                                |        0.3249 |      0.0983 |        3.3049 |    0.0009 |        0.1322 |        0.5176 |
| C(region, Treatment(reference='North America'))[T.Africa]                                   |        0.3987 |      0.2178 |        1.8309 |    0.0671 |       -0.0281 |        0.8255 |
| C(region, Treatment(reference='North America'))[T.Asia-Pacific]                             |        0.4934 |      0.0606 |        8.139  |    0      |        0.3746 |        0.6122 |
| C(region, Treatment(reference='North America'))[T.Europe]                                   |        0.1279 |      0.0673 |        1.8995 |    0.0575 |       -0.0041 |        0.2598 |
| C(region, Treatment(reference='North America'))[T.Latin America]                            |        0.3746 |      0.1039 |        3.6036 |    0.0003 |        0.1709 |        0.5783 |
| C(region, Treatment(reference='North America'))[T.Middle East]                              |       -0.416  |      0.0886 |       -4.6957 |    0      |       -0.5897 |       -0.2424 |
| C(region, Treatment(reference='North America'))[T.Other / International]                    |        0.082  |      0.3113 |        0.2635 |    0.7921 |       -0.5281 |        0.6922 |
| funding_log                                                                                 |        0.1415 |      0.0209 |        6.7569 |    0      |        0.1004 |        0.1825 |

## Model 2: Layoff Intensity (Percentage Workforce Laid Off)
**Sample Size (N):** 2,556 | **R²:** 0.3145 | **Adj R²:** 0.3061 | **F-Stat:** 32.94 (p = 2.9899e-161)
**Standard Errors:** HC3 (MacKinnon and White heteroscedasticity-consistent)

|                                                                                             |   Coefficient |   Robust_SE |   t_statistic |   p_value |   CI_Lower_95 |   CI_Upper_95 |
|:--------------------------------------------------------------------------------------------|--------------:|------------:|--------------:|----------:|--------------:|--------------:|
| Intercept                                                                                   |        0.8934 |      0.0327 |       27.3237 |    0      |        0.8293 |        0.9575 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Acquired / Subsidiary]          |       -0.4261 |      0.0416 |      -10.2326 |    0      |       -0.5077 |       -0.3445 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Early Venture (Series A)]       |       -0.2909 |      0.0388 |       -7.4987 |    0      |       -0.3669 |       -0.2149 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Expansion Stage (Series B)]     |       -0.3655 |      0.0347 |      -10.547  |    0      |       -0.4334 |       -0.2976 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Growth Stage (Series E+)]       |       -0.4793 |      0.0363 |      -13.1967 |    0      |       -0.5505 |       -0.4081 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Late Stage (Series C-D)]        |       -0.448  |      0.0341 |      -13.1523 |    0      |       -0.5148 |       -0.3813 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Private Equity Owned]           |       -0.4359 |      0.0513 |       -8.4945 |    0      |       -0.5365 |       -0.3353 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Public (Post-IPO)]              |       -0.5105 |      0.0348 |      -14.6758 |    0      |       -0.5787 |       -0.4423 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Unspecified / Private]          |       -0.3893 |      0.0366 |      -10.6292 |    0      |       -0.4611 |       -0.3175 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.EdTech & Learning]            |       -0.0273 |      0.0304 |       -0.8956 |    0.3705 |       -0.0869 |        0.0324 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Enterprise & Infrastructure]  |       -0.0969 |      0.0182 |       -5.3251 |    0      |       -0.1325 |       -0.0612 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Fintech & Financial Services] |       -0.0441 |      0.0166 |       -2.6636 |    0.0077 |       -0.0766 |       -0.0117 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Hardware & Manufacturing]     |       -0.0062 |      0.0447 |       -0.1377 |    0.8904 |       -0.0937 |        0.0814 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Healthcare & BioTech]         |        0.0475 |      0.0227 |        2.0907 |    0.0366 |        0.003  |        0.0921 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Marketing & Media]            |       -0.1037 |      0.0194 |       -5.3423 |    0      |       -0.1417 |       -0.0657 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Other / Diversified]          |       -0.0596 |      0.0178 |       -3.3382 |    0.0008 |       -0.0946 |       -0.0246 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Professional Services]        |       -0.1309 |      0.0232 |       -5.6488 |    0      |       -0.1764 |       -0.0855 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Real Estate & PropTech]       |        0.042  |      0.0305 |        1.3767 |    0.1686 |       -0.0178 |        0.1017 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Travel & Transportation]      |        0.0325 |      0.0206 |        1.5761 |    0.115  |       -0.0079 |        0.0728 |
| C(year, Treatment(reference='2022'))[T.2020]                                                |        0.0189 |      0.0152 |        1.2425 |    0.214  |       -0.0109 |        0.0486 |
| C(year, Treatment(reference='2022'))[T.2021]                                                |        0.3346 |      0.0975 |        3.4308 |    0.0006 |        0.1434 |        0.5257 |
| C(year, Treatment(reference='2022'))[T.2023]                                                |        0.0427 |      0.0122 |        3.5111 |    0.0004 |        0.0189 |        0.0666 |
| C(year, Treatment(reference='2022'))[T.2024]                                                |        0.0945 |      0.0178 |        5.3079 |    0      |        0.0596 |        0.1294 |
| C(year, Treatment(reference='2022'))[T.2025]                                                |        0.1223 |      0.0256 |        4.7829 |    0      |        0.0722 |        0.1725 |
| C(year, Treatment(reference='2022'))[T.2026]                                                |        0.0838 |      0.0214 |        3.9094 |    0.0001 |        0.0418 |        0.1258 |
| C(region, Treatment(reference='North America'))[T.Africa]                                   |       -0.0286 |      0.0586 |       -0.4874 |    0.626  |       -0.1434 |        0.0863 |
| C(region, Treatment(reference='North America'))[T.Asia-Pacific]                             |       -0.0191 |      0.0177 |       -1.0814 |    0.2795 |       -0.0538 |        0.0156 |
| C(region, Treatment(reference='North America'))[T.Europe]                                   |        0.0137 |      0.0178 |        0.7658 |    0.4438 |       -0.0213 |        0.0486 |
| C(region, Treatment(reference='North America'))[T.Latin America]                            |       -0.0986 |      0.0239 |       -4.1283 |    0      |       -0.1455 |       -0.0518 |
| C(region, Treatment(reference='North America'))[T.Middle East]                              |       -0.0204 |      0.0234 |       -0.8719 |    0.3833 |       -0.0664 |        0.0255 |
| C(region, Treatment(reference='North America'))[T.Other / International]                    |       -0.0245 |      0.0604 |       -0.4059 |    0.6848 |       -0.143  |        0.0939 |
| funding_log                                                                                 |       -0.0394 |      0.0043 |       -9.2185 |    0      |       -0.0478 |       -0.031  |

## Model 3: Theoretical Interaction (Funding Capitalization × Macroeconomic Regime)
**Sample Size (N):** 2,556 | **R²:** 0.3057 | **Adj R²:** 0.2988
|                                                                                                                                         |   Coefficient |   Robust_SE |   t_statistic |   p_value |   CI_Lower_95 |   CI_Upper_95 |
|:----------------------------------------------------------------------------------------------------------------------------------------|--------------:|------------:|--------------:|----------:|--------------:|--------------:|
| Intercept                                                                                                                               |        0.8357 |      0.0499 |       16.7414 |    0      |        0.7379 |        0.9336 |
| C(macro_regime, Treatment(reference='Phase 1: COVID Shock & Virtualization'))[T.Phase 2: Tech Overhiring & Peak Valuation]              |        0.022  |      0.0658 |        0.3339 |    0.7384 |       -0.107  |        0.151  |
| C(macro_regime, Treatment(reference='Phase 1: COVID Shock & Virtualization'))[T.Phase 3: Rate Hikes & Tech Contraction]                 |        0.0383 |      0.0513 |        0.746  |    0.4557 |       -0.0623 |        0.1389 |
| C(macro_regime, Treatment(reference='Phase 1: COVID Shock & Virtualization'))[T.Phase 4: AI Pivot & Structural Realignment]             |        0.2272 |      0.0546 |        4.1587 |    0      |        0.1201 |        0.3343 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Acquired / Subsidiary]                                                      |       -0.4166 |      0.0412 |      -10.1032 |    0      |       -0.4974 |       -0.3358 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Early Venture (Series A)]                                                   |       -0.2904 |      0.0384 |       -7.5656 |    0      |       -0.3656 |       -0.2151 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Expansion Stage (Series B)]                                                 |       -0.3662 |      0.0343 |      -10.6756 |    0      |       -0.4334 |       -0.2989 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Growth Stage (Series E+)]                                                   |       -0.4866 |      0.0359 |      -13.5726 |    0      |       -0.5569 |       -0.4164 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Late Stage (Series C-D)]                                                    |       -0.4543 |      0.0335 |      -13.5495 |    0      |       -0.52   |       -0.3886 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Private Equity Owned]                                                       |       -0.4478 |      0.0507 |       -8.8268 |    0      |       -0.5472 |       -0.3483 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Public (Post-IPO)]                                                          |       -0.5053 |      0.0345 |      -14.6505 |    0      |       -0.573  |       -0.4377 |
| C(stage_group, Treatment(reference='Early Stage (Seed)'))[T.Unspecified / Private]                                                      |       -0.3902 |      0.0363 |      -10.7625 |    0      |       -0.4613 |       -0.3192 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.EdTech & Learning]                                                        |       -0.017  |      0.0304 |       -0.5597 |    0.5757 |       -0.0765 |        0.0425 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Enterprise & Infrastructure]                                              |       -0.0887 |      0.0179 |       -4.9611 |    0      |       -0.1238 |       -0.0537 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Fintech & Financial Services]                                             |       -0.0443 |      0.0166 |       -2.668  |    0.0076 |       -0.0768 |       -0.0117 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Hardware & Manufacturing]                                                 |        0.0024 |      0.0434 |        0.0556 |    0.9556 |       -0.0827 |        0.0876 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Healthcare & BioTech]                                                     |        0.0473 |      0.0227 |        2.0811 |    0.0374 |        0.0028 |        0.0918 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Marketing & Media]                                                        |       -0.0992 |      0.0195 |       -5.0904 |    0      |       -0.1374 |       -0.061  |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Other / Diversified]                                                      |       -0.0535 |      0.0178 |       -3.0166 |    0.0026 |       -0.0883 |       -0.0188 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Professional Services]                                                    |       -0.126  |      0.0225 |       -5.611  |    0      |       -0.1701 |       -0.082  |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Real Estate & PropTech]                                                   |        0.0372 |      0.03   |        1.2419 |    0.2143 |       -0.0215 |        0.0959 |
| C(industry_group, Treatment(reference='Consumer & Retail'))[T.Travel & Transportation]                                                  |        0.0338 |      0.0208 |        1.6265 |    0.1039 |       -0.0069 |        0.0744 |
| funding_log                                                                                                                             |       -0.0207 |      0.0086 |       -2.4192 |    0.0156 |       -0.0375 |       -0.0039 |
| funding_log:C(macro_regime, Treatment(reference='Phase 1: COVID Shock & Virtualization'))[T.Phase 2: Tech Overhiring & Peak Valuation]  |       -0.015  |      0.0117 |       -1.2874 |    0.1979 |       -0.0379 |        0.0078 |
| funding_log:C(macro_regime, Treatment(reference='Phase 1: COVID Shock & Virtualization'))[T.Phase 3: Rate Hikes & Tech Contraction]     |       -0.0112 |      0.0096 |       -1.1718 |    0.2413 |       -0.0299 |        0.0075 |
| funding_log:C(macro_regime, Treatment(reference='Phase 1: COVID Shock & Virtualization'))[T.Phase 4: AI Pivot & Structural Realignment] |       -0.0335 |      0.0098 |       -3.4144 |    0.0006 |       -0.0528 |       -0.0143 |